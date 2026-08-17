# Workflow запуска CATMAN-RU V3 в Gemini Spark

# 1. Нужен ли новый Spark?

## Не требуется

- новый аккаунт;
- новая подписка;
- отдельная установка;
- продолжение старого V2 Task.

## Требуется

- актуальный доступный runtime того же Gemini Spark;
- **новая top-level Task**;
- **новый Skill V3**;
- чистый task context;
- новые subagent runs;
- новая output folder.

Правило:

```text
тот же Spark account/runtime
→ новый Skill V3
→ новая Task V3
→ новые clean-context agents
```

Продолжать V2 Task нельзя: в ней закреплены прежние claims, economics и winner ranking.

Новый отдельный workspace/account нужен только если Spark не позволяет отключить старую память/Skill, достигнут лимит файлов/tasks или нужна организационная изоляция доступа.

---

# 2. Параметры

| Parameter | Recommended value |
|---|---|
| Task name | `CATMAN-RU-V3-GLOBAL-SOLUTIONS-KB` |
| Run mode | One-time long-running task |
| Personal memory | Off |
| Active Skill | Только V3 |
| V1/V2 Skills | Off |
| Preferred concurrency | 8 |
| Maximum concurrency | 10 |
| Retry | 1 per specialist |
| Repair budget | 5 bounded runs |
| Web access | Для G/V/O/X и назначенных Q/D/Z |
| GitHub access | Для O01–O05 |
| Unrelated connectors | Off |
| File output | On |
| Chat output | Status/gates only |
| Research cutoff | Run date |
| Target | L4 External Decision-Ready |

Если доступен reasoning level:

- Q/G/V/O: medium-high;
- M01/D01–D04/X01/Z01: high;
- J01: maximum available;
- K01: high with strict schemas.

---

# 3. Что загрузить

## В контекстное окно

Вставить полное содержимое:

```text
CATMAN-RU-V3/ORCHESTRATOR_V3_PROMPT.xml
```

## В Skills

Создать новый Skill:

```text
CATMAN-RU-V3/SKILL_V3.md
```

## Как V3 instruction files

```text
CATMAN-RU-V3/SUFFICIENCY_STANDARD.md
CATMAN-RU-V3/MASTER_BRIEF_V3.md
CATMAN-RU-V3/v3_manifest.yaml
CATMAN-RU-V3/V3_SCHEMAS.json
CATMAN-RU-V3/SOURCE_AND_QUERY_MAP.md
CATMAN-RU-V3/KB_TARGET_ARCHITECTURE.md
```

## Как V2 input — один объединенный файл

Загрузите только:

```text
CATMAN-RU-V3/V2_INPUT_BUNDLE_FOR_V3.json
```

Не загружайте отдельные DOCX из `CATMAN-RU/v2`: bundle уже содержит structured handoff, repaired evidence, repair ledger, solution patterns, corpus registry, Red Team, adjudication, run/quality manifests, полный final report, Solution Pattern Atlas, Corpus Index, gaps и bibliography.

В bundle дополнительно встроены:

- trust policy `UNTRUSTED_PRIOR_RESEARCH_INPUT`;
- SHA-256 manifest исходных DOCX;
- обязательные forensic directives;
- автоматическая сверка evidence counts;
- список V2 patterns без явных evidence ID arrays;
- 49 расхождений URL между corpus registry и narrative corpus index;
- 17 placeholder-looking URL в narrative index;
- контроль отсутствующих fetch/multimodal statuses;
- observation о дубликате adjudication-файла.

Эти observations — стартовая очередь аудита, а не автоматически доказанные ошибки фактов.

---

# 4. Запуск по waves

## C0 — capability re-attestation

Spark запускает T01/T02 с разными nonce. Первый файл:

```text
00_v3_capability_attestation.json
```

Нужны новые run IDs и подтверждение clean contexts. Старый V2 PASS не копируется.

## Q — forensic audit V2

Q01–Q03 независимы, Q04 adjudicates.

Проверяются:

- evidence counts 196 vs 227;
- economics → evidence traceability;
- corpus registry vs narrative index;
- multimedia access/transcripts;
- source tiers;
- URLs/citations;
- zero rejected/unresolved;
- duplicate files and records.

После Q Spark показывает gate `V2_BASE_ACCEPTED`.

### Если gate принят

```text
Forensic gate принят. Заморозь accepted V2 base и запускай L_GLOBAL_LANDSCAPE batches по v3_manifest.yaml. Не передавай agents V2 winner как ground truth.
```

### Если есть critical defects

```text
Forensic gate не принят. Не запускай глобальный synthesis. Исправь critical defects в пределах repair budget либо исключи записи из accepted V2 base и выпусти обновленный forensic report.
```

## L — global/vendor/GitHub landscape

Запускаются 17 независимых runs:

```text
G01–G08
V01–V04
O01–O05
```

При concurrency 8:

1. G01–G08;
2. V01–V04 + O01–O04;
3. O05 и bounded repairs.

Agents не видят peer conclusions.

## M — shortlist

M01 получает frozen outputs и выбирает ровно четыре finalists. Применяет mandatory L4 pre-gates. Создает:

```text
40_four_finalists.json
41_shortlist_decision.md
```

## D — architectures

D01–D04 запускаются параллельно по одному finalist на clean context. После них X01 проверяет economics и Russia fit.

## A — final

Последовательно:

```text
Z01 Red Team
→ J01 L4 Adjudicator
→ K01 KB Builder
```

K01 получает только accepted/qualified records J01.

---

# 5. Контроль достаточности

Не задавайте требование «найди 500 источников». Остановка определяется `SUFFICIENCY_STANDARD.md`.

Для каждого finalist J01 должен показать Gates A–H:

```text
A Russian pull
B Global production evidence
C Value/economics
D Reference architecture
E Products/frameworks
F Russia transferability
G Pilot decision
H Epistemic/Red Team
```

Допустимые verdicts:

```text
L4_PASS
L4_PASS_WITH_QUALIFICATIONS
L3_ONLY
REJECTED
L5_INTERNAL_VALIDATION_REQUIRED
```

Если отсутствуют внутренние данные конкретной сети, итог не может называться L5.

---

# 6. Что должно быть в progress report

После wave:

- actual run IDs;
- completed/failed/retried;
- files;
- accepted/qualified/rejected/unresolved counts;
- coverage by region/archetype/pattern;
- source/customer confirmation counts;
- failed L4 gates;
- next gate.

Не принимать «я сыграл роли нескольких агентов» без run IDs.

---

# 7. Финальные файлы

Обязателен весь список `required_outputs` из manifest.

Критический минимум:

```text
03_v2_forensic_report.md
10_global_cases.jsonl
11_china_original_language_evidence.jsonl
20_vendor_products.jsonl
30_github_repositories.jsonl
40_four_finalists.json
54_reference_architectures.md
60_sourced_economics_ledger.jsonl
61_russia_transferability_matrix.jsonl
62_build_buy_partner_matrix.md
71_v3_adjudication.jsonl
72_l4_sufficiency_assessment.json
73_c_level_decision_pack.md
74_pilot_blueprints.md
80_CATMAN_KB/
90_V3_ARENA_HANDOFF.json
90_V3_ARENA_HANDOFF.md
99_v3_quality_report.json
```

---

# 8. Что загрузить обратно в Arena

Минимум:

```text
90_V3_ARENA_HANDOFF.json
90_V3_ARENA_HANDOFF.md
72_l4_sufficiency_assessment.json
73_c_level_decision_pack.md
74_pilot_blueprints.md
99_v3_quality_report.json
```

Желательно также CATMAN-KB либо его manifest/nodes/edges.

Инструкция Arena:

```text
Загружены результаты CATMAN-RU V3.

Сначала проверь forensic audit V2, global customer confirmations, vendor claims, GitHub license/maintenance, international-to-Russia transferability, sourced economics, L4 Gates A–H и Red Team. Затем проверь referential integrity CATMAN-KB. Не повышай L4 до L5 без внутренних данных и пилота.
```
