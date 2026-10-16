==================================
Atlassian-Konnektor
==================================

Übersicht
=========

Der Atlassian-Konnektor bietet die Funktionalität, Daten von Atlassian-Produkten (Jira, Confluence) abzurufen und im |Fess|-Index zu registrieren.

Diese Funktion erfordert das Plugin ``fess-ds-atlassian``.

Unterstützte Produkte
=====================

- Jira (Cloud / Server / Data Center)
- Confluence (Cloud / Server / Data Center)

Voraussetzungen
===============

1. Plugin-Installation ist erforderlich
2. Entsprechende Anmeldedaten für Atlassian-Produkte sind erforderlich
3. Für Cloud-Version ist OAuth 2.0, für Server-Version ist OAuth 1.0a oder Basic-Authentifizierung verfügbar

Plugin-Installation
-------------------

Installieren Sie über "System" -> "Plugins" in der Administrationsoberfläche:

1. Laden Sie ``fess-ds-atlassian-X.X.X.jar`` von Maven Central herunter
2. Laden Sie es hoch und installieren Sie es über die Plugin-Verwaltung
3. Starten Sie |Fess| neu

Konfiguration
=============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - Company Jira/Confluence
   * - Handler-Name
     - JiraDataStore oder ConfluenceDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Beispiel für Cloud-Version (OAuth 2.0):

::

    home=https://yourcompany.atlassian.net
    deployment=cloud
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Beispiel für Server-Version (Basic-Authentifizierung):

::

    home=https://jira.yourcompany.com
    deployment=datacenter
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Beispiel für Server-Version (OAuth 1.0a):

::

    home=https://jira.yourcompany.com
    deployment=datacenter
    auth_type=oauth
    oauth.consumer_key=OauthKey
    oauth.private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...=\n-----END RSA PRIVATE KEY-----
    oauth.secret=verification_code
    oauth.access_token=your_access_token

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``home``
     - Ja
     - URL der Atlassian-Instanz
   * - ``deployment``
     - Nein
     - ``cloud`` für Atlassian Cloud, ``datacenter`` für Data Center oder Server (``data_center`` und ``dc`` werden ebenfalls akzeptiert). Wenn nicht angegeben, wird ein Hostname mit der Endung ``.atlassian.net`` als Cloud und jeder andere als Data Center behandelt.
   * - ``is_cloud``
     - Nein
     - **Veraltet** (verwenden Sie ``deployment``). ``true`` für Cloud, ``false`` für Data Center / Server. Wird weiterhin ausgewertet und schreibt eine Warnung ins Log; bei Angabe beider Parameter hat ``deployment`` Vorrang. Wird in 16.0 entfernt.
   * - ``auth_type``
     - Ja
     - Authentifizierungstyp: ``oauth``, ``oauth2``, ``basic``, ``pat``
   * - ``oauth.consumer_key``
     - Bei OAuth 1.0a
     - Consumer Key (normalerweise ``OauthKey``)
   * - ``oauth.private_key``
     - Bei OAuth 1.0a
     - RSA Private Key (PEM-Format)
   * - ``oauth.secret``
     - Bei OAuth 1.0a
     - Verification Code
   * - ``oauth.access_token``
     - Bei OAuth 1.0a
     - Access Token
   * - ``oauth2.client_id``
     - Bei OAuth 2.0
     - Client-ID
   * - ``oauth2.client_secret``
     - Bei OAuth 2.0
     - Client-Secret
   * - ``oauth2.access_token``
     - Bei OAuth 2.0
     - Access Token
   * - ``oauth2.refresh_token``
     - Nein
     - Refresh Token (OAuth 2.0)
   * - ``oauth2.token_url``
     - Nein
     - Token-URL (OAuth 2.0, Standard: ``https://auth.atlassian.com/oauth/token``)
   * - ``oauth2.grant_type``
     - Nein
     - Grant-Typ (OAuth 2.0): ``authorization_code`` (Standard) oder ``client_credentials``. Bei ``client_credentials`` sind nur ``oauth2.client_id`` und ``oauth2.client_secret`` erforderlich; die erhaltenen Tokens werden nicht in die Konfiguration des Datenspeichers zurückgeschrieben.
   * - ``basic.username``
     - Bei Basic-Authentifizierung
     - Benutzername
   * - ``basic.password``
     - Bei Basic-Authentifizierung
     - Passwort
   * - ``pat.token``
     - Bei PAT-Authentifizierung
     - Persönliches Zugriffstoken (``auth_type=pat``, nur Data Center)
   * - ``jira.jql``
     - Nein
     - JQL (nur Jira, erweiterte Suchbedingungen). Wenn nicht angegeben, werden alle Issues (``created is not empty``) berücksichtigt.
   * - ``jira.max_results``
     - Nein
     - Maximale Ergebnisse pro Jira-API-Anfrage (Standard: ``50``, nur Jira)
   * - ``confluence.limit``
     - Nein
     - Maximale Inhalte pro Confluence-API-Anfrage (Standard: ``25``, nur Confluence)
   * - ``issue.jql``
     - Nein
     - **Veraltet** (verwenden Sie ``jira.jql``). Wird weiterhin ausgewertet und schreibt eine Warnung ins Log; bei Angabe beider Parameter hat der neue Name Vorrang. Wird in 16.0 entfernt.
   * - ``issue_max_results``
     - Nein
     - **Veraltet** (verwenden Sie ``jira.max_results``). Behandlung wie oben.
   * - ``content_limit``
     - Nein
     - **Veraltet** (verwenden Sie ``confluence.limit``). Behandlung wie oben.
   * - ``ignore_error``
     - Nein
     - Verarbeitung bei Fehlern fortsetzen (Standard: ``true``)
   * - ``include_pattern``
     - Nein
     - URL-Einschlussmuster (Regex)
   * - ``exclude_pattern``
     - Nein
     - URL-Ausschlussmuster (Regex)
   * - ``number_of_threads``
     - Nein
     - Anzahl der Threads für parallele Verarbeitung (Standard: ``1``)
   * - ``proxy_host``
     - Nein
     - HTTP-Proxy-Hostname
   * - ``proxy_port``
     - Nein
     - HTTP-Proxy-Portnummer
   * - ``connection_timeout``
     - Nein
     - HTTP-Verbindungs-Timeout (Millisekunden, Standard: ``20000``)
   * - ``read_timeout``
     - Nein
     - HTTP-Lese-Timeout (Millisekunden, Standard: ``60000``)
   * - ``read_interval``
     - Nein
     - Mindestabstand zwischen API-Anfragen (in Millisekunden, Standard: ``0``). Der Abstand gilt gemeinsam für alle Threads und bleibt daher auch bei ``number_of_threads`` größer als ``1`` erhalten.

Skript-Einstellungen
--------------------

Für Jira
~~~~~~~~

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\n" + issue.comments
    last_modified=issue.last_modified

Verfügbare Felder:

- ``issue.view_url`` - URL des Issues
- ``issue.summary`` - Issue-Zusammenfassung
- ``issue.description`` - Issue-Beschreibung
- ``issue.comments`` - Issue-Kommentare
- ``issue.last_modified`` - Letztes Änderungsdatum

Für Confluence
~~~~~~~~~~~~~~

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\n" + content.comments
    last_modified=content.last_modified

Verfügbare Felder:

- ``content.view_url`` - URL der Seite
- ``content.title`` - Seitentitel
- ``content.body`` - Seiteninhalt
- ``content.comments`` - Seitenkommentare
- ``content.last_modified`` - Letztes Änderungsdatum

.. note::
   Der Confluence-Konnektor ruft sowohl reguläre Seiten (page) als auch Blog-Beiträge (blogpost) ab.

OAuth 2.0-Authentifizierung einrichten
======================================

Für Cloud-Version (empfohlen)
-----------------------------

1. Erstellen Sie eine Anwendung in der Atlassian Developer Console
2. Erhalten Sie OAuth 2.0-Anmeldedaten
3. Konfigurieren Sie die erforderlichen Scopes:

   - Jira: ``read:jira-work``, ``read:jira-user``
   - Confluence: ``read:confluence-content.all``, ``read:confluence-user``

4. Erhalten Sie Access Token und Refresh Token

OAuth 1.0a-Authentifizierung einrichten
=======================================

Für Server-Version
------------------

1. Erstellen Sie einen Application Link in Jira oder Confluence
2. Generieren Sie ein RSA-Schlüsselpaar:

   ::

       openssl genrsa -out private_key.pem 2048
       openssl rsa -in private_key.pem -pubout -out public_key.pem

3. Registrieren Sie den öffentlichen Schlüssel im Application Link
4. Konfigurieren Sie den privaten Schlüssel in den Parametern

Basic-Authentifizierung einrichten
==================================

Einfache Einrichtung für Server-Version
---------------------------------------

.. warning::
   Basic-Authentifizierung wird aus Sicherheitsgründen nicht empfohlen. Verwenden Sie wenn möglich OAuth-Authentifizierung.

Bei Verwendung von Basic-Authentifizierung:

1. Bereiten Sie ein Benutzerkonto mit Administratorrechten vor
2. Konfigurieren Sie Benutzername und Passwort in den Parametern
3. Stellen Sie eine sichere Verbindung über HTTPS sicher

Erweiterte Suche mit JQL
========================

Filtern von Jira-Issues mit JQL
-------------------------------

Crawlen Sie nur Issues, die bestimmte Bedingungen erfüllen:

::

    # Nur bestimmtes Projekt
    jira.jql=project = "MYPROJECT"

    # Bestimmten Status ausschließen
    jira.jql=project = "MYPROJECT" AND status != "Closed"

    # Zeitraum angeben
    jira.jql=updated >= -30d

    # Kombination mehrerer Bedingungen
    jira.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

Für Details zu JQL siehe die `Atlassian JQL-Dokumentation <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Anwendungsbeispiele
===================

Jira Cloud crawlen
------------------

Parameter:

::

    home=https://yourcompany.atlassian.net
    deployment=cloud
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    jira.jql=project = "SUPPORT" AND status != "Closed"

Skript:

::

    url=issue.view_url
    title=issue.summary
    content=issue.description + "\n\nKommentare:\n" + issue.comments
    last_modified=issue.last_modified

Confluence Server crawlen
-------------------------

Parameter:

::

    home=https://wiki.yourcompany.com
    deployment=datacenter
    auth_type=basic
    basic.username=crawler_user
    basic.password=secure_password

Skript:

::

    url=content.view_url
    title=content.title
    content=content.body + "\n\nKommentare:\n" + content.comments
    last_modified=content.last_modified
    digest=content.title

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``401 Unauthorized`` oder ``403 Forbidden``

**Zu überprüfen**:

1. Überprüfen Sie die Richtigkeit der Anmeldedaten
2. Bei Cloud-Version, überprüfen Sie, ob die entsprechenden Scopes konfiguriert sind
3. Bei Server-Version, überprüfen Sie, ob der Benutzer die entsprechenden Berechtigungen hat
4. Bei OAuth 2.0, überprüfen Sie die Gültigkeit des Tokens

Verbindungsfehler
-----------------

**Symptom**: ``Connection refused`` oder Verbindungs-Timeout

**Zu überprüfen**:

1. Überprüfen Sie, ob die ``home``-URL korrekt ist
2. Überprüfen Sie die Firewall-Einstellungen
3. Überprüfen Sie, ob die Atlassian-Instanz läuft
4. Überprüfen Sie, ob der ``deployment``-Parameter korrekt eingestellt ist (oder, falls er fehlt, ob der Hostname in ``home`` zur Umgebung passt)

Keine Daten abrufbar
--------------------

**Symptom**: Crawling ist erfolgreich, aber 0 Dokumente

**Zu überprüfen**:

1. Überprüfen Sie, ob JQL zu restriktiv filtert
2. Überprüfen Sie, ob der Benutzer Lesezugriff auf die Projekte/Spaces hat
3. Überprüfen Sie die Skript-Einstellungen
4. Prüfen Sie die Logs auf Fehler

OAuth 2.0-Token-Aktualisierung
------------------------------

**Symptom**: Authentifizierungsfehler treten nach einiger Zeit auf

**Lösung**:

OAuth 2.0-Access-Tokens haben ein Ablaufdatum. Durch Konfiguration des Refresh Tokens ist eine automatische Aktualisierung möglich:

::

    oauth2.refresh_token=your_refresh_token

Bei einer Token-Aktualisierung werden das neue Access Token und das neue Refresh Token automatisch in der Datenspeicher-Konfiguration gespeichert, sodass nachfolgende Crawling-Vorgänge die aktualisierten Tokens verwenden (eine manuelle Aktualisierung ist nicht erforderlich).

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Atlassian Developer <https://developer.atlassian.com/>`_
