==========================
Ollama-Konfiguration
==========================

Übersicht
=========

Ollama ist eine Open-Source-Plattform zur Ausführung großer Sprachmodelle (LLM) in lokalen Umgebungen.
Die Ollama-Integrationsfunktion von |Fess| wird als Plugin ``fess-llm-ollama`` bereitgestellt und eignet sich für den Einsatz in privaten Umgebungen.

Durch die Verwendung von Ollama können Sie die KI-Suchmodus-Funktion nutzen, ohne Daten extern zu senden.

Hauptmerkmale
-------------

- **Lokale Ausführung**: Daten werden nicht extern gesendet, Datenschutz ist gewährleistet
- **Vielfältige Modelle**: Unterstützt viele Modelle wie Llama, Mistral, Gemma, CodeLlama
- **Kosteneffizienz**: Keine API-Kosten (nur Hardware-Kosten)
- **Anpassbar**: Auch selbst feinabgestimmte Modelle können verwendet werden

Unterstützte Modelle
--------------------

Hauptsächlich verfügbare Modelle bei Ollama:

- ``llama3.3:70b`` - Llama 3.3 von Meta (70B Parameter)
- ``gemma4:e4b`` - Gemma 4 von Google (E4B Parameter, Standard)
- ``mistral:7b`` - Mistral von Mistral AI (7B Parameter)
- ``codellama:13b`` - Code Llama von Meta (13B Parameter)
- ``phi3:3.8b`` - Phi-3 von Microsoft (3.8B Parameter)

.. note::
   Die aktuelle Liste verfügbarer Modelle finden Sie unter `Ollama Library <https://ollama.com/library>`__.

Voraussetzungen
===============

Bevor Sie Ollama verwenden, überprüfen Sie Folgendes.

1. **Ollama-Installation**: Laden Sie von `https://ollama.com/ <https://ollama.com/>`__ herunter und installieren Sie es
2. **Modell-Download**: Laden Sie das zu verwendende Modell in Ollama herunter
3. **Ollama-Server starten**: Stellen Sie sicher, dass Ollama läuft

Ollama-Installation
-------------------

Linux/macOS
~~~~~~~~~~~

::

    curl -fsSL https://ollama.com/install.sh | sh

Windows
~~~~~~~

Laden Sie den Installer von der offiziellen Website herunter und führen Sie ihn aus.

Docker
~~~~~~

::

    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Modell-Download
---------------

::

    # Standardmodell (Gemma 4 E4B) herunterladen
    ollama pull gemma4:e4b

    # Llama 3.3 herunterladen
    ollama pull llama3.3:70b

    # Modell testen
    ollama run gemma4:e4b "Hello, how are you?"

Plugin-Installation
===================

Die Ollama-Integrationsfunktion wird als Plugin bereitgestellt.
Zur Verwendung von Ollama ist die Installation des ``fess-llm-ollama``-Plugins erforderlich.

1. Laden Sie `fess-llm-ollama-15.8.0.jar` herunter.
2. Legen Sie die Datei im Verzeichnis ``app/WEB-INF/plugin/`` im |Fess|-Installationsverzeichnis ab.

::

    cp fess-llm-ollama-15.8.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Starten Sie |Fess| neu.

.. note::
   Die Plugin-Version muss mit der Version von |Fess| übereinstimmen.

Grundeinstellungen
==================

Die LLM-bezogenen Einstellungen sind auf mehrere Konfigurationsdateien aufgeteilt.

Minimalkonfiguration
--------------------

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf Ollama setzen
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # Ollama-URL (lokale Umgebung)
    rag.llm.ollama.api.url=http://localhost:11434

    # Zu verwendendes Modell
    rag.llm.ollama.model=gemma4:e4b

.. note::
   Die LLM-Anbietereinstellung kann auch über die Administrationsoberfläche (Administration > System > Allgemein) durch Setzen von ``rag.llm.name`` konfiguriert werden.

Empfohlene Konfiguration (Produktionsumgebung)
----------------------------------------------

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter-Einstellungen
    rag.llm.name=ollama

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # Ollama-URL
    rag.llm.ollama.api.url=http://localhost:11434

    # Modelleinstellungen (großes Modell verwenden)
    rag.llm.ollama.model=llama3.3:70b

    # Timeout-Einstellungen (für große Modelle erhöht)
    rag.llm.ollama.timeout=120000

    # Steuerung gleichzeitiger Anfragen
    rag.llm.ollama.max.concurrent.requests=5

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den Ollama-Client. Alle Einstellungen außer ``rag.llm.name`` werden in ``fess_config.properties`` vorgenommen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.ollama.api.url``
     - Basis-URL des Ollama-Servers
     - ``http://localhost:11434``
   * - ``rag.llm.ollama.model``
     - Zu verwendendes Modell (muss in Ollama heruntergeladen sein)
     - ``gemma4:e4b``
   * - ``rag.llm.ollama.timeout``
     - Anfrage-Timeout (Millisekunden)
     - ``60000``
   * - ``rag.llm.ollama.availability.check.interval``
     - Intervall der Verfügbarkeitsprüfung (Sekunden). Bei einem Wert von ``0`` oder kleiner wird die regelmäßige Verfügbarkeitsprüfung deaktiviert
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Maximale Anzahl gleichzeitiger Anfragen
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl relevanter Dokumente bei der Bewertung
     - ``3``
   * - ``rag.llm.ollama.concurrency.wait.timeout``
     - Timeout beim Warten auf eine Semaphore für die Gleichzeitigkeitssteuerung (Millisekunden)
     - ``30000``
   * - ``rag.llm.ollama.connect.timeout``
     - TCP-Verbindungs-Timeout (Millisekunden). Kann unabhängig von ``rag.llm.ollama.timeout`` angegeben werden
     - ``5000``
   * - ``rag.llm.ollama.retry.max``
     - Maximale Anzahl von HTTP-Wiederholungsversuchen (bei ``429``- und ``5xx``-Fehlern)
     - ``3``
   * - ``rag.llm.ollama.retry.base.delay.ms``
     - Basisverzögerung des exponentiellen Backoffs (Millisekunden)
     - ``2000``

Detaileinstellungen
-------------------

Detaillierte Einstellungselemente zu Verlauf und Kontextgröße.

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.ollama.chat.evaluation.description.max.chars``
     - Maximale Zeichenzahl der Beschreibung bei der Bewertung
     - ``500``
   * - ``rag.llm.ollama.history.max.chars``
     - Maximale Zeichenzahl des Gesprächsverlaufs
     - ``4000``
   * - ``rag.llm.ollama.intent.history.max.messages``
     - Maximale Nachrichtenanzahl im Verlauf bei der Absichtserkennung
     - ``6``
   * - ``rag.llm.ollama.intent.history.max.chars``
     - Maximale Zeichenzahl im Verlauf bei der Absichtserkennung
     - ``3000``
   * - ``rag.llm.ollama.history.assistant.max.chars``
     - Maximale Zeichenzahl der Assistentenantwort im Verlauf
     - ``500``
   * - ``rag.llm.ollama.history.assistant.summary.max.chars``
     - Maximale Zeichenzahl der Assistentenzusammenfassung im Verlauf
     - ``500``

Gleichzeitigkeitssteuerung
---------------------------

Mit ``rag.llm.ollama.max.concurrent.requests`` kann die Anzahl gleichzeitiger Anfragen an Ollama gesteuert werden.
Der Standardwert ist 5. Passen Sie diesen Wert entsprechend den Ressourcen des Ollama-Servers an.
Bei zu vielen gleichzeitigen Anfragen kann der Ollama-Server überlastet werden und die Antwortgeschwindigkeit sinken.

Prompttypspezifische Einstellungen
===================================

In |Fess| können LLM-Parameter für jeden Prompttyp angepasst werden.
Die Konfiguration erfolgt in ``fess_config.properties``.

Für jeden Prompttyp können folgende Parameter konfiguriert werden:

- ``rag.llm.ollama.{promptType}.temperature`` - Temperature bei der Generierung
- ``rag.llm.ollama.{promptType}.max.tokens`` - Maximale Token-Anzahl (wird auf ``num_predict`` der Ollama-API abgebildet)
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Maximale Zeichenzahl des Kontexts
- ``rag.llm.ollama.{promptType}.thinking.budget`` - Thinking-Budget (boolesche Steuerung des Denkens; Details siehe „Unterstützung für Thinking-Modelle")
- ``rag.llm.ollama.{promptType}.thinking.level`` - Thinking-Level (Zeichenfolgenformat ``high`` / ``medium`` / ``low``; Details siehe „Unterstützung für Thinking-Modelle")
- ``rag.llm.ollama.{promptType}.top.p`` - Wert für Top-P-Sampling
- ``rag.llm.ollama.{promptType}.top.k`` - Wert für Top-K-Sampling
- ``rag.llm.ollama.{promptType}.num.ctx`` - Kontextfenstergröße

Die Parameter werden in folgender Reihenfolge aufgelöst: ``rag.llm.ollama.{promptType}.<param>`` (prompttypspezifische Einstellung) → ``rag.llm.ollama.default.<param>`` (gemeinsamer Fallback für alle Prompttypen) → hartcodierter Standardwert je Prompttyp. Explizit in der Anfrage angegebene Werte haben stets Vorrang.

Verfügbare Prompttypen:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Prompttyp
     - Beschreibung
   * - ``intent``
     - Prompt zur Bestimmung der Benutzerabsicht
   * - ``evaluation``
     - Prompt zur Bewertung der Suchergebnisse
   * - ``unclear``
     - Antwort-Prompt für unklare Anfragen
   * - ``noresults``
     - Prompt bei fehlenden Suchergebnissen
   * - ``docnotfound``
     - Prompt, wenn kein Dokument gefunden wurde
   * - ``answer``
     - Prompt zur Antwortgenerierung
   * - ``summary``
     - Prompt zur Zusammenfassungsgenerierung
   * - ``faq``
     - Prompt zur FAQ-Generierung
   * - ``direct``
     - Prompt für direkte Antworten
   * - ``queryregeneration``
     - Prompt zur Abfrage-Neugenerierung

Für jeden Prompttyp gelten hartcodierte Standardwerte, die angewendet werden, wenn keine Einstellung vorgenommen wurde.

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Prompttyp
     - temperature
     - max.tokens
     - thinking.budget
     - context.max.chars
   * - ``intent``
     - ``0.1``
     - ``256``
     - ``0``
     - ``6000``
   * - ``evaluation``
     - ``0.1``
     - ``512``
     - ``0``
     - ``6000``
   * - ``unclear``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``noresults``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``docnotfound``
     - ``0.7``
     - ``512``
     - ``0``
     - ``6000``
   * - ``answer``
     - ``0.5``
     - ``8192``
     - (nicht gesetzt)
     - ``10000``
   * - ``summary``
     - ``0.3``
     - ``8192``
     - (nicht gesetzt)
     - ``10000``
   * - ``faq``
     - ``0.7``
     - ``4096``
     - (nicht gesetzt)
     - ``6000``
   * - ``direct``
     - ``0.7``
     - ``4096``
     - (nicht gesetzt)
     - ``6000``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``
     - ``0``
     - ``6000``

Konfigurationsbeispiel::

    # Temperature bei der Antwortgenerierung festlegen
    rag.llm.ollama.answer.temperature=0.7

    # Maximale Token-Anzahl bei der Zusammenfassungsgenerierung festlegen
    rag.llm.ollama.summary.max.tokens=2048

    # Maximale Zeichenzahl des Kontexts bei der Absichtsbestimmung festlegen
    rag.llm.ollama.intent.context.max.chars=4000

Ollama-Modelloptionen
======================

Modellparameter für Ollama können in ``fess_config.properties`` konfiguriert werden.
Durch Angabe im Format ``rag.llm.ollama.default.<param>`` wird der Wert als gemeinsamer Fallback für alle Prompttypen verwendet.
Der Fallback über ``default`` gilt nicht nur für ``top.p`` / ``top.k`` / ``num.ctx``, sondern auch für ``temperature`` / ``max.tokens`` / ``thinking.budget`` / ``thinking.level``.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.ollama.default.top.p``
     - Wert für Top-P-Sampling (0,0–1,0). Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.top.p`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.top.k``
     - Wert für Top-K-Sampling. Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.top.k`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.num.ctx``
     - Kontextfenstergröße. Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.num.ctx`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.temperature``
     - Fallback-Wert für die Temperature bei der Generierung. Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.temperature`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.max.tokens``
     - Fallback-Wert für die maximale Token-Anzahl. Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.max.tokens`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.thinking.budget``
     - Fallback-Wert für das Thinking-Budget. Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.thinking.budget`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.thinking.level``
     - Fallback-Wert für den Thinking-Level (``high`` / ``medium`` / ``low``). Kann je Prompttyp mit ``rag.llm.ollama.{promptType}.thinking.level`` überschrieben werden
     - (nicht gesetzt)
   * - ``rag.llm.ollama.options.*``
     - Globale Optionen, die direkt an die Ollama-API weitergegeben werden. Das Suffix wird als Optionsname verwendet (Beispiel: ``rag.llm.ollama.options.repeat_penalty=1.1``). Werte werden automatisch in Integer, Double, Boolean oder String konvertiert
     - (nicht gesetzt)

Konfigurationsbeispiel::

    # Standard-Top-P-Sampling (gemeinsam für alle Prompttypen)
    rag.llm.ollama.default.top.p=0.9

    # Standard-Top-K-Sampling
    rag.llm.ollama.default.top.k=40

    # Standard-Kontextfenstergröße
    rag.llm.ollama.default.num.ctx=4096

    # Top-P nur bei der Antwortgenerierung ändern
    rag.llm.ollama.answer.top.p=0.95

    # Globale Option (wird direkt an die Ollama-API weitergegeben)
    rag.llm.ollama.options.repeat_penalty=1.1

Unterstützung für Thinking-Modelle
====================================

Bei Verwendung von Thinking-Modellen wie gemma4 oder qwen3 unterstützt |Fess| die Konfiguration des Thinking-Budgets.

Das Thinking-Budget wird je Prompttyp in ``fess_config.properties`` konfiguriert:

::

    # Thinking-Budget bei der Antwortgenerierung konfigurieren
    rag.llm.ollama.answer.thinking.budget=1024

    # Thinking-Budget bei der Zusammenfassungsgenerierung konfigurieren
    rag.llm.ollama.summary.thinking.budget=1024

Durch Konfiguration des Thinking-Budgets kann die Anzahl der Token gesteuert werden, die dem Modell für den „Denkschritt" vor der Antwortgenerierung zur Verfügung stehen.

.. note::
   Bei Ollama wird das Thinking-Budget in ein boolesches Flag umgewandelt (bei einem Wert größer als 0: ``think: true``, bei 0: ``think: false``). Eine feingranulare Steuerung über die Token-Anzahl ist aufgrund von Einschränkungen der Ollama-API nicht verfügbar.

Thinking-Level
--------------

Einige Modelle wie gpt-oss ignorieren das boolesche ``think``-Flag und erfordern stattdessen die Angabe des Thinking-Levels im Zeichenfolgenformat ``high`` / ``medium`` / ``low``.
Für solche Modelle wird ``rag.llm.ollama.{promptType}.thinking.level`` verwendet.

::

    # Thinking-Level bei der Antwortgenerierung konfigurieren
    rag.llm.ollama.answer.thinking.level=high

    # Thinking-Level bei der Zusammenfassungsgenerierung konfigurieren
    rag.llm.ollama.summary.thinking.level=medium

Gültige Werte für ``thinking.level`` sind ``high`` / ``medium`` / ``low`` (Groß-/Kleinschreibung wird nicht beachtet). Ungültige Werte werden ignoriert und eine Warnung wird protokolliert.

.. note::
   Wenn sowohl ``thinking.level`` (Zeichenfolgenformat) als auch ``thinking.budget`` (boolesches Format) konfiguriert sind, hat ``thinking.level`` Vorrang. Verwenden Sie ``thinking.level`` für GPT-OSS-Modelle und ``thinking.budget`` für andere Thinking-Modelle.

Netzwerkkonfiguration
=====================

Docker-Konfiguration
--------------------

Das offizielle `docker-fess <https://github.com/codelibs/docker-fess>`__ von |Fess| enthält das Ollama-Overlay ``compose-ollama.yaml``. Die minimalen Schritte sind:

::

    docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    docker exec -it ollama01 ollama pull gemma4:e4b

``compose-ollama.yaml`` ist für den Einsatz mit NVIDIA-GPUs konfiguriert (NVIDIA Container Toolkit erforderlich). Der Inhalt lautet wie folgt:

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-ollama:15.8.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434"
        depends_on:
          - ollama01

      ollama01:
        image: ollama/ollama:latest
        container_name: ollama01
        ports:
          - "11434:11434"
        volumes:
          - ollama-data:/root/.ollama
        networks:
          - search_net
        restart: unless-stopped
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

    volumes:
      ollama-data:
        driver: local

Hinweise:

- ``FESS_PLUGINS=fess-llm-ollama:15.8.0`` bewirkt, dass das Startskript die Plugin-JAR automatisch herunterlädt und in ``app/WEB-INF/plugin/`` ablegt (passen Sie die Version an Ihre |Fess|-Version an)
- ``-Dfess.config.rag.chat.enabled=true`` aktiviert den KI-Suchmodus
- ``-Dfess.config.rag.llm.ollama.api.url=...`` legt die URL des Ollama-Servers fest (innerhalb des Docker-Compose-Netzwerks wird der Servicename wie ``ollama01`` aufgelöst)
- Da der Standard-LLM-Anbieter (``rag.llm.name``) bereits ``ollama`` ist, ist bei ausschließlicher Verwendung von Ollama keine explizite Angabe erforderlich. Beim Wechsel von einem anderen Anbieter fügen Sie ``-Dfess.system.rag.llm.name=ollama`` zu ``FESS_JAVA_OPTS`` hinzu oder konfigurieren Sie den Wert nach dem Start unter Administration > System > Allgemein im RAG-Abschnitt
- Der Block ``deploy.resources.reservations.devices`` dient der GPU-Nutzung. Wenn Sie keine GPU verwenden (nur CPU), entfernen Sie diesen Block

.. note::
   Großgeschriebene Snake-Case-Umgebungsvariablen wie ``RAG_CHAT_ENABLED`` oder ``RAG_LLM_NAME`` werden von |Fess| nicht direkt erkannt. Konfigurationswerte müssen stets innerhalb von ``FESS_JAVA_OPTS`` als ``-Dfess.config.<key>`` (für ``fess_config.properties``) oder ``-Dfess.system.<key>`` (für ``system.properties``) übergeben werden.

Remote-Ollama-Server
--------------------

Wenn Ollama auf einem separaten Server als Fess läuft:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama hat standardmäßig keine Authentifizierungsfunktion. Bei externem Zugriff sollten Sie Sicherheitsmaßnahmen auf Netzwerkebene (Firewall, VPN usw.) in Betracht ziehen.

HTTP-Proxy verwenden
====================

Der Ollama-Client nutzt die globale HTTP-Proxy-Konfiguration von |Fess|. Wenn die Verbindung zum Ollama-Server über einen Proxy erfolgen muss (z. B. bei Verwendung eines Remote-Ollama-Servers), geben Sie die folgenden Eigenschaften in ``fess_config.properties`` an.

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

.. note::
   Da Ollama in der Regel lokal oder in einem internen Netzwerk betrieben wird, ist eine Proxy-Konfiguration nur in begrenzten Fällen notwendig (z. B. bei Verwendung eines Remote-Ollama-Servers, der nur über einen Unternehmens-Proxy erreichbar ist).
   Diese Einstellung wirkt sich auch auf den HTTP-Zugriff von |Fess| insgesamt (z. B. Crawler) aus.

Modellauswahl-Leitfaden
========================

Richtlinien zur Modellauswahl je nach Verwendungszweck.

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Modell
     - Größe
     - Erforderlicher VRAM
     - Anwendungsfall
   * - ``phi3:3.8b``
     - Klein
     - 4GB+
     - Leichte Umgebung, einfache Frage-Antwort
   * - ``gemma4:e4b``
     - Klein-Mittel
     - 8GB+
     - Ausgewogener Allzweck, Thinking-Unterstützung (Standard)
   * - ``mistral:7b``
     - Mittel
     - 8GB+
     - Wenn hochwertige Antworten erforderlich sind
   * - ``llama3.3:70b``
     - Groß
     - 48GB+
     - Höchste Qualität, komplexe Schlussfolgerungen

GPU-Unterstützung
-----------------

Ollama unterstützt GPU-Beschleunigung. Mit NVIDIA-GPUs wird die Inferenzgeschwindigkeit erheblich verbessert.

::

    # GPU-Unterstützung prüfen
    ollama run gemma4:e4b --verbose

Fehlerbehebung
==============

Verbindungsfehler
-----------------

**Symptom**: Fehler in der Chat-Funktion, LLM als nicht verfügbar angezeigt

**Zu überprüfen**:

1. Überprüfen Sie, ob Ollama läuft::

    curl http://localhost:11434/api/tags

2. Überprüfen Sie, ob das Modell heruntergeladen ist::

    ollama list

3. Überprüfen Sie die Firewall-Einstellungen

4. Überprüfen Sie, ob das Plugin ``fess-llm-ollama`` in ``app/WEB-INF/plugin/`` vorhanden ist

Modell nicht gefunden
---------------------

**Symptom**: Log gibt „Configured model not found" aus

**Lösung**:

1. Überprüfen Sie, ob der Modellname korrekt ist (kann ``:latest``-Tag enthalten)::

    # Modellliste überprüfen
    ollama list

2. Laden Sie das benötigte Modell herunter::

    ollama pull gemma4:e4b

Timeout
-------

**Symptom**: Anfragen laufen in Timeout

**Lösung**:

1. Verlängern Sie die Timeout-Zeit::

    rag.llm.ollama.timeout=120000

2. Erwägen Sie ein kleineres Modell oder eine GPU-Umgebung

Debug-Einstellungen
-------------------

Zur Untersuchung von Problemen können Sie den Log-Level von |Fess| anpassen, um detaillierte Logs zu Ollama auszugeben.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Weiterführende Informationen
============================

- `Ollama offizielle Website <https://ollama.com/>`__
- `Ollama Modellbibliothek <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`rag-chat` - Details zur KI-Suchmodus-Funktion
