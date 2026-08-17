#!/usr/bin/env python3
"""Validate static swarm package integrity without running any agents."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AGENTS = {
    "U01", "O01", *{f"R{i:02d}" for i in range(1, 11)},
    "X01", "X02", "X03", "X04", "F01", "F02", "F03",
    "N01", "N02", "N03", "P01", "Z01", "J01",
}

errors: list[str] = []


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Invalid JSON {path.relative_to(ROOT)}: {exc}")
        return None


schemas = {}
for path in sorted((ROOT / "schemas").glob("*.schema.json")):
    data = load_json(path)
    if data is not None:
        schemas[path.name] = data

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None
else:
    for name, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"Invalid JSON Schema {name}: {exc}")

task_ids = set()
for path in sorted((ROOT / "tasks").glob("*.json")):
    data = load_json(path)
    if not data:
        continue
    task_ids.add(data.get("agent_id"))
    if data.get("agent_id") != path.stem:
        errors.append(f"Task filename/id mismatch: {path.name} -> {data.get('agent_id')}")
    if not data.get("require_real_independent_context"):
        errors.append(f"Task does not require real context isolation: {path.name}")

if task_ids != EXPECTED_AGENTS:
    errors.append(f"Task set mismatch. Missing={sorted(EXPECTED_AGENTS-task_ids)} Extra={sorted(task_ids-EXPECTED_AGENTS)}")

required_files = [
    ROOT.parent / "MASTER_BRIEF_RU_CATMAN_DEMAND_2024_2026.md",
    ROOT / "ORCHESTRATOR_BOOTSTRAP_PROMPT.xml",
    ROOT / "ORCHESTRATOR_INSTRUCTIONS_GEMINI_SPARK.md",
    ROOT / "SKILL.md",
    ROOT / "swarm_manifest.yaml",
    ROOT / "prompts" / "COMMON_POLICY.xml",
    ROOT / "upload_bundle" / "ALL_ROLE_PROMPTS.xml",
    ROOT / "upload_bundle" / "ALL_TASKS.json",
    ROOT / "upload_bundle" / "ALL_SCHEMAS.json",
]
for path in required_files:
    if not path.exists() or path.stat().st_size == 0:
        errors.append(f"Missing/empty required file: {path}")

bundle_tasks = load_json(ROOT / "upload_bundle" / "ALL_TASKS.json")
if bundle_tasks and len(bundle_tasks.get("tasks", [])) != 25:
    errors.append("ALL_TASKS.json must contain 25 task packets")

bundle_schemas = load_json(ROOT / "upload_bundle" / "ALL_SCHEMAS.json")
if bundle_schemas and set(bundle_schemas.get("schemas", {})) != set(schemas):
    errors.append("ALL_SCHEMAS.json is stale; rebuild upload bundle")

try:
    import yaml
except ImportError:
    yaml = None
if yaml:
    try:
        manifest = yaml.safe_load((ROOT / "swarm_manifest.yaml").read_text(encoding="utf-8"))
        manifest_agents = set(manifest.get("agents", {}))
        if manifest_agents != EXPECTED_AGENTS:
            errors.append(f"Manifest agent set mismatch: {sorted(manifest_agents ^ EXPECTED_AGENTS)}")
        if not manifest.get("execution_policy", {}).get("require_real_subagents"):
            errors.append("Manifest does not require real subagents")
    except Exception as exc:
        errors.append(f"Invalid YAML manifest: {exc}")

if errors:
    print("PACKAGE VALIDATION FAILED", file=sys.stderr)
    for item in errors:
        print(f"- {item}", file=sys.stderr)
    raise SystemExit(1)

print(f"PACKAGE VALID: {len(task_ids)} agents, {len(schemas)} schemas")
if Draft202012Validator is None:
    print("NOTE: jsonschema not installed; schemas were parsed but not meta-validated")
if yaml is None:
    print("NOTE: PyYAML not installed; manifest was not parsed")
