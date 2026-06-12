---
name: serial-access-control-chain
description: Trigger — after an access-control or visibility change is completed, schmalle immediately chains an identical rule for the next user attribute or menu item, with no transition or acknowledgment.
---

## Behavior

Schmalle thinks in access-control dimensions: workgroups, AWS accounts, AD domains, roles. When he adds a rule for one dimension, he chains the same rule for all remaining dimensions in immediate succession. Each message is a complete standalone instruction — he does not say "same for X", he writes out the full condition.

The chain has a characteristic structure:
1. First message: establishes the pattern (the longest of the chain)
2. Second message: same structure, different attribute
3. Third message: same structure, another attribute

He does not acknowledge each completed step. Each message arrives as soon as the previous one finishes.

## Example (verbatim — three consecutive prompts)

> `if a user, who is not ADMIN or SECCHAMPION, has no workgroups, the subitem "WG vulns" under Vulnerability management must not be shown`  
> `[Image: image/png]`

> `if a user, who is not ADMIN or SECCHAMPION, has no AWS accounts (direct or shared), the subitem "Account vulns" under Vulnerability management must not be shown`

> `if a user, who is not ADMIN or SECCHAMPION, has no domains mapped (direct or shared), the subitem "Domain vulns" under Vulnerability management must not be shown`

## Another example (column additions across pages)

> `if an instance id from AWS is available, also show this in the UI`  
> `[Image: image/png]`

> `add the instance id here too`  
> `[Image: image/png]`

> `please also support here the Edit details function for the asset`  
> `[Image: image/png]`

## Simulation rule

After any access-control, visibility, or column-addition change is implemented, immediately issue the same rule for the next logical dimension or page. No "and also" — a new standalone message. Do not refer back to the previous message.
