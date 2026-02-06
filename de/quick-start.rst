====================
Schnellstart-Anleitung
====================

Fess in unter 5 Minuten zum Laufen bringen
==========================================

Willkommen! Diese Anleitung hilft Ihnen, Fess so schnell wie möglich zum Laufen zu bringen.
Wählen Sie die Methode, die am besten zu Ihrer Umgebung passt.

.. tip::

   **Schnellster Weg: Docker (Empfohlen)**

   Wenn Sie Docker installiert haben, können Sie Fess in etwa 3 Minuten
   mit nur wenigen Befehlen starten – keine weiteren Abhängigkeiten erforderlich.

----

Methode 1: Docker (Empfohlen)
=============================

Docker bietet den schnellsten und zuverlässigsten Weg, Fess auszuführen. Alle Abhängigkeiten
sind gebündelt, sodass Sie nichts anderes installieren müssen.

**Voraussetzungen:**

- Docker 20.10 oder neuer
- Docker Compose 2.0 oder neuer

**Schritt 1: Konfigurationsdateien herunterladen**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Schritt 2: Container starten**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Schritt 3: Auf Fess zugreifen**

Warten Sie einige Minuten, bis die Dienste initialisiert sind, und öffnen Sie dann Ihren Browser:

- **Suchoberfläche:** http://localhost:8080/
- **Admin-Bereich:** http://localhost:8080/admin
- **Standard-Anmeldedaten:** admin / admin

.. warning::

   **Sicherheitshinweis:** Ändern Sie das Standard-Admin-Passwort sofort nach Ihrer ersten Anmeldung.

**Fess stoppen:**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

Für erweiterte Docker-Konfiguration (benutzerdefinierte Einstellungen, externes OpenSearch, Kubernetes)
siehe die `Docker-Installationsanleitung <15.5/install/install-docker.html>`__.

----

Methode 2: ZIP-Paket
====================

Wenn Sie Docker nicht verwenden möchten, können Sie Fess direkt aus dem ZIP-Paket ausführen.

.. note::

   Diese Methode ist für Evaluierungszwecke gedacht. Für Produktionsumgebungen
   empfehlen wir Docker oder die Installation mit :doc:`RPM/DEB-Paketen <setup>`.

Voraussetzungen
---------------

**Java 21** ist erforderlich. Wir empfehlen `Eclipse Temurin <https://adoptium.net/temurin>`__.

Überprüfen Sie Ihre Java-Installation:

.. code-block:: bash

    java -version

Download und Installation
-------------------------

1. Laden Sie das neueste ZIP-Paket von `GitHub Releases <https://github.com/codelibs/fess/releases>`__ herunter

2. Entpacken Sie es und wechseln Sie in das Verzeichnis:

.. code-block:: bash

    unzip fess-15.5.0.zip
    cd fess-15.5.0

Fess starten
------------

.. code-block:: bash

    # Linux/Mac
    ./bin/fess

    # Windows
    bin\fess.bat

Warten Sie etwa 30 Sekunden, bis Fess gestartet ist, und greifen Sie dann zu auf:

- http://localhost:8080/ (Suche)
- http://localhost:8080/admin (Admin - Login: admin/admin)

Fess stoppen
------------

Drücken Sie ``Strg+C`` im Terminal oder verwenden Sie ``kill``, um den Fess-Prozess zu beenden.

----

Ihre erste Suche: Ein kurzes Tutorial
=====================================

Jetzt, da Fess läuft, richten wir Ihren ersten Web-Crawl ein.

Schritt 1: Web-Crawl-Konfiguration erstellen
--------------------------------------------

1. Melden Sie sich im Admin-Bereich an (http://localhost:8080/admin)
2. Navigieren Sie zu **Crawler** → **Web** im linken Menü
3. Klicken Sie auf **Neu**, um eine neue Konfiguration zu erstellen
4. Füllen Sie die erforderlichen Felder aus:

   - **Name:** Mein erster Crawl
   - **URL:** https://fess.codelibs.org/ (oder eine beliebige Website, die Sie indexieren möchten)
   - **Max. Zugriffe:** 100 (begrenzt die zu crawlenden Seiten)
   - **Intervall:** 1000 (Millisekunden zwischen Anfragen)

5. Klicken Sie auf **Erstellen**, um zu speichern

Schritt 2: Crawler ausführen
----------------------------

1. Gehen Sie zu **System** → **Scheduler**
2. Finden Sie **Default Crawler** in der Liste
3. Klicken Sie auf **Jetzt starten**
4. Überwachen Sie den Fortschritt unter **System** → **Crawl-Informationen**

Schritt 3: Ihre Inhalte durchsuchen
-----------------------------------

Sobald das Crawling abgeschlossen ist (prüfen Sie WebIndexSize in den Sitzungsinformationen):

1. Besuchen Sie http://localhost:8080/
2. Geben Sie einen Suchbegriff ein, der sich auf die gecrawlten Seiten bezieht
3. Sehen Sie Ihre Suchergebnisse!

----

Was kommt als Nächstes?
=======================

**Bereit, tiefer einzusteigen?**

- `Vollständige Dokumentation <documentation.html>`__ - Umfassendes Referenzhandbuch
- `Installationsanleitung <setup.html>`__ - Optionen für Produktionsbereitstellung
- `Admin-Handbuch <15.5/admin/index.html>`__ - Konfiguration und Verwaltung
- `API-Referenz <15.5/api/index.html>`__ - Integration der Suche in Ihre Anwendungen

**Brauchen Sie Hilfe?**

- `Diskussionsforum <https://discuss.codelibs.org/c/fessen/>`__ - Fragen stellen, Tipps teilen
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Fehler melden, Features anfordern
- `Kommerzieller Support <support-services.html>`__ - Professionelle Unterstützung

**Weitere Funktionen entdecken:**

- Dateisystem-Crawling (lokale Dateien, Netzwerkfreigaben)
- Datenbankintegration
- LDAP/Active Directory-Authentifizierung
- Benutzerdefiniertes Ranking der Suchergebnisse
- Mehrsprachige Unterstützung

