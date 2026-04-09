============================================================
Part 18: Fundamentals of AI Search -- Evolution from Keyword Search to Semantic Search
============================================================

Introduction
============

In previous articles, we have focused on keyword-based full-text search.
Full-text search is very effective when users can enter appropriate keywords.
However, there are cases where keyword search alone cannot adequately address needs such as "I don't know what keywords to search for" or "I want an answer to a conceptual question."

This article organizes the spectrum of search technologies and explains how search evolves from keyword search to semantic search.

Target Audience
===============

- Those interested in AI search who want to organize the concepts
- Those considering the introduction of semantic search
- Those who want to understand the AI-related features of Fess

Spectrum of Search Technologies
================================

Search technologies form a spectrum ranging from simple to advanced, as follows.

.. list-table:: Spectrum of Search Technologies
   :header-rows: 1
   :widths: 20 35 45

   * - Technology
     - Mechanism
     - Characteristics
   * - Keyword Search
     - Matches input terms against terms in documents
     - Fast and reliable. Requires exact term matching
   * - Fuzzy Search
     - Also matches terms with similar spelling
     - Handles typos
   * - Synonym Search
     - Expands synonyms for matching
     - Handles notation variations (manual configuration)
   * - Semantic Search
     - Matches based on semantic similarity
     - Finds related documents even without term matching
   * - Hybrid Search
     - Combination of keyword + semantic search
     - Leverages the strengths of both approaches

Limitations of Keyword Search
==============================

Keyword search is effective in many situations, but its limitations become apparent in the following cases.

Vocabulary Mismatch
--------------------

This occurs when the words used by users differ from the words used in documents.

Example: Even if a user searches for "I want to change my salary deposit destination," if the internal document uses the term "salary account change procedure," the keywords may not match.

This can be partially addressed with synonyms (see Part 8), but it is not practical to register all possible vocabulary combinations in advance.

Conceptual Search
------------------

This is the case where users want to search by concept rather than specific keywords, such as "internal rules about remote work."
In this case, various related documents could be relevant, including those about "working from home," "telework," "office attendance rules," and "attendance management."

How Semantic Search Works
==========================

Vector Representation (Embedding)
----------------------------------

The foundation of semantic search is converting text into "vectors (arrays of numbers)."
These vectors are mathematical representations of the "meaning" of the text.

Texts with similar meanings are placed close to each other in vector space.
For example, the vectors for "dog" and "pet" are close, while the vectors for "dog" and "automobile" are far apart.

How Search Works
-----------------

1. The user enters a search query
2. The query is converted to a vector
3. Similarity is calculated against document vectors in the index
4. Documents are returned in order of highest similarity

This allows finding semantically related documents even when keywords do not match exactly.

Semantic Search in Fess
========================

Fess can achieve vector-based search through semantic search plugins.

Enabling Semantic Search
-------------------------

1. Install the semantic search plugin
2. Configure the embedding model
3. Rebuild the index (vectorize existing documents)

Choosing an Embedding Model
-----------------------------

Select a model (embedding model) for converting text to vectors.

The key considerations are as follows:

- **Language support**: Whether it can properly handle the target language
- **Accuracy**: Quality of vectors (accuracy of semantic capture)
- **Speed**: Time required for conversion
- **Cost**: API usage fees, hardware requirements

Hybrid Search: Rank Fusion
============================

Semantic search is powerful but not omnipotent.
For searching proper nouns or cases requiring exact matching, keyword search is more appropriate.

The Concept of Hybrid Search
------------------------------

Hybrid search executes both keyword search and semantic search, then integrates the results.

Fess uses Rank Fusion to merge results from different search methods.
Specifically, the RRF (Reciprocal Rank Fusion) algorithm ensures that documents ranked highly in both search results are ultimately ranked at the top.

Benefits of Hybrid Search
---------------------------

- Combines the "reliability" of keyword search with the "flexibility" of semantic search
- Proper nouns are covered by keyword search
- Conceptual searches are covered by semantic search
- Overall search quality improves compared to using either method alone

Criteria for Adoption
======================

Semantic search should not necessarily be introduced in every environment.

Cases Where Adoption Should Be Considered
-------------------------------------------

- There are many "zero-hit queries" in search logs
- Users report that they "don't know the right keywords"
- You want to support natural language questions (a prerequisite for RAG in Part 19)
- You want to enhance cross-language search for multilingual documents

Cases Where It Is Not Yet Needed
----------------------------------

- Sufficient search quality is achieved with keyword search + synonyms
- The number of documents is small and users know the appropriate keywords
- Computing resources (GPU or cloud API costs) are limited

Gradual Adoption
-----------------

1. First, improve quality with keyword search + synonyms (Part 8)
2. If zero-hit queries remain frequent, consider semantic search
3. Use hybrid search to benefit from both approaches

Summary
=======

This article organized the path of evolution from keyword search to semantic search.

- The spectrum of search technologies (keyword -> fuzzy -> synonym -> semantic -> hybrid)
- How semantic search works (vector representation and similarity calculation)
- Semantic search and hybrid search in Fess (Rank Fusion)
- Criteria for adoption and a gradual approach

In the next article, we will further develop semantic search and build an AI assistant using RAG.

References
==========

- `Fess AI Search Features <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `OpenSearch Vector Search <https://opensearch.org/docs/latest/search-plugins/knn/>`__
