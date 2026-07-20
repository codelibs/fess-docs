==========================
AI-Suchmodus-Funktion konfigurieren
==========================

Übersicht
=========

AI-Suchmodus (RAG: Retrieval-Augmented Generation) ist eine Funktion, die die |Fess|-Suchergebnisse mit einem LLM (Large Language Model) erweitert und Informationen in dialogorientierter Form bereitstellt. Benutzer können Fragen in natürlicher Sprache stellen und detaillierte Antworten basierend auf den Suchergebnissen erhalten.

In |Fess| 15.8 wurde die LLM-Funktion als ``fess-llm-*``-Plugin ausgelagert.
Kerneinstellungen und LLM-anbieterspezifische Einstellungen werden in ``fess_config.properties`` vorgenommen,
während die LLM-Anbieterauswahl (``rag.llm.name``) in ``system.properties`` oder über die Administrationsoberfläche konfiguriert wird.

Suchpipeline
============

Der AI-Suchmodus ruft seine Quelldokumente über die standardmäßige |Fess|-Suchpipeline (Rank Fusion) ab, wobei die üblichen rollen- und labelbasierten Zugriffskontrollen von |Fess| gelten. Standardmäßig handelt es sich dabei um eine Schlüsselwortsuche (BM25); das LLM sucht, rankt oder erzeugt selbst keine Dokumenten-Embeddings.

Je nach Anfragetyp wird eine leicht unterschiedliche Pipeline ausgeführt:

- ``POST /api/v2/chat/stream`` (von der Weboberfläche verwendet) durchläuft den vollständigen Ablauf: **Absichtsanalyse → Suche → LLM-Bewertung der Relevanz → Inhaltsabruf → Antwortgenerierung** (gestreamt).
- ``POST /api/v2/chat`` (nicht-streaming) durchläuft einen kürzeren Ablauf: **Absichtsanalyse → Suche → Antwortgenerierung** (ohne Relevanzbewertung oder separaten Inhaltsabruf).

Im Streaming-Ablauf bewertet ein zusätzlicher LLM-Aufruf **die Suchergebnisse** und behält nur die als relevant eingestuften Dokumente, bevor die Antwort generiert wird.

AI-Suchmodus-Funktionsweise
========================

AI-Suchmodus arbeitet mit dem folgenden mehrstufigen Ablauf.

1. **Absichtsanalysephase**: Analyse der Benutzerfrage und Extraktion optimaler Suchbegriffe
2. **Suchphase**: Dokumentensuche mit der |Fess|-Suchmaschine anhand der extrahierten Begriffe
3. **Query-Regenerierungsfallback**: Wenn keine Suchergebnisse gefunden werden, regeneriert das LLM die Abfrage und versucht es erneut
4. **Bewertungsphase**: Bewertung der Relevanz der Suchergebnisse und Auswahl der am besten geeigneten Dokumente
5. **Generierungsphase**: LLM generiert eine Antwort basierend auf den ausgewählten Dokumenten
6. **Ausgabephase**: Rückgabe von Antwort und Quellinformationen an den Benutzer (mit Markdown-Rendering)

Durch diesen Ablauf sind qualitativ hochwertigere Antworten möglich, die den Kontext besser verstehen als eine einfache Stichwortsuche.
Die Query-Regenerierung verbessert die Antwortabdeckung, wenn die ursprüngliche Suchabfrage nicht optimal ist.

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

Konfigurationspfad-Schnellreferenz
==================================

In |Fess| 15.8 sind die Einstellungen in zwei Familien aufgeteilt: die FessConfig-Familie
(``fess_config.properties``) und die SystemProperty-Familie (``system.properties``,
in OpenSearch persistiert). Die Konfigurationspfade unterscheiden sich, daher nicht vermischen.

.. list-table::
   :header-rows: 1
   :widths: 35 18 32 15

   * - Eigenschaft
     - Familie
     - Übergabe via Docker / JVM-Optionen
     - Admin-UI
   * - ``rag.chat.enabled``
     - FessConfig
     - ``-Dfess.config.rag.chat.enabled=true``
     - Nein
   * - ``rag.llm.name``
     - SystemProperty
     - ``-Dfess.system.rag.llm.name=gemini`` (nur als initialer Default)
     - Ja (Allgemein)
   * - ``rag.llm.gemini.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.api.key=...``
     - Nein
   * - ``rag.llm.gemini.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.gemini.model=...``
     - Nein
   * - ``rag.llm.openai.api.key``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.api.key=...``
     - Nein
   * - ``rag.llm.openai.model``
     - FessConfig
     - ``-Dfess.config.rag.llm.openai.model=...``
     - Nein
   * - ``rag.llm.ollama.api.url``
     - FessConfig
     - ``-Dfess.config.rag.llm.ollama.api.url=...``
     - Nein

.. note::

   ``rag.llm.type`` ist der frühere Eigenschaftsname aus |Fess| 15.5 und davor.
   In 15.8 und später wurde er in ``rag.llm.name`` umbenannt; Werte unter
   ``rag.llm.type`` werden nicht mehr gelesen.

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
     - ``30``
   * - ``rag.chat.content.fields``
     - Aus Dokumenten abzurufende Felder
     - ``title,url,content,doc_id,content_title,content_description``
   * - ``rag.chat.message.max.length``
     - Maximale Zeichenzahl von Benutzernachrichten. Dieser Wert wird als System Property gelesen; der Eintrag in ``fess_config.properties`` wird nicht verwendet. Legen Sie ihn über System Properties oder ``-Dfess.system.rag.chat.message.max.length`` fest.
     - ``4000``
   * - ``rag.chat.highlight.fragment.size``
     - Fragmentgröße für Such-Hervorhebungen
     - ``500``
   * - ``rag.chat.highlight.number.of.fragments``
     - Anzahl der Fragmente für Such-Hervorhebungen
     - ``3``
   * - ``rag.chat.content.fulltext.max.length``
     - Schwellenwert, ab dem Dokumente (anhand von ``content_length``) im Antwort-Kontext Hervorhebungsauszüge statt des vollständigen Inhalts verwenden
     - ``3000``
   * - ``rag.chat.answer.highlight.fragment.size``
     - Hervorhebungs-Fragmentgröße beim Extrahieren von Auszügen aus großen Dokumenten für den Antwort-Kontext
     - ``1000``
   * - ``rag.chat.answer.highlight.number.of.fragments``
     - Anzahl der Hervorhebungs-Fragmente beim Extrahieren von Auszügen aus großen Dokumenten für den Antwort-Kontext
     - ``5``
   * - ``rag.chat.history.assistant.content``
     - Art des im Assistentenverlauf enthaltenen Inhalts ( ``full`` / ``smart_summary`` / ``source_titles`` / ``source_titles_and_urls`` / ``truncated`` / ``none`` )
     - ``smart_summary``
   * - ``rag.chat.history.titles.max.count``
     - Maximale Anzahl referenzierter Dokumenttitel, die im ``smart_summary``-Modus pro Turn gespeichert werden
     - ``5``

Generierungsparameter
=====================

In |Fess| 15.8 werden Generierungsparameter (maximale Token-Anzahl, Temperature usw.) pro Anbieter
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
Für ``{promptType}`` wird der Prompttyp wie ``intent``, ``evaluation``, ``answer``, ``summary``, ``faq``, ``queryregeneration``,
``unclear``, ``noresults``, ``docnotfound``, ``direct`` eingesetzt.
Die unterstützten Prompttypen sind in der jeweiligen ``*LlmClient``-Implementierung jedes Plugins definiert.

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

In |Fess| 15.8 werden Systemprompts nicht in Property-Dateien, sondern im DI-XML (``fess_llm++.xml``) der jeweiligen ``fess-llm-*``-Plugins definiert.

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
     - ``30``

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

    # Maximale Anzahl gleichzeitiger Anfragen pro Anbieter (Standard: 5)
    rag.llm.ollama.max.concurrent.requests=5
    rag.llm.openai.max.concurrent.requests=5
    rag.llm.gemini.max.concurrent.requests=5

    # Timeout für das Warten auf einen Gleichzeitigkeits-Permit (Millisekunden, Standard: 30000)
    rag.llm.ollama.concurrency.wait.timeout=30000

Überlegungen zur Gleichzeitigkeitssteuerung
--------------------------------------------

- Berücksichtigen Sie auch die Ratenbegrenzung des LLM-Anbieters
- In Hochlastumgebungen wird ein niedrigerer Wert empfohlen
- Bei Erreichen der maximalen gleichzeitigen Anfragen werden weitere Anfragen in die Warteschlange gestellt und der Reihe nach verarbeitet
- Wenn das Warten auf einen Permit die ``concurrency.wait.timeout``-Grenze überschreitet, schlägt die Anfrage mit einem Timeout-Fehler fehl

Gesprächsverlaufsmodus
======================

``rag.chat.history.assistant.content`` steuert, wie Assistentenantworten im Gesprächsverlauf gespeichert werden.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Modus
     - Beschreibung
   * - ``smart_summary``
     - (Standard) Der Antwortkörper wird aus dem Verlauf weggelassen; pro Turn werden nur die vergangene Suchabfrage und die referenzierten Dokumenttitel (maximal ``rag.chat.history.titles.max.count`` Einträge) gespeichert
   * - ``full``
     - Behält die gesamte Antwort unverändert bei
   * - ``source_titles``
     - Behält nur die Quelltitel bei
   * - ``source_titles_and_urls``
     - Behält Quelltitel und URLs bei
   * - ``truncated``
     - Kürzt die Antwort auf die maximale Zeichenzahl
   * - ``none``
     - Speichert keinen Verlauf

.. note::

   Im ``smart_summary``-Modus wird der Antwortkörper durch die Suchabfrage und die referenzierten Titel ersetzt, um den Kontext effizient zu bewahren und den Tokenverbrauch zu reduzieren.
   Benutzer- und Assistentennachrichtenpaare werden als Turns gruppiert und innerhalb eines Zeichenbudgets optimal gepackt.
   Die maximale Zeichenzahl für Verlauf und Zusammenfassung wird durch die ``LlmClient``-Implementierung jedes ``fess-llm-*``-Plugins gesteuert.

Query-Regenerierung
===================

Wenn keine Suchergebnisse gefunden werden oder keine relevanten Ergebnisse identifiziert werden, regeneriert das LLM automatisch die Abfrage und wiederholt die Suche.

- Bei null Suchergebnissen: Query-Regenerierung mit Grund ``no_results``
- Wenn keine relevanten Dokumente gefunden werden: Query-Regenerierung mit Grund ``no_relevant_results``
- Fällt auf die ursprüngliche Abfrage zurück, wenn die Regenerierung fehlschlägt

Diese Funktion ist standardmäßig aktiviert und in synchrone und Streaming-RAG-Flows integriert.
Query-Regenerierungsprompts werden in jedem ``fess-llm-*``-Plugin definiert.

Markdown-Rendering
==================

Antworten des AI-Suchmodus werden im Markdown-Format gerendert.

- LLM-Antworten werden als Markdown geparst und in HTML konvertiert
- Das konvertierte HTML wird bereinigt, wobei nur sichere Tags und Attribute zugelassen werden
- Unterstützt Überschriften, Listen, Codeblöcke, Tabellen, Links und andere Markdown-Syntax
- Clientseitig werden ``marked.js`` und ``DOMPurify`` verwendet; serverseitig der OWASP-Sanitizer

API-Verwendung
==============

Die AI-Suchmodus-Funktion ist über die REST-API (v2-API) verfügbar.
Die Basis-URL lautet ``http://<Servername>/api/v2/``.

Die Chat-API stellt die folgenden drei Endpunkte bereit.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Endpunkt
     - Beschreibung
   * - ``POST /api/v2/chat``
     - Batch- (nicht-streaming) RAG-Chat-Completion
   * - ``POST /api/v2/chat/stream``
     - Streaming-RAG-Chat-Completion (Server-Sent Events)
   * - ``DELETE /api/v2/chat/sessions/{session_id}``
     - Konversationsverlauf einer Chat-Sitzung löschen

Anfragen werden als JSON-Body mit ``Content-Type: application/json`` gesendet.
Zustandsändernde Anfragen (``POST`` / ``DELETE``) erfordern den CSRF-Token (``X-Fess-CSRF-Token``-Header).
Antworten sind im gemeinsamen ``response``-Envelope enthalten.

.. note::

   Die ``/api/v1/chat``-Endpunkte mit Formularparametern, die bis |Fess| 15.5 bereitgestellt wurden, wurden entfernt.
   Verwenden Sie in 15.8 die JSON-basierte API unter ``/api/v2/``.

Nicht-Streaming-API
-------------------

Endpunkt: ``POST /api/v2/chat``

Anfrage-Body (JSON):

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``message``
     - Ja
     - Benutzernachricht
   * - ``session_id``
     - Nein
     - Sitzungs-ID (zur Fortsetzung eines Gesprächs). Wird weggelassen, erstellt der Server eine Sitzung und gibt sie in der Antwort zurück
   * - ``fields``
     - Nein
     - Optionale Filterfelder für den Abrufschritt (object)
   * - ``fields.label``
     - Nein
     - Suchfilter nach Label
   * - ``extra_queries``
     - Nein
     - Zusätzliche Abfrageausdrücke für Facettenfilter

Anfrage-Beispiel:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -d '{"message":"Wie installiere ich Fess?"}'

Antwort-Beispiel:

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session_id": "abc123",
        "content": "Die Installation von Fess erfolgt...",
        "sources": [
          {
            "rank": 1,
            "title": "Installationsanleitung",
            "url": "https://...",
            "doc_id": "...",
            "snippet": "..."
          }
        ]
      }
    }

Streaming-API
-------------

Endpunkt: ``POST /api/v2/chat/stream``

Der Anfrage-Body entspricht dem von ``POST /api/v2/chat`` (JSON).
Die Antwort wird im Server-Sent Events (SSE)-Format gestreamt.

Anfrage-Beispiel:

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/v2/chat/stream" \
         -H "Content-Type: application/json" \
         -H "X-Fess-CSRF-Token: <token>" \
         -H "Accept: text/event-stream" \
         --no-buffer \
         -d '{"message":"Was sind die Funktionen von Fess?"}'

SSE-Ereignisse:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Ereignis
     - Beschreibung (Payload)
   * - ``phase``
     - Phasenübergang der Verarbeitungs-Pipeline (``intent``, ``search``, ``evaluate``, ``fetch``, ``answer``). ``{ phase, status, message?, keywords?, hit_count?, ... }``
   * - ``chunk``
     - Fragment des generierten Textes (``{ content }``)
   * - ``retry``
     - Wird gesendet, wenn eine LLM-Anfrage wiederholt wird (``{ phase, operation, attempt, max_attempts, sleep_ms, cause? }``)
   * - ``waiting``
     - Fortschritt bei lang andauernden Phasen wie dem Warten auf einen Gleichzeitigkeits-Permit (``{ phase, reason, elapsed_ms, timeout_ms }``)
   * - ``fallback``
     - Wird gesendet, wenn die Abfrage neu generiert wurde, z. B. bei fehlenden oder nicht relevanten Ergebnissen (``{ phase, reason, original_query?, new_query? }``, Grund: ``no_results`` oder ``no_relevant_results``)
   * - ``warning``
     - Behebbarer Warnhinweis (``{ phase, code, detail? }``, z. B. Token-Erschöpfung bei Reasoning-Modellen)
   * - ``sources``
     - Informationen zu Quelldokumenten (``{ sources: [...] }``)
   * - ``done``
     - Verarbeitung abgeschlossen (``{ session_id, html_content? }``). ``html_content`` enthält den als Markdown gerenderten HTML-String
   * - ``error``
     - Terminaler Stream-Fehler mitten im Stream (``{ phase?, message, error_code }``). Liefert spezifische Meldungen für Timeout, Kontextlängenüberschreitung, Modell nicht gefunden, ungültige Antwort und Verbindungsfehler

Sitzung löschen
---------------

Endpunkt: ``DELETE /api/v2/chat/sessions/{session_id}``

Löscht den Konversationsverlauf der angegebenen Chat-Sitzung.
Bei Erfolg wird ``cleared: true`` zurückgegeben.

Detaillierte API-Dokumentation (Authentifizierung, CSRF, Rate-Limits, HTTP-Statuscodes) finden Sie unter :doc:`../api/api-chat`.

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

AI-Modus-Schaltfläche erscheint nicht im Suchbildschirm
-------------------------------------------------------

**Symptom**: Die AI-Modus-Schaltfläche wird nicht im Header der Suchergebnisse angezeigt
und der Aufruf von ``/chat`` leitet zur Startseite zurück.

**Checkliste**: Überprüfen Sie die folgenden Punkte der Reihe nach.

1. Ist ``rag.chat.enabled=true`` gesetzt?

   - Docker: ``-Dfess.config.rag.chat.enabled=true`` in ``FESS_JAVA_OPTS`` enthalten?
   - Paketinstallation: in ``app/WEB-INF/conf/fess_config.properties`` gesetzt?

2. Ist das passende ``fess-llm-*``-Plugin installiert?

   - Docker: ``FESS_PLUGINS=fess-llm-gemini:15.8.0`` (oder ``fess-llm-openai`` / ``fess-llm-ollama``) gesetzt?
   - Paketinstallation: JAR liegt in ``app/WEB-INF/plugin/``?
   - Startup-Log enthält ``Installing fess-llm-XXX-15.8.0.jar``?

3. Stimmt ``rag.llm.name`` mit dem installierten Plugin überein?

   - Standardwert ist ``ollama``. Ist nur das Gemini-Plugin installiert, muss explizit ``gemini`` (bzw. ``openai``) gesetzt werden
   - Methode (a): ``rag.llm.name`` unter Administration > System > Allgemein (RAG-Sektion) bearbeiten und speichern
   - Methode (b): ``-Dfess.system.rag.llm.name=gemini`` in ``FESS_JAVA_OPTS`` beim Start. Wirkt nur als initialer Default, bevor ein Wert in OpenSearch persistiert wurde

4. Erscheint im Startup-Log wiederholt ein WARN wie ``[LLM] LlmClient not found. componentName=ollamaLlmClient``?

   - Typisches Symptom, wenn ``rag.llm.name`` weiterhin ``ollama`` ist, das Ollama-Plugin aber nicht installiert ist
   - Das Setzen von ``rag.llm.name`` auf den tatsächlich verwendeten Anbieter behebt es
   - Analog zeigt ``componentName=geminiLlmClient`` an, dass ``rag.llm.name=gemini`` gesetzt, ``fess-llm-gemini`` aber nicht installiert ist

5. Ist der anbieterspezifische API-Key konfiguriert?

   - Wenn ``rag.llm.gemini.api.key`` / ``rag.llm.openai.api.key`` leer ist, liefert ``checkAvailabilityNow`` ``false`` und der AI-Modus ist deaktiviert
   - Mit DEBUG auf ``org.codelibs.fess.llm.gemini`` in ``log4j2.xml`` erscheinen Meldungen wie ``[LLM:GEMINI] Gemini is not available. apiKey is blank``

6. Kann der Fess-Host den LLM-Anbieter erreichen?

   - Bei Cloud-APIs (Gemini / OpenAI) muss der Container Internetzugriff haben
   - Bei Proxy-Nutzung konfigurieren Sie ``http.proxy.host`` / ``http.proxy.port`` (bei Bedarf ``http.proxy.username`` / ``http.proxy.password``) in ``fess_config.properties``. In Docker-Umgebungen fügen Sie ``-Dfess.config.http.proxy.host=... -Dfess.config.http.proxy.port=...`` zu ``FESS_JAVA_OPTS`` hinzu (seit |Fess| 15.8 verwenden die LLM-Clients die gemeinsame Proxy-Konfiguration von |Fess|)

.. note::

   Die Seite "Allgemein" enthält keine Checkbox für ``rag.chat.enabled`` (per Design).
   Diese FessConfig-Eigenschaft kann nur über ``fess_config.properties`` oder
   ``-Dfess.config.rag.chat.enabled=true`` gesetzt werden.

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
    <Logger name="org.codelibs.fess.api.v2.handlers" level="DEBUG"/>
    <Logger name="org.codelibs.fess.chat" level="DEBUG"/>

Die Log-Meldungen verwenden das Präfix ``[RAG]``, mit Unterpräfixen wie ``[RAG:INTENT]``, ``[RAG:EVAL]`` und ``[RAG:ANSWER]`` für jede Phase.
Auf INFO-Ebene werden Chat-Abschluss-Logs (Dauer, Quellenanzahl) ausgegeben. Auf DEBUG-Ebene werden Tokenverbrauch, Gleichzeitigkeitssteuerung und Verlaufspaketierungsdetails ausgegeben.

Suchprotokoll und Zugriffstyp
------------------------------

Suchen über den AI-Suchmodus werden mit dem LLM-Anbieternamen (z.B. ``ollama``, ``openai``, ``gemini``) als Zugriffstyp im Suchprotokoll aufgezeichnet. Dies ermöglicht die Unterscheidung von AI-Suchmodus-Suchen und regulären Web- oder API-Suchen in der Analyse.

Weiterführende Informationen
============================

- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`llm-openai` - OpenAI-Konfiguration
- :doc:`llm-gemini` - Google Gemini-Konfiguration
- :doc:`../api/api-chat` - Chat-API-Referenz
- :doc:`../user/chat-search` - Chat-Such-Anleitung für Endbenutzer
