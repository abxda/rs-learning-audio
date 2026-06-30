"""Regenerate flagged Qwen clips: clean abbreviations/units, split into sentences,
synthesize with Qwen (sampling re-roll fixes most garbage). Reads qa_flagged.txt."""
import os, json, subprocess, tempfile, re
import torch, soundfile as sf, numpy as np
from qwen_tts import Qwen3TTSModel
ADIR = "out/audio/qwen"; SPK = os.environ.get("QWEN_SPEAKER", "ryan")
LANG = {"en": "English", "es": "Spanish"}
ont = json.load(open("out/ontology.json")); nodes = {n["id"]: n for n in ont["nodes"]}
flag = f"{ADIR}/qa_flagged.txt"
if not os.path.exists(flag):
    print("no qa_flagged.txt"); raise SystemExit
items = [l.split()[0] for l in open(flag) if l.strip()]
print(f"regenerating {len(items)} flagged Qwen clips", flush=True)
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice", device_map="cuda:0",
                                      torch_dtype=torch.bfloat16, trust_remote_code=True)
def to_np(w): return w.detach().cpu().numpy() if hasattr(w, "detach") else np.asarray(w)
def clean(text, lang):
    t = re.sub(r"\bp\.\s*ej\.?,?", "por ejemplo,", text, flags=re.I)
    t = re.sub(r"\be\.\s*g\.?,?", "for example,", t, flags=re.I)
    t = re.sub(r"\bi\.\s*e\.?,?", "that is,", t, flags=re.I)
    t = t.replace("(", ", ").replace(")", ", ")
    unit = " micrómetros " if lang == "es" else " micrometers "
    t = t.replace("µm", unit).replace("μm", unit)
    t = re.sub(r"(\d)\s*[-–]\s*(\d)", (r"\1 a \2" if lang == "es" else r"\1 to \2"), t)
    t = re.sub(r"\s*,(\s*,)+", ", ", t)
    return re.sub(r"\s+", " ", t).strip()
def sentences(text):
    out = []
    for p in re.split(r"(?<=[.!?])\s+", text.strip()):
        p = p.strip()
        if len(p) > 200: out += [c.strip() for c in re.split(r"(?<=[;,])\s+", p) if c.strip()]
        elif p: out.append(p)
    return out or [text]
def mp3(wav, dst):
    subprocess.run(["ffmpeg","-y","-i",wav,"-codec:a","libmp3lame","-q:a","6","-ar","24000",dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
for base in items:
    cid, lang = base.rsplit("_", 1)
    if cid not in nodes or lang not in ("en", "es"): continue
    text = clean(f"{nodes[cid]['name'][lang]}. {nodes[cid]['definition'][lang]}", lang)
    chunks = sentences(text)
    try:
        wavs, sr = model.generate_custom_voice(chunks, language=LANG[lang], speaker=SPK)
        gap = np.zeros(int(sr*0.12), dtype=np.float32)
        pieces = []
        for w in wavs: pieces += [to_np(w).astype(np.float32), gap]
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf: wav = tf.name
        sf.write(wav, np.concatenate(pieces), sr); mp3(wav, f"{ADIR}/{base}.mp3"); os.remove(wav)
        print(f"regen {base} ({len(chunks)} chunks)", flush=True)
    except Exception as e:
        torch.cuda.empty_cache(); print(f"FAIL {base}: {str(e)[:70]}", flush=True)
print("REGEN_DONE", flush=True)
