"""Local source coexistence only: no Studio execution or Gold approval."""
import json
from pathlib import Path

from leadtime_guardian.qa import audit_case as independent_qa
from qa.inventory import manifest_entries, strict_json
from qa.review_records import inspect_records
from qa.xlsx_snapshot import encode_value

ROOT = Path(__file__).resolve().parents[1]


def test_separate_qa_packages_remain_importable():
    assert callable(independent_qa)
    assert callable(strict_json)
    assert callable(inspect_records)
    assert encode_value(100)["python_type"] == "int"


def test_member3_manifest_covers_twenty_cases_and_sixty_documents():
    rows = manifest_entries(ROOT)
    assert len(rows) == 60
    assert len({case_id for case_id, _, _, _ in rows}) == 20


def test_unapproved_candidate_cannot_be_used_as_official_gold():
    candidate = json.loads(
        (ROOT / "qa/gold_candidates/SYN-C001/candidate.v1.json").read_text(encoding="utf-8")
    )
    assert candidate["label_status"] == "AI_CANDIDATE"
    assert candidate["human_reviewed"] is False
    assert candidate["team_approved"] is False
    assert candidate["gold_frozen"] is False
    assert candidate["eligible_for_official_metrics"] is False
