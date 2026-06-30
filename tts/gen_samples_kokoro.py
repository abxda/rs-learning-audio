import json, numpy as np, soundfile as sf
from kokoro import KPipeline

OUT = "out/tts_samples"
ont = json.load(open("out/ontology.json"))
nodes = {n["id"]: n for n in ont["nodes"]}
ids = ["remote-sensing", "ndvi"]
VOICE = {"en": ("a", "af_heart"), "es": ("e", "ef_dora")}  # (lang_code, voice)

pipes = {lc: KPipeline(lang_code=lc) for lc, _ in VOICE.values()}
for cid in ids:
    n = nodes[cid]
    for lang in ("en", "es"):
        lc, voice = VOICE[lang]
        txt = f"{n['name'][lang]}. {n['definition'][lang]}"
        audio = np.concatenate([a for _, _, a in pipes[lc](txt, voice=voice)])
        fp = f"{OUT}/{cid}_{lang}_kokoro.wav"
        sf.write(fp, audio, 24000)
        print("wrote", fp)
print("KOKORO_SAMPLES_DONE")
