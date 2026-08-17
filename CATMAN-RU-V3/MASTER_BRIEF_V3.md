# Master Brief V3

## Global CatMan Solutions, Frameworks, Reference Architectures and Russia Transferability

**Версия:** 3.0

**Дата:** 17 августа 2026 года

**Research cutoff:** фактическая дата запуска

**Целевой уровень:** L4 External Decision-Ready

---

# 1. Решение, которое должно поддержать исследование

Для 3–4 наиболее значимых CatMan-направлений определить:

1. какие решения реально внедрены в России и мире;
2. какие свойства приводят к C-level sponsorship и масштабированию;
3. какие commercial products и open-source frameworks доступны;
4. как выглядит production reference architecture;
5. что переносимо в российский ритейл;
6. что следует строить, покупать или интегрировать;
7. какой пилот способен доказать ценность без выдуманного ROI.

V3 не является новым широким поиском всех болей. Боли и российский спрос берутся из V2 после forensic audit.

---

# 2. Входные гипотезы, а не готовые победители

Широкий scan охватывает шесть V2 patterns:

1. Dynamic Clearance / Fresh / RTE;
2. Space-to-Shelf / Schemograms / CV;
3. Private Label Tiering / Target Costing;
4. Forecasting & Replenishment / OSA;
5. Pricing / Promo / RGM / Net-Net;
6. Macro-Clustering / Assortment / Cost-to-Serve.

После broad scan выбираются 4 finalists. Старый рейтинг V2 не переносится автоматически.

---

# 3. Wave Q — Forensic audit V2

До международного синтеза проверить:

- несоответствие 196 vs 227 evidence в разных документах;
- traceability `sourced_economics` до evidence IDs;
- согласованность corpus registry и corpus index;
- реальность и доступность multimedia URLs;
- source tier P0/P1/S1;
- citation-to-claim alignment;
- отсутствие supported IDs в solution pattern JSON;
- zero rejected/unresolved после масштабного repair;
- подлинность KPI и attribution retailer/vendor;
- duplicate adjudication files;
- machine-readable status transcript/OCR/fetch.

Выход — `V3_ACCEPTED_V2_BASE`. Только принятые или qualified записи доступны следующим waves.

---

# 4. Wave G — Global Retail Cases

## 4.1. Исследовать по retail archetypes

- North American omnichannel grocers;
- UK/EU grocers;
- hard discounters;
- Japan/Korea convenience and fresh;
- China O2O/new retail;
- q-commerce/e-grocery;
- B2B/HoReCa wholesale;
- academic/standards benchmark.

## 4.2. Карточка кейса

```text
Retailer
→ Country/archetype
→ Pain
→ Observed solution
→ Sponsor/owner
→ Vendor or in-house
→ Architecture/capabilities
→ Data requirements
→ Pilot/scale
→ KPI/outcome
→ Duration/persistence
→ Failure/friction
→ Source provenance
→ Russia transferability notes
```

## 4.3. Правила

- vendor case не равен customer-confirmed outcome;
- международный KPI не переносится на РФ как ожидаемый эффект;
- одинаковый press release в нескольких СМИ — один source group;
- negative cases обязательны;
- market popularity отделяется от production maturity.

---

# 5. Wave V — Commercial Product Landscape

По каждому solution pattern собрать:

- product/vendor;
- capabilities;
- confirmed retailer clients;
- architecture/deployment;
- APIs/integrations;
- explainability/HITL;
- data requirements;
- implementation duration, если раскрыта;
- pricing/TCO, если раскрыты;
- security/compliance;
- Russian availability;
- sanctions/licensing/vendor-lock risk;
- customer-confirmed outcome;
- gaps.

Стартовые классы, не whitelist:

- RELEX, Blue Yonder, SymphonyAI, o9, Oracle Retail, SAP Retail;
- NielsenIQ Spaceman, dunnhumby;
- Revionics, Competera, Pricefx;
- ToolsGroup, Slimstock;
- Afresh, Invafresh, Smartway, Whywaste, Wasteless.

---

# 6. Wave O — GitHub and Open-Source Landscape

## 6.1. Категории

- forecasting;
- optimization;
- causal inference/promo;
- CV/shelf recognition;
- data quality/MDM/feature store;
- MLOps/observability;
- workflow/agents/HITL;
- vector/graph/retrieval.

## 6.2. Репозиторий оценивается по

- exact URL and owner;
- license and commercial implications;
- latest release/commit;
- release cadence;
- maintainers/contributors;
- issue response;
- tests/CI;
- security history;
- documentation;
- scale benchmarks;
- deployment references;
- fit to capability;
- integration effort;
- abandonment/fork risk.

Stars — только слабый дополнительный сигнал.

## 6.3. Минимальный кодовый due diligence

Для shortlisted repos:

- открыть LICENSE;
- проверить latest release и commit;
- просмотреть issues/security notices;
- найти runnable example;
- зафиксировать required data shape;
- оценить production gaps;
- не утверждать совместимость без документации или теста.

---

# 7. Wave D — Finalist Deep Dives and Reference Architecture

Динамически назначить D01–D04 четырем finalists после broad scan.

Для каждого создать:

1. business capability map;
2. reference data model;
3. deterministic/ML/LLM responsibility split;
4. model/optimizer architecture;
5. orchestration and HITL;
6. integration contracts;
7. observability and governance;
8. failure modes and fallbacks;
9. commercial products map;
10. open-source component map;
11. Build/Buy/Partner variants;
12. Russia transferability;
13. pilot blueprint;
14. kill criteria.

LLM не должен выполнять точные финансовые вычисления, оптимизацию или compliance rules, если их можно сделать детерминированно.

---

# 8. Wave X — Economics and Russia Transferability

Отдельный агент проверяет все finalists по двум независимым осям.

## Economics

- retailer-side outcome;
- vendor claim;
- research benchmark;
- internal assumption;
- sensitivity;
- TCO components;
- confounders;
- time-to-value evidence;
- no unsourced effect range.

## Russia fit

- sanctions and vendor access;
- 1C/local POS/WMS integration;
- FAS and pricing regulation;
- DataMatrix/marking systems;
- PII and loyalty data;
- master data quality;
- labor availability;
- store formats/logistics;
- local vendor alternatives;
- localization effort.

Global evidence оценивает solution feasibility, но не заменяет Russian market pull.

---

# 9. Wave Z/J/K — Red Team, Adjudication and KB

## Red Team

Атакует:

- survivorship bias;
- vendor laundering;
- geographic non-transferability;
- fake/open-source maturity;
- license/security risk;
- architecture theater;
- invented economics;
- data readiness;
- organizational adoption;
- commodity risk;
- excessive AI where deterministic logic is better.

## Adjudicator

Присваивает каждому finalist:

- `L4_PASS`;
- `L4_PASS_WITH_QUALIFICATIONS`;
- `L3_ONLY`;
- `REJECTED`;
- `L5_INTERNAL_VALIDATION_REQUIRED`.

## KB Builder

Строит AI-friendly KB только из adjudicated records. Narrative report не является источником данных; он генерируется из KB.

---

# 10. Финальные deliverables

1. forensic audit V2;
2. global cases registry;
3. China/Asia original-language evidence;
4. vendor/product registry;
5. GitHub/open-source registry;
6. finalist reference architectures;
7. Build/Buy/Partner matrix;
8. Russia transferability matrix;
9. sourced economics ledger;
10. Red Team and adjudication;
11. L4 sufficiency assessment;
12. C-level decision pack;
13. pilot blueprints;
14. AI-friendly `CATMAN-KB`;
15. explicit L5 validation agenda.
