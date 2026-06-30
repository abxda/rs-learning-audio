import os, json
os.environ["COQUI_TOS_AGREED"] = "1"
import torch
# shim: provide isin_mps_friendly removed from newer transformers (coqui-tts tortoise needs it)
import transformers.pytorch_utils as _pu
if not hasattr(_pu, "isin_mps_friendly"):
    def isin_mps_friendly(elements, test_elements):
        return torch.isin(elements, test_elements)
    _pu.isin_mps_friendly = isin_mps_friendly
from TTS.api import TTS

OUT = "out/tts_samples"
ont = json.load(open("out/ontology.json")); nodes = {n["id"]: n for n in ont["nodes"]}
ids = ["remote-sensing", "ndvi"]
VOICES = {"female": "Ana Florence", "male": "Damien Black"}
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda" if torch.cuda.is_available() else "cpu")
avail = list(tts.synthesizer.tts_model.speaker_manager.name_to_id)
print("speakers:", avail[:15])
for tag, spk in VOICES.items():
    if spk not in avail: spk = avail[0]
    for cid in ids:
        n = nodes[cid]
        for lang in ("en", "es"):
            txt = f"{n['name'][lang]}. {n['definition'][lang]}"
            fp = f"{OUT}/{cid}_{lang}_xtts_{tag}.wav"
            tts.tts_to_file(text=txt, speaker=spk, language=lang, file_path=fp); print("wrote", fp)
print("XTTS_SAMPLES_DONE")
