"""Inspect literal 49 in an XLSX export and separate raw stage JSON values.

No workbook mutation, OCR, Excel formula evaluation, or causal inference.
Uses OOXML ZIP/XML directly to preserve original cell types without Excel APIs.
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from decimal import Decimal, InvalidOperation
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from leadtime_guardian.qa.audit import load_json_strict

XML = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def classify(value, kind):
    if value is None:
        return "BLANK"
    if kind in ("s", "str", "inlineStr"):
        return "STRING_49" if value == "49" else "OTHER_STRING"
    if kind == "b":
        return "BOOLEAN"
    if kind in ("n", None):
        try:
            return "NUMBER_49" if Decimal(value) == 49 else "OTHER_NUMBER"
        except (InvalidOperation, TypeError):
            return "INVALID_NUMBER"
    return "OTHER"


def inspect_workbook(data):
    sheets = []
    with zipfile.ZipFile(BytesIO(data)) as archive:
        names = sorted(x for x in archive.namelist()
                       if x.startswith("xl/worksheets/sheet") and x.endswith(".xml"))
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            xml = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.iter(XML + "t"))
                      for si in xml.iter(XML + "si")]
        for sheet in names:
            matches = []
            coordinate_values = {}
            root = ET.fromstring(archive.read(sheet))
            for cell in root.iter(XML + "c"):
                kind = cell.get("t", "n")
                node = cell.find(XML + "v")
                raw = node.text if node is not None else None
                if kind == "s":
                    if raw is None or not raw.isdigit() or int(raw) >= len(shared):
                        raise ValueError("malformed shared string reference")
                    value = shared[int(raw)]
                elif kind == "inlineStr":
                    inline = cell.find(XML + "is")
                    value = "".join(t.text or "" for t in inline.iter(XML + "t")) if inline is not None else None
                else:
                    value = raw
                coordinate = cell.get("r")
                if coordinate:
                    coordinate_values[coordinate] = value
                category = classify(value, kind)
                formula = cell.find(XML + "f")
                has_formula = formula is not None
                # A formula's cached 49 is not a literal source value.
                if category in ("NUMBER_49", "STRING_49"):
                    matches.append({"cell": cell.get("r"), "raw_cell_type": kind,
                                    "raw_v": raw, "value": value,
                                    "has_formula": has_formula,
                                    "formula_expression": (
                                        formula.text if has_formula else None
                                    ),
                                    "match_type": (
                                        "FORMULA_CACHED_49" if has_formula else category
                                    )})
            # The first row is only a candidate header; do not infer an
            # authoritative Studio JSON mapping without a real export schema.
            for match in matches:
                coordinate = match["cell"] or ""
                letters = "".join(ch for ch in coordinate if ch.isalpha())
                match["column_header_row1_candidate"] = (
                    coordinate_values.get(letters + "1") if letters else None
                )
                match["json_field_mapping_verified"] = False
                # The actual table header can start lower than row 1. Expose
                # candidate cells only; never assume they map to Studio JSON.
                coordinate_parts = re.fullmatch(r"([A-Z]+)([1-9][0-9]*)", coordinate)
                near = {}
                above = []
                if coordinate_parts:
                    col, row = coordinate_parts.group(1), int(coordinate_parts.group(2))
                    col_number = sum((ord(ch) - 64) * (26 ** pos)
                                     for pos, ch in enumerate(reversed(col)))
                    for other_coordinate, other_value in coordinate_values.items():
                        other = re.fullmatch(r"([A-Z]+)([1-9][0-9]*)", other_coordinate)
                        if other is None:
                            continue
                        other_col, other_row = other.group(1), int(other.group(2))
                        other_col_number = sum((ord(ch) - 64) * (26 ** pos)
                                               for pos, ch in enumerate(reversed(other_col)))
                        if (other_row == row and other_coordinate != coordinate
                                and abs(other_col_number - col_number) <= 2):
                            near[other_coordinate] = other_value
                        if other_col == col and other_row < row and other_value is not None:
                            above.append({"cell": other_coordinate, "value": other_value})
                match["same_row_context_unverified"] = near
                match["potential_header_cells_above"] = sorted(
                    above, key=lambda item: int(re.search(r"[0-9]+$", item["cell"]).group()),
                    reverse=True,
                )[:3]
            sheets.append({"worksheet_xml": sheet, "matches": matches})
    return sheets


def stage_matches(value, trail="$"):
    found = []
    if isinstance(value, dict):
        for key, member in value.items():
            found.extend(stage_matches(member, trail + "." + key))
    elif isinstance(value, list):
        for index, member in enumerate(value):
            found.extend(stage_matches(member, f"{trail}[{index}]"))
    elif isinstance(value, str) and value == "49":
        found.append({"json_path": trail, "match_type": "STRING_49"})
    elif type(value) in (int, float) and value == 49:
        found.append({"json_path": trail, "match_type": "NUMBER_49"})
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xlsx", required=True, type=Path)
    parser.add_argument("--extract-json", type=Path)
    parser.add_argument("--merge-json", type=Path)
    parser.add_argument("--normalize-json", type=Path)
    args = parser.parse_args()
    try:
        raw = args.xlsx.read_bytes()
        sheets = inspect_workbook(raw)
        matches = []
        for sheet in sheets:
            for item in sheet["matches"]:
                matches.append({"worksheet_xml": sheet["worksheet_xml"], **item})
        stages = {}
        for name, path in (
            ("Extract", args.extract_json),
            ("Merge", args.merge_json),
            ("NormalizeDocuments", args.normalize_json),
        ):
            if path is None:
                stages[name] = {"status": "NOT_PROVIDED", "matches": []}
            else:
                content = path.read_bytes()
                parsed = load_json_strict(content)
                stages[name] = {"status": "EXAMINED_LOCAL_BYTES",
                                "sha256": hashlib.sha256(content).hexdigest(),
                                "matches": stage_matches(parsed)}
        result = {
            "qa_status": "NOT_VERIFIED",
            "xlsx_sha256": hashlib.sha256(raw).hexdigest(),
            "xlsx_49_count": len(matches),
            "xlsx_matches": matches,
            "stage_evidence": stages,
            "causal_origin": "UNKNOWN",
            "source_pdf_verified": False,
            "original_files_modified": False,
        }
    except (OSError, ValueError, TypeError, ET.ParseError, zipfile.BadZipFile) as exc:
        result = {"qa_status": "FAIL", "reason": type(exc).__name__,
                  "original_files_modified": False}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["qa_status"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
