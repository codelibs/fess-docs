==========================
Backup API
==========================

Overview
========

Backup API is an API for backing up and restoring |Fess| configuration data.
You can export and import crawl configurations, users, roles, dictionaries, and other settings.

Base URL
========

::

    /api/admin/backup

Endpoint List
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Method
     - Path
     - Description
   * - GET
     - /export
     - Export configuration data
   * - POST
     - /import
     - Import configuration data

Export Configuration Data
=========================

Request
-------

::

    GET /api/admin/backup/export

Parameters
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Type
     - Required
     - Description
   * - ``types``
     - String
     - No
     - Export targets (comma-separated, default: all)

Export Target Types
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Type
     - Description
   * - ``webconfig``
     - Web crawl configurations
   * - ``fileconfig``
     - File crawl configurations
   * - ``dataconfig``
     - Data store configurations
   * - ``scheduler``
     - Schedule configurations
   * - ``user``
     - User configurations
   * - ``role``
     - Role configurations
   * - ``group``
     - Group configurations
   * - ``labeltype``
     - Label type configurations
   * - ``keymatch``
     - Key match configurations
   * - ``dict``
     - Dictionary data
   * - ``all``
     - All configurations (default)

Response
--------

Binary data (ZIP format)

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

ZIP File Contents
~~~~~~~~~~~~~~~~~

::

    fess-backup-20250129-100000.zip
    ├── webconfig.json
    ├── fileconfig.json
    ├── dataconfig.json
    ├── scheduler.json
    ├── user.json
    ├── role.json
    ├── group.json
    ├── labeltype.json
    ├── keymatch.json
    ├── dict/
    │   ├── synonym.txt
    │   ├── mapping.txt
    │   └── protwords.txt
    └── metadata.json

Import Configuration Data
=========================

Request
-------

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

Request Body
~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [binary data]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

Field Description
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Field
     - Required
     - Description
   * - ``file``
     - Yes
     - Backup ZIP file
   * - ``overwrite``
     - No
     - Overwrite existing configurations (default: false)
   * - ``types``
     - No
     - Import targets (comma-separated, default: all)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Backup imported successfully",
        "imported": {
          "webconfig": 5,
          "fileconfig": 3,
          "dataconfig": 2,
          "scheduler": 4,
          "user": 10,
          "role": 5,
          "group": 3,
          "labeltype": 8,
          "keymatch": 12,
          "dict": 3
        }
      }
    }

Usage Examples
==============

Export All Configurations
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

Export Specific Configurations
------------------------------

.. code-block:: bash

    # Export only web crawl configurations and user configurations
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

Import Configurations
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

Import with Overwrite
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

Import Specific Configurations Only
-----------------------------------

.. code-block:: bash

    # Import only users and roles
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

Automate Backups
----------------

.. code-block:: bash

    #!/bin/bash
    # Example script for daily backup at 2 AM

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # Delete backups older than 30 days
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

Cautions
========

- Backups include password information, so store them securely
- Specifying ``overwrite=true`` during import will overwrite existing configurations
- Large configurations may take time to export/import
- Importing between different Fess versions may cause compatibility issues

Reference
=========

- :doc:`api-admin-overview` - Admin API Overview
- :doc:`../../admin/backup-guide` - Backup Management Guide
- :doc:`../../admin/maintenance-guide` - Maintenance Guide

