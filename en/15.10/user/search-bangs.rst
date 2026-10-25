==============================
Bangs (Searching Another Site)
==============================

A bang sends a search to another site instead of searching |Fess|. It works like the bangs of DuckDuckGo: put ``!`` and a short trigger word in the query, and |Fess| sends the rest of the query to the site the trigger stands for.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Query
     - Goes to
   * - ``airplane !g``
     - Google, searching for ``airplane``
   * - ``!w Ohm's law``
     - Wikipedia, searching for ``Ohm's law``
   * - ``!g``
     - The home page of Google
   * - ``airplane !unknown``
     - |Fess|, as a normal search (``!`` means NOT, see :doc:`search-not`)

Bangs are provided by the ``fess-webapp-bangs`` plugin, which requires |Fess| 15.9 or later. Install it from [System > Plugin] in the admin console or with ``bin/fess-setup install plugin fess-webapp-bangs`` (see :doc:`../admin/plugin-guide`), and restart |Fess|.

How a Bang Is Recognized
========================

- A bang is ``!`` followed by a trigger, written as a separate word. The trigger is case-insensitive.
- The bang is removed from the query, and the rest of the query is sent to the URL of the bang.
- When a query holds more than one defined bang, only the first one counts.
- A trigger that is not defined is not a bang. ``!unknown`` is searched as usual, and excludes the word ``unknown``.
- ``-g`` and ``NOT g`` still exclude the word ``g``. Only ``!g`` is a bang.

The search page and ``/api/v2/search`` follow the redirect: the API returns ``redirect_url`` (see :doc:`../api/api-search`), and the ``bootstrap`` theme bundled with |Fess| navigates to it. Other themes need the same handling.

Callers that cannot redirect, such as chat, MCP, the v1 and classic JSON APIs, and the admin search, do not send the search elsewhere. They drop the bang and search the rest of the query.

Defining Bangs
==============

Bangs are defined by the system property ``bangs.definitions``. Set it in ``app/WEB-INF/conf/system.properties``, or pass it as ``-Dfess.system.bangs.definitions=...``. A change in ``system.properties`` is picked up without restarting |Fess|.

The value is a whitespace-separated list of ``trigger=url`` entries. In the URL, ``{query}`` is replaced with the URL-encoded rest of the query:

::

    bangs.definitions=g=https://www.google.com/search?q={query} w=https://en.wikipedia.org/wiki/Special:Search?search={query}

- A trigger cannot contain whitespace, ``(``, ``)``, ``!``, ``"``, ``=`` or ``:``.
- Only absolute ``http`` or ``https`` URLs are accepted.
- An entry that does not follow these rules is not used. A warning is written to the |Fess| log, and the other entries stay in effect.
- If the same trigger is defined twice, the first definition is used.
- An empty value turns every bang off.

When ``bangs.definitions`` is not set, the following five bangs are available:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Trigger
     - Site
   * - ``g``
     - Google
   * - ``b``
     - Bing
   * - ``ddg``
     - DuckDuckGo
   * - ``w``
     - Wikipedia (English)
   * - ``gh``
     - GitHub

Setting ``bangs.definitions`` replaces this list. To keep the defaults and add one more, write all of the entries you need.

Related Topics
==============

- :doc:`search-not` - NOT search syntax
- :doc:`special-char` - Special characters and escaping
- :doc:`../api/api-search` - Search API
