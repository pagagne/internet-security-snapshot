"""Guards on the pinned environment (prereg section 9: versions pinned in a lockfile).

Regenerate the lockfile only deliberately, and log it if any published number changes:
    uv pip compile pyproject.toml --extra dev --python-version 3.12 \
        --python-platform x86_64-unknown-linux-gnu --generate-hashes -o requirements.lock
"""

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _name(req: str) -> str:
    return re.split(r"[<>=!~\[ ;]", req, maxsplit=1)[0].strip().lower().replace("_", "-")


def test_lockfile_pins_every_dependency_with_hashes():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    wanted = {_name(r) for r in project["dependencies"] + project["optional-dependencies"]["dev"]}
    lock = (ROOT / "requirements.lock").read_text()
    pinned = {m.group(1).lower(): m.group(2) for m in re.finditer(r"^([A-Za-z0-9_.-]+)==(\S+)", lock, re.M)}
    missing = wanted - set(pinned)
    assert not missing, f"not pinned in requirements.lock: {sorted(missing)}"
    blocks = re.split(r"\n(?=[A-Za-z0-9_.-]+==)", lock)
    for b in blocks:
        if re.match(r"[A-Za-z0-9_.-]+==", b):
            assert "--hash=sha256:" in b, f"no hash for {b.split()[0]}"


def test_workflows_use_the_lockfile_and_pin_actions_by_commit():
    for wf in (ROOT / ".github/workflows").glob("*.yml"):
        text = wf.read_text()
        for m in re.finditer(r"uses:\s*([\w.-]+/[\w.-]+)@(\S+)", text):
            assert re.fullmatch(r"[0-9a-f]{40}", m.group(2)), f"{wf.name}: {m.group(1)} not pinned to a commit SHA"
        if "pip install" in text:
            assert "--require-hashes -r requirements.lock" in text, f"{wf.name}: installs without the lockfile"
            assert 'pip install -e ".[dev]"' not in text
        for m in re.finditer(r'python-version:\s*"([^"]+)"', text):
            assert re.fullmatch(r"\d+\.\d+\.\d+", m.group(1)), f"{wf.name}: Python not pinned to a patch version"


def test_manifest_records_the_environment(tmp_path):
    from snapshot.util import Manifest, Quarter
    import json

    path = Manifest(Quarter(2026, 4), "dry-run", tmp_path).write()
    env = json.loads(path.read_text())["environment"]
    assert env["python"] and env["requirements_lock_sha256"]
    assert set(env["packages"]) >= {"pandas", "numpy", "lifelines"}
