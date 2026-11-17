#### Step 4: Match Heuristic

For each candidate, score theme overlap:
- Tokenize the candidate's filename (sans extension and any legacy date prefix) and summary
- Count keyword overlap with this session's theme keywords
- Higher overlap = stronger merge signal

Identify:
- **Top match**: highest-scoring candidate (if any meaningful overlap exists)
- **Runner-ups**: 2nd-3rd scoring candidates if scores are close

If the top match has zero meaningful overlap, treat as "no match" → skip to Step 6 (Create branch).

