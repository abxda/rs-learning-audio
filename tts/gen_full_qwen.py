import os, json, subprocess, tempfile, time
import torch, soundfile as sf, numpy as np
from qwen_tts import Qwen3TTSModel
OUT = "out/audio/qwen"; os.makedirs(OUT, exist_ok=True)
SPK = os.environ.get("QWEN_SPEAKER", "ryan"); LANG = {"en": "English", "es": "Spanish"}
BATCH = int(os.environ.get("QWEN_BATCH", "4"))
ont = json.load(open("out/ontology.json")); nodes = ont["nodes"]
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice", device_map="cuda:0",
                                      torch_dtype=torch.bfloat16, trust_remote_code=True)
def to_np(w): return w.detach().cpu().numpy() if hasattr(w, "detach") else np.asarray(w)
def mp3(wav, dst):
    subprocess.run(["ffmpeg","-y","-i",wav,"-codec:a","libmp3lame","-q:a","6","-ar","24000",dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def save(cid, lang, w, sr):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf: wav = tf.name
    sf.write(wav, to_np(w), sr); mp3(wav, f"{OUT}/{cid}_{lang}.mp3"); os.remove(wav)

work = {"en": [], "es": []}
for n in nodes:
    for lang in ("en", "es"):
        if not os.path.exists(f"{OUT}/{n['id']}_{lang}.mp3"):
            work[lang].append((n["id"], f"{n['name'][lang]}. {n['definition'][lang]}".strip()))
todo = len(work["en"]) + len(work["es"])
print(f"to generate: {todo} (en={len(work['en'])}, es={len(work['es'])}), batch={BATCH}", flush=True)
model.generate_custom_voice("warm up.", language="English", speaker=SPK)

done = fail = 0; t0 = time.time()
for lang in ("en", "es"):
    items = work[lang]; lf = LANG[lang]
    for s in range(0, len(items), BATCH):
        chunk = items[s:s+BATCH]
        try:
            wavs, sr = model.generate_custom_voice([t for _, t in chunk], language=lf, speaker=SPK)
            for (cid, _), w in zip(chunk, wavs): save(cid, lang, w, sr); done += 1
        except Exception as e:
            torch.cuda.empty_cache()
            # fallback: one clip at a time (minimal memory)
            for cid, txt in chunk:
                try:
                    wavs, sr = model.generate_custom_voice([txt], language=lf, speaker=SPK)
                    save(cid, lang, wavs[0], sr); done += 1
                except Exception as e2:
                    torch.cuda.empty_cache(); fail += 1
                    print(f"FAIL {cid}_{lang}: {str(e2)[:70]}", flush=True)
        el = time.time()-t0; rate = done/el if el else 0
        print(f"[{done}/{todo}] {lang} fail={fail} {rate:.2f}/s eta={(todo-done)/rate/60 if rate else 0:.0f}min", flush=True)
print(f"QWEN_FULL_DONE done={done} fail={fail}", flush=True)
