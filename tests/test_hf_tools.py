"""Hugging Face companion sweep (X25, author's decision 30 Oct 2026)."""
from snapshot.research import hf_tools as H


def test_item_labels_and_safety_removed():
    r = H.item("models", {"id": "someone/Llama-3-8B-abliterated-pentest", "createdAt": "2026-05-01T00:00:00Z",
                          "likes": 3, "downloads": 10, "tags": ["base_model:meta-llama/Meta-Llama-3-8B"]})
    assert r["role"] == "attack" and r["safety_removed"] == "yes" and r["base_lab"] == "Meta"


def test_hf_roles_on_real_names_from_the_first_baseline():
    cases = {
        "Qwen3.8-27B-Uncensored-FP8": "safety_removed", "PixArt-Sigma-900M": "unrelated",
        "hackernews-summaries": "unrelated", "ESM_tdavidson__hate_speech_offensive_default": "unrelated",
        "gpt-oss-120b-reward-hacker-step-496": "unrelated", "shopper-persona_016__r16_lr1e-3_bs4_ep4": "unrelated",
        "Qwen-QwQ-32b-Pentest-CoT-Q8_0-GGUF": "attack", "exploit-path-tracer-agent": "attack",
        "Gemma-4-12b-RedTeam-BlackICE": "attack", "HackerAI-Pro-Agent-8B-GGUF": "attack",
        "phishing-email-detection-distilbert_v2.4.1": "defence", "Threat-Detection-RFDETR": "defence",
        "vulnerability-severity-classification-roberta-base": "defence",
        "Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF": "general_security",
        "GLM-5.3-CYBERSECURITY-FP8": "general_security",
        "jailbreak-prompts-classifier": "model_testing",
        "llama_70b_synth_docs_only_then_redteam_high_defend_objects": "model_testing",
        "offensive-detector": "unrelated", "hackertyper": "unrelated",
    }
    for name, want in cases.items():
        assert H.hf_role(name, []) == want, (name, H.hf_role(name, []))


def test_individuals_named_by_item_only():
    rows = [H.item("models", {"id": "alice/sec-model"}), H.item("spaces", {"id": "acme/soc-analyst"})]
    H.name_rows(rows, H.owners_kind(["alice", "acme"], pause=0, check=lambda o: o == "acme"))
    assert rows[0]["name"] == "sec-model" and rows[1]["name"] == "acme/soc-analyst"
