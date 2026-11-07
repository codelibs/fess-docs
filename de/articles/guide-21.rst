==================================================
Teil 21: Bilder und Text übergreifend durchsuchen
==================================================

Einführung
============

In den bisherigen Artikeln haben wir uns hauptsächlich auf die Suche in textbasierten Dokumenten konzentriert.
Das Wissen in Unternehmen umfasst jedoch auch zahlreiche Inhalte jenseits von Text.
Produktfotos, technische Zeichnungen, Folienbilder aus Präsentationen, Whiteboard-Fotos -- wenn auch diese "Bilder" durchsuchbar wären, würden sich die Möglichkeiten der Wissensnutzung erheblich erweitern.

In diesem Artikel stellen wir vor, wie Sie eine multimodale Suchumgebung aufbauen, die eine übergreifende Suche über Text und Bilder ermöglicht.

Zielgruppe
==========

- Personen, die Herausforderungen bei der Suche in Dokumenten mit Bildern haben
- Personen, die sich für Anwendungen der Vektorsuche interessieren
- Personen, die das Konzept multimodaler KI verstehen möchten

Was ist multimodale Suche?
============================

Multimodale Suche ist eine Technologie, die eine übergreifende Suche über verschiedene Datentypen (Text, Bilder, Audio usw.) ermöglicht.

Wenn Sie beispielsweise mit dem Text "Design eines roten Sportwagens" suchen, werden konzeptionell passende Bilder in den Suchergebnissen angezeigt.
Es handelt sich um einen Mechanismus, der es ermöglicht, mit Text nach Bildern oder mit Bildern nach Text zu suchen.

CLIP-Modell
-----------

Die Grundlage der multimodalen Suche bilden Modelle wie CLIP (Contrastive Language-Image Pre-Training).
CLIP wandelt Text und Bilder in denselben Vektorraum um und ermöglicht so die Berechnung der Ähnlichkeit zwischen Text und Bildern.

Multimodale Suche in Fess
=============================

Fess kann durch sein multimodales Such-Plugin eine übergreifende Suche über Text und Bilder realisieren.

Komponenten
------------

Die Komponenten der multimodalen Suche sind wie folgt aufgebaut:

1. **CLIP-Server**: Wandelt Text und Bilder in Vektoren um
2. **OpenSearch**: Durchsucht Vektoren mittels KNN (K-Nearest Neighbor)
3. **Fess**: Stellt Crawling, Indexierung und Such-UI bereit

Einrichtungsschritte
---------------------

**1. Vorbereitung des CLIP-Servers**

Bereiten Sie einen Server vor, auf dem das CLIP-Modell ausgeführt wird.
Eine Umgebung mit verfügbarer GPU wird empfohlen.

Sie können einen CLIP-Server mit Docker Compose hinzufügen.

**2. Installation des Plugins**

Installieren Sie das multimodale Such-Plugin für Fess.

**3. Konfiguration des KNN-Index**

Konfigurieren Sie die KNN-Index-Einstellungen, um die Vektorsuche in OpenSearch durchzuführen.
Stellen Sie die Vektordimensionen passend zum verwendeten CLIP-Modell ein.

**4. Crawl-Einstellungen**

Konfigurieren Sie Verzeichnisse und Websites mit Bildern als Crawl-Ziele.
Bilddateien (PNG, JPEG, GIF usw.) werden ebenfalls als Crawl-Ziele erfasst.

Sucherlebnis
=============

Bilder mit Text suchen
------------------------

Wenn Sie mit Text wie "Produktaußenfoto", "Meeting-Whiteboard" oder "technische Zeichnung" suchen, werden konzeptionell übereinstimmende Bilder in den Suchergebnissen angezeigt.

In den Suchergebnissen werden Vorschaubilder angezeigt, sodass Sie die gewünschten Bilder visuell finden können.

Gemischte Ergebnisse aus Text und Bildern
-------------------------------------------

Bei der multimodalen Suche werden Suchergebnisse zurückgegeben, die eine Mischung aus Textdokumenten und Bildern enthalten.
Rank Fusion (siehe Teil 18) wird verwendet, um die Ergebnisse der Textsuche und der Bildsuche zu integrieren.

Anwendungsfälle
==================

Fertigungsindustrie: Suche nach Teile- und Produktbildern
-----------------------------------------------------------

In der Fertigungsindustrie wird eine große Anzahl von Teilefotos und Produktbildern verwaltet.
Durch die Suche mit Text wie "rundes Metallteil" oder durch die Suche nach ähnlichen Teilen anhand eines Fotos eines bestimmten Teils können vergangene Designressourcen genutzt werden.

Designteams: Verwaltung von Design-Assets
-------------------------------------------

Designteams verwalten große Mengen visueller Assets wie Logos, Icons, Fotomaterial und Mockups.
Da Sie mit natürlicher Sprache wie "blauer Gradientenhintergrund" suchen können, wird das Auffinden von Assets erleichtert.

Forschung und Entwicklung: Suche nach Experimentaldaten
---------------------------------------------------------

Forschungs- und Entwicklungsabteilungen verwalten Diagramme von Versuchsergebnissen, Mikroskopaufnahmen und Bilder von Messdaten.
Indem diese Bilder durchsuchbar gemacht werden, wird der Zugriff auf vergangene Experimentaldaten erleichtert.

Überlegungen zur Einführung
===============================

Hardwareanforderungen
----------------------

Die multimodale Suche erfordert Rechenressourcen für die Ausführung des CLIP-Modells.

- **Empfohlen**: GPU-Server (NVIDIA GPU)
- **Minimum**: Läuft auch auf der CPU, jedoch mit reduzierter Indexierungsgeschwindigkeit

Die Indexierungszeit hängt von der Verarbeitungsgeschwindigkeit des Modells ab. Daher wird bei der Indexierung einer großen Anzahl von Bildern eine GPU-Umgebung dringend empfohlen.

Unterstützte Bildformate
---------------------------

Gängige Bildformate (JPEG, PNG, GIF, BMP, TIFF usw.) werden unterstützt.
Die Unterstützung von Bildern in PDFs und eingebetteten Bildern in Office-Dokumenten hängt von den Crawl-Einstellungen ab.

Schrittweise Einführung
--------------------------

Die multimodale Suche kann als Ergänzung zu einer bestehenden Textsuchumgebung eingeführt werden.

1. Führen Sie zunächst eine Testinstallation für Verzeichnisse und Websites mit vielen Bildern durch
2. Überprüfen Sie die Suchqualität und Nutzung
3. Erweitern Sie den Umfang schrittweise

Zusammenfassung
================

In diesem Artikel haben wir die übergreifende Suche über Bilder und Text mittels multimodaler Suche vorgestellt.

- Das Konzept der multimodalen Suche (einheitlicher Vektorraum für Text und Bilder durch CLIP)
- Komponenten und Konfiguration der multimodalen Suche in Fess
- Das Erlebnis der Bildsuche mit Text und der Suche nach ähnlichen Bildern mit Bildern
- Anwendungsfälle in der Fertigung, im Design und in der Forschung und Entwicklung
- GPU-Anforderungen und ein Ansatz zur schrittweisen Einführung

Im nächsten Artikel behandeln wir die Wissenvisualisierung in Organisationen durch Analyse von Suchdaten.

Referenzen
==========

- `OpenSearch KNN-Suche <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin-Verwaltung <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
