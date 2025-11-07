===============
Konfiguration von Thumbnail-Bildern
===============

Anzeige von Thumbnail-Bildern
===============

|Fess| kann Thumbnail-Bilder in Suchergebnissen anzeigen.
Thumbnail-Bilder werden basierend auf dem MIME-Typ der Suchergebnisse generiert.
Bei unterstützten MIME-Typen werden Thumbnail-Bilder bei der Anzeige von Suchergebnissen generiert.
Die Verarbeitung zur Generierung von Thumbnail-Bildern kann für jeden MIME-Typ konfiguriert und hinzugefügt werden.

Um Thumbnail-Bilder anzuzeigen, melden Sie sich als Administrator an, aktivieren Sie die Thumbnail-Anzeige in den allgemeinen Einstellungen und speichern Sie.

Thumbnail-Bilder für HTML-Dateien
======================

Für HTML-Thumbnails werden im HTML angegebene oder enthaltene Bilder verwendet.
Thumbnail-Bilder werden in folgender Reihenfolge gesucht und angezeigt, wenn angegeben:

- Der Wert des content-Attributs eines meta-Tags mit name-Attribut thumbnail
- Der Wert des content-Attributs eines meta-Tags mit property-Attribut og:image
- Bilder in geeigneter Größe für Thumbnails in img-Tags


Thumbnail-Bilder für MS Office-Dateien
===========================

Thumbnail-Bilder für MS Office-Dateien werden mit LibreOffice und ImageMagick generiert.
Wenn die Befehle unoconv und convert installiert sind, werden Thumbnail-Bilder generiert.

Installation von Paketen
------------------

Bei Redhat-basierten Betriebssystemen installieren Sie folgende Pakete zur Bildgenerierung:

::

    $ sudo yum install unoconv libreoffice-headless vlgothic-fonts ImageMagick

Generierungsskript
-----------

Bei Installation über RPM/DEB-Paket wird das Thumbnail-Generierungsskript für MS Office unter /usr/share/fess/bin/generate-thumbnail installiert.

Thumbnail-Bilder für PDF-Dateien
=====================

Thumbnail-Bilder für PDF werden mit ImageMagick generiert.
Wenn der Befehl convert installiert ist, werden Thumbnail-Bilder generiert.

Deaktivierung des Thumbnail-Jobs
==================

Um den Thumbnail-Job zu deaktivieren, konfigurieren Sie Folgendes:

1. Entfernen Sie in der Verwaltungsoberfläche unter System > Allgemein das Häkchen bei „Thumbnail-Anzeige" und klicken Sie auf „Aktualisieren".
2. Setzen Sie ``thumbnail.crawler.enabled`` in ``app/WEB-INF/classes/fess_config.properties`` oder ``/etc/fess/fess_config.properties`` auf ``false``.

::

    thumbnail.crawler.enabled=false

3. Starten Sie den Fess-Dienst neu.
