================================
Bulk Retrieval of Search Results
================================

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
- Retrieving large amounts of data for data analysis
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
To enable it, change the following setting in ``app/WEB-INF/classes/fess_config.properties`` (or
``/etc/fess/fess_config.properties`` for RPM/DEB packages).

::

    api.search.scroll=true

.. note::
   After changing settings, you must restart |Fess|.

Scroll Context Lifetime
-----------------------

The scroll context lifetime for scroll search is fixed internally in |Fess| at ``1m`` (1 minute).
This value cannot be changed from ``fess_config.properties``.

.. note::
   There is a setting called ``index.scroll.search.timeout``, but it is used for internal operations
   involving index updates or deletions (update by query / delete by query) and does not affect
   the timeout for this feature (search scrolling).

Response Field Configuration
-----------------------------

You can customize the fields included in search result responses.
By default, many fields are returned, but you can also specify additional fields.

::

    query.additional.scroll.response.fields=content

When specifying multiple fields, list them separated by commas.

.. note::
   The ``content`` field is not included in the default response.
   To retrieve full text, add it using the setting above.

Usage
=====

Basic Usage
-----------

Access scroll search using the following URL:

::

    http://localhost:8080/api/v2/documents/all?q=search keyword

Search results are returned in NDJSON (Newline Delimited JSON) format.
Each line outputs one document in JSON format.

**Example:**

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess"

Request Parameters
------------------

The following parameters can be used with scroll search:

.. note::
   Scroll search only supports the GET method. Accessing with any method other than GET returns
   ``405 Method Not Allowed``.

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
   The maximum value of ``num`` is controlled by ``paging.search.page.max.size`` (default: 100).
   Values exceeding the maximum are automatically capped.
   The default value uses ``paging.search.page.size`` (default: 10).
   If a value of 0 or less is specified for ``num``, an error (``INVALID_REQUEST``) is returned.

Specifying Search Queries
--------------------------

You can specify search queries just like normal searches.

**Example: Keyword search**

::

    curl "http://localhost:8080/api/v2/documents/all?q=search engine"

**Example: Field-specific search**

::

    curl "http://localhost:8080/api/v2/documents/all?q=title:Fess"

**Example: Retrieve all (no search conditions)**

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*"

Specifying Retrieval Count
---------------------------

You can change the number of items retrieved per scroll.

::

    curl "http://localhost:8080/api/v2/documents/all?q=Fess&num=100"

.. note::
   Increasing the ``num`` parameter too much will increase memory usage.
   The default maximum is 100. If a larger value is needed, change the
   ``paging.search.page.max.size`` setting.

Filtering by Label
------------------

You can retrieve only documents belonging to a specific label.

::

    curl "http://localhost:8080/api/v2/documents/all?q=*:*&fields.label=public"

About Access Control
--------------------

.. note::
   Scroll search applies role-based access control (RBAC) just like normal search.
   Only documents accessible based on the role information in the request are returned;
   documents for which the user does not have view permissions are not included in the results.

.. warning::
   The scroll search endpoint does not require authentication by default (anyone can access it).
   However, the documents returned are filtered by the role-based access control described above.
   If you wish to restrict access to the endpoint itself, configure IP address restrictions or
   authentication via a reverse proxy or similar mechanism.

Response Format
===============

NDJSON Format
-------------

Scroll search responses are returned in NDJSON (Newline Delimited JSON) format.
The Content-Type is ``application/x-ndjson; charset=UTF-8``.
Each line represents one document wrapped in the ``{"data": {...}}`` format.

**Example:**

::

    {"data":{"url":"http://example.com/page1","title":"Page 1","digest":"..."}}
    {"data":{"url":"http://example.com/page2","title":"Page 2","digest":"..."}}
    {"data":{"url":"http://example.com/page3","title":"Page 3","digest":"..."}}

.. note::
   Each document is stored under the ``data`` key. On the client side, parse each line and
   then refer to the value of the ``data`` key.

Error Behavior
--------------

If an error occurs on the server side after the stream has started being sent, the following
error terminator line is output as the final line of the response.

::

    {"error":{"code":"internal_error","message":"stream error"}}

.. note::
   On the client side, you can determine whether the stream completed successfully or whether
   a server-side error occurred mid-stream by checking whether the final line contains the
   ``error`` key. Note that if writing the error terminator line itself fails, the terminator
   line will not be output and the stream will end mid-way; treat unexpected disconnections
   as errors as well.

Response Fields
---------------

Fields included by default:

- ``score``: Search score
- ``_id``: Document ID (OpenSearch document ID)
- ``doc_id``: Document ID (internal to |Fess|)
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
- ``has_cache``: Cache availability
- ``content_title``: Display title
- ``content_description``: Display body excerpt
- ``url_link``: Display link URL
- ``site_path``: Site path

.. note::
   The fields actually output are limited to those permitted as API response fields.
   Fields with no value are not output.

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
    url = "http://localhost:8080/api/v2/documents/all"
    params = {
        "q": "Fess",
        "num": 100
    }

    response = requests.get(url, params=params, stream=True)

    # Process NDJSON response line by line
    for line in response.iter_lines():
        if line:
            record = json.loads(line)
            if "error" in record:
                # An error occurred mid-stream
                print("stream error:", record["error"])
                break
            doc = record["data"]
            print(f"Title: {doc.get('title')}")
            print(f"URL: {doc.get('url')}")
            print("---")

Saving to File
--------------

Example of saving search results to a file:

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=*:*" > all_documents.ndjson

Converting to CSV
-----------------

Example of converting to CSV using the jq command:

.. code-block:: bash

    curl "http://localhost:8080/api/v2/documents/all?q=Fess" | \
        jq -r '.data | [.url, .title, .score] | @csv' > results.csv

Data Analysis
-------------

Example of analyzing retrieved data:

.. code-block:: python

    import json
    import pandas as pd

    # Read NDJSON file (extract the data key from each line)
    documents = []
    with open('all_documents.ndjson', 'r') as f:
        for line in f:
            record = json.loads(line)
            if "data" in record:
                documents.append(record["data"])

    # Convert to DataFrame
    df = pd.DataFrame(documents)

    # Basic statistics
    print(f"Total documents: {len(df)}")
    print(f"Average score: {df['score'].mean()}")

    # URL domain analysis
    df['domain'] = df['url'].apply(lambda x: x.split('/')[2])
    print(df['domain'].value_counts())

Performance and Best Practices
================================

Efficient Usage
---------------

1. **Set an appropriate num parameter**

   - Too small increases communication overhead
   - Too large increases memory usage
   - Default maximum: 100

2. **Optimize search conditions**

   - Specify search conditions to retrieve only necessary documents
   - Execute full retrieval only when truly necessary

3. **Use off-peak hours**

   - Retrieve large amounts of data during periods of low system load

4. **Use in batch processing**

   - Execute periodic data synchronization as batch jobs

Optimizing Memory Usage
------------------------

When processing large amounts of data, use streaming processing to reduce memory usage.

.. code-block:: python

    import requests
    import json

    url = "http://localhost:8080/api/v2/documents/all"
    params = {"q": "*:*", "num": 100}

    # Process with streaming
    with requests.get(url, params=params, stream=True) as response:
        for line in response.iter_lines(decode_unicode=True):
            if line:
                record = json.loads(line)
                if "error" in record:
                    break
                # Process document
                process_document(record["data"])

Security Considerations
=======================

Access Restrictions
-------------------

Since scroll search returns large amounts of data, configure appropriate access restrictions.
The endpoint does not require authentication by default, so consider the following measures as needed.

1. **IP Address Restriction**

   Allow access only from specific IP addresses

2. **API Authentication**

   Use API tokens or Basic authentication via a reverse proxy or similar mechanism

3. **Role-Based Access Control**

   Documents returned are filtered by |Fess| role-based access control

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
2. Narrow search conditions to reduce the amount of retrieved data.

Out of Memory Errors
--------------------

1. Reduce the ``num`` parameter.
2. Increase the |Fess| heap memory size.
3. Check the OpenSearch heap memory size.

Response is Empty
-----------------

1. Verify that the search query is correct.
2. Verify that specified labels or filter conditions are correct.
3. Role-based access control means documents for which the user does not have view permissions are not included in the results. Verify the role settings on the request.

References
==========

- :doc:`search-basic` - Search features details
- :doc:`search-advanced` - Search-related settings
- `OpenSearch Scroll API <https://opensearch.org/docs/latest/api-reference/scroll/>`_
