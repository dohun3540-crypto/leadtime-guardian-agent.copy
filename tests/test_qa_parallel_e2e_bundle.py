"""New cross-file intake checks use local synthetic bytes, never Studio jobs."""
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from leadtime_guardian.qa.e2e_bundle_preflight import audit_parallel_e2e_bundle

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/team1_e2e_preflight.py"
TYPES = ("purchase_order", "delivery_notice", "quotation")


def write_json(path, object_value):
    path.write_text(json.dumps(object_value, ensure_ascii=False),
                    encoding="utf-8")
    return path


def make_bundle(tmp_path):
    """All source files are fake fixtures; only local identity is tested."""
    hashes = {}
    op_files = []
    qa_files = []
    native_sources = []
    pdf_paths = {}
    for kind in TYPES:
        name = f"SYN-C001_{kind}.pdf"
        raw = ("%PDF-1.4\nsynthetic " + kind + "\n%%EOF").encode()
        (tmp_path / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
        pdf_paths[kind] = name
        op_files.append({
            "filename": name, "sha256": hashes[name],
            "file_id": "file_OP_" + kind,
        })
        qa_files.append({
            "filename": name, "sha256": hashes[name],
            "file_id": "file_QA_" + kind,
        })
        native_sources.append({
            "file_name": name, "file_id": "file_OP_" + kind,
        })
    native = {
        "content": json.dumps({"documents": [
            {"document_id": "C001-" + kind, "document_type": kind}
            for kind in TYPES
        ]}),
        "metadata": {
            "job_execution_id": "job_OPERATION",
            "step_run_id": "step_NORMALIZE",
            "source_files": native_sources,
        },
    }
    native_path = write_json(tmp_path / "operational_native.json", native)
    sidecar = {
        "contract_version": "studio-provenance/1",
        "export_sha256": hashlib.sha256(native_path.read_bytes()).hexdigest(),
        "studio_metadata_supplied": {"job_execution_id": "job_OPERATION"},
        "evidence_verified_against_pdf": False,
        "business_validation_status": "COMPLETED",
    }
    write_json(tmp_path / "sidecar.json", sidecar)
    write_json(tmp_path / "op_receipt.json", {
        "case_id": "C001", "files": op_files,
    })
    write_json(tmp_path / "qa_receipt.json", {
        "case_id": "C001", "files": qa_files,
    })
    manifest = {
        "schema_version": "leadtime-release-evidence/v1",
        "case_id": "C001",
        "operational_job_id": "job_OPERATION",
        "config_id": "cfg_SYNTHETIC",
        "config_version": 1,
        "sources": {
            "source_pdfs": pdf_paths,
            "operational_native": native_path.name,
            "team2_provenance": "sidecar.json",
            "operational_pdf_receipt": "op_receipt.json",
            "qa_pdf_receipt": "qa_receipt.json",
        },
    }
    return write_json(tmp_path / "release.json", manifest)


def codes(report):
    return {item["issue_code"] for item in report["issues"]}


def update_json(path, transform):
    raw = json.loads(path.read_text())
    transform(raw)
    write_json(path, raw)


def test_no_origins_never_authenticates_or_invents_gold(tmp_path):
    path = write_json(tmp_path / "release.json", {
        "schema_version": "leadtime-release-evidence/v1",
        "case_id": "C001", "operational_job_id": "job_OP",
        "config_id": "cfg_TEST", "config_version": 1, "sources": {},
    })
    report = audit_parallel_e2e_bundle(path)
    assert report["status"] == "BLOCKED"
    assert report["missing_human_gold"] is True
    assert report["missing_team2_sidecar"] is True
    assert "stage.Extract.purchase_order" in report["missing_stage_records"]
    assert "qa_report" in report["missing_qa_records"]
    assert report["release_authorized"] is False
    assert report["improvement_status"] == "NOT_MEASURED"


def test_matching_local_receipts_sidecar_and_native_never_grant_live(tmp_path):
    manifest = make_bundle(tmp_path)
    originals = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    report = audit_parallel_e2e_bundle(manifest)
    assert report["status"] == "BLOCKED"
    assert report["local_pdf_receipt_match"] is True
    assert report["local_operational_native_binding"] is True
    assert report["local_team2_sidecar_binding"] is True
    assert report["studio_execution_authenticated"] is False
    assert report["human_gold_approved"] is False
    assert report["release_authorized"] is False
    assert originals == {
        p.name: p.read_bytes() for p in tmp_path.iterdir()
    }


@pytest.mark.parametrize("broken", [
    "hash", "file_id", "wrong_case", "duplicate_file_id",
])
def test_receipt_spoof_or_source_conflict_fails_closed(tmp_path, broken):
    manifest = make_bundle(tmp_path)
    p = tmp_path / "op_receipt.json"

    def tamper(value):
        if broken == "hash":
            value["files"][0]["sha256"] = "a" * 64
        elif broken == "file_id":
            value["files"][0]["file_id"] = "file_WRONG"
        elif broken == "wrong_case":
            value["case_id"] = "C013"
        else:
            value["files"][1]["file_id"] = value["files"][0]["file_id"]

    update_json(p, tamper)
    report = audit_parallel_e2e_bundle(manifest)
    assert report["status"] == "FAIL"
    assert report["release_authorized"] is False
    assert report["invalid_inputs"]


@pytest.mark.parametrize("broken", ["sha", "job", "contract", "pdf_claim"])
def test_sidecar_spoof_never_passes(tmp_path, broken):
    manifest = make_bundle(tmp_path)

    def tamper(value):
        if broken == "sha":
            value["export_sha256"] = "f" * 64
        elif broken == "job":
            value["studio_metadata_supplied"]["job_execution_id"] = "job_OTHER"
        elif broken == "contract":
            value["contract_version"] = "untrusted"
        else:
            value["evidence_verified_against_pdf"] = True

    update_json(tmp_path / "sidecar.json", tamper)
    report = audit_parallel_e2e_bundle(manifest)
    assert report["status"] == "FAIL"
    assert report["local_team2_sidecar_binding"] is False
    assert report["release_authorized"] is False


def test_separate_qa_job_is_not_operational_conflict(tmp_path):
    manifest = make_bundle(tmp_path)
    source = json.loads((tmp_path / "operational_native.json").read_text())
    qa = deepcopy(source)
    qa["metadata"]["job_execution_id"] = "job_DIFFERENT_QA"
    qa["metadata"]["step_run_id"] = "step_QA"
    for row in qa["metadata"]["source_files"]:
        row["file_id"] = row["file_id"].replace("file_OP_", "file_QA_")
    write_json(tmp_path / "qa_native.json", qa)
    update_json(
        manifest,
        lambda x: x["sources"].update({"qa_native": "qa_native.json"}),
    )
    report = audit_parallel_e2e_bundle(manifest)
    assert report["status"] == "BLOCKED"
    assert report["local_qa_native_checked"] is True
    assert "TEAM2_OPERATIONAL_JOB_CONFLICT" not in codes(report)


def test_duplicate_pdf_filename_manifest_is_rejected(tmp_path):
    manifest = make_bundle(tmp_path)
    update_json(manifest, lambda x: x["sources"]["source_pdfs"].update({
        "quotation": x["sources"]["source_pdfs"]["purchase_order"],
    }))
    assert "DUPLICATE_SOURCE_PDF_FILENAME" in codes(
        audit_parallel_e2e_bundle(manifest)
    )


def test_invalid_json_receipt_never_raises_or_passes(tmp_path):
    manifest = make_bundle(tmp_path)
    (tmp_path / "qa_receipt.json").write_bytes(
        b'{"case_id":"C001","files":[],"files":[]}'
    )
    report = audit_parallel_e2e_bundle(manifest)
    assert report["status"] == "FAIL"
    assert "VERIFIED_JSON_UNREADABLE" in codes(report)


def test_cli_missing_inputs_exit_two_and_no_overwrite(tmp_path):
    manifest = make_bundle(tmp_path)
    report = tmp_path / "preflight_output.json"
    args = [sys.executable, str(CLI), "--manifest", str(manifest),
            "--json-report", str(report)]
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                          timeout=40, check=False)
    assert proc.returncode == 2, proc.stderr
    assert json.loads(proc.stdout)["status"] == "BLOCKED"
    assert json.loads(report.read_text())["release_authorized"] is False
    second = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                            timeout=40, check=False)
    assert second.returncode == 1
    assert json.loads(second.stdout)["status"] == "FAIL"
    assert report.read_bytes() == report.read_bytes()


def test_cli_output_cannot_overwrite_input_manifest(tmp_path):
    manifest = make_bundle(tmp_path)
    original = manifest.read_bytes()
    proc = subprocess.run([
        sys.executable, str(CLI), "--manifest", str(manifest),
        "--json-report", str(manifest),
    ], cwd=ROOT, capture_output=True, text=True, timeout=40, check=False)
    assert proc.returncode == 1
    assert manifest.read_bytes() == original
