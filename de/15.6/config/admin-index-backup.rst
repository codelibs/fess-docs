==================
Index-Verwaltung
==================

Übersicht
====

Von |Fess| verwaltete Daten werden als OpenSearch-Indizes verwaltet.
Backup und Wiederherstellung von Suchindizes sind für stabilen Systembetrieb unerlässlich.
Dieser Abschnitt beschreibt Backup-, Wiederherstellungs- und Migrationsverfahren für Indizes.

Index-Struktur
==================

|Fess| verwendet folgende Indizes:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Indexname
     - Beschreibung
   * - ``fess.{Datum}``
     - Index für zu durchsuchende Dokumente (täglich erstellt)
   * - ``fess_log``
     - Suchprotokolle und Klickprotokolle
   * - ``fess_user``
     - Benutzerinformationen
   * - ``fess_config``
     - Systemkonfigurationsinformationen
   * - ``configsync``
     - Konfigurationssynchronisierungsinformationen

Index-Backup und -Wiederherstellung
====================================

Mit OpenSearch-Snapshot-Funktion können Sie Index-Backup und -Wiederherstellung durchführen.

Konfiguration des Snapshot-Repositorys
--------------------------------

Konfigurieren Sie zuerst ein Repository zum Speichern von Backup-Daten.

**Bei Dateisystem-Repository:**

1. Fügen Sie Repository-Pfad zur OpenSearch-Konfigurationsdatei (``config/opensearch.yml``) hinzu.

::

    path.repo: ["/var/opensearch/backup"]

2. Starten Sie OpenSearch neu.

3. Registrieren Sie Repository.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "fs",
      "settings": {
        "location": "/var/opensearch/backup",
        "compress": true
      }
    }'

.. note::
   In Standardkonfiguration von |Fess| startet OpenSearch auf Port 9201.

Snapshot-Erstellung (Backup)
------------------------------------

Backup aller Indizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alle Indizes sichern.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Wiederherstellung aus Snapshot
------------------------------

Wiederherstellung aller Indizes
~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Backup von Konfigurationsdateien
==========================

Zusätzlich zu OpenSearch-Indizes sichern Sie auch folgende Konfigurationsdateien.

Zu sichernde Dateien
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Datei/Verzeichnis
     - Beschreibung
   * - ``app/WEB-INF/conf/system.properties``
     - Systemkonfiguration (bei Zip-Installation)
   * - ``/etc/fess/system.properties``
     - Systemkonfiguration (bei RPM/DEB-Paketen)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - Detaillierte Fess-Konfiguration
   * - ``/etc/fess/fess_config.properties``
     - Detaillierte Fess-Konfiguration (RPM/DEB-Pakete)
   * - ``app/WEB-INF/classes/log4j2.xml``
     - Protokollkonfiguration
   * - ``/etc/fess/log4j2.xml``
     - Protokollkonfiguration (RPM/DEB-Pakete)

Referenzinformationen
========

Für detaillierte Informationen siehe offizielle OpenSearch-Dokumentation.

- `Snapshot-Funktion <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Repository-Konfiguration <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
