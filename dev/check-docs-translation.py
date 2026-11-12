"""
Report documentation translation coverage per language.

Usage:
    python dev/check-docs-translation.py [language ...]

Untranslated messages are not an error: Sphinx falls back to the English
source. This script is a progress report, so it exits non-zero only when a
language has no catalog at all or a catalog cannot be read.
"""

from __future__ import annotations

import sys
from pathlib import Path

from babel.messages.pofile import read_po

LOCALE_DIR = Path(__file__).resolve().parents[1] / "docs" / "locale"


def catalog_stats(path: Path) -> tuple[int, int]:
    """
    Return ``(translated, translatable)`` message counts for one catalog.
    """
    with path.open(encoding="utf-8") as file:
        catalog = read_po(file)

    translated = translatable = 0
    for message in catalog:
        # Empty msgid is the catalog header; tuple ids are plural forms.
        if not message.id or isinstance(message.id, tuple):
            continue
        translatable += 1
        if message.string and not message.fuzzy:
            translated += 1
    return translated, translatable


def main(argv: list[str]) -> int:
    languages = argv or ["zh_CN"]
    failed = False

    for language in languages:
        message_dir = LOCALE_DIR / language / "LC_MESSAGES"
        po_files = sorted(message_dir.rglob("*.po"))
        if not po_files:
            print(f"{language}: no catalogs found under {message_dir}")
            failed = True
            continue

        translated = translatable = 0
        incomplete: list[str] = []
        for path in po_files:
            done, total = catalog_stats(path)
            translated += done
            translatable += total
            if done < total:
                name = path.relative_to(message_dir).with_suffix("")
                incomplete.append(f"  {name}: {total - done} untranslated")

        percent = 100.0 * translated / translatable if translatable else 100.0
        print(f"{language}: {translated}/{translatable} messages translated ({percent:.1f}%)")
        if incomplete:
            print("\n".join(incomplete))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
