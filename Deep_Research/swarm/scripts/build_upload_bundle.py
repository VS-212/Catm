#!/usr/bin/env python3
"""Build compact upload files for web orchestrators with attachment limits."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "upload_bundle"
OUT.mkdir(parents=True, exist_ok=True)

prompt_parts = ["<role_prompt_bundle version=\"1.0\">"]
for path in sorted((ROOT / "prompts").glob("*.xml")):
    prompt_parts.append(f"  <file name=\"{path.name}\">")
    prompt_parts.append(path.read_text(encoding="utf-8"))
    prompt_parts.append("  </file>")
prompt_parts.append("</role_prompt_bundle>\n")
(OUT / "ALL_ROLE_PROMPTS.xml").write_text("\n".join(prompt_parts), encoding="utf-8")

tasks = []
for path in sorted((ROOT / "tasks").glob("*.json")):
    tasks.append(json.loads(path.read_text(encoding="utf-8")))
(OUT / "ALL_TASKS.json").write_text(
    json.dumps({"bundle_version": "1.0", "tasks": tasks}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

schemas = {}
for path in sorted((ROOT / "schemas").glob("*.schema.json")):
    schemas[path.name] = json.loads(path.read_text(encoding="utf-8"))
(OUT / "ALL_SCHEMAS.json").write_text(
    json.dumps({"bundle_version": "1.0", "schemas": schemas}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)

upload_manifest = {
    "bundle_version": "1.0",
    "project_id": "CATMAN-RU-DR-2024-2026",
    "required_external_files": [
        "../../MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md",
        "../ORCHESTRATOR_BOOTSTRAP_PROMPT.xml",
        "../swarm_manifest.yaml",
        "ALL_ROLE_PROMPTS.xml",
        "ALL_TASKS.json",
        "ALL_SCHEMAS.json",
    ],
    "optional_external_files": ["../SKILL.md", "../ORCHESTRATOR_INSTRUCTIONS_GEMINI_SPARK.md"],
    "note": "Paths are repository-relative hints. Upload the six required file contents from their actual locations.",
}
(OUT / "UPLOAD_MANIFEST.json").write_text(
    json.dumps(upload_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(f"Built compact upload bundle in {OUT}")
