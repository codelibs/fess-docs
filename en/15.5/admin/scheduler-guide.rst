=========
Scheduler
=========

Overview
========

This page explains the configuration settings for the job scheduler.

Management Operations
=====================

Display Method
--------------

To open the job scheduler configuration list page shown below, click [System > Scheduler] in the left menu.

|image0|

Click the configuration name to edit it.

Creating Configuration
----------------------

To open the scheduler configuration page, click the New button.

|image1|

Configuration Items
-------------------

Name
::::

The name displayed in the list.

Target
::::::

The target serves as an identifier to determine whether a job should be executed when directly invoked via batch commands.
If you do not execute crawls via command, specify "all".

Schedule
::::::::

Configures the schedule settings.
Jobs written in the script will be executed according to the schedule configured here.

The notation format follows CRON format: "minute hour day month day-of-week".
For example, "0 12 \* \* 3" executes the job every Wednesday at 12:00 PM.

Executor
::::::::

Specifies the script execution environment.
Currently, only "groovy" is supported.

Script
::::::

Describes the job execution content in the language specified by the execution method.

For example, to execute only three crawl configurations as a crawl job (assuming web crawl configuration IDs are 1 and 2, and file system crawl configuration ID is 1), write as follows:

::

    return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"] as String[]).fileConfigIds(["1"] as String[]).dataConfigIds([] as String[]).execute(executor);

Logging
:::::::

When enabled, the job is recorded in the job log.

Crawler Job
:::::::::::

When enabled, the job is treated as a crawler job.
By configuring job.max.crawler.processes in fess_config.properties, you can prevent an excessive number of crawlers from starting.
By default, there is no limit on the number of crawler processes.

Status
::::::

Specifies whether the job is enabled or disabled.
When disabled, the job will not execute.

Display Order
:::::::::::::

Specifies the display order in the job list.

Deleting Configuration
----------------------

Click the configuration name on the list page, then click the Delete button to display a confirmation screen.
Click the Delete button to remove the configuration.

Manual Crawl Method
===================

Click "Default Crawler" in the "Scheduler" and click the Start Now button.
To stop the crawler, click "Default Crawler" and click the Stop button.

.. |image0| image:: ../../../resources/images/en/15.5/admin/scheduler-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/scheduler-2.png
