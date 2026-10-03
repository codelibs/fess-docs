==================================
OCR-Konfiguration
==================================

Übersicht
=========

|Fess| extrahiert Text aus Dokumenten mit Apache Tika.
Der Tesseract-OCR-Parser von Tika ist in |Fess| enthalten. Wenn Sie ihn aktivieren, erkennt |Fess| Text in Bildern und gescannten PDFs und macht ihn durchsuchbar.

OCR wird ausgeführt, wenn beide der folgenden Bedingungen erfüllt sind:

- Der Befehl ``tesseract`` ist auf dem Host installiert, auf dem der Crawler-Prozess von |Fess| läuft
- OCR ist in |Fess| aktiviert

OCR ist standardmäßig deaktiviert.
Ist ``tesseract`` nicht installiert, überspringt |Fess| die OCR. Es tritt kein Fehler auf.

Wofür OCR gilt
==============

Bei aktivierter OCR gilt sie für Folgendes:

- Bilddateien (PNG, JPEG, TIFF, GIF, BMP usw.)
- In Dokumente eingebettete Bilder, die Tika verarbeitet (z. B. Office-Dateien)
- PDFs mit leerer Textebene (gescannte PDFs)

Behandlung gescannter PDFs
--------------------------

|Fess| extrahiert Text aus PDFs normalerweise mit PDFBox.
Ist OCR aktiviert und erhält PDFBox aus einem PDF überhaupt keinen Text, extrahiert |Fess| das PDF erneut über Tika.
Tika rendert die Seiten als Bilder und führt OCR darauf aus.

.. note::
   PDFs, die bereits Text enthalten, werden nicht per OCR verarbeitet.
   Gemischte PDFs, bei denen nur einige Seiten gescannte Bilder sind, werden nicht abgedeckt.

Tesseract installieren
======================

Installieren Sie Tesseract auf dem Host, auf dem |Fess| läuft.
Um japanischen Text zu erkennen, benötigen Sie außerdem die japanischen Trainingsdaten (traineddata).

Debian / Ubuntu::

    $ sudo apt-get install tesseract-ocr tesseract-ocr-jpn

RHEL / Rocky Linux / AlmaLinux (EPEL zuvor aktivieren)::

    $ sudo dnf install tesseract tesseract-langpack-jpn

Die installierten Sprachen prüfen Sie mit folgendem Befehl::

    $ tesseract --list-langs

OCR aktivieren
==============

Legen Sie in ``fess_config.properties`` die folgenden Eigenschaften fest.

- ZIP-Paket: ``app/WEB-INF/classes/fess_config.properties``
- RPM/DEB-Paket: ``/etc/fess/fess_config.properties``

::

    # OCR aktivieren (Standard: false)
    crawler.document.ocr.enabled=true

    # Tesseract-Sprache(n), mit + verbunden (Standard: eng)
    crawler.document.ocr.language=jpn+eng

    # Timeout in Sekunden für einen Tesseract-Lauf (Standard: 120)
    crawler.document.ocr.timeout=120

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Eigenschaft
     - Standard
     - Beschreibung
   * - ``crawler.document.ocr.enabled``
     - ``false``
     - Mit ``true`` wird OCR aktiviert.
   * - ``crawler.document.ocr.language``
     - ``eng``
     - Tesseract-Sprache(n). Mehrere Sprachen werden mit ``+`` verbunden (z. B. ``jpn+eng``). Die passenden Trainingsdaten (traineddata) müssen installiert sein.
   * - ``crawler.document.ocr.timeout``
     - ``120``
     - Timeout für einen Tesseract-Lauf (ein Bild oder eine PDF-Seite) in Sekunden.

Sie können diese Einstellungen auch als JVM-Systemeigenschaften angeben.
Geben Sie sie zum Beispiel in ``FESS_JAVA_OPTS`` an. Das ist in Docker-Umgebungen praktisch.

::

    -Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng

.. note::
   Starten Sie |Fess| nach einer Änderung dieser Einstellungen neu.

OCR mit Docker verwenden
========================

Um OCR in einer Docker-Umgebung zu nutzen, fügen Sie dem |Fess|-Image Tesseract hinzu.
Erstellen Sie mit ``compose/tesseract/Dockerfile`` aus `docker-fess <https://github.com/codelibs/docker-fess>`__ ein Image mit Tesseract.

Beispiel für ``compose/tesseract/Dockerfile``::

    FROM ghcr.io/codelibs/fess:15.9.0

    RUN apk add --no-cache tesseract-ocr tesseract-ocr-data-osd tesseract-ocr-data-eng tesseract-ocr-data-jpn

Ersetzen Sie in ``compose/compose.yaml`` die Zeile ``image:`` durch ``build: ./tesseract`` und aktivieren Sie die Zeile ``FESS_JAVA_OPTS``.
Das funktioniert genauso wie ``build: ./playwright``.

::

    services:
      fess01:
        # image: ghcr.io/codelibs/fess:15.9.0
        build: ./tesseract
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_JAVA_OPTS=-Dfess.config.crawler.document.ocr.enabled=true -Dfess.config.crawler.document.ocr.language=jpn+eng"

Erstellen Sie nach der Änderung das Image neu und starten Sie die Container::

    $ docker compose up -d --build

.. note::
   Wenn Sie ein Basis-Image verwenden, das nicht auf Alpine basiert (z. B. ``-noble`` oder ``-al2023``), installieren Sie Tesseract statt mit ``apk`` mit dem Paketmanager der jeweiligen Distribution.

Weitere Informationen finden Sie unter :doc:`../install/install-docker`.

Einstellungen pro Crawl-Konfiguration
=====================================

Wenn Sie in den „Konfigurationsparametern“ einer Crawl-Konfiguration ``config.tika.tesseract.config`` angeben, können Sie die OCR-Einstellungen nur für diese Crawl-Konfiguration überschreiben.

::

    config.tika.tesseract.config=tesseract.properties

``tesseract.properties`` ist ein Klassenpfad-Ressourcenname, kein Dateisystempfad.
Legen Sie die Datei im Konfigurationsverzeichnis von |Fess| ab, das im Klassenpfad des Crawlers liegt.

- ZIP-Paket: ``app/WEB-INF/classes/``
- RPM/DEB-Paket: ``/etc/fess/``

In ``tesseract.properties`` schreiben Sie Eigenschaften der Tika-Klasse ``TesseractOCRConfig``.
Zuverlässig angewendet werden nur einfache Schlüssel wie ``language`` und ``timeoutSeconds``.

::

    language=jpn
    timeoutSeconds=300

Für diese Crawl-Konfiguration hat dies Vorrang vor den oben beschriebenen globalen Einstellungen.

Betriebshinweise
================

- OCR ist rechenintensiv und verlangsamt das Crawlen erheblich. Erwägen Sie, die Anzahl der Crawler-Threads zu verringern oder OCR nur für die Crawl-Konfigurationen zu aktivieren, die sie benötigen.
- Bei neuen Web-Crawl-Konfigurationen schließt das standardmäßige Ausschlussmuster Bild-URLs (jpg, png, gif usw.) aus. Um Bilder auf einer Website zu crawlen, entfernen Sie diese aus „Vom Crawlen ausgeschlossene URL“. Beim Dateisystem-Crawl werden Bilder berücksichtigt.
- Auch die Größenbeschränkungen des Crawlers gelten. Die Größenbeschränkung für die Indexierung je Dateityp (Standard: 10 MB) finden Sie unter :doc:`crawler-basic`.
- Die OCR-Genauigkeit hängt von der Qualität des Scans ab. Handschrift wird im Allgemeinen nicht gut erkannt.
- Dateien, die vor dem Aktivieren von OCR indexiert wurden, werden nicht automatisch per OCR verarbeitet. Bei aktiviertem inkrementellem Crawling ("Letzte Änderung prüfen" in :doc:`../admin/general-guide`) wird eine Datei, deren Änderungszeit sich nicht geändert hat, beim erneuten Crawlen nicht noch einmal abgerufen. Um OCR auf diese Dateien anzuwenden, deaktivieren Sie "Letzte Änderung prüfen" für einen Crawl, oder löschen Sie die Dokumente aus dem Index und crawlen Sie erneut.

Hinweise zum Upgrade
====================

Bis 15.8 schloss die mitgelieferte ``tika.xml`` ``org.apache.tika.parser.ocr.TesseractOCRParser`` aus.
Ab 15.9 schließt die mitgelieferte ``tika.xml`` diesen Parser nicht mehr aus.

Wenn Sie eine angepasste ``tika.xml`` weiterverwenden, entfernen Sie die folgende Zeile:

::

    <parser-exclude class="org.apache.tika.parser.ocr.TesseractOCRParser"/>

Bleibt diese Zeile bestehen, bleibt OCR auch mit ``crawler.document.ocr.enabled=true`` ausgeschaltet.

Der Speicherort von ``tika.xml`` ist wie folgt:

- ZIP-Paket: ``app/WEB-INF/conf/tika.xml``
- RPM/DEB-Paket: ``/etc/fess/tika.xml``

OCR überprüfen
==============

1. Legen Sie eine Dateisystem-Crawl-Konfiguration für einen Ordner an, der ein gescanntes Bild (ein Bild mit Text) enthält.
2. Führen Sie den Crawl aus.
3. Suchen Sie nach einem Wort, das im Bild vorkommt, und prüfen Sie, ob das Bild in den Suchergebnissen erscheint.

Erscheint das Bild nicht, prüfen Sie Folgendes:

- ``tesseract --list-langs`` listet die verwendete Sprache auf
- ``crawler.document.ocr.enabled`` ist ``true``
- ``tika.xml`` schließt ``TesseractOCRParser`` nicht mehr aus
- ``fess-crawler.log`` des Crawls zeigt ``OCR is enabled`` (die Warnung ``Tesseract OCR is not available`` bedeutet, dass |Fess| Tesseract nicht verwenden kann)
