============================================================
Teil 21: Bilder und Text uebergreifend durchsuchen -- Wissensmanagement der naechsten Generation mit multimodaler Suche
============================================================

Einfuehrung
============

In den bisherigen Artikeln haben wir uns hauptsaechlich auf die Suche in textbasierten Dokumenten konzentriert.
Das Wissen in Unternehmen umfasst jedoch auch zahlreiche Inhalte jenseits von Text.
Produktfotos, technische Zeichnungen, Folienbilder aus Praesentationen, Whiteboard-Fotos -- wenn auch diese "Bilder" durchsuchbar waeren, wuerden sich die Moeglichkeiten der Wissensnutzung erheblich erweitern.

In diesem Artikel stellen wir vor, wie Sie eine multimodale Suchumgebung aufbauen, die eine uebergreifende Suche ueber Text und Bilder ermoeglicht.

Zielgruppe
==========

- Personen, die Herausforderungen bei der Suche in Dokumenten mit Bildern haben
- Personen, die sich fuer Anwendungen der Vektorsuche interessieren
- Personen, die das Konzept multimodaler KI verstehen moechten

Was ist multimodale Suche?
============================

Multimodale Suche ist eine Technologie, die eine uebergreifende Suche ueber verschiedene Datentypen (Text, Bilder, Audio usw.) ermoeglicht.

Wenn Sie beispielsweise mit dem Text "Design eines roten Sportwagens" suchen, werden konzeptionell passende Bilder in den Suchergebnissen angezeigt.
Es handelt sich um einen Mechanismus, der es ermoeglicht, mit Text nach Bildern oder mit Bildern nach Text zu suchen.

CLIP-Modell
-----------

Die Grundlage der multimodalen Suche bilden Modelle wie CLIP (Contrastive Language-Image Pre-Training).
CLIP wandelt Text und Bilder in denselben Vektorraum um und ermoeglicht so die Berechnung der Aehnlichkeit zwischen Text und Bildern.

Multimodale Suche in Fess
=============================

Fess kann durch sein multimodales Such-Plugin eine uebergreifende Suche ueber Text und Bilder realisieren.

Komponenten
------------

Die Komponenten der multimodalen Suche sind wie folgt aufgebaut:

1. **CLIP-Server**: Wandelt Text und Bilder in Vektoren um
2. **OpenSearch**: Durchsucht Vektoren mittels KNN (K-Nearest Neighbor)
3. **Fess**: Stellt Crawling, Indexierung und Such-UI bereit

Einrichtungsschritte
---------------------

**1. Vorbereitung des CLIP-Servers**

Bereiten Sie einen Server vor, auf dem das CLIP-Modell ausgefuehrt wird.
Eine Umgebung mit verfuegbarer GPU wird empfohlen.

Sie koennen einen CLIP-Server mit Docker Compose hinzufuegen.

**2. Installation des Plugins**

Installieren Sie das multimodale Such-Plugin fuer Fess.

**3. Konfiguration des KNN-Index**

Konfigurieren Sie die KNN-Index-Einstellungen, um die Vektorsuche in OpenSearch durchzufuehren.
Stellen Sie die Vektordimensionen passend zum verwendeten CLIP-Modell ein.

**4. Crawl-Einstellungen**

Konfigurieren Sie Verzeichnisse und Websites mit Bildern als Crawl-Ziele.
Bilddateien (PNG, JPEG, GIF usw.) werden ebenfalls als Crawl-Ziele erfasst.

Sucherlebnis
=============

Bilder mit Text suchen
------------------------

Wenn Sie mit Text wie "Produktaussenfoto", "Meeting-Whiteboard" oder "technische Zeichnung" suchen, werden konzeptionell uebereinstimmende Bilder in den Suchergebnissen angezeigt.

In den Suchergebnissen werden Vorschaubilder angezeigt, sodass Sie die gewuenschten Bilder visuell finden koennen.

Gemischte Ergebnisse aus Text und Bildern
-------------------------------------------

Bei der multimodalen Suche werden Suchergebnisse zurueckgegeben, die eine Mischung aus Textdokumenten und Bildern enthalten.
Rank Fusion (siehe Teil 18) wird verwendet, um die Ergebnisse der Textsuche und der Bildsuche zu integrieren.

Anwendungsfaelle
==================

Fertigungsindustrie: Suche nach Teile- und Produktbildern
-----------------------------------------------------------

In der Fertigungsindustrie wird eine grosse Anzahl von Teilefotos und Produktbildern verwaltet.
Durch die Suche mit Text wie "rundes Metallteil" oder durch die Suche nach aehnlichen Teilen anhand eines Fotos eines bestimmten Teils koennen vergangene Designressourcen genutzt werden.

Designteams: Verwaltung von Design-Assets
-------------------------------------------

Designteams verwalten grosse Mengen visueller Assets wie Logos, Icons, Fotomaterial und Mockups.
Da Sie mit natuerlicher Sprache wie "blauer Gradientenhintergrund" suchen koennen, wird das Auffinden von Assets erleichtert.

Forschung und Entwicklung: Suche nach Experimentaldaten
---------------------------------------------------------

Forschungs- und Entwicklungsabteilungen verwalten Diagramme von Versuchsergebnissen, Mikroskopaufnahmen und Bilder von Messdaten.
Indem diese Bilder durchsuchbar gemacht werden, wird der Zugriff auf vergangene Experimentaldaten erleichtert.

Ueberlegungen zur Einfuehrung
===============================

Hardwareanforderungen
----------------------

Die multimodale Suche erfordert Rechenressourcen fuer die Ausfuehrung des CLIP-Modells.

- **Empfohlen**: GPU-Server (NVIDIA GPU)
- **Minimum**: Laeuft auch auf der CPU, jedoch mit reduzierter Indexierungsgeschwindigkeit

Die Indexierungszeit haengt von der Verarbeitungsgeschwindigkeit des Modells ab. Daher wird bei der Indexierung einer grossen Anzahl von Bildern eine GPU-Umgebung dringend empfohlen.

Unterstuetzte Bildformate
---------------------------

Gaengige Bildformate (JPEG, PNG, GIF, BMP, TIFF usw.) werden unterstuetzt.
Die Unterstuetzung von Bildern in PDFs und eingebetteten Bildern in Office-Dokumenten haengt von den Crawl-Einstellungen ab.

Schrittweise Einfuehrung
--------------------------

Die multimodale Suche kann als Ergaenzung zu einer bestehenden Textsuchumgebung eingefuehrt werden.

1. Fuehren Sie zunaechst eine Testinstallation fuer Verzeichnisse und Websites mit vielen Bildern durch
2. Ueberpruefen Sie die Suchqualitaet und Nutzung
3. Erweitern Sie den Umfang schrittweise

Zusammenfassung
================

In diesem Artikel haben wir die uebergreifende Suche ueber Bilder und Text mittels multimodaler Suche vorgestellt.

- Das Konzept der multimodalen Suche (einheitlicher Vektorraum fuer Text und Bilder durch CLIP)
- Komponenten und Konfiguration der multimodalen Suche in Fess
- Das Erlebnis der Bildsuche mit Text und der Suche nach aehnlichen Bildern mit Bildern
- Anwendungsfaelle in der Fertigung, im Design und in der Forschung und Entwicklung
- GPU-Anforderungen und ein Ansatz zur schrittweisen Einfuehrung

Im naechsten Artikel behandeln wir die Wissenvisualisierung in Organisationen durch Analyse von Suchdaten.

Referenzen
==========

- `OpenSearch KNN-Suche <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin-Verwaltung <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
