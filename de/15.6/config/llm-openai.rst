==========================
OpenAI-Konfiguration
==========================

Übersicht
=========

OpenAI ist ein Cloud-Dienst, der leistungsstarke große Sprachmodelle (LLM) wie GPT-4 anbietet.
|Fess| kann die OpenAI-API verwenden, um die AI-Suchmodus-Funktion zu realisieren.

Durch die Verwendung von OpenAI wird eine hochwertige Antwortgenerierung durch modernste KI-Modelle ermöglicht.

Hauptmerkmale
-------------

- **Hochwertige Antworten**: Hochpräzise Antwortgenerierung durch modernste GPT-Modelle
- **Skalierbarkeit**: Als Cloud-Dienst leicht skalierbar
- **Kontinuierliche Verbesserung**: Leistungssteigerung durch regelmäßige Modell-Updates
- **Vielfältige Funktionen**: Unterstützt verschiedene Aufgaben wie Textgenerierung, Zusammenfassung, Übersetzung

Unterstützte Modelle
--------------------

Hauptsächlich verfügbare Modelle bei OpenAI:

- ``gpt-5`` - Neuestes Hochleistungsmodell
- ``gpt-5-mini`` - Kompaktversion von GPT-5 (kosteneffizienter)
- ``gpt-4o`` - Hochleistungs-Multimodalmodell
- ``gpt-4o-mini`` - Kompaktversion von GPT-4o
- ``o3-mini`` - Leichtgewichtiges Modell für Schlussfolgerungen
- ``o4-mini`` - Leichtgewichtiges Modell der nächsten Generation für Schlussfolgerungen

.. note::
   Aktuelle Informationen zu verfügbaren Modellen finden Sie unter `OpenAI Models <https://platform.openai.com/docs/models>`__.

.. note::
   Bei Verwendung von Modellen der o1/o3/o4-Serie oder der gpt-5-Serie verwendet |Fess| automatisch den OpenAI-API-Parameter ``max_completion_tokens``. Eine Konfigurationsänderung ist nicht erforderlich.

Voraussetzungen
===============

Bevor Sie OpenAI verwenden, bereiten Sie Folgendes vor.

1. **OpenAI-Konto**: Erstellen Sie ein Konto unter `https://platform.openai.com/ <https://platform.openai.com/>`__
2. **API-Schlüssel**: Generieren Sie einen API-Schlüssel im OpenAI-Dashboard
3. **Abrechnungseinstellungen**: Konfigurieren Sie die Abrechnungsinformationen, da für die API-Nutzung Kosten anfallen

API-Schlüssel abrufen
---------------------

1. Melden Sie sich bei `OpenAI Platform <https://platform.openai.com/>`__ an
2. Navigieren Sie zum Abschnitt "API keys"
3. Klicken Sie auf "Create new secret key"
4. Geben Sie einen Schlüsselnamen ein und erstellen Sie ihn
5. Speichern Sie den angezeigten Schlüssel sicher (er wird nur einmal angezeigt)

.. warning::
   Der API-Schlüssel ist vertraulich. Beachten Sie folgende Punkte:

   - Nicht in Versionskontrollsysteme committen
   - Nicht in Logs ausgeben
   - Mit Umgebungsvariablen oder sicheren Konfigurationsdateien verwalten

Plugin-Installation
===================

In |Fess| 15.6 wird die OpenAI-Integrationsfunktion als Plugin bereitgestellt. Zur Verwendung ist die Installation des ``fess-llm-openai``-Plugins erforderlich.

1. Laden Sie `fess-llm-openai-15.6.0.jar` herunter
2. Legen Sie die JAR-Datei im Verzeichnis ``app/WEB-INF/plugin/`` im |Fess|-Installationsverzeichnis ab::

    cp fess-llm-openai-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Starten Sie |Fess| neu

.. note::
   Die Plugin-Version muss mit der Version von |Fess| übereinstimmen.

Grundeinstellungen
==================

In |Fess| 15.6 sind die Einstellungen je nach Verwendungszweck auf folgende zwei Dateien aufgeteilt.

- ``app/WEB-INF/conf/fess_config.properties`` - Einstellungen für |Fess| selbst und anbieterspezifische LLM-Einstellungen
- ``system.properties`` - LLM-Anbieterauswahl (``rag.llm.name``), die über die Administrationsoberfläche (Administration > System > Allgemein) oder direkt in der Datei konfiguriert wird

Minimalkonfiguration
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # OpenAI API-Schlüssel
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Zu verwendendes Modell
    rag.llm.openai.model=gpt-5-mini

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf OpenAI setzen
    rag.llm.name=openai

Empfohlene Konfiguration (Produktionsumgebung)
----------------------------------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # OpenAI API-Schlüssel
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelleinstellungen (Hochleistungsmodell verwenden)
    rag.llm.openai.model=gpt-4o

    # API-Endpunkt (normalerweise keine Änderung erforderlich)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Timeout-Einstellungen
    rag.llm.openai.timeout=120000

    # Begrenzung gleichzeitiger Anfragen
    rag.llm.openai.max.concurrent.requests=5

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter-Einstellungen
    rag.llm.name=openai

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den OpenAI-Client.

.. list-table::
   :header-rows: 1
   :widths: 35 35 15 15

   * - Eigenschaft
     - Beschreibung
     - Standard
     - Konfigurationsort
   * - ``rag.llm.name``
     - Name des LLM-Anbieters (``openai`` angeben)
     - (erforderlich)
     - system.properties
   * - ``rag.llm.openai.api.key``
     - OpenAI API-Schlüssel
     - (erforderlich)
     - fess_config.properties
   * - ``rag.llm.openai.model``
     - Name des zu verwendenden Modells
     - ``gpt-5-mini``
     - fess_config.properties
   * - ``rag.llm.openai.api.url``
     - Basis-URL der API
     - ``https://api.openai.com/v1``
     - fess_config.properties
   * - ``rag.llm.openai.timeout``
     - Anfrage-Timeout (Millisekunden)
     - ``120000``
     - fess_config.properties
   * - ``rag.llm.openai.availability.check.interval``
     - Intervall der Verfügbarkeitsprüfung (Sekunden)
     - ``60``
     - fess_config.properties
   * - ``rag.llm.openai.max.concurrent.requests``
     - Maximale Anzahl gleichzeitiger Anfragen
     - ``5``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl relevanter Dokumente bei der Bewertung
     - ``3``
     - fess_config.properties
   * - ``rag.chat.enabled``
     - AI-Suchmodus-Funktion aktivieren
     - ``false``
     - fess_config.properties

Prompttypspezifische Einstellungen
===================================

In |Fess| können für jeden Prompttyp individuelle Parameter konfiguriert werden. Die Konfiguration erfolgt in ``fess_config.properties``.

Konfigurationsmuster
--------------------

Prompttypspezifische Einstellungen werden nach folgendem Muster angegeben:

- ``rag.llm.openai.{promptType}.temperature`` - Zufälligkeit der Generierung (0.0-2.0)
- ``rag.llm.openai.{promptType}.max.tokens`` - Maximale Token-Anzahl
- ``rag.llm.openai.{promptType}.context.max.chars`` - Maximale Zeichenzahl des Kontexts

Prompttypen
-----------

Verfügbare Prompttypen:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Prompttyp
     - Beschreibung
   * - ``intent``
     - Prompt zur Bestimmung der Benutzerabsicht
   * - ``evaluation``
     - Prompt zur Bewertung der Relevanz von Suchergebnissen
   * - ``unclear``
     - Antwort-Prompt für unklare Anfragen
   * - ``noresults``
     - Antwort-Prompt bei fehlenden Suchergebnissen
   * - ``docnotfound``
     - Antwort-Prompt, wenn kein Dokument gefunden wurde
   * - ``answer``
     - Prompt zur Antwortgenerierung
   * - ``summary``
     - Prompt zur Zusammenfassungsgenerierung
   * - ``faq``
     - Prompt zur FAQ-Generierung
   * - ``direct``
     - Prompt für direkte Antworten

Konfigurationsbeispiel
----------------------

::

    # Temperatureinstellung für den answer-Prompt
    rag.llm.openai.answer.temperature=0.7

    # Maximale Token-Anzahl für den answer-Prompt
    rag.llm.openai.answer.max.tokens=2048

    # Temperatureinstellung für den summary-Prompt (für Zusammenfassungen niedrig setzen)
    rag.llm.openai.summary.temperature=0.3

    # Temperatureinstellung für den intent-Prompt (für Absichtsbestimmung niedrig setzen)
    rag.llm.openai.intent.temperature=0.1

Unterstützung für Reasoning-Modelle
=====================================

Bei Verwendung von Reasoning-Modellen der o1/o3/o4-Serie oder der gpt-5-Serie verwendet |Fess| automatisch den OpenAI-API-Parameter ``max_completion_tokens`` anstelle von ``max_tokens``. Keine zusätzlichen Konfigurationsänderungen sind erforderlich.

Zusätzliche Parameter für Reasoning-Modelle
--------------------------------------------

Bei Verwendung von Reasoning-Modellen können folgende zusätzliche Parameter in ``fess_config.properties`` konfiguriert werden:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.openai.reasoning.effort``
     - Reasoning-Effort-Einstellung für o-Modelle (``low``, ``medium``, ``high``)
     - (nicht gesetzt)
   * - ``rag.llm.openai.top.p``
     - Wahrscheinlichkeitsschwelle für die Token-Auswahl (0.0-1.0)
     - (nicht gesetzt)
   * - ``rag.llm.openai.frequency.penalty``
     - Häufigkeitsstrafe (-2.0-2.0)
     - (nicht gesetzt)
   * - ``rag.llm.openai.presence.penalty``
     - Anwesenheitsstrafe (-2.0-2.0)
     - (nicht gesetzt)

Konfigurationsbeispiel
----------------------

::

    # Reasoning-Effort für o3-mini auf high setzen
    rag.llm.openai.model=o3-mini
    rag.llm.openai.reasoning.effort=high

    # top_p und Strafen für gpt-5 konfigurieren
    rag.llm.openai.model=gpt-5
    rag.llm.openai.top.p=0.9
    rag.llm.openai.frequency.penalty=0.5

Konfiguration mit Umgebungsvariablen
=====================================

Aus Sicherheitsgründen wird empfohlen, den API-Schlüssel über Umgebungsvariablen zu konfigurieren.

Docker-Umgebung
---------------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.6.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-5-mini

systemd-Umgebung
----------------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_OPENAI_API_KEY=sk-xxx..."

Azure OpenAI verwenden
======================

Bei Verwendung von OpenAI-Modellen über Microsoft Azure ändern Sie den API-Endpunkt.

::

    # Azure OpenAI-Endpunkt
    rag.llm.openai.api.url=https://your-resource.openai.azure.com/openai/deployments/your-deployment

    # Azure API-Schlüssel
    rag.llm.openai.api.key=your-azure-api-key

    # Deployment-Name (als Modellname angeben)
    rag.llm.openai.model=your-deployment-name

.. note::
   Bei Verwendung von Azure OpenAI kann das API-Anforderungsformat leicht abweichen.
   Details finden Sie in der Azure OpenAI-Dokumentation.

Modellauswahl-Leitfaden
========================

Richtlinien zur Modellauswahl je nach Verwendungszweck.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modell
     - Kosten
     - Qualität
     - Anwendungsfall
   * - ``gpt-5-mini``
     - Mittel
     - Hoch
     - Ausgewogener Einsatz (empfohlen)
   * - ``gpt-4o-mini``
     - Niedrig-Mittel
     - Hoch
     - Kostenorientierter Einsatz
   * - ``gpt-5``
     - Hoch
     - Sehr hoch
     - Komplexe Schlussfolgerungen, wenn hohe Qualität erforderlich
   * - ``gpt-4o``
     - Mittel-Hoch
     - Sehr hoch
     - Wenn Multimodal-Unterstützung erforderlich ist
   * - ``o3-mini`` / ``o4-mini``
     - Mittel
     - Sehr hoch
     - Schlussfolgerungsaufgaben wie Mathematik und Programmierung

Kostenrichtlinien
-----------------

Die OpenAI-API wird nutzungsbasiert abgerechnet.

.. note::
   Aktuelle Preise finden Sie unter `OpenAI Pricing <https://openai.com/pricing>`__.

Gleichzeitige Anfragensteuerung
================================

In |Fess| kann die Anzahl gleichzeitiger Anfragen an die OpenAI-API über ``rag.llm.openai.max.concurrent.requests`` in ``fess_config.properties`` gesteuert werden. Der Standardwert ist ``5``.

::

    # Maximale Anzahl gleichzeitiger Anfragen festlegen
    rag.llm.openai.max.concurrent.requests=5

Diese Einstellung verhindert übermäßige Anfragen an die OpenAI-API und vermeidet Ratenbegrenzungsfehler.

Tier-basierte OpenAI-Limits
----------------------------

Die Limits variieren je nach OpenAI-Kontostufe:

- **Free**: 3 RPM (Anfragen/Minute)
- **Tier 1**: 500 RPM
- **Tier 2**: 5.000 RPM
- **Tier 3+**: Höhere Limits

Passen Sie ``rag.llm.openai.max.concurrent.requests`` entsprechend der OpenAI-Kontostufe an.

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: "401 Unauthorized"-Fehler

**Zu überprüfen**:

1. Überprüfen Sie, ob der API-Schlüssel korrekt konfiguriert ist
2. Überprüfen Sie, ob der API-Schlüssel gültig ist (im OpenAI-Dashboard prüfen)
3. Überprüfen Sie, ob der API-Schlüssel die erforderlichen Berechtigungen hat

Ratenbegrenzungsfehler
----------------------

**Symptom**: "429 Too Many Requests"-Fehler

**Lösung**:

1. Verringern Sie den Wert von ``rag.llm.openai.max.concurrent.requests``::

    rag.llm.openai.max.concurrent.requests=3

2. Upgraden Sie die OpenAI-Kontostufe

Kontingentüberschreitung
------------------------

**Symptom**: "You exceeded your current quota"-Fehler

**Lösung**:

1. Überprüfen Sie die Nutzung im OpenAI-Dashboard
2. Überprüfen Sie die Abrechnungseinstellungen und erhöhen Sie bei Bedarf das Limit

Timeout
-------

**Symptom**: Anfragen laufen in Timeout

**Lösung**:

1. Verlängern Sie die Timeout-Zeit::

    rag.llm.openai.timeout=180000

2. Erwägen Sie ein schnelleres Modell (gpt-5-mini usw.)

Debug-Einstellungen
-------------------

Zur Untersuchung von Problemen können Sie den Log-Level anpassen, um detaillierte Logs zu OpenAI auszugeben.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.openai" level="DEBUG"/>

Sicherheitshinweise
===================

Bei der Verwendung der OpenAI-API beachten Sie folgende Sicherheitsaspekte.

1. **Datenschutz**: Suchergebnisinhalte werden an OpenAI-Server gesendet
2. **API-Schlüsselverwaltung**: Schlüssellecks können zu Missbrauch führen
3. **Compliance**: Bei vertraulichen Daten überprüfen Sie die Richtlinien Ihrer Organisation
4. **Nutzungsrichtlinien**: Halten Sie die OpenAI-Nutzungsbedingungen ein

Weiterführende Informationen
============================

- `OpenAI Platform <https://platform.openai.com/>`__
- `OpenAI API Reference <https://platform.openai.com/docs/api-reference>`__
- `OpenAI Pricing <https://openai.com/pricing>`__
- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`rag-chat` - Details zur AI-Suchmodus-Funktion
