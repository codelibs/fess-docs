==========
Dictionary
==========

Overview
========

This page explains the configuration settings related to dictionaries.

Make changes to dictionaries only after understanding the specifications of each dictionary.
Incorrect dictionary changes may make the index inaccessible.

List
====

To open the manageable dictionary list page shown below, click [System > Dictionary] in the left menu.

|image0|

What Each Dictionary Affects, and When It Takes Effect
======================================================

Each dictionary applies to different fields and takes effect at a different
point. If you edited a dictionary and the search results did not change, check
this table first.

.. list-table::
   :header-rows: 1
   :widths: 22 26 28 24

   * - Dictionary
     - File
     - Fields it applies to
     - When it takes effect
   * - Kuromoji
     - ``ja/kuromoji.txt``
     - ``_ja`` fields only, such as ``content_ja``
     - At index time (a recrawl is required)
   * - Synonym
     - ``synonym.txt``
     - ``content`` and ``title``
     - At search time (no recrawl needed)
   * - Mapping (all languages)
     - ``mapping.txt``
     - ``content`` and ``title``
     - At index time (a recrawl is required)
   * - Mapping (per language)
     - ``ja/mapping.txt``
     - ``_ja`` fields only, such as ``content_ja``
     - At index time (a recrawl is required)
   * - Protwords
     - ``en/protwords.txt``
     - ``content`` and ``title``
     - At index time and at search time
   * - Stopwords
     - ``en/stopwords.txt``
     - ``content`` and ``title``
     - At index time and at search time
   * - Stemmer Override
     - ``en/stemmer_override.txt``
     - ``content`` and ``title``
     - At index time and at search time

.. note::

   An analyzer is built when the index is opened, so updating a dictionary file
   does not take effect **until the index is closed and opened again**.
   A dictionary that applies at index time is not applied retroactively to
   documents that are already indexed either, so those documents have to be
   crawled again.

.. warning::

   The character mapping dictionary that applies to ``content``, the field most
   searches are answered from, is the **root** ``mapping.txt``, not
   ``ja/mapping.txt``. They share the name Mapping but they are different files.

The Kuromoji User Dictionary and Search Results
-----------------------------------------------

The ``content`` field is analyzed with the standard tokenizer and
``cjk_bigram``, so it is not affected by how Kuromoji segments a word.
Registering a Japanese compound word in the Kuromoji user dictionary and
crawling again therefore does not change what a search against ``content``
returns. The registration shows up in ``content_ja``, which is added to the
query depending on the language of the request.

Kuromoji
========

Manages the dictionary for Japanese morphological analysis.
ja/kuromoji.txt is the dictionary file for Japanese morphological analysis.

Synonym
=======

Manages the synonym dictionary.
synonym.txt is the synonym dictionary file used across all languages.

Mapping
=======

Manages the character replacement dictionary.
mapping.txt is the word replacement dictionary file used across all languages or for each language.

Protwords
=========

Manages the protected words dictionary.
protwords.txt is deployed for each language and contains a list of words to exclude from stemming.

Stopwords
=========

Manages the stopwords dictionary.
stopwords.txt is deployed for each language and contains a list of words to exclude during index creation.

Stemmer Override
================

Manages the stemmer override dictionary.
stemmer_override.txt is deployed for each language and is a word replacement dictionary file for overriding stemming processing.

.. |image0| image:: ../../../resources/images/en/15.9/admin/dict-1.png
            :height: 940px
