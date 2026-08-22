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
2. Captured events are accumulated in an in-memory buffer (up to 1,000 entries by default). When the buffer exceeds its limit, the oldest events are discarded first.
3. A timer flushes the buffered events to an OpenSearch index (``fess_log.notification_queue``) at 30-second intervals.
4. The "Log Notification" scheduled job reads events from OpenSearch at 5-minute intervals, groups them by log level, and sends a notification for each level.
5. After notifications are sent, the processed events are deleted from the index.

.. note::
   Each node sends notifications only for the logs it recorded itself (events are filtered by ``hostname``).
   In a cluster configuration, separate notifications are sent for each node.

.. note::
   To prevent infinite loops, logs from the loggers related to the notification feature itself
   (``LogNotificationAppender``, ``LogNotificationHelper``, ``LogNotificationTarget``,
   ``LogNotificationJob``, ``NotificationHelper``, and ``org.codelibs.curl``, which is used for
   HTTP communication) are excluded from notification targets.

Setup
=====

Enabling
--------

Enabling from the Administration Screen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Log in to the administration screen.
2. Select **General** from the **System** menu.
3. Enable the **Log Notification** checkbox.
4. Select the target level in **Log Notification Level** (``ERROR``, ``WARN``, ``INFO``, ``DEBUG``, ``TRACE``).
5. Click the "Update" button.

.. note::
   By default, only ``ERROR`` level events are targeted for notification.
   If you select ``WARN``, both ``WARN`` and ``ERROR`` events will be notified.

Enabling via System Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also directly set the system properties (``system.properties``) that are saved in the **General** settings of the administration screen.

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

Notification Destination Configuration
--------------------------------------

The notification destinations (email recipients, Slack / Google Chat Webhook URLs) are all configured in the
**System** -> **General** settings of the administration screen. Configure at least one notification destination.
If no notification destination is configured, the log notification job terminates without sending anything.

Email Notification
~~~~~~~~~~~~~~~~~~~

To use email notification, the following configuration is required.

1. Mail server configuration (``fess_env.properties``):

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. Enter email addresses in **Notification Mail** in the **General** settings of the administration screen.
   Multiple addresses can be specified separated by commas.

Slack Notification
~~~~~~~~~~~~~~~~~~~

Enter a Slack Incoming Webhook URL in **Slack Webhook URLs** in the **General** settings of the administration screen.
Multiple URLs can be specified separated by commas or whitespace.
This value is saved as the system property ``slack.webhook.urls``.

Google Chat Notification
~~~~~~~~~~~~~~~~~~~~~~~~~~

Enter a Google Chat Webhook URL in **Google Chat Webhook URLs** in the **General** settings of the administration screen.
Multiple URLs can be specified separated by commas or whitespace.
This value is saved as the system property ``google.chat.webhook.urls``.

.. note::
   If you configure only the Slack or Google Chat Webhook URL without configuring **Notification Mail**,
   no email is sent and only the Slack / Google Chat notification is performed.
   The same subject and body as the email notification are sent to Slack / Google Chat as a message.

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
     - Aggregation period (seconds) displayed in the notification message. This is a display-only value and is not the actual job execution interval (see the note below).
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
   Changes to ``log.notification.flush.interval`` take effect after restarting |Fess|.
   The other properties take effect from the next notification cycle.

.. note::
   ``log.notification.interval`` is the value used for the "in the last N seconds" display text in the
   notification message; it does not change the job execution frequency. The actual execution interval is
   determined by the cron setting of the "Log Notification" scheduled job (5-minute intervals by default).
   To change the job execution interval, modify the cron expression of this job from
   **System** -> **Scheduler**, and adjust ``log.notification.interval`` accordingly so that the display
   matches the actual behavior.

Notification Message Format
===========================

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
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR and WARN events are sent as separate notifications for each level.

.. note::
   When the number of events to display exceeds ``log.notification.max.display.events``, the beginning of the
   details section becomes ``Total: N event(s) (showing M)`` and ``... and X more`` is appended at the end.
   Each log message is truncated at the end with ``...`` when it exceeds ``log.notification.max.message.length``,
   and once the entire details section exceeds ``log.notification.max.details.length`` the remainder is
   discarded.

Slack / Google Chat Notification
--------------------------------

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

The log notification feature uses the ``fess_log.notification_queue`` index for temporary event storage
(the index name is the value of ``index.log`` (default ``fess_log``) with ``.notification_queue`` appended).
This index is automatically created when the feature is first used.
Since events are deleted after notifications are sent, the index size does not typically grow large.

.. note::
   The number of events processed in a single job execution is capped by ``log.notification.search.size``
   (default 1,000). Events accumulated beyond this limit are discarded together after notifications are sent
   and are not carried over to subsequent executions. In environments where a large volume of logs occurs in a
   short period, raise ``log.notification.search.size`` as needed.

Troubleshooting
===============

Notifications Are Not Being Sent
--------------------------------

1. **Verify enablement**

   Check that **Log Notification** is enabled in the **General** settings of the administration screen.

2. **Verify notification destination**

   Check that at least one notification destination (**Notification Mail**, **Slack Webhook URLs**, or
   **Google Chat Webhook URLs**) is configured. If none are configured, the job outputs
   ``No notification targets configured.`` and sends nothing.

3. **Verify mail server configuration**

   When using email notification, verify that the mail server is correctly configured in
   ``fess_env.properties``.

4. **Verify the scheduled job**

   Check that the "Log Notification" job is enabled in **System** -> **Scheduler**.
   If this job is disabled, no notifications are sent.

5. **Check logs**

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
---------------------------------

Adjust the following properties:

- ``log.notification.max.details.length``: Maximum character count for the details section
- ``log.notification.max.display.events``: Maximum number of events to display
- ``log.notification.max.message.length``: Maximum character count for each message

References
==========

- :doc:`admin-logging` - Log Configuration
- :doc:`setup-memory` - Memory Configuration
