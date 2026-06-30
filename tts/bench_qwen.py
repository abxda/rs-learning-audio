import json, time
import torch, numpy as np
from qwen_tts import Qwen3TTSModel
ont=json.load(open("out/ontology.json")); nodes={n["id"]:n for n in ont["nodes"]}
ids=["data","ndvi","machine-learning"]; LANG={"en":"English","es":"Spanish"}
m=Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice", device_map="cuda:0",
                                torch_dtype=torch.bfloat16, trust_remote_code=True)
spk="ryan"
m.generate_custom_voice("warm up.", language="English", speaker=spk)  # warmup
tot_gen=tot_aud=0
for cid in ids:
    for lang in ("en","es"):
        txt=f"{nodes[cid]['name'][lang]}. {nodes[cid]['definition'][lang]}"
        t=time.time(); wavs,sr=m.generate_custom_voice(txt, language=LANG[lang], speaker=spk); g=time.time()-t
        w=wavs[0]; w=w.detach().cpu().numpy() if hasattr(w,"detach") else np.asarray(w)
        aud=len(w)/sr; tot_gen+=g; tot_aud+=aud
        print(f"  QWEN {cid}_{lang}: gen={g:.2f}s audio={aud:.2f}s RTF={g/aud:.2f}", flush=True)
print(f"QWEN_TOTAL gen={tot_gen:.1f}s for {tot_aud:.1f}s audio | avg {tot_gen/6:.2f}s/clip | RTF={tot_gen/tot_aud:.2f}", flush=True)
