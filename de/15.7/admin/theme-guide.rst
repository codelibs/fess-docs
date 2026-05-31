=====
Theme
=====

Übersicht
=========

Die Theme-Funktion verwaltet „statische Themes" – Pakete aus statischen Assets (HTML / CSS / JavaScript usw.), die das Erscheinungsbild des Suchbildschirms bestimmen. Statische Themes werden als ZIP-Archiv hochgeladen und in das Theme-Verzeichnis auf dem Server entpackt (Standard: ``themes``, änderbar über ``theme.directory.path``). Im Stammverzeichnis jedes Themes muss sich das ``theme.yml``-Manifest mit den Theme-Metadaten befinden.

.. note::
   JSP-basierte Themes werden über die Plug-in-Verwaltung behandelt und sind nicht Gegenstand dieser Seite.
   Für die hier beschriebenen Operationen ist die Rolle ``admin-theme`` erforderlich (für reinen Lesezugriff genügt die Rolle ``admin-theme-view``).

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite der registrierten Themes zu öffnen, klicken Sie im linken Menü auf [System > Theme].

Themenliste
-----------

Die Übersichtsseite zeigt alle im Theme-Verzeichnis registrierten statischen Themes an. Folgende Spalten werden pro Eintrag angezeigt:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Vorschaubild
     - Zeigt die Datei ``thumbnail.png`` im Theme-Verzeichnis an. Ist diese Datei nicht vorhanden, wird kein Bild angezeigt.
   * - Name
     - Name des Themes (entspricht dem Verzeichnisnamen des Themes). Durch Klicken wird die Detailseite geöffnet.
   * - Anzeigename
     - Der Wert ``displayName`` aus dem Manifest.
   * - Version
     - Der Wert ``version`` aus dem Manifest.
   * - Standard
     - Ein Häkchen wird angezeigt, wenn dieses Theme als Standardtheme festgelegt ist.
   * - Aktion
     - Zeigt eine Schaltfläche „Löschen" zum Entfernen des Themes an (wird für das Standardtheme nicht angezeigt).

Tabelle: Spalten der Themenliste


Standardtheme festlegen
-----------------------

Wählen Sie im Dropdown-Menü oben auf der Übersichtsseite ein Theme aus und klicken Sie auf die Schaltfläche [Als Standard festlegen], um das Standardtheme für den Suchbildschirm festzulegen. Wenn Sie [(kein Standard)] auswählen und bestätigen, wird die Standardtheme-Zuweisung aufgehoben. Nach dem Speichern werden die Theme-Informationen neu geladen und die Änderung tritt sofort in Kraft.


Theme hochladen
---------------

Klicken Sie auf die Schaltfläche [Hochladen], um die Upload-Seite zu öffnen. Wählen Sie eine Theme-ZIP-Datei aus und klicken Sie auf die Schaltfläche [Hochladen], um das Theme zu installieren.

* Es können nur Archive im Format ``.zip`` hochgeladen werden.
* Die maximale Dateigröße des komprimierten Archivs beträgt standardmäßig 50 MB (``theme.upload.max.size``).
* Das ZIP-Archiv muss im Stammverzeichnis ein ``theme.yml``-Manifest enthalten.

Wenn bereits ein Theme mit demselben Namen vorhanden ist, wird es ersetzt. Das ersetzte Theme wird für einen festgelegten Zeitraum (Standard: 7 Tage, ``theme.upload.attic.retention.days``) als Sicherung aufbewahrt.

Falls das hochgeladene Archiv die Manifest-Validierung nicht besteht oder die Größe, Anzahl der Einträge oder das Komprimierungsverhältnis nach dem Entpacken die Servergrenzen überschreitet (Schutz vor Zip-Bomben), wird die Installation abgelehnt und eine Fehlermeldung angezeigt.


theme.yml-Manifest
------------------

Im Stammverzeichnis eines statischen Themes muss die Datei ``theme.yml`` (YAML-Format) mit den Theme-Metadaten vorhanden sein. Folgende Felder können angegeben werden:

.. tabularcolumns:: |p{3cm}|p{2cm}|p{7cm}|
.. list-table::
   :header-rows: 1

   * - Feld
     - Pflichtfeld
     - Beschreibung
   * - ``apiVersion``
     - Pflichtfeld
     - Gibt ``fess.codelibs.org/v1`` an.
   * - ``kind``
     - Pflichtfeld
     - Gibt ``StaticTheme`` an.
   * - ``name``
     - Pflichtfeld
     - Name des Themes. Muss dem Muster ``^[a-z0-9][a-z0-9_-]{0,63}$`` entsprechen und mit dem Verzeichnisnamen des Themes übereinstimmen.
   * - ``displayName``
     - Pflichtfeld
     - Der auf der Oberfläche angezeigte Name (maximal 4096 Zeichen).
   * - ``version``
     - Pflichtfeld
     - Versionsnummer im SemVer-Format (Beispiel: ``1.0.0``).
   * - ``author``
     - Optional
     - Autor des Themes.
   * - ``description``
     - Optional
     - Beschreibung des Themes.
   * - ``license``
     - Optional
     - Lizenz des Themes.
   * - ``homepage``
     - Optional
     - Homepage-URL des Themes.
   * - ``minFessVersion``
     - Optional
     - Mindest-|Fess|-Version, die von diesem Theme unterstützt wird.
   * - ``supportedLocales``
     - Optional
     - Vom Theme unterstützte Sprachregionen.
   * - ``entry``
     - Optional
     - Einstiegspunktdatei des Themes (Standard: ``index.html``).
   * - ``spaFallback``
     - Optional
     - Aktiviert oder deaktiviert den SPA-Fallback-Modus (Standard: ``true``).

Tabelle: Felder der theme.yml


Theme löschen
-------------

Ein Theme kann über die Schaltfläche „Löschen" in der Übersichtsseite oder über die Schaltfläche [Löschen] auf der Detailseite entfernt werden. Das als Standardtheme festgelegte Theme kann nicht gelöscht werden. Heben Sie zuerst die Standardtheme-Zuweisung auf, bevor Sie das Theme löschen. Gelöschte Themes werden für einen festgelegten Zeitraum (Standard: 7 Tage, ``theme.upload.attic.retention.days``) als Sicherung aufbewahrt.


Neu laden
---------

Wenn das Theme-Verzeichnis direkt auf dem Server bearbeitet wurde, können Sie durch Klicken auf die Schaltfläche [Neu laden] die Theme-Informationen vom Datenträger neu in den Arbeitsspeicher laden.


Theme-Details
-------------

Durch Klicken auf einen Theme-Namen in der Übersichtsseite wird die Detailseite geöffnet. Auf der Detailseite können die Manifest-Inhalte eingesehen werden (Name, Anzeigename, Version, Standard-Flag, Zustand).


Konfigurationseigenschaften
===========================

Die wichtigsten Einstellungen der Theme-Funktion können in ``fess_config.properties`` geändert werden.

.. tabularcolumns:: |p{6cm}|p{3cm}|p{5cm}|
.. list-table::
   :header-rows: 1

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``theme.directory.path``
     - ``themes``
     - Verzeichnis zur Speicherung der Themes (relativer Pfad vom Servlet-Kontext oder absoluter Pfad).
   * - ``theme.upload.max.size``
     - ``52428800``
     - Maximale ZIP-Uploadgröße in Bytes (ca. 50 MB).
   * - ``theme.upload.max.extracted.size``
     - ``209715200``
     - Maximale Gesamtgröße nach dem Entpacken in Bytes (ca. 200 MB).
   * - ``theme.upload.max.entries``
     - ``1000``
     - Maximale Anzahl von Einträgen im ZIP-Archiv.
   * - ``theme.upload.max.compression.ratio``
     - ``100``
     - Maximales Komprimierungsverhältnis pro Eintrag.
   * - ``theme.upload.zip.ratio.max``
     - ``50``
     - Obergrenze des kumulierten Komprimierungsverhältnisses (Schutz vor Zip-Bomben).
   * - ``theme.upload.zip.ratio.check.threshold.bytes``
     - ``65536``
     - Komprimierte Bytegröße, ab der das kumulierte Komprimierungsverhältnis geprüft wird.
   * - ``theme.upload.attic.retention.days``
     - ``7``
     - Anzahl der Tage, für die Sicherungen ersetzter oder gelöschter Themes aufbewahrt werden.

Tabelle: Konfigurationseigenschaften der Theme-Funktion
