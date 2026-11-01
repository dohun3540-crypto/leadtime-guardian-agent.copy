"""Combined same-tree CLI tests. QA report is synthetic, no new Studio run."""
import hashlib
import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

from leadtime_guardian.qa.audit import load_json_strict

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/qa_combined_e2e_check.py"
OPERATING = ROOT / "data/results/studio_runs/C001_20261030_v4/instruct_original.json"
BASE = ROOT / "data/cases/SYN-C001/trusted_base_case.json"
SCHEMA = ROOT / "configs/schemas/document_extraction.schema.json"
AGENT = "agt_HdtUJPQPXir9rGKgPWSyZG"
CONFIG = "cfg_X2xXakDtmDTHh2RoqVysvL"


def invoke(*extra):
    raw = load_json_strict(OPERATING.read_bytes())
    expected_job = raw["metadata"]["job_execution_id"]
    proc = subprocess.run([
        sys.executable, str(CLI), "--operational-native", str(OPERATING),
        "--trusted-base", str(BASE), "--schema", str(SCHEMA),
        "--operational-job-id", expected_job, "--case-id", "C001",
        "--github-sha", "a" * 40, *extra,
    ], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    return proc, json.loads(proc.stdout)


def test_verified_archive_to_team2_python_qa_without_live_pair():
    proc, output = invoke()
    assert proc.returncode == 2, proc.stderr
    assert output["python_business_status"] == "COMPLETED"
    assert output["python_safety_status"] == "PASS_LOCAL"
    assert output["python_summary"]["changed_shortage_quantity"] == 60
    assert Decimal(output["python_summary"]["estimated_quote_cost_krw"]) == Decimal(60500)
    assert output["sha256"]["operational_native"] == hashlib.sha256(
        OPERATING.read_bytes()
    ).hexdigest()
    assert output["studio_document_status"] == "NOT_VERIFIED"
    assert output["cross_agent_status"] == "BLOCKED"
    assert output["status"] == "BLOCKED"
    assert output["release_or_merge_authorized"] is False


def test_missing_or_mismatched_operational_job_fails_closed():
    proc, output = invoke("--operational-job-id", "job_WRONG")
    assert proc.returncode == 1
    assert output["status"] == "FAIL"
    assert output["release_or_merge_authorized"] is False


def test_wrong_case_id_cannot_bind_current_operational_native():
    proc, output = invoke("--case-id", "C013")
    assert proc.returncode == 1
    assert output["status"] == "FAIL"


def test_qa_native_without_qa_report_keeps_cross_agent_blocked():
    proc, output = invoke("--qa-native", str(OPERATING))
    assert proc.returncode == 2
    assert output["cross_agent_status"] == "BLOCKED"
    assert "QA_STUDIO_RAW_ARTIFACT_PAIR_INCOMPLETE" in {
        x["issue_code"] for x in output["issues"]
    }


def test_archived_operational_bytes_plus_synthetic_raw_qa_never_release(tmp_path):
    source = load_json_strict(OPERATING.read_bytes())
    document_ids = [
        x["document_id"] for x in load_json_strict(source["content"])["documents"]
    ]
    synthetic_report = {
        "case_id": "C001", "qa_status": "NOT_VERIFIED",
        "checked_document_ids": document_ids, "issues": [],
        "evidence_status": "PARTIAL", "recommended_action": "human review required",
        "workflow_version": "v1", "execution_provenance": None,
        "field_checks": [
            {"field": key, "status": "SOURCE_NOT_VERIFIED"} for key in document_ids
        ],
    }
    qa_file = tmp_path / "synthetic_qa_report.json"
    qa_file.write_bytes(json.dumps(synthetic_report).encode())
    proc, output = invoke(
        "--qa-native", str(OPERATING), "--qa-report", str(qa_file),
        "--qa-agent-id", AGENT, "--qa-config-id", CONFIG,
        "--qa-config-version", "1", "--execution-kind", "ARCHIVED_REPLAY",
    )
    assert proc.returncode == 2, proc.stderr
    assert output["python_safety_status"] == "PASS_LOCAL"
    assert output["studio_document_status"] == "NOT_VERIFIED"
    assert output["cross_agent_status"] == "BLOCKED"
    assert output["actual_studio_e2e_status"] == "NOT_VERIFIED"
    assert output["same_original_pdf_bytes_verified"] is False
    assert output["release_or_merge_authorized"] is False
    assert output["sha256"]["qa_report"] == hashlib.sha256(
        qa_file.read_bytes()
    ).hexdigest()


def test_malformed_trusted_case_json_is_error(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_bytes(b'{"case_id":"SYN-C001","case_id":"SYN-C013"}')
    proc, output = invoke("--trusted-base", str(bad))
    assert proc.returncode == 1
    assert output["status"] == "FAIL"
