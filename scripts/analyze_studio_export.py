"""Archive a real Studio export and run the existing engine through the strict boundary."""
import argparse
import hashlib
import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

def main():
    from leadtime_guardian.studio_integration import (
        analyze_studio_documents,
        documents_from_export,
    )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--config-version", required=True)
    parser.add_argument("--prompt-version", required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(args.export, args.output / "studio_original.json")
    base = json.loads(args.base.read_text(encoding="utf-8-sig"))
    schema = json.loads((ROOT / "configs/schemas/document_extraction.schema.json")
                        .read_text(encoding="utf-8"))
    metadata = {"run_id": args.run_id, "config_version": args.config_version,
                "prompt_version": args.prompt_version,
                "processed_at_utc": datetime.now(UTC).isoformat(),
                "export_sha256": hashlib.sha256(args.export.read_bytes()).hexdigest(),
                "studio_provenance": "user-supplied export; verify against native run history",
                "evidence_verified_against_pdf": False}
    try:
        raw = json.loads(args.export.read_text(encoding="utf-8-sig"))
        documents = documents_from_export(raw)
        result = analyze_studio_documents(base, documents, schema)
        (args.output / "normalized_documents.json").write_text(
            json.dumps(documents, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (ValueError, TypeError, KeyError) as exc:
        result = {"status": "NEEDS_REVIEW", "execution_status": "BLOCKED",
                  "needs_review": True, "review_flags": [f"EXPORT:{exc}"],
                  "evidence_verified_against_pdf": False, "external_action_taken": False}
    for name, data in (("analysis.json", result), ("run_metadata.json", metadata)):
        (args.output / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                        encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "OK" else 2


if __name__ == "__main__":
    raise SystemExit(main())
