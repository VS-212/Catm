# CATMAN-RU V3 LITE — progressive-context workflow

Используйте этот вариант, если одна большая V3 Task зависает или переполняет контекст.

## Основная идея

- не прикладывать `V2_INPUT_BUNDLE_FOR_V3.json` размером 2,5 МБ;
- не запускать V3 одной долгой Task;
- выполнить четыре новые Spark Tasks с чистыми контекстами;
- передавать между Tasks только компактный handoff;
- полные V2-данные хранить в GitHub shards и загружать только назначенному subagent.

## Лимит

Начальный прикрепленный контекст каждой Task — не более **200 КБ**, то есть примерно на уровне первоначального V2-задания.

## Tasks

```text
Task A — V2 Forensic Audit
→ A_HANDOFF ≤90 KB
Task B — Global/Vendor/GitHub Landscape
→ B_HANDOFF ≤130 KB
Task C — Four Reference Architectures
→ C_HANDOFF ≤160 KB
Task D — Red Team, L4 Adjudication and CATMAN-KB
```

## Файлы

- `LITE_MULTI_TASK_WORKFLOW.md` — пошаговый запуск;
- `SKILL_V3_LITE.md` — один общий Skill для четырех Tasks;
- `V2_RESOURCE_INDEX.json` — указатели на 44 небольших resource shards;
- `TASK_A_PROMPT.xml`…`TASK_D_PROMPT.xml` — prompts;
- `LITE_HANDOFF_SCHEMAS.json` — контракты handoff;
- `resources/v2/` — native JSON/JSONL/Markdown shards, не загружать все сразу;
- `build_v2_shards.py` — воспроизводимая сборка ресурсов.
