"""Evidence-bounded NormalizeDocuments → IndependentQA input consistency check.

Completed upstream nodes and downstream model claims are insufficient to prove
that the exact documents were transmitted. This is a read-only local checker.
"""
from __future__ import annotations

import math
from typing import Any


def _same_json_value(left: Any, right: Any) -> bool:
    """값을 변환하지 않고 JSON 값과 타입을 재귀 비교한다. 클라우드 출처 증명은 아니다."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        if not all(type(key) is str for key in left):
            return False
        if not all(type(key) is str for key in right):
            return False
        return left.keys() == right.keys() and all(
            _same_json_value(value, right[key]) for key, value in left.items()
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            _same_json_value(a, b) for a, b in zip(left, right, strict=True)
        )
    if type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and left == right
    if left is None or type(left) in (str, int, bool):
        return left == right
    return False


def audit_normalize_qa_input(
    normalize_step: Any, qa_step_input: Any = None, qa_report: Any = None,
) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    status = "UNKNOWN"

    def note(code: str, severity: str = "WARNING") -> None:
        issues.append({"issue_code": code, "severity": severity})

    if not isinstance(normalize_step, dict):
        note("NORMALIZE_STEP_NOT_PROVIDED")
    else:
        completed = normalize_step.get("status") in ("completed", "COMPLETED")
        if not completed:
            status = "NORMALIZE_NOT_COMPLETED"
            note("NORMALIZE_EXECUTION_NOT_COMPLETED")
        else:
            payload = normalize_step.get("output")
            if not isinstance(payload, dict) or not isinstance(payload.get("documents"), list):
                note("NORMALIZE_OUTPUT_NOT_OBSERVED")
            elif not isinstance(qa_step_input, dict):
                note("QA_INPUT_NOT_OBSERVED")
            else:
                # The exact documented key must be observed, not inferred from
                # the mere presence of a completed preceding node.
                delivered = qa_step_input.get("normalized_documents")
                if not isinstance(delivered, list):
                    note("QA_NORMALIZED_DOCUMENTS_FIELD_NOT_OBSERVED")
                elif _same_json_value(delivered, payload["documents"]):
                    status = "LOCAL_CONTENT_MATCH"
                else:
                    status = "LOCAL_CONTENT_MISMATCH"
                    note("QA_NORMALIZED_DOCUMENTS_MISMATCH", "ERROR")

    if isinstance(qa_report, dict):
        feedback = qa_report.get("issues")
        if isinstance(feedback, list):
            for item in feedback:
                if (isinstance(item, dict)
                        and item.get("issue_code", item.get("code"))
                        == "NORMALIZED_OUTPUT_NOT_PROVIDED"):
                    note("QA_REPORTS_NORMALIZED_OUTPUT_MISSING")
                    # Report allegation is not independently confirmed.
                    break
        provenance = qa_report.get("execution_provenance")
        if not isinstance(provenance, dict) or any(
            provenance.get(k) is None
            for k in ("workflow_id", "config_id", "job_id", "source_files")
        ):
            note("QA_EXECUTION_PROVENANCE_INCOMPLETE")

    return {
        "qa_status": "FAIL" if status == "LOCAL_CONTENT_MISMATCH" else "BLOCKED",
        "input_delivery_status": status,
        "requires_human_review": bool(issues),
        "actual_cloud_input_authenticated": False,
        "release_or_merge_authorized": False,
        "issues": issues,
    }
