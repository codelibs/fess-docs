==========================
Bulk Retrieval of Search Results
==========================

Overview
========

In |Fess| normal search, only a certain number of search results are displayed via paging functionality.
To retrieve all search results in bulk, use the Scroll Search feature.

This feature is useful when you need to process all search results,
such as bulk data export or backup, and large-scale data analysis.

Use Cases
=========

Scroll search is suitable for purposes such as:

- Exporting all search results
- Retrieving large amounts of data for analysis
- Data retrieval in batch processing
- Data synchronization to external systems
- Data collection for report generation

.. warning::
   Scroll search returns large amounts of data and consumes more server resources
   compared to normal search. Enable only when necessary.

Configuration
=============

Enabling Scroll Search
----------------------

By default, scroll search is disabled from security and performance perspectives.
To enable it, change the following setting in ``app/WEB-INF/classes/fess_config.properties`` or ``/etc/fess/fess_config.properties``.

::

    api.search.scroll=true

.. note::
   After changing settings, you must restart |Fess|.

Response Field Configuration
-----------------------------

You can customize fields included in search result responses.
By default, many fields are returned, but you can specify additional fields.

::

    query.additional.scroll.response.fields=content

When specifying multiple fields, list them separated by commas.

.. note::
   ``content`` is not included in default response fields.

Usage
=====

Basic Usage
-----------

Access scroll search using the following URL:

::

    http://localhost:8080/api/v1/documents/all?q=search keyword

Search results are returned in NDJSON (Newline Delimited JSON) format.
Each line outputs one document in JSON format.

**Example:**

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess"

Request Parameters
------------------

The following parameters can be used with scroll search:

.. note::
   Scroll search only supports the GET method.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Parameter Name
     - Description
   * - ``q``
     - Search query (required)
   * - ``num``
     - Number of items to retrieve per scroll (default: 10, max: 100)
   * - ``fields.label``
     - Filtering by label

.. note::
   The maximum value of ``num`` is controlled by ``paging.search.page.max.size`` (default: 100). Values exceeding the maximum are automatically capped.

Specifying Search Queries
--------------------------

You can specify search queries just like normal searches.

**Example: Keyword search**

::

    curl "http://localhost:8080/api/v1/documents/all?q=search engine"

**Example: Field-specific search**

::

    curl "http://localhost:8080/api/v1/documents/all?q=title:Fess"

**Example: Retrieve all (no search conditions)**

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*"

Specifying Retrieval Count
---------------------------

You can change the number of items retrieved per scroll.

::

    curl "http://localhost:8080/api/v1/documents/all?q=Fess&num=100"

.. note::
   The ``num`` parameter has a default maximum of 100.
   To allow larger values, change ``paging.search.page.max.size``.

Filtering by Label
------------------

You can retrieve only documents belonging to a specific label.

::

    curl "http://localhost:8080/api/v1/documents/all?q=*:*&fields.label=public"

About Authentication
--------------------

.. warning::
   Scroll search does not apply |Fess| role-based access control (RBAC).
   All documents matching the search criteria are returned regardless of user permissions.
   If access restrictions are needed, configure IP address restrictions or authentication via a reverse proxy.

Response Format
===============

NDJSON Format
-------------

Scroll search responses are returned in NDJSON (Newline Delimited JSON) format.
Each line represents one document.

**Example:**

::

    {"url":"http://example.com/page1","title":"Page 1","content":"..."}
    {"url":"http://example.com/page2","title":"Page 2","content":"..."}
    {"url":"http://example.com/page3","title":"Page 3","content":"..."}

Response Fields
---------------

Fields included by default:

- ``score``: Search score
- ``id``: Document ID
- ``doc_id``: Document ID (internal)
- ``boost``: Boost value
- ``content_length``: Content length
- ``host``: Hostname
- ``site``: Site
- ``last_modified``: Last modified date/time
- ``timestamp``: Timestamp
- ``mimetype``: MIME type
- ``filetype``: File type
- ``filename``: Filename
- ``created``: Creation date/time
- ``title``: Title
- ``digest``: Body excerpt
- ``url``: Document URL
- ``thumbnail``: Thumbnail
- ``click_count``: Click count
- ``favorite_count``: Favorite count
- ``config_id``: Config ID
- ``lang``: Language
- ``has_cache``: Cache availability

.. note::
   ``content`` (full text) is not included by default.
   It can be added via ``query.additional.scroll.response.fields``.

Data Processing Examples
========================

Python Processing Example
--------------------------

.. code-block:: python

    import requests
    import json

    # Execute scroll search
    url = "http://localhost:8080/api/v1/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # Process NDJSON response line by line
    for line in response.iter_lines():
        if line:
            doc = json.loads(line)
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Saving to File
--------------

Example of saving search results to a file:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=*:*" > all_documents.ndjson

Converting to CSV
-----------------

Example of converting to CSV using jq command:

.. code-block:: bash

    curl "http://localhost:8080/api/v1/documents/all?q=Fess" | \
        jq -r '[.url, .title, .score] | @csv' > results.csv

Data Analysis
-------------

Example of analyzing retrieved data:

.. code-block:: python

    import json
    import pandas as pd
    from collections import Counter

    # Read NDJSON file
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            documents.append(json.loads(line))

    # Convert to DataFrame
    df = pd.DataFrame(documents)

    # Basic statistics
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL domain analysis
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Performance and Best Practices
===============================

Efficient Usage
---------------

1. **Set appropriate num parameter**

   - Too small increases communication overhead
   - Too large increases memory usage
   - Default maximum: 100

2. **Optimize search conditions**

   - Specify search conditions to retrieve only necessary documents
   - Execute full retrieval only when truly necessary

3. **Use off-peak hours**

   - Retrieve large amounts of data during low system load periods

4. **Use in batch processing**

   - Execute periodic data synchronization as batch jobs

Optimizing Memory Usage
------------------------

When processing large amounts of data, use streaming processing to reduce memory usage.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v1/documents/all"
    params = {"q": "*:*", "num": 100}

    # Process with streaming
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                doc = json.loads(line)
                # Process document
                process_document(doc)

Security Considerations
=======================

Access Restrictions
-------------------

Since scroll search returns large amounts of data, set appropriate access restrictions.

1. **IP Address Restriction**

   Allow access only from specific IP addresses

2. **API Authentication**

   Use API tokens or Basic authentication

3. **Role-Based Restrictions**

   Allow access only to users with specific roles

Rate Limiting
-------------

To prevent excessive access, it is recommended to configure rate limiting with a reverse proxy.

Troubleshooting
===============

Cannot Use Scroll Search
------------------------

1. Verify that ``api.search.scroll`` is set to ``true``.
2. Verify that |Fess| was restarted.
3. Check error logs.

Timeout Errors Occur
--------------------

1. Reduce the ``num`` parameter to distribute processing.
2. Narrow search conditions to reduce amount of retrieved data.

Out of Memory Errors
--------------------

1. Reduce the ``num`` parameter.
2. Increase |Fess| heap memory size.
3. Check OpenSearch heap memory size.

Response is Empty
-----------------

1. Verify that the search query is correct.
2. Verify that specified labels or filter conditions are correct.
3. Verify role-based search permission settings.

References
==========

- :doc:`search-basic` - Search features details
- :doc:`search-advanced` - Search-related settings
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
