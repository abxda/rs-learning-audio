"""Reverse check: transcribe each generated mp3 and compare with the source text.
Detects BOTH missing content (truncation/omission) and garbage (insertions/loops).
Usage: python tts/qa_stt.py <model> [whisper_size] [--only <listfile>]
  --only re-QAs only the clips in listfile (id_lang per line) and updates the report."""
import os, sys, json, glob, re, unicodedata, html
from difflib import SequenceMatcher
from faster_whisper import WhisperModel

args = sys.argv[1:]
ONLY = None
if "--only" in args:
    i = args.index("--only"); ONLY = args[i+1]; del args[i:i+2]
MODEL = args[0] if len(args) > 0 else "xtts"
WSIZE = args[1] if len(args) > 1 else "large-v3"
ADIR = f"out/audio/{MODEL}"
ont = json.load(open("out/ontology.json")); nodes = {n["id"]: n for n in ont["nodes"]}

def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()

def max_ngram_repeat(words, n=4):
    if len(words) < n: return 1
    c = {}
    for i in range(len(words)-n+1):
        g = tuple(words[i:i+n]); c[g] = c.get(g, 0) + 1
    return max(c.values())

def analyze(ref, hyp):
    r, h = norm(ref).split(), norm(hyp).split()
    sm = SequenceMatcher(None, r, h); dele = ins = sub = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "delete": dele += i2-i1
        elif tag == "insert": ins += j2-j1
        elif tag == "replace": sub += max(i2-i1, j2-j1)
    nr = max(1, len(r))
    del_rate, ins_rate, sub_rate = dele/nr, ins/nr, sub/nr
    len_ratio = len(h)/nr; rep = max_ngram_repeat(h)
    reasons = []
    if del_rate > 0.18 or len_ratio < 0.82: reasons.append("FALTA_CONTENIDO")
    if ins_rate > 0.22 or len_ratio > 1.25 or rep >= 3: reasons.append("BASURA")
    if sub_rate > 0.30 and not reasons: reasons.append("DIFERENCIAS")
    return {"similarity": round(sm.ratio(), 3), "wer": round((dele+ins+sub)/nr, 3),
            "del_rate": round(del_rate, 3), "ins_rate": round(ins_rate, 3),
            "len_ratio": round(len_ratio, 3), "ngram_repeat": rep,
            "flag": bool(reasons), "reasons": reasons}

def qa_clip(w, cid, lang):
    src = f"{nodes[cid]['name'][lang]}. {nodes[cid]['definition'][lang]}"
    segs, _ = w.transcribe(f"{ADIR}/{cid}_{lang}.mp3", language=lang, beam_size=5)
    hyp = " ".join(s.text for s in segs).strip()
    a = analyze(src, hyp); a.update({"id": cid, "lang": lang, "source": src, "transcript": hyp})
    return a

def write_outputs(rows):
    rows.sort(key=lambda r: (not r["flag"], r["similarity"]))
    flagged = [r for r in rows if r["flag"]]
    miss = [r for r in flagged if "FALTA_CONTENIDO" in r["reasons"]]
    junk = [r for r in flagged if "BASURA" in r["reasons"]]
    mean = round(sum(r["similarity"] for r in rows)/max(1, len(rows)), 3)
    json.dump({"model": MODEL, "whisper": WSIZE, "clips": len(rows), "mean_similarity": mean,
               "flagged": len(flagged), "missing_content": len(miss), "garbage": len(junk),
               "rows": rows}, open(f"{ADIR}/qa_report.json", "w"), ensure_ascii=False, indent=2)
    with open(f"{ADIR}/qa_flagged.txt", "w") as f:
        for r in flagged: f.write(f"{r['id']}_{r['lang']} {','.join(r['reasons'])}\n")
    esc = lambda s: html.escape(s or "")
    cards = "".join(
        f"<div class='c {'bad' if r['flag'] else ''}'><div class=h><b>{esc(r['id'])}</b> · {r['lang'].upper()} "
        f"· sim={r['similarity']} · falta={r['del_rate']} · basura={r['ins_rate']} · rep={r['ngram_repeat']} "
        f"{('⚠️ '+','.join(r['reasons'])) if r['flag'] else '✅'} "
        f"<audio controls preload=none src='{r['id']}_{r['lang']}.mp3'></audio></div>"
        f"<div class=s><b>texto:</b> {esc(r['source'])}</div>"
        f"<div class=t><b>STT:</b> {esc(r['transcript'])}</div></div>" for r in rows)
    open(f"{ADIR}/qa.html", "w").write(
        f"<!doctype html><meta charset=utf-8><title>QA {MODEL}</title>"
        "<style>body{font-family:system-ui;max-width:920px;margin:20px auto;padding:0 14px}"
        ".c{border:1px solid #ddd;border-radius:10px;padding:10px 12px;margin:8px 0}.c.bad{border-color:#c62828;background:#fff5f5}"
        ".h{font-size:.86rem;margin-bottom:6px}.s{color:#222}.t{color:#666}audio{height:30px;vertical-align:middle}</style>"
        f"<h1>🔎 Revisión inversa STT — {MODEL}</h1>"
        f"<p>{len(rows)} clips · similitud media <b>{mean}</b> · marcados <b>{len(flagged)}</b> "
        f"(faltantes: {len(miss)}, basura: {len(junk)}) · Whisper {WSIZE}</p>{cards}")
    return mean, len(flagged), len(miss), len(junk)

w = WhisperModel(WSIZE, device="cuda", compute_type="float16")
if ONLY:
    rep = json.load(open(f"{ADIR}/qa_report.json"))
    rows = rep["rows"]; idx = {(r["id"], r["lang"]): r for r in rows}
    targets = [l.split()[0] for l in open(ONLY) if l.strip()]
    print(f"re-QA {len(targets)} clips (--only)", flush=True)
    for t in targets:
        cid, lang = t.rsplit("_", 1)
        if cid in nodes and lang in ("en", "es") and os.path.exists(f"{ADIR}/{cid}_{lang}.mp3"):
            a = qa_clip(w, cid, lang)
            if (cid, lang) in idx:
                idx[(cid, lang)].update(a)
            else:
                rows.append(a); idx[(cid, lang)] = a   # clip was missing from prior report
    mean, fl, miss, junk = write_outputs(rows)
else:
    files = sorted(glob.glob(f"{ADIR}/*.mp3"))
    print(f"QA {MODEL}: {len(files)} clips with whisper {WSIZE}", flush=True)
    rows = []
    for i, fp in enumerate(files):
        cid, lang = os.path.basename(fp)[:-4].rsplit("_", 1)
        if cid in nodes and lang in ("en", "es"):
            rows.append(qa_clip(w, cid, lang))
        if (i+1) % 50 == 0: print(f"  {i+1}/{len(files)}", flush=True)
    mean, fl, miss, junk = write_outputs(rows)
print(f"QA_DONE model={MODEL} mean_sim={mean} flagged={fl} missing={miss} garbage={junk}", flush=True)
