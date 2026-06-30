import os, json, subprocess, tempfile, sys
import torch, soundfile as sf, numpy as np
from qwen_tts import Qwen3TTSModel

MODEL = "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
OUT = "out/audio/qwen"; os.makedirs(OUT, exist_ok=True)
PREF_SPK = os.environ.get("QWEN_SPEAKER", "Ryan")
LANG = {"en": "English", "es": "Spanish"}
# concepts to generate (overlap with XTTS so you can A/B in the app)
IDS = sys.argv[1:] or ["remote-sensing","ndvi","data","crop","area","accuracy",
                       "machine-learning","random-forest","satellite","classification"]

model = Qwen3TTSModel.from_pretrained(MODEL, device_map="cuda:0",
                                      torch_dtype=torch.bfloat16, trust_remote_code=True)
speakers = model.get_supported_speakers()
print("SUPPORTED_SPEAKERS:", speakers, flush=True)
print("SUPPORTED_LANGS:", model.get_supported_languages(), flush=True)
spk = PREF_SPK if PREF_SPK in speakers else speakers[0]
print("USING_SPEAKER:", spk, flush=True)

ont = json.load(open("out/ontology.json")); nodes = {n["id"]: n for n in ont["nodes"]}
def to_np(w):
    return w.detach().cpu().numpy() if hasattr(w, "detach") else np.asarray(w)
def mp3(wav, dst):
    subprocess.run(["ffmpeg","-y","-i",wav,"-codec:a","libmp3lame","-q:a","6","-ar","24000",dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for cid in IDS:
    if cid not in nodes: continue
    n = nodes[cid]
    for lang in ("en","es"):
        dst = f"{OUT}/{cid}_{lang}.mp3"
        if os.path.exists(dst): continue
        txt = f"{n['name'][lang]}. {n['definition'][lang]}".strip()
        try:
            wavs, sr = model.generate_custom_voice(txt, language=LANG[lang], speaker=spk)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf: wav = tf.name
            sf.write(wav, to_np(wavs[0]), sr); mp3(wav, dst); os.remove(wav)
            print("wrote", dst, flush=True)
        except Exception as e:
            print("FAIL", cid, lang, str(e)[:120], flush=True)
print("QWEN_DONE", flush=True)
