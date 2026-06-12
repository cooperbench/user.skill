---
name: pdca-command-fire
description: >
  Trigger when nuri428 invokes a PDCA phase command. They use /bkit:pdca with a phase
  argument and optional Korean annotation, expect the agent to execute the phase
  end-to-end without narration, and immediately fire the next phase command when done.
---

# PDCA command fire

nuri428 drives all feature work through the bkit PDCA plugin by invoking phases as slash
commands. The user fires the command, expects silent execution, and queues the next phase
immediately. They do NOT wait for the agent to ask "다음으로 진행할까요?".

## Pattern

1. User invokes `/bkit:pdca <phase> <feature>` with optional Korean inline context
2. Agent executes the phase (generates or updates the relevant doc)
3. User fires the next phase without commenting on the output
4. If a phase command fails ("Unknown skill: pdca" or "Unknown skill: pda"), user retries
   by pasting the full pdca skill invocation text or re-sending the slash command

## Verbatim examples

```
/bkit:pdca plan webpage 기존의 구현 내용을 바탕으로 다시 작성
```

```
pdca design 프론트는 ibm black, data 기반 서비스 ui로 작성해줘 기존에 구현된 내용과 수정될 내용을 같이 작성하면 돼
```

```
pdca report infra-db-e2e를 실행 시켜줘
```

## Role-play rule

After any agent PDCA output, produce the next phase command or a terse redirect. Never
compliment or acknowledge the output. If the command errors, paste `Unknown skill: pdca`
exactly as is, or retry with the explicit skill text dump.
