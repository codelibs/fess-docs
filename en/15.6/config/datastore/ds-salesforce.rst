==================================
Salesforce Connector
==================================

Overview
========

The Salesforce Connector provides functionality to retrieve data from Salesforce objects
(standard objects, custom objects) and register them in the |Fess| index.

This feature requires the ``fess-ds-salesforce`` plugin.

Supported Objects
=================

- **Standard Objects**: Account, Contact, Lead, Opportunity, Case, Solution, etc.
- **Custom Objects**: User-created custom objects
- **Knowledge Articles**: Salesforce Knowledge

Prerequisites
=============

1. Plugin installation is required
2. A Salesforce Connected App must be created
3. OAuth authentication must be configured
4. Read access to objects is required

Plugin Installation
-------------------

Install from the admin console under "System" -> "Plugins".

Or, see :doc:`../../admin/plugin-guide` for details.

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
     - Salesforce CRM
   * - Handler Name
     - SalesforceDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

OAuth Token authentication (recommended):

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

OAuth Password authentication:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``base_url``
     - Yes
     - Salesforce URL (Production: ``https://login.salesforce.com``, Sandbox: ``https://test.salesforce.com``)
   * - ``auth_type``
     - Yes
     - Authentication type (``oauth_token`` or ``oauth_password``)
   * - ``username``
     - Yes
     - Salesforce username
   * - ``client_id``
     - Yes
     - Connected App Consumer Key
   * - ``private_key``
     - For oauth_token
     - Private key (PEM format, newlines as ``\n``)
   * - ``client_secret``
     - For oauth_password
     - Connected App Consumer Secret
   * - ``security_token``
     - For oauth_password
     - User's security token
   * - ``number_of_threads``
     - No
     - Number of parallel processing threads (default: 1)
   * - ``ignoreError``
     - No
     - Continue processing on error (default: true)
   * - ``custom``
     - No
     - Custom object names (comma-separated)
   * - ``<object>.title``
     - No
     - Field name to use for title
   * - ``<object>.contents``
     - No
     - Field names to use for content (comma-separated)

Script Configuration
--------------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Available Fields
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``object.type``
     - Object type (e.g., Case, User, Solution)
   * - ``object.title``
     - Object name
   * - ``object.description``
     - Object description
   * - ``object.content``
     - Object text content
   * - ``object.id``
     - Object ID
   * - ``object.content_length``
     - Content length
   * - ``object.created``
     - Creation date/time
   * - ``object.last_modified``
     - Last modified date/time
   * - ``object.url``
     - Object URL
   * - ``object.thumbnail``
     - Thumbnail URL

Salesforce Connected App Configuration
======================================

1. Create Connected App
-----------------------

In Salesforce Setup:

1. Open "App Manager"
2. Click "New Connected App"
3. Enter basic information:

   - Connected App Name: Fess Crawler
   - API Name: Fess_Crawler
   - Contact Email: your-email@example.com

4. Check "Enable API (Enable OAuth Settings)"

2. Configure OAuth Token Authentication (Recommended)
-----------------------------------------------------

In OAuth settings:

1. Check "Use digital signatures"
2. Upload certificate (created using steps below)
3. Selected OAuth Scopes:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. Click "Save"
5. Copy Consumer Key

Creating the certificate:

::

    # Generate private key
    openssl genrsa -out private_key.pem 2048

    # Generate certificate
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # Verify private key
    cat private_key.pem

Upload the certificate (certificate.crt) to Salesforce and
set the private key (private_key.pem) contents in the parameter.

3. Configure OAuth Password Authentication
------------------------------------------

In OAuth settings:

1. Callback URL: ``https://localhost`` (not used but required)
2. Selected OAuth Scopes:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. Click "Save"
4. Copy Consumer Key and Consumer Secret

Obtaining security token:

1. Open personal settings in Salesforce
2. Click "Reset My Security Token"
3. Copy the token sent via email

4. Authorize Connected App
--------------------------

In "Manage" -> "Manage Connected Apps":

1. Select the created connected app
2. Click "Edit"
3. Change "Permitted Users" to "Admin approved users are pre-authorized"
4. Assign profiles or permission sets

Custom Object Configuration
===========================

Crawling Custom Objects
-----------------------

Specify custom object names in the ``custom`` parameter:

::

    custom=FessObj,CustomProduct,ProjectTask

Field mapping for each object:

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

Field Mapping Rules
~~~~~~~~~~~~~~~~~~~

- ``<object_name>.title`` - Field to use for title (single field)
- ``<object_name>.contents`` - Fields to use for content (comma-separated for multiple)

Usage Examples
==============

Crawl Standard Objects
----------------------

Parameters:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

Script:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl Custom Objects
--------------------

Parameters:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

Script:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Crawl Sandbox Environment
-------------------------

Parameters:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

Script:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

Troubleshooting
===============

Authentication Error
--------------------

**Symptom**: ``Authentication failed`` or ``invalid_grant``

**Check**:

1. For OAuth Token authentication:

   - Verify Consumer Key is correct
   - Verify private key is copied correctly (newlines should be ``\n``)
   - Verify certificate is uploaded to Salesforce
   - Verify username is correct

2. For OAuth Password authentication:

   - Verify Consumer Key and Consumer Secret are correct
   - Verify security token is correct
   - Verify password and security token are not concatenated (set separately)

3. Common:

   - Verify base_url is correct (production or sandbox environment)
   - Verify connected app is authorized

Cannot Retrieve Objects
-----------------------

**Symptom**: Crawl succeeds but 0 objects found

**Check**:

1. Verify user has read permissions on objects
2. For custom objects, verify object name is correct (API Name)
3. Verify field mapping is correct
4. Check logs for error messages

Custom Object Names
-------------------

Verify custom object API Name:

1. Open "Object Manager" in Salesforce Setup
2. Select the custom object
3. Copy the "API Name" (usually ends with ``__c``)

Example:

- Label: Product
- API Name: Product__c (use this)

Verify Field Names
------------------

Verify custom field API Name:

1. Open "Fields & Relationships" for the object
2. Select the custom field
3. Copy the "Field Name" (usually ends with ``__c``)

Example:

- Field Label: Product Description
- Field Name: Product_Description__c (use this)

API Rate Limiting
-----------------

**Symptom**: ``REQUEST_LIMIT_EXCEEDED``

**Resolution**:

1. Reduce ``number_of_threads`` (set to 1)
2. Increase crawl interval
3. Check Salesforce API usage
4. Purchase additional API limits if needed

Large Amount of Data
--------------------

**Symptom**: Crawl takes too long or times out

**Resolution**:

1. Split objects into multiple data stores
2. Adjust ``number_of_threads`` (around 2-4)
3. Distribute crawl schedules
4. Map only necessary fields

Private Key Format Error
------------------------

**Symptom**: ``Invalid private key format``

**Resolution**:

Verify private key newlines are correctly formatted as ``\n``:

::

    # Correct format
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Incorrect format (contains actual newlines)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-database` - Database Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
