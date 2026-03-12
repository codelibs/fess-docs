==================================
JSON Connector
==================================

Overview
========

The JSON Connector provides functionality to retrieve data from JSON files or JSON APIs
and register them in the |Fess| index.

This feature requires the ``fess-ds-json`` plugin.

Prerequisites
=============

1. Plugin installation is required
2. Access to JSON files or APIs is required
3. Understanding of JSON structure is necessary

Plugin Installation
-------------------

Method 1: Place JAR file directly

::

    # Download from Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Place the file
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # or
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Method 2: Install from admin console

1. Open "System" -> "Plugins"
2. Upload the JAR file
3. Restart |Fess|

Configuration
=============

Configure in the admin console under "Crawler" -> "Data Store" -> "Create New".

Basic Settings
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Item
     - Example
   * - Name
     - Products JSON
   * - Handler Name
     - JsonDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

Local file:

::

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

HTTP file:

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

REST API (with authentication):

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

Multiple files:

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``file_path``
     - Yes
     - JSON file path or API URL (multiple allowed: comma-separated)
   * - ``encoding``
     - No
     - Character encoding (default: UTF-8)
   * - ``json_path``
     - No
     - JSONPath for data extraction (default: ``$``)
   * - ``http_method``
     - No
     - HTTP method (GET, POST, etc., default: GET)
   * - ``auth_type``
     - No
     - Authentication type (bearer, basic)
   * - ``auth_token``
     - No
     - Authentication token (for bearer authentication)
   * - ``auth_username``
     - No
     - Authentication username (for basic authentication)
   * - ``auth_password``
     - No
     - Authentication password (for basic authentication)
   * - ``http_headers``
     - No
     - Custom HTTP headers (JSON format)

Script Configuration
--------------------

Simple JSON object:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

Nested JSON object:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

Processing array elements:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

Available Fields
~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - JSON object field
- ``data.<parent>.<child>`` - Nested object
- ``data.<array>[<index>]`` - Array element
- ``data.<array>.<method>`` - Array method (join, length, etc.)

JSON Format Details
===================

Simple Array
------------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

Parameters:

::

    json_path=$

Nested Structure
----------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

Parameters:

::

    json_path=$.data.products

Script:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

Complex Array
-------------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

Parameters:

::

    json_path=$.articles

Script:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

Using JSONPath
==============

What is JSONPath
----------------

JSONPath is a query language for specifying elements within JSON.
It is equivalent to XPath for XML.

Basic Syntax
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Syntax
     - Description
   * - ``$``
     - Root element
   * - ``$.field``
     - Top-level field
   * - ``$.parent.child``
     - Nested field
   * - ``$.array[0]``
     - First element of array
   * - ``$.array[*]``
     - All elements of array
   * - ``$..field``
     - Recursive search

JSONPath Examples
-----------------

Target all elements (root):

::

    json_path=$

Target specific array:

::

    json_path=$.data.items

Nested array:

::

    json_path=$.response.results.products

Recursive search:

::

    json_path=$..products

Usage Examples
==============

Product Catalog API
-------------------

API response:

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": 1200,
            "category": "Computers",
            "in_stock": true
          }
        ]
      }
    }

Parameters:

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Price: $" + data.price
    digest=data.category
    price=data.price

Blog Articles API
-----------------

API response:

::

    {
      "posts": [
        {
          "id": 1,
          "title": "Article Title",
          "body": "Article body text...",
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          },
          "tags": ["technology", "programming"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

Parameters:

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

Script:

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

Bearer Authentication API
-------------------------

Parameters:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

Basic Authentication API
------------------------

Parameters:

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

Script:

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

Using Custom Headers
--------------------

Parameters:

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Combining Multiple JSON Files
-----------------------------

Parameters:

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

POST Request
------------

Parameters:

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

Script:

::

    url="https://example.com/result/" + data.id
    title=data.title
    content=data.content

Troubleshooting
===============

File Not Found
--------------

**Symptom**: ``FileNotFoundException`` or ``404 Not Found``

**Check**:

1. Verify file path or URL is correct
2. Verify file exists
3. For URLs, verify API is running
4. Check network connection

JSON Parse Error
----------------

**Symptom**: ``JsonParseException`` or ``Unexpected character``

**Check**:

1. Verify JSON file format is correct:

   ::

       # Validate JSON
       cat data.json | jq .

2. Verify character encoding is correct
3. Check for invalid characters or line breaks
4. Verify no comments are included (comments not allowed in standard JSON)

JSONPath Error
--------------

**Symptom**: Cannot retrieve data, or empty results

**Check**:

1. Verify JSONPath syntax is correct
2. Verify target element exists
3. Test JSONPath with a validation tool:

   ::

       # Verify using jq
       cat data.json | jq '$.data.products'

4. Verify path points to correct hierarchy

Authentication Error
--------------------

**Symptom**: ``401 Unauthorized`` or ``403 Forbidden``

**Check**:

1. Verify authentication type is correct (bearer, basic)
2. Verify authentication token or username/password is correct
3. Check token expiration
4. Check API permission settings

Cannot Retrieve Data
--------------------

**Symptom**: Crawl succeeds but 0 items found

**Check**:

1. Verify JSONPath points to correct element
2. Verify JSON structure
3. Verify script configuration is correct
4. Verify field names are correct (including case sensitivity)
5. Check logs for error messages

Array Processing
----------------

When JSON is an array:

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

Parameters:

::

    json_path=$

When JSON is an object containing an array:

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

Parameters:

::

    json_path=$.items

Large JSON Files
----------------

**Symptom**: Out of memory or timeout

**Resolution**:

1. Split JSON files into multiple smaller files
2. Use JSONPath to extract only necessary parts
3. For APIs, use pagination
4. Increase |Fess| heap size

API Rate Limiting
-----------------

**Symptom**: ``429 Too Many Requests``

**Resolution**:

1. Increase crawl interval
2. Check API rate limits
3. Use multiple API keys for load distribution

Advanced Script Examples
========================

Conditional Processing
----------------------

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Joining Arrays
--------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

Setting Default Values
----------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "Untitled"
    content=data.description || data.summary || "No description"
    price=data.price || 0

Date Formatting
---------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Numeric Processing
------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-csv` - CSV Connector
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
