==================================
Slack Connector
==================================

Overview
========

The Slack Connector provides functionality to retrieve channel messages from Slack workspaces
and register them in the |Fess| index.

This feature requires the ``fess-ds-slack`` plugin.

Supported Content
=================

- Public channel messages
- Private channel messages
- Thread reply messages (retrieved via ``conversations.replies``)
- File attachments (optional)

The following are out of scope:

- System event messages (``channel_join``, ``channel_topic``, ``pinned_item``, etc.) are
  excluded from indexing by default (``ignore_system_events``)
- Direct messages (DMs) and group DMs
- Huddle transcripts and Clips (Slack has no public API for these, so they cannot be crawled)

Prerequisites
=============

1. Plugin installation is required
2. Slack App creation and permission configuration is required
3. OAuth Access Token must be obtained

Plugin Installation
-------------------

Install from the admin console under "System" -> "Plugins":

1. Download ``fess-ds-slack-X.X.X.jar`` from Maven Central
2. Upload and install from the plugin management screen
3. Restart |Fess|

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
     - Company Slack
   * - Handler Name
     - SlackDataStore
   * - Enabled
     - On

Parameter Configuration
-----------------------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

Parameter List
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Required
     - Description
   * - ``token``
     - Yes
     - Slack app OAuth Access Token
   * - ``channels``
     - No
     - Target channels for crawling (comma-separated, or ``*all``). If not specified, all channels are fetched (same behavior as ``*all``)
   * - ``file_crawl``
     - No
     - Also crawl files (default: ``false``)
   * - ``include_private``
     - No
     - Include private channels (default: ``false``)
   * - ``number_of_threads``
     - No
     - Number of parallel processing threads (default: ``1``)
   * - ``max_filesize``
     - No
     - Maximum file size in bytes to crawl (default: ``10000000``)
   * - ``ignore_error``
     - No
     - Continue processing on error (default: ``true``)
   * - ``supported_mimetypes``
     - No
     - Regex for allowed MIME types (default: ``.*``)
   * - ``include_pattern``
     - No
     - Regex pattern for URLs to include
   * - ``exclude_pattern``
     - No
     - Regex pattern for URLs to exclude
   * - ``proxy_host``
     - No
     - HTTP proxy host
   * - ``proxy_port``
     - No
     - HTTP proxy port (required when ``proxy_host`` is specified)
   * - ``file_types``
     - No
     - File type filter for Slack API (default: ``all``)
   * - ``channel_count``
     - No
     - Number of channels per API page (default: ``100``)
   * - ``message_count``
     - No
     - Number of messages per API page (default: ``100``)
   * - ``file_count``
     - No
     - Number of files per API page (default: ``20``)
   * - ``user_count``
     - No
     - Number of users per API page (default: ``100``)
   * - ``user_cache_size``
     - No
     - Maximum number of entries in the user information cache (default: ``10000``)
   * - ``bot_cache_size``
     - No
     - Maximum number of entries in the bot information cache (default: ``10000``)
   * - ``channel_cache_size``
     - No
     - Maximum number of entries in the channel information cache (default: ``10000``)

Advanced Parameters
~~~~~~~~~~~~~~~~~~~

The following parameters control connection and retry behavior, fine-grained crawl scope, and
permission synchronization:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Description
   * - ``connection_timeout``
     - Connection timeout for each Slack API request, in milliseconds (default: ``20000``)
   * - ``read_timeout``
     - Read timeout for each Slack API request, in milliseconds (default: ``20000``)
   * - ``max_retry_count``
     - Maximum number of retries after a ``429`` (rate limited) or ``5xx`` response (default: ``3``)
   * - ``retry_interval``
     - Wait time, in milliseconds, before the first retry when the response carries no ``Retry-After`` header (default: ``3000``). Doubles with each further attempt, capped at ``60000`` milliseconds. When the response has a ``Retry-After`` header, that value (in seconds) is used instead
   * - ``executor_timeout``
     - Seconds to wait, at the end of a crawl, for queued work to finish before forcing shutdown (default: ``60``)
   * - ``exclude_archived``
     - Whether to exclude archived channels from the ``conversations.list`` results (default: ``false``). When set to ``true``, an archived channel specified by name in ``channels`` can no longer be resolved (see Troubleshooting for details)
   * - ``ignore_system_events``
     - Whether to exclude Slack-generated channel administration messages (``channel_join``, ``channel_topic``, ``pinned_item``, etc.) from indexing (default: ``true``)
   * - ``read_interval``
     - Wait time, in milliseconds, after processing each message or file (default: ``0`` = no wait). Use this to slow down the crawl against a rate-limited workspace
   * - ``max_content_length``
     - Maximum number of characters the content extractor (Tika) may extract from a file (default: unset, deferring to Fess's per-MIME-type limit). ``max_filesize`` is the transfer-side limit that rejects files by size before download, while ``max_content_length`` is the extraction-side limit on the amount of text extracted after download; the two work independently. Lowering ``max_filesize`` does not substitute for ``max_content_length`` (for example, a 1MB archive can expand into far more text once extracted)
   * - ``permission_sync``
     - Whether to convert private channel membership into search permissions (roles) (default: ``false``). See "Permission Synchronization (ACL)" below for details
   * - ``default_permissions``
     - Additional permissions applied to every indexed document regardless of channel membership (``{user}``/``{group}``/``{role}`` format, comma-separated, default: empty). Applied only when ``permission_sync`` is enabled

.. note::

   ``ignore_system_events`` defaults to ``true``. Even an existing crawl configuration that
   does not set this parameter will, after upgrading |Fess|, stop indexing system event
   messages such as ``channel_join`` -- the number of indexed documents will drop with no
   error or warning. Set ``ignore_system_events=false`` explicitly to keep indexing these
   messages as before.

Script Configuration
--------------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Available Fields
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``message.title``
     - Title (empty string for messages, file name and title for file entries)
   * - ``message.text``
     - Message text content (for file entries, the file name and the extracted file body)
   * - ``message.user``
     - Message sender's display name (if not set, resolved in the order of real name, user name, then user ID)
   * - ``message.channel``
     - Channel name where message was sent
   * - ``message.timestamp``
     - Message sent date/time
   * - ``message.permalink``
     - Message permalink
   * - ``message.attachments``
     - Attachment fallback information
   * - ``message.roles``
     - The list of search permissions (roles) allowed to see this message or file. Present only when ``permission_sync=true``. Unless the script maps ``role=message.roles``, the computed roles are never reflected in the indexed document

Slack App Configuration
=======================

1. Create Slack App
-------------------

Access https://api.slack.com/apps:

1. Click "Create New App"
2. Select "From scratch"
3. Enter app name (e.g., Fess Crawler)
4. Select workspace
5. Click "Create App"

2. Configure OAuth & Permissions
--------------------------------

In the "OAuth & Permissions" menu:

**Add to Bot Token Scopes**:

Base scopes (always required):

- ``channels:history`` - Read public channel messages
- ``channels:read`` - Read public channel information
- ``users:read`` - Read user information (required for display name resolution)
- ``team:read`` - Read workspace information. ``team.info`` is called on every crawl, so this
  scope is required; without it, this connector falls back to an extra
  ``chat.getPermalink`` call for every message, greatly increasing the number of API calls

When also including private channels (``include_private=true``):

- ``groups:history`` - Read private channel messages
- ``groups:read`` - Read private channel information

When also crawling files (``file_crawl=true``):

- ``files:read`` - Read file content

When also synchronizing private channel permissions (``permission_sync=true``):

- ``users:read.email`` - Read member email addresses (required for permission synchronization)

3. Install the App
------------------

In the "Install App" menu:

1. Click "Install to Workspace"
2. Review permissions and click "Allow"
3. Copy the "Bot User OAuth Token" (starts with ``xoxb-``)

.. note::
   Normally use the Bot User OAuth Token that starts with ``xoxb-``,
   but User OAuth Token starting with ``xoxp-`` can also be used in parameters.

4. Add to Channels
------------------

Add the app to target channels for crawling:

1. Open the channel in Slack
2. Click on the channel name
3. Select the "Integrations" tab
4. Click "Add apps"
5. Add the created app

Permission Synchronization (ACL)
================================

The Slack Connector can convert a private channel's membership into |Fess| search
permissions (roles), so that only that channel's members can search its content. This
feature is disabled by default.

.. note::

   ``permission_sync`` only computes roles; it does not apply them automatically. Only after
   you add ``role=message.roles`` to the script are the computed roles reflected in indexed
   documents. Forgetting this mapping still pays for the extra API calls and skipped private
   channels that ``permission_sync=true`` causes, while providing no access control at all.

Enabling It
-----------

1. Add the ``users:read.email`` scope to the Slack App (required to resolve member email addresses)
2. Set ``permission_sync=true`` in the parameters
3. Add ``role=message.roles`` to the script

Parameters:

::

    include_private=true
    permission_sync=true

Script:

::

    role=message.roles

Fail-Closed Behavior
--------------------

A private channel is not indexed at all in a given crawl if any of the following applies
(this fails closed: the risk is under-indexing, never accidentally exposing content to
everyone):

- Retrieving the channel's member list failed
- The member list came back empty (this happens when the crawling token's own bot user is
  not itself a member of the private channel)
- The channel has members, but none of their email addresses could be resolved (usually
  because the ``users:read.email`` scope is missing)

Public channels never call ``conversations.members`` and are always treated as visible to
everyone.

Principal Name Matching
-----------------------

Search-time permission checks use the |Fess| login name (the principal name). Because the
roles this feature computes are derived from Slack email addresses, the |Fess| login name
must match the Slack email address. Slack normalizes email addresses to lowercase, so keep
|Fess| login names lowercase as well. A mismatch does not expose another user's content --
it simply means the affected user's searches always return zero results, which can be easy
to mistake for an unrelated bug.

Other Notes
-----------

- Slack user groups are not used; permissions are computed directly from each member's
  email address
- ``default_permissions`` lets you grant additional permissions to every document regardless
  of channel membership (applied only when ``permission_sync=true``)
- Leaving ``permission_sync=false`` while setting ``include_private=true`` indexes private
  channel content using only the permissions configured on the data store's "Permission"
  field; if that field is left empty, the content is effectively public to everyone
- Enabling ``permission_sync`` later does not retroactively secure content already indexed
  by an earlier, unrestricted crawl. To apply roles to that content, set
  ``permission_sync=true`` and ``role=message.roles``, then re-crawl

Usage Examples
==============

Crawl Specific Channels
-----------------------

Parameters:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

Script:

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Crawl All Channels
------------------

Parameters:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

Script:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Crawl Including Private Channels
--------------------------------

Parameters:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

Script:

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\nAttachments: " + message.attachments
    created=message.timestamp
    url=message.permalink

Crawl Including Files
---------------------

Parameters:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

Script:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Include Detailed Message Information
------------------------------------

Script:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Crawl With Permission Sync
--------------------------

Restrict private channel content so that only that channel's members can search it. Add the
``users:read.email`` scope to the Slack App beforehand.

Parameters:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

Script:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::
   If you forget ``role=message.roles``, the computed roles are never reflected in the
   indexed documents. See "Permission Synchronization (ACL)" for details.

Troubleshooting
===============

How Error Handling Works
------------------------

The Slack Connector treats Slack API errors as one of three kinds:

- **Fatal errors** (``invalid_auth``, ``token_revoked``, ``account_inactive``,
  ``missing_scope``, ``not_authed``, ``token_expired``): the token itself cannot be used, so
  the entire crawl job fails
- **Transient errors** (``ratelimited``, ``internal_error``, ``fatal_error``,
  ``service_unavailable``, ``request_timeout``): if retrying does not resolve the error, the
  entire crawl job fails (see "API Rate Limiting" below for the retry behavior)
- **Channel-scoped errors** (``channel_not_found``, ``not_in_channel``, etc.): only that
  channel is skipped with a warning, and crawling continues with the next channel

In earlier versions, a fatal error could still be reported as a "successful" crawl that
silently indexed zero or only some documents. This three-way split now ensures that fatal
and transient errors are always reported as a job failure.

Authentication Error
--------------------

**Symptom**: ``invalid_auth`` or ``not_authed``

**Check**:

1. Verify token is copied correctly
2. Verify token format:

   - Bot User OAuth Token: starts with ``xoxb-``
   - User OAuth Token: starts with ``xoxp-``

3. Verify app is installed to workspace
4. Verify required permissions are granted

Channel Not Found
-----------------

**Symptom**: ``channel_not_found``

**Check**:

1. Verify channel name is correct (# is not needed)
2. Verify app is added to the channel
3. For private channels, set ``include_private=true``
4. Check whether ``exclude_archived=true`` is set. By default (``exclude_archived=false``),
   archived channels are still listed and crawled; only when set to ``true`` does an archived
   channel specified by name in ``channels`` fail to resolve

Cannot Retrieve Messages
------------------------

**Symptom**: Crawl succeeds, but few or no documents are indexed

**Check**:

1. ``ignore_system_events`` defaults to ``true``. If a channel's messages are all system
   events such as ``channel_join``, zero documents are indexed for it (see "Advanced
   Parameters")
2. Verify messages actually exist in the channel
3. Verify app is added to the channel
4. With ``permission_sync=true``, a private channel whose membership cannot be resolved is
   not indexed in that crawl (fail-closed; see "Permission Synchronization (ACL)")

.. note::

   In earlier versions, a missing scope (``missing_scope``) could still let the crawl
   "succeed" with zero messages. Fatal errors, including ``missing_scope``, now fail the
   entire crawl job. If your job is failing, check "Insufficient Permissions Error" below
   instead of this section.

Insufficient Permissions Error
------------------------------

**Symptom**: ``missing_scope`` (fails the entire crawl job)

**Resolution**:

1. Add required scopes in Slack App settings:

   **Base** (always required):

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **Private channels**:

   - ``groups:history``
   - ``groups:read``

   **Files**:

   - ``files:read``

   **Permission synchronization** (``permission_sync=true``):

   - ``users:read.email``

2. Reinstall the app
3. Restart |Fess|

Cannot Crawl Files
------------------

**Symptom**: Files not retrieved even with ``file_crawl=true``

**Check**:

1. Verify ``files:read`` scope is granted
2. Verify files are actually posted in the channel
3. Verify file access permissions
4. A file larger than ``max_filesize`` is not downloaded (check the log for a warning)

API Rate Limiting
-----------------

**Symptom**: ``ratelimited`` (fails the entire crawl job)

**Resolution**:

1. If the default ``max_retry_count`` and ``retry_interval`` do not resolve it, increase them
2. Set ``read_interval`` to slow down the crawl
3. Reduce the number of channels, or split into multiple data stores and distribute schedules

A Slack API ``ratelimited`` error is retried automatically: using the ``Retry-After``
header's value, in seconds, when present, or otherwise an exponential backoff starting from
``retry_interval`` (up to ``max_retry_count`` attempts, capped at 60 seconds). If the error
persists after every retry is exhausted, the entire crawl job fails.

Slack API tiers (call-frequency limits):

- Tier 1: 1+ requests/minute
- Tier 2: 20+ requests/minute -- ``conversations.list``, ``users.list`` (fetched
  unconditionally in full at the start of every crawl, making this the tier most likely to
  be exhausted)
- Tier 3: 50+ requests/minute -- ``conversations.history``, ``conversations.replies``,
  ``files.list``
- Tier 4: 100+ requests/minute -- ``conversations.members`` (only when
  ``permission_sync=true``), ``files.info``

.. note::

   Slack's May 29, 2025 rate limit tightening (limiting ``conversations.history`` and
   ``conversations.replies`` to 50+ requests/minute) applies only to apps distributed outside
   the workspace that created them, such as through the Slack Marketplace. It does not apply
   to an internal app created for |Fess| that is installed only in the workspace that created
   it.

Large Number of Messages
------------------------

**Symptom**: Crawl takes too long or times out

**Resolution**:

1. Split channels and configure multiple data stores
2. Distribute crawl schedules

Advanced Script Examples
========================

Message Processing
------------------

Summarize long messages:

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

Format channel name:

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

Reference Information
=====================

- :doc:`ds-overview` - Data Store Connector Overview
- :doc:`ds-atlassian` - Atlassian Connector
- :doc:`../../admin/dataconfig-guide` - Data Store Configuration Guide
- :doc:`../security-role` - Role-Based Search Configuration
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
