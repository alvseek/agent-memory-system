### § persist-user-profile

`insert(scope="shared", record_type="user_profile", title="User Profile", content="<the profile markdown>")`. No `agent_id`: the profile has no owner, and `scope="shared"` forbids one. Write **one** record carrying all three values in the same bullet form the markdown backend uses — never one record per field, because presence is answered by a row count and three rows would admit partial states with no rule for resolving them.

