==================
Deinstallationsverfahren
==================

Diese Seite beschreibt die Verfahren zur vollständigen Deinstallation von |Fess|.

.. warning::

   **Wichtige Hinweise vor der Deinstallation**

   - Bei der Deinstallation werden alle Daten gelöscht
   - Bei wichtigen Daten erstellen Sie unbedingt ein Backup
   - Backup-Verfahren finden Sie unter :doc:`upgrade`

Vorbereitung vor der Deinstallation
====================================

Erstellung eines Backups
-------------------------

Erstellen Sie Backups der benötigten Daten:

1. **Konfigurationsdaten**

   Download über die Verwaltungsseite unter „System" → „Backup"

2. **Crawl-Konfiguration**

   Exportieren Sie bei Bedarf die Crawl-Konfiguration

3. **Angepasste Konfigurationsdateien**

   TAR.GZ/ZIP-Version::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB-Version::

       $ sudo cp -r /etc/fess /backup/

Stopp der Dienste
-----------------

Stoppen Sie vor der Deinstallation alle Dienste.

TAR.GZ/ZIP-Version::

    $ ps aux | grep fess
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB-Version::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Deinstallation der TAR.GZ/ZIP-Version
======================================

Schritt 1: Löschen von Fess
----------------------------

Löschen Sie das Installationsverzeichnis::

    $ rm -rf /path/to/fess-15.4.0

Schritt 2: Löschen von OpenSearch
----------------------------------

Löschen Sie das OpenSearch-Installationsverzeichnis::

    $ rm -rf /path/to/opensearch-3.3.2

Schritt 3: Löschen des Datenverzeichnisses (Optional)
------------------------------------------------------

Standardmäßig befindet sich das Datenverzeichnis im Fess-Installationsverzeichnis.
Falls Sie einen anderen Speicherort angegeben haben, löschen Sie auch dieses Verzeichnis::

    $ rm -rf /path/to/data

Schritt 4: Löschen des Protokollverzeichnisses (Optional)
----------------------------------------------------------

Löschen Sie die Protokolldateien::

    $ rm -rf /path/to/fess/logs
    $ rm -rf /path/to/opensearch/logs

Deinstallation der RPM-Version
===============================

Schritt 1: Deinstallation von Fess
-----------------------------------

Deinstallieren Sie das RPM-Paket::

    $ sudo rpm -e fess

Schritt 2: Deinstallation von OpenSearch
-----------------------------------------

::

    $ sudo rpm -e opensearch

Schritt 3: Deaktivierung und Löschung der Dienste
--------------------------------------------------

Bei chkconfig::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

Bei systemd::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Schritt 4: Löschen des Datenverzeichnisses
-------------------------------------------

.. warning::

   Diese Operation löscht alle Indexdaten und Konfigurationen vollständig.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Schritt 5: Löschen der Konfigurationsdateien
---------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Schritt 6: Löschen der Protokolldateien
----------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Schritt 7: Löschen von Benutzer und Gruppe (Optional)
------------------------------------------------------

Falls Sie Systembenutzer und -gruppen löschen möchten::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Deinstallation der DEB-Version
===============================

Schritt 1: Deinstallation von Fess
-----------------------------------

Deinstallieren Sie das DEB-Paket::

    $ sudo dpkg -r fess

Zum vollständigen Löschen einschließlich Konfigurationsdateien::

    $ sudo dpkg -P fess

Schritt 2: Deinstallation von OpenSearch
-----------------------------------------

::

    $ sudo dpkg -r opensearch

Oder vollständiges Löschen einschließlich Konfigurationsdateien::

    $ sudo dpkg -P opensearch

Schritt 3: Deaktivierung der Dienste
-------------------------------------

::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Schritt 4: Löschen des Datenverzeichnisses
-------------------------------------------

.. warning::

   Diese Operation löscht alle Indexdaten und Konfigurationen vollständig.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Schritt 5: Löschen der Konfigurationsdateien (bei Nicht-Verwendung von dpkg -P)
--------------------------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/opensearch

Schritt 6: Löschen der Protokolldateien
----------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Schritt 7: Löschen von Benutzer und Gruppe (Optional)
------------------------------------------------------

Falls Sie Systembenutzer und -gruppen löschen möchten::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Deinstallation der Docker-Version
==================================

Schritt 1: Löschen von Containern und Netzwerken
-------------------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Schritt 2: Löschen der Volumes
-------------------------------

.. warning::

   Diese Operation löscht alle Daten vollständig.

Liste der Volumes überprüfen::

    $ docker volume ls

Fess-bezogene Volumes löschen::

    $ docker volume rm fess-es-data
    $ docker volume rm fess-data

Oder alle Volumes auf einmal löschen::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Schritt 3: Löschen der Images (Optional)
-----------------------------------------

Falls Sie Docker-Images löschen und Festplattenplatz freigeben möchten::

    $ docker images | grep fess
    $ docker rmi codelibs/fess:15.4.0

    $ docker images | grep opensearch
    $ docker rmi opensearchproject/opensearch:3.3.2

Schritt 4: Löschen der Netzwerke (Optional)
--------------------------------------------

Löschen Sie von Docker Compose erstellte Netzwerke::

    $ docker network ls
    $ docker network rm <network_name>

Schritt 5: Löschen der Compose-Dateien
---------------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Überprüfung der Deinstallation
===============================

Überprüfen Sie, dass alle Komponenten gelöscht wurden.

Überprüfung der Prozesse
-------------------------

::

    $ ps aux | grep fess
    $ ps aux | grep opensearch

Wenn nichts angezeigt wird, sind die Prozesse gestoppt.

Überprüfung der Ports
---------------------

::

    $ sudo netstat -tuln | grep 8080
    $ sudo netstat -tuln | grep 9200

Überprüfen Sie, dass keine Ports verwendet werden.

Überprüfung der Dateien
------------------------

TAR.GZ/ZIP-Version::

    $ ls /path/to/fess-15.4.0  # Überprüfen, dass Verzeichnis nicht existiert

RPM/DEB-Version::

    $ ls /var/lib/fess  # Überprüfen, dass Verzeichnis nicht existiert
    $ ls /etc/fess      # Überprüfen, dass Verzeichnis nicht existiert

Docker-Version::

    $ docker ps -a | grep fess  # Überprüfen, dass Container nicht existieren
    $ docker volume ls | grep fess  # Überprüfen, dass Volumes nicht existieren

Überprüfung der Pakete
-----------------------

RPM-Version::

    $ rpm -qa | grep fess
    $ rpm -qa | grep opensearch

DEB-Version::

    $ dpkg -l | grep fess
    $ dpkg -l | grep opensearch

Wenn nichts angezeigt wird, sind die Pakete gelöscht.

Teilweise Deinstallation
========================

Nur Fess löschen und OpenSearch behalten
-----------------------------------------

Falls Sie OpenSearch auch für andere Anwendungen verwenden, können Sie nur Fess löschen.

1. Fess stoppen
2. Fess-Paket oder -Verzeichnis löschen
3. Fess-Datenverzeichnis löschen (``/var/lib/fess`` usw.)
4. OpenSearch nicht löschen

Nur OpenSearch löschen und Fess behalten
-----------------------------------------

.. warning::

   Wenn Sie OpenSearch löschen, funktioniert Fess nicht mehr.
   Ändern Sie die Konfiguration, um sich mit einem anderen OpenSearch-Cluster zu verbinden.

1. OpenSearch stoppen
2. OpenSearch-Paket oder -Verzeichnis löschen
3. OpenSearch-Datenverzeichnis löschen (``/var/lib/opensearch`` usw.)
4. Fess-Konfiguration aktualisieren und anderen OpenSearch-Cluster angeben

Fehlerbehebung
==============

Paket kann nicht gelöscht werden
---------------------------------

**Symptom:**

Fehler bei ``rpm -e`` oder ``dpkg -r``.

**Lösung:**

1. Überprüfen Sie, dass der Dienst gestoppt ist::

       $ sudo systemctl stop fess.service

2. Überprüfen Sie Abhängigkeiten::

       $ rpm -qa | grep fess
       $ dpkg -l | grep fess

3. Erzwungenes Löschen (letzte Option)::

       $ sudo rpm -e --nodeps fess
       $ sudo dpkg -r --force-all fess

Verzeichnis kann nicht gelöscht werden
---------------------------------------

**Symptom:**

Verzeichnis kann mit ``rm -rf`` nicht gelöscht werden.

**Lösung:**

1. Überprüfen Sie Berechtigungen::

       $ ls -ld /path/to/directory

2. Löschen mit sudo::

       $ sudo rm -rf /path/to/directory

3. Überprüfen Sie, ob Prozesse Dateien verwenden::

       $ sudo lsof | grep /path/to/directory

Vorbereitung für Neuinstallation
=================================

Bei Neuinstallation nach der Deinstallation überprüfen Sie Folgendes:

1. Alle Prozesse sind gestoppt
2. Alle Dateien und Verzeichnisse sind gelöscht
3. Ports 8080 und 9200 werden nicht verwendet
4. Keine früheren Konfigurationsdateien vorhanden

Neuinstallationsverfahren finden Sie unter :doc:`install`.

Nächste Schritte
================

Nach Abschluss der Deinstallation:

- Bei Installation einer neuen Version siehe :doc:`install`
- Bei Datenmigration siehe :doc:`upgrade`
- Bei Erwägung alternativer Suchlösungen siehe die offizielle Fess-Website
