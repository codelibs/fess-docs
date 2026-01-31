==========================
Ollama-Konfiguration
==========================

Übersicht
=========

Ollama ist eine Open-Source-Plattform zur Ausführung großer Sprachmodelle (LLM) in lokalen Umgebungen.
Es ist als Standard-LLM-Anbieter in |Fess| konfiguriert und eignet sich für den Einsatz in privaten Umgebungen.

Durch die Verwendung von Ollama können Sie die KI-Chat-Funktion nutzen, ohne Daten extern zu senden.

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
- ``gemma3:4b`` - Gemma 3 von Google (4B Parameter, Standard)
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

    # Standardmodell (Gemma 3 4B) herunterladen
    ollama pull gemma3:4b

    # Llama 3.3 herunterladen
    ollama pull llama3.3:70b

    # Modell testen
    ollama run gemma3:4b "Hello, how are you?"

Grundeinstellungen
==================

Fügen Sie die folgenden Einstellungen zu ``app/WEB-INF/conf/system.properties`` hinzu.

Minimalkonfiguration
--------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter auf Ollama setzen
    rag.llm.type=ollama

    # Ollama-URL (lokale Umgebung)
    rag.llm.ollama.api.url=http://localhost:11434

    # Zu verwendendes Modell
    rag.llm.ollama.model=gemma3:4b

Empfohlene Konfiguration (Produktionsumgebung)
----------------------------------------------

::

    # AI-Modus-Funktion aktivieren
    rag.chat.enabled=true

    # LLM-Anbieter-Einstellungen
    rag.llm.type=ollama

    # Ollama-URL
    rag.llm.ollama.api.url=http://localhost:11434

    # Modelleinstellungen (großes Modell verwenden)
    rag.llm.ollama.model=llama3.3:70b

    # Timeout-Einstellungen (für große Modelle erhöht)
    rag.llm.ollama.timeout=120000

Einstellungselemente
====================

Alle verfügbaren Einstellungselemente für den Ollama-Client.

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
     - ``gemma3:4b``
   * - ``rag.llm.ollama.timeout``
     - Anfrage-Timeout (Millisekunden)
     - ``60000``

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
        image: codelibs/fess:15.5.0
        environment:
          - RAG_CHAT_ENABLED=true
          - RAG_LLM_TYPE=ollama
          - RAG_LLM_OLLAMA_API_URL=http://ollama:11434
          - RAG_LLM_OLLAMA_MODEL=gemma3:4b
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

Modellauswahl-Leitfaden
=======================

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
   * - ``gemma3:4b``
     - Klein-Mittel
     - 6GB+
     - Ausgewogener Allzweck (Standard)
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
    ollama run gemma3:4b --verbose

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

Modell nicht gefunden
---------------------

**Symptom**: Log zeigt "Configured model not found in Ollama"

**Lösung**:

1. Überprüfen Sie, ob der Modellname korrekt ist (kann ``:latest``-Tag enthalten)::

    # Modellliste überprüfen
    ollama list

2. Laden Sie das benötigte Modell herunter::

    ollama pull gemma3:4b

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
- :doc:`rag-chat` - Details zur AI-Modus-Funktion
