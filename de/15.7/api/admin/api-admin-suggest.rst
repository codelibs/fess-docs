==========================
Suggest API
==========================

Übersicht
=========

Die Suggest API dient zur Verwaltung der Suggest-Funktion (Suchvorschläge) in |Fess|.
Sie können statistische Informationen zu Suggest-Wörtern abrufen und Suggest-Wörter löschen.

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
          "queryWordsNum": 300
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
     - Gesamtzahl der Suggest-Wörter
   * - ``setting.documentWordsNum``
     - Anzahl der aus Dokumenten abgeleiteten Suggest-Wörter
   * - ``setting.queryWordsNum``
     - Anzahl der aus Suchanfragen abgeleiteten Suggest-Wörter

Alle Suggest-Wörter löschen
===========================

Löscht alle Suggest-Wörter.

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
=================================================

Löscht die aus Dokumenten generierten Suggest-Wörter.

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
===================================================

Löscht die aus Suchanfragen generierten Suggest-Wörter.

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

Verwendungsbeispiele
====================

Statistische Informationen abrufen
----------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

Alle Suggest-Wörter löschen
---------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

Aus Dokumenten abgeleitete Suggest-Wörter löschen
-------------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-badword` - Bad Word API
- :doc:`api-admin-elevateword` - Elevate Word API
- :doc:`../../admin/suggest-guide` - Suggest Verwaltungsanleitung
