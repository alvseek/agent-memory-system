+++
format_version = 2
id = "update-episodic"
kind = "procedure"
title = "Update Episodic Memory Protocol"
description = "Save a dated session entry in a new or existing episode for the current project."
argument_name = "mode"
argument_description = "`new` to force a new episode instead of appending"
+++
# Update Episodic Memory Protocol

An episode groups dated session entries by theme. By default, look for a matching active episode in the current project. Add the entry to that episode, or create one if none matches.

## Arguments

`$ARGUMENTS` — optional `new`. Create a separate episode without searching for a match.

## Phase 1 — Choose where to save

### Identify the project and theme

- **Project:** Use the project supplied by the caller. If none is supplied, leave the episode unassigned. For a new unassigned episode, use the theme alone as its name.
- **Theme:** Identify the subject of the work being recorded. Choose keywords from that subject to compare candidate episodes.
- **If `new` was supplied:** choose Path B and go straight to Phase 2. Skip both the active and archived candidate searches.

### List active candidates

List the acting agent’s active (non-archived) episodes for the selected project, or only their unassigned episodes if no project was supplied (**§ list-candidate-episodes**).

@start storage id="update-episodic.list-candidate-episodes" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.list-candidate-episodes"
@end storage

### Compare candidates

- Read each candidate’s title and summary.
- Ask: **Does the work being saved continue the task, decision, or problem recorded in this episode?**
- Use shared keywords as clues. Don’t choose an episode just because it uses the same words.

### Choose a path

- **One clear continuation** → Choose Path A without asking.
- **No active match** → Choose Path B unless the user asked to continue a specific theme. In that case, check the archive first.
- **Unsure** → Show only the plausible candidates. Give one reason each might fit, then ask: **“Append to one of these, or start a new episode?”** Wait for the answer.

When checking the archive, use the same project scope. Reopen a matching episode (**§ reopen-archived-theme**) and choose Path A only to continue that work. For follow-up work on a finished theme, or if no archived episode fits, choose Path B.

@start storage id="update-episodic.reopen-archived-theme" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.reopen-archived-theme"
@end storage

## Phase 2 — Save the entry

Use the entry template for either path (**§ template**). Follow only the path chosen in Phase 1, then go to Phase 3.

@start storage id="update-episodic.template" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.template"
@end storage
@start storage id="update-episodic.stamp-date" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.stamp-date" applies_to="markdown"
@end storage

### Path A — Add to an existing episode

1. **Carry-forward review:** Read the latest entry’s **Tech Debts** and **Next Steps**. Keep unresolved items, including any whose status is uncertain. Drop confirmed resolutions and add new open items.
2. **Write the entry newest-first:** Compose its title and body from the work being saved. Put it above the older entries and update the episode summary (**§ append-sub-episode**).

@start storage id="update-episodic.append-sub-episode" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.append-sub-episode"
@end storage
@start storage id="update-episodic.housekeeping" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.housekeeping" applies_to="markdown"
@end storage

3. **Update the theme state:** Mark it `finished` only if this entry closes the theme; otherwise remove that marker if present (**§ record-theme-state**).

@start storage id="update-episodic.record-theme-state" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.record-theme-state"
@end storage

### Path B — Create a new episode

1. **Compose the first entry:** Write the title and body from the work being saved. Its **Tech Debts** and **Next Steps** come from that work alone.
2. **Register the episode:** Save the first entry under the project and theme chosen in Phase 1. List it in the index and leave it open (no `finished` marker) (**§ create-episode**).

@start storage id="update-episodic.create-episode" ref="procedures/memory/storage-backends/{backend}.md" target="update-episodic.create-episode"
@end storage

## Phase 3 — Return the open items

After the chosen path succeeds, return **Tech Debts** and **Next Steps** exactly as saved. “None declared” is a valid result for either field. Return them as data so the caller can report them once.
