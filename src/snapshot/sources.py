"""Switches for the sources that need permission (config/sources.yaml).

    python -m snapshot.sources          # print each switch

Plan 1 / Plan 2 in docs/RESEARCH_PLAN.md is a settings change in that file: `collect` decides
whether the quarterly pull fetches a source, `publish` whether anything derived from it may
appear in public outputs. A source may be published only with permission granted.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parents[2] / "config" / "sources.yaml"
PERMISSIONS = ("awaiting", "granted", "declined")


def load(path: Path = CONFIG) -> dict[str, dict]:
    data = yaml.safe_load(Path(path).read_text())["permissioned"]
    for key, s in data.items():
        if s.get("permission") not in PERMISSIONS:
            raise ValueError(f"{key}: permission must be one of {PERMISSIONS}")
        for flag in ("collect", "publish"):
            if not isinstance(s.get(flag), bool):
                raise ValueError(f"{key}: {flag} must be true or false")
        if s["publish"] and s["permission"] != "granted":
            raise ValueError(f"{key}: publish needs permission: granted")
        if s["collect"] and s["permission"] == "declined":
            raise ValueError(f"{key}: collect is on but permission was declined")
        if s["collect"] and not s.get("pull"):
            raise ValueError(f"{key}: collect is on but no collector exists yet (pull: null)")
    return data


def disabled_pulls(path: Path = CONFIG) -> set[str]:
    """Pull names the quarterly pull must skip."""
    return {s["pull"] for s in load(path).values() if s.get("pull") and not s["collect"]}


def by_pull(path: Path = CONFIG) -> dict[str, dict]:
    return {s["pull"]: s for s in load(path).values() if s.get("pull")}


def may_publish(key: str, path: Path = CONFIG) -> bool:
    return bool(load(path)[key]["publish"])


def summary(path: Path = CONFIG) -> str:
    return "; ".join(f"{s['name']}: permission {s['permission']}, collect {'on' if s['collect'] else 'off'}, "
                     f"publish {'on' if s['publish'] else 'off'}" for s in load(path).values())


if __name__ == "__main__":
    for key, s in load().items():
        print(f"{key:16} permission={s['permission']:9} collect={s['collect']!s:5} publish={s['publish']!s:5} pull={s.get('pull')}")
    sys.exit(0)
