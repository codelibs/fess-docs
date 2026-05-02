==================
Bereichssuche
==================

Wenn Sie Daten, für die Bereichsangaben möglich sind, wie z. B. Zahlen, in einem Feld speichern, können Sie eine Bereichssuche für dieses Feld durchführen.

Verwendung
-----------

Um eine Bereichssuche durchzuführen, geben Sie "Feldname:[Wert TO Wert]" in das Suchformular ein.

Um beispielsweise Dokumente im content_length-Feld zu suchen, die zwischen 1 kByte und 10 kByte liegen, geben Sie Folgendes in das Suchformular ein:

::

    content_length:[1000 TO 10000]

Um eine Zeitbereichssuche durchzuführen, geben Sie "last_modified:[Datum/Zeit1 TO Datum/Zeit2]" (Datum/Zeit1 < Datum/Zeit2) in das Suchformular ein.

Datums-/Zeitangaben basieren auf ISO 8601.

.. list-table::

   * - Jahr, Monat, Tag sowie Stunde, Minute, Sekunde und Bruchteile
     - Bei Verwendung der aktuellen Zeit als Referenz
   * - YYYY-MM-DDThh:mm:sssZ (Beispiel: 2012-12-02T10:45:235Z)
     - now (aktuelle Zeit), y (Jahr), M (Monat), w (Woche), d (Tag), h (Stunde), m (Minute), s (Sekunde)

Bei Verwendung von now oder Zeit als Referenz können Symbole wie +, - (Addition, Subtraktion) und / (Rundung) hinzugefügt werden. Bei Verwendung von Zeit als Referenz muss jedoch || zwischen dem Symbol eingefügt werden.

/ ist ein Symbol zum Runden auf die Einheit nach /. now-1d/d repräsentiert 00:00 Uhr des Vortages, unabhängig davon, zu welcher Uhrzeit es am heutigen Tag ausgeführt wird (heutiger Tag 00:00 Uhr - 1 Tag).

Um beispielsweise Dokumente zu suchen, die im last_modified-Feld innerhalb der letzten 30 Tage ab dem 21. Februar 2016 um 20:00 Uhr (angenommene aktuelle Zeit) aktualisiert wurden, geben Sie Folgendes in das Suchformular ein:

::

    last_modified:[now-30d TO now](=[2016-01-23T00:00:000Z+TO+2016-02-21T20:00:000Z(aktuelle Zeit)])
