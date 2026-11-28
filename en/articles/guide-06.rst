==================================================
Searching Your Team's Git, Confluence, Jira, Slack
==================================================

Introduction
============

A development team's information is split across tools: code and READMEs live in Git, design documents in Confluence, issues in Jira, and discussions in Slack.
Searching all four tools one after another every time you need to find "where was that specification decided?" is tedious.
With the Fess data store plugins, you can search the information in all four tools from a single search page.

If the configuration is wrong, however, you end up with situations like these:

- All Git files are registered with an empty URL, so the original file cannot be opened from the search results
- All Slack messages are shown with an empty title
- Messages from private channels appear in the search results of users who are not logged in
- Git files disappear from the index after a few days

For each tool, this article shows a minimal configuration that works as written, and explains how each setting avoids the pitfalls above.
The steps common to all data stores, such as installing plugins, writing the handler name, parameters and script, and creating jobs, are covered in :doc:`datastore-basics`.
Read that article first before continuing.
The settings in this article match Fess 15.9 and version 15.9.0 of each plugin.

What We Will Build
==================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - Tool
     - Plugin
     - Handler name
     - What to prepare on the tool side
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - An access token with read permission (must be able to clone over HTTPS)
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - An API token for the crawl account
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - The Bot User OAuth Token (``xoxb-``) of a Slack app

If you run Fess on Docker, you can install all of the plugins at startup by listing the plugin names and versions, separated by spaces, in the ``FESS_PLUGINS`` environment variable.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

If you install them from the admin console or with ``fess-setup``, restart Fess after installation.

Decide First: Who Can See the Search Results
============================================

When you create a new data store configuration, the "Permissions" field is prefilled with ``{role}guest``.
If you leave it as is, the imported information can be found by users who are not logged in.

The Git, Confluence and Jira plugins do not carry the access rights of the original tool over into Fess.
Everything the crawl account can read is imported, and it is visible to anyone who has a role or group written in the "Permissions" field.
You therefore decide the scope by combining the following two points:

- Replace ``{role}guest`` in the "Permissions" field with the people who should see the content (e.g. ``{group}developers``)
- Narrow what is imported to what those people may see, using the permissions of the crawl account, and ``jira.jql`` and ``include_pattern`` described later

Only the Slack plugin can import the members of private channels as permissions (described later).
For how groups and roles work, see :doc:`guide-05`.

Git Repositories
================

Preparation
-----------

``fess-ds-git`` clones over HTTPS.
SSH URIs (the ``git@...`` form) are not supported.
For private repositories, create an access token for reading.
For a GitHub classic token, that is the ``repo`` scope; for GitLab, the ``read_repository`` scope.

Parameters and Script
---------------------

In [Crawler] > [Data Store] > [Create New], select ``GitDataStore`` as the "Handler Name".

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

Each line means the following:

- ``base_url``: the script's ``url`` is ``base_url`` concatenated as is with the path within the repository. If you omit it, ``url`` becomes an empty string, and all files get the same document ID and overwrite each other. End it with ``/``, and make the branch name match the branch being crawled (by default the remote's default branch; to change it, use ``commit_id``).
- ``username`` / ``password``: used for authentication only when both are specified. Do not embed the token in ``uri``; write it in ``password`` (``password`` is encrypted when saved, but ``uri`` is not).
- ``include_pattern``: a regular expression that must match the entire path within the repository (e.g. ``docs/setup.md``). It is not a URL.
- ``title=path``: with ``name``, which is only the file name, files with the same name such as ``README.md`` cannot be told apart in the search results, so the path is used instead.

Differential Crawling and Expiration
------------------------------------

When a crawl succeeds, ``fess-ds-git`` writes its commit ID back to ``prev_commit_id`` in the "Parameters" field.
From the second crawl on, it registers only the files in the diff from the previous commit, and deletes the documents of files that were deleted or renamed (reflecting deletions requires ``base_url``).

This differential crawling does not work well with Fess's document expiration, which is why the example above specifies ``time_to_live``.
Data store documents are given an expiration date when they are registered.
By default it is determined by "Delete old documents" in [System] > [General] (3 days by default), and documents past their expiration are deleted by the "Doc Purger" job, which runs every minute.
In differential crawling, unchanged files are not registered again, so their expiration is not extended and they disappear a few days after the first crawl.
``time_to_live`` is a parameter that specifies the expiration of this configuration's documents in minutes; ``5256000`` is about 10 years.

For the same reason, changes to the script, ``base_url``, ``include_pattern`` or the "Permissions" field are not reflected in unchanged files.
To register all files again, follow these steps:

1. In [System Info] > [Search], search for ``label:code`` and delete the old documents with [Delete All by this Query]
2. Clear the value of ``prev_commit_id=`` in the "Parameters" field and save
3. Run the job

If you changed the "Permissions" field or ``base_url``, the document IDs change, so old documents remain if you skip step 1.
When you delete this data store configuration, also delete its documents first with step 1.

Confluence
==========

On Atlassian Cloud, create an API token with the crawl account and use it as the Basic authentication password.
What is imported are the pages and blog posts in the spaces that this account can view.
Select ``ConfluenceDataStore`` as the "Handler Name".

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home`` works with or without ``/wiki``. On Cloud, ``/wiki`` is added for Confluence.
- If ``deployment`` is omitted, it is treated as ``cloud`` when the host name ends with ``.atlassian.net``, and as ``datacenter`` otherwise.
- Adding ``content.comments`` makes the page's comments searchable as part of the body. The comments are concatenated, separated by blank lines.
- ``include_pattern`` is matched against the entire document URL. On Cloud, page URLs have the form ``https://<site>/wiki/spaces/<space-key>/pages/<page-id>``, so you can narrow by space key. Data Center URLs (``/pages/viewpage.action?pageId=...``) do not contain the space key, so this method cannot be used there.

On Data Center, set ``deployment=datacenter``, and to use a personal access token, specify ``auth_type=pat`` and ``pat.token``.

Jira
====

Authentication is the same as for Confluence.
Select ``JiraDataStore`` as the "Handler Name" and narrow the issues to import with JQL.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

The JQL parameter is named ``jira.jql``.
The old name ``issue.jql`` still works, but the log shows the warning ``Parameter "issue.jql" is deprecated``.
The old name is scheduled to be removed in 16.0.
If ``jira.jql`` is omitted, ``created is not empty`` is used, which means every issue the account can view.

Adding ``issue.comments`` puts the issue's comments into the body as well, separated by blank lines, so they become searchable.
Comments are fetched through the API for each issue, which increases the number of calls (see the rate limits described later).

Slack
=====

Preparing the Slack App
-----------------------

Create an app at https://api.slack.com/apps and add the following scopes to Bot Token Scopes under [OAuth & Permissions]; then install the app to your workspace.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Scope
     - When it is needed
   * - ``channels:read``, ``channels:history``, ``users:read``, ``team:read``
     - Always
   * - ``groups:read``, ``groups:history``
     - To import private channels (``include_private=true``)
   * - ``users:read.email``
     - To use private channel members as permissions (``permission_sync=true``)
   * - ``files:read``
     - To import files as well (``file_crawl=true``)

Without ``team:read``, the plugin calls ``chat.getPermalink`` for every message, which greatly increases the number of API calls.
After installation, add the app to each channel you want to import.
Channels the app has not joined are skipped with a warning.

Create two separate data store configurations: one for public channels and one for private channels.
The reason is explained in the "Private Channels" section.

Public Channels
---------------

Select ``SlackDataStore`` as the "Handler Name", and set the "Permissions" field to the people who should see the public channels.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

``message.title`` is always an empty string for messages, so if you write ``title=message.title``, every result has no title.
As in the example above, build the title from the poster and the channel name.
Thread replies are also registered as individual documents.
System messages such as ``channel_join`` are excluded by default (``ignore_system_events=true``).

Private Channels
----------------

With ``permission_sync=true``, the plugin creates a user role for each member from the email addresses of the private channel's members and puts them in ``message.roles``.
However, the values of ``default_permissions`` and the "Permissions" field are also added to this value.
Public channels have no roles of their own, so if both of these are empty, documents from public channels are visible to no one.
Conversely, if you put the audience for public channels in either of them, that audience can also see the documents from private channels.
Because a single configuration cannot handle both correctly, private channels get a separate configuration.

In the second data store configuration, delete ``{role}guest`` from the "Permissions" field to leave it empty, and list the names of the private channels to import in ``channels``.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- If you do not write ``role=message.roles``, the computed roles are not used. In that case, the warning ``no script value references message.roles`` is shown when the crawl starts.
- If you mix public channels into ``channels``, their documents have empty roles and are visible to no one.
- With this configuration, the warning ``default_permissions is not set and this crawl's DataConfig permission field is empty`` is shown when the crawl starts. As long as no public channels are included, this is not a problem.
- Channels whose members could not be retrieved, or for which not a single email address could be resolved (for example, because ``users:read.email`` was forgotten), are not imported in that crawl. They are recorded in [System Info] > [Failure URL] with the channel ID and channel name.

At search time, the user name of the user logged in to Fess is matched against these email addresses.
The Fess user name must therefore match the Slack email address.
Slack handles email addresses in lowercase, so Fess user names should be lowercase too.
Users who do not match simply do not see the private channel documents; they never see anyone else's documents.
For which value becomes the user name when users log in with SSO, see :doc:`guide-15`.

If you had already imported private channels without ``permission_sync``, those documents remain without permissions until they expire.
Delete those documents in [System Info] > [Search] before crawling with this configuration.

Labels, Boost and Schedules
===========================

Labels are assigned by the ``label="..."`` line in each script above.
To show them as filters on the search page, create labels with the same values (``code``, ``docs``, ``tickets``, ``slack``) in [Crawler] > [Label].
Note that if a label has "Included Paths" that match the document URL, the script's label is lost (:doc:`datastore-basics`).

Rules in [Crawler] > [Document Boost] are not applied to data store documents.
To rank Confluence design documents above Slack messages, raise the "Boost" (initial value ``1.0``) of the Confluence data store configuration.
The value is multiplied into the search score, so change it gradually and compare the search results.

To run each tool at a different frequency, use [Create New Job] on the details page of each data store configuration (:doc:`datastore-basics`).

API Rate Limits
===============

The Slack and Atlassian plugins automatically retry ``429`` and ``5xx`` responses, and if there is a ``Retry-After`` header, they wait that many seconds (up to 60 seconds for Slack).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Plugin
     - Adjustable parameters
   * - Slack
     - ``read_interval`` (wait time per message, in milliseconds, default ``0``), ``max_retry_count`` (default ``3``), ``retry_interval`` (wait time before the first retry, in milliseconds, default ``3000``; doubled on each retry, up to 60 seconds)
   * - Atlassian
     - ``read_interval`` (minimum interval between API calls, in milliseconds, default ``0``; shared between threads). The number of retries and their interval are fixed

When Slack exhausts its retries, the crawl is aborted.
The status in the job log stays "OK", so check it with the steps in the next section.

Verifying the Results
=====================

How to read job results and logs is explained in :doc:`datastore-basics`.
A data store crawl can fail while the job is still shown as "OK", so judge by document counts and logs.
For the setup in this article, also check the following:

1. In [System Info] > [Search], search for each of ``label:code``, ``label:docs``, ``label:tickets`` and ``label:slack``, and confirm that the count is not 0
2. Open the URL of a Git document and confirm that the repository file is displayed. If ``fess-crawler.log`` contains the warning ``base_url is blank``, review ``base_url``
3. Open the details page of the Git configuration and confirm that ``prev_commit_id`` has been written back to the parameters
4. While logged out, search for a word that appears only in a private channel, and confirm that nothing is found
5. Log in as a member of that channel and confirm that the same word is found

If it is not found in step 5, check whether the Fess user name matches the Slack email address, and whether ``fess-crawler.log`` contains the warning ``private channel(s) skipped``.
If an entire configuration fails, for example because of an authentication error, it is recorded per configuration in [System Info] > [Failure URL].

Summary
=======

- For Git, always specify ``base_url``, and add ``time_to_live`` so that documents do not expire under differential crawling.
- For Confluence and Jira, import comments too with ``content.comments`` / ``issue.comments``, and write JQL in ``jira.jql``.
- For Slack, build the title from ``message.user`` and ``message.channel``.
- Git, Confluence and Jira do not carry over the original permissions, so decide who can see the content with the "Permissions" field and the import scope.
- Put Slack private channels in a separate configuration, and import them with ``permission_sync=true``, ``role=message.roles`` and an empty "Permissions" field.
- Adjust the priority of each information source with the "Boost" of its data store configuration.

References
==========

- `Git Connector <https://fess.codelibs.org/stable/config/datastore/ds-git.html>`__
- `Atlassian Connector <https://fess.codelibs.org/stable/config/datastore/ds-atlassian.html>`__
- `Slack Connector <https://fess.codelibs.org/stable/config/datastore/ds-slack.html>`__
- `Data Store Crawling <https://fess.codelibs.org/stable/admin/dataconfig-guide.html>`__
- `General Settings <https://fess.codelibs.org/stable/admin/general-guide.html>`__
- `fess-ds-slack 15.9.0 README (scopes and permission sync) <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
