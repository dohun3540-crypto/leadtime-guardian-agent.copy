"""합성 입력의 타입 보존 회귀. 실제 Studio 입력 전달이나 PDF 정확도 증거가 아니다."""
from copy import deepcopy

import pytest

from leadtime_guardian.qa.input_delivery import audit_normalize_qa_input


def audit(left, right):
    return audit_normalize_qa_input(
        {"status": "COMPLETED", "output": {"documents": left}},
        {"normalized_documents": right},
    )


@pytest.mark.parametrize(
    ("left", "right"),
    [
        (0, False), (False, 0), (1, True), (100, 100.0), (0, 0.0),
        (100, "100"), (None, "null"), (None, ""), (None, []),
        ({"quantity": 0}, {"quantity": False}),
        ({"items": [{"quantity": 100}]}, {"items": [{"quantity": 100.0}]}),
        ({"quote": None}, {}),
        ({"evidence": [{"confidence": 0}]}, {"evidence": [{"confidence": False}]}),
        ([1, 2], [2, 1]),
        ({1: "value"}, {"1": "value"}),
    ],
)
def test_type_or_structure_changes_are_not_local_matches(left, right):
    result = audit([left], [right])
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MISMATCH"
    assert result["qa_status"] == "FAIL"
    assert result["requires_human_review"] is True
    assert result["actual_cloud_input_authenticated"] is False
    assert result["release_or_merge_authorized"] is False


@pytest.mark.parametrize("value", [100, 0, -1, None, False, "null", "100", "", [],
                                   {"quote": None}, {"evidence": []}, 0.5])
def test_unchanged_values_match_without_authorizing_release(value):
    result = audit([value], [deepcopy(value)])
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MATCH"
    assert result["qa_status"] == "BLOCKED"
    assert result["actual_cloud_input_authenticated"] is False
    assert result["release_or_merge_authorized"] is False


def test_object_key_order_is_not_a_content_change():
    result = audit([{"quantity": 0, "quote": None}], [{"quote": None, "quantity": 0}])
    assert result["input_delivery_status"] == "LOCAL_CONTENT_MATCH"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"),
                                   (1, 2), {1: "value"}])
def test_non_json_values_cannot_be_matches(value):
    assert audit([value], [value])["input_delivery_status"] == "LOCAL_CONTENT_MISMATCH"


def test_comparison_does_not_mutate_evidence():
    left = [{"items": [{"quantity": 0}], "quote": None}]
    right = [{"items": [{"quantity": False}], "quote": None}]
    before_left, before_right = deepcopy(left), deepcopy(right)
    audit(left, right)
    assert left == before_left
    assert right == before_right
    assert type(left[0]["items"][0]["quantity"]) is int
    assert type(right[0]["items"][0]["quantity"]) is bool
