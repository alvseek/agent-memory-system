#!/bin/bash
# Claude Code Memory Refresh After Compaction
# This hook fires after context compaction to do memory restoration

echo "{
  \"continue\": true,
  \"hookSpecificOutput\": {
    \"hookEventName\": \"PreCompact\",/
    \"additionalContext\": \"Update your episodic memory immediately before getting compacted!\"
  }
}"