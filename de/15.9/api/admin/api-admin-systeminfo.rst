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
        "version": "15.9",
        "status": 0,
        "env_props": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "system_props": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fess_props": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bug_report_props": [
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
     - Produktversion von |Fess| (Beispiel: ``15.9``).
   * - ``status``
     - Ergebniscode der Verarbeitung. ``0`` steht für erfolgreiche Ausführung.
   * - ``env_props``
     - Liste der Umgebungsvariablen (Array aus ``label`` / ``value``). Zurückgegeben werden die über ``System.getenv()`` ermittelten Werte; vertrauliche Einträge werden maskiert (siehe den Hinweis unten).
   * - ``system_props``
     - Liste der Java-Systemeigenschaften (Array aus ``label`` / ``value``). Zurückgegeben werden die über ``System.getProperties()`` ermittelten Werte; vertrauliche Einträge werden maskiert (siehe den Hinweis unten).
   * - ``fess_props``
     - Liste der |Fess|-Konfigurationseigenschaften (Array aus ``label`` / ``value``). Enthält die Einstellungen aus ``fess_config.properties`` sowie die über die Administrationsoberfläche gesetzten Systemeigenschaften. Vertrauliche Einträge werden maskiert (siehe Hinweis unten).
   * - ``bug_report_props``
     - Liste der für Fehlerberichte gesammelten Informationen (Array aus ``label`` / ``value``). Enthält wichtige Systemeigenschaften zu Betriebssystem und Java-Laufzeitumgebung (``os.name``, ``os.version``, ``java.vm.version`` u. a.) sowie die |Fess|-Systemeigenschaftswerte.

.. note::

   In ``fess_props``, ``env_props`` und ``system_props`` werden die Werte der folgenden vertraulichen Einträge maskiert und als ``XXXXXXXX`` zurückgegeben:
   ``http.proxy.password``, ``search_engine.password``, ``index.user.initial_password``,
   ``ldap.admin.security.credentials``, ``spnego.preauth.password``, ``app.cipher.key``,
   ``content_chunker.embedding.opensearch.password``,
   sowie jeder Eintrag, dessen Schlüssel auf ``.client.id``, ``.client.secret``, ``.privatekey`` oder ``.key.password`` endet
   oder zu ``content_chunker.embedding.*.api.key`` bzw. ``rag.llm.*.api.key`` passt.
   Eine Systemeigenschaft mit dem Namen ``fess.system.<Schlüssel>`` oder ``fess.config.<Schlüssel>`` (die Form, in der eine Einstellung als ``-D``-Option übergeben wird)
   wird nach derselben Regel maskiert wie ``<Schlüssel>``.
   In ``env_props`` und ``system_props`` wird außerdem der Wert einer solchen vertraulichen ``-DSchlüssel=Wert``-Option innerhalb einer längeren Zeichenfolge
   (z. B. ``FESS_JAVA_OPTS`` oder ``JAVA_TOOL_OPTIONS``) maskiert; der Rest der Zeichenfolge bleibt lesbar.

.. warning::

   Maskiert werden nur die oben genannten Schlüssel. Wenn Sie ein Geheimnis unter einem anderen Namen
   (z. B. ``DB_PASSWORD``) in einer Umgebungsvariablen oder einer Java-Systemeigenschaft ablegen, wird es NICHT maskiert:
   Der Wert wird unverändert zurückgegeben und erscheint im Response.

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
         | jq -r '.response.system_props[] | select(.label == "java.version") | .value'

Umgebungsvariablen auflisten
----------------------------

.. code-block:: bash

    # Umgebungsvariablen im Format label=value anzeigen
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.env_props[] | "\(.label)=\(.value)"'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-stats` - Statistik API
- :doc:`api-admin-general` - Allgemeine Einstellungen API
- :doc:`../../admin/systeminfo-guide` - Systeminformationen Anleitung
