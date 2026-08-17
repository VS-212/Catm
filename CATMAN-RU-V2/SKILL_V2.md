---
name: catman-ru-v2-repair-solutions-corpus
description: Продолжает CATMAN-RU через evidence repair, solution-pattern research, targeted Retail.ru/TAdviser corpus и independent adjudication. Требует новую Spark Task и реальные изолированные subagents.
version: 2.0
language: ru
---

# CATMAN-RU V2 Skill

## Когда применять

Только после существующего swarm-run `CATMAN-RU-DR-2024-2026`, когда доступны его handoff, run manifest и quality report.

## Процесс

1. Прочитать `DELTA_BRIEF_V2.md` и `v2_manifest.yaml`.
2. Повторить capability attestation в новой top-level Task.
3. Выполнить Evidence Repair и заморозить repaired dataset.
4. Параллельно выполнить Solution Pattern Atlas и Targeted Retail.ru/TAdviser Corpus.
5. Выполнить новый Red Team и independent adjudication.
6. Создать полный V2 handoff.

## Критические ограничения

- не продолжать старый Task context;
- не принимать старый final report за ground truth;
- не выполнять полный исторический crawl без trigger;
- не смешивать proposed project и observed solution;
- не использовать отсутствие публичных данных как доказательство отсутствия проекта;
- не сохранять unsupported project numbers как sourced;
- не считать обычные search tool calls отдельными agents;
- при отсутствии реальных subagents остановиться.

## Временная модель

- repair baseline: до 2026-08-14;
- new delta: после baseline до фактической даты запуска;
- historical backfill: 2019–2023, только triggered;
- cold layer не влияет на Current Demand Score.
