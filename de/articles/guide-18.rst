==================================================
Semantische Suche: Dokumente nach Bedeutung finden
==================================================

Einleitung
==========

Sucht ein Benutzer nach „mein Lohn soll auf eine andere Bank gehen“, die interne Richtlinie heißt aber „Änderung des Gehaltskontos“, findet die Schlüsselwortsuche sie nicht.
In Fess 15.9 ist die „semantische Suche“, die Texte in Vektoren umwandelt, die ihre Bedeutung abbilden, und damit sucht, fest in den Kern integriert und funktioniert ohne Plugin (je nachdem, wo das Embedding-Modell läuft, fügen Sie ein Plugin hinzu).

Wenn Sie die Schritte in diesem Artikel ausführen, können Sie Folgendes:

- Erkennen, wann die semantische Suche hilft und wann die Schlüsselwortsuche genügt
- Mit Docker sofort eine Umgebung starten, in der die semantische Suche bereits konfiguriert ist
- In einem bestehenden Fess ``content_chunker.*`` konfigurieren und mit dem Indexer-Job Vektoren erzeugen
- Anhand des Feldes ``searcher`` prüfen, ob ein Suchergebnis durch die Vektorsuche gefunden wurde

Die Konfiguration des KI-Suchmodus (RAG) wird in :doc:`guide-19` behandelt.

Wann die semantische Suche hilft
================================

Die semantische Suche von Fess ersetzt die Schlüsselwortsuche (BM25) nicht.
Sie arbeitet als „hybride Suche“: Schlüsselwortsuche und Vektorsuche werden beide ausgeführt, und die Ergebnisse werden mit Rank Fusion (RRF) zu einer einzigen Rangfolge zusammengeführt.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Die semantische Suche hilft
     - Die Schlüsselwortsuche genügt
   * - Benutzer und Dokumente verwenden unterschiedliche Wörter („Bank für den Lohn“ und „Gehaltskonto“, „Homeoffice“ und „Telearbeit“)
     - Suche nach derselben Zeichenkette wie im Dokument, etwa Produktmodellnummern, Fehlercodes oder Personennamen
   * - Fragen als Satz stellen („Wie beantrage ich einen neuen PC“)
     - Es gibt nur wenige Umschreibungen, und sie lassen sich vollständig in einem Synonymwörterbuch erfassen
   * - Auf Deutsch suchen und englische Dokumente finden (erfordert ein mehrsprachiges Embedding-Modell)
     - Verwendung von Suchsyntax wie Phrasen oder Platzhaltern (in diesem Fall wird die Vektorsuche gar nicht ausgeführt)

Wenn die Zahl der Umschreibungen begrenzt ist, ist es einfacher, zuerst ein Synonymwörterbuch auszuprobieren.
Wie Sie Synonyme anhand der Begriffe ohne Treffer im Suchprotokoll registrieren, lesen Sie in :doc:`guide-08`.

Der Verarbeitungsablauf in Fess
===============================

#. Der Crawler registriert Dokumente wie gewohnt im Index. Zu diesem Zeitpunkt gibt es noch keine Vektoren.
#. Der Scheduler-Job ``Content Chunk Vector Indexer`` findet unverarbeitete Dokumente, teilt den Text in Chunks (Abschnitte) auf, erzeugt für jeden Chunk einen Embedding-Vektor und speichert ihn im Feld ``content_chunk_vector``. Das Ergebnis wird im Feld ``content_chunk_status`` festgehalten.
#. Bei ``content_chunker.search.enabled=true`` werden bei jeder Suche die Schlüsselwortsuche (Searcher-Name ``default``) und die Vektorsuche (Searcher-Name ``semantic_chunk``) ausgeführt und mit RRF fusioniert.

Dieser Job ist standardmäßig deaktiviert und nicht mit dem Crawling verknüpft.
Beachten Sie, dass allein durch das Eintragen der Einstellungen keine Vektoren entstehen und die Suchergebnisse weiterhin reine Schlüsselwortsuche bleiben.

Voraussetzungen
===============

**OpenSearch mit dem k-NN-Plugin**

Der von Fess 15.9 erstellte Suchindex enthält ein Feld vom Typ ``knn_vector``, unabhängig davon, ob Sie die semantische Suche verwenden.
Das Docker-Image ``ghcr.io/codelibs/fess-opensearch`` und die Standarddistribution von OpenSearch enthalten das k-NN-Plugin.
Mit der minimal-Distribution, die das k-NN-Plugin nicht enthält, kann der Index nicht erstellt werden, und Fess startet nicht.

**Embedding-Anbieter**

Mit ``content_chunker.embedding.name`` wählen Sie, wo das Modell läuft, das Texte in Vektoren umwandelt.

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - Wert
     - Voraussetzung
     - Beschreibung
   * - ``opensearch`` (Standard)
     - Kein zusätzliches Plugin
     - Verwendet ein in OpenSearch ML Commons bereitgestelltes Modell
   * - ``ollama``
     - Plugin ``fess-llm-ollama``
     - Verwendet ein Embedding-Modell von Ollama (Standardmodell: ``embeddinggemma``)
   * - ``openai``
     - Plugin ``fess-llm-openai``
     - Verwendet die Embedding-API von OpenAI (Standardmodell: ``text-embedding-3-small``)
   * - ``gemini``
     - Plugin ``fess-llm-gemini``
     - Verwendet die Embedding-API von Google Gemini
   * - ``bedrock``
     - Plugin ``fess-llm-bedrock``
     - Verwendet ein Embedding-Modell von Amazon Bedrock

Installieren Sie das Plugin in derselben Minor-Version wie Fess (15.9.x) und starten Sie Fess nach der Installation neu.
OpenAI, Gemini und Bedrock werden nutzungsabhängig abgerechnet; beim ersten Joblauf fallen die Kosten für alle vorhandenen Dokumente auf einmal an.

Der schnellste Weg: mit docker-semanticsearch ausprobieren
==========================================================

Das Repository docker-semanticsearch startet mit Docker Compose ein Fess 15.9, in dem die semantische Suche bereits konfiguriert ist.
Es stellt automatisch ein mehrsprachiges Embedding-Modell (``paraphrase-multilingual-MiniLM-L12-v2``, 384 Dimensionen) in OpenSearch ML Commons bereit und aktiviert sogar den Indexer-Job.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh`` lädt das Theme ``semanticlens`` für die Suchseite aus dem Repository ``fess-themes``.
Das Theme auf ``main``, der Standardquelle von ``v15.9.0``, ist für Fess 15.10 und neuer bestimmt (``minFessVersion: 15.10``); deshalb wird mit ``FESS_THEMES_REF`` der Branch ``15.9.x`` angegeben, der das Theme für 15.9 enthält.

Beim ersten Start dauert das Herunterladen des Modells (etwa 490MB) einige Minuten.
Die Umgebung ist bereit, wenn ``docker compose ps -a`` ``fess01`` als healthy und ``init-semantic`` sowie ``init-fess-chunk`` als ``Exited (0)`` anzeigt.

Danach legen Sie wie bei einem normalen Fess in der Administrationsoberfläche (``http://localhost:8080/admin``) eine Crawl-Konfiguration an und führen das Crawling aus.
In dieser Umgebung läuft der Indexer-Job stündlich.
Wenn Sie die Vektoren sofort erzeugen möchten, öffnen Sie unter [System] > [Scheduler] den Eintrag ``Content Chunk Vector Indexer`` und klicken auf [Jetzt starten].

Neben den weiter unten in diesem Artikel erläuterten Einstellungen verwendet diese Umgebung folgende Werte:

- Die Fusion erfolgt auf der OpenSearch-Seite (``rank.fusion.engine.enabled=true``)
- Die Chunk-Länge beträgt 250 Zeichen (weil das Eingabelimit des Modells 128 Token beträgt)
- Untergrenze der Ähnlichkeit ``content_chunker.search.min_score=0.5``
- Das Theme ``semanticlens``, das bei jedem Suchergebnis anzeigt, ob es durch Schlüsselwortsuche, semantische Suche oder beide gefunden wurde

Wie Sie die Werte ändern, lesen Sie im Abschnitt Configuration der README des Repositorys.

Die semantische Suche in einem bestehenden Fess aktivieren
==========================================================

Hier werden die Schritte am Beispiel von ``embeddinggemma`` von Ollama (768 Dimensionen, mehrsprachig) gezeigt.
Wenn Sie den eingebauten Anbieter ``opensearch`` verwenden, stellen Sie statt der Schritte 1 und 2 ein Modell in ML Commons bereit und setzen ``content_chunker.embedding.name=opensearch`` sowie ``content_chunker.embedding.opensearch.model.id``.
Das Verfahren finden Sie unter „Einrichtungsverfahren (Beispiel mit dem Anbieter opensearch)“ in `Semantische Suche <https://fess.codelibs.org/de/stable/config/search-semantic.html>`__.

Schritt 1: Das Plugin installieren
----------------------------------

Wählen Sie unter [System] > [Plugin] > [Installieren] ``fess-llm-ollama`` in der Version 15.9.x aus, installieren Sie es und starten Sie Fess neu.
Bei Docker geben Sie in ``compose.yaml`` für ``fess01`` ``FESS_PLUGINS=fess-llm-ollama:15.9.0`` an.

Schritt 2: Das Embedding-Modell vorbereiten
-------------------------------------------

Laden Sie das Modell auf dem Server herunter, auf dem Ollama läuft.

::

    $ ollama pull embeddinggemma

Schritt 3: Die Einstellungen in system.properties eintragen
-----------------------------------------------------------

Die Einstellungen ``content_chunker.*`` werden ausschließlich aus ``system.properties`` gelesen.
In ``fess_config.properties`` oder mit ``-Dfess.config.`` angegeben, werden sie ignoriert.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Installationsart
     - Speicherort
   * - ZIP-Version
     - ``app/WEB-INF/conf/system.properties``
   * - RPM/DEB-Version
     - ``/etc/fess/system.properties``
   * - Docker (docker-fess)
     - In ``compose.yaml`` in ``FESS_JAVA_OPTS`` in der Form ``-Dfess.system.<Schlüssel>=<Wert>`` angeben

``/opt/fess/system.properties`` im Docker-Container wird ebenfalls gelesen, aber ``fess01`` von docker-fess hat kein Volume, sodass die Datei bei ``docker compose down`` verloren geht.

Tragen Sie Folgendes ein:

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url`` ist die Adresse von Ollama aus Sicht von Fess.
Läuft Fess in Docker, verweist ``localhost`` auf den Container selbst; ändern Sie die Adresse daher in eine, die vom Container aus erreichbar ist.

``content_chunker.embedding.dimension`` muss unbedingt mit der Ausgabedimension des Modells übereinstimmen.
Dieser Wert wird beim Erstellen des Index in das Mapping geschrieben und kann später nicht geändert werden.

Schritt 4: Fess neu starten
---------------------------

Die Änderung von ``content_chunker.search.enabled`` auf ``true`` wird erst nach einem Neustart wirksam (die übrigen ``content_chunker.*`` werden während des Betriebs neu eingelesen).

Schritt 5: Den bestehenden Index neu erstellen
----------------------------------------------

In einer Umgebung, in der Fess schon einmal gestartet wurde, ist das Mapping mit der neuen Dimension nicht im Index angekommen.
Aktivieren Sie unter [Systeminformationen] > [Wartung] im Bereich „Neuindizierung“ die Option „Aliase ersetzen“ und klicken Sie auf [Start].
In einer neuen Umgebung, in der Sie Schritt 3 vor dem ersten Start erledigt haben, ist dies nicht nötig.

Die Neuindizierung läuft asynchron im Hintergrund, und der Bildschirm zeigt ihr Ende nicht an.
Bevor Sie mit dem nächsten Schritt fortfahren, prüfen Sie, dass sowohl der Alias ``fess.search`` als auch ``fess.update`` auf den neuen Index (``fess.<Zeitstempel>``) zeigen.

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

Der alte Index wird nicht automatisch gelöscht; löschen Sie ihn nach der Prüfung manuell.
Ein erneutes Crawling ist nicht nötig.
Der Indexer-Job erzeugt die Vektoren aus dem gespeicherten Text.

Schritt 6: Den Indexer-Job aktivieren und ausführen
---------------------------------------------------

#. Öffnen Sie unter [System] > [Scheduler] ``Content Chunk Vector Indexer`` und klicken Sie auf [Bearbeiten].
#. Setzen Sie bei „Status“ das Häkchen bei „Aktiviert“, ändern Sie bei Bedarf den Zeitplan und klicken Sie auf [Aktualisieren]. Der Standardzeitplan ist ``0 13 * * *`` (täglich um 13:00 Uhr).
#. Zurück in der Detailansicht wird [Jetzt starten] angezeigt; klicken Sie darauf, um den Job einmal auszuführen.

Da der Job nicht mit dem Crawling verknüpft ist, sind gecrawlte Dokumente zwar sofort per Schlüsselwort auffindbar, werden aber erst nach dem nächsten Lauf dieses Jobs von der Vektorsuche erfasst.
Legen Sie den Zeitplan auf einen Zeitpunkt nach dem Ende Ihrer Crawl-Jobs.

Funktion prüfen
===============

Prüfen, ob Vektoren erzeugt wurden
----------------------------------

Lassen Sie OpenSearch die Verarbeitungsergebnisse pro Dokument aggregieren.

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Wert
     - Bedeutung
   * - ``pending``
     - Unverarbeitet (wird beim nächsten Joblauf verarbeitet). Erneut gecrawlte Dokumente kehren ebenfalls in diesen Zustand zurück
   * - ``done``
     - Chunk-Aufteilung und Vektorerzeugung abgeschlossen
   * - ``chunked``
     - Nur Chunk-Aufteilung. Diesen Zustand erhalten Dokumente auch, wenn das Plugin des Anbieters nicht installiert ist
   * - ``skipped``
     - Der Text ist leer, oder die Zahl der Chunks hat das Limit (Standard 1000) überschritten
   * - ``fail``
     - Fehlgeschlagen. Prüfen Sie die Ursache in der Protokolldatei ``fess-chunk.log``

Wenn ``pending`` mit jedem Joblauf abnimmt und ``done`` zunimmt, läuft alles wie vorgesehen.

Prüfen, ob ein Ergebnis durch die Vektorsuche gefunden wurde
------------------------------------------------------------

Das Feld ``searcher`` eines Suchergebnisses enthält die Namen der Searcher, die das Dokument gefunden haben.
Standardmäßig ist es nicht in der Antwort der Such-API enthalten; fügen Sie daher die folgende Zeile in ``fess_config.properties`` ein und starten Sie neu (bei Docker ``-Dfess.config.query.additional.api.response.fields=searcher``).

::

    query.additional.api.response.fields=searcher

Suchen Sie mit einer Umschreibung, deren Schlüsselwörter nicht mit dem Dokument übereinstimmen.
Wenn es ein Dokument gibt, das die „Änderung des Gehaltskontos“ erläutert, suchen Sie wie folgt:

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=mein Lohn soll auf eine andere Bank gehen" \
      | jq '.response.data[] | {title, searcher}'

Ein Ergebnis mit ``searcher`` gleich ``["semantic_chunk"]`` wurde nur durch die Vektorsuche gefunden, ``["default", "semantic_chunk"]`` durch beide.
Haben alle Ergebnisse nur ``["default"]``, liefert die Vektorsuche keine Ergebnisse.
Prüfen Sie den nächsten Abschnitt.

Häufige Stolpersteine
=====================

**rank.fusion.searchers aus der Zeit des alten Plugins ist noch gesetzt**

Beim Plugin ``fess-webapp-semantic-search`` für 15.7 und früher wurde ``-Drank.fusion.searchers=default,semantic`` angegeben.
In 15.9 heißt der Searcher ``semantic_chunk``; bleibt diese Einstellung bestehen, wird die semantische Suche nicht ausgeführt, und es werden nur Ergebnisse der Schlüsselwortsuche zurückgegeben.
Beim Start erscheint die WARN-Meldung ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'``.
Prüfen Sie sowohl die JVM-Optionen als auch das Feld „Systemeigenschaft“ unter [System] > [Allgemein] und entfernen Sie diese Einstellung (ohne Angabe werden alle Searcher verwendet).
Wie Sie vom alten Plugin migrieren, lesen Sie unter „Migration von 15.7 oder früheren Versionen“ in `Semantische Suche <https://fess.codelibs.org/de/stable/config/search-semantic.html>`__.

**Bei Abfragen mit Suchsyntax wird die Vektorsuche nicht ausgeführt**

Die folgenden Abfragen werden nur mit der Schlüsselwortsuche verarbeitet:

- Phrasen (``"..."``), Platzhalter, unscharfe Suche und Bereichsangaben
- Sätze, die mit einem ASCII-``?`` enden (z. B. „Was ist ...?“). Das im Japanischen und Chinesischen verwendete Fragezeichen voller Breite „？“ zählt nicht dazu
- Ausschlüsse (``-Wort``, ``NOT Wort``) und Gewichtungen (``Wort^2``)
- Suchen mit angegebener Sortierung

Eingrenzungen mit ``label:``, ``site:`` oder Facetten sind unproblematisch, da sie auch auf die Vektorsuche als Filter angewendet werden.

**Die Dimension stimmt nicht, oder der Index wurde ohne diese Einstellung erstellt**

Wird der Index erstellt, ohne ``content_chunker.embedding.dimension`` zu setzen, erhält das Mapping 768 Dimensionen, und der Job setzt Dokumente auf ``fail``.
Hat das Modell eine andere Dimension als 768, setzen Sie den richtigen Wert und wiederholen die Neuindizierung aus Schritt 5.
``fail`` und ``skipped`` werden auch bei erneutem Joblauf nicht neu verarbeitet.
Nachdem Sie die Ursache behoben haben, setzen Sie vorübergehend ``content_chunker.job.retry_failed=true`` und führen den Job aus.

**Das Embedding-Modell wurde gewechselt**

Die gespeicherten Vektoren wurden mit dem alten Modell erzeugt; wechseln Sie nur das Modell, leidet die Suchgenauigkeit (auch bei gleicher Dimension erscheint kein Fehler).
Das Verfahren, ``content_chunk_vector`` und ``content_chunk_status`` zu löschen und den Job erneut auszuführen, steht unter „Hinweise“ in der Referenz.

**Auch kaum verwandte Dokumente landen weit oben**

Die Vektorsuche liefert Dokumente nach Nähe sortiert, auch solche mit geringer Ähnlichkeit.
Wenn Sie in ``content_chunker.search.min_score`` eine Untergrenze der Kosinusähnlichkeit (0 bis 1) setzen, werden Dokumente ausgeschlossen, die sie nicht erreichen.
Der passende Wert hängt vom Modell und den Dokumenten ab; passen Sie ihn an, während Sie sowohl mit Begriffen, die bisher keine Treffer hatten, als auch mit themenfremden Begriffen suchen.

**Ab der zweiten Hälfte von Seite 2 ändert sich die Art der Ergebnisse**

In der Standardkonfiguration mit Fusion auf der Fess-Seite werden nur die ersten 200 Ergebnisse jedes Searchers (``rank.fusion.window_size``) fusioniert, und ab dem 101. Ergebnis stammen die Ergebnisse nur aus der Schlüsselwortsuche.
Auch die Trefferzahl steigt um die Dokumente, die nur die Vektorsuche gefunden hat.
Zur Funktionsweise der Fusion und zu den Einstellmöglichkeiten (``rank.fusion.rank_constant``, Fusion auf der OpenSearch-Seite) lesen Sie `Hybride Suche und Rank Fusion <https://fess.codelibs.org/de/stable/config/rank-fusion.html>`__.

Zusammenhang mit dem KI-Suchmodus und der multimodalen Suche
============================================================

Der KI-Suchmodus (RAG) lässt sich auch ohne aktivierte semantische Suche nutzen.
Für Dokumente, deren Vektoren mit ``content_chunker.enabled=true`` erzeugt wurden, wird der für die Antwort verwendete Text auf die Chunks eingegrenzt, die der Frage am nächsten sind, sodass auch bei langen Dokumenten die relevanten Teile an das LLM übergeben werden können.
Zur Konfiguration des KI-Suchmodus lesen Sie :doc:`guide-19`.

Die multimodale Suche (``fess-webapp-multimodal``), die Bilder und Texte gemeinsam durchsucht, kann im selben Fess nicht gleichzeitig mit der semantischen Textsuche aus diesem Artikel verwendet werden.
Einzelheiten finden Sie in :doc:`guide-21`.

Weiterführende Artikel
======================

- Begriffe ohne Treffer aus dem Suchprotokoll mit Synonymen und Schlüsselübereinstimmung verbessern: :doc:`guide-08`
- Generative KI aus internen Dokumenten antworten lassen: :doc:`guide-19`
- Auch Bilder durchsuchen: :doc:`guide-21`
- Über die Such-API aus Geschäftssystemen suchen: :doc:`guide-11`

Referenzen
==========

- `Semantische Suche (Content-Chunking + Vektorsuche) <https://fess.codelibs.org/de/stable/config/search-semantic.html>`__
- `Hybride Suche und Rank Fusion (Semantisch + Schlüsselwort) <https://fess.codelibs.org/de/stable/config/rank-fusion.html>`__
- `Ollama-Konfiguration (Lokales LLM / RAG) <https://fess.codelibs.org/de/stable/config/llm-ollama.html>`__
- `Scheduler <https://fess.codelibs.org/de/stable/admin/scheduler-guide.html>`__
- `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch (GitHub) <https://github.com/codelibs/docker-semanticsearch>`__
