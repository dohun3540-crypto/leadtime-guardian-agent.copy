"""One-command read-only evidence inventory; never changes original files."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from leadtime_guardian.qa.release_inventory import audit_release_folder, render_markdown


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--json-report", type=Path)
    parser.add_argument("--markdown-report", type=Path)
    args = parser.parse_args()
    result = audit_release_folder(args.manifest)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        if args.json_report is not None:
            with args.json_report.open("x", encoding="utf-8") as output:
                output.write(rendered)
        if args.markdown_report is not None:
            with args.markdown_report.open("x", encoding="utf-8") as output:
                output.write(render_markdown(result))
    except OSError:
        result["status"] = "FAIL"
        result["release_authorized"] = False
        result["blocking_issues"].append({
            "issue_code": "REPORT_OUTPUT_NOT_WRITABLE", "source": "cli",
        })
        rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    return 1 if result["status"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
