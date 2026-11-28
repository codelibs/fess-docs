=================================================
Searching Japanese, English and Chinese Documents
=================================================

Introduction
============

When Japanese meeting minutes, English technical specifications and Chinese market reports sit side by side on the same file server or intranet site, users start to say things like "English documents are found, but Japanese inflected forms don't match", "I want to search only the Chinese documents", or "I want to find material written in English using Japanese words".

Fess can search documents in any language without special configuration.
However, if you add dictionary entries without knowing which language analysis applies where, the results will not change.
This article explains how Fess 15.9 indexes and searches multilingual documents, based on the actual values in its configuration files.
With that understanding, you will be able to:

- Check the language detected for each document, and narrow searches by language with ``lang:``
- Decide which languages' analysis is used at search time, with ``query.default.languages`` and related settings
- Edit dictionaries (synonyms, Kuromoji, stopwords and so on) according to the fields they affect, and apply the changes
- Confirm that a change took effect, using search results and the ``_analyze`` API

How to drive improvements from search logs is covered in :doc:`guide-08`.

How Indexing Works: Common Fields and Language-Specific Fields
==============================================================

In the Fess index, the body text and title are stored in two forms.
They are defined in ``fess_indices/fess.json`` (analyzers) and ``fess_indices/fess/doc.json`` (mappings), both bundled with Fess.

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - Field
     - Analyzer
     - What the analysis does
   * - ``content``, ``title``, ``important_content``
     - ``standard_analyzer`` (``standard_search_analyzer`` at search time)
     - Common to all documents. Kanji, hiragana, katakana and Hangul are split into two-character units (bi-grams), and English stopword removal and stemming are applied. Synonyms are expanded only at search time
   * - ``content_ja``, ``title_ja`` and so on
     - ``japanese_analyzer``
     - Morphological analysis with Kuromoji. Verbs and other words are normalized to their base forms, and particles, auxiliary verbs and symbols are removed
   * - ``content_en``, ``title_en`` and so on
     - ``english_analyzer``
     - English stopword removal and stemming
   * - ``content_zh-cn``, ``title_zh-cn`` and so on
     - ``simplified_chinese_analyzer``
     - Splits text into words with a tokenizer for Chinese
   * - ``content_zh-tw``, ``title_zh-tw`` and so on
     - ``traditional_chinese_analyzer``
     - Converts Traditional Chinese to Simplified Chinese, then splits it with the same tokenizer as Simplified Chinese

Every document has the common fields.
Language-specific fields are created only when the document's language has been determined.
During indexing, the language code is put into the ``lang`` field, and the values of ``content``, ``important_content`` and ``title`` (``indexer.language.fields``) are copied into ``<field>_<language>`` fields such as ``content_ja``.
Each document is assigned only one language.

How a Document's Language Is Determined
---------------------------------------

``lang`` is determined in the following order.

1. For HTML from a web crawl, the value of ``<html lang="...">`` is used (``crawler.document.html.lang.xpath=//HTML/@lang``). Writing ``field.xpath.default.lang=<XPath>`` in the "Config Parameters" of a crawl configuration changes where the value is read from for that configuration only
2. Documents whose language is not determined by step 1 are detected automatically from their text. The first 1000 characters (``indexer.language.detect.length``) of ``content``, ``important_content`` and ``title`` are examined, in that order. For file crawls, the language is detected from the extracted body text only
3. If the detected language is not in ``supported.languages``, or if the language cannot be detected, no ``lang`` is set and no language-specific fields are created

Values such as ``ja-JP`` or ``zh_CN`` are normalized to lowercase with hyphens (``ja``, ``zh-cn``) when stored.

Documents from data stores also go through the same automatic detection at indexing time.
If a script sets ``lang`` to a language listed in ``supported.languages`` (such as ``ja``), that value takes precedence over automatic detection.

How Searching Works: Which Language Fields Are Searched
=======================================================

Search terms are always searched against the common fields.
In addition, for each "search language" determined at each search, the corresponding language-specific fields are added to the query.
The conditions on each field are combined with OR (``should`` in a ``bool`` query), so a document appears in the results if it matches any one of the fields.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Field
     - Configuration key
     - Default value
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<search language>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<search language>``
     - ``query.boost.content.lang``
     - ``0.1``

The search languages are taken from the first of the following that has a value.

1. ``query.default.languages`` in ``fess_config.properties`` (empty by default). If it has a value, all the other settings are ignored
2. The ``lang`` parameter of the request: the language selected in [Options] > "Preferred Language" on the search page or in "Preferred Language" in advanced search, or ``lang`` of ``/api/v2/search``
3. The language in the ``Accept-Language`` header sent by the browser

For example, if you search for 「会議」 ("meeting") in a browser set to Japanese, the search language is ``ja``, and ``content_ja`` is searched in addition to ``content``.
English documents do not have ``content_ja``, so they match only through the bi-grams of the common fields.
Conversely, when a Japanese document also matches in ``title_ja`` or ``content_ja``, its score increases accordingly and it tends to rank higher.
Because Kuromoji normalizes inflected forms to their base forms, searching for 「走った」 ("ran") also matches Japanese documents containing 「走る」 ("run") through ``content_ja``.

For this reason, "Preferred Language" pulls documents in that language toward the top; it is not a filter that excludes documents in other languages.

Narrowing by Language: ``lang:`` Search
=======================================

To narrow results by language, search with the ``lang`` field specified.
``lang`` is a searchable keyword field, so you do not need to create a label for each language.

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

The last example searches for 「会議」 while excluding documents detected as Japanese.
From the API, write the same expression in ``q``, or add ``fields.lang=en`` (which adds a ``lang:"en"`` condition).

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

Documents without ``lang`` (documents whose language could not be detected) do not match any ``lang:`` condition.

Checking the Detected Language
------------------------------

Before changing dictionaries or settings, check which language your documents have been assigned.

1. On the search page, search for ``lang:ja``, ``lang:en``, ``lang:zh-cn`` and ``lang:zh-tw`` in turn, and compare the hit counts. With the API, the count is in ``response.record_count``

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. For an individual document, find it by URL or similar in [System Info] > [Search] of the admin console and open it; the value is shown in the ``lang`` field

If the detection is not what you expect, check the following points.

- The HTML ``<html lang>`` takes precedence over automatic detection. If the site template outputs ``lang="en"`` even on Japanese pages, those pages are treated as English
- Chinese without a region, such as ``<html lang="zh">``, becomes ``zh``. There is no language-specific field with a Chinese analyzer for ``zh``, so Chinese analysis is limited to the bi-grams of the common fields
- Short Japanese documents with many kanji and few kana may be detected as ``zh-cn`` or similar

There are also settings that treat all HTML, or all files, as a single language.
If you set values for ``crawler.document.html.default.lang`` and ``crawler.document.file.default.lang``, neither ``<html lang>`` nor automatic detection is used, and the language is fixed to that value for all crawls in Fess.
In an environment where documents are in mixed languages, leave them empty.

Deciding the Search Languages: ``query.default.languages``
==========================================================

By default, the search language changes with each user's browser language.
For example, when an employee using an English browser searches Japanese documents, ``content_ja`` is not used, so the ranking of results differs from user to user.
To avoid this, fix the search languages with ``query.default.languages``.

::

    query.default.languages=ja,en,zh-cn,zh-tw

In this example, all four language-specific fields are added to the query, no matter who searches in which language.
Each document has only one field for its own language, so documents in every language benefit from language-specific analysis under the same conditions.
In exchange, pulling a specific language to the top with "Preferred Language" no longer has any effect.
If most of your documents are in Japanese, you can also specify a single language, as in ``query.default.languages=ja``.

Write the setting in ``fess_config.properties`` and restart Fess.
The file is located at ``app/WEB-INF/classes/fess_config.properties`` for the ZIP version, and at ``/etc/fess/fess_config.properties`` for the RPM/DEB versions.
With Docker, add it as a JVM option to ``environment`` of ``fess01`` in ``compose.yaml``, and recreate the container.

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS`` is split on spaces, so do not include spaces in the value.
When the container is recreated, settings changed in [System] > [General] are lost along with ``system.properties`` inside the container (:doc:`guide-02`).

How much weight to give matches in language-specific fields can be adjusted with ``query.boost.title.lang`` and ``query.boost.content.lang``.
After changing them, compare the ranking of search results following the steps in "Verifying" below.

Using Dictionaries for Each Language
====================================

Dictionaries are edited in [System] > [Dictionary].
Each dictionary affects specific fields, so unless you choose the dictionary that affects the field you are targeting, the search results will not change.

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - Dictionary (file)
     - Fields affected
     - Use in a multilingual environment
   * - Synonym (``synonym.txt``)
     - ``content``, ``title`` (search time only)
     - Cross-language paraphrases (「会議」 and "meeting") and spelling variations. Does not affect language-specific fields
   * - Kuromoji (``ja/kuromoji.txt``)
     - ``_ja`` fields only
     - Make internal terms and product names be treated as single Japanese words
   * - Stopwords (``ja/stopwords.txt``)
     - ``_ja`` fields only
     - Words that should not be used for searching Japanese documents
   * - Stopwords (``en/stopwords.txt``)
     - ``content``, ``title`` and ``_en`` fields
     - Unneeded English words. Because it affects the common fields, it affects documents in every language
   * - Protwords (``en/protwords.txt``)
     - ``content``, ``title`` and ``_en`` fields
     - English words you do not want stemmed (such as product names)
   * - Stemmer Override (``en/stemmer_override.txt``)
     - ``content``, ``title`` and ``_en`` fields
     - Specify the result of English stemming
   * - Mapping (``mapping.txt``)
     - ``content``, ``title``
     - Character replacement. ``ja/mapping.txt`` is a separate file for the ``_ja`` fields

There is no protected-words (Protwords) dictionary for Japanese.
This is because ``japanese_analyzer`` has no filter that reads protected words.
The Simplified and Traditional Chinese fields have no user dictionary that can be edited from the admin console (their stopwords are ``zh-cn/stopwords.txt`` and ``zh-tw/stopwords.txt``).

Cross-Language Synonyms
-----------------------

To find English documents with Japanese words, register the translations as synonyms.
In the format used for uploading a file, list words with the same meaning on one line, separated by commas.

::

    会議,ミーティング,meeting
    見積,quotation

Synonyms are expanded in the common fields at search time, so no re-crawl is needed.
For registration rules, such as registering hiragana as katakana and full-width alphanumerics as half-width, see `Synonym Dictionary <https://fess.codelibs.org/stable/admin/synonym-guide.html>`__.

Kuromoji User Dictionary
------------------------

In the Kuromoji dictionary, you register a token, its segmented tokens, its reading (in katakana) and its part of speech.
To have an internal term or product name that Kuromoji splits too finely treated as a single word, write the same word for the token and the segmented tokens.

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

This dictionary affects only the ``_ja`` fields.
The common field ``content`` is split into bi-grams, so changing the Kuromoji dictionary does not change matches in ``content``.
The effect appears only in searches whose search languages include ``ja``, and only for documents detected as Japanese.

Applying Dictionary Changes
---------------------------

Saving a dictionary alone does not change the search results.

1. Open [System Info] > [Maintenance] and click [Reload] under "Reload Document Index". The index is closed and reopened, so searches return errors or zero results in the meantime. Run it at a time of low usage
2. Synonyms are used only at search time, so the reload is all that is needed to apply them
3. The other dictionaries (Kuromoji, Mapping, Stopwords, Protwords and Stemmer Override) also change the analysis used when building the index. Documents already in the index remain analyzed with the old dictionary, so re-crawl the affected content

When re-crawling, if "Check Last Modified" in [System] > [General] is enabled (the default), files and pages that have not been updated are not fetched again.
Temporarily disable it, run the crawl, and re-enable it when the crawl finishes.

Verifying
=========

Viewing Token Boundaries with the ``_analyze`` API
--------------------------------------------------

The most reliable way to check whether a dictionary change has taken effect is to use the OpenSearch ``_analyze`` API to run the same string through the analyzers of the common field and the Japanese field, and compare the results.
In the Docker setup from :doc:`guide-02`, OpenSearch can be reached on port 9200 of the host.

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

With ``japanese_analyzer``, the text is split into words, and 「を」 and 「た」 are removed.
With ``standard_analyzer``, it is split into two-character units such as 「全文」, 「文検」 and 「検索」.
After you register 「東京スカイツリー」 in the Kuromoji dictionary and reload, analyzing this word with ``japanese_analyzer`` returns a single token.
A registered synonym can be checked by analyzing 「会議」 with ``"analyzer":"standard_search_analyzer"`` and confirming that a token generated from "meeting" (stemmed to ``meet``) appears.

Checking the Search Results
---------------------------

1. On the search page, search for a word that appears in both Japanese and English documents
2. Switch [Options] > "Preferred Language" between "Japanese" and "English", and confirm that the language of the top documents changes. If you set ``query.default.languages``, confirm that the ranking does not change when you switch
3. After registering translation synonyms and reloading, confirm that ``lang:en 会議`` finds English documents
4. After changing the Kuromoji dictionary and re-crawling, search for the registered word and confirm that Japanese documents containing it are found. Check that the token boundaries themselves have changed with ``_analyze`` as described above

If the results do not change, compare the "Fields affected" column of the dictionary table with the document's ``lang``.
For example, adding a Japanese word of three or more characters to ``en/stopwords.txt`` has no effect, because in the common fields the text becomes two-character tokens and never matches it.

Summary
=======

- Every document can be searched through the common fields (``content``, ``title``), which apply bi-grams and English stemming
- The detected language in ``lang`` and the language-specific fields (such as ``content_ja``) add analysis suited to the language
- The search languages are determined by ``query.default.languages``, the request's ``lang``, and the browser language, in that order, and they pull documents toward the top rather than filtering them
- To narrow by language, specify the ``lang`` field, as in ``lang:en``
- Edit the dictionary that affects the field you are targeting, and apply it by reloading the document index and, if necessary, re-crawling

What to Read Next
=================

- Find improvement points in search logs and fix them with synonyms and key matches: :doc:`guide-08`
- Crawl internal websites and file servers together: :doc:`guide-04`
- Find documents with similar meaning even when the keywords do not match: :doc:`guide-18`
- Call the search API from business systems: :doc:`guide-11`

References
==========

- `Dictionary <https://fess.codelibs.org/stable/admin/dict-guide.html>`__
- `Kuromoji Dictionary <https://fess.codelibs.org/stable/admin/kuromoji-guide.html>`__
- `Synonym Dictionary <https://fess.codelibs.org/stable/admin/synonym-guide.html>`__
- `Stopwords Dictionary <https://fess.codelibs.org/stable/admin/stopwords-guide.html>`__
- `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__
- `Search-Related Settings (Default Search Language) <https://fess.codelibs.org/stable/config/search-advanced.html>`__
- `Advanced Crawler Configuration <https://fess.codelibs.org/stable/config/crawler-advanced.html>`__
- `Field Search <https://fess.codelibs.org/stable/user/search-field.html>`__
- `Search API <https://fess.codelibs.org/stable/api/api-search.html>`__
