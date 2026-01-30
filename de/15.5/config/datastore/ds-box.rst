==================================
Box-Konnektor
==================================

Übersicht
=========

Der Box-Konnektor bietet die Funktionalität, Dateien aus dem Box.com-Cloud-Speicher abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-box`` erforderlich.

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Ein Box-Entwicklerkonto und eine Anwendung müssen erstellt werden
3. JWT-Authentifizierung (JSON Web Token) oder OAuth 2.0-Authentifizierung muss konfiguriert werden

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-box/X.X.X/fess-ds-box-X.X.X.jar

    # Platzieren
    cp fess-ds-box-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-box-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Company Box Storage
   * - Handler-Name
     - BoxDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Beispiel für JWT-Authentifizierung (empfohlen):

::

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``client_id``
     - Ja
     - Client-ID der Box-App
   * - ``client_secret``
     - Ja
     - Client-Secret der Box-App
   * - ``public_key_id``
     - Ja
     - ID des öffentlichen Schlüssels
   * - ``private_key``
     - Ja
     - Privater Schlüssel (PEM-Format, Zeilenumbrüche als ``\n``)
   * - ``passphrase``
     - Ja
     - Passphrase des privaten Schlüssels
   * - ``enterprise_id``
     - Ja
     - Box Enterprise-ID

Skript-Einstellungen
--------------------

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Verfügbare Felder
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``file.url``
     - Link zum Öffnen der Datei im Browser
   * - ``file.contents``
     - Textinhalt der Datei
   * - ``file.mimetype``
     - MIME-Typ der Datei
   * - ``file.filetype``
     - Dateityp
   * - ``file.name``
     - Dateiname
   * - ``file.size``
     - Dateigröße (Bytes)
   * - ``file.created_at``
     - Erstellungsdatum
   * - ``file.modified_at``
     - Datum der letzten Änderung

Weitere Details finden Sie unter `Box File Object <https://developer.box.com/reference#file-object>`_.

Box-Authentifizierung konfigurieren
===================================

Schritte zur JWT-Authentifizierung
----------------------------------

1. Anwendung in der Box Developer Console erstellen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Besuchen Sie https://app.box.com/developers/console:

1. Klicken Sie auf "Create New App"
2. Wählen Sie "Custom App"
3. Wählen Sie als Authentifizierungsmethode "Server Authentication (with JWT)"
4. Geben Sie den App-Namen ein und erstellen Sie sie

2. Anwendungskonfiguration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Konfigurieren Sie im Tab "Configuration":

**Application Scopes**:

- Aktivieren Sie "Read all files and folders stored in Box"

**Advanced Features**:

- Klicken Sie auf "Generate a Public/Private Keypair"
- Laden Sie die generierte JSON-Datei herunter (wichtig!)

**App Access Level**:

- Wählen Sie "App + Enterprise Access"

3. Enterprise-Genehmigung
~~~~~~~~~~~~~~~~~~~~~~~~~

In der Box Admin-Konsole:

1. Öffnen Sie "Apps" -> "Custom Apps"
2. Genehmigen Sie die erstellte App

4. Authentifizierungsinformationen abrufen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rufen Sie die folgenden Informationen aus der heruntergeladenen JSON-Datei ab:

::

    {
      "boxAppSettings": {
        "clientID": "hdf8a7sd...",         // client_id
        "clientSecret": "kMN7sd8f...",      // client_secret
        "appAuth": {
          "publicKeyID": "4tg5h6j7",        // public_key_id
          "privateKey": "-----BEGIN...",    // private_key
          "passphrase": "7ba8sd9f..."       // passphrase
        }
      },
      "enterpriseID": "1923456"             // enterprise_id
    }

Format des privaten Schlüssels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``private_key`` wird in eine Zeile umgewandelt, wobei Zeilenumbrüche durch ``\n`` ersetzt werden:

::

    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgk...=\n-----END ENCRYPTED PRIVATE KEY-----\n

Anwendungsbeispiele
===================

Gesamten Box-Speicher des Unternehmens crawlen
----------------------------------------------

Parameter:

::

    client_id=abc123def456ghi789jkl012mno345
    client_secret=pqr678stu901vwx234yz567abc890
    public_key_id=a1b2c3d4
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDjBABgkqhkiG9w0BBQ0wOzAbBgkqhkiG9w0BBQwwDgQI...=\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    enterprise_id=123456789

Skript:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Nur bestimmte Ordner crawlen
----------------------------

Im Skript kann auch nach Ordnerpfaden gefiltert werden:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at

Nur PDF-Dateien crawlen
-----------------------

Filterung nach MIME-Typ im Skript:

::

    if (file.mimetype == "application/pdf") {
        url=file.url
        title=file.name
        content=file.contents
        mimetype=file.mimetype
        filename=file.name
        created=file.created_at
        last_modified=file.modified_at
    }

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``Authentication failed`` oder ``Invalid grant``

**Zu überprüfen**:

1. Überprüfen Sie, ob ``client_id`` und ``client_secret`` korrekt sind
2. Überprüfen Sie, ob der private Schlüssel korrekt kopiert wurde (Zeilenumbrüche als ``\n``)
3. Überprüfen Sie, ob die Passphrase korrekt ist
4. Überprüfen Sie, ob die App in der Box Admin-Konsole genehmigt wurde
5. Überprüfen Sie, ob die ``enterprise_id`` korrekt ist

Formatfehler beim privaten Schlüssel
------------------------------------

**Symptom**: ``Invalid private key format``

**Lösung**:

Überprüfen Sie, ob die Zeilenumbrüche im privaten Schlüssel korrekt in ``\n`` umgewandelt wurden:

::

    # Korrektes Format
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n

    # Falsches Format (enthält tatsächliche Zeilenumbrüche)
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----
    MIIFDj...
    -----END ENCRYPTED PRIVATE KEY-----

Keine Dateien abrufbar
----------------------

**Symptom**: Crawling erfolgreich, aber 0 Dateien

**Zu überprüfen**:

1. Überprüfen Sie, ob "Read all files and folders" in den Application Scopes aktiviert ist
2. Überprüfen Sie, ob der App Access Level auf "App + Enterprise Access" gesetzt ist
3. Überprüfen Sie, ob tatsächlich Dateien im Box-Speicher existieren
4. Überprüfen Sie, ob das Service-Konto die entsprechenden Berechtigungen hat

Bei großen Dateimengen
----------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

Teilen Sie die Verarbeitung in den Datenspeicher-Einstellungen auf:

1. Passen Sie das Crawl-Intervall an
2. Teilen Sie in mehrere Datenspeicher auf (z.B. nach Ordner)
3. Verteilen Sie die Last über die Zeitplaneinstellungen

Berechtigungen und Zugriffskontrolle
====================================

Box-Dateiberechtigungen abbilden
--------------------------------

.. note::
   In der aktuellen Implementierung werden keine detaillierten Box-Berechtigungsinformationen abgerufen.
   Bei Bedarf können Sie das ``role``-Feld verwenden, um die Zugriffskontrolle zu konfigurieren.

Standardberechtigungen festlegen:

::

    # Parameter
    default_permissions={role}box-users

Berechtigungen im Skript setzen:

::

    url=file.url
    title=file.name
    content=file.contents
    role=["box-users"]
    mimetype=file.mimetype
    filename=file.name
    created=file.created_at
    last_modified=file.modified_at

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-dropbox` - Dropbox-Konnektor
- :doc:`ds-gsuite` - Google Workspace-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Box Developer Documentation <https://developer.box.com/>`_
- `Box Platform Authentication <https://developer.box.com/guides/authentication/>`_
