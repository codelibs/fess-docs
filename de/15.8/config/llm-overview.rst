=======================================================
Übersicht über KI-Suchmodus (RAG) und LLM-Integration
=======================================================

Übersicht
=========

|Fess| unterstützt eine KI-Suchmodus-Funktion (RAG: Retrieval-Augmented Generation), die große Sprachmodelle (LLM) nutzt.
Mit dieser Funktion können Benutzer Informationen in einem dialogorientierten Format mit einem KI-Assistenten abrufen, der auf Suchergebnissen basiert, und erhalten so Antworten auf natürlichsprachliche Fragen direkt aus Ihrem Unternehmens-Suchindex mit zitierten Quellen.

Die LLM-Integrationsfunktion wird als ``fess-llm-*``-Plugin bereitgestellt. Installieren Sie das Plugin, das dem LLM-Anbieter entspricht, den Sie verwenden möchten.

Der KI-Suchmodus ruft Dokumente über die standardmäßige |Fess|-Suchpipeline (Rank Fusion) ab, nicht über einen separaten Vektorindex — standardmäßig handelt es sich dabei um eine Schlüsselwortsuche (BM25). Da diese Pipeline wiederverwendet wird, nimmt der semantische Sucher der im Kern integrierten semantischen Suche (Content-Chunking + Vektorsuche), sofern aktiviert, an der Rank Fusion für alle Suchen teil, einschließlich des Abrufschritts des KI-Suchmodus; damit der semantische Sucher teilnimmt, ist keine KI-Suchmodus-spezifische Konfiguration erforderlich. Die Anzahl der Chunks, die an die Antwortgenerierung übergeben werden, lässt sich jedoch über ``content_chunker.chat.top_k`` anpassen. Siehe :doc:`rank-fusion` und :doc:`search-semantic`.

Unterstützte Anbieter
=====================

|Fess| unterstützt die folgenden LLM-Anbieter.

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - Anbieter
     - Einstellungswert
     - Plugin
     - Beschreibung
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - Open-Source-LLM-Server, der in lokalen Umgebungen läuft. Kann Modelle wie Llama, Mistral und Gemma ausführen. Standardeinstellung.
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - Cloud-API von OpenAI. Ermöglicht die Nutzung von Modellen wie GPT-5.
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Cloud-API von Google. Ermöglicht die Nutzung von Gemini-Modellen.

Anbietervergleich
------------------

.. list-table::
   :header-rows: 1

   * - Anbieter (``rag.llm.name``)
     - Standardmodell
     - Endpunkt
     - Authentifizierung
     - Datenstandort
   * - Ollama (``ollama``)
     - ``gemma4:e4b``
     - ``http://localhost:11434``
     - Keine (lokal)
     - Lokal / selbst gehostet — Fragen und Dokumente verbleiben auf Ihrem Host
   * - OpenAI (``openai``)
     - ``gpt-5-mini``
     - ``https://api.openai.com/v1``
     - ``Authorization: Bearer`` (``rag.llm.openai.api.key``)
     - Cloud — die Frage und die abgerufenen Dokumente werden an OpenAI gesendet
   * - Google Gemini (``gemini``)
     - ``gemini-3.1-flash-lite-preview``
     - ``https://generativelanguage.googleapis.com/v1beta``
     - ``x-goog-api-key`` (``rag.llm.gemini.api.key``)
     - Cloud — die Frage und die abgerufenen Dokumente werden an Google gesendet

.. note::

   Der Standardwert von ``rag.llm.name`` ist ``ollama``. Dieser Wert bestimmt den Namen der zu ladenden DI-Komponente (``{rag.llm.name}LlmClient``).
   Wenn Sie daher ``rag.llm.name`` auf dem Standardwert belassen und nur ein anderes Plugin als ``fess-llm-ollama`` installieren, wird kein einziger LLM-Client aktiv.
   In diesem Fall erscheint im Log die Warnung ``[LLM] LlmClient not found. componentName=ollamaLlmClient``, und der KI-Suchmodus steht nicht zur Verfügung.
   Setzen Sie ``rag.llm.name`` unbedingt entsprechend dem installierten Plugin. Mit ``none`` lässt sich die LLM-Integration explizit deaktivieren.

Plugin-Installation
===================

Die LLM-Funktion wird als Plugin bereitgestellt. Installieren Sie das ``fess-llm-{provider}``-Plugin, das dem gewünschten Anbieter entspricht.

Die Installation ist über die Seite **System > Plugin** in der Administrationsoberfläche möglich. ``fess-llm-*``-Plugins werden in der Liste der installierbaren Plugins angezeigt.

Für die manuelle Installation legen Sie die entsprechende JAR-Datei (Beispiel: ``fess-llm-openai-15.8.0.jar`` für den OpenAI-Anbieter) im folgenden Verzeichnis ab.

::

    app/WEB-INF/plugin/

In beiden Fällen wird das Plugin nach der Installation beim nächsten Neustart von |Fess| geladen.

Architektur
===========

Die KI-Suchmodus-Funktion arbeitet mit dem folgenden Ablauf.

1. **Benutzereingabe**: Der Benutzer gibt eine Frage in der Chat-Oberfläche ein
2. **Absichtsanalyse (intent)**: Das LLM analysiert die Benutzerfrage und extrahiert Suchbegriffe
3. **Suchausführung (search)**: Die |Fess|-Suchmaschine sucht nach relevanten Dokumenten
4. **Ergebnisbewertung (evaluate)**: Das LLM bewertet die Relevanz der Suchergebnisse und wählt die optimalen Dokumente aus
5. **Query-Regenerierung (bei Bedarf)**: Werden keine Suchergebnisse gefunden oder keine relevanten Dokumente in der Bewertung ermittelt, regeneriert das LLM die Abfrage und führt eine erneute Suche durch
6. **Inhaltsabruf (fetch)**: Der Volltext der ausgewählten Dokumente wird abgerufen
7. **Antwortgenerierung (answer)**: Das LLM generiert eine Antwort auf Basis der abgerufenen Dokumente (mit Markdown-Rendering)
8. **Quellenangabe**: Die Antwort enthält Links zu den referenzierten Quelldokumenten

.. note::

   Die interne Verarbeitung besteht aus fünf Phasen: ``intent``, ``search``, ``evaluate``, ``fetch`` und ``answer``. Der Fortschritt jeder Phase wird dem Client per Streaming (SSE) mitgeteilt.
   Die Query-Regenerierung ist keine eigenständige Phase, sondern wird als Fallback der ``search``-Phase gemeldet; anschließend wird ``search`` erneut ausgeführt.

.. note::

   Der oben beschriebene Ablauf gilt für den Fall, dass die Streaming-API die Absicht als „Suche“ einstuft. Je nach Ergebnis der Absichtserkennung kann der Ablauf abweichen.
   Wird die Frage als unklar eingestuft, wird eine Antwort ohne Suche generiert; wird eine URL-Zusammenfassung angefordert, erfolgt eine URL-Suche ohne Bewertungsphase.
   Zudem führt das nicht-streamende ``POST /api/v2/chat`` keine Bewertungsphase aus und meldet auch keinen phasenweisen Fortschritt.

Grundeinstellungen
==================

Die LLM-Funktion wird an den folgenden zwei Stellen konfiguriert.

Allgemeine Einstellungen in der Administrationsoberfläche / system.properties
------------------------------------------------------------------------------

Konfiguration über die allgemeinen Einstellungen der Administrationsoberfläche oder in ``system.properties``. Wird zur Auswahl des LLM-Anbieters verwendet.

::

    # LLM-Anbieter angeben (ollama, openai, gemini)
    rag.llm.name=ollama

fess_config.properties
-----------------------

Konfiguration in ``app/WEB-INF/classes/fess_config.properties`` (bei der Paketversion ``/etc/fess/fess_config.properties``).
Diese Datei dient der Aktivierung des KI-Suchmodus, der Sitzungs- und Verlaufskonfiguration sowie anbieterspezifischer Einstellungen (Verbindungs-URLs, API-Schlüssel, Generierungsparameter usw.).

::

    # KI-Suchmodus-Funktion aktivieren (Standard: false)
    rag.chat.enabled=true

    # Beispiel für anbieterspezifische Einstellungen (OpenAI)
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

Detaillierte Einstellungen für jeden Anbieter finden Sie in den folgenden Dokumenten.

- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`llm-openai` - OpenAI-Konfiguration
- :doc:`llm-gemini` - Google Gemini-Konfiguration

Gemeinsame Einstellungen
========================

Einstellungselemente, die für alle LLM-Anbieter gemeinsam gelten. Diese werden in ``fess_config.properties`` konfiguriert.

Kontexteinstellungen
--------------------

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

.. note::

   Die maximale Zeichenzahl des Kontexts (``context.max.chars``) wurde auf eine anbieter- und prompttypspezifische Einstellung umgestellt. Konfigurieren Sie diese in ``fess_config.properties`` als ``rag.llm.{provider}.{promptType}.context.max.chars``.

Systemprompt
------------

Systemprompts werden nicht in Property-Dateien, sondern in den DI-XML-Dateien der jeweiligen Plugins verwaltet.

Der Systemprompt wird in der Datei ``fess_llm++.xml`` definiert, die in der JAR-Datei jedes ``fess-llm-*``-Plugins enthalten ist.
Um den Prompt anzupassen, müssen Sie die JAR-Datei nicht entpacken und die Datei darin bearbeiten. Dank des LastaDi-Mechanismus zur
Neudefinition von Komponenten wird die Komponentendefinition des Plugins ersetzt, wenn Sie in ``app/WEB-INF/classes/`` eine Datei mit
dem Namen ``fess_llm+{Komponentenname}.xml`` ablegen.

Die Komponentennamen sind je nach Anbieter wie folgt:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Anbieter
     - Komponentenname
   * - Ollama
     - ``ollamaLlmClient``
   * - OpenAI
     - ``openaiLlmClient``
   * - Google Gemini
     - ``geminiLlmClient``

Um beispielsweise den Antwortgenerierungs-Prompt des OpenAI-Anbieters zu ändern, erstellen Sie ``app/WEB-INF/classes/fess_llm+openaiLlmClient.xml``.

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="openaiLlmClient" class="org.codelibs.fess.llm.openai.OpenAiLlmClient">
            <postConstruct name="register"/>
            <postConstruct name="init"/>
            <preDestroy name="destroy"/>
            <property name="answerGenerationSystemPrompt">"Eigener Antwortgenerierungs-Prompt"</property>
            <!-- Auch alle unveränderten Prompt-Eigenschaften vollständig angeben -->
        </component>
    </components>

.. warning::

   Die Neudefinitionsdatei ersetzt die Komponentendefinition vollständig. Geben Sie daher alle Inhalte an, die in der ursprünglichen
   ``fess_llm++.xml`` enthalten sind (Klassenname, ``postConstruct``, ``preDestroy`` sowie alle unveränderten Prompt-Eigenschaften).
   Nicht angegebene Eigenschaften werden zurückgesetzt.

.. warning::

   Kopieren Sie nicht einfach ``fess_llm++.xml`` selbst nach ``app/WEB-INF/classes/``.
   Da bei DI-XML-Dateien, deren Dateiname auf ``++`` endet, alle Vorkommen im Classpath als „Ergänzung“ geladen werden, würde dieselbe
   Komponente doppelt registriert, was zu ``TooManyRegistrationComponentException`` führt und den Start von |Fess| verhindert.

Verfügbarkeitsprüfung
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervall zur regelmäßigen Prüfung der LLM-Verfügbarkeit (Sekunden)
     - ``60``

Diese Einstellung wird in ``fess_config.properties`` vorgenommen. |Fess| überprüft regelmäßig den Verbindungsstatus zum LLM-Anbieter.

.. note::

   Wird für diese Eigenschaft ein Wert kleiner oder gleich ``0`` oder ein nicht-numerischer Wert angegeben, wird dieser ignoriert, und stattdessen wird der Standardwert (``60``) verwendet.
   Mit dieser Eigenschaft lässt sich die Verfügbarkeitsprüfung nicht deaktivieren.
   Zudem wird die Verfügbarkeitsprüfung nicht ausgeführt, wenn ``rag.chat.enabled`` auf ``false`` gesetzt ist, sowie für Anbieter, die nicht über ``rag.llm.name`` ausgewählt sind.

Sitzungsverwaltung
==================

Einstellungen zu Chat-Sitzungen. Diese werden in ``fess_config.properties`` konfiguriert.

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
     - Maximale Anzahl der Sitzungen
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximale Anzahl der Nachrichten im Gesprächsverlauf
     - ``30``

Gleichzeitigkeitssteuerung
===========================

Einstellungen zur Steuerung der gleichzeitigen Anfragen an das LLM. Konfiguration in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - Maximale Anzahl gleichzeitiger Anfragen an den Anbieter
     - ``5``
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - Maximale Wartezeit (Millisekunden) bis eine freie Kapazität verfügbar ist, wenn die Gleichzeitigkeitsgrenze erreicht wurde. Wird innerhalb dieser Zeit keine Kapazität frei, wird ein Ratenlimitierungsfehler zurückgegeben
     - ``30000``

Um beispielsweise die Gleichzeitigkeitssteuerung für den OpenAI-Anbieter zu konfigurieren:

::

    rag.llm.openai.max.concurrent.requests=10

Bewertungseinstellungen
=======================

Einstellungen zur Bewertung der Suchergebnisse. Konfiguration in ``fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl der in der Bewertungsphase ausgewählten relevanten Dokumente
     - ``3``

Prompttypspezifische Einstellungen
====================================

Generierungsparameter können für jeden Prompttyp einzeln konfiguriert werden. Dies ermöglicht eine feinere Abstimmung je nach Verwendungszweck. Die Konfiguration erfolgt in ``fess_config.properties``.

Prompttypen-Übersicht
---------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Prompttyp
     - Einstellungswert
     - Beschreibung
   * - Absichtsanalyse
     - ``intent``
     - Analysiert die Benutzerfrage und extrahiert Suchbegriffe
   * - Bewertung
     - ``evaluation``
     - Bewertet die Relevanz der Suchergebnisse
   * - Unklare Anfrage
     - ``unclear``
     - Generiert eine Antwort, wenn die Frage unklar ist
   * - Keine Ergebnisse
     - ``noresults``
     - Generiert eine Antwort, wenn keine Suchergebnisse gefunden werden
   * - Dokument nicht vorhanden
     - ``docnotfound``
     - Generiert eine Antwort, wenn kein passendes Dokument existiert
   * - Antwortgenerierung
     - ``answer``
     - Generiert eine Antwort auf Basis der Suchergebnisse
   * - Zusammenfassung
     - ``summary``
     - Generiert eine Zusammenfassung des Dokuments
   * - FAQ
     - ``faq``
     - Generiert eine Antwort im FAQ-Format
   * - Direkte Antwort
     - ``direct``
     - Generiert eine Antwort ohne Suchumweg (wird in der aktuellen Version nicht aufgerufen)
   * - Query-Regenerierung
     - ``queryregeneration``
     - Regeneriert die Abfrage, wenn keine Suchergebnisse gefunden werden

Konfigurationsmuster
--------------------

Prompttypspezifische Einstellungen werden nach folgendem Muster angegeben.

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

Konfigurationsbeispiel (OpenAI-Anbieter):

::

    # Temperatur für die Antwortgenerierung niedrig setzen
    rag.llm.openai.answer.temperature=0.5
    # Maximale Token-Anzahl für die Antwortgenerierung
    rag.llm.openai.answer.max.tokens=4096
    # Für die Absichtsanalyse ist eine kurze Antwort ausreichend, daher niedrig setzen
    rag.llm.openai.intent.max.tokens=256
    # Maximale Zeichenzahl des Kontexts für die Zusammenfassung
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature``, ``max.tokens`` und ``context.max.chars`` sind bei allen Anbietern gemeinsam verfügbar. Die Standardwerte dieser Parameter unterscheiden sich jedoch je nach Anbieter und Prompttyp.

Darüber hinaus unterstützt jeder Anbieter eigene Parameter. Die Unterstützung im Überblick:

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - Parameter
     - Ollama
     - OpenAI
     - Gemini
   * - ``thinking.budget``
     - Unterstützt
     - Nicht unterstützt
     - Unterstützt
   * - ``thinking.level``
     - Unterstützt
     - Nicht unterstützt
     - Nicht unterstützt
   * - ``top.p``
     - Unterstützt
     - Unterstützt
     - Nicht unterstützt
   * - ``top.k``, ``num.ctx``
     - Unterstützt
     - Nicht unterstützt
     - Nicht unterstützt
   * - ``reasoning.effort``
     - Nicht unterstützt
     - Unterstützt
     - Nicht unterstützt
   * - ``frequency.penalty``, ``presence.penalty``
     - Nicht unterstützt
     - Unterstützt
     - Nicht unterstützt

.. note::

   Wird ein „nicht unterstützter“ Parameter angegeben, führt dies nicht zu einem Fehler, sondern der Parameter wird einfach ignoriert. Details zur Bedeutung der einzelnen Parameter und den zulässigen Werten finden Sie in der jeweiligen Anbieterdokumentation.

.. note::

   Nur beim Ollama-Anbieter gibt es einen Fallback, der bei fehlender prompttypspezifischer Einstellung auf ``rag.llm.ollama.default.{Parameter}`` zurückgreift
   (mit Ausnahme von ``context.max.chars``). Für die Anbieter OpenAI und Gemini gibt es diesen Fallback nicht; fehlt eine prompttypspezifische Einstellung,
   wird stattdessen der im Plugin fest hinterlegte Standardwert verwendet.

Nächste Schritte
================

- :doc:`llm-ollama` - Detaillierte Ollama-Konfiguration
- :doc:`llm-openai` - Detaillierte OpenAI-Konfiguration
- :doc:`llm-gemini` - Detaillierte Google Gemini-Konfiguration
- :doc:`rag-chat` - Detaillierte Konfiguration der KI-Suchmodus-Funktion
- :doc:`rank-fusion` - Rank Fusion Konfiguration (Zusammenführung hybrider Suchergebnisse)
- :doc:`../user/chat-search` - Verwendung des KI-Suchmodus
- :doc:`../api/api-chat` - Chat-API-Referenz
