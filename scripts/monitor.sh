#!/bin/bash
# Monitor et restart le job poubelles si nécessaire
LOG="$HOME/.openclaw/workspace/output/poubelles/haloscan_run.log"
PID_FILE="$HOME/.openclaw/workspace/output/poubelles/haloscan.pid"
PYTHON="/home/ubuntu/.venv/bin/python3"
SCRIPT="$HOME/.openclaw/workspace/scripts/poubelles_pages.py"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "$(date) — Job Haloscan en cours (PID $PID), rien à faire" >> "$LOG"
        exit 0
    fi
fi

# Vérifier s'il reste des pages à enrichir
REMAINING=$(${PYTHON} ${SCRIPT} --phase stats 2>/dev/null | grep "Enrichies" | awk '{print $3}')
echo "$(date) — Job terminé ou absent. Relance..." >> "$LOG"
nohup ${PYTHON} ${SCRIPT} --phase haloscan --limit 300 >> "$LOG" 2>&1 &
echo $! > "$PID_FILE"
