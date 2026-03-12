===================
API Quick Start
===================

This page provides a practical guide to quickly start using the |Fess| API.

Get Started in 5 Minutes
========================

Prerequisites
-------------

- |Fess| is running (accessible at http://localhost:8080/)
- JSON response is enabled in Admin Panel > System > General

Try the Search API
------------------

**curl command examples:**

.. code-block:: bash

    # Basic search
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # Get 20 search results
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # Get page 2 (starting from result 21)
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # Search with label filter
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # Search with facets (aggregations)
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # Search with special characters (URL encoded)
    curl "http://localhost:8080/api/v1/documents?q=search%20engine"

**Example response (formatted):**

.. code-block:: json

    {
      "q": "fess",
      "exec_time": 0.15,
      "record_count": 125,
      "page_size": 20,
      "page_number": 1,
      "data": [
        {
          "title": "Fess - Open Source Enterprise Search Server",
          "url": "https://fess.codelibs.org/",
          "content_description": "<strong>Fess</strong> is an easy to deploy...",
          "host": "fess.codelibs.org",
          "mimetype": "text/html"
        }
      ]
    }

Try the Suggest API
-------------------

.. code-block:: bash

    # Get suggestions
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # Example response
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

Try the Label API
-----------------

.. code-block:: bash

    # Get available labels
    curl "http://localhost:8080/api/v1/labels"

Try the Health Check API
------------------------

.. code-block:: bash

    # Check server status
    curl "http://localhost:8080/api/v1/health"

    # Example response
    # {"data":{"status":"green","cluster_name":"fess"}}

Using Postman
=============

The |Fess| API can be easily used with Postman.

Collection Setup
----------------

1. Open Postman and create a new collection
2. Add the following requests:

**Search API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/documents``
- Query Parameters:
  - ``q``: Search keyword
  - ``num``: Number of results (optional)
  - ``start``: Start position (optional)

**Suggest API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/suggest``
- Query Parameters:
  - ``q``: Input string

**Label API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/labels``

Environment Variables
---------------------

We recommend using Postman environment variables to manage server URLs.

1. Create a new environment in "Environments"
2. Add variable: ``fess_url`` = ``http://localhost:8080``
3. Change request URL to ``{{fess_url}}/api/v1/documents``

Code Samples by Programming Language
====================================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # Fess server URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Call Fess Search API"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # Usage example
    results = search("enterprise search")
    print(f"Total hits: {results['record_count']}")
    for doc in results['data']:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v1/documents?${params}`);
      return response.json();
    }

    // Usage example
    search('enterprise search').then(results => {
      console.log(`Total hits: ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

JavaScript (Browser)
--------------------

.. code-block:: javascript

    // Using JSONP
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // Callback function
    function handleResults(results) {
      console.log(`Total hits: ${results.record_count}`);
    }

    // Usage example
    search('Fess', 'handleResults');

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
                .uri(URI.create(FESS_URL + "/api/v1/documents?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("enterprise search");
            System.out.println(result);
        }
    }

API Version Compatibility
=========================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess Version
     - API Version
     - Notes
   * - 15.x
     - v1
     - Latest version. Full feature support
   * - 14.x
     - v1
     - Similar API. Some parameter differences may exist
   * - 13.x
     - v1
     - Basic API support

.. note::

   API compatibility is maintained, but new features are only available in the latest version.
   For detailed differences between versions, refer to the `Release Notes <https://github.com/codelibs/fess/releases>`__.

Troubleshooting
===============

API Not Working
---------------

1. **Verify JSON response is enabled**

   Check that "JSON Response" is enabled in Admin Panel > System > General.

2. **CORS errors from browser**

   If you get CORS errors when accessing from a browser, use JSONP or
   configure CORS settings on the server.

   JSONP example:

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **Authentication required**

   If access tokens are configured, include them in the request header:

   .. code-block:: bash

       curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
            "http://localhost:8080/api/v1/documents?q=fess"

Next Steps
==========

- :doc:`api-search` - Search API details
- :doc:`api-suggest` - Suggest API details
- :doc:`admin/index` - Admin API usage

