==========================
AI-Modus-Funktion konfigurieren
==========================

Übersicht
=========

AI-Modus (RAG: Retrieval-Augmented Generation) ist eine Funktion, die die |Fess|-Suchergebnisse mit einem LLM (Large Language Model) erweitert und Informationen in dialogorientierter Form bereitstellt. Benutzer können Fragen in natürlicher Sprache stellen und detaillierte Antworten basierend auf den Suchergebnissen erhalten.

AI-Modus-Funktionsweise
=======================

AI-Modus arbeitet mit dem folgenden mehrstufigen Ablauf.

1. **Absichtsanalysephase**: Analyse der Benutzerfrage und Extraktion optimaler Suchbegriffe
2. **Suchphase**: Dokumentensuche mit der |Fess|-Suchmaschine anhand der extrahierten Begriffe
3. **Bewertungsphase**: Bewertung der Relevanz der Suchergebnisse und Auswahl der am besten geeigneten Dokumente
4. **Generierungsphase**: LLM generiert eine Antwort basierend auf den ausgewählten Dokumenten
5. **Ausgabephase**: Rückgabe von Antwort und Quellinformationen an den Benutzer

Durch diesen Ablauf sind qualitativ hochwertigere Antworten möglich, die den Kontext besser verstehen als eine einfache Stichwortsuche.

Grundeinstellungen
==================

Grundlegende Einstellungen zur Aktivierung der AI-Modus-Funktion.

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter auswählen (ollama, openai, gemini)
    rag.llm.type=ollama

Detaillierte Einstellungen für LLM-Anbieter finden Sie unter:

- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`llm-openai` - OpenAI-Konfiguration
- :doc:`llm-gemini` - Google Gemini-Konfiguration

Generierungsparameter
=====================

Parameter zur Steuerung des LLM-Generierungsverhaltens.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.max.tokens``
     - Maximale Anzahl der zu generierenden Token
     - ``4096``
   * - ``rag.chat.temperature``
     - Zufälligkeit der Generierung (0.0-1.0)
     - ``0.7``

Temperature-Einstellungen
-------------------------

- **0.0**: Deterministische Antworten (gleiche Eingabe ergibt immer gleiche Antwort)
- **0.3-0.5**: Konsistente Antworten (geeignet für faktenbasierte Fragen)
- **0.7**: Ausgewogene Antworten (Standard)
- **1.0**: Kreative Antworten (geeignet für Brainstorming usw.)

Kontexteinstellungen
====================

Einstellungen für den Kontext, der aus Suchergebnissen an das LLM übergeben wird.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.context.max.documents``
     - Maximale Anzahl der Dokumente im Kontext
     - ``5``
   * - ``rag.chat.context.max.chars``
     - Maximale Zeichenzahl des Kontexts
     - ``4000``
   * - ``rag.chat.content.fields``
     - Aus Dokumenten abzurufende Felder
     - ``title,url,content,...``
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl der in der Bewertungsphase ausgewählten relevanten Dokumente
     - ``3``

Inhaltsfelder
-------------

Mit ``rag.chat.content.fields`` spezifizierbare Felder:

- ``title`` - Dokumenttitel
- ``url`` - Dokument-URL
- ``content`` - Dokumentinhalt
- ``doc_id`` - Dokument-ID
- ``content_title`` - Inhaltstitel
- ``content_description`` - Inhaltsbeschreibung

Systemprompt
============

Der Systemprompt definiert das grundlegende Verhalten des LLM.

Standardeinstellung
-------------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Anpassungsbeispiele
-------------------

Bei Bevorzugung deutscher Antworten:

::

    rag.chat.system.prompt=Sie sind ein KI-Assistent für die Fess-Suchmaschine. Beantworten Sie Fragen basierend auf den bereitgestellten Suchergebnissen. Geben Sie die Antworten auf Deutsch und zitieren Sie die Quellen immer im Format [1], [2] usw.

Anpassung für Fachgebiete:

::

    rag.chat.system.prompt=You are a technical documentation assistant. Provide detailed and accurate answers based on the search results. Include code examples when relevant. Always cite your sources using [1], [2], etc.

Sitzungsverwaltung
==================

Einstellungen zur Verwaltung von Chat-Sitzungen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.session.timeout.minutes``
     - Sitzungs-Timeout (Minuten)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Maximale Anzahl gleichzeitig gehaltener Sitzungen
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximale Anzahl der Nachrichten im Gesprächsverlauf
     - ``20``

Sitzungsverhalten
-----------------

- Wenn ein Benutzer einen neuen Chat startet, wird eine neue Sitzung erstellt
- In der Sitzung wird der Gesprächsverlauf gespeichert, um kontextbezogene Dialoge zu ermöglichen
- Nach Ablauf der Timeout-Zeit wird die Sitzung automatisch gelöscht
- Wenn der Gesprächsverlauf die maximale Nachrichtenanzahl überschreitet, werden ältere Nachrichten gelöscht

Ratenbegrenzung
===============

Ratenbegrenzungseinstellungen zur Vermeidung von API-Überlastung.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.rate.limit.enabled``
     - Ratenbegrenzung aktivieren
     - ``true``
   * - ``rag.chat.rate.limit.requests.per.minute``
     - Maximale Anfragen pro Minute
     - ``10``

Überlegungen zur Ratenbegrenzung
--------------------------------

- Berücksichtigen Sie auch die Ratenbegrenzung des LLM-Anbieters
- In Hochlastumgebungen wird eine strengere Begrenzung empfohlen
- Bei Erreichen der Ratenbegrenzung wird dem Benutzer eine Fehlermeldung angezeigt

API-Verwendung
==============

Die AI-Modus-Funktion ist über REST-API verfügbar.

Nicht-Streaming-API
-------------------

Endpunkt: ``POST /api/v1/chat``

Parameter:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``message``
     - Ja
     - Benutzernachricht
   * - ``sessionId``
     - Nein
     - Sitzungs-ID (bei Fortsetzung des Gesprächs)
   * - ``clear``
     - Nein
     - ``true`` zum Löschen der Sitzung

Anfrage-Beispiel:

::

    curl -X POST "http://localhost:8080/api/v1/chat" \
         -d "message=Wie installiere ich Fess?"

Antwort-Beispiel:

::

    {
      "status": "ok",
      "sessionId": "abc123",
      "content": "Die Installation von Fess erfolgt...",
      "sources": [
        {"title": "Installationsanleitung", "url": "https://..."}
      ]
    }

Streaming-API
-------------

Endpunkt: ``POST /api/v1/chat/stream``

Streamt die Antwort im Server-Sent Events (SSE)-Format.

Parameter:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``message``
     - Ja
     - Benutzernachricht
   * - ``sessionId``
     - Nein
     - Sitzungs-ID (bei Fortsetzung des Gesprächs)

Anfrage-Beispiel:

::

    curl -X POST "http://localhost:8080/api/v1/chat/stream" \
         -d "message=Was sind die Funktionen von Fess?" \
         -H "Accept: text/event-stream"

SSE-Events:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Event
     - Beschreibung
   * - ``session``
     - Sitzungsinformationen (sessionId)
   * - ``phase``
     - Start/Ende der Verarbeitungsphase (intent_analysis, search, evaluation, generation)
   * - ``chunk``
     - Fragment des generierten Textes
   * - ``sources``
     - Informationen zu Quelldokumenten
   * - ``done``
     - Verarbeitung abgeschlossen (sessionId, htmlContent)
   * - ``error``
     - Fehlerinformationen

Detaillierte API-Dokumentation finden Sie unter :doc:`../api/api-chat`.

Weboberfläche
=============

In der |Fess|-Weboberfläche ist die AI-Modus-Funktion über die Suchseite verfügbar.

Chat starten
------------

1. Besuchen Sie die |Fess|-Suchseite
2. Klicken Sie auf das Chat-Symbol
3. Das Chat-Panel wird angezeigt

Chat verwenden
--------------

1. Geben Sie Ihre Frage in das Textfeld ein
2. Klicken Sie auf die Senden-Schaltfläche oder drücken Sie Enter
3. Die Antwort des KI-Assistenten wird angezeigt
4. Die Antwort enthält Links zu den Quellen

Gespräch fortsetzen
-------------------

- Sie können das Gespräch innerhalb derselben Chat-Sitzung fortsetzen
- Antworten berücksichtigen den Kontext früherer Fragen
- Klicken Sie auf "Neuer Chat", um die Sitzung zurückzusetzen

Fehlerbehebung
==============

AI-Modus wird nicht aktiviert
-----------------------------

**Zu überprüfen**:

1. Ist ``rag.chat.enabled=true`` gesetzt?
2. Ist der LLM-Anbieter korrekt konfiguriert?
3. Ist die Verbindung zum LLM-Anbieter möglich?

Antwortqualität ist niedrig
---------------------------

**Verbesserungsmöglichkeiten**:

1. Verwenden Sie ein leistungsfähigeres LLM-Modell
2. Erhöhen Sie ``rag.chat.context.max.documents``
3. Passen Sie den Systemprompt an
4. Passen Sie ``rag.chat.temperature`` an

Antworten sind langsam
----------------------

**Verbesserungsmöglichkeiten**:

1. Verwenden Sie ein schnelleres LLM-Modell (z.B.: Gemini Flash)
2. Verringern Sie ``rag.chat.max.tokens``
3. Verringern Sie ``rag.chat.context.max.chars``

Sitzung wird nicht beibehalten
------------------------------

**Zu überprüfen**:

1. Wird die sessionId clientseitig korrekt gesendet?
2. Überprüfen Sie die ``rag.chat.session.timeout.minutes``-Einstellung
3. Überprüfen Sie die Sitzungsspeicherkapazität

Debug-Einstellungen
-------------------

Zur Untersuchung von Problemen können Sie den Log-Level anpassen, um detaillierte Logs auszugeben.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm" level="DEBUG"/>
    <Logger name="org.codelibs.fess.api.chat" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Weiterführende Informationen
============================

- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`llm-openai` - OpenAI-Konfiguration
- :doc:`llm-gemini` - Google Gemini-Konfiguration
- :doc:`../api/api-chat` - Chat-API-Referenz
- :doc:`../user/chat-search` - Chat-Such-Anleitung für Endbenutzer
