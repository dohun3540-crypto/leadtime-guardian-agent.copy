"""Review and demonstration boundaries; no simulated run may become Native PASS."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_numeric_nullable_flag_is_not_a_confirmed_live_defect():
    review = load_script("team1_schema_review")
    config = {"workflowConfig": {"informationExtractConfiguration": {"schemas": [{
        "addNullTypeToNumericTypes": True,
        "json_schema": {"name": "Extract_quotation", "schema": {
            "type": "object", "properties": {"quote": {
                "type": "array", "items": {"type": "object", "required": ["capacity"],
                "properties": {"capacity": {"type": "integer", "description": "Null if absent"}}}
            }}
        }}
    }]}}}
    original = copy.deepcopy(config)
    row = review.review_config(config, [])["rows"][0]
    assert row["field_path"] == "Extract_quotation.quote[].capacity"
    assert row["required_in_immediate_container"] is True
    assert row["required_if_parent_absent"] is False
    assert row["classification"] == "NOT_VERIFIED"
    assert row["reproduction"]["json_null_rejected_by_declared_leaf"] is True
    assert row["reproduction"]["live_null_type_failure_confirmed"] is False
    assert config == original


def test_empty_quote_array_does_not_exercise_nullable_quote_leaf():
    review = load_script("team1_schema_review")
    config = {"workflowConfig": {"informationExtractConfiguration": {"schemas": [{
        "json_schema": {"name": "Extract_purchase_order", "schema": {
            "properties": {"quote": {"type": "array", "items": {"properties": {
                "quote_id": {"type": "string", "description": "Null if absent"}
            }}}}
        }}
    }]}}}
    observation = {"source": "gold/unapproved.json", "sha256": "a" * 64,
                   "document": {"document_type": "purchase_order", "quote": []}}
    row = review.review_config(config, [observation])["rows"][0]
    assert row["classification"] == "POTENTIAL_CONFLICT"
    assert row["observed_extract"][0]["branch_exercised"] is False
    assert row["null_observed"] is False
    assert row["reproduction"]["live_null_type_failure_confirmed"] is False


def test_demo_rejects_qa_from_another_job_before_running_python(tmp_path):
    demo = load_script("team1_replay_demo")
    folder = tmp_path / "verification_v2/studio_originals"
    folder.mkdir(parents=True)
    for name, job in (("NormalizeDocuments", "job_one"), ("IndependentQA", "job_two")):
        (folder / f"C001_{name}.native.json").write_text(json.dumps({
            "metadata": {"job_execution_id": job}, "content": "{}"
        }))
    with pytest.raises(ValueError, match="Job mismatch"):
        demo.replay_case("C001", tmp_path, tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_demo_rejects_same_job_with_different_source_rows(tmp_path):
    demo = load_script("team1_replay_demo")
    folder = tmp_path / "verification_v2/studio_originals"
    folder.mkdir(parents=True)
    for name, file_id in (("NormalizeDocuments", "file_one"), ("IndependentQA", "file_two")):
        (folder / f"C001_{name}.native.json").write_text(json.dumps({
            "metadata": {"job_execution_id": "job_same", "source_files": [file_id]},
            "content": "{}"
        }))
    with pytest.raises(ValueError, match="source rows mismatch"):
        demo.replay_case("C001", tmp_path, tmp_path / "out")
    assert not (tmp_path / "out").exists()
