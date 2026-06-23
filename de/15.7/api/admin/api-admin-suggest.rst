==========================
Suggest API
==========================

Übersicht
=========

Die Suggest API dient zur Verwaltung der Suggest-Wörter (Suchvorschläge), die von der Suggest-Funktion in |Fess| verwendet werden.
Sie können statistische Informationen zur Anzahl der Suggest-Wörter abrufen und Suggest-Wörter löschen.

Suggest-Wörter werden entweder aus gecrawlten Dokumenten generiert (Dokument-Herkunft) oder aus den Suchanfragen der Benutzer (Suchanfrage-Herkunft). Über diese API können Sie Suggest-Wörter nach Herkunftstyp oder alle zusammen löschen.

Authentifizierung
=================

Für den Zugriff auf diese API ist eine Authentifizierung mittels Zugriffstoken erforderlich. Geben Sie das Zugriffstoken im Request-Header an.

::

    Authorization: Bearer <Zugriffstoken>

Das Zugriffstoken muss die Berechtigung für die Admin API (standardmäßig ``Radmin-api``) besitzen.
Informationen zur Beschaffung von Zugriffstokens und zu den Berechtigungen finden Sie unter :doc:`api-admin-overview`.

Basis-URL
=========

::

    /api/admin/suggest

Endpunktliste
=============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Pfad
     - Beschreibung
   * - GET
     - /
     - Statistische Informationen zu Suggest-Wörtern abrufen
   * - DELETE
     - /all
     - Alle Suggest-Wörter löschen
   * - DELETE
     - /document
     - Aus Dokumenten abgeleitete Suggest-Wörter löschen
   * - DELETE
     - /query
     - Aus Suchanfragen abgeleitete Suggest-Wörter löschen

Statistische Informationen zu Suggest-Wörtern abrufen
=====================================================

Ruft statistische Informationen zur Anzahl der Suggest-Wörter ab.

Request
-------

::

    GET /api/admin/suggest

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
        }
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``setting.totalWordsNum``
     - Gesamtzahl der Suggest-Wörter (Anzahl der im Suggest-Index registrierten Suggest-Wörter)
   * - ``setting.documentWordsNum``
     - Anzahl der aus Dokumenten abgeleiteten Suggest-Wörter (Suggest-Wörter mit einer Dokumenthäufigkeit von 1 oder mehr)
   * - ``setting.queryWordsNum``
     - Anzahl der aus Suchanfragen abgeleiteten Suggest-Wörter (Suggest-Wörter mit einer Anfragehäufigkeit von 1 oder mehr)

.. note::

   ``documentWordsNum`` und ``queryWordsNum`` schließen sich nicht gegenseitig aus. Wenn ein Suggest-Wort sowohl aus Dokumenten als auch aus Suchanfragen stammt, wird es in beiden Zählungen berücksichtigt. Daher kann die Summe von ``documentWordsNum`` und ``queryWordsNum`` von ``totalWordsNum`` abweichen.

Alle Suggest-Wörter löschen
============================

Löscht alle Suggest-Wörter. Es werden alle Suggest-Wörter im Suggest-Index gelöscht, unabhängig davon, ob sie aus Dokumenten oder Suchanfragen stammen.

Request
-------

::

    DELETE /api/admin/suggest/all

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Aus Dokumenten abgeleitete Suggest-Wörter löschen
==================================================

Löscht die aus Dokumenten generierten Suggest-Wörter (Suggest-Wörter mit Dokument-Herkunft).

Request
-------

::

    DELETE /api/admin/suggest/document

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Aus Suchanfragen abgeleitete Suggest-Wörter löschen
====================================================

Löscht die aus Suchanfragen generierten Suggest-Wörter (Suggest-Wörter mit Suchanfrage-Herkunft).

Request
-------

::

    DELETE /api/admin/suggest/query

Response
--------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Fehlerantwort
=============

Wenn die Löschoperation fehlschlägt, wird der HTTP-Status ``400`` zurückgegeben, ``status`` im Response-Body wird auf ``1`` (BAD_REQUEST) gesetzt und ``message`` enthält eine Fehlermeldung.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

Wenn das Zugriffstoken fehlt, ungültig ist oder keine ausreichenden Berechtigungen vorliegen, wird ``status`` im Response-Body auf ``3`` (UNAUTHORIZED) gesetzt. Eine Liste der ``status``-Werte und HTTP-Statuscodes finden Sie unter :doc:`api-admin-overview`.

Verwendungsbeispiele
====================

Statistische Informationen abrufen
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alle Suggest-Wörter löschen
----------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Aus Dokumenten abgeleitete Suggest-Wörter löschen
--------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

Aus Suchanfragen abgeleitete Suggest-Wörter löschen
----------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-badword` - Bad Word API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/suggest-guide` - Suggest Verwaltungsanleitung
