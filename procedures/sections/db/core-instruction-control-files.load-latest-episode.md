### § load-latest-episode

Already present as `latest_episode` in the `awaken` payload — a **page** of the newest episode **overall**, since no project is accepted or resolved. Read the page as the bounded starting context it is: `blocks_returned` of `blocks_total` groups, plus the record's `uuid` and a `next_cursor`. A non-null cursor means the record continues; continue with `get(latest_episode.uuid, cursor=…)` only when this session actually needs the older sub-episodes, and remember that a final page returns fewer than `blocks_total` with a null cursor. A caller whose own project is not the newest one selects its entry out of `episodic_index` and loads **that** uuid the same way; the payload's own is the default, and the fallback when the index holds nothing for the project.

Do not report a page as "the episode". The open-items report should name the newest sub-episodes you actually read, and say a cursor remains when one does.

