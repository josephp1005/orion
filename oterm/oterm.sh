#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

CURR_DATE="$(date +%Y%m%d_%H%M%S)"

script "$ORION_HOME/oterm/logs/mysession_$CURR_DATE.log"

# This runs AFTER the user exits the subshell
sed -i '' -E "s/$(printf '\033')\\[[0-9;?]*[A-Za-z]//g" $ORION_HOME/oterm/logs/mysession_$CURR_DATE.log
echo "Session ended, updating orion..."
cd "$ORION_HOME"
python3 -c "from dense_embeddings import terminal_pipeline; terminal_pipeline()"
