#!/usr/bin/env python3
"""Validate a JSONL file against one record JSON Schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("schema", type=Path)
    args = parser.parse_args()

    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    failures = 0
    records = 0

    for lineno, raw in enumerate(args.jsonl.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        records += 1
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"line {lineno}: invalid JSON: {exc}")
            failures += 1
            continue
        errors = sorted(validator.iter_errors(obj), key=lambda e: list(e.path))
        for error in errors:
            path = ".".join(map(str, error.path)) or "$"
            print(f"line {lineno} {path}: {error.message}")
            failures += 1

    print(f"records={records} validation_errors={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
