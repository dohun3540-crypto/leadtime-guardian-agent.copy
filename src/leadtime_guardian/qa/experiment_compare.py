"""B0/E1 experiment eligibility contract; no fabricated QA or accuracy metrics.

Manifest-only evidence may block a comparison or establish a structural mismatch.
It cannot independently authenticate Upstage jobs or source PDF upload bytes.
"""
from __future__ import annotations

import re
from typing import Any

HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
REQUIRED_TYPES = frozenset({"purchase_order", "delivery_notice", "quotation"})
REQUIRED_STEPS = frozenset({
    "Extract", "MergeDocuments", "NormalizeDocuments", "IndependentQA",
})
VERSION = "leadtime-experiment-compare/v1"


def audit_b0_e1_readiness(b0: Any, e1: Any) -> dict[str, Any]:
    """Never compute accuracy/cost/quality metrics from incomplete manifests."""
    issues: list[dict[str, str]] = []
    status = "BLOCKED"

    def add(code: str, side: str, *, severity: str = "WARNING") -> None:
        issues.append({"issue_code": code, "side": side, "severity": severity})

    result = {
        "comparison_status": "NOT_MEASURED",
        "eligibility": "BLOCKED",
        "case_id": None,
        "pdf_sha256_sets_equal": False,
        "local_pdf_bytes_verified": False,
        "studio_job_authenticity_verified": False,
        "exact_saved_config_verified": False,
        "independent_qa_report_verified": False,
        "accuracy": "NOT_MEASURED",
        "evidence_completeness": "NOT_MEASURED",
        "null_and_zero_preservation": "NOT_MEASURED",
        "qa_status_change": "NOT_MEASURED",
        "release_or_merge_authorized": False,
        "issues": issues,
    }
    if not isinstance(b0, dict) or not isinstance(e1, dict):
        add("MANIFESTS_REQUIRED", "both", severity="ERROR")
        return result

    def inspect(raw: dict, side: str):
        if raw.get("schema_version") != VERSION:
            add("INVALID_EXPERIMENT_MANIFEST_VERSION", side, severity="ERROR")
        if raw.get("experiment") != side:
            add("WRONG_EXPERIMENT_ALIAS", side, severity="ERROR")
        case = raw.get("case_id")
        if not isinstance(case, str) or not case.strip():
            add("CASE_ID_NOT_OBSERVED", side, severity="ERROR")
        if (type(raw.get("single_case_job_count")) is not int
                or raw["single_case_job_count"] != 1):
            add("SINGLE_CASE_JOB_NOT_CONFIRMED", side)
        job = raw.get("job_id")
        if not isinstance(job, str) or not job.startswith("job_"):
            add("JOB_ID_NOT_OBSERVED", side)
        config = raw.get("config_id")
        version = raw.get("config_version")
        if (not isinstance(config, str) or not config.startswith("cfg_")
                or type(version) is not int or version < 1):
            add("SAVED_CONFIG_REFERENCE_MISSING", side)
        if raw.get("saved_config_evidence") is not True:
            add("SAVED_CONFIG_NOT_AUTHENTICATED", side)
        originals = raw.get("source_pdfs")
        mapping = {}
        if not isinstance(originals, list) or len(originals) != 3:
            add("THREE_PDF_SOURCES_NOT_OBSERVED", side)
        else:
            for item in originals:
                if not isinstance(item, dict):
                    add("INVALID_PDF_SOURCE_ENTRY", side, severity="ERROR")
                    continue
                name, digest, fid, kind = (
                    item.get("filename"), item.get("sha256"),
                    item.get("file_id"), item.get("document_type"),
                )
                if (not isinstance(name, str) or not name.endswith(".pdf")
                        or "/" in name or "\\" in name
                        or not isinstance(digest, str) or not HEX64.fullmatch(digest)
                        or not isinstance(fid, str) or not fid.startswith("file_")
                        or not isinstance(kind, str) or kind not in REQUIRED_TYPES):
                    add("PDF_ORIGINAL_SHA_AND_FILE_ID_REQUIRED", side)
                    continue
                if name in mapping:
                    add("DUPLICATE_PDF_FILENAME", side, severity="ERROR")
                mapping[name] = (digest.lower(), kind)
            if {x[1] for x in mapping.values()} != REQUIRED_TYPES:
                add("PDF_DOCUMENT_TYPE_SET_INCOMPLETE", side)
        steps = raw.get("step_artifacts")
        if not isinstance(steps, dict):
            add("STEP_ARTIFACTS_NOT_PROVIDED", side)
        else:
            for step in sorted(REQUIRED_STEPS):
                data = steps.get(step)
                if (not isinstance(data, dict)
                        or not isinstance(data.get("step_run_id"), str)
                        or not data["step_run_id"].strip()
                        or not isinstance(data.get("original_sha256"), str)
                        or not HEX64.fullmatch(data["original_sha256"])):
                    add("RAW_STEP_ARTIFACT_NOT_VERIFIED:" + step, side)
        if not isinstance(raw.get("execution_conditions"), dict):
            add("EXECUTION_CONDITIONS_NOT_RECORDED", side)
        return case, mapping

    case0, pdf0 = inspect(b0, "B0")
    case1, pdf1 = inspect(e1, "E1")
    if isinstance(case0, str) and case0 == case1:
        result["case_id"] = case0
    else:
        add("EXPERIMENT_CASE_ID_MISMATCH", "pair", severity="ERROR")
    if pdf0 and pdf1 and pdf0 == pdf1 and len(pdf0) == 3:
        result["pdf_sha256_sets_equal"] = True
    elif pdf0 and pdf1:
        add("B0_E1_PDF_SOURCE_MISMATCH", "pair", severity="ERROR")
    if (b0.get("job_id") is not None and b0.get("job_id") == e1.get("job_id")):
        add("DUPLICATE_EXPERIMENT_JOB_ID", "pair", severity="ERROR")
    conditions_b = b0.get("execution_conditions")
    conditions_e = e1.get("execution_conditions")
    if (isinstance(conditions_b, dict) and isinstance(conditions_e, dict)
            and set(conditions_b) != set(conditions_e)):
        add("EXPERIMENT_CONDITION_KEYS_DIFFER", "pair")
    if any(x["severity"] == "ERROR" for x in issues):
        status = "FAIL"
    # No local raw bytes were supplied through this manifest-only API.
    # Equal self-asserted SHA values cannot authenticate actual Studio uploads.
    result["eligibility"] = status
    return result
