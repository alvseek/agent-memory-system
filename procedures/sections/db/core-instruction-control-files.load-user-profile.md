### § load-user-profile

Already in the `awaken` payload: `shared.user_profile` is the whole record, or `null`. `null` means no profile has ever been written for this user, which is Phase 1's first-run branch. A record that exists with an empty value inside it is **not** that case — that is a deliberate blank, and re-asking it turns a one-time courtesy into a nag.

