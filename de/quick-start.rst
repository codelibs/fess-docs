====================
Schnellstart-Anleitung
====================

Einführung
==========

Fess ist ein Open-Source-Volltextsuchserver, der Websites und Dateiserver durchsucht und eine dokumentenübergreifende Suche des gesammelten Inhalts ermöglicht.

Diese Anleitung richtet sich an Personen, die Fess schnell ausprobieren möchten, und beschreibt die Mindestschritte zur Inbetriebnahme.

Welche Methode sollten Sie verwenden?
======================================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - Docker (Empfohlen)
     - ZIP-Paket
   * - Voraussetzungen
     - Docker und Docker Compose
     - Java 21, OpenSearch
   * - Einfachheit
     - ◎ Nur wenige Befehle
     - △ Mehrere Software-Installationen erforderlich
   * - Am besten für
     - Diejenigen, die es zuerst ausprobieren möchten
     - Umgebungen, in denen Docker nicht verfügbar ist

Methode 1: Docker (Empfohlen)
==============================

Geschätzte Zeit: **5–10 Minuten beim ersten Start** (einschließlich Docker-Image-Download)

Docker bietet den schnellsten und zuverlässigsten Weg, Fess auszuführen. Alle Abhängigkeiten
sind gebündelt, sodass Sie nichts anderes installieren müssen.

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

**Schritt 4: Fess stoppen**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

Für erweiterte Docker-Konfiguration (benutzerdefinierte Einstellungen, externes OpenSearch, Kubernetes)
siehe die :doc:`Docker-Installationsanleitung <15.6/install/install-docker>`.

----

Methode 2: ZIP-Paket
=====================

Geschätzte Zeit: **20–30 Minuten beim ersten Start** (einschließlich Java- und OpenSearch-Installation)

Wenn Sie Docker nicht verwenden möchten, können Sie Fess direkt aus dem ZIP-Paket ausführen.

.. note::

   Diese Methode ist für Evaluierungszwecke gedacht. Für Produktionsumgebungen
   empfehlen wir Docker oder die Installation mit :doc:`RPM/DEB-Paketen <setup>`.

Voraussetzungen
---------------

Bitte installieren Sie die folgende Software, bevor Sie Fess starten.

**1. Java 21 installieren**

Wir empfehlen `Eclipse Temurin <https://adoptium.net/temurin>`__ Java 21.

**2. OpenSearch installieren und starten**

OpenSearch wird zum Speichern der Fess-Daten benötigt.
Bitte installieren und starten Sie es gemäß der :doc:`Installationsanleitung <setup>`.

Download und Installation
-------------------------

1. Laden Sie das neueste ZIP-Paket von `GitHub Releases <https://github.com/codelibs/fess/releases>`__ herunter

2. Entpacken Sie es und wechseln Sie in das Verzeichnis:

.. code-block:: bash

    unzip fess-x.y.z.zip
    cd fess-x.y.z

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

.. warning::

   Bitte ändern Sie das Standard-Passwort. In Produktionsumgebungen wird empfohlen,
   das Passwort sofort nach der ersten Anmeldung zu ändern.

Fess stoppen (ZIP)
------------------

Drücken Sie ``Strg+C`` im Terminal oder verwenden Sie ``kill``, um den Fess-Prozess zu beenden.

----

Crawl-Konfiguration und Suche
==============================

**1. Web-Crawl-Konfiguration erstellen**

1. Melden Sie sich im Admin-Bereich an (http://localhost:8080/admin)
2. Navigieren Sie zu **Crawler** → **Web** im linken Menü
3. Klicken Sie auf **Neu**, um eine neue Konfiguration zu erstellen
4. Füllen Sie die erforderlichen Felder aus:

   - **Name:** Mein erster Crawl
   - **URL:** https://www.example.com/ (URL der zu crawlenden Website)
   - **Max. Zugriffe:** 10 (für erste Tests wird ein kleiner Wert empfohlen)
   - **Intervall:** 1000 (Millisekunden zwischen Anfragen; der Standardwert ``1000`` ms wird empfohlen)

5. Klicken Sie auf **Erstellen**, um zu speichern

.. warning::

   Ein zu hoher Max.-Zugriffsanzahl-Wert kann den Zielserver übermäßig belasten.
   Beginnen Sie bei der Funktionsprüfung immer mit einem kleinen Wert (ca. 10–100).
   Beim Crawlen von Seiten, die Sie nicht verwalten, befolgen Sie bitte die robots.txt-Einstellungen.

**2. Crawler ausführen**

1. Gehen Sie zu **System** → **Scheduler**
2. Finden Sie **Default Crawler** in der Liste
3. Klicken Sie auf **Jetzt starten**
4. Überwachen Sie den Fortschritt unter **System** → **Crawl-Informationen**

Für geplante Ausführung wählen Sie **Default Crawler** und konfigurieren Sie den Zeitplan.
Wenn die Startzeit 10:35 Uhr ist, geben Sie ``35 10 * * ?`` ein (Format: ``Minute Stunde Tag Monat Wochentag``).

**3. Suchen**

Sobald das Crawling abgeschlossen ist (prüfen Sie WebIndexSize in den Sitzungsinformationen):

Besuchen Sie http://localhost:8080/ und geben Sie einen Suchbegriff ein, um Ihre Ergebnisse zu sehen.

----

Was kommt als Nächstes?
=======================

- :doc:`Vollständige Dokumentation <documentation>` - Umfassendes Referenzhandbuch
- :doc:`Installationsanleitung <setup>` - Optionen für Produktionsbereitstellung
- :doc:`Admin-Handbuch <15.6/admin/index>` - Konfiguration und Verwaltung
- :doc:`API-Referenz <15.6/api/index>` - Integration der Suche in Ihre Anwendungen
- `Diskussionsforum <https://discuss.codelibs.org/c/fessen/>`__ - Fragen stellen, Tipps teilen
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Fehler melden, Features anfordern
