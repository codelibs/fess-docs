====================
Upgrade-Verfahren
====================

Diese Seite beschreibt die Verfahren zum Upgrade von |Fess| von einer früheren Version auf die neueste Version.

.. warning::

   **Wichtige Hinweise vor dem Upgrade**

   - Erstellen Sie vor dem Upgrade unbedingt ein Backup
   - Es wird dringend empfohlen, das Upgrade zunächst in einer Testumgebung zu überprüfen
   - Während des Upgrades wird der Dienst gestoppt, planen Sie daher eine angemessene Wartungszeit ein
   - Je nach Version kann sich das Format der Konfigurationsdateien geändert haben

Unterstützte Versionen
======================

Dieses Upgrade-Verfahren unterstützt Upgrades zwischen folgenden Versionen:

- Fess 14.x → Fess 15.3
- Fess 15.x → Fess 15.3

.. note::

   Bei Upgrades von älteren Versionen (13.x oder früher) kann ein stufenweises Upgrade erforderlich sein.
   Details finden Sie in den Release Notes.

Vorbereitung vor dem Upgrade
=============================

Überprüfung der Versionskompatibilität
---------------------------------------

Überprüfen Sie die Kompatibilität zwischen der Zielversion und der aktuellen Version des Upgrades.

- `Release Notes <https://github.com/codelibs/fess/releases>`__
- `Upgrade-Leitfaden <https://fess.codelibs.org/de/>`__

Planung der Ausfallzeit
------------------------

Die Upgrade-Arbeiten erfordern einen Systemstopp. Planen Sie die Ausfallzeit unter Berücksichtigung folgender Punkte:

- Backup-Zeit: 10 Minuten ~ mehrere Stunden (abhängig vom Datenvolumen)
- Upgrade-Zeit: 10 ~ 30 Minuten
- Funktionsprüfungszeit: 30 Minuten ~ 1 Stunde
- Pufferzeit: 30 Minuten

**Empfohlene Wartungszeit**: Insgesamt 2 ~ 4 Stunden

Schritt 1: Daten-Backup
========================

Erstellen Sie vor dem Upgrade ein Backup aller Daten.

Backup der Konfigurationsdaten
-------------------------------

1. **Backup über die Verwaltungsseite**

   Melden Sie sich in der Verwaltungsseite an und klicken Sie auf „System" → „Backup".

   Laden Sie folgende Dateien herunter:

   - ``fess_basic_config.bulk``
   - ``fess_user.bulk``

2. **Backup der Konfigurationsdateien**

   TAR.GZ/ZIP-Version::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/

   RPM/DEB-Version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/

3. **Angepasste Konfigurationsdateien**

   Falls angepasste Konfigurationsdateien vorhanden sind, erstellen Sie auch von diesen Backups::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

Backup der Indexdaten
----------------------

Erstellen Sie ein Backup der OpenSearch-Indexdaten.

Methode 1: Verwendung der Snapshot-Funktion (empfohlen)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verwenden Sie die Snapshot-Funktion von OpenSearch für das Backup der Indizes.

1. Repository-Konfiguration::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. Snapshot-Erstellung::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. Snapshot-Überprüfung::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

Methode 2: Backup des gesamten Verzeichnisses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stoppen Sie OpenSearch und erstellen Sie ein Backup des Datenverzeichnisses.

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Backup der Docker-Version
--------------------------

Erstellen Sie ein Backup der Docker-Volumes::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker run --rm -v fess-es-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-es-data-backup.tar.gz /data
    $ docker run --rm -v fess-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fess-data-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

Schritt 2: Stopp der aktuellen Version
=======================================

Stoppen Sie Fess und OpenSearch.

TAR.GZ/ZIP-Version::

    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB-Version (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Schritt 3: Installation der neuen Version
==========================================

Die Vorgehensweise unterscheidet sich je nach Installationsmethode.

TAR.GZ/ZIP-Version
------------------

1. Neue Version herunterladen und entpacken::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.3.2/fess-15.3.2.tar.gz
       $ tar -xzf fess-15.3.2.tar.gz

2. Konfiguration der alten Version kopieren::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.3.2/app/WEB-INF/conf/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.3.2/bin/

3. Überprüfen Sie Konfigurationsdifferenzen und passen Sie diese bei Bedarf an

RPM/DEB-Version
---------------

Installieren Sie das Paket der neuen Version::

    # RPM
    $ sudo rpm -Uvh fess-15.3.2.rpm

    # DEB
    $ sudo dpkg -i fess-15.3.2.deb

.. note::

   Konfigurationsdateien (``/etc/fess/*``) werden automatisch beibehalten.
   Bei neuen Konfigurationsoptionen ist jedoch eine manuelle Anpassung erforderlich.

Docker-Version
--------------

1. Neue Version der Compose-Dateien herunterladen::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.3.2/compose/compose-opensearch3.yaml

2. Neue Images herunterladen::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

Schritt 4: Upgrade von OpenSearch (falls erforderlich)
=======================================================

Bei Upgrade von OpenSearch befolgen Sie bitte folgende Schritte.

.. warning::

   Führen Sie Major-Version-Upgrades von OpenSearch vorsichtig durch.
   Es können Index-Kompatibilitätsprobleme auftreten.

1. Installieren Sie die neue Version von OpenSearch

2. Plugins neu installieren::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.2
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.2

3. OpenSearch starten::

       $ sudo systemctl start opensearch.service

Schritt 5: Start der neuen Version
===================================

TAR.GZ/ZIP-Version::

    $ cd /path/to/fess-15.3.2
    $ ./bin/fess -d

RPM/DEB-Version::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Schritt 6: Funktionsprüfung
============================

1. **Überprüfung der Protokolle**

   Stellen Sie sicher, dass keine Fehler vorliegen::

       $ tail -f /path/to/fess/logs/fess.log

2. **Zugriff auf die Weboberfläche**

   Greifen Sie mit dem Browser auf http://localhost:8080/ zu.

3. **Anmeldung in der Verwaltungsseite**

   Greifen Sie auf http://localhost:8080/admin zu und melden Sie sich mit dem Administratorkonto an.

4. **Überprüfung der Systeminformationen**

   Klicken Sie in der Verwaltungsseite auf „System" → „Systeminformationen" und überprüfen Sie, dass die Version aktualisiert wurde.

5. **Funktionsprüfung der Suche**

   Führen Sie auf der Suchseite eine Suche durch und überprüfen Sie, dass Ergebnisse korrekt zurückgegeben werden.

Schritt 7: Neuerstellung des Index (empfohlen)
===============================================

Bei Major-Version-Upgrades wird die Neuerstellung des Index empfohlen.

1. Überprüfen Sie bestehende Crawl-Zeitpläne
2. Führen Sie „Default Crawler" unter „System" → „Scheduler" aus
3. Warten Sie, bis der Crawl abgeschlossen ist
4. Überprüfen Sie die Suchergebnisse

Rollback-Verfahren
==================

Bei fehlgeschlagenem Upgrade können Sie mit folgenden Schritten ein Rollback durchführen.

Schritt 1: Stopp der neuen Version
-----------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Schritt 2: Wiederherstellung der alten Version
-----------------------------------------------

Stellen Sie Konfigurationsdateien und Daten aus dem Backup wieder her.

Bei RPM/DEB-Version::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

oder::

    $ sudo dpkg -i fess-<old-version>.deb

Schritt 3: Datenwiederherstellung
----------------------------------

Wiederherstellung aus Snapshot::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

Oder Wiederherstellung des Verzeichnisses aus dem Backup::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

Schritt 4: Start und Überprüfung des Dienstes
----------------------------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Überprüfen Sie den Betrieb und stellen Sie sicher, dass alles wieder normal läuft.

Häufig gestellte Fragen
=======================

F: Ist ein Upgrade ohne Ausfallzeit möglich?
---------------------------------------------

A: Ein Upgrade von Fess erfordert einen Dienststopp. Um die Ausfallzeit zu minimieren, sollten Sie Folgendes in Betracht ziehen:

- Überprüfung der Vorgehensweise in der Testumgebung im Voraus
- Backup im Voraus erstellen
- Ausreichend Wartungszeit einplanen

F: Muss auch OpenSearch aktualisiert werden?
---------------------------------------------

A: Je nach Fess-Version ist eine bestimmte Version von OpenSearch erforderlich.
Überprüfen Sie in den Release Notes die empfohlene OpenSearch-Version.

F: Muss der Index neu erstellt werden?
---------------------------------------

A: Bei Minor-Version-Upgrades normalerweise nicht erforderlich, bei Major-Version-Upgrades wird jedoch eine Neuerstellung empfohlen.

F: Nach dem Upgrade werden keine Suchergebnisse angezeigt
----------------------------------------------------------

A: Überprüfen Sie Folgendes:

1. Überprüfen Sie, ob OpenSearch läuft
2. Überprüfen Sie, ob Indizes vorhanden sind (``curl http://localhost:9200/_cat/indices``)
3. Crawl erneut ausführen

Nächste Schritte
================

Nach Abschluss des Upgrades:

- :doc:`run` - Überprüfung von Start und Erstkonfiguration
- :doc:`security` - Überprüfung der Sicherheitseinstellungen
- Überprüfung neuer Funktionen in den Release Notes
