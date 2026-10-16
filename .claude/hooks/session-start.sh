#!/bin/bash
# Install the YouTube skill's Python dependencies in Claude Code cloud sessions.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

python3 -m pip install --quiet --disable-pip-version-check --root-user-action=ignore \
  -r "$CLAUDE_PROJECT_DIR/.claude/skills/youtube/requirements.txt"
