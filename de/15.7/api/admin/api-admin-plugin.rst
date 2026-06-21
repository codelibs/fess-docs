==========================
Plugin API
==========================

Übersicht
=========

Die Plugin API dient zur Verwaltung von Plugins (Artefakten) in |Fess|.
Sie können installierte und installierbare Plugins auflisten sowie Plugins installieren und löschen.

Basis-URL
=========

::

    /api/admin/plugin

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /installed
     - Installierte Plugins auflisten
   * - GET
     - /available
     - Installierbare Plugins auflisten
   * - POST
     - /
     - Plugin installieren
   * - DELETE
     - /
     - Plugin löschen

Felder der Plugin-Informationen
================================

Jedes Element des ``plugins``-Arrays, das von den Auflistungs-Endpunkten (``/installed`` und ``/available``) zurückgegeben wird, ist ein Objekt mit den folgenden Feldern.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Feld
     - Beschreibung
   * - ``type``
     - Typ-ID des Artefakts. Einer der folgenden Werte: ``fess-ds`` (Datenspeicher), ``fess-theme`` (Theme),
       ``fess-ingest`` (Ingest), ``fess-script`` (Skript), ``fess-webapp`` (Web-App),
       ``fess-thumbnail`` (Thumbnail), ``fess-crawler`` (Crawler), ``fess-llm`` (LLM),
       ``jar`` (allgemeine JAR-Datei für alle anderen Fälle).
   * - ``id``
     - Bezeichner im Format ``{name}:{version}``.
   * - ``name``
     - Plugin-Name.
   * - ``version``
     - Plugin-Version.
   * - ``url``
     - URL der Download-Quelle. Nur in der Antwort von ``/available`` enthalten. Bei ``/installed``
       ist kein Wert vorhanden, daher wird das Feld weggelassen.

.. note::

   In den API-Antworten von |Fess| werden Felder mit dem Wert ``null`` nicht ausgegeben. Daher
   enthält jedes Element der installierten Plugins kein ``url``-Feld.

Installierte Plugins auflisten
==============================

Gibt die Liste der installierten Plugins zurück. Die Artefakte im Plugin-Verzeichnis werden
nach Typ durchsucht, alphabetisch nach Namen sortiert und zurückgegeben.

Request
-------

::

    GET /api/admin/plugin/installed

Response
--------

In ``plugins`` wird ein Array von Objekten gespeichert, die die Plugin-Informationen darstellen.
Die Felder jedes Objekts sind unter `Felder der Plugin-Informationen`_ beschrieben.
Bei installierten Plugins wird ``url`` nicht ausgegeben.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

Installierbare Plugins auflisten
================================

Gibt die Liste der installierbaren Plugins zurück. Die Artefakte aller Typen werden aus den
Repositorys abgerufen, die in ``plugin.repositories`` der ``fess_config.properties`` konfiguriert sind.
Das Ergebnis wird für eine bestimmte Zeit (standardmäßig 5 Minuten) zwischengespeichert.

Request
-------

::

    GET /api/admin/plugin/available

Response
--------

In ``plugins`` wird ein Array von Objekten gespeichert, die die Informationen der installierbaren Plugins darstellen.
Die Felder jedes Objekts sind unter `Felder der Plugin-Informationen`_ beschrieben.
Bei installierbaren Plugins ist die Download-Quelle ``url`` enthalten.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.7.0",
            "name": "fess-ds-slack",
            "version": "15.7.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.7.0/fess-ds-slack-15.7.0.jar"
          }
        ]
      }
    }

Plugin installieren
===================

Installiert das Plugin mit dem angegebenen Namen und der angegebenen Version.

Request
-------

::

    POST /api/admin/plugin
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Plugin-Name (maximal 100 Zeichen)
   * - ``version``
     - Ja
     - Plugin-Version (maximal 100 Zeichen)

.. note::

   ``name`` und ``version`` müssen mit einem der installierbaren Plugins übereinstimmen, die über
   ``/available`` abgerufen werden können. Wenn kein passendes Artefakt vorhanden ist,
   wird ein Fehler zurückgegeben.

Response
--------

Wenn die Anfrage akzeptiert wird, wird eine Antwort mit ``status`` ``0`` (OK) zurückgegeben.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Wenn kein Artefakt zu ``name`` oder ``version`` gefunden wird, wird ``status`` auf
``1`` (BAD_REQUEST) gesetzt und ``message`` enthält ``invalid name or version``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   Die Installation wird asynchron im Hintergrund ausgeführt. Die Antwort mit ``status: 0``
   zeigt lediglich an, dass die Anfrage akzeptiert wurde, und garantiert nicht den Abschluss
   der Installation. Nach dem Abschluss der Installation werden Plugins mit demselben Namen,
   aber einer anderen Version, die bereits installiert sind, automatisch entfernt. Wenn der
   Download oder die Installation fehlschlägt, wird dies im Serverprotokoll aufgezeichnet,
   aber nicht in der API-Antwort widergespiegelt.

Plugin löschen
==============

Löscht das Plugin mit dem angegebenen Namen und der angegebenen Version.

Request
-------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

Feldbeschreibungen
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``name``
     - Ja
     - Plugin-Name (maximal 100 Zeichen)
   * - ``version``
     - Nein
     - Plugin-Version (maximal 100 Zeichen). Es wird empfohlen, diese Angabe zu machen, um das zu löschende Plugin eindeutig zu identifizieren.

Response
--------

Wenn die Anfrage akzeptiert wird, wird eine Antwort mit ``status`` ``0`` (OK) zurückgegeben.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

.. note::

   Die Löschung wird asynchron im Hintergrund ausgeführt. Die Antwort mit ``status: 0``
   zeigt lediglich an, dass die Anfrage akzeptiert wurde, und prüft weder, ob das entsprechende
   Plugin vorhanden ist, noch ob die Löschung erfolgreich war. Wenn die Löschung fehlschlägt
   (z. B. wenn die Zieldatei nicht vorhanden ist), wird dies im Serverprotokoll aufgezeichnet,
   aber nicht in der API-Antwort widergespiegelt.

Verwendungsbeispiele
====================

Installierte Plugins auflisten
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

Plugin installieren
-------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Plugin löschen
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
