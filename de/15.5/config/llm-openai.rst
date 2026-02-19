==========================
OpenAI-Konfiguration
==========================

Übersicht
=========

OpenAI ist ein Cloud-Dienst, der leistungsstarke große Sprachmodelle (LLM) wie GPT-4 anbietet.
|Fess| kann die OpenAI-API verwenden, um die AI-Modus-Funktion zu realisieren.

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

- ``gpt-4o`` - Neuestes Hochleistungsmodell
- ``gpt-4o-mini`` - Kompaktversion von GPT-4o (kosteneffizienter)
- ``gpt-4-turbo`` - Schnelle Version von GPT-4
- ``gpt-3.5-turbo`` - Modell mit gutem Preis-Leistungs-Verhältnis

.. note::
   Aktuelle Informationen zu verfügbaren Modellen finden Sie unter `OpenAI Models <https://platform.openai.com/docs/models>`__.

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

Grundeinstellungen
==================

Fügen Sie die folgenden Einstellungen zu ``app/WEB-INF/conf/fess_config.properties`` hinzu.

Minimalkonfiguration
--------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter auf OpenAI setzen
    rag.llm.type=openai

    # OpenAI API-Schlüssel
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Zu verwendendes Modell
    rag.llm.openai.model=gpt-4o-mini

Empfohlene Konfiguration (Produktionsumgebung)
----------------------------------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter-Einstellungen
    rag.llm.type=openai

    # OpenAI API-Schlüssel
    rag.llm.openai.api.key=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelleinstellungen (Hochleistungsmodell verwenden)
    rag.llm.openai.model=gpt-4o

    # API-Endpunkt (normalerweise keine Änderung erforderlich)
    rag.llm.openai.api.url=https://api.openai.com/v1

    # Timeout-Einstellungen
    rag.llm.openai.timeout=60000

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den OpenAI-Client.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.openai.api.key``
     - OpenAI API-Schlüssel
     - (erforderlich)
   * - ``rag.llm.openai.model``
     - Name des zu verwendenden Modells
     - ``gpt-5-mini``
   * - ``rag.llm.openai.api.url``
     - Basis-URL der API
     - ``https://api.openai.com/v1``
   * - ``rag.llm.openai.timeout``
     - Anfrage-Timeout (Millisekunden)
     - ``60000``

Konfiguration mit Umgebungsvariablen
====================================

Aus Sicherheitsgründen wird empfohlen, den API-Schlüssel über Umgebungsvariablen zu konfigurieren.

Docker-Umgebung
---------------

::

    docker run -e RAG_LLM_OPENAI_API_KEY=sk-xxx... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=openai
          - RAG_LLM_OPENAI_API_KEY=${OPENAI_API_KEY}
          - RAG_LLM_OPENAI_MODEL=gpt-4o-mini

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
=======================

Richtlinien zur Modellauswahl je nach Verwendungszweck.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modell
     - Kosten
     - Qualität
     - Anwendungsfall
   * - ``gpt-3.5-turbo``
     - Niedrig
     - Gut
     - Allgemeine Frage-Antwort, kostenorientiert
   * - ``gpt-4o-mini``
     - Mittel
     - Hoch
     - Ausgeglichener Einsatz (empfohlen)
   * - ``gpt-4o``
     - Hoch
     - Sehr hoch
     - Komplexe Schlussfolgerungen, wenn hohe Qualität erforderlich
   * - ``gpt-4-turbo``
     - Hoch
     - Sehr hoch
     - Wenn schnelle Antworten erforderlich sind

Kostenrichtlinien
-----------------

Die OpenAI-API wird nutzungsbasiert abgerechnet. Folgende Referenzpreise gelten (Stand 2024).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modell
     - Eingabe (1K Token)
     - Ausgabe (1K Token)
   * - gpt-3.5-turbo
     - $0.0005
     - $0.0015
   * - gpt-4o-mini
     - $0.00015
     - $0.0006
   * - gpt-4o
     - $0.005
     - $0.015

.. note::
   Aktuelle Preise finden Sie unter `OpenAI Pricing <https://openai.com/pricing>`__.

Ratenbegrenzung
===============

Die OpenAI-API hat Ratenbegrenzungen. Kombinieren Sie diese mit der Ratenbegrenzungsfunktion von |Fess|.

::

    # Fess-Ratenbegrenzungseinstellungen
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Tier-basierte OpenAI-Limits
---------------------------

Die Limits variieren je nach OpenAI-Kontostufe:

- **Free**: 3 RPM (Anfragen/Minute)
- **Tier 1**: 500 RPM
- **Tier 2**: 5.000 RPM
- **Tier 3+**: Höhere Limits

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

1. Konfigurieren Sie strengere Ratenbegrenzungen in |Fess|::

    rag.chat.rate.limit.requests.per.minute=5

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

    rag.llm.openai.timeout=120000

2. Erwägen Sie ein schnelleres Modell (gpt-3.5-turbo usw.)

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
- :doc:`rag-chat` - Details zur AI-Modus-Funktion
