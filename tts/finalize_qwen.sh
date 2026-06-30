#!/bin/bash
cd /mnt/data_4tb/handbook-rs
source /home/abxda/miniconda3/etc/profile.d/conda.sh
LOG=/tmp/claude-1000/-mnt-data-4tb-handbook-rs/0969678b-6ce6-4dce-bf38-7eae9432d7c2/scratchpad/gen_qwen_full.log
echo "[finalize-qwen] esperando fin de generación Qwen..."
until grep -q QWEN_FULL_DONE "$LOG" 2>/dev/null; do sleep 60; done
echo "[finalize-qwen] generación lista ($(ls out/audio/qwen/*.mp3 | wc -l) clips)"
echo "[finalize-qwen] QA inversa completa de Qwen"
conda run -n stt-whisper python tts/qa_stt.py qwen large-v3
for r in 1 2 3; do
  n=$(wc -l < out/audio/qwen/qa_flagged.txt 2>/dev/null || echo 0)
  echo "[finalize-qwen] ronda $r: $n marcados"
  [ "$n" -le 0 ] && break
  conda run -n tts-qwen python tts/regen_flagged_qwen.py qwen
  conda run -n stt-whisper python tts/qa_stt.py qwen large-v3 --only out/audio/qwen/qa_flagged.txt
done
FLAGGED=$(wc -l < out/audio/qwen/qa_flagged.txt 2>/dev/null || echo 0)
echo "[finalize-qwen] QA final: $FLAGGED marcados restantes; regenerando app y subiendo"
PYTHONPATH=src .venv/bin/python -c "from handbook_rs.stage9_app import run; run(force=True)"
git add -A
git -c user.name="abxda" -c user.email="acoronadoiruegas@gmail.com" commit -q -m "Add QA-verified complete Qwen3-TTS audio corpus

Full Qwen (ryan) corpus after STT reverse-check + garbage-clip regeneration.
Remaining flagged after QA loop: $FLAGGED.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no" git push origin main
echo "QWEN_FINALIZE_DONE flagged=$FLAGGED pushed=yes"
