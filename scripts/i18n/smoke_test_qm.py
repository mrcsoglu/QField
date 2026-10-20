#!/usr/bin/env python3
"""Load the compiled catalog through Qt and verify representative lookups."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QLocale, QTranslator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("qm", type=Path)
    args = parser.parse_args()

    QLocale.setDefault(QLocale("tr_TR"))
    app = QCoreApplication(sys.argv[:1])
    translator = QTranslator()
    loaded = translator.load(str(args.qm.resolve()))
    app.installTranslator(translator)
    cases = [
        ("QfAppSettings", "Map Canvas", -1, "Harita Tuvali"),
        ("QfAppSettings", "Port", -1, "Port"),
        ("QObject", "Buffer", -1, "Tampon bölge oluştur"),
        ("QObject", "Translate", -1, "Geometrileri ötele"),
        ("QObject", "Dissolve result", -1, "Ortak sınırları kaldırarak birleştir"),
        ("QObject", "Field calculator", -1, "Alan hesaplayıcı"),
        ("QFieldCloudService", "%n file(s) remaining", 2, "2 dosya kaldı"),
    ]
    results = []
    passed = loaded
    for context, source, number, expected in cases:
        actual = QCoreApplication.translate(context, source, None, number)
        ok = actual == expected
        passed = passed and ok
        results.append({"context": context, "source": source, "expected": expected, "actual": actual, "passed": ok})
    print(json.dumps({"loaded": loaded, "cases": results, "passed": passed}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

