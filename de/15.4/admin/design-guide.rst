===============
Seitendesign
===============

Übersicht
=========

Hier wird die Konfiguration des Designs des Suchbildschirms erläutert.

Konfiguration
=============

Anzeige
-------

Um die Übersichtsseite für die Seitendesignkonfiguration zu öffnen, klicken Sie im linken Menü auf [System > Seitendesign].

|image0|


Dateimanager
------------

Sie können für den Suchbildschirm verfügbare Dateien herunterladen oder löschen.

Seitendateien anzeigen
----------------------

Sie können JSP-Dateien des Suchbildschirms bearbeiten.
Durch Klicken auf die Schaltfläche „Bearbeiten" für die Ziel-JSP-Datei können Sie diese JSP-Datei bearbeiten.
Durch Klicken auf die Schaltfläche „Standard verwenden" können Sie zur JSP-Datei der Installation zurückkehren.
Speichern Sie im Bearbeitungsbildschirm mit der Schaltfläche „Aktualisieren", um die Änderungen zu übernehmen.

Im Folgenden werden die bearbeitbaren Seiten zusammengefasst:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - /index.jsp
     - JSP-Datei der Such-Startseite. Diese JSP-Datei bindet alle Teilbereiche der JSP-Dateien ein.
   * - /header.jsp
     - JSP-Datei für den Header.
   * - /footer.jsp
     - JSP-Datei für den Footer.
   * - /search.jsp
     - JSP-Datei der Suchergebnisliste. Diese JSP-Datei bindet alle Teilbereiche der JSP-Dateien ein.
   * - /searchResults.jsp
     - JSP-Datei zur Darstellung des Suchergebnisteils der Suchergebnisliste. Diese JSP-Datei wird verwendet, wenn Suchergebnisse vorhanden sind. Ändern Sie diese, wenn Sie die Darstellung der Suchergebnisse anpassen möchten.
   * - /searchNoResult.jsp
     - JSP-Datei zur Darstellung des Suchergebnisteils der Suchergebnisliste. Diese JSP-Datei wird verwendet, wenn keine Suchergebnisse vorhanden sind.
   * - /searchOptions.jsp
     - JSP-Datei für den Suchoptionsbildschirm.
   * - /advance.jsp
     - JSP-Datei für den erweiterten Suchbildschirm.
   * - /help.jsp
     - JSP-Datei für die Hilfeseite.
   * - /error/error.jsp
     - JSP-Datei für die Suchfehlerseite. Ändern Sie diese, wenn Sie die Darstellung von Suchfehlern anpassen möchten.
   * - /error/notFound.jsp
     - JSP-Datei für die Fehlerseite, die angezeigt wird, wenn eine Seite nicht gefunden wird.
   * - /error/system.jsp
     - JSP-Datei für die Fehlerseite, die bei Systemfehlern angezeigt wird.
   * - /error/redirect.jsp
     - JSP-Datei für die Fehlerseite, die bei HTTP-Weiterleitungen angezeigt wird.
   * - /error/badRequest.jsp
     - JSP-Datei für die Fehlerseite, die bei ungültigen Anforderungen angezeigt wird.
   * - /cache.hbs
     - Datei zur Anzeige des Caches von Suchergebnissen.
   * - /login/index.jsp
     - JSP-Datei für den Anmeldebildschirm.
   * - /profile/index.jsp
     - JSP für den Passwortänderungsbildschirm für Benutzer.
   * - /profile/newpassword.jsp
     - JSP für den Passwortaktualisierungsbildschirm für Administratoren. Fordert eine Passwortänderung an, wenn Benutzername und Passwort bei der Anmeldung identisch sind.


Tabelle: Bearbeitbare JSP-Dateien

|image1|

Hochzuladende Dateien
---------------------

Sie können Dateien hochladen, die auf dem Suchbildschirm verwendet werden.
Unterstützte Bilddateinamen sind jpg, gif, png, css, js.

Datei-Upload
::::::::::::

Geben Sie die hochzuladende Datei an.

Dateiname (optional)
::::::::::::::::::::

Verwenden Sie dies, wenn Sie der hochzuladenden Datei einen Dateinamen geben möchten.
Wenn weggelassen, wird der Name der hochgeladenen Datei verwendet.
Wenn Sie beispielsweise logo.png angeben, wird das Bild auf der Such-Startseite geändert.


.. |image0| image:: ../../../resources/images/en/15.4/admin/design-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/design-2.png
