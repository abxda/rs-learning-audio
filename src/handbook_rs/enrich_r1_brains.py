"""R1 — synthesize the 14 thematic 'documentary brains' (+1 Platform) from the
Handbook concepts, the book's own bibliography (R0 seeds) and verified deep-research
evidence. DeepSeek writes bilingual brains citing ONLY the provided verified refs.

Output: out/brains/<slug>.md (bilingual) + build/brains/brain_<idx>.json + index.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .config import build_dir, out_dir
from .io_utils import read_json, write_json
from .llm.client import chat
from .norms import slugify

BRAIN_SYS = (
    "You are a bilingual (EN/ES) scientific editor building a 'documentary brain' for a learning "
    "theme in a course on Remote Sensing for Agricultural Statistics. The UN Handbook is the "
    "backbone; deep research is ADDITIVE and must cite ONLY the provided verified references by "
    "their [Rn] tag (never invent references or URLs). Output strict JSON only."
)


def _theme_refs(theme_evidence: dict, seed_refs: list[dict], max_seed: int = 5) -> tuple[str, list]:
    """Combine deep-research refs (with URL) + top Handbook bibliography seeds (with DOI)."""
    refs, lines = [], []
    n = 1
    for r in theme_evidence.get("refs", []):
        refs.append({"tag": f"R{n}", "text": r["t"], "url": r["u"], "kind": "deep-research"})
        lines.append(f"[R{n}] {r['t']}. {r['u']}")
        n += 1
    seeds = [s for s in seed_refs if s.get("dois")][:max_seed]
    for s in seeds:
        url = s.get("url") or (f"https://doi.org/{s['dois'][0]}" if s["dois"] else "")
        refs.append({"tag": f"R{n}", "text": s["text"][:160], "url": url, "kind": "handbook-bibliography"})
        lines.append(f"[R{n}] (Handbook bibliography) {s['text'][:150]} {url}")
        n += 1
    return "\n".join(lines), refs


def _synth(idx: str, theme: dict, evid: dict, by_id: dict, compact: bool = False) -> dict:
    members = theme.get("members") or theme.get("reps", [])
    enrich_ids = members[: (3 if compact else 4)]
    concept_block = "\n".join(
        f"- {m} ({by_id[m]['name']['en']}): {by_id[m]['definition']['en'][:140]}"
        for m in members if m in by_id)
    refs_block, refs = _theme_refs(evid, theme.get("refs", []))
    title_en = theme["title"]["en"] if isinstance(theme["title"], dict) else theme["title"]
    words = "350-450" if compact else "420-560"
    plat = " (NOTE: this theme is the Handbook's reproducibility PLATFORM/infrastructure, not an Earth-observation method; disambiguate clearly and cite the 'howto' page)" if evid.get("is_platform") else ""
    user = f"""THEME: {title_en}{plat}

HANDBOOK CONCEPTS (backbone - keep canonical):
{concept_block}

VERIFIED RESEARCH FINDINGS (deep research):
{evid.get('findings','')}

VERIFIED REFERENCES (cite ONLY these as [Rn]):
{refs_block}

Produce JSON (keep it concise so it is valid and complete):
{{"brain_en":"<{words} word markdown: overview; key methods/distinctions grounded in science; how it grounds the Handbook concepts (short bullets by concept id); what GAP it fills; cite [Rn] inline>",
"brain_es":"<same in natural Spanish>",
"enrich":[{{"id":"<concept id>","disambiguation_en":"<1 sentence>","disambiguation_es":"<es>","enrich_en":"<=40 words added scientific layer, cite [Rn]>","enrich_es":"<es>","refs":["R1"]}}]}}
Include one enrich entry for EACH of these ids only: {", ".join(enrich_ids)}."""
    res = chat(BRAIN_SYS, user, json_mode=True, max_tokens=8000)
    d = res.json()
    return {"idx": idx, "title": theme["title"], "slug": slugify(title_en),
            "members": members, "refs": refs, "call_id": res.call_id,
            "brain_en": d.get("brain_en", ""), "brain_es": d.get("brain_es", ""),
            "enrich": d.get("enrich", [])}


def run(force: bool = False) -> Path:
    bdir = build_dir() / "brains"; bdir.mkdir(parents=True, exist_ok=True)
    odir = out_dir() / "brains"; odir.mkdir(parents=True, exist_ok=True)
    idx_out = bdir / "index.json"
    if idx_out.exists() and not force:
        print("R1 cached.")
        return idx_out

    r0 = read_json(build_dir() / "R0_references.json")
    themes = {str(t["idx"]): t for t in r0["themes"]}
    evidence = {}
    for b in ("R1_evidence_b1.json", "R1_evidence_b2.json", "R1_evidence_b3.json"):
        evidence.update(read_json(build_dir() / b))
    ont = read_json(out_dir() / "ontology.json"); by_id = {n["id"]: n for n in ont["nodes"]}

    # platform theme (idx 14) is not in clusters; build a synthetic theme entry
    if "14" in evidence and "14" not in themes:
        e = evidence["14"]
        themes["14"] = {"idx": 14, "title": {"en": e["title"], "es": "Plataforma y Reproducibilidad"},
                        "desc": {"en": "", "es": ""}, "reps": e["members"], "members": e["members"], "refs": []}

    order = [str(i) for i in range(15) if str(i) in evidence]
    print(f"  synthesizing {len(order)} brains ...")

    def do(idx):
        th = dict(themes[idx])
        if evidence[idx].get("members"):
            th["members"] = evidence[idx]["members"]
        try:
            return _synth(idx, th, evidence[idx], by_id)
        except Exception as e1:  # noqa: BLE001 — retry compact, then give up gracefully
            print(f"  ! brain {idx} failed ({str(e1)[:50]}); retrying compact", flush=True)
            try:
                return _synth(idx, th, evidence[idx], by_id, compact=True)
            except Exception as e2:  # noqa: BLE001
                print(f"  !! brain {idx} failed again ({str(e2)[:50]})", flush=True)
                return None

    with ThreadPoolExecutor(max_workers=6) as ex:
        brains = [b for b in ex.map(do, order) if b]

    index = []
    for b in brains:
        refs_md = "\n".join(f"[{r['tag']}] {r['text']} — {r['url']}  *({r['kind']})*" for r in b["refs"])
        title = b["title"]["en"] if isinstance(b["title"], dict) else b["title"]
        title_es = b["title"]["es"] if isinstance(b["title"], dict) else title
        md = (f"# 🧠 {title} / {title_es}\n\n> Cerebro documental — el Handbook es la columna; "
              f"la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; "
              f"research is additive and cited.*\n\n## English\n\n{b['brain_en']}\n\n## Español\n\n"
              f"{b['brain_es']}\n\n## Referencias verificadas / Verified references\n{refs_md}\n")
        (odir / f"{b['slug']}.md").write_text(md, encoding="utf-8")
        write_json(bdir / f"brain_{b['idx']}.json", b)
        index.append({"idx": int(b["idx"]), "title": b["title"], "slug": b["slug"],
                      "file": f"brains/{b['slug']}.md", "n_refs": len(b["refs"]),
                      "n_enrich": len(b["enrich"]), "members": b["members"]})
        print(f"  [{b['idx']:>2}] {title:34s} refs={len(b['refs'])} enrich={len(b['enrich'])}")

    index.sort(key=lambda x: x["idx"])
    write_json(idx_out, {"brains": index})
    write_json(odir.parent / "brains_index.json", {"brains": index})
    print(f"R1 done: {len(index)} brains -> {odir}")
    return idx_out


if __name__ == "__main__":
    run()
