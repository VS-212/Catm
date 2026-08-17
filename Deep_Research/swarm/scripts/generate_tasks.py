#!/usr/bin/env python3
"""Generate deterministic task packets for the CatMan research swarm."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
TASKS.mkdir(parents=True, exist_ok=True)

COMMON = {
    "project_id": "CATMAN-RU-DR-2024-2026",
    "task_packet_version": "1.0",
    "language": "ru",
    "research_cutoff": "2026-08-14",
    "common_policy_ref": "prompts/COMMON_POLICY.xml",
    "master_brief_ref": "../MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md",
    "require_real_independent_context": True,
    "forbid_role_simulation_in_orchestrator_context": True,
}


def emit(agent_id: str, payload: dict) -> None:
    data = {**COMMON, "agent_id": agent_id, **payload}
    (TASKS / f"{agent_id}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


emit("U01", {
    "role": "universe_curator",
    "wave": "W0_FOUNDATION",
    "objective": "Определить воспроизводимый Top-10 grocery/FMCG-ритейлеров РФ по авторитетному ranking source.",
    "scope": {"market": "Russia grocery/FMCG retail", "task": "universe only"},
    "inputs": ["master_brief", "common_policy"],
    "forbidden_inputs": ["collector_outputs", "preliminary_conclusions", "project_preferences"],
    "outputs": ["01_retailer_universe.json", "01_universe_decision.md"],
    "completion_criteria": ["ranking publisher/year/metric fixed", "Top-10 IDs R01..R10 assigned", "adjacent group separated", "sensitivity alternative documented"]
})

emit("O01", {
    "role": "ontology_curator",
    "wave": "W0_FOUNDATION",
    "objective": "Зафиксировать CatMan ontology, synonym map, maturity stages и терминологические границы.",
    "scope": {"task": "ontology only"},
    "inputs": ["master_brief", "common_policy"],
    "forbidden_inputs": ["collector_outputs", "preliminary_conclusions", "project_preferences"],
    "outputs": ["02_ontology.json", "02_ontology_notes.md"],
    "completion_criteria": ["L1/L2 topics fixed", "raw-to-normalized rules fixed", "store terminology separated", "stakeholder and maturity vocabularies fixed"]
})

for rank in range(1, 11):
    agent_id = f"R{rank:02d}"
    emit(agent_id, {
        "role": "retailer_researcher",
        "wave": "W1_COLLECTION",
        "objective": f"Собрать retailer-specific evidence для сети rank {rank} frozen universe.",
        "dynamic_assignment": {"retailer_selector": {"rank": rank, "from": "01_retailer_universe.json"}},
        "inputs": ["common_policy", "assigned_retailer_card_only", "02_ontology.json"],
        "forbidden_inputs": ["peer_collector_outputs", "preliminary_conclusions", "project_shortlist", "user_conversation"],
        "search_requirements": ["2024", "2025", "2026_YTD", "all_L1_topics", "P0_P1_first", "implementation_signals", "disconfirming_search", "not_found_log"],
        "output_schemas": ["schemas/source_record.schema.json", "schemas/evidence_record.schema.json"],
        "outputs": [f"{agent_id}_sources.jsonl", f"{agent_id}_evidence.jsonl", f"{agent_id}_search_log.md", f"{agent_id}_gaps.md"],
        "id_prefixes": {"source": f"{agent_id}-S", "evidence": f"{agent_id}-E"}
    })

cross_lanes = {
    "X01": {
        "lane": "official_corporate",
        "scope": ["annual reports", "strategy", "CMD/investor presentations", "official retailer news", "regulatory filings"],
        "special_rules": ["Prefer original documents", "Capture page/slide for quotes and numbers"]
    },
    "X02": {
        "lane": "commitment_signals",
        "scope": ["vacancies", "RFP/tenders", "procurement notices", "partnerships", "organizational changes"],
        "special_rules": ["Commitment is not outcome", "Record job/RFP expiry and archived URL where possible"]
    },
    "X03": {
        "lane": "video_and_conferences",
        "scope": ["official videos", "conference videos", "webinars", "podcasts", "conference programs"],
        "special_rules": ["Build 15-30 video shortlist", "Evidence requires transcript and verified timestamp", "Program title is metadata only"]
    },
    "X04": {
        "lane": "media_research_vendor_disconfirmation",
        "scope": ["trade media", "business media", "industry research", "vendor cases as leads", "negative/disconfirming evidence"],
        "special_rules": ["Trace claims to originating source", "Do not upgrade vendor claim", "Group reposts"]
    },
}
for agent_id, lane in cross_lanes.items():
    emit(agent_id, {
        "role": "cross_source_researcher",
        "wave": "W1_COLLECTION",
        "objective": f"Провести cross-retailer поиск в lane {lane['lane']}.",
        "source_lane": lane,
        "inputs": ["common_policy", "01_retailer_universe.json", "02_ontology.json"],
        "forbidden_inputs": ["retailer_collector_outputs", "preliminary_conclusions", "project_shortlist"],
        "output_schemas": ["schemas/source_record.schema.json", "schemas/evidence_record.schema.json"],
        "outputs": [f"{agent_id}_sources.jsonl", f"{agent_id}_evidence.jsonl", f"{agent_id}_lane_log.md"],
        "id_prefixes": {"source": f"{agent_id}-S", "evidence": f"{agent_id}-E"}
    })

fact_lanes = {
    "F01": {
        "primary_partition": "stable_hash(evidence_id) mod 3 == 0",
        "overlays": ["all records with numbers/KPI", "all C-level/C-1 records", "all maturity >= 4"],
        "focus": "quote/date/number/speaker provenance"
    },
    "F02": {
        "primary_partition": "stable_hash(evidence_id) mod 3 == 1",
        "overlays": ["all vendor records", "all secondary media", "all duplicate independence groups"],
        "focus": "source independence, vendor laundering and deduplication"
    },
    "F03": {
        "primary_partition": "stable_hash(evidence_id) mod 3 == 2",
        "overlays": ["all video-derived records", "all store terminology records", "all H1 timeline records"],
        "focus": "terminology, timestamps, maturity and temporal integrity"
    },
}
for agent_id, lane in fact_lanes.items():
    emit(agent_id, {
        "role": "blind_fact_checker",
        "wave": "W2_FACT_CHECK",
        "objective": f"Проверить assigned records; specialty: {lane['focus']}.",
        "assignment": lane,
        "inputs": ["common_policy", "01_retailer_universe.json", "02_ontology.json", "03_source_registry_raw.jsonl", "04_evidence_raw.jsonl"],
        "forbidden_inputs": ["preliminary_conclusions", "trend_rankings", "project_shortlist", "peer_fact_check_outputs"],
        "output_schema": "schemas/fact_check.schema.json",
        "outputs": [f"{agent_id}_fact_checks.jsonl", f"{agent_id}_exceptions.md"],
        "id_prefixes": {"check": f"{agent_id}-C"}
    })

analysis_lanes = {
    "N01": {
        "lane": "temporal_trends",
        "objective": "Построить temporal waves 2024→2025→2026 YTD и проверить H1 Лента-2025→рынок-2026 против H0.",
        "required_outputs": ["trend claims", "first observed signals", "maturity transitions", "H1 verdict candidates", "counterexplanations"]
    },
    "N02": {
        "lane": "pain_stakeholder",
        "objective": "Построить pain chains и содержательно разделить C-level, CCO, CatMan, PM и смежных owners.",
        "required_outputs": ["pain claims", "stakeholder ownership", "KPI mechanisms", "current response and limitations", "gaps"]
    },
    "N03": {
        "lane": "alternative_hypotheses",
        "objective": "Сравнить широту/зрелость конкурирующих CatMan-направлений без проектного дизайна и confirmation bias.",
        "required_outputs": ["topic demand breadth", "maturity comparison", "media-vs-demand separation", "strongest alternatives", "commodity and evidence risks"]
    },
}
for agent_id, lane in analysis_lanes.items():
    emit(agent_id, {
        "role": "blind_analyst",
        "wave": "W3_ANALYSIS",
        "objective": lane["objective"],
        "analytical_lane": lane["lane"],
        "inputs": ["common_policy", "01_retailer_universe.json", "02_ontology.json", "06_evidence_verified.jsonl", "06_dataset_freeze_manifest.json"],
        "forbidden_inputs": ["project_winner", "peer_analysis", "user_conversation_outside_brief"],
        "output_schema": "schemas/claim.schema.json",
        "required_outputs": lane["required_outputs"],
        "outputs": [f"{agent_id}_claims.jsonl", f"{agent_id}_analysis.md"],
        "id_prefixes": {"claim": f"{agent_id}-K"}
    })

emit("P01", {
    "role": "project_designer",
    "wave": "W4_PROJECTS",
    "objective": "Сформировать 5-7 evidence-linked CatMan проектов, top-3 и условного лидера.",
    "inputs": ["common_policy", "06_evidence_verified.jsonl", "08_claims_ledger_pre_adjudication.jsonl", "N01_analysis.md", "N02_analysis.md", "N03_analysis.md", "master_brief_project_rules"],
    "forbidden_inputs": ["red_team_output", "user_conversation_outside_brief"],
    "mandatory_alternatives": ["store clustering/local assortment", "AI assortment", "SKU/full cost", "space", "fresh/OOS/waste", "promo/RGM", "private label/e-grocery", "supplier collaboration", "data foundation"],
    "output_schema": "schemas/project_hypothesis.schema.json",
    "outputs": ["10_project_hypotheses.jsonl", "10_project_one_pagers.md", "10_project_scorecard.csv"]
})

emit("Z01", {
    "role": "adversarial_reviewer",
    "wave": "W5_RED_TEAM",
    "objective": "Попытаться опровергнуть material claims, trend ranking и project winner.",
    "inputs": ["common_policy", "06_evidence_verified.jsonl", "08_claims_ledger_pre_adjudication.jsonl", "09_analytical_synthesis_pre_redteam.md", "10_project_hypotheses.jsonl", "10_project_one_pagers.md", "10_project_scorecard.csv"],
    "forbidden_inputs": ["adjudicator_verdict"],
    "required_attacks": ["confirmation bias", "semantic drift", "media amplification", "vendor laundering", "maturity inflation", "stakeholder inflation", "temporal illusion", "alternative winner", "commodity risk", "causality", "data readiness", "organizational fit"],
    "output_schema": "schemas/red_team_challenge.schema.json",
    "outputs": ["11_red_team_challenges.jsonl", "11_adversarial_review.md"],
    "id_prefixes": {"challenge": "Z01-Z"}
})

emit("J01", {
    "role": "adjudicator",
    "wave": "W6_ADJUDICATION",
    "objective": "Разрешить material conflicts, утвердить allowed wording и собрать финальный handoff bundle.",
    "inputs": ["all frozen outputs through W5", "00_capability_attestation.json", "00_run_manifest.json"],
    "repair_budget": {"max_runs": 4, "only_for": ["invalid schema", "broken critical citation", "critical coverage gap", "material unresolved conflict"]},
    "output_schemas": ["schemas/adjudication.schema.json", "schemas/run_manifest.schema.json", "schemas/quality_report.schema.json"],
    "outputs": ["12_adjudication.jsonl", "13_final_report.md", "14_research_gaps.md", "15_bibliography.md", "90_ARENA_HANDOFF.json", "90_ARENA_HANDOFF.md", "99_run_quality_report.json"],
    "id_prefixes": {"adjudication": "J01-J"}
})

print(f"Generated {len(list(TASKS.glob('*.json')))} task packets in {TASKS}")
