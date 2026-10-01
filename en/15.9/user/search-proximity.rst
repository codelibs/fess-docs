==================
Proximity Search
==================
Proximity Search (Word Distance Search)
=========================================

Proximity search finds documents in which the words of a phrase appear close to each other, even if they are not directly adjacent. It is useful when other words may appear between the words you are looking for.

Usage
-------

Enclose the words in double quotation marks, and add "~" and a number after the closing quotation mark.

For example, the following search finds documents in which "Fess" and "search" appear within a distance of 3:

::

    "Fess search"~3

The number is the maximum number of position moves allowed between the words (see "How the Distance Is Counted" below). The larger the number, the farther apart the words may be.

You can also perform a proximity search on a specific field. In the following example, the title field is searched.

::

    title:"Fess search"~3

If you omit the number and specify only "~" (for example, ``"Fess search"~``), the phrase is searched as a normal phrase in which the words must be adjacent. A decimal number is truncated to an integer (``~2.5`` is treated as ``~2``).

Proximity search can be combined with a boost. In the following example, the proximity search is boosted by 2 (see :doc:`search-boost`).

::

    "Fess search"~5^2

How the Distance Is Counted
-----------------------------

* The number is the maximum number of position moves allowed between the words. It is counted in tokens produced by the analyzer of the target field, not in characters or whitespace-separated words. For English text, it is roughly the number of words between the terms. Words removed as stop words during analysis are still counted.
* The words may appear in a different order, but a reversed order requires a larger number. For example, a document containing "quick brown fox" matches ``"quick fox"~1``, but it matches ``"fox quick"`` only with ``~3`` or larger.

::

    "quick fox"~1
    "fox quick"~3

Japanese and Other CJK Text
-----------------------------

For Japanese and other CJK text, the unit in which the distance is counted depends on the field.

* On the general title and content fields, the distance is close to the number of characters between the words.
* On the language-specific fields, the distance is counted in morphological tokens, and removed particles are also counted.

Because of this, separate the words with spaces and specify a generous number.

::

    "全文 検索"~5
    "大阪 おいしい"~10

A string without spaces (for example, ``"大阪おいしい"~10``) may not work as a proximity search between the words as expected, because on the general fields it is matched as one continuous string. Separate the words with spaces. The distance cannot be converted exactly into a number of characters, so start with a generous number and narrow it down while checking the results.

Related Topics
----------------

- :doc:`search-fuzzy` - Fuzzy search
- :doc:`search-boost` - Boost search
- :doc:`search-field` - Field-specified search
- :doc:`special-char` - Special characters and escaping
