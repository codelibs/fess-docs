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
- File attachments (optional)

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

    token=xoxp-your-token-here
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
     - Yes
     - Target channels for crawling (comma-separated, or ``*all``)
   * - ``file_crawl``
     - No
     - Also crawl files (default: ``false``)
   * - ``include_private``
     - No
     - Include private channels (default: ``false``)

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
   * - ``message.text``
     - Message text content
   * - ``message.user``
     - Message sender's display name
   * - ``message.channel``
     - Channel name where message was sent
   * - ``message.timestamp``
     - Message sent date/time
   * - ``message.permalink``
     - Message permalink
   * - ``message.attachments``
     - Attachment fallback information

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

For public channels only:

- ``channels:history`` - Read public channel messages
- ``channels:read`` - Read public channel information

When including private channels (``include_private=true``):

- ``channels:history``
- ``channels:read``
- ``groups:history`` - Read private channel messages
- ``groups:read`` - Read private channel information

When also crawling files (``file_crawl=true``):

- ``files:read`` - Read file content

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

Troubleshooting
===============

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
4. Verify channel exists and is not archived

Cannot Retrieve Messages
------------------------

**Symptom**: Crawl succeeds but 0 messages found

**Check**:

1. Verify required scopes are granted:

   - ``channels:history``
   - ``channels:read``
   - For private channels: ``groups:history``, ``groups:read``

2. Verify messages exist in the channel
3. Verify app is added to the channel
4. Verify Slack app is enabled

Insufficient Permissions Error
------------------------------

**Symptom**: ``missing_scope``

**Resolution**:

1. Add required scopes in Slack App settings:

   **Public channels**:

   - ``channels:history``
   - ``channels:read``

   **Private channels**:

   - ``groups:history``
   - ``groups:read``

   **Files**:

   - ``files:read``

2. Reinstall the app
3. Restart |Fess|

Cannot Crawl Files
------------------

**Symptom**: Files not retrieved even with ``file_crawl=true``

**Check**:

1. Verify ``files:read`` scope is granted
2. Verify files are actually posted in the channel
3. Verify file access permissions

API Rate Limiting
-----------------

**Symptom**: ``rate_limited``

**Resolution**:

1. Increase crawl interval
2. Reduce number of channels
3. Split into multiple data stores and distribute schedules

Slack API limits:

- Tier 3 methods: 50+ requests/minute
- Tier 4 methods: 100+ requests/minute

Large Number of Messages
------------------------

**Symptom**: Crawl takes too long or times out

**Resolution**:

1. Split channels and configure multiple data stores
2. Distribute crawl schedules
3. Consider settings to exclude old messages

Advanced Script Examples
========================

Message Filtering
-----------------

Index only messages from a specific user:

::

    if (message.user == "John Doe") {
        title=message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

Messages containing specific keywords only:

::

    if (message.text.contains("important") || message.text.contains("incident")) {
        title="[Important] " + message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

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
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
