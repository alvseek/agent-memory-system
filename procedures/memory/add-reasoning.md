+++
format_version = 2
id = "add-reasoning"
kind = "procedure"
title = "Add Reasoning Memory Protocol"
description = "Capture anti-patterns and decision-making approaches as **lean, memorable** reasoning entries. *How* the store is read/written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics))."
argument_name = "context"
argument_description = "the reasoning pattern to document; asks if omitted"
+++
# Add Reasoning Memory Protocol

Capture anti-patterns and decision-making approaches as **lean, memorable** reasoning entries. *How* the store is read/written is delegated to the active **storage backend**.

## Arguments

**Context:** `$ARGUMENTS` — the reasoning pattern or anti-pattern to document. If omitted, ask: "What reasoning pattern or anti-pattern should I document?"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below to prevent context loss and ensure complete execution*

### Step 1: Read the Reasoning Store

Read the reasoning memory for the domain you are acting as, so the new pattern fits alongside the existing ones and doesn't duplicate one (**§ read-reasoning-store**).

@start storage id="add-reasoning.read-reasoning-store" ref="procedures/memory/storage-backends/{backend}.md" target="add-reasoning.read-reasoning-store"
@end storage
### Step 2: Draft from the Template

Read the reasoning-pattern template (**§ template**) and draft the entry using its fixed structure.

@start storage id="add-reasoning.template" ref="procedures/memory/storage-backends/{backend}.md" target="add-reasoning.template"
@end storage
### Step 3: Check the Entry

Check every required field against the template. For a new entry, generate its UUID (**§ generate-uuid**); for a rewrite, preserve the existing UUID. Keep the instructions, anchor, and example distinct, and check that the Final Conclusion stands on its own.

@start storage id="add-reasoning.generate-uuid" ref="procedures/memory/storage-backends/{backend}.md" target="add-reasoning.generate-uuid"
@end storage
### Step 4: Persist

Persist the completed pattern into the reasoning store (**§ persist-reasoning**).

---

@start storage id="add-reasoning.persist-reasoning" ref="procedures/memory/storage-backends/{backend}.md" target="add-reasoning.persist-reasoning"
@end storage
