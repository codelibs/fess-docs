=============================================
Google Gemini-Konfiguration (AI-Suche / RAG)
=============================================

Übersicht
=========

Diese Seite erläutert, wie Sie das Plugin ``fess-llm-gemini`` konfigurieren, damit |Fess| Google Gemini für seinen **AI-Suchmodus (RAG: Retrieval-Augmented Generation)** nutzen kann — die Beantwortung natürlichsprachlicher Fragen aus Ihrem Unternehmens-Suchindex mit zitierten Quellen. |Fess| ruft die Google AI API (Generative Language API) auf, um RAG über Ihre gecrawlten Dokumente mit Gemini-Modellen auszuführen.

Google Gemini ist ein hochmodernes großes Sprachmodell (LLM) von Google.
|Fess| kann die Google AI API (Generative Language API) verwenden, um die AI-Suchmodus-Funktion mit Gemini-Modellen zu realisieren.

Durch die Verwendung von Gemini wird eine hochwertige Antwortgenerierung mit Googles neuester KI-Technologie ermöglicht.

Hauptmerkmale
-------------

- **Multimodal-Unterstützung**: Kann nicht nur Text, sondern auch Bilder verarbeiten
- **Langer Kontext**: Langes Kontextfenster zur gleichzeitigen Verarbeitung großer Dokumentmengen
- **Kosteneffizienz**: Flash-Modelle sind schnell und kostengünstig
- **Google-Integration**: Einfache Integration mit Google Cloud-Diensten

Unterstützte Modelle
--------------------

Hauptsächlich verfügbare Modelle bei Gemini:

- ``gemini-3.1-flash-lite-preview`` - Schnelles Modell, leichtgewichtig und kostengünstig (Standard)
- ``gemini-3-flash-preview`` - Standard-Flash-Modell
- ``gemini-3.1-pro`` / ``gemini-3-pro`` - Modelle mit hoher Schlussfolgerungsfähigkeit
- ``gemini-2.5-flash`` - Stabile Version des schnellen Modells
- ``gemini-2.5-pro`` - Stabile Version des Schlussfolgerungsmodells

.. note::
   Aktuelle Informationen zu verfügbaren Modellen finden Sie unter `Google AI for Developers <https://ai.google.dev/models/gemini>`__.

Voraussetzungen
===============

Bevor Sie Gemini verwenden, bereiten Sie Folgendes vor.

1. **Google-Konto**: Ein Google-Konto ist erforderlich
2. **Google AI Studio-Zugang**: Besuchen Sie `https://aistudio.google.com/ <https://aistudio.google.com/>`__
3. **API-Schlüssel**: Generieren Sie einen API-Schlüssel in Google AI Studio

API-Schlüssel abrufen
---------------------

1. Besuchen Sie `Google AI Studio <https://aistudio.google.com/>`__
2. Klicken Sie auf "Get API key"
3. Wählen Sie "Create API key"
4. Wählen Sie ein Projekt aus oder erstellen Sie ein neues
5. Speichern Sie den generierten API-Schlüssel sicher

.. warning::
   Der API-Schlüssel ist vertraulich. Beachten Sie folgende Punkte:

   - Nicht in Versionskontrollsysteme committen
   - Nicht in Logs ausgeben
   - Mit Umgebungsvariablen oder sicheren Konfigurationsdateien verwalten

Plugin-Installation
===================

Die Gemini-Integrationsfunktion wird als Plugin ``fess-llm-gemini`` bereitgestellt.
Zur Verwendung von Gemini ist die Installation des Plugins erforderlich.

1. Laden Sie `fess-llm-gemini-15.8.0.jar` herunter
2. Legen Sie die Datei im Verzeichnis ``app/WEB-INF/plugin/`` von |Fess| ab
3. Starten Sie |Fess| neu

::

    # Beispiel für die Plugin-Ablage
    cp fess-llm-gemini-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   Die Plugin-Version muss mit der Version von |Fess| übereinstimmen.

Grundeinstellungen
==================

Die Auswahl des LLM-Anbieters (``rag.llm.name``) erfolgt über die Administrationsoberfläche oder in ``system.properties``; die Aktivierung der AI-Suchmodus-Funktion und Gemini-spezifische Einstellungen werden in ``fess_config.properties`` vorgenommen.

fess_config.properties konfigurieren
-------------------------------------

Fügen Sie die Aktivierungseinstellung für die AI-Suchmodus-Funktion in ``app/WEB-INF/conf/fess_config.properties`` hinzu.

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

LLM-Anbieter konfigurieren
---------------------------

Der LLM-Anbietername (``rag.llm.name``) wird über die Administrationsoberfläche (Administration > System > Allgemein) oder in ``system.properties`` konfiguriert. Gemini-spezifische Einstellungen werden in ``fess_config.properties`` eingetragen.

Minimalkonfiguration
~~~~~~~~~~~~~~~~~~~~

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf Gemini setzen
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # Gemini API-Schlüssel
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Zu verwendendes Modell
    rag.llm.gemini.model=gemini-3.1-flash-lite-preview

Empfohlene Konfiguration (Produktionsumgebung)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf Gemini setzen
    rag.llm.name=gemini

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # Gemini API-Schlüssel
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelleinstellungen (schnelles Modell verwenden)
    rag.llm.gemini.model=gemini-3-flash-preview

    # API-Endpunkt (normalerweise keine Änderung erforderlich)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Timeout-Einstellungen
    rag.llm.gemini.timeout=60000

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den Gemini-Client. Alle Einstellungen außer ``rag.llm.name`` werden in ``fess_config.properties`` vorgenommen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.gemini.api.key``
     - Google AI API-Schlüssel (muss zur Nutzung der Gemini API gesetzt werden)
     - ``""``
   * - ``rag.llm.gemini.model``
     - Name des zu verwendenden Modells
     - ``gemini-3.1-flash-lite-preview``
   * - ``rag.llm.gemini.api.url``
     - Basis-URL der API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Anfrage-Timeout (Millisekunden)
     - ``60000``
   * - ``rag.llm.gemini.availability.check.interval``
     - Intervall der Verfügbarkeitsprüfung (Sekunden)
     - ``60``
   * - ``rag.llm.gemini.max.concurrent.requests``
     - Maximale Anzahl gleichzeitiger Anfragen
     - ``5``
   * - ``rag.llm.gemini.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl relevanter Dokumente bei der Bewertung
     - ``3``
   * - ``rag.llm.gemini.chat.evaluation.description.max.chars``
     - Maximale Zeichenzahl für Dokumentbeschreibung bei der Bewertung
     - ``500``
   * - ``rag.llm.gemini.concurrency.wait.timeout``
     - Wartezeit bei gleichzeitigen Anfragen (Millisekunden)
     - ``30000``
   * - ``rag.llm.gemini.history.max.chars``
     - Maximale Zeichenzahl für Chat-Verlauf
     - ``10000``
   * - ``rag.llm.gemini.intent.history.max.messages``
     - Maximale Anzahl von Verlaufsnachrichten für Absichtserkennung
     - ``10``
   * - ``rag.llm.gemini.intent.history.max.chars``
     - Maximale Verlaufszeichenzahl für Absichtserkennung
     - ``5000``
   * - ``rag.llm.gemini.history.assistant.max.chars``
     - Maximale Zeichenzahl für Assistenten-Verlauf
     - ``1000``
   * - ``rag.llm.gemini.history.assistant.summary.max.chars``
     - Maximale Zeichenzahl für Assistenten-Zusammenfassungsverlauf
     - ``1000``
   * - ``rag.llm.gemini.retry.max``
     - Maximale Anzahl von HTTP-Wiederholungsversuchen (bei ``429`` und ``5xx``-Fehlern)
     - ``10``
   * - ``rag.llm.gemini.retry.base.delay.ms``
     - Basisverzögerung des exponentiellen Backoffs (in Millisekunden)
     - ``2000``

Authentifizierung
=================

Der API-Schlüssel wird über den HTTP-Anfrageheader ``x-goog-api-key`` gesendet (die von Google empfohlene Methode).
Er wird nicht mehr wie zuvor über den Query-Parameter ``?key=...`` an die URL angehängt, sodass der API-Schlüssel nicht in den Zugriffslogs erscheint.

Retry-Verhalten
===============

Anfragen an die Gemini API werden bei folgenden HTTP-Statuscodes automatisch wiederholt:

- ``429`` Resource Exhausted (Kontingentüberschreitung / Ratenbegrenzung)
- ``500`` Internal Server Error
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Bei einem Wiederholungsversuch wird mit exponentiellem Backoff gewartet (Basiswert ``rag.llm.gemini.retry.base.delay.ms`` Millisekunden, maximal ``rag.llm.gemini.retry.max`` Versuche, mit ±20% Jitter).
Bei Streaming-Anfragen wird nur der initiale Verbindungsaufbau wiederholt; Fehler, die nach Beginn des Empfangs des Antwortkörpers auftreten, werden sofort weitergegeben.

Prompttypspezifische Einstellungen
===================================

In |Fess| können LLM-Parameter für jeden Prompttyp detailliert konfiguriert werden.
Prompttypspezifische Einstellungen werden in ``fess_config.properties`` eingetragen.

Konfigurationsformat
--------------------

::

    rag.llm.gemini.{promptType}.temperature
    rag.llm.gemini.{promptType}.max.tokens
    rag.llm.gemini.{promptType}.thinking.budget
    rag.llm.gemini.{promptType}.context.max.chars

Verfügbare Prompttypen
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Prompttyp
     - Beschreibung
   * - ``intent``
     - Prompt zur Bestimmung der Benutzerabsicht
   * - ``evaluation``
     - Prompt zur Bewertung der Dokumentrelevanz
   * - ``unclear``
     - Prompt bei unklarer Frage
   * - ``noresults``
     - Prompt bei fehlenden Suchergebnissen
   * - ``docnotfound``
     - Prompt, wenn kein Dokument gefunden wurde
   * - ``answer``
     - Prompt zur Antwortgenerierung
   * - ``summary``
     - Prompt zur Zusammenfassungsgenerierung
   * - ``faq``
     - Prompt zur FAQ-Generierung
   * - ``direct``
     - Prompt für direkte Antworten
   * - ``queryregeneration``
     - Prompt zur Abfrageneugenerierung

Standardwerte pro Prompttyp
------------------------------

Standardwerte für jeden Prompttyp. Diese Werte werden verwendet, wenn keine explizite Konfiguration vorliegt.

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20

   * - Prompttyp
     - temperature
     - max.tokens
     - thinking.budget
   * - ``intent``
     - ``0.1``
     - ``512``
     - ``0``
   * - ``evaluation``
     - ``0.1``
     - ``256``
     - ``0``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``0``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - ``0``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``0``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``

Konfigurationsbeispiel
----------------------

::

    # Temperatureinstellung für die Antwortgenerierung
    rag.llm.gemini.answer.temperature=0.7

    # Maximale Token-Anzahl für die Zusammenfassungsgenerierung
    rag.llm.gemini.summary.max.tokens=2048

    # Maximale Zeichenzahl des Kontexts für die Antwortgenerierung
    rag.llm.gemini.answer.context.max.chars=16000

    # Maximale Zeichenzahl des Kontexts für die Zusammenfassungsgenerierung
    rag.llm.gemini.summary.context.max.chars=16000

    # Maximale Zeichenzahl des Kontexts für die FAQ-Generierung
    rag.llm.gemini.faq.context.max.chars=10000

.. note::
   Der Standardwert von ``context.max.chars`` variiert je nach Prompttyp.
   Für ``answer`` und ``summary`` beträgt er 16000, für ``faq`` 10000, für andere Prompttypen 10000.

Unterstützung für Thinking-Modelle
====================================

Gemini unterstützt Thinking-Modelle.
Bei Verwendung von Thinking-Modellen führt das Modell vor der Antwortgenerierung einen internen Denkprozess durch und kann so genauere Antworten liefern.

Das Thinking-Budget wird pro Prompttyp in ``fess_config.properties`` konfiguriert. |Fess| konvertiert den Ganzzahlwert (Anzahl Tokens) aus ``rag.llm.gemini.{promptType}.thinking.budget`` zur Anfragezeit automatisch in das passende API-Feld der erkannten Modellgeneration.

::

    # Thinking-Budget für die Antwortgenerierung
    rag.llm.gemini.answer.thinking.budget=1024

    # Thinking-Budget für die Zusammenfassungsgenerierung
    rag.llm.gemini.summary.thinking.budget=1024

Mapping nach Modellgeneration
-----------------------------

- **Gemini 2.x** (z. B. ``gemini-2.5-flash``): Der konfigurierte Ganzzahlwert wird unverändert als ``thinkingConfig.thinkingBudget`` gesendet. Bei ``0`` wird das Thinking vollständig deaktiviert.
- **Gemini 3.x** (z. B. ``gemini-3.1-flash-lite-preview``): Der Ganzzahlwert wird in den Aufzählungswert ``thinkingConfig.thinkingLevel`` (``MINIMAL`` / ``LOW`` / ``MEDIUM`` / ``HIGH``) eingruppiert und gesendet.

Das Bucket-Mapping für Gemini 3.x ist wie folgt:

.. list-table::
   :header-rows: 1
   :widths: 35 25 40

   * - Budget-Wert
     - thinkingLevel
     - Hinweise
   * - ``<=0``
     - ``MINIMAL`` oder ``LOW``
     - Bei Flash- / Flash-Lite-Modellen ``MINIMAL``; bei Pro-Modellen, die ``MINIMAL`` nicht unterstützen (``gemini-3-pro`` / ``gemini-3.1-pro``), ``LOW``.
   * - ``<=4096``
     - ``MEDIUM``
     -
   * - ``>4096``
     - ``HIGH``
     -

.. note::
   Gemini 3.x verbraucht in jedem Bucket eine bestimmte Anzahl an Thinking-Tokens (selbst bei ``thinkingLevel=MINIMAL`` können einige hundert Tokens verbraucht werden).
   Aus diesem Grund fügt |Fess| bei Verwendung von Gemini 3.x-Modellen den standardmäßigen ``maxOutputTokens`` automatisch zusätzlichen Headroom (1024 Tokens) hinzu, um das Abschneiden der Antwort durch ``finishReason=MAX_TOKENS`` zu vermeiden.
   Bei Gemini 2.x wird mit ``thinkingBudget=0`` das Thinking selbst deaktiviert, daher wird kein zusätzlicher Headroom hinzugefügt.

.. note::
   Ein hoch konfiguriertes Thinking-Budget kann die Antwortzeit verlängern.
   Setzen Sie einen geeigneten Wert entsprechend dem Verwendungszweck.

Konfiguration über JVM-Optionen
================================

Aus Sicherheitsgründen wird empfohlen, API-Schlüssel über die Laufzeitumgebung (JVM-Optionen) statt in Dateien zu konfigurieren.

Docker-Umgebung
---------------

Das offizielle |Fess|-Image `docker-fess <https://github.com/codelibs/docker-fess>`__ enthält ein Gemini-Overlay (``compose-gemini.yaml``). Die minimalen Schritte sind:

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Inhalt von ``compose-gemini.yaml`` (als Referenz für eigenes Setup):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-3.1-flash-lite-preview} -Dfess.system.rag.llm.name=gemini"

Hinweise:

- ``FESS_PLUGINS=fess-llm-gemini:15.8.0`` lässt das ``run.sh`` des Containers das Plugin automatisch herunterladen und in ``app/WEB-INF/plugin/`` installieren
- ``-Dfess.config.rag.chat.enabled=true`` aktiviert den AI-Suchmodus
- ``-Dfess.config.rag.llm.gemini.api.key=...`` setzt den API-Schlüssel, ``-Dfess.config.rag.llm.gemini.model=...`` wählt das Modell
- ``-Dfess.system.rag.llm.name=gemini`` wirkt nur als initialer Default, bevor ein Wert in OpenSearch persistiert wurde. Nach dem Start kann der Wert auch unter Administration > System > Allgemein (RAG-Sektion) geändert werden

Bei Internetzugang über einen Proxy geben Sie die ``http.proxy.*``-Einstellungen von |Fess| über ``FESS_JAVA_OPTS`` an (siehe Abschnitt "HTTP-Proxy verwenden" weiter unten).

systemd-Umgebung
----------------

In ``/etc/sysconfig/fess`` (oder ``/etc/default/fess``) ``FESS_JAVA_OPTS`` ergänzen:

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

HTTP-Proxy verwenden
====================

Der Gemini-Client nutzt die globale HTTP-Proxy-Konfiguration von |Fess|. Geben Sie die folgenden Eigenschaften in ``fess_config.properties`` an.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``http.proxy.host``
     - Proxy-Hostname (bei leerer Zeichenkette wird kein Proxy verwendet)
     - ``""``
   * - ``http.proxy.port``
     - Proxy-Portnummer
     - ``8080``
   * - ``http.proxy.username``
     - Benutzername für die Proxy-Authentifizierung (optional; wenn angegeben, wird Basic-Authentifizierung aktiviert)
     - ``""``
   * - ``http.proxy.password``
     - Passwort für die Proxy-Authentifizierung
     - ``""``

In Docker-Umgebungen geben Sie die Werte wie folgt über ``FESS_JAVA_OPTS`` an::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   Diese Einstellung wirkt sich auch auf den HTTP-Zugriff von |Fess| insgesamt (z. B. Crawler) aus.
   Die bisherigen Java-Systemeigenschaften (``-Dhttps.proxyHost`` usw.) werden vom Gemini-Client nicht mehr ausgewertet.

Verwendung über Vertex AI
==========================

Wenn Sie Google Cloud Platform verwenden, können Sie Gemini auch über Vertex AI nutzen.
Bei Verwendung von Vertex AI unterscheiden sich API-Endpunkt und Authentifizierungsmethode.

.. note::
   Die aktuelle |Fess|-Version verwendet die Google AI API (generativelanguage.googleapis.com).
   Falls die Verwendung über Vertex AI erforderlich ist, kann eine benutzerdefinierte Implementierung notwendig sein.

Modellauswahl-Leitfaden
========================

Richtlinien zur Modellauswahl je nach Verwendungszweck.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modell
     - Geschwindigkeit
     - Qualität
     - Anwendungsfall
   * - ``gemini-3.1-flash-lite-preview``
     - Schnell
     - Hoch
     - Leichtgewichtig und kostengünstig (Standard, unterstützt ``thinkingLevel=MINIMAL``)
   * - ``gemini-3-flash-preview``
     - Schnell
     - Sehr hoch
     - Allgemeiner Einsatz (unterstützt ``thinkingLevel=MINIMAL``)
   * - ``gemini-3.1-pro`` / ``gemini-3-pro``
     - Mittel
     - Sehr hoch
     - Komplexe Schlussfolgerungen (``MINIMAL`` nicht unterstützt; mindestens ``LOW``)
   * - ``gemini-2.5-flash``
     - Schnell
     - Hoch
     - Stabile Version, kostenorientiert
   * - ``gemini-2.5-pro``
     - Mittel
     - Hoch
     - Stabile Version, langer Kontext

Kontextfenster
--------------

Gemini-Modelle unterstützen sehr lange Kontextfenster:

- **Gemini 3 Flash / 2.5 Flash**: Bis zu 1 Million Token
- **Gemini 3.1 Pro / 2.5 Pro**: Bis zu 1 Million Token (3.1 Pro) / 2 Millionen Token (2.5 Pro)

Diese Eigenschaft ermöglicht es, mehr Suchergebnisse in den Kontext einzubeziehen.

::

    # Mehr Dokumente in den Kontext einbeziehen (Konfiguration in fess_config.properties)
    rag.llm.gemini.answer.context.max.chars=20000

Kostenrichtlinien
-----------------

Die Google AI API wird nutzungsbasiert abgerechnet (mit Gratiskontingent).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modell
     - Eingabe (1M Zeichen)
     - Ausgabe (1M Zeichen)
   * - Gemini 3 Flash Preview
     - $0.50
     - $3.00
   * - Gemini 3.1 Pro Preview
     - $2.00
     - $12.00
   * - Gemini 2.5 Flash
     - $0.075
     - $0.30
   * - Gemini 2.5 Pro
     - $1.25
     - $5.00

.. note::
   Aktuelle Preise und Informationen zum Gratiskontingent finden Sie unter `Google AI Pricing <https://ai.google.dev/pricing>`__.

Gleichzeitige Anfragensteuerung
=================================

In |Fess| kann die Anzahl gleichzeitiger Anfragen an Gemini gesteuert werden.
Konfigurieren Sie dazu folgendes Property in ``fess_config.properties``.

::

    # Maximale Anzahl gleichzeitiger Anfragen (Standard: 5)
    rag.llm.gemini.max.concurrent.requests=5

Diese Einstellung verhindert übermäßige Anfragen an die Google AI API und vermeidet Ratenbegrenzungsfehler.

Gratiskontingent-Limits
------------------------

Die Google AI API hat ein Gratiskontingent, aber folgende Einschränkungen:

- Anfragen/Minute: 15 RPM
- Token/Minute: 1 Million TPM
- Anfragen/Tag: 1.500 RPD

Bei Verwendung des Gratiskontingents wird empfohlen, ``rag.llm.gemini.max.concurrent.requests`` auf einen niedrigen Wert zu setzen.

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: API-Schlüssel-bezogene Fehler

**Zu überprüfen**:

1. Überprüfen Sie, ob der API-Schlüssel korrekt konfiguriert ist
2. Überprüfen Sie, ob der API-Schlüssel in Google AI Studio gültig ist
3. Überprüfen Sie, ob der API-Schlüssel die erforderlichen Berechtigungen hat
4. Überprüfen Sie, ob die API im Projekt aktiviert ist

Ratenbegrenzungsfehler
----------------------

**Symptom**: "429 Resource has been exhausted"-Fehler

**Lösung**:

1. Verringern Sie die Anzahl gleichzeitiger Anfragen in ``fess_config.properties``::

    rag.llm.gemini.max.concurrent.requests=3

2. Warten Sie einige Minuten und versuchen Sie es erneut
3. Beantragen Sie bei Bedarf eine Kontingenterhöhung

Regionale Einschränkungen
-------------------------

**Symptom**: Fehler, dass der Dienst nicht verfügbar ist

**Zu überprüfen**:

Die Google AI API ist nur in bestimmten Regionen verfügbar. Überprüfen Sie die unterstützten Regionen in der Google-Dokumentation.

Timeout
-------

**Symptom**: Anfragen laufen in Timeout

**Lösung**:

1. Verlängern Sie die Timeout-Zeit::

    rag.llm.gemini.timeout=120000

2. Erwägen Sie die Verwendung des Flash-Modells (schneller)

Debug-Einstellungen
-------------------

Zur Untersuchung von Problemen können Sie den Log-Level anpassen, um detaillierte Logs zu Gemini auszugeben.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.gemini" level="DEBUG"/>

Sicherheitshinweise
===================

Bei der Verwendung der Google AI API beachten Sie folgende Sicherheitsaspekte.

1. **Datenschutz**: Suchergebnisinhalte werden an Google-Server gesendet
2. **API-Schlüsselverwaltung**: Schlüssellecks können zu Missbrauch führen
3. **Compliance**: Bei vertraulichen Daten überprüfen Sie die Richtlinien Ihrer Organisation
4. **Nutzungsbedingungen**: Halten Sie Googles Nutzungsbedingungen und Acceptable Use Policy ein

Weiterführende Informationen
============================

- `Google AI for Developers <https://ai.google.dev/>`__
- `Google AI Studio <https://aistudio.google.com/>`__
- `Gemini API Documentation <https://ai.google.dev/docs>`__
- `Google AI Pricing <https://ai.google.dev/pricing>`__
- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`rag-chat` - Details zur AI-Suchmodus-Funktion
- :doc:`rank-fusion` - Hybride Suche: Kombination aus Keyword- und semantischer (Vektor-)Suche
- :doc:`../user/chat-search` - Verwendung des AI-Suchmodus (Anwenderleitfaden)
