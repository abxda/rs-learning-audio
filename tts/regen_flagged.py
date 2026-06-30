"""Regenerate flagged XTTS clips: clean abbreviations/units/parentheses, split into
sentences, synthesize each separately. Reads out/audio/<model>/qa_flagged.txt."""
import os, json, subprocess, tempfile, sys, re
os.environ["COQUI_TOS_AGREED"] = "1"
import torch, numpy as np, soundfile as sf
import transformers.pytorch_utils as _pu
if not hasattr(_pu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)
    _pu.isin_mps_friendly = isin_mps_friendly
from TTS.api import TTS

MODEL = sys.argv[1] if len(sys.argv) > 1 else "xtts"
ADIR = f"out/audio/{MODEL}"; SPK = "Damien Black"
ont = json.load(open("out/ontology.json")); nodes = {n["id"]: n for n in ont["nodes"]}
flag_file = f"{ADIR}/qa_flagged.txt"
if not os.path.exists(flag_file):
    print("no qa_flagged.txt; nothing to regen"); sys.exit(0)
items = [l.split()[0] for l in open(flag_file) if l.strip()]
print(f"regenerating {len(items)} flagged clips (clean+sentence-split)", flush=True)

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")
SR = tts.synthesizer.output_sample_rate

def clean_for_tts(text, lang):
    t = re.sub(r"\bp\.\s*ej\.?,?", "por ejemplo,", text, flags=re.I)
    t = re.sub(r"\be\.\s*g\.?,?", "for example,", t, flags=re.I)
    t = re.sub(r"\bi\.\s*e\.?,?", "that is,", t, flags=re.I)
    t = t.replace("(", ", ").replace(")", ", ")
    unit = " micrómetros " if lang == "es" else " micrometers "
    t = t.replace("µm", unit).replace("μm", unit).replace("nm", " nanómetros " if lang=="es" else " nanometers ")
    t = re.sub(r"(\d)\s*[-–]\s*(\d)", (r"\1 a \2" if lang == "es" else r"\1 to \2"), t)
    t = re.sub(r"\s*,(\s*,)+", ", ", t)
    return re.sub(r"\s+", " ", t).strip()

def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    out = []
    for p in parts:
        p = p.strip()
        if len(p) > 200:
            out += [c.strip() for c in re.split(r"(?<=[;,])\s+", p) if c.strip()]
        elif p:
            out.append(p)
    return out

gap = np.zeros(int(SR * 0.12), dtype=np.float32)
def mp3(wav, dst):
    subprocess.run(["ffmpeg","-y","-i",wav,"-codec:a","libmp3lame","-q:a","6","-ar","24000",dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for base in items:
    cid, lang = base.rsplit("_", 1)
    if cid not in nodes or lang not in ("en", "es"): continue
    text = clean_for_tts(f"{nodes[cid]['name'][lang]}. {nodes[cid]['definition'][lang]}", lang)
    chunks = sentences(text)
    pieces = []
    for ch in chunks:
        w = np.asarray(tts.tts(text=ch, speaker=SPK, language=lang), dtype=np.float32)
        pieces.append(w); pieces.append(gap)
    audio = np.concatenate(pieces) if pieces else np.zeros(1, dtype=np.float32)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf: wav = tf.name
    sf.write(wav, audio, SR); mp3(wav, f"{ADIR}/{base}.mp3"); os.remove(wav)
    print(f"regen {base} ({len(chunks)} chunks): {text[:70]}", flush=True)
print("REGEN_DONE", flush=True)
