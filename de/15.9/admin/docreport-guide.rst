===============
Dokumentbericht
===============

Übersicht
=========

Die Seite Dokumentbericht hilft beim Aufräumen gecrawlter Dateiserver und Ähnlichem. Sie listet
Dokumente mit gleichem Inhalt und Dokumente auf, die lange nicht geändert wurden; jede Liste lässt
sich als CSV herunterladen.

Um die Seite zu öffnen, wählen Sie im linken Menü [Systeminformationen > Dokumentbericht]. Zum
Anzeigen ist die Rolle ``admin-docreport`` oder ``admin-docreport-view`` erforderlich. Die Seite
zeigt Berichte nur an und lädt sie herunter; sie ändert keine Dokumente.

Beide Registerkarten lassen sich mit „URL-Präfix“ eingrenzen, zum Beispiel ``smb://server/share/``.

Duplikate
=========

Dokumente mit gleichem oder nahezu gleichem Inhalt werden gruppiert, die größte Gruppe zuerst. Die
Gruppen beruhen auf der beim Indexieren berechneten Inhaltssignatur (``content_minhash_bits``,
dieselbe, die doppelte Suchergebnisse zusammenfasst); eine Neuindexierung ist daher nicht nötig.
Dokumente, deren Inhalt keine Wörter enthält (etwa leere Dateien), werden ausgelassen.

Die Seite zeigt bis zu ``docreport.duplicate.group.size`` (Standard: 100) Gruppen und je Gruppe bis zu
``docreport.duplicate.docs.size`` (Standard: 10) Dokumente. Mit [CSV herunterladen] erhalten Sie alle
Gruppen. Die CSV-Datei liest auch bei einem großen Index alle Gruppen, mit den Spalten
``group, groupSize, url, title, filename, contentLength, lastModified, owner, lastModifier, clickCount, docId``.

.. note::

   Bei einem Index, der die Inhaltssignatur nicht speichert (die Mappings ``cloud`` und ``aws``), ist
   der Duplikatbericht nicht verfügbar.

Inaktive Dokumente
==================

Dokumente, deren letzte Änderung älter als die angegebene Anzahl von Tagen ist („Nicht geändert seit
(Tagen)“, Standard 365 aus ``docreport.dormant.days``), werden aufgelistet, die ältesten zuerst.
Dokumente ohne Änderungsdatum werden nicht aufgeführt. Mit „Nie aus den Suchergebnissen geöffnet“
werden Dokumente ausgelassen, die aus Suchergebnissen angeklickt wurden.

Die Seite zeigt die Anzahl der passenden Dokumente, ihre Gesamtgröße und eine seitenweise Liste. Das
Blättern endet bei ``indexer.max.result.window.size``; Dokumente darüber hinaus erhalten Sie mit
[CSV herunterladen].

Einstellungen
=============

Die folgenden Einstellungen in ``fess_config.properties`` steuern den Bericht.

.. list-table::
   :header-rows: 1
   :widths: 40 45 15

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``docreport.duplicate.group.size``
     - Höchstzahl der Duplikatgruppen, die die Seite anzeigt
     - ``100``
   * - ``docreport.duplicate.docs.size``
     - Höchstzahl der Dokumente, die die Seite je Gruppe auflistet
     - ``10``
   * - ``docreport.duplicate.export.page.size``
     - Anzahl der Inhaltssignaturen, die beim CSV-Download je Anfrage gelesen werden
     - ``10000``
   * - ``docreport.dormant.days``
     - Standardanzahl der Tage seit der letzten Änderung, ab der ein Dokument als inaktiv gilt
     - ``365``
