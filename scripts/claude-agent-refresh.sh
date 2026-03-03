#!/bin/bash
# Claude Code Memory Refresh After Compaction
# This hook fires after context compaction to do memory restoration

echo "{
  \"continue\": true,
  \"hookSpecificOutput\": {
    \"hookEventName\": \"SessionStart\",
    \"additionalContext\": \"Wait! I made a mistake! Instead of continuing without asking further question, I first need to execute /refresh-memory [your agent domain] then continue after ONLY if everything is clear and no need to clarify anything!\"
  }
}"