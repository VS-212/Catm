# V3 Lite — запуск без переполнения контекста

## Почему предыдущая Task могла зависнуть

Проблема вероятнее связана не с количеством файлов как таковым, а с одновременной загрузкой:

- V2 bundle около 2,5 МБ;
- длинных V3 instructions;
- накопленной памяти одной long-running Task;
- outputs десятков agents в orchestrator context.

Даже если модель имеет большое context window, orchestration, web pages, tool outputs и промежуточные summaries быстро расходуют его.

## Решение

Запустить V3 как **четыре отдельные top-level Tasks**. Каждая начинает чистый контекст. Между Tasks передается только compact handoff.

---

# Общие настройки

Используйте тот же Spark account/runtime.

Создайте один Skill:

```text
CATMAN-RU-V3/LITE/SKILL_V3_LITE.md
```

Для каждой фазы создавайте новую Task; предыдущую не продолжайте.

```text
Personal memory: Off
V1/V2/V3 Full Skills: Off
Active Skill: только V3 Lite
Concurrency: 6–8, максимум 10
Retry: 1
Schedule: none
Files first
```

---

# Task A — Forensic Audit

## Название

```text
CATMAN-V3-LITE-A-FORENSIC
```

## В контекст

Вставить `TASK_A_PROMPT.xml`.

## Прикрепить — всего около 20 КБ

```text
V2_RESOURCE_INDEX.json
LITE_HANDOFF_SCHEMAS.json
```

Полные данные не прикрепляются. Workers получают назначенные `resources/v2/...` через GitHub.

## Результат

Скачать:

```text
A_HANDOFF.json        # ≤90 KB
A_audit_verdicts.jsonl
A_accepted_v2_base.jsonl
A_rejected_unresolved.jsonl
A_forensic_report.md
```

Task A завершить.

---

# Task B — Global/Vendor/GitHub Landscape

## Название

```text
CATMAN-V3-LITE-B-LANDSCAPE
```

## В контекст

Вставить `TASK_B_PROMPT.xml`.

## Прикрепить — целевой объем ≤120 КБ

```text
A_HANDOFF.json                    # ≤90 KB
SOURCE_AND_QUERY_MAP.md
SUFFICIENCY_STANDARD.md
LITE_HANDOFF_SCHEMAS.json
```

Если A_HANDOFF превышает 90 KB — вернуть его на сокращение, не запускать B.

## Результат

```text
B_HANDOFF.json        # ≤130 KB
B_global_cases.jsonl
B_china_evidence.jsonl
B_negative_cases.jsonl
B_vendor_products.jsonl
B_github_repos.jsonl
B_shortlist.json
```

Task B завершить.

---

# Task C — Reference Architectures

## Название

```text
CATMAN-V3-LITE-C-ARCHITECTURES
```

## В контекст

Вставить `TASK_C_PROMPT.xml`.

## Прикрепить — целевой объем ≤170 КБ

```text
B_HANDOFF.json                    # ≤130 KB
KB_TARGET_ARCHITECTURE.md
V3_SCHEMAS.json
LITE_HANDOFF_SCHEMAS.json
```

## Результат

```text
C_HANDOFF.json        # ≤160 KB
C_architecture_01.json
C_architecture_02.json
C_architecture_03.json
C_architecture_04.json
C_architectures.md
C_economics.jsonl
C_transferability.jsonl
C_build_buy_partner.md
C_pilot_blueprints.md
```

Task C завершить.

---

# Task D — Final Adjudication and KB

## Название

```text
CATMAN-V3-LITE-D-FINAL-KB
```

## В контекст

Вставить `TASK_D_PROMPT.xml`.

## Прикрепить — целевой объем ≤200 КБ

```text
C_HANDOFF.json                    # ≤160 KB
SUFFICIENCY_STANDARD.md
KB_TARGET_ARCHITECTURE.md
V3_SCHEMAS.json
```

Если фактический лимит ниже 200 KB, перед загрузкой C_HANDOFF сократить до 140 KB, сохраняя IDs, gates, summaries и resource pointers.

## Результат

```text
D_l4_assessment.json
D_c_level_pack.md
D_pilots.md
CATMAN-KB/
90_V3_ARENA_HANDOFF.json
90_V3_ARENA_HANDOFF.md
99_v3_quality_report.json
```

---

# Доступ workers к GitHub resources

Каталог:

```text
CATMAN-RU-V3/LITE/resources/v2/
```

Главное правило:

```text
orchestrator читает только V2_RESOURCE_INDEX.json
worker читает только назначенные shards
```

Нельзя давать всем workers весь `resources/v2/`.

Если Spark не может читать GitHub-файлы по path:

- скачайте только shards, указанные для конкретной группы workers;
- добавьте их в Task A batches;
- не прикладывайте все 44 resources одновременно.

---

# Контроль handoff

Handoff содержит только:

- concise summaries;
- IDs;
- gate results;
- rejected/unresolved list;
- resource pointers;
- run IDs.

Handoff не содержит:

- полные source pages;
- все quotes;
- все evidence records;
- полные transcripts;
- длинные narrative reports.

Полные outputs сохраняются отдельно и доступны по pointers.

---

# Что делать с зависшей Task

1. Остановить ее.
2. Не продолжать тот же thread.
3. Не просить «сожми контекст и продолжи» — накопленное состояние остается.
4. Создать новую Task A по Lite workflow.
5. Не прикладывать `V2_INPUT_BUNDLE_FOR_V3.json`.
6. Использовать resource index и progressive handoffs.
