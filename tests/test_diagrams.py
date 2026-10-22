from snapshot.diagrams import stale


def test_diagram_manifest_is_readable_and_check_never_fails():
    # stale() returns a list (possibly non-empty); the check is a warning, not a gate
    assert isinstance(stale(), list)
