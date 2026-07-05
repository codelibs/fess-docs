==========================
Backup API
==========================

Übersicht
=========

Die Backup API dient zum Sichern und Wiederherstellen von Konfigurationsdaten in |Fess|.
Sie können Crawl-Konfigurationen, Benutzer, Rollen, Wörterbücher und andere Einstellungen exportieren und importieren.

Basis-URL
=========

::

    /api/admin/backup

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /export
     - Konfigurationsdaten exportieren
   * - POST
     - /import
     - Konfigurationsdaten importieren

Konfigurationsdaten exportieren
===============================

Request
-------

::

    GET /api/admin/backup/export

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``types``
     - String
     - Nein
     - Export-Ziele (kommagetrennt, Standard: all)

Exportierbare Typen
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Typ
     - Beschreibung
   * - ``webconfig``
     - Web-Crawl-Konfiguration
   * - ``fileconfig``
     - Datei-Crawl-Konfiguration
   * - ``dataconfig``
     - Datenspeicher-Konfiguration
   * - ``scheduler``
     - Scheduler-Konfiguration
   * - ``user``
     - Benutzereinstellungen
   * - ``role``
     - Rolleneinstellungen
   * - ``group``
     - Gruppeneinstellungen
   * - ``labeltype``
     - Label-Typ-Einstellungen
   * - ``keymatch``
     - Key-Match-Einstellungen
   * - ``dict``
     - Wörterbuchdaten
   * - ``all``
     - Alle Einstellungen (Standard)

Response
--------

Binärdaten (ZIP-Format)

Content-Type: ``application/zip``
Content-Disposition: ``attachment; filename="fess-backup-20250129-100000.zip"``

ZIP-Dateiinhalt
~~~~~~~~~~~~~~~

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

Konfigurationsdaten importieren
===============================

Request
-------

::

    POST /api/admin/backup/import
    Content-Type: multipart/form-data

Request-Body
~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="file"; filename="fess-backup.zip"
    Content-Type: application/zip

    [Binärdaten]
    --boundary
    Content-Disposition: form-data; name="overwrite"

    true
    --boundary--

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``file``
     - Ja
     - Backup-ZIP-Datei
   * - ``overwrite``
     - Nein
     - Bestehende Einstellungen überschreiben (Standard: false)
   * - ``types``
     - Nein
     - Import-Ziele (kommagetrennt, Standard: all)

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

Verwendungsbeispiele
====================

Alle Einstellungen exportieren
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup.zip

Bestimmte Einstellungen exportieren
-----------------------------------

.. code-block:: bash

    # Nur Web-Crawl-Konfiguration und Benutzereinstellungen exportieren
    curl -X GET "http://localhost:8080/api/admin/backup/export?types=webconfig,user" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess-backup-partial.zip

Einstellungen importieren
-------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=false"

Mit Überschreiben importieren
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "overwrite=true"

Nur bestimmte Einstellungen importieren
---------------------------------------

.. code-block:: bash

    # Nur Benutzer und Rollen importieren
    curl -X POST "http://localhost:8080/api/admin/backup/import" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@fess-backup.zip" \
         -F "types=user,role" \
         -F "overwrite=false"

Automatisiertes Backup
----------------------

.. code-block:: bash

    #!/bin/bash
    # Beispielskript für tägliches Backup um 2:00 Uhr

    DATE=$(date +%Y%m%d)
    BACKUP_DIR="/backup/fess"

    curl -X GET "http://localhost:8080/api/admin/backup/export" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o "${BACKUP_DIR}/fess-backup-${DATE}.zip"

    # Backups löschen, die älter als 30 Tage sind
    find "${BACKUP_DIR}" -name "fess-backup-*.zip" -mtime +30 -delete

Hinweise
========

- Backups enthalten auch Passwortinformationen, daher sollten sie sicher aufbewahrt werden
- Bei Angabe von ``overwrite=true`` werden bestehende Einstellungen überschrieben
- Bei umfangreichen Konfigurationen kann der Export/Import einige Zeit in Anspruch nehmen
- Der Import zwischen verschiedenen Fess-Versionen kann zu Kompatibilitätsproblemen führen

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`../../admin/backup-guide` - Backup-Verwaltungsanleitung
- :doc:`../../admin/maintenance-guide` - Wartungsanleitung
