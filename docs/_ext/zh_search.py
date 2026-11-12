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

It also replaces the stemmer with an identity one, because the Python side only
lowercases (see ``stem()`` below) and both sides must agree. Sphinx wires the
browser stemmer differently across versions:

- 8.x: ``SearchChinese.js_stemmer_code`` holds an English Porter stemmer, which
  ``get_js_stemmer_code()`` returns whenever ``js_stemmer_rawcode`` is empty.
  Leaving it inherited would stem browser queries (``reading`` -> ``read``)
  against an index that only lowercased them.
- 9.x: ``SearchChinese.js_stemmer_rawcode`` points at the bundled
  ``english-stemmer.js``, and ``get_js_stemmer_code()`` appends
  ``window.Stemmer = ChineseStemmer;`` although that file only defines
  ``EnglishStemmer``. The resulting ``ReferenceError`` aborts the whole
  ``language_data.js`` script, so the splitter below is never installed.

``js_stemmer_code`` therefore defines an identity ``Stemmer`` explicitly and
``js_stemmer_rawcode`` is cleared, which behaves the same on both majors.
"""

from __future__ import annotations

import re

from sphinx.search.zh import SearchChinese

# CJK Unified Ideographs, Extension A and the compatibility block.
_CJK_CHARACTER = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

_JS_STEMMER = r"""
/**
 * Identity stemmer: keep in sync with `stem()` below, which only lowercases.
 */
var Stemmer = function () {
  this.stemWord = function (w) {
    return w;
  };
};
"""

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

    # Both must be set: an empty ``js_stemmer_rawcode`` alone falls back to the
    # inherited ``js_stemmer_code``, which is the English Porter stemmer on
    # Sphinx 8.x (see the module docstring).
    js_stemmer_rawcode = ""
    js_stemmer_code = _JS_STEMMER

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
