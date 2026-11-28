=============================================
Interne Dokumente per KI-Suche (RAG) befragen
=============================================

Einleitung
==========

Statt Suchergebnisse einzeln zu öffnen und miteinander zu vergleichen, möchte man oft einfach eine Frage stellen wie „Bis wann muss die Reisekostenabrechnung eingereicht werden?“ und eine Antwort erhalten, die auf internen Dokumenten beruht.
Der KI-Suchmodus von Fess (RAG-Chat) lässt Fess selbst nach Dokumenten suchen, die zur Frage passen, übergibt deren Inhalt an ein LLM (Large Language Model), das daraus eine Antwort erzeugt, und gibt diese zusammen mit Links auf die zugrunde gelegten Dokumente zurück.

Dieser Artikel zeigt, wie Sie den KI-Suchmodus unter Fess 15.9 in Betrieb nehmen, einschränken, wer ihn nutzen darf und auf welche Dokumente er sich stützt, und seine Funktion auf der Suchseite und über die API prüfen.
Nach den Schritten dieses Artikels können Sie Folgendes:

- Einen von vier LLM-Anbietern auswählen und das passende Plugin samt Einstellungen installieren
- Ein LLM mit den Overlay-Compose-Dateien von docker-fess an Fess unter Docker anbinden
- Einschränken, welche Benutzer den Chat verwenden dürfen und auf welche Dokumente sich die Antworten stützen
- Auf der Suchseite, über ``/api/v2/chat`` und im Suchprotokoll prüfen, ob alles funktioniert

Voraussetzung ist, dass Fess läuft und bereits Dokumente gecrawlt wurden.
Falls nicht, bereiten Sie dies mit den Schritten aus :doc:`guide-02` vor.
Die semantische Suche, die Dokumente mit ähnlicher Bedeutung findet, wird in :doc:`guide-18` behandelt, und MCP, mit dem KI-Agenten in Fess suchen können, in :doc:`guide-20`.

So funktioniert der KI-Suchmodus
================================

Der KI-Suchmodus verwendet keinen eigenen Vektorindex.
Er findet Dokumente mit derselben Suchverarbeitung wie die normale Suche (standardmäßig Stichwortsuche), daher können Sie ohne Embedding-Modell und ohne Chunking loslegen.
Ist die semantische Suche aktiviert, fließt sie automatisch auch in die Suchen des KI-Suchmodus ein.

Der Verarbeitungsablauf hängt vom aufgerufenen Endpunkt ab.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Endpunkt
     - Verarbeitungsablauf
   * - ``POST /api/v2/chat/stream`` (wird von der KI-Suche auf der Suchseite verwendet)
     - Absichtserkennung → Suche → Relevanzbewertung durch das LLM → Abruf des Dokumentinhalts → Erzeugung der Antwort. Der Fortschritt jeder Phase und die Teile der Antwort werden der Reihe nach als Server-Sent Events zurückgegeben
   * - ``POST /api/v2/chat``
     - Absichtserkennung → Suche → Erzeugung der Antwort. Es gibt keine Relevanzbewertung, und das Ergebnis wird als ein einziges JSON zurückgegeben

In beiden Fällen formuliert das LLM die Suchbegriffe neu und sucht erneut, wenn eine Suche keine Treffer liefert (standardmäßig bis zu 2 Mal, ``rag.chat.query.regeneration.max.count``).
Da für eine einzige Frage das LLM mehrmals aufgerufen wird, dauern Antworten länger als eine normale Suche, und bei einem Cloud-LLM wird jeder Aufruf berechnet.

An das LLM werden die Frage des Benutzers sowie der Inhalt oder Auszüge der bei der Suche gefundenen Dokumente gesendet.
Prüfen Sie bei der Wahl des Anbieters, wohin diese Daten gehen.

Gespräche werden über ``session_id`` identifiziert und im Speicher von Fess gehalten.
Standardmäßig wird ein Gespräch nach 30 Minuten ohne Aktivität verworfen (``rag.chat.session.timeout.minutes``), und pro Gespräch werden bis zu 30 Nachrichten aufbewahrt (``rag.chat.history.max.messages``).
Auch ein Neustart von Fess löscht die Gespräche.

Einen LLM-Anbieter wählen
=========================

In Fess 15.9 wird die Anbindung an ein LLM für jeden Anbieter durch ein eigenes ``fess-llm-*``-Plugin bereitgestellt.
Welcher Anbieter verwendet wird, legen Sie mit ``rag.llm.name`` fest.

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - Anbieter
     - ``rag.llm.name``
     - Plugin
     - Standardmodell
     - Für die Verbindung nötige Einstellungen und Ziel von Fragen und Dokumenten
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url`` (Standard ``http://localhost:11434``). Die Daten gehen an den Ollama-Server, den Sie selbst betreiben
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``. Die Daten gehen an OpenAI
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``. Die Daten gehen an Google
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region`` (Standard ``us-east-1``) sowie ``rag.llm.bedrock.api.key`` oder AWS-Anmeldedaten. Die Daten gehen an Amazon Bedrock in der angegebenen Region

Das Modell lässt sich mit ``rag.llm.<Anbieter>.model`` ändern.

Bei OpenAI und Gemini genügt ein API-Schlüssel für den Einstieg, allerdings werden Fragen und Dokumente an den jeweiligen Dienst gesendet.
Ollama hält Fragen und Dokumente auf Ihren eigenen Servern, benötigt aber einen Server, auf dem das Modell läuft.
Die Compose-Datei von docker-fess für Ollama setzt eine NVIDIA-GPU voraus.
Bedrock erfordert AWS-Anmeldedaten und die Angabe einer Region.
Zur Einrichtung siehe `Amazon Bedrock-Konfiguration <https://fess.codelibs.org/de/stable/config/llm-bedrock.html>`__.

Drei Dinge sind zu konfigurieren
================================

Der KI-Suchmodus funktioniert nur, wenn alle drei der folgenden Punkte erfüllt sind.

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Einstellung
     - Wo sie gesetzt wird
     - Übergabe unter Docker
   * - ``rag.chat.enabled=true`` (Standard ``false``)
     - ``fess_config.properties``. In der Administrationsoberfläche gibt es dafür kein Feld
     - ``-Dfess.config.rag.chat.enabled=true`` in ``FESS_JAVA_OPTS``
   * - Ein ``fess-llm-*``-Plugin
     - [System] > [Plugin] oder ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0`` usw.
   * - ``rag.llm.name`` und die Verbindungseinstellungen des jeweiligen Anbieters
     - ``rag.llm.name`` unter [System] > [Allgemein], die Verbindungseinstellungen (``rag.llm.<Anbieter>.*``) in ``fess_config.properties``
     - ``-Dfess.system.rag.llm.name=openai``, ``-Dfess.config.rag.llm.openai.api.key=...`` usw.

Der Standardwert von ``rag.llm.name`` ist ``ollama``.
Wenn Sie nur das OpenAI-Plugin installieren und ``rag.llm.name`` nicht ändern, sucht Fess fortwährend nach einem nicht vorhandenen Ollama-Client, und der KI-Suchmodus lässt sich nicht verwenden.
In diesem Fall erscheint im Log die Warnung ``[LLM] LlmClient not found. componentName=ollamaLlmClient``.

``-Dfess.system.rag.llm.name`` ist ein Anfangswert, der nur verwendet wird, wenn ``system.properties`` keinen Wert enthält.
Sobald ein unter [Allgemein] gespeicherter Wert in ``system.properties`` geschrieben ist, hat dieser Vorrang.

Unter Docker betreiben (OpenAI und Gemini)
==========================================

docker-fess stellt Overlay-Compose-Dateien zur Anbindung eines LLM bereit.
Laden Sie im Verzeichnis, in dem Sie in :doc:`guide-02` die Compose-Dateien abgelegt haben, die Datei für v15.9.0 herunter.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

Legen Sie den API-Schlüssel in einer Umgebungsvariablen der Shell ab und starten Sie mit Angabe der drei Dateien.

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` ergänzt ``fess01`` um die folgenden Umgebungsvariablen.
API-Schlüssel und Modellname werden aus ``OPENAI_API_KEY`` und ``OPENAI_MODEL`` der Shell übernommen (``gpt-5-mini``, falls nicht gesetzt), daher müssen Sie den Schlüssel nicht in die Datei schreiben.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

Die Plugins aus ``FESS_PLUGINS`` werden beim Start des Containers noch vor Fess installiert, ein separater Neustart ist daher nicht nötig.
Läuft ``fess01`` bereits, wird ``fess01`` durch diesen Befehl neu erstellt, und Einstellungen, die Sie unter [Allgemein] geändert haben, gehen zusammen mit dem Container verloren.
Geben Sie auch bei nachfolgenden Befehlen wie ``ps``, ``logs`` und ``down`` dieselben drei Dateien an.

Für Gemini laden Sie ``compose-gemini.yaml`` herunter, setzen ``GEMINI_API_KEY`` und geben die Datei auf dieselbe Weise als dritte Datei an.
Diese Datei setzt das Modell aus ``GEMINI_MODEL`` (``gemini-2.5-flash``, falls nicht gesetzt), daher wird statt des Standardmodells des Plugins ``gemini-2.5-flash`` verwendet.

.. note::

   Geben Sie zwei oder mehr Overlay-Dateien an, die ``FESS_JAVA_OPTS`` setzen (etwa in Kombination mit Einstellungen für OCR), wird nur der Wert aus der letzten Datei verwendet.
   Erstellen Sie in diesem Fall eine eigene Compose-Datei, die alle benötigten ``-D``-Optionen in einem einzigen ``FESS_JAVA_OPTS`` zusammenfasst.
   ``FESS_JAVA_OPTS`` wird an Leerzeichen aufgetrennt, daher lassen sich dort keine Optionen angeben, deren Wert Leerzeichen enthält.

Ein wie bei ``-Dfess.config.rag.llm.openai.api.key`` übergebener API-Schlüssel wird unter [Systeminformationen] > [Konfigurationsinformationen] maskiert angezeigt.
Wenn der Zugang nach außen über einen internen Proxy erfolgen muss, ergänzen Sie ``-Dfess.config.http.proxy.host=...`` und ``-Dfess.config.http.proxy.port=...``.
Die LLM-Plugins verwenden die gemeinsamen Proxy-Einstellungen von Fess.

Unter Docker betreiben (Ollama)
===============================

``compose-ollama.yaml`` fügt einen Ollama-Container ``ollama01`` hinzu und verbindet ``fess01`` mit ihm.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Ziel
     - Was gesetzt wird
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``, ``-Dfess.config.rag.chat.enabled=true``, ``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - Image ``ollama/ollama:latest``, Netzwerk ``search_net``, Port 11434, Volume ``ollama-data`` und Zuweisung einer NVIDIA-GPU

``rag.llm.name`` und das Modell werden nicht gesetzt, daher werden die Standardwerte ``ollama`` und ``gemma4:e4b`` verwendet.
Die URL zeigt auf ``ollama01``, weil das standardmäßige ``http://localhost:11434`` auf den Container ``fess01`` selbst verweisen würde.

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

Für diese Datei wird eine Umgebung mit installiertem NVIDIA Container Toolkit benötigt.
Um es in einer Umgebung ohne GPU auszuprobieren, löschen Sie in der heruntergeladenen Datei den Abschnitt ``deploy:`` von ``ollama01``.
Das Modell läuft dann auf der CPU, Antworten dauern also länger.

Fess betrachtet Ollama nur dann als verfügbar, wenn das konfigurierte Modell in der Modellliste von Ollama (``/api/tags``) enthalten ist, und prüft dies standardmäßig alle 60 Sekunden.
Deshalb steht der KI-Suchmodus etwa eine Minute nach dem Herunterladen des Modells zur Verfügung.
Die Kommentare am Anfang der Datei nennen einen anderen Dateinamen und Schritte zum Herunterladen von ``gpt-oss:20b``; folgen Sie jedoch den obigen Schritten.
Um ein anderes Modell zu verwenden, laden Sie es mit ``ollama pull`` herunter und ergänzen ``-Dfess.config.rag.llm.ollama.model=<Modellname>`` in ``FESS_JAVA_OPTS``.

Ohne Docker konfigurieren (ZIP, RPM und DEB)
============================================

1. Installieren Sie das Plugin. Wählen Sie es unter [System] > [Plugin] > [Installieren] aus oder installieren Sie es per Befehl

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. Fügen Sie die Einstellungen in ``fess_config.properties`` hinzu. Beim ZIP-Paket ist dies ``app/WEB-INF/classes/fess_config.properties``, bei den RPM/DEB-Paketen ``/etc/fess/fess_config.properties``

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. Starten Sie Fess neu. Sowohl das Plugin als auch die Änderungen an ``fess_config.properties`` werden beim Neustart geladen
4. Öffnen Sie [System] > [Allgemein], wählen Sie im Bereich „KI-Suche“ unter „LLM-Anbieter“ ``openai`` aus und klicken Sie auf [Aktualisieren]

Der Bereich „KI-Suche“ wird nur angezeigt, wenn ``rag.chat.enabled=true`` gesetzt und mindestens ein LLM-Plugin geladen ist.
Zur Auswahl unter „LLM-Anbieter“ stehen nur die Anbieter der installierten Plugins.
Wenn Sie den Bereich nicht finden, überprüfen Sie die Schritte 1 bis 3.

Funktion prüfen
===============

Auf der Suchseite prüfen
------------------------

1. Öffnen Sie ``http://localhost:8080/``. In der Navigationsleiste oben erscheint [KI-Suche] mit einem Robotersymbol
2. Klicken Sie auf [KI-Suche], um die Chat-Seite (``/chat``) zu öffnen
3. Geben Sie eine Frage ein, die sich aus den gecrawlten Dokumenten beantworten lässt. Wenn Sie in :doc:`guide-02` die Suchanleitung gecrawlt haben, können Sie es etwa mit „Welche Zeichen kann ich bei der Wildcard-Suche verwenden?“ versuchen

Während die Antwort erzeugt wird, werden die Phasen Analyse, Suche, Bewertung, Abruf und Antwort nacheinander angezeigt.
Unter der Antwort werden die zugrunde gelegten Dokumente nummeriert unter „Quellen“ aufgeführt; die Nummern entsprechen Verweisen wie ``[1]`` im Antworttext.
Wenn Sie das Thema wechseln, klicken Sie auf [Neuer Chat]; dadurch wird der Gesprächsverlauf gelöscht.

Wird [KI-Suche] nicht angezeigt, sehen Sie unten unter „Häufige Stolperfallen“ nach.

Über die API prüfen
-------------------

Um ohne die Oberfläche zu prüfen, rufen Sie ``/api/v2/ui/config`` auf.
Ist ``response.features.rag_chat_enabled`` gleich ``true``, kann dieser Benutzer den KI-Suchmodus verwenden.

Zustandsändernde Anfragen wie ``/api/v2/chat`` müssen ein an die Sitzung gebundenes CSRF-Token im Header ``X-Fess-CSRF-Token`` senden.
Die Antwort von ``/api/v2/ui/config`` enthält das Token; rufen Sie es also unter Speicherung der Cookies ab und senden Sie die Anfrage mit denselben Cookies (das Beispiel verwendet ``jq``).

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"Welche Zeichen kann ich bei der Wildcard-Suche verwenden?"}' | jq '.response'

In der Antwort ist ``content`` die Antwort, ``sources`` die zugrunde gelegten Dokumente (``rank``, ``title``, ``url`` usw.) und ``session_id`` die ID des Gesprächs.
Für eine Folgefrage senden Sie die ``session_id`` zurück, etwa als ``{"message":"...","session_id":"<vorherige session_id>"}``.

Dieses Beispiel ruft die API als anonymer, nicht angemeldeter Benutzer auf, daher werden nur Dokumente mit ``{role}guest`` durchsucht.
Wie Sie die API als angemeldeter Benutzer aufrufen, welche Ereignisse die Streaming-Variante ``/api/v2/chat/stream`` liefert und welche Fehlercodes es gibt, entnehmen Sie `Chat-API <https://fess.codelibs.org/de/stable/api/api-chat.html>`__ und `API-Übersicht <https://fess.codelibs.org/de/stable/api/api-overview.html>`__.
``/api/v1/chat`` ist eine API im alten Format, die nur verfügbar ist, wenn das Plugin ``fess-webapp-v1-api`` installiert ist.
Verwenden Sie für neue Integrationen ``/api/v2/chat``.

In der Administrationsoberfläche und in den Logs prüfen
-------------------------------------------------------

Der Reiter [KI-Chat] unter [Systeminformationen] > [Suchprotokoll] zeigt die Anzahl der Anfragen, die Anzahl der Benutzer, die Gesamtzahl der Tokens, die durchschnittliche Antwortzeit und die Fehlerquote sowie die Anzahl je Benutzer, je Absicht und je Modell.
Diese Protokollierung ist über ``rag.chat.log.enabled`` (Standard ``true``) aktiviert; der Text von Fragen und Antworten wird nicht aufgezeichnet.
Tokenzahlen werden nur aufgezeichnet, wenn das LLM-Plugin sie meldet.

Unter Docker können Sie im Container-Log prüfen, ob das Plugin installiert wurde.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

Erscheint ``Installing fess-llm-openai-15.9.0.jar``, ist das Plugin installiert.
Erscheint danach fortlaufend ``[LLM] LlmClient not found``, passen ``rag.llm.name`` und das installierte Plugin nicht zusammen.

Benutzer und herangezogene Dokumente einschränken
=================================================

Die Suchen des KI-Suchmodus werden wie die normale Suche nach Rollen gefiltert.
Dokumente, die ein Benutzer in den Suchergebnissen nicht sehen kann, werden weder als Grundlage einer Antwort noch als Quelle verwendet.
Welche Dokumente wer sehen darf, bestimmen die „Berechtigungen“ der Crawl-Konfiguration.
Zum Konzept siehe :doc:`guide-05`.

Darüber hinaus können Sie im Bereich „KI-Suche“ unter [System] > [Allgemein] einschränken, wer den Chat selbst nutzen darf.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Feld
     - Beschreibung
   * - „Chat-Berechtigungen“ (``rag.chat.permissions``)
     - Legt die Benutzer, die den Chat verwenden dürfen, als kommagetrennte Liste fest, etwa ``{role}rag_user,{group}sales,{user}taro``. Ist das Feld leer, darf jeder den Chat verwenden. Sollen auch nicht angemeldete Benutzer ihn nutzen können, nehmen Sie ``{role}guest`` auf
   * - „Chat-Labels“ (``rag.chat.labels``)
     - Beschränkt die Dokumente, auf die sich Antworten stützen, auf solche mit einem der angegebenen Labelwerte. Geben Sie sie als kommagetrennte Liste an, etwa ``faq,policy``; ist das Feld leer, werden alle Dokumente herangezogen, die der Benutzer sehen kann

Benutzer, die nicht unter die „Chat-Berechtigungen“ fallen, sehen [KI-Suche] nicht, und die API gibt 401 zurück, wenn sie nicht angemeldet sind, bzw. 403, wenn sie angemeldet sind.
Angemeldete Benutzer haben nicht ``{role}guest``; geben Sie also nur ``{role}guest`` an, können angemeldete Benutzer den Chat nicht mehr verwenden.
Speichern Sie einen Wert ohne gültigen Eintrag (etwa nur ``{role}``), kann niemand den Chat verwenden.

„Chat-Labels“ eignet sich, wenn Antworten nur aus Dokumenten stammen sollen, die Sie als verlässliche Grundlage betrachten, etwa interne Richtlinien und FAQs, und die Sie zuvor mit einem Label versehen haben.
Wie Sie Labels anlegen und zuweisen, erfahren Sie in :doc:`guide-04`.

Häufige Stolperfallen
=====================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Symptom
     - Was zu prüfen ist
   * - [KI-Suche] wird nicht angezeigt
     - Prüfen Sie in dieser Reihenfolge: (1) Wird ``rag.chat.enabled=true`` übergeben? (2) Ist das Plugin installiert (``Installing`` im Log)? (3) Passt ``rag.llm.name`` zum installierten Plugin (Warnung ``LlmClient not found``)? (4) Ist der API-Schlüssel nicht leer bzw. wurde bei Ollama das Modell heruntergeladen? (5) Sind Sie selbst von den „Chat-Berechtigungen“ ausgeschlossen?
   * - Unter [Allgemein] fehlt der Bereich „KI-Suche“
     - Entweder steht ``rag.chat.enabled`` noch auf ``false``, oder es ist kein LLM-Plugin geladen. Prüfen Sie, ob Sie Fess nach dem Setzen der Einstellung und der Installation des Plugins neu gestartet haben
   * - Nach ``down`` und ``up -d`` ist „LLM-Anbieter“ wieder auf dem alten Wert
     - Die Werte unter [Allgemein] werden in ``system.properties`` im Container ``fess01`` gespeichert und gehen verloren, wenn der Container neu erstellt wird. Legen Sie den Wert mit ``-Dfess.system.rag.llm.name`` in ``FESS_JAVA_OPTS`` fest
   * - Die API gibt ``403`` zurück
     - Prüfen Sie, ob Sie das CSRF-Token in ``X-Fess-CSRF-Token`` senden und ob Sie die Cookies vom Abruf des Tokens mitsenden. Auch ein angemeldeter Benutzer, der von den „Chat-Berechtigungen“ ausgeschlossen ist, erhält 403
   * - Die API gibt ``429`` zurück
     - Pro Benutzer sind höchstens 30 Anfragen pro Minute erlaubt (``api.chat.rate.limit.per.user.per.minute``)
   * - Keine Verbindung zu einem Cloud-LLM
     - Prüfen Sie, ob der Container nach außen kommunizieren kann, und setzen Sie bei Bedarf eines Proxys ``http.proxy.host`` und ``http.proxy.port``

Um die Qualität der Antworten zu verbessern, prüfen Sie zunächst die Qualität der Suche.
Der KI-Suchmodus stützt sich auf die bei einer normalen Suche am höchsten eingestuften Dokumente (standardmäßig 5, ``rag.chat.context.max.documents``); liefert eine Suche mit den Wörtern der Frage oben unpassende Dokumente, wird auch die Antwort davon beeinflusst.
Die Verbesserung der Suche wird in :doc:`guide-08` behandelt.
Zu Temperatur und maximaler Tokenzahl je Prompt-Typ sowie zum Austausch von Prompts siehe `Übersicht über KI-Suchmodus (RAG) und LLM-Integration <https://fess.codelibs.org/de/stable/config/llm-overview.html>`__.

Weiterführende Artikel
======================

- Dokumente mit ähnlicher Bedeutung in die Suchergebnisse aufnehmen, auch wenn die Stichwörter nicht übereinstimmen: :doc:`guide-18`
- KI-Agenten wie Claude in Fess suchen lassen: :doc:`guide-20`
- Durchsuchbare Dokumente nach Abteilung oder Rolle trennen: :doc:`guide-05`
- Die Suchqualität anhand des Suchprotokolls verbessern: :doc:`guide-08`
- Benutzer per SSO anmelden und jedem Benutzer andere Dokumente zeigen: :doc:`guide-15`

Referenzen
==========

- `AI-Suchmodus-Funktion konfigurieren <https://fess.codelibs.org/de/stable/config/rag-chat.html>`__
- `Übersicht über KI-Suchmodus (RAG) und LLM-Integration <https://fess.codelibs.org/de/stable/config/llm-overview.html>`__
- `Ollama-Konfiguration <https://fess.codelibs.org/de/stable/config/llm-ollama.html>`__
- `OpenAI-Konfiguration <https://fess.codelibs.org/de/stable/config/llm-openai.html>`__
- `Google Gemini-Konfiguration <https://fess.codelibs.org/de/stable/config/llm-gemini.html>`__
- `Amazon Bedrock-Konfiguration <https://fess.codelibs.org/de/stable/config/llm-bedrock.html>`__
- `Chat-API <https://fess.codelibs.org/de/stable/api/api-chat.html>`__
- `KI-Suchmodus (für Benutzer) <https://fess.codelibs.org/de/stable/user/chat-search.html>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `compose-Verzeichnis von docker-fess (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
