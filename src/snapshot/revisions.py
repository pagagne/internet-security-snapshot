"""Revision drift between two pulls (author, 23 Nov 2026).

The quality report already flags format drift (a field gone or empty) and volume drift (row
counts). This module looks for the third kind: sources quietly rewriting records they already
published, such as a changed CISA KEV date, a changed NVD published date or status, or an EPSS
score for a past day that is no longer the same. For the race measures a rewritten date moves
the clock, so the 21 Dec 2026 decision session needs to know how often it happens.

It matches the records two bundles share (same key) and counts, field by field, how many
changed; records present in the older pull but missing from the newer one are counted as
removed. Counts and a few example identifiers only; nothing is scored. Run it on two bundles
of the same quarter, for example run zero (23 Nov) against the 1 Dec dry run:

    python -m snapshot.revisions OLD_BUNDLE NEW_BUNDLE --out DIR

VulnCheck lives in the private part of a bundle: pass --private-old/--private-new to include it,
and keep that output private.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

# file inside a bundle -> the columns that identify one record
KEYS = {
    "kev/kev_entries.parquet": ["cve_id"],
    "cve/cve_records.parquet": ["cve_id"],
    "nvd/nvd_cves.parquet": ["cve_id"],
    "epss/epss_scores.parquet": ["cve", "date"],
}
PRIVATE_KEYS = {"vulncheck/vulncheck_kev.parquet": ["cve_id"]}
# fields that move the race clock or the cohort; listed first in the report
WATCH = {"date_added", "date_published", "nvd_published", "nvd_status", "state", "epss",
         "dueDate", "due_date", "exploited_date", "date_exploited"}
EXAMPLES = 5


def _norm(v):
    """Comparable form: lists and arrays to tuples, missing values to None."""
    if v is None:
        return None
    if hasattr(v, "tolist") and not isinstance(v, (str, bytes)):
        v = v.tolist()
    if isinstance(v, (list, tuple)):
        return tuple(_norm(x) for x in v)
    if isinstance(v, dict):
        return tuple(sorted((k, _norm(x)) for k, x in v.items()))
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, pd.Timestamp):
        return v.isoformat()
    return v


def compare_table(old: pd.DataFrame, new: pd.DataFrame, key: list[str]) -> dict:
    old = old.drop_duplicates(subset=key, keep="last").set_index(key)
    new = new.drop_duplicates(subset=key, keep="last").set_index(key)
    common = old.index.intersection(new.index)
    removed = old.index.difference(new.index)
    added = new.index.difference(old.index)
    cols = [c for c in old.columns if c in new.columns]
    fields = {}
    for c in cols:
        a = [_norm(v) for v in old.loc[common, c].tolist()]
        b = [_norm(v) for v in new.loc[common, c].tolist()]
        changed = pd.Series([x != y for x, y in zip(a, b)], dtype=bool)
        n = int(changed.sum())
        if n:
            ex = [str(i if not isinstance(i, tuple) else "/".join(map(str, i))) for i in common[changed.values][:EXAMPLES]]
            fields[c] = {"changed": n, "share": round(n / len(common), 4) if len(common) else 0.0,
                         "examples": ex, "watched": c in WATCH}
    return {"old_rows": len(old), "new_rows": len(new), "shared": len(common),
            "removed": len(removed), "added": len(added),
            "removed_examples": [str(i) for i in removed[:EXAMPLES]],
            "fields": dict(sorted(fields.items(), key=lambda kv: (not kv[1]["watched"], -kv[1]["changed"])))}


def compare(old_bundle: Path, new_bundle: Path, keys: dict = KEYS) -> dict:
    out = {}
    for rel, key in keys.items():
        po, pn = old_bundle / rel, new_bundle / rel
        if not (po.exists() and pn.exists()):
            out[rel] = {"skipped": "missing in " + ("both" if not po.exists() and not pn.exists() else "old" if not po.exists() else "new")}
            continue
        out[rel] = compare_table(pd.read_parquet(po), pd.read_parquet(pn), key)
    return out


def report(result: dict, old_name: str, new_name: str) -> str:
    L = [f"# Revision drift: {old_name} -> {new_name}", "",
         "Records both pulls share, compared field by field. Removed = in the older pull, gone from",
         "the newer. Watched fields (dates and statuses that move the race clock or the cohort) first.", ""]
    for rel, r in result.items():
        L.append(f"## {rel}")
        if "skipped" in r:
            L += [f"- skipped: {r['skipped']}", ""]
            continue
        L.append(f"- rows {r['old_rows']:,} -> {r['new_rows']:,}; shared {r['shared']:,}; added {r['added']:,}; removed {r['removed']:,}"
                 + (f" (e.g. {', '.join(r['removed_examples'])})" if r["removed"] else ""))
        if not r["fields"]:
            L.append("- no shared record changed")
        for c, f in r["fields"].items():
            L.append(f"- {'**' if f['watched'] else ''}{c}{'**' if f['watched'] else ''}: {f['changed']:,} changed "
                     f"({f['share']:.2%} of shared), e.g. {', '.join(f['examples'])}")
        L.append("")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("old", type=Path)
    ap.add_argument("new", type=Path)
    ap.add_argument("--private-old", type=Path)
    ap.add_argument("--private-new", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    res = compare(a.old, a.new)
    if a.private_old and a.private_new:
        res.update(compare(a.private_old, a.private_new, PRIVATE_KEYS))
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "revisions.json").write_text(json.dumps(res, indent=1, default=str))
    (a.out / "revisions.md").write_text(report(res, a.old.name, a.new.name))
    print(report(res, a.old.name, a.new.name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
