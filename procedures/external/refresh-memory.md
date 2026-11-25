+++
format_version = 2
id = "refresh-memory"
kind = "external"
title = "Refresh Memory Dependencies"
description = "Dependency declaration only: the complete refresh-memory command remains on the legacy renderer."
+++
@start component id="refresh-memory.include-no-subagent-load" ref="procedures/components/no-subagent-load.md"
@end component
@start storage id="core-instruction-control-files.load-agent-memory" ref="procedures/memory/storage-backends/{backend}.md" target="core-instruction-control-files.load-agent-memory"
@end storage
@start component id="refresh-memory.include-core-instruction-control-files" ref="procedures/components/core-instruction-control-files.md"
@end component
