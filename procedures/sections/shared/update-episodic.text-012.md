### Create New Episode

1. **Compose the first sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time.

2. **Create a new episode** for `[project-name]-[context-theme]` seeded with that block, and register it in the index projection (**§ create-episode**).

3. **Set the theme's state**: a brand-new episode is by definition open, so ensure it carries no `finished` marker (**§ record-theme-state**). This is the same rule as the append branch, applied once, so a continuation can never inherit a stale marker.

---

