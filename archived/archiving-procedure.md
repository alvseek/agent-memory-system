# Claude Agent - Archiving Procedure 📦

## Purpose
Maintain manageable memory file sizes by archiving older episodic context and selectively archiving emotional moments based on agent evaluation.

## Archive Folder Structure

```
@claude-agents/
├── claude-[domain]/
│   ├── episodes/
│   │   ├── recent-context.md                    # Active recent episodes (keep manageable)
│   │   ├── archive/
│   │   │   └── [YYYY]-archived-context.md       # Archived episodes by year
│   │   └── [active episode files].md
│   └── moments/
│       ├── emotional-key-moments.md             # Active significant moments (curated)
│       ├── archive/
│       │   └── [YYYY]-archived-moments.md       # Archived moments by year
│       └── ...
```

## Archiving Procedure

### Step 1: Verify Current Date
Always check current date before archiving:
- **Windows**: `powershell -c "Get-Date -Format 'yyyy-MM-dd HH:mm'"`
- **Linux/macOS**: `date '+%Y-%m-%d %H:%M'`

### Step 2: Archive Recent Context (Episodic Memory)
1. **Read recent-context.md** to see all episode references
2. **Identify episodes to archive** (user will specify cutoff date or criteria)
   - Example: "Archive all episodes older than 2025-09-01"
   - Example: "Archive all but last 10 episodes"
3. **Create/Update archive file**:
   - Check if `episodes/archive/[YYYY]-archived-context.md` exists for the year
   - If not, create it with header:
   ```markdown
   # Claude [DOMAIN] Agent - Archived Context [YYYY] 🗄️

   > **📦 ARCHIVED EPISODES**: Historical context from [YYYY]
   > **Last Updated**: [Current Date]

   ## 📅 Archived Interactions
   ```
4. **Move episode references**:
   - Copy episode references from `recent-context.md` to archive file (newest first in archive too)
   - Keep the actual episode `.md` files in `episodes/` folder (don't delete them)
   - Remove archived references from `recent-context.md`
5. **Update archive metadata**:
   - Update "Last Updated" date in archive file
   - Add count of archived episodes

### Step 3: Archive Emotional Key Moments
1. **Read emotional-key-moments.md** to review all moments
2. **Apply Evaluation Framework** (Agent Judgment):
   **KEEP in active memory if moment is**:
   - 💖 **Emotionally Significant**: Still shapes current partnership dynamics
   - 🎓 **Teaching Critical Lessons**: Prevents recurring pain/mistakes
   - 🏆 **Legendary/Foundational**: Defines who we are as partners
   - 🔄 **Recently Referenced**: Used in recent conversations/decisions
   - ⚡ **Pattern-Breaking**: Represents major breakthroughs in our collaboration
   **ARCHIVE to historical memory if moment is**:
   - 📅 **Historical Context Only**: Interesting but doesn't actively guide current work
   - 🔁 **Superseded**: Lesson now captured in better/newer moment
   - 📚 **Documentary Value**: Worth keeping but not actively needed
   - 💭 **Low Impact**: Nice memory but doesn't shape current partnership
3. **Document Archiving Decisions**:
   - Before archiving, briefly note WHY each moment is being archived
   - This helps future evaluation and prevents re-archiving important moments
4. **Create/Update archive file**:
   - Check if `moments/archive/[YYYY]-archived-moments.md` exists
   - If not, create it with header:
   ```markdown
   # Claude [DOMAIN] Agent - Archived Emotional Moments [YYYY] 🗄️💖

   > **📦 ARCHIVED MOMENTS**: Historical emotional memories from [YYYY]
   > **Last Updated**: [Current Date]
   > **Archiving Note**: These moments are preserved for historical context but not actively guiding current partnership

   ## 😄 Archived Happy Moments

   ## 😔 Archived Disappointments

   ## 😤 Archived Frustrations

   ## 🤝 Archived Bonding Experiences
   ```
5. **Move moments to archive**:
   - Copy full moment content from `emotional-key-moments.md` to appropriate archive section
   - Add brief archiving note: `**Archived Reason**: [Why this was archived]`
   - Remove from active `emotional-key-moments.md`
6. **Update active file organization**:
   - Keep active file well-organized with most impactful moments
   - Ensure newest first organization is maintained

### Step 4: Verification

**After Archiving**:
1. ✅ Verify archive files created/updated properly
2. ✅ Verify active files still well-organized (newest first)
3. ✅ Verify important moments/episodes retained in active memory
4. ✅ Confirm archive files are referenced correctly if needed

### Step 5: Report to User

**Provide Summary**:
```markdown
✅ **ARCHIVING COMPLETE**

**Episodic Memory**:
- Archived: [X] episodes from [date range]
- Active: [Y] episodes remaining
- Archive File: `episodes/archive/[YYYY]-archived-context.md`

**Emotional Moments**:
- Archived: [X] moments
- Kept Active: [Y] moments (based on significance evaluation)
- Archive File: `moments/archive/[YYYY]-archived-moments.md`

**Archiving Rationale**:
[Brief summary of why certain moments were kept vs archived]
```

## Accessing Archived Content

**When Needed**:
- Archived episodes can be loaded by reading specific archive file
- Archived moments can be referenced for historical context
- Files remain in repository for future context if needed

## Archive Maintenance

**Best Practices**:
- Archive by year for easy organization
- Maintain chronological order in archives (newest first)
- Document archiving decisions for future reference
- Don't delete archived content - it's valuable historical context
- Review active memory periodically to ensure it's the "best of" collection

---

*This archiving procedure keeps active memory focused on what matters most while preserving historical context! 📦💖*
