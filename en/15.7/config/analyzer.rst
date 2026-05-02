======================
Analyzer Configuration
======================

About Analyzers
===============

When creating an index for searching, it's essential to segment documents for indexing purposes. In |Fess|, we register the functionality of breaking down documents into words as Analyzers. Analyzers consist of CharFilters, Tokenizers, and TokenFilters.

In general, items smaller than the units segmented by Analyzers won't be retrieved, even if a search is performed. For example, consider the sentence "I live in Tokyo." Let's assume that this sentence is divided by the Analyzer into "I," "live," and "in Tokyo." In this case, searching using the term "Tokyo" will yield a match. However, searching using "Kyoto" will not.

Analyzer settings are registered and created for the fess index in the app/WEB-INF/classes/fess_indices/fess.json file if the fess index doesn't exist when |Fess| is started. For information on configuring Analyzers, please refer to the OpenSearch Analyzer documentation.

Analyzer settings have a significant impact on search results. If you intend to modify the Analyzer, it's recommended to do so with an understanding of how Lucene's Analyzers work or consult with commercial support.
