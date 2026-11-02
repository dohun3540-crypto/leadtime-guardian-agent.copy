"""One-command read-only E2E evidence cross-binding; never runs Studio."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from leadtime_guardian.qa.e2e_bundle_preflight import audit_parallel_e2e_bundle


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Local-only E2E bundle joins; never authorizes release."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args()
    result = audit_parallel_e2e_bundle(args.manifest)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if args.json_report is not None:
        try:
            if (args.json_report.resolve(strict=False)
                    == args.manifest.resolve(strict=False)):
                raise FileExistsError("source manifest is not a report path")
            # Exclusive mode: never overwrite the original evidence or results.
            with args.json_report.open("x", encoding="utf-8") as output:
                output.write(rendered + "\n")
        except OSError:
            result["status"] = "FAIL"
            result["release_authorized"] = False
            result["invalid_inputs"].append("json_report")
            result["issues"].append({
                "issue_code": "REPORT_OUTPUT_NOT_WRITABLE",
                "source": "json_report",
            })
            rendered = json.dumps(result, ensure_ascii=False, indent=2,
                                  sort_keys=True)
    print(rendered)
    return 1 if result["status"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
