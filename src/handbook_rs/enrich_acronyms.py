"""Build a bilingual acronym glossary from the whole corpus (names, definitions,
bridges, brains). Each acronym -> {en, es} expansion via DeepSeek. The app shows,
on every concept card, the meaning of the acronyms it uses (a validation layer)."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from .config import build_dir, out_dir
from .io_utils import read_json, write_json
from .llm.client import chat

TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9]{1,8}")
STOP = {"NDVI"}  # placeholder; real filtering is by uppercase count below
COMMON = {"ID", "AI", "OK", "II", "III", "IV", "EO", "ML", "DL", "US", "UN"}  # keep short well-known too


def candidates(texts: list[str]) -> Counter:
    c: Counter = Counter()
    for t in texts:
        for tok in TOKEN.findall(t):
            up = sum(ch.isupper() for ch in tok)
            if up >= 2 and not tok.isupper() or (tok.isupper() and len(tok) >= 2 and up >= 2):
                # require >=2 uppercase letters (NDVI, SAR, TempCNN, EnKF, OBIA, WOFOST ...)
                if any(ch.isalpha() for ch in tok):
                    c[tok] += 1
    return c


def run(force: bool = False) -> Path:
    out = build_dir() / "acronyms.json"
    if out.exists() and not force:
        print("Acronyms cached.")
        return out

    ont = read_json(out_dir() / "ontology.json")
    texts: list[str] = []
    for n in ont["nodes"]:
        texts += [n["name"]["en"], n["name"]["es"], n["definition"]["en"], n["definition"]["es"]]
        texts += n["aliases"].get("en", []) + n["aliases"].get("es", [])
    for e in ont["edges"]:
        if e.get("bridge_en"):
            texts += [e["bridge_en"], e.get("bridge_es", "")]
    bdir = build_dir() / "brains"
    if bdir.exists():
        for f in bdir.glob("brain_*.json"):
            b = read_json(f)
            texts += [b.get("brain_en", ""), b.get("brain_es", "")]

    cand = candidates(texts)
    acrs = sorted([a for a, n in cand.items() if n >= 1], key=lambda a: (-cand[a], a))
    print(f"  {len(acrs)} candidate acronyms (top: {', '.join(acrs[:15])})")

    sys_p = ("You expand acronyms/abbreviations used in a course on Remote Sensing for Agricultural "
             "Statistics. For each token decide if it is a real acronym/abbreviation in this domain; "
             "if yes give its expansion in English and Spanish (translate the expansion, keep the acronym). "
             "If it is NOT an acronym (an ordinary word, a proper noun, or noise), omit it. JSON only.")
    result: dict[str, dict] = {}
    B = 50
    for i in range(0, len(acrs), B):
        batch = acrs[i:i + B]
        user = ("Expand these tokens. Return JSON {\"acronyms\":[{\"a\":\"<TOKEN>\",\"en\":\"<English "
                "expansion>\",\"es\":\"<Spanish expansion>\"}]} including ONLY real domain "
                "acronyms/abbreviations:\n" + "\n".join(batch))
        data = chat(sys_p, user, json_mode=True, max_tokens=6000).json()
        for it in data.get("acronyms", []):
            a = (it.get("a") or "").strip()
            if a and it.get("en"):
                result[a] = {"en": it["en"].strip(), "es": (it.get("es") or it["en"]).strip()}
        print(f"  expanded {min(i+B, len(acrs))}/{len(acrs)} -> {len(result)} real acronyms", flush=True)

    write_json(out, {"count": len(result), "acronyms": result})
    # tracked copy for reproducibility
    (out_dir().parent / "enrichment").mkdir(exist_ok=True)
    write_json(out_dir().parent / "enrichment" / "acronyms.json", {"count": len(result), "acronyms": result})
    print(f"Acronyms done: {len(result)} expansions -> {out}")
    print("  sample:", {k: result[k]["en"] for k in list(result)[:8]})
    return out


if __name__ == "__main__":
    run()
