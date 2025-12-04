===================================
Konfiguration von Thumbnail-Bildern
===================================

Übersicht
=========

|Fess| kann Thumbnail-Bilder in Suchergebnissen anzeigen.
Thumbnail-Bilder werden basierend auf dem MIME-Typ der Suchergebnisse generiert.
Bei unterstützten MIME-Typen werden Thumbnail-Bilder bei der Anzeige von Suchergebnissen generiert.
Die Verarbeitung zur Generierung von Thumbnail-Bildern kann für jeden MIME-Typ konfiguriert und hinzugefügt werden.

Um Thumbnail-Bilder anzuzeigen, melden Sie sich als Administrator an, aktivieren Sie die Thumbnail-Anzeige in den allgemeinen Einstellungen und speichern Sie.

Unterstützte Dateiformate
=========================

Bilddateien
-----------

.. list-table::
   :widths: 15 40 20
   :header-rows: 1

   * - Format
     - MIME-Typ
     - Beschreibung
   * - JPEG
     - ``image/jpeg``
     - Fotos usw.
   * - PNG
     - ``image/png``
     - Transparente Bilder usw.
   * - GIF
     - ``image/gif``
     - Einschließlich animierter GIFs
   * - BMP
     - ``image/bmp``, ``image/x-windows-bmp``, ``image/x-ms-bmp``
     - Bitmap-Bilder
   * - TIFF
     - ``image/tiff``
     - Hochqualitative Bilder
   * - SVG
     - ``image/svg+xml``
     - Vektorbilder
   * - Photoshop
     - ``image/vnd.adobe.photoshop``, ``image/photoshop``, ``application/x-photoshop``, ``application/photoshop``
     - PSD-Dateien

Dokumentdateien
---------------

.. list-table::
   :widths: 15 50 20
   :header-rows: 1

   * - Format
     - MIME-Typ
     - Beschreibung
   * - PDF
     - ``application/pdf``
     - PDF-Dokumente
   * - Word
     - ``application/msword``, ``application/vnd.openxmlformats-officedocument.wordprocessingml.document``
     - Word-Dokumente
   * - Excel
     - ``application/vnd.ms-excel``, ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet``
     - Excel-Tabellen
   * - PowerPoint
     - ``application/vnd.ms-powerpoint``, ``application/vnd.openxmlformats-officedocument.presentationml.presentation``
     - PowerPoint-Präsentationen
   * - RTF
     - ``application/rtf``
     - Rich Text
   * - PostScript
     - ``application/postscript``
     - PostScript-Dateien

HTML-Inhalte
------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Format
     - MIME-Typ
     - Beschreibung
   * - HTML
     - ``text/html``
     - Generiert Thumbnails aus eingebetteten Bildern in HTML-Seiten

Erforderliche externe Tools
===========================

Die Thumbnail-Generierung erfordert die folgenden externen Tools. Installieren Sie diese entsprechend den Dateiformaten, die Sie unterstützen möchten.

Basis-Tools (erforderlich)
--------------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Zweck
     - Linux (apt)
     - Mac (Homebrew)
   * - ImageMagick
     - Bildkonvertierung & Größenänderung
     - ``apt install imagemagick``
     - ``brew install imagemagick``

.. note::

   Sowohl ImageMagick 6 (``convert``-Befehl) als auch ImageMagick 7 (``magick``-Befehl) werden unterstützt.

SVG-Unterstützung
-----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Zweck
     - Linux (apt)
     - Mac (Homebrew)
   * - rsvg-convert
     - SVG zu PNG Konvertierung
     - ``apt install librsvg2-bin``
     - ``brew install librsvg``

PDF-Unterstützung
-----------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Zweck
     - Linux (apt)
     - Mac (Homebrew)
   * - pdftoppm
     - PDF zu PNG Konvertierung
     - ``apt install poppler-utils``
     - ``brew install poppler``

MS Office-Unterstützung
-----------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Zweck
     - Linux (apt)
     - Mac (Homebrew)
   * - unoconv
     - Office zu PDF Konvertierung
     - ``apt install unoconv``
     - ``brew install unoconv``
   * - pdftoppm
     - PDF zu PNG Konvertierung
     - ``apt install poppler-utils``
     - ``brew install poppler``

Bei Redhat-basierten Betriebssystemen installieren Sie folgende Pakete:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick poppler-utils

PostScript-Unterstützung
------------------------

.. list-table::
   :widths: 15 25 30 30
   :header-rows: 1

   * - Tool
     - Zweck
     - Linux (apt)
     - Mac (Homebrew)
   * - ps2pdf
     - PS zu PDF Konvertierung
     - ``apt install ghostscript``
     - ``brew install ghostscript``
   * - pdftoppm
     - PDF zu PNG Konvertierung
     - ``apt install poppler-utils``
     - ``brew install poppler``

Thumbnail-Bilder für HTML-Dateien
=================================

Für HTML-Thumbnails werden im HTML angegebene oder enthaltene Bilder verwendet.
Thumbnail-Bilder werden in folgender Reihenfolge gesucht und angezeigt:

1. Der Wert des content-Attributs eines meta-Tags mit name-Attribut "thumbnail"
2. Der Wert des content-Attributs eines meta-Tags mit property-Attribut "og:image"
3. Bilder in geeigneter Größe für Thumbnails in img-Tags

Konfiguration
=============

Konfigurationsdatei
-------------------

Der Thumbnail-Generator wird in ``fess_thumbnail.xml`` konfiguriert.

::

    src/main/resources/fess_thumbnail.xml

Hauptkonfigurationsoptionen (fess_config.properties)
----------------------------------------------------

Die folgenden Optionen können in ``app/WEB-INF/classes/fess_config.properties`` oder ``/etc/fess/fess_config.properties`` konfiguriert werden.

::

    # Mindestbreite für Thumbnail-Bilder (Pixel)
    thumbnail.html.image.min.width=100

    # Mindesthöhe für Thumbnail-Bilder (Pixel)
    thumbnail.html.image.min.height=100

    # Maximales Seitenverhältnis (Breite:Höhe oder Höhe:Breite)
    thumbnail.html.image.max.aspect.ratio=3.0

    # Generierte Thumbnail-Breite
    thumbnail.html.image.thumbnail.width=100

    # Generierte Thumbnail-Höhe
    thumbnail.html.image.thumbnail.height=100

    # Ausgabeformat
    thumbnail.html.image.format=png

    # XPath zum Extrahieren von Bildern aus HTML
    thumbnail.html.image.xpath=//IMG

    # Ausgeschlossene Erweiterungen
    thumbnail.html.image.exclude.extensions=svg,html,css,js

    # Thumbnail-Generierungsintervall (Millisekunden)
    thumbnail.generator.interval=0

    # Befehlsausführungs-Timeout (Millisekunden)
    thumbnail.command.timeout=30000

    # Prozessbeendigungs-Timeout (Millisekunden)
    thumbnail.command.destroy.timeout=5000

generate-thumbnail Skript
=========================

Übersicht
---------

``generate-thumbnail`` ist ein Shell-Skript, das die eigentliche Thumbnail-Generierung durchführt.
Bei Installation über RPM/DEB-Paket wird es unter ``/usr/share/fess/bin/generate-thumbnail`` installiert.

Verwendung
----------

::

    generate-thumbnail <type> <url> <output_file> [mimetype]

Argumente
---------

.. list-table::
   :widths: 15 40 30
   :header-rows: 1

   * - Argument
     - Beschreibung
     - Beispiel
   * - ``type``
     - Dateityp
     - ``image``, ``svg``, ``pdf``, ``msoffice``, ``ps``
   * - ``url``
     - Eingabedatei-URL
     - ``file:/path/to/file.jpg``
   * - ``output_file``
     - Ausgabedateipfad
     - ``/var/lib/fess/thumbnails/_0/_1/abc.png``
   * - ``mimetype``
     - MIME-Typ (optional)
     - ``image/gif``

Unterstützte Typen
------------------

.. list-table::
   :widths: 15 30 40
   :header-rows: 1

   * - Typ
     - Beschreibung
     - Verwendete Tools
   * - ``image``
     - Bilddateien
     - ImageMagick (convert/magick)
   * - ``svg``
     - SVG-Dateien
     - rsvg-convert
   * - ``pdf``
     - PDF-Dateien
     - pdftoppm + ImageMagick
   * - ``msoffice``
     - MS Office-Dateien
     - unoconv + pdftoppm + ImageMagick
   * - ``ps``
     - PostScript-Dateien
     - ps2pdf + pdftoppm + ImageMagick

Beispiele
---------

::

    # Thumbnail für Bilddatei generieren
    ./generate-thumbnail image file:/path/to/image.jpg /tmp/thumbnail.png image/jpeg

    # Thumbnail für SVG-Datei generieren
    ./generate-thumbnail svg file:/path/to/image.svg /tmp/thumbnail.png

    # Thumbnail für PDF-Datei generieren
    ./generate-thumbnail pdf file:/path/to/document.pdf /tmp/thumbnail.png

    # GIF-Datei (MIME-Typ angeben für Format-Hinweis)
    ./generate-thumbnail image file:/path/to/image.gif /tmp/thumbnail.png image/gif

Thumbnail-Speicherort
=====================

Standardpfad
------------

::

    ${FESS_VAR_PATH}/thumbnails/

oder

::

    /var/lib/fess/thumbnails/

Verzeichnisstruktur
-------------------

Thumbnails werden in einer hash-basierten Verzeichnisstruktur gespeichert.

::

    thumbnails/
    ├── _0/
    │   ├── _1/
    │   │   ├── _2/
    │   │   │   └── _3/
    │   │   │       └── abcdef123456.png
    │   │   └── ...
    │   └── ...
    └── ...

Deaktivierung des Thumbnail-Jobs
================================

Um den Thumbnail-Job zu deaktivieren, konfigurieren Sie Folgendes:

1. Entfernen Sie in der Verwaltungsoberfläche unter System > Allgemein das Häkchen bei "Thumbnail-Anzeige" und klicken Sie auf "Aktualisieren".
2. Setzen Sie ``thumbnail.crawler.enabled`` in ``app/WEB-INF/classes/fess_config.properties`` oder ``/etc/fess/fess_config.properties`` auf ``false``.

::

    thumbnail.crawler.enabled=false

3. Starten Sie den Fess-Dienst neu.

Fehlerbehebung
==============

Thumbnails werden nicht generiert
---------------------------------

1. **Externe Tools überprüfen**

::

    # ImageMagick überprüfen
    which convert || which magick

    # rsvg-convert überprüfen (für SVG)
    which rsvg-convert

    # pdftoppm überprüfen (für PDF)
    which pdftoppm

2. **Logs überprüfen**

::

    ${FESS_LOG_PATH}/fess-thumbnail.log

3. **Skript manuell ausführen**

::

    /usr/share/fess/bin/generate-thumbnail image file:/path/to/test.jpg /tmp/test_thumbnail.png image/jpeg

Fehler bei GIF/TIFF-Dateien
---------------------------

Bei Verwendung von ImageMagick 6 geben Sie den MIME-Typ an, um Format-Hinweise zu aktivieren. Dies geschieht automatisch, wenn Fess korrekt konfiguriert ist.

Fehlerbeispiel::

    convert-im6.q16: corrupt image `/tmp/thumbnail_xxx' @ error/gif.c/DecodeImage/512

Lösungen:

- Auf ImageMagick 7 aktualisieren
- Oder überprüfen, dass der MIME-Typ korrekt übergeben wird

SVG-Thumbnails werden nicht generiert
-------------------------------------

1. Prüfen Sie, ob ``rsvg-convert`` installiert ist

::

    which rsvg-convert

2. Konvertierung manuell testen

::

    rsvg-convert -w 100 -h 100 --keep-aspect-ratio input.svg -o output.png

Berechtigungsfehler
-------------------

Überprüfen Sie die Berechtigungen des Thumbnail-Speicherverzeichnisses.

::

    ls -la /var/lib/fess/thumbnails/

Korrigieren Sie die Berechtigungen bei Bedarf.

::

    chown -R fess:fess /var/lib/fess/thumbnails/
    chmod -R 755 /var/lib/fess/thumbnails/

Plattformunterstützung
======================

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Plattform
     - Unterstützungsstatus
     - Hinweise
   * - Linux
     - Vollständig unterstützt
     - \-
   * - macOS
     - Vollständig unterstützt
     - Externe Tools über Homebrew installieren
   * - Windows
     - Nicht unterstützt
     - Aufgrund der Bash-Skript-Abhängigkeit
