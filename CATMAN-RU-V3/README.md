# CATMAN-RU V3 — Global Solutions, Frameworks and AI-friendly Knowledge Base

V3 превращает российскую карту спроса V1/V2 в decision-ready базу решений:

```text
Russian pain and demand
→ observed global solutions
→ commercial products
→ open-source frameworks
→ reference architectures
→ Russia transferability
→ Build / Buy / Partner
→ pilot decision pack
→ AI-friendly Knowledge Base
```

## Целевой уровень

V3 должен достичь **Sufficiency Level L4 — External Decision-Ready**. Уровень L5 требует внутренних данных ритейлера, интервью и пилота и не может быть достигнут только веб-исследованием.

## Главные файлы

- `SUFFICIENCY_STANDARD.md` — когда исследование можно остановить;
- `MASTER_BRIEF_V3.md` — полный research brief;
- `SPARK_V3_WORKFLOW.md` — запуск в Gemini Spark;
- `ORCHESTRATOR_V3_PROMPT.xml` — текст в контекст новой Task;
- `SKILL_V3.md` — новый Spark Skill;
- `v3_manifest.yaml` — 30 specialist runs + 2 capability workers;
- `SOURCE_AND_QUERY_MAP.md` — русские, английские, китайские, научные и GitHub-источники;
- `V3_SCHEMAS.json` — контракты данных;
- `KB_TARGET_ARCHITECTURE.md` — структура итоговой knowledge base;
- `V2_INPUT_BUNDLE_FOR_V3.json` — все необходимые V2-артефакты и forensic audit seeds в одном AI-friendly файле;
- `build_v2_input_bundle.py` — воспроизводимая сборка V2 bundle из исходных DOCX.

## Runtime

Используется тот же аккаунт и актуальная версия Gemini Spark, но создается **новая top-level Task и новый Skill V3**. Продолжать V2 Task запрещено из-за контекстного загрязнения предыдущими выводами.

Если одна V3 Task зависает или переполняет контекст, используйте `LITE/LITE_MULTI_TASK_WORKFLOW.md`: четыре отдельные Tasks, compact handoffs и GitHub resource shards. В Lite-режиме большой `V2_INPUT_BUNDLE_FOR_V3.json` не загружается.
