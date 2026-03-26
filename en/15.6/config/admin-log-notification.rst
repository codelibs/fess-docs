================
Log Notification
================

Overview
========

|Fess| has a feature that automatically captures ERROR and WARN level log events and notifies administrators.
This feature enables rapid detection of system anomalies and early initiation of incident response.

Key features:

- **Supported notification channels**: Email, Slack, Google Chat
- **Target processes**: Main application, crawler, suggest generation, thumbnail generation
- **Disabled by default**: Since this is an opt-in feature, it must be explicitly enabled

How It Works
============

Log notification operates through the following flow:

1. Log4j2's ``LogNotificationAppender`` captures log events at or above the configured level.
2. Captured events are accumulated in an in-memory buffer (up to 1,000 entries).
3. A timer flushes the buffered events to an OpenSearch index (``fess_log.notification_queue``) at 30-second intervals.
4. A scheduled job reads events from OpenSearch at 5-minute intervals, groups them by log level, and sends notifications.
5. After notifications are sent, processed events are deleted from the index.

.. note::
   Logs from the notification feature itself (such as ``LogNotificationHelper`` and ``LogNotificationJob``)
   are excluded from notification targets to prevent infinite loops.

Setup
=====

Enabling
--------

Enabling from the Administration Screen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Log in to the administration screen.
2. Select "General" from the "System" menu.
3. Enable the "Log Notification" checkbox.
4. Select the target level in "Log Notification Level" (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Click the "Update" button.

.. note::
   By default, only ``ERROR`` level events are targeted for notification.
   If you select ``WARN``, both ``WARN`` and ``ERROR`` events will be notified.

Enabling via Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also enable the feature by directly editing ``fess_config.properties``.

::

    log.notification.enabled=true
    log.notification.level=ERROR

Notification Destination Configuration
--------------------------------------

Email Notification
~~~~~~~~~~~~~~~~~~

To use email notification, the following configuration is required.

1. Mail server configuration (``fess_config.properties``):

   ::

       mail.smtp.host=smtp.example.com
       mail.smtp.port=587

2. Enter an email address in "Notification Destination" in the "General" settings of the administration screen. Multiple addresses can be specified separated by commas.

Slack Notification
~~~~~~~~~~~~~~~~~~

You can send notifications to a Slack channel by configuring a Slack Incoming Webhook URL.

Google Chat Notification
~~~~~~~~~~~~~~~~~~~~~~~~

You can send notifications to a Google Chat space by configuring a Google Chat Webhook URL.

Configuration Properties
========================

The following properties can be configured in ``fess_config.properties``.

.. list-table:: Log Notification Configuration Properties
   :header-rows: 1
   :widths: 40 15 45

   * - Property
     - Default Value
     - Description
   * - ``log.notification.flush.interval``
     - ``30``
     - Flush interval from buffer to OpenSearch (seconds)
   * - ``log.notification.buffer.size``
     - ``1000``
     - Maximum number of events to hold in the in-memory buffer
   * - ``log.notification.interval``
     - ``300``
     - Notification job execution interval (seconds)
   * - ``log.notification.search.size``
     - ``1000``
     - Maximum number of events to retrieve from OpenSearch per job execution
   * - ``log.notification.max.display.events``
     - ``50``
     - Maximum number of events to include in a single notification message
   * - ``log.notification.max.message.length``
     - ``200``
     - Maximum character count for each log message (excess is truncated)
   * - ``log.notification.max.details.length``
     - ``3000``
     - Maximum character count for the details section of a notification message

.. note::
   Changes to these properties take effect after restarting |Fess|.

Notification Message Format
============================

Email Notification
------------------

Email notifications are sent in the following format.

**Subject:**

::

    [FESS] ERROR Log Alert: hostname

**Body:**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR and WARN events are sent as separate notifications for each level.

Slack / Google Chat Notification
---------------------------------

Slack and Google Chat notifications are sent as messages with similar content.

Operations Guide
================

Recommended Settings
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Environment
     - Recommended Level
     - Reason
   * - Production
     - ``ERROR``
     - Notify only on critical errors and reduce noise
   * - Staging
     - ``WARN``
     - Include potential issues in notifications
   * - Development
     - Disabled
     - Check log files directly

OpenSearch Index
----------------

The log notification feature uses the ``fess_log.notification_queue`` index for temporary event storage.
This index is automatically created when the feature is first used.
Since events are deleted after notifications are sent, the index size does not typically grow large.

Troubleshooting
===============

Notifications Are Not Being Sent
---------------------------------

1. **Verify enablement**

   Check that "Log Notification" is enabled in the "General" settings of the administration screen.

2. **Verify notification destination**

   For email notification, verify that an email address is configured in "Notification Destination".

3. **Verify mail server configuration**

   Verify that the mail server is correctly configured in ``fess_config.properties``.

4. **Check logs**

   Check ``fess.log`` for notification-related error messages.

   ::

       grep -i "notification" /var/log/fess/fess.log

Too Many Notifications
----------------------

1. **Raise the log level**

   Change the notification level from ``WARN`` to ``ERROR``.

2. **Address root causes**

   If errors are occurring frequently, investigate the root cause of the errors.

Notification Content Is Truncated
----------------------------------

Adjust the following properties:

- ``log.notification.max.details.length``: Maximum character count for the details section
- ``log.notification.max.display.events``: Maximum number of events to display
- ``log.notification.max.message.length``: Maximum character count for each message

References
==========

- :doc:`admin-logging` - Log Configuration
- :doc:`setup-memory` - Memory Configuration
