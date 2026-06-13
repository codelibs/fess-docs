==========================
SystemInfo API
==========================

Übersicht
=========

Die SystemInfo API dient zum Abrufen von Systeminformationen in |Fess|.
Sie können Umgebungsvariablen, Java-Systemeigenschaften, |Fess|-Konfigurationseigenschaften und Informationen für Fehlerberichte einsehen.

Basis-URL
=========

::

    /api/admin/systeminfo

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
     - Systeminformationen abrufen

Systeminformationen abrufen
===========================

Request
-------

::

    GET /api/admin/systeminfo

Response
--------

Die Antwort enthält ``version`` (die Produktversion), ``status`` (das Verarbeitungsergebnis) sowie
die folgenden vier Eigenschaftsgruppen. Jede Eigenschaftsgruppe ist ein Array von Objekten
mit ``key`` und ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

Response-Felder
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``envProps``
     - Liste der Umgebungsvariablen (Array aus ``key`` / ``value``)
   * - ``systemProps``
     - Liste der Java-Systemeigenschaften (Array aus ``key`` / ``value``)
   * - ``fessProps``
     - Liste der |Fess|-Konfigurationseigenschaften (Array aus ``key`` / ``value``)
   * - ``bugReportProps``
     - Liste der für Fehlerberichte gesammelten Informationen (Array aus ``key`` / ``value``)

Verwendungsbeispiele
====================

Systeminformationen abrufen
---------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

Eine bestimmte Systemeigenschaft extrahieren
--------------------------------------------

.. code-block:: bash

    # Nur den Wert von java.version extrahieren
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

Umgebungsvariablen auflisten
----------------------------

.. code-block:: bash

    # Umgebungsvariablen im Format key=value anzeigen
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-stats` - Statistik API
- :doc:`api-admin-general` - Allgemeine Einstellungen API
- :doc:`../../admin/systeminfo-guide` - Systeminformationen Anleitung
