# START HERE — инструкция следующему агенту

## Цель

Продолжить исследование CatMan до L4 External Decision-Ready и собрать проверенную AI-friendly Knowledge Base.

## Порядок чтения

1. `README.md`.
2. `KNOWN_ISSUES.json` — обязательная forensic очередь.
3. `context/retailer_universe.json` и `context/catman_ontology.json`.
4. `RESOURCE_INDEX.json`.
5. Загружать только нужные `knowledge/retailers/Rxx.json`, а не все одновременно.
6. Для нового глобального исследования использовать `workflow/LITE_MULTI_TASK_WORKFLOW.md`.

## Критическое правило

V2 reports, solution patterns, confidence и economics — prior research input, не ground truth. Сначала выполнить Task A forensic audit. Не принимать `PASS` из старого quality report автоматически.

## Контекстный бюджет

Не загружать всю папку в одно context window. Использовать progressive loading и handoff ≤90/130/160 KB.
