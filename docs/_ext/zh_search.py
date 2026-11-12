"""
Chinese search language with a client-side query splitter.

Sphinx's built-in ``SearchChinese`` segments the *index* with jieba but ships no
``js_splitter_code``, so the browser's ``splitQuery`` falls back to splitting on
whitespace: a Chinese query typed without spaces becomes a single term, which
never matches the jieba words stored in the index.

This subclass keeps the jieba segmentation for the index, additionally indexes
every single CJK character, and splits queries in the browser with a greedy
longest match over the terms that are actually in the index. That reproduces
jieba's word boundaries without shipping a dictionary to the browser, and falls
back to individual characters (always indexed) when nothing longer matches.

It also drops the English stemmer. Sphinx appends
``window.Stemmer = ChineseStemmer;`` to the bundled English stemmer for Chinese
(`sphinx/search/__init__.py`, ``get_js_stemmer_code``), but the bundled file only
defines ``EnglishStemmer``. That ``ReferenceError`` aborts the whole
``language_data.js`` script, so no splitter is ever installed. With the stemmer
disabled, both the index (Python) and the browser only lowercase the terms, which
keeps them consistent.
"""

from __future__ import annotations

import re

from sphinx.search.zh import SearchChinese

# CJK Unified Ideographs, Extension A and the compatibility block.
_CJK_CHARACTER = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

_JS_SPLITTER = r"""
/**
 * Split a query into terms: greedy longest match over the search index
 * vocabulary, falling back to the individual CJK characters (always indexed).
 */
var splitQuery = function (query) {
  const cjk = /[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]/;
  const wordChar = /[a-zA-Z0-9_]/;
  let vocab = null;
  try {
    if (typeof Search !== "undefined" && Search._index) {
      vocab = Search._index.terms || null;
    }
  } catch (e) {
    vocab = null; // the index is not loaded yet: split into characters only
  }
  const known = (term) =>
    vocab !== null && Object.prototype.hasOwnProperty.call(vocab, term);

  const terms = [];
  let latin = "";
  const flushLatin = () => {
    if (latin) {
      terms.push(latin);
      latin = "";
    }
  };

  let i = 0;
  while (i < query.length) {
    const ch = query[i];
    if (cjk.test(ch)) {
      flushLatin();
      let best = 1;
      const limit = Math.min(8, query.length - i);
      for (let size = 2; size <= limit; size++) {
        if (!cjk.test(query[i + size - 1])) break;
        if (known(query.slice(i, i + size))) best = size;
      }
      terms.push(query.slice(i, i + best));
      i += best;
    } else if (wordChar.test(ch)) {
      latin += ch;
      i += 1;
    } else {
      flushLatin();
      i += 1;
    }
  }
  flushLatin();
  return terms;
};
"""


class SearchChineseWithSplitter(SearchChinese):
    """
    jieba index plus single characters, with a matching browser splitter.
    """

    js_splitter_code = _JS_SPLITTER

    # Fall back to the identity stemmer shipped by ``SearchLanguage`` rather
    # than the English one, whose generated alias is broken for Chinese (see
    # the module docstring). ``stem()`` below keeps index and query in sync.
    js_stemmer_rawcode = ""

    def split(self, input: str) -> list[str]:
        words = super().split(input)
        return words + _CJK_CHARACTER.findall(input)

    def stem(self, word: str) -> str:
        # No stemming: the browser cannot reuse the Python snowball results, and
        # search identifiers in these docs are matched verbatim.
        return word.lower()

    def word_filter(self, word: str) -> bool:
        # Single CJK characters are indexed: the browser splitter queries them
        # wherever no multi-character term covers a position.
        if len(word) > 1:
            return True
        return _CJK_CHARACTER.fullmatch(word) is not None
