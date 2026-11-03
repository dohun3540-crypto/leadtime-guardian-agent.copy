"""Native closure regressions. Manufactured bundles are local-only fixtures."""
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from test_qa_experiment_identity_hardening import _manifest, _normalized
from test_qa_stage_trace import evidence

from leadtime_guardian.qa.experiment_compare import (
    audit_b0_e1_readiness,
    compare_normalized_field_values,
)
from leadtime_guardian.qa.stage_trace import audit_stage_evidence

ROOT = Path(__file__).resolve().parents[1]
CURRENT_QA_AGENT = "agt_oMuHCjkGkVUkyyxjVDJda4"
CURRENT_QA_CONFIG = "cfg_mokhkXae6d5U7CfgpL7ffw"


def _bound_compare(payload):
    b0, e1 = _manifest("B0"), _manifest("E1")
    digest = hashlib.sha256(json.dumps(payload).encode()).hexdigest()
    b0["step_artifacts"]["NormalizeDocuments"]["original_sha256"] = digest
    ready = audit_b0_e1_readiness(b0, e1)
    return compare_normalized_field_values(
        payload, _normalized("C001", 40), ready,
        original_raw_sha256_by_side={"B0": digest, "E1": "b" * 64},
    )


def test_comparison_cannot_hide_wrong_job_under_matching_root_metadata():
    payload = {"metadata": {"job_execution_id": "job_B0"},
               "output": {"metadata": {"job_execution_id": "job_OTHER"},
                          "content": json.dumps(_normalized("C001", 40))}}
    result = _bound_compare(payload)
    assert result["field_comparison_status"] == "BLOCKED"
    assert any("IDENTITY_MISMATCH" in code for code in result["issues"])
    assert result["fields_compared"] == 0


def test_comparison_checks_root_identity_even_when_metadata_exists():
    payload = _normalized("C001", 40)
    payload.update(job_id="job_E1", metadata={"job_execution_id": "job_B0"})
    assert _bound_compare(payload)["field_comparison_status"] == "BLOCKED"


def test_comparison_does_not_treat_boolean_config_version_as_integer_one():
    payload = _normalized("C001", 40)
    payload["metadata"] = {"config_version": True}
    assert _bound_compare(payload)["field_comparison_status"] == "BLOCKED"


def test_experiment_manifest_rejects_boolean_operational_config_version():
    b0, e1 = _manifest("B0"), _manifest("E1")
    b0["step_artifacts"]["NormalizeDocuments"]["config_version"] = True
    assert audit_b0_e1_readiness(b0, e1)["eligibility"] == "FAIL"


def _c013_stages():
    manifest, raw = evidence()
    manifest["case_id"] = "C013"
    manifest["operational_job_id"] = "job_SYNTHETIC_C013"
    for name, value in list(raw.items()):
        data = json.loads(value)
        data["case_id"] = "C013"
        entry = manifest["stages"][name]
        entry["case_id"] = "C013"
        if name in ("Extract", "MergeDocuments", "NormalizeDocuments"):
            data["job_id"] = entry["job_id"] = "job_SYNTHETIC_C013"
        raw[name] = json.dumps(data).encode()
        entry["sha256"] = hashlib.sha256(raw[name]).hexdigest()
    return manifest, raw


def test_c013_stage_contract_accepts_complete_local_chain_without_c001_xlsx_claims():
    manifest, raw = _c013_stages()
    before = deepcopy((manifest, raw))
    result = audit_stage_evidence(manifest, raw)
    assert result["status"] == "BLOCKED"
    assert result["case_id"] == "C013"
    assert result["all_expected_raw_stages_present"] is True
    assert result["normalize_qa_input_status"] == "LOCAL_CONTENT_MATCH"
    assert result["field_trace"] == []
    assert result["xlsx_reference_sha256"] is None
    assert result["xlsx_shared_index_49_empty_reference_count"] is None
    assert result["studio_live_execution_authenticated"] is False
    assert (manifest, raw) == before


def test_c013_stage_contract_still_rejects_embedded_other_case():
    manifest, raw = _c013_stages()
    data = json.loads(raw["NormalizeDocuments"])
    data["metadata"] = {"case_id": "C001"}
    raw["NormalizeDocuments"] = json.dumps(data).encode()
    manifest["stages"]["NormalizeDocuments"]["sha256"] = hashlib.sha256(
        raw["NormalizeDocuments"]).hexdigest()
    result = audit_stage_evidence(manifest, raw)
    assert result["status"] == "FAIL"
    assert any("RAW_STAGE_IDENTITY_CONFLICT" in x["issue_code"] for x in result["issues"])


@pytest.mark.parametrize("location", ["metadata", "additional_values"])
def test_matching_nested_identity_and_document_order_remain_comparable(location):
    inner = _normalized("C001", 40)
    inner["documents"].reverse()
    payload = {location: {"job_execution_id": "job_B0", "config_version": 1},
               "content": json.dumps(inner)}
    result = _bound_compare(payload)
    assert result["field_comparison_status"] == "UNCHANGED"
    assert result["studio_comparison_authenticated"] is False
    assert result["release_or_merge_authorized"] is False


def test_c013_single_document_native_stops_before_python(monkeypatch):
    sys.path.insert(0, str(ROOT / "scripts"))
    import qa_combined_e2e_check as combined

    def forbidden(*args, **kwargs):
        raise AssertionError("Incomplete C013 reached Python")

    monkeypatch.setattr(combined, "analyze_studio_documents", forbidden)
    source = json.loads((ROOT / "data/results/studio_runs/C001_20261030_v4/"
                         "instruct_original.json").read_bytes())
    docs = json.loads(source["content"])["documents"]
    source["content"] = json.dumps({"documents": docs[:1]})
    source["metadata"]["merge"]["items"] = source["metadata"]["merge"]["items"][:1]
    source["metadata"]["source_files"] = source["metadata"]["source_files"][:1]
    result = combined.audit_combined_bytes(
        json.dumps(source).encode(),
        (ROOT / "data/cases/SYN-C013/trusted_base_case.json").read_bytes(),
        (ROOT / "configs/schemas/document_extraction.schema.json").read_bytes(),
        case_id="C013", operational_job_id=source["metadata"]["job_execution_id"],
        github_sha="a" * 40,
    )
    assert result["status"] == "BLOCKED"
    assert result["python_business_status"] == "NOT_VERIFIED"
    assert "python_summary" not in result
    assert "C013_NOT_SINGLE_THREE_DOCUMENT_JOB" in {
        x["issue_code"] for x in result["issues"]}


def test_c013_release_intake_lists_missing_evidence_instead_of_rejecting_case(tmp_path):
    from leadtime_guardian.qa.e2e_bundle_preflight import audit_parallel_e2e_bundle

    path = tmp_path / "release.json"
    path.write_text(json.dumps({
        "schema_version": "leadtime-release-evidence/v1",
        "case_id": "C013", "operational_job_id": "job_C013",
        "config_id": "cfg_C013", "config_version": 1, "sources": {},
    }))
    result = audit_parallel_e2e_bundle(path)
    assert result["status"] == "BLOCKED"
    assert result["invalid_inputs"] == []
    assert "human_gold" in result["missing_inputs"]
    assert "stage.NormalizeDocuments" in result["missing_inputs"]
    assert result["release_authorized"] is False


def _synthetic_current_handoff(tmp_path, *, report_case="SYN-C001"):
    from test_qa_combined_e2e_cli import OPERATING, make_synthetic_pdf_receipt_bundle

    _paths, payloads = make_synthetic_pdf_receipt_bundle(tmp_path)
    report = payloads["qa_report"]
    report["case_id"] = report_case
    return OPERATING.read_bytes(), json.dumps(report).encode()


def test_observed_current_qa_identity_can_join_original_report_case_alias(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import qa_combined_e2e_check as combined

    native, report = _synthetic_current_handoff(tmp_path)
    result = combined.audit_combined_bytes(
        native, (ROOT / "data/cases/SYN-C001/trusted_base_case.json").read_bytes(),
        (ROOT / "configs/schemas/document_extraction.schema.json").read_bytes(),
        case_id="C001", operational_job_id=json.loads(native)["metadata"]["job_execution_id"],
        github_sha="a" * 40, qa_native_bytes=native, qa_report_bytes=report,
        qa_agent_id=CURRENT_QA_AGENT, qa_config_id=CURRENT_QA_CONFIG, qa_config_version=1,
        execution_kind="ARCHIVED_REPLAY",
    )
    assert result["status"] == "BLOCKED"
    assert result["cross_agent_status"] == "BLOCKED"
    assert result["studio_document_status"] == "NOT_VERIFIED"
    assert result["qa_case_binding"] == {"canonical_case_id": "C001",
                                        "original_report_case_id": "SYN-C001"}
    assert result["sha256"]["qa_report"] == hashlib.sha256(report).hexdigest()
    assert result["actual_studio_e2e_status"] == "NOT_VERIFIED"
    assert result["release_or_merge_authorized"] is False


@pytest.mark.parametrize("config,version", [
    ("cfg_OTHER", 1), (CURRENT_QA_CONFIG, 2), (CURRENT_QA_CONFIG, True),
])
def test_observed_current_qa_agent_requires_frozen_config_and_version(tmp_path, config, version):
    from leadtime_guardian.qa.handoff_builder import build_studio_raw_handoff

    native, report = _synthetic_current_handoff(tmp_path)
    with pytest.raises(ValueError):
        build_studio_raw_handoff(
            native, report, case_id="SYN-C001", agent_id=CURRENT_QA_AGENT,
            config_id=config, config_version=version, github_sha="a" * 40,
        )


def test_current_qa_report_other_case_never_uses_synthetic_alias_mapping(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import qa_combined_e2e_check as combined

    native, report = _synthetic_current_handoff(tmp_path, report_case="SYN-C013")
    result = combined.audit_combined_bytes(
        native, (ROOT / "data/cases/SYN-C001/trusted_base_case.json").read_bytes(),
        (ROOT / "configs/schemas/document_extraction.schema.json").read_bytes(),
        case_id="C001", operational_job_id=json.loads(native)["metadata"]["job_execution_id"],
        github_sha="a" * 40, qa_native_bytes=native, qa_report_bytes=report,
        qa_agent_id=CURRENT_QA_AGENT, qa_config_id=CURRENT_QA_CONFIG, qa_config_version=1,
    )
    assert result["status"] == "FAIL"
    assert "qa_case_binding" not in result
    assert result["release_or_merge_authorized"] is False


def test_stage_qa_native_report_preserves_alias_and_observed_verdict():
    manifest, raw = _c013_stages()
    binding = manifest["stages"]["IndependentQA_Report"]
    native = {"content": json.dumps({"case_id": "SYN-C013", "qa_status": "NEEDS_REVIEW"}),
              "metadata": {"job_execution_id": binding["job_id"],
                           "step_run_id": binding["step_run_id"]}}
    raw["IndependentQA_Report"] = json.dumps(native).encode()
    binding["sha256"] = hashlib.sha256(raw["IndependentQA_Report"]).hexdigest()
    before = raw["IndependentQA_Report"]
    result = audit_stage_evidence(manifest, raw)
    assert result["status"] == "BLOCKED"
    assert result["stages"]["IndependentQA_Report"]["qa_report_status"] == "NEEDS_REVIEW"
    assert result["all_expected_raw_stages_present"] is True
    assert raw["IndependentQA_Report"] == before


def test_arbitrary_json_object_cannot_count_as_completed_qa_report():
    manifest, raw = evidence()
    raw["IndependentQA_Report"] = b'{}'
    manifest["stages"]["IndependentQA_Report"]["sha256"] = hashlib.sha256(b'{}').hexdigest()
    result = audit_stage_evidence(manifest, raw)
    assert result["status"] == "FAIL"
    assert result["all_expected_raw_stages_present"] is False
