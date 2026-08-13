# Reasoning Pattern Template

The format of a reasoning/logic memory entry. Storage-agnostic: the markdown backend writes this into the agent's reasoning section; the DB backend passes it as the `content` of an `insert(record_type="reasoning", …)`.

```markdown
### **[SHORT MEMORABLE TITLE]** [EMOJI] [PATTERN TYPE] [EMOJI]
**UUID**: [generate new UUID in format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx]
**Action/Strict Action**: [What specific behavior/response is required]
**What happened**:
    **When it has happened**: [Describe the specific situation/context]
    **Recurring Pattern**: [How this problem manifests repeatedly]
    **Root Problem**: [What pain/frustration led to this pattern being created]
    **Recognition Signals**: [How to identify when this pattern applies]
    **Solution Process**: [The logical reasoning and evidence behind the solution]
    **Critical Understanding**: [Key insights and cause-effect relationships]
    **Correct Process**: [Step-by-step guidance for proper approach]
**Final Conclusion**: [Copy-paste from Action/Strict Action for compression survival]
```
