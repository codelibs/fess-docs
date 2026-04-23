================
Installationsanleitung
================

Installationsmethode
====================

Fess bietet Distributionen als ZIP-Archive, RPM/DEB-Pakete und Docker-Images an.
Mit Docker können Sie Fess auf Windows, Mac und anderen Systemen einfach einrichten.

.. note::

   Diese Seite erklärt das Setup unter **Windows mit Docker**. Benutzer von Linux oder macOS können ähnliche Schritte befolgen, aber die Docker Desktop-Installation unterscheidet sich je nach Plattform.
   Weitere Details finden Sie in der `Docker <https://docs.docker.com/get-docker/>`_-Dokumentation.

Wenn Sie eine Produktionsumgebung aufbauen, lesen Sie bitte unbedingt :doc:`15.6/install/index`.
Die Systemanforderungen finden Sie unter :doc:`15.6/install/prerequisites`.

.. warning::

   **Wichtige Hinweise für die Produktionsumgebung**

   In Produktionsumgebungen oder bei Lasttests wird der Betrieb mit eingebettetem OpenSearch nicht empfohlen.
   Richten Sie unbedingt einen externen OpenSearch-Server ein.

Setup-Übersicht
---------------

Gehen Sie die folgenden Schritte der Reihe nach durch:

1. Docker Desktop installieren
2. Betriebssystem konfigurieren (vm.max_map_count anpassen)
3. Fess-Startdateien herunterladen
4. Fess starten und Betrieb überprüfen

Installation von Docker Desktop
================================

Wenn Docker Desktop nicht installiert ist, folgen Sie bitte den folgenden Schritten zur Installation.

Download
--------

Laden Sie das Installationsprogramm für Ihr Betriebssystem von `Docker Desktop <https://www.docker.com/products/docker-desktop/>`__ herunter.

Ausführen des Installationsprogramms
-------------------------------------

Doppelklicken Sie auf das heruntergeladene Installationsprogramm, um die Installation zu starten.

Vergewissern Sie sich, dass „Install required Windows components for WSL 2" oder
„Install required Enable Hyper-V Windows Features" ausgewählt ist,
und klicken Sie auf OK.

|image0|

Wenn die Installation abgeschlossen ist, klicken Sie auf die Schaltfläche „close", um das Fenster zu schließen.

|image1|

Starten von Docker Desktop
---------------------------

Klicken Sie im Windows-Menü auf „Docker Desktop", um es zu starten.

|image2|

Nach dem Start von Docker Desktop werden die Nutzungsbedingungen angezeigt. Aktivieren Sie „I accept the terms" und klicken Sie auf „Accept".

Es erscheint eine Aufforderung zum Start des Tutorials, aber hier klicken wir auf „Skip tutorial", um es zu überspringen.
Wenn Sie auf „Skip tutorial" klicken, wird das Dashboard angezeigt.

|image3|

Konfiguration
=============

Damit OpenSearch als Docker-Container ausgeführt werden kann, passen Sie den Wert von „vm.max_map_count" auf der Betriebssystemseite an.
Die Konfigurationsmethode variiert je nach verwendeter Umgebung. Informationen zu den jeweiligen Konfigurationsmethoden finden Sie unter „`Set vm.max_map_count to at least 262144 <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144>`_".

Einrichten von Fess
===================

Erstellen der Startdatei
-------------------------

Erstellen Sie einen geeigneten Ordner und laden Sie `compose.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml>`_ und `compose-opensearch3.yaml <https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml>`_ herunter.

.. note::

   ``compose-opensearch3.yaml`` ist eine zusätzliche Konfigurationsdatei für die Verwendung von OpenSearch 3.x.
   Sie wird in Kombination mit ``compose.yaml`` verwendet.

Sie können sie auch mit dem curl-Befehl wie folgt abrufen:

.. code-block:: bash

    curl -o compose.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -o compose-opensearch3.yaml https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

Starten von Fess
----------------

Starten Sie Fess mit dem docker compose-Befehl.

Öffnen Sie die Eingabeaufforderung, navigieren Sie zu dem Ordner, in dem sich die Datei compose.yaml befindet, und führen Sie den folgenden Befehl aus:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Der Start kann einige Minuten dauern.
   Sie können die Logs mit folgendem Befehl überprüfen:

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f

   Mit ``Ctrl+C`` können Sie die Protokollanzeige beenden.


Funktionsüberprüfung
====================

.. note::

   Nach dem Start können Sie den Betrieb in Ihrem Browser unter folgenden URLs überprüfen:

   - **Suche:** http://localhost:8080/
   - **Verwaltungs-UI:** http://localhost:8080/admin/

Der Standard-Benutzername/das Passwort für das Administratorkonto ist admin/admin.

.. warning::

   **Wichtiger Sicherheitshinweis**

   Ändern Sie unbedingt das Standardpasswort.
   Besonders in Produktionsumgebungen wird dringend empfohlen, das Passwort sofort nach der ersten Anmeldung zu ändern.

Das Administratorkonto wird vom Anwendungsserver verwaltet.
Die Verwaltungs-UI von Fess betrachtet Benutzer als Administratoren, die vom Anwendungsserver mit der fess-Rolle authentifiziert wurden.

Sonstiges
=========

Stoppen von Fess
----------------

Um Fess zu stoppen, führen Sie den folgenden Befehl im Ordner aus, in dem Sie Fess gestartet haben:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml stop

Um Container zu stoppen und zu entfernen:

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   Um auch Volumes mit dem ``down``-Befehl zu entfernen, fügen Sie die Option ``-v`` hinzu.
   In diesem Fall werden alle Daten gelöscht, seien Sie also vorsichtig.

   .. code-block:: bash

       docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Ändern des Administrator-Passworts
-----------------------------------

Sie können das Passwort im Benutzerbearbeitungsbildschirm der Verwaltungs-UI ändern.

1. Rufen Sie http://localhost:8080/admin/ auf und melden Sie sich an.
2. Wählen Sie „Benutzer" aus dem Menü oben rechts.
3. Öffnen Sie die Bearbeitungsseite des Admin-Benutzers und ändern Sie das Passwort.

Nächste Schritte
================

Nach dem Einrichten von Fess können Sie mit folgender Dokumentation weiterarbeiten:

- :doc:`15.6/install/run` — Detaillierte Anleitung zum Starten, Stoppen und Konfigurieren
- :doc:`15.6/admin/index` — Administratorhandbuch (Crawl-Einstellungen, Benutzerverwaltung usw.)
- :doc:`15.6/user/index` — Benutzerhandbuch (Suche verwenden)

Bei Problemen lesen Sie bitte :doc:`15.6/install/troubleshooting`.

.. |image0| image:: ../resources/images/en/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/en/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/en/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/en/install/dockerdesktop-4.png
