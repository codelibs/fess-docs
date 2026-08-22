====================
Index-Verwaltung
====================

Übersicht
=========

Von |Fess| verwaltete Daten werden als OpenSearch-Indizes verwaltet.
Backup und Wiederherstellung von Suchindizes sind für den stabilen Systembetrieb unerlässlich.
Dieser Abschnitt beschreibt Backup-, Wiederherstellungs- und Migrationsverfahren für Indizes mithilfe der OpenSearch-Snapshot-Funktion.

.. note::
   |Fess| verfügt neben dem in diesem Abschnitt beschriebenen Index-Backup über OpenSearch-Snapshots auch über eine Funktion zum Export/Import von Konfigurationsdaten (Crawl-Einstellungen, Benutzerinformationen, Systemeinstellungen usw.) über die Verwaltungsoberfläche. Wenn Sie nur Konfigurationsdaten sichern oder migrieren möchten, siehe :doc:`../admin/backup-guide`. OpenSearch-Snapshots eignen sich für den physischen Backup eines gesamten Index einschließlich der Suchdokumente.

Index-Struktur
==============

|Fess| verwendet folgende Indizes:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Indexname
     - Beschreibung
   * - ``fess.{Zeitstempel}``
     - Index für Suchdokumente. Wird beim Index-Neuaufbau im Format ``fess.{yyyyMMddHHmmssSSS}`` (Zeitstempel mit Millisekundengenauigkeit) erstellt und über die Aliase ``fess.search`` (für Suche) und ``fess.update`` (für Aktualisierungen) referenziert.
   * - ``fess_config.*``
     - Systemkonfigurationsdaten (bestehend aus mehreren Sub-Indizes wie ``fess_config.web_config``, ``fess_config.scheduled_job``, ``fess_config.data_config`` usw.)
   * - ``fess_user.*``
     - Benutzerinformationen (``fess_user.user``, ``fess_user.role``, ``fess_user.group``)
   * - ``fess_log.*``
     - Such- und Klickprotokolle sowie weitere Protokolle (``fess_log.search_log``, ``fess_log.click_log``, ``fess_log.favorite_log``, ``fess_log.user_info``, ``fess_log.notification_queue``)
   * - ``fess_crawler.*``
     - Temporäre Indizes, die während der Crawl-Verarbeitung verwendet werden (``fess_crawler.queue``, ``fess_crawler.data``, ``fess_crawler.filter``). Da diese nach Abschluss des Crawlings nicht mehr benötigt werden, müssen sie normalerweise nicht in das Backup einbezogen werden.

Index-Backup und -Wiederherstellung
=====================================

Mit der OpenSearch-Snapshot-Funktion können Sie Index-Backup und -Wiederherstellung durchführen.

Konfiguration des Snapshot-Repositorys
---------------------------------------

Konfigurieren Sie zunächst ein Repository zum Speichern der Backup-Daten.

**Bei Dateisystem-Repository:**

1. Fügen Sie den Repository-Pfad zur OpenSearch-Konfigurationsdatei (``opensearch.yml``) hinzu.

::

    path.repo: ["/var/opensearch/backup"]

2. Starten Sie OpenSearch neu.

3. Registrieren Sie das Repository.

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
   In der Standardkonfiguration der zip/tar.gz-Version von |Fess| startet OpenSearch auf Port 9201 (``search_engine.http.url`` in ``fess_config.properties``). Bei der RPM/DEB-Paketversion ist standardmäßig eine Verbindung zu Port 9200 konfiguriert (``SEARCH_ENGINE_HTTP_URL`` in der Umgebungskonfigurationsdatei ``/etc/sysconfig/fess`` (RPM) bzw. ``/etc/default/fess`` (DEB)). Passen Sie die Portnummer entsprechend Ihrer Umgebung an.

**Bei AWS-S3-Repository:**

Wenn Sie S3 als Backup-Ziel verwenden möchten, installieren und konfigurieren Sie das Plugin ``repository-s3``.

::

    curl -X PUT "localhost:9201/_snapshot/fess_s3_backup" -H 'Content-Type: application/json' -d'
    {
      "type": "s3",
      "settings": {
        "bucket": "my-fess-backup-bucket",
        "region": "ap-northeast-1",
        "base_path": "fess-snapshots"
      }
    }'

Snapshot-Erstellung (Backup)
------------------------------

Backup aller Indizes
~~~~~~~~~~~~~~~~~~~~~

Alle Indizes sichern.

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_1?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Backup bestimmter Indizes
~~~~~~~~~~~~~~~~~~~~~~~~~~

Nur bestimmte Indizes sichern. Das folgende Beispiel bezieht sich ausschließlich auf |Fess|-bezogene Indizes (Indizes, die mit ``fess`` beginnen).

::

    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_fess_only?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Regelmäßiges automatisches Backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mit cron oder ähnlichen Tools können Sie regelmäßige Backups einrichten.

::

    #!/bin/bash
    DATE=$(date +%Y%m%d_%H%M%S)
    curl -X PUT "localhost:9201/_snapshot/fess_backup/snapshot_${DATE}?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Snapshot-Überprüfung
---------------------

Liste der erstellten Snapshots anzeigen.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/_all?pretty"

Details zu einem bestimmten Snapshot anzeigen.

::

    curl -X GET "localhost:9201/_snapshot/fess_backup/snapshot_1?pretty"

Wiederherstellung aus Snapshot
--------------------------------

Wiederherstellung aller Indizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "*",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Wiederherstellung bestimmter Indizes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der Index für Suchdokumente hat einen Namen im Format ``fess.{yyyyMMddHHmmssSSS}``. Prüfen Sie den tatsächlichen Indexnamen z. B. über ``_cat/indices``, bevor Sie die Wiederherstellung durchführen.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

Wiederherstellung mit umbenennen des Index
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Beim Wiederherstellen kann der Indexname geändert werden.

::

    curl -X POST "localhost:9201/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true" -H 'Content-Type: application/json' -d'
    {
      "indices": "fess.20250101000000000",
      "rename_pattern": "fess\\.(.+)",
      "rename_replacement": "restored_fess.$1",
      "ignore_unavailable": true,
      "include_global_state": false
    }'

.. note::
   Wenn Sie den Index für Suchdokumente (``fess.{Zeitstempel}``) wiederhergestellt haben, stellen Sie unbedingt sicher, dass die Aliase ``fess.search`` und ``fess.update`` auf den wiederhergestellten Index zeigen. Da Snapshots auch Alias-Informationen enthalten, werden Aliase bei einer Wiederherstellung aller Indizes mit unverändertem Namen normalerweise ebenfalls wiederhergestellt. Wenn Sie den Indexnamen jedoch über ``rename_pattern`` geändert haben oder zu einem anderen Cluster migrieren, werden die Aliase möglicherweise nicht korrekt gesetzt. Setzen Sie die Aliase in diesem Fall manuell neu (ersetzen Sie den Indexnamen durch den tatsächlichen Namen):

   ::

       curl -X POST "localhost:9201/_aliases" -H 'Content-Type: application/json' -d'
       {
         "actions": [
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.search" } },
           { "add": { "index": "restored_fess.20250101000000000", "alias": "fess.update" } }
         ]
       }'

Snapshot-Löschung
------------------

Alte Snapshots können gelöscht werden, um Speicherplatz zu sparen.

::

    curl -X DELETE "localhost:9201/_snapshot/fess_backup/snapshot_1"

Backup von Konfigurationsdateien
=================================

Sichern Sie zusätzlich zu den OpenSearch-Indizes auch die folgenden Konfigurationsdateien. Der Speicherort der Konfigurationsdateien hängt von der Installationsmethode ab.

Zu sichernde Dateien
---------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Datei/Verzeichnis
     - Installationsmethode
     - Beschreibung
   * - ``app/WEB-INF/conf/system.properties``
     - zip/tar.gz
     - Systemkonfiguration (allgemeine Einstellungen)
   * - ``/etc/fess/system.properties``
     - RPM/DEB
     - Systemkonfiguration (allgemeine Einstellungen)
   * - ``app/WEB-INF/classes/fess_config.properties``
     - zip/tar.gz
     - Detaillierte |Fess|-Konfiguration
   * - ``/etc/fess/fess_config.properties``
     - RPM/DEB
     - Detaillierte |Fess|-Konfiguration
   * - ``app/WEB-INF/classes/log4j2.xml``
     - zip/tar.gz
     - Protokollkonfiguration
   * - ``/usr/share/fess/app/WEB-INF/classes/log4j2.xml``
     - RPM/DEB
     - Protokollkonfiguration
   * - ``app/WEB-INF/classes/fess_indices/``
     - zip/tar.gz
     - Index-Definitionsdateien
   * - ``/usr/share/fess/app/WEB-INF/classes/fess_indices/``
     - RPM/DEB
     - Index-Definitionsdateien
   * - ``app/WEB-INF/thumbnails/``
     - zip/tar.gz
     - Vorschaubilder (bei Bedarf)
   * - ``/var/lib/fess/thumbnails/``
     - RPM/DEB
     - Vorschaubilder (bei Bedarf)

.. note::
   Bei der RPM/DEB-Paketversion befinden sich im Verzeichnis ``/etc/fess/`` neben ``fess_config.properties`` auch Konfigurationsdateien wie ``fess_env_crawler.properties`` und weitere ``fess_env_*.properties``-Dateien sowie ``tika.xml``. Es wird empfohlen, das gesamte Verzeichnis ``/etc/fess/`` zu sichern. Die Datei ``system.properties`` wird als ``/etc/fess/system.properties`` erstellt bzw. aktualisiert, wenn Einstellungen unter "System > Allgemein" in der Verwaltungsoberfläche gespeichert werden.

Beispiel für das Backup von Konfigurationsdateien
---------------------------------------------------

Das folgende Beispiel zeigt das Backup von Konfigurationsdateien bei der RPM/DEB-Paketversion.

::

    #!/bin/bash
    BACKUP_DIR="/backup/fess/$(date +%Y%m%d_%H%M%S)"
    mkdir -p ${BACKUP_DIR}

    # Konfigurationsdateien kopieren (einschließlich system.properties, fess_config.properties usw.)
    cp -r /etc/fess/ ${BACKUP_DIR}/

    # Index-Definitionsdateien und Protokollkonfiguration
    cp -r /usr/share/fess/app/WEB-INF/classes/fess_indices/ ${BACKUP_DIR}/
    cp /usr/share/fess/app/WEB-INF/classes/log4j2.xml ${BACKUP_DIR}/

    # Optional: Vorschaubilder
    # cp -r /var/lib/fess/thumbnails/ ${BACKUP_DIR}/

    echo "Backup completed: ${BACKUP_DIR}"

Datenmigration
==============

Migrationsverfahren in eine andere Umgebung
--------------------------------------------

1. **Backup in der Quellumgebung erstellen**

   - Erstellen Sie einen OpenSearch-Snapshot.
   - Sichern Sie die Konfigurationsdateien.

2. **Zielumgebung vorbereiten**

   - Installieren Sie |Fess| in der neuen Umgebung.
   - Starten Sie OpenSearch.

3. **Konfigurationsdateien wiederherstellen**

   - Kopieren Sie die gesicherten Konfigurationsdateien in die neue Umgebung.
   - Passen Sie Pfade, Hostnamen usw. bei Bedarf an.

4. **Indizes wiederherstellen**

   - Konfigurieren Sie das Snapshot-Repository.
   - Stellen Sie die Indizes aus dem Snapshot wieder her.
   - Vergewissern Sie sich nach der Wiederherstellung, dass die Aliase ``fess.search`` und ``fess.update`` auf den wiederhergestellten Index zeigen.

5. **Funktionstest**

   - Starten Sie |Fess|.
   - Öffnen Sie die Verwaltungsoberfläche und überprüfen Sie die Einstellungen.
   - Überprüfen Sie, ob die Suchfunktion ordnungsgemäß funktioniert.

Hinweise beim Versionsupgrade
------------------------------

Beachten Sie beim Migrieren von Daten zwischen verschiedenen Versionen von |Fess| folgende Punkte:

- Bei unterschiedlichen OpenSearch-Hauptversionen können Kompatibilitätsprobleme auftreten.
- Wenn sich die Index-Struktur geändert hat, kann eine Neuindizierung erforderlich sein.
- Wenn Sie Konfigurationsdaten über eine Änderung der Index-Struktur hinweg migrieren möchten, erwägen Sie die Verwendung der Backup-Funktion der Verwaltungsoberfläche (:doc:`../admin/backup-guide`) für einen logischen Export/Import anstelle von OpenSearch-Snapshots.
- Weitere Einzelheiten finden Sie im Upgrade-Leitfaden der jeweiligen Version.

Fehlerbehebung
==============

Snapshot-Erstellung schlägt fehl
----------------------------------

1. Überprüfen Sie die Berechtigungen für den Repository-Pfad.
2. Überprüfen Sie, ob ausreichend Speicherplatz vorhanden ist.
3. Prüfen Sie die OpenSearch-Protokolldateien auf Fehlermeldungen.

Wiederherstellung schlägt fehl
--------------------------------

1. Überprüfen Sie, ob bereits ein Index mit demselben Namen vorhanden ist. In OpenSearch kann keine Wiederherstellung auf einen geöffneten Index mit demselben Namen durchgeführt werden. Schließen Sie den betreffenden Index vor der Wiederherstellung (``_close``) oder löschen Sie ihn, oder stellen Sie ihn über ``rename_pattern`` unter einem anderen Namen wieder her.
2. Überprüfen Sie, ob die OpenSearch-Version kompatibel ist.
3. Überprüfen Sie, ob der Snapshot beschädigt ist.

Nach der Wiederherstellung ist keine Suche möglich
----------------------------------------------------

1. Überprüfen Sie, ob der Index ordnungsgemäß wiederhergestellt wurde: ``curl -X GET "localhost:9201/_cat/indices?v"``
2. Überprüfen Sie, ob die Aliase ``fess.search`` und ``fess.update`` auf den wiederhergestellten Index zeigen: ``curl -X GET "localhost:9201/_cat/aliases?v"``. Falls die Aliase nicht gesetzt sind, setzen Sie sie über die ``_aliases``-API neu.
3. Prüfen Sie die |Fess|-Protokolldateien auf Fehler.
4. Überprüfen Sie, ob die Konfigurationsdateien korrekt wiederhergestellt wurden.

Verwandte Themen
================

- :doc:`../admin/backup-guide` - Backup/Wiederherstellung von Konfigurationsdaten über die Verwaltungsoberfläche
- :doc:`admin-index-export` - Index-Exportfunktion
- :doc:`admin-logging` - Protokollkonfiguration

Referenzinformationen
=====================

Für detaillierte Informationen siehe die offizielle OpenSearch-Dokumentation.

- `Snapshot-Funktion <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/index/>`_
- `Repository-Konfiguration <https://opensearch.org/docs/latest/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/>`_
- `S3-Repository <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/plugins/#s3-repository>`_
