# Как запустить реальный исследовательский рой в Gemini Spark

## 1. Что именно запускается

Пакет рассчитан на **25 отдельных specialist runs плюс внешний orchestrator**:

| Волна | Агенты | Задача |
|---|---:|---|
| W0 | U01, O01 | Universe и CatMan ontology |
| W1 | R01–R10, X01–X04 | Независимый сбор evidence |
| W2 | F01–F03 | Слепой факт-чек |
| W3 | N01–N03 | Независимый анализ |
| W4 | P01 | Проектный shortlist |
| W5 | Z01 | Red Team |
| W6 | J01 | Adjudication и финальная сборка |

Это не ролевая игра одного Gemini-контекста. Каждый specialist должен быть отдельным фактическим run с собственным context window.

---

# 2. Перед запуском

## 2.1. Проверьте доступность функций

В используемом Gemini Spark должны быть доступны:

- создание настоящих subagents/worker tasks;
- отдельный контекст каждого worker;
- web research у collectors;
- параллельное или хотя бы изолированное последовательное выполнение;
- сохранение отдельных файлов;
- длительная задача, не завершающаяся после одного ответа.

Если Spark умеет только составлять agent briefs/workflow plans, но не запускает subagents, этот пакет нельзя считать выполненным. Capability gate специально остановит такую попытку.

## 2.2. Не добавляйте в постановку желаемый ответ

Не дописывайте:

- «кластеризация наверняка победит»;
- «докажи, что весь рынок пришел к теме»;
- «Лента была первым игроком»;
- ожидаемые проценты ROI.

Все это должно остаться проверяемыми гипотезами.

---

# 3. Получение файлов с GitHub

Каталог проекта на рабочей ветке GitHub:

```text
https://github.com/VS-212/Catm/tree/arena/01a0008b-catm/Deep_Research
```

Путь внутри репозитория:

```text
Deep_Research/
```

Исполняемый пакет:

```text
Deep_Research/swarm/
```

Если репозиторий доступен Spark через GitHub, передайте ссылку на каталог ветки и попросите прочитать только перечисленные ниже файлы. Если репозиторий приватный или Spark не умеет надежно читать GitHub, скачайте файлы и загрузите их напрямую либо положите в одну папку Google Drive и прикрепите эту папку к задаче.

## Минимальный upload set — 6 файлов

1. `Deep_Research/MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md`
2. `Deep_Research/swarm/ORCHESTRATOR_BOOTSTRAP_PROMPT.xml`
3. `Deep_Research/swarm/swarm_manifest.yaml`
4. `Deep_Research/swarm/upload_bundle/ALL_ROLE_PROMPTS.xml`
5. `Deep_Research/swarm/upload_bundle/ALL_TASKS.json`
6. `Deep_Research/swarm/upload_bundle/ALL_SCHEMAS.json`

Опционально:

7. `Deep_Research/swarm/SKILL.md`
8. этот файл с инструкцией.

Компактный upload bundle эквивалентен индивидуальным файлам `prompts/`, `tasks/` и `schemas/`. Не нужно одновременно загружать и compact bundle, и все 40+ исходных файлов.

---

# 4. Настройка Spark

Названия элементов интерфейса могут отличаться между версиями. Нужны логические действия, а не конкретная кнопка.

## Вариант A — через Skill

Если Spark позволяет создавать reusable Skill:

1. Создайте новый Skill.
2. Название: `CatMan RU Evidence Swarm`.
3. Загрузите `SKILL.md` как основную инструкцию.
4. Добавьте к Skill пять остальных исполняемых файлов, если интерфейс это поддерживает.
5. Не включайте память других исследований и старые CatMan-выводы.
6. Создайте новую Task с этим Skill.

## Вариант B — обычная Task

1. Создайте отдельную новую задачу, а не продолжайте старый чат.
2. Название: `CATMAN-RU-DR-2024-2026`.
3. Прикрепите шесть файлов минимального upload set.
4. Отключите ненужный personal context, если UI позволяет.
5. Вставьте в task instruction **полное содержимое** `ORCHESTRATOR_BOOTSTRAP_PROMPT.xml`.
6. Запустите задачу.

---

# 5. Первый обязательный контроль: capability gate

Первым результатом должен стать:

```text
00_capability_attestation.json
```

Не принимайте простую фразу «я могу работать как несколько агентов». Требуйте:

- `attestation_status = PASS_REAL_SWARM`;
- минимум два фактически созданных test sub-agent runs;
- разные run/task IDs;
- подтверждение отдельных context windows;
- отдельные outputs тестовых workers;
- web access и file output у worker runs.

Если вернулся один из статусов:

```text
HALT_NO_REAL_SUBAGENTS
HALT_NO_CONTEXT_ISOLATION
HALT_NO_WEB
```

не просите Spark «все равно продолжить». Иначе получится симуляция роя.

Если статус `LIMITED_REQUIRES_USER_APPROVAL`, разрешайте продолжение только когда ограничение касается concurrency. Ограничение можно обойти batches; отсутствие изоляции — нельзя.

---

# 6. Как контролировать волны

## W0 — Foundation

Ожидается два независимых run ID и файлы:

```text
01_retailer_universe.json
01_universe_decision.md
02_ontology.json
02_ontology_notes.md
```

Проверьте:

- рейтинг имеет издателя, год, метрику и URL;
- Top-10 не выбран приблизительно;
- присвоены стабильные IDs R01–R10;
- кластеризация и локализация не объявлены одним термином.

После этого universe и ontology замораживаются.

## W1 — Collection

Должны существовать 14 отдельных collector runs:

```text
R01–R10
X01–X04
```

Критерии:

- R-агент видел только одну assigned retailer card;
- X-агент видел только свою source lane;
- collectors не видели outputs друг друга;
- каждый сохранил собственный search log;
- прямые URL и цитаты присутствуют;
- конференционная программа не подменяет transcript.

Если concurrency ограничена, допустимы batches, например `R01–R07`, затем `R08–R10 + X01–X04`. Контексты должны оставаться отдельными.

## W2 — Blind fact-check

Три отдельные проверки:

- F01 — цитаты, даты, роли и числа;
- F02 — независимость источников, перепечатки и vendor laundering;
- F03 — терминология, видео, maturity и временная целостность.

Они не должны видеть project shortlist или предварительный вывод о тренде.

Обязательные результаты:

```text
05_fact_checks.jsonl
06_evidence_verified.jsonl
06_dataset_freeze_manifest.json
```

До появления dataset freeze проектные рекомендации запрещены.

## W3–W6

Далее Spark выполняет manifest:

- N01–N03 — три независимых analytical lenses;
- P01 — 5–7 проектов после freeze;
- Z01 — отдельный Red Team после фиксации shortlist;
- J01 — adjudication и максимум четыре bounded repair runs.

Не позволяйте orchestrator объединять N01–N03 в один общий prompt: независимые разногласия являются частью контроля качества.

---

# 7. Что должно быть на выходе

Обязателен весь список `required_handoff_bundle` из `swarm_manifest.yaml`.

Особенно важны:

```text
00_capability_attestation.json
00_run_manifest.json
03_source_registry.jsonl
04_evidence_raw.jsonl
05_fact_checks.jsonl
06_evidence_verified.jsonl
08_claims_ledger.jsonl
10_project_hypotheses.jsonl
11_red_team_challenges.jsonl
12_adjudication.jsonl
13_final_report.md
90_ARENA_HANDOFF.json
90_ARENA_HANDOFF.md
99_run_quality_report.json
```

`00_run_manifest.json` должен содержать для каждого worker:

- agent ID;
- фактический Spark run/task ID;
- start/end timestamp;
- input file names;
- output file names;
- status;
- retry count;
- error summary;
- желательно model/runtime identifier, если Spark его раскрывает.

## Минимальные количественные признаки нормального запуска

Это не автоматическое доказательство качества, но smoke test:

- 25 specialist runs без учета capability-test и repairs;
- все 10 ритейлеров покрыты;
- цель 80–120 raw records, минимум 50 только при реальном наличии;
- 15–30 video candidates;
- отдельное число фактически транскрибированных/проверенных видео;
- каждый material claim связан с evidence IDs;
- rejected records не находятся в verified dataset;
- Red Team содержит доказательные, а не риторические возражения.

Не требуйте добивать record quota мусорными источниками.

---

# 8. Сообщения для управления Spark

## Если Spark остановился после capability gate

```text
Capability gate принят. Продолжай строго с W0_FOUNDATION по swarm_manifest.yaml. Не выполняй роли U01 и O01 в контексте оркестратора: создай два отдельных agent runs. После W0 покажи run IDs, файлы и freeze decision.
```

## После W0

```text
Universe и ontology проверены. Заморозь их и запускай W1_COLLECTION. Создай отдельные runs R01–R10 и X01–X04. Не передавай collectors outputs их peers. При лимите concurrency используй batches без объединения контекстов.
```

## Если агент начал предлагать проект раньше времени

```text
Останови project synthesis. Dataset еще не прошел W2 и не заморожен. Удали преждевременные recommendations из рабочего состояния и вернись к текущему gate. Продолжение разрешено только по manifest.
```

## Для финальной проверки

```text
Перед завершением проверь required_handoff_bundle, JSON Schema validation, referential integrity source_id/evidence_id/claim_id и наличие фактических run IDs всех specialists. Затем создай 90_ARENA_HANDOFF.json и 90_ARENA_HANDOFF.md.
```

---

# 9. Как передать результаты обратно в Arena

ZIP может быть неудобен для загрузки и чтения. Лучше приложить отдельными файлами:

1. `90_ARENA_HANDOFF.json`;
2. `90_ARENA_HANDOFF.md`;
3. `13_final_report.md`;
4. `99_run_quality_report.json`;
5. при допустимом размере — `03_source_registry.jsonl`, `05_fact_checks.jsonl`, `06_evidence_verified.jsonl`, `12_adjudication.jsonl`.

Если интерфейс не принимает `.jsonl`, используйте созданный `90_ARENA_HANDOFF.json`. Не вставляйте десятки тысяч строк в чат.

Текст нового запроса в Arena:

```text
Загружены результаты внешнего реального swarm-run по проекту CATMAN-RU-DR-2024-2026.

Проверь сначала:
1. capability attestation и run manifest;
2. соответствие evidence/source/claim IDs;
3. факт-чек и rejected records;
4. не стали ли формулировки финального отчета сильнее adjudication;
5. не подтверждена ли исходная гипотеза через confirmation bias.

Затем собери независимый итоговый артефакт для C-level и PM CatMan. Не добавляй новых фактов без отдельного web fact-check. При конфликте приоритет имеют verified evidence и adjudication, а не narrative report.
```

Если `90_ARENA_HANDOFF.json` слишком велик, попросите Spark разделить его без изменения записей:

```text
90_ARENA_HANDOFF_part_01.json
90_ARENA_HANDOFF_part_02.json
...
90_ARENA_HANDOFF_INDEX.json
```

Разделять лучше по верхнеуровневым массивам либо по retailer_id, сохраняя глобальные IDs.

---

# 10. Признаки фиктивного «роя»

Остановите run, если:

- Spark пишет «я выступил в роли 25 агентов»;
- отсутствуют отдельные run IDs;
- все specialist outputs появились в одном ответе без файлов;
- fact-checker ссылается на project winner до W4;
- collectors знают результаты peers;
- search calls названы agents;
- один и тот же narrative повторяется во всех результатах;
- нет raw evidence, но уже есть уверенный финальный проект;
- capability attestation заполнена обещаниями без test runs.

Главный критерий: **не количество названий ролей, а фактическая независимость вызовов и проверяемый provenance каждого вывода**.
