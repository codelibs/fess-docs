==========================
Google Gemini-Konfiguration
==========================

Übersicht
=========

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

- ``gemini-3-flash-preview`` - Neuestes schnelles Modell (empfohlen)
- ``gemini-3.1-pro-preview`` - Neuestes Modell mit hoher Schlussfolgerungsfähigkeit
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

In |Fess| 15.6 wird die Gemini-Integrationsfunktion als Plugin ``fess-llm-gemini`` bereitgestellt.
Zur Verwendung von Gemini ist die Installation des Plugins erforderlich.

1. Laden Sie `fess-llm-gemini-15.6.0.jar` herunter
2. Legen Sie die Datei im Verzeichnis ``app/WEB-INF/plugin/`` von |Fess| ab
3. Starten Sie |Fess| neu

::

    # Beispiel für die Plugin-Ablage
    cp fess-llm-gemini-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   Die Plugin-Version muss mit der Version von |Fess| übereinstimmen.

Grundeinstellungen
==================

In |Fess| 15.6 wird die Aktivierung der AI-Suchmodus-Funktion und Gemini-spezifische Einstellungen in ``fess_config.properties`` vorgenommen, während die Auswahl des LLM-Anbieters (``rag.llm.name``) über die Administrationsoberfläche oder in ``system.properties`` konfiguriert wird.

LLM-Anbieter konfigurieren
---------------------------

Der LLM-Anbieter wird über die Administrationsoberfläche (Administration > System > Allgemein) oder in ``system.properties`` konfiguriert.

Minimalkonfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # Gemini API-Schlüssel
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Zu verwendendes Modell
    rag.llm.gemini.model=gemini-3-flash-preview

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf Gemini setzen
    rag.llm.name=gemini

Empfohlene Konfiguration (Produktionsumgebung)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf Gemini setzen
    rag.llm.name=gemini

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den Gemini-Client. Alle Einstellungen werden in ``fess_config.properties`` vorgenommen.

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
     - ``gemini-3-flash-preview``
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
     - ``256``
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
     - ``256``
     - ``0``
   * - ``direct``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``faq``
     - ``0.7``
     - ``2048``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``4096``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``4096``
     - ``2048``
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

Das Thinking-Budget kann pro Prompttyp in ``fess_config.properties`` konfiguriert werden.

::

    # Thinking-Budget für die Antwortgenerierung
    rag.llm.gemini.answer.thinking.budget=1024

    # Thinking-Budget für die Zusammenfassungsgenerierung
    rag.llm.gemini.summary.thinking.budget=1024

.. note::
   Die Konfiguration des Thinking-Budgets kann die Antwortzeit verlängern.
   Setzen Sie einen geeigneten Wert entsprechend dem Verwendungszweck.

Konfiguration über JVM-Optionen
===============================

Aus Sicherheitsgründen wird empfohlen, API-Schlüssel über die Laufzeitumgebung
(JVM-Optionen) statt in eingecheckten Dateien zu konfigurieren.

|Fess| ordnet einfache Shell-Variablen wie ``RAG_CHAT_ENABLED`` **nicht** automatisch zu.
Alle RAG-/LLM-Einstellungen müssen innerhalb von ``FESS_JAVA_OPTS`` als
``-Dfess.config.*`` (FessConfig-Familie) oder ``-Dfess.system.*`` (SystemProperty-Familie)
JVM-Optionen übergeben werden.

Docker-Umgebung
---------------

Das offizielle `docker-fess <https://github.com/codelibs/docker-fess>`__ Repository
liefert ein Gemini-Overlay (``compose-gemini.yaml``) mit. Die minimalen Schritte sind:

::

    export GEMINI_API_KEY="AIzaSy..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-gemini.yaml up -d

Inhalt von ``compose-gemini.yaml`` (als Referenz für eigenes Setup):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-gemini:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=${GEMINI_API_KEY:-} -Dfess.config.rag.llm.gemini.model=${GEMINI_MODEL:-gemini-2.5-flash} -Dfess.system.rag.llm.name=gemini"

Hinweise:

- ``FESS_PLUGINS=fess-llm-gemini:15.6.0`` lässt das ``run.sh`` des Containers das Plugin automatisch herunterladen und in ``app/WEB-INF/plugin/`` installieren
- ``-Dfess.config.rag.chat.enabled=true`` aktiviert den AI-Modus
- ``-Dfess.config.rag.llm.gemini.api.key=...`` setzt den API-Schlüssel, ``-Dfess.config.rag.llm.gemini.model=...`` wählt das Modell
- ``-Dfess.system.rag.llm.name=gemini`` wirkt nur als initialer Default, bevor ein Wert in OpenSearch persistiert wurde. Nach dem Start kann der Wert auch unter Administration > System > Allgemein (RAG-Sektion) geändert werden

Bei Internetzugang über Proxy ``-Dhttps.proxyHost=... -Dhttps.proxyPort=...`` an
``FESS_JAVA_OPTS`` anhängen.

systemd-Umgebung
----------------

In ``/etc/sysconfig/fess`` (oder ``/etc/default/fess``) ``FESS_JAVA_OPTS`` ergänzen:

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.gemini.api.key=AIzaSy... -Dfess.system.rag.llm.name=gemini"

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
   * - ``gemini-3-flash-preview``
     - Schnell
     - Sehr hoch
     - Allgemeiner Einsatz (empfohlen)
   * - ``gemini-3.1-pro-preview``
     - Mittel
     - Sehr hoch
     - Komplexe Schlussfolgerungen
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
