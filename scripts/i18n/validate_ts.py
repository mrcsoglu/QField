#!/usr/bin/env python3
"""Validate a Qt TS catalog and emit machine-readable quality metrics."""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

from lxml import etree


INACTIVE_TYPES = {"vanished", "obsolete"}
PLACEHOLDER_RE = re.compile(r"%(?:L?n|L?\d+)")
TAG_RE = re.compile(r"</?(a|b|br|code|em|font|i|li|ol|p|pre|span|strong|u|ul)\b[^>]*>", re.IGNORECASE)
ENGLISH_WORDS = re.compile(
    r"\b(?:the|and|or|is|are|was|were|to|from|with|without|for|of|in|on|at|this|that|failed|successfully|please|select|open|close|save|delete|feature|layer|project|settings|download|upload|error|warning)\b",
    re.IGNORECASE,
)
ALLOW_IDENTICAL = re.compile(
    r"^(?:QField(?:Cloud)?|QGIS|GNSS|GPS|NTRIP|EPSG|WGS ?84|UTM|URL|UUID|ID|X|Y|Z|M|OK|PDF|CSV|GeoPackage|GeoJSON|Bluetooth|NFC|HTTP|HTTPS|[\W\d_]+)$",
    re.IGNORECASE,
)


def text(element: etree._Element) -> str:
    return "".join(element.itertext()).strip()


def active(root: etree._Element):
    for context in root.findall("context"):
        name = context.findtext("name", default="")
        for message in context.findall("message"):
            translation = message.find("translation")
            if translation is None or translation.get("type", "") in INACTIVE_TYPES:
                continue
            yield name, message, translation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    try:
        tree = etree.parse(str(args.catalog))
    except etree.XMLSyntaxError as error:
        print(error, file=sys.stderr)
        return 2

    root = tree.getroot()
    issues: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    source_targets: dict[str, set[str]] = collections.defaultdict(set)
    counts = collections.Counter()
    counts["all_messages"] = len(root.xpath("./context/message"))

    for context, message, translation in active(root):
        counts["active"] += 1
        source = message.findtext("source", default="").strip()
        forms = translation.findall("numerusform")
        targets = [text(form) for form in forms] if forms else [text(translation)]
        target = " | ".join(targets)
        record = {"context": context, "source": source, "translation": target}

        if translation.get("type") == "unfinished":
            counts["unfinished"] += 1
            issues["unfinished"].append(record)
        if not targets or any(not item for item in targets):
            counts["empty"] += 1
            issues["empty"].append(record)
            continue
        counts["translated"] += 1
        if message.get("numerus") == "yes":
            counts["numerus"] += 1
            if not forms:
                issues["numerus"].append(record)

        source_placeholders = collections.Counter(PLACEHOLDER_RE.findall(source))
        for item in targets:
            if collections.Counter(PLACEHOLDER_RE.findall(item)) != source_placeholders:
                issues["placeholders"].append(record)
                break

        source_tags = collections.Counter(TAG_RE.findall(source))
        for item in targets:
            if collections.Counter(TAG_RE.findall(item)) != source_tags:
                issues["markup"].append(record)
                break

        if source == target and not ALLOW_IDENTICAL.fullmatch(source):
            issues["identical"].append(record)
        if ENGLISH_WORDS.search(target):
            issues["english_suspect"].append(record)
        source_targets[source].add(target)

    for source, targets in source_targets.items():
        if len(targets) > 1:
            issues["inconsistent"].append(
                {"context": "*", "source": source, "translation": " || ".join(sorted(targets))}
            )

    counts["inactive"] = counts["all_messages"] - counts["active"]
    report = {
        "catalog": str(args.catalog),
        "language": root.get("language"),
        "counts": dict(counts),
        "issues": dict(issues),
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(rendered + "\n", "utf-8")
    print(json.dumps({"counts": report["counts"], "issue_counts": {k: len(v) for k, v in issues.items()}}, ensure_ascii=False, indent=2))

    fatal = sum(len(issues[key]) for key in ("unfinished", "empty", "placeholders", "markup", "numerus"))
    return 1 if args.strict and fatal else 0


if __name__ == "__main__":
    raise SystemExit(main())

