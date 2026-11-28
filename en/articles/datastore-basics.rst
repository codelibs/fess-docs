==========================
Data Store Crawling Basics
==========================

Introduction
============

The contents of Google Drive, Slack or a database cannot be made searchable with web crawling or file crawling.
A CSV file crawled as a file also becomes a single document, so its rows cannot be searched individually.
Fess handles these sources as "data stores" and imports them record by record through plugins (data store connectors).

The data store settings screen has different fields from the web and file system settings screens.
You have to write yourself which values become the URL, the title and so on, and with the default values the documents are registered so that they can be searched without logging in.
Even when processing fails, the job may be shown as "OK".

This article explains the mechanisms common to all connectors, based on Fess 15.9.
Using a small example with a CSV file, we go through the whole process: installing the plugin, configuring, running, and checking the results.
For connector-specific authentication and parameters, see the articles and references listed at the end.

How It Differs from Web and File Crawling
=========================================

In web crawling and file crawling, Fess follows links and folders and automatically extracts the title and body from the documents it fetches.
In data store crawling, a connector reads records from an API or a file.
Which value of a record goes into which field of the index is written in the "Script" of the configuration.

Fess itself does not include any data store handlers.
The "Handler Name" drop-down in [Crawler] > [Data Store] lists only the handlers provided by the installed ``fess-ds-*`` plugins.

Data store configurations also differ in the following ways (explained in later sections).

- The settings screen has no "Label" field
- The rules in [Crawler] > [Document Boost] are not applied

Installing the Plugin
=====================

Here we use the CSV connector ``fess-ds-csv`` as an example.
Match the plugin version to the minor version of the Fess you are using (15.9.x for Fess 15.9).

To install it from the admin console, go to [System] > [Plugin] and click [Install].
On the [Remote] tab, select ``fess-ds-csv`` from the drop-down and click [Install].
To use a jar file you have at hand, use the [Local] tab.

In environments installed from the ZIP package or RPM / DEB, you can also install it from the command line.

.. code-block:: bash

    bin/fess-setup install plugin fess-ds-csv:15.9.0

With Docker, add ``FESS_PLUGINS`` to the ``environment`` of ``fess01`` in ``compose.yaml`` so that the plugin is installed at startup.
To install several plugins, separate them with spaces (not commas).

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-csv:15.9.0"

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

With Docker, a plugin installed from the admin console is placed inside the container, so it disappears when the container is recreated.
With Docker, ``FESS_PLUGINS`` is the more reliable way.
Changing an environment variable and running ``up -d`` recreates the container.
For the settings that are lost at that point, see :doc:`guide-02`.

If you installed the plugin from the admin console or with ``fess-setup``, restart Fess (``FESS_PLUGINS`` installs plugins before Fess starts, so no restart is needed).
After the restart, the plugin is installed if ``CsvDataStore`` appears in "Handler Name" under [Crawler] > [Data Store] > [Create New].

The Three Main Fields of the Settings Screen
============================================

A data store configuration centers on three fields: "Handler Name", "Parameters" and "Script".

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - Handler Name
     - The connector to use. Examples: ``CsvDataStore``, ``SlackDataStore``
   * - Parameters
     - Instructions for the connector. One ``key=value`` per line (the files to read, the connection target, credentials and so on)
   * - Script
     - The mapping to fields of the index. One ``field=expression`` per line

``script_type`` in the Parameters
---------------------------------

On the create screen, the "Parameters" field already contains ``script_type=javascript``.
This specifies that the expressions in the "Script" field are evaluated as JavaScript.
Keep this line and add the connector parameters below it.

If you delete the ``script_type`` line, the script is evaluated as Groovy (the default, so that configurations created before 15.9 keep working).
Evaluating with Groovy requires the ``fess-script-groovy`` plugin.
It is included in the standard Docker image but not in the slim image.
In an environment without the plugin, evaluating a line that contains an expression fails with the error ``groovy is not found``, and the record is not registered (a line whose right-hand side is only an item name, such as ``title=subject``, uses the value as is without going through a script engine).
Conversely, with the standard Docker image, the configuration keeps working with Groovy even if you delete the line, which makes the problem hard to notice.
When you paste an example from a connector's reference into the "Parameters" field, make sure not to delete the ``script_type=javascript`` line.

Writing the Script
------------------

Each line in the "Script" field has an index field name on the left-hand side and a JavaScript expression on the right-hand side.
Enclose strings in double quotation marks.
Do not put a semicolon at the end of a line.
With a semicolon, the value of the expression becomes ``null`` and nothing is set for that field.
No error or log message is produced, so the only way to notice is that the field is empty (for details, see "JavaScript Scripting Guide" in the references at the end).

The item names you can refer to on the right-hand side differ by connector.

- The CSV, JSON and database connectors refer to column names and field names directly (CSV columns can also be referred to as ``cell1``, ``cell2``, ...)
- Many cloud connectors pass the fetched object with a prefix. For example, Box, Google Drive and OneDrive use ``file.*``, Slack uses ``message.*``, Jira uses ``issue.*``, and Salesforce uses ``object.*``

Check the available item names in the script description of each connector's reference (``https://fess.codelibs.org/stable/config/datastore/ds-<name>.html``).
If you refer to an undefined name, for example writing ``url`` where it should be ``file.url``, evaluating the expression fails and the record is not registered.

Example: Making a CSV File Searchable
=====================================

In this example, an internal FAQ is maintained as a CSV file, and we make it searchable.
Save the following content as ``faq.csv`` in UTF-8.

.. code-block:: text

    faq_id,question,answer
    1,When is the deadline for expense reports,Submit your expense reports by the end of each month.
    2,How do I connect to internal systems from outside the office,Connect using the VPN client.
    3,What should I do if I lose my building pass,Contact the General Affairs Department and ask for a new one.

A CSV file saved by Excel is often not in UTF-8 but in a legacy encoding; for example, Japanese Excel saves it in MS932.
In that case, specify the encoding in the parameters shown below, such as ``file_encoding=MS932``.
Place the file at a path that the Fess crawler can read.
The crawler runs on the same server as Fess, so in a ZIP or RPM / DEB environment, place it in a directory that the user running Fess can read.
If you are just trying it out with Docker, copying the file into the container is the easiest way (it disappears when the container is recreated).

.. code-block:: bash

    docker cp faq.csv fess01:/tmp/faq.csv

In [Crawler] > [Data Store], click [Create New] and enter the following.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Field
     - Value
   * - Name
     - Internal FAQ
   * - Handler Name
     - ``CsvDataStore``
   * - Parameters
     - See below
   * - Script
     - See below
   * - Permissions
     - Leave ``{role}guest`` as is (the FAQ may be searched without logging in)

Parameters:

.. code-block:: properties

    script_type=javascript
    files=/tmp/faq.csv
    file_encoding=UTF-8
    has_header_line=true

Script:

.. code-block:: javascript

    url="https://intranet.example.com/faq/" + faq_id
    title=question
    content=question + " " + answer
    digest=answer
    label="faq"

With ``has_header_line=true``, the column names in the first line (``faq_id``, ``question``, ``answer``) can be referred to in the script.
For ``url``, specify the URL of a page that can display the record, which opens when the link in the search results is clicked.
The URL in this example is fictitious.
Replace it with the URL of your actual FAQ page.

After saving with [Create], create and run a job as described in the "Scheduling" section below, and check the results as described in the "Checking the Results" section.
If everything works, searching for "VPN" on the search page while logged out (or in a private browser window) finds the second FAQ entry.
Documents with ``{role}guest`` are shown to users who are not logged in and to users who have the ``guest`` role (including the initial user ``admin``). They are not shown when you are logged in as any other user.

To show the label ``faq`` in the search page's filter, create a label whose "Value" is ``faq`` in [Crawler] > [Label] (see the next section, "Labels").

Index Fields
============

The fields commonly set in a script are as follows.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Field
     - Description
   * - ``url``
     - Required. The link target in search results. Must be unique for each record
   * - ``title``
     - The heading in search results. Searchable
   * - ``content``
     - The body. Searchable
   * - ``digest``
     - The summary shown in search results
   * - ``label``
     - The label value (described later)
   * - ``role``
     - The roles that can view the document. Used when the connector provides ACLs (described later)

In addition, ``config_id``, ``boost``, ``role``, ``virtual_host``, ``mimetype`` and others are set automatically (``boost``, ``role`` and ``virtual_host`` are the values of "Boost", "Permissions" and "Virtual Hosts" on the settings screen).
If the script specifies the same field, the script value overwrites it.

Note the following about ``url``.

- A record whose expression evaluates to ``null`` is not registered. The CSV connector does not record such rows as failure URLs; it only writes one WARN line with the count to ``fess-crawler.log``
- The document ID is built from the URL, the roles and the virtual host. Records whose ``url`` is an empty string, or records with the same ``url``, get the same document ID if their roles and virtual host are also the same; they overwrite each other and only the last one remains

Permissions
===========

On the create screen, "Permissions" already contains ``{role}guest``.
This value becomes the role of every document registered from that data store.
The guest role is given to users who are not logged in, so as it is, the documents can be searched without logging in.
For data that may be public, such as an internal FAQ, you can leave it as is.

For data whose viewers you want to restrict, control access in one of the following ways.

- Change the "Permissions" field to the groups or roles that should see the data (for example ``{group}sales``). All documents in the data store get the same permissions
- If the connector builds roles from the sharing settings (ACLs) of the source service, map them in the script, for example ``role=file.roles``. The item name differs by connector (``message.roles`` for Slack), and some connectors need additional parameters to fetch ACLs (such as ``permission_sync=true`` for Slack). Check each connector's reference

When you use ACLs, delete ``{role}guest`` from the "Permissions" field.
Connectors such as Box, Slack and Microsoft 365 (OneDrive) also include the value of the "Permissions" field in ``file.roles`` / ``message.roles``.
So if you leave ``{role}guest``, the documents remain searchable without logging in even though ACLs are configured.

Conversely, if you leave the "Permissions" field empty and do not set ``role`` in the script either, the documents get no roles at all.
Such documents are not shown to anyone on the search page.

Roles are written when documents are registered.
If you change the permissions or the script, existing documents are not updated until they are crawled again.
Designing roles and groups is explained in :doc:`guide-05`.

Labels
======

The data store settings screen does not have the "Label" field that the web and file system settings screens have.
To assign labels, use one of the following.

- Write ``label="faq"`` or similar in the script. The label is assigned to all documents of that data store
- In [Crawler] > [Label], write a regular expression that matches the document URLs in "Included Paths". At registration time, the URL is matched against this regular expression and the label is assigned to matching documents

"Included Paths" is evaluated as a match against the whole URL, so to match by prefix, append ``.*`` (for example ``https://intranet\.example\.com/faq/.*``).

Note: a label assigned in the script is lost if even one label in [Crawler] > [Label] matches the document's URL; only the matching labels remain.
Labels created for web crawling (for example ``https://intranet\.example\.com/.*``) and labels that set only "Excluded Paths" are also subject to matching.
When you assign labels in the script, make sure that no label matches the document URLs.

Specify the label "Value" using only alphanumeric characters and underscores (hyphens and non-ASCII characters such as Japanese cannot be used).
To show the label among the label choices on the search page, register a label with the same value in [Crawler] > [Label], even when you assign it in the script.
In that case, "Included Paths" can be left empty.

Boost
=====

The "Boost" value on the data store settings screen (default ``1.0``) is set on every document registered from that data store.
The boost value is multiplied into the score at search time.
To rank documents from a particular data source higher, change this boost value.

The rules in [Crawler] > [Document Boost] apply only to documents registered by web crawling and file crawling.
They are not applied to data store documents.

Scheduling
==========

The default job "Default Crawler" runs daily at 0:00 and crawls all enabled web, file system and data store configurations.
To run each data store at a different frequency, create a job for each configuration.

1. In the list in [Crawler] > [Data Store], click the configuration name to open its details screen
2. Click [Create New Job]. The scheduler create screen opens with "Name" (``Data Crawler - Internal FAQ``) and a script that crawls only this configuration already filled in
3. Enter the run time in "Schedule" in cron format (minute hour day month day-of-week) and click [Create]. Example: ``0 2 * * *`` (daily at 2:00)

A job with an empty "Schedule" does not run periodically; it runs only when started manually.
To try it right away, open the job you created in [System] > [Scheduler] and click [Start Now].

Even after you create a job for a configuration, "Default Crawler" continues to crawl that configuration as well.
To avoid running it twice, disable the "Status" of that data store configuration.
"Default Crawler" targets only enabled configurations, but a job that specifies a configuration ID also crawls disabled configurations.
If you create a dedicated job for every configuration, you can also empty the "Schedule" of "Default Crawler" (see :doc:`guide-04`).

Document Expiration
===================

Documents registered from a data store have an expiration time.
It is the start time of that crawl plus the number of days in "Delete old documents" under [System] > [General] (default ``3`` days).
Expired documents are removed from the index by the "Doc Purger" job, which runs every minute.
When the same document is registered again by the next crawl, its expiration is extended.

As a result, documents disappear from the search results in the following two cases.

- The interval between job runs is longer than the number of days in "Delete old documents"
- In incremental crawling, which reads only changed items (such as ``incremental=true`` for Git or Google Drive), unchanged documents are not registered again

To change the expiration per configuration, specify ``time_to_live`` in minutes in the parameters (for example ``time_to_live=11520`` for 8 days).
Items deleted from the source data also disappear from the search results only when this expiration passes.
If you make the expiration too long, deletions take a very long time to be reflected.

Checking the Results
====================

In data store crawling, a job status of "OK" does not necessarily mean success.
Even when an exception occurs in the connector, Fess records it per configuration or per record and continues processing.
As a result, the job log status becomes "OK", and "Crawler Status" in [System Info] > [Crawling Info] does not change either.
Check the following in order.

1. In [System Info] > [Job Log], confirm that the job has finished. The ``Data Config Id:`` line of "Result" shows the target configuration ID
2. In [System Info] > [Crawling Info], check "Index Size (Data Store)" of that session. This is the number of documents registered in that session (for "Default Crawler", the total of all data stores)
3. In [System Info] > [Failure URL], check that no errors have been recorded
4. Download ``fess-crawler.log`` from [System Info] > [Log File] and check the ERROR and WARN lines (it is in ``/var/log/fess/`` for Docker and RPM / DEB, and in ``logs/`` for the ZIP package)
5. In [System Info] > [Search], search for something like ``label:faq`` and check the number of hits

Where the clues are left depends on how the crawl fails.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Situation
     - Failure URL
     - fess-crawler.log
   * - The handler is not found (for example, the plugin was removed after the configuration was created)
     - Not recorded
     - ``DataStore(...) is not found.``
   * - The whole configuration fails (an authentication error that prevents the connector from continuing, a missing required parameter, and so on)
     - One entry. The URL column is ``D<config ID>:<config name>``
     - ``Failed to process a data crawling: <config name>``
   * - A single record fails (a script evaluation error, and so on)
     - One per record. For CSV, ``<file path>:<line number>``
     - WARN lines

With the CSV connector, it is not an error either when the file specified in ``files`` is not found or when its extension is not ``.csv`` / ``.tsv``.
The connector logs the WARN messages ``is not found.`` and ``No CSV file.`` and finishes with 0 documents.

[System Info] > [Search] shows all documents without filtering by permissions, which makes it suitable for checking the number of documents.
On the other hand, it cannot be used to check whether the permissions are as intended.
Check permissions on the regular search page while logged in as the target user (or logged out, for documents with ``{role}guest``) (:doc:`guide-05`).

If you do not know which item names a connector passes, some connectors write the fetched values to the log when the crawler log level is set to DEBUG (the CSV connector outputs the values of each row).
For how to configure this, see "Debug Configuration" in `Data Store Connector Overview <https://fess.codelibs.org/stable/config/datastore/ds-overview.html>`__.

Connector-Specific Articles and References
==========================================

The settings for each connector are explained in the following articles.

- :doc:`guide-06` - Git, Confluence, Jira, Slack
- :doc:`guide-07` - Google Drive, SharePoint Online / OneDrive, Box
- :doc:`guide-12` - Databases, CSV, Salesforce

References:

- `Data Store Connector Overview <https://fess.codelibs.org/stable/config/datastore/ds-overview.html>`__ (a list of all connectors and their plugin names)
- `CSV Connector <https://fess.codelibs.org/stable/config/datastore/ds-csv.html>`__ / `JSON Connector <https://fess.codelibs.org/stable/config/datastore/ds-json.html>`__ / `Database Connector <https://fess.codelibs.org/stable/config/datastore/ds-database.html>`__
- `Google Drive <https://fess.codelibs.org/stable/config/datastore/ds-gsuite.html>`__ / `Microsoft 365 <https://fess.codelibs.org/stable/config/datastore/ds-microsoft365.html>`__ / `Box <https://fess.codelibs.org/stable/config/datastore/ds-box.html>`__
- `Atlassian <https://fess.codelibs.org/stable/config/datastore/ds-atlassian.html>`__ / `Slack <https://fess.codelibs.org/stable/config/datastore/ds-slack.html>`__ / `Git <https://fess.codelibs.org/stable/config/datastore/ds-git.html>`__ / `Salesforce <https://fess.codelibs.org/stable/config/datastore/ds-salesforce.html>`__
- `Data Store Crawling (admin console) <https://fess.codelibs.org/stable/admin/dataconfig-guide.html>`__ / `Scheduler <https://fess.codelibs.org/stable/admin/scheduler-guide.html>`__ / `Plugin <https://fess.codelibs.org/stable/admin/plugin-guide.html>`__ / `Label <https://fess.codelibs.org/stable/admin/labeltype-guide.html>`__ / `JavaScript Scripting Guide <https://fess.codelibs.org/stable/config/scripting-javascript.html>`__
