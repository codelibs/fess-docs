===========================================================================
Part 9: Search Infrastructure for Multilingual Organizations -- Building an Environment to Properly Search Documents in Japanese, English, and Chinese
===========================================================================

Introduction
============

In companies that operate globally or organizations with employees of various nationalities, internal documents are created in multiple languages.
A search infrastructure that can properly handle documents in mixed languages -- such as Japanese meeting minutes, English technical specifications, and Chinese market reports -- is essential.

In this article, we assume an environment where documents in Japanese, English, and Chinese coexist, and build an environment that can correctly search documents in each language.

Target Audience
===============

- Administrators of organizations that handle multilingual documents
- Those who want to improve search quality for languages other than Japanese
- Those who want to learn the basics of full-text search Analyzers

Scenario
========

We assume a company with offices in Japan, the United States, and China.

- Japan office: Creates Japanese documents (specifications, meeting minutes, reports)
- US office: Creates English documents (technical documents, presentation materials)
- China office: Creates Chinese documents (market research, business partner information)
- Common: Global policy documents written in English

The goal is to create an environment where employees at each office can search for documents regardless of language.

Fundamentals of Multilingual Search
=====================================

Language Processing in Full-Text Search
----------------------------------------

For a full-text search engine to make documents searchable, it needs to split text into "tokens" (searchable units).
This process is called "tokenization."

The tokenization method differs significantly depending on the language.

**English**: Words separated by spaces become tokens directly.
Additionally, stemming (e.g., running -> run) and lowercasing are applied.

**Japanese**: Since words are not separated by spaces, a morphological analyzer (such as Kuromoji) is used to split text into words.
For example, a phrase is split like this: "full-text search server" -> "full-text" "search" "server."

**Chinese**: Like Japanese, words are not separated by spaces, so a dedicated tokenizer is required. Fess uses its own Chinese tokenizer for processing.

Fess Multilingual Support
---------------------------

Fess uses OpenSearch as its backend and can leverage the multilingual Analyzers provided by OpenSearch.
In Fess's default configuration, the Japanese (Kuromoji) Analyzer is enabled, but other languages are also supported.

Fess has index settings supporting over 20 languages, with a feature that automatically detects the language of a document and applies the appropriate Analyzer.

Language-Specific Settings
===========================

Japanese Settings
------------------

Japanese documents are processed by the Kuromoji Analyzer.
Since Japanese is properly handled by Fess's default settings, no special additional configuration is required.

However, search quality can be improved with the following customizations.

**User Dictionary**

Register industry-specific terms and internal terminology in the dictionary.
This can be configured by selecting the Kuromoji dictionary from [System] > [Dictionary] in the admin console.

For example, this is useful when you want a compound term to be treated as a single token rather than being split into separate words.

**Synonyms**

Handle spelling variations specific to Japanese.

::

    サーバー,サーバ
    データベース,DB,ディービー
    ユーザー,ユーザ,利用者

English Settings
-----------------

English documents are automatically processed with the appropriate Analyzer through Fess's multilingual index.

English-specific customizations include the following.

**Stop Words**

Common English stop words (the, a, an, is, are, etc.) are excluded by default, but industry-specific stop words can also be added.

**Stemmer Override**

Override the stemming of specific words.
This can be configured by selecting the Stemmer Override dictionary from [System] > [Dictionary] in the admin console.

For example, this is used when technical terms undergo unintended transformations.

Chinese Settings
-----------------

Chinese documents use Fess's own Chinese tokenizer.
In Fess's multilingual index, both Simplified and Traditional Chinese text are properly tokenized.

Chinese-specific considerations include the following.

- Mapping between Simplified and Traditional Chinese characters
- Search support via Pinyin input
- Chinese-specific synonym settings

Search Experience in a Multilingual Environment
=================================================

Search UI Considerations
-------------------------

In a multilingual environment, the search UI also needs to match the user's language.

Fess has a feature that automatically switches the UI language based on the browser's language settings.
The search screen UI is provided in multiple languages, including Japanese, English, and Chinese.

Cross-Language Search Considerations
-------------------------------------

There is also a need for cross-language search, such as "finding English documents using Japanese keywords."
At present, Fess alone does not support fully automatic translation-based search, but the following methods can partially address this need.

**Multilingual Synonym Settings**

Register translations between Japanese and English as synonyms.

::

    会議,meeting,ミーティング
    報告書,report,レポート
    仕様書,specification,スペック

This allows a search for "meeting" in Japanese to also return English documents containing "meeting."

**Language Filtering with Labels**

Set up labels for each language so that users can select the language scope of their search.

- ``lang-ja``: Japanese documents
- ``lang-en``: English documents
- ``lang-zh``: Chinese documents

Dictionary Management Best Practices
======================================

In a multilingual environment, dictionary management has a significant impact on search quality.

Dictionary Maintenance by Language
-----------------------------------

.. list-table:: Dictionary Maintenance Points
   :header-rows: 1
   :widths: 20 40 40

   * - Dictionary
     - Japanese
     - English / Chinese
   * - Synonyms
     - Spelling variations, abbreviations, technical terms
     - Abbreviation expansion, synonyms
   * - Stop Words
     - Industry-specific unnecessary words
     - Domain-specific unnecessary words
   * - User Dictionary
     - Internal terms, product names
     - (Kuromoji-specific)
   * - Protwords (Protected Words)
     - Words that should not be stemmed
     - Technical terms, proper nouns

Regular Dictionary Maintenance
-------------------------------

Dictionaries are not something you set once and forget; they need to be reviewed regularly.

- Add new product names and project names
- Clean up terms that are no longer used
- Add new synonym candidates discovered from search logs

Combine this with the search quality tuning cycle introduced in Part 8 to maintain dictionaries on an ongoing basis.

Summary
=======

In this article, we explained how to build a search infrastructure in an environment where Japanese, English, and Chinese documents coexist.

- Understanding the different tokenization processes for each language
- Fess's multilingual index and Analyzer settings
- Customization for Japanese (Kuromoji), English, and Chinese
- Cross-language search support through multilingual synonyms
- Dictionary management best practices

Multilingual support is not something that can be completed with a single configuration; continuous improvement based on usage patterns is important.

In the next article, we will cover the stable operation of search systems.

References
==========

- `Fess Dictionary Management <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__

- `OpenSearch Analyzer <https://opensearch.org/docs/latest/analyzers/>`__
