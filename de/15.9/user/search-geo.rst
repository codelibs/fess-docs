=========================
Standortbasierte Suche
=========================

Indem Sie bei der Indexerstellung jedem Dokument Standortinformationen (Breiten- und Längengrad) hinzufügen, können Sie bei der Suche nach dem Abstand von einem angegebenen Punkt filtern.

Übersicht
------------

Bei der standortbasierten Suche werden nur Dokumente in die Suchergebnisse aufgenommen, die sich innerhalb eines Radius um einen angegebenen Punkt (Breiten- und Längengrad) befinden. Diese Einschränkung wird als Filter mithilfe einer geo_distance-Abfrage von OpenSearch angewendet und wirkt sich daher nicht auf die Bewertung (Relevanz) aus. Zudem wird eine Sortierung nach Entfernung nicht unterstützt.

Das Feld, in dem die Standortinformationen gespeichert werden, muss im OpenSearch-Mapping als Typ ``geo_point`` definiert sein. Standardmäßig ist das Feld ``location`` als Typ ``geo_point`` vorbereitet. Da jedoch standardmäßig kein Mechanismus zum Speichern von Werten im Feld ``location`` bereitgestellt wird, müssen Sie die Standortinformationen selbst hinterlegen, etwa über die Feldzuordnung beim Data-Store-Crawling, per Skript oder über die API zum Registrieren von Dokumenten in der Suchmaschine.

Verwendung
-------------

Die standortbasierte Suche wird angegeben, indem Sie der Suchanfrage die folgenden Parameter hinzufügen. Standardmäßig ist sie für das Feld ``location`` verfügbar.

.. list-table::
   :header-rows: 1

   * - Parameter
     - Beschreibung
   * - ``geo.<fieldname>.point``
     - Geben Sie Breiten- und Längengrad des Mittelpunkts im Format ``Breitengrad,Längengrad`` an. Die Werte sind Dezimalgrad (Typ Double); geben Sie zwei durch Komma getrennte Zahlen an. Beispiel: ``35.681236,139.767125``
   * - ``geo.<fieldname>.distance``
     - Geben Sie die Entfernung (den Radius) vom Mittelpunkt an. Beispiel: ``10km``

Tabelle: Anfrageparameter

Für ``<fieldname>`` geben Sie den Namen des Feldes an, in dem die Standortinformationen gespeichert sind. Angegeben werden können nur Felder, die in ``query.geo.fields`` registriert sind; standardmäßig ist dies ``location``. Um ein anderes Feld zu verwenden, mappen Sie es als Typ ``geo_point`` und fügen Sie es durch Komma getrennt in ``query.geo.fields`` in ``fess_config.properties`` hinzu.

Um beispielsweise Dokumente innerhalb eines Radius von 10 km um den Punkt mit Breitengrad 35.681236 und Längengrad 139.767125 (in der Nähe des Bahnhofs Tokio) zu suchen, fügen Sie der Suchanfrage die folgenden Parameter hinzu.

::

    geo.location.point=35.681236,139.767125&geo.location.distance=10km

Entfernungseinheiten
------------------------

Der Wert von ``geo.<fieldname>.distance`` wird als Entfernungseinheit von OpenSearch interpretiert. Neben ``km`` (Kilometer) können unter anderem ``mm``, ``cm``, ``m``, ``in``, ``ft``, ``yd``, ``mi`` (Meilen) und ``nmi`` (Seemeilen) verwendet werden. Wird die Einheit weggelassen und nur eine Zahl angegeben, wird diese als Meter interpretiert (Beispiel: ``500`` entspricht 500 Metern).

Mehrfachangabe
-----------------

* Wenn Sie für dasselbe Feld mehrere ``geo.<fieldname>.point``-Werte angeben, werden Dokumente gesucht, die sich innerhalb des Radius mindestens eines der Punkte befinden (ODER-Bedingung).
* Wenn Sie für unterschiedliche Felder jeweils Standortinformationen angeben, werden Dokumente gesucht, die alle Bedingungen erfüllen (UND-Bedingung).

.. note::

   ``geo.<fieldname>.point`` und ``geo.<fieldname>.distance`` müssen beide angegeben werden. Wird ``distance`` nicht angegeben, wird die Bedingung für dieses ``point`` ignoriert. Zudem tritt ein Fehler auf, wenn der Wert von ``point`` nicht dem Format ``Breitengrad,Längengrad`` (zwei durch Komma getrennte Zahlen) entspricht oder nicht als Zahl interpretiert werden kann.
