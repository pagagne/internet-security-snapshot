"""Hugging Face companion sweep (X25, author's decision 30 Oct 2026)."""
from snapshot.research import hf_tools as H


def test_item_labels_and_safety_removed():
    r = H.item("models", {"id": "someone/Llama-3-8B-abliterated-pentest", "createdAt": "2026-05-01T00:00:00Z",
                          "likes": 3, "downloads": 10, "tags": ["base_model:meta-llama/Meta-Llama-3-8B"]})
    assert r["role"] == "attack" and r["safety_removed"] == "yes" and r["base_lab"] == "Meta"


def test_individuals_named_by_item_only():
    rows = [H.item("models", {"id": "alice/sec-model"}), H.item("spaces", {"id": "acme/soc-analyst"})]
    H.name_rows(rows, H.owners_kind(["alice", "acme"], pause=0, check=lambda o: o == "acme"))
    assert rows[0]["name"] == "sec-model" and rows[1]["name"] == "acme/soc-analyst"
