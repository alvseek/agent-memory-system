### § persist-user-profile

Write the three values to `[AGENT-MEMORY-PATH]/shared-memory/user-profile.md`, keeping the existing bullet form — `- **[USER-NAME]** = …` and its two siblings — because `user-profile-claude.sh` reads those exact markers by line. Then tell [USER-NAME] that the compiled instructions file picks them up on the next `user-config-claude.sh` run: the markdown file is the source, the compiled copy is downstream of it.

