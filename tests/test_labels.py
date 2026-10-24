"""Registered labelling rule (prereg section 4) and the companion check beside it."""

import random

from snapshot.labels import companion_check, direction, registered_label


def test_registered_rule_examples():
    assert direction([1, 2, 3, 4, 9], 4) == 1
    assert registered_label([5, 5, 5, 5, 9, 9]) == "Rising"
    assert registered_label([5, 5, 5, 5, 1, 1]) == "Falling"
    assert registered_label([5, 5, 5, 5, 9, 1]) == "No clear direction"
    assert registered_label([5, 5, 5, 5, 9, 9], better="lower") == "Worsening"
    assert registered_label([5, 5, 5, 5, 1, 1], better="lower") == "Improving"


def test_companion_check_agrees_only_with_clear_moves():
    se = [1.0] * 6
    assert companion_check([0, 0, 0, 0, 5, 5], se, "Rising")["check"] == "supported"
    assert companion_check([0, 0, 0, 0, 0.3, 0.3], se, "Rising")["check"] == "not supported"
    assert companion_check([0, 0, 0, 0, 5, -5], se, "No clear direction")["check"] == "no label"
    # direction comes from the values, so a 'lower is better' question works the same way
    assert companion_check([5, 5, 5, 5, 0, 0], se, "Improving")["check"] == "supported"


def test_false_alarm_rates_under_no_change():
    """Registered rule labels noise in about half of quarters; the check in about 10%."""
    rng = random.Random(20261024)
    n, labelled, supported = 20000, 0, 0
    for _ in range(n):
        x = [rng.gauss(0, 1) for _ in range(6)]
        lab = registered_label(x)
        if lab != "No clear direction":
            labelled += 1
        res = companion_check(x, [1.0] * 6, lab)
        # count the check's own false alarms regardless of the label
        if abs(res["z"]) > 1.6449:
            supported += 1
    assert 0.40 < labelled / n < 0.56
    assert 0.08 < supported / n < 0.12
