#!/bin/bash
cd /mnt/data_4tb/handbook-rs
source /home/abxda/miniconda3/etc/profile.d/conda.sh
LOG=/tmp/claude-1000/-mnt-data-4tb-handbook-rs/0969678b-6ce6-4dce-bf38-7eae9432d7c2/scratchpad/gen_qwen_full.log
echo "[finalize-qwen] esperando fin de generación Qwen..."
until grep -q QWEN_FULL_DONE "$LOG" 2>/dev/null; do sleep 60; done
echo "[finalize-qwen] generación lista ($(ls out/audio/qwen/*.mp3 | wc -l) clips); regenerando app"
PYTHONPATH=src .venv/bin/python -c "from handbook_rs.stage9_app import run; run(force=True)"
echo "[finalize-qwen] QA inversa de Qwen (Whisper large-v3)"
conda run -n stt-whisper python tts/qa_stt.py qwen large-v3
echo "QWEN_FINALIZE_DONE flagged=$(wc -l < out/audio/qwen/qa_flagged.txt 2>/dev/null || echo 0)"
