"""No assertion of cloud delivery from local Normalize status alone."""
from leadtime_guardian.qa.input_delivery import audit_normalize_qa_input


def test_completed_normalize_does_not_imply_qa_input_delivery():
    result = audit_normalize_qa_input(
        {"status": "COMPLETED", "output": {"documents": [{"document_id": "A"}]}}
    )
    assert result["input_delivery_status"] == "UNKNOWN"
    assert result["qa_status"] == "BLOCKED"


def test_explicit_qa_input_payload_match_is_only_local_evidence():
    value = [{"document_id": "A"}, {"document_id": "B"}]
    result = audit_normalize_qa_input(
        {"status": "COMPLETED", "output": {"documents": value}},
        {"normalized_documents": value},
    )
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MATCH"
    assert result["qa_status"] == "BLOCKED"
    assert result["actual_cloud_input_authenticated"] is False


def test_qa_input_payload_mismatch_is_error():
    result = audit_normalize_qa_input(
        {"status": "COMPLETED", "output": {"documents": [1, 2, 3]}},
        {"normalized_documents": [1, 2, 4]},
    )
    assert result["qa_status"] == "FAIL"
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MISMATCH"


def test_qa_missing_report_is_not_evidence_of_missing_transmission():
    result = audit_normalize_qa_input(
        {"status": "COMPLETED", "output": {"documents": [1]}},
        qa_report={
            "issues": [{"issue_code": "NORMALIZED_OUTPUT_NOT_PROVIDED"}],
            "execution_provenance": None,
        },
    )
    assert result["input_delivery_status"] == "UNKNOWN"
    assert "QA_REPORTS_NORMALIZED_OUTPUT_MISSING" in {
        i["issue_code"] for i in result["issues"]
    }


def test_incomplete_normalize_not_falsely_mapped_to_qa_input_failure():
    result = audit_normalize_qa_input({"status": "queued"})
    assert result["input_delivery_status"] == "NORMALIZE_NOT_COMPLETED"
    assert result["qa_status"] == "BLOCKED"
