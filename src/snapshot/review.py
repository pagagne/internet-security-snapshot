"""Monthly cohort draw over real data and the author's review list.

    python -m snapshot.review --cve data/raw/2026Q3/dry-run/cve/cve_records.parquet \
        --months 2026-07 2026-08 2026-09 --out review/2026Q3.csv

For each month: eligible CVEs (cohort_rules.yaml), one pick per slot by the seeded
random draw (snapshot.cohort). Slots a and b need no judgment. For slots c and d the
review list shows the top three in draw order: mark them in order until one is "yes";
rows after the first "yes" are ignored, so a "no" never needs a second round. Every
pick's fix date is pre-filled (snapshot.fixdates) with its source; the author confirms or
corrects it. Separately, every distinct AI-credit text in the
period is listed once for the T7 check.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd

from .classify import lab_name_only, product_category
from .cohort import draw_order
from .fixdates import prefill
from .autoaccept import auto_accept, spot_check
from .util import Quarter, load_config

BACKUPS = 3
CARRIED: dict[str, str] = {}   # credit texts carried over from earlier decisions (last run)
RETEST_N = 5                     # earlier author decisions shown again, unmarked, each quarter


def eligible(cve: pd.DataFrame, month: str) -> pd.DataFrame:
    el = load_config("cohort_rules.yaml")["eligibility"]
    d = cve.copy()
    d["date_published"] = pd.to_datetime(d["date_published"], utc=True, errors="coerce")
    sev = d["cvss_severity"].fillna("").str.upper()
    m = (d["state"] == "PUBLISHED") & (d["date_published"].dt.strftime("%Y-%m") == month) \
        & (d["date_published"].dt.day <= el["publish_day_max"]) \
        & ((d["cvss_base"] >= el["min_cvss_base"]) | (sev == "CRITICAL"))
    e = d[m].copy()
    e["slot"] = e["affected"].map(lambda a: product_category(list(a)))
    e["ai_candidate"] = e["ai_credit_terms"].map(lambda x: len(x) > 0)
    return e


def _links(r) -> list[str]:
    fix = list(r.get("fix_links", []) if r.get("fix_links") is not None else [])
    ref = list(r.get("ref_links", []) if r.get("ref_links") is not None else [])
    return (fix if len(fix) else ref)[:3]


def _links_all(r) -> list[str]:
    out = []
    for key in ("fix_links", "ref_links"):
        v = r.get(key)
        if v is not None:
            out += [u for u in list(v) if u not in out]
    return out


def _row(month, slot, rank, r, task, question):
    fix_date, fix_source = prefill(_links_all(r), str(r["date_published"]))
    return {
        "month": month, "slot": slot, "draw_rank": rank, "cve_id": r["cve_id"],
        "product": "; ".join(list(r["affected"])[:2]), "cvss": r["cvss_base"],
        "published": str(r["date_published"])[:10], "task": task, "question": question,
        "credit": " | ".join(list(r["credit_values"])[:3]),
        "links": " ".join(_links(r)),
        "answer": "", "patch_date": fix_date, "patch_source": fix_source, "notes": "",
    }


def month_rows(cve: pd.DataFrame, month: str) -> tuple[list[dict], dict]:
    e = eligible(cve, month)
    taken, rows, stats = set(), [], {"month": month}
    pools = {"a_edge": e[e.slot == "a_edge"], "b_web_collab": e[e.slot == "b_web_collab"],
             "c_other": e[e.slot == "c_other"], "d_ai_credited": e[e.ai_candidate]}
    for slot, pool in pools.items():
        stats[slot] = len(pool)
        order = [c for c in draw_order(month, slot, pool["cve_id"]) if c not in taken]
        if not order:
            rows.append({"month": month, "slot": slot, "draw_rank": "", "cve_id": "(empty)", "task": "none",
                         "question": "No eligible CVE this month; slot stays empty."})
            continue
        by_id = pool.set_index("cve_id")
        if slot in ("a_edge", "b_web_collab"):
            r = by_id.loc[order[0]].copy(); r["cve_id"] = order[0]
            rows.append(_row(month, slot, 1, r, "patch_date", "Find the vendor's fix date."))
            taken.add(order[0])
        else:
            q = ("Is this product reachable from the internet in normal use? If yes, also find the fix date."
                 if slot == "c_other" else
                 "Did an AI tool take part in finding this flaw (per the credit)? If yes, also find the fix date.")
            for i, cid in enumerate(order[:BACKUPS], 1):
                r = by_id.loc[cid].copy(); r["cve_id"] = cid
                rows.append(_row(month, slot, i, r, "yes_no_then_patch_date", q))
            taken.add(order[0])  # provisional; a "no" releases it to the next rank
    return rows, stats


def credit_rows(cve: pd.DataFrame, months: list[str], already: dict[str, str] | None = None) -> list[dict]:
    """One row per distinct AI-credit text. Texts already decided in an earlier scored
    batch (review/decisions.csv) are carried over and not asked again."""
    d = cve.copy()
    d["m"] = pd.to_datetime(d["date_published"], utc=True, errors="coerce").dt.strftime("%Y-%m")
    d = d[d["m"].isin(months) & d["ai_credit_terms"].map(lambda x: len(x) > 0)]
    groups = {}
    for _, r in d.iterrows():
        key = " | ".join(list(r["credit_values"]))
        g = groups.setdefault(key, {"n": 0, "terms": list(r["ai_credit_terms"]), "example": r["cve_id"], "ids": [], "types": set()})
        g["types"].update(list(r["credit_types"]) if r.get("credit_types") is not None else [])
        g["n"] += 1
        if len(g["ids"]) < 5:
            g["ids"].append(r["cve_id"])
    already = already or {}
    CARRIED.clear()
    CARRIED.update({k: already[k[:300]] for k in groups if k[:300] in already})
    groups = {k: g for k, g in groups.items() if k[:300] not in already}
    rules = {k: auto_accept(k, g["types"]) for k, g in groups.items()}
    spots = spot_check([k for k, r in rules.items() if r], seed=f"spot|{','.join(months)}")
    return [{"month": ",".join(months), "slot": "T7", "draw_rank": "", "cve_id": g["example"],
             "task": ("auto_accept" if rules[k] and k not in spots else "ai_credit"),
             "auto_rule": rules[k] or "", "spot_check": k in spots,
             "question": f"Does this credit say an AI tool took part? Applies to {g['n']} CVE(s)."
             + (" Lab name only: needs an explicit AI-tool mention." if lab_name_only(g["terms"]) else ""),
             "credit": k[:300], "terms": "; ".join(g["terms"]), "examples": " ".join(g["ids"]),
             "answer": "", "notes": ""} for k, g in sorted(groups.items(), key=lambda x: -x[1]["n"])]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cve", required=True, type=Path)
    ap.add_argument("--months", nargs="+", help="YYYY-MM months (or use --quarter)")
    ap.add_argument("--quarter", help="e.g. 2026Q3: its three months")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--decisions", type=Path, default=Path("review/decisions.csv"),
                    help="earlier scored decisions; decided credit texts are not asked again")
    a = ap.parse_args(argv)
    if a.quarter and not a.months:
        q = Quarter.parse(a.quarter)
        a.months = [f"{q.start.year}-{q.start.month + i:02d}" for i in range(3)]
    if not a.months:
        ap.error("give --months or --quarter")
    cve = pd.read_parquet(a.cve)
    rows, stats = [], []
    for m in a.months:
        r, s = month_rows(cve, m)
        rows += r; stats.append(s)
    from .decisions import decided_credits, no_fix_rechecks, retest_sample
    for r in no_fix_rechecks(a.decisions, a.months[-1]):
        rows.append({"month": r["month"], "slot": r["slot"], "draw_rank": r["rank"], "cve_id": r["cve_id"],
                     "task": "patch_date", "question": f"Re-check: no fix found on {r['checked_on']}. Has the vendor released one?",
                     "patch_date": "", "patch_source": f"no fix yet as of {r['checked_on']}"})
    rows += credit_rows(cve, a.months, decided_credits(a.decisions))
    rows += [{"month": ",".join(a.months), "slot": "T7", "draw_rank": "", "cve_id": "", "task": "ai_credit",
              "retest": True, "auto_rule": "", "spot_check": False,
              "question": "Does this credit say an AI tool took part?", "credit": k, "terms": "", "examples": ""}
             for k in retest_sample(a.decisions, RETEST_N, seed=",".join(a.months))]
    if CARRIED:
        print(f"{len(CARRIED)} credit texts carried over from earlier decisions")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["month", "slot", "draw_rank", "cve_id", "product", "cvss", "published", "task", "question",
              "credit", "terms", "examples", "auto_rule", "spot_check", "retest", "links", "answer", "patch_date", "patch_source", "notes"]
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print(pd.DataFrame(stats).to_string(index=False))
    print(pd.DataFrame(rows)["task"].value_counts().to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
