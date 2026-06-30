import os, json, time
os.environ["COQUI_TOS_AGREED"]="1"
import torch, numpy as np
import transformers.pytorch_utils as _pu
if not hasattr(_pu,"isin_mps_friendly"):
    def isin_mps_friendly(elements,test_elements): return torch.isin(elements,test_elements)
    _pu.isin_mps_friendly=isin_mps_friendly
from TTS.api import TTS
ont=json.load(open("out/ontology.json")); nodes={n["id"]:n for n in ont["nodes"]}
ids=["data","ndvi","machine-learning"]
tts=TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda"); SR=tts.synthesizer.output_sample_rate
# warmup
tts.tts(text="warm up.", speaker="Damien Black", language="en")
tot_gen=tot_aud=0
for cid in ids:
    for lang in ("en","es"):
        txt=f"{nodes[cid]['name'][lang]}. {nodes[cid]['definition'][lang]}"
        t=time.time(); w=np.asarray(tts.tts(text=txt, speaker="Damien Black", language=lang)); g=time.time()-t
        aud=len(w)/SR; tot_gen+=g; tot_aud+=aud
        print(f"  XTTS {cid}_{lang}: gen={g:.2f}s audio={aud:.2f}s RTF={g/aud:.2f}", flush=True)
print(f"XTTS_TOTAL gen={tot_gen:.1f}s for {tot_aud:.1f}s audio | avg {tot_gen/6:.2f}s/clip | RTF={tot_gen/tot_aud:.2f}", flush=True)
