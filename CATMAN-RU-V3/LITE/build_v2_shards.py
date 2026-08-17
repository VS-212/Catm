#!/usr/bin/env python3
"""Extract V1/V2 DOCX wrappers into small native resource shards.

These shards stay in GitHub/Drive and are fetched by assigned subagents on
demand. They must not all be attached to the orchestrator's initial context.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
V1 = ROOT / "CATMAN-RU"
V2 = V1 / "v2"
OUT = Path(__file__).resolve().parent / "resources" / "v2"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def extract(path: Path) -> str:
    with ZipFile(path) as archive:
        tree = ET.fromstring(archive.read("word/document.xml"))
    lines: list[str] = []
    for p in tree.iter(W + "p"):
        parts: list[str] = []
        for e in p.iter():
            if e.tag == W + "t" and e.text:
                parts.append(e.text)
            elif e.tag == W + "tab":
                parts.append("\t")
            elif e.tag == W + "br":
                parts.append("\n")
        lines.append("".join(parts))
    return "\n".join(lines)


def json_doc(path: Path):
    return json.loads(extract(path))


def jsonl_doc(path: Path) -> list[dict]:
    return [json.loads(line) for line in extract(path).splitlines() if line.strip()]


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = "\n".join(line.rstrip() for line in text.splitlines())
    path.write_text(cleaned + "\n", encoding="utf-8")


sources = jsonl_doc(V1 / "03_source_registry.jsonl.docx")
evidence = jsonl_doc(V2 / "06_v2_evidence_repaired.jsonl.docx")
repairs = jsonl_doc(V2 / "05_v2_repair_ledger.jsonl.docx")
corpus = jsonl_doc(V2 / "17_v2_corpus_registry.jsonl.docx")
patterns = jsonl_doc(V2 / "16_v2_solution_patterns.jsonl.docx")
red_team = jsonl_doc(V2 / "18_v2_red_team_challenges.jsonl.docx")
adjudication = jsonl_doc(V2 / "19_v2_adjudication_rulings.jsonl.docx")

# Canonical small machine resources.
write_json(OUT / "manifests" / "quality.json", json_doc(V2 / "99_v2_quality_report.json.docx"))
write_json(OUT / "manifests" / "freeze.json", json_doc(V2 / "06_v2_dataset_freeze_manifest.json.docx"))
write_json(OUT / "manifests" / "run.json", json_doc(V2 / "00_v2_run_manifest.json.docx"))
write_jsonl(OUT / "patterns" / "solution_patterns.jsonl", patterns)
write_jsonl(OUT / "patterns" / "red_team.jsonl", red_team)
write_jsonl(OUT / "patterns" / "adjudication.jsonl", adjudication)

# Evidence and source shards by retailer; market/cross-source records stay separate.
retailer_ids = [f"R{i:02d}" for i in range(1, 11)]
for rid in retailer_ids:
    write_jsonl(OUT / "evidence" / f"{rid}.jsonl", [r for r in evidence if r.get("retailer_id") == rid])
    write_jsonl(OUT / "sources" / f"{rid}.jsonl", [r for r in sources if r.get("retailer_id") == rid])
write_jsonl(
    OUT / "evidence" / "MARKET_CONTEXT.jsonl",
    [r for r in evidence if r.get("retailer_id") not in retailer_ids],
)
write_jsonl(
    OUT / "sources" / "CROSS_SOURCE.jsonl",
    [r for r in sources if r.get("retailer_id") not in retailer_ids],
)

# Repair shards follow retailer ownership of the linked evidence.
evidence_to_retailer = {r.get("evidence_id"): r.get("retailer_id") for r in evidence}
repair_groups = {
    "R01_R02": {"R01", "R02"},
    "R03_R04": {"R03", "R04"},
    "R05_R06": {"R05", "R06"},
    "R07_R08": {"R07", "R08"},
    "R09_R10_MARKET": {"R09", "R10", "market_context_only", None},
}
for name, members in repair_groups.items():
    write_jsonl(
        OUT / "repairs" / f"{name}.jsonl",
        [r for r in repairs if evidence_to_retailer.get(r.get("evidence_id")) in members],
    )

# Corpus shards by source family.
def domain(row: dict) -> str:
    value = (row.get("url") or "").lower()
    if "retail.ru" in value:
        return "retail_ru"
    if "tadviser" in value:
        return "tadviser"
    if "youtube" in value or "youtu.be" in value:
        return "youtube"
    return "other"

for family in ("retail_ru", "tadviser", "youtube", "other"):
    write_jsonl(OUT / "corpus" / f"{family}.jsonl", [r for r in corpus if domain(r) == family])

# Narrative resources are lower-trust comparison inputs.
narratives = {
    "solution_pattern_atlas.md": "16_v2_solution_pattern_atlas.md.docx",
    "corpus_index.md": "17_v2_corpus_index.md.docx",
    "adversarial_review.md": "18_v2_adversarial_review.md.docx",
    "adjudication.md": "19_v2_adjudication_rulings.md.docx",
    "final_report.md": "20_v2_final_report.md.docx",
    "research_gaps.md": "21_v2_research_gaps.md.docx",
    "bibliography.md": "22_v2_bibliography.md.docx",
}
for target, source in narratives.items():
    write_text(OUT / "narratives" / target, extract(V2 / source))

# Deterministic resource index.
resources = []
for path in sorted(OUT.rglob("*")):
    if not path.is_file():
        continue
    payload = path.read_bytes()
    record_count = None
    if path.suffix == ".jsonl":
        record_count = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    resources.append(
        {
            "resource_id": "RES-" + hashlib.sha1(str(path.relative_to(OUT)).encode()).hexdigest()[:10].upper(),
            "repo_path": str(path.relative_to(ROOT)),
            "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "record_count": record_count,
            "trust": "structured_prior_input" if "narratives" not in path.parts else "narrative_untrusted",
            "load_policy": "assigned_subagent_only",
        }
    )
index = {
    "index_version": "1.0",
    "repository": "VS-212/Catm",
    "branch": "arena/01a0008b-catm",
    "rule": "Do not preload all resources. Each worker fetches only repo_paths assigned by the task prompt.",
    "resources": resources,
}
write_json(Path(__file__).resolve().parent / "V2_RESOURCE_INDEX.json", index)

print(f"Wrote {len(resources)} resource files under {OUT}")
print(f"Index: {Path(__file__).resolve().parent / 'V2_RESOURCE_INDEX.json'}")
