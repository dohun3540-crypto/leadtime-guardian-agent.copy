"""Offline combined Team2 V6 / QA E2E ingestion without Studio or release claims.

Read exact source bytes. Never infer that two Studio jobs used identical PDFs
from their file names, case IDs, or unrelated provider file IDs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from leadtime_guardian.qa.audit import load_json_strict
from leadtime_guardian.qa.cross_agent import (
    APPROVED_SANDBOX_AGENTS,
    audit_cross_agent_handoff,
)
from leadtime_guardian.qa.handoff_builder import build_studio_raw_handoff
from leadtime_guardian.qa.portfolio import audit_portfolio
from leadtime_guardian.qa.studio_contract import audit_native_envelope
from leadtime_guardian.studio_adapter import apply_studio_extractions
from leadtime_guardian.studio_integration import (
    analyze_studio_documents,
    documents_from_export,
    validate_documents,
)


def audit_combined_bytes(
    operational_native_bytes: bytes, base_case_bytes: bytes, schema_bytes: bytes,
    *, operational_job_id: str, case_id: str, github_sha: str,
    qa_native_bytes: bytes | None = None, qa_report_bytes: bytes | None = None,
    qa_agent_id: str | None = None, qa_config_id: str | None = None,
    qa_config_version: int | None = None,
    execution_kind: str = "ARCHIVED_STUDIO",
) -> dict:
    """Independently check the joined code path; no authentication of cloud runs."""
    result = {
        "status": "BLOCKED",
        "python_business_status": "NOT_VERIFIED",
        "python_safety_status": "NOT_VERIFIED",
        "studio_document_status": "NOT_VERIFIED",
        "cross_agent_status": "BLOCKED",
        "same_original_pdf_bytes_verified": False,
        "actual_studio_e2e_status": "NOT_VERIFIED",
        "release_or_merge_authorized": False,
        "external_action_taken": False,
        "issues": [],
        "sha256": {},
    }

    def record(code: str, stage: str) -> None:
        result["issues"].append({"issue_code": code, "stage": stage})

    try:
        if type(operational_native_bytes) is not bytes:
            raise TypeError("operational Native must be bytes")
        if type(base_case_bytes) is not bytes or type(schema_bytes) is not bytes:
            raise TypeError("trusted case and schema must be original bytes")
        result["sha256"]["operational_native"] = hashlib.sha256(
            operational_native_bytes
        ).hexdigest()
        operational = load_json_strict(operational_native_bytes)
        base = load_json_strict(base_case_bytes)
        schema = load_json_strict(schema_bytes)
        if not isinstance(operational, dict) or not isinstance(base, dict):
            raise TypeError("Native and base must be JSON objects")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError("explicit nonempty case ID required")
        if base.get("case_id") not in (case_id, "SYN-" + case_id):
            raise ValueError("operational trusted base case ID differs from expected case")
        if not isinstance(operational.get("metadata"), dict):
            raise TypeError("operational Native metadata not observed")
        metadata = operational["metadata"]
        if metadata.get("job_execution_id") != operational_job_id:
            raise ValueError("operational job ID does not match expected")
        native = audit_native_envelope(
            operational, expected_job_id=operational_job_id,
            expected_step_run_id=metadata.get("step_run_id"),
        )
        if native["qa_status"] != "PASS":
            raise ValueError("operational Native contract did not pass")
        docs = documents_from_export(
            operational, expected_job_id=operational_job_id
        )
        python_result = analyze_studio_documents(base, docs, schema)
        result["python_business_status"] = python_result["execution_status"]
        result["python_summary"] = {
            "case_id": python_result.get("case_id"),
            "execution_status": python_result.get("execution_status"),
            "review_flags": python_result.get("review_flags"),
            "baseline_shortage_quantity": python_result.get("baseline_shortage_quantity"),
            "changed_shortage_quantity": python_result.get("changed_shortage_quantity"),
            "estimated_quote_cost_krw": python_result.get("estimated_quote_cost_krw"),
            "evidence_verified_against_pdf": False,
        }
        if python_result["execution_status"] == "COMPLETED":
            from_case = apply_studio_extractions(base, docs)
            from_case["quotes"] = validate_documents(base, docs, schema)
            safety = audit_portfolio(from_case, python_result)
        else:
            safety = audit_portfolio(base, python_result)
        if safety["qa_status"] != "PASS":
            result["python_safety_status"] = "FAIL"
            record("INDEPENDENT_PYTHON_QA_FAILED", "python_safety")
        else:
            result["python_safety_status"] = (
                "PASS_LOCAL" if python_result["execution_status"] == "COMPLETED"
                else "SAFELY_BLOCKED_LOCAL"
            )
        if qa_native_bytes is None and qa_report_bytes is None:
            record("QA_STUDIO_RAW_ARTIFACTS_NOT_PROVIDED", "studio_qa")
        elif qa_native_bytes is None or qa_report_bytes is None:
            record("QA_STUDIO_RAW_ARTIFACT_PAIR_INCOMPLETE", "studio_qa")
        else:
            if (qa_agent_id is None or qa_config_id is None
                    or qa_config_version is None):
                raise ValueError("explicit QA agent/config/version required")
            if qa_agent_id not in APPROVED_SANDBOX_AGENTS:
                raise ValueError("QA agent not in frozen allow-list")
            result["sha256"]["qa_native"] = hashlib.sha256(
                qa_native_bytes
            ).hexdigest()
            result["sha256"]["qa_report"] = hashlib.sha256(
                qa_report_bytes
            ).hexdigest()
            manifest = build_studio_raw_handoff(
                qa_native_bytes, qa_report_bytes, case_id=case_id,
                agent_id=qa_agent_id, config_id=qa_config_id,
                config_version=qa_config_version,
                github_sha=github_sha, execution_kind=execution_kind,
            )
            verdict = audit_cross_agent_handoff(
                manifest, native_bytes=qa_native_bytes,
                report_bytes=qa_report_bytes,
                expected_agent_id=qa_agent_id,
                expected_config_id=qa_config_id,
                expected_github_sha=github_sha,
            )
            result["studio_document_status"] = verdict["document_qa_status"]
            result["cross_agent_status"] = verdict["qa_status"]
            result["requires_human_review"] = verdict["requires_human_review"]
            result["cross_agent_issues"] = verdict["issues"]
            if verdict["qa_status"] == "FAIL":
                record("CROSS_AGENT_CONTRACT_FAILED", "cross_agent")
        if result["python_safety_status"] == "FAIL" or result["cross_agent_status"] == "FAIL":
            result["status"] = "FAIL"
    except (ValueError, TypeError, KeyError, IndexError, UnicodeDecodeError) as exc:
        result["status"] = "FAIL"
        record("COMBINED_E2E_INPUT_OR_BOUNDARY_FAILED", type(exc).__name__)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--operational-native", required=True, type=Path)
    parser.add_argument("--trusted-base", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=ROOT /
                        "configs/schemas/document_extraction.schema.json")
    parser.add_argument("--operational-job-id", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--qa-native", type=Path)
    parser.add_argument("--qa-report", type=Path)
    parser.add_argument("--qa-agent-id", choices=sorted(APPROVED_SANDBOX_AGENTS))
    parser.add_argument("--qa-config-id")
    parser.add_argument("--qa-config-version", type=int)
    parser.add_argument("--github-sha", required=True)
    parser.add_argument("--execution-kind", choices=(
        "ARCHIVED_STUDIO", "ARCHIVED_REPLAY", "NEW_LIVE_STUDIO",
    ), default="ARCHIVED_STUDIO")
    args = parser.parse_args()
    try:
        result = audit_combined_bytes(
            args.operational_native.read_bytes(), args.trusted_base.read_bytes(),
            args.schema.read_bytes(),
            operational_job_id=args.operational_job_id,
            case_id=args.case_id, github_sha=args.github_sha,
            qa_native_bytes=args.qa_native.read_bytes() if args.qa_native else None,
            qa_report_bytes=args.qa_report.read_bytes() if args.qa_report else None,
            qa_agent_id=args.qa_agent_id, qa_config_id=args.qa_config_id,
            qa_config_version=args.qa_config_version,
            execution_kind=args.execution_kind,
        )
    except OSError:
        result = {
            "status": "FAIL", "release_or_merge_authorized": False,
            "issues": [{"issue_code": "INPUT_FILE_NOT_READABLE", "stage": "cli"}],
        }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 1 if result["status"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
