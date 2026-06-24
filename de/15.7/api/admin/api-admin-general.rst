==========================
General API
==========================

Übersicht
=========

Die General API dient zur Verwaltung der allgemeinen Einstellungen (systemweite
Konfiguration) von |Fess|. Sie können Einstellungen für Crawling, Protokollierung,
Anzeige von Suchergebnissen, Suggest, Protokoll-Aufbewahrungszeiträume,
Benachrichtigungen, Authentifizierung (LDAP / SSO) und Cloud-Speicher-Anbindung
abrufen und aktualisieren. Diese Einstellungen entsprechen den
„Allgemein"-Einstellungen in der Admin-Oberfläche
(:doc:`../../admin/general-guide`).

Basis-URL
=========

::

    /api/admin/general

Für den Zugriff auf diese API ist ein Zugriffstoken mit der Berechtigung ``Radmin-api``
erforderlich. Weitere Informationen zur Authentifizierung finden Sie unter
:doc:`api-admin-overview`.

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
     - Allgemeine Einstellungen abrufen
   * - PUT
     - /
     - Allgemeine Einstellungen aktualisieren

Allgemeine Einstellungen abrufen
================================

Request
-------

::

    GET /api/admin/general

Dieser Endpunkt akzeptiert keine Abfrageparameter.

Response
--------

``response.setting`` enthält die aktuellen allgemeinen Einstellungen. Die Antwort
enthält alle aktualisierbaren Einstellungsfelder; das nachstehende Beispiel zeigt nur
repräsentative Felder. Ein-/Aus-Einstellungen werden als Zeichenketten ``"true"`` /
``"false"`` ausgedrückt, während Werte wie Aufbewahrungstage und Thread-Anzahl als
Zahlen ausgedrückt werden.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "incrementalCrawling": "true",
          "dayForCleanup": -1,
          "crawlingThreadCount": 5,
          "searchLog": "true",
          "userInfo": "true",
          "userFavorite": "false",
          "webApiJson": "true",
          "defaultLabelValue": "",
          "defaultSortValue": "",
          "appendQueryParameter": "false",
          "loginRequired": "false",
          "thumbnail": "true",
          "failureCountThreshold": -1,
          "popularWord": "true",
          "csvFileEncoding": "UTF-8",
          "purgeSearchLogDay": 30,
          "purgeJobLogDay": 30,
          "purgeUserInfoDay": 30,
          "purgeSuggestSearchLogDay": 30,
          "notificationTo": "",
          "suggestSearchLog": "true",
          "suggestDocuments": "true",
          "ldapProviderUrl": "ldap://localhost:389/",
          "ldapBaseDn": "dc=example,dc=com",
          "ldapAdminSecurityPrincipal": "cn=admin,dc=example,dc=com",
          "ldapAdminSecurityCredentials": null,
          "storageAccessKey": "**********",
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   Aus Sicherheitsgründen werden Passwörter und geheime Werte nicht unverändert
   zurückgegeben. Das LDAP-Administratorpasswort ``ldapAdminSecurityCredentials``
   wird stets als ``null`` zurückgegeben. Andere geheime Felder
   (``storageAccessKey``, ``storageSecretKey``, ``oicClientId``,
   ``oicClientSecret``, ``spnegoPreauthPassword``, ``entraidClientId``,
   ``entraidClientSecret``) werden als maskierter Wert ``"**********"``
   zurückgegeben, wenn sie gesetzt sind, bzw. als leere Zeichenkette, wenn sie
   nicht gesetzt sind.

Allgemeine Einstellungen aktualisieren
======================================

Request
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

Aktualisierungen werden als partielle Aktualisierung (merge) verarbeitet. Der
Server lädt die aktuellen Einstellungen und überschreibt dann nur die
Nicht-``null``-Felder, die in der Anfrage enthalten sind. Felder, die nicht in
der Anfrage enthalten sind, sowie Felder, die auf ``null`` gesetzt sind, behalten
ihre vorhandenen Werte.

.. important::

   Der Request-Body wird vor der Anwendung der Überschreibung validiert. Daher
   müssen die Pflichtfelder (``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold``, ``csvFileEncoding``) **immer in der Anfrage
   enthalten sein**, unabhängig davon, was geändert wird. Fehlt eines dieser
   Felder, schlägt die Validierung fehl und ``status: 1`` wird zurückgegeben.
   Um nur einige Felder zu ändern, rufen Sie zunächst die aktuellen Einstellungen
   mit ``GET`` ab und senden Sie dann den ``PUT``-Request mit den aktuellen
   Werten der Pflichtfelder.

.. note::

   Passwort- und Geheimfelder (``ldapAdminSecurityCredentials``,
   ``storageAccessKey``, ``storageSecretKey``, ``oicClientId``,
   ``oicClientSecret``, ``spnegoPreauthPassword``, ``entraidClientId``,
   ``entraidClientSecret``) werden ignoriert, wenn eine leere Zeichenkette oder
   der maskierte Wert (``**********``) gesendet wird, und der vorhandene Wert
   wird beibehalten. Diese Felder werden nur aktualisiert, wenn ein tatsächlicher
   Wert gesendet wird.

.. code-block:: json

    {
      "incrementalCrawling": "true",
      "dayForCleanup": -1,
      "crawlingThreadCount": 10,
      "failureCountThreshold": 100,
      "csvFileEncoding": "UTF-8",
      "popularWord": "true"
    }

Wichtigste Felder
~~~~~~~~~~~~~~~~~

Es gibt zahlreiche Konfigurationselemente. Im Folgenden sind die wichtigsten
Felder aufgeführt (alle Felder entsprechen den „Allgemein"-Einstellungen in der
Admin-Oberfläche). Ein-/Aus-Einstellungen werden als Zeichenketten ``"true"`` /
``"false"`` angegeben.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Feld
     - Erforderlich
     - Beschreibung
   * - ``incrementalCrawling``
     - Nein
     - Inkrementelles Crawling aktivieren/deaktivieren
   * - ``dayForCleanup``
     - Ja
     - Anzahl der Tage, die gecrawlte Dokumente aufbewahrt werden (-1 = Cleanup deaktiviert; Bereich: -1 bis 1000)
   * - ``crawlingThreadCount``
     - Ja
     - Anzahl der für das Crawling verwendeten Threads (Bereich: 0 bis 100)
   * - ``failureCountThreshold``
     - Ja
     - Schwellenwert der Fehleranzahl, ab der das Crawling einer URL gestoppt wird (-1 = deaktiviert; Bereich: -1 bis 10000)
   * - ``csvFileEncoding``
     - Ja
     - Kodierung des CSV-Exports
   * - ``searchLog``
     - Nein
     - Suchanfragen-Protokoll aktivieren/deaktivieren
   * - ``userInfo``
     - Nein
     - Aufzeichnung von Benutzerinformationen aktivieren/deaktivieren
   * - ``userFavorite``
     - Nein
     - Favoriten-Funktion aktivieren/deaktivieren
   * - ``webApiJson``
     - Nein
     - JSON-Web-API aktivieren/deaktivieren
   * - ``popularWord``
     - Nein
     - Aggregation/Anzeige beliebter Wörter aktivieren/deaktivieren
   * - ``defaultLabelValue``
     - Nein
     - Standard-Labelwert
   * - ``defaultSortValue``
     - Nein
     - Standard-Sortierreihenfolge
   * - ``appendQueryParameter``
     - Nein
     - Anfügen von Abfrageparametern an die Suchergebnis-URL
   * - ``loginRequired``
     - Nein
     - Ob für die Suche eine Anmeldung erforderlich ist
   * - ``thumbnail``
     - Nein
     - Generierung von Vorschaubildern aktivieren/deaktivieren
   * - ``ignoreFailureType``
     - Nein
     - Zu ignorierende Crawl-Fehlertypen
   * - ``purgeSearchLogDay``
     - Nein
     - Anzahl der Tage, die das Suchprotokoll aufbewahrt wird (-1 = deaktiviert; Bereich: -1 bis 100000)
   * - ``purgeJobLogDay``
     - Nein
     - Anzahl der Tage, die das Job-Protokoll aufbewahrt wird (-1 = deaktiviert; Bereich: -1 bis 100000)
   * - ``purgeUserInfoDay``
     - Nein
     - Anzahl der Tage, die Benutzerinformationen aufbewahrt werden (-1 = deaktiviert; Bereich: -1 bis 100000)
   * - ``purgeSuggestSearchLogDay``
     - Nein
     - Anzahl der Tage, die das Suggest-Suchprotokoll aufbewahrt wird (0 = deaktiviert; Bereich: 0 bis 100000)
   * - ``purgeByBots``
     - Nein
     - Bot-User-Agents, deren Suchprotokolle verworfen werden
   * - ``notificationTo``
     - Nein
     - Empfänger-E-Mail-Adresse für Systembenachrichtigungen
   * - ``notificationLogin``
     - Nein
     - Benachrichtigungstext, der auf der Anmeldeseite angezeigt wird
   * - ``notificationSearchTop``
     - Nein
     - Benachrichtigungstext, der auf der Suchstartseite angezeigt wird
   * - ``notificationAdvanceSearch``
     - Nein
     - Benachrichtigungstext, der auf der erweiterten Suchseite angezeigt wird
   * - ``suggestSearchLog``
     - Nein
     - Suggest aus dem Suchprotokoll aktivieren/deaktivieren
   * - ``suggestDocuments``
     - Nein
     - Suggest aus Dokumenten aktivieren/deaktivieren
   * - ``logLevel``
     - Nein
     - Log-Level des Systemprotokolls
   * - ``logNotificationEnabled``
     - Nein
     - Benachrichtigung über ERROR/WARN-Protokolle aktivieren/deaktivieren
   * - ``logNotificationLevel``
     - Nein
     - Log-Benachrichtigungsstufe
   * - ``slackWebhookUrls``
     - Nein
     - Slack-Webhook-URL für Benachrichtigungen
   * - ``googleChatWebhookUrls``
     - Nein
     - Google-Chat-Webhook-URL für Benachrichtigungen

Authentifizierungsbezogene Felder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Auch die Einstellungen zu LDAP und SSO (OpenID Connect, SAML, SPNEGO, Entra ID)
werden über diese API verwaltet. Im Folgenden sind die wichtigsten Felder
aufgeführt (alle Felder entsprechen den „Allgemein"-Einstellungen in der
Admin-Oberfläche).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Feld
     - Beschreibung
   * - ``ldapProviderUrl``
     - LDAP-Verbindungs-URL
   * - ``ldapBaseDn``
     - LDAP-Basis-DN
   * - ``ldapSecurityPrincipal``
     - Security Principal für die LDAP-Bindung
   * - ``ldapAdminSecurityPrincipal``
     - Security Principal für LDAP-Verwaltungsoperationen
   * - ``ldapAdminSecurityCredentials``
     - LDAP-Administratorpasswort (in der Antwort durch ``null`` ersetzt)
   * - ``ldapAccountFilter`` / ``ldapGroupFilter``
     - Suchfilter für Benutzer/Gruppen
   * - ``ssoType``
     - SSO-Typ (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oicClientId`` / ``oicClientSecret`` / ``oicAuthServerUrl`` usw.
     - OpenID-Connect-Einstellungen
   * - ``samlIdpEntityid`` / ``samlSpEntityid`` usw.
     - SAML-Einstellungen
   * - ``spnegoKrb5Conf`` / ``spnegoLoginConf`` usw.
     - SPNEGO-Einstellungen
   * - ``entraidClientId`` / ``entraidTenant`` usw.
     - Microsoft-Entra-ID-Einstellungen

Speicherbezogene Felder
~~~~~~~~~~~~~~~~~~~~~~~~

Auch die Einstellungen für die Cloud-Speicher-Anbindung (S3 / GCS) können
verwaltet werden.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Feld
     - Beschreibung
   * - ``storageType``
     - Speichertyp (``auto`` / ``s3`` / ``gcs``)
   * - ``storageEndpoint``
     - Endpunkt-URL des Speichers
   * - ``storageAccessKey`` / ``storageSecretKey``
     - Access Key / Secret Key für die Authentifizierung
   * - ``storageBucket``
     - Bucket-Name
   * - ``storageRegion``
     - S3-Region
   * - ``storageProjectId`` / ``storageCredentialsPath``
     - GCS-Projekt-ID / Pfad zur Anmeldeinformationsdatei

Response
--------

Bei erfolgreicher Aktualisierung werden nur ``version`` und ``status``
zurückgegeben (``id`` und ``created`` sind nicht enthalten).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Schlägt die Aktualisierung fehl (z. B. aufgrund eines Validierungsfehlers), wird
``status`` auf einen Wert ungleich null gesetzt (``1`` bei einem
Validierungsfehler), und ``message`` enthält die Fehlerdetails. Die Liste der
``status``-Werte finden Sie unter :doc:`api-admin-overview`.

Verwendungsbeispiele
====================

.. note::

   Die nachstehenden Beispiele enthalten die Pflichtfelder (``dayForCleanup``,
   ``crawlingThreadCount``, ``failureCountThreshold``, ``csvFileEncoding``). Da
   diese unabhängig von der jeweiligen Änderung stets angegeben werden müssen,
   verwenden Sie im realen Betrieb die über ``GET`` abgerufenen aktuellen Werte.

Crawl-Einstellungen aktualisieren
----------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incrementalCrawling": "true",
           "crawlingThreadCount": 10,
           "failureCountThreshold": 100,
           "dayForCleanup": -1,
           "csvFileEncoding": "UTF-8"
         }'

Protokoll-Aufbewahrungsdauer aktualisieren
------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "purgeSearchLogDay": 90,
           "purgeJobLogDay": 90,
           "purgeUserInfoDay": 90
         }'

Suggest-Einstellungen aktualisieren
------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "dayForCleanup": -1,
           "crawlingThreadCount": 5,
           "failureCountThreshold": -1,
           "csvFileEncoding": "UTF-8",
           "suggestSearchLog": "true",
           "suggestDocuments": "true"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-systeminfo` - Systeminformationen API
- :doc:`../../admin/general-guide` - Allgemeine Einstellungen Anleitung
