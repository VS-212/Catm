# Agent: Analyst Agent

**ID**: `agent:Analyst`  
**Тип**: Analytical Agent (L2)  
**Роль в вертикальной интеграции**: Средний слой — превращает данные в insights

## Описание
Постоянно мониторит данные (продажи, остатки, маржа, drift), генерирует аналитику и передаёт контекст Strategist Agent.

## Основные задачи (MVP)

1. ABC-XYZ анализ
2. Детекция drift (изменение поведения SKU)
3. OOS (out-of-stock) алерты
4. Маржинальный детектор (walk rate, утечки)
5. Сезонный post-mortem
6. Ранние сигналы (Early Warning)

## Инструменты (Tools)

- Чтение Excel / 1С (через Integration Agent)
- Статистические расчёты (Python / pandas)
- Генерация отчётов в Markdown / JSON
- Передача контекста в n8n workflow

## Вход / Выход

**Вход**:
- Данные из POS / 1С / Excel (реал-тайм или batch)
- Сигналы от Integration Agent

**Выход**:
- Структурированные insights (JSON)
- Контекст для Strategist Agent
- Алерты в Telegram / Email

## Пример workflow (n8n)

```yaml
trigger: schedule (каждые 4 часа)
  ↓
Integration Agent → данные
  ↓
Analyst Agent:
  - ABC-XYZ
  - Drift detection
  - Margin watch
  ↓
Output: structured JSON + alert
  ↓
Strategist Agent (следующий слой)
```

## "Вау"-эффект

> "Утром я вижу не сырые цифры, а готовые выводы: 'Категория X теряет 4,2 п.п. маржи из-за drift SKU-78432'"

## Связанные сущности

- `Category`, `SKU`, `Margin`, `Forecast`

## Статус
MVP — высокоприоритетный агент.