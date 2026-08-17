# Source and Query Map V3

Все перечисленные продукты, сайты и репозитории — discovery seeds, а не автоматически одобренные решения.

# 1. Источниковая иерархия

## P0/P1

- retailer annual reports, strategy, CMD/investor presentations;
- official engineering/product blogs;
- executive interviews and verified conference transcripts;
- procurement/RFP and official project announcements;
- customer-confirmed implementation outcomes;
- product documentation, release notes and LICENSE files;
- peer-reviewed papers with reproducible methodology.

## Secondary/context

- отраслевые СМИ;
- analyst reports;
- vendor pages;
- aggregators;
- GitHub popularity metrics.

Secondary source может дать lead, но material outcome требует первичного либо независимого подтверждения.

---

# 2. Global retailer seeds by archetype

## North America

Walmart, Kroger, Target, Costco, Loblaw, Albertsons, Publix.

## UK/Europe

Tesco, Carrefour, Ahold Delhaize, Sainsbury’s, Morrisons, Coop, E.Leclerc, Mercadona.

## Hard discount

Aldi, Lidl, Penny, Netto.

## Japan/Korea convenience and fresh

7-Eleven Japan, Lawson, FamilyMart, AEON, Ito-Yokado, CU, GS25.

## China/O2O

Hema/Freshippo, JD Retail/7Fresh, Meituan, Yonghui, Sun Art, RT-Mart.

## E-grocery/q-commerce

Ocado, Instacart, Picnic, Rohlik, Wolt Market.

## B2B/HoReCa

Metro, Sysco, US Foods, Booker.

Выбор кейса определяется решением и архетипом, а не известностью бренда.

---

# 3. Англоязычные отраслевые источники

- NRF;
- FMI;
- IGD;
- Grocery Dive;
- Progressive Grocer;
- Retail TouchPoints;
- RetailWire;
- RIS News;
- ECR Retail Loss;
- Retail Systems Research;
- retailer engineering blogs;
- investor relations portals;
- conference organizers and verified video channels.

# 4. Scientific/technical

- INFORMS;
- ACM Digital Library;
- IEEE Xplore;
- arXiv;
- SSRN;
- Google Scholar;
- university operations research and retail labs;
- GS1 standards;
- NRF ARTS data models where relevant.

Search concepts:

```text
retail assortment optimization field experiment
shelf space allocation retail production case
perishable markdown optimization supermarket
retail demand substitution assortment rationalization
promotion incrementality causal inference grocery
store clustering localized assortment production
on shelf availability phantom inventory retail
private label target costing retail
retail category management decision support architecture
```

---

# 5. Китайские источники

## Industry and association

- 中国连锁经营协会 / CCFA;
- 联商网 / Linkshop;
- 亿邦动力 / Ebrun;
- 36氪 / 36Kr;
- CNKI;
- official Alibaba/Hema materials;
- JD Retail/JD Logistics materials;
- Meituan technical and investor materials;
- annual reports and exchange filings.

## Chinese query seeds

```text
零售 品类管理 优化
商品组合 优化 零售
门店 聚类 本地化 商品
生鲜 损耗 动态折扣
便利店 鲜食 订货 预测
货架 空间 优化 陈列
零售 促销 效果 因果推断
自有品牌 成本 管理
即时零售 商品结构
零售 补货 预测 系统
```

## Translation protocol

Каждый material claim хранит:

- original Chinese quote;
- source URL/title/date;
- literal translation;
- normalized Russian/English term;
- translator agent ID;
- ambiguity note;
- independent corroboration where possible.

Китайский кейс оценивается отдельно по transferability: density, delivery economics, payments, data access, labor, regulation and platform structure.

---

# 6. Commercial product seeds

## Assortment/space/merchandising

RELEX, Blue Yonder, SymphonyAI, o9, Oracle Retail, SAP Retail, NielsenIQ Spaceman, dunnhumby.

## Pricing/RGM/promo

Revionics, Competera, Pricefx, Blue Yonder Pricing, SymphonyAI, o9, antuit.ai.

## Forecasting/replenishment

RELEX, Blue Yonder, SAP F&R, Oracle Retail, ToolsGroup, Slimstock, o9.

## Fresh/waste/markdown

Afresh, Invafresh, Smartway, Whywaste, Wasteless, Too Good To Go Platform.

Queries:

```text
{product} retailer customer case KPI
{product} implementation architecture API
{product} grocery rollout annual report
{retailer} {product} pilot scale outcome
{product} documentation integration data model
{product} pricing TCO implementation time
{product} Russia availability sanctions
```

---

# 7. GitHub/open-source seeds

## Forecasting

- `Nixtla/statsforecast`;
- `Nixtla/mlforecast`;
- `Nixtla/neuralforecast`;
- `awslabs/gluonts`;
- `sktime/pytorch-forecasting`;
- `unit8co/darts`.

## Optimization

- `google/or-tools`;
- `Pyomo/pyomo`;
- `cvxpy/cvxpy`;
- Optuna and compatible optimization tooling.

## Causal/promo

- `py-why/dowhy`;
- EconML/PyWhy;
- `uber/causalml`;
- Bayesian/time-series causal packages.

## Data/MLOps

- `feast-dev/feast`;
- `mlflow/mlflow`;
- Great Expectations;
- Soda Core;
- `datahub-project/datahub`;
- OpenMetadata;
- dbt.

## Computer vision

- `opencv/opencv`;
- `open-mmlab/mmdetection`;
- `facebookresearch/detectron2`;
- `ultralytics/ultralytics`;
- SKU110K-related datasets/implementations.

## Agent/workflow/retrieval

- `langchain-ai/langgraph`;
- Temporal SDKs;
- `n8n-io/n8n`;
- Haystack;
- LlamaIndex;
- `pgvector/pgvector`;
- `qdrant/qdrant`;
- Neo4j/Memgraph.

## GitHub queries

```text
"retail assortment optimization" language:Python
"shelf space optimization" retail
"perishable markdown optimization"
"retail demand forecasting" grocery
"promotion uplift" causal inference retail
"planogram compliance" computer vision
"SKU110K" detection
"store clustering" assortment
"phantom inventory" retail
```

## Repository due diligence

Check exact repo, license, latest release/commit, contributors, issue velocity, CI/tests, security advisories, docs, deployment examples, scale and commercial restrictions. Forks and abandoned demos are not production frameworks.
