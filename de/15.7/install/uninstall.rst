========================
Deinstallationsverfahren
========================

Diese Seite beschreibt die Verfahren zur vollständigen Deinstallation von |Fess|.

.. warning::

   **Wichtige Hinweise vor der Deinstallation**

   - Bei der Deinstallation werden alle Daten gelöscht
   - Bei wichtigen Daten erstellen Sie unbedingt ein Backup
   - Backup-Verfahren finden Sie unter :doc:`upgrade`

Vorbereitung vor der Deinstallation
===================================

Erstellung eines Backups
------------------------

Erstellen Sie Backups der benötigten Daten:

1. **Konfigurationsdaten**

   Download über die Verwaltungsseite unter „System" → „Sicherung".
   Mit diesem Vorgang können Sie verschiedene Einstellungen (einschließlich der Crawl-Einstellungen) sowie Suchprotokolle gesammelt exportieren.

2. **Angepasste Konfigurationsdateien**

   TAR.GZ/ZIP-Version::

       $ cp -r /path/to/fess/app/WEB-INF/conf /backup/
       $ cp -r /path/to/fess/app/WEB-INF/classes /backup/

   RPM/DEB-Version::

       $ sudo cp -r /etc/fess /backup/

.. note::

   Der Großteil der Indizes und Einstellungen von |Fess| wird in OpenSearch gespeichert.
   Wenn Sie die Indexdaten sichern möchten, verwenden Sie die Snapshot-Funktion von OpenSearch.
   Ausführliche Anweisungen finden Sie unter :doc:`upgrade`.

Stopp der Dienste
-----------------

Stoppen Sie vor der Deinstallation alle Dienste.

TAR.GZ/ZIP-Version::

    $ ps aux | grep -E 'fess|opensearch'
    $ kill <fess_pid>
    $ kill <opensearch_pid>

RPM/DEB-Version::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Deinstallation der TAR.GZ/ZIP-Version
=====================================

Schritt 1: Löschen von Fess
---------------------------

Löschen Sie das Installationsverzeichnis::

    $ rm -rf /path/to/fess-15.7.0

Schritt 2: Löschen von OpenSearch
---------------------------------

Löschen Sie das OpenSearch-Installationsverzeichnis::

    $ rm -rf /path/to/opensearch-3.7.0

Schritt 3: Löschen des Datenverzeichnisses (Optional)
-----------------------------------------------------

Die Indexdaten von |Fess| werden in OpenSearch gespeichert.
Standardmäßig werden sie innerhalb des OpenSearch-Installationsverzeichnisses gespeichert (z. B. ``opensearch-3.7.0/data``).
Falls Sie mit ``path.data`` einen anderen Speicherort angegeben haben, löschen Sie auch dieses Verzeichnis::

    $ rm -rf /path/to/data

Schritt 4: Löschen des Protokollverzeichnisses (Optional)
---------------------------------------------------------

Löschen Sie die Protokolldateien::

    $ rm -rf /path/to/fess-15.7.0/logs
    $ rm -rf /path/to/opensearch-3.7.0/logs

Deinstallation der RPM-Version
==============================

Schritt 1: Deinstallation von Fess
----------------------------------

Deinstallieren Sie das RPM-Paket::

    $ sudo rpm -e fess

.. note::

   Bei der Deinstallation des |Fess|-Pakets werden durch das Löschskript des Pakets
   der ``fess``-Dienst gestoppt und deaktiviert sowie der Benutzer ``fess`` und die Gruppe ``fess`` automatisch gelöscht.
   Die folgenden Schritte werden ausgeführt, um sicherzustellen, dass diese zuverlässig gelöscht wurden, oder
   um Daten und Konfigurationsdateien manuell zu löschen.

Schritt 2: Deinstallation von OpenSearch
----------------------------------------

::

    $ sudo rpm -e opensearch

Schritt 3: Überprüfung der Deaktivierung der Dienste
----------------------------------------------------

Normalerweise werden die Dienste beim Löschen des Pakets deaktiviert. Um sie sicherheitshalber zu überprüfen bzw. zu deaktivieren, führen Sie Folgendes aus.

Bei systemd::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Bei einer älteren SysV-init-Umgebung (chkconfig)::

    $ sudo /sbin/chkconfig --del fess
    $ sudo /sbin/chkconfig --del opensearch

Schritt 4: Löschen des Datenverzeichnisses
------------------------------------------

.. warning::

   Bei Ausführung dieser Operation werden alle Indexdaten vollständig gelöscht.

Da das Datenverzeichnis bei der Deinstallation des Pakets nicht gelöscht wird, löschen Sie es manuell::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Schritt 5: Löschen der Konfigurationsdateien
--------------------------------------------

Löschen Sie die Konfigurationsdateien und die Umgebungseinstellungsdateien::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/sysconfig/fess
    $ sudo rm -rf /etc/opensearch

.. note::

   Bei RPM können die Konfigurationsdateien in ``/etc/fess`` unter dem Namen ``.rpmsave`` zurückbleiben.
   Um sie vollständig zu löschen, löschen Sie sie wie oben gezeigt manuell.

Schritt 6: Löschen der Protokolldateien
---------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Schritt 7: Löschen des temporären Verzeichnisses (Optional)
-----------------------------------------------------------

::

    $ sudo rm -rf /var/tmp/fess

Schritt 8: Löschen von Benutzer und Gruppe (Optional)
-----------------------------------------------------

Normalerweise werden der Benutzer ``fess`` und die Gruppe ``fess`` beim Löschen des Pakets gelöscht.
Falls sie zurückgeblieben sind oder Sie den Benutzer und die Gruppe für OpenSearch löschen möchten, führen Sie Folgendes aus::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Deinstallation der DEB-Version
==============================

Schritt 1: Deinstallation von Fess
----------------------------------

Deinstallieren Sie das DEB-Paket::

    $ sudo dpkg -r fess

Um es einschließlich der Konfigurationsdateien und der Umgebungseinstellungsdateien vollständig zu löschen, verwenden Sie purge::

    $ sudo dpkg -P fess

.. note::

   Bei ``dpkg -r`` (remove) bleiben die Konfigurationsdateien (conffile) wie ``/etc/default/fess`` zurück.
   Wenn Sie ``dpkg -P`` (purge) verwenden, werden diese Konfigurationsdateien sowie der Benutzer ``fess`` und die Gruppe ``fess`` ebenfalls gelöscht.

Schritt 2: Deinstallation von OpenSearch
----------------------------------------

::

    $ sudo dpkg -r opensearch

Oder vollständiges Löschen einschließlich der Konfigurationsdateien::

    $ sudo dpkg -P opensearch

Schritt 3: Überprüfung der Deaktivierung der Dienste
----------------------------------------------------

Normalerweise werden die Dienste beim Löschen des Pakets deaktiviert. Um sie sicherheitshalber zu überprüfen bzw. zu deaktivieren, führen Sie Folgendes aus::

    $ sudo systemctl disable fess.service
    $ sudo systemctl disable opensearch.service
    $ sudo systemctl daemon-reload

Schritt 4: Löschen des Datenverzeichnisses
------------------------------------------

.. warning::

   Bei Ausführung dieser Operation werden alle Indexdaten vollständig gelöscht.

::

    $ sudo rm -rf /var/lib/fess
    $ sudo rm -rf /var/lib/opensearch

Schritt 5: Löschen der Konfigurationsdateien (bei Nicht-Verwendung von dpkg -P)
-------------------------------------------------------------------------------

::

    $ sudo rm -rf /etc/fess
    $ sudo rm -rf /etc/default/fess
    $ sudo rm -rf /etc/opensearch

Schritt 6: Löschen der Protokolldateien
---------------------------------------

::

    $ sudo rm -rf /var/log/fess
    $ sudo rm -rf /var/log/opensearch

Schritt 7: Löschen von Benutzer und Gruppe (Optional)
-----------------------------------------------------

Falls Sie ``dpkg -P`` nicht verwendet haben, bleiben der Benutzer ``fess`` und die Gruppe ``fess`` zurück.
Um sie zu löschen, führen Sie Folgendes aus::

    $ sudo userdel fess
    $ sudo groupdel fess
    $ sudo userdel opensearch
    $ sudo groupdel opensearch

Deinstallation der Docker-Version
=================================

Schritt 1: Löschen von Containern und Netzwerken
------------------------------------------------

Löschen Sie die Container sowie das von Docker Compose erstellte Netzwerk (``search_net``)::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Schritt 2: Löschen der Volumes
------------------------------

.. warning::

   Bei Ausführung dieser Operation werden alle Daten vollständig gelöscht.

Die Daten von |Fess| (Indizes, Wörterbücher usw.) werden in den Volumes von OpenSearch gespeichert.
Überprüfen Sie zunächst die Liste der Volumes::

    $ docker volume ls

Löschen Sie die OpenSearch-bezogenen Volumes::

    $ docker volume rm <project>_search01_data
    $ docker volume rm <project>_search01_dictionary

.. note::

   Den Volume-Namen wird der Projektname von Docker Compose (normalerweise der Name des
   Verzeichnisses, in dem die Compose-Dateien abgelegt sind) als Präfix vorangestellt. Überprüfen Sie die tatsächlichen Namen mit ``docker volume ls``.

Um Container und Volumes auf einmal zu löschen, fügen Sie ``down`` die Option ``-v`` hinzu::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Schritt 3: Löschen der Images (Optional)
----------------------------------------

Wenn Sie Docker-Images löschen und Festplattenplatz freigeben möchten::

    $ docker images | grep fess
    $ docker rmi ghcr.io/codelibs/fess:15.7.0
    $ docker rmi ghcr.io/codelibs/fess-opensearch:3.7.0

Schritt 4: Löschen der Compose-Dateien
--------------------------------------

::

    $ rm compose.yaml compose-opensearch3.yaml

Überprüfung der Deinstallation
==============================

Überprüfen Sie, dass alle Komponenten gelöscht wurden.

Überprüfung der Prozesse
------------------------

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
-----------------------

TAR.GZ/ZIP-Version::

    $ ls /path/to/fess-15.7.0  # Überprüfen, dass Verzeichnis nicht existiert

RPM/DEB-Version::

    $ ls /var/lib/fess  # Überprüfen, dass Verzeichnis nicht existiert
    $ ls /etc/fess      # Überprüfen, dass Verzeichnis nicht existiert

Docker-Version::

    $ docker ps -a | grep -E 'fess01|search01'  # Überprüfen, dass Container nicht existieren
    $ docker volume ls | grep search01           # Überprüfen, dass Volumes nicht existieren

Überprüfung der Pakete
----------------------

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
----------------------------------------

Falls Sie OpenSearch auch für andere Anwendungen verwenden, können Sie nur Fess löschen.

1. Fess stoppen
2. Fess-Paket oder -Verzeichnis löschen
3. Fess-Datenverzeichnis löschen (``/var/lib/fess`` usw.)
4. Die in OpenSearch erstellten |Fess|-Indizes (``fess.*``, ``.fess_*`` usw.) löschen
5. OpenSearch nicht löschen

Nur OpenSearch löschen und Fess behalten
----------------------------------------

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
--------------------------------

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
--------------------------------------

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
================================

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
