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

.. |image0| image:: ../../../resources/images/en/15.4/admin/dict-1.png
            :height: 940px
