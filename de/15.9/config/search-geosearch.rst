=============
Standortsuche
=============

=========
Übersicht
=========

|Fess| kann geografische Bereichssuchen für Dokumente mit Breiten- und Längengraden durchführen.
Mit dieser Funktion können Sie Dokumente innerhalb einer bestimmten Entfernung von einem bestimmten Punkt suchen
oder Suchsysteme in Verbindung mit Kartendiensten wie Google Maps aufbauen.

Intern wird die geo-distance-Abfrage von OpenSearch verwendet, um Dokumente zu filtern,
die innerhalb einer angegebenen Entfernung vom angegebenen Mittelpunkt liegen.

===============
Anwendungsfälle
===============

Standortsuche kann für folgende Zwecke genutzt werden:

- Geschäftssuche: Suche nach Geschäften in der Nähe des aktuellen Standorts des Benutzers
- Immobiliensuche: Suche nach Immobilien innerhalb einer bestimmten Entfernung von einem Bahnhof oder einer Einrichtung
- Veranstaltungssuche: Suche nach Veranstaltungsinformationen in der Umgebung eines bestimmten Ortes
- Einrichtungssuche: Suche nach Sehenswürdigkeiten oder öffentlichen Einrichtungen in der Nähe

=============
Konfiguration
=============

Konfiguration bei der Indexgenerierung
---------------------------------------

Definition des Standortfeldes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In |Fess| ist ``location`` als Standardfeld für Standortinformationen definiert.
Dieses Feld ist als OpenSearch-Typ ``geo_point`` konfiguriert.

Registrierungsformat für Standortinformationen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bei der Indexgenerierung werden Breiten- und Längengrad durch Komma getrennt im ``location``-Feld festgelegt.

**Format:**

::

    Breitengrad,Längengrad

**Beispiel:**

::

    45.17614,-93.87341

.. note::
   Breitengrad wird im Bereich von -90 bis 90, Längengrad im Bereich von -180 bis 180 angegeben.

Konfigurationsbeispiel für Datenspeicher-Crawling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bei Verwendung von Datenspeicher-Crawling werden Breiten- und Längengrade
aus einer Datenquelle mit Standortinformationen im ``location``-Feld festgelegt.

**Beispiel: Abruf aus Datenbank**

Wenn Breiten- und Längengrad in getrennten Spalten gespeichert sind, verbinden Sie diese per SQL zu einer kommaseparierten Zeichenfolge.

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) AS location
    FROM stores

Im Konfigurationsskript des Datenspeichers ordnen Sie den abgerufenen Wert dem ``location``-Feld zu.

::

    location=data.location

Hinzufügen von Standortinformationen per Skript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sie können Standortinformationen auch dynamisch zu Dokumenten hinzufügen, indem Sie die Skriptfunktion (Groovy) der Crawl-Konfiguration verwenden.
Weisen Sie den Wert direkt dem Feldnamen zu.

::

    // Breiten- und Längengrad im location-Feld festlegen
    location="35.681236,139.767125"

Weitere Details zu Skripten finden Sie unter :doc:`scripting-groovy`.

Konfiguration bei der Suche
----------------------------

Für die Standortsuche geben Sie Mittelpunkt und Suchradius über Request-Parameter an.

Request-Parameter
~~~~~~~~~~~~~~~~~

Der Parametername für die Standortsuche hat das Format ``geo.<Feldname>.point`` und ``geo.<Feldname>.distance``.
Für ``<Feldname>`` wird der in ``query.geo.fields`` konfigurierte Feldname eingesetzt
(Standardwert: ``location``).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parametername
     - Beschreibung
   * - ``geo.location.point``
     - Breiten-/Längengrad des Suchmittelpunkts (durch Komma getrennt. Beispiel: ``35.681236,139.767125`` )
   * - ``geo.location.distance``
     - Suchradius vom Mittelpunkt (mit Einheit. Beispiel: ``10km`` )

.. note::
   ``point`` und ``distance`` müssen immer zusammen angegeben werden. Ein ``point`` ohne ``distance`` wird ignoriert.
   Außerdem muss der Wert von ``point`` aus genau zwei numerischen Werten (Breiten- und Längengrad) bestehen;
   bei ungültigem Format tritt ein Fehler auf.

.. note::
   Werden für dasselbe Feld mehrere ``point``-Werte angegeben, gelten diese als ODER-Bedingung (innerhalb eines der Bereiche).
   Werden Werte für mehrere Felder angegeben, gelten diese als UND-Bedingung (innerhalb aller Bereiche).

Entfernungseinheiten
~~~~~~~~~~~~~~~~~~~~

Für Entfernungen können folgende Einheiten verwendet werden:

- ``km``: Kilometer
- ``m``: Meter
- ``mi``: Meilen
- ``yd``: Yards

.. note::
   Da der Entfernungswert direkt an OpenSearch übergeben wird, können neben den oben genannten Einheiten
   auch alle anderen von OpenSearch unterstützten Einheiten verwendet werden
   ( ``cm`` , ``mm`` , ``ft`` , ``in`` , ``nmi`` usw.).

Reihenfolge der Suchergebnisse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Die Standortsuche wirkt als **Filter**, der die Ergebnisse auf Dokumente innerhalb des angegebenen Bereichs einschränkt.
Sie hat keinen Einfluss auf den Suchscore (Relevanz) und sortiert die Ergebnisse nicht nach der Entfernung vom Mittelpunkt.
Die Ergebnisse werden wie gewohnt nach Relevanz (oder der mit dem ``sort``-Parameter angegebenen Reihenfolge) zurückgegeben.

.. note::
   |Fess| unterstützt keine Sortierung nach Entfernung (Sortierung nach Nähe).
   Wenn Sie Ergebnisse nach Entfernung sortiert anzeigen möchten, verwenden Sie die im Response enthaltenen Koordinaten und sortieren Sie clientseitig.

=============
Suchbeispiele
=============

Grundlegende Suche
------------------

Suche nach Dokumenten innerhalb eines Radius von 10 km vom Bahnhof Tokyo (35.681236, 139.767125):

::

    http://localhost:8080/search?q=Suchschlüsselwort&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Suche in der Nähe des aktuellen Standorts
------------------------------------------

Suche innerhalb von 1 km vom aktuellen Standort des Benutzers:

::

    http://localhost:8080/search?q=Ramen&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Verwendung in der API
---------------------

Die Standortsuche kann auch über die JSON-Suche-API v2 ( ``/api/v2/search`` ) verwendet werden.
Geben Sie ``geo.location.point`` und ``geo.location.distance`` als Request-Parameter an.

::

    curl "http://localhost:8080/api/v2/search?q=Hotel&geo.location.point=35.681236,139.767125&geo.location.distance=5km"

Die Suchergebnisse werden im ``response.data``-Array des gemeinsamen Envelopes zurückgegeben. Weitere Details zur API finden Sie unter :doc:`../api/api-search`
und :doc:`../api/api-overview`.

.. note::
   Das ``location``-Feld ist standardmäßig nicht in der API-Antwort enthalten. Um Breiten- und Längengrad in den Suchergebnissen einzuschließen,
   fügen Sie folgende Einstellung in ``fess_config.properties`` hinzu:

   ::

       query.additional.api.response.fields=location

=======================
Anpassung von Feldnamen
=======================

Änderung des Standard-Feldnamens
---------------------------------

Um den für die Standortsuche verwendeten Feldnamen zu ändern,
passen Sie folgende Einstellung in ``fess_config.properties`` an:

::

    query.geo.fields=location

Zur Angabe mehrerer Feldnamen trennen Sie diese durch Kommas.

::

    query.geo.fields=location,geo_point,coordinates

.. note::
   - Der Name des Request-Parameters richtet sich nach dem konfigurierten Feldnamen. Bei der Einstellung
     ``query.geo.fields=coordinates`` werden beispielsweise ``geo.coordinates.point`` und
     ``geo.coordinates.distance`` verwendet.
   - Jedes hier angegebene Feld muss im Index-Mapping als ``geo_point``-Typ definiert sein.

=========================
Implementierungsbeispiele
=========================

Implementierung in einer Webanwendung
--------------------------------------

Beispiel für die Suche mit JavaScript unter Abruf des aktuellen Standorts:

.. code-block:: javascript

    // Aktuellen Standort mit der Browser-Geolocation-API abrufen
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const distance = "5km";

        // Such-URL erstellen
        const searchUrl = `/search?q=&geo.location.point=${latitude},${longitude}&geo.location.distance=${distance}`;

        // Suche ausführen
        window.location.href = searchUrl;
    });

Integration mit Google Maps
----------------------------

Beispiel für die Anzeige von Suchergebnissen als Marker auf Google Maps:

.. note::
   Dieses Beispiel greift auf das ``location``-Feld aus den Suchergebnissen zu. Setzen Sie zuvor
   ``query.additional.api.response.fields=location``, um die Koordinaten in der Antwort einzuschließen.

.. code-block:: javascript

    // Karte initialisieren
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Standortsuche mit der Fess v2-Suche-API ausführen
    fetch('/api/v2/search?q=Geschäfte&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(json => {
            // Suchergebnisse (response.data-Array) als Marker anzeigen
            json.response.data.forEach(doc => {
                if (doc.location) {
                    const [lat, lng] = doc.location.split(',').map(Number);
                    new google.maps.Marker({
                        position: {lat: lat, lng: lng},
                        map: map,
                        title: doc.title
                    });
                }
            });
        });

====================
Leistungsoptimierung
====================

Überprüfung der Indexeinstellungen
------------------------------------

Das Standortfeld ist in der Installationsumgebung unter
``app/WEB-INF/classes/fess_indices/fess/doc.json`` als ``geo_point``-Typ definiert.

::

    "location": {
        "type": "geo_point"
    }

Da Felder vom Typ ``geo_point`` im BKD-Baum indexiert werden, werden geo-distance-Abfragen effizient ausgeführt.

Optimierung von Suchbereich und Antwort
-----------------------------------------

Ein größerer Suchradius erhöht die Anzahl der übereinstimmenden Dokumente, was das Abrufen und Rendern der Ergebnisse verlangsamen kann.

- Legen Sie je nach Verwendungszweck einen angemessenen Suchradius fest.
- Wenn viele Ergebnisse für die Kartenanzeige verarbeitet werden, begrenzen Sie die Anzahl der abgerufenen Einträge durch Anpassen der Seitengröße (``num``-Parameter).

==============
Fehlerbehebung
==============

Standortsuche funktioniert nicht
----------------------------------

1. Überprüfen Sie, ob Daten korrekt im ``location``-Feld gespeichert sind.
2. Überprüfen Sie, ob das Format für Breiten-/Längengrad korrekt ist (durch Komma getrennt: ``Breitengrad,Längengrad``; bei nicht genau zwei Werten tritt ein Fehler auf).
3. Überprüfen Sie, ob ``location`` im OpenSearch-Index-Mapping als ``geo_point``-Typ definiert ist.
4. Überprüfen Sie, ob sowohl ``point`` als auch ``distance`` angegeben sind (ein ``point`` ohne ``distance`` wird ignoriert).

Keine Suchergebnisse zurückgegeben
------------------------------------

1. Überprüfen Sie, ob Dokumente innerhalb der angegebenen Entfernung existieren.
2. Überprüfen Sie, ob die Breiten-/Längengradwerte im korrekten Bereich liegen (Breitengrad: -90 bis 90, Längengrad: -180 bis 180).
3. Überprüfen Sie, ob die Entfernungseinheit korrekt angegeben ist.

API-Antwort enthält keine Standortinformationen
------------------------------------------------

Das ``location``-Feld ist standardmäßig nicht in der API-Antwort enthalten.
Um Koordinaten in die Suchergebnisse aufzunehmen, setzen Sie
``query.additional.api.response.fields=location`` in ``fess_config.properties``.

Standortinformationen werden nicht korrekt gespeichert
-------------------------------------------------------

1. Überprüfen Sie, ob das ``location``-Feld beim Crawling korrekt gesetzt wird.
2. Überprüfen Sie, ob Breiten-/Längengrad aus der Datenquelle korrekt abgerufen werden.
3. Wenn Standortinformationen per Skript gesetzt werden, überprüfen Sie, ob das Zeichenfolgenformat ``Breitengrad,Längengrad`` korrekt ist.

=====================
Referenzinformationen
=====================

Weitere Details zur Standortsuche finden Sie in folgenden Ressourcen:

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/de/docs/Web/API/Geolocation_API>`_
