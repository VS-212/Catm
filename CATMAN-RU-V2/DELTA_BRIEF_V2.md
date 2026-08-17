# Delta Brief V2

## CATMAN-RU: Evidence Repair → Solution Pattern Atlas → Targeted Corpus → Independent Adjudication

**Версия:** 2.0

**Дата подготовки:** 17 августа 2026 года

**Baseline cutoff:** 14 августа 2026 года

**V2 cutoff:** фактическая дата запуска Spark Task

**Язык:** русский; поиск на русском и английском

---

# 1. Мандат

Не повторять исходное исследование целиком. Использовать артефакты `CATMAN-RU/` как входной dataset, но не считать их claims, confidence, project scores и final report автоматически истинными.

Нужно:

1. исправить provenance, coverage и validation defects;
2. отделить фактические внедрения от сгенерированных проектных гипотез;
3. определить повторяющиеся паттерны решений, которые получают executive sponsorship, масштабирование или повторное финансирование;
4. закрыть критические пробелы через Retail.ru и Retail TAdviser;
5. выполнить только targeted historical backfill;
6. заново провести Red Team и adjudication.

---

# 2. Известные дефекты, обязательные к проверке

Это стартовый audit queue, а не окончательный обвинительный verdict.

1. `04_evidence_raw` содержит 190 records, `05_fact_checks` — 106 verdicts, но `06_evidence_verified` содержит 189 records. Проверить 84 records без явного check.
2. Run `R08` отмечен completed, но в merged registry отсутствуют его собственные source/evidence records.
3. У `R09` присутствуют собственные source records, но отсутствуют собственные evidence records.
4. Покрытие Top-10 неравномерно; R08/R09 существенно слабее R01/R02/R04.
5. Проверить baseline cutoff: материалы после 2026-08-14 не должны молча входить в baseline dataset.
6. Пересмотреть P0/P1/S1: публикация отраслевого СМИ не является P0 только потому, что содержит конкретные сведения.
7. Проверить дедупликацию URL и independence groups.
8. Проверить ontology drift: normalized_topic_l1 должен соответствовать frozen L1 для каждого L2.
9. Перекалибровать confidence: все 57 claims не должны автоматически быть high; unresolved допустим.
10. Проверить numerical provenance в project hypotheses. Числа, встречающиеся только в project record, должны стать `A/TBD`, а не `sourced`.
11. Проверить citation-to-claim alignment, включая URL, которые ведут на материал с другой темой.
12. Rejected evidence не должно находиться в verified dataset или supporting claims.

---

# 3. Временная политика без перегрузки backfill

## 3.1. Hot layer

Период `2024-01-01..v2_cutoff` используется для Current Value, executive demand и выбора проектов.

## 3.2. Baseline/delta

- события и публикации до 2026-08-14 остаются baseline;
- публикации после 2026-08-14 получают `delta_post_baseline=true`;
- нельзя исправлять cutoff violation простой заменой даты публикации на дату события;
- baseline и delta показываются отдельно.

## 3.3. Cold layer

Период 2019–2023 используется только при trigger:

- claim содержит «первый», «новый», «emerging»;
- нужно установить prior art;
- нужно понять, почему решение раньше не масштабировалось;
- Red Team выявил повтор старого commodity;
- solution finalist требует проверки устойчивости.

Cold layer не увеличивает Current Demand Score. Он дает context, prior art и failure history.

---

# 4. Wave R — Evidence Repair

## Цель

Создать канонический `verified_dataset_v2`, которому можно доверять перед новым анализом.

## Работы

1. Извлечь DOCX wrappers в нативные JSON/JSONL/Markdown/CSV без семантического изменения.
2. Повторно проверить 84 records без explicit fact check.
3. Восстановить или честно зафиксировать gaps R08/R09.
4. Проверить URL, даты, цитаты, роли, числа, source tier и maturity.
5. Пересобрать independence groups и deduplication.
6. Нормализовать L1/L2 по frozen ontology.
7. Перепроверить все claims и project numerical assumptions.
8. Создать immutable repair log.

## Запрещено

- защищать старый final report;
- проектировать новые решения;
- повышать confidence при merge;
- исправлять цитату «по смыслу» без источника;
- добивать coverage выдуманными records.

## Gate R

Продолжение разрешено только если:

- каждый verified record имеет explicit check либо прозрачный policy exception;
- все source/evidence/claim references целы;
- coverage gaps честно зафиксированы;
- numerical assumptions переклассифицированы;
- quality status не скрывает material qualifications.

---

# 5. Wave S — Solution Pattern Atlas

## Главный вопрос

Какие свойства решений приводят не просто к пилоту, а к C-level/CCO sponsorship, rollout, повторному бюджету, раскрытому KPI или переносу на другие форматы?

## Не путать

- `project hypothesis` — предложенный исследователем проект;
- `observed solution` — реально заявленное/внедренное решение сети;
- `executive acceptance` — наблюдаемый сигнал поддержки;
- `successful outcome` — результат, подтвержденный KPI и scope;
- `media popularity` — частота публикаций.

## Executive acceptance signals

Сильные:

- прямая поддержка CEO/CCO/CFO/COO;
- budget/team/ownership;
- pilot → rollout;
- расширение охвата;
- повторное финансирование/renewal;
- KPI disclosure;
- перенос на другие категории/форматы;
- сохранение решения после 12+ месяцев.

Слабые:

- одно интервью;
- conference title;
- vendor case без retailer confirmation;
- пилот без последующего статуса;
- PR-фраза «используем AI».

## Обязательные solution lenses

1. Simplify before automate.
2. Central engine + format-specific guardrails.
3. Fast measurable P&L loop.
4. In-house core vs vendor module by retailer tier.
5. Labor-reducing vs labor-adding automation.
6. Data readiness as admission gate.
7. Human approval/governance.
8. Format-specific solution architecture.
9. Failure and de-scaling patterns.
10. Commodity vs differentiating capability.

## Выход

- observed solution registry;
- executive acceptance signals;
- solution patterns;
- anti-patterns/failures;
- pain→solution graph;
- format segmentation;
- pattern confidence and counterexamples.

---

# 6. Wave C — Targeted Retail.ru + Retail TAdviser Corpus

## Scope

### Исчерпывающий goal-relevant scan

`2024-01-01..v2_cutoff`:

- CatMan;
- assortment;
- space/planograms;
- pricing/promo/RGM;
- STM/private label;
- fresh/waste/OOS/F&R;
- supplier/JBP;
- retail data/AI/automation;
- store formats/clustering/localization;
- actual solution outcomes and failures.

### Targeted historical backfill

2019–2023 только по finalist patterns и prior-art triggers.

## Content types

- news, articles, interviews and cases;
- company/project/product cards;
- photos and diagrams;
- embedded video/audio;
- conference records;
- documents, slides and tables;
- vendor claims and retailer confirmations.

## Multimodal protocol

- OCR meaningful images/slides;
- transcribe relevant audio/video;
- verify timestamps for quotations;
- store metadata-only status when content was not actually processed;
- do not infer content from title/thumbnail.

## Source policy

Retail.ru и TAdviser — отраслевые corpora, а не автоматические primary sources. Material claims require original retailer documents, direct speech or independent corroboration where available.

## Completeness

Report:

- URL inventory size;
- fetched/failed/blocked counts;
- content-type and year coverage;
- duplicate clusters;
- transcript/OCR coverage;
- source gaps;
- reason for stopping historical backfill.

---

# 7. Wave A — Independent Red Team and Adjudication

Новый Red Team не видит старый project winner до завершения собственного review repaired claims.

Adjudicator получает:

- repaired dataset;
- solution patterns;
- site corpus evidence;
- old conclusions as hypotheses;
- new Red Team challenges.

Финал должен содержать:

1. current pain map;
2. observed solution map;
3. executive acceptance pattern atlas;
4. anti-patterns;
5. format segmentation;
6. revised project shortlist;
7. top-3 with switch conditions;
8. sourced vs assumption economics;
9. pilot decision pack;
10. remaining gaps and next evidence needed.

---

# 8. Критерии завершения V2

- исходные файлы сохранены неизменными;
- все repairs прослеживаются;
- нет unchecked verified evidence;
- baseline и post-baseline delta разделены;
- current demand не раздувается историческими records;
- solution acceptance подтверждается behavior/scale, а не словом «нравится»;
- каждая pattern card содержит counterexample;
- Retail.ru/TAdviser coverage измерено, а не объявлено «полным»;
- project numbers имеют provenance либо маркировку A/TBD;
- final wording не сильнее adjudication.
