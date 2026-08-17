# CATMAN-KB Target Architecture

## 1. Принцип

Knowledge Base — не папка отчетов и не только vector index. Источник истины — versioned structured records с provenance; граф, chunks и narrative views являются производными.

## 2. Структура

```text
CATMAN-KB/
├── 00_manifest/
│   ├── kb_manifest.json
│   ├── versions.json
│   ├── provenance_policy.md
│   └── quality_report.json
├── 01_ontology/
│   ├── catman_ontology.json
│   ├── terminology.json
│   ├── entity_types.json
│   └── relation_types.json
├── 02_entities/
│   ├── retailers.jsonl
│   ├── stakeholders.jsonl
│   ├── pains.jsonl
│   ├── solution_patterns.jsonl
│   ├── observed_solutions.jsonl
│   ├── products.jsonl
│   ├── repositories.jsonl
│   ├── architectures.jsonl
│   ├── technologies.jsonl
│   ├── kpis.jsonl
│   └── regulations.jsonl
├── 03_evidence/
│   ├── sources.jsonl
│   ├── evidence.jsonl
│   ├── claims.jsonl
│   ├── fact_checks.jsonl
│   ├── adjudications.jsonl
│   ├── sourced_economics.jsonl
│   └── rejected_records.jsonl
├── 04_global/
│   ├── retailer_cases.jsonl
│   ├── china_original_language.jsonl
│   ├── negative_cases.jsonl
│   ├── vendor_products.jsonl
│   ├── github_repositories.jsonl
│   └── transferability.jsonl
├── 05_multimodal/
│   ├── media_registry.jsonl
│   ├── transcripts/
│   ├── transcript_segments.jsonl
│   ├── image_ocr/
│   └── slide_table_extractions.jsonl
├── 06_graph/
│   ├── nodes.jsonl
│   ├── edges.jsonl
│   └── catman_knowledge_graph.jsonld
├── 07_retrieval/
│   ├── chunks.jsonl
│   ├── chunk_source_map.jsonl
│   ├── retrieval_filters.json
│   └── retrieval_instructions.md
├── 08_decision/
│   ├── sufficiency_assessments.jsonl
│   ├── build_buy_partner.jsonl
│   ├── pilot_blueprints.jsonl
│   └── l5_validation_agenda.jsonl
└── 09_views/
    ├── current_pains.md
    ├── c_level_view.md
    ├── commercial_director_view.md
    ├── catman_pm_view.md
    ├── solution_catalog.md
    └── decision_pack.md
```

## 3. Главная цепочка

```text
Retailer
→ Stakeholder
→ Pain
→ Business impact/KPI
→ Observed solution
→ Solution pattern
→ Global case
→ Commercial product / OSS repository
→ Reference architecture
→ Russia transferability
→ Build/Buy/Partner
→ Pilot
→ Evidence / Source / Fact-check / Adjudication
```

## 4. Retrieval design

Каждый chunk должен хранить:

- `chunk_id`;
- semantic text;
- source/evidence/claim IDs;
- entity IDs;
- topic and geography;
- event/publication dates;
- current vs historical layer;
- F/R/I/H/A class;
- confidence;
- source tier;
- adjudication status;
- language/original language;
- access restrictions.

Нельзя индексировать rejected records как обычный факт. Их можно хранить в отдельном corpus для hallucination defense.

## 5. Graph rules

- любой material edge имеет evidence IDs;
- inference edge отличается от observed edge;
- temporal validity обязательна для ownership, product status и maturity;
- vendor claim и customer confirmation — разные nodes/edges;
- international outcome и Russia expected effect не соединяются relation `proves`; допустимо `benchmarks`;
- assumptions не повышают confidence при повторном цитировании.

## 6. Narrative views

Markdown views генерируются из KB и не редактируют source of truth. При обновлении evidence views пересобираются.

## 7. Versioning

- immutable source/evidence IDs;
- correction через supersedes/replaces;
- `valid_from/valid_to`;
- changelog;
- run ID и agent ID;
- content hash where available;
- schema version;
- reproducible build manifest.

## 8. Quality checks

- schema validation;
- referential integrity;
- duplicate URL/source-group detection;
- claim without evidence detection;
- broken URL queue;
- date cutoff and temporal contradictions;
- unsupported numerical claim detection;
- source-tier consistency;
- transcript/timestamp validation;
- graph orphan nodes;
- final-view wording vs adjudication.
