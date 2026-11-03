"""Reproduce C001/C013 from retained Native bytes; no cloud requests or purchases.

Use the unpacked PRIVATE_EVIDENCE_SNAPSHOT from the resume checkpoint as input.
The existing Combined E2E CLI supplies the conservative integration verdict.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from leadtime_guardian.qa.audit import load_json_strict
from leadtime_guardian.qa.studio_qa_adapter import normalize_studio_qa_report
from leadtime_guardian.studio_integration import analyze_studio_documents, documents_from_export


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replay_case(case_id: str, evidence_root: Path, output: Path) -> dict:
    originals = evidence_root / "verification_v2/studio_originals"
    native_path = originals / f"{case_id}_NormalizeDocuments.native.json"
    qa_path = originals / f"{case_id}_IndependentQA.native.json"
    base_path = ROOT / f"data/cases/SYN-{case_id}/trusted_base_case.json"
    schema_path = ROOT / "configs/schemas/document_extraction.schema.json"
    native = load_json_strict(native_path.read_bytes())
    qa = load_json_strict(qa_path.read_bytes())
    job = native["metadata"]["job_execution_id"]
    if job != qa["metadata"]["job_execution_id"]:
        raise ValueError("Normalize/QA Job mismatch; refuse mixed-run demonstration")
    if native["metadata"]["source_files"] != qa["metadata"]["source_files"]:
        raise ValueError("Normalize/QA source rows mismatch")
    docs = documents_from_export(native, expected_job_id=job)
    base = load_json_strict(base_path.read_bytes())
    schema = load_json_strict(schema_path.read_bytes())
    result = analyze_studio_documents(base, docs, schema)
    qa_report = load_json_strict(qa["content"])
    qa_adapter = normalize_studio_qa_report(
        qa_report, expected_case_id="SYN-" + case_id,
        expected_document_ids=[d["document_id"] for d in docs],
    )
    run = subprocess.run([
        sys.executable, str(ROOT / "scripts/qa_combined_e2e_check.py"),
        "--operational-native", str(native_path), "--trusted-base", str(base_path),
        "--schema", str(schema_path), "--operational-job-id", job,
        "--case-id", case_id, "--github-sha", "8b671d4a67cd649b08c4e6603a457f607342c3d7",
        "--execution-kind", "ARCHIVED_REPLAY",
    ], capture_output=True, text=True, check=False)
    if run.returncode not in (0, 2):
        raise ValueError("Existing combined CLI failed: " + run.stderr)
    combined = load_json_strict(run.stdout)
    expected = (result["execution_status"] == "COMPLETED"
                and result["changed_shortage_quantity"] == 60
                and result["estimated_quote_cost_krw"] == "60500.00") if case_id == "C001" else (
                    result["execution_status"] == "BLOCKED"
                    and result["estimated_quote_cost_krw"] is None
                    and not result["supplier_options"])
    passed = (expected and combined["status"] == "BLOCKED"
              and combined["release_or_merge_authorized"] is False
              and qa_adapter["adapter_status"] == "PASS")
    case_out = output / case_id
    save(case_out / "analysis.json", result)
    save(case_out / "combined_e2e.json", combined)
    save(case_out / "qa_adapter.json", qa_adapter)
    summary = {
        "case_id": case_id, "status": "PASS_LOCAL" if passed else "FAIL",
        "execution_provenance": "LOCAL_REPLAY_OF_RETAINED_NATIVE",
        "historical_job_id": job, "new_studio_runs_started": 0,
        "python_execution_status": result["execution_status"],
        "changed_shortage_quantity": result["changed_shortage_quantity"],
        "estimated_quote_cost_krw": result["estimated_quote_cost_krw"],
        "review_flags": result["review_flags"],
        "studio_document_qa_status": qa_adapter["document_qa_status"],
        "combined_e2e_status": combined["status"],
        "combined_cli_exit_code": run.returncode,
        "combined_cli_qa_artifacts_supplied": False,
        "qa_report_validation_scope": "SEPARATE_STRUCTURAL_ADAPTER_CHECK_ONLY",
        "actual_qa_input_available": False, "release_authorized": False,
        "input_files": [{"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in (native_path, qa_path, base_path, schema_path)],
        "pdf_inputs": [{"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                       for p in sorted((originals / "source_pdfs").glob(f"SYN-{case_id}_*.pdf"))],
        "pdf_note": "C001 retained provider bytes; C013 provider PDF bytes not acquired",
        "official_accuracy": None, "pdf_grounding_verified": False,
    }
    save(case_out / "summary.json", summary)
    return summary


def replay_draft(case_id: str, output: Path) -> dict:
    """Optional fixture scenarios, explicitly separate from retained Native replay."""
    folder = ROOT / f"data/cases/SYN-{case_id}"
    draft_path = folder / "extraction_gold.DRAFT.json"
    base_path = folder / "trusted_base_case.json"
    result = analyze_studio_documents(
        load_json_strict(base_path.read_bytes()),
        load_json_strict(draft_path.read_bytes())["documents"],
        load_json_strict((ROOT / "configs/schemas/document_extraction.schema.json").read_bytes()),
    )
    shortage, cost = (40, "40500.00") if case_id == "C008" else (60, "60500.00")
    passed = (result["execution_status"] == "COMPLETED"
              and result["changed_shortage_quantity"] == shortage
              and result["estimated_quote_cost_krw"] == cost)
    save(output / case_id / "analysis.json", result)
    return {"case_id": case_id, "status": "PASS_LOCAL" if passed else "FAIL",
            "execution_provenance": "SYNTHETIC_DRAFT_LOCAL_ONLY",
            "draft_sha256": hashlib.sha256(draft_path.read_bytes()).hexdigest(),
            "changed_shortage_quantity": result["changed_shortage_quantity"],
            "estimated_quote_cost_krw": result["estimated_quote_cost_krw"],
            "new_studio_runs_started": 0, "gold_approved": False,
            "note": "C017 starts from ISO fixture; Korean PDF-to-ISO conversion is unmeasured",
            "release_authorized": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--include-drafts", action="store_true")
    args = parser.parse_args()
    try:
        rows = [replay_case(c, args.evidence_root.resolve(), args.out.resolve())
                for c in ("C001", "C013")]
        if args.include_drafts:
            rows.extend(replay_draft(c, args.out.resolve()) for c in ("C008", "C017"))
        report = {"status": "PASS_LOCAL" if all(r["status"] == "PASS_LOCAL" for r in rows)
                  else "FAIL", "cases": rows, "release_gate": "BLOCKED",
                  "gold_approved": False, "official_metrics": "NOT_MEASURED"}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        report = {"status": "FAIL", "error_type": type(exc).__name__,
                  "reason": str(exc), "release_gate": "BLOCKED"}
    save(args.out / "DEMO_EVALUATION.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS_LOCAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
