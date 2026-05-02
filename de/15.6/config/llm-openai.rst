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
     - ``ollama``
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
   * - ``rag.llm.openai.concurrency.wait.timeout``
     - Timeout fuer gleichzeitige Anfragewartung (ms)
     - ``30000``
     - fess_config.properties
   * - ``rag.llm.openai.reasoning.token.multiplier``
     - Max-Tokens-Multiplikator fuer Reasoning-Modelle
     - ``4``
     - fess_config.properties
   * - ``rag.llm.openai.retry.max``
     - Maximale Anzahl von HTTP-Wiederholungsversuchen (bei ``429`` und ``5xx``-Fehlern)
     - ``10``
     - fess_config.properties
   * - ``rag.llm.openai.retry.base.delay.ms``
     - Basisverzögerung des exponentiellen Backoffs (in Millisekunden)
     - ``2000``
     - fess_config.properties
   * - ``rag.llm.openai.stream.include.usage``
     - Beim Streaming ``stream_options.include_usage=true`` senden, um im letzten Chunk die Token-Nutzungsinformationen zu erhalten
     - ``true``
     - fess_config.properties
   * - ``rag.llm.openai.history.max.chars``
     - Maximale Zeichenzahl fuer Konversationsverlauf
     - ``8000``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.messages``
     - Maximale Verlaufsnachrichten fuer Absichtserkennung
     - ``8``
     - fess_config.properties
   * - ``rag.llm.openai.intent.history.max.chars``
     - Maximale Verlaufszeichen fuer Absichtserkennung
     - ``4000``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.max.chars``
     - Maximale Zeichenzahl fuer Assistenznachrichten
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.history.assistant.summary.max.chars``
     - Maximale Zeichenzahl fuer Assistenzzusammenfassung
     - ``800``
     - fess_config.properties
   * - ``rag.llm.openai.chat.evaluation.description.max.chars``
     - Maximale Zeichenzahl fuer Dokumentbeschreibung bei der Bewertung
     - ``500``
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

- ``rag.llm.openai.{promptType}.temperature`` - Zufaelligkeit der Generierung (0.0-2.0). Wird bei Reasoning-Modellen (o1/o3/o4/gpt-5-Serie) ignoriert
- ``rag.llm.openai.{promptType}.max.tokens`` - Maximale Token-Anzahl
- ``rag.llm.openai.{promptType}.context.max.chars`` - Maximale Zeichenzahl des Kontexts (Standard: ``16000`` fuer answer/summary, ``10000`` fuer andere)

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
     - Prompt fuer direkte Antworten
   * - ``queryregeneration``
     - Prompt zur Neugenerierung von Suchanfragen

Standardwerte
-------------

Standardwerte fuer jeden Prompttyp. Die Temperatureinstellung wird bei Reasoning-Modellen (o1/o3/o4/gpt-5-Serie) ignoriert.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Prompttyp
     - Temperature
     - Max Tokens
     - Hinweise
   * - ``intent``
     - 0.1
     - 256
     - Deterministische Absichtserkennung
   * - ``evaluation``
     - 0.1
     - 256
     - Deterministische Relevanzbewertung
   * - ``unclear``
     - 0.7
     - 512
     -
   * - ``noresults``
     - 0.7
     - 512
     -
   * - ``docnotfound``
     - 0.7
     - 256
     -
   * - ``direct``
     - 0.7
     - 1024
     -
   * - ``faq``
     - 0.7
     - 1024
     -
   * - ``answer``
     - 0.5
     - 2048
     - Hauptantwortgenerierung
   * - ``summary``
     - 0.3
     - 2048
     - Zusammenfassungsgenerierung
   * - ``queryregeneration``
     - 0.3
     - 256
     - Suchanfrageneugenerierung

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

Retry-Verhalten
===============

Anfragen an die OpenAI-API werden bei folgenden HTTP-Statuscodes automatisch wiederholt:

- ``429`` Too Many Requests (Ratenbegrenzung)
- ``500`` Internal Server Error
- ``502`` Bad Gateway (kann von OpenAI bei Überlastung des Upstreams zurückgegeben werden)
- ``503`` Service Unavailable
- ``504`` Gateway Timeout

Bei einem Wiederholungsversuch wird mit exponentiellem Backoff gewartet (Basiswert ``rag.llm.openai.retry.base.delay.ms`` Millisekunden, maximal ``rag.llm.openai.retry.max`` Versuche, mit ±20% Jitter).
Sendet der Server einen ``Retry-After``-Header (ganzzahlige Sekunden, auf maximal ``600`` Sekunden begrenzt), so hat dessen Wert Vorrang vor dem exponentiellen Backoff. Dies entspricht der offiziellen Empfehlung von OpenAI.

Beachten Sie, dass ``IOException`` (Verbindungstimeout, Socket-Reset, DNS-Fehler) nicht wiederholt werden. Falls die Anfrage den Server möglicherweise erreicht hat, könnte ein Wiederholungsversuch zu doppelter Abrechnung führen.
Bei Streaming-Anfragen wird nur der initiale Verbindungsaufbau wiederholt; Fehler, die nach Beginn des Empfangs des Antwortkörpers auftreten, werden sofort weitergegeben.

.. note::
   Im Worst Case mit den Standardwerten (max. 10 Versuche, Basis 2 Sekunden) beträgt die Summe der Backoff-Zeiten für 9 Versuche ``2 + 4 + 8 + ... + 512 ≈ 1022 Sekunden (etwa 17 Minuten)``. Wenn jedes Mal ein ``Retry-After`` (max. 600 Sekunden) zurückgegeben wird, kann sich dies im Extremfall auf ``9 × 600 Sekunden = 90 Minuten`` ausdehnen. Wenn Sie die Latenz strenger kontrollieren möchten, setzen Sie ``rag.llm.openai.retry.max`` auf einen kleineren Wert.

Streaming und Nutzungsinformationen
===================================

Standardmäßig wird ``stream_options.include_usage=true`` an die Anfrage angehängt, sodass im letzten SSE-Chunk der Streaming-Antwort ein ``usage``-Objekt empfangen wird (bei Reasoning-Modellen einschließlich ``completion_tokens_details.reasoning_tokens``, bei aktivierter Prompt-Caching-Funktion einschließlich ``prompt_tokens_details.cached_tokens``).

Wenn Sie Backends verwenden, die das Feld ``stream_options.include_usage`` nicht akzeptieren (z. B. vLLM oder Azure OpenAI-kompatible Gateways), deaktivieren Sie diese Option wie folgt::

    rag.llm.openai.stream.include.usage=false

Logging und Anomalieerkennung
=============================

Seit |Fess| 15.6.1 gibt der OpenAI-Client folgende strukturierten Logmeldungen aus. Damit können Token-Nutzung und Antwortanomalien überwacht werden, ohne dass die ``DEBUG``-Stufe aktiviert werden muss.

- ``[LLM:OPENAI] Stream completed.`` (INFO) – Wird beim Abschluss einer Streaming-Antwort ausgegeben und enthält die Anzahl der Chunks, die Zeit bis zum ersten Chunk, Token-Nutzungsinformationen usw.
- ``[LLM:OPENAI] Chat response received.`` (INFO) – Wird beim Abschluss einer nicht-streamenden Antwort mit den gleichen Informationen ausgegeben.
- ``[LLM:OPENAI] Chat finished abnormally`` / ``Stream finished abnormally`` (WARN) – Wird ausgegeben, wenn ``finish_reason`` nicht ``stop`` ist (z. B. ``length`` für Abschneidung durch max_tokens, ``content_filter`` für Moderation, ``tool_calls`` / ``function_call`` für nicht beabsichtigte Tool-Aufrufkonfigurationen).
- ``[LLM:OPENAI] Stream refusal.`` (WARN) – Wird ausgegeben, wenn bei strukturierter Ausgabe ein ``delta.refusal`` zurückgegeben wird.

Diese WARN-Logs lassen sich nutzen, um ``max_tokens`` anzupassen, Content-Filter zu überprüfen und Fehlkonfigurationen von ``extra_params`` zu erkennen.

Maskierung von Anmeldeinformationen in URL-Logs
-----------------------------------------------

In den geloggten URLs werden Query-Parameter, die Anmeldeinformationen enthalten (``api_key``, ``apikey``, ``api-key``, ``key``, ``token``, ``access_token``, ``access-token``; Groß-/Kleinschreibung wird ignoriert), automatisch durch ``***`` ersetzt.

Der offizielle OpenAI-Endpunkt (``https://api.openai.com``) authentifiziert sich über den Header ``Authorization: Bearer``, sodass keine Anmeldeinformationen in der URL enthalten sind. Auch bei Verwendung benutzerdefinierter Proxys, die Anmeldeinformationen über Query-Parameter akzeptieren (z. B. einige Azure-Deployments oder vLLM-Gateways) und über ``rag.llm.openai.api.url`` konfiguriert werden, wird so verhindert, dass API-Schlüssel in den Logs erscheinen.

Unterstützung für Reasoning-Modelle
=====================================

Bei Verwendung von Reasoning-Modellen der o1/o3/o4-Serie oder der gpt-5-Serie verwendet |Fess| automatisch den OpenAI-API-Parameter ``max_completion_tokens`` anstelle von ``max_tokens``. Keine zusaetzlichen Konfigurationsaenderungen sind erforderlich.

.. note::
   Reasoning-Modelle (o1/o3/o4/gpt-5-Serie) ignorieren die ``temperature``-Einstellung und verwenden einen festen Wert (1). Ausserdem wird bei Reasoning-Modellen der Standard-``max_tokens`` mit ``reasoning.token.multiplier`` (Standard: 4) multipliziert.

Zusaetzliche Parameter fuer Reasoning-Modelle
--------------------------------------------

Bei Verwendung von Reasoning-Modellen können folgende zusätzliche Parameter in ``fess_config.properties`` konfiguriert werden:

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.openai.{promptType}.reasoning.effort``
     - Reasoning-Effort-Einstellung fuer o-Modelle (``low``, ``medium``, ``high``)
     - ``low`` (intent/evaluation/docnotfound/unclear/noresults/queryregeneration), nicht gesetzt (andere)
   * - ``rag.llm.openai.{promptType}.top.p``
     - Wahrscheinlichkeitsschwelle fuer die Token-Auswahl (0.0-1.0)
     - (nicht gesetzt)
   * - ``rag.llm.openai.{promptType}.frequency.penalty``
     - Haeufigkeitsstrafe (-2.0-2.0)
     - (nicht gesetzt)
   * - ``rag.llm.openai.{promptType}.presence.penalty``
     - Anwesenheitsstrafe (-2.0-2.0)
     - (nicht gesetzt)

``{promptType}`` kann ``intent``, ``evaluation``, ``answer``, ``summary`` usw. sein.

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

Konfiguration über JVM-Optionen
===============================

Aus Sicherheitsgründen wird empfohlen, API-Schlüssel über die Laufzeitumgebung
(JVM-Optionen) statt in eingecheckten Dateien zu konfigurieren.

Docker-Umgebung
---------------

Das offizielle `docker-fess <https://github.com/codelibs/docker-fess>`__ Repository
liefert ein OpenAI-Overlay (``compose-openai.yaml``) mit. Die minimalen Schritte sind:

::

    export OPENAI_API_KEY="sk-..."
    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

Inhalt von ``compose-openai.yaml`` (als Referenz für eigenes Setup):

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.6.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Hinweise:

- ``FESS_PLUGINS=fess-llm-openai:15.6.0`` lässt das ``run.sh`` des Containers das Plugin automatisch herunterladen und in ``app/WEB-INF/plugin/`` installieren
- ``-Dfess.config.rag.chat.enabled=true`` aktiviert den AI-Modus
- ``-Dfess.config.rag.llm.openai.api.key=...`` setzt den API-Schlüssel, ``-Dfess.config.rag.llm.openai.model=...`` wählt das Modell
- ``-Dfess.system.rag.llm.name=openai`` wirkt nur als initialer Default, bevor ein Wert in OpenSearch persistiert wurde. Nach dem Start kann der Wert auch unter Administration > System > Allgemein (RAG-Sektion) geändert werden

Bei Internetzugang über einen Proxy geben Sie die ``http.proxy.*``-Einstellungen von |Fess| über ``FESS_JAVA_OPTS`` an (siehe Abschnitt "HTTP-Proxy verwenden" weiter unten).

systemd-Umgebung
----------------

In ``/etc/sysconfig/fess`` (oder ``/etc/default/fess``) ``FESS_JAVA_OPTS`` ergänzen:

::

    FESS_JAVA_OPTS="-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=sk-... -Dfess.system.rag.llm.name=openai"

HTTP-Proxy verwenden
====================

Seit |Fess| 15.6.1 nutzt der OpenAI-Client die globale HTTP-Proxy-Konfiguration von |Fess|. Geben Sie die folgenden Eigenschaften in ``fess_config.properties`` an.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``http.proxy.host``
     - Proxy-Hostname (bei leerer Zeichenkette wird kein Proxy verwendet)
     - ``""``
   * - ``http.proxy.port``
     - Proxy-Portnummer
     - ``8080``
   * - ``http.proxy.username``
     - Benutzername für die Proxy-Authentifizierung (optional; wenn angegeben, wird Basic-Authentifizierung aktiviert)
     - ``""``
   * - ``http.proxy.password``
     - Passwort für die Proxy-Authentifizierung
     - ``""``

In Docker-Umgebungen geben Sie die Werte wie folgt über ``FESS_JAVA_OPTS`` an::

    -Dfess.config.http.proxy.host=proxy.example.com
    -Dfess.config.http.proxy.port=8080

.. note::
   Diese Einstellung wirkt sich auch auf den HTTP-Zugriff von |Fess| insgesamt (z. B. Crawler) aus.
   Die bisherigen Java-Systemeigenschaften (``-Dhttps.proxyHost`` usw.) werden vom OpenAI-Client nicht mehr ausgewertet.

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
