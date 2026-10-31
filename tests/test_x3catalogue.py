"""The AI attack catalogue is generated from the X3 log and must be current (29 Oct 2026)."""
from snapshot import x3catalogue as X
from snapshot.util import _repo_root

from conftest import needs_private


@needs_private
def test_catalogue_is_current():
    assert (_repo_root() / X.OUT).read_text() == X.build_text(), "run python -m snapshot.x3catalogue build"
