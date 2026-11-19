"""Turn snapshot.review lists into Hand Check app items (19 Nov 2026).

The app (private artifact "Snapshot Hand Check") reads items from its database at
batches/<batch>/items, ordered by "order". Kinds: "credit" (an AI-credit text), "fix" (a fix date
to confirm: slots a and b, and race-list flaws), "slot_c" / "slot_d" (yes or no, then a fix date;
backups shown only after a "no"), "empty" (a slot with no eligible CVE; nothing to answer).
Race-list flaws whose fix date came from a source the rules accept without a check are left out
(they are not hand-checked, HAND_CHECK.md); every flagged one is included (12 Nov 2026 decision).

    python -m snapshot.handcheck review-2025Q4.csv ... --out items.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .classify import lab_name_only

SLOT_KIND = {"a_edge": "fix", "b_web_collab": "fix", "c_other": "slot_c", "d_ai_credited": "slot_d"}


def _split(s: str) -> list[str]:
    return [x for x in str(s or "").split() if x]


def items(frames: list[pd.DataFrame]) -> tuple[list[dict], dict]:
    out, seen_credit, skipped_race = [], set(), 0
    for d in frames:
        d = d.fillna("")
        for r in d.to_dict("records"):
            task, slot = r["task"], r["slot"]
            base = {"month": r["month"], "cve_id": r["cve_id"], "product": r["product"], "cvss": r["cvss"],
                    "published": r["published"], "credit": r["credit"], "links": _split(r["links"])[:3],
                    "prefill_date": r["patch_date"], "prefill_source": r["patch_source"]}
            if task in ("ai_credit", "auto_accept"):
                if r["credit"] in seen_credit:      # the same text in two quarters is asked once
                    continue
                seen_credit.add(r["credit"])
                ex = _split(r["examples"])
                covers = int(pd.Series(r["question"]).str.extract(r"Applies to (\d+)")[0].fillna(len(ex)).iloc[0])
                terms = [t.strip() for t in r["terms"].split(";") if t.strip()]
                out.append({"kind": "credit", "credit": r["credit"], "cve_id": ex[0] if ex else r["cve_id"],
                            "examples": ex[:5], "covers": covers, "terms": terms,
                            "auto_rule": r["auto_rule"], "spot_check": r["spot_check"] == "True",
                            "lab_only": bool(lab_name_only(terms))})
            elif task == "none":
                out.append({**base, "kind": "empty", "slot": slot, "rank": 1, "group": f"{r['month']}|{slot}"})
            elif slot == "race":
                if "Check this one." not in r["question"]:
                    skipped_race += 1
                    continue
                out.append({**base, "kind": "fix", "slot": "race_kev", "rank": 1, "group": f"race|{r['cve_id']}"})
            elif slot in SLOT_KIND:
                rank = int(r["draw_rank"] or 1)
                out.append({**base, "kind": SLOT_KIND[slot], "slot": slot, "rank": rank, "group": f"{r['month']}|{slot}"})
    # cohort first (month, slot, rank), then race, then credits, so a session can stop at a clean break
    key = {"fix": 0, "slot_c": 0, "slot_d": 0, "empty": 0}
    def sort_key(it):
        if it["kind"] == "credit":
            return (2, "", "", 0)
        if it.get("slot") == "race_kev":
            return (1, it["month"], it["cve_id"], 0)
        return (key[it["kind"]], it["month"], it["slot"], it["rank"])
    out.sort(key=sort_key)
    for i, it in enumerate(out, 1):
        it["order"] = i
    stats = {"items": len(out), "race_skipped_no_check_needed": skipped_race,
             **pd.Series([("race" if it.get("slot") == "race_kev" else it["kind"]) for it in out]).value_counts().to_dict()}
    return out, stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="+", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    its, stats = items([pd.read_csv(p, dtype=str) for p in a.csv])
    a.out.write_text(json.dumps(its, indent=1))
    print(json.dumps(stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
