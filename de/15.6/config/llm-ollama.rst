==========================
Ollama-Konfiguration
==========================

Übersicht
=========

Ollama ist eine Open-Source-Plattform zur Ausführung großer Sprachmodelle (LLM) in lokalen Umgebungen.
In |Fess| 15.6 wird die Ollama-Integrationsfunktion als Plugin ``fess-llm-ollama`` bereitgestellt und eignet sich für den Einsatz in privaten Umgebungen.

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

In |Fess| 15.6 wurde die Ollama-Integrationsfunktion als Plugin ausgelagert.
Zur Verwendung von Ollama ist die Installation des ``fess-llm-ollama``-Plugins erforderlich.

1. Laden Sie `fess-llm-ollama-15.6.0.jar` herunter.
2. Legen Sie die Datei im Verzeichnis ``app/WEB-INF/plugin/`` im |Fess|-Installationsverzeichnis ab.

::

    cp fess-llm-ollama-15.6.0.jar /path/to/fess/app/WEB-INF/plugin/

3. Starten Sie |Fess| neu.

.. note::
   Die Plugin-Version muss mit der Version von |Fess| übereinstimmen.

Grundeinstellungen
==================

In |Fess| 15.6 sind die LLM-bezogenen Einstellungen auf mehrere Konfigurationsdateien aufgeteilt.

Minimalkonfiguration
--------------------

``app/WEB-INF/conf/fess_config.properties``:

::

    # AI-Suchmodus-Funktion aktivieren
    rag.chat.enabled=true

    # Ollama-URL (lokale Umgebung)
    rag.llm.ollama.api.url=http://localhost:11434

    # Zu verwendendes Modell
    rag.llm.ollama.model=gemma4:e4b

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    # LLM-Anbieter auf Ollama setzen
    rag.llm.name=ollama

.. note::
   Die LLM-Anbietereinstellung kann auch über die Administrationsoberfläche (Administration > System > Allgemein) durch Setzen von ``rag.llm.name`` konfiguriert werden.

Empfohlene Konfiguration (Produktionsumgebung)
----------------------------------------------

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

``system.properties``:

::

    # LLM-Anbieter-Einstellungen
    rag.llm.name=ollama

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den Ollama-Client. Alle Einstellungen werden in ``fess_config.properties`` vorgenommen.

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
     - Intervall der Verfügbarkeitsprüfung (Sekunden)
     - ``60``
   * - ``rag.llm.ollama.max.concurrent.requests``
     - Maximale Anzahl gleichzeitiger Anfragen
     - ``5``
   * - ``rag.llm.ollama.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl relevanter Dokumente bei der Bewertung
     - ``3``

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
- ``rag.llm.ollama.{promptType}.max.tokens`` - Maximale Token-Anzahl
- ``rag.llm.ollama.{promptType}.context.max.chars`` - Maximale Zeichenzahl des Kontexts

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

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.ollama.top.p``
     - Wert für Top-P-Sampling (0.0-1.0)
     - (nicht gesetzt)
   * - ``rag.llm.ollama.top.k``
     - Wert für Top-K-Sampling
     - (nicht gesetzt)
   * - ``rag.llm.ollama.num.ctx``
     - Kontextfenstergröße
     - (nicht gesetzt)
   * - ``rag.llm.ollama.default.*``
     - Standard-Fallback-Einstellungen
     - (nicht gesetzt)
   * - ``rag.llm.ollama.options.*``
     - Globale Optionen
     - (nicht gesetzt)

Konfigurationsbeispiel::

    # Top-P-Sampling
    rag.llm.ollama.top.p=0.9

    # Top-K-Sampling
    rag.llm.ollama.top.k=40

    # Kontextfenstergröße
    rag.llm.ollama.num.ctx=4096

Unterstützung für Thinking-Modelle
====================================

Bei Verwendung von Thinking-Modellen wie gemma4 oder qwen3.5 unterstützt |Fess| die Konfiguration des Thinking-Budgets.

Folgendes in ``fess_config.properties`` eintragen:

::

    # Thinking-Budget konfigurieren
    rag.llm.ollama.thinking.budget=1024

Durch Konfiguration des Thinking-Budgets kann die Anzahl der Token gesteuert werden, die dem Modell für den "Denkschritt" vor der Antwortgenerierung zur Verfügung stehen.

Netzwerkkonfiguration
=====================

Docker-Konfiguration
--------------------

Beispielkonfiguration, wenn sowohl |Fess| als auch Ollama in Docker laufen.

``docker-compose.yml``:

::

    version: '3'
    services:
      fess:
        image: codelibs/fess:15.6.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_NAME=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma4:e4b
        depends_on:
          - ollama
        # ... weitere Einstellungen

      ollama:
        image: ollama/ollama
        volumes:
          - ollama_data:/root/.ollama
        ports:
          - "11434:11434"

    volumes:
      ollama_data:

.. note::
   In Docker Compose-Umgebungen verwenden Sie ``ollama`` als Hostnamen (nicht ``localhost``).

Remote Ollama-Server
--------------------

Wenn Ollama auf einem separaten Server als Fess läuft:

::

    rag.llm.ollama.api.url=http://ollama-server.example.com:11434

.. warning::
   Ollama hat standardmäßig keine Authentifizierungsfunktion. Bei externem Zugriff sollten Sie Sicherheitsmaßnahmen auf Netzwerkebene (Firewall, VPN usw.) in Betracht ziehen.

HTTP-Proxy verwenden
====================

Seit |Fess| 15.6.1 nutzt der Ollama-Client die globale HTTP-Proxy-Konfiguration von |Fess|. Wenn die Verbindung zum Ollama-Server über einen Proxy erfolgen muss (z. B. bei Verwendung eines Remote-Ollama-Servers), geben Sie die folgenden Eigenschaften in ``fess_config.properties`` an.

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

**Symptom**: Log zeigt "Configured model not found in Ollama"

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

Zur Untersuchung von Problemen können Sie den Log-Level anpassen, um detaillierte Logs zu Ollama auszugeben.

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.llm.ollama" level="DEBUG"/>

Weiterführende Informationen
============================

- `Ollama offizielle Website <https://ollama.com/>`__
- `Ollama Modellbibliothek <https://ollama.com/library>`__
- `Ollama GitHub <https://github.com/ollama/ollama>`__
- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`rag-chat` - Details zur AI-Suchmodus-Funktion
