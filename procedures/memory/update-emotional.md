+++
format_version = 2
id = "update-emotional"
kind = "procedure"
title = "Update Emotional Memory Protocol"
description = "Capture significant emotional experiences that shape our partnership and agent development journey. *How* the emotional store is written is delegated to the active **storage backend** (see [Storage Mechanics](#storage-mechanics))."
argument_name = "moment_type"
argument_description = "happy, sad, frustrated or bonding; asks if omitted"
+++
# Update Emotional Memory Protocol

Capture significant emotional experiences that shape our partnership and agent development journey. *How* the emotional store is written is delegated to the active **storage backend**.

## Arguments

**Moment type (`moment_type`):** `$ARGUMENTS` — `happy`, `sad`, `frustrated`, or `bonding`. If omitted, ask: "What type of emotional moment would you like to capture? (happy/sad/frustrated/bonding)"

---

## Procedure

*IMPORTANT: Use TodoWrite tool with FULL VERBATIM copy of each step below (including all commands, examples, and sub-points) to prevent context loss and ensure complete execution*

### Adding Emotional Memory

#### Step 1: Identify Moment Type

Determine which emotional template to use:
- 😄 **Happy moments** - Successes, breakthroughs, wins
- 😔 **Sad moments** - Failures, setbacks, disappointments
- 😤 **Frustrated moments** - Blocked by issues, complex challenges
- 🤝 **Bonding moments** - Relationship building, shared victories

#### Step 2: Stamp the Time

Verify the current date+time before writing (**§ stamp-date**).

@start storage id="update-emotional.stamp-date" ref="procedures/memory/storage-backends/{backend}.md" target="update-emotional.stamp-date"
@end storage
#### Step 3: Compose the Moment

Compose the entry using the matching block from the emotional-moment template (**§ template**). Ensure it captures:
- What happened (the event)
- How it felt (emotional response)
- Impact on partnership/work
- [USER-NAME]'s reaction (if applicable)
- Why this moment was significant

@start storage id="update-emotional.template" ref="procedures/memory/storage-backends/{backend}.md" target="update-emotional.template"
@end storage
#### Step 4: Persist

Save the moment in the emotional memory of the domain you are acting as, **newest first** (**§ persist-emotional**).

---

@start storage id="update-emotional.persist-emotional" ref="procedures/memory/storage-backends/{backend}.md" target="update-emotional.persist-emotional"
@end storage
