==================================
Salesforce-Konnektor
==================================

Übersicht
=========

Der Salesforce-Konnektor bietet die Funktionalität, Daten von Salesforce-Objekten (Standardobjekte, benutzerdefinierte Objekte) abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-salesforce`` erforderlich.

Unterstützte Objekte
====================

- **Standardobjekte**: Account, Contact, Lead, Opportunity, Case, Solution usw.
- **Benutzerdefinierte Objekte**: Selbst erstellte Objekte
- **Knowledge-Artikel**: Salesforce Knowledge

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Eine Salesforce Connected App muss erstellt werden
3. OAuth-Authentifizierung muss konfiguriert werden
4. Lesezugriff auf die Objekte ist erforderlich

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins".

Oder weitere Details finden Sie unter :doc:`../../admin/plugin-guide`.

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
     - Salesforce CRM
   * - Handler-Name
     - SalesforceDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

OAuth Token-Authentifizierung (empfohlen):

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true
    custom=FessObj,CustomProduct
    FessObj.title=Name
    FessObj.contents=Name,Description__c
    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c

OAuth Password-Authentifizierung:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=admin@example.com
    client_id=3MVG9...
    client_secret=1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrSt
    number_of_threads=1
    ignoreError=true

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``base_url``
     - Ja
     - Salesforce-URL (Produktion: ``https://login.salesforce.com``, Sandbox: ``https://test.salesforce.com``)
   * - ``auth_type``
     - Ja
     - Authentifizierungstyp (``oauth_token`` oder ``oauth_password``)
   * - ``username``
     - Ja
     - Salesforce-Benutzername
   * - ``client_id``
     - Ja
     - Consumer Key der Connected App
   * - ``private_key``
     - bei oauth_token
     - Privater Schlüssel (PEM-Format, Zeilenumbrüche als ``\n``)
   * - ``client_secret``
     - bei oauth_password
     - Consumer Secret der Connected App
   * - ``security_token``
     - bei oauth_password
     - Sicherheitstoken des Benutzers
   * - ``number_of_threads``
     - Nein
     - Anzahl paralleler Verarbeitungs-Threads (Standard: 1)
   * - ``ignoreError``
     - Nein
     - Bei Fehler Verarbeitung fortsetzen (Standard: true)
   * - ``custom``
     - Nein
     - Namen benutzerdefinierter Objekte (kommagetrennt)
   * - ``<Objekt>.title``
     - Nein
     - Feldname für Titel
   * - ``<Objekt>.contents``
     - Nein
     - Feldnamen für Inhalt (kommagetrennt)

Skript-Einstellungen
--------------------

::

    title="[" + object.type + "] " + object.title
    digest=object.description
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Verfügbare Felder
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``object.type``
     - Objekttyp (z.B.: Case, User, Solution)
   * - ``object.title``
     - Name des Objekts
   * - ``object.description``
     - Beschreibung des Objekts
   * - ``object.content``
     - Textinhalt des Objekts
   * - ``object.id``
     - Objekt-ID
   * - ``object.content_length``
     - Länge des Inhalts
   * - ``object.created``
     - Erstellungsdatum
   * - ``object.last_modified``
     - Letztes Änderungsdatum
   * - ``object.url``
     - URL des Objekts
   * - ``object.thumbnail``
     - Thumbnail-URL

Salesforce Connected App konfigurieren
======================================

1. Connected App erstellen
--------------------------

Im Salesforce Setup:

1. Öffnen Sie "App-Manager"
2. Klicken Sie auf "Neue verbundene App"
3. Geben Sie die grundlegenden Informationen ein:

   - Name der verbundenen App: Fess Crawler
   - API-Name: Fess_Crawler
   - Kontakt-E-Mail: your-email@example.com

4. Aktivieren Sie "API aktivieren (OAuth-Einstellungen aktivieren)"

2. OAuth Token-Authentifizierung konfigurieren (empfohlen)
----------------------------------------------------------

In den OAuth-Einstellungen:

1. Aktivieren Sie "Digitale Signatur verwenden"
2. Laden Sie ein Zertifikat hoch (im folgenden Schritt erstellt)
3. Ausgewählte OAuth-Bereiche:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

4. Klicken Sie auf "Speichern"
5. Kopieren Sie den Consumer Key

Zertifikaterstellung:

::

    # Privaten Schlüssel generieren
    openssl genrsa -out private_key.pem 2048

    # Zertifikat generieren
    openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

    # Privaten Schlüssel überprüfen
    cat private_key.pem

Laden Sie das Zertifikat (certificate.crt) in Salesforce hoch und setzen Sie den Inhalt des privaten Schlüssels (private_key.pem) in den Parametern.

3. OAuth Password-Authentifizierung konfigurieren
-------------------------------------------------

In den OAuth-Einstellungen:

1. Callback-URL: ``https://localhost`` (wird nicht verwendet, aber erforderlich)
2. Ausgewählte OAuth-Bereiche:

   - Full access (full)
   - Perform requests on your behalf at any time (refresh_token, offline_access)

3. Klicken Sie auf "Speichern"
4. Kopieren Sie Consumer Key und Consumer Secret

Sicherheitstoken abrufen:

1. Öffnen Sie die persönlichen Einstellungen in Salesforce
2. Klicken Sie auf "Mein Sicherheitstoken zurücksetzen"
3. Kopieren Sie das per E-Mail gesendete Token

4. Connected App genehmigen
---------------------------

Unter "Verwalten" -> "Verbundene Apps verwalten":

1. Wählen Sie die erstellte Connected App
2. Klicken Sie auf "Bearbeiten"
3. Ändern Sie "Zulässige Benutzer" auf "Vom Administrator genehmigte Benutzer sind vorab genehmigt"
4. Weisen Sie Profile oder Berechtigungssets zu

Benutzerdefinierte Objekte konfigurieren
========================================

Benutzerdefinierte Objekte crawlen
----------------------------------

Geben Sie in den Parametern mit ``custom`` die Namen der benutzerdefinierten Objekte an:

::

    custom=FessObj,CustomProduct,ProjectTask

Feldmapping für jedes Objekt:

::

    FessObj.title=Name
    FessObj.contents=Name,Description__c,Notes__c

    CustomProduct.title=Product_Name__c
    CustomProduct.contents=Product_Name__c,Product_Description__c,Specifications__c

    ProjectTask.title=Task_Name__c
    ProjectTask.contents=Task_Name__c,Task_Description__c

Feldmapping-Regeln
~~~~~~~~~~~~~~~~~~

- ``<Objektname>.title`` - Feld für Titel (einzelnes Feld)
- ``<Objektname>.contents`` - Felder für Inhalt (mehrere kommagetrennt)

Anwendungsbeispiele
===================

Standardobjekte crawlen
-----------------------

Parameter:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=1
    ignoreError=true

Skript:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    timestamp=object.last_modified
    url=object.url

Benutzerdefinierte Objekte crawlen
----------------------------------

Parameter:

::

    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=admin@example.com
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    number_of_threads=2
    ignoreError=true
    custom=Product__c,Contract__c
    Product__c.title=Name
    Product__c.contents=Name,Description__c,Category__c
    Contract__c.title=Contract_Name__c
    Contract__c.contents=Contract_Name__c,Terms__c,Notes__c

Skript:

::

    title="[" + object.type + "] " + object.title
    content=object.content
    created=object.created
    timestamp=object.last_modified
    url=object.url

Sandbox-Umgebung crawlen
------------------------

Parameter:

::

    base_url=https://test.salesforce.com
    auth_type=oauth_password
    username=admin@example.com.sandbox
    client_id=3MVG9A2kN3Bn17hvOLkjEo7GFdC...
    client_secret=1234567890ABCDEF1234567890ABCDEF
    security_token=AbCdEfGhIjKlMnOpQrStUvWxYz
    number_of_threads=1
    ignoreError=true

Skript:

::

    title="[SANDBOX] [" + object.type + "] " + object.title
    content=object.content
    timestamp=object.last_modified
    url=object.url

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``Authentication failed`` oder ``invalid_grant``

**Zu überprüfen**:

1. Bei OAuth Token-Authentifizierung:

   - Überprüfen Sie, ob der Consumer Key korrekt ist
   - Überprüfen Sie, ob der private Schlüssel korrekt kopiert wurde (Zeilenumbrüche als ``\n``)
   - Überprüfen Sie, ob das Zertifikat in Salesforce hochgeladen wurde
   - Überprüfen Sie, ob der Benutzername korrekt ist

2. Bei OAuth Password-Authentifizierung:

   - Überprüfen Sie Consumer Key und Consumer Secret
   - Überprüfen Sie das Sicherheitstoken
   - Überprüfen Sie, dass Passwort und Sicherheitstoken nicht verkettet sind (separat konfigurieren)

3. Gemeinsam:

   - Überprüfen Sie, ob base_url korrekt ist (Produktions- oder Sandbox-Umgebung)
   - Überprüfen Sie, ob die Connected App genehmigt wurde

Objekte werden nicht abgerufen
------------------------------

**Symptom**: Crawling erfolgreich, aber 0 Objekte

**Zu überprüfen**:

1. Überprüfen Sie, ob der Benutzer Leseberechtigung für die Objekte hat
2. Bei benutzerdefinierten Objekten überprüfen Sie, ob der Objektname korrekt ist (API-Name)
3. Überprüfen Sie das Feldmapping
4. Überprüfen Sie die Logs auf Fehlermeldungen

Name des benutzerdefinierten Objekts
------------------------------------

API-Namen des benutzerdefinierten Objekts ermitteln:

1. Öffnen Sie "Objekt-Manager" im Salesforce Setup
2. Wählen Sie das benutzerdefinierte Objekt
3. Kopieren Sie den "API-Namen" (endet normalerweise mit ``__c``)

Beispiel:

- Bezeichnung: Product
- API-Name: Product__c (diesen verwenden)

Feldname ermitteln
------------------

API-Namen des benutzerdefinierten Felds ermitteln:

1. Öffnen Sie "Felder und Beziehungen" des Objekts
2. Wählen Sie das benutzerdefinierte Feld
3. Kopieren Sie den "Feldnamen" (endet normalerweise mit ``__c``)

Beispiel:

- Feldbeschriftung: Product Description
- Feldname: Product_Description__c (diesen verwenden)

API-Ratenbegrenzung
-------------------

**Symptom**: ``REQUEST_LIMIT_EXCEEDED``

**Lösung**:

1. Reduzieren Sie ``number_of_threads`` (auf 1 setzen)
2. Verlängern Sie das Crawl-Intervall
3. Überprüfen Sie die Salesforce API-Nutzung
4. Bei Bedarf zusätzliche API-Limits erwerben

Bei großen Datenmengen
----------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

1. Teilen Sie Objekte in mehrere Datenspeicher auf
2. Passen Sie ``number_of_threads`` an (ca. 2-4)
3. Verteilen Sie die Crawl-Zeitplanung
4. Mappen Sie nur benötigte Felder

Formatfehler beim privaten Schlüssel
------------------------------------

**Symptom**: ``Invalid private key format``

**Lösung**:

Überprüfen Sie, ob die Zeilenumbrüche im privaten Schlüssel korrekt als ``\n`` vorliegen:

::

    # Korrektes Format
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n

    # Falsches Format (enthält tatsächliche Zeilenumbrüche)
    private_key=-----BEGIN PRIVATE KEY-----
    MIIEvgIBADANBgkqhkiG9w0BAQE...
    -----END PRIVATE KEY-----

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Salesforce REST API <https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/>`_
- `Salesforce OAuth 2.0 JWT Bearer Flow <https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm>`_
- `Salesforce Connected Apps <https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm>`_
