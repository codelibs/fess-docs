==================
Analyzer Configuration
==================

About Analyzer
==============

When creating indexes for search, it is necessary to segment documents for registration as indexes.
In |Fess|, the functionality to break documents into words is registered as an Analyzer.
Analyzers consist of CharFilter, Tokenizer, and TokenFilter.

Basically, items smaller than the units separated by the Analyzer will not be found even when searched.
For example, consider the sentence "Living in Tokyo".
Suppose this sentence is divided by the Analyzer into "Tokyo", "in", and "Living".
In this case, a search for "Tokyo" will produce a hit.
However, a search for "Kyo" will not produce a hit.

Analyzer configuration is registered when the fess index does not exist at |Fess| startup by creating the fess index with app/WEB-INF/classes/fess_indices/fess.json.
For how to configure Analyzers, refer to the OpenSearch Analyzer documentation.

Analyzer configuration has a major impact on search.
When changing Analyzers, either understand how Lucene Analyzers work before implementing changes, or consult commercial support.
