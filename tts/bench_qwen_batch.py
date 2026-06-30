import json, time
import torch, numpy as np
from qwen_tts import Qwen3TTSModel
ont=json.load(open("out/ontology.json")); nodes=ont["nodes"]
# pick 8 ES texts of varied length
ids=[n["id"] for n in nodes[:8]]
texts=[f"{nodes[i]['name']['es']}. {nodes[i]['definition']['es']}" for i in range(8)]
m=Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice", device_map="cuda:0",
                                torch_dtype=torch.bfloat16, trust_remote_code=True)
spk="ryan"
m.generate_custom_voice("calienta.", language="Spanish", speaker=spk)
def dur(wavs,sr): 
    return sum((len(w.detach().cpu().numpy()) if hasattr(w,'detach') else len(np.asarray(w))) for w in wavs)/sr
for B in (4, 8):
    batch=texts[:B]
    t=time.time(); wavs,sr=m.generate_custom_voice(batch, language="Spanish", speaker=spk); g=time.time()-t
    aud=dur(wavs,sr)
    print(f"BATCH={B}: total_gen={g:.1f}s  audio={aud:.1f}s  por_clip={g/B:.2f}s  (vs ~23s/clip secuencial)", flush=True)
print("BATCH_DONE", flush=True)
