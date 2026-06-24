==========================
General API
==========================

Übersicht
=========

Die General API dient zur Verwaltung der allgemeinen Einstellungen in |Fess|.
Sie können systemweite Konfigurationen abrufen und aktualisieren.

Basis-URL
=========

::

    /api/admin/general

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

Response
--------

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
          "logLevel": "",
          "ssoType": "none",
          "storageType": "",
          "notificationLogin": "",
          "notificationSearchTop": ""
        }
      }
    }

.. note::

   Das obige Beispiel zeigt nur repräsentative Felder. Das ``setting``-Objekt in der
   tatsächlichen Antwort enthält alle Felder der allgemeinen Einstellungen (Crawling,
   Suche, Benachrichtigungen, LDAP, SSO, Speicher usw.). Die vollständige Feldliste
   ist in ``EditForm.java`` zu finden.

.. note::

   Aus Sicherheitsgründen werden Felder mit Anmeldeinformationen nicht mit ihren
   tatsächlichen Werten in der Antwort zurückgegeben.

   - Das LDAP-Administratorpasswort ``ldapAdminSecurityCredentials`` wird stets durch
     ``null`` ersetzt.
   - Andere Secrets (``storageAccessKey`` / ``storageSecretKey`` /
     ``oicClientId`` / ``oicClientSecret`` / ``spnegoPreauthPassword`` /
     ``entraidClientId`` / ``entraidClientSecret``) werden bei gesetztem Wert als
     Maskierungswert ``"**********"`` zurückgegeben.

Allgemeine Einstellungen aktualisieren
======================================

Request
-------

::

    PUT /api/admin/general
    Content-Type: application/json

Request-Body
~~~~~~~~~~~~

Die Aktualisierung wird als partielle Zusammenführung (merge) verarbeitet. Die
Anfragewerte werden mit den aktuellen Einstellungen zusammengeführt; Felder, die
nicht in der Anfrage enthalten sind (``null``-Felder), werden ignoriert und behalten
ihren bestehenden Wert.

.. warning::

   Die folgenden vier Felder haben eine ``@Required``-Einschränkung und MÜSSEN in
   **jedem** PUT-Request enthalten sein. Werden sie weggelassen, tritt ein
   Validierungsfehler (HTTP 400) auf.

   - ``dayForCleanup``
   - ``crawlingThreadCount``
   - ``failureCountThreshold``
   - ``csvFileEncoding``

   Diese Felder können auch bei einer partiellen Aktualisierung nicht weggelassen
   werden. Da der gesendete Wert die bestehende Einstellung überschreibt, sollte für
   Felder, die nicht geändert werden sollen, zunächst der aktuelle Wert per ``GET``
   abgerufen und unverändert übermittelt werden. Alle anderen Felder sind optional;
   weggelassene Felder behalten ihren bestehenden Wert.

.. note::

   Numerische Felder unterliegen einer Typ- und Bereichsvalidierung. Das Senden eines
   Werts, der nicht als Ganzzahl interpretiert werden kann, oder eines Werts außerhalb
   des zulässigen Bereichs führt zu einem Validierungsfehler (HTTP 400).

   - ``dayForCleanup``: ``-1`` bis ``1000``
   - ``crawlingThreadCount``: ``0`` bis ``100``
   - ``failureCountThreshold``: ``-1`` bis ``10000``
   - ``purgeSearchLogDay`` / ``purgeJobLogDay`` / ``purgeUserInfoDay``:
     ``-1`` bis ``100000``
   - ``purgeSuggestSearchLogDay``: ``0`` bis ``100000``

.. note::

   Bei Ein-/Aus-Feldern (``available``-Typ) bedeutet ausschließlich ``"true"`` oder
   ``"on"`` (jeweils unabhängig von Groß-/Kleinschreibung) eine Aktivierung. Jeder
   andere Wert (z. B. ``"false"`` oder eine leere Zeichenkette) wird als deaktiviert
   (``false``) behandelt. Der bestehende Wert bleibt nur dann erhalten, wenn das Feld
   weggelassen (nicht gesendet) wird. Im GET-Response werden diese Felder als
   Zeichenketten ``"true"`` / ``"false"`` zurückgegeben.

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

Es gibt zahlreiche Konfigurationselemente. Im Folgenden sind die wichtigsten Felder
aufgeführt (alle Felder siehe ``EditForm.java``; der Typ des API-Request-/Response-Body
ist ``EditBody``, der ``EditForm`` erweitert, jedoch liegen die Felddefinitionen in
``EditForm``). Die Ein-/Aus-Einstellungen vom Typ ``available`` werden als
Zeichenketten ``"true"`` / ``"false"`` dargestellt.

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
     - Anzahl der Tage, die gecrawlte Dokumente aufbewahrt werden (-1=Cleanup deaktiviert)
   * - ``crawlingThreadCount``
     - Ja
     - Anzahl der für das Crawling verwendeten Threads
   * - ``failureCountThreshold``
     - Ja
     - Schwellenwert der Fehleranzahl, ab der das Crawling einer URL gestoppt wird (-1=deaktiviert)
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
   * - ``appValue``
     - Nein
     - Anwendungsspezifischer zusätzlicher Konfigurationswert
   * - ``virtualHostValue``
     - Nein
     - Virtuelle-Host-Konfiguration (für Mehrmandanten-Setups)
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
     - Anfügen von Query-Parametern an die Suchergebnis-URL
   * - ``loginRequired``
     - Nein
     - Ob für die Suche eine Anmeldung erforderlich ist
   * - ``loginLink``
     - Nein
     - Anzeige des Anmeldelinks auf der Suchseite aktivieren/deaktivieren
   * - ``thumbnail``
     - Nein
     - Generierung von Vorschaubildern aktivieren/deaktivieren
   * - ``resultCollapsed``
     - Nein
     - Einklappen ähnlicher Dokumente in den Suchergebnissen aktivieren/deaktivieren
   * - ``ignoreFailureType``
     - Nein
     - Zu ignorierende Crawl-Fehlertypen
   * - ``crawlingUserAgent``
     - Nein
     - User-Agent-Zeichenkette, die beim Crawling gesendet wird
   * - ``purgeSearchLogDay``
     - Nein
     - Anzahl der Tage, die das Suchprotokoll aufbewahrt wird (-1=deaktiviert)
   * - ``purgeJobLogDay``
     - Nein
     - Anzahl der Tage, die das Job-Protokoll aufbewahrt wird (-1=deaktiviert)
   * - ``purgeUserInfoDay``
     - Nein
     - Anzahl der Tage, die Benutzerinformationen aufbewahrt werden (-1=deaktiviert)
   * - ``purgeSuggestSearchLogDay``
     - Nein
     - Anzahl der Tage, die das Suggest-Suchprotokoll aufbewahrt wird (0=deaktiviert)
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
   * - ``searchUseBrowserLocale``
     - Nein
     - Ob der Browser-Locale bei der Suche verwendet werden soll
   * - ``ragLlmName``
     - Nein
     - Name des LLM-Providers für RAG
   * - ``llmLogLevel``
     - Nein
     - Log-Level für LLM-bezogene Pakete

Authentifizierungsbezogene Felder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Auch die Einstellungen zu LDAP und SSO (OpenID Connect, SAML, SPNEGO, Entra ID) werden
über diese API verwaltet. Im Folgenden sind die wichtigsten Felder aufgeführt
(alle Felder siehe ``EditForm.java``).

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
   * - ``ldapMemberofAttribute``
     - LDAP-Attributname, der die Gruppenzugehörigkeit angibt
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

Auch die Einstellungen für die Cloud-Speicher-Anbindung (S3 / GCS) können verwaltet werden.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Feld
     - Beschreibung
   * - ``storageType``
     - Speichertyp (``s3`` / ``gcs`` / ``auto``)
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

.. note::

   Secret-Felder wie ``ldapAdminSecurityCredentials``, ``storageAccessKey`` /
   ``storageSecretKey``, ``oicClientId`` / ``oicClientSecret``,
   ``entraidClientId`` / ``entraidClientSecret`` sowie ``spnegoPreauthPassword``
   behalten ihren gespeicherten Wert (werden nicht aktualisiert), wenn der Maskierungswert
   ``"**********"`` unverändert gesendet wird. Senden Sie den tatsächlichen Wert nur dann,
   wenn Sie ihn ändern möchten.

   Da diese Prüfung darauf basiert, ob die Zeichenkette nach dem Entfernen aller
   Sternzeichen leer ist, führt auch das Senden einer leeren Zeichenkette (``""``) oder
   eines ausschließlich aus Sternzeichen bestehenden Werts dazu, dass der Wert unverändert
   bleibt. Daher können diese Secret-Felder über die API nicht auf einen leeren Wert
   zurückgesetzt werden.

Response
--------

Bei erfolgreicher Aktualisierung wird nur ``status`` zurückgegeben (``id`` oder ``created`` sind nicht enthalten).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

Verwendungsbeispiele
====================

.. note::

   Da die vier Felder ``dayForCleanup``, ``crawlingThreadCount``,
   ``failureCountThreshold`` und ``csvFileEncoding`` in PUT-Requests erforderlich sind,
   enthalten alle folgenden Beispiele diese Felder. Da die gesendeten Werte die
   bestehenden Einstellungen überschreiben, sollten in der realen Nutzung die per
   ``GET`` abgerufenen aktuellen Werte angegeben werden (die folgenden Beispiele
   verwenden Standardwerte).

Crawl-Einstellungen aktualisieren
---------------------------------

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
-----------------------------------

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
