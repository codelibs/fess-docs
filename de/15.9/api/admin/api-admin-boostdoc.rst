==========================
BoostDoc API
==========================

Übersicht
=========

Die BoostDoc API dient zur Verwaltung der Dokument-Boost-Konfiguration in |Fess|.
Durch die Konfiguration von Dokument-Boosts können Sie den Score von Dokumenten, die bestimmten Bedingungen entsprechen, anheben
und dadurch erreichen, dass diese Dokumente in den Suchergebnissen weiter oben erscheinen.

Boosts werden zum Zeitpunkt der Indexierung (beim Crawlen) auf die einzelnen Dokumente angewendet.
Sowohl die Bedingung (``urlExpr``) als auch der Boost-Wert (``boostExpr``) werden mit der im Feld ``scriptType``
angegebenen Skript-Engine ausgewertet. Für ``scriptType`` können Sie ``javascript`` oder ``groovy`` (erfordert
das Plugin ``fess-script-groovy``) angeben. Der Erstellungsbildschirm der Administrationsoberfläche füllt
``scriptType`` mit ``javascript`` vor; wird ``scriptType`` im Request-Body dieser API jedoch weggelassen, erfolgt
keine automatische Vorbelegung, und die Ausdrücke werden als Groovy ausgewertet.
Mehrere Regeln werden in aufsteigender Reihenfolge von ``sortOrder`` ausgewertet; nur der Boost-Wert der ersten zutreffenden Regel wird angewendet
(sobald eine passende Regel gefunden wurde, werden die nachfolgenden Regeln nicht mehr ausgewertet).

.. note::

   In der Administrationsoberfläche wird ``urlExpr`` als „Bedingung", ``boostExpr`` als „Boost-Wert-Ausdruck" und
   ``scriptType`` als „Skripttyp" angezeigt. ``scriptType`` erscheint nur in den Request-Bodies und Responses
   von Erstellung/Aktualisierung/Abruf (Liste und Einzelabruf), nicht bei den Filterparametern der Listenabfrage
   (``urlExpr``, ``boostExpr``).
   Einzelheiten zu den Konfigurationsfeldern finden Sie unter :doc:`../../admin/boostdoc-guide`.

Basis-URL
=========

::

    /api/admin/boostdoc

Authentifizierung
=================

Für die Nutzung dieser API ist ein Access Token mit der Berechtigung ``Radmin-api`` erforderlich.
Informationen zum Erhalt und zur Angabe des Access Tokens finden Sie unter :doc:`api-admin-overview`.

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /settings
     - Dokument-Boost-Liste abrufen
   * - GET
     - /setting/{id}
     - Dokument-Boost abrufen
   * - POST
     - /setting
     - Dokument-Boost erstellen
   * - PUT
     - /setting
     - Dokument-Boost aktualisieren
   * - DELETE
     - /setting/{id}
     - Dokument-Boost löschen

Dokument-Boost-Liste abrufen
=============================

Request
-------

::

    GET /api/admin/boostdoc/settings

Parameter
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parameter
     - Typ
     - Erforderlich
     - Beschreibung
   * - ``size``
     - Integer
     - Nein
     - Anzahl der Einträge pro Seite (Standard: 25)
   * - ``page``
     - Integer
     - Nein
     - Seitennummer (beginnt bei 1, Standard: 1)
   * - ``urlExpr``
     - String
     - Nein
     - Filterung nach Bedingungsausdruck (Teilübereinstimmung)
   * - ``boostExpr``
     - String
     - Nein
     - Filterung nach Boost-Wert-Ausdruck (Teilübereinstimmung)

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
            "boostExpr": "3.0",
            "scriptType": "javascript",
            "sortOrder": 1,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   Jedes Einstellungsobjekt in der Antwort enthält neben den oben gezeigten Feldern auch Metadaten zur Erstellung und Aktualisierung (``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``).
   ``versionNo`` ist bei der Aktualisierung (PUT) erforderlich; rufen Sie den aktuellen Wert daher zuvor über die Get- oder List-API ab.

Dokument-Boost abrufen
======================

Request
-------

::

    GET /api/admin/boostdoc/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
          "boostExpr": "3.0",
          "scriptType": "javascript",
          "sortOrder": 1,
          "versionNo": 1
        }
      }
    }

Dokument-Boost erstellen
========================

Request
-------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "5.0",
      "scriptType": "javascript",
      "sortOrder": 0
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``urlExpr``
     - Ja
     - Bedingungsausdruck. Ein Skript-Ausdruck, der bestimmt, ob ein Dokument geboostet werden soll; muss einen ``Boolean``-Wert zurückgeben. Entspricht dem Feld „Bedingung" in der Administrationsoberfläche (maximal 10000 Zeichen).
   * - ``boostExpr``
     - Ja
     - Boost-Wert-Ausdruck. Ein Skript-Ausdruck, der den Boost-Wert (Zahl) zurückgibt. Es kann auch ein fester Wert wie ``3.0`` angegeben werden. Entspricht dem Feld „Boost-Wert-Ausdruck" in der Administrationsoberfläche (maximal 10000 Zeichen).
   * - ``scriptType``
     - Nein
     - Die Skript-Engine zur Auswertung von ``urlExpr`` und ``boostExpr``. Entweder ``javascript`` oder ``groovy`` (erfordert das Plugin ``fess-script-groovy``). Entspricht dem Feld „Skripttyp" in der Administrationsoberfläche (maximal 100 Zeichen). Wird das Feld weggelassen, werden die Ausdrücke als Groovy ausgewertet.
   * - ``sortOrder``
     - Ja
     - Anwendungsreihenfolge. Regeln werden in aufsteigender Reihenfolge ausgewertet; der Boost-Wert der ersten zutreffenden Regel wird angewendet (Formular-Standardwert: 0; ganze Zahl ≥ 0).

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

Dokument-Boost aktualisieren
============================

Request
-------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "scriptType": "javascript",
      "sortOrder": 0,
      "versionNo": 1
    }

Bei der Aktualisierung sind zusätzlich zu den Feldern beim Erstellen ``id`` (ID der Zielregel, bis zu 1000 Zeichen) und ``versionNo`` (Versionsnummer für optimistisches Sperren) erforderlich.
Geben Sie für ``versionNo`` den aktuellen Wert aus der Antwort der Get- oder List-API an.
Die Aktualisierung schlägt fehl, wenn die Versionsnummer nicht übereinstimmt.

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

Dokument-Boost löschen
=======================

Request
-------

::

    DELETE /api/admin/boostdoc/setting/{id}

Response
--------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Bedingungsausdrücke und Boost-Wert-Ausdrücke
============================================

Sowohl ``urlExpr`` (Bedingung) als auch ``boostExpr`` (Boost-Wert-Ausdruck) werden mit der über ``scriptType``
angegebenen Skript-Engine ausgewertet (Standard: Groovy; nur der Erstellungsbildschirm der
Administrationsoberfläche füllt ``javascript`` vor).
Innerhalb eines Ausdrucks können Sie auf die Feldwerte des zu indexierenden Dokuments über Variablen mit dem jeweiligen Feldnamen zugreifen.

- ``urlExpr`` muss einen ``Boolean``-Wert zurückgeben (Beispiel: ``url.startsWith("https://docs.example.com/")``). Ein einfacher regulärer Ausdrucks-String (z. B. ``.*docs\.example\.com.*``) gibt als Skript-Ausdruck keinen ``Boolean``-Wert zurück und funktioniert daher nicht als Bedingung. Für reguläre Ausdrücke verwenden Sie ``String#matches`` (in Groovy und JavaScript mit derselben Schreibweise verfügbar).
- ``boostExpr`` muss einen numerischen Wert zurückgeben. Das Ergebnis wird in ``float`` umgewandelt; ein Boost wird nur angewendet, wenn der Wert größer als 0 ist.

.. note::

   Wichtige Feldvariablen, die innerhalb von Ausdrücken referenziert werden können: ``url``, ``title``, ``content``, ``content_length``, ``last_modified`` usw.
   ``click_count`` und ``favorite_count`` stehen zur Verfügung, wenn jeweils ``indexer.click.count.enabled`` bzw.
   ``indexer.favorite.count.enabled`` aktiviert ist (beide standardmäßig aktiviert).
   Die OpenSearch-Datumsberechnungssyntax wie ``now - 7d`` kann weder in Groovy noch in JavaScript verwendet werden.

Beispiele für Bedingungsausdrücke (``urlExpr``)
-----------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Bedingungsausdruck
     - Beschreibung
   * - ``url.startsWith("https://docs.example.com/")``
     - Dokumente, deren URL mit dem angegebenen Wert beginnt, als Ziel festlegen
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - URL per regulärem Ausdruck prüfen (``String#matches``)
   * - ``title.contains("Versionshinweise")``
     - Dokumente, deren Titel einen bestimmten Begriff enthält, als Ziel festlegen

Beispiele für Boost-Wert-Ausdrücke (``boostExpr``)
---------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Boost-Wert-Ausdruck
     - Beschreibung
   * - ``3.0``
     - Boost mit einem festen Wert
   * - ``click_count * 0.1 + 1``
     - Boost proportional zur Klickanzahl
   * - ``Math.log(click_count + 1)``
     - Boost auf logarithmischer Skala basierend auf der Klickanzahl

Verwendungsbeispiele
====================

Dokumentations-Website boosten
-------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

Inhalte mit vielen Klicks boosten
----------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://www.example.com/\")",
           "boostExpr": "click_count * 0.1 + 1",
           "sortOrder": 10
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-elevateword` - ElevateWord API
- :doc:`../../admin/boostdoc-guide` - Dokument-Boost-Verwaltungsanleitung
