=========================================
Improving Search Quality with Search Logs
=========================================

Introduction
============

Once people start using search, you will hear things like "the document I'm looking for doesn't show up" or "the document I want is buried near the bottom".
What is happening for each search term can be seen in the search logs and click logs that Fess records.

In Fess 15.9, the [System Info] > [Search Log] screen of the admin console includes an analytics report that aggregates figures such as the zero-hit rate and click positions.
This article explains how to use this screen to find problematic search terms, decide whether to fix them with synonyms, Key Match, Document Boost, Related Query or stopwords, apply the fix, and then confirm its effect on the same screen.

Building your own aggregations of search logs in OpenSearch Dashboards is covered in :doc:`guide-22`, and how documents that mix Japanese, English and Chinese are analyzed is covered in :doc:`guide-09`.

What to Look at on the Search Log Screen
========================================

Open [System Info] > [Search Log] in the left menu, and the [Overview] tab is displayed.
Viewing it requires the ``admin-searchlog`` or ``admin-searchlog-view`` role.

At the top of each tab, choose the period ("Today", "Yesterday", "Last 7 days", "Last 28 days", "Last 90 days", "Custom") and the access type, then click [Apply].
If you enable "Compare to previous period", the values for the preceding period of the same number of days are shown side by side.
Use this to compare before and after an improvement.

The metrics that give clues for improvement, and the measures that work for each, are as follows.

.. list-table::
   :header-rows: 1
   :widths: 24 22 30 24

   * - Metric
     - Where it is shown
     - What it tells you
     - Main measures
   * - Zero-hit rate, zero-hit queries
     - [Overview] and [Queries] tabs
     - The share of searches that returned no hits at all, and their search terms
     - Synonyms, Related Query, adding documents
   * - Zero-click queries
     - [Queries] tab
     - Search terms that returned hits, but whose results were never clicked
     - Key Match, Document Boost
   * - Avg. click position
     - [Queries] tab (per search term), [Clicks] tab (overall)
     - The position at which clicked results appeared (the top result is 1)
     - Key Match, Document Boost
   * - Click position distribution, next-page view rate
     - [Clicks] tab
     - Whether clicks concentrate on positions 1-10, 11-20 or 21 and below, and the share of searches in which page 2 or later was viewed
     - Key Match, Document Boost
   * - Top queries, most clicked URLs
     - [Overview] tab, [Clicks] tab
     - The words people search for most often, and the documents they actually open
     - Check the results starting from the top terms

As background for these figures, keep the following in mind.

- Recording is enabled with "Search Log" and "User Log" in [System] > [General] (both are enabled by default). If "User Log" is disabled, the number of users is not counted.
- A click is recorded when "Search Log" is enabled and a link in the search results is opened via ``/go/``. The search page of the standard theme (bootstrap) builds its links this way.
- The per-term click metrics and the zero-click queries count only clicks from 15.9 onward, the version in which clicks started to be recorded together with the search term.
- If a number of days is set in "Delete old search logs" in [General], logs older than that cannot be used for comparison (the default ``-1`` deletes nothing).
- Logs are written in batches, so it may take a little while for a search to appear on the screen.

Telling Apart the Causes of Zero-Hit Queries
============================================

Clicking a zero-hit query on the [Overview] or [Queries] tab shows that term's search logs on the [Logs] tab, filtered with "Hit Count" set to "Zero hits only".
After checking when and with which access type it was searched, actually search for the term on the search page and classify the cause as one of the following three.

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Situation
     - Measure
     - What is needed to apply it
   * - The documents exist but use different wording (e.g. users search for "telecommuting", the documents say "telework")
     - Synonyms
     - Reloading the document index
   * - You want to steer users to the official wording (abbreviations, former names, misspellings)
     - Related Query
     - Nothing (applied when saved)
   * - No matching documents are in the index
     - Adding crawl targets (:doc:`guide-04`)
     - Running a crawl

Key Match and Document Boost do not help with zero-hit queries.
Both raise the ranking of documents that match the search term, and neither adds documents that do not match the search term to the results.

Worked Example: Fixing the Zero-Hit Query "telecommuting" with a Synonym
========================================================================

Suppose "telecommuting" keeps appearing among the zero-hit queries on the [Queries] tab, while the company's policies use the word "telework".
Using this situation as an example, we go through everything from the fix to the confirmation.

1. Confirm the Cause
--------------------

Search for "telework" on the search page and confirm that the documents users were presumably looking for are found.
If they are not found here, the problem is not the wording: the documents are not in the index.
Review the crawl targets instead of adding a synonym.

2. Register the Synonym
-----------------------

1. Open [System] > [Dictionary], and in the list click the row whose "Type" is ``synonym`` (the one whose name ends with ``synonym.txt``).
2. Click [Create New].
3. Enter the following two lines in both "Source" and "Target", then click [Create].

::

    telecommuting
    telework

If you put the same words in "Source" and "Target", the dictionary stores them as the single line ``telecommuting,telework``, and searching for either word also finds documents that contain the other.
If you want to expand only searches for "telecommuting", make "Source" the single line "telecommuting" and "Target" the two lines above (this becomes ``telecommuting=>telecommuting,telework``).
Note that if "Target" does not include the original word, searches no longer look for the original word itself.

Write one word per line in the input fields.
Words that contain a comma (,) or ``=>`` cannot be registered.
The synonym dictionary reference lists the following rules for registration.

- Register hiragana as katakana, small katakana as full-size katakana, and full-width alphanumerics as half-width alphanumerics
- By default, Japanese and other CJK text is indexed as bi-grams split every two characters, so do not register one-character words
- Do not register the same word more than once

Synonyms apply to the ``content`` and ``title`` fields, and expand words at search time.
There is no need to re-index.

3. Apply the Dictionary Change
------------------------------

Saving the dictionary alone does not change the search results.
The open index keeps running with the old dictionary.

1. Open [System Info] > [Maintenance].
2. Click [Reload] under "Reload Document Index".

This button writes the saved dictionaries out to files, then closes the document index and opens it again.

.. warning::

   While the index is closed, and after it is opened until its shards are allocated, searches are not possible and return errors or zero hits.
   The larger the index, the longer this takes, so run it at a time of low usage.

4. Confirm the Effect
---------------------

First, search for "telecommuting" on the search page and confirm that documents containing "telework" are found.

Next, on the [Logs] tab of [System Info] > [Search Log], filter by entering "telecommuting" in "Search word" and choosing "One or more hits" for "Hit Count".
If searches made by users after the change are recorded with hits, the fix is working.

After a few days, on the [Overview] tab set the period to "Custom", set the start date to the day after the change, and enable "Compare to previous period".
Periods are divided by day (dates in the server's time zone), so if you include the day of the change, the zero hits from before the change are counted too.
Confirm that the zero-hit rate is lower than in the previous period, and that "telecommuting" has disappeared from the list of zero-hit queries.
If you leave the period at something like "Last 7 days", the zero-hit searches from before the change stay within the period, so the term does not disappear from the list right away.

The dictionary contents can be saved as a file with [Download] on the list screen.
Saving it before and after a change lets you use it when you need to revert.

Bringing Target Documents to the Top: Key Match
===============================================

Terms with a high average click position on the [Queries] tab, or terms that are zero-click queries, may be cases where the right document is found but is buried low in the results.
Looking at the most clicked URLs on the [Clicks] tab shows which documents users end up opening.
Key Match is the feature that brings such a document to the top for a specific search term.

In [Crawler] > [Key Match], click [Create New], enter the following, and click [Create].

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Field
     - Example
     - Description
   * - Term
     - ``expenses``
     - Applied when a word in the search keywords matches this value (case-insensitive). Specify a single word
   * - Query
     - ``url:"https://portal.example.com/manual/expense.html"``
     - A search query that selects the documents to bring to the top
   * - Size
     - ``10`` (default)
     - The maximum number of documents matching the query that are targeted
   * - Boost
     - ``100`` (default)
     - The weight multiplied into the score of the target documents

Always enclose the URL in the query in ``"``.
If it is not enclosed, as in ``url:https://...``, parsing the query fails on the ``:`` in the URL, and the Key Match is not loaded and does nothing (only a WARN is written to ``fess.log``).
The ``url`` field is an exact match, so the value must be identical, character for character, to the URL that is indexed.
Before registering, run the same query on the search page and confirm that exactly one target document is found.

No reload like the one for dictionaries is needed.
Saving starts reloading the Key Match entries in the background, and they switch over once all entries have been read.
Loading waits one second between entries, so with many entries it takes a while to take effect.

Check the result on the details screen of the registered Key Match, opened from the list.
If the URL of the target document is shown in the "URLs" field, it is in effect.
Right after saving, the reload may not have finished yet, so the field can be empty.
If it is still empty after waiting a little and reopening the details screen, the query does not match any document.
The documents that match the query are determined again when you save and each time a crawl job finishes.
Documents that have not been crawled yet therefore become targets after the next crawl.

Note also that only documents that match the search term are targeted.
If searching for "expenses" does not find the target document in the first place, registering a Key Match will not make it appear in the results.

Raising a Site or Group of Documents: Document Boost
====================================================

To raise a specific group of documents, such as the official manual site, regardless of the search term, use [Crawler] > [Document Boost].

Click [Create New] and enter the following.

- Condition: ``url.startsWith("https://portal.example.com/manual/")``
- Boost Expression: ``10``
- Script Type: ``javascript`` (pre-filled when creating a new rule)
- Sort Order: ``0``

The condition and the boost expression are evaluated as script expressions, and each field of the document can be used as a variable.
For documents for which the condition returns ``true``, the value of the boost expression is put into the ``boost`` field.
This is the same field as "Boost" in the web and file system crawl configurations (default 1.0); for documents that match a rule, the rule's value is used.
If a document matches several rules, the rule with the smallest sort order is used.
In JavaScript, do not put a semicolon at the end of an expression.
With a semicolon, the value becomes ``null`` and the rule has no effect.

Document Boost takes effect differently from Key Match and synonyms.

- Rules are evaluated when documents are registered in the index by web crawls and file crawls. They are not applied to documents from data store crawls.
- Adding or changing a rule does not change the values of documents that are already indexed.
- When "Check Last Modified" in [General] is enabled (the default), documents whose content has not changed are not registered again on a re-crawl. To apply the rule to existing documents, delete the target documents in [System Info] > [Search] and then crawl again.

Once it has taken effect, search with words that match that group of documents to confirm that their ranking has gone up, and after a while compare the average click position on the [Queries] tab with the previous period.

Suggesting Alternative Wording: Related Query
=============================================

To suggest searching with a different word without widening the user's search term, use Related Query.
In [Crawler] > [Related Query], click [Create New], enter the user's word in "Term" (e.g. ``VPN``), and enter the suggested words in "Queries", one per line (e.g. ``remote access``, ``off-site connection``).

With the standard theme (bootstrap), when the search term matches, buttons are shown above the search results under "Related searches:".
They are also shown on a results page with zero hits, so they can be used to steer users away from zero-hit queries.
The term is compared with the whole search string that was entered (case-insensitive).
It takes effect when saved, with no reload needed.

With [Generate from Search Logs] on the list screen, related queries can be created automatically from pairs of words that the same user searched again within a short interval.
This requires both "Search Log" and "User Log" in [General] to be enabled.
Terms that already have a related query are not changed.
For the generation conditions and the settings for tuning them, see `Related Query <https://fess.codelibs.org/stable/admin/relatedquery-guide.html>`__.

Before Using Stopwords
======================

If a word contained in every document (for example, an English word in the footer of every page) gets mixed into search terms and widens the results too much, you can remove that word from analysis with stopwords.
However, each stopword dictionary file applies only to specific fields.

- ``en/stopwords.txt`` is used for analyzing ``content``, ``title`` and the fields ending in ``_en``.
- ``ja/stopwords.txt`` is used only for fields ending in ``_ja``, such as ``content_ja`` and ``title_ja``, of documents detected as Japanese. It is empty by default.

Taking Japanese text as an example: particles such as "の" and "は" are removed by the part-of-speech filter in the ``_ja`` fields, but not in ``content`` and ``title``.
Japanese text in ``content`` and ``title`` is split into two-character units, and hiragana is converted to katakana before matching ("VPNとは" becomes ``vpn`` and ``トハ``).
Therefore, adding a Japanese word to ``en/stopwords.txt`` does not remove it unless it exactly matches a two-character unit produced by that splitting.
Use stopwords mainly for English words, and check whether they take effect with the OpenSearch ``_analyze`` API.

.. code-block:: bash

    curl -X POST "localhost:9200/fess.search/_analyze" -H "Content-Type: application/json" \
      -d '{"analyzer": "standard_search_analyzer", "text": "VPNとは"}'

Stopwords take effect both at index time and at search time.
After saving the dictionary, reload the document index as with synonyms, and re-crawl to remove the words from documents that are already indexed.
For how the language-specific fields work, see :doc:`guide-09`.

Troubleshooting
===============

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptom
     - What to check
   * - Registered a synonym but the results do not change
     - Whether you reloaded the document index. Whether the entry follows the registration rules (hiragana, one-character words, and so on)
   * - Key Match does not work
     - Whether the "URLs" field on the details screen is empty. Whether you enclosed the URL in the query in ``"``. Whether the user's search keywords contain exactly the same word as the term, as a separate word (a different form such as "expense" does not match). Whether the target document is found by that word
   * - Document Boost does not work
     - Whether the targets are data store documents. Whether the documents were registered again after the rule was added. Whether the condition ends with a semicolon
   * - Related queries are not shown
     - Whether the term matches the whole search string. If you use your own theme, whether it is built to display related queries
   * - Click metrics are empty
     - Whether "Search Log" in [General] is enabled. Whether search result links go through ``/go/``. Whether the period contains only clicks recorded before 15.9

What to Read Next
=================

- To build your own aggregations of search logs in OpenSearch Dashboards: :doc:`guide-22`
- To improve search over documents that mix Japanese, English and Chinese: :doc:`guide-09`
- If the cause of zero hits was missing documents: :doc:`guide-04`
- To show documents that are close in meaning even when the words do not match: :doc:`guide-18`
- To manage dictionary and Key Match settings as code: :doc:`guide-16`

References
==========

- `Search Log <https://fess.codelibs.org/stable/admin/searchlog-guide.html>`__
- `Dictionary <https://fess.codelibs.org/stable/admin/dict-guide.html>`__
- `Synonym Dictionary <https://fess.codelibs.org/stable/admin/synonym-guide.html>`__
- `Stopwords Dictionary <https://fess.codelibs.org/stable/admin/stopwords-guide.html>`__
- `Key Match <https://fess.codelibs.org/stable/admin/keymatch-guide.html>`__
- `Document Boost <https://fess.codelibs.org/stable/admin/boostdoc-guide.html>`__
- `Related Query <https://fess.codelibs.org/stable/admin/relatedquery-guide.html>`__
- `Maintenance <https://fess.codelibs.org/stable/admin/maintenance-guide.html>`__
