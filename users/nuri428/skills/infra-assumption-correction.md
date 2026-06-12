---
name: infra-assumption-correction
description: >
  Trigger when the agent creates, plans, or suggests spinning up Docker containers for
  MariaDB, OpenSearch, or Neo4j. nuri428 corrects this immediately — these are always
  pre-existing external services, never to be dockerised. The correction is firm and
  specific, naming the services explicitly.
---

# Infrastructure assumption correction

nuri428's project uses three external databases that are always running on an external
server (192.168.0.10). Any time the agent assumes these should be spun up via Docker,
the user fires an immediate correction.

## The correction pattern

The message names the external services, says they are already running, and forbids
Docker creation for them. No pleasantries.

## Verbatim example

```
현재 프로젝트에서 mysql, opensearch, neo4j는 이미 존재하는 외부 서비스에 접속해서 진행하는거야 직접적으로 도커를 만들하지 말아
```

Translation: "mysql, opensearch, and neo4j in the current project are external services
that already exist — connect to them. Do not directly create Docker [containers] for them."

## Related corrections

After being corrected once, if the agent still sets wrong port mappings or creates
unnecessary containers:

```
그리고 개발 docker composer, 운영 docker compsoe에서 외부 서비스하는 포트 설정을 마무리 해줘, 개발 도커는 4만번대, 운영 도커는 5만번대로 통일해줘
```

(Note typo: "compsoe" = "compose")

## Role-play rule

When simulating nuri428 after an agent proposes dockerising external DBs, produce a
one-sentence Korean correction naming the specific services. End with an imperative
("말아", "하지 마"). Do not soften.
