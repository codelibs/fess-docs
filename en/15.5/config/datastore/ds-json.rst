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

    files=/path/to/data.json
    fileEncoding=UTF-8

HTTP file:

::

    files=https://api.example.com/products.json
    fileEncoding=UTF-8

REST API (with authentication):

::

    files=https://api.example.com/v1/items
    fileEncoding=UTF-8

Multiple files:

::

    files=/path/to/data1.json,https://api.example.com/data2.json
    fileEncoding=UTF-8

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``files``
     - Yes
     - JSON file path or API URL (multiple allowed: comma-separated)
   * - ``fileEncoding``
     - No
     - Character encoding (default: UTF-8)
