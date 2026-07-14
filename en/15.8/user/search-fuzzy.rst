============
Fuzzy Search
============

Fuzzy Search (Approximate Search)
=================================

You can use fuzzy search (approximate search) when you want to search for words that do not exactly match the search term. Fuzzy search is a method that treats a word in the index as a match if the difference (edit distance) between the search term and that word is within a certain range. Edit distance is the minimum number of character insertions, deletions, and substitutions required to transform one word into another. By default, |Fess| uses the Damerau-Levenshtein distance (optimal string alignment), which, in addition to these operations, also counts the transposition of two adjacent characters as a single difference.

Usage
-----

Add "~" after the search term to which you want to apply fuzzy search.

For example, to perform a fuzzy search for the word "Fess", enter it in the search form as shown below to search for documents containing words similar to "Fess" (such as "Fes"):

::

    Fess~

By adding a number after "~", you can specify the allowed edit distance (how many characters of difference are permitted). The value can be an integer of 0, 1, or 2.

::

    Fess~1

In the example above, words with an edit distance of 1 or less from "Fess" are searched for.

If you omit the number and specify only "~", the edit distance is treated as 2. The maximum edit distance is 2, and specifying a value of 3 or higher is also treated as 2.

You can also perform a fuzzy search on a specific field. In the following example, documents containing words similar to "Fess" in the title field are searched for.

::

    title:Fess~

If you do not specify a field, fuzzy search is performed on the title and content fields.

Usage Conditions
----------------

Please note the following points when using fuzzy search.

* Fuzzy search is applied on a per-word basis. It cannot be applied to phrases enclosed in quotation marks. Note that a number placed after a phrase (for example, ``"Fess Search"~2``) is not a fuzzy search but a proximity search that represents the distance between words.
* Fuzzy search targets words that have been registered in the index, and the search term is not re-analyzed. As a result, it may not work as expected for text such as Japanese, which is tokenized using bi-grams or morphological analysis. Fuzzy search is mainly effective for alphanumeric words.
* For very short words of one or two characters, since the edit distance must be smaller than the length of the word for a match to occur, adding "~" may result in behavior close to an exact match.

.. note::

    The behavior of fuzzy search can be adjusted in ``fess_config.properties``.

    * ``query.fuzzy.prefix_length`` (default: ``0``): The number of characters from the beginning of the word that must match exactly. Increasing this value narrows the range of errors allowed.
    * ``query.fuzzy.expansions`` (default: ``50``): The maximum number of words expanded as match candidates.
    * ``query.fuzzy.transpositions`` (default: ``true``): Specifies whether the transposition of two adjacent characters is counted as a single edit. When ``true``, the Damerau-Levenshtein distance is used; when ``false``, the classic Levenshtein distance is used.

.. note::

    Even in a normal search without "~", |Fess| automatically adds a small amount of weighted fuzzy matching as an auxiliary aid, for the purpose of increasing relevance, for search terms of a certain length or longer (4 characters or more by default) (``query.boost.fuzzy.*``). This is a feature for adjusting the ranking of search results and is a separate mechanism from fuzzy search using "~".
