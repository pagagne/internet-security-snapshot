"""Second-coder check of the author's hand decisions (decision item 20;
docs/STATISTICAL_REVIEW_2026-10-24.md, point 7).

Re-showing the author's own decisions measures consistency; only a second, independent
coder can show a systematic bias. Each quarter a seeded sample of 20 of the author's
decisions goes to a second coder, blinded (no answers, only what the author saw).

    # after the author's hand check: write the blinded list for the second coder
    python -m snapshot.agreement sample --batch 2027Q1 --out review/second-2027Q1.csv

    # the second coder fills the answer columns in that file (or answers the same items in
    # the Hand Check app as a batch whose metadata names them: coder=<name>); then
    python -m snapshot.agreement score --batch 2027Q1 --second review/second-2027Q1.csv

The weights go to a separate file (review/second-2027Q1.weights.csv), which the second
coder is not given.

Sampling: easy cases agree almost always, so a purely random sample says little. The sample
takes up to half its items from uncertain cases (author marked unsure; fix date corrected,
unknown or "no fix yet"; pre-fill assumed or flagged) and the rest from routine ones, and
records each item's weight (stratum size / items drawn from it) so overall agreement is
weighted back to the whole batch.

Scores: yes/no checks (AI credit, slot c internet-facing) as raw agreement, Cohen's kappa,
Gwet's AC1 and agreement on Yes and on No separately (kappa understates agreement when one
answer dominates); fix dates as the share within one day and the median difference in days.
Nothing here feeds a label or the cohort; second-coder answers never enter
review/decisions.csv.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import statistics
from pathlib import Path

from .decisions import is_retest

N_SECOND = 20
YES_NO = ("credit", "slot_c")
BLIND_FIELDS = ["item_id", "kind", "month", "slot", "cve_id", "credit", "prefill_date", "prefill_source",
                "answer", "fix_date", "fix_status", "note"]
WEIGHT_FIELDS = ["item_id", "stratum", "weight"]   # kept in a separate file: the stratum would hint at the author's answer


def _uncertain(r: dict) -> bool:
    src = (r.get("prefill_source") or "").lower()
    return (str(r.get("unsure", "")).lower() == "true"
            or r.get("fix_status") in ("corrected", "unknown", "no_fix_yet")
            or "assumed" in src or "may ship later" in src or "changed later" in src or "not stated" in src)


def sample(decisions_csv: Path, batch: str, n: int = N_SECOND, seed: str | None = None) -> list[dict]:
    """Blinded, weighted sample of the author's decisions in one batch."""
    with open(decisions_csv, newline="") as f:
        rows = [r for r in csv.DictReader(f)
                if r["batch"] == batch and r.get("decided_by", "author") == "author" and not is_retest(r)
                and ((r["kind"] in YES_NO and r["decision"]) or (r["kind"] == "fix" and r.get("fix_status")))]
    seed = seed or f"second|{batch}"
    key = lambda r: hashlib.sha256(f"{seed}|{r['item_id']}".encode()).hexdigest()
    strata = {"uncertain": sorted([r for r in rows if _uncertain(r)], key=key),
              "routine": sorted([r for r in rows if not _uncertain(r)], key=key)}
    take_u = min(len(strata["uncertain"]), n // 2)
    take_r = min(len(strata["routine"]), n - take_u)
    take_u = min(len(strata["uncertain"]), n - take_r)   # top up if routine ran short
    out = []
    for name, k in (("uncertain", take_u), ("routine", take_r)):
        pool = strata[name]
        for r in pool[:k]:
            out.append({f: r.get(f, "") for f in ("item_id", "kind", "month", "slot", "cve_id", "credit",
                                                  "prefill_date", "prefill_source")}
                       | {"stratum": name, "weight": round(len(pool) / k, 4), "answer": "", "fix_date": "",
                          "fix_status": "", "note": ""})
    return out


def _yes_no_stats(pairs: list[tuple[str, str, float]]) -> dict:
    """pairs: (author, second, weight) with answers 'yes'/'no'."""
    W = sum(w for *_, w in pairs)
    if not W:
        return {"n": 0}
    p = lambda cond: sum(w for a, b, w in pairs if cond(a, b)) / W
    po = p(lambda a, b: a == b)
    pa, pb = p(lambda a, b: a == "yes"), p(lambda a, b: b == "yes")
    pe_k = pa * pb + (1 - pa) * (1 - pb)
    pi = (pa + pb) / 2
    pe_g = 2 * pi * (1 - pi)
    yy, nn = p(lambda a, b: a == b == "yes"), p(lambda a, b: a == b == "no")
    return {
        "n": len(pairs),
        "raw_agreement": round(po, 3),
        "cohen_kappa": round((po - pe_k) / (1 - pe_k), 3) if pe_k < 1 else None,
        "gwet_ac1": round((po - pe_g) / (1 - pe_g), 3) if pe_g < 1 else None,
        "agreement_on_yes": round(2 * yy / (pa + pb), 3) if pa + pb else None,
        "agreement_on_no": round(2 * nn / ((1 - pa) + (1 - pb)), 3) if (1 - pa) + (1 - pb) else None,
    }


def score(decisions_csv: Path, batch: str, second: list[dict]) -> dict:
    """Agreement between the author's decisions in `batch` and a second coder's answers."""
    import datetime as dt
    with open(decisions_csv, newline="") as f:
        author = {r["item_id"]: r for r in csv.DictReader(f)
                  if r["batch"] == batch and r.get("decided_by", "author") == "author"}
    yn, fix_days, fix_status = [], [], []
    for s in second:
        a = author.get(s["item_id"])
        if not a:
            continue
        w = float(s.get("weight") or 1)
        if s["kind"] in YES_NO and s.get("answer") in ("yes", "no"):
            yn.append((a["decision"], s["answer"], w))
        elif s["kind"] == "fix" and s.get("fix_status"):
            fix_status.append((a.get("fix_status") == s["fix_status"], w))
            if a.get("fix_date") and s.get("fix_date"):
                try:
                    d = abs((dt.date.fromisoformat(a["fix_date"][:10]) - dt.date.fromisoformat(s["fix_date"][:10])).days)
                    fix_days.append((d, w))
                except ValueError:
                    pass
    Wd = sum(w for _, w in fix_days)
    Ws = sum(w for _, w in fix_status)
    return {
        "yes_no": _yes_no_stats(yn),
        "fix_dates": {
            "n_status": len(fix_status),
            "status_agreement": round(sum(w for ok, w in fix_status if ok) / Ws, 3) if Ws else None,
            "n_dated": len(fix_days),
            "share_within_1_day": round(sum(w for d, w in fix_days if d <= 1) / Wd, 3) if Wd else None,
            "median_difference_days": statistics.median(d for d, _ in fix_days) if fix_days else None,
        },
    }


def weights_path(sheet: Path) -> Path:
    return sheet.with_name(sheet.stem + ".weights.csv")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("sample"); s1.add_argument("--batch", required=True); s1.add_argument("--out", type=Path, required=True)
    s2 = sub.add_parser("score"); s2.add_argument("--batch", required=True); s2.add_argument("--second", type=Path, required=True)
    for s in (s1, s2):
        s.add_argument("--decisions", type=Path, default=Path("review/decisions.csv"))
    a = ap.parse_args(argv)
    if a.cmd == "sample":
        rows = sample(a.decisions, a.batch)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=BLIND_FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
        with open(weights_path(a.out), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=WEIGHT_FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
        print(f"{len(rows)} items for the second coder -> {a.out} (weights: {weights_path(a.out)}, not for the coder)")
    else:
        import json
        second = list(csv.DictReader(open(a.second, newline="")))
        wp = weights_path(a.second)
        if wp.exists():
            wts = {r["item_id"]: r["weight"] for r in csv.DictReader(open(wp, newline=""))}
            for r in second:
                r["weight"] = wts.get(r["item_id"], 1)
        print(json.dumps(score(a.decisions, a.batch, second), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
