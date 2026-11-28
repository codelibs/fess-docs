==================================================
Bilder und Text gemeinsam durchsuchen (multimodal)
==================================================

Einleitung
==========

Auf Dateiservern und internen Websites liegen große Mengen an Bildern wie Produkt- oder Baustellenfotos, zu deren Inhalt es außer dem Dateinamen keinerlei Anhaltspunkt gibt.
Mit der Stichwortsuche lassen sich Bilder nur über Wörter finden, die im Dateinamen oder in den Metadaten vorkommen.

Mit dem Plugin für multimodale Suche ``fess-webapp-multimodal`` können Sie mit Wörtern wie „Sonnenuntergang in den Bergen“ oder „Hund“ nach Bildern suchen, deren Inhalt diesen Wörtern nahekommt.
In diesem Artikel gehen wir mit Fess 15.9 folgende Schritte durch.

- Die Docker-Umgebung ``docker-multimodalsearch`` zum Ausprobieren in der Version 15.9 starten, Bilder crawlen und durchsuchen
- Anhand der Antwort der Such-API bestätigen, dass Bilder über die Vektorsuche gefunden wurden
- Die Einstellungen für die Integration in ein bestehendes Fess und typische Stolpersteine kennenlernen

Was möglich ist und was nicht
=============================

Zunächst grenzen wir den Funktionsumfang von ``fess-webapp-multimodal`` in 15.9 ab.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Punkt
     - Verhalten in 15.9
   * - Suchrichtung
     - Nur die Suche nach Bildern per Text. Eine Funktion, mit der man ein Bild hochlädt und ähnliche Bilder sucht, gibt es nicht
   * - Vektorisierte Bilder
     - Nur Dateien mit dem MIME-Typ ``image/gif``, ``image/jpeg`` oder ``image/png``. BMP und TIFF werden nicht vektorisiert
   * - Bilder in PDF- oder Office-Dokumenten
     - Werden nicht vektorisiert. Um Text in Bildern zu durchsuchen, verwenden Sie OCR (eine separate Funktion)
   * - Dokumente, die keine Bilder sind
     - Werden wie gewohnt per Stichwortsuche (BM25) gefunden. In den Suchergebnissen erscheinen Bilder und Textdokumente gemischt
   * - Suchbegriffe in anderen Sprachen als Englisch (z. B. Deutsch)
     - Erfordern ein mehrsprachiges CLIP-Modell. Das Standardmodell von ``docker-multimodalsearch`` ist laut README ein mehrsprachiges Modell, das nicht auf Englisch beschränkt ist (die README nennt als Beispiel Japanisch)
   * - Semantische Suche über Text
     - Kann nicht im selben Fess verwendet werden (siehe unten)

Zu OCR siehe `OCR-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-ocr.html>`__.

Funktionsweise
==============

CLIP ist ein Modell, das Text und Bilder in denselben Vektorraum überführt.
Der Vektor des Texts „Hund“ liegt in der Nähe der Vektoren von Bildern, auf denen ein Hund zu sehen ist; daher lassen sich Bilder über die Nähe der Vektoren zueinander suchen.

Seit Fess 15.8 übernimmt Fess selbst das Speichern und Durchsuchen der Vektoren.
Das Plugin ergänzt nur die Kommunikation mit dem CLIP-Server.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Zeitpunkt
     - Verarbeitung
   * - Beim Crawlen
     - GIF-, JPEG- und PNG-Bilder werden an den CLIP-Server gesendet, in Vektoren umgewandelt und in das Vektorfeld ``content_chunk_vector`` von Fess geschrieben
   * - Bei der Suche
     - Der Suchbegriff wird vom CLIP-Server in einen Vektor umgewandelt, und es wird nach nahe gelegenen Bildern gesucht. Diese Suche läuft parallel zur Stichwortsuche, und beide werden per Rank Fusion zu einem Ergebnis zusammengeführt
   * - Ergebnis
     - Dokumente, die über die Vektorsuche gefunden wurden, tragen im Feld ``searcher`` den Wert ``multi_modal``. Per Stichwortsuche gefundene Dokumente tragen ``default``

Zur Funktionsweise von Rank Fusion siehe `Hybride Suche und Rank Fusion (Semantisch + Schlüsselwort) <https://fess.codelibs.org/de/stable/config/rank-fusion.html>`__.

Mit docker-multimodalsearch ausprobieren
========================================

``docker-multimodalsearch`` ist eine Docker-Compose-Umgebung, die die benötigten Container und Einstellungen bündelt, damit Sie die multimodale Suche sofort ausprobieren können.
Mit dem Tag ``v15.9.0`` starten die folgenden Dienste.

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - Dienst
     - Aufgabe
   * - ``fess01``
     - Fess selbst. Das Image ist ``ghcr.io/codelibs/fess:15.9.0-noble``; beim Start wird das Plugin ``fess-webapp-multimodal:15.9.0`` eingebunden. Die Suchseite verwendet das Bildergalerie-Theme ``mosaic``
   * - ``search01``
     - OpenSearch 3.9.0. Port 9200 wird nur auf der Loopback-Schnittstelle des Hosts (127.0.0.1) veröffentlicht
   * - ``clip_server``
     - Der CLIP-Server. Das Standardmodell ist das mehrsprachige ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k`` (512 Dimensionen) und läuft auf der CPU
   * - ``content``
     - nginx, das Beispielbilder unter ``http://content/`` ausliefert. Erreichbar nur aus dem Netzwerk zwischen den Containern
   * - ``init-fess-verify``
     - Läuft beim Start einmalig, prüft, ob das Vektorfeld des Index den Einstellungen entspricht, und beendet sich

Vorbereitung
------------

- Docker (Befehl ``docker compose``), Git, bash
- Eine Internetverbindung (zum Abrufen der Images und des CLIP-Modells; laut README ist das Modell etwa 1,6 GB groß)
- Unter Linux ``vm.max_map_count`` für OpenSearch erhöhen (wie in den Vorbereitungsschritten von :doc:`guide-02`)

Die Version 15.9 beziehen
-------------------------

Der Standard-Branch von ``docker-multimodalsearch`` folgt der nächsten, noch in Entwicklung befindlichen Version; geben Sie daher beim Klonen den Tag ``v15.9.0`` an.

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

Öffnen Sie ``.env`` und stellen Sie die Quelle der Themes auf den Branch für 15.9 um.

::

    FESS_THEMES_REF=15.9.x

In ``v15.9.0`` steht in ``.env.example`` noch ``FESS_THEMES_REF=main``, das ``mosaic``-Theme auf ``main`` von ``fess-themes`` ist inzwischen jedoch für Fess 15.10 und neuer bestimmt (``minFessVersion: 15.10``).
Das ``mosaic``-Theme für 15.9 liegt im Branch ``15.9.x``.

Lassen Sie ``FESS_VERSION=15.9.0`` und ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0`` in ``.env`` unverändert.
Die Plugin-Version muss mit der Fess-Version übereinstimmen.

Einrichten und starten
----------------------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh`` legt die Datenverzeichnisse an, holt das Theme und bereitet das Skript zur Erzeugung der Miniaturansichten vor.
Beim ersten ``docker compose up -d`` wird das Image von ``clip_server`` gebaut und das CLIP-Modell heruntergeladen.
``fess01`` wartet mit dem Start, bis ``clip_server`` bereit ist; der erste Start dauert daher einige Minuten.

Den Status prüfen Sie mit den folgenden Befehlen.

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

Wenn ``fess01`` den Status ``(healthy)`` erreicht, ``init-fess-verify`` mit ``Exited (0)`` endet und das Log die folgende Zeile enthält, wurde das Vektorfeld wie konfiguriert angelegt.

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

Die Beispielbilder crawlen
--------------------------

Laden Sie die Beispielbilder (Tiere, Fahrzeuge, Speisen, Natur, Gebäude) sowie HTML- und PDF-Dateien herunter.

::

    $ bash bin/fetch-sample-images.sh

Crawlen Sie anschließend über die Administrationsoberfläche.

1. Melden Sie sich unter ``http://localhost:8080/admin/`` mit ``admin`` / ``admin`` an und legen Sie bei Aufforderung ein neues Passwort fest
2. Klicken Sie unter [Crawler] > [Web] auf [Neu erstellen], geben Sie bei „Name“ ``content`` und bei „URLs“ ``http://content/`` ein und klicken Sie auf [Erstellen]
3. Öffnen Sie unter [System] > [Scheduler] den Job „Default Crawler“ und klicken Sie auf [Jetzt starten]
4. Warten Sie unter [Systeminformationen] > [Crawling-Informationen], bis das Crawlen abgeschlossen ist

Die Bildvektoren werden während dieses Crawl-Vorgangs geschrieben.
Laut README werden mit den mitgelieferten Beispielen 43 Dokumente registriert (37 Bilder, 5 HTML, 1 PDF).
Die Anzahl ist ein Richtwert.

Suchen
------

Öffnen Sie ``http://localhost:8080/`` und suchen Sie nach ``Hund``, ``Sonnenuntergang in den Bergen`` oder ``mountain sunset``.
Das Standardmodell ist mehrsprachig, daher werden sowohl bei deutschen als auch bei englischen Suchbegriffen Bilder zurückgegeben.

Das ``mosaic``-Theme zeigt die Ergebnisse als Galerie von Miniaturansichten an und versieht jedes Ergebnis mit dem Badge „Stichwort“, „Visuell“ oder „Mischung“.
„Visuell“ steht für Bildähnlichkeit, „Mischung“ für Ergebnisse, die sowohl per Stichwort als auch über das Bild gefunden wurden.

Die Miniaturansichten werden nach dem Crawlen von einem Hintergrund-Job erzeugt.
Werden direkt nach dem Crawlen einige davon nicht angezeigt, warten Sie kurz und laden Sie die Seite neu.

Zum Beenden führen Sie ``docker compose down`` aus.
Die Daten bleiben unter ``./data`` erhalten.

Das Verhalten prüfen
====================

``searcher`` in der Such-API ansehen
------------------------------------

Ob die Vektorsuche verwendet wurde, erkennen Sie am Feld ``searcher`` in der Antwort der Such-API.
Wenn ``jq`` installiert ist, führen Sie Folgendes aus.

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=Hund' | jq -c '.response.data[] | {url, searcher}'

Die Werte von ``searcher`` bedeuten Folgendes.

- ``["multi_modal"]``: über Bildähnlichkeit gefunden
- ``["default"]``: per Stichwortsuche gefunden
- Beide enthalten: auf beiden Wegen gefunden

Haben alle Ergebnisse nur ``["default"]``, wurde die Vektorsuche nicht ausgeführt.
Prüfen Sie, ob einer der Fälle aus dem folgenden Abschnitt „Suchen, bei denen die Vektorsuche nicht ausgeführt wird“ zutrifft.

``searcher`` ist standardmäßig nicht in der API-Antwort enthalten.
``docker-multimodalsearch`` setzt ``query.additional.api.response.fields=searcher`` aus ``fess_config.properties`` als Startoption (``-Dfess.config.query.additional.api.response.fields=searcher``), daher ist das Feld in der Antwort enthalten.
Einzelheiten zur Such-API finden Sie unter `Such-API <https://fess.codelibs.org/de/stable/api/api-search.html>`__.

Prüfen, ob Vektoren geschrieben wurden
--------------------------------------

Wenn die Suche überhaupt keine Bilder liefert, zählen Sie in OpenSearch die Dokumente mit Vektoren (Port 9200 dieser Umgebung ist nur vom Host aus nutzbar).

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

Ist ``count`` gleich 0, wurden beim Crawlen keine Vektoren erzeugt.
Prüfen Sie in ``docker compose logs fess01`` und in den Crawler-Logs, ob die Warnung ``Failed to convert an image to a vector.`` erscheint.

Suchen, bei denen die Vektorsuche nicht ausgeführt wird
-------------------------------------------------------

In den folgenden Fällen wird die Vektorsuche nicht ausgeführt, und das Ergebnis stammt allein aus der Stichwortsuche.
Da kein Fehler gemeldet wird, fällt dies leicht nicht auf.

- Suchen mit vorgegebener Sortierreihenfolge (Parameter ``sort``). Wenn Sie unter [System] > [Allgemein] einen „Standard-Sortierwert“ festlegen, sendet das ``mosaic``-Theme diesen Wert als ``sort``; dann fallen auch normale Suchen unter diesen Fall
- Suchen mit Suchsyntax im Suchbegriff: Phrasen (``"Sonnenuntergang in den Bergen"``), Platzhalter (``dog*``), Gewichtung (``dog^2``), Ausschluss (``-dog``), ``allintitle:``, ``allinurl:``
- Suchen ohne Suchbegriff, die nur Filterbedingungen wie Labels enthalten
- Seiten ab dem 101. Ergebnis (wenn die Startposition mindestens die Hälfte von ``rank.fusion.window_size`` (Standardwert 200) beträgt)
- Wenn der CLIP-Server nicht erreichbar ist (``fess.log`` enthält eine WARN-Meldung wie ``Embedding provider is unavailable``)

Verwenden Sie dagegen zusammen mit dem Suchbegriff eine Feldangabe wie ``filetype:jpg`` oder einen Label-Filter, wird die Vektorsuche ausgeführt und durch diese Bedingung eingeschränkt.

In ein bestehendes Fess integrieren
===================================

Um die Funktion ohne ``docker-multimodalsearch`` in ein bestehendes Fess 15.9 zu integrieren, gehen Sie wie folgt vor.

1. Das Plugin installieren
--------------------------

Installieren Sie ``fess-webapp-multimodal`` 15.9.x auf einem der folgenden Wege und starten Sie Fess anschließend neu.

- In der Administrationsoberfläche unter [System] > [Plugin] > [Installieren]
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- Bei Docker ``fess-webapp-multimodal:15.9.0`` zur Umgebungsvariablen ``FESS_PLUGINS`` hinzufügen

Einzelheiten finden Sie unter `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__.

2. Einen CLIP-Server bereitstellen
----------------------------------

Das Plugin verbindet sich mit einer HTTP-API im selben Format wie der CLIP-Server von Jina.
Für die Vektorisierung wird ``POST /post`` verwendet, für die Verbindungsprüfung ``GET /health``.
Liefert ``/health`` keinen 2xx-Status, läuft das Plugin mit deaktivierter Vektorsuche weiter.
Das Ziel wird mit ``content_chunker.embedding.clip.api.url`` angegeben; der Standardwert ist ``http://localhost:51000``.

- ``docker/compose.yaml`` im Repository des Plugins startet ``jinaai/clip-server``. Die Konfiguration ``docker/clip_config.yaml`` gibt kein Modell an, daher wird das Standardmodell verwendet (laut README ViT-B/32 mit 512 Dimensionen). Außerdem setzt diese Compose-Datei eine GPU voraus
- Für Suchbegriffe in anderen Sprachen als Englisch (z. B. Deutsch) stellen Sie einen Server mit einem mehrsprachigen Modell bereit, etwa wie ``docker/clip-server`` aus ``docker-multimodalsearch``

3. In system.properties konfigurieren
-------------------------------------

Die Einstellungen der multimodalen Suche gehören in ``system.properties``.
Die Datei liegt beim ZIP-Paket unter ``app/WEB-INF/conf/system.properties``, bei den RPM/DEB-Paketen unter ``/etc/fess/system.properties`` und bei Docker unter ``/opt/fess/system.properties``.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- Setzen Sie ``content_chunker.embedding.dimension`` auf die Anzahl der Dimensionen, die das CLIP-Modell ausgibt (512 bei der ViT-B/32-Familie)
- ``content_chunker.search.enabled`` wird nur beim Start gelesen; starten Sie Fess nach der Einstellung daher neu
- Um die Werte als Startoptionen zu übergeben, verwenden Sie ``-Dfess.system.<Schlüssel>``. Einträge in ``fess_config.properties`` oder als ``-Dfess.config.<Schlüssel>`` werden ohne jede Warnung ignoriert
- Werte in ``system.properties`` haben Vorrang vor ``-Dfess.system.*``. Ist ein Schlüssel an beiden Stellen gesetzt, wird der Wert aus der Datei verwendet
- In den Compose-Dateien von docker-fess hat ``fess01`` kein Volume, sodass ``docker compose down`` die ``system.properties`` verwirft. Bei Docker ist es am zuverlässigsten, ``-Dfess.system.<Schlüssel>=<Wert>`` in der Umgebungsvariablen ``FESS_JAVA_OPTS`` aufzuführen (auch die ``compose.yaml`` von ``docker-multimodalsearch`` macht es so)

Die Liste der Schlüssel finden Sie unter „Konfigurationsreferenz“ in `Semantische Suche (Content-Chunking + Vektorsuche) <https://fess.codelibs.org/de/stable/config/search-semantic.html>`__.
Die multimodale Suche verwendet dieselben ``content_chunker.*``-Schlüssel.

4. Den Index neu erstellen
--------------------------

Das Mapping des Vektorfelds ``content_chunk_vector`` wird beim Anlegen des Index mit der dann eingestellten Anzahl an Dimensionen erstellt.
Falls Sie Fess vor den obigen Einstellungen schon einmal gestartet haben, führen Sie unter [Systeminformationen] > [Wartung] die „Neuindizierung“ mit aktivierter Option „Aliase ersetzen“ aus.
Einzelheiten finden Sie unter `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__.

5. Miniaturansichten aktivieren
-------------------------------

Bei der Bildsuche lassen sich die Ergebnisse ohne Miniaturansichten nicht unterscheiden.
Miniaturansichten sind standardmäßig deaktiviert.

- Aktivieren Sie unter [System] > [Allgemein] die Option „Miniaturansicht anzeigen“ und speichern Sie
- Für Miniaturansichten von Bildern, PDF- und Office-Dokumenten sind externe Werkzeuge wie ImageMagick nötig. Sie sind im Standard-Docker-Image (Alpine) nicht enthalten; verwenden Sie daher ein ``-noble``-Image (z. B. ``ghcr.io/codelibs/fess:15.9.0-noble``)

Die benötigten Werkzeuge finden Sie unter `Konfiguration von Thumbnail-Bildern <https://fess.codelibs.org/de/stable/config/crawler-thumbnail.html>`__.

6. Crawlen und prüfen
---------------------

Crawlen Sie eine Website oder einen Ordner mit GIF-, JPEG- oder PNG-Bildern.
Die Bildvektoren werden beim Crawlen geschrieben.

Um ``searcher`` in der Such-API zu prüfen, setzen Sie in ``fess_config.properties`` ``query.additional.api.response.fields=searcher`` (als Startoption ``-Dfess.config.query.additional.api.response.fields=searcher``).

Lassen Sie den Job „Content Chunk Vector Indexer“ im Scheduler deaktiviert (er ist standardmäßig deaktiviert).
Die Bildvektoren schreibt der Crawler, daher wird dieser Job nicht benötigt.
Wenn Sie ihn aktivieren, werden auch Textdokumente mit der Textseite von CLIP vektorisiert, und das Feld ``content`` wird aufgeteilt.

Hinweise für den Betrieb
========================

Keine Kombination mit der semantischen Suche über Text
------------------------------------------------------

Das Plugin ersetzt die Suchverarbeitung der semantischen Suche von Fess (``semanticChunkSearcher``) durch eine für CLIP.
Außerdem kann ``content_chunker.embedding.name`` nur einen Wert enthalten.
Deshalb lassen sich die semantische Suche über Text aus :doc:`guide-18` und die multimodale Suche nicht gleichzeitig in einem Fess verwenden.
Wenn Sie beides benötigen, bauen Sie getrennte Fess-Instanzen auf.

Beachten Sie außerdem: Wenn Sie die verwendeten Suchverarbeitungen mit ``rank.fusion.searchers`` einschränken, wird die Vektorsuche ausgeschlossen, sofern ``multi_modal`` nicht enthalten ist.
Lassen Sie diese Einstellung normalerweise leer.

Beim Modellwechsel bis zum erneuten Crawlen gehen
-------------------------------------------------

Ändern Sie Modell und Anzahl der Dimensionen immer gemeinsam.
Die Anzahl der Dimensionen wird beim Anlegen des Index im Mapping festgeschrieben; nach der Änderung sind daher folgende Schritte nötig.

1. Unter [Systeminformationen] > [Wartung] die „Neuindizierung“ (mit aktivierter Option „Aliase ersetzen“) ausführen und den Index mit der neuen Anzahl an Dimensionen neu erstellen
2. Erneut crawlen

Die Neuindizierung kopiert nur die Dokumente und berechnet die Vektoren nicht neu.
Auch bei gleicher Anzahl an Dimensionen ändert sich mit einem anderen Modell oder CLIP-Server der Vektorraum; löschen Sie daher die Dokumente und crawlen Sie erneut.
In ``docker-multimodalsearch`` ändern Sie ``CLIP_MODEL_NAME`` und ``MULTIMODAL_DIMENSION`` in ``.env``.
Das Vorgehen ist im Abschnitt „Model swap“ der README beschrieben.

CPU und GPU
-----------

Das Standardmodell von ``docker-multimodalsearch`` (512 Dimensionen) ist für den Betrieb auf der CPU ausgelegt; ``CLIP_DEVICE=cpu`` ist der Standard.
Beim Wechsel auf das größere ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k`` (1024 Dimensionen) wird eine GPU empfohlen; mit ``CLIP_DEVICE=auto`` wird eine GPU verwendet, sofern vorhanden.

Zusammenfassung
===============

- ``fess-webapp-multimodal`` sucht GIF-, JPEG- und PNG-Bilder per Text. Die Suche per Bild und die Vektorisierung von in Dokumente eingebetteten Bildern sind nicht möglich
- Zum Ausprobieren verwenden Sie ``v15.9.0`` von ``docker-multimodalsearch`` und geben ``FESS_THEMES_REF=15.9.x`` an
- Die Einstellungen ``content_chunker.*`` gehören in ``system.properties`` (oder als ``-Dfess.system.*``)
- Ob die Vektorsuche verwendet wurde, erkennen Sie an ``multi_modal`` in ``searcher`` der Such-API
- Suchbegriffe in anderen Sprachen als Englisch (z. B. Deutsch) erfordern ein mehrsprachiges Modell, und die semantische Suche über Text lässt sich nicht im selben Fess mitverwenden

Weiterführende Artikel
======================

- :doc:`guide-18` — Textdokumente per Vektor durchsuchen (eine von der multimodalen Suche getrennte Konfiguration)
- :doc:`guide-02` — Grundlagen zum Betrieb von Fess mit Docker
- :doc:`guide-11` — Mit der Such-API an Geschäftssysteme anbinden

Referenzen
==========

- `docker-multimodalsearch (v15.9.0) <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal (15.9.0) <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
