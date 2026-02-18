#!/bin/bash
# Claude Code Memory Refresh After Compaction
# This hook fires after context compaction to do memory restoration

echo "{
  \"continue\": true,
  \"hookSpecificOutput\": {
    \"hookEventName\": \"SessionStart\",
    \"additionalContext\": \"OH NO! My memory has been compacted! I need to execute the ## **MEMORY RECOVERY AFTER COMPACTION** **UUID**: 176b0df7-036f-48f9-927d-432e27cd4116 POST-COMPACT PROTOCOL!\"
  }
}"