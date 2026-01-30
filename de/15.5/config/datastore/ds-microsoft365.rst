==================================
Microsoft 365-Konnektor
==================================

Übersicht
=========

Der Microsoft 365-Konnektor bietet die Funktionalität, Daten von Microsoft 365-Diensten (OneDrive, OneNote, Teams, SharePoint) abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-microsoft365`` erforderlich.

Unterstützte Dienste
====================

- **OneDrive**: Benutzer-Drives, Gruppen-Drives, freigegebene Dokumente
- **OneNote**: Notizbücher (Site, Benutzer, Gruppe)
- **Teams**: Kanäle, Nachrichten, Chats
- **SharePoint Document Libraries**: Dokumentbibliothek-Metadaten
- **SharePoint Lists**: Listen und Listenelemente
- **SharePoint Pages**: Site-Seiten, Nachrichtenartikel

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Eine Azure AD-Anwendungsregistrierung ist erforderlich
3. Microsoft Graph API-Berechtigungen und Administratoreinwilligung sind erforderlich
4. Java 21 oder höher, Fess 15.2.0 oder höher

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-microsoft365/X.X.X/fess-ds-microsoft365-X.X.X.jar

    # Platzieren
    cp fess-ds-microsoft365-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    sudo cp fess-ds-microsoft365-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2: Aus Quellcode erstellen

::

    git clone https://github.com/codelibs/fess-ds-microsoft365.git
    cd fess-ds-microsoft365
    mvn clean package
    cp target/fess-ds-microsoft365-*.jar $FESS_HOME/app/WEB-INF/lib/

Starten Sie |Fess| nach der Installation neu.

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
     - Microsoft 365 OneDrive
   * - Handler-Name
     - OneDriveDataStore / OneNoteDataStore / TeamsDataStore / SharePointDocLibDataStore / SharePointListDataStore / SharePointPageDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen (gemeinsam)
-----------------------------------

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=abcdefghijklmnopqrstuvwxyz123456
    number_of_threads=1
    ignore_error=false

Gemeinsame Parameterliste
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``tenant``
     - Ja
     - Azure AD Mandanten-ID
   * - ``client_id``
     - Ja
     - Client-ID der App-Registrierung
   * - ``client_secret``
     - Ja
     - Client-Secret der App-Registrierung
   * - ``number_of_threads``
     - Nein
     - Anzahl paralleler Verarbeitungs-Threads (Standard: 1)
   * - ``ignore_error``
     - Nein
     - Bei Fehler Verarbeitung fortsetzen (Standard: false)
   * - ``include_pattern``
     - Nein
     - Regex-Muster für einzuschließende Inhalte
   * - ``exclude_pattern``
     - Nein
     - Regex-Muster für auszuschließende Inhalte
   * - ``default_permissions``
     - Nein
     - Standard-Rollenzuweisung

Azure AD-Anwendungsregistrierung
================================

1. Anwendung im Azure Portal registrieren
-----------------------------------------

Öffnen Sie Azure Active Directory unter https://portal.azure.com:

1. Klicken Sie auf "App-Registrierungen" -> "Neue Registrierung"
2. Geben Sie den Anwendungsnamen ein
3. Wählen Sie den unterstützten Kontotyp
4. Klicken Sie auf "Registrieren"

2. Client-Secret erstellen
--------------------------

Unter "Zertifikate und Geheimnisse":

1. Klicken Sie auf "Neuer geheimer Clientschlüssel"
2. Legen Sie Beschreibung und Ablaufdatum fest
3. Kopieren Sie den Geheimniswert (kann später nicht mehr eingesehen werden)

3. API-Berechtigungen hinzufügen
--------------------------------

Unter "API-Berechtigungen":

1. Klicken Sie auf "Berechtigung hinzufügen"
2. Wählen Sie "Microsoft Graph"
3. Wählen Sie "Anwendungsberechtigungen"
4. Fügen Sie die erforderlichen Berechtigungen hinzu (siehe unten)
5. Klicken Sie auf "Administratoreinwilligung erteilen"

Erforderliche Berechtigungen nach Datenspeicher
===============================================

OneDriveDataStore
-----------------

Erforderliche Berechtigungen:

- ``Files.Read.All``

Bedingte Berechtigungen:

- ``User.Read.All`` - bei user_drive_crawler=true
- ``Group.Read.All`` - bei group_drive_crawler=true
- ``Sites.Read.All`` - bei shared_documents_drive_crawler=true

OneNoteDataStore
----------------

Erforderliche Berechtigungen:

- ``Notes.Read.All``

Bedingte Berechtigungen:

- ``User.Read.All`` - bei user_note_crawler=true
- ``Group.Read.All`` - bei group_note_crawler=true
- ``Sites.Read.All`` - bei site_note_crawler=true

TeamsDataStore
--------------

Erforderliche Berechtigungen:

- ``Team.ReadBasic.All``
- ``Group.Read.All``
- ``Channel.ReadBasic.All``
- ``ChannelMessage.Read.All``
- ``ChannelMember.Read.All``
- ``User.Read.All``

Bedingte Berechtigungen:

- ``Chat.Read.All`` - bei Angabe von chat_id
- ``Files.Read.All`` - bei append_attachment=true

SharePointDocLibDataStore
-------------------------

Erforderliche Berechtigungen:

- ``Files.Read.All``
- ``Sites.Read.All``

Oder ``Sites.Selected`` (bei Angabe von site_id, muss pro Site konfiguriert werden)

SharePointListDataStore / SharePointPageDataStore
-------------------------------------------------

Erforderliche Berechtigungen:

- ``Sites.Read.All``

Oder ``Sites.Selected`` (bei Angabe von site_id, muss pro Site konfiguriert werden)

Skript-Einstellungen
====================

OneDrive
--------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Verfügbare Felder:

- ``file.name`` - Dateiname
- ``file.description`` - Dateibeschreibung
- ``file.contents`` - Textinhalt
- ``file.mimetype`` - MIME-Typ
- ``file.filetype`` - Dateityp
- ``file.created`` - Erstellungsdatum
- ``file.last_modified`` - Letztes Änderungsdatum
- ``file.size`` - Dateigröße
- ``file.web_url`` - URL zum Öffnen im Browser
- ``file.roles`` - Zugriffsberechtigungen

OneNote
-------

::

    title=notebook.name
    content=notebook.contents
    created=notebook.created
    last_modified=notebook.last_modified
    url=notebook.web_url
    role=notebook.roles
    size=notebook.size

Verfügbare Felder:

- ``notebook.name`` - Notizbuchname
- ``notebook.contents`` - Integrierter Inhalt von Abschnitten und Seiten
- ``notebook.size`` - Inhaltsgröße (Zeichenanzahl)
- ``notebook.created`` - Erstellungsdatum
- ``notebook.last_modified`` - Letztes Änderungsdatum
- ``notebook.web_url`` - URL zum Öffnen im Browser
- ``notebook.roles`` - Zugriffsberechtigungen

Teams
-----

::

    title=message.title
    content=message.content
    created=message.created_date_time
    last_modified=message.last_modified_date_time
    url=message.web_url
    role=message.roles

Verfügbare Felder:

- ``message.title`` - Nachrichtentitel
- ``message.content`` - Nachrichteninhalt
- ``message.created_date_time`` - Erstellungsdatum
- ``message.last_modified_date_time`` - Letztes Änderungsdatum
- ``message.web_url`` - URL zum Öffnen im Browser
- ``message.roles`` - Zugriffsberechtigungen
- ``message.from`` - Absenderinformationen

SharePoint Document Libraries
-----------------------------

::

    title=doclib.name
    content=doclib.content
    created=doclib.created
    last_modified=doclib.modified
    url=doclib.url
    role=doclib.roles

Verfügbare Felder:

- ``doclib.name`` - Name der Dokumentbibliothek
- ``doclib.description`` - Beschreibung der Bibliothek
- ``doclib.content`` - Integrierter Suchinhalt
- ``doclib.created`` - Erstellungsdatum
- ``doclib.modified`` - Letztes Änderungsdatum
- ``doclib.url`` - SharePoint-URL
- ``doclib.site_name`` - Site-Name

SharePoint Lists
----------------

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Verfügbare Felder:

- ``item.title`` - Titel des Listenelements
- ``item.content`` - Textinhalt
- ``item.created`` - Erstellungsdatum
- ``item.modified`` - Letztes Änderungsdatum
- ``item.url`` - SharePoint-URL
- ``item.fields`` - Map aller Felder
- ``item.roles`` - Zugriffsberechtigungen

SharePoint Pages
----------------

::

    title=page.title
    content=page.content
    created=page.created
    last_modified=page.modified
    url=page.url
    role=page.roles

Verfügbare Felder:

- ``page.title`` - Seitentitel
- ``page.content`` - Seiteninhalt
- ``page.created`` - Erstellungsdatum
- ``page.modified`` - Letztes Änderungsdatum
- ``page.url`` - SharePoint-URL
- ``page.type`` - Seitentyp (news/article/page)
- ``page.roles`` - Zugriffsberechtigungen

Zusätzliche Parameter nach Datenspeicher
========================================

OneDrive
--------

::

    max_content_length=-1
    ignore_folder=true
    supported_mimetypes=.*
    drive_id=
    shared_documents_drive_crawler=true
    user_drive_crawler=true
    group_drive_crawler=true

OneNote
-------

::

    site_note_crawler=true
    user_note_crawler=true
    group_note_crawler=true

Teams
-----

::

    team_id=
    exclude_team_ids=
    include_visibility=
    channel_id=
    chat_id=
    ignore_replies=false
    append_attachment=true
    ignore_system_events=true
    title_dateformat=yyyy/MM/dd'T'HH:mm:ss
    title_timezone_offset=Z

SharePoint Document Libraries
-----------------------------

::

    site_id=
    exclude_site_id=
    ignore_system_libraries=true

SharePoint Lists
----------------

::

    site_id=hostname,siteCollectionId,siteId
    list_id=
    exclude_list_id=
    list_template_filter=
    ignore_system_lists=true

SharePoint Pages
----------------

::

    site_id=
    exclude_site_id=
    ignore_system_pages=true
    page_type_filter=

Anwendungsbeispiele
===================

Alle OneDrive-Laufwerke crawlen
-------------------------------

Parameter:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    user_drive_crawler=true
    group_drive_crawler=true
    shared_documents_drive_crawler=true

Skript:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created
    last_modified=file.last_modified
    url=file.web_url
    role=file.roles

Teams-Nachrichten eines bestimmten Teams crawlen
------------------------------------------------

Parameter:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    team_id=19:abc123def456@thread.tacv2
    ignore_replies=false
    append_attachment=true
    title_timezone_offset=+01:00

Skript:

::

    title=message.title
    content=message.content
    created=message.created_date_time
    url=message.web_url
    role=message.roles

SharePoint-Listen crawlen
-------------------------

Parameter:

::

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your_client_secret
    site_id=contoso.sharepoint.com,686d3f1a-a383-4367-b5f5-93b99baabcf3,12048306-4e53-420e-bd7c-31af611f6d8a
    list_template_filter=100,101
    ignore_system_lists=true

Skript:

::

    title=item.title
    content=item.content
    created=item.created
    last_modified=item.modified
    url=item.url
    role=item.roles

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``Authentication failed`` oder ``Insufficient privileges``

**Zu überprüfen**:

1. Überprüfen Sie, ob Mandanten-ID, Client-ID und Client-Secret korrekt sind
2. Überprüfen Sie, ob die erforderlichen API-Berechtigungen im Azure Portal erteilt wurden
3. Überprüfen Sie, ob die Administratoreinwilligung erteilt wurde
4. Überprüfen Sie das Ablaufdatum des Client-Secrets

API-Ratenbegrenzungsfehler
--------------------------

**Symptom**: ``429 Too Many Requests``

**Lösung**:

1. Reduzieren Sie ``number_of_threads`` (auf 1 oder 2 setzen)
2. Verlängern Sie das Crawl-Intervall
3. Setzen Sie ``ignore_error=true`` zur Fortsetzung der Verarbeitung

Keine Daten abrufbar
--------------------

**Symptom**: Crawling erfolgreich, aber 0 Dokumente

**Zu überprüfen**:

1. Überprüfen Sie, ob die Zieldaten existieren
2. Überprüfen Sie, ob die API-Berechtigungen korrekt konfiguriert sind
3. Überprüfen Sie die Einstellungen der Benutzer-/Gruppen-Drive-Crawler
4. Überprüfen Sie die Logs auf Fehlermeldungen

SharePoint-Site-ID ermitteln
----------------------------

Mit PowerShell:

::

    Connect-PnPOnline -Url "https://contoso.sharepoint.com/sites/yoursite" -Interactive
    Get-PnPSite | Select Id

Oder mit Microsoft Graph API:

::

    GET https://graph.microsoft.com/v1.0/sites/contoso.sharepoint.com:/sites/yoursite

Crawling großer Datenmengen
---------------------------

**Lösung**:

1. In mehrere Datenspeicher aufteilen (nach Site, Drive usw.)
2. Last über Zeitplaneinstellungen verteilen
3. ``number_of_threads`` für parallele Verarbeitung anpassen
4. Nur bestimmte Ordner/Sites crawlen

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-gsuite` - Google Workspace-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Microsoft Graph API <https://docs.microsoft.com/en-us/graph/>`_
- `Azure AD App Registration <https://docs.microsoft.com/en-us/azure/active-directory/develop/>`_
