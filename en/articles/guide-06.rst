============================================================
Part 6: A Knowledge Hub for Development Teams -- Unified Search Across Code, Wiki, and Tickets
============================================================

Introduction
============

Software development teams use a variety of tools in their daily work.
Code lives in Git repositories, specifications in Confluence, tasks in Jira, and everyday communication in Slack.
Each tool has its own search functionality, but when you ask "Where did we discuss that?", searching each tool individually is inefficient.

In this article, we will aggregate information from the tools that development teams use daily into Fess and build a knowledge hub that enables unified search.

Target Audience
===============

- Software development team leaders and infrastructure administrators
- Anyone who wants to search across development-related tools
- Anyone who wants to learn the basics of using data store plugins

Scenario
========

We will enable unified search across the information of a development team of 20 members.

.. list-table:: Target Data Sources
   :header-rows: 1
   :widths: 20 30 50

   * - Tool
     - Purpose
     - Information to Search
   * - Git Repository
     - Source code management
     - Code, README, configuration files
   * - Confluence
     - Document management
     - Design documents, meeting minutes, procedures
   * - Jira
     - Ticket management
     - Bug reports, tasks, stories
   * - Slack
     - Communication
     - Technical discussions, decision records

What Is Data Store Crawling?
============================

Web crawling and file crawling collect documents by following URLs and file paths.
On the other hand, to collect information from SaaS tools, you use "data store crawling."

Data store crawling retrieves data through each tool's API and registers it in the Fess index.
Fess provides a data store plugin for each tool.

Installing Plugins
==================

Data store plugins can be installed from the Fess administration console.

1. Go to [System] > [Plugins] in the administration console
2. Review the list of installed plugins
3. Click the [Install] button to go to the installation screen, then install the required plugins from the [Remote] tab

For this scenario, we will use the following plugins:

- ``fess-ds-git``: Crawling Git repositories
- ``fess-ds-atlassian``: Crawling Confluence / Jira
- ``fess-ds-slack``: Crawling Slack messages

Configuring Each Data Source
============================

Git Repository Configuration
-----------------------------

Crawl Git repositories to make code and documents searchable.

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select GitDataStore as the handler name
3. Configure the parameters

**Parameter Configuration Example**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**Script Configuration Example**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

Specify the repository URL in ``uri`` and authentication credentials in ``username`` / ``password``. For private repositories, set an access token in ``password``. Use ``include_pattern`` to filter the file extensions to crawl using a regular expression.

Confluence Configuration
------------------------

Make Confluence pages and blog posts searchable.

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select ConfluenceDataStore as the handler name
3. Configure the parameters

**Parameter Configuration Example**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**Script Configuration Example**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

Specify the Confluence URL in ``home`` and select the authentication method with ``auth_type``. For Confluence Cloud, use ``basic`` authentication and set the API token in ``basic.password``.

Jira Configuration
------------------

Make Jira tickets (Issues) searchable.

Use the JiraDataStore handler included in the same ``fess-ds-atlassian`` plugin.
You can use JQL (Jira Query Language) to narrow down the tickets to crawl.
For example, you can target only tickets from a specific project or only tickets with a specific status (other than Closed).

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select JiraDataStore as the handler name
3. Configure the parameters

**Parameter Configuration Example**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**Script Configuration Example**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

Specify a JQL query in ``issue.jql`` to narrow down the tickets to crawl.

Slack Configuration
-------------------

Make Slack messages searchable.

1. Go to [Crawler] > [Data Store] > [Create New]
2. Select SlackDataStore as the handler name
3. Configure the parameters

**Parameter Configuration Example**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**Script Configuration Example**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

Specify the Slack Bot OAuth token in ``token``. Use ``channels`` to specify the channels to crawl; set ``*all`` to target all channels. To include private channels, set ``include_private=true`` and make sure the Bot has been invited to those channels.

Using Labels
============

Distinguishing Information Sources with Labels
-----------------------------------------------

By assigning labels to each data source, users can switch between information sources when searching.

- ``code``: Code from Git repositories
- ``docs``: Documents from Confluence
- ``tickets``: Tickets from Jira
- ``discussions``: Messages from Slack

Users can search across all sources with "All" and narrow down by label as needed.

Improving Search Quality
========================

Using Document Boost
--------------------

In a development team's knowledge hub, not all documents have the same importance.
For example, the following priority order might be appropriate:

1. Confluence documents (official specifications and procedures)
2. Jira tickets (latest issues and in-progress tasks)
3. Git repositories (code and README)
4. Slack messages (discussion records)

Document boost allows you to increase the search score of documents that match specific conditions.
You can configure boost values based on URL patterns or labels from [Crawler] > [Document Boost] in the administration console.

Using Related Content
---------------------

Displaying "related content" in search results can help users reach the information they are looking for.
For example, when searching for a design document in Confluence, it is useful to see related Jira tickets displayed as "related content."

Operational Considerations
==========================

Crawl Schedule
--------------

Set an appropriate crawl frequency for each data source.

.. list-table:: Schedule Example
   :header-rows: 1
   :widths: 25 25 50

   * - Data Source
     - Recommended Frequency
     - Reason
   * - Confluence
     - Every 4 hours
     - Document updates are moderately frequent
   * - Jira
     - Every 2 hours
     - Ticket updates are frequent
   * - Git
     - Daily
     - Aligned with the release cycle
   * - Slack
     - Every 4 hours
     - Real-time capability is not needed, but freshness matters

Handling API Rate Limits
------------------------

SaaS tool APIs have rate limits.
Set the crawl interval appropriately to avoid hitting API rate limits.
Slack API rate limits are particularly strict, so it is important to allow sufficient margin in the crawl interval.

Access Token Management
-----------------------

Data store plugin configurations require API access tokens for each tool.
From a security perspective, keep the following points in mind:

- Principle of least privilege: Use read-only access tokens
- Regular rotation: Update tokens periodically
- Dedicated accounts: Use service accounts instead of personal accounts

Summary
=======

In this article, we built a knowledge hub by aggregating information from the tools that development teams use daily into Fess, enabling unified search.

- Collected data from Git, Confluence, Jira, and Slack using data store plugins
- Provided a developer-friendly search experience with labels
- Controlled information priority with document boost
- Addressed operational considerations such as API rate limits and token management

With a development team knowledge hub, you can quickly find answers to questions like "Where was that discussion?" and "Where is that specification document?"

The next article will cover unified search across cloud storage.

References
==========

- `Fess Data Store Configuration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
