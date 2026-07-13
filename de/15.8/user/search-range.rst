=============
Bereichssuche
=============

Wenn Sie in einem Feld Daten speichern, für die sich ein Bereich angeben lässt, wie z. B. Zahlen oder Datums-/Zeitangaben, können Sie für dieses Feld eine Bereichssuche durchführen.

Verwendung
----------

Um eine Bereichssuche durchzuführen, geben Sie "Feldname:[Wert TO Wert]" in das Suchformular ein. Als Trennzeichen für den Bereich wird das großgeschriebene ``TO`` in Halbbreitenschreibweise verwendet.

Um beispielsweise Dokumente zu suchen, deren content_length-Feld einen Wert zwischen 1 kByte und 10 kByte hat, geben Sie Folgendes in das Suchformular ein:

::

    content_length:[1000 TO 10000]

Eckige Klammern ``[ ]`` schließen die Bereichsgrenzen ein (größer/gleich bzw. kleiner/gleich), geschweifte Klammern ``{ }`` schließen die Bereichsgrenzen aus (größer als bzw. kleiner als). Beide Klammertypen lassen sich auch kombinieren. So steht ``content_length:{1000 TO 10000]`` beispielsweise für Dokumente, deren Wert größer als 1000 und kleiner oder gleich 10000 ist.

Setzen Sie eine Seite auf ``*``, geben Sie damit einen offenen Bereich an, bei dem nur die Ober- oder Untergrenze festgelegt ist. ``content_length:[1000 TO *]`` steht für "größer oder gleich 1000", ``content_length:[* TO 10000]`` für "kleiner oder gleich 10000".

Die Bereichssuche ist nur für Felder verfügbar, die als Suchziel registriert sind. Standardmäßig lässt sich die Bereichssuche für Felder wie content_length, last_modified, timestamp, click_count und favorite_count verwenden.

Zeitbereichssuche
-----------------

Um eine Bereichssuche nach Zeit (Datum/Uhrzeit) durchzuführen, geben Sie "last_modified:[Datum/Zeit1 TO Datum/Zeit2]" (Datum/Zeit1 < Datum/Zeit2) in das Suchformular ein. Liegt Datum/Zeit1 dabei nach Datum/Zeit2, führt dies nicht zu einem Fehler, sondern liefert lediglich 0 Treffer.

Datum und Uhrzeit werden im Format ISO 8601 angegeben. Das Format lautet ``YYYY-MM-DDThh:mm:ss.SSSZ``, wobei die Uhrzeit und alles danach weggelassen werden kann.

.. list-table::
   :header-rows: 1

   * - Angabe
     - Beispiel
   * - Nur Jahr, Monat, Tag
     - 2012-12-02
   * - Jahr, Monat, Tag sowie Stunde, Minute, Sekunde
     - 2012-12-02T10:45:23Z
   * - Jahr, Monat, Tag sowie Stunde, Minute, Sekunde (bis Millisekunden)
     - 2012-12-02T10:45:23.235Z

Bei der Angabe von Datum und Uhrzeit können Sie eine Datums-/Zeitarithmetik verwenden, die auf dem aktuellen Zeitpunkt basiert. Die verfügbaren Symbole sind wie folgt:

.. list-table::
   :header-rows: 1

   * - Symbol
     - Bedeutung
   * - ``now``
     - Aktuelles Datum/Aktuelle Uhrzeit
   * - ``y`` / ``M`` / ``w`` / ``d`` / ``h`` / ``m`` / ``s``
     - Jahr / Monat / Woche / Tag / Stunde / Minute / Sekunde
   * - ``+`` / ``-``
     - Addition / Subtraktion
   * - ``/``
     - Runden (auf die Einheit nach ``/``)

Wenn Sie ``now`` oder ein bestimmtes Datum/eine bestimmte Uhrzeit als Referenz verwenden, können Sie Symbole wie ``+``, ``-`` (Addition, Subtraktion) oder ``/`` (Runden) anhängen. Verwenden Sie jedoch nicht ``now``, sondern ein bestimmtes Datum/eine bestimmte Uhrzeit als Referenz, müssen Sie zwischen Datum/Uhrzeit und dem Symbol ``||`` einfügen (Beispiel: ``2016-01-01||+1M/d``).

``/`` ist ein Symbol, das auf die dem ``/`` folgende Einheit rundet. ``now-1d/d`` steht unabhängig davon, um welche Uhrzeit die Suche heute ausgeführt wird, für 00:00 Uhr des Vortages, also für 00:00 Uhr des heutigen Tages minus 1 Tag.

Diese Datums-/Zeitarithmetik wird auf Seiten der Suchmaschine (OpenSearch) ausgewertet und ist nur für Felder vom Datums-/Zeittyp gültig.

Um beispielsweise Dokumente zu suchen, deren last_modified-Feld einen Wert zwischen dem aktuellen Datum (angenommen 21. Februar 2016, 20 Uhr) und 30 Tagen davor aufweist, geben Sie Folgendes in das Suchformular ein:

::

    last_modified:[now-30d TO now]

Ist die aktuelle Zeit der 21. Februar 2016, 20 Uhr (UTC), entspricht dies ungefähr dem Bereich ``[2016-01-22T20:00:00Z TO 2016-02-21T20:00:00Z]``.
