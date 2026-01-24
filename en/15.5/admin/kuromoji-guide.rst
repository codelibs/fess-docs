==================
Kuromoji Dictionary
==================

Overview
========

You can register personal names, proper nouns, technical terms, and other words for morphological analysis.

Management Operations
=====================

Display Method
--------------

To open the Kuromoji configuration list page shown below, click [System > Dictionary] in the left menu, then click kuromoji.

|image0|

Click the configuration name to edit it.

Configuration Method
--------------------

To open the Kuromoji configuration page, click the New button.

|image1|

Configuration Items
-------------------

Token
:::::

Enters the word to process in morphological analysis.

Segmentation
::::::::::::

When a word is composed of compound words, you can make it searchable even when searching with segmented words.
For example, by entering "全文検索エンジン" as "全文 検索 エンジン", you can search with the segmented words.

Reading
:::::::

Enters the reading of the word entered as a token in katakana.
If segmentation is used, enter the reading in segmented form.
For example, enter "ゼンブン ケンサク エンジン".

POS
:::

Enters the part of speech of the entered word.

Download
========

You can download in Kuromoji dictionary format.

Upload
======

You can upload in Kuromoji dictionary format.
The Kuromoji dictionary format uses comma (,) delimiters: "token,segmented tokens,reading of segmented tokens,part of speech".
Segmented tokens are separated by spaces.
If segmentation is not needed, the token and segmented tokens are equal.
For example:

::

    朝青龍,朝青龍,アサショウリュウ,カスタム名詞
    関西国際空港,関西 国際 空港,カンサイ コクサイ クウコウ,カスタム名詞

.. |image0| image:: ../../../resources/images/en/15.5/admin/kuromoji-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/kuromoji-2.png
