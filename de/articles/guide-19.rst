============================================================
Teil 19: Aufbau eines internen KI-Assistenten -- Ein suchbasiertes Frage-Antwort-System mit RAG
============================================================

Einleitung
==========

Im vorherigen Artikel haben wir die Konzepte der semantischen Suche erläutert.
In diesem Artikel bauen wir als Weiterentwicklung dieses Ansatzes einen internen KI-Assistenten mit RAG (Retrieval-Augmented Generation) auf.

RAG ist ein Mechanismus, der „relevante Dokumente über die Suche findet und ein LLM (Large Language Model) auf Basis deren Inhalts Antworten generiert".
Da die Antworten auf internen Dokumenten basieren, kann RAG unternehmensspezifische Fragen beantworten, die eine allgemeine Chat-KI nicht beantworten kann.

Zielgruppe
==========

- Personen, die am Aufbau eines internen KI-Assistenten interessiert sind
- Personen, die lernen möchten, wie RAG implementiert wird
- Personen, die die Optionen für die LLM-Integration verstehen möchten

Funktionsweise von RAG
=======================

RAG-Pipeline
------------

Der KI-Suchmodus von Fess arbeitet mit folgender Pipeline:

1. **Absichtsanalyse (Intent)**: Analysiert die Frage des Benutzers und klassifiziert die Absicht (Suche, Zusammenfassung, FAQ, unklar)
2. **Suche (Search)**: Ruft relevante Dokumente aus dem Fess-Index ab (bei null Treffern werden Abfragen automatisch neu generiert und erneut gesucht)
3. **Bewertung (Evaluate)**: Das LLM bewertet die Relevanz der abgerufenen Dokumente
4. **Volltextabruf (Fetch)**: Ruft den vollständigen Text hochrelevanter Dokumente ab
5. **Antwortgenerierung (Answer)**: Das LLM generiert eine Streaming-Antwort mit Quellenangaben basierend auf dem Dokumentinhalt

Diese Pipeline reduziert „plausible, aber ungenaue Antworten (Halluzinationen)" des LLM und liefert Antworten, die durch interne Dokumente belegt sind.

Der KI-Suchmodus von Fess erfordert keine Vektorsuche (Embedding-Modelle).
Er nutzt bestehende Volltextsuchindizes unverändert, wobei das LLM die Bewertung der Suchergebnisse und die Antwortgenerierung übernimmt.
Dadurch können Sie RAG-basierte KI-Suche sofort einführen, ohne zusätzliche Infrastrukturvorbereitungen wie die Auswahl von Embedding-Modellen oder den Aufbau von Vektordatenbanken.

Auswahl eines LLM-Anbieters
============================

Fess unterstützt drei LLM-Backends.
Im Folgenden finden Sie eine Zusammenfassung der Merkmale und Auswahlkriterien der einzelnen Anbieter.

.. list-table:: Vergleich der LLM-Anbieter
   :header-rows: 1
   :widths: 15 25 25 35

   * - Anbieter
     - Plugin
     - Kosten
     - Merkmale
   * - OpenAI
     - fess-llm-openai
     - Nutzungsbasierte API-Abrechnung
     - Hohe Antwortqualität, GPT-4o-Unterstützung, einfacher Einstieg
   * - Google Gemini
     - fess-llm-gemini
     - Nutzungsbasierte API-Abrechnung
     - Unterstützung für erweitertes Denken, langer Kontext
   * - Ollama
     - fess-llm-ollama
     - Hardwarekosten
     - Lokale Ausführung, Daten verlassen das Unternehmen nicht, Datenschutz im Fokus

Auswahlkriterien
----------------

**Wann Sie eine Cloud-API (OpenAI / Gemini) wählen sollten**

- Sie möchten die anfänglichen Kosten minimieren
- Sie können keinen GPU-Server bereitstellen
- Sie priorisieren die Antwortqualität über alles
- Das Senden von Daten an externe Dienste ist zulässig

**Wann Sie lokale Ausführung (Ollama) wählen sollten**

- Das Senden interner Daten an externe Dienste ist nicht gestattet
- Die Sicherheits- und Datenschutzanforderungen sind streng
- Sie können einen GPU-Server bereitstellen
- Sie möchten die laufenden Kosten senken (bei hohem Nutzungsvolumen)

Einrichtung des KI-Suchmodus
==============================

Installation des Plugins
------------------------

Installieren Sie das Plugin, das Ihrem gewählten LLM-Anbieter entspricht.

1. Navigieren Sie in der Administrationskonsole zu [System] > [Plugins]
2. Installieren Sie das entsprechende Plugin (z. B. ``fess-llm-openai``)

Aktivierung des KI-Suchmodus
-----------------------------

Aktivieren Sie den KI-Suchmodus in den Fess-Einstellungen.

Setzen Sie ``rag.chat.enabled=true`` in den Einstellungen der Administrationskonsole oder in der Konfigurationsdatei.

LLM-Verbindungseinstellungen
-----------------------------

Konfigurieren Sie die Verbindungsinformationen für Ihren gewählten LLM-Anbieter.

**Für OpenAI**

- API-Schlüssel
- Zu verwendendes Modell (gpt-4o, gpt-4o-mini usw.)
- Maximale Tokenanzahl

**Für Ollama**

- URL des Ollama-Servers
- Name des zu verwendenden Modells
- Hinzufügen eines Dienstes über Docker Compose

.. code-block:: yaml

    services:
      ollama:
        image: ollama/ollama
        volumes:
          - ollama-data:/root/.ollama
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

Das KI-Chat-Erlebnis
=====================

Chat-Benutzeroberfläche
-----------------------

Wenn der KI-Suchmodus aktiviert ist, wird der KI-Suchmodus zur Fess-Suchoberfläche hinzugefügt.
Benutzer können zwischen Stichwortsuche und KI-Chat wechseln.

Beispiel für Frage und Antwort
------------------------------

**Frage**: „Wie beantrage ich Urlaub?"

**KI-Antwort**:

    Um Urlaub zu beantragen, gehen Sie wie folgt vor:

    1. Rufen Sie die Seite „Zeiterfassung" im internen Portal auf
    2. Wählen Sie „Urlaub" im Menü „Abwesenheitsantrag"
    3. Geben Sie die Daten ein, wählen Sie Ihren Vorgesetzten und reichen Sie den Antrag ein

    Bitte reichen Sie Ihren Antrag mindestens 3 Werktage vor dem Urlaubstermin ein.

    Referenz: [Betriebsordnung, Artikel 15](https://portal/rules/chapter15.html)

Die Antwort enthält Quellenlinks, sodass Benutzer die Originaldokumente überprüfen können.

Nutzung der Chat-API (SSE)
============================

Um den KI-Suchmodus programmgesteuert zu nutzen, verwenden Sie die Chat-API.
Die Chat-API liefert Streaming-Antworten über Server-Sent Events (SSE).

Für Streaming-Antworten (SSE):

::

    GET /api/v1/chat/stream?message=Wie beantrage ich Urlaub

Für nicht-streamende JSON-Antworten:

::

    POST /api/v1/chat
    Content-Type: application/x-www-form-urlencoded

    message=Wie beantrage ich Urlaub

Mit SSE werden Antworten in Echtzeit an den Client gesendet, sobald sie generiert werden.
Benutzer können die schrittweise angezeigte Antwort lesen, ohne auf die vollständige Generierung warten zu müssen.

Gesprächsverlauf
----------------

Die Chat-API unterstützt sitzungsbasierten Gesprächsverlauf.
Folgefragen basierend auf dem Kontext vorheriger Fragen sind möglich.

Beispiel:

- F1: „Wie beantrage ich Urlaub?"
- A1: (Antwort wie oben)
- F2: „Was soll ich tun, wenn ich die Antragsfrist verpasst habe?"
- A2: (Antwort basierend auf dem Kontext von F1)

RAG-Tuning
===========

Verbesserung der Antwortqualität
---------------------------------

Die Antwortqualität von RAG wird durch folgende Faktoren beeinflusst:

**Suchqualität**

Da RAG Antworten auf Basis von Suchergebnissen generiert, wirkt sich die Suchqualität direkt auf die Antwortqualität aus.
Die Verbesserung der Suchqualität durch den in Teil 8 beschriebenen Tuning-Zyklus führt auch zu einer verbesserten RAG-Qualität.

**Dokumentqualität**

Wenn die durchsuchten Dokumente veraltet, ungenau oder mehrdeutig sind, sinkt auch die Antwortqualität von RAG.
Regelmäßige Aktualisierungen und Qualitätsmanagement der Dokumente sind wichtig.

**Prompt-Einstellungen**

Durch das Tuning der an das LLM gesendeten Prompts (Anweisungstexte) können Sie den Stil und die Genauigkeit der Antworten anpassen.

Sicherheitsaspekte
===================

Schutz vor Prompt-Injection
----------------------------

Die RAG-Funktion von Fess verfügt über einen integrierten Schutz vor Prompt-Injection.
Sie schützt vor Angriffen, die versuchen, das Verhalten des LLM durch bösartige Eingaben zu manipulieren.

Verhinderung von Informationslecks
------------------------------------

Da RAG Antworten auf Basis von Suchergebnissen generiert, stellt die Kombination mit der rollenbasierten Suche (Teil 5) sicher, dass nur Antworten generiert werden, die den Berechtigungen des Benutzers entsprechen.
Inhalte aus Dokumenten, auf die der Benutzer keinen Zugriff hat, werden in RAG-Antworten nicht berücksichtigt.

Zusammenfassung
===============

In diesem Artikel haben wir erklärt, wie Sie mit dem KI-Suchmodus von Fess einen internen KI-Assistenten aufbauen.

- Funktionsweise der RAG-Pipeline (Absichtsanalyse -> Suche -> Bewertung -> Antwortgenerierung)
- Auswahlkriterien für drei LLM-Anbieter (OpenAI, Gemini, Ollama)
- Einrichtung und Erfahrung des KI-Suchmodus
- Programmgesteuerte Nutzung über die Chat-API (SSE)
- Tuning der Antwortqualität und Sicherheitsaspekte

Mit einem KI-Assistenten, der auf internen Dokumenten basiert, wandelt sich die Wissensnutzung von „Suchen" zu „Fragen".

Im nächsten Artikel behandeln wir, wie Sie Fess als MCP-Server in KI-Agenten integrieren.

Referenzen
==========

- `Fess AI Search Mode Settings <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Fess Chat API <https://fess.codelibs.org/ja/15.5/api/api-chat.html>`__
