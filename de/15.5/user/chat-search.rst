==========================
KI-Chat-Suche
==========================

Übersicht
=========

Mit der KI-Chat-Suche von |Fess| können Sie neben der herkömmlichen Stichwortsuche auch
in natürlicher Gesprächsform nach Informationen suchen. Wenn Sie eine Frage eingeben,
analysiert der KI-Assistent die Suchergebnisse und generiert eine verständliche Antwort.

Merkmale der KI-Chat-Suche
==========================

Dialogbasierte Suche
--------------------

Anstatt Schlüsselwörter zu formulieren, können Sie wie in einem normalen Gespräch fragen.

Beispiele:

- "Wie installiere ich Fess?"
- "Wie kann ich Dateien crawlen?"
- "Was kann ich tun, wenn keine Suchergebnisse angezeigt werden?"

Kontextbezogene Antworten
-------------------------

Der KI-Assistent versteht die Absicht Ihrer Frage und fasst relevante Informationen zusammen.
Er extrahiert die benötigten Informationen aus mehreren Suchergebnissen und präsentiert sie in strukturierter Form.

Quellenangabe
-------------

Die KI-Antworten enthalten Quellenangaben (Referenzdokumente).
Wenn Sie die Genauigkeit einer Antwort überprüfen möchten, können Sie direkt auf das Originaldokument zugreifen.

Gesprächsfortsetzung
--------------------

Sie müssen nicht bei einer einzigen Frage aufhören und können das Gespräch fortsetzen.
Sie können Folgefragen stellen, die den Kontext vorheriger Fragen und Antworten berücksichtigen.

Verwendung der Chat-Suche
=========================

Chat starten
------------

1. Öffnen Sie die Suchseite von |Fess|
2. Klicken Sie auf das Chat-Symbol unten rechts auf dem Bildschirm
3. Das Chat-Panel wird angezeigt

Frage eingeben
--------------

1. Geben Sie Ihre Frage in das Textfeld ein
2. Klicken Sie auf die Senden-Schaltfläche oder drücken Sie Enter
3. Der KI-Assistent generiert eine Antwort

.. note::
   Die Generierung der Antwort kann einige Sekunden dauern.
   Während der Verarbeitung wird die aktuelle Phase angezeigt (Suche, Analyse usw.).

Antwort überprüfen
------------------

Die Antwort des KI-Assistenten wird angezeigt und enthält:

- **Antworttext**: Detaillierte Antwort auf Ihre Frage
- **Quellen**: Links zu den Dokumenten, auf denen die Antwort basiert ([1], [2] usw.)

Klicken Sie auf einen Quellenlink, um das Originaldokument zu überprüfen.

Gespräch fortsetzen
-------------------

Bei weiteren Fragen können Sie direkt weiterfragen:

- "Können Sie das genauer erklären?"
- "Gibt es noch andere Möglichkeiten?"
- "Mehr Details zu XXX"

Der KI-Assistent berücksichtigt den Kontext des vorherigen Gesprächs bei seiner Antwort.

Neues Gespräch beginnen
-----------------------

Wenn Sie zu einem anderen Thema wechseln möchten, klicken Sie auf "Neuer Chat".
Dadurch wird der Gesprächsverlauf gelöscht und Sie können ein neues Gespräch beginnen.

Tipps für effektive Fragen
==========================

Konkret fragen
--------------

Konkrete Fragen liefern bessere Antworten als vage Fragen.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Vage Frage
     - Konkrete Frage
   * - Wie konfiguriert man das?
     - Wie ändere ich die Speichereinstellungen von Fess?
   * - Es gibt einen Fehler
     - Ich bekomme bei der Suche den Fehler "Index nicht gefunden"
   * - Über Crawling
     - Wie konfiguriere ich Ausschlussregeln beim Crawlen einer Website?

Hintergrundinformationen angeben
--------------------------------

Wenn Sie die Situation oder den Zweck beschreiben, erhalten Sie gezieltere Antworten.

Gute Beispiele:

- "Ich betreibe Fess in einer Docker-Umgebung. Wie kann ich den Log-Speicherort ändern?"
- "Ich benutze Fess zum ersten Mal. Was sollte ich zuerst tun?"

Schrittweise fragen
-------------------

Bei komplexen Problemen wird es durch schrittweises Fragen verständlicher.

1. "Kann Fess Dateifreigaben crawlen?"
2. "Wie verbinde ich mich über das SMB-Protokoll?"
3. "Was mache ich bei einem Freigabeordner mit Authentifizierung?"

Häufig gestellte Fragen
=======================

F: Die Chat-Funktion wird nicht angezeigt
-----------------------------------------

A: Möglicherweise ist die Chat-Funktion nicht aktiviert.
Fragen Sie Ihren Systemadministrator, ob die AI-Modus-Funktion aktiviert ist.

F: Die Antwort dauert lange
---------------------------

A: Da die KI die Suchergebnisse analysiert und eine Antwort generiert, kann es einige Sekunden bis mehrere Sekunden dauern.
Während der Verarbeitung wird die aktuelle Phase angezeigt ("Suche", "Analyse", "Antwortgenerierung" usw.).

F: Die Quellenangaben scheinen falsch zu sein
---------------------------------------------

A: Klicken Sie auf den Quellenlink, um das Originaldokument zu überprüfen.
Die KI generiert Antworten basierend auf Suchergebnissen, aber es kann zu Interpretationsfehlern kommen.
Bei wichtigen Informationen empfehlen wir, immer das Originaldokument zu überprüfen.

F: Das vorherige Gespräch scheint vergessen zu sein
---------------------------------------------------

A: Möglicherweise ist die Sitzung abgelaufen.
Nach einer gewissen Zeit ohne Aktivität wird der Gesprächsverlauf gelöscht.
Bitte starten Sie ein neues Gespräch.

F: Ich bekomme keine Antwort auf bestimmte Fragen
-------------------------------------------------

A: Mögliche Gründe:

- In den durchsuchten Dokumenten gibt es keine relevanten Informationen
- Die Frage ist zu vage für eine geeignete Suche
- Das Rate-Limit wurde erreicht

Versuchen Sie, die Frage umzuformulieren, oder warten Sie eine Weile und versuchen Sie es erneut.

F: Kann ich in anderen Sprachen als Deutsch fragen?
---------------------------------------------------

A: Ja, je nach Konfiguration können Sie in vielen Fällen auch auf Englisch oder in anderen Sprachen fragen.
Die KI erkennt die Sprache der Frage und versucht, in derselben Sprache zu antworten.

Hinweise
========

Über KI-Antworten
-----------------

- KI-Antworten werden basierend auf Suchergebnissen generiert
- Die Genauigkeit der Antworten ist nicht garantiert
- Bei wichtigen Entscheidungen überprüfen Sie immer das Originaldokument
- Aktuelle Informationen finden Sie in der offiziellen Dokumentation

Über Datenschutz
----------------

- Eingegebene Fragen werden für Suche und KI-Verarbeitung verwendet
- Der Gesprächsverlauf wird nach Sitzungsende gelöscht
- Je nach Systemeinstellungen können Protokolle aufgezeichnet werden

Referenzinformationen
=====================

- :doc:`search-and` - UND-Suche verwenden
- :doc:`search-not` - NICHT-Suche verwenden
- :doc:`search-field` - Feldsuche verwenden
- :doc:`advanced-search` - Erweiterte Suchfunktionen
