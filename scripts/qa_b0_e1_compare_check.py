"""No experimental improvement metrics without original B0 AND E1 evidence."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from leadtime_guardian.qa.audit import load_json_strict
from leadtime_guardian.qa.experiment_compare import audit_b0_e1_readiness


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--b0", required=True, type=Path)
    parser.add_argument("--e1", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = audit_b0_e1_readiness(
            load_json_strict(args.b0.read_bytes()),
            load_json_strict(args.e1.read_bytes()),
        )
    except (ValueError, TypeError, UnicodeDecodeError, OSError):
        result = {
            "eligibility": "FAIL",
            "comparison_status": "NOT_MEASURED",
            "issues": [{"issue_code": "UNREADABLE_COMPARISON_INPUT"}],
            "release_or_merge_authorized": False,
        }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["eligibility"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
