"""Finish the recursive static null review without asserting provider runtime behavior.

Extract ZIPs are observations, even when Studio names their directory 'gold'.
This command never edits a config, imports a workflow, or approves Gold.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from jsonschema import Draft202012Validator

from leadtime_guardian.qa.audit import load_json_strict


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def review_config(config: dict, observations: list[dict]) -> dict:
    """Classify explicit Null-if/when candidates at their real container depth."""
    rows = []
    schemas = config["workflowConfig"]["informationExtractConfiguration"]["schemas"]

    def visit(field, pointer, human, required, branch, entry, parts):
        typ = field.get("type")
        description = field.get("description", "")
        nullable = typ == "null" or isinstance(typ, list) and "null" in typ
        explicit = any(x in description.lower() for x in ("null if", "null when"))
        if explicit and not nullable:
            numeric_flag = entry.get("addNullTypeToNumericTypes")
            affected_by_flag = typ in ("integer", "number") and numeric_flag is True
            observed = []
            for item in observations:
                doc = item["document"]
                if doc.get("document_type") != branch.removeprefix("Extract_"):
                    continue
                values = [doc]
                for part in parts:
                    values = [v[part] for v in values if isinstance(v, dict) and part in v]
                    if part == "quote":
                        values = [v for vs in values if isinstance(vs, list) for v in vs]
                observed.append({
                    "source": item["source"], "sha256": item["sha256"],
                    "document_id": doc.get("document_id"), "values": values,
                    "branch_exercised": bool(values),
                    "declared_leaf_validation": [
                        not list(Draft202012Validator(field).iter_errors(v)) for v in values
                    ],
                    "source_scope": "PROVIDER_EXTRACT_EXPORT_UNAPPROVED_NOT_GOLD",
                })
            rows.append({
                "field_path": human, "node": branch, "json_pointer": pointer,
                "declared_type": typ, "required_in_immediate_container": required,
                "required_if_parent_absent": False if "quote[]" in human else required,
                "declared_nullable": nullable, "null_instruction": description,
                "addNullTypeToNumericTypes": numeric_flag,
                "effective_provider_nullability": "NOT_VERIFIED",
                "numeric_flag_may_cover_field": affected_by_flag,
                "observed_extract": observed,
                "null_observed": any(v is None for o in observed for v in o["values"]),
                "classification": "NOT_VERIFIED" if affected_by_flag else "POTENTIAL_CONFLICT",
                "reproduction": {
                    "scope": "LOCAL_DECLARED_LEAF_SCHEMA_ONLY",
                    "json_null_rejected_by_declared_leaf": bool(list(
                        Draft202012Validator(field).iter_errors(None)
                    )),
                    "live_null_type_failure_confirmed": False,
                },
                "minimal_action": (
                    "VERIFY_NUMERIC_NULL_FLAG_ON_DISPOSABLE_CONFIG_WITH_AUTHORIZED_RUN"
                    if affected_by_flag else
                    "VERIFY_ABSENT_FIELD_RUNTIME_BEFORE_ANY_NULLABLE_SCHEMA_CHANGE"
                ),
                "side_effect_risk": (
                    "Provider support for union types unknown; allowing null must not bypass "
                    "required PO/quote business validation. Empty quote table is not a null row."
                ),
                "qa_block_condition": (
                    "Missing business identifiers, quantity, date, currency or quote facts "
                    "must remain blocked by the existing document validator; optional "
                    "supplier/irrelevant quote absence alone is not an error."
                ),
                "owner": "구도훈; Adapter interface review 윤현준",
                "config_modified": False,
            })
        for key, value in field.get("properties", {}).items():
            visit(value, pointer + "/properties/" + key, human + "." + key,
                  key in field.get("required", []), branch, entry, parts + [key])
        if isinstance(field.get("items"), dict):
            visit(field["items"], pointer + "/items", human + "[]", False,
                  branch, entry, parts)

    for index, entry in enumerate(schemas):
        spec = entry["json_schema"]
        visit(spec["schema"],
              f"/workflowConfig/informationExtractConfiguration/schemas/{index}/json_schema/schema",
              spec["name"], False, spec["name"], entry, [])
    return {
        "schema_version": "team1-schema-review/v1", "status": "PASS_LOCAL",
        "candidate_count": len(rows),
        "classification_counts": dict(Counter(r["classification"] for r in rows)),
        "confirmed_live_defects": 0, "runtime_gate": "BLOCKED",
        "config_identity": config.get("exportedFrom"), "rows": rows,
        "intended_transformations": [
            "Extract quote[] single row -> Normalize quote object; empty table -> null",
            "Absent optional scalar empty string -> Normalize null; preserve zero and false",
        ],
        "config_modified": False, "gold_approved": False,
        "official_extraction_accuracy": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--extract-zip", type=Path, action="append", default=[])
    parser.add_argument("--expected-candidates", type=int, default=40)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    observations = []
    inputs = [{"name": args.config.name, "sha256": digest(args.config.read_bytes())}]
    for path in args.extract_zip:
        inputs.append({"name": path.name, "sha256": digest(path.read_bytes())})
        with zipfile.ZipFile(path) as archive:
            for member in archive.namelist():
                if member.endswith(".json"):
                    data = archive.read(member)
                    observations.append({"source": path.name + "::" + member,
                                         "sha256": digest(data),
                                         "document": load_json_strict(data)})
    report = review_config(load_json_strict(args.config.read_bytes()), observations)
    report["inputs"] = inputs
    if report["candidate_count"] != args.expected_candidates:
        report["status"] = "FAIL"
        report["error"] = "CANDIDATE_INVENTORY_CHANGED_REVIEW_REQUIRED"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "status", "candidate_count", "classification_counts", "confirmed_live_defects"
    )}))
    return 0 if report["status"] == "PASS_LOCAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
