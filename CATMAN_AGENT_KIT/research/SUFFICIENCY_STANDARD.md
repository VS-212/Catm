# Стандарт достаточности исследования CATMAN-RU

## 1. Уровни зрелости

| Level | Название | Что можно делать |
|---:|---|---|
| L0 | Inventory | Перечислять источники и термины |
| L1 | Signal Map | Формировать гипотезы о болях и трендах |
| L2 | Evidence-Based Market Map | Уверенно описывать российский рыночный спрос |
| L3 | Solution-Informed | Сравнивать наблюдаемые решения и кейсы |
| **L4** | **External Decision-Ready** | **Выбрать 3–4 решения, Build/Buy/Partner и спроектировать пилот** |
| L5 | Organization-Specific Investment-Ready | Защищать бюджет на данных конкретного ритейлера и результатах пилота |

## 2. Достаточный уровень для верхнеуровневой цели

Цель V3 — **L4**.

L4 достаточно, чтобы:

- выбрать проектные направления;
- сформировать reference architecture;
- отобрать готовые продукты и open-source-компоненты;
- подготовить C-level decision pack;
- определить pilot design и data readiness;
- принять предварительное Build/Buy/Partner решение.

L4 недостаточно, чтобы обещать конкретный ROI конкретной сети. Для этого нужен L5.

---

# 3. Обязательные L4-gates для каждого финального решения

Средний высокий балл не компенсирует провал обязательного gate.

## Gate A — Russian Market Pull

- минимум 3 независимых российских ритейлера с retailer-specific signal;
- минимум один signal уровня commitment/scale;
- минимум один подтвержденный C/C-1 owner либо прямая связь с его KPI;
- все material claims имеют проверяемый provenance;
- absence of evidence не превращена в negative fact.

## Gate B — Global Production Evidence

- минимум 3 независимых международных retailer cases;
- минимум 2 географии или retail archetypes;
- минимум один production/scale case;
- минимум один negative, stopped, replaced или materially constrained case;
- vendor case без customer confirmation маркируется отдельно.

## Gate C — Value Mechanism and Economics

- построена причинная цепочка capability → process → operational KPI → financial KPI;
- есть минимум один retailer-side disclosed outcome либо честно указано, что его нет;
- sourced numbers отделены от benchmark и assumptions;
- есть sensitivity model и confounders;
- отсутствуют диапазоны эффекта без источника.

## Gate D — Reference Architecture

Зафиксированы:

- data inputs и data quality requirements;
- canonical entities и grain;
- deterministic calculations vs ML/LLM responsibilities;
- optimization/forecast/causal components;
- APIs, ERP/POS/WMS/MDM/BI integration;
- human approval и exception workflow;
- observability, audit trail, fallback;
- security, privacy и model governance;
- batch/streaming requirements;
- pilot-to-production migration.

## Gate E — Product and Framework Landscape

- минимум 2 релевантных commercial products;
- минимум 2 open-source building blocks либо доказано, что OSS-вариант непрактичен;
- проверены license, maintenance, releases, security и integration maturity;
- stars не используются как единственный критерий;
- определены gaps между готовыми компонентами и необходимым продуктом.

## Gate F — Russia Transferability

Проверены:

- доступность в РФ и sanctions/vendor lock-in;
- локальные ERP/POS/WMS и 1С-интеграции;
- ФАС, маркировка, персональные данные и отраслевое регулирование;
- качество российских master data;
- стоимость и дефицит персонала;
- логистическая и форматная специфика;
- требования к аппаратному парку;
- российские аналоги/замены.

## Gate G — Pilot Decision

Есть:

- pilot unit и owner;
- treatment/control или другой credible evaluation design;
- baseline requirements;
- primary KPI и guardrails;
- data readiness checklist;
- implementation dependencies;
- stop/kill criteria;
- scale decision rule;
- список данных, которые нужно получить у заказчика в первую неделю.

## Gate H — Epistemic and Adversarial Quality

- 100% material claims связаны с evidence IDs;
- ссылки открыты и соответствуют тезисам;
- quotes/timestamps проверены;
- есть independent Red Team;
- у каждого finalist — strongest counterargument;
- unresolved issues сохранены;
- final wording не сильнее adjudication.

---

# 4. Saturation stop rule

Исследование по направлению можно остановить, когда одновременно:

1. выполнены Gates A–H;
2. два независимых поисковых прохода не добавили нового material solution pattern;
3. новые источники преимущественно повторяют существующие independence groups;
4. найден минимум один counterexample;
5. remaining gaps не способны поменять top-3 без внутренних данных;
6. adjudicator присвоил `L4_PASS` или `L4_PASS_WITH_QUALIFICATIONS`.

Нельзя продолжать поиск только ради количества источников.

---

# 5. Условия L5

L5 достигается только после внешнего исследования:

- 5–10 интервью CCO/CatMan/PM/Operations/Supply Chain;
- data audit конкретной сети;
- внутренний baseline;
- TCO и integration estimate;
- пилот с контрольной группой или credible counterfactual;
- подтвержденный эффект;
- решение о rollout.

До L5 любые ROI конкретного заказчика маркируются `assumption / to be measured`.
