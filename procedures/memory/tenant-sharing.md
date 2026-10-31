# Working in a Shared Account

Work inside an account somebody else owns, or let somebody work inside yours. Every call acts in exactly one **tenant**, you are always acting in one, and this procedure is how you find out which and change it. *Who* may enter *which* tenant is a grant, not a role: your own tenant is yours by construction, and any other arrives as an invitation its owner issued.

## Arguments

`$ARGUMENTS`

- `/tenant-sharing` → show the tenants open to the caller and the one in use
- `/tenant-sharing switch [tenant]` → act in that tenant, by id or by unique label
- `/tenant-sharing switch home` → go back to your own tenant
- `/tenant-sharing members`, `/tenant-sharing invite`, `/tenant-sharing revoke [member]` → the owner's side

---

## Procedure

### Step 1: Say where you are

Call `list_tenants`. Every entry carries `user_id`, `role` (`owner` for your own tenant, `guest` for a granted one), `label`, `active` marking the tenant your calls are acting in, and `revoked`, which is true only for a tenant you are still standing in but may no longer enter.

- **No guest entry, and the caller expected one** → nobody has invited them yet, or their access was revoked. Do not guess at a tenant id.
- **`active` is a guest tenant** → say so before writing anything. What you read and write belongs to that account, and its fleet is the one that answers.

### Step 2: Switch when asked, and only then

Call `use_tenant` with the `user_id` from the list, or with its `label` when that label names exactly one tenant open to the caller. `use_tenant` with no argument, or with the caller's own tenant, returns to the default.

Two facts to state when you switch, because both surprise people:

- **The choice is remembered per person, not per client.** A switch made here moves the same person's other sessions, and it survives a restart. Nothing is per project and nothing is per agent: the whole tenant is the unit.
- **Switching does not copy anything.** The other account's memories, agents and user profile are read where they live.

### Step 3: Treat a refusal as information, never as a bug

A memory call that answers that access was revoked means exactly that, and it names the tenant. The fix is `use_tenant` back to the caller's own tenant, which always works — that is why the membership tools are reachable while every memory tool is refusing.

Do not retry the same call, and do not switch tenants silently to make an error go away. Say what happened and let the person decide.

### Step 4: The owner's side, and only the owner's

While `active` is the caller's own tenant, these are available and they act on it:

- `list_members` → everybody with access, the owner first.
- `create_invite` → a single-use code with an expiry, to be sent out of band.
- `revoke_invite` → retire a code that has not been used.
- `revoke_member` → end somebody's access on their next call. Nothing they wrote is deleted.

While `active` is somebody else's tenant, all four refuse. That is not a limitation to work around: only an account's owner decides who else may enter it.

## Storage Mechanics

This procedure exists only where the store is a server with tenants: it is served by Munnin and has no markdown counterpart, which is why the markdown compilation skips it rather than installing a command whose ops do not exist.

- **§ list-tenants** · **§ switch-tenant**
- **§ list-members** · **§ invite** · **§ revoke-invite**
- **§ redeem** · **§ revoke-member**

---

## Notes

- **Joining does not switch you.** After `redeem_invite`, call `list_tenants` and then `use_tenant` when the person actually wants to work there.
- **A guest is still visible as themselves.** `awaken` carries a `caller` block naming the person signed in and whether they are a guest, while the memory belongs to the account being read.
- **Your own tenant and everything in it are never touched by joining or leaving.** Access is a row about somebody else's account; it never moves your records.
