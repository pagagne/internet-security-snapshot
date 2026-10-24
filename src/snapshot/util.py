"""Shared helpers: quarters, checksums, manifests, config loading."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

def _repo_root() -> Path:
    """The checkout holding config/: SNAPSHOT_ROOT if set, else the source tree, else the
    working directory (the package may be installed outside the checkout)."""
    import os
    for cand in (os.environ.get("SNAPSHOT_ROOT"), Path(__file__).resolve().parents[2], Path.cwd()):
        if cand and (Path(cand) / "config" / "cohort_rules.yaml").exists():
            return Path(cand)
    raise FileNotFoundError("config/ not found; run from the repository root or set SNAPSHOT_ROOT")


REPO_ROOT = _repo_root()
CONFIG_DIR = REPO_ROOT / "config"


@dataclass(frozen=True)
class Quarter:
    year: int
    q: int

    @classmethod
    def parse(cls, text: str) -> "Quarter":
        m = re.fullmatch(r"(\d{4})Q([1-4])", text.strip().upper())
        if not m:
            raise ValueError(f"Quarter must look like 2026Q4, got {text!r}")
        return cls(int(m.group(1)), int(m.group(2)))

    @classmethod
    def previous_to(cls, day: dt.date) -> "Quarter":
        """The most recent quarter that has fully ended before `day`."""
        q = (day.month - 1) // 3 + 1
        year = day.year
        q -= 1
        if q == 0:
            q, year = 4, year - 1
        return cls(year, q)

    @property
    def start(self) -> dt.date:
        return dt.date(self.year, 3 * (self.q - 1) + 1, 1)

    @property
    def end(self) -> dt.date:
        """Last day of the quarter (inclusive)."""
        if self.q == 4:
            return dt.date(self.year, 12, 31)
        return dt.date(self.year, 3 * self.q + 1, 1) - dt.timedelta(days=1)

    def contains(self, day: dt.date) -> bool:
        return self.start <= day <= self.end

    def shift(self, n: int) -> "Quarter":
        idx = self.year * 4 + (self.q - 1) + n
        return Quarter(idx // 4, idx % 4 + 1)

    def __str__(self) -> str:
        return f"{self.year}Q{self.q}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_config(name: str) -> dict:
    with open(CONFIG_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


class Manifest:
    """Records every file a pull wrote, with checksums and source versions."""

    def __init__(self, quarter: Quarter, run: str, out_dir: Path):
        self.quarter = quarter
        self.run = run
        self.out_dir = out_dir
        self.entries: list[dict] = []
        self.started_at = utcnow()

    def add_file(self, source: str, path: Path, source_version: str, status: str = "ok", note: str = "") -> None:
        self.entries.append(
            {
                "source": source,
                "file_path": str(path.relative_to(self.out_dir)),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
                "source_version": source_version,
                "retrieved_at": utcnow(),
                "status": status,
                "note": note,
            }
        )

    def add_gap(self, source: str, reason: str) -> None:
        self.entries.append(
            {
                "source": source,
                "file_path": None,
                "sha256": None,
                "bytes": 0,
                "source_version": None,
                "retrieved_at": utcnow(),
                "status": "gap",
                "note": reason,
            }
        )

    def write(self) -> Path:
        path = self.out_dir / "manifest.json"
        doc = {
            "quarter": str(self.quarter),
            "run": self.run,
            "started_at": self.started_at,
            "finished_at": utcnow(),
            "environment": environment(),
            "files": self.entries,
        }
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        return path


def environment() -> dict:
    """The software a run used, so any published number can be recomputed with the same
    environment: Python version, the checksum of the hash-locked requirements file, the
    installed versions of the analysis packages, and the git commit and runner image when
    run under GitHub Actions."""
    import os
    import platform
    from importlib import metadata

    lock = REPO_ROOT / "requirements.lock"
    pkgs = {}
    for name in ("duckdb", "pandas", "numpy", "pyarrow", "scipy", "lifelines", "statsmodels", "ruptures"):
        try:
            pkgs[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            pkgs[name] = None
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "requirements_lock_sha256": sha256_file(lock) if lock.exists() else None,
        "packages": pkgs,
        "git_commit": os.environ.get("GITHUB_SHA"),
        "runner_image": " ".join(filter(None, (os.environ.get("ImageOS"), os.environ.get("ImageVersion")))) or None,
    }


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(text: str | None) -> dt.datetime | None:
    """Parse an ISO-8601 timestamp (with or without Z/offset) to aware UTC."""
    if not text:
        return None
    t = text.strip().replace("Z", "+00:00")
    try:
        val = dt.datetime.fromisoformat(t)
    except ValueError:
        val = dt.datetime.fromisoformat(t[:10])
    if val.tzinfo is None:
        val = val.replace(tzinfo=dt.timezone.utc)
    return val.astimezone(dt.timezone.utc)
