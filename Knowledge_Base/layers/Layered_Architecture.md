# Layered Architecture — Детальное описание слоёв

## Общая схема вертикальной интеграции

```
L6 Infrastructure
        ↑
L5 Governance & Memory
        ↑
L4 Execution ← Executor / Negotiator
        ↑
L3 Strategic ← Strategist Agent
        ↑
L2 Analytical ← Analyst Agent
        ↑
L1 Business ← Domain Rules
```

## Подробное описание каждого слоя

### L1 — Business / Domain Layer
**Назначение**: Бизнес-правила и политика компании.

**Сущности**: Category, SKU, Supplier, Promo (бизнес-атрибуты)

**Агенты**: Domain Rules Agent

**Примеры правил**:
- Минимальная маржа по категории ≥ 28%
- SKU с ABC=C и XYZ=Z подлежат выводу
- Запрет промо на определённые категории без одобрения КД

### L2 — Analytical Layer
**Назначение**: Превращение данных в insights.

**Сущности**: Forecast, Margin (расчётные), Drift, Elasticity

**Агенты**: Analyst Agent, Watchdog, Margin Detector

**Ключевые процессы**:
- ABC-XYZ анализ
- Детекция изменений поведения
- Прогнозирование
- Маржинальный мониторинг

### L3 — Strategic Layer
**Назначение**: Принятие решений и сценарии.

**Сущности**: Decision, Recommendation, Scenario, WhatIf

**Агенты**: Strategist Agent

**Ключевые процессы**:
- Генерация рекомендаций
- What-if анализ
- Подготовка сценариев для C-level

### L4 — Execution Layer
**Назначение**: Реализация решений в системах.

**Сущности**: EmailDraft, ExcelUpdate, 1CTransaction, PromoAction

**Агенты**: Executor Agent, Negotiator Agent

**Ключевые процессы**:
- Отправка писем
- Обновление цен и остатков
- Создание промо

### L5 — Governance & Memory Layer
**Назначение**: Корпоративная память, аудит, профиль пользователя.

**Сущности**: AuditTrail, CorporateMemory, UserProfile, NegotiationHistory

**Агенты**: Governance Agent, Memory Agent

**Ключевые процессы**:
- Хранение всех решений с обоснованием
- X-ray поставщика
- Институциональная память переговоров

### L6 — Infrastructure / Integration Layer
**Назначение**: Подключение к внешним системам.

**Сущности**: 1CConnection, ExcelFile, EmailAccount, POSStream, MarketplaceAPI

**Агенты**: Integration Agent

**Ключевые процессы**:
- Синхронизация данных
- Выполнение действий через API / файлы

## Принципы взаимодействия слоёв

1. **Контекст передаётся вниз** (L2 → L4)
2. **Результаты и подтверждения — вверх** (L4 → L5)
3. **Human-in-the-Loop** на L3–L4 (approval gates)
4. **Память** на L5 — доступна всем слоям

## Преимущества архитектуры

- Чёткое разделение ответственности
- Легко тестировать и масштабировать
- Готовность к multi-agent системам
- Поддержка "вау"-эффекта через вертикальную интеграцию

**Статус**: Определена. Готова к детализации в `layers/`.