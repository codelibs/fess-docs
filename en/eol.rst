================
Product Support Period
================

Products beyond their End-of-Life (EOL) date will no longer receive maintenance or updates.
CodeLibs Project strongly recommends migrating to a supported release.
This prevents situations where necessary services and support become unavailable.
The latest release can be downloaded from the `download page <downloads.html>`__.

If support is needed for products beyond their End-of-Life period, please consult `commercial support <https://www.n2sm.net/products/n2search.html>`__.

.. warning::

   **Recommended Actions Before End of Support**

   Before the support end date, please plan and execute the following actions:

   1. **Create backups**: Back up configuration files and index data
   2. **Test in staging environment**: Verify operation with the new version before production migration
   3. **Review release notes**: Check for breaking changes and deprecated features
   4. **Plan migration schedule**: Create a plan considering downtime requirements

Upgrade Path
================

The following table shows the recommended upgrade path from your current version to the latest release.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Current Version
     - Recommended Path
     - Notes
   * - 15.x to 15.5
     - Direct upgrade possible
     - See `Upgrade Guide <15.5/install/upgrade.html>`__
   * - 14.x to 15.5
     - Direct upgrade possible
     - Pay attention to configuration file changes
   * - 13.x to 15.5
     - Via 14.x recommended
     - Upgrade in order: 13.x to 14.19 to 15.5
   * - 12.x or earlier to 15.5
     - Staged upgrade required
     - Upgrade 1-2 major versions at a time

.. note::

   For detailed upgrade procedures, see the `Upgrade Guide <15.5/install/upgrade.html>`__.
   For large-scale environments or complex configurations, we recommend consulting `commercial support <support-services.html>`__.

Migration Resources
======================

Useful documents for upgrading:

- `Upgrade Guide <15.5/install/upgrade.html>`__ - Detailed steps from backup to upgrade completion
- `Release Notes <https://github.com/codelibs/fess/releases>`__ - Changes and notes for each version
- `Troubleshooting <15.5/install/troubleshooting.html>`__ - Common problems and solutions
- `Docker Upgrade <15.5/install/install-docker.html>`__ - Upgrading in Docker environments

Maintenance Table
==============

The EOL date for Fess is approximately 18 months after release.

**Legend**:

- 🟢 **Supported**: Security fixes and bug fixes are provided
- 🟡 **Nearing End of Support**: Support ends within 6 months
- 🔴 **End of Support**: No maintenance is provided

Currently Supported Versions
------------------------

.. tabularcolumns:: |p{3cm}|p{4cm}|p{3cm}|
.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Fess
     - EOL Date
     - Status
   * - 15.5.x
     - 2027-08-01
     - 🟢 Latest (Recommended)
   * - 15.4.x
     - 2027-06-01
     - 🟢 Supported
   * - 15.3.x
     - 2027-04-01
     - 🟢 Supported
   * - 15.2.x
     - 2027-03-01
     - 🟢 Supported
   * - 15.1.x
     - 2027-01-01
     - 🟢 Supported
   * - 15.0.x
     - 2026-12-01
     - 🟢 Supported
   * - 14.19.x
     - 2026-08-01
     - 🟡 Nearing End of Support
   * - 14.18.x
     - 2026-05-01
     - 🟡 Nearing End of Support
   * - 14.17.x
     - 2026-03-01
     - 🔴 End of Support
   * - 14.16.x
     - 2026-02-01
     - 🔴 End of Support
   * - 14.15.x
     - 2026-01-01
     - 🔴 End of Support

End-of-Life Versions
------------------------

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Fess
     - EOL Date
   * - 14.14.x
     - 2025-11-01
   * - 14.13.x
     - 2025-10-01
   * - 14.12.x
     - 2025-08-01
   * - 14.11.x
     - 2025-04-01
   * - 14.10.x
     - 2025-01-01
   * - 14.9.x
     - 2024-12-01
   * - 14.8.x
     - 2024-11-01
   * - 14.7.x
     - 2024-09-01
   * - 14.6.x
     - 2024-07-01
   * - 14.5.x
     - 2024-05-01
   * - 14.4.x
     - 2024-02-24
   * - 14.3.x
     - 2023-12-28
   * - 14.2.x
     - 2023-10-26
   * - 14.1.x
     - 2023-09-08
   * - 14.0.x
     - 2023-08-08
   * - 13.16.x
     - 2023-06-07
   * - 13.15.x
     - 2023-03-22
   * - 13.14.x
     - 2023-02-03
   * - 13.13.x
     - 2022-11-25
   * - 13.12.x
     - 2022-09-23
   * - 13.11.x
     - 2022-08-10
   * - 13.10.x
     - 2022-05-11
   * - 13.9.x
     - 2022-02-18
   * - 13.8.x
     - 2021-12-18
   * - 13.7.x
     - 2021-11-13
   * - 13.6.x
     - 2021-08-11
   * - 13.5.x
     - 2021-06-02
   * - 13.4.x
     - 2021-04-01
   * - 13.3.x
     - 2021-01-31
   * - 13.2.x
     - 2020-12-25
   * - 13.1.x
     - 2020-11-20
   * - 13.0.x
     - 2020-10-10
   * - 12.7.x
     - 2020-11-20
   * - 12.6.x
     - 2020-09-26
   * - 12.5.x
     - 2020-07-29
   * - 12.4.x
     - 2020-05-14
   * - 12.3.x
     - 2020-02-23
   * - 12.2.x
     - 2020-12-13
   * - 12.1.x
     - 2019-08-19
   * - 12.0.x
     - 2019-06-02
   * - 11.4.x
     - 2019-03-23
   * - 11.3.x
     - 2019-02-14
   * - 11.2.x
     - 2018-12-15
   * - 11.1.x
     - 2018-11-11
   * - 11.0.x
     - 2018-08-13
   * - 10.3.x
     - 2018-05-24
   * - 10.2.x
     - 2018-02-30
   * - 10.1.x
     - 2017-12-09
   * - 10.0.x
     - 2017-08-05
   * - 9.4.x
     - 2016-11-21
   * - 9.3.x
     - 2016-05-06
   * - 9.2.x
     - 2015-12-28
   * - 9.1.x
     - 2015-09-26
   * - 9.0.x
     - 2015-08-07
   * - 8.x
     - 2014-08-23
   * - 7.x
     - 2014-02-03
   * - 6.x
     - 2013-09-02
   * - 5.x
     - 2013-06-15
   * - 4.x
     - 2012-06-19
   * - 3.x
     - 2011-09-07
   * - 2.x
     - 2011-07-16
   * - 1.x
     - 2011-04-10

Frequently Asked Questions
==========================

Q: Can I continue using Fess after the support period ends?
------------------------------------------------------------

A: Technically it is possible, but security fixes and bug fixes will not be provided.
To mitigate security risks, we strongly recommend upgrading to a supported version.

Q: How long does an upgrade take?
----------------------------------

A: It depends on the scale of your environment, but typically 2 to 4 hours.
For large-scale environments or complex configurations, we recommend testing in a staging environment first.
See the `Upgrade Guide <15.5/install/upgrade.html>`__ for details.

Q: What should I do if I encounter a problem with an end-of-life version?
--------------------------------------------------------------------------

A: You have the following options:

1. **Upgrade to the latest version**: The recommended action
2. **Ask on community forums**: You may be able to get advice from other users
3. **Consult commercial support**: `N2SM commercial support <support-services.html>`__ can provide maintenance for specific versions

Q: What should I check before upgrading?
------------------------------------------

A: Please verify the following:

1. Check `Release Notes <https://github.com/codelibs/fess/releases>`__ for breaking changes
2. Verify OpenSearch version compatibility
3. If you have customizations, check compatibility of settings and plugins
4. Create thorough backups

Q: Does upgrading in a Docker environment require special steps?
-----------------------------------------------------------------

A: You will need to back up Docker volumes and obtain the new Docker Compose files.
See the `Docker Installation Guide <15.5/install/install-docker.html>`__ for details.

