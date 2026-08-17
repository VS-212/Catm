# CatMan RU Deep Research — AI-native swarm package

Этот каталог содержит два слоя одного исследования:

1. **Смысловой источник истины** — `MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md`.
2. **Исполняемый пакет реального роя** — `swarm/`.

Исследование должно установить доказанный спрос на CatMan-проекты у Top-10 российских grocery/FMCG-ритейлеров за 01.01.2024–14.08.2026, проверить гипотезу «Лента-2025 → рынок-2026», сравнить конкурирующие проектные направления и сформировать проектный shortlist без выдуманных фактов и ROI.

## Быстрый запуск в Gemini Spark

1. Откройте `swarm/ORCHESTRATOR_INSTRUCTIONS_GEMINI_SPARK.md`.
2. Загрузите в Spark файлы, перечисленные в разделе «Минимальный upload set».
3. Вставьте без изменений текст из `swarm/ORCHESTRATOR_BOOTSTRAP_PROMPT.xml`.
4. Не разрешайте исследование, пока Spark не пройдет capability gate и не подтвердит реальные изолированные sub-agent calls.
5. После завершения выгрузите обязательный handoff bundle и добавьте его в следующую Arena-сессию для независимой сборки и ревью.

## Структура

```text
Deep_Research/
├── README.md
├── MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md
└── swarm/
    ├── README.md
    ├── ORCHESTRATOR_INSTRUCTIONS_GEMINI_SPARK.md
    ├── ORCHESTRATOR_BOOTSTRAP_PROMPT.xml
    ├── SKILL.md
    ├── swarm_manifest.yaml
    ├── prompts/
    ├── schemas/
    ├── tasks/
    ├── scripts/
    └── templates/
```

## Важное ограничение

XML-like теги, роли и отдельные task-файлы сами по себе не создают независимых агентов. Изоляцию контекстов должен фактически обеспечивать внешний оркестратор. Если платформа не умеет порождать отдельные sub-agent runs, выполнение следует остановить, а не имитировать рой одним контекстом.
