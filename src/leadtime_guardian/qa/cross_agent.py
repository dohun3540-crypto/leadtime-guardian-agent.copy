"""Cross-agent QA handoff validator, independent of the Studio QA output schema.

This validates an explicit *handoff manifest*, NOT an unobserved Studio node
output. Live claims remain self-reported until externally evidenced.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

from .audit import load_json_strict
from .studio_contract import audit_native_envelope

HANDOFF_VERSION = "leadtime-cross-agent/v1"
SANDBOX_AGENT_ID = "agt_GhP9GywhbcDWquFqWTsmtq"
DOCUMENT_STATES = frozenset({"PASS", "FAIL", "NEEDS_REVIEW", "NOT_VERIFIED"})
PYTHON_STATES = frozenset({"PASS", "FAIL", "NOT_RUN", "NOT_VERIFIED", "BLOCKED"})
KINDS = frozenset({"NEW_LIVE_STUDIO", "ARCHIVED_STUDIO", "ARCHIVED_REPLAY",
                   "SDK_HTTP_MOCK", "FAKE_CLIENT_TEST", "SYNTHETIC_FIXTURE"})
SEVERITIES = frozenset({"INFO", "WARNING", "ERROR"})
ISSUE_SCOPES = frozenset({"document", "python", "provenance", "integration"})
HEX64 = re.compile(r"^[a-fA-F0-9]{64}$")
HEX40 = re.compile(r"^[a-fA-F0-9]{40}$")


def audit_cross_agent_handoff(
    manifest: Any, *,
    native_bytes: bytes | None = None, report_bytes: bytes | None = None,
    expected_agent_id: str = SANDBOX_AGENT_ID,
    expected_config_id: str | None = None,
    expected_github_sha: str | None = None,
    archived_job_ids: tuple[str, ...] = ("job_gPmEYKzuJdBA6BmKhVnujs",),
) -> dict[str, Any]:
    """Evaluate provided evidence without inferring authenticity or live QA accuracy.

    The manifest is a *separately produced adapter/handoff contract*; it is
    intentionally not asserted to be the current Upstage QA Sandbox schema.
    """
    issues: list[dict[str, str]] = []

    def fail(code: str, field: str) -> None:
        issues.append({"issue_code": code, "field": field, "severity": "ERROR"})

    def out(status: str, doc: str = "NOT_VERIFIED", python: str = "NOT_VERIFIED") -> dict[str, Any]:
        return {
            "qa_status": status,
            "document_qa_status": doc,
            "python_qa_status": python,
            "release_or_merge_authorized": False,
            "new_studio_run_performed_by_validator": False,
            "studio_live_execution_authenticated": False,
            "issues": issues,
            "protocol_version": HANDOFF_VERSION,
        }

    if not isinstance(manifest, dict):
        fail("INVALID_MANIFEST", "$")
        return out("FAIL")
    if manifest.get("protocol_version") != HANDOFF_VERSION:
        fail("HANDOFF_VERSION_MISMATCH", "protocol_version")
    if manifest.get("producer") != "UPSTAGE_QA_SANDBOX":
        fail("HANDOFF_PRODUCER_MISMATCH", "producer")
    studio = manifest.get("studio")
    verdict = manifest.get("verdict")
    github = manifest.get("github")
    if not all(isinstance(v, dict) for v in (studio, verdict, github)):
        fail("INVALID_HANDOFF_SECTIONS", "$")
        return out("FAIL")

    doc = verdict.get("document_qa_status")
    python = verdict.get("python_qa_status")
    if not isinstance(doc, str) or doc not in DOCUMENT_STATES:
        fail("INVALID_DOCUMENT_QA_STATUS", "verdict.document_qa_status")
        doc = "NOT_VERIFIED"
    if not isinstance(python, str) or python not in PYTHON_STATES:
        fail("INVALID_PYTHON_QA_STATUS", "verdict.python_qa_status")
        python = "NOT_VERIFIED"
    if studio.get("agent_id") != expected_agent_id:
        fail("SANDBOX_AGENT_ID_MISMATCH", "studio.agent_id")
    config_id = studio.get("config_id")
    if not isinstance(config_id, str) or not config_id.startswith("cfg_"):
        fail("UNVERIFIED_CONFIG_ID", "studio.config_id")
    elif expected_config_id is not None and config_id != expected_config_id:
        fail("CONFIG_ID_MISMATCH", "studio.config_id")
    version = studio.get("config_version")
    if type(version) is not int or version < 1:
        fail("INVALID_CONFIG_VERSION", "studio.config_version")
    job = studio.get("job_id")
    step = studio.get("step_run_id")
    if not isinstance(job, str) or not job.startswith("job_"):
        fail("MISSING_JOB_ID", "studio.job_id")
    if not isinstance(step, str) or not step.strip():
        fail("MISSING_STEP_RUN_ID", "studio.step_run_id")
    kind = studio.get("execution_kind")
    if not isinstance(kind, str) or kind not in KINDS:
        fail("INVALID_EXECUTION_KIND", "studio.execution_kind")
    elif kind == "NEW_LIVE_STUDIO" and isinstance(job, str) and job in archived_job_ids:
        fail("ARCHIVED_JOB_REUSED_AS_NEW", "studio.job_id")
    file_ids = studio.get("input_file_ids")
    if (not isinstance(file_ids, list) or not file_ids
            or any(not isinstance(x, str) or not x.startswith("file_") for x in file_ids)
            or len({x for x in file_ids if isinstance(x, str)}) != len(file_ids)):
        fail("INVALID_INPUT_FILE_IDS", "studio.input_file_ids")
    digest = studio.get("native_sha256")
    if not isinstance(digest, str) or HEX64.fullmatch(digest) is None:
        fail("INVALID_NATIVE_DIGEST", "studio.native_sha256")
    report_hash = studio.get("qa_report_sha256")
    if not isinstance(report_hash, str) or HEX64.fullmatch(report_hash) is None:
        fail("INVALID_REPORT_DIGEST", "studio.qa_report_sha256")
    sha = github.get("head_sha")
    if not isinstance(sha, str) or HEX40.fullmatch(sha) is None:
        fail("INVALID_GITHUB_COMMIT", "github.head_sha")
    elif expected_github_sha is not None and sha != expected_github_sha:
        fail("GITHUB_COMMIT_MISMATCH", "github.head_sha")
    if github.get("repository") != "dohun3540-crypto/leadtime-guardian-agent.copy":
        fail("GITHUB_REPOSITORY_MISMATCH", "github.repository")
    if github.get("contract_version") != HANDOFF_VERSION:
        fail("GITHUB_CONTRACT_VERSION_MISMATCH", "github.contract_version")

    feedback = verdict.get("issues")
    if not isinstance(feedback, list):
        fail("INVALID_QA_ISSUES", "verdict.issues")
    else:
        for index, issue in enumerate(feedback):
            field = f"verdict.issues[{index}]"
            if not isinstance(issue, dict) or (
                not isinstance(issue.get("code"), str) or not issue["code"].strip()
                or not isinstance(issue.get("scope"), str) or issue["scope"] not in ISSUE_SCOPES
                or not isinstance(issue.get("severity"), str)
                or issue["severity"] not in SEVERITIES
            ):
                fail("INVALID_QA_ISSUE", field)
                continue
            if issue["scope"] == "document" and issue["severity"] == "ERROR" and doc == "PASS":
                fail("DOCUMENT_FALSE_PASS", field)
            if issue["scope"] == "python" and issue["severity"] == "ERROR" and python == "PASS":
                fail("PYTHON_FALSE_PASS", field)
            if issue["code"] == "EXTERNAL_SAFETY_NOT_VERIFIED" and python == "PASS":
                fail("UNVERIFIED_PYTHON_MARKED_PASS", field)

    report_verified = False
    if report_bytes is not None:
        if not isinstance(report_bytes, bytes):
            fail("INVALID_QA_REPORT_BYTES", "qa_report_bytes")
        elif (not isinstance(report_hash, str)
              or hashlib.sha256(report_bytes).hexdigest() != report_hash.lower()):
            fail("QA_REPORT_HASH_MISMATCH", "studio.qa_report_sha256")
        else:
            try:
                report = load_json_strict(report_bytes)
            except (ValueError, TypeError, UnicodeDecodeError):
                fail("INVALID_QA_REPORT_JSON", "qa_report_bytes")
            else:
                if not isinstance(report, dict):
                    fail("INVALID_QA_REPORT_OBJECT", "qa_report_bytes")
                else:
                    # The external Studio QA schema is not yet observed. A
                    # handoff adapter must explicitly expose these two statuses.
                    required = ("document_qa_status", "python_qa_status")
                    missing = [field for field in required if field not in report]
                    if missing:
                        fail("QA_REPORT_VERDICT_MISSING", "qa_report_bytes")
                    else:
                        report_verified = True
                        for field in required:
                            if report[field] != verdict.get(field):
                                fail("QA_REPORT_VERDICT_MISMATCH", "qa_report_bytes." + field)

    native_verified = False
    if native_bytes is not None:
        if not isinstance(native_bytes, bytes):
            fail("INVALID_NATIVE_BYTES", "native_bytes")
        elif not isinstance(digest, str) or hashlib.sha256(native_bytes).hexdigest() != digest.lower():
            fail("NATIVE_HASH_MISMATCH", "studio.native_sha256")
        else:
            try:
                native = load_json_strict(native_bytes)
            except (ValueError, TypeError, UnicodeDecodeError):
                fail("INVALID_NATIVE_JSON", "native_bytes")
            else:
                result = audit_native_envelope(
                    native, expected_job_id=job if isinstance(job, str) else None,
                    expected_step_run_id=step if isinstance(step, str) else None,
                )
                if result["qa_status"] != "PASS":
                    for issue in result["issues"]:
                        fail("NATIVE_" + issue["issue_code"], "native." + issue["field"])
                else:
                    native_verified = True
                if (isinstance(native, dict) and isinstance(native.get("metadata"), dict)
                        and isinstance(file_ids, list)):
                    source_ids = native["metadata"].get("source_files")
                    if isinstance(source_ids, list):
                        actual = [x.get("file_id") for x in source_ids if isinstance(x, dict)]
                        if (any(not isinstance(x, str) for x in actual)
                                or any(not isinstance(x, str) for x in file_ids)
                                or set(actual) != set(file_ids)):
                            fail("NATIVE_INPUT_FILE_MISMATCH", "studio.input_file_ids")

    if issues:
        return out("FAIL", doc, python)
    if doc in {"FAIL", "NEEDS_REVIEW"} or python == "FAIL":
        return out("FAIL", doc, python)
    if python in {"NOT_RUN", "NOT_VERIFIED", "BLOCKED"}:
        return out("BLOCKED", doc, python)
    # No native bytes: a producer's own digest is not external verification.
    if not native_verified or not report_verified or kind != "NEW_LIVE_STUDIO" or doc != "PASS":
        return out("NOT_VERIFIED", doc, python)
    # Local contract PASS only. This is never a cloud-authenticity/release claim.
    return out("PASS", doc, python)
