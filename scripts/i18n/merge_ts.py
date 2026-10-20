#!/usr/bin/env python3
"""Merge Qt TS catalogs without collapsing context-sensitive messages."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from xml.etree import ElementTree as ET


INACTIVE = {"vanished", "obsolete"}


def message_key(context: str, message: ET.Element) -> tuple[str, str, str, bool]:
    return (
        context,
        message.findtext("source", ""),
        message.findtext("comment", ""),
        message.get("numerus") == "yes",
    )


def active(message: ET.Element) -> bool:
    translation = message.find("translation")
    return translation is not None and translation.get("type", "") not in INACTIVE


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary", type=Path, help="Catalog whose entries win on duplicate keys")
    parser.add_argument("additional", type=Path, nargs="+", help="Catalogs to append")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    tree = ET.parse(args.primary)
    root = tree.getroot()
    contexts = {context.findtext("name", ""): context for context in root.findall("context")}
    keys = {
        message_key(context.findtext("name", ""), message)
        for context in root.findall("context")
        for message in context.findall("message")
        if active(message)
    }

    added = 0
    duplicates = 0
    for catalog in args.additional:
        extra_root = ET.parse(catalog).getroot()
        for extra_context in extra_root.findall("context"):
            name = extra_context.findtext("name", "")
            destination = contexts.get(name)
            if destination is None:
                destination = ET.SubElement(root, "context")
                ET.SubElement(destination, "name").text = name
                contexts[name] = destination
            for message in extra_context.findall("message"):
                if not active(message):
                    continue
                key = message_key(name, message)
                if key in keys:
                    duplicates += 1
                    continue
                destination.append(copy.deepcopy(message))
                keys.add(key)
                added += 1

    root.set("language", "tr_TR")
    ET.indent(tree, space="    ")
    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(xml.replace(b"?>", b"?>\n<!DOCTYPE TS>", 1) + b"\n")
    print(f"Merged {len(keys)} active messages ({added} added, {duplicates} duplicates kept from primary)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

