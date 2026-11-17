"""Checks on the X25 AI-tool sweeps (author's decisions, 5 Nov 2026; built 17 Nov 2026, issue #70).

After comparing the sweeps with a published audit of an agent-skill registry, the author asked for
five checks, all made without downloading or running any code:

1. Red flags in READMEs already read: encoded payloads, install lines that pipe a download into a
   shell, antivirus or OS-protection bypass, password-protected archives, oversized repositories.
2. A mislabel sample: about fifty items drawn reproducibly from a sweep, for a hand check of their
   labels, so an error rate can be published.
3. Copy and burst flags: renamed clones (the same description under different names), bursts of
   projects from one new account (usernames never published), and star bursts. Item counts are the
   headline; stars are context.
4. Searches split by creation date, so no query hits GitHub's 1,000-result cap
   (`github_tools.search_all`).
5. Anything else found along the way: listed in the 23 Nov proposal.

A flag is a reason to look, not a verdict: security tools legitimately discuss evasion, and many
honest projects install with a one-line script. Flags are reported as counts; the flagged items stay
in the private outputs.
"""
from __future__ import annotations

import datetime as dt
import random
import re
from collections import defaultdict

# 1. README red flags ---------------------------------------------------------------------------
RED_FLAGS = {
    "encoded payload": re.compile(
        r"[A-Za-z0-9+/]{300,}={0,2}"                                   # a long base64 blob
        r"|\bbase64\s+(-d|--decode)\b|frombase64string|\bpowershell(\.exe)?\s+-e(nc(odedcommand)?)?\s",
        re.I),
    "download piped into a shell": re.compile(
        r"\b(curl|wget)\b[^\n|]{0,300}\|\s*(sudo\s+)?(ba|z)?sh\b"
        r"|\b(iwr|irm|invoke-webrequest|invoke-restmethod)\b[^\n]{0,300}\|\s*(iex|invoke-expression)\b"
        r"|\biex\s*\(\s*(new-object\s+net\.webclient|iwr|irm)", re.I),
    "antivirus or OS-protection bypass": re.compile(
        r"\b(disable|turn off|deactivate)\s+(windows\s+)?(defender|antivirus|real-?time protection|smartscreen|gatekeeper)"
        r"|set-mppreference|add-mppreference\s+-exclusion|spctl\s+--master-disable|xattr\s+-d\s+com\.apple\.quarantine"
        r"|\b(add|create)\s+an?\s+(antivirus|defender)\s+exclusion|\bbypass\s+(amsi|edr|antivirus|defender|smartscreen)\b",
        re.I),
    "password-protected archive": re.compile(
        r"\b(zip|rar|7z|archive)\b[^\n]{0,80}\b(password|passcode|pass)\s*[:=]"
        r"|\b(password|passcode)\s*(for|to)\s+(the\s+)?(zip|rar|7z|archive)\b|\barchive password\b", re.I),
}
OVERSIZED_KB = 500_000   # a repository over about 500 MB, from the search result's size field


def red_flags(readme: str, size_kb: int | None = None) -> list[str]:
    """Names of the red flags found in a README (and the repository size)."""
    text = readme or ""
    out = [name for name, rx in RED_FLAGS.items() if rx.search(text)]
    if size_kb and size_kb > OVERSIZED_KB:
        out.append("oversized repository")
    return out


# 2. Mislabel sample ----------------------------------------------------------------------------
SAMPLE_COLUMNS = ["sample_id", "full_name", "url", "description", "types", "group", "ai_use", "labs",
                  "weights", "toolkits", "targets", "readme_read",
                  "check_types_ok", "check_group_ok", "check_ai_use_ok", "check_note"]


def mislabel_sample(rows: list[dict], n: int = 50, seed: str = "") -> list[dict]:
    """A reproducible sample for the hand check: stratified by group in proportion to its size
    (at least two per group), originals only. The check_* columns are left for the checker."""
    pool = [r for r in rows if not r.get("is_fork")]
    if not pool:
        return []
    rng = random.Random(f"x25-mislabel-{seed}")
    by_group = defaultdict(list)
    for r in sorted(pool, key=lambda r: r["full_name"]):
        by_group[r.get("group") or "unclassified"].append(r)
    quota = {g: max(2, round(n * len(v) / len(pool))) for g, v in by_group.items()}
    while sum(quota.values()) > n:                       # trim the largest groups back to n
        g = max(quota, key=lambda k: quota[k])
        quota[g] -= 1
    out = []
    for g, items in sorted(by_group.items()):
        for r in rng.sample(items, min(quota[g], len(items))):
            out.append({c: r.get(c, "") for c in SAMPLE_COLUMNS})
    for i, r in enumerate(out, 1):
        r["sample_id"] = f"s{i:03d}"
        for c in ("check_types_ok", "check_group_ok", "check_ai_use_ok", "check_note"):
            r[c] = ""
    return out


def error_rate(checked: list[dict]) -> dict:
    """Share of checked items with any label marked wrong ("no"), with a Wilson 95% interval."""
    done = [r for r in checked if any(str(r.get(c, "")).strip() for c in
                                      ("check_types_ok", "check_group_ok", "check_ai_use_ok"))]
    wrong = sum(1 for r in done if any(str(r.get(c, "")).strip().lower() == "no" for c in
                                       ("check_types_ok", "check_group_ok", "check_ai_use_ok")))
    n = len(done)
    if not n:
        return {"checked": 0, "wrong": 0, "rate": None, "lo": None, "hi": None}
    p, z = wrong / n, 1.96
    den = 1 + z * z / n
    mid = (p + z * z / (2 * n)) / den
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return {"checked": n, "wrong": wrong, "rate": round(p, 3), "lo": round(max(0, mid - half), 3),
            "hi": round(min(1, mid + half), 3)}


# 3. Copy and burst flags -----------------------------------------------------------------------
def _norm(desc: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", re.sub(r"\s+", " ", (desc or "").lower())).strip()


def clone_flags(rows: list[dict], min_len: int = 40) -> dict[str, str]:
    """full_name -> 'renamed copy of <earliest>' when the same description (40+ characters)
    appears under a different repository name; the earliest-created one is the original."""
    groups = defaultdict(list)
    for r in rows:
        d = _norm(r.get("description", ""))
        if len(d) >= min_len:
            groups[d].append(r)
    out = {}
    for items in groups.values():
        names = {r["full_name"].split("/")[-1].lower() for r in items}
        if len(items) < 2 or len(names) < 2:
            continue          # the same name everywhere is handled by the copies rule (COPY_MIN)
        items = sorted(items, key=lambda r: (r.get("created", ""), r["full_name"]))
        first = items[0]
        for r in items[1:]:
            if r["full_name"].split("/")[-1].lower() != first["full_name"].split("/")[-1].lower():
                out[r["full_name"]] = f"renamed copy of {first['full_name']}"
    return out


def burst_owners(rows: list[dict], window_days: int = 7, min_projects: int = 3) -> dict[str, int]:
    """owner -> the most projects that owner created within any `window_days` window, for owners
    with at least `min_projects` in one window. Owners are never published; counts only."""
    by_owner = defaultdict(list)
    for r in rows:
        try:
            by_owner[r["full_name"].split("/")[0]].append(dt.date.fromisoformat(r.get("created", "")[:10]))
        except ValueError:
            continue
    out = {}
    for owner, days in by_owner.items():
        days.sort()
        best, j = 0, 0
        for i in range(len(days)):
            while (days[i] - days[j]).days > window_days:
                j += 1
            best = max(best, i - j + 1)
        if best >= min_projects:
            out[owner] = best
    return out


def new_account(owner_created: str, first_project: str, days: int = 90) -> bool:
    """True when the account was made within `days` before its first flagged project."""
    try:
        a = dt.date.fromisoformat(owner_created[:10])
        b = dt.date.fromisoformat(first_project[:10])
    except (TypeError, ValueError):
        return False
    return 0 <= (b - a).days <= days


def star_bursts(rows: list[dict], today: dt.date, max_age: int = 60, per_day: float = 50.0,
                min_stars: int = 200) -> list[str]:
    """Young projects (under `max_age` days) gaining stars unusually fast."""
    out = []
    for r in rows:
        try:
            age = max(1, (today - dt.date.fromisoformat(r.get("created", "")[:10])).days)
        except ValueError:
            continue
        s = int(r.get("stars") or 0)
        if age <= max_age and s >= min_stars and s / age >= per_day:
            out.append(r["full_name"])
    return out


def summary_lines(rows: list[dict], flags: dict) -> list[str]:
    """Counts only (no names) for the public summary."""
    n = len(rows) or 1
    rf = flags.get("red_flags", {})
    read = sum(1 for r in rows if r.get("readme_read") == "yes")
    L = ["## Checks (author's decisions of 5 Nov 2026; counts only, flagged items stay private)", "",
         f"- READMEs read: {read}. With at least one red flag: {sum(1 for v in rf.values() if v)}."]
    for name in list(RED_FLAGS) + ["oversized repository"]:
        L.append(f"  - {name}: {sum(1 for v in rf.values() if name in v)}")
    L += [f"- Likely renamed copies (same description, different name): {len(flags.get('clones', {}))} "
          f"({100 * len(flags.get('clones', {})) / n:.1f}% of items).",
          f"- Owners with 3+ projects in one week: {len(flags.get('burst_owners', {}))}, holding "
          f"{flags.get('burst_projects', 0)} projects; of those owners, new accounts (made within 90 days "
          f"of the burst): {flags.get('new_accounts', 'not checked')}.",
          f"- Star bursts (under 60 days old, 200+ stars, 50+ a day): {len(flags.get('star_bursts', []))}.",
          f"- Searches split by creation date to stay under GitHub's 1,000-result cap: "
          f"{flags.get('split_searches', 0)}.", ""]
    return L
