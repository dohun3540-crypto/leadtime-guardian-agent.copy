"""Cross-review reproductions: Studio report schema and in-memory JSON type safety.

All observations are synthetic regression contracts, NOT authenticated E1 raw.
"""
from __future__ import annotations

from copy import deepcopy

import pytest

from leadtime_guardian.qa.input_delivery import audit_normalize_qa_input
from leadtime_guardian.qa.studio_qa_adapter import normalize_studio_qa_report


DOCS = [{"document_id": "PO-DOC", "document_type": "purchase_order"}]


def studio_report():
    return {
        "case_id": "C001",
        "qa_status": "NOT_VERIFIED",
        "checked_document_ids": ["PO-DOC"],
        "issues": [{"issue_code": "NO_NATIVE", "scope": "integration", "severity": "info"}],
        "evidence_status": "PARTIAL",
        "recommended_action": "Obtain raw evidence",
        "workflow_version": None,
        "execution_provenance": {
            "workflow_id": None, "config_id": None, "job_id": None,
            "source_files": None,
        },
        "field_checks": [{"field": "po_id", "status": "NOT_VERIFIED"}],
    }


def adapt(report):
    return normalize_studio_qa_report(
        report, expected_case_id="C001", expected_document_ids=["PO-DOC"],
    )


def delivery(left, right):
    return audit_normalize_qa_input(
        {"status": "COMPLETED", "case_id": "C001",
         "output": {"documents": [{"document_id": "PO-DOC", "value": left}]}},
        {"case_id": "C001",
         "normalized_documents": [{"document_id": "PO-DOC", "value": right}]},
        expected_case_id="C001",
    )


def test_lowercase_info_and_null_workflow_version_are_structurally_adapted():
    source = studio_report()
    original = deepcopy(source)
    got = adapt(source)
    assert got["adapter_status"] == "PASS"
    assert got["document_qa_status"] == "NOT_VERIFIED"
    assert got["python_qa_status"] == "NOT_VERIFIED"
    assert got["workflow_version"] is None
    assert got["execution_provenance"]["job_id"] is None
    assert got["requires_human_review"] is True
    assert got["pdf_grounding_verified"] is False
    assert got["original_report_modified"] is False
    assert got["issues"][0] == {
        "code": "STUDIO_ISSUE_SEVERITY_CASE_NORMALIZED",
        "scope": "integration", "severity": "WARNING",
    }
    assert {"code": "NO_NATIVE", "scope": "integration", "severity": "INFO"} in got["issues"]
    assert {"code": "STUDIO_WORKFLOW_VERSION_NOT_VERIFIED",
            "scope": "integration", "severity": "WARNING"} in got["issues"]
    assert source == original


@pytest.mark.parametrize("raw,expected", [
    ("info", "INFO"), ("warning", "WARNING"), ("error", "ERROR"),
])
def test_lowercase_known_severity_normalized_with_explicit_warning(raw, expected):
    source = studio_report()
    source["issues"][0]["severity"] = raw
    source["workflow_version"] = "v1"
    got = adapt(source)
    assert got["adapter_status"] == "PASS"
    assert {"code": "NO_NATIVE", "scope": "integration",
            "severity": expected} in got["issues"]
    assert got["requires_human_review"] is True
    assert source["issues"][0]["severity"] == raw


def test_missing_version_key_is_still_structurally_invalid():
    source = studio_report()
    del source["workflow_version"]
    assert adapt(source)["adapter_status"] == "FAIL"


@pytest.mark.parametrize("severity", ["verbose", "Info", "", None, ["info"]])
def test_unknown_or_malformed_issue_severity_is_rejected(severity):
    source = studio_report()
    source["issues"][0]["severity"] = severity
    assert adapt(source)["adapter_status"] == "FAIL"


def test_missing_version_cannot_promote_optimistic_pass():
    source = studio_report()
    source["qa_status"] = "PASS"
    source["evidence_status"] = "VERIFIED"
    source["field_checks"] = [{"field": "po_id", "status": "VERIFIED"}]
    source["execution_provenance"] = {
        "workflow_id": "wf1", "config_id": "cfg1",
        "job_id": "job1", "source_files": ["pdf1"],
    }
    got = adapt(source)
    assert got["adapter_status"] == "PASS"
    assert got["document_qa_status"] != "PASS"
    assert got["requires_human_review"] is True
    assert got["python_run_verified"] is False


@pytest.mark.parametrize("left,right", [
    ({"nested": (1, 2)}, {"nested": [1, 2]}),
    ({"nested": [1, 2]}, {"nested": (1, 2)}),
    ({1: "one"}, {"1": "one"}),
    ({"1": "one"}, {1: "one"}),
    ({1: "one"}, {1: "one"}),
    ((1, 2), (1, 2)),
    (0, False),
    (1, True),
    (100, 100.0),
    (None, "null"),
    ([], ()),
    ([1, [2, 3]], [1, [3, 2]]),
    (float("nan"), float("nan")),
    (float("inf"), float("inf")),
])
def test_non_json_or_changed_json_value_cannot_match(left, right):
    result = delivery(left, right)
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MISMATCH"
    assert result["qa_status"] == "FAIL"
    assert result["actual_cloud_input_authenticated"] is False


def test_valid_json_with_reordered_object_keys_still_matches():
    left = {"a": [0, None, {"b": "x"}], "z": 100}
    right = {"z": 100, "a": [0, None, {"b": "x"}]}
    result = delivery(left, right)
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MATCH"
    assert result["qa_status"] == "BLOCKED"
    assert result["actual_cloud_input_authenticated"] is False


def test_comparison_does_not_mutate_source_documents():
    left = {"nested": (1, 2)}
    right = {"nested": [1, 2]}
    a, b = deepcopy(left), deepcopy(right)
    delivery(left, right)
    assert left == a
    assert right == b
