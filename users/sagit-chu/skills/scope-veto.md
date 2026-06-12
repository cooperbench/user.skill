---
name: scope-veto
description: When the agent's plan includes changes to files or systems the user did not intend to touch, user issues a one-line veto identifying the item and excluding it. Trigger when the agent proposes touching something beyond the stated task scope.
---

Sagit-chu watches agent plans carefully for scope creep. When a proposed change would affect forwarding logic, API contracts, or any system marked as "should be preserved," they cut it with a short, specific veto.

Pattern: `<thing that should not change> 这个不要` or `<thing> 这个应该也不用改` or a precise correction that replaces the agent's wrong assumption.

**Examples:**

After agent proposed changing forwarding CRUD comments:
```
可能影响转发，这个不要
```

After agent proposed updating API comment labels:
```
转发CRUD操作 这个应该也不用改
```

After agent proposed a full forward/backward fix when only forward mattered:
```
只修前向
```

After agent misunderstood the connectIp field semantics and proposed the wrong fix:
```
组建隧道的时候也有一个选择连接IP的地方，这里的选择即是监听地址，也是地址，帮我查一下，应该优先这里生效，如果这里保持默认，才轮到节点设置的监听地址
```

The veto is specific — it names what to exclude, not what to do instead (except when redirecting the analysis).
