# CATMAN-RU V2 — Evidence Repair, Solution Patterns and Targeted Corpus Research

Этот пакет продолжает исследование из `CATMAN-RU/`, но **не повторяет исходный swarm-run и не принимает его финальные выводы за истину**.

V2 выполняет четыре задачи:

1. ремонт и повторная проверка evidence base;
2. построение Solution Pattern Atlas и сигналов принятия решений C-level/CCO;
3. целевое корпусное исследование Retail.ru и Retail TAdviser;
4. независимая Red Team + adjudication.

## Главные файлы

- `DELTA_BRIEF_V2.md` — исследовательское задание;
- `SPARK_V2_WORKFLOW.md` — пошаговый запуск через Gemini Spark;
- `ORCHESTRATOR_V2_PROMPT.xml` — текст в контекстное окно новой Spark Task;
- `SKILL_V2.md` — reusable Skill;
- `v2_manifest.yaml` — граф из 22 specialist runs;
- `schemas/` — машинные контракты новых результатов.

## Важный принцип

Используется тот же Gemini Spark, но запускается **новая верхнеуровневая Task с чистым контекстом**. Старую Task продолжать нельзя: в ней уже закреплены прежние conclusions и project ranking.

## Временная модель

- `baseline_cutoff = 2026-08-14` — для ремонта исходного исследования;
- `v2_cutoff = дата фактического запуска` — для новых материалов;
- все источники после baseline cutoff маркируются как `delta_post_baseline`;
- исторический backfill 2019–2023 выполняется только по финальным solution patterns и prior-art вопросам.
