#!/usr/bin/env bash
# Regenerate the documentation translation catalogs from the English sources.
#
# Usage: dev/update-docs-translations.sh [language ...]   (default: zh_CN)
#
# Run this after adding or editing anything under docs/. Then translate the new
# and fuzzy entries in docs/locale/<language>/LC_MESSAGES/**/*.po - see
# docs/locale/README.md. Untranslated entries fall back to English, so the
# documentation keeps building while a translation is in progress.
set -euo pipefail

cd "$(dirname "$0")/.."
# shellcheck source=/dev/null
source .venv/bin/activate

languages=("$@")
if [[ ${#languages[@]} -eq 0 ]]; then
    languages=(zh_CN)
fi

rm -rf build/gettext
python -m sphinx -b gettext docs build/gettext
# Docstrings are English-only source text; keep them out of the catalogs.
python dev/strip-docstring-messages.py build/gettext

for lang in "${languages[@]}"; do
    sphinx-intl update -p build/gettext -l "${lang}" -d docs/locale --no-obsolete
done

python dev/check-docs-translation.py "${languages[@]}"
