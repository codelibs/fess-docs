==================================
Google Workspace-Konnektor
==================================

Übersicht
=========

Der Google Workspace-Konnektor bietet die Funktionalität, Dateien aus Google Drive (ehemals G Suite) abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-gsuite`` erforderlich.

Unterstützte Dienste
====================

- Google Drive (Mein Drive, freigegebene Ablagen)
- Google Docs, Tabellen, Präsentationen, Formulare usw.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Ein Google Cloud Platform-Projekt muss erstellt werden
3. Ein Dienstkonto muss erstellt und Anmeldedaten abgerufen werden
4. Domain-weite Delegierung für Google Workspace muss konfiguriert werden

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-gsuite/X.X.X/fess-ds-gsuite-X.X.X.jar

    # Platzieren
    cp fess-ds-gsuite-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-gsuite-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2: Über die Administrationsoberfläche installieren

1. Öffnen Sie "System" -> "Plugins"
2. Laden Sie die JAR-Datei hoch
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
     - Company Google Drive
   * - Handler-Name
     - GSuiteDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``private_key``
     - Ja
     - Privater Schlüssel des Dienstkontos (PEM-Format, Zeilenumbrüche als ``\n``)
   * - ``private_key_id``
     - Ja
     - ID des privaten Schlüssels
   * - ``client_email``
     - Ja
     - E-Mail-Adresse des Dienstkontos

Skript-Einstellungen
--------------------

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.url
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    role=file.roles
    filename=file.name

Verfügbare Felder
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``file.name``
     - Dateiname
   * - ``file.description``
     - Dateibeschreibung
   * - ``file.contents``
     - Textinhalt der Datei
   * - ``file.mimetype``
     - MIME-Typ der Datei
   * - ``file.filetype``
     - Dateityp
   * - ``file.created_time``
     - Erstellungsdatum
   * - ``file.modified_time``
     - Letztes Änderungsdatum
   * - ``file.web_view_link``
     - Link zum Öffnen im Browser
   * - ``file.url``
     - URL der Datei
   * - ``file.thumbnail_link``
     - Thumbnail-Link (kurze Gültigkeit)
   * - ``file.size``
     - Dateigröße (Bytes)
   * - ``file.roles``
     - Zugriffsberechtigungen

Weitere Details finden Sie unter `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Google Cloud Platform-Konfiguration
===================================

1. Projekt erstellen
--------------------

Besuchen Sie https://console.cloud.google.com/:

1. Erstellen Sie ein neues Projekt
2. Geben Sie den Projektnamen ein
3. Wählen Sie Organisation und Standort

2. Google Drive API aktivieren
------------------------------

Unter "APIs und Dienste" -> "Bibliothek":

1. Suchen Sie nach "Google Drive API"
2. Klicken Sie auf "Aktivieren"

3. Dienstkonto erstellen
------------------------

Unter "APIs und Dienste" -> "Anmeldedaten":

1. Wählen Sie "Anmeldedaten erstellen" -> "Dienstkonto"
2. Geben Sie den Dienstkontonamen ein (z.B.: fess-crawler)
3. Klicken Sie auf "Erstellen und fortfahren"
4. Rolle ist nicht erforderlich (überspringen)
5. Klicken Sie auf "Fertig"

4. Dienstkonto-Schlüssel erstellen
----------------------------------

Beim erstellten Dienstkonto:

1. Klicken Sie auf das Dienstkonto
2. Öffnen Sie den Tab "Schlüssel"
3. "Schlüssel hinzufügen" -> "Neuen Schlüssel erstellen"
4. Wählen Sie JSON-Format
5. Speichern Sie die heruntergeladene JSON-Datei

5. Domain-weite Delegierung aktivieren
--------------------------------------

In den Dienstkonto-Einstellungen:

1. Aktivieren Sie "Domain-weite Delegierung aktivieren"
2. Klicken Sie auf "Speichern"
3. Kopieren Sie die "OAuth 2.0-Client-ID"

6. In der Google Workspace Admin-Konsole genehmigen
---------------------------------------------------

Besuchen Sie https://admin.google.com/:

1. Öffnen Sie "Sicherheit" -> "Zugriffs- und Datenverwaltung" -> "API-Steuerung"
2. Wählen Sie "Domain-weite Delegierung"
3. Klicken Sie auf "Neu hinzufügen"
4. Geben Sie die Client-ID ein
5. Geben Sie den OAuth-Bereich ein:

   ::

       https://www.googleapis.com/auth/drive.readonly

6. Klicken Sie auf "Autorisieren"

Anmeldedaten konfigurieren
==========================

Informationen aus der JSON-Datei abrufen
----------------------------------------

Heruntergeladene JSON-Datei:

::

    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgk...\n-----END PRIVATE KEY-----\n",
      "client_email": "fess-crawler@your-project.iam.gserviceaccount.com",
      "client_id": "123456789012345678901",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
    }

Setzen Sie die folgenden Informationen in den Parametern:

- ``private_key_id`` -> ``private_key_id``
- ``private_key`` -> ``private_key`` (Zeilenumbrüche bleiben als ``\n``)
- ``client_email`` -> ``client_email``

Format des privaten Schlüssels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``private_key`` behält Zeilenumbrüche als ``\n`` bei:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG...\n-----END PRIVATE KEY-----\n

Anwendungsbeispiele
===================

Gesamtes Google Drive crawlen
-----------------------------

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com

Skript:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    thumbnail=file.thumbnail_link
    content_length=file.size
    filetype=file.filetype
    filename=file.name

Crawlen mit Berechtigungen
--------------------------

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

Skript:

::

    title=file.name
    content=file.description + "\n" + file.contents
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link
    role=file.roles
    filename=file.name

Nur bestimmte Dateitypen crawlen
--------------------------------

Nur Google Docs:

::

    if (file.mimetype == "application/vnd.google-apps.document") {
        title=file.name
        content=file.description + "\n" + file.contents
        mimetype=file.mimetype
        created=file.created_time
        last_modified=file.modified_time
        url=file.web_view_link
    }

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``401 Unauthorized`` oder ``403 Forbidden``

**Zu überprüfen**:

1. Überprüfen Sie die Anmeldedaten des Dienstkontos:

   - Sind die Zeilenumbrüche im ``private_key`` als ``\n``?
   - Ist die ``private_key_id`` korrekt?
   - Ist die ``client_email`` korrekt?

2. Überprüfen Sie, ob die Google Drive API aktiviert ist
3. Überprüfen Sie, ob die Domain-weite Delegierung konfiguriert ist
4. Überprüfen Sie, ob die Genehmigung in der Google Workspace Admin-Konsole erteilt wurde
5. Überprüfen Sie den OAuth-Bereich (``https://www.googleapis.com/auth/drive.readonly``)

Fehler bei Domain-weiter Delegierung
------------------------------------

**Symptom**: ``Not Authorized to access this resource/api``

**Lösung**:

1. Überprüfen Sie die Genehmigung in der Google Workspace Admin-Konsole:

   - Ist die Client-ID korrekt registriert?
   - Ist der OAuth-Bereich korrekt (``https://www.googleapis.com/auth/drive.readonly``)?

2. Überprüfen Sie, ob die Domain-weite Delegierung beim Dienstkonto aktiviert ist

Keine Dateien abrufbar
----------------------

**Symptom**: Crawling erfolgreich, aber 0 Dateien

**Zu überprüfen**:

1. Überprüfen Sie, ob Dateien in Google Drive existieren
2. Überprüfen Sie, ob das Dienstkonto Leseberechtigung hat
3. Überprüfen Sie, ob die Domain-weite Delegierung korrekt konfiguriert ist
4. Überprüfen Sie, ob der Zugriff auf das Drive des Zielbenutzers möglich ist

API-Kontingentfehler
--------------------

**Symptom**: ``403 Rate Limit Exceeded`` oder ``429 Too Many Requests``

**Lösung**:

1. Überprüfen Sie das Kontingent in der Google Cloud Platform
2. Verlängern Sie das Crawl-Intervall
3. Beantragen Sie bei Bedarf eine Kontingenterhöhung

Formatfehler beim privaten Schlüssel
------------------------------------

**Symptom**: ``Invalid private key format``

**Lösung**:

Überprüfen Sie, ob die Zeilenumbrüche korrekt als ``\n`` vorliegen:

::

    # Korrekt
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Falsch (enthält tatsächliche Zeilenumbrüche)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Freigegebene Ablagen crawlen
----------------------------

.. note::
   Beim Crawlen freigegebener Ablagen mit dem Dienstkonto muss das Dienstkonto als Mitglied zur freigegebenen Ablage hinzugefügt werden.

1. Öffnen Sie die freigegebene Ablage in Google Drive
2. Klicken Sie auf "Mitglieder verwalten"
3. Fügen Sie die E-Mail-Adresse des Dienstkontos hinzu
4. Setzen Sie die Berechtigungsstufe auf "Betrachter"

Bei großen Dateimengen
----------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

1. Teilen Sie in mehrere Datenspeicher auf
2. Verteilen Sie die Last über Zeitplaneinstellungen
3. Passen Sie das Crawl-Intervall an
4. Crawlen Sie nur bestimmte Ordner

Berechtigungen und Zugriffskontrolle
====================================

Google Drive-Freigabeberechtigungen abbilden
--------------------------------------------

Google Drive-Freigabeeinstellungen auf Fess-Berechtigungen abbilden:

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    default_permissions={role}drive-users

Skript:

::

    title=file.name
    content=file.description + "\n" + file.contents
    role=file.roles
    mimetype=file.mimetype
    created=file.created_time
    last_modified=file.modified_time
    url=file.web_view_link

``file.roles`` enthält die Google Drive-Freigabeinformationen.

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-microsoft365` - Microsoft 365-Konnektor
- :doc:`ds-box` - Box-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
