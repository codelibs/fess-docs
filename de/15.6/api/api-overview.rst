==============
API-Übersicht
==============


Von |Fess| bereitgestellte APIs
================================

Diese Dokumentation beschreibt die von |Fess| bereitgestellten APIs.
Durch die Verwendung der API können Sie |Fess| auch in bestehenden Websystemen als Suchserver einsetzen.

Basis-URL
=========

Die API-Endpunkte von |Fess| werden unter folgender Basis-URL bereitgestellt:

::

    http://<Servername>/api/v1/

Beispielsweise sieht die URL bei einem lokal betriebenen System wie folgt aus:

::

    http://localhost:8080/api/v1/

Authentifizierung
=================

In der aktuellen Version ist für die Nutzung der API keine Authentifizierung erforderlich.
Allerdings müssen die APIs in den verschiedenen Einstellungen der Administrationsoberfläche aktiviert werden.

HTTP-Methoden
=============

Auf alle API-Endpunkte wird mit der **GET**-Methode zugegriffen.

Antwortformat
=============

Alle API-Antworten werden im **JSON-Format** zurückgegeben (mit Ausnahme der GSA-kompatiblen API).
Der ``Content-Type`` der Antwort ist ``application/json``.

Fehlerbehandlung
================

Wenn eine API-Anfrage fehlschlägt, werden Fehlerinformationen zusammen mit einem entsprechenden HTTP-Statuscode zurückgegeben.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: HTTP-Statuscodes

   * - 200
     - Die Anfrage wurde erfolgreich verarbeitet.
   * - 400
     - Die Anfrageparameter sind ungültig.
   * - 404
     - Die angeforderte Ressource wurde nicht gefunden.
   * - 500
     - Es ist ein interner Serverfehler aufgetreten.

Tabelle: HTTP-Statuscodes

API-Typen
=========

|Fess| stellt folgende APIs bereit:

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - API zum Abrufen von Suchergebnissen.
   * - popularword
     - API zum Abrufen beliebter Suchbegriffe.
   * - label
     - API zum Abrufen der Liste erstellter Labels.
   * - health
     - API zum Abrufen des Serverstatus.
   * - suggest
     - API zum Abrufen von Vorschlagswörtern.

Tabelle: API-Typen
