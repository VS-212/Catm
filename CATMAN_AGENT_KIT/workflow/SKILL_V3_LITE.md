---
name: catman-ru-v3-lite-progressive-context
description: Выполняет V3 как четыре отдельные Spark Tasks с чистыми контекстами, GitHub resource shards и компактными handoff, не загружая весь V2 dataset в orchestrator context.
version: 1.0
language: ru
---

# V3 Lite Progressive Context Skill

## Правила

1. Одна Task выполняет только одну фазу A/B/C/D.
2. Orchestrator не загружает все resource shards в собственный контекст.
3. Каждый worker получает только назначенные repo paths.
4. Между Tasks передается только schema-valid compact handoff.
5. A_HANDOFF ≤90 KB, B_HANDOFF ≤130 KB, C_HANDOFF ≤160 KB.
6. Full records сохраняются отдельными output files и передаются по pointers/IDs.
7. Старые V2 conclusions не являются ground truth.
8. Реальные subagents и run IDs обязательны.
9. Narrative documents имеют более низкий trust, чем independently opened sources.
10. L4 определяется обязательными gates, не количеством материалов.

## Context hygiene

- не вставлять длинные evidence arrays в chat;
- не цитировать peer output целиком;
- сохранять summaries, IDs и paths;
- после завершения Task создавать новую Task, а не продолжать thread;
- не переносить conversational memory между Tasks.
