===================
API Quick Start
===================

This page provides a practical guide to quickly start using the |Fess| API (v2).

Get Started in 5 Minutes
=========================

Prerequisites
-------------

- |Fess| is running (accessible at http://localhost:8080/)

Try the Search API
------------------

The v2 search endpoint is ``GET /api/v2/search``.

**curl command examples:**

.. code-block:: bash

    # Basic search
    curl "http://localhost:8080/api/v2/search?q=fess"

    # Get 20 search results
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # Get page 2 (starting from result 21)
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # Search with label filter
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # Search with facets (aggregations)
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # Search in Japanese (URL-encoded)
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**Example response (formatted):**

v2 responses are returned in the ``response`` envelope.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fess",
        "record_count": 125,
        "page_size": 20,
        "page_number": 1,
        "data": [
          {
            "title": "Fess - Open Source Enterprise Search Server",
            "url": "https://fess.codelibs.org/ja/",
            "content_description": "<strong>Fess</strong> is easy to deploy...",
            "host": "fess.codelibs.org",
            "mimetype": "text/html"
          }
        ]
      }
    }

Try the Suggest API
-------------------

The suggest endpoint is ``GET /api/v2/suggest-words``.

.. code-block:: bash

    # Get suggestions
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**Example response (formatted):**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fes",
        "suggest_words": [
          { "text": "fess", "types": ["document"] }
        ]
      }
    }

Try the Label API
-----------------

.. code-block:: bash

    # Get available label list
    curl "http://localhost:8080/api/v2/labels"

Try the Health Check API
------------------------

The health check endpoint is ``GET /api/v2/health``.

.. code-block:: bash

    # Check server (search engine cluster) status
    curl "http://localhost:8080/api/v2/health"

**Example response (formatted):**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess",
          "status": "green",
          "ping_status": 200
        }
      }
    }

Using Postman
=============

The |Fess| API can be easily used with Postman.

Collection Setup
----------------

1. Open Postman and create a new collection
2. Add the following requests:

**Search API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query Parameters:
  - ``q``: Search keyword
  - ``num``: Number of results (optional)
  - ``start``: Start position (optional)

**Suggest API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query Parameters:
  - ``q``: Input string

**Label API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

Environment Variables
---------------------

We recommend using Postman environment variables to manage server URLs.

1. Create a new environment in "Environments"
2. Add variable: ``fess_url`` = ``http://localhost:8080``
3. Change request URL to ``{{fess_url}}/api/v2/search``

Code Samples by Programming Language
======================================

All samples call ``GET /api/v2/search`` and reference the ``response`` envelope.

Python
------

.. code-block:: python

    import requests

    # Fess server URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Call the Fess Search API"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # Usage example
    results = search("Fess search")
    print(f"Hit count: {results['response']['record_count']}")
    for doc in results["response"]["data"]:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v2/search?${params}`);
      return response.json();
    }

    // Usage example
    search('Fess search').then(results => {
      console.log(`Hit count: ${results.response.record_count}`);
      results.response.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

Java
----

.. code-block:: java

    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.net.URLEncoder;
    import java.nio.charset.StandardCharsets;

    public class FessApiClient {
        private static final String FESS_URL = "http://localhost:8080";
        private final HttpClient client = HttpClient.newHttpClient();

        public String search(String query) throws Exception {
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(FESS_URL + "/api/v2/search?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("Fess search");
            System.out.println(result);
        }
    }

API Version Compatibility
==========================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess Version
     - API Version
     - Notes
   * - 15.x
     - v2
     - Latest version. Full feature support.
   * - 14.x
     - v1
     - Legacy API only.
   * - 13.x
     - v1
     - Basic API support.

.. note::

   In |Fess| 15.7, the former ``/api/v1`` JSON search API and chat API were discontinued.
   Clients using ``/api/v1`` should migrate to ``/api/v2``.
   For detailed differences between versions, refer to the `Release Notes <https://github.com/codelibs/fess/releases>`__.

Troubleshooting
===============

API Not Working
---------------

1. **Verify |Fess| is running**

   Confirm that http://localhost:8080/ is accessible.

2. **Verify the endpoint uses v2**

   Make sure the request path starts with ``/api/v2/...``.
   The legacy ``/api/v1`` endpoints have been discontinued.

3. **When authentication is required**

   For endpoints that require authentication, see :doc:`api-auth`.

Next Steps
==========

- :doc:`api-search` - Search API details
- :doc:`api-suggest` - Suggest API details
- :doc:`admin/index` - Admin API usage
