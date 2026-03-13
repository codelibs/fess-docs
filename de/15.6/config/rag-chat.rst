==========================
AI-Suchmodus-Funktion konfigurieren
==========================

Übersicht
=========

AI-Suchmodus (RAG: Retrieval-Augmented Generation) ist eine Funktion, die die |Fess|-Suchergebnisse mit einem LLM (Large Language Model) erweitert und Informationen in dialogorientierter Form bereitstellt. Benutzer können Fragen in natürlicher Sprache stellen und detaillierte Antworten basierend auf den Suchergebnissen erhalten.

In |Fess| 15.6 wurde die LLM-Funktion als ``fess-llm-*``-Plugin ausgelagert.
Kerneinstellungen und LLM-anbieterspezifische Einstellungen werden in ``fess_config.properties`` vorgenommen,
während die LLM-Anbieterauswahl (``rag.llm.name``) in ``system.properties`` oder über die Administrationsoberfläche konfiguriert wird.

AI-Suchmodus-Funktionsweise
========================

AI-Suchmodus arbeitet mit dem folgenden mehrstufigen Ablauf.

1. **Absichtsanalysephase**: Analyse der Benutzerfrage und Extraktion optimaler Suchbegriffe
2. **Suchphase**: Dokumentensuche mit der |Fess|-Suchmaschine anhand der extrahierten Begriffe
3. **Bewertungsphase**: Bewertung der Relevanz der Suchergebnisse und Auswahl der am besten geeigneten Dokumente
4. **Generierungsphase**: LLM generiert eine Antwort basierend auf den ausgewählten Dokumenten
5. **Ausgabephase**: Rückgabe von Antwort und Quellinformationen an den Benutzer

Durch diesen Ablauf sind qualitativ hochwertigere Antworten möglich, die den Kontext besser verstehen als eine einfache Stichwortsuche.

Grundeinstellungen
==================

Die Konfiguration der AI-Suchmodus-Funktion gliedert sich in Kern- und Anbietereinstellungen.

Kerneinstellungen (fess_config.properties)
-------------------------------------------

Grundlegende Einstellungen zur Aktivierung der AI-Suchmodus-Funktion.
Konfiguration in ``app/WEB-INF/conf/fess_config.properties``.

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

Anbieterauswahl (system.properties / Administrationsoberfläche)
----------------------------------------------------------------------

Die Auswahl des LLM-Anbieters erfolgt über die Administrationsoberfläche oder in ``system.properties``.

**Konfiguration über die Administrationsoberfläche**:

Wählen Sie den gewünschten LLM-Anbieter in der Einstellungsmaske unter Administration > System > Allgemein.

**Konfiguration in system.properties**:

::

    # LLM-Anbieter auswählen (ollama, openai, gemini)
    rag.llm.name=ollama

Detaillierte Einstellungen für LLM-Anbieter finden Sie unter:

- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`llm-openai` - OpenAI-Konfiguration
- :doc:`llm-gemini` - Google Gemini-Konfiguration

Kerneinstellungen-Übersicht
============================

Liste der Kerneinstellungen, die in ``fess_config.properties`` konfiguriert werden können.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.enabled``
     - AI-Suchmodus-Funktion aktivieren
     - ``false``
   * - ``rag.chat.context.max.documents``
     - Maximale Anzahl der Dokumente im Kontext
     - ``5``
   * - ``rag.chat.session.timeout.minutes``
     - Sitzungs-Timeout (Minuten)
     - ``30``
   * - ``rag.chat.session.max.size``
     - Maximale Anzahl gleichzeitig gehaltener Sitzungen
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximale Anzahl der Nachrichten im Gesprächsverlauf
     - ``20``
   * - ``rag.chat.intent.history.max.messages``
     - Maximale Anzahl der für die Absichtsanalyse verwendeten Verlaufsnachrichten
     - ``4``
   * - ``rag.chat.content.fields``
     - Aus Dokumenten abzurufende Felder
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Maximale Zeichenzahl von Benutzernachrichten
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Fragmentgröße für die Hervorhebungsanzeige
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Anzahl der Fragmente für die Hervorhebungsanzeige
     - ``3``
   * - ``rag.chat.history.assistant.content``
     - Art des im Assistentenverlauf enthaltenen Inhalts
     - ``source_titles``
   * - ``rag.chat.history.assistant.max.chars``
     - Maximale Zeichenzahl des Assistentenverlaufs
     - ``500``
   * - ``rag.chat.history.assistant.summary.max.chars``
     - Maximale Zeichenzahl der Zusammenfassung des Assistentenverlaufs
     - ``500``
   * - ``rag.chat.history.max.chars``
     - Maximale Zeichenzahl des Gesprächsverlaufs
     - ``2000``

Generierungsparameter
=====================

In |Fess| 15.6 werden Generierungsparameter (maximale Token-Anzahl, Temperature usw.) pro Anbieter
und pro Prompttyp konfiguriert. Diese Einstellungen werden nicht als Kerneinstellungen, sondern als
Einstellungen der jeweiligen ``fess-llm-*``-Plugins verwaltet.

Detaillierte Informationen finden Sie in der Dokumentation des jeweiligen Anbieters:

- :doc:`llm-ollama` - Generierungsparameter-Einstellungen für Ollama
- :doc:`llm-openai` - Generierungsparameter-Einstellungen für OpenAI
- :doc:`llm-gemini` - Generierungsparameter-Einstellungen für Google Gemini

Kontexteinstellungen
=====================

Einstellungen für den Kontext, der aus Suchergebnissen an das LLM übergeben wird.

Kerneinstellungen
-----------------

Folgende Einstellungen werden in ``fess_config.properties`` vorgenommen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.context.max.documents``
     - Maximale Anzahl der Dokumente im Kontext
     - ``5``
   * - ``rag.chat.content.fields``
     - Aus Dokumenten abzurufende Felder
     - ``title,url,content,doc_id,content_title,content_description``

Anbieterspezifische Einstellungen
----------------------------------

Folgende Einstellungen werden pro Anbieter in ``fess_config.properties`` vorgenommen.

- ``rag.llm.{provider}.{promptType}.context.max.chars`` - Maximale Zeichenzahl des Kontexts
- ``rag.llm.{provider}.chat.evaluation.max.relevant.docs`` - Maximale Anzahl relevanter Dokumente in der Bewertungsphase

Für ``{provider}`` wird der Anbietername wie ``ollama``, ``openai`` oder ``gemini`` eingesetzt.
Für ``{promptType}`` wird der Prompttyp wie ``chat``, ``intent_analysis`` oder ``evaluation`` eingesetzt.

Detaillierte Informationen finden Sie in der Dokumentation des jeweiligen Anbieters.

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

In |Fess| 15.6 werden Systemprompts nicht in Property-Dateien, sondern im DI-XML (``fess_llm++.xml``) der jeweiligen ``fess-llm-*``-Plugins definiert.

Prompt anpassen
---------------

Um den Systemprompt anzupassen, überschreiben Sie die ``fess_llm++.xml`` im Plugin-JAR.

1. Rufen Sie ``fess_llm++.xml`` aus der JAR-Datei des verwendeten Plugins ab
2. Nehmen Sie die erforderlichen Änderungen vor
3. Legen Sie die Datei am geeigneten Ort unter ``app/WEB-INF/`` ab, um die Datei zu überschreiben

Für jeden Prompttyp (Absichtsanalyse, Bewertung, Generierung) ist ein eigener Systemprompt definiert, der für den jeweiligen Verwendungszweck optimiert ist.

Detaillierte Informationen finden Sie in der Dokumentation des jeweiligen Anbieters:

- :doc:`llm-ollama` - Ollama-Prompt-Einstellungen
- :doc:`llm-openai` - OpenAI-Prompt-Einstellungen
- :doc:`llm-gemini` - Google Gemini-Prompt-Einstellungen

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

Gleichzeitigkeitssteuerung
===========================

Die Anzahl gleichzeitiger LLM-Anfragen wird pro Anbieter in ``fess_config.properties`` gesteuert.

::

    # Maximale Anzahl gleichzeitiger Anfragen pro Anbieter
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=10
    rag.llm.gemini.max.concurrent.requests=10

Überlegungen zur Gleichzeitigkeitssteuerung
--------------------------------------------

- Berücksichtigen Sie auch die Ratenbegrenzung des LLM-Anbieters
- In Hochlastumgebungen wird ein niedrigerer Wert empfohlen
- Bei Erreichen der maximalen gleichzeitigen Anfragen werden weitere Anfragen in die Warteschlange gestellt und der Reihe nach verarbeitet

API-Verwendung
==============

Die AI-Suchmodus-Funktion ist über REST-API verfügbar.

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

In der |Fess|-Weboberfläche ist die AI-Suchmodus-Funktion über die Suchseite verfügbar.

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

AI-Suchmodus wird nicht aktiviert
------------------------------

**Zu überprüfen**:

1. Ist ``rag.chat.enabled=true`` gesetzt?
2. Ist der LLM-Anbieter über ``rag.llm.name`` korrekt konfiguriert?
3. Ist das entsprechende ``fess-llm-*``-Plugin installiert?
4. Ist eine Verbindung zum LLM-Anbieter möglich?

Antwortqualität ist niedrig
----------------------------

**Verbesserungsmöglichkeiten**:

1. Verwenden Sie ein leistungsfähigeres LLM-Modell
2. Erhöhen Sie ``rag.chat.context.max.documents``
3. Passen Sie den Systemprompt im DI-XML an
4. Passen Sie die anbieterspezifischen Temperature-Einstellungen an (siehe Dokumentation der jeweiligen ``fess-llm-*``-Plugins)

Antworten sind langsam
-----------------------

**Verbesserungsmöglichkeiten**:

1. Verwenden Sie ein schnelleres LLM-Modell (z.B.: Gemini Flash)
2. Verringern Sie die anbieterspezifische max.tokens-Einstellung (siehe Dokumentation der jeweiligen ``fess-llm-*``-Plugins)
3. Verringern Sie ``rag.chat.context.max.documents``

Sitzung wird nicht beibehalten
--------------------------------

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
