"""Read-only cross-artifact joins absent from single-file evidence inventory.

Reuse existing release, native and experiment validators; these comparisons
prove local byte/identity consistency, never cloud upload authentication.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .audit import load_json_strict
from .experiment_compare import audit_b0_e1_readiness
from .release_inventory import PDF_KINDS, audit_release_folder
from .studio_contract import audit_native_envelope

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
CASE_PREFIX = re.compile(r"^(?:SYN-)?(C[0-9]{3})[-_]")
MAX_JSON_BYTES = 16 * 1024 * 1024


def audit_parallel_e2e_bundle(manifest_path: str | Path) -> dict[str, Any]:
    """Join already hash-verified source files without accepting self-attestation.

    A complete local bundle remains BLOCKED until the real provider, reviewer,
    and measured B0/E1 evidence are independently authenticated.
    """
    path = Path(manifest_path)
    inventory = audit_release_folder(path)
    missing = list(inventory["missing_inputs"])
    invalid = list(inventory["invalid_inputs"])
    conflicts: list[str] = []
    issues: list[dict[str, str]] = []
    checked = inventory["checked_inputs"]
    results: dict[str, Any] = {
        "schema_version": "leadtime-team1-parallel-preflight/v1",
        "status": "FAIL" if inventory["status"] == "FAIL" else "BLOCKED",
        "missing_inputs": missing,
        "invalid_inputs": invalid,
        "source_identity_conflicts": conflicts,
        "missing_stage_records": [
            x for x in missing if x.startswith("stage.")
        ],
        "missing_qa_records": [
            x for x in missing if x in ("qa_native", "qa_report")
        ],
        "missing_team2_sidecar": "team2_provenance" in missing,
        "missing_human_gold": "human_gold" in missing,
        "local_pdf_receipt_match": False,
        "local_operational_native_binding": False,
        "local_team2_sidecar_binding": False,
        "local_qa_native_checked": False,
        "local_stage_status": inventory["local_stage_status"],
        "b0_e1_eligibility": "NOT_VERIFIED",
        "improvement_status": "NOT_MEASURED",
        "official_metrics_eligible": False,
        "verification_scope": "LOCAL_SOURCE_BYTES_ONLY",
        "studio_execution_authenticated": False,
        "human_gold_approved": False,
        "release_authorized": False,
        "issues": issues,
        "next_required_action": inventory["next_required_action"],
    }

    def flag(code: str, source: str, *, conflict: bool = False) -> None:
        issues.append({"issue_code": code, "source": source})
        if source not in invalid:
            invalid.append(source)
        if conflict and code not in conflicts:
            conflicts.append(code)

    def read_checked(name: str) -> Any | None:
        entry = checked.get(name)
        if entry is None:
            return None
        try:
            file = (path.resolve(strict=True).parent / entry["relative_path"])
            file = file.resolve(strict=True)
            if not file.is_relative_to(path.resolve(strict=True).parent):
                raise ValueError("escaped source root")
            if file.stat().st_size > MAX_JSON_BYTES:
                raise ValueError("oversized JSON input")
            raw = file.read_bytes()
            if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
                raise ValueError("changed bytes since inventory")
            value = load_json_strict(raw)
            if not isinstance(value, dict):
                flag("VERIFIED_JSON_NOT_OBJECT", name)
                return None
            return value
        except (OSError, TypeError, ValueError, UnicodeError, RecursionError):
            flag("VERIFIED_JSON_UNREADABLE", name)
            return None

    try:
        if path.stat().st_size > 1024 * 1024:
            raise ValueError("oversized release manifest")
        header = load_json_strict(path.read_bytes())
        if not isinstance(header, dict):
            raise TypeError("header must be object")
    except (OSError, TypeError, ValueError, UnicodeError, RecursionError):
        header = {}
        # The existing inventory already records invalid manifest identity.

    case = header.get("case_id")
    job = header.get("operational_job_id")
    expected_pdf = {}
    pdf_by_kind: dict[str, str] = {}
    for kind in PDF_KINDS:
        name = "source_pdfs." + kind
        data = checked.get(name)
        if isinstance(data, dict):
            filename = Path(data["relative_path"]).name
            if filename in expected_pdf:
                flag("DUPLICATE_SOURCE_PDF_FILENAME", name, conflict=True)
            expected_pdf[filename] = data["sha256"]
            pdf_by_kind[kind] = filename

    def receipt(name: str) -> dict[str, tuple[str, str]] | None:
        payload = read_checked(name)
        if payload is None:
            return None
        if not isinstance(payload, dict):
            flag("INVALID_RECEIPT_OBJECT", name)
            return None
        if payload.get("case_id") != case:
            flag("RECEIPT_CASE_MISMATCH", name, conflict=True)
        entries = payload.get("files")
        if not isinstance(entries, list) or len(entries) != 3:
            flag("RECEIPT_THREE_FILES_REQUIRED", name)
            return None
        rows: dict[str, tuple[str, str]] = {}
        ids: set[str] = set()
        for i, item in enumerate(entries):
            source = f"{name}.files[{i}]"
            if not isinstance(item, dict):
                flag("INVALID_RECEIPT_ROW", source)
                continue
            filename, digest, file_id = (
                item.get("filename"), item.get("sha256"), item.get("file_id")
            )
            if (not isinstance(filename, str)
                    or not filename.endswith(".pdf")
                    or Path(filename).name != filename
                    or filename in rows
                    or not isinstance(digest, str)
                    or HEX64.fullmatch(digest) is None
                    or not isinstance(file_id, str)
                    or not file_id.startswith("file_")
                    or file_id in ids):
                flag("INVALID_RECEIPT_IDENTITY", source)
                continue
            ids.add(file_id)
            rows[filename] = (digest.lower(), file_id)
        if len(rows) != 3:
            flag("INCOMPLETE_RECEIPT_ROWS", name)
        if (len(expected_pdf) == 3 and
                {n: sha for n, (sha, _) in rows.items()} != expected_pdf):
            flag("RECEIPT_PDF_BYTE_IDENTITY_MISMATCH", name, conflict=True)
        return rows

    operational_receipt = receipt("operational_pdf_receipt")
    qa_receipt = receipt("qa_pdf_receipt")
    if operational_receipt is not None and qa_receipt is not None:
        op_hashes = {k: v[0] for k, v in operational_receipt.items()}
        qa_hashes = {k: v[0] for k, v in qa_receipt.items()}
        if op_hashes != qa_hashes:
            flag("OPERATION_QA_PDF_HASH_SET_CONFLICT",
                 "pdf_receipts", conflict=True)
        elif len(expected_pdf) == 3 and op_hashes == expected_pdf:
            results["local_pdf_receipt_match"] = True

    native = read_checked("operational_native")
    if native is not None:
        audit = audit_native_envelope(native, expected_job_id=job)
        if audit["qa_status"] != "PASS":
            flag("OPERATIONAL_NATIVE_CONTRACT_FAILED",
                 "operational_native")
        else:
            meta = native["metadata"]
            # Optional provider-supplied identity must agree with the
            # saved operational manifest. Missing metadata is not invented.
            for field in ("config_id", "config_version"):
                if field in meta and (
                    type(meta[field]) is not type(header.get(field))
                    or meta[field] != header.get(field)
                ):
                    flag(
                        "OPERATIONAL_NATIVE_" + field.upper() + "_CONFLICT",
                        "operational_native", conflict=True,
                    )
            # Actual archived Native can use PO-DOC/NOTICE-DOC IDs; only
            # explicit C###-prefixed document identities are case-bound.
            normalized = load_json_strict(native["content"])
            for document in normalized["documents"]:
                document_id = document.get("document_id")
                match = CASE_PREFIX.match(document_id)
                if match is not None and match.group(1) != case:
                    flag("OPERATIONAL_DOCUMENT_CASE_CONFLICT",
                         "operational_native", conflict=True)
            merge = meta.get("merge")
            if isinstance(merge, dict):
                items = merge.get("items")
                if isinstance(items, list):
                    for item in items:
                        if not isinstance(item, dict):
                            continue
                        expected_name = pdf_by_kind.get(item.get("document_type"))
                        references = item.get("source_files")
                        if expected_name is None or not isinstance(references, list):
                            continue
                        if any(
                            isinstance(ref, dict)
                            and ref.get("file_name") != expected_name
                            for ref in references
                        ):
                            flag("MERGE_SOURCE_DOCUMENT_TYPE_MISMATCH",
                                 "operational_native", conflict=True)
            sources = meta.get("source_files")
            if operational_receipt is None:
                pass  # Receipt absence is already a BLOCKED inventory issue.
            elif not isinstance(sources, list) or len(sources) != 3:
                flag("NATIVE_SOURCE_FILE_SET_INCOMPLETE",
                     "operational_native")
            else:
                native_ids = {}
                for item in sources:
                    if isinstance(item, dict):
                        name = item.get("file_name")
                        fid = item.get("file_id")
                        if isinstance(name, str) and isinstance(fid, str):
                            native_ids[name] = fid
                op_ids = {n: fid for n, (_, fid) in operational_receipt.items()}
                if len(native_ids) != 3 or native_ids != op_ids:
                    flag("NATIVE_RECEIPT_FILE_ID_MISMATCH",
                         "operational_native", conflict=True)
                elif (results["local_pdf_receipt_match"]
                      and not any(
                          x["source"] == "operational_native" for x in issues
                      )):
                    results["local_operational_native_binding"] = True

    sidecar = read_checked("team2_provenance")
    if sidecar is not None:
        if (not isinstance(sidecar, dict)
                or sidecar.get("contract_version") != "studio-provenance/1"):
            flag("INVALID_TEAM2_PROVENANCE_CONTRACT", "team2_provenance")
        else:
            metadata = sidecar.get("studio_metadata_supplied")
            if (not isinstance(metadata, dict)
                    or metadata.get("job_execution_id") != job):
                flag("TEAM2_OPERATIONAL_JOB_CONFLICT",
                     "team2_provenance", conflict=True)
            if "operational_native" in checked:
                expected = checked["operational_native"]["sha256"]
                if sidecar.get("export_sha256") != expected:
                    flag("TEAM2_NATIVE_SHA_CONFLICT",
                         "team2_provenance", conflict=True)
                elif not any(
                    x["source"] == "team2_provenance" for x in issues
                ):
                    results["local_team2_sidecar_binding"] = True
            if sidecar.get("evidence_verified_against_pdf") is not False:
                flag("UNSUPPORTED_TEAM2_PDF_VERIFICATION",
                     "team2_provenance")
                results["local_team2_sidecar_binding"] = False

    qa_native = read_checked("qa_native")
    if qa_native is not None:
        meta = qa_native.get("metadata")
        qa_raw = qa_native.get("content")
        if (not isinstance(meta, dict)
                or not isinstance(meta.get("job_execution_id"), str)
                or not meta["job_execution_id"].startswith("job_")
                or not isinstance(meta.get("step_run_id"), str)
                or not meta["step_run_id"].strip()
                or not isinstance(qa_raw, str)):
            flag("QA_NATIVE_METADATA_INVALID", "qa_native")
        else:
            try:
                parsed_qa = load_json_strict(qa_raw)
                if not isinstance(parsed_qa, dict):
                    raise TypeError("QA content must be JSON object")
            except (TypeError, ValueError, UnicodeError, RecursionError):
                flag("QA_NATIVE_CONTENT_INVALID", "qa_native")
            else:
                # The QA step may emit a QA verdict, not an operational
                # Normalize 'documents' wrapper, and can have a separate Job.
                results["local_qa_native_checked"] = True
                files = meta.get("source_files")
                if files is not None and qa_receipt is not None:
                    local_ids = {
                        item.get("file_name"): item.get("file_id")
                        for item in files if isinstance(item, dict)
                        and isinstance(item.get("file_name"), str)
                    } if isinstance(files, list) else {}
                    qa_ids = {n: fid for n, (_, fid) in qa_receipt.items()}
                    if len(local_ids) != 3 or local_ids != qa_ids:
                        flag("QA_NATIVE_RECEIPT_ID_MISMATCH",
                             "qa_native", conflict=True)
                        results["local_qa_native_checked"] = False
    # A supplied raw QA report must at least be strict JSON, not just a
    # file with matching declared hash. Full schema is the Cross-Agent CLI's job.
    qa_report = read_checked("qa_report")
    results["local_qa_report_json_checked"] = qa_report is not None
    # The existing Cross-Agent CLI separately validates report semantics and
    # original QA Input; never treat parseable content as a trusted QA verdict.

    b0 = read_checked("b0_manifest")
    e1 = read_checked("e1_manifest")
    if (b0 is None) != (e1 is None):
        results["b0_e1_eligibility"] = "BLOCKED"
        results["next_required_action"] = (
            "Supply both original B0/E1 manifests for same-PDF comparison."
        )
    elif b0 is not None and e1 is not None:
        comparison = audit_b0_e1_readiness(b0, e1)
        results["b0_e1_eligibility"] = comparison["eligibility"]
        if comparison["eligibility"] == "FAIL":
            flag("B0_E1_SOURCE_CONTRACT_CONFLICT",
                 "experiment_manifests", conflict=True)
        elif comparison["case_id"] != case:
            flag("EXPERIMENT_RELEASE_CASE_CONFLICT",
                 "experiment_manifests", conflict=True)
        else:
            declared = header.get("sources", {}).get("source_pdfs")
            if isinstance(declared, dict) and len(expected_pdf) == 3:
                for alias, exp in (("B0", b0), ("E1", e1)):
                    rows = exp.get("source_pdfs")
                    if not isinstance(rows, list):
                        continue
                    claimed = {
                        x["filename"]: x["sha256"].lower()
                        for x in rows
                        if isinstance(x, dict)
                        and isinstance(x.get("filename"), str)
                        and isinstance(x.get("sha256"), str)
                    }
                    if claimed != expected_pdf:
                        flag("EXPERIMENT_LOCAL_PDF_HASH_CONFLICT",
                             alias, conflict=True)

    invalid.sort()
    missing.sort()
    conflicts.sort()
    issues.sort(key=lambda item: (item["source"], item["issue_code"]))
    if invalid or inventory["status"] == "FAIL":
        results["status"] = "FAIL"
        results["next_required_action"] = (
            "Correct the identified raw-byte, manifest, or identity conflicts."
        )
    elif not results["next_required_action"]:
        results["next_required_action"] = (
            "Run existing combined QA/Studio/Gold validators after authentic "
            "provider upload and human-review evidence is supplied."
        )
    return results
