#!/bin/bash
# Codex Memory Refresh Reminder Hook
# This hook injects developer context at session start (startup/resume/clear)
# to remind the agent to run memory recovery first.

echo '{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Wait! I made a mistake! Instead of continuing without asking further question, I first need to execute /refresh-memory [your agent domain] then continue after ONLY if everything is clear and no need to clarify anything!"
  }
}'
