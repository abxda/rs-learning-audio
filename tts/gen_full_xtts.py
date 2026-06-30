import os, json, subprocess, tempfile, sys, time
os.environ["COQUI_TOS_AGREED"] = "1"
import torch
import transformers.pytorch_utils as _pu
if not hasattr(_pu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)
    _pu.isin_mps_friendly = isin_mps_friendly
from TTS.api import TTS

OUT = "out/audio/xtts"; os.makedirs(OUT, exist_ok=True)
SPK = "Damien Black"
ont = json.load(open("out/ontology.json"))
nodes = ont["nodes"]
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

def mp3(wav, dst):
    subprocess.run(["ffmpeg","-y","-i",wav,"-codec:a","libmp3lame","-q:a","6","-ar","24000",dst],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total = len(nodes)*2; done=0; fail=0; t0=time.time()
for i, n in enumerate(nodes):
    for lang in ("en","es"):
        dst = f"{OUT}/{n['id']}_{lang}.mp3"
        if os.path.exists(dst):
            done+=1; continue
        txt = f"{n['name'][lang]}. {n['definition'][lang]}".strip()
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                wav = tf.name
            tts.tts_to_file(text=txt, speaker=SPK, language=lang, file_path=wav)
            mp3(wav, dst); os.remove(wav); done+=1
        except Exception as e:
            fail+=1; print(f"FAIL {n['id']} {lang}: {str(e)[:80]}", flush=True)
    if (i+1) % 20 == 0:
        el=time.time()-t0; rate=done/el if el else 0
        print(f"[{i+1}/{total//2}] done={done} fail={fail} {rate:.2f} clips/s eta={(total-done)/rate/60:.1f}min", flush=True)
print(f"FULL_DONE done={done} fail={fail}", flush=True)
