#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.env"

script "$ORION_HOME/oterm/logs/mysession_$(date +%Y%m%d_%H%M%S).log"

# This runs AFTER the user exits the subshell
echo "Session ended, updating orion..."
cd "$ORION_HOME"
python3 -c "from dense_embeddings import terminal_pipeline; terminal_pipeline()"
