# Исполняемый swarm-пакет

## Назначение

Пакет предназначен для внешнего web-оркестратора, способного создавать реальные независимые sub-agent runs с отдельными контекстными окнами, web research и файловыми результатами.

## Топология

- **1 внешний оркестратор** — управляет графом, но не подменяет специалистов.
- **25 specialist runs**:
  - 2 foundation agents;
  - 10 retailer researchers;
  - 4 cross-source researchers;
  - 3 blind fact-checkers;
  - 3 blind analysts;
  - 1 project designer;
  - 1 adversarial reviewer;
  - 1 adjudicator.
- **До 4 repair runs** разрешены только для исправления невалидного формата или критических пробелов.

## Волны

```text
W0: U01 + O01
 ↓ freeze universe and ontology
W1: R01…R10 + X01…X04
 ↓ raw evidence merge and deduplication
W2: F01…F03
 ↓ verified dataset freeze
W3: N01…N03
 ↓ claims/trends/pains
W4: P01
 ↓ project shortlist
W5: Z01
 ↓ adversarial challenge
W6: J01
 ↓ adjudication and final bundle
```

## Принцип независимости

- R/X-агенты не видят результаты других collectors.
- F-агенты не видят preliminary conclusions, project shortlist или предпочтение победителя.
- N-агенты получают один frozen verified dataset, но разные аналитические задания.
- P01 не получает историю пользовательской переписки; только adjudicable claims и verified evidence.
- Z01 получает проектный shortlist только после его фиксации.
- J01 получает обе стороны: synthesis/project outputs и Red Team.

## Форматы

- конфигурация: YAML;
- agent task packet: JSON;
- prompt boundaries: XML-like;
- machine outputs: JSONL по JSON Schema;
- narrative outputs: Markdown;
- таблицы для человека: CSV как производный экспорт.

## Критическое правило

Оркестратор обязан сначала создать `00_capability_attestation.json`. Если он не может доказуемо породить отдельные agent runs, он должен вернуть `HALT_NO_REAL_SUBAGENTS` и остановиться. Ролевая симуляция внутри одного чата запрещена.

## Source of truth

При конфликте файлов действует порядок:

1. `MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md` — исследовательский смысл;
2. `swarm_manifest.yaml` — граф исполнения и доступы;
3. JSON Schemas — формат результата;
4. task packet — локальный scope конкретного агента;
5. prompt role file — поведение роли.

Локальная инструкция не может отменить эпистемические правила мастер-брифа.
