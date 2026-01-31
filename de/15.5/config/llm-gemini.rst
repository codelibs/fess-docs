==========================
Google Gemini-Konfiguration
==========================

Übersicht
=========

Google Gemini ist ein hochmodernes großes Sprachmodell (LLM) von Google.
|Fess| kann die Google AI API (Generative Language API) verwenden, um die AI-Modus-Funktion mit Gemini-Modellen zu realisieren.

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

- ``gemini-2.5-flash`` - Schnelles und effizientes Modell (empfohlen)
- ``gemini-2.5-pro`` - Modell mit höherer Schlussfolgerungsfähigkeit
- ``gemini-1.5-flash`` - Stabile Version des Flash-Modells
- ``gemini-1.5-pro`` - Stabile Version des Pro-Modells

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

Grundeinstellungen
==================

Fügen Sie die folgenden Einstellungen zu ``app/WEB-INF/conf/system.properties`` hinzu.

Minimalkonfiguration
--------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter auf Gemini setzen
    rag.llm.type=gemini

    # Gemini API-Schlüssel
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Zu verwendendes Modell
    rag.llm.gemini.model=gemini-2.5-flash

Empfohlene Konfiguration (Produktionsumgebung)
----------------------------------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter-Einstellungen
    rag.llm.type=gemini

    # Gemini API-Schlüssel
    rag.llm.gemini.api.key=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx

    # Modelleinstellungen (schnelles Modell verwenden)
    rag.llm.gemini.model=gemini-2.5-flash

    # API-Endpunkt (normalerweise keine Änderung erforderlich)
    rag.llm.gemini.api.url=https://generativelanguage.googleapis.com/v1beta

    # Timeout-Einstellungen
    rag.llm.gemini.timeout=60000

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den Gemini-Client.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.gemini.api.key``
     - Google AI API-Schlüssel
     - (erforderlich)
   * - ``rag.llm.gemini.model``
     - Name des zu verwendenden Modells
     - ``gemini-2.5-flash``
   * - ``rag.llm.gemini.api.url``
     - Basis-URL der API
     - ``https://generativelanguage.googleapis.com/v1beta``
   * - ``rag.llm.gemini.timeout``
     - Anfrage-Timeout (Millisekunden)
     - ``60000``

Konfiguration mit Umgebungsvariablen
====================================

Aus Sicherheitsgründen wird empfohlen, den API-Schlüssel über Umgebungsvariablen zu konfigurieren.

Docker-Umgebung
---------------

::

    docker run -e RAG_LLM_GEMINI_API_KEY=AIzaSy... codelibs/fess:15.5.0

docker-compose.yml
~~~~~~~~~~~~~~~~~~

::

    services:
      fess:
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=gemini
          - RAG_LLM_GEMINI_API_KEY=${GEMINI_API_KEY}
          - RAG_LLM_GEMINI_MODEL=gemini-2.5-flash

systemd-Umgebung
----------------

``/etc/systemd/system/fess.service.d/override.conf``:

::

    [Service]
    Environment="RAG_LLM_GEMINI_API_KEY=AIzaSy..."

Verwendung über Vertex AI
=========================

Wenn Sie Google Cloud Platform verwenden, können Sie Gemini auch über Vertex AI nutzen.
Bei Verwendung von Vertex AI unterscheiden sich API-Endpunkt und Authentifizierungsmethode.

.. note::
   Die aktuelle |Fess|-Version verwendet die Google AI API (generativelanguage.googleapis.com).
   Falls die Verwendung über Vertex AI erforderlich ist, kann eine benutzerdefinierte Implementierung notwendig sein.

Modellauswahl-Leitfaden
=======================

Richtlinien zur Modellauswahl je nach Verwendungszweck.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modell
     - Geschwindigkeit
     - Qualität
     - Anwendungsfall
   * - ``gemini-2.5-flash``
     - Schnell
     - Hoch
     - Allgemeiner Einsatz, ausgeglichen (empfohlen)
   * - ``gemini-2.5-pro``
     - Mittel
     - Sehr hoch
     - Komplexe Schlussfolgerungen, wenn hohe Qualität erforderlich
   * - ``gemini-1.5-flash``
     - Schnell
     - Gut
     - Kostenorientiert, Stabilitätsorientiert
   * - ``gemini-1.5-pro``
     - Mittel
     - Hoch
     - Wenn langer Kontext erforderlich ist

Kontextfenster
--------------

Gemini-Modelle unterstützen sehr lange Kontextfenster:

- **Gemini 1.5/2.5 Flash**: Bis zu 1 Million Token
- **Gemini 1.5/2.5 Pro**: Bis zu 2 Millionen Token

Diese Eigenschaft ermöglicht es, mehr Suchergebnisse in den Kontext einzubeziehen.

::

    # Mehr Dokumente in den Kontext einbeziehen
    rag.chat.context.max.documents=10
    rag.chat.context.max.chars=20000

Kostenrichtlinien
-----------------

Die Google AI API wird nutzungsbasiert abgerechnet (mit Gratiskontingent).

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Modell
     - Eingabe (1M Zeichen)
     - Ausgabe (1M Zeichen)
   * - Gemini 1.5 Flash
     - $0.075
     - $0.30
   * - Gemini 1.5 Pro
     - $1.25
     - $5.00
   * - Gemini 2.5 Flash
     - Preise können variieren
     - Preise können variieren

.. note::
   Aktuelle Preise und Informationen zum Gratiskontingent finden Sie unter `Google AI Pricing <https://ai.google.dev/pricing>`__.

Ratenbegrenzung
===============

Die Google AI API hat Ratenbegrenzungen. Kombinieren Sie diese mit der Ratenbegrenzungsfunktion von |Fess|.

::

    # Fess-Ratenbegrenzungseinstellungen
    rag.chat.rate.limit.enabled=true
    rag.chat.rate.limit.requests.per.minute=10

Gratiskontingent-Limits
-----------------------

Die Google AI API hat ein Gratiskontingent, aber folgende Einschränkungen:

- Anfragen/Minute: 15 RPM
- Token/Minute: 1 Million TPM
- Anfragen/Tag: 1.500 RPD

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

1. Konfigurieren Sie strengere Ratenbegrenzungen in |Fess|::

    rag.chat.rate.limit.requests.per.minute=5

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
- :doc:`rag-chat` - Details zur AI-Modus-Funktion
