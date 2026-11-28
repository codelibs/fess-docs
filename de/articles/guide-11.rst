===========================================
Geschäftssysteme über die Such-API anbinden
===========================================

Einführung
==========

Sie möchten im Kundenbildschirm Ihres CRM passende Unterlagen auflisten, im Formular für neue Anfragen zuerst ähnliche FAQs anzeigen oder auch die Berichte Ihres eigenen Systems durchsuchbar machen.
Solche Anforderungen lassen sich umsetzen, indem der Server des Geschäftssystems die Such-API von Fess (``/api/v2``) aufruft.

In diesem Artikel gehen wir mit Fess 15.9 die folgenden Schritte nacheinander durch.

- Die APIs für Suche, Labels, Vorschläge und beliebte Wörter mit curl aufrufen und die Form der Antworten prüfen
- Ein Zugriffstoken erstellen und über die Rollen des Tokens steuern, welche Dokumente zurückgegeben werden
- Eine Funktion schreiben, die die Such-API auf der Serverseite des Geschäftssystems aufruft
- Daten, die sich nicht crawlen lassen, mit ``PUT /api/admin/documents/bulk`` registrieren
- Auf Fehler und Ratenbegrenzungen vorbereitet sein

Wie Sie ein Suchfeld oder eine Suchseite in eine bestehende Website einbinden (Einbindung im Browser, Themes, Fess Site Search), behandelt :doc:`guide-03`.
Falls Sie Fess noch nicht gestartet und noch nicht gecrawlt haben, arbeiten Sie zuerst :doc:`guide-02` durch.

Der Aufbau in diesem Artikel
============================

::

    [Browser des Benutzers] --> [Server des Geschäftssystems] --(mit Token)--> [Fess /api/v2]
                                      Das Token liegt nur hier

Der Browser greift nur auf das Geschäftssystem zu; Fess wird vom Server des Geschäftssystems aufgerufen.
Legen Sie das Zugriffstoken zum Beispiel in einer Umgebungsvariablen des Servers ab und geben Sie es nicht an den Browser weiter.
Die Gründe dafür erläutert der Abschnitt „Ein Zugriffstoken erstellen“.

Die APIs im Überblick
=====================

Die suchbezogenen APIs, die Fess 15.9 selbst bereitstellt, liegen unter ``/api/v2``.
In diesem Artikel verwenden wir die folgenden.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Endpunkt
     - Zweck
   * - ``GET /api/v2/search``
     - Volltextsuche. Die Ergebnisse stehen in ``response.data``
   * - ``GET /api/v2/labels``
     - Liste der Labels, die der Aufrufer verwenden darf
   * - ``GET /api/v2/suggest-words``
     - Vorschläge zu einem teilweise eingegebenen Wort
   * - ``GET /api/v2/popular-words``
     - Beliebte Wörter
   * - ``GET /api/v2/health``
     - Zustand der Suchmaschine (Verwendung im Monitoring siehe :doc:`guide-10`)
   * - ``PUT /api/admin/documents/bulk``
     - Massenregistrierung von Dokumenten (Admin-API)

Alle Antworten von ``/api/v2`` sind in ``{"response": {...}}`` eingepackt; ist ``response.status`` gleich 0, war der Aufruf erfolgreich.
Die JSON-Schlüssel sind in ``snake_case`` geschrieben.

.. note::

   Fess 15.9 selbst stellt ``/api/v1`` nicht bereit.
   Wenn bestehende Clients, die ``/api/v1`` aufrufen, weiterlaufen sollen, benötigen Sie das Plugin ``fess-webapp-v1-api`` (es ist nicht im Docker-Image enthalten).
   Verwenden Sie für neue Anbindungen ``/api/v2``.

Zuerst mit curl ausprobieren
============================

Wenn die anonyme Suche erlaubt ist („Anmeldung erforderlich“ unter [System] > [Allgemein] ist aus, das ist der Standard), können Sie die API ohne Token aufrufen.
Suchbegriffe mit Leerzeichen oder Nicht-ASCII-Zeichen werden mit ``-G --data-urlencode`` URL-kodiert gesendet.
Damit die Ausgabe besser lesbar ist, verwenden wir ``jq``.

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=Handbuch Suche" \
        --data-urlencode "num=3" \
      | jq '.response | {status, record_count, page_size, data: [.data[] | {doc_id, title, url_link, content_description}]}'

Die Antwort sieht so aus (von ``data`` ist nur das erste Element gezeigt; die Werte hängen von Ihrer Umgebung ab).

.. code-block:: json

    {
      "status": 0,
      "record_count": 12,
      "page_size": 3,
      "data": [
        {
          "doc_id": "5d4c0e0e5a7b4b5c9d2f6a1b3c8e7f90",
          "title": "Handbuch zur Suche",
          "url_link": "https://fess.codelibs.org/de/stable/user/index.html",
          "content_description": "Das <strong>Handbuch</strong> zur <strong>Suche</strong> in Fess. ..."
        }
      ]
    }

``response`` enthält außerdem ``page_count``, ``next_page``, ``exec_time``, ``query_id`` und weitere Werte.
Jedes Element von ``data`` enthält nur die für API-Antworten freigegebenen Felder, etwa ``title``, ``url``, ``url_link``, ``content_description``, ``last_modified``, ``filetype`` und ``score``.
Der vollständige Text (``content``) und die Labels (``label``) werden standardmäßig nicht zurückgegeben.
Um weitere Felder zurückzugeben, ergänzen Sie sie in ``query.additional.api.response.fields`` in der ``fess_config.properties``.
``content_description`` ist ein Auszug, in dem die Suchbegriffe von ``<strong>``-Tags umschlossen sind. Behandeln Sie ihn bei der Anzeige als HTML oder entfernen Sie die Tags.

Häufig verwendete Parameter sind die folgenden.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Bedeutung
   * - ``q``
     - Suchbegriffe. Es gilt dieselbe Syntax wie auf der Suchseite (AND, OR, Ausschluss, Feldangaben usw.)
   * - ``num`` / ``start``
     - Anzahl der Treffer pro Seite (Standard 10; Werte über der Obergrenze werden auf die Obergrenze gekürzt) und Startposition (ab 0)
   * - ``sort``
     - Sortierreihenfolge. Beispiel: ``last_modified.desc`` (zuletzt aktualisierte zuerst)
   * - ``fields.label``
     - Eingrenzung nach Labelwert. Kann mehrfach angegeben werden

Weitere Parameter (Facetten, Sprache, Geodaten usw.) finden Sie unter `Such-API <https://fess.codelibs.org/de/stable/api/api-search.html>`__.

Labels, Vorschläge und beliebte Wörter rufen Sie auf dieselbe Weise auf.

::

    $ curl -s "http://localhost:8080/api/v2/labels" | jq .response
    $ curl -s -G "http://localhost:8080/api/v2/suggest-words" --data-urlencode "q=fe" | jq .response
    $ curl -s "http://localhost:8080/api/v2/popular-words" | jq .response

Die Ergebnisse stehen jeweils in ``response.labels[]`` (``label`` und ``value``), ``response.suggest_words[]`` (``text`` und ``types``) und ``response.popular_words`` (ein Array von Zeichenketten).
Warum Vorschläge und beliebte Wörter leer sein können, erklärt der Abschnitt „Labels, Vorschläge und beliebte Wörter nutzen“.

Ein Zugriffstoken erstellen
===========================

Für Aufrufe aus einem Geschäftssystem verwenden Sie ein Zugriffstoken.
Dem Token werden „Berechtigungen“ zugewiesen, und nach diesen Berechtigungen werden die Suchergebnisse eingegrenzt.

Vorgehen
--------

1. Öffnen Sie in der Administrationsoberfläche [System] > [Zugriffstoken] und klicken Sie auf [Neu erstellen].
2. Geben Sie unter „Name“ einen Namen ein, der den Zweck erkennen lässt (zum Beispiel ``crm-search``).
3. Tragen Sie unter „Berechtigungen“ die Rollen der Dokumente, die dieses Token anzeigen darf, je eine pro Zeile ein. Die Formate sind ``{role}Rollenname``, ``{group}Gruppenname`` und ``{user}Benutzername``.
4. Geben Sie „Läuft ab“ im Format ``2027-03-31T23:59:59`` ein. Bleibt das Feld leer, läuft das Token nicht ab.
5. Lassen Sie „Parametername“ leer.
6. Klicken Sie auf [Erstellen]. Klicken Sie zurück in der Liste auf den Namen und notieren Sie den Wert, der auf der Detailseite unter „Token“ angezeigt wird (60 alphanumerische Zeichen).

Wenn Sie „Parametername“ setzen, kann der Aufrufer über diesen Anfrageparameter Berechtigungen hinzufügen.
Verwenden Sie das nur, wenn Sie die Aufrufer vollständig unter Kontrolle haben.

Das Token senden
----------------

Senden Sie das Token im ``Authorization``-Header.
``Authorization: <Token>`` ohne ``Bearer`` wird ebenfalls akzeptiert.

::

    $ export FESS_SEARCH_TOKEN=<notiertes Token>
    $ curl -s -G "http://localhost:8080/api/v2/search" \
        -H "Authorization: Bearer $FESS_SEARCH_TOKEN" \
        --data-urlencode "q=Angebot" | jq '.response.record_count'

Die Übergabe des Tokens als Abfrageparameter ist deaktiviert, weil ``api.access.token.request.parameter`` standardmäßig leer ist.
URLs landen in den Zugriffsprotokollen, verwenden Sie daher den Header.

Die Rollen des Tokens bestimmen die Ergebnisse
----------------------------------------------

Bei einer Anfrage mit Token werden ausschließlich die Berechtigungen des Tokens als Rollen verwendet.
Die Gastrolle (``{role}guest``), die anonyme Aufrufe ohne Token erhalten, wird nicht hinzugefügt, solange die Berechtigungen des Tokens nicht leer sind.

Andererseits steht beim Neuanlegen einer Crawl-Konfiguration ``{role}guest`` im Berechtigungsfeld, sodass gewöhnliche öffentliche Dokumente ``{role}guest`` tragen.
Ein Token, dessen einzige Berechtigung ``{group}sales`` ist, lässt öffentliche Dokumente deshalb aus den Suchergebnissen verschwinden.
Sollen sowohl öffentliche Dokumente als auch Dokumente für den Vertrieb zurückgegeben werden, geben Sie dem Token die folgenden zwei Zeilen als Berechtigungen.

::

    {role}guest
    {group}sales

Vergleichen Sie danach ``record_count`` für dieselben Suchbegriffe ohne Token und mit Token und prüfen Sie, ob die Zahl wie erwartet steigt oder sinkt.
Die Gestaltung der Berechtigungen auf Dokumentseite behandelt :doc:`guide-05`.

Warum das Token nicht in den Browser gehört
-------------------------------------------

- Ein Token im JavaScript des Browsers kann jeder mit den Entwicklertools auslesen. Wer es ausliest, kann alle Dokumente, die mit den Berechtigungen des Tokens sichtbar sind, am Geschäftssystem vorbei durchsuchen.
- Ein Token gehört nicht zu einem einzelnen Benutzer, sondern bündelt die bei der Ausstellung angegebenen Berechtigungen. Verteilen Sie es an Browser, gehen die Unterschiede in den Rechten der einzelnen Benutzer verloren.
- Auch wenn „Anmeldung erforderlich“ eingeschaltet ist, antworten ``/search``, ``/documents/all``, ``/documents/export``, ``/suggest-words``, ``/labels`` und ``/popular-words`` bei gültigem Token ohne Anmeldung. Ein durchgesickertes Token kann also anstelle einer Anmeldung verwendet werden.

Soll der sichtbare Bereich vom Benutzer des Geschäftssystems abhängen, erstellen Sie für jeden Bereich ein eigenes Token und wählen auf der Serverseite je nach Benutzer das passende aus.

Die Such-API vom Server aus aufrufen
====================================

Hier ein Beispiel für eine Python-Funktion im Backend des Geschäftssystems.
Sie verwendet nur die Standardbibliothek und gibt die Suchergebnisse auf die Felder reduziert zurück, die der Bildschirm braucht.

.. code-block:: python

    import json
    import os
    import urllib.error
    import urllib.parse
    import urllib.request

    FESS_URL = os.environ.get("FESS_URL", "http://localhost:8080")
    FESS_SEARCH_TOKEN = os.environ["FESS_SEARCH_TOKEN"]


    class FessApiError(Exception):
        def __init__(self, http_status, code, retry_after=None):
            super().__init__(f"Fess API error: {http_status} {code}")
            self.http_status = http_status
            self.code = code
            self.retry_after = retry_after


    def search_documents(query, label=None, num=5):
        params = [("q", query), ("num", str(num))]
        if label:
            params.append(("fields.label", label))
        url = FESS_URL + "/api/v2/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + FESS_SEARCH_TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                body = json.load(res)
        except urllib.error.HTTPError as e:
            try:
                code = json.load(e)["response"]["error"]["code"]
            except (ValueError, KeyError, TypeError):
                code = "unknown"
            raise FessApiError(e.code, code, e.headers.get("Retry-After")) from e
        response = body["response"]
        return {
            "total": response["record_count"],
            "items": [
                {
                    "title": doc.get("title"),
                    "url": doc.get("url_link"),
                    "snippet": doc.get("content_description"),
                    "last_modified": doc.get("last_modified"),
                }
                for doc in response["data"]
            ],
        }

Im Kundenbildschirm eines CRM übergeben Sie Kundenname und Label, etwa ``search_documents("Beispiel GmbH", label="sales_docs")``, und stellen den Rückgabewert direkt auf dem Bildschirm dar.

- Das Timeout ist etwas länger gewählt als das Such-Timeout auf der Fess-Seite (``query.timeout``, standardmäßig 10000 Millisekunden).
- Anhand von ``code`` und ``retry_after`` des ``FessApiError`` entscheiden Sie über die Meldung an den Benutzer und über Wiederholungen (siehe „Fehlerbehandlung“).
- ``content_description`` enthält ``<strong>``-Tags. Wenn Ihr Template den Wert als HTML ausgibt, lassen Sie nur das Tag ``<strong>`` zu.

Daten aus externen Systemen registrieren
========================================

Daten, die sich nicht crawlen lassen (vom Geschäftssystem erzeugte Berichte, Zusammenfassungen von Tickets usw.), können Sie mit ``PUT /api/admin/documents/bulk`` der Admin-API direkt im Index registrieren.

Ein eigenes Token für die Admin-API
-----------------------------------

Die Admin-API erfordert ein Token, dessen Berechtigungen ``{role}admin-api`` enthalten (``api.admin.access.permissions=Radmin-api``).
Diese Berechtigung erlaubt sämtliche Endpunkte der Admin-API.
Eine Berechtigung, die nur das Registrieren von Dokumenten erlaubt, gibt es nicht.
Mit einem solchen Token lassen sich auch Crawl-Konfigurationen, Benutzer und sogar die Zugriffstoken selbst bearbeiten. Bewahren Sie es daher so sorgfältig auf wie das Administratorpasswort.

Sucht man zudem mit einem Token, das nur ``{role}admin-api`` hat, ist ``admin-api`` die einzige Rolle, und es werden fast keine Dokumente zurückgegeben.
Verwenden Sie getrennte Tokens zum Suchen und zum Registrieren.
Erstellen Sie unter [System] > [Zugriffstoken] ein weiteres Token, dessen Berechtigungen nur aus der einen Zeile ``{role}admin-api`` bestehen (zum Beispiel mit dem Namen ``crm-indexer``), und notieren Sie seinen Wert.

::

    $ export FESS_ADMIN_TOKEN=<notiertes Token für die Admin-API>

Registrieren
------------

``url`` und ``title`` sind Pflichtangaben.
``content`` ist der Text, ``label`` ein Array von Labelwerten.

::

    $ curl -s -X PUT "http://localhost:8080/api/admin/documents/bulk" \
        -H "Authorization: Bearer $FESS_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "documents": [
            {
              "url": "https://crm.example.com/reports/2026-11",
              "title": "Vertriebsmonatsbericht November 2026",
              "content": "Die Zahl neuer Verkaufschancen ist im November gegenüber dem Vormonat gestiegen.",
              "label": ["sales_docs"]
            }
          ]
        }' | jq .response

Bei Erfolg wird das Ergebnis für jedes Dokument in ``items`` zurückgegeben.
Eine Neuanlage liefert ``CREATED``, die Aktualisierung eines vorhandenen Dokuments ``OK``.

.. code-block:: json

    {
      "version": "15.9",
      "status": 0,
      "items": [
        { "result": "CREATED", "id": "9c1e47b2...e04b" }
      ]
    }

``id`` ist ein aus ``url`` und weiteren Werten berechneter Hashwert (128 Hexadezimalstellen); im Beispiel oben ist der mittlere Teil ausgelassen.
Die Registrierung ist abgeschlossen, wenn eine Suche nach ``q=Vertriebsmonatsbericht`` mit dem Such-Token das Dokument findet.

Hinweise zur Registrierung
--------------------------

- Lassen Sie ``role`` weg, erhält das Dokument die Gastrolle und ist für alle auffindbar. Um den Kreis einzuschränken, tragen Sie in ``role`` Werte im internen Format als Array ein. Im internen Format wird ``{role}x`` zu ``Rx``, ``{group}x`` zu ``2x`` und ``{user}x`` zu ``1x`` (zum Beispiel ``"role": ["2sales"]``).
- Die Dokument-ID wird aus ``url`` und ``role`` (sowie dem virtuellen Host) gebildet. Erneutes Senden mit derselben ``url`` aktualisiert das Dokument; senden Sie es jedoch mit geänderter ``role``, wird es als separates Dokument hinzugefügt und das alte bleibt bestehen.
- ``items[].id`` in der Antwort ist die ID im Index und unterscheidet sich von der ``doc_id`` des Dokuments. Für das Löschen einzelner Dokumente mit ``DELETE /api/admin/searchlist/doc/{id}`` übergeben Sie die ``doc_id`` aus den Suchergebnissen. Zum Löschen mehrerer Dokumente nach einer Bedingung verwenden Sie ``DELETE /api/admin/searchlist/query`` (`SearchList API <https://fess.codelibs.org/de/stable/api/admin/api-admin-searchlist.html>`__).
- Schlagen nur einzelne Dokumente fehl, wird ``status`` zu 9, und die fehlgeschlagenen Elemente enthalten ``message``. Ist die Anfrage selbst ungültig, etwa weil ``url`` oder ``title`` fehlt oder ein Wert den falschen Typ hat, wird ``status`` zu 1, und es wird nichts registriert.

Labels, Vorschläge und beliebte Wörter nutzen
=============================================

Kategorien mit Labels bilden
----------------------------

Die Labels, nach denen Sie mit ``fields.label`` eingrenzen, legen Sie unter [Crawler] > [Label] an.
„Wert“ darf nur alphanumerische Zeichen und Unterstriche enthalten (``sales-docs`` oder Nicht-ASCII-Zeichen sind nicht möglich).
Ein gecrawltes Dokument erhält ein Label, wenn seine URL zum Feld „Eingeschlossene Pfade“ des Labels passt (:doc:`guide-04`).
Für per Bulk registrierte Dokumente senden Sie ``label`` wie im vorigen Abschnitt.

``/api/v2/labels`` gibt nur die Labels zurück, die die Rollen des Aufrufers verwenden dürfen.
Auch Labels haben Berechtigungen; Labels, die nicht zu den Berechtigungen des Tokens passen, erscheinen nicht in der Liste.
Die Kategorienliste eines Portals bauen Sie aus ``label`` (Anzeigename) und ``value`` (der an ``fields.label`` zu übergebende Wert) dieser Antwort.

Vorschläge
----------

``/api/v2/suggest-words`` liefert Kandidaten, die mit ``q`` beginnen.
Die Anzahl legt ``num`` fest (Standard 10), die Zielfelder geben Sie durch wiederholtes ``fn`` an.
Die Kandidaten stammen aus Wörtern der gecrawlten Dokumente („Vorschläge aus Dokumenten“ unter [System] > [Allgemein]), aus Suchbegriffen („Vorschläge aus Suchbegriffen“ auf derselben Seite) und aus vom Administrator registrierten Vorschlagswörtern.
Wörter aus Dokumenten erscheinen erst als Kandidaten, nachdem der Job „Suggest Indexer“ im Scheduler gelaufen ist (standardmäßig einmal täglich).
Auch die Kandidaten werden nach den Rollen des Aufrufers eingegrenzt.

Beliebte Wörter
---------------

``/api/v2/popular-words`` gibt unter den im Suchprotokoll gesammelten Suchbegriffen diejenigen zurück, die häufig gesucht wurden.
Kommt ein leeres Array zurück, prüfen Sie die folgenden Punkte.

- Ist „Antwort für beliebtes Wort“ unter [System] > [Allgemein] (``web.api.popularword``, standardmäßig an) ausgeschaltet, endet der Aufruf mit ``invalid_request`` (HTTP 400).
- „Vorschläge aus Suchbegriffen“ muss eingeschaltet sein. Suchbegriffe werden nur gesammelt, solange diese Einstellung an ist.
- Derselbe Begriff muss mindestens 10-mal gesucht worden sein (``suggest.popular.word.query.freq=10``). Wiederholte Suchen aus derselben Sitzung innerhalb einer Minute zählen als eine. Direkt nach der Einführung ist ein leeres Ergebnis normal.
- Gezählt werden nur Suchen, die allein mit der Gastrolle ausgeführt wurden (``suggest.search.log.permissions={user}guest,{role}guest``). Suchen mit Tokens, die etwa ``{group}sales`` haben, und Suchen angemeldeter Benutzer werden nicht gezählt.
- Auch beliebte Wörter werden nach den Rollen des Aufrufers eingegrenzt. Die gezählten Begriffe tragen nur die Gastrolle, daher bleibt das Ergebnis für ein Token, dessen Berechtigungen ``{role}guest`` nicht enthalten, immer leer.
- Die Ergebnisse werden zwischengespeichert und ändern sich daher nicht sofort, wenn die Suchen zunehmen.

Wenn Sie ``seed`` ändern, wird eine andere Kombination aus den Kandidaten zurückgegeben.

Fehlerbehandlung
================

Im Fehlerfall liefert ``/api/v2`` einen HTTP-Status und ``response.error.code``.

::

    {"response": {"status": 1, "error": {"code": "invalid_request", "message": "..."}}}

Für die folgenden Fälle sollte die anbindende Seite die Behandlung im Voraus festlegen.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - HTTP
     - ``error.code``
     - Ursache und Maßnahme
   * - 400
     - ``invalid_request``
     - ``num`` ist 0 oder kleiner, die Suchbegriffe enthalten einen Syntaxfehler, ``q`` überschreitet ``api.param.max.length`` (standardmäßig 1000 Zeichen) usw. Nicht wiederholen, sondern die Eingabe prüfen
   * - 401
     - ``auth_required``
     - Nicht registriertes oder abgelaufenes Token, oder kein Token, während „Anmeldung erforderlich“ eingeschaltet ist. Ein ungültiges Token führt nicht zurück zum anonymen Zugriff, sondern zu 401. Erstellen Sie das Token neu
   * - 503
     - ``service_unavailable``
     - Die Suchmaschine war überlastet und hat die Suche abgelehnt. ``Retry-After: 5`` wird mitgeliefert; Sie können nach 5 Sekunden erneut versuchen
   * - 500
     - ``internal_error``
     - Interner Fehler in Fess. Prüfen Sie ``fess.log`` unter [Systeminformationen] > [Protokolldatei]

Bei den Ratenbegrenzungen haben die Endpunkte für Anmeldung, Passwortänderung, Chat und Export jeweils eigene Obergrenzen; wird eine überschritten, kommen 429 ``rate_limited`` und ``Retry-After`` zurück.
Die serverweite Begrenzung der Anfragezahl (``rate.limit.enabled``) ist standardmäßig deaktiviert.
Wenn Sie sie aktivieren, lautet der Rumpf der 429-Antwort bei Überschreitung ``{"error":"rate_limit_exceeded", ...}`` und hat nicht die oben gezeigte ``response``-Form.
Beachten Sie bei Aufrufen vom Server eines Geschäftssystems, dass alle Suchen von derselben IP-Adresse kommen.
Einzelheiten finden Sie unter `Rate-Limiting-Konfiguration <https://fess.codelibs.org/de/stable/config/rate-limiting.html>`__.

Die Admin-API (``/api/admin/*``) verwendet eine andere Fehlerform.
Fehlt das Token oder hat es kein ``{role}admin-api``, lautet die Antwort HTTP 401 mit ``response.status`` gleich 3, und der Grund steht in ``response.message``.

Direkter Aufruf aus dem Browser (CORS)
======================================

Für Aufrufe zwischen Servern spielt CORS keine Rolle.
Nur wenn JavaScript im Browser Fess auf einem anderen Origin direkt aufruft, wirken ``api.cors.allow.origin`` (Standard ``*``), ``api.cors.allow.methods``, ``api.cors.allow.headers`` (enthält standardmäßig ``Authorization``), ``api.cors.allow.credentials`` (Standard ``true``) und ``api.cors.max.age`` (Standard ``3600`` Sekunden) in der ``fess_config.properties``.

Ist ``api.cors.allow.origin`` gleich ``*``, werden Anfragen mit Anmeldedaten wie Cookies nicht zugelassen.
Soll der Browser mit den Rechten eines angemeldeten Benutzers suchen, zählen Sie die Origins auf, etwa ``https://portal.example.com`` (kommagetrennt).
Unter Docker können Sie auch ``-Dfess.config.api.cors.allow.origin=https://portal.example.com`` in ``FESS_JAVA_OPTS`` angeben.
Starten Sie Fess nach der Änderung neu.
Wie die Einbindung im Browser funktioniert, beschreibt :doc:`guide-03`.

Weiterführende Artikel
======================

- Suchfeld oder Suchseite in eine bestehende Website einbinden: :doc:`guide-03`
- Festlegen, welche Dokumente je Token oder Benutzer sichtbar sind: :doc:`guide-05`
- Die API für Health-Checks und Monitoring nutzen: :doc:`guide-10`
- Einstellungen mit der Admin-API und fessctl als Code verwalten: :doc:`guide-16`
- Die Suchplattform einschließlich des Betriebs von SSO und Zugriffstokens absichern: :doc:`guide-15`

Referenzen
==========

- `API-Übersicht <https://fess.codelibs.org/de/stable/api/api-overview.html>`__
- `Such-API <https://fess.codelibs.org/de/stable/api/api-search.html>`__
- `Label-API <https://fess.codelibs.org/de/stable/api/api-label.html>`__
- `Vorschlags-API <https://fess.codelibs.org/de/stable/api/api-suggest.html>`__
- `Beliebte-Wörter-API <https://fess.codelibs.org/de/stable/api/api-popularword.html>`__
- `Documents API <https://fess.codelibs.org/de/stable/api/admin/api-admin-documents.html>`__
- `Admin API Übersicht <https://fess.codelibs.org/de/stable/api/admin/api-admin-overview.html>`__
- `Zugriffstoken <https://fess.codelibs.org/de/stable/admin/accesstoken-guide.html>`__
