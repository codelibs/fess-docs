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
     - Java 21 (OpenSearch wird mit dem Befehl ``fess-setup`` installiert)
   * - Einfachheit
     - ◎ Nur wenige Befehle
     - △ Java installieren, dann einige Setup-Befehle ausführen
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
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose-opensearch3.yaml

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
siehe die :doc:`Docker-Installationsanleitung <15.9/install/install-docker>`.

----

Methode 2: ZIP-Paket
=====================

Geschätzte Zeit: **20–30 Minuten beim ersten Start** (einschließlich Java-Installation und OpenSearch-Download)

Wenn Sie Docker nicht verwenden möchten, können Sie Fess direkt aus dem ZIP-Paket ausführen.
Fess bündelt keine Suchmaschine. Der im ZIP-Paket enthaltene Befehl ``fess-setup``
lädt OpenSearch herunter und installiert die von Fess benötigten Plugins.

.. note::

   Diese Methode ist für Evaluierungszwecke gedacht. Für Produktionsumgebungen
   empfehlen wir Docker oder die Installation mit :doc:`RPM/DEB-Paketen <setup>`.

Voraussetzungen
---------------

Installieren Sie vor dem Start Java 21. Wir empfehlen `Eclipse Temurin <https://adoptium.net/temurin>`__ Java 21.
OpenSearch muss nicht vorab installiert werden: Schritt 2 installiert es.

.. note::

   OpenSearch veröffentlicht offizielle Builds nur für Linux und Windows. Unter macOS
   endet ``fess-setup install opensearch`` mit einem Fehler; verwenden Sie Docker (Methode 1) oder lesen Sie
   :doc:`15.9/install/install-linux` zur Installation von OpenSearch mit Homebrew.

Schritt 1: Herunterladen und Entpacken
--------------------------------------

Laden Sie das neueste ZIP-Paket von `GitHub Releases <https://github.com/codelibs/fess/releases>`__ herunter,
entpacken Sie es und wechseln Sie in das Verzeichnis:

.. code-block:: bash

    unzip fess-x.y.z.zip
    cd fess-x.y.z

Schritt 2: OpenSearch installieren
----------------------------------

Führen Sie ``fess-setup`` als normaler Benutzer aus, nicht als ``root``: OpenSearch weigert sich, als ``root`` zu starten.

.. code-block:: bash

    # Linux
    bin/fess-setup install opensearch

    # Windows
    bin\fess-setup.bat install opensearch

Dies lädt die von dieser Fess-Version unterstützte OpenSearch-Version in das Verzeichnis ``opensearch/`` im Fess-Verzeichnis herunter,
installiert die vier von Fess benötigten Plugins und fügt die von Fess benötigten Einstellungen in die Datei
``config/opensearch.yml`` ein. ``bin/fess`` findet dieses OpenSearch selbstständig, sodass keine Konfigurationsdatei
bearbeitet werden muss, solange OpenSearch auf demselben Host läuft.

.. warning::

   Der Befehl setzt ``plugins.security.disabled: true``, sodass OpenSearch Anfragen ohne
   Authentifizierung akzeptiert. Standardmäßig lauscht es nur auf der Loopback-Adresse; setzen Sie es keinem
   Netzwerk aus. Einstellungen für die Produktion finden Sie unter :doc:`15.9/install/security`.

Alle Befehle (Installation von Node.js und Plugins, ``check``) finden Sie unter :doc:`15.9/install/fess-setup`.

Schritt 3: OpenSearch und Fess starten
--------------------------------------

Starten Sie zuerst OpenSearch, dann Fess:

.. code-block:: bash

    # Linux
    opensearch/opensearch-3.9.0/bin/opensearch -d
    bin/fess

.. code-block:: bat

    :: Windows (jeweils in einer eigenen Eingabeaufforderung ausführen)
    opensearch\opensearch-3.9.0\bin\opensearch.bat
    bin\fess.bat

Warten Sie etwa 30 Sekunden, bis Fess gestartet ist, und greifen Sie dann zu auf:

- http://localhost:8080/ (Suche)
- http://localhost:8080/admin (Admin - Login: admin/admin)

Zur Überprüfung der Installation führen Sie ``bin/fess-setup check`` aus (unter Windows ``bin\fess-setup.bat check``).
Der Befehl meldet, ob OpenSearch erreichbar ist und die von Fess benötigten Plugins besitzt.

.. warning::

   Bitte ändern Sie das Standard-Passwort. In Produktionsumgebungen wird empfohlen,
   das Passwort sofort nach der ersten Anmeldung zu ändern.

Fess stoppen (ZIP)
------------------

Drücken Sie ``Strg+C`` im Terminal oder verwenden Sie ``kill``, um den Fess-Prozess zu beenden.
Beenden Sie anschließend OpenSearch auf dieselbe Weise (``kill`` für den Prozess oder ``Strg+C``, wenn es im Vordergrund läuft).

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
   - **Intervall:** 10000 (Millisekunden zwischen Anfragen; der Standardwert ``10000`` ms wird empfohlen)

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
- :doc:`Admin-Handbuch <15.9/admin/index>` - Konfiguration und Verwaltung
- :doc:`API-Referenz <15.9/api/index>` - Integration der Suche in Ihre Anwendungen
- `Diskussionsforum <https://discuss.codelibs.org/c/fessen/>`__ - Fragen stellen, Tipps teilen
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - Fehler melden, Features anfordern
