===============
Wildcard Search
===============

Wildcard Search
===============

|Fess| supports single and multiple character wildcard search.
Wildcard search performs indexed terms, not phrase.

Usage
-----

To perform a single character wildcard search, use "?" symbol.

::

    te?t

The above search looks for terms that match that with the single character replaced, such as text or test.

To perform a multiple character wildcard search, use "*" symbol.

::

    test*

Multiple character wildcard search looks for 0 or more characters, such as test, tests or tester.

You can also use the wildcard search in the middle of a term.
::

    te*t

Notice
------

Wildcard search support terms, not phrase.
If a word is indexed by bi-gram and so on, Wildcard search will not work properly.
So, to use Wildcard search, a proper morphological analysis needs to be used.
