"""The privacy scan finds what must stay private and passes the public repository."""
from snapshot import privacy


def test_repository_is_clean():
    assert privacy.scan() == []


def test_finds_secrets_personal_details_and_private_figures(monkeypatch):
    # ransomware.live has been publishable since 27 Oct; pretend it is not, to test the figure check.
    from snapshot import sources
    real = sources.load
    def as_before():
        cfg = real()
        cfg["ransomware_live"] = {**cfg["ransomware_live"], "publish": False, "permission": "awaiting"}
        return cfg
    monkeypatch.setattr(sources, "load", as_before)
    sample = "\n".join([
        "client GOCSPX-abcdefghijklmnop",
        '{"refresh_token": "1//0abcdefghijklmnopqrstuvwxyz"}',
        "mail someone@gmail.com",
        "call (843) 555-0199",
        "note: monthly totals [{'month': '2026-07', 'count': 952}]",
    ])
    kinds = {k for _, _, k in privacy.scan_text("x.md", sample)}
    assert {"google client secret", "oauth token field", "email address", "phone number"} <= kinds
    assert any("ransomware.live" in k for k in kinds)


def test_allow_list_and_dates_pass():
    sample = "noreply@anthropic.com contact@shadowserver.org 2026-10-27 12:34 (706) 542-3375"
    assert privacy.scan_text("x.md", sample) == []


def test_exploratory_figures_are_flagged_unless_cleared():
    from snapshot import privacy as P
    assert P.exploratory_lines("docs/x.md", "The October jump: 377 offensive-security projects against 172 in September.")
    assert not P.exploratory_lines("docs/x.md", "Run the GitHub sweep (X25) on 6 Jan 2027 at 10:00.")
    assert not P.exploratory_lines("docs/x.md", "X25 uses 48 fixed searches " + P.MARK)
    assert not P.exploratory_lines("exploratory/x.md", "377 offensive-security projects")   # private files are not public
