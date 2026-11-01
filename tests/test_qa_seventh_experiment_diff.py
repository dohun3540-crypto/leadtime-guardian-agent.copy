"""Actual B0/E1 E1 has NOT been provided. All scenarios are synthetic."""
import json
import subprocess
import sys
from pathlib import Path

from leadtime_guardian.qa.experiment_compare import (
    audit_b0_e1_readiness,
    compare_normalized_field_values,
)

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/qa_b0_e1_compare_check.py"
TYPES = ("purchase_order", "delivery_notice", "quotation")
STEPS = ("Extract", "MergeDocuments", "NormalizeDocuments", "IndependentQA")


def manifest(kind):
    return {
        "schema_version": "leadtime-experiment-compare/v1",
        "experiment": kind, "case_id": "C001",
        "single_case_job_count": 1,
        "job_id": "job_SYNTH_" + kind,
        "config_id": "cfg_SYNTH_" + kind,
        "config_version": 1, "saved_config_evidence": True,
        "source_pdfs": [
            {"filename": f"sample_{t}.pdf", "sha256": "a" * 64,
             "file_id": f"file_{kind}_{t}", "document_type": t}
            for t in TYPES
        ],
        "step_artifacts": {
            t: {"step_run_id": f"step_{kind}_{t}",
                "original_sha256": "b" * 64} for t in STEPS
        },
        "execution_conditions": {"task": "C001"},
    }


def normalized(*, altered=False):
    return {
        "case_id": "C001",
        "documents": [
            {"document_id": "PO-DOC", "document_type": "purchase_order",
             "supplier_id": "" if altered else None,
             "items": [{"quantity": 0, "receipt_id": "R1"}]},
            {"document_id": "NOTICE-DOC", "document_type": "delivery_notice",
             "revised_delivery": "2026-11-08"},
            {"document_id": "QUOTE-DOC", "document_type": "quotation",
             "quote": {"capacity": 60, "unit_price": "1000.00"}},
        ],
    }


def readiness():
    return audit_b0_e1_readiness(manifest("B0"), manifest("E1"))


def test_semantic_field_delta_is_only_unverified_change():
    report = compare_normalized_field_values(
        normalized(), normalized(altered=True), readiness(),
    )
    assert report["field_comparison_status"] == "CHANGED_UNVERIFIED"
    assert report["changed_field_count"] == 1
    row = report["changes"][0]
    assert row["path"] == "purchase_order.supplier_id"
    assert row["b0_type"] == "NoneType"
    assert row["e1_type"] == "str"
    assert row["e1_value"] == ""
    assert report["human_gold_accuracy"] == "NOT_MEASURED"
    assert report["studio_comparison_authenticated"] is False
    assert report["release_or_merge_authorized"] is False


def test_unchanged_local_values_do_not_assert_improvement():
    report = compare_normalized_field_values(normalized(), normalized(), readiness())
    assert report["field_comparison_status"] == "UNCHANGED"
    assert report["improvement_verdict"] == "NOT_MEASURED"
    assert report["changed_field_count"] == 0


def test_true_zero_vs_boolean_is_detected_by_type():
    a = normalized()
    b = normalized()
    b["documents"][0]["items"][0]["quantity"] = False
    report = compare_normalized_field_values(a, b, readiness())
    assert report["field_comparison_status"] == "CHANGED_UNVERIFIED"
    assert report["changes"][0]["b0_type"] == "int"
    assert report["changes"][0]["e1_type"] == "bool"


def test_missing_pdf_hash_comparison_is_blocked():
    bad = readiness()
    bad["pdf_sha256_sets_equal"] = False
    report = compare_normalized_field_values(normalized(), normalized(), bad)
    assert report["field_comparison_status"] == "BLOCKED"


def test_duplicate_document_ids_block_pair():
    a = normalized()
    a["documents"][1]["document_id"] = "PO-DOC"
    report = compare_normalized_field_values(a, normalized(), readiness())
    assert report["field_comparison_status"] == "BLOCKED"
    assert "B0_DOCUMENTS_DUPLICATE_OR_MISSING" in report["issues"]


def test_cross_case_report_blocks_diff():
    a = normalized()
    a["case_id"] = "C013"
    report = compare_normalized_field_values(a, normalized(), readiness())
    assert report["field_comparison_status"] == "BLOCKED"


def test_cli_synthetic_pair_with_normalize_files_is_not_live_success(tmp_path):
    paths = {}
    for kind in ("B0", "E1"):
        path = tmp_path / (kind + ".json")
        path.write_text(json.dumps(manifest(kind)))
        paths[kind] = path
        norm = tmp_path / (kind + "-normalize.json")
        norm.write_text(json.dumps(normalized(altered=kind == "E1")))
        paths[kind + "_NORMALIZE"] = norm
    proc = subprocess.run([
        sys.executable, str(CLI),
        "--b0", str(paths["B0"]), "--e1", str(paths["E1"]),
        "--b0-normalize", str(paths["B0_NORMALIZE"]),
        "--e1-normalize", str(paths["E1_NORMALIZE"]),
    ], cwd=ROOT, capture_output=True, text=True, check=False, timeout=30)
    out = json.loads(proc.stdout)
    assert proc.returncode == 2, proc.stderr
    assert out["comparison_status"] == "NOT_MEASURED"
    assert out["field_comparison"]["field_comparison_status"] == "CHANGED_UNVERIFIED"
    assert out["eligibility"] == "BLOCKED"
