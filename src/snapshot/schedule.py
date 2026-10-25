"""The study's schedule as code (docs/schedule/schedule.yaml).

    python -m snapshot.schedule build        # write docs/ANNUAL_PLAN.md and docs/schedule/snapshot.ics
    python -m snapshot.schedule check        # exit 1 if those files are out of date
    python -m snapshot.schedule due [--date YYYY-MM-DD]   # JSON: issues to open, runs to start
    python -m snapshot.schedule act [--date ...] [--dry-run]   # open them / start them (needs gh)

The daily Schedule workflow (.github/workflows/schedule.yml) calls `due` and opens one GitHub
issue per author or Claude item when it falls due, and starts the workflow named by any GitHub
item with a `dispatch` block. Issues are the durable to-do list: any Claude session, or the
author, can see what is open without depending on a particular chat.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import yaml

from .util import REPO_ROOT

SOURCE = REPO_ROOT / "docs/schedule/schedule.yaml"
ICS = REPO_ROOT / "docs/schedule/snapshot.ics"
REVIEWER_ICS = REPO_ROOT / "docs/schedule/reviewer.ics"   # the external reviewer's own feed
PLAN = REPO_ROOT / "docs/ANNUAL_PLAN.md"
README = REPO_ROOT / "README.md"
BEGIN, END = "<!-- schedule:begin -->", "<!-- schedule:end -->"
OWNERS = ("author", "reviewer", "claude", "github")
OWNER_NAME = {"author": "Author", "reviewer": "External reviewer", "claude": "Claude", "github": "GitHub (automatic)"}
DEFAULT_OPEN = {"author": 2, "reviewer": 0, "claude": 0, "github": 0}


# --- time zone: America/New_York without relying on system tz data ---------------------
def _nth_sunday(year: int, month: int, n: int) -> dt.date:
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def ny_offset(day: dt.date, hour: int = 12) -> int:
    """UTC offset in hours for America/New_York (US rules since 2007)."""
    start = _nth_sunday(day.year, 3, 2)   # second Sunday in March, 02:00 local
    end = _nth_sunday(day.year, 11, 1)    # first Sunday in November, 02:00 local
    dst = (start < day < end) or (day == start and hour >= 2) or (day == end and hour < 2)
    return -4 if dst else -5


def to_utc(day: dt.date, hhmm: str, utc: bool) -> dt.datetime:
    h, m = map(int, hhmm.split(":"))
    t = dt.datetime(day.year, day.month, day.day, h, m)
    return t if utc else t - dt.timedelta(hours=ny_offset(day, h))


# --- loading and expanding -----------------------------------------------------------
def load(path: Path = SOURCE) -> list[dict]:
    items = yaml.safe_load(path.read_text())["items"]
    seen = set()
    for it in items:
        missing = {"id", "owner", "title"} - set(it)
        if missing:
            raise ValueError(f"{it.get('id', '?')}: missing {sorted(missing)}")
        if it["id"] in seen:
            raise ValueError(f"duplicate id {it['id']}")
        seen.add(it["id"])
        if it["owner"] not in OWNERS:
            raise ValueError(f"{it['id']}: owner must be one of {OWNERS}")
        if ("date" in it) == ("repeat" in it):
            raise ValueError(f"{it['id']}: give exactly one of date or repeat")
        if "dispatch" in it and it["owner"] != "github":
            raise ValueError(f"{it['id']}: only github items can dispatch a workflow")
    return items


def _months(frm: str, until: str):
    y, m = map(int, frm.split("-"))
    uy, um = map(int, until.split("-"))
    while (y, m) <= (uy, um):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def expand(items: list[dict]) -> list[dict]:
    """One occurrence per date, sorted by date then owner."""
    out = []
    for it in items:
        if "date" in it:
            d = it["date"] if isinstance(it["date"], dt.date) else dt.date.fromisoformat(str(it["date"]))
            dates = [d]
        else:
            r = it["repeat"]
            dates = [dt.date(y, m, r["day"]) for y, m in _months(str(r["from"]), str(r["until"])) if m in r["months"]]
        for d in dates:
            occ = {
                "uid": f"{it['id']}@{d.isoformat()}",
                "id": it["id"], "owner": it["owner"], "title": it["title"], "date": d,
                "details": " ".join(str(it.get("details", "")).split()),
                "time": it.get("time"), "utc": bool(it.get("utc")),
                "minutes": int(it.get("minutes", 30)), "days": int(it.get("days", 1)),
                "open": int(it.get("open", DEFAULT_OPEN[it["owner"]])),
                "dispatch": it.get("dispatch"),
                "feeds": list(it.get("feeds") or []),
            }
            out.append(occ)
    return sorted(out, key=lambda o: (o["date"], o["time"] or "", OWNERS.index(o["owner"]), o["id"]))


# --- outputs -------------------------------------------------------------------------
def _ics_text(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def _fold(line: str) -> list[str]:
    out, b = [], line.encode()
    while len(b) > 75:
        cut = 75
        while (b[cut] & 0xC0) == 0x80:   # do not split a UTF-8 character
            cut -= 1
        out.append(b[:cut].decode())
        b = b" " + b[cut:]
    out.append(b.decode())
    return out


ALL_FEED = ("Internet Security Snapshot",
            "Every action item of the study: author, external reviewer, Claude and automatic GitHub runs. "
            "Source: docs/schedule/schedule.yaml in github.com/pagagne/internet-security-snapshot")
REVIEWER_FEED = ("Internet Security Snapshot: reviewer",
                 "The external reviewer's tasks and the project dates they depend on. "
                 "Source: docs/schedule/schedule.yaml in github.com/pagagne/internet-security-snapshot")


def reviewer_occ(occ: list[dict]) -> list[dict]:
    return [o for o in occ if o["owner"] == "reviewer" or "reviewer" in o["feeds"]]


def ics(occ: list[dict], feed: tuple[str, str] = ALL_FEED, you: str = "author") -> str:
    name, desc = feed
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//internet-security-snapshot//schedule//EN",
         "CALSCALE:GREGORIAN", "METHOD:PUBLISH", f"X-WR-CALNAME:{_ics_text(name)}",
         f"X-WR-CALDESC:{_ics_text(desc)}", "X-WR-TIMEZONE:America/New_York"]
    for o in occ:
        tag = "[You]" if o["owner"] == you else {"author": "[Paul]", "reviewer": "[Reviewer]", "claude": "[Claude]", "github": "[GitHub]"}[o["owner"]]
        L += ["BEGIN:VEVENT", f"UID:{o['uid']}@internet-security-snapshot", "DTSTAMP:20261024T000000Z"]
        if o["time"]:
            s = to_utc(o["date"], o["time"], o["utc"])
            e = s + dt.timedelta(minutes=o["minutes"])
            L += [f"DTSTART:{s:%Y%m%dT%H%M%SZ}", f"DTEND:{e:%Y%m%dT%H%M%SZ}"]
        else:
            L += [f"DTSTART;VALUE=DATE:{o['date']:%Y%m%d}",
                  f"DTEND;VALUE=DATE:{o['date'] + dt.timedelta(days=o['days']):%Y%m%d}",
                  "TRANSP:TRANSPARENT"]
        L += [f"SUMMARY:{_ics_text(f'{tag} Snapshot: ' + o['title'])}",
              f"DESCRIPTION:{_ics_text(o['details'] + chr(10) + chr(10) + 'Owner: ' + OWNER_NAME[o['owner']] + '. Source: docs/schedule/schedule.yaml')}",
              f"CATEGORIES:{OWNER_NAME[o['owner']]}", "END:VEVENT"]
    L.append("END:VCALENDAR")
    return "\r\n".join(x for line in L for x in _fold(line)) + "\r\n"


def _when(o: dict) -> str:
    d = f"{o['date']:%a %d %b %Y}"
    if o["days"] > 1:
        d += f" to {o['date'] + dt.timedelta(days=o['days'] - 1):%d %b}"
    if o["time"]:
        d += f", {o['time']} {'UTC' if o['utc'] else 'ET'}"
    return d


def plan(items: list[dict], occ: list[dict]) -> str:
    L = ["# Annual plan: every action item, by who does it", "",
         "Generated from `docs/schedule/schedule.yaml` by `python -m snapshot.schedule build`; do not edit by hand.",
         "The same items are in the calendar feed `docs/schedule/snapshot.ics`, and each author or Claude item",
         "opens a GitHub issue when it falls due (label `schedule`, plus `owner:author` or `owner:claude`).", ""]
    repeating = [it for it in items if "repeat" in it]
    L += ["## Every quarter and every month", "", "| Who | What | When |", "|---|---|---|"]
    for it in sorted(repeating, key=lambda i: (OWNERS.index(i["owner"]), min(i["repeat"]["months"]), i["repeat"]["day"])):
        r = it["repeat"]
        months = "every month" if len(r["months"]) == 12 else ", ".join(dt.date(2000, m, 1).strftime("%b") for m in r["months"])
        when = f"day {r['day']}, {months}, {r['from']} to {r['until']}"
        if it.get("days", 1) > 1:
            when += f" ({it['days']} days)"
        if it.get("time"):
            when += f", {it['time']} {'UTC' if it.get('utc') else 'ET'}"
        L.append(f"| {OWNER_NAME[it['owner']]} | {it['title']} | {when} |")
    L.append("")
    one_off = [o for o in occ if o["id"] not in {i["id"] for i in repeating}]
    for owner in OWNERS:
        L += [f"## {OWNER_NAME[owner]}: dated items", "", "| When | What | Details |", "|---|---|---|"]
        for o in [o for o in one_off if o["owner"] == owner]:
            L.append(f"| {_when(o)} | {o['title']} | {o['details'].replace('|', '/')} |")
        L.append("")
    return "\n".join(L)


CATCH_UP_DAYS = 6   # a missed daily run is made up for within this many days


def due(occ: list[dict], today: dt.date, catch_up: int = CATCH_UP_DAYS) -> dict:
    """Items whose issue should be open (or run started) by today, looking back `catch_up`
    days so a missed daily run loses nothing. The caller skips anything already done."""
    lo = today - dt.timedelta(days=catch_up)
    issues = [o for o in occ if o["owner"] in ("author", "claude")
              and lo <= o["date"] - dt.timedelta(days=o["open"]) <= today]
    runs = [o for o in occ if o["dispatch"] and lo <= o["date"] <= today]
    js = lambda o: {"uid": o["uid"], "owner": o["owner"], "title": o["title"], "when": _when(o),
                    "details": o["details"], "dispatch": o["dispatch"]}
    return {"date": today.isoformat(), "issues": [js(o) for o in issues], "runs": [js(o) for o in runs]}


MARKER = "<!-- schedule-uid: {} -->"


def issue_body(o: dict) -> str:
    return "\n\n".join([
        f"**When:** {o['when']}  \n**Who:** {OWNER_NAME[o['owner']]}",
        o["details"],
        "Close this issue when it is done (or comment why it was skipped). Source: "
        "`docs/schedule/schedule.yaml`; how the study runs: `docs/OPERATIONS.md`.",
        MARKER.format(o["uid"]),
    ])


def act(today: dt.date, dry: bool = False, gh=None) -> list[str]:
    """Open the due issues and start the due runs, skipping any already done. `gh` runs a
    GitHub CLI command (list of args) and returns its stdout; injectable for tests."""
    import re
    import subprocess
    gh = gh or (lambda args: subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout)
    d = due(expand(load()), today)
    existing = gh(["issue", "list", "--label", "schedule", "--state", "all", "--limit", "1000", "--json", "body"])
    done = set(re.findall(r"<!-- schedule-uid: (\S+) -->", existing))
    log = []
    for o in d["issues"]:
        if o["uid"] in done:
            continue
        args = ["issue", "create", "--title", f"[{OWNER_NAME[o['owner']]}] {o['title']} ({o['when']})",
                "--label", "schedule", "--label", f"owner:{o['owner']}", "--body", issue_body(o)]
        log.append("open " + o["uid"])
        if not dry:
            gh(args)
    for o in d["runs"]:
        if o["uid"] in done:
            continue
        w = o["dispatch"]
        log.append(f"run {o['uid']} ({w['workflow']})")
        if not dry:
            gh(["workflow", "run", w["workflow"], *[x for k, v in (w.get("inputs") or {}).items() for x in ("-f", f"{k}={v}")]])
            url = gh(["issue", "create", "--title", f"[GitHub] Started: {o['title']} ({o['when']})", "--label", "schedule",
                      "--label", "owner:github", "--body", issue_body(o) + "\n\nStarted automatically by the Schedule workflow."]).strip()
            gh(["issue", "close", url, "--comment", "Run started; see the Actions tab for its result."])
    return log


def load_milestones(path: Path = SOURCE) -> list[dict]:
    return yaml.safe_load(path.read_text()).get("milestones") or []


def _dates(ds: list[dt.date]) -> str:
    """1 Dec 2026; 1 Jan / 1 Feb 2027; 21 Dec 2026 / 4 Jan 2027."""
    if len({d.year for d in ds}) == 1:
        return " / ".join(f"{d.day} {d:%b}" for d in ds) + f" {ds[0].year}"
    return " / ".join(f"{d.day} {d:%b %Y}" for d in ds)


def readme_table(occ: list[dict], milestones: list[dict]) -> str:
    by_uid = {o["uid"]: o for o in occ}
    by_id: dict[str, list[dict]] = {}
    for o in occ:
        by_id.setdefault(o["id"], []).append(o)
    rows = []
    for m in milestones:
        if "when" in m:
            when, key = str(m["when"]), dt.datetime.strptime(str(m["when"]), "%d %b %Y").date()
        else:
            ds = []
            for ref in m["at"]:
                if ref in by_uid:
                    ds.append(by_uid[ref]["date"])
                elif len(by_id.get(ref, [])) == 1:
                    ds.append(by_id[ref][0]["date"])
                else:
                    raise ValueError(f"milestone '{m['text']}': no single occurrence '{ref}'")
            when, key = m.get("prefix", "") + _dates(ds) + m.get("suffix", ""), ds[0]
        rows.append((key, f"| {when} | {m['text']} |"))
    rows.sort(key=lambda r: r[0])
    return "\n".join(["| Date | Milestone |", "|---|---|", *(r for _, r in rows)])


def readme(text: str, table: str) -> str:
    if BEGIN not in text or END not in text:
        raise ValueError(f"README.md needs {BEGIN} and {END} around the schedule table")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{BEGIN}\n<!-- Generated from docs/schedule/schedule.yaml (milestones); edit there, then run python -m snapshot.schedule build. -->\n{table}\n{END}{tail}"


def build() -> tuple[str, str]:
    items = load()
    occ = expand(items)
    return plan(items, occ), ics(occ)


def build_reviewer_ics() -> str:
    return ics(reviewer_occ(expand(load())), REVIEWER_FEED, you="reviewer")


def build_readme() -> str:
    return readme(README.read_text(), readme_table(expand(load()), load_milestones()))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build"); sub.add_parser("check")
    d = sub.add_parser("due"); d.add_argument("--date")
    x = sub.add_parser("act"); x.add_argument("--date"); x.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in ("due", "act"):
        today = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(dt.timezone.utc).date()
        if a.cmd == "due":
            print(json.dumps(due(expand(load()), today), indent=2))
        else:
            for line in act(today, dry=a.dry_run) or ["nothing due"]:
                print(line)
        return 0
    md, cal = build()
    if a.cmd == "build":
        PLAN.write_text(md + "\n")
        ICS.write_bytes(cal.encode())
        REVIEWER_ICS.write_bytes(build_reviewer_ics().encode())
        README.write_text(build_readme())
        print(f"wrote {PLAN.relative_to(REPO_ROOT)}, {ICS.relative_to(REPO_ROOT)} and the reviewer feed and the README schedule table")
        return 0
    stale = [p for p, want in ((PLAN, (md + "\n").encode()), (ICS, cal.encode()), (REVIEWER_ICS, build_reviewer_ics().encode()), (README, build_readme().encode()))
             if not p.exists() or p.read_bytes() != want]
    if stale:
        print("out of date: " + ", ".join(str(p.relative_to(REPO_ROOT)) for p in stale) + " (run: python -m snapshot.schedule build)")
        return 1
    print("schedule outputs are current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
