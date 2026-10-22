"""Record the author's Hand Check answers in the repository.

Input: a folder exported from the Hand Check app's database (one JSON file per document,
as written by Claude's ArtifactData read with out_dir):
    <export>/batches/<batch>/items/<id>.json
    <export>/batches/<batch>/answers/<id>.json
    <export>/batches/<batch>.json            (batch metadata; optional)

Output:
- scored batches  -> review/decisions.csv (one row per answered item, upserted by batch+item)
- practice batches -> review/practice/<batch>.csv (never read by the evaluation)

    python -m snapshot.decisions <export> --batch practice-2026Q3

Rows record what the author decided, never what Claude suggested. The evaluation reads
only review/decisions.csv.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path

FIELDS = ["batch", "item_id", "decided_by", "kind", "month", "slot", "rank", "cve_id", "credit", "terms",
          "decision", "unsure", "bulk", "fix_date", "fix_status", "prefill_date", "prefill_source",
          "seconds", "note", "answered_at", "recorded_at"]


def _doc(path: Path) -> dict:
    d = json.loads(path.read_text())
    return d.get("data", d) if isinstance(d, dict) else {}


def load(export: Path, batch: str) -> tuple[dict, list[dict]]:
    base = export / "batches" / batch
    meta_file = export / "batches" / f"{batch}.json"
    meta = _doc(meta_file) if meta_file.exists() else {}
    items = {p.stem: _doc(p) for p in (base / "items").glob("*.json")}
    answers = {p.stem: _doc(p) for p in (base / "answers").glob("*.json")} if (base / "answers").exists() else {}
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    rows = []
    for iid, a in sorted(answers.items()):
        it = items.get(iid, {})
        rows.append({
            "batch": batch, "item_id": iid, "decided_by": "author", "kind": it.get("kind", a.get("kind", "")),
            "month": it.get("month", ""), "slot": it.get("slot", ""), "rank": it.get("rank", ""),
            "cve_id": it.get("cve_id", a.get("cve_id", "")), "credit": it.get("credit", ""),
            "terms": "; ".join(it.get("terms", []) or []),
            "decision": a.get("decision", ""), "unsure": bool(a.get("unsure")), "bulk": bool(a.get("bulk")),
            "fix_date": a.get("fix_date", ""), "fix_status": a.get("fix_status", ""),
            "prefill_date": it.get("prefill_date", ""), "prefill_source": it.get("prefill_source", ""),
            "seconds": a.get("seconds", 0), "note": a.get("note", ""), "answered_at": a.get("at", ""),
            "recorded_at": now,
        })
    return meta, rows


def auto_rows(review_csv: Path, batch: str) -> list[dict]:
    """Rows for credits accepted by a rule (config/ai_credit_auto_accept.yaml), not shown to the author."""
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    out = []
    with open(review_csv, newline="") as f:
        for i, r in enumerate(csv.DictReader(f), 1):
            if r.get("task") == "auto_accept":
                out.append({"batch": batch, "item_id": f"auto{i:04d}", "decided_by": f"rule:{r['auto_rule']}",
                            "kind": "credit", "cve_id": r["cve_id"], "credit": r["credit"], "terms": r.get("terms", ""),
                            "decision": "yes", "unsure": False, "bulk": False, "seconds": 0, "recorded_at": now})
    return out


def suspended_rules(rows: list[dict], items: dict) -> set[str]:
    """Rules whose spot-checked credits the author answered 'no' to."""
    return {items[r["item_id"]].get("auto_rule") for r in rows
            if items.get(r["item_id"], {}).get("spot_check") and r["decision"] == "no"} - {None, ""}


def write(rows: list[dict], out: Path) -> int:
    """Upsert rows into out, keyed by (batch, item_id)."""
    existing = {}
    if out.exists():
        with open(out, newline="") as f:
            for r in csv.DictReader(f):
                existing[(r["batch"], r["item_id"])] = r
    for r in rows:
        existing[(r["batch"], r["item_id"])] = r
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(existing.values(), key=lambda r: (r["batch"], r["item_id"])))
    return len(existing)


def decided_credits(decisions_csv: Path) -> dict[str, str]:
    """Credit text -> latest decision, from scored batches only (for carry-over)."""
    out: dict[str, tuple[str, str]] = {}
    if not decisions_csv.exists():
        return {}
    with open(decisions_csv, newline="") as f:
        for r in csv.DictReader(f):
            if r["kind"] == "credit" and r["decision"] and r["credit"]:
                prev = out.get(r["credit"])
                if not prev or r["answered_at"] > prev[1]:
                    out[r["credit"]] = (r["decision"], r["answered_at"])
    return {k: v[0] for k, v in out.items()}


def retest_sample(decisions_csv: Path, n: int, seed: str) -> list[str]:
    """Seeded sample of credit texts the author decided before, shown again unmarked."""
    import hashlib
    if not decisions_csv.exists():
        return []
    with open(decisions_csv, newline="") as f:
        keys = sorted({r["credit"] for r in csv.DictReader(f)
                       if r["kind"] == "credit" and r.get("decided_by", "author") == "author" and r["credit"] and r["decision"]})
    ranked = sorted(keys, key=lambda k: hashlib.sha256(f"retest|{seed}|{k}".encode()).hexdigest())
    return ranked[:n]


def consistency(decisions_csv: Path) -> dict:
    """Share of re-shown credit texts the author answered the same way as before."""
    if not decisions_csv.exists():
        return {"pairs": 0, "same": 0, "rate": None}
    by_text: dict[str, list[tuple[str, str]]] = {}
    with open(decisions_csv, newline="") as f:
        for r in csv.DictReader(f):
            if r["kind"] == "credit" and r.get("decided_by", "author") == "author" and r["decision"]:
                by_text.setdefault(r["credit"], []).append((r["answered_at"], r["decision"]))
    pairs = same = 0
    for answers in by_text.values():
        answers.sort()
        for (_, a), (_, b) in zip(answers, answers[1:]):
            pairs += 1
            same += a == b
    return {"pairs": pairs, "same": same, "rate": round(same / pairs, 3) if pairs else None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--review-csv", type=Path, help="the batch's review list, to record auto-accepted credits")
    a = ap.parse_args(argv)
    meta, rows = load(a.export, a.batch)
    items = {p.stem: _doc(p) for p in (a.export / "batches" / a.batch / "items").glob("*.json")}
    bad = suspended_rules(rows, items)
    if bad:
        print(f"WARNING: author rejected spot-checked credits for rule(s) {sorted(bad)}: suspend and review them")
    if a.review_csv:
        rows += auto_rows(a.review_csv, a.batch)
    practice = bool(meta.get("practice")) or a.batch.startswith("practice-")
    out = a.repo / ("review/practice" if practice else "review") / (f"{a.batch}.csv" if practice else "decisions.csv")
    total = write(rows, out)
    secs = sum(float(r["seconds"] or 0) for r in rows)
    print(f"{len(rows)} answers from {a.batch} -> {out} ({total} rows in file); review time {secs / 60:.0f} min"
          + (" [practice: not used by the evaluation]" if practice else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
