=======================================
Fess per MCP aus KI-Agenten durchsuchen
=======================================

Einleitung
==========

Wenn ein KI-Agent wie Claude Code interne Dokumente recherchieren soll, kann er die indexierten Dokumente direkt als Belege verwenden, sofern er die Fess-Suche selbst aufrufen kann.
Der Mechanismus dafür ist MCP (Model Context Protocol).
In Fess fügt das Plugin ``fess-webapp-mcp`` unter ``/mcp`` einen MCP-Server-Endpunkt hinzu.

Dieser Artikel beschreibt, wie Sie das Plugin in Fess 15.9 installieren, die Authentifizierung verpflichtend machen, sich aus einem KI-Agenten verbinden und die Funktion überprüfen.

Nach den Schritten dieses Artikels ist Folgendes erreicht:

- Sie können mit ``curl`` prüfen, dass ``/mcp`` funktioniert
- Aufrufe ohne Zugriffstoken werden abgelehnt
- Welche Dokumente der Agent durchsuchen kann, legen Sie über die Berechtigungen des Tokens fest
- Claude Code kann das Fess-Werkzeug ``search`` aufrufen

.. note::

   Die Aufrufrichtung ist umgekehrt zum KI-Suchmodus aus :doc:`guide-19`.
   Im KI-Suchmodus ruft Fess ein LLM (Ollama, OpenAI usw.) auf, um Antworten zu erzeugen. Ollama ist dabei die Laufzeitumgebung für das LLM, kein MCP-Client.
   Bei MCP ruft ein externer KI-Agent Fess als Suchwerkzeug auf, und die Antwort erzeugt das LLM auf der Seite des Agenten.

Was ``/mcp`` bereitstellt
=========================

``/mcp`` akzeptiert nur ``POST`` und gibt pro Anfrage genau ein JSON zurück (es werden keine Sitzungen gehalten).
Suchen durchlaufen dieselbe Verarbeitung wie die Suchseite, sodass die rollenbasierte Filterung der Suchergebnisse unverändert greift.

Das Plugin in Version 15.9.0 stellt Folgendes bereit.
Alles ist schreibgeschützt; nichts davon verändert Daten in Fess.

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - Name
     - Inhalt
     - Verfügbarkeit
   * - ``search`` (Werkzeug)
     - Volltextsuche. Jeder Treffer enthält eine ``doc_id``
     - Immer verfügbar
   * - ``suggest`` (Werkzeug)
     - Vorschläge zu einem teilweise eingegebenen Begriff
     - Immer verfügbar
   * - ``get_document`` (Werkzeug)
     - Ruft den Text eines Dokuments anhand der ``doc_id`` ab
     - Immer verfügbar
   * - ``get_index_stats`` (Werkzeug)
     - Indexname, Anzahl der Dokumente und JVM-Speicherauslastung
     - In der Standardkonfiguration nicht verfügbar (siehe unten)
   * - ``fess://document/{doc_id}`` (Ressource)
     - Führt denselben Abruf wie ``get_document`` als Ressource aus
     - Immer verfügbar
   * - ``fess://index/stats`` (Ressource)
     - Derselbe Inhalt wie ``get_index_stats``
     - Wie ``get_index_stats``
   * - ``basic_search`` / ``advanced_search`` (Prompt)
     - Prompt-Vorlagen für die Suche. ``advanced_search`` nimmt zusätzlich ``sort`` und ``num`` entgegen
     - Immer verfügbar

Wenn Sie bei ``search`` den Parameter ``num`` weglassen, werden nur 3 Treffer zurückgegeben (der Standardwert von ``mcp.default.page.size``).
Sowohl die Auszüge von ``search`` als auch der Text von ``get_document`` werden auf höchstens 10000 Zeichen gekürzt; bei ``get_document`` wird dann ``truncated`` auf ``true`` gesetzt (``mcp.content.max.length``).

Das Plugin installieren
=======================

Die Plugin-Version richtet sich nach der Minor-Version von Fess.
Für Fess 15.9 verwenden Sie ``fess-webapp-mcp`` 15.9.x.
Installieren Sie es auf einem der folgenden Wege und starten Sie Fess danach neu.

- Administrationsoberfläche: Klicken Sie unter [System] > [Plugin] auf [Installieren], wählen Sie auf der Registerkarte [Remote] ``fess-webapp-mcp`` aus und installieren Sie es
- Kommandozeile: ``bin/fess-setup install plugin fess-webapp-mcp:15.9.0``
- Docker: Fügen Sie ``FESS_PLUGINS`` zu ``environment`` von ``fess01`` in ``compose.yaml`` hinzu. Das Docker-Image enthält dieses Plugin nicht

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"

Ist in der Docker-Version der Name oder die Version falsch angegeben, wird das Plugin übersprungen und der Container startet trotzdem.
Prüfen Sie nach dem Hinzufügen im Startprotokoll, ob das Plugin heruntergeladen wurde.

.. warning::

   Ersetzen Sie bei einem Upgrade von Fess auch dieses Plugin durch die neue Version, bevor Sie Fess starten.
   Bleibt die jar-Datei einer alten Plugin-Version (z. B. für 15.8) in ``WEB-INF/plugin`` liegen, schlägt die Initialisierung von Fess 15.9 beim Start fehl, und nicht nur ``/mcp``, sondern alle Seiten und APIs liefern 404.
   Auf der Kommandozeile können Sie die Plugins mit ``bin/fess-setup upgrade plugins`` ersetzen.

Erscheint nach dem Neustart in der Protokolldatei ``fess.log`` die folgende WARN-Meldung, ist der Endpunkt aktiv.

::

    [MCP] mcp.auth.mode=none - every /mcp caller is treated as anonymous. Set mcp.auth.mode=fess_token, ...

Diese Meldung zeigt, dass der Endpunkt ohne Authentifizierung läuft, wie im nächsten Abschnitt beschrieben.

Zunächst ohne Authentifizierung testen
======================================

.. warning::

   Direkt nach der Installation läuft ``/mcp`` ohne Authentifizierung (``mcp.auth.mode=none``).
   Jeder, der ``/mcp`` erreicht, kann mit denselben Rechten wie ein nicht angemeldeter Benutzer (Gast) suchen und mit ``get_document`` sogar den Text von Dokumenten abrufen.
   Betroffen sind alle Dokumente aus Crawl-Konfigurationen, deren Berechtigungen auf dem Standardwert ``{role}guest`` belassen wurden.
   Beschränken Sie Tests in diesem Zustand auf Ihre lokale Umgebung und machen Sie die Authentifizierung wie im nächsten Abschnitt beschrieben verpflichtend.
   Ist unter [System] > [Allgemein] „Anmeldung erforderlich“ aktiviert, lehnt ``/mcp`` in diesem Zustand jeden Aufruf mit HTTP 403 ab. Fahren Sie in diesem Fall mit dem nächsten Abschnitt fort.

Angenommen, Fess läuft unter ``http://localhost:8080``. Rufen Sie ``server/discover`` auf.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: server/discover' \
        -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

Der Aufruf war erfolgreich, wenn ``result.supportedVersions`` in der Antwort ``2026-07-28`` und ``result.capabilities`` unter anderem ``tools`` enthält.

Rufen Sie anschließend das Werkzeug ``search`` auf.
Geben Sie in ``q`` ein Wort an, das in Ihren gecrawlten Dokumenten vorkommt.

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: tools/call' \
        -H 'Mcp-Name: search' \
        -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"q":"Fess","num":5},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

Die Suchergebnisse stehen in ``result.structuredContent.hits``, die Trefferzahl in ``total``.
Die Header-Werte müssen mit dem Anfragetext übereinstimmen.
``MCP-Protocol-Version`` muss der Version in ``params._meta`` entsprechen, ``Mcp-Method`` dem Wert von ``method`` und ``Mcp-Name`` dem Werkzeugnamen.
Weichen sie ab, ist das Ergebnis HTTP 400 (Fehlercode ``-32020``).

Authentifizierung verpflichtend machen
======================================

Wechseln Sie in den Modus ``fess_token``, der mit Fess-Zugriffstokens authentifiziert.
Daneben gibt es den Modus ``oauth``, der mit JWTs eines externen Autorisierungsservers authentifiziert.
Die Konfiguration dafür finden Sie im Abschnitt „OAuth 2.1 reference“ der README.

Ein Zugriffstoken erstellen
---------------------------

1. Öffnen Sie in der Administrationsoberfläche [System] > [Zugriffstoken] und klicken Sie auf [Neu erstellen]
2. Geben Sie unter „Name“ einen Namen ein, der den Zweck erkennen lässt, z. B. ``mcp-agent``
3. Geben Sie unter „Berechtigungen“ die Rollen der Dokumente ein, die der Agent sehen darf, eine pro Zeile. Genügen Dokumente für Gäste, ist das ``{role}guest`` (wie Sie die Werte wählen, erklärt „Token-Berechtigungen und Suchergebnisse“)
4. Legen Sie bei Bedarf „Läuft ab“ fest und klicken Sie auf [Erstellen]
5. Klicken Sie in der Liste auf den Namen des erstellten Tokens; auf der Detailseite wird der Wert unter „Token“ angezeigt

mcp.auth.mode einstellen
------------------------

Alle ``mcp.*``-Einstellungen werden aus den Systemeigenschaften von Fess (``system.properties``) gelesen.
Einträge in ``fess_config.properties`` oder als ``-Dfess.config.*`` werden ignoriert, ohne Fehler und ohne Protokollmeldung.

Fügen Sie bei der ZIP-Version in ``app/WEB-INF/conf/system.properties``, bei den RPM/DEB-Versionen in ``/etc/fess/system.properties`` die folgende Zeile hinzu.

::

    mcp.auth.mode=fess_token

Der Wert wird zur Laufzeit neu eingelesen und wirkt daher nach wenigen Sekunden; ein Neustart ist nicht nötig.

Der Container ``fess01`` der Docker-Version hat kein Volume; Einstellungen in Dateien innerhalb des Containers gehen verloren, wenn der Container neu erstellt wird.
Geben Sie die Einstellung in ``FESS_JAVA_OPTS`` in ``compose.yaml`` mit dem Präfix ``-Dfess.system.`` an (nicht ``fess.config.``).

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"
      - "FESS_JAVA_OPTS=-Dfess.system.mcp.auth.mode=fess_token"

``FESS_PLUGINS`` und ``FESS_JAVA_OPTS`` werden wirksam, wenn der Container neu erstellt wird.
Führen Sie nach dem Bearbeiten von ``compose.yaml`` den folgenden Befehl aus.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Ist derselbe Schlüssel in ``system.properties`` vorhanden, hat dieser Vorrang.

Prüfen, ob die Authentifizierung greift
---------------------------------------

Führen Sie den ``server/discover``-Aufruf aus dem vorigen Abschnitt unverändert erneut aus.
Da kein Token angehängt ist, kommt HTTP 401 mit dem Header ``WWW-Authenticate: Bearer realm="fess-mcp"`` zurück (mit ``curl -i`` werden die Header angezeigt).
Im Modus ``fess_token`` erfordert auch ``server/discover`` eine Authentifizierung.

Führen Sie dann den ``search``-Aufruf mit ``curl`` aus dem vorigen Abschnitt mit zusätzlichem ``-H 'Authorization: Bearer <Token>'`` aus.
Ersetzen Sie ``<Token>`` durch den auf der Detailseite angezeigten Wert.
Werden Suchergebnisse zurückgegeben, ist die Einrichtung abgeschlossen.
Ein nicht vorhandenes oder abgelaufenes Token führt zu HTTP 401.

Token-Berechtigungen und Suchergebnisse
=======================================

Im Modus ``fess_token`` werden die Berechtigungen des Tokens unverändert als Rollen für die Suche verwendet.
Nicht nur ``search``, sondern auch ``get_document`` wird mit denselben Rollen gefiltert; Dokumente ohne passende Berechtigung lassen sich daher auch mit bekannter ``doc_id`` nicht abrufen.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Berechtigungen des Tokens
     - Durchsuchbare Dokumente
   * - Leer
     - Wie ein Gast (Dokumente mit ``{role}guest``)
   * - ``{role}guest``
     - Wie ein Gast
   * - ``{role}sales``
     - Nur Dokumente mit ``{role}sales``. Dokumente für Gäste sind nicht enthalten
   * - ``{role}sales`` und ``{role}guest``
     - Dokumente beider Rollen

Die Gastrolle wird nur bei Tokens mit leeren Berechtigungen ergänzt.
Soll der Agent sowohl Abteilungsdokumente als auch Dokumente für alle durchsuchen, geben Sie zusätzlich ``{role}guest`` an.
Wie Rollen und Berechtigungen zusammenhängen, erklärt :doc:`guide-05`.

Zur Überprüfung führen Sie ``search`` für dasselbe Wort mit zwei Tokens unterschiedlicher Berechtigungen aus und vergleichen ``total``.

.. warning::

   Weisen Sie einem Token für Agenten nicht ``{role}admin-api`` zu.
   Ein Token mit ``{role}admin-api`` kann die gesamte Admin API von Fess aufrufen.
   Zudem liefert ``search`` mit einem Token, das nur ``{role}admin-api`` besitzt, 0 Treffer, da kein Dokument diese Rolle hat.

``get_index_stats`` verfügbar machen
------------------------------------

``get_index_stats`` und ``fess://index/stats`` werden nur Aufrufern angezeigt, die eine der in ``mcp.tools.index_stats.permissions`` aufgeführten Berechtigungen besitzen.
Der Standardwert ist ``Radmin-api`` (die interne Schreibweise von ``{role}admin-api``); im Modus ``none`` hat kein Aufrufer Berechtigungen, sodass sie niemandem angezeigt werden.
Aufrufer ohne Berechtigung erhalten denselben Fehler wie bei einem nicht existierenden Werkzeug.

Für die reine Suche wird dieses Werkzeug nicht benötigt.
Wenn Sie es verwenden, legen Sie statt ``{role}admin-api`` eine eigene Rolle fest und fügen Sie diese den Berechtigungen des Tokens hinzu.
In ``system.properties`` schreiben Sie die interne Schreibweise (``R`` für ``{role}``).

::

    mcp.tools.index_stats.permissions=Rmcp-stats

In diesem Beispiel fügen Sie den Berechtigungen des Tokens ``{role}mcp-stats`` hinzu.

Weitere Einstellungen
=====================

Alle folgenden Einstellungen gehören in ``system.properties`` (in der Docker-Version ``-Dfess.system.<Schlüssel>``).
Bei booleschen Werten gilt nur ``true`` als wahr; ``1`` oder ``yes`` gelten als falsch.

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - Schlüssel
     - Standardwert
     - Inhalt
   * - ``mcp.allowed.origins``
     - (leer)
     - Für Aufrufe aus dem Browser die zulässigen ``Origin``-Werte in der Form ``https://app.example.com``, kommagetrennt. Ist der Wert leer, werden alle Anfragen mit ``Origin``-Header mit HTTP 403 abgelehnt. ``curl`` und CLI-Agenten senden kein ``Origin`` und sind daher nicht betroffen
   * - ``mcp.rate.limit.per.minute``
     - ``60``
     - Obergrenze pro Minute für ``tools/call`` und ähnliche Aufrufe je Aufrufer (Token, sonst IP-Adresse). Bei Überschreitung werden HTTP 429 und ``Retry-After`` zurückgegeben. ``0`` deaktiviert die Grenze
   * - ``mcp.content.max.length``
     - ``10000``
     - Maximale Zeichenzahl des Textes, den ``search`` und ``get_document`` zurückgeben
   * - ``mcp.default.page.size``
     - ``3``
     - Anzahl der Treffer, wenn bei ``search`` ``num`` weggelassen wird
   * - ``mcp.enabled``
     - ``true``
     - Bei ``false`` gibt ``/mcp`` immer HTTP 503 zurück
   * - ``mcp.legacy.protocol.enabled``
     - ``true``
     - Akzeptiert auch ältere Clients (``2025-11-25`` / ``2025-06-18``), die sich mit ``initialize`` verbinden

Die folgenden zwei Einstellungen gehören im Gegensatz zu ``mcp.*`` in die ``fess_config.properties`` von Fess (in der Docker-Version ``-Dfess.config.<Schlüssel>``).

- Laufen Aufrufe über einen Reverse-Proxy auf einem anderen Host, fügen Sie die IP-Adresse des Proxys zu ``rate.limit.trusted.proxies`` (Standardwert ``127.0.0.1,::1``) hinzu. Andernfalls teilen sich alle Aufrufer hinter dem Proxy dieselbe Obergrenze
- Bei Aufrufen aus dem Browser von einem anderen Origin fügen Sie zusätzlich zu ``mcp.allowed.origins`` die Header ``MCP-Protocol-Version``, ``Mcp-Method`` und ``Mcp-Name`` zu ``api.cors.allow.headers`` hinzu. Details finden Sie im Abschnitt „Browser clients“ der README

Aus KI-Agenten verbinden
========================

Claude Code
-----------

Claude Code kann sich direkt mit ``2026-07-28`` verbinden.
Registrieren Sie Fess mit ``claude mcp add`` als HTTP-MCP-Server und übergeben Sie das Token mit ``--header``.

::

    $ claude mcp add --transport http fess http://localhost:8080/mcp \
        --header "Authorization: Bearer <Token>"

``claude mcp list`` zeigt den registrierten Eintrag ``fess`` an; dort lässt sich auch der Verbindungsstatus prüfen.
Bitten Sie Claude Code etwa „Suche in Fess nach dem Ablauf der Reisekostenabrechnung“, ruft der Agent das Werkzeug ``search`` mit Argumenten wie den folgenden auf und liest anschließend mit ``get_document`` und der ``doc_id`` aus den Ergebnissen den Text.

.. code-block:: json

    {
      "name": "search",
      "arguments": {
        "q": "Reisekostenabrechnung",
        "num": 5,
        "fields": { "label": ["manual"] }
      }
    }

Für ``label`` in ``fields`` geben Sie den Wert eines Fess-Labels an (ohne Filterung nach Label lassen Sie es weg).
Weitere Argumente von ``search`` sind unter anderem ``start`` (Paginierung), ``sort`` (z. B. ``last_modified.desc``) und ``lang``.

Andere Clients
--------------

Clients, die sich mit dem älteren Protokoll (``initialize``) verbinden, etwa OpenCode, Codex CLI und Gemini CLI, funktionieren ebenfalls, solange ``mcp.legacy.protocol.enabled`` auf dem Standardwert ``true`` steht.
Clients, die nur ``2025-03-26`` oder ältere Versionen beherrschen, können sich nicht verbinden.
Desktop-Clients, die MCP-Server nur über stdio starten können, nutzen ``mcp-remote``, das zwischen stdio und HTTP vermittelt.
Welche Clients sich verbinden können, ist im Abschnitt „Client compatibility“ der README zusammengefasst.

Vorsicht bei der Weitergabe von Suchergebnissen nach außen
----------------------------------------------------------

Ist das vom Agenten verwendete LLM ein Cloud-Dienst, werden die Auszüge von ``search`` und die Texte von ``get_document`` an diesen Dienst gesendet.
Um den Umfang einzugrenzen, wählen Sie über die Berechtigungen des Tokens nur Dokumente aus, die gesendet werden dürfen, und verkleinern Sie bei Bedarf ``mcp.content.max.length``.

Fehlerbehebung
==============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Symptom
     - Ursache und Abhilfe
   * - HTTP 400, Fehlercode ``-32020``
     - ``MCP-Protocol-Version``, ``Mcp-Method`` oder ``Mcp-Name`` fehlt oder stimmt nicht mit dem Anfragetext überein
   * - HTTP 401
     - Im Modus ``fess_token`` fehlt das Token, existiert nicht oder ist abgelaufen
   * - Alle Anfragen liefern HTTP 403
     - Der ``Origin``-Header ist nicht in ``mcp.allowed.origins`` enthalten. Oder im Modus ``none`` ist „Anmeldung erforderlich“ aktiviert
   * - Der erste Aufruf scheitert mit ``-32601`` und erwähnt ``initialize``
     - Es handelt sich um einen älteren Client, und ``mcp.legacy.protocol.enabled`` ist nicht ``true``
   * - ``search`` liefert 0 Treffer
     - Die Berechtigungen des Tokens enthalten die Rollen der Dokumente nicht. Ist ``partial`` im Ergebnis ``true``, wurde die Suche nicht abgeschlossen (Zeitüberschreitung oder Störung von OpenSearch); es gibt dann nicht zwingend keine Treffer
   * - ``Tool execution failed (error_code:...)``
     - Die Ursache ist in ``fess.log`` als WARN protokolliert. Durchsuchen Sie das Protokoll nach dem Wert von ``error_code``

Weiterführende Artikel
======================

- Über MCP sichtbare Dokumente nach Rollen trennen: :doc:`guide-05`
- Fess selbst mit einem LLM antworten lassen: :doc:`guide-19`
- Bedeutungsähnliche Dokumente auch ohne übereinstimmende Schlüsselwörter finden: :doc:`guide-18`
- Die Such-API aus Geschäftsanwendungen nutzen oder Zugriffstokens je nach Zweck trennen: :doc:`guide-11`
- SSO und Zugriffsschutz gemeinsam einrichten: :doc:`guide-15`

Referenzen
==========

- `fess-webapp-mcp README (15.9.0) <https://github.com/codelibs/fess-webapp-mcp/blob/fess-webapp-mcp-15.9.0/README.md>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `Zugriffstoken <https://fess.codelibs.org/de/stable/admin/accesstoken-guide.html>`__
- `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__
- `Model Context Protocol <https://modelcontextprotocol.io/>`__
