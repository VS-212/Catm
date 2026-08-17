---
name: catman-ru-evidence-swarm
description: Оркестрирует реальный изолированный рой для evidence-based исследования CatMan-спроса Top-10 grocery/FMCG-ритейлеров РФ за 2024–14.08.2026. Использовать только при доступности настоящих sub-agent runs, web research и файловых outputs.
version: 1.0
language: ru
---

# CatMan RU Evidence Swarm

## Когда использовать

Используй этот Skill только для проекта `CATMAN-RU-DR-2024-2026`, когда нужно выполнить мастер-бриф через отдельные независимые агенты: collectors → blind fact-checkers → blind analysts → project designer → Red Team → adjudicator.

## Главная инструкция

1. Прочитай `ORCHESTRATOR_BOOTSTRAP_PROMPT.xml`.
2. Прочитай `swarm_manifest.yaml`.
3. Выполни capability gate.
4. При отсутствии реальных изолированных subagents остановись со статусом `HALT_NO_REAL_SUBAGENTS`.
5. После PASS выполняй волны W0–W6 без смешивания контекстов.
6. Валидируй outputs по JSON Schemas.
7. Создай весь `required_handoff_bundle`.

## Запрещено

- изображать 25 агентов одним контекстом;
- считать обычные поисковые tool calls отдельными агентами;
- показывать fact-checkers предварительные выводы;
- давать project designer сырые непроверенные records;
- делать финальный вывод до Red Team и adjudication;
- выдумывать citations, quotes, timestamps или ROI.

## Форматы

- JSONL — только JSON object per line без code fences;
- narrative — Markdown;
- orchestration — YAML;
- agent prompt boundaries — XML-like;
- все claims должны ссылаться на evidence IDs.

## Пользовательский контроль

После capability gate и после каждой wave покажи короткий status report с фактическими run IDs. При critical ambiguity не меняй scope молча: запиши decision log и запроси подтверждение только если без него невозможно продолжить.
