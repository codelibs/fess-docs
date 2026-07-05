========================
Analyzer Configuration
========================

About Analyzer
==============

When creating indexes for search, it is necessary to segment documents for registration as indexes.
In |Fess|, the functionality to break documents into words is registered as an Analyzer.
An Analyzer consists of CharFilter, Tokenizer, and TokenFilter.

Basically, items smaller than the units separated by the Analyzer will not be found even when searched.
For example, consider the sentence "Living in Tokyo".
Suppose this sentence is divided by the Analyzer into "Tokyo", "in", and "Living".
In this case, a search for "Tokyo" will produce a hit.
However, a search for "Kyo" will not produce a hit.

|Fess| provides a dedicated Analyzer for each language.
The Analyzer applied is automatically switched based on the suffix of the field name in the index (e.g. ``content_ja``, ``content_en``).

Analyzer Definition Files
==========================

The Analyzer has no dedicated administration screen; it is changed by directly editing configuration files.
The relevant files are located under ``app/WEB-INF/classes/fess_indices/``.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - File
     - Description
   * - ``fess_indices/fess.json``
     - Settings for the document index. Contains definitions for CharFilter, Tokenizer, TokenFilter, and Analyzer.
   * - ``fess_indices/fess/doc.json``
     - Mapping for the document index. Assigns the Analyzer to apply for each field name pattern such as ``*_ja`` and ``*_en``.
   * - ``fess_indices/fess/<lang>/``
     - Dictionary files per language (e.g. ``ja/kuromoji.txt``, ``ko/nori.txt``, ``en/protwords.txt``, ``en/stemmer_override.txt``, and ``stopwords.txt`` for each language).
   * - ``fess_indices/fess/mapping.txt``, ``fess_indices/fess/synonym.txt``
     - Character mapping dictionary and synonym dictionary shared across all languages.

The Analyzer definitions themselves (combinations of Tokenizer and TokenFilter) are specified in ``fess.json``, while which Analyzer to apply to which field is specified in ``fess/doc.json``.

.. note::
   When using a managed service such as Amazon OpenSearch Service, a configuration file corresponding to the search engine type takes precedence, such as ``fess_indices/_aws/fess.json`` or ``fess_indices/_cloud/fess.json``.

Registering Analyzers
======================

Analyzer settings are registered by creating an index based on the configuration files described above when no search index exists at |Fess| startup.
The index is created with a timestamped name (e.g. ``fess.20240101120000000``), and the aliases ``fess.search`` and ``fess.update`` are assigned to it.

Placeholders such as ``${fess.dictionary.path}`` in the configuration files are replaced with actual values when the index is created.
The location where dictionary files are placed can be changed with the system property ``fess.dictionary.path``.

If an existing index is present, the already-defined settings are reused.
Therefore, if you change Analyzer definitions, you must rebuild the index to reflect those changes.

Tuning with Dictionaries
=========================

The dictionaries referenced by the Analyzer can be edited from the administration screen.

* :doc:`../admin/kuromoji-guide` - User dictionary for Japanese morphological analysis
* :doc:`../admin/synonym-guide` - Synonym dictionary
* :doc:`../admin/mapping-guide` - Character mapping
* :doc:`../admin/stopwords-guide` - Stop words
* :doc:`../admin/protwords-guide` - Protected words
* :doc:`../admin/stemmeroverride-guide` - Stemming overrides

For how to configure Analyzers, refer to the OpenSearch Analyzer documentation.

Notes
=====

Analyzer configuration has a major impact on search.
When changing Analyzers, either understand how Lucene Analyzers work before implementing changes, or consult commercial support.
