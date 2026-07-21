=======================================================
Übersicht über KI-Suchmodus (RAG) und LLM-Integration
=======================================================

Übersicht
=========

|Fess| unterstützt eine KI-Suchmodus-Funktion (RAG: Retrieval-Augmented Generation), die große Sprachmodelle (LLM) nutzt.
Mit dieser Funktion können Benutzer Informationen in einem dialogorientierten Format mit einem KI-Assistenten abrufen, der auf Suchergebnissen basiert, und erhalten so Antworten auf natürlichsprachliche Fragen direkt aus Ihrem Unternehmens-Suchindex mit zitierten Quellen.

Die LLM-Integrationsfunktion wird als ``fess-llm-*``-Plugin bereitgestellt. Installieren Sie das Plugin, das dem LLM-Anbieter entspricht, den Sie verwenden möchten.

Der KI-Suchmodus ruft Dokumente über die standardmäßige |Fess|-Suchpipeline (Rank Fusion) ab, nicht über einen separaten Vektorindex — standardmäßig handelt es sich dabei um eine Schlüsselwortsuche (BM25). Da diese Pipeline wiederverwendet wird, nimmt der semantische Sucher (Vektorsuche) des Semantic Search-Plugins, sofern installiert und konfiguriert, an der Rank Fusion für alle Suchen teil, einschließlich des Abrufschritts des KI-Suchmodus; eine KI-Suchmodus-spezifische Konfiguration ist nicht erforderlich. Siehe :doc:`rank-fusion`.

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
     - Cloud-API von OpenAI. Ermöglicht die Nutzung von Modellen wie GPT-4.
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

   Wenn ``rag.llm.name`` nicht gesetzt ist, ist standardmäßig nur der Ollama-Client aktiv; installieren Sie den gewünschten Anbieter und wählen Sie ihn über ``rag.llm.name`` aus.

Plugin-Installation
===================

Die LLM-Funktion wird als Plugin bereitgestellt. Die JAR-Datei des ``fess-llm-{provider}``-Plugins für den gewünschten Anbieter muss im Plugin-Verzeichnis abgelegt werden.

Als Beispiel: Wenn Sie den OpenAI-Anbieter verwenden möchten, laden Sie ``fess-llm-openai-15.8.0.jar`` herunter und legen Sie es im folgenden Verzeichnis ab.

::

    app/WEB-INF/plugin/

Nach der Ablage wird das Plugin beim nächsten Neustart von |Fess| geladen.

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

Konfiguration in ``app/WEB-INF/conf/fess_config.properties``. Diese Datei dient der Aktivierung des KI-Suchmodus, der Sitzungs- und Verlaufskonfiguration sowie anbieterspezifischer Einstellungen (Verbindungs-URLs, API-Schlüssel, Generierungsparameter usw.).

::

    # KI-Suchmodus-Funktion aktivieren
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

Der Systemprompt wird in der Datei ``fess_llm++.xml`` definiert, die in der JAR-Datei jedes ``fess-llm-*``-Plugins enthalten ist. Da diese Datei eine im Plugin-JAR gebündelte Classpath-Ressource ist, muss die DI-XML-Datei innerhalb des JARs bearbeitet werden, um den Prompt anzupassen.

Verfügbarkeitsprüfung
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.{provider}.availability.check.interval``
     - Intervall zur Prüfung der LLM-Verfügbarkeit (Sekunden). 0 zum Deaktivieren
     - ``60``

Diese Einstellung wird in ``fess_config.properties`` vorgenommen. |Fess| überprüft regelmäßig den Verbindungsstatus zum LLM-Anbieter.

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
     - Generiert eine Antwort ohne Suchumweg
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

   ``temperature``, ``max.tokens`` und ``context.max.chars`` sind bei allen Anbietern gemeinsam verfügbar. Darüber hinaus unterstützt jeder Anbieter eigene Parameter wie ``thinking.budget``, ``top.p`` oder ``reasoning.effort``. Details entnehmen Sie bitte der jeweiligen Anbieterdokumentation.

Nächste Schritte
================

- :doc:`llm-ollama` - Detaillierte Ollama-Konfiguration
- :doc:`llm-openai` - Detaillierte OpenAI-Konfiguration
- :doc:`llm-gemini` - Detaillierte Google Gemini-Konfiguration
- :doc:`rag-chat` - Detaillierte Konfiguration der KI-Suchmodus-Funktion
- :doc:`rank-fusion` - Rank Fusion Konfiguration (Zusammenführung hybrider Suchergebnisse)
