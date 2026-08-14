# Catman Ontology (High-Level Semantic Model)

**Версия**: 0.9 (готово к эволюции в OWL/RDF)  
**Метод**: Entity + Layered + GRACE-like

## Core Classes (Сущности)

```turtle
@prefix cat: <https://catm.ai/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

cat:Category a owl:Class ;
    rdfs:label "Category" ;
    cat:hasLayer cat:L1, cat:L2, cat:L3, cat:L4, cat:L5 .

cat:SKU a owl:Class ;
    rdfs:label "SKU" ;
    cat:belongsTo cat:Category ;
    cat:hasMargin cat:Margin .

cat:Supplier a owl:Class ;
    rdfs:label "Supplier" ;
    cat:supplies cat:SKU, cat:Category .

cat:Margin a owl:Class ;
    rdfs:label "Margin" ;
    cat:calculatedFor cat:SKU, cat:Category, cat:Supplier .

cat:Forecast a owl:Class ;
    rdfs:label "Forecast" ;
    cat:predicts cat:SKU, cat:Category .

cat:Promo a owl:Class ;
    rdfs:label "Promo" ;
    cat:affects cat:SKU, cat:Margin .

cat:Decision a owl:Class ;
    rdfs:label "Decision" ;
    cat:approvedBy cat:User ;
    cat:basedOn cat:Recommendation .
```

## Layers as Contexts

```turtle
cat:Layer a owl:Class .
cat:L1 a cat:Layer ; rdfs:label "Business/Domain" .
cat:L2 a cat:Layer ; rdfs:label "Analytical" .
cat:L3 a cat:Layer ; rdfs:label "Strategic" .
cat:L4 a cat:Layer ; rdfs:label "Execution" .
cat:L5 a cat:Layer ; rdfs:label "Governance & Memory" .
cat:L6 a cat:Layer ; rdfs:label "Infrastructure" .
```

## Agent Hierarchy (GRACE-like)

```turtle
cat:Agent a owl:Class .
cat:AnalystAgent a cat:Agent ; cat:operatesOn cat:L2 .
cat:StrategistAgent a cat:Agent ; cat:operatesOn cat:L3 .
cat:ExecutorAgent a cat:Agent ; cat:operatesOn cat:L4 .
cat:NegotiatorAgent a cat:Agent ; cat:operatesOn cat:L4 .
cat:GovernanceAgent a cat:Agent ; cat:operatesOn cat:L5 .
```

## Key Relationships

- `cat:Category` → `cat:hasSKU` → `cat:SKU`
- `cat:SKU` → `cat:hasMargin` → `cat:Margin`
- `cat:Margin` → `cat:drives` → `cat:Decision`
- `cat:Decision` → `cat:executedBy` → `cat:ExecutorAgent`
- `cat:Supplier` → `cat:hasXRay` → `cat:NegotiationHistory` (L5)

## Future Evolution Path

1. **v1.0** — текущая модель (Markdown + JSON Schema)
2. **v1.5** — экспорт в RDF/TTL
3. **v2.0** — полноценная OWL-онтология + SHACL constraints + Semantica integration
4. **v3.0** — reasoning engine + multi-agent marketplace (GRACE)

**Статус**: Высокоуровневая семантическая модель готова.