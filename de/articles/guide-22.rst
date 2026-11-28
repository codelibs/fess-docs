====================================================
Suchprotokolle mit OpenSearch Dashboards analysieren
====================================================

Einleitung
==========

In Fess 15.9 zeigt [Systeminformationen] > [Suchprotokoll] in der Administrationsoberfläche die Quote ohne Treffer, die Klickrate, die Verteilung der Klickpositionen, die Antwortzeiten, die Suchanzahl nach Wochentag und Uhrzeit sowie die Suchanzahl nach Rolle und Gruppe.
Jede Tabelle lässt sich als CSV herunterladen.
Wie Sie problematische Suchbegriffe finden und mit Synonymen oder Schlüsselübereinstimmungen beheben, beschreibt :doc:`guide-08`.

Folgende Auswertungen sind auf dieser Seite dagegen nicht möglich:

- Verläufe über Zeiträume von mehr als 366 Tagen (der Zeitraum „Benutzerdefiniert“ auf der Seite ist auf 366 Tage begrenzt)
- Welche Begriffe ohne Treffer bleiben, aufgeschlüsselt nach Rolle oder Label
- Welche URLs zu jedem Suchbegriff tatsächlich geöffnet wurden
- Ein Dashboard mit Diagrammen nach selbst gewählten Gesichtspunkten

Such- und Klickprotokolle werden in OpenSearch-Indizes gespeichert, daher können Sie sie direkt in OpenSearch Dashboards auswerten.
Dieser Artikel startet OpenSearch Dashboards mit den Compose-Dateien von docker-fess, importiert das mit Fess ausgelieferte Dashboard, prüft die Protokollfelder und erstellt anschließend die vier oben genannten Auswertungen.

Vor dem Start: Zugriff beschränken
==================================

In docker-fess läuft OpenSearch Dashboards wie OpenSearch selbst ohne das Security-Plugin.
Wer Port 5601 erreicht, kann ohne Anmeldung alle Felder der Suchprotokolle lesen (Benutzer-IDs, IP-Adressen usw.).
Außerdem lässt sich über Dev Tools jeder Index ändern oder löschen, einschließlich der Fess-Indizes für Benutzer und Einstellungen.

Machen Sie Port 5601 (und 9200) deshalb nur von den Rechnern der Administratoren aus erreichbar.
Wenn Sie Auswertungen der Suchprotokolle auch Personen zeigen möchten, die keine Administratoren sind, veröffentlichen Sie nicht OpenSearch Dashboards, sondern legen in Fess unter [Benutzer] > [Rolle] eine Rolle mit dem Namen ``admin-searchlog-view`` an und weisen sie diesen Personen zu.
Mit dieser Rolle kann man [Systeminformationen] > [Suchprotokoll] ansehen, aber keine Protokolle löschen.

OpenSearch Dashboards starten
=============================

Fügen Sie die Dateien für Dashboards dem Verzeichnis hinzu, in dem Sie gemäß :doc:`guide-02` ``compose.yaml`` und ``compose-opensearch3.yaml`` abgelegt haben.
``compose-dashboards3.yaml`` baut sein Image aus dem Dockerfile im Verzeichnis ``dashboards/``, daher werden drei Dateien benötigt.

::

    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-dashboards3.yaml
    $ mkdir dashboards
    $ curl -L -o dashboards/Dockerfile https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/Dockerfile
    $ curl -L -o dashboards/opensearch_dashboards.yml https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/dashboards/opensearch_dashboards.yml

Starten Sie unter Angabe der drei Compose-Dateien.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-dashboards3.yaml up -d

Beim ersten ``up`` wird aus ``opensearch-dashboards:3.9.0`` ein Image gebaut, aus dem das Plugin ``securityDashboards`` entfernt ist.
Der Container verbindet sich im Netzwerk ``search_net`` mit ``OPENSEARCH_HOSTS='["http://search01:9200"]'`` und gibt Port 5601 frei.

Öffnen Sie ``http://localhost:5601`` im Browser; erscheint die Startseite, läuft der Dienst.
Geben Sie auch beim Stoppen oder bei der Statusabfrage die drei Dateien mit ``-f`` an.
Gespeicherte Objekte wie Dashboards liegen im Index ``.kibana`` in OpenSearch; wenn Sie die Volumes mit ``down -v`` entfernen, werden sie ebenfalls gelöscht.

Das mitgelieferte Dashboard importieren
=======================================

Fess enthält mit ``fess_log.ndjson`` eine Dashboard-Definition für Suchprotokolle.
Bei Docker kopieren Sie sie aus dem Container.
In der ZIP-Version liegt sie im entpackten Verzeichnis unter ``extension/kibana/fess_log.ndjson``.

::

    $ docker cp fess01:/usr/share/fess/extension/kibana/fess_log.ndjson .

Dieselbe Datei erhalten Sie auch von GitHub unter ``https://raw.githubusercontent.com/codelibs/fess/fess-15.9.0/src/main/assemblies/extension/kibana/fess_log.ndjson``.

1. Öffnen Sie im linken Menü [Dashboards Management] und wählen Sie [Saved objects]
2. Klicken Sie auf [Import], wählen Sie ``fess_log.ndjson`` aus und importieren Sie die Datei
3. Öffnen Sie im linken Menü unter [Dashboards] das Dashboard ``fess_log``

Der Import registriert das Index-Pattern ``fess_log*`` (Zeitfeld ``requestedAt``), sechs Visualisierungen und das Dashboard ``fess_log``.
Da das Index-Pattern enthalten ist, müssen Sie ``fess_log*`` nicht vorher manuell anlegen.
Legen Sie es manuell an und importieren danach, gibt es zwei Patterns mit demselben Namen.

Wie das mitgelieferte Dashboard zählt
-------------------------------------

``fess_log*`` umfasst alle Indizes, deren Name mit ``fess_log`` beginnt, und die mitgelieferten Visualisierungen filtern nicht nach Index.
In 15.9 enthalten Klickprotokolle den Suchbegriff (``searchWord``) und ``requestedAt``; die Anzahl in „search-term-rank“ etwa addiert daher Suchen und Klicks.
Wenn Sie den Modus KI-Suche verwenden, fließen auch die Chat-Protokolle (``fess_log.chat_log``) in Anzahlen und Antwortzeiten ein.

Um nur Suchen zu zählen, geben Sie vor dem Ablesen die folgende Bedingung in die Suchleiste oben im Dashboard ein.

::

    _index : "fess_log.search_log"

Außerdem stammt die in ``fess_log*`` gespeicherte Feldliste aus einer älteren Version und enthält neuere Felder wie ``rank`` nicht.
Für eigene Auswertungen verwenden Sie die Index-Patterns aus dem nächsten Abschnitt.

Index-Patterns für Auswertungen anlegen
=======================================

Wenn Sie Such- und Klickprotokolle in getrennten Index-Patterns führen, vermischen sie sich nicht, und alle aktuellen Felder stehen zur Auswahl.

1. Klicken Sie unter [Dashboards Management] > [Index patterns] auf [Create index pattern]
2. Geben Sie unter „Index pattern name“ ``fess_log.search_log`` ein und klicken Sie auf [Next step]
3. Wählen Sie unter „Time field“ ``requestedAt`` und klicken Sie auf [Create index pattern]
4. Legen Sie auf dieselbe Weise ``fess_log.click_log`` an (Zeitfeld ``requestedAt``)

Kommen später Felder hinzu (etwa wenn zum ersten Mal eine nach Label gefilterte Suche protokolliert wird), klicken Sie auf der Seite des Index-Patterns auf [Refresh field list].

Umgang mit Zeitangaben
----------------------

Fess speichert Datum und Uhrzeit in UTC.
OpenSearch Dashboards zeigt sie standardmäßig in der Zeitzone des Browsers an und teilt auch die Tage danach ein.
Um sie in einer anderen Zeitzone zu sehen, stellen Sie ``dateFormat:tz`` unter [Dashboards Management] > [Advanced settings] auf Ihre Zeitzone um, zum Beispiel ``Asia/Tokyo``.

Die Seite [Suchprotokoll] in Fess teilt die Tage nach der Zeitzone des Servers ein.
Die Container von docker-fess verwenden standardmäßig UTC; vergleichen Sie die Tageswerte beider Seiten, können sie sich daher um die unterschiedlichen Tagesgrenzen verschieben.

Protokollfelder
===============

Das Suchprotokoll (``fess_log.search_log``) enthält einen Eintrag pro Suche.
Die für Auswertungen am häufigsten verwendeten Felder sind folgende.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Inhalt
   * - ``queryId``
     - keyword
     - ID jeder Suche. Entspricht ``queryId`` im Klickprotokoll
   * - ``searchWord``
     - keyword
     - Der Suchbegriff. Bei einer nach Label gefilterten Suche enthält er auch die Bedingung, etwa ``Antrag label:"hr"``
   * - ``searchField.*``
     - keyword
     - Der Suchbegriff nach Feldern aufgeteilt. Gewöhnliche Begriffe landen in ``searchField._default``, Label-Filter in ``searchField.label``
   * - ``requestedAt``
     - date
     - Datum und Uhrzeit der Suche (in UTC gespeichert)
   * - ``hitCount``
     - long
     - Anzahl der Treffer. ``0`` bedeutet eine Suche ohne Treffer
   * - ``responseTime`` / ``queryTime``
     - long
     - Verarbeitungszeit der gesamten Suche und Suchzeit in OpenSearch (Millisekunden)
   * - ``queryOffset`` / ``queryPageSize``
     - integer
     - Startposition und Seitengröße. Ab der zweiten Seite ist ``queryOffset`` größer als 0
   * - ``accessType``
     - keyword
     - Einer der Werte ``json``, ``gsa``, ``admin``, ``other`` und ``web``. Die Suchseite des Standard-Themes ruft ``/api/v2/search`` auf und ergibt daher ``json``; Suchen über [Systeminformationen] > [Suche] in der Administrationsoberfläche ergeben ``admin``
   * - ``user`` / ``roles``
     - keyword
     - Die ID des angemeldeten Benutzers und die Liste der für die Suche verwendeten Rollen. Das erste Zeichen eines ``roles``-Werts gibt die Art an: ``R`` ist eine Rolle, ``2`` eine Gruppe und ``1`` ein Benutzer (Beispiel: ``Rguest``)
   * - ``userSessionId`` / ``clientIp`` / ``userAgent`` / ``referer`` / ``virtualHost``
     - keyword
     - Der Cookie-Wert, der den Benutzer identifiziert, die IP-Adresse, der Browser, die verweisende Seite und der virtuelle Host

Das Klickprotokoll (``fess_log.click_log``) wird geschrieben, wenn ein Link in den Suchergebnissen über ``/go/`` geöffnet wird.
Für Anfragen, bei denen der Browser keine Fess-Sitzung hat (kein gültiges Sitzungs-Cookie sendet), wird es jedoch nicht geschrieben.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Typ
     - Inhalt
   * - ``queryId``
     - keyword
     - ``queryId`` der Suche, von der der Klick ausging
   * - ``url`` / ``docId``
     - keyword
     - URL und Dokument-ID des geöffneten Dokuments
   * - ``rank``
     - integer
     - Position innerhalb aller Suchergebnisse (der erste Platz ist 1). Das erste Ergebnis auf der zweiten Seite ist 11
   * - ``order``
     - integer
     - Position innerhalb der Seite (die erste ist 0). Für Auswertungen der Position verwenden Sie ``rank``
   * - ``searchWord`` / ``accessType``
     - keyword
     - Aus der Ausgangssuche übernommener Suchbegriff und Zugriffstyp. Sie können nach Suchbegriff auswerten, ohne mit dem Suchprotokoll zu verknüpfen
   * - ``requestedAt`` / ``queryRequestedAt``
     - date
     - Datum und Uhrzeit des Klicks sowie der Ausgangssuche

``searchWord``, ``accessType`` und ``rank`` sind erst ab 15.9 im Klickprotokoll enthalten.
Davor protokollierte Klicks haben diese Felder nicht.

Rezepte für Auswertungen
========================

Hier erstellen wir die vier eingangs genannten „Auswertungen, die die Seite nicht kann“.
Die erste wird mit Visualize erstellt, die übrigen werden im linken Menü unter [Dev Tools] mit der Such-API ausgeführt.

Geöffnete URLs je Suchbegriff
-----------------------------

Diese Tabelle zeigt für jeden Suchbegriff, welche Dokumente an welcher Position geöffnet wurden.
Sie hilft bei der Auswahl von Kandidaten für Schlüsselübereinstimmung oder Dokument-Boost.

1. Klicken Sie im linken Menü unter [Visualize] auf [Create visualization] und wählen Sie „Data Table“
2. Wählen Sie ``fess_log.click_log`` als Quelle
3. Fügen Sie unter Metrics mit [Add] eine Metric hinzu und wählen Sie unter „Aggregation“ „Average“ und unter „Field“ ``rank``
4. Wählen Sie unter Buckets [Add] > [Split rows] und setzen Sie „Aggregation“ auf „Terms“, „Field“ auf ``searchWord`` und „Size“ auf 20
5. Fügen Sie ein weiteres [Split rows] mit „Terms“, „Field“ auf ``url`` und „Size“ auf 5 hinzu
6. Klicken Sie auf [Update], wählen Sie oben rechts den Zeitraum und speichern Sie

Kombinationen mit hoher durchschnittlicher Position sind Dokumente, die Benutzer erst weit unten in den Ergebnissen gefunden und geöffnet haben.

Begriffe ohne Treffer nach Rolle
--------------------------------

Wenn Sie Rollen nach Abteilungen aufteilen, prüfen Sie, was die Suchen der einzelnen Abteilungen nicht finden.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [
            { "term": { "hitCount": 0 } },
            { "range": { "requestedAt": { "gte": "now-90d/d" } } }
          ]
        }
      },
      "aggs": {
        "roles": {
          "terms": { "field": "roles", "size": 20, "exclude": "1.*" },
          "aggs": {
            "words": { "terms": { "field": "searchWord", "size": 10 } }
          }
        }
      }
    }

``exclude`` entfernt Werte, die mit ``1`` beginnen (einzelne Benutzer), sodass nur Rollen und Gruppen aufgelistet werden.
Eine Suche wird bei jeder Rolle und Gruppe des jeweiligen Benutzers gezählt.
Suchen nicht angemeldeter Benutzer fallen unter ``Rguest``.

Suchen und Suchen ohne Treffer nach Label
-----------------------------------------

Zählen Sie für jedes Label, wie oft mit ausgewähltem Label auf der Suchseite gesucht wurde und wie viele dieser Suchen ohne Treffer blieben.

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": { "range": { "requestedAt": { "gte": "now-90d/d" } } },
      "aggs": {
        "labels": {
          "terms": { "field": "searchField.label", "size": 20 },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } }
          }
        }
      }
    }

Wurde noch keine nach Label gefilterte Suche protokolliert, existiert das Feld ``searchField.label`` noch nicht, und die Buckets von ``labels`` bleiben leer.

Monatliche Quote ohne Treffer (zwei Jahre)
------------------------------------------

Betrachten Sie über die Zeitraumgrenze der Seite hinaus den langfristigen Verlauf der Quote ohne Treffer (als Anteil, nicht als Anzahl).

.. code-block:: text

    GET fess_log.search_log/_search
    {
      "size": 0,
      "query": {
        "bool": {
          "filter": [ { "range": { "requestedAt": { "gte": "now-2y/d" } } } ],
          "must_not": [ { "term": { "accessType": "admin" } } ]
        }
      },
      "aggs": {
        "per_month": {
          "date_histogram": {
            "field": "requestedAt",
            "calendar_interval": "month",
            "time_zone": "Asia/Tokyo"
          },
          "aggs": {
            "zero_hit": { "filter": { "term": { "hitCount": 0 } } },
            "zero_hit_rate": {
              "bucket_script": {
                "buckets_path": { "zero": "zero_hit>_count", "total": "_count" },
                "script": "params.zero / params.total"
              }
            }
          }
        }
      }
    }

Jeder Monats-Bucket liefert die Anzahl der Suchen (``doc_count``), die Anzahl der Suchen ohne Treffer (``zero_hit.doc_count``) und die Quote ohne Treffer (``zero_hit_rate.value``, zwischen 0 und 1).
Mit ``time_zone`` beginnen die Monate um Mitternacht in der angegebenen Zeitzone (hier ``Asia/Tokyo``; ersetzen Sie sie durch Ihre eigene), und ``must_not`` schließt Suchen aus der Administrationsoberfläche aus.
Ob Protokolle für zwei Jahre vorhanden sind, hängt von den Aufbewahrungseinstellungen im nächsten Abschnitt ab.

Aufbewahrung und personenbezogene Daten
=======================================

Standardmäßig werden Suchprotokolle unbegrenzt aufbewahrt.
Der Grund ist, dass „Alte Suchprotokolle löschen“ unter [System] > [Allgemein] standardmäßig auf ``-1`` (nicht löschen) steht.
Geben Sie eine Anzahl von Tagen an, löscht der täglich um Mitternacht laufende Job „Log Purger“ Suchprotokolle, die älter als diese Anzahl von Tagen sind.
Klick-, Favoriten- und Chat-Protokolle werden nach derselben Anzahl von Tagen gelöscht.
Benutzerdatensätze werden über eine eigene Einstellung, „Alte Benutzerprotokolle löschen“, gesteuert; auch sie steht standardmäßig auf ``-1``.

Legen Sie die Anzahl der Tage fest, indem Sie abwägen, wie weit Sie Verläufe zurückverfolgen möchten und welche Regeln in Ihrer Organisation für personenbezogene Daten gelten.
Suchprotokolle enthalten die ID des angemeldeten Benutzers (``user`` und die mit ``1`` beginnenden Werte von ``roles``), die IP-Adresse und den User-Agent.
Außerdem werden standardmäßig URLs und Titel der in den Suchergebnissen angezeigten Dokumente im Feld ``documents`` gespeichert (``logging.search.docs.enabled=true``).
All das ist in OpenSearch Dashboards sichtbar; halten Sie sich daher an die eingangs beschriebenen Zugriffsbeschränkungen.

Fehlerbehebung
==============

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptom
     - Zu prüfen
   * - In Discover oder in Visualisierungen erscheinen keine Daten
     - Ob der Zeitraum oben rechts die Zeitpunkte der Protokolle umfasst. Nach einer Suche kann es etwa eine Minute dauern, bis das Protokoll geschrieben ist (es schreibt der minütlich laufende Job „Log Aggregator“)
   * - ``rank`` oder ``searchField.label`` lässt sich nicht auswählen
     - Ob Sie ``fess_log*`` verwenden. Legen Sie ein eigenes Index-Pattern an oder klicken Sie auf [Refresh field list]
   * - Die Anzahlen sind höher als auf der Seite [Suchprotokoll]
     - Ob ``fess_log*`` auch Klick- oder Chat-Protokolle mitzählt. Ob der Filter nach Zugriffstyp und die Zeitzone der Tagesgrenzen übereinstimmen
   * - Es werden wenige Klicks gezählt
     - Die Links laufen nicht über ``/go/``, „Suchprotokoll“ unter [Allgemein] ist deaktiviert, oder der Browser öffnet ``/go/`` ohne Fess-Sitzung. Prüfen Sie auch die Voraussetzungen in :doc:`guide-08`

Weiterführende Artikel
======================

- Gefundene Suchbegriffe mit Synonymen oder Schlüsselübereinstimmungen verbessern: :doc:`guide-08`
- Den Entwurf von Rollen und Gruppen überprüfen: :doc:`guide-05`
- Den Betrieb einschließlich Überwachung und Sicherung einrichten: :doc:`guide-10`
- Festlegen, was in jeder Phase einer unternehmensweiten Einführung gemessen wird: :doc:`guide-23`

Referenzen
==========

- `Suchprotokoll <https://fess.codelibs.org/de/stable/admin/searchlog-guide.html>`__
- `Konfiguration der Suchprotokoll-Visualisierung <https://fess.codelibs.org/de/stable/config/admin-opensearch-dashboards.html>`__
- `Allgemein <https://fess.codelibs.org/de/stable/admin/general-guide.html>`__
- `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__
- `Compose-Dateien von docker-fess (GitHub) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
- `OpenSearch Dashboards <https://opensearch.org/docs/latest/dashboards/index/>`__
