"""Seeded metamorphic/adversarial checks, never evidence of a new Studio run."""
import hashlib
import json
import random
import zipfile
from copy import deepcopy
from pathlib import Path

from test_qa_provenance_link import fixture as receipt_fixture
from test_qa_stage_trace import JOB, TYPES, evidence

from leadtime_guardian.qa.input_delivery import audit_normalize_qa_input
from leadtime_guardian.qa.provenance_link import audit_team2_provenance_link
from leadtime_guardian.qa.stage_trace import audit_stage_evidence
from leadtime_guardian.studio_integration import analyze_studio_documents, documents_from_export

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261103
ARCHIVE = ROOT / "data/results/studio_runs/C001_20261030_v4"


def bind(raw, manifest, stage, value):
    data = json.dumps(value, ensure_ascii=False).encode()
    raw[stage] = data
    manifest["stages"][stage]["sha256"] = hashlib.sha256(data).hexdigest()


def test_seeded_document_permutations_preserve_local_join_and_determinism():
    rng = random.Random(SEED)
    for _ in range(24):
        manifest, raw = evidence()
        for stage in ("Extract", "MergeDocuments", "NormalizeDocuments", "IndependentQA_Input"):
            value = json.loads(raw[stage])
            key = "normalized_documents" if stage == "IndependentQA_Input" else "documents"
            rng.shuffle(value[key])
            bind(raw, manifest, stage, value)
        original = deepcopy((manifest, raw))
        first = audit_stage_evidence(manifest, raw)
        assert first == audit_stage_evidence(manifest, raw)
        assert first["status"] == "BLOCKED"
        assert first["normalize_qa_input_status"] == "LOCAL_CONTENT_MATCH"
        assert first["all_expected_raw_stages_present"] is True
        assert first["release_or_merge_authorized"] is False
        assert (manifest, raw) == original


def test_identity_conflicts_survive_no_documented_wrapper_depth():
    conflicts = [("job_execution_id", "job_other"), ("step_run_id", "step_other"),
                 ("config_id", "cfg_other"), ("config_version", True)]
    for field, bad in conflicts:
        for container in ("root", "metadata", "additional_values"):
            for depth in range(3):
                manifest, raw = evidence()
                value = json.loads(raw["NormalizeDocuments"])
                if container == "root":
                    value[field] = bad
                else:
                    value[container] = {field: bad}
                for _ in range(depth):
                    value = {"output": {"content": json.dumps(value)}}
                bind(raw, manifest, "NormalizeDocuments", value)
                result = audit_stage_evidence(manifest, raw)
                assert result["status"] == "FAIL", (field, container, depth)
                assert result["all_expected_raw_stages_present"] is False


def test_real_original_extract_zip_bytes_remain_unmodified_and_not_gold():
    archive = ARCHIVE / "extractions_native.zip"
    original_sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    manifest, _ = evidence()
    branches, bindings = {}, {}
    with zipfile.ZipFile(archive) as source:
        for name in source.namelist():
            if not name.endswith(".json"):
                continue
            payload = source.read(name)
            kind = json.loads(payload)["document_type"]
            branches[kind] = payload
            bindings[kind] = {
                "sha256": hashlib.sha256(payload).hexdigest(), "case_id": "C001",
                "job_id": JOB, "config_id": "cfg_SYNTH", "config_version": 1,
                "step_run_id": "SYNTHETIC_LOCAL_SHAPE_BINDING_" + kind,
            }
    assert set(branches) == set(TYPES)
    # These are local shape-test bindings, not fabricated provider Step IDs.
    manifest["stages"] = {"Extract": {"branches": bindings}}
    before = deepcopy(branches)
    result = audit_stage_evidence(manifest, {"Extract": branches})
    assert result["status"] == "BLOCKED"
    assert result["stages"]["Extract"]["document_count"] == 3
    assert result["all_expected_raw_stages_present"] is False
    assert result["studio_live_execution_authenticated"] is False
    assert branches == before
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == original_sha


def test_file_id_adversaries_fail_in_both_manifest_and_receipt_without_exception(tmp_path):
    malformed = [None, 0, False, {}, [], ["file_QA"], "", "wrong", "file_", "file_  "]
    for bad in malformed:
        args = list(receipt_fixture(tmp_path))
        args[0]["studio"]["input_file_ids"] = [bad]
        assert audit_team2_provenance_link(*args, pdf_root=tmp_path)["qa_status"] == "FAIL"
        args = list(receipt_fixture(tmp_path))
        args[2]["files"][0]["file_id"] = bad
        result = audit_team2_provenance_link(*args, pdf_root=tmp_path)
        assert result["qa_status"] == "FAIL"
        assert result["cross_agent_release_authorized"] is False
    args = list(receipt_fixture(tmp_path))
    args[0]["studio"]["input_file_ids"] = ["file_QA", "file_QA"]
    assert audit_team2_provenance_link(*args, pdf_root=tmp_path)["qa_status"] == "FAIL"


def test_boundary_mutations_block_without_changing_reference_data():
    native = json.loads((ARCHIVE / "instruct_original.json").read_text())
    original = documents_from_export(native)
    base = json.loads((ROOT / "data/cases/SYN-C001/trusted_base_case.json").read_text())
    schema = json.loads((ROOT / "configs/schemas/document_extraction.schema.json").read_text())
    baseline = deepcopy((base, original))
    variants = []
    for quantity in (-1, 0, False, None, "0"):
        docs = deepcopy(original)
        po = next(d for d in docs if d["document_type"] == "purchase_order")
        po["items"][0]["quantity"] = quantity
        variants.append(docs)
    for field, value in (("unit_price", None), ("shipping_cost", None),
                         ("arrival_date", "2026-02-30")):
        docs = deepcopy(original)
        next(d for d in docs if d["document_type"] == "quotation")["quote"][field] = value
        variants.append(docs)
    docs = deepcopy(original)
    po = next(d for d in docs if d["document_type"] == "purchase_order")
    po["items"].append(deepcopy(po["items"][0]))
    variants.append(docs)
    for docs in variants:
        result = analyze_studio_documents(base, docs, schema)
        assert result["execution_status"] == "BLOCKED"
        assert result["estimated_quote_cost_krw"] is None
        assert result["external_action_taken"] is False
    assert (base, original) == baseline


def test_missing_qa_input_blocks_evidence_while_valid_calculation_is_available():
    native = json.loads((ARCHIVE / "instruct_original.json").read_text())
    documents = documents_from_export(native)
    result = audit_normalize_qa_input({"status": "completed", "documents": documents})
    assert result["qa_status"] == "BLOCKED"
    assert result["actual_cloud_input_authenticated"] is False
    assert result["release_or_merge_authorized"] is False
