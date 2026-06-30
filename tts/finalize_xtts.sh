#!/bin/bash
cd /mnt/data_4tb/handbook-rs
source /home/abxda/miniconda3/etc/profile.d/conda.sh
LOG=/tmp/claude-1000/-mnt-data-4tb-handbook-rs/0969678b-6ce6-4dce-bf38-7eae9432d7c2/scratchpad/gen_full2.log
echo "[finalize] esperando fin de generación XTTS..."
until grep -q FULL_DONE "$LOG" 2>/dev/null; do sleep 30; done
echo "[finalize] generación lista ($(ls out/audio/xtts/*.mp3 | wc -l) clips); regenerando app"
PYTHONPATH=src .venv/bin/python -c "from handbook_rs.stage9_app import run; run(force=True)"
echo "[finalize] QA completa (Whisper large-v3)"
conda run -n stt-whisper python tts/qa_stt.py xtts large-v3
for r in 1 2 3; do
  n=$(wc -l < out/audio/xtts/qa_flagged.txt 2>/dev/null || echo 0)
  echo "[finalize] ronda $r: $n marcados"
  [ "$n" -le 0 ] && break
  conda run -n tts-xtts python tts/regen_flagged.py xtts
  conda run -n stt-whisper python tts/qa_stt.py xtts large-v3 --only out/audio/xtts/qa_flagged.txt
done
PYTHONPATH=src .venv/bin/python -c "from handbook_rs.stage9_app import run; run(force=True)"
echo "FINALIZE_DONE flagged_final=$(wc -l < out/audio/xtts/qa_flagged.txt 2>/dev/null || echo 0)"
