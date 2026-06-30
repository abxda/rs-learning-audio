import json, numpy as np, soundfile as sf
from kokoro import KPipeline
ont=json.load(open("out/ontology.json")); nodes={n["id"]:n for n in ont["nodes"]}
VOICE={"en":("a","am_michael"),"es":("e","em_alex")}
pipes={lc:KPipeline(lang_code=lc) for lc,_ in VOICE.values()}
for cid in ["remote-sensing","ndvi"]:
    n=nodes[cid]
    for lang in ("en","es"):
        lc,v=VOICE[lang]; txt=f"{n['name'][lang]}. {n['definition'][lang]}"
        audio=np.concatenate([a for _,_,a in pipes[lc](txt,voice=v)])
        sf.write(f"out/tts_samples/{cid}_{lang}_kokoro2.wav",audio,24000); print("wrote",cid,lang)
print("KOKORO2_DONE")
