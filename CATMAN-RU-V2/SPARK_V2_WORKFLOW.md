# Workflow запуска CATMAN-RU V2 в Gemini Spark

## Короткий ответ

**Новую версию приложения Gemini Spark устанавливать не нужно.** Используйте тот же аккаунт и доступный актуальный runtime Spark.

Но обязательно создайте:

- **новую top-level Task**;
- новый чистый task context;
- новые sub-agent runs;
- отдельную папку outputs.

Старую Task, в которой выполнялся CATMAN-RU V1, продолжать нельзя: ее память уже содержит прежние project rankings и может создать confirmation bias.

---

# 1. Рекомендуемая конфигурация

| Параметр | Значение |
|---|---|
| Spark account/runtime | Тот же, актуальный |
| Top-level Task | Новая |
| Task name | `CATMAN-RU-V2-EVIDENCE-AND-SOLUTIONS` |
| Old task context | Не использовать |
| Skill | Новый `SKILL_V2.md` |
| Personal memory | Off, если доступно |
| Web research | On для Q02/Q05/S02/S03/S05/C01–C06 |
| Concurrency | Предпочтительно 8, максимум 10 |
| Retries | 1 на specialist |
| Repair runs | Максимум 4 |
| Schedule | Не нужен; one-time long-running Task |
| Workspace connectors | Только нужные Drive/GitHub read access |
| Gmail/Calendar и прочие | Отключить |
| File write | Разрешить только в V2 output folder |
| Output style | Files first, chat only for status/gates |
| Baseline cutoff | 2026-08-14 |
| V2 cutoff | Дата запуска |
| Historical backfill | Triggered only, 2019–2023 |

Если Spark позволяет выбирать reasoning level:

- collectors/inventory: standard/medium;
- fact-checkers Q02–Q06: high;
- pattern synthesizer S06: high;
- Red Team Z02: high;
- adjudicator J02: maximum available.

Если Spark сам выбирает модель, не пытайтесь вручную маршрутизировать модели; сохраните фактический runtime/model ID в run manifest, если UI его показывает.

---

# 2. Что загрузить

## В контекстное окно новой Task

Вставьте полное содержимое:

```text
CATMAN-RU-V2/ORCHESTRATOR_V2_PROMPT.xml
```

## В Skills

Создайте новый Skill из:

```text
CATMAN-RU-V2/SKILL_V2.md
```

Старый Skill V1 можно оставить в аккаунте, но не активировать одновременно с V2 Skill.

## Как файлы новой Task

### V2 instructions

```text
CATMAN-RU-V2/DELTA_BRIEF_V2.md
CATMAN-RU-V2/v2_manifest.yaml
CATMAN-RU-V2/V2_SCHEMAS.json
```

### Compact V1 input

```text
CATMAN-RU/90_ARENA_HANDOFF.json.docx
CATMAN-RU/00_run_manifest.json.docx
CATMAN-RU/00_capability_attestation.json.docx
CATMAN-RU/99_run_quality_report.json.docx
CATMAN-RU/14_research_gaps.md.docx
CATMAN-RU/13_final_report.md.docx
```

`90_ARENA_HANDOFF.json.docx` содержит universe, ontology, sources, raw evidence, fact checks, verified evidence, claims, projects, Red Team и adjudication. Поэтому не нужно загружать все остальные V1 DOCX одновременно, если Spark корректно извлек compact handoff.

Если extraction `90_ARENA_HANDOFF` не удался, тогда дополнительно загрузите отдельные:

```text
03_source_registry.jsonl.docx
04_evidence_raw.jsonl.docx
05_fact_checks.jsonl.docx
06_evidence_verified.jsonl.docx
08_claims_ledger.jsonl.docx
10_project_hypotheses.jsonl.docx
12_adjudication.jsonl.docx
```

---

# 3. Запуск

## Шаг 1 — новая Task

1. Откройте Spark.
2. Создайте новую Task.
3. Назовите `CATMAN-RU-V2-EVIDENCE-AND-SOLUTIONS`.
4. Активируйте только V2 Skill.
5. Прикрепите файлы из раздела 2.
6. Вставьте `ORCHESTRATOR_V2_PROMPT.xml` в task context.
7. Запустите.

## Шаг 2 — сокращенная re-attestation

Первый результат:

```text
00_v2_capability_attestation.json
```

Нужны два новых test run IDs T01 и T02. Старый capability PASS нельзя просто скопировать.

При отсутствии отдельных subagents остановить run.

## Шаг 3 — Evidence Repair

Spark запускает Q01–Q06, затем Q07.

Ожидайте:

```text
01_canonicalization_manifest.json
02_repair_issues.jsonl
03_sources_v2.jsonl
04_evidence_v2.jsonl
05_fact_checks_v2.jsonl
06_claims_v2.jsonl
07_repair_log.md
08_repair_quality_report.json
```

После этого Spark должен остановиться на gate `REPAIRED_DATASET_FROZEN`, если нашел critical unresolved issues.

### Сообщение после проверки Repair

```text
Gate Evidence Repair принят. Заморозь repaired dataset. Параллельно запускай V2-S Solution Pattern lane и V2-C Corpus lane. Не передавай S-агентам старый project winner как ground truth. Historical backfill разрешен только по finalist-pattern triggers.
```

Если repair не принят:

```text
Gate Evidence Repair не принят. Не запускай Solution Pattern и Corpus synthesis. Исправь перечисленные critical issues в пределах repair budget и выпусти новый repair quality report.
```

## Шаг 4 — Solution и Corpus lanes

После repair параллельно идут:

- S01–S06: observed solutions, acceptance, friction, formats, outcomes, patterns;
- C01–C07: Retail.ru/TAdviser inventory, multimodal processing, primary verification и targeted backfill.

При ограничении concurrency:

1. S01–S05;
2. C01–C04;
3. S06;
4. C05–C06;
5. C07.

Нельзя объединять несколько agent roles в одном worker context только ради concurrency.

## Шаг 5 — Red Team и adjudication

После freeze обеих lanes:

```text
Solution Pattern и Corpus gates приняты. Запускай Z02 в новом слепом контексте, затем J02. Старые project scores считать hypotheses. Создай весь V2 handoff и quality report.
```

---

# 4. Контроль прогресса

После каждой wave Spark должен показать:

- фактические run IDs;
- completed/failed/retried;
- input/output filenames;
- record counts;
- unresolved issues;
- следующий gate.

Не принимайте фразу «я выполнил несколько ролей» без отдельных run IDs.

## Обязательные checkpoints

### Checkpoint R

- 190 raw records учтены;
- у каждого V2 verified record есть explicit check;
- R08/R09 gap разрешен или честно оставлен gap;
- cutoff исправлен;
- source tiers пересчитаны;
- numerical provenance исправлен;
- citations alignment проверен.

### Checkpoint S/C

- observed solutions отделены от proposed projects;
- acceptance signals основаны на rollout/budget/KPI/renewal;
- каждая pattern card содержит counterexample;
- Retail.ru/TAdviser coverage имеет URL counts и failure counts;
- metadata-only multimedia не выдано за обработанное;
- backfill ограничен finalist patterns.

### Checkpoint A

- новый Red Team независим;
- final report не сильнее adjudication;
- Current Value отделен от historical context;
- sourced economics отделена от assumptions;
- unresolved issues не скрыты.

---

# 5. Когда нужна полностью новая Spark-сессия/инстанс

Новая Task внутри текущего Spark достаточна, если:

- Task получает чистый контекст;
- старые conversations не подмешиваются автоматически;
- можно отключить personal memory;
- создаются новые subagent run IDs.

Новый отдельный Spark workspace/account нужен только если:

- Spark автоматически передает новым Tasks старую память;
- невозможно отключить старый Skill;
- нельзя ограничить доступ к старым conclusions;
- текущий workspace достиг лимита файлов/tasks;
- требуется организационная изоляция прав доступа.

То есть по умолчанию:

```text
тот же Spark → новый Skill V2 → новая Task → новые subagents
```

а не новая подписка или установка.

---

# 6. Что скачать после завершения

Минимум:

```text
90_V2_ARENA_HANDOFF.json
90_V2_ARENA_HANDOFF.md
08_repair_quality_report.json
15_solution_pattern_atlas.md
24_corpus_coverage_report.md
31_v2_adjudication.jsonl
32_current_value_report.md
33_c_level_decision_pack.md
99_v2_quality_report.json
```

Для полного аудита также сохранить все файлы из `required_outputs` в `v2_manifest.yaml`.

---

# 7. Что затем загрузить в Arena

Загрузите минимум:

```text
90_V2_ARENA_HANDOFF.json
90_V2_ARENA_HANDOFF.md
99_v2_quality_report.json
32_current_value_report.md
33_c_level_decision_pack.md
```

И дайте инструкцию:

```text
Загружены результаты CATMAN-RU V2.

Сначала проверь Evidence Repair, coverage Retail.ru/TAdviser, разделение observed solutions и proposed projects, numerical provenance, Red Team и adjudication. Затем собери независимую итоговую архитектуру продукта и pilot decision pack. Не переносить claims из V1, если они не подтверждены V2.
```
