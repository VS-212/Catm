# CATMAN Agent Kit

Единая чистая папка для передачи другому AI-агенту.

## Состав

- `START_HERE.md` — точка входа;
- `KNOWN_ISSUES.json` — открытые проблемы качества;
- `RESOURCE_INDEX.json` — карта файлов и hashes;
- `context/` — universe и ontology;
- `knowledge/retailers/` — по одному компактному файлу на сеть;
- `knowledge/market_context.json` — межрыночные сигналы;
- `knowledge/corpus.json` — Retail.ru/TAdviser corpus;
- `knowledge/analysis.json` — claims, patterns, Red Team, adjudication;
- `knowledge/manifests.json` — run/freeze/quality metadata;
- `reports/` — V2 narrative outputs с предупреждением;
- `research/` — V3 sufficiency, sources, schemas, KB target;
- `workflow/` — облегченный четырехзадачный Spark workflow.

## Source of truth

Ни один narrative report не является source of truth. Источник истины после V3 — только adjudicated structured records с evidence IDs и provenance.
