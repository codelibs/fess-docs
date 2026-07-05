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

Für den Zugriff auf diese API ist ein Zugriffstoken mit der Berechtigung ``Radmin-api`` erforderlich.
Einzelheiten zur Authentifizierung finden Sie unter :doc:`api-admin-overview`.

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

Dieser Endpunkt akzeptiert keine Query-Parameter.

Response
--------

Die Antwort enthält ``version`` (die Produktversion), ``status`` (das Verarbeitungsergebnis) sowie
die folgenden vier Eigenschaftsgruppen. Jede Eigenschaftsgruppe ist ein Array von Objekten
mit ``label`` und ``value``.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
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
   * - ``version``
     - Produktversion von |Fess| (Beispiel: ``15.8.0``).
   * - ``status``
     - Ergebniscode der Verarbeitung. ``0`` steht für erfolgreiche Ausführung.
   * - ``envProps``
     - Liste der Umgebungsvariablen (Array aus ``label`` / ``value``). Die Werte werden unverändert über ``System.getenv()`` zurückgegeben.
   * - ``systemProps``
     - Liste der Java-Systemeigenschaften (Array aus ``label`` / ``value``). Die Werte werden unverändert über ``System.getProperties()`` zurückgegeben.
   * - ``fessProps``
     - Liste der |Fess|-Konfigurationseigenschaften (Array aus ``label`` / ``value``). Enthält die Einstellungen aus ``fess_config.properties`` sowie die über die Administrationsoberfläche gesetzten Systemeigenschaften. Vertrauliche Einträge werden maskiert (siehe Hinweis unten).
   * - ``bugReportProps``
     - Liste der für Fehlerberichte gesammelten Informationen (Array aus ``label`` / ``value``). Enthält wichtige Systemeigenschaften zu Betriebssystem und Java-Laufzeitumgebung (``os.name``, ``os.version``, ``java.vm.version`` u. a.) sowie die |Fess|-Systemeigenschaftswerte.

.. note::

   In ``fessProps`` werden die folgenden vertraulichen Konfigurationswerte maskiert und als ``XXXXXXXX`` zurückgegeben:
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (Umgebungsvariablen) und ``systemProps`` (Java-Systemeigenschaften) werden nicht maskiert —
   die gesetzten Werte werden unverändert zurückgegeben. Wenn Umgebungsvariablen oder Systemeigenschaften
   Zugangsdaten oder andere vertrauliche Informationen enthalten, erscheinen diese im Response.

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
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

Umgebungsvariablen auflisten
----------------------------

.. code-block:: bash

    # Umgebungsvariablen im Format label=value anzeigen
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-stats` - Statistik API
- :doc:`api-admin-general` - Allgemeine Einstellungen API
- :doc:`../../admin/systeminfo-guide` - Systeminformationen Anleitung
