============
Standortsuche
============

Übersicht
====

|Fess| kann geografische Bereichssuchen für Dokumente mit Breiten- und Längengraden durchführen.
Mit dieser Funktion können Sie Dokumente innerhalb einer bestimmten Entfernung von einem bestimmten Punkt suchen
oder Suchsysteme in Verbindung mit Kartendiensten wie Google Maps erstellen.

Anwendungsfälle
============

Standortsuche kann für folgende Zwecke genutzt werden:

- Geschäftssuche: Suche nach Geschäften in der Nähe des aktuellen Standorts des Benutzers
- Immobiliensuche: Suche nach Immobilien innerhalb einer bestimmten Entfernung von einem bestimmten Bahnhof oder einer Einrichtung
- Veranstaltungssuche: Suche nach Veranstaltungsinformationen in der Umgebung eines bestimmten Ortes
- Einrichtungssuche: Suche nach Sehenswürdigkeiten oder öffentlichen Einrichtungen in der Nähe

Konfigurationsmethode
========

Konfiguration bei Indexgenerierung
------------------------

Definition des Standortfeldes
~~~~~~~~~~~~~~~~~~~~~~~~

In |Fess| ist ``location`` als Standardfeld für Standortinformationen definiert.
Dieses Feld ist als OpenSearch-Typ ``geo_point`` konfiguriert.

Registrierungsformat für Standortinformationen
~~~~~~~~~~~~~~~~~~

Bei Indexgenerierung werden Breiten- und Längengrad durch Komma getrennt im ``location``-Feld festgelegt.

**Format:**

::

    Breitengrad,Längengrad

**Beispiel:**

::

    45.17614,-93.87341

.. note::
   Breitengrad wird im Bereich von -90 bis 90, Längengrad im Bereich von -180 bis 180 angegeben.

Konfigurationsbeispiel für Datenspeicher-Crawling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bei Verwendung von Datenspeicher-Crawling werden Breiten- und Längengrade
aus einer Datenquelle mit Standortinformationen im ``location``-Feld festgelegt.

**Beispiel: Abruf aus Datenbank**

::

    SELECT
        id,
        name,
        address,
        CONCAT(latitude, ',', longitude) as location
    FROM stores

Hinzufügen von Standortinformationen per Skript
~~~~~~~~~~~~~~~~~~~~~~~~~~

Sie können auch dynamisch Standortinformationen zu Dokumenten hinzufügen, indem Sie die Skriptfunktion der Crawl-Konfiguration verwenden.

::

    // Breiten- und Längengrad im location-Feld festlegen
    doc.location = "35.681236,139.767125";

Konfiguration bei Suche
------------

Für Standortsuche geben Sie Mittelpunkt und Bereich der Suche über Request-Parameter an.

Request-Parameter
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parametername
     - Beschreibung
   * - ``geo.location.point``
     - Breiten-/Längengrad des Suchmittelpunkts (durch Komma getrennt)
   * - ``geo.location.distance``
     - Suchradius vom Mittelpunkt (mit Einheit)

Entfernungseinheiten
~~~~~~~~~~

Für Entfernungen können folgende Einheiten verwendet werden:

- ``km``: Kilometer
- ``m``: Meter
- ``mi``: Meilen
- ``yd``: Yards

Suchbeispiele
======

Grundlegende Suche
------------

Suche nach Dokumenten innerhalb eines Radius von 10 km vom Bahnhof Tokyo (35.681236, 139.767125):

::

    http://localhost:8080/search?q=Suchschlüsselwort&geo.location.point=35.681236,139.767125&geo.location.distance=10km

Suche in der Nähe des aktuellen Standorts
----------------

Suche innerhalb 1 km vom aktuellen Standort des Benutzers:

::

    http://localhost:8080/search?q=Ramen&geo.location.point=35.681236,139.767125&geo.location.distance=1km

Sortierung nach Entfernung
----------------

Um Suchergebnisse nach Entfernung zu sortieren, verwenden Sie den ``sort``-Parameter.

::

    http://localhost:8080/search?q=Convenience&geo.location.point=35.681236,139.767125&geo.location.distance=5km&sort=location.distance

Verwendung in API
-----------

Standortsuche kann auch in JSON-API verwendet werden.

::

    curl -X POST "http://localhost:8080/json/?q=Hotel" \
      -H "Content-Type: application/json" \
      -d '{
        "geo.location.point": "35.681236,139.767125",
        "geo.location.distance": "5km"
      }'

Anpassung von Feldnamen
==========================

Änderung des Standard-Feldnamens
----------------------------

Um den für Standortsuche verwendeten Feldnamen zu ändern,
ändern Sie in ``fess_config.properties`` folgende Einstellung:

::

    query.geo.fields=location

Zur Angabe mehrerer Feldnamen trennen Sie diese durch Kommas.

::

    query.geo.fields=location,geo_point,coordinates

Implementierungsbeispiele
======

Implementierung in Webanwendung
---------------------------

Beispiel für Suche mit JavaScript unter Abruf des aktuellen Standorts:

.. code-block:: javascript

    // Aktuellen Standort mit Browser-Geolocation-API abrufen
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
--------------------

Beispiel für Anzeige von Suchergebnissen als Marker auf Google Maps:

.. code-block:: javascript

    // Karte initialisieren
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.681236, lng: 139.767125},
        zoom: 13
    });

    // Standortsuche mit Fess-API ausführen
    fetch('/json/?q=Geschäfte&geo.location.point=35.681236,139.767125&geo.location.distance=5km')
        .then(response => response.json())
        .then(data => {
            // Suchergebnisse als Marker anzeigen
            data.response.result.forEach(doc => {
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

Leistungsoptimierung
====================

Optimierung der Indexeinstellungen
------------------------

Bei Umgang mit großen Mengen an Standortdaten optimieren Sie Indexeinstellungen.

Überprüfen Sie Standortfeld-Einstellungen in ``app/WEB-INF/classes/fess_indices/fess.json``.

::

    "location": {
        "type": "geo_point"
    }

Beschränkung des Suchbereichs
--------------

Aus Leistungsgründen wird empfohlen, den Suchbereich auf das notwendige Minimum zu beschränken.

- Weitreichende Suchen (50 km oder mehr) können längere Verarbeitungszeiten erfordern
- Konfigurieren Sie angemessene Bereiche je nach Verwendungszweck

Fehlersuche
======================

Standortsuche funktioniert nicht
------------------------

1. Überprüfen Sie, ob Daten korrekt im ``location``-Feld gespeichert sind.
2. Überprüfen Sie, ob das Breiten-/Längengrad-Format korrekt ist (durch Komma getrennt).
3. Überprüfen Sie, ob ``location`` im OpenSearch-Index-Mapping als ``geo_point``-Typ definiert ist.

Keine Suchergebnisse zurückgegeben
----------------------

1. Überprüfen Sie, ob Dokumente innerhalb der angegebenen Entfernung existieren.
2. Überprüfen Sie, ob Breiten-/Längengradwerte im korrekten Bereich liegen (Breitengrad: -90~90, Längengrad: -180~180).
3. Überprüfen Sie, ob Entfernungseinheit korrekt angegeben ist.

Standortinformationen werden nicht korrekt angezeigt
----------------------------

1. Überprüfen Sie, ob ``location``-Feld beim Crawling korrekt festgelegt wurde.
2. Überprüfen Sie, ob Breiten-/Längengrad-Datentyp in der Datenquelle numerisch ist.
3. Bei Festlegung von Standortinformationen per Skript überprüfen Sie, ob das Zeichenfolgen-Konkatenationsformat korrekt ist.

Referenzinformationen
========

Für Details zur Standortsuche siehe folgende Ressourcen:

- `OpenSearch Geo Queries <https://opensearch.org/docs/latest/query-dsl/geo-and-xy/index/>`_
- `OpenSearch Geo Point <https://opensearch.org/docs/latest/field-types/supported-field-types/geo-point/>`_
- `Geolocation API (MDN) <https://developer.mozilla.org/de/docs/Web/API/Geolocation_API>`_
