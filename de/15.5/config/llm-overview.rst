==========================
Übersicht LLM-Integration
==========================

Übersicht
=========

|Fess| 15.5 unterstützt eine AI-Modus-Funktion (RAG: Retrieval-Augmented Generation), die große Sprachmodelle (LLM) nutzt.
Mit dieser Funktion können Benutzer Informationen in einem dialogorientierten Format mit einem KI-Assistenten abrufen, der auf Suchergebnissen basiert.

Unterstützte Anbieter
=====================

|Fess| unterstützt die folgenden LLM-Anbieter.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Anbieter
     - Einstellungswert
     - Beschreibung
   * - Ollama
     - ``ollama``
     - Open-Source-LLM-Server, der in lokalen Umgebungen läuft. Kann Modelle wie Llama, Mistral, Gemma ausführen. Standardeinstellung.
   * - OpenAI
     - ``openai``
     - Cloud-API von OpenAI. Ermöglicht die Nutzung von Modellen wie GPT-4.
   * - Google Gemini
     - ``gemini``
     - Cloud-API von Google. Ermöglicht die Nutzung von Gemini-Modellen.

Architektur
===========

Die AI-Modus-Funktion arbeitet mit dem folgenden Ablauf.

1. **Benutzereingabe**: Benutzer gibt eine Frage in der Chat-Oberfläche ein
2. **Absichtsanalyse**: LLM analysiert die Benutzerfrage und extrahiert Suchbegriffe
3. **Suchausführung**: Suche nach relevanten Dokumenten mit der |Fess|-Suchmaschine
4. **Ergebnisbewertung**: LLM bewertet die Relevanz der Suchergebnisse und wählt optimale Dokumente aus
5. **Antwortgenerierung**: LLM generiert eine Antwort basierend auf den ausgewählten Dokumenten
6. **Quellenangabe**: Die Antwort enthält Links zu den Quelldokumenten

Grundeinstellungen
==================

Um die LLM-Funktion zu aktivieren, fügen Sie die folgenden Einstellungen zu ``app/WEB-INF/conf/system.properties`` hinzu.

AI-Modus aktivieren
-------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

LLM-Anbieter auswählen
----------------------

::

    # LLM-Anbieter angeben (ollama, openai, gemini)
    rag.llm.type=ollama

Detaillierte Einstellungen für jeden Anbieter finden Sie in den folgenden Dokumenten.

- :doc:`llm-ollama` - Ollama-Konfiguration
- :doc:`llm-openai` - OpenAI-Konfiguration
- :doc:`llm-gemini` - Google Gemini-Konfiguration

Gemeinsame Einstellungen
========================

Einstellungselemente, die für alle LLM-Anbieter gemeinsam sind.

Generierungsparameter
---------------------

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
     - Zufälligkeit der Generierung (0.0-1.0). Niedrigere Werte ergeben deterministischere Antworten
     - ``0.7``

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
   * - ``rag.chat.context.max.chars``
     - Maximale Zeichenzahl des Kontexts
     - ``4000``
   * - ``rag.chat.content.fields``
     - Aus Dokumenten abzurufende Felder
     - ``title,url,content,...``

Systemprompt
------------

::

    rag.chat.system.prompt=You are an AI assistant for Fess search engine. Answer questions based on the search results provided. Always cite your sources using [1], [2], etc.

Dieser Prompt definiert das grundlegende Verhalten des LLM. Er kann bei Bedarf angepasst werden.

Verfügbarkeitsprüfung
---------------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.availability.check.interval``
     - Intervall zur Prüfung der LLM-Verfügbarkeit (Sekunden). 0 zum Deaktivieren
     - ``60``

Mit dieser Einstellung überprüft |Fess| regelmäßig den Verbindungsstatus zum LLM-Anbieter.

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
     - Maximale Anzahl der Sitzungen
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - Maximale Anzahl der Nachrichten im Gesprächsverlauf
     - ``20``

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

Bewertungseinstellungen
=======================

Einstellungen zur Bewertung der Suchergebnisse.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl der in der Bewertungsphase ausgewählten relevanten Dokumente
     - ``3``

Nächste Schritte
================

- :doc:`llm-ollama` - Detaillierte Ollama-Konfiguration
- :doc:`llm-openai` - Detaillierte OpenAI-Konfiguration
- :doc:`llm-gemini` - Detaillierte Google Gemini-Konfiguration
- :doc:`rag-chat` - Detaillierte Konfiguration der AI-Modus-Funktion
