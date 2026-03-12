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
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=your_client_id
    oauth2.client_secret=your_client_secret
    oauth2.access_token=your_access_token
    oauth2.refresh_token=your_refresh_token

Beispiel für Server-Version (Basic-Authentifizierung):

::

    home=https://jira.yourcompany.com
    is_cloud=false
    auth_type=basic
    basic.username=admin
    basic.password=your_password

Beispiel für Server-Version (OAuth 1.0a):

::

    home=https://jira.yourcompany.com
    is_cloud=false
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
   * - ``is_cloud``
     - Ja
     - ``true`` für Cloud-Version, ``false`` für Server-Version
   * - ``auth_type``
     - Ja
     - Authentifizierungstyp: ``oauth``, ``oauth2``, ``basic``
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
     - Token-URL (OAuth 2.0, Standardwert vorhanden)
   * - ``basic.username``
     - Bei Basic-Authentifizierung
     - Benutzername
   * - ``basic.password``
     - Bei Basic-Authentifizierung
     - Passwort
   * - ``issue.jql``
     - Nein
     - JQL (nur Jira, erweiterte Suchbedingungen)

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
    issue.jql=project = "MYPROJECT"

    # Bestimmten Status ausschließen
    issue.jql=project = "MYPROJECT" AND status != "Closed"

    # Zeitraum angeben
    issue.jql=updated >= -30d

    # Kombination mehrerer Bedingungen
    issue.jql=project IN ("PROJ1", "PROJ2") AND updated >= -90d AND status != "Done"

Für Details zu JQL siehe die `Atlassian JQL-Dokumentation <https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html>`_.

Anwendungsbeispiele
===================

Jira Cloud crawlen
------------------

Parameter:

::

    home=https://yourcompany.atlassian.net
    is_cloud=true
    auth_type=oauth2
    oauth2.client_id=Abc123DefGhi456
    oauth2.client_secret=xyz789uvw456rst123
    oauth2.access_token=eyJhbGciOiJIUzI1...
    oauth2.refresh_token=def456ghi789jkl012
    issue.jql=project = "SUPPORT" AND status != "Closed"

Skript:

::

    url=issue.view_url
    title="[" + issue.key + "] " + issue.summary
    content=issue.description + "\n\nKommentare:\n" + issue.comments
    last_modified=issue.last_modified

Confluence Server crawlen
-------------------------

Parameter:

::

    home=https://wiki.yourcompany.com
    is_cloud=false
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
4. Überprüfen Sie, ob der ``is_cloud``-Parameter korrekt eingestellt ist

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

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Atlassian Developer <https://developer.atlassian.com/>`_
