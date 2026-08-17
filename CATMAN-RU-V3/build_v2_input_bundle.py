#!/usr/bin/env python3
"""Build one AI-friendly V2 input file for the V3 Spark task.

The script extracts the uploaded DOCX wrappers, preserves the structured V2
handoff, adds narrative documents, file hashes, trust policy, and deterministic
forensic-audit seeds. It does not declare V2 claims true.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "CATMAN-RU" / "v2"
OUT = Path(__file__).resolve().parent / "V2_INPUT_BUNDLE_FOR_V3.json"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract_docx(path: Path) -> str:
    with ZipFile(path) as archive:
        tree = ET.fromstring(archive.read("word/document.xml"))
    lines: list[str] = []
    for paragraph in tree.iter(W + "p"):
        parts: list[str] = []
        for elem in paragraph.iter():
            if elem.tag == W + "t" and elem.text:
                parts.append(elem.text)
            elif elem.tag == W + "tab":
                parts.append("\t")
            elif elem.tag == W + "br":
                parts.append("\n")
        lines.append("".join(parts))
    return "\n".join(lines)


def doc(name: str) -> str:
    return extract_docx(V2 / name)


def doc_json(name: str):
    return json.loads(doc(name))


def doc_jsonl(name: str) -> list[dict]:
    return [json.loads(line) for line in doc(name).splitlines() if line.strip()]


def file_meta(path: Path) -> dict:
    payload = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "docx_wrapper": path.suffix.lower() == ".docx",
    }


handoff = doc_json("90_V2_ARENA_HANDOFF.json.docx")
quality = doc_json("99_v2_quality_report.json.docx")
run_manifest = doc_json("00_v2_run_manifest.json.docx")
capability = doc_json("00_v2_capability_attestation.json.docx")
freeze = doc_json("06_v2_dataset_freeze_manifest.json.docx")
patterns = doc_jsonl("16_v2_solution_patterns.jsonl.docx")
corpus = doc_jsonl("17_v2_corpus_registry.jsonl.docx")
repair_ledger = doc_jsonl("05_v2_repair_ledger.jsonl.docx")
repaired_evidence = doc_jsonl("06_v2_evidence_repaired.jsonl.docx")
red_team = doc_jsonl("18_v2_red_team_challenges.jsonl.docx")
adjudication = doc_jsonl("19_v2_adjudication_rulings.jsonl.docx")

atlas_md = doc("16_v2_solution_pattern_atlas.md.docx")
corpus_index_md = doc("17_v2_corpus_index.md.docx")
final_report_md = doc("20_v2_final_report.md.docx")
gaps_md = doc("21_v2_research_gaps.md.docx")
bibliography_md = doc("22_v2_bibliography.md.docx")
adversarial_md = doc("18_v2_adversarial_review.md.docx")
adjudication_md = doc("19_v2_adjudication_rulings.md.docx")

# Compare corpus-registry URLs with URLs printed in the narrative corpus index.
registry_by_id = {row["corpus_id"]: row for row in corpus}
index_rows: dict[str, str] = {}
for line in corpus_index_md.splitlines():
    match = re.search(r"`(V2-CORP-\d+)`", line)
    if not match:
        continue
    urls = re.findall(r"\]\((https?://[^)]+)\)", line)
    if urls:
        index_rows[match.group(1)] = urls[0]
url_mismatches = []
for corpus_id, index_url in index_rows.items():
    registry = registry_by_id.get(corpus_id)
    if registry and registry.get("url") != index_url:
        url_mismatches.append(
            {
                "corpus_id": corpus_id,
                "registry_url": registry.get("url"),
                "index_url": index_url,
            }
        )

placeholder_urls = sorted(
    {
        url
        for url in index_rows.values()
        if any(token in url for token in ("retail_conf_", "retail_ru_"))
    }
)

atlas_count_match = re.search(r"\((\d+) верифицированных свидетельств\)", atlas_md)
atlas_claimed_evidence = int(atlas_count_match.group(1)) if atlas_count_match else None
freeze_evidence = freeze.get("total_evidence_repaired")

patterns_without_evidence_links = [
    row.get("pattern_id")
    for row in patterns
    if not row.get("supporting_evidence_ids") and not row.get("evidence_ids")
]

corpus_missing_machine_status = [
    row.get("corpus_id")
    for row in corpus
    if "fetch_status" not in row or "multimodal_status" not in row
]

status_counts = freeze.get("evidence_status_breakdown", {})

source_names = [
    "00_v2_capability_attestation.json.docx",
    "00_v2_run_manifest.json.docx",
    "05_v2_repair_ledger.jsonl.docx",
    "06_v2_dataset_freeze_manifest.json.docx",
    "06_v2_evidence_repaired.jsonl.docx",
    "16_v2_solution_pattern_atlas.md.docx",
    "16_v2_solution_patterns.jsonl.docx",
    "17_v2_corpus_index.md.docx",
    "17_v2_corpus_registry.jsonl.docx",
    "18_v2_adversarial_review.md.docx",
    "18_v2_red_team_challenges.jsonl.docx",
    "19_v2_adjudication_rulings.jsonl.docx",
    "19_v2_adjudication_rulings.md.docx",
    "20_v2_final_report.md.docx",
    "21_v2_research_gaps.md.docx",
    "22_v2_bibliography.md.docx",
    "90_V2_ARENA_HANDOFF.json.docx",
    "90_V2_ARENA_HANDOFF.md.docx",
    "99_v2_quality_report.json.docx",
]

bundle = {
    "bundle_manifest": {
        "bundle_id": "CATMAN-RU-V2-INPUT-FOR-V3",
        "bundle_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "Single-file, AI-friendly V2 input for V3 forensic audit and global solution research.",
        "source_directory": "CATMAN-RU/v2",
        "semantic_priority": [
            "trust_policy_and_forensic_directives",
            "structured_v2_handoff",
            "direct_machine_artifacts",
            "narrative_documents",
        ],
        "important": "This bundle is an audit input, not ground truth. V2 PASS status must be re-tested.",
    },
    "trust_policy_and_forensic_directives": {
        "classification": "UNTRUSTED_PRIOR_RESEARCH_INPUT",
        "rules": [
            "Do not copy V2 confidence, source tier, sourced economics, project rank, or PASS status without forensic verification.",
            "Structured records have priority over narrative prose only for locating records; both remain subject to audit.",
            "Any material numerical claim requires traceable evidence/source IDs and a matching source excerpt.",
            "Corpus registry and corpus narrative index must be reconciled by ID, URL, title, date, and access status.",
            "Metadata-only or inaccessible video cannot support a transcript-derived claim.",
            "International or vendor evidence cannot retroactively validate a Russian V2 claim.",
            "Rejected and unresolved records must remain visible; zero-rejection outcomes require explicit justification.",
        ],
        "required_first_action": "Run V3 Wave Q forensic audit before exposing records to global, vendor, GitHub, architecture, or KB agents.",
    },
    "deterministic_forensic_seed": {
        "evidence_count_mismatch": {
            "freeze_manifest_count": freeze_evidence,
            "quality_report_count": quality.get("schema_validation", {}).get("evidence_repaired_valid"),
            "atlas_claimed_count": atlas_claimed_evidence,
            "direct_repaired_records_count": len(repaired_evidence),
        },
        "status_distribution": status_counts,
        "patterns_without_explicit_evidence_id_arrays": patterns_without_evidence_links,
        "corpus_records_count": len(corpus),
        "corpus_index_rows_with_url": len(index_rows),
        "corpus_registry_vs_index_url_mismatch_count": len(url_mismatches),
        "corpus_registry_vs_index_url_mismatches": url_mismatches,
        "placeholder_looking_index_urls": placeholder_urls,
        "corpus_records_missing_fetch_or_multimodal_status_count": len(corpus_missing_machine_status),
        "corpus_records_missing_fetch_or_multimodal_status_ids": corpus_missing_machine_status,
        "duplicate_file_observation": {
            "files": [
                "19_v2_adjudication_rulings.jsonl.docx",
                "19_v2_adjudication_rulings.jsonl(1).docx"
            ],
            "instruction": "Compare hashes/content and retain one canonical artifact with a documented decision."
        },
        "audit_note": "These are deterministic consistency checks, not final fact-check verdicts. Agents must open sources independently.",
    },
    "source_file_manifest": [file_meta(V2 / name) for name in source_names],
    "structured_v2_handoff": handoff,
    "direct_machine_artifacts": {
        "capability_attestation": capability,
        "run_manifest": run_manifest,
        "quality_report": quality,
        "dataset_freeze_manifest": freeze,
        "repair_ledger": repair_ledger,
        "repaired_evidence": repaired_evidence,
        "solution_patterns": patterns,
        "corpus_registry": corpus,
        "red_team_challenges": red_team,
        "adjudication_rulings": adjudication,
    },
    "narrative_documents": {
        "solution_pattern_atlas_md": atlas_md,
        "corpus_index_md": corpus_index_md,
        "adversarial_review_md": adversarial_md,
        "adjudication_rulings_md": adjudication_md,
        "final_report_md": final_report_md,
        "research_gaps_md": gaps_md,
        "bibliography_md": bibliography_md,
    },
    "v3_handoff_instruction": {
        "allowed_use": [
            "forensic audit",
            "candidate discovery after audit",
            "record repair with immutable before/after log",
            "provenance-aware input to V3 only after Q04 adjudication",
        ],
        "forbidden_use": [
            "direct copy into CATMAN-KB",
            "automatic acceptance of V2 rankings",
            "automatic acceptance of sourced_economics",
            "using narrative-only claims as evidence",
        ],
        "expected_output": "V3 accepted base containing accepted, qualified, rejected, and unresolved records with explicit reasons.",
    },
}

OUT.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
print(f"Corpus URL mismatches: {len(url_mismatches)}")
print(f"Placeholder-looking narrative URLs: {len(placeholder_urls)}")
