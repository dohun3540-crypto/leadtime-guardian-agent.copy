"""Normalize Studio-extracted delivery notice dates onto uniquely matched CSV receipts."""
from copy import deepcopy
from datetime import date


class AdapterError(ValueError):
    """A document cannot be safely mapped to trusted inventory records."""


def apply_studio_extractions(base_case, predictions):
    """Input must be actual normalized Studio predictions, never gold labels."""
    if not isinstance(predictions, list):
        raise AdapterError("predictions: expected list")
    case = deepcopy(base_case)
    case["documents"] = deepcopy(predictions)
    for doc in predictions:
        if not isinstance(doc, dict):
            raise AdapterError("prediction: expected object")
        if doc.get("document_type") != "delivery_notice":
            continue
        eta = doc.get("revised_delivery")
        try:
            if not isinstance(eta, str) or date.fromisoformat(eta).isoformat() != eta:
                raise ValueError("bad date")
        except ValueError as exc:
            raise AdapterError("delivery_notice: revised_delivery missing/invalid") from exc
        items = doc.get("items")
        if not isinstance(items, list) or not items:
            raise AdapterError("delivery_notice: items missing")
        for item in items:
            if not isinstance(item, dict):
                raise AdapterError("delivery_notice: item malformed")
            matches = [
                row for row in case["inbound"]
                if row.get("po_id") == doc.get("po_id")
                and row.get("product_id") == item.get("product_id")
                and (not item.get("receipt_id")
                     or row.get("receipt_id") == item.get("receipt_id"))
            ]
            if len(matches) != 1:
                raise AdapterError(f"ambiguous/unknown receipt: {doc.get('document_id')}")
            matches[0]["eta"] = eta
    return case
