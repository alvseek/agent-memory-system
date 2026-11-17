### Step 1: Load the Awakening Set

Load the agent's full awakening set into **your own context** (**§ load-agent-memory**). First call the awakening tool once and return its full response for reading, without selecting fields, summarizing, slicing, or preemptively redirecting it to a file. Do not assume it will truncate before trying. For a file-backed load, likewise try one whole read per required source first.

If the platform explicitly reports truncation or says the result was saved to a file, read the saved result to recover all omitted context before continuing. Try one whole read of that file first; only if that read also reports a limit, recover the missing content using a method that preserves it, including long lines. A preview, clipped JSON string, or summary is not a full load. If required context remains unavailable, name the source and failure and stop the work that depends on it; never report a partial load as complete.

The awakening set has four layers:

1. **Agent identity** — this domain's identity, core knowledge, and RAS triggers.
2. **Agent context + knowledge index** — the episodic index and knowledge directory (bodies loaded on demand).
3. **Shared reasoning patterns.**
4. **Shared knowledge** — an index for the store backend; bodies loaded on relevance.

*(The awakening protocol itself is not one of them — it is carried by Step 2 below.)*

🚨 **CRITICAL — load the awakening set into YOUR OWN context**

