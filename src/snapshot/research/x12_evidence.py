"""Evidence for the 12 Nov research review, decisions 7 and 8 (X12, open-weight release curve).

(A) Hugging Face Hub: language-model repositories created by a fixed list of major labs, per
quarter since January 2023, after dropping obvious derivatives (quantized copies, adapters,
embedding, reward and guard models). (B) Epoch AI's model database: open-weight models per
quarter, all and "notable", to check (A) against. (C) Epoch AI's benchmark data: which
benchmarks exist, how many models each scores and since when, and for candidate coding and
security benchmarks how many open-weight models reach a few trial bars. Public metadata only.

    python -m snapshot.research.x12_evidence --out DIR
"""
from __future__ import annotations

import argparse
import io
import json
import re
import time
import zipfile
from pathlib import Path

import pandas as pd

from snapshot.collect.http import get

LABS = ["deepseek-ai", "Qwen", "meta-llama", "mistralai", "google", "microsoft", "nvidia", "openai",
        "moonshotai", "zai-org", "THUDM", "01-ai", "allenai", "ibm-granite", "CohereLabs",
        "CohereForAI", "tiiuae", "MiniMaxAI", "xai-org", "LGAI-EXAONE", "baidu", "tencent",
        "stepfun-ai", "internlm", "openbmb"]
LLM_TAGS = {"text-generation", "image-text-to-text", "any-to-any"}
DERIV = re.compile(r"(gguf|awq|gptq|fp8|fp4|int4|int8|bnb|mlx|onnx|exl2|-quant|quantized|lora|adapter|"
                   r"embed|reward|guard|-rm\b|tokenizer|draft|eagle|mtp)", re.I)
EPOCH = {"all": "https://epoch.ai/data/all_ai_models.csv",
         "notable": "https://epoch.ai/data/notable_ai_models.csv",
         "bench": "https://epoch.ai/data/benchmark_data.zip"}
CODING = re.compile(r"swe|code|humaneval|livecodebench|aider|terminal", re.I)
SECURITY = re.compile(r"cyber|cybench|ctf|security|secbench|vuln|exploit|cve", re.I)


def _q(d) -> str:
    return pd.Period(d, "Q").strftime("%YQ%q") if pd.notna(d) else "?"


def hub(pause: float = 1.0) -> dict:
    rows = []
    for lab in LABS:
        url = f"https://huggingface.co/api/models?author={lab}&limit=1000&full=true&sort=createdAt&direction=-1"
        try:
            data = get(url, timeout=60).json()
        except Exception as e:  # noqa: BLE001 - record and go on
            rows.append({"lab": lab, "error": str(e)[:120]})
            time.sleep(pause)
            continue
        for m in data:
            mid = m.get("id") or m.get("modelId") or ""
            rows.append({"lab": lab, "id": mid, "created": m.get("createdAt"),
                         "pipeline": m.get("pipeline_tag"), "derivative": bool(DERIV.search(mid))})
        time.sleep(pause)
    df = pd.DataFrame(rows)
    errors = df[df.get("error").notna()]["lab"].tolist() if "error" in df else []
    df = df[df.get("id").notna()] if "id" in df else df
    df["created"] = pd.to_datetime(df["created"], utc=True, errors="coerce").dt.tz_localize(None)
    llm = df[df["pipeline"].isin(LLM_TAGS) & ~df["derivative"] & (df["created"] >= "2023-01-01")].copy()
    llm["quarter"] = llm["created"].map(_q)
    per_q = llm.groupby("quarter").size().to_dict()
    per_lab = llm.groupby("lab").size().sort_values(ascending=False).to_dict()
    return {"labs_tried": len(LABS), "labs_failed": errors, "repos_seen": int(len(df)),
            "llm_repos_kept": int(len(llm)), "per_quarter": per_q, "per_lab": per_lab,
            "dropped_as_derivative": int(df["derivative"].sum()) if len(df) else 0,
            "sample_recent": llm.sort_values("created", ascending=False).head(15)[["lab", "id", "created"]]
            .assign(created=lambda x: x["created"].dt.date.astype(str)).to_dict("records")}


def epoch_models() -> tuple[dict, pd.DataFrame]:
    out, frames = {}, {}
    for key in ("all", "notable"):
        df = pd.read_csv(io.BytesIO(get(EPOCH[key], timeout=120).content), low_memory=False)
        frames[key] = df
        acc = next((c for c in df.columns if "accessib" in c.lower()), None)
        dcol = next((c for c in df.columns if "publication date" in c.lower()), None)
        out[key] = {"rows": int(len(df)), "columns_used": [acc, dcol]}
        if acc and dcol:
            d = df.copy()
            d["date"] = pd.to_datetime(d[dcol], errors="coerce")
            ow = d[d[acc].astype(str).str.contains("open weights", case=False, na=False) & (d["date"] >= "2023-01-01")]
            out[key]["accessibility_values"] = d[acc].value_counts().head(8).to_dict()
            out[key]["open_weight_per_quarter"] = ow.groupby(ow["date"].map(_q)).size().to_dict()
    return out, frames["all"]


def epoch_benchmarks(models: pd.DataFrame) -> dict:
    z = zipfile.ZipFile(io.BytesIO(get(EPOCH["bench"], timeout=180).content))
    acc = next((c for c in models.columns if "accessib" in c.lower()), None)
    name_col = next((c for c in models.columns if c.lower() in ("model", "system")), None)
    open_names = set()
    if acc and name_col:
        open_names = {re.sub(r"[^a-z0-9]", "", str(n).lower()) for n in
                      models.loc[models[acc].astype(str).str.contains("open weights", case=False, na=False), name_col]}
    files, cands = [], []
    for n in z.namelist():
        if not n.lower().endswith(".csv"):
            continue
        try:
            df = pd.read_csv(z.open(n), low_memory=False)
        except Exception:  # noqa: BLE001
            continue
        kind = "coding" if CODING.search(n) else "security" if SECURITY.search(n) else None
        info = {"file": n, "rows": int(len(df)), "columns": list(df.columns)[:12], "kind": kind}
        files.append(info)
        if kind:
            score = next((c for c in df.columns if re.search(r"score|accuracy|resolved|pass", c, re.I)), None)
            mcol = next((c for c in df.columns if re.search(r"^model|model version|^system", c, re.I)), None)
            dcol = next((c for c in df.columns if re.search(r"release date|date", c, re.I)), None)
            if score and mcol:
                s = pd.to_numeric(df[score], errors="coerce")
                s = s * 100 if s.notna().any() and s.max() <= 1.0 else s
                def _open(x) -> bool:
                    x = re.sub(r"[^a-z0-9]", "", str(x).lower())
                    return len(x) >= 4 and any(o and (x.startswith(o) or o.startswith(x)) for o in open_names)
                is_open = df[mcol].map(_open)
                bars = {}
                for bar in (20, 30, 40, 50, 60):
                    hit = df[(s >= bar)]
                    bars[str(bar)] = {"models": int(len(hit)), "open_weight": int(is_open[s >= bar].sum())}
                cands.append({"file": n, "kind": kind, "score_column": score, "models_scored": int(s.notna().sum()),
                              "open_weight_scored": int(is_open.sum()),
                              "first_date": str(pd.to_datetime(df[dcol], errors="coerce").min())[:10] if dcol else None,
                              "best": round(float(s.max()), 1) if s.notna().any() else None, "bars": bars})
    return {"files": sorted(files, key=lambda x: -x["rows"]), "candidates": cands}


def report(R: dict) -> str:
    H, E, B = R["hub"], R["epoch"], R["bench"]
    L = ["# X12 evidence for decisions 7 and 8 (12 Nov 2026)", "",
         "## Decision 7: release counts", "",
         f"Hugging Face, fixed list of {H['labs_tried']} labs (failed: {', '.join(H['labs_failed']) or 'none'}): "
         f"{H['repos_seen']:,} repositories seen, {H['dropped_as_derivative']:,} dropped as derivatives, "
         f"{H['llm_repos_kept']:,} language-model repositories kept since January 2023.", "",
         "| Quarter | Hugging Face (labs) | Epoch open-weight (all) | Epoch open-weight (notable) |", "|---|---|---|---|"]
    qs = sorted(set(H["per_quarter"]) | set(E["all"].get("open_weight_per_quarter", {})))
    for q in qs:
        L.append(f"| {q} | {H['per_quarter'].get(q, 0)} | {E['all'].get('open_weight_per_quarter', {}).get(q, 0)} | "
                 f"{E['notable'].get('open_weight_per_quarter', {}).get(q, 0)} |")
    L += ["", "By lab (Hugging Face, kept): " + ", ".join(f"{k} {v}" for k, v in H["per_lab"].items()), "",
          "Most recent kept: " + "; ".join(f"{r['id']} ({r['created']})" for r in H["sample_recent"]), "",
          f"Epoch accessibility values (all models): {E['all'].get('accessibility_values')}", "",
          "## Decision 8: candidate benchmarks", "",
          "| Benchmark file | Kind | Models scored | Open-weight scored | First date | Best | Open-weight at 20/30/40/50/60 |",
          "|---|---|---|---|---|---|---|"]
    for c in B["candidates"]:
        L.append(f"| {c['file']} | {c['kind']} | {c['models_scored']} | {c['open_weight_scored']} | {c['first_date']} | "
                 f"{c['best']} | " + "/".join(str(c['bars'][b]['open_weight']) for b in ('20', '30', '40', '50', '60')) + " |")
    L += ["", f"All benchmark files in Epoch's data: {len(B['files'])} (largest: "
          + ", ".join(f"{f['file']} {f['rows']}" for f in B["files"][:12]) + ").", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start"); ap.add_argument("--end")
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    R = {"hub": hub()}
    R["epoch"], models = epoch_models()
    R["bench"] = epoch_benchmarks(models)
    (a.out / "x12_evidence.json").write_text(json.dumps(R, indent=1, default=str))
    (a.out / "summary.md").write_text(report(R))
    print("x12_evidence: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
