=====================================================
Teil 7 Suchstrategien im Zeitalter von Cloud-Speicher
=====================================================

Einführung
============

In vielen Unternehmen ist die Nutzung von Cloud-Speicherdiensten längst selbstverständlich.
Dennoch ist es keine Seltenheit, dass je nach Abteilung oder Einsatzzweck unterschiedliche Cloud-Speicherdienste verwendet werden.
Die Zeit, die damit verbracht wird, sich zu fragen "War diese Datei in Google Drive, SharePoint oder doch in Box?", beeinträchtigt die Produktivität.

In diesem Artikel wird beschrieben, wie Sie mehrere Cloud-Speicherdienste mit Fess integrieren und eine Umgebung aufbauen, in der Sie alle Dateien in der Cloud über ein einziges Suchfeld dienstübergreifend durchsuchen können.

Zielgruppe
==========

- Administratoren von Organisationen, die mehrere Cloud-Speicherdienste nutzen
- Personen, die bei der Suche in Cloud-Speicherdiensten auf Herausforderungen stoßen
- Personen, die mit den Grundkonzepten der OAuth-Authentifizierung vertraut sind

Szenario
========

Ein Unternehmen nutzt die folgenden Cloud-Speicherdienste.

.. list-table:: Nutzung von Cloud-Speicherdiensten
   :header-rows: 1
   :widths: 25 35 40

   * - Dienst
     - Nutzende Abteilung
     - Hauptverwendungszweck
   * - Google Drive
     - Vertrieb und Marketing
     - Angebote, Berichte, Tabellenkalkulationen
   * - SharePoint Online
     - Unternehmensweit
     - Intranet-Portal, gemeinsame Dokumente
   * - Box
     - Rechtsabteilung und Buchhaltung
     - Verträge, Rechnungen, vertrauliche Dokumente

Vorbereitung der Cloud-Speicher-Integration
=============================================

Installation der Datenspeicher-Plugins
--------------------------------------

Für das Crawling von Cloud-Speicherdiensten werden die folgenden Plugins verwendet.

- ``fess-ds-gsuite``: Crawling von Google Drive / Google Workspace
- ``fess-ds-microsoft365``: Crawling von SharePoint Online / OneDrive
- ``fess-ds-box``: Crawling von Box

Die Installation erfolgt über die Verwaltungsoberfläche unter [System] > [Plugins].

OAuth-Authentifizierung konfigurieren
-------------------------------------

Für den Zugriff auf die APIs der Cloud-Speicherdienste ist die Konfiguration der OAuth-Authentifizierung erforderlich.
Registrieren Sie in der Verwaltungskonsole des jeweiligen Dienstes eine Anwendung und rufen Sie die Client-ID und das Client-Secret ab.

**Allgemeine Vorgehensweise**

1. Registrieren Sie eine Anwendung in der Verwaltungskonsole des jeweiligen Dienstes
2. Konfigurieren Sie die erforderlichen API-Scopes (Berechtigungen) (Lesezugriff ist ausreichend)
3. Rufen Sie die Client-ID und das Client-Secret ab
4. Tragen Sie diese Informationen in die Datenspeicher-Konfiguration von Fess ein

Konfiguration der einzelnen Dienste
=====================================

Google Drive konfigurieren
---------------------------

Machen Sie die Dateien in Google Drive suchbar.

**Vorbereitung in der Google Cloud Console**

1. Erstellen Sie ein Projekt in der Google Cloud Console
2. Aktivieren Sie die Google Drive API
3. Erstellen Sie ein Dienstkonto und laden Sie die JSON-Schlüsseldatei herunter
4. Geben Sie das Dienstkonto für die gewünschten Laufwerke und Ordner frei

**Konfiguration in Fess**

1. [Crawler] > [Datenspeicher] > [Neu erstellen]
2. Handler-Name: GoogleDriveDataStore auswählen
3. Parameter und Skripte konfigurieren
4. Label: ``google-drive`` festlegen

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    private_key=-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n-----END RSA PRIVATE KEY-----
    private_key_id=your-private-key-id
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    supported_mimetypes=.*
    include_pattern=
    exclude_pattern=

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_time

Tragen Sie die Werte für ``private_key``, ``private_key_id`` und ``client_email`` aus der JSON-Schlüsseldatei des Dienstkontos ein. Google-eigene Formate wie Google Docs, Tabellen und Präsentationen können ebenfalls als Text extrahiert und durchsucht werden.

SharePoint Online konfigurieren
---------------------------------

Machen Sie die Dokumentbibliotheken von SharePoint Online suchbar.

**Vorbereitung in Entra ID (Azure AD)**

1. Registrieren Sie eine Anwendung in Entra ID
2. Konfigurieren Sie die Berechtigungen für die Microsoft Graph API (z. B. Sites.Read.All)
3. Erstellen Sie ein Client-Secret oder ein Zertifikat

**Konfiguration in Fess**

1. [Crawler] > [Datenspeicher] > [Neu erstellen]
2. Handler-Name: SharePointDocLibDataStore auswählen (für Dokumentbibliotheken. Je nach Einsatzzweck können auch SharePointListDataStore, SharePointPageDataStore oder OneDriveDataStore verwendet werden)
3. Parameter und Skripte konfigurieren
4. Label: ``sharepoint`` festlegen

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    tenant=your-tenant-id
    client_id=your-client-id
    client_secret=your-client-secret
    site_id=your-site-id

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=name
    content=content
    last_modified=modified

``tenant``, ``client_id`` und ``client_secret`` werden mit den Werten aus der Anwendungsregistrierung in Entra ID konfiguriert. Wenn ``site_id`` angegeben wird, wird nur die angegebene Website gecrawlt. Wird der Wert weggelassen, werden alle zugänglichen Websites erfasst.

Box konfigurieren
------------------

Machen Sie die Dateien in Box suchbar.

**Vorbereitung in der Box Developer Console**

1. Erstellen Sie eine benutzerdefinierte Anwendung in der Box Developer Console
2. Wählen Sie als Authentifizierungsmethode "Serverauthentifizierung (mit Client-Anmeldeinformationen)"
3. Bitten Sie einen Administrator um die Genehmigung der Anwendung

**Konfiguration in Fess**

1. [Crawler] > [Datenspeicher] > [Neu erstellen]
2. Handler-Name: BoxDataStore auswählen
3. Parameter und Skripte konfigurieren
4. Label: ``box`` festlegen

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    client_id=your-client-id
    client_secret=your-client-secret
    enterprise_id=your-enterprise-id
    public_key_id=your-public-key-id
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIE...\n-----END ENCRYPTED PRIVATE KEY-----
    passphrase=your-passphrase
    supported_mimetypes=.*

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=name
    content=contents
    mimetype=mimetype
    content_length=size
    last_modified=modified_at

Konfigurieren Sie die Authentifizierungsinformationen der in der Box Developer Console erstellten benutzerdefinierten Anwendung. Mit ``supported_mimetypes`` können Sie die zu crawlenden Dateiformate per regulärem Ausdruck einschränken.

Optimierung der dienstübergreifenden Suche
=============================================

Nutzung des inkrementellen Crawlings
--------------------------------------

Beim Crawling von Cloud-Speicherdiensten ist es effizienter, anstatt jedes Mal alle Dateien abzurufen, nur die seit dem letzten Crawling aktualisierten Dateien zu erfassen (inkrementelles Crawling).

Prüfen Sie in der Konfiguration der jeweiligen Plugins, ob die Option für inkrementelles Crawling verfügbar ist.
Durch inkrementelles Crawling lässt sich die Anzahl der API-Aufrufe reduzieren und die Crawling-Dauer verkürzen.

URL der Suchergebnisse
-----------------------

Bei Dokumenten, die aus Cloud-Speicherdiensten gecrawlt wurden, öffnet ein Klick auf den Link in den Suchergebnissen die Datei in der Web-Oberfläche des jeweiligen Dienstes.
Dies ist für die Benutzer ein natürliches Verhalten, und es ist in der Regel keine besondere Konfiguration erforderlich.

Hinweise zum Betrieb
======================

Erneuerung der OAuth-Tokens
-----------------------------

Bei der Integration mit Cloud-Speicherdiensten ist auf die Gültigkeit der OAuth-Tokens zu achten.

- **Google Drive**: Bei Dienstkonten werden die Tokens automatisch erneuert
- **SharePoint Online**: Client-Secrets haben ein Ablaufdatum und müssen regelmäßig erneuert werden
- **Box**: Es kann erforderlich werden, die Anwendung erneut genehmigen zu lassen

Tragen Sie die Ablaufdaten der Tokens in Ihren Kalender ein, um einen Crawling-Stopp durch abgelaufene Tokens zu vermeiden.

Überwachung der API-Nutzung
------------------------------

Die APIs der Cloud-Speicherdienste unterliegen Nutzungsbeschränkungen.
Insbesondere beim Crawling großer Datenmengen sollten Sie die API-Nutzung überwachen und die Crawling-Konfiguration so anpassen, dass die Limits nicht überschritten werden.

Berechtigungen und Sicherheit
-------------------------------

Konfigurieren Sie für das Fess-Dienstkonto der Cloud-Speicherdienste ausschließlich Lesezugriffsberechtigungen.
Schreibberechtigungen sind nicht erforderlich -- folgen Sie dem Prinzip der Minimierung von Sicherheitsrisiken.

Darüber hinaus lässt sich durch die Kombination mit der in Teil 5 behandelten rollenbasierten Suche eine Steuerung der Suchergebnisse realisieren, die dem Berechtigungskonzept der Cloud-Speicherdienste entspricht.

Zusammenfassung
================

In diesem Artikel wurde beschrieben, wie Sie die drei Cloud-Speicherdienste Google Drive, SharePoint Online und Box mit Fess integrieren und eine dienstübergreifende Suchumgebung aufbauen.

- Konfiguration der Datenspeicher-Plugins und der OAuth-Authentifizierung für die einzelnen Cloud-Speicherdienste
- Unterscheidung und Filterung der Informationsquellen mithilfe von Labels
- Optimierung des Sucherlebnisses durch inkrementelles Crawling
- Verwaltung von OAuth-Tokens und Überwachung der API-Nutzung

Das Ergebnis ist eine Umgebung, in der Sie benötigte Dateien sofort finden können, ohne darüber nachdenken zu müssen, in welchem Cloud-Speicher sie sich befinden.

Im nächsten Teil wird es um den Tuning-Zyklus zur kontinuierlichen Verbesserung der Suchqualität gehen.

Referenzen
==========

- `Fess Datenspeicher-Konfiguration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin-Übersicht <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
