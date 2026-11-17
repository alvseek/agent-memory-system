### Append Sub-Episode

1. **Carry-forward review of prior open items**: the target's most recent prior sub-episode (the top H3 our new block will sit above) holds the latest open items. Review them so the new block stays self-contained:
   - **a. Read prior open items**: extract the `**Tech Debts**` and `**Next Steps**` fields from the prior top sub-episode's Outcomes.
   - **b. Review each against work done since that prior sub-episode's timestamp**:
     - *Resolved by the delta work?* → drop from carry-forward list.
     - *Still open?* → keep (verbatim, or refined if the delta clarified scope).
   - **c. Stage the carry-forward list**: the new block's `**Tech Debts**` and `**Next Steps**` become the **union** of (still-open carried forward) + (genuinely new items from this delta window).

   > **Why this matters**: both wrap-up and awakening read only the newest sub-episode when surfacing open items. Without carry-forward, prior unresolved debts get hidden and the next awakening won't see them. Carry-forward keeps the newest block self-contained, preserving the read-newest-only invariant.

   > **Why no time threshold**: the prior sub-episode's timestamp is deterministic. Recent prior (same conversation) → full context to review each item. Older prior (different session) → items are still carry-forward candidates, reviewed on their own descriptions; items that can't be confidently evaluated default to "still open" (conservative, per UUID a1b2c3d4 — debts never silently dropped).

2. **Compose the sub-episode block** using the sub-episode-block template (**§ template**). The H3 header includes the stamped date+time:
   ```
   ### YYYY-MM-DD HH.MM - [SESSION SUB-THEME] (agent: [domain])
   ```

3. **Append it newest-first** to the chosen episode (at the top, above older sub-episodes) and reflect the change in the index projection (**§ append-sub-episode**).

4. **Run post-write housekeeping** (**§ housekeeping**).

5. **Set the theme's state**: does this block close the theme? Ensure the record carries the `finished` marker when it does and does not carry it when it does not (**§ record-theme-state**). One state per block, written once at the end — never remove the marker in order to add it back in the same run.

---

