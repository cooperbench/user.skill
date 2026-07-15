> DEVELOPER

[$codex-md-docs](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md) 优化这个skill
新增一条硬规则：同名服务也不能跨设备合并，必须按主机/路径/公网域名判断是否同一环
  境。

• Edited ../../root/.codex/skills/codex-md-docs/SKILL.md (+11 -1)
    23  - Search filenames and headings for the topic, service name, date, or keywords from the user request.
    24 -- Prefer updating or appending to an existing relevant document over creating a near-duplicate.
    24 +- Identify the device/environment first. Compare hostname, OS, cloud provider, public domain, deployment root, and path s
        tyle before deciding that an existing document is relevant.
    25 +- Do not merge records across different devices or environments only because the service name matches. For example, a mac
        OS/OrbStack deployment under `/Users/...` and an Ubuntu server deployment under `/srv/projects/...` must be separate docu
        ments.
    26 +- Prefer updating or appending to an existing relevant document only when it is the same device/environment and same serv
        ice or operational topic.
    27  - Preserve unrelated content and formatting.
       ⋮
    30
    31 +When creating a new operational document, include an environment marker near the top when relevant:
    32 +
    33 +- Hostname or device name.
    34 +- OS/cloud/provider when known.
    35 +- Main domain/IP, if public.
    36 +- Deployment root path.
    37 +- Whether the record is server-side, local desktop, container-only, or tunnel/reverse-proxy related.

我们要分设备看，分设备写文档

> SYSTEM

<skill>
<name>codex-md-docs</name>
<path>/Users/lyston/.codex/skills/codex-md-docs/SKILL.md</path>
---
name: codex-md-docs
description: Route Markdown documentation work into the user's Codex Obsidian space, including choosing or creating suitable subfolders and deciding whether to create, append, or update notes. Use when the user asks Codex to create, write, update, append, record, summarize, or save any Markdown document, md note, deployment record, operation guide, SOP, troubleshooting note, or other .md documentation unless the user explicitly gives a different destination.
---

# Codex Markdown Docs

## Root

When the user asks to create, write, update, append, record, summarize, or save a Markdown document, use this default root:

```text
/Users/lyston/Obsidian/lyston/Codex
```

Prefer this root even if older notes exist elsewhere, unless the user explicitly names another path. The final file may be directly under this root or under a suitable subfolder.

## Workflow

1. If the user gives an exact file path, use that path.
2. If the user gives a folder path, choose or create the `.md` file inside that folder.
3. If the user gives only a title or topic, inspect existing files and folders under `/Users/lyston/Obsidian/lyston/Codex` before writing.
4. Prefer an existing relevant folder or note when there is a clear match by filename, heading, project name, system name, or topic.
5. If the topic belongs to a recurring category or project and no suitable folder exists, create a concise subfolder under the Codex root. Keep folder depth shallow, usually one level.
6. If the topic is a one-off note or the category is unclear, write directly under the Codex root with a descriptive filename.
7. Read any likely matching document before editing it.
8. Preserve existing Markdown structure, frontmatter, headings, and Obsidian links.
9. Do not create database backups, code backups, or duplicate archival files unless the user explicitly asks.

## Organization

Use the existing directory structure as the source of truth. If a new folder is needed, use clear Chinese names when the user's request is Chinese. Prefer practical categories such as:

```text
部署记录
运维记录
故障排查
SOP
项目
调研
会议记录
会话交接
```

Do not create a new folder just to hold a single small note unless the topic is likely to recur, belongs to a project, or the user asks for a category.

## Create, Append, Or Update

Choose the write mode intentionally:

- Create a new file when no strong matching note exists, or the new topic is distinct from existing notes.
- Append when continuing history, deployment records, operational logs, troubleshooting timelines, meeting notes, session handoffs, or dated observations.
- Update an existing section when maintaining a living guide, SOP, configuration record, checklist, or summary whose current content should be refined.
- If updating risks overwriting important history, append a dated section instead.
- If multiple plausible target files or folders exist and the choice would materially affect organization, ask one concise clarifying question. Otherwise choose the safest match and report the choice.

For dated append entries, prefer headings like:

```markdown
## 2026-04-30
```

## Naming

Use clear Chinese filenames when the user's request is Chinese. Prefer concise names such as:

```text
Sub2API Docker（OrbStack）部署记录.md
Cloudflare Tunnel 外网访问配置记录.md
Codex 会话同步与迁移指南.md
```

If unsure, choose a descriptive filename based on the user's topic and keep it under the Codex root or the most relevant existing subfolder.

## Verification

After writing, briefly report:

- The file path written
- Whether content was created, appended, or updated
- Whether a folder was selected or created, if relevant
- Any important status or caveat discovered while writing

</skill>

> AGENT

我会同时看一下目标 skill 和 skill 编写规范，然后把“按设备/环境隔离文档”的规则直接固化进 `codex-md-docs`。这条规则会放在决策流程里，而不只是命名建议里。

> AGENT

我看到当前文件还没有那条规则落进去，所以我会补成一组更硬的判断：先识别设备/环境，再决定复用旧文档；服务名只作为线索，不能作为合并依据。命名和验收部分也会顺手收紧，让后续 agent 更不容易把不同机器的记录揉到一起。

> AGENT

规则已经写入了。我再快速读一遍改后的 skill，确认流程、命名和环境标记三处表达一致，没有把“同服务分设备写文档”写成软建议。

> AGENT

我还会补一刀到元数据和冲突处理上：skill 的触发描述里也标出“按环境隔离”，并且在环境信息不足但存在同名服务碰撞时要求先问清楚。这样规则不只在正文里可见，实际调用时也更稳定。

> AGENT

元数据和 UI 提示也同步了。现在我做最后一次 diff 检查，确认改动集中在 skill 本身，没有带入别的文件。

> AGENT

小插曲：这个 skill 目录本身不是 git 仓库，所以 `git status` 没法用；我用文件读取来确认最终内容。改动范围很小，只动了 `SKILL.md` 和它的 `agents/openai.yaml` 展示文案。

> AGENT

已优化 `codex-md-docs`，现在规则更硬了：

- 更新了 [SKILL.md](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md:23)：写入“先识别设备/环境”的流程，要求按主机、OS、云厂商、公网域名/IP、部署根路径、路径风格、容器运行时、Tunnel/反代端点判断。
- 加了硬规则 [SKILL.md](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md:24)：同名服务不能跨设备/环境合并，必须分设备写文档。
- 更新创建/追加/更新策略 [SKILL.md](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md:54)：同名服务只要环境不同就创建新文件；环境线索不足且存在多个同名服务时先问清楚。
- 增加环境标记要求 [SKILL.md](/Users/lyston/.codex/skills/codex-md-docs/SKILL.md:80)：运维类文档顶部要记录主机、OS/云厂商、域名/IP、部署路径、容器/本机/服务器/Tunnel 等信息。
- 同步更新了 [openai.yaml](/Users/lyston/.codex/skills/codex-md-docs/agents/openai.yaml:3)，让 skill 的展示文案也体现“按环境隔离”。

我也读回确认过最终内容了。这个 skill 目录本身不适合作为独立 git 仓库检查，所以没有可用的 `git status` 结果。
