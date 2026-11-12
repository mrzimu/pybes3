# Documentation translations

The documentation under `docs/` is written in English and is the only source of truth. Translations are gettext catalogs in `docs/locale/<language>/LC_MESSAGES/**/*.po` and are selected at build time:

- Read the Docs sets `READTHEDOCS_LANGUAGE` to the project language (`zh-cn` for the `pybes3-zh-cn` project),
- locally, pass `-D language=zh_CN` to `sphinx-build`.

Untranslated and fuzzy messages fall back to English, so a partially translated catalog still builds and the build is never blocked by a translation in progress.

## Workflow

```bash
source .venv/bin/activate

# 1. regenerate the catalogs after editing anything under docs/
bash dev/update-docs-translations.sh            # default language: zh_CN

# 2. translate the new or fuzzy entries in docs/locale/zh_CN/LC_MESSAGES/
# 3. build both languages
python -m sphinx -b dirhtml -W --keep-going docs build/docs
python -m sphinx -b dirhtml -W --keep-going -D language=zh_CN docs build/docs-zh

# optional: live preview of the Chinese site
sphinx-autobuild docs build/docs-zh -b dirhtml -D language=zh_CN
```

The script also prints the coverage per catalog (`dev/check-docs-translation.py`). It never overwrites existing translations: messages are matched by text and uuid (`gettext_uuid = True`), so moving a paragraph keeps its translation.

Docstrings are not part of the catalogs — `dev/strip-docstring-messages.py` removes autodoc messages, so the API reference pages stay English while the pages around them are translated. Pass additional languages as arguments (`bash dev/update-docs-translations.sh zh_CN ja`) when a new language is added; the same `language` mapping in `docs/conf.py` has to be extended.

## Translating a message

Only edit `msgstr`, never `msgid`.

- Keep the Markdown syntax: inline code in backticks, `**bold**`, `$math$`, `[text](url)` (translate the text, keep the URL), lists and tables.
- Do not translate code blocks, inline code, identifiers, or `:::` directive options (`:link:`, `:sync:`, `:class:`). The directives themselves are not in the catalogs; only their texts (tab labels, card titles, paragraph bodies) are.
- Empty `msgstr` (or `#, fuzzy`) means "show the English text" — use it when a translation would be wrong or is not worth it.
- `sphinx-intl update --no-obsolete` drops entries that no longer exist in the sources; there is nothing to clean up manually.
- CJK headings get generated anchors (`id1`, `id2`, ...) because docutils drops non-ASCII characters. Add an explicit `(zh-...)=` target before a heading when a stable anchor is needed.

## Glossary

Keep these terms consistent; leave the ones marked "keep" in English.

| English | 中文 |
| :-- | :-- |
| gid | 全局 ID（保留 `gid`） |
| digi / raw data | 电子学读出数据 / 原始数据 |
| hit | 击中（保留 `hit`） |
| strip / wire | 条 / 丝 |
| layer / sheet / segment | 层 / 层片 / 段 |
| module / counter | 模块 / 计数器 |
| barrel / endcap | 桶部 / 端盖 |
| sub-detector | 子探测器 |
| crystal / corner point | 晶体 / 角点 |
| charge / time | 电荷 / 时间 |
| helix / pivot | 螺旋线 / pivot 点 |
| geometry table | 几何表 |
| deprecated | 已废弃 |
| ADC, TDC, MC, PDGID | keep |

## 中文说明

`docs/` 下的英文 Markdown 是唯一源文件，中文只写在 `docs/locale/zh_CN/LC_MESSAGES/**/*.po` 里。改完英文文档后先运行 `bash dev/update-docs-translations.sh` 更新目录，再补译新增或标为 `fuzzy` 的条目；未翻译的条目自动显示英文，不会阻塞构建。

翻译时只改 `msgstr`，不改 `msgid`；保留行内代码、粗体、公式与链接地址，不要翻译代码块、标识符以及 `:::` 指令的选项。docstring 不进目录，API 参考页保持英文。术语请与上面的对照表保持一致。

英文源文件与本手册都遵守「一个段落一行」：段落和列表项各占一个物理行，不在句中硬换行，由编辑器自动折行；表格、代码块和 `:::` 指令体保持语法要求的排版。
