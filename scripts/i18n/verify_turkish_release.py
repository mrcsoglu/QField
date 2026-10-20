#!/usr/bin/env python3
"""Verify source coverage, compiled QM files, and the app-wide plugin ZIP."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path

from lxml import etree


INACTIVE = {"vanished", "obsolete"}
QM_MAGIC = bytes.fromhex("3cb86418caef9c95cd211cbf60a1bddd")


def inventory(path: Path) -> set[tuple[str, str, str, bool]]:
    root = etree.parse(str(path)).getroot()
    result = set()
    for context in root.findall("context"):
        name = context.findtext("name", default="")
        for message in context.findall("message"):
            translation = message.find("translation")
            if translation is not None and translation.get("type", "") in INACTIVE:
                continue
            result.add(
                (
                    name,
                    message.findtext("source", default=""),
                    message.findtext("comment", default=""),
                    message.get("numerus") == "yes",
                )
            )
    return result


def qm_valid(path: Path) -> bool:
    return path.is_file() and path.read_bytes().startswith(QM_MAGIC)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-catalog", type=Path, required=True)
    parser.add_argument("--core-source-inventory", type=Path, required=True)
    parser.add_argument("--processing-catalog", type=Path, required=True)
    parser.add_argument("--processing-source-inventory", type=Path, required=True)
    parser.add_argument("--merged-catalog", type=Path, required=True)
    parser.add_argument("--core-qm", type=Path, required=True)
    parser.add_argument("--zip", dest="zip_path", type=Path, required=True)
    args = parser.parse_args()

    core = inventory(args.core_catalog)
    core_source = inventory(args.core_source_inventory)
    processing = inventory(args.processing_catalog)
    processing_source = inventory(args.processing_source_inventory)
    merged = inventory(args.merged_catalog)
    expected_merged = core | processing

    with zipfile.ZipFile(args.zip_path) as archive:
        names = set(archive.namelist())
        required = {"main.qml", "metadata.txt", "main_tr.qm", "main_tr_TR.qm", "main_tr.ts", "README_TR.md"}
        zip_qm_valid = {
            name: archive.read(name).startswith(QM_MAGIC)
            for name in ("main_tr.qm", "main_tr_TR.qm")
            if name in names
        }

    report = {
        "core_catalog_active": len(core),
        "core_source_inventory": len(core_source),
        "core_missing": len(core_source - core),
        "core_extra": len(core - core_source),
        "processing_catalog_active": len(processing),
        "processing_source_inventory": len(processing_source),
        "processing_missing": len(processing_source - processing),
        "processing_extra": len(processing - processing_source),
        "merged_catalog_active": len(merged),
        "merged_expected": len(expected_merged),
        "merged_missing": len(expected_merged - merged),
        "merged_extra": len(merged - expected_merged),
        "core_qm_magic_valid": qm_valid(args.core_qm),
        "zip_root_main_qml": "main.qml" in names,
        "zip_missing_entries": sorted(required - names),
        "zip_qm_magic_valid": zip_qm_valid,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    passed = (
        report["core_missing"] == 0
        and report["core_extra"] == 0
        and report["processing_missing"] == 0
        and report["processing_extra"] == 0
        and report["merged_missing"] == 0
        and report["merged_extra"] == 0
        and report["core_qm_magic_valid"]
        and report["zip_root_main_qml"]
        and not report["zip_missing_entries"]
        and len(zip_qm_valid) == 2
        and all(zip_qm_valid.values())
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

