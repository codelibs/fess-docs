============================================================
Part 8: Growing Search Quality -- A Search Tuning Cycle Based on User Behavior Data
============================================================

Introduction
============

Deploying a search system is not the end of the journey.
Once users begin using search in practice, feedback such as "I can't find the results I expected" or "irrelevant results appear at the top" may arise.

This article introduces a search quality tuning cycle that involves analyzing search logs to identify issues, implementing improvements, and measuring their effectiveness.
Rather than achieving perfect search quality all at once, this is an approach of continuous improvement based on data.

Target Audience
===============

- Search system administrators
- Those who want to improve search quality
- Those already operating Fess who have received feedback from users

The Search Quality Tuning Cycle
===============================

Search quality improvement follows a four-step cycle:

1. **Analyze**: Review search logs and identify issues
2. **Improve**: Implement solutions for the identified issues
3. **Verify**: Confirm the effectiveness of the improvements
4. **Continue**: Repeat the cycle to continuously enhance quality

Step 1: Analyzing Search Logs
=============================

How to Check Search Logs
------------------------

Fess automatically records user search behavior.
You can review search logs from [System Info] > [Search Log] in the admin console.

Search logs contain the following information:

- Search keywords
- Search date and time
- Number of search results
- User agent

Patterns to Watch For
---------------------

When analyzing search logs, there are specific patterns you should pay attention to.

**Zero-Hit Queries**

These are queries that return zero results.
The information the user is looking for may not exist, or the search keywords may not be matching appropriately.

For example, a search for "company trip" returns zero hits, but a document titled "employee recreation" exists.
This can be resolved by configuring synonyms.

**High-Frequency Queries**

Frequently searched keywords represent important information needs for the organization.
Check whether appropriate results are displayed at the top for these queries.

**Click Logs**

These are records of which links in the search results were clicked.
If the top results are not being clicked and only lower-ranked results are clicked, there is room for improvement in the ranking.

Step 2: Implementing Improvements
=================================

Based on the analysis results, implement the following improvements in combination.

Configuring Synonyms
--------------------

Register synonyms to handle variations in wording and abbreviations.

Configure them by selecting the synonym dictionary from [System] > [Dictionary] in the admin console.

Configuration example:

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

By configuring synonyms, searching for one term will also return documents containing its synonyms.

Configuring Key Match
---------------------

This feature displays a specific document at the top of results for a particular keyword.

Configure it from [Crawler] > [Key Match] in the admin console.

For example, you can configure the expense report manual page to appear at the top when users search for "expense report."

.. list-table:: Key Match Configuration Example
   :header-rows: 1
   :widths: 30 50 20

   * - Search Term
     - Query
     - Boost Value
   * - 経費精算
     - url:https://portal/manual/expense.html
     - 100
   * - 有給申請
     - url:https://portal/manual/paid-leave.html
     - 100
   * - VPN接続
     - url:https://portal/manual/vpn-setup.html
     - 100

Configuring Document Boost
--------------------------

This adjusts the overall score of documents that match specific conditions.

Configure it from [Crawler] > [Document Boost] in the admin console.

For example, the following boost strategies can be considered:

- Increase the score of official manuals (portal site)
- Prioritize documents with more recent last-modified dates
- Increase the score of documents with a specific label (official documents)

Configuring Related Queries
---------------------------

This feature suggests related keywords on the search results page.
It helps users refine their search or search from a different angle.

Configure it from [Crawler] > [Related Query] in the admin console.

Configuration example:

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Configuring Stop Words
----------------------

Configure words that should be ignored during search.
Common particles such as "no," "wa," and "wo" are handled by default, but you can add industry-specific noise words as needed.

Configure them by selecting the stop word dictionary from [System] > [Dictionary] in the admin console.

Step 3: Verifying Effectiveness
===============================

After implementing improvements, verify their effectiveness.

Verification Methods
--------------------

**Change in Zero-Hit Rate**

Check how the proportion of zero-hit queries has changed before and after the improvement.
If the zero-hit rate has decreased after adding synonyms or configuring key matches, you can conclude that the improvement was effective.

**Change in Click Position**

Check the distribution of which position in the search results is being clicked.
If the proportion of clicks on top results has increased, you can conclude that the ranking has improved.

**Checking Popular Words**

Check the popular words displayed on the search page and the frequently searched keywords aggregated from search logs.
It is also effective to manually verify whether appropriate results are returned by searching for popular words.

Step 4: Continuous Improvement
==============================

Search quality tuning is not something that ends with a single effort.

Establishing an Operational Cycle
---------------------------------

We recommend establishing an operational cycle such as the following.

.. list-table:: Tuning Cycle Example
   :header-rows: 1
   :widths: 25 35 40

   * - Frequency
     - Action
     - Details
   * - Weekly
     - Check zero-hit queries
     - Check for new zero-hit queries and address them with synonyms or key matches
   * - Monthly
     - Overall search log analysis
     - Review trends in high-frequency queries, click rates, and zero-hit rates
   * - Quarterly
     - Comprehensive review
     - Conduct a comprehensive evaluation of search quality and formulate an improvement plan

Feedback from Users
-------------------

In addition to log analysis, feedback from actual users is also an important input for improvement.
Establish a mechanism to collect feedback such as "I couldn't find what I was looking for with this keyword" or "this result was helpful."

Summary
=======

This article introduced a tuning cycle for continuously improving search quality.

- Search log analysis (zero hits, high-frequency queries, click logs)
- Improvements through synonyms, key match, document boost, and related queries
- Methods for verifying improvement effectiveness
- Establishing a continuous operational cycle

Let us grow search quality through data-driven improvement, moving from "search that is used" to "search that is useful."

The next article will cover building a search infrastructure in multilingual environments.

References
==========

- `Fess Search Log <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Dictionary Management <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
