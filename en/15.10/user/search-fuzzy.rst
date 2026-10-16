============
Fuzzy Search
============

Fuzzy Search (Approximate Search)
=================================

You can use fuzzy search (approximate search) when you want to search for words that do not exactly match the search term. Fuzzy search is a method that treats a word in the index as a match if the difference (edit distance) between the search term and that word is within a certain range. Edit distance is the minimum number of character insertions, deletions, and substitutions required to transform one word into another. By default, |Fess| uses the Damerau-Levenshtein distance (optimal string alignment), which, in addition to these operations, also counts the transposition of two adjacent characters as a single difference.

Usage
-----

Add "~" after the search term to which you want to apply fuzzy search.

For example, to perform a fuzzy search for the word "fess", enter it in the search form as shown below to search for documents containing words similar to "fess" (such as "fes"):

::

    fess~

By adding a number after "~", you can specify the allowed edit distance (how many characters of difference are permitted). The value can be an integer of 0, 1, or 2.

::

    fess~1

In the example above, words with an edit distance of 1 or less from "fess" are searched for.

If you omit the number and specify only "~", the edit distance is treated as 2. The maximum edit distance is 2, and specifying a value of 3 or higher is also treated as 2.

You can also perform a fuzzy search on a specific field. In the following example, documents containing words similar to "fess" in the title field are searched for.

::

    title:fess~

If you do not specify a field, fuzzy search is performed on the title and content fields.

Usage Conditions
----------------

Please note the following points when using fuzzy search.

* Fuzzy search is applied on a per-word basis. It cannot be applied to phrases enclosed in quotation marks. Note that a number placed after a phrase (for example, ``"Fess Search"~2``) is not a fuzzy search but a :doc:`proximity search <search-proximity>` that represents the distance between words.
* Fuzzy search targets words that have been registered in the index, and the search term is not re-analyzed. As a result, it may not work as expected for text such as Japanese, which is tokenized using bi-grams or morphological analysis. Fuzzy search is mainly effective for alphanumeric words.
* The search term of a fuzzy search is counted for edit distance as is, including the distinction between uppercase and lowercase. Since alphabetic words registered in the index are usually converted to lowercase, use lowercase letters in the search term. For example, ``Fess~1`` uses up its edit distance of 1 on the leading uppercase ``F`` alone, so it does not give the same results as ``fess~1``. Also, ``Fess~0`` matches nothing because the index has no word that matches the uppercase word ``Fess`` (the lowercase ``fess~0`` is an exact match).
* If you add "~" (edit distance 2) to a very short word of one or two characters, it also matches words in which only about as many characters as the length of the word have been replaced. For example, ``ab~`` matches ``xy``, in which both characters differ, in addition to ``ab`` and ``ac``. Because this increases unintended results, specify a small edit distance such as ``ab~1`` for short words.

.. note::

    The behavior of fuzzy search can be adjusted in ``fess_config.properties``.

    * ``query.fuzzy.prefix_length`` (default: ``0``): The number of characters from the beginning of the word that must match exactly. Increasing this value narrows the range of errors allowed.
    * ``query.fuzzy.expansions`` (default: ``50``): The maximum number of words expanded as match candidates.
    * ``query.fuzzy.transpositions`` (default: ``true``): Specifies whether the transposition of two adjacent characters is counted as a single edit. When ``true``, the Damerau-Levenshtein distance is used; when ``false``, the classic Levenshtein distance is used.

.. note::

    Even in a normal search without "~", |Fess| automatically adds a small amount of weighted fuzzy matching as an auxiliary aid, for the purpose of increasing relevance, for search terms of a certain length or longer (4 characters or more by default) (``query.boost.fuzzy.*``). This is mainly a feature for adjusting the ranking of search results and is a separate mechanism from fuzzy search using "~". However, this auxiliary matching is also included in the search results, so documents that do not contain the search term itself but contain only a word that differs by one character may be added to the results (documents containing the search term itself are ranked higher). If you want to stop this behavior, specify a negative value (for example, ``-1``) for ``query.boost.fuzzy.min.length``.

Related Topics
--------------

- :doc:`search-wildcard` - Wildcard search
- :doc:`search-proximity` - Proximity search
- :doc:`special-char` - Special characters and escaping
