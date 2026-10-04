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
        "version": "15.9.0",
        "status": 0,
        "setting": {
          "incremental_crawling": "true",
          "day_for_cleanup": -1,
          "crawling_thread_count": 5,
          "search_log": "true",
          "user_info": "true",
          "user_favorite": "false",
          "web_api_json": "true",
          "default_label_value": "",
          "default_sort_value": "",
          "append_query_parameter": "false",
          "login_required": "false",
          "thumbnail": "true",
          "failure_count_threshold": -1,
          "popular_word": "true",
          "csv_file_encoding": "UTF-8",
          "purge_search_log_day": 30,
          "purge_job_log_day": 30,
          "purge_user_info_day": 30,
          "purge_suggest_search_log_day": 30,
          "notification_to": "",
          "suggest_search_log": "true",
          "suggest_documents": "true",
          "ldap_provider_url": "ldap://localhost:389/",
          "ldap_base_dn": "dc=example,dc=com",
          "ldap_admin_security_principal": "cn=admin,dc=example,dc=com",
          "log_level": "",
          "sso_type": "none",
          "storage_type": "",
          "notification_login": "",
          "notification_search_top": ""
        }
      }
    }

.. note::

   Das obige Beispiel zeigt nur repräsentative Felder. Das ``setting``-Objekt in der
   tatsächlichen Antwort enthält alle Felder der allgemeinen Einstellungen (Crawling,
   Suche, Benachrichtigungen, LDAP, SSO, Speicher usw.). Die vollständige Feldliste
   finden Sie auf der Admin-Seite „Allgemein".

.. note::

   Aus Sicherheitsgründen werden Felder mit Anmeldeinformationen nicht mit ihren
   tatsächlichen Werten in der Antwort zurückgegeben.

   - Das LDAP-Administratorpasswort ``ldap_admin_security_credentials`` ist nie in der
     Antwort enthalten.
   - Andere Secrets (``storage_access_key`` / ``storage_secret_key`` /
     ``oic_client_id`` / ``oic_client_secret`` / ``spnego_preauth_password`` /
     ``entraid_client_id`` / ``entraid_client_secret``) werden bei gesetztem Wert als
     Maskierungswert ``"**********"`` zurückgegeben, bzw. als leere Zeichenkette
     (``""``), wenn sie nicht gesetzt sind.

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

.. warning::

   Die folgenden vier Felder sind erforderlich und MÜSSEN in **jedem** PUT-Request
   enthalten sein, auch bei einer partiellen Aktualisierung:

   - ``day_for_cleanup``
   - ``crawling_thread_count``
   - ``failure_count_threshold``
   - ``csv_file_encoding``

   Fehlt eines dieser Felder, schlägt die Validierung fehl und die API gibt
   HTTP 400 mit ``status: 1`` und einer Fehlermeldung ``message`` zurück. Da der
   gesendete Wert die bestehende Einstellung überschreibt, sollte für Felder, die
   nicht geändert werden sollen, zunächst der aktuelle Wert per ``GET`` abgerufen
   und unverändert übermittelt werden. Alle anderen Felder sind optional;
   weggelassene Felder behalten ihren bestehenden Wert.

.. note::

   Numerische Felder unterliegen einer Typ- und Bereichsvalidierung. Das Senden eines
   Werts, der nicht als Ganzzahl interpretiert werden kann, oder eines Werts außerhalb
   des zulässigen Bereichs führt zu einem Validierungsfehler (HTTP 400 mit
   ``status: 1``). Der zulässige Bereich für jedes numerische Feld ist in der
   nachstehenden Feldtabelle aufgeführt.

.. note::

   Bei Ein-/Aus-Feldern (``available``-Typ) bedeutet ausschließlich ``"true"`` oder
   ``"on"`` (jeweils unabhängig von Groß-/Kleinschreibung) eine Aktivierung. Jeder
   andere Wert (z. B. ``"false"`` oder eine leere Zeichenkette) wird als deaktiviert
   (``false``) behandelt. Der bestehende Wert bleibt nur dann erhalten, wenn das Feld
   weggelassen (nicht gesendet) wird. Im GET-Response werden diese Felder als
   Zeichenketten ``"true"`` / ``"false"`` zurückgegeben.

.. code-block:: json

    {
      "incremental_crawling": "true",
      "day_for_cleanup": -1,
      "crawling_thread_count": 10,
      "failure_count_threshold": 100,
      "csv_file_encoding": "UTF-8",
      "popular_word": "true"
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
   * - ``incremental_crawling``
     - Nein
     - Inkrementelles Crawling aktivieren/deaktivieren
   * - ``day_for_cleanup``
     - Ja
     - Anzahl der Tage, die gecrawlte Dokumente aufbewahrt werden (-1 = Cleanup deaktiviert; Bereich: -1 bis 1000)
   * - ``crawling_thread_count``
     - Ja
     - Anzahl der für das Crawling verwendeten Threads (Bereich: 0 bis 100)
   * - ``failure_count_threshold``
     - Ja
     - Schwellenwert der Fehleranzahl, ab der das Crawling einer URL gestoppt wird (-1 = deaktiviert; Bereich: -1 bis 10000)
   * - ``csv_file_encoding``
     - Ja
     - Kodierung des CSV-Exports
   * - ``search_log``
     - Nein
     - Suchanfragen-Protokoll aktivieren/deaktivieren
   * - ``user_info``
     - Nein
     - Aufzeichnung von Benutzerinformationen aktivieren/deaktivieren
   * - ``user_favorite``
     - Nein
     - Favoriten-Funktion aktivieren/deaktivieren
   * - ``web_api_json``
     - Nein
     - JSON-Web-API aktivieren/deaktivieren
   * - ``app_value``
     - Nein
     - Anwendungsspezifischer zusätzlicher Konfigurationswert
   * - ``virtual_host_value``
     - Nein
     - Virtuelle-Host-Konfiguration (für Mehrmandanten-Setups)
   * - ``popular_word``
     - Nein
     - Aggregation/Anzeige beliebter Wörter aktivieren/deaktivieren
   * - ``default_label_value``
     - Nein
     - Standard-Labelwert
   * - ``default_sort_value``
     - Nein
     - Standard-Sortierreihenfolge
   * - ``append_query_parameter``
     - Nein
     - Anfügen von Abfrageparametern an die Suchergebnis-URL
   * - ``login_required``
     - Nein
     - Ob für die Suche eine Anmeldung erforderlich ist
   * - ``login_link``
     - Nein
     - Anzeige des Anmeldelinks auf der Suchseite aktivieren/deaktivieren
   * - ``thumbnail``
     - Nein
     - Generierung von Vorschaubildern aktivieren/deaktivieren
   * - ``result_collapsed``
     - Nein
     - Einklappen ähnlicher Dokumente in den Suchergebnissen aktivieren/deaktivieren
   * - ``ignore_failure_type``
     - Nein
     - Zu ignorierende Crawl-Fehlertypen
   * - ``crawling_user_agent``
     - Nein
     - User-Agent-Zeichenkette, die beim Crawling gesendet wird
   * - ``purge_search_log_day``
     - Nein
     - Anzahl der Tage, die das Suchprotokoll aufbewahrt wird (-1 = deaktiviert; Bereich: -1 bis 100000)
   * - ``purge_job_log_day``
     - Nein
     - Anzahl der Tage, die das Job-Protokoll aufbewahrt wird (-1 = deaktiviert; Bereich: -1 bis 100000)
   * - ``purge_user_info_day``
     - Nein
     - Anzahl der Tage, die Benutzerinformationen aufbewahrt werden (-1 = deaktiviert; Bereich: -1 bis 100000)
   * - ``purge_suggest_search_log_day``
     - Nein
     - Anzahl der Tage, die das Suggest-Suchprotokoll aufbewahrt wird (0 = deaktiviert; Bereich: 0 bis 100000)
   * - ``purge_by_bots``
     - Nein
     - Bot-User-Agents, deren Suchprotokolle verworfen werden
   * - ``notification_to``
     - Nein
     - Empfänger-E-Mail-Adresse für Systembenachrichtigungen
   * - ``notification_login``
     - Nein
     - Benachrichtigungstext, der auf der Anmeldeseite angezeigt wird
   * - ``notification_search_top``
     - Nein
     - Benachrichtigungstext, der auf der Suchstartseite angezeigt wird
   * - ``notification_advance_search``
     - Nein
     - Benachrichtigungstext, der auf der erweiterten Suchseite angezeigt wird
   * - ``suggest_search_log``
     - Nein
     - Suggest aus dem Suchprotokoll aktivieren/deaktivieren
   * - ``suggest_documents``
     - Nein
     - Suggest aus Dokumenten aktivieren/deaktivieren
   * - ``log_level``
     - Nein
     - Log-Level des Systemprotokolls
   * - ``log_notification_enabled``
     - Nein
     - Benachrichtigung über ERROR/WARN-Protokolle aktivieren/deaktivieren
   * - ``log_notification_level``
     - Nein
     - Log-Benachrichtigungsstufe
   * - ``slack_webhook_urls``
     - Nein
     - Slack-Webhook-URL für Benachrichtigungen
   * - ``google_chat_webhook_urls``
     - Nein
     - Google-Chat-Webhook-URL für Benachrichtigungen
   * - ``search_use_browser_locale``
     - Nein
     - Ob der Browser-Locale bei der Suche verwendet werden soll
   * - ``rag_llm_name``
     - Nein
     - Name des LLM-Providers für RAG
   * - ``llm_log_level``
     - Nein
     - Log-Level für LLM-bezogene Pakete

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
   * - ``ldap_provider_url``
     - LDAP-Verbindungs-URL
   * - ``ldap_base_dn``
     - LDAP-Basis-DN
   * - ``ldap_security_principal``
     - Security Principal für die LDAP-Bindung
   * - ``ldap_admin_security_principal``
     - Security Principal für LDAP-Verwaltungsoperationen
   * - ``ldap_admin_security_credentials``
     - LDAP-Administratorpasswort (nie in der Antwort enthalten)
   * - ``ldap_account_filter`` / ``ldap_group_filter``
     - Suchfilter für Benutzer/Gruppen
   * - ``ldap_memberof_attribute``
     - LDAP-Attributname, der die Gruppenzugehörigkeit angibt
   * - ``sso_type``
     - SSO-Typ (``none`` / ``oic`` / ``saml`` / ``spnego`` / ``entraid``)
   * - ``oic_client_id`` / ``oic_client_secret`` / ``oic_auth_server_url`` usw.
     - OpenID-Connect-Einstellungen
   * - ``saml_idp_entityid`` / ``saml_sp_entityid`` usw.
     - SAML-Einstellungen
   * - ``spnego_krb5_conf`` / ``spnego_login_conf`` usw.
     - SPNEGO-Einstellungen
   * - ``entraid_client_id`` / ``entraid_tenant`` usw.
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
   * - ``storage_type``
     - Speichertyp (``auto`` / ``s3`` / ``gcs``)
   * - ``storage_endpoint``
     - Endpunkt-URL des Speichers
   * - ``storage_access_key`` / ``storage_secret_key``
     - Access Key / Secret Key für die Authentifizierung
   * - ``storage_bucket``
     - Bucket-Name
   * - ``storage_region``
     - S3-Region
   * - ``storage_project_id`` / ``storage_credentials_path``
     - GCS-Projekt-ID / Pfad zur Anmeldeinformationsdatei

.. note::

   Secret-Felder wie ``ldap_admin_security_credentials``, ``storage_access_key`` /
   ``storage_secret_key``, ``oic_client_id`` / ``oic_client_secret``,
   ``entraid_client_id`` / ``entraid_client_secret`` sowie ``spnego_preauth_password``
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

Bei erfolgreicher Aktualisierung werden nur ``version`` und ``status``
zurückgegeben (``id`` und ``created`` sind nicht enthalten).

.. code-block:: json

    {
      "response": {
        "version": "15.9.0",
        "status": 0
      }
    }

Schlägt die Aktualisierung fehl (z. B. aufgrund eines Validierungsfehlers), gibt
die API HTTP 400 zurück, und ``status`` wird auf einen Wert ungleich null gesetzt
(``1`` bei einem Validierungsfehler), wobei ``message`` die Fehlerdetails enthält.
Die Liste der ``status``-Werte finden Sie unter :doc:`api-admin-overview`.

Verwendungsbeispiele
====================

.. note::

   Die nachstehenden Beispiele enthalten die Pflichtfelder (``day_for_cleanup``,
   ``crawling_thread_count``, ``failure_count_threshold``, ``csv_file_encoding``). Da
   diese unabhängig von der jeweiligen Änderung stets angegeben werden müssen,
   rufen Sie im realen Betrieb die aktuellen Werte über ``GET`` ab und geben Sie
   sie an (die folgenden Beispiele verwenden Standardwerte).

Crawl-Einstellungen aktualisieren
----------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "incremental_crawling": "true",
           "crawling_thread_count": 10,
           "failure_count_threshold": 100,
           "day_for_cleanup": -1,
           "csv_file_encoding": "UTF-8"
         }'

Protokoll-Aufbewahrungsdauer aktualisieren
------------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "purge_search_log_day": 90,
           "purge_job_log_day": 90,
           "purge_user_info_day": 90
         }'

Suggest-Einstellungen aktualisieren
------------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/general" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "day_for_cleanup": -1,
           "crawling_thread_count": 5,
           "failure_count_threshold": -1,
           "csv_file_encoding": "UTF-8",
           "suggest_search_log": "true",
           "suggest_documents": "true"
         }'

Referenzinformationen
=====================

- :doc:`api-admin-overview` - Admin API Übersicht
- :doc:`api-admin-systeminfo` - Systeminformationen API
- :doc:`../../admin/general-guide` - Allgemeine Einstellungen Anleitung
