"""The Snapshot manual (author's request, 29 Oct 2026): complete and current."""
from snapshot import manual as M


def test_every_markdown_file_is_in_the_manual_or_excluded():
    assert M.unlisted() == []


def test_headings_shift_but_code_blocks_do_not():
    t = M._shift_headings("# A\n## B\n```\n# not a heading\n```\n###### deep")
    assert t.split("\n") == ["### A", "#### B", "```", "# not a heading", "```", "###### deep"]


def test_links_point_inside_the_manual_or_to_github():
    t = M._fix_links("[a](WORKFLOWS.md) [b](../config/x.yaml) ![c](diagrams/p.png) [d](https://x.org)",
                     "docs/SOP_MANUAL_RUNS.md", "docs/manual", {"docs/WORKFLOWS.md"})
    assert "[a](#doc-docs-workflows-md)" in t
    assert "[b](https://github.com/pagagne/internet-security-snapshot/blob/main/config/x.yaml)" in t
    assert "![c](../../docs/diagrams/p.png)" in t and "[d](https://x.org)" in t


def test_github_copy_is_split_small_and_linked():
    """Author's request, 30 Oct 2026: a GitHub copy in parts small enough to display, with a
    contents page of dropdowns linking to every section; it grows by splitting further."""
    import re
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    parts = M.build_parts(root)
    index = parts.pop(M.INDEX)
    assert index.count("<details>") == len(M.load(root)["parts"])
    for f, text in parts.items():
        assert len(text.encode()) <= M.MAX_FILE * 1.3, f       # one oversized section may exceed a little
        for target, anchor in re.findall(r"\]\(([\w.-]*\.md)?#(doc-[\w-]+)\)", text):
            dest = parts[f"{M.PARTS_DIR}/{target}"] if target else text
            assert f'<a id="{anchor}"></a>' in dest, (f, target, anchor)
    for target, anchor in re.findall(r"\(parts/([\w.-]+\.md)#(doc-[\w-]+)\)", index):
        assert f'<a id="{anchor}"></a>' in parts[f"{M.PARTS_DIR}/{target}"], (target, anchor)
