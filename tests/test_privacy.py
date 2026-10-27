"""The privacy scan finds what must stay private and passes the public repository."""
from snapshot import privacy


def test_repository_is_clean():
    assert privacy.scan() == []


def test_finds_secrets_personal_details_and_private_figures():
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
