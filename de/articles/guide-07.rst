==================================================
Dateien in Google Drive, SharePoint und Box finden
==================================================

Einführung
==========

Wenn Abteilungen Google Drive, SharePoint Online und Box parallel nutzen, verbringt man immer mehr Zeit damit, sich zu erinnern, wo ein Dokument abgelegt wurde.
Mit den Datenspeicher-Plugins von Fess lassen sich die Dateien aller drei Dienste über eine einzige Suchseite finden.

In Cloud-Speichern liegen jedoch Dateien mit unterschiedlichen Zugriffsrechten nebeneinander.
Bei einer Fehlkonfiguration erscheinen vertrauliche Dateien wie Verträge sogar in den Suchergebnissen von Benutzern, die nicht angemeldet sind.
Dieser Artikel zeigt für jeden Dienst eine Minimalkonfiguration, die sich unverändert übernehmen lässt und funktioniert, sowie den Weg, die ursprünglichen Berechtigungen in Fess zu übernehmen.

Schritte, die für alle Datenspeicher gleich sind – Plugins installieren, Handler-Namen, Parameter, Skripte schreiben und Jobs anlegen –, sind in :doc:`datastore-basics` zusammengefasst.
Lesen Sie zuerst diesen Artikel, bevor Sie fortfahren.
Die Einstellungen in diesem Artikel beziehen sich auf Fess 15.9 und die Version 15.9.0 der jeweiligen Plugins.

Was wir aufbauen
================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Dienst
     - Plugin
     - Handler-Name
     - Was auf der Seite des Dienstes vorzubereiten ist
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - Ein JSON-Schlüssel eines Dienstkontos und domainweite Delegierung
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - Eine App-Registrierung in Entra ID (Clientgeheimnis) und Anwendungsberechtigungen für Microsoft Graph
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - Eine benutzerdefinierte Box-App mit JWT-Authentifizierung

Wenn Fess unter Docker läuft, können Sie Plugin-Namen und Versionen, durch Leerzeichen getrennt, in der Umgebungsvariablen ``FESS_PLUGINS`` aufführen, um sie beim Start gemeinsam zu installieren.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

Wenn Sie die Plugins über die Administrationsoberfläche oder mit ``fess-setup`` installieren, müssen Sie Fess nach der Installation neu starten (``FESS_PLUGINS`` installiert die Plugins vor dem Start von Fess, daher ist dort kein Neustart nötig).

Vorab entscheiden: Wer darf die Suchergebnisse sehen?
=====================================================

Wenn Sie eine neue Datenspeicher-Konfiguration anlegen, enthält das Feld „Berechtigungen“ bereits ``{role}guest``.
Bleibt dieser Wert stehen, können auch nicht angemeldete Benutzer die importierten Dateien finden.
Alle drei Plugins schreiben die aus den ursprünglichen Freigabeeinstellungen gebildeten Rollen in ``file.roles``.
Die Konfiguration ist deshalb bei allen drei in den folgenden zwei Punkten gleich:

- ``{role}guest`` aus dem Feld „Berechtigungen“ löschen und das Feld leer lassen
- ``role=file.roles`` in das Skript schreiben

Beide Punkte sind nötig, weil die Plugins das Feld „Berechtigungen“ unterschiedlich behandeln.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Plugin
     - Wert des Felds „Berechtigungen“
     - Parameter ``default_permissions``
   * - Google Drive
     - Wird nicht verwendet, wenn Sie ``role=file.roles`` schreiben. Andernfalls wird der Feldwert (anfangs ``{role}guest``) unverändert an alle Dateien angehängt
     - Wird nur für Dateien verwendet, für die sich aus der Drive-ACL nichts ermitteln ließ. Ist auch er nicht gesetzt, wird die Datei nicht importiert
   * - SharePoint (OneDriveDataStore)
     - Wird mit ``file.roles`` zusammengeführt. Bleibt ``{role}guest`` stehen, werden alle Dateien öffentlich
     - Wird allen Dateien hinzugefügt
   * - Box
     - Wird mit ``file.roles`` zusammengeführt. Bleibt ``{role}guest`` stehen, werden alle Dateien öffentlich
     - Wird allen Dateien hinzugefügt

``file.roles`` enthält Zeichenketten, die die Benutzer und Gruppen des jeweiligen Dienstes darstellen.

- Google Drive: Benutzer und Gruppen sind E-Mail-Adressen, Dateieigentümer haben dasselbe Format. Eine Domainfreigabe wird zu ``{group}<Domainname>`` (änderbar mit ``domain_permission_format``), eine öffentliche, über die Suche auffindbare Freigabe (``anyone``) wird zur Rolle ``guest``. Eine Freigabe nur für Personen mit dem Link wird zu keiner Rolle.
- SharePoint: Benutzer sind Objekt-ID und UPN, Gruppen sind ID und Anzeigename. Ein Freigabelink für „Personen in Ihrer Organisation“ wird zur Gruppe ``EVERYONE_IN_TENANT``.
- Box: Benutzer sind Box-Benutzer-ID und Login (E-Mail-Adresse), Gruppen sind die Box-Gruppen-ID. Neben den Kollaborationen der Datei selbst werden auch die Kollaborationen und Eigentümer der übergeordneten Ordner einbezogen.

Bei der Suche werden diese Werte mit dem Benutzernamen und den Gruppennamen des bei Fess angemeldeten Benutzers abgeglichen.
Damit zum Beispiel Benutzerberechtigungen von Google Drive greifen, muss der Fess-Benutzername mit der E-Mail-Adresse übereinstimmen.
Zum Konzept der Rollen siehe :doc:`guide-05`, zur Anmeldung per SSO :doc:`guide-15`.

Für Labels, mit denen sich Suchergebnisse nach Dienst eingrenzen lassen, hat die Datenspeicher-Konfiguration kein eigenes Feld.
Fügen Sie dem Skript eine Zeile wie ``label="box"`` hinzu oder legen Sie ein Label an, das auf die URLs passt (Einzelheiten in :doc:`datastore-basics`).
Label-Werte dürfen nur alphanumerische Zeichen und ``_`` enthalten; ein Wert mit Bindestrich wie ``google-drive`` lässt sich nicht anlegen.

Google Drive: Freigegebene Ablagen importieren
==============================================

Vorbereitung bei Google
-----------------------

In 15.9 arbeitet ``fess-ds-gsuite`` standardmäßig mit ``crawl_target=shared_drives``.
Dabei werden alle freigegebenen Ablagen der Domain gelesen, indem sich das Plugin als Domainadministrator ausgibt.

1. In der Google Cloud Console ein Projekt anlegen und die Google Drive API aktivieren
2. Ein Dienstkonto anlegen und auf dem Tab [Keys] einen Schlüssel im JSON-Format erstellen und herunterladen
3. Für das Dienstkonto die domainweite Delegierung aktivieren und die OAuth-2-Client-ID notieren
4. In der Google Workspace Admin Console unter [Security] > [Access and data control] > [API controls] > [Domain-wide delegation] dieser Client-ID den Bereich ``https://www.googleapis.com/auth/drive.readonly`` erlauben

Das in ``impersonate_user`` angegebene Konto muss Domainadministrator von Google Workspace sein.
Ist ``crawl_target`` nicht ``legacy`` und fehlt ``impersonate_user``, bricht der Crawl beim Start mit einem Fehler ab.

Parameter und Skript
--------------------

Wählen Sie unter [Crawler] > [Datenspeicher] > [Neu erstellen] als „Handler-Name“ ``GoogleDriveDataStore`` und leeren Sie das Feld „Berechtigungen“.
Übernehmen Sie in ``private_key``, ``private_key_id`` und ``client_email`` die gleichnamigen Werte aus dem JSON-Schlüssel.
Schreiben Sie ``private_key`` in eine einzige Zeile und lassen Sie die Zeilenumbrüche als ``\n`` stehen.

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url`` ist der ``webViewLink`` der Datei.
Das Übernehmen von Löschungen setzt voraus, dass die indexierte URL die Drive-Datei-ID enthält.
Verwenden Sie ``url`` deshalb unverändert, ohne es umzuschreiben.

Die weiteren Importbereiche sind:

- ``crawl_target=users``: liest „Meine Ablage“ aller Benutzer. Dazu müssen Sie die Admin SDK API aktivieren und den Bereich ``https://www.googleapis.com/auth/admin.directory.user.readonly`` hinzufügen (sowohl in der Delegierung als auch im Parameter ``scopes``).
- ``crawl_target=legacy``: liest nur Dateien, die direkt mit der Adresse des Dienstkontos geteilt wurden. Delegierung und ``impersonate_user`` sind nicht erforderlich.

Inkrementelles Crawlen
----------------------

Mit ``incremental=true`` liest das Plugin ab dem zweiten Durchlauf nur noch den Änderungsfeed von Drive.
Dabei wird ``delete_old_docs`` zwangsweise auf ``false`` gesetzt, sodass aus Drive gelöschte Dateien im Index verbleiben können.
Außerdem werden unveränderte Dateien nicht neu registriert und verschwinden daher ohne weitere Maßnahmen aus den Suchergebnissen, sobald die Anzahl Tage unter „Alte Dokumente löschen“ (standardmäßig 3 Tage) abgelaufen ist (siehe den Abschnitt über das Ablaufdatum von Dokumenten in :doc:`datastore-basics`).

Wenn Sie inkrementell crawlen, kombinieren Sie es wie folgt:

- Legen Sie zusätzlich eine Konfiguration für einen vollständigen Crawl ohne ``incremental`` an und führen Sie sie regelmäßig aus, etwa einmal pro Woche
- Geben Sie in beiden Konfigurationen ein ``time_to_live`` an, das etwas länger ist als das Intervall des vollständigen Crawls (bei einem wöchentlichen vollständigen Crawl ``time_to_live=11520``, also 8 Tage)

Aus Drive gelöschte Dateien verschwinden aus den Suchergebnissen, sobald diese Frist abläuft.
Die Position im Änderungsfeed schreibt das Plugin in das Feld „Parameter“ zurück; bearbeiten Sie den zurückgeschriebenen Wert nicht.

SharePoint Online: Dateien aus Dokumentbibliotheken importieren
===============================================================

Welcher Handler?
----------------

Um den Inhalt von Dateien in SharePoint-Dokumentbibliotheken zu durchsuchen, verwenden Sie ``OneDriveDataStore`` aus ``fess-ds-microsoft365``.

- ``SharePointDocLibDataStore`` registriert jede Bibliothek nur als ein einziges Dokument und importiert die darin enthaltenen Dateien nicht.
- ``fess-ds-sharepoint`` (``SharePointDataStore``) ist für lokal betriebene SharePoint Server gedacht. Es unterstützt Microsoft Graph nicht, und für SharePoint Online wird auf ``fess-ds-microsoft365`` verwiesen.

Vorbereitung in Entra ID
------------------------

1. Im Azure Portal unter [App registrations] eine neue Registrierung anlegen
2. Unter [Certificates & secrets] ein neues Clientgeheimnis erstellen und den Wert notieren (hier legen Sie die Gültigkeitsdauer fest)
3. Unter [API permissions] > [Microsoft Graph] > [Application permissions] die vier unten aufgeführten Berechtigungen hinzufügen
4. [Grant admin consent] ausführen

Fügen Sie die folgenden Anwendungsberechtigungen hinzu:

- ``Files.Read.All``
- ``User.Read.All``, ``Group.Read.All``: in jedem Importbereich erforderlich, um Benutzer- und Gruppennamen der ACLs nachzuschlagen
- ``Sites.Read.All``: erforderlich, um mit ``shared_documents_drive_crawler=true`` die Websites aufzulisten

Parameter und Skript
--------------------

Ohne weitere Angaben liest ``OneDriveDataStore`` alle SharePoint-Websites und zusätzlich das OneDrive aller Benutzer sowie die Laufwerke aller Microsoft 365-Gruppen.
Um nur SharePoint zu erfassen, setzen Sie die drei Flags explizit.

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

Um nur bestimmte Bibliotheken zu importieren, setzen Sie alle drei Flags auf ``false`` und geben die Laufwerks-ID in ``drive_id`` an.
Die Laufwerks-ID ermitteln Sie in Microsoft Graph mit ``GET /sites/{site-id}/drives``.
Geben Sie nur ``drive_id`` an und lassen die Flags stehen, wird dieses Laufwerk dem Gesamtimport lediglich „hinzugefügt“.

Fehlende Berechtigungen und Wiederholungen
------------------------------------------

Die ACL einer Datei wird mit einem eigenen Graph-Aufruf pro Datei abgerufen.
Was bei einem Fehlschlag dieses Aufrufs geschieht, bestimmt ``permission_failure_policy``.
Mit dem Standardwert ``skip`` wird die Datei nicht registriert und unter [Systeminformationen] > [Fehler-URL] sowie im WARN-Log festgehalten.
Mit ``index_without_acl`` werden Dateien mit unvollständiger ACL registriert; für Bibliotheken mit hoher Vertraulichkeit ist es daher sicherer, den Standardwert beizubehalten.

Wiederholungen von Graph-Aufrufen lassen sich mit ``max_retry_count`` (Standard 3, höchstens 10) und ``retry_interval`` (Sekunden, Standard 3, höchstens 180) anpassen.
``OneDriveDataStore`` bietet keine Option für inkrementelles Crawlen und liest jedes Mal alles.

Box: Einen Vertragsordner mit Berechtigungen importieren
========================================================

Vorbereitung bei Box
--------------------

``fess-ds-box`` unterstützt nur die Serverauthentifizierung mit JWT.

1. In der Box Developer Console eine „Custom App“ anlegen und als Authentifizierungsmethode „Server Authentication (with JWT)“ wählen
2. Auf dem Tab [Configuration] unter Application Scopes „Read all files and folders stored in Box“ aktivieren
3. Als App Access Level „App + Enterprise Access“ wählen
4. Mit [Generate a Public/Private Keypair] ein Schlüsselpaar erzeugen und die JSON-Datei speichern
5. Die App in der Box Admin Console autorisieren

``clientID``, ``clientSecret``, ``publicKeyID``, ``privateKey``, ``passphrase`` und ``enterpriseID`` aus der JSON-Datei entsprechen jeweils ``client_id``, ``client_secret``, ``public_key_id``, ``private_key``, ``passphrase`` und ``enterprise_id``.
Alle sechs sind Pflichtangaben.

Den Import auf einen Ordner beschränken
---------------------------------------

Steht das Ziel fest, etwa die Verträge der Rechtsabteilung, lesen Sie mit ``root_folder_id`` nur einen einzigen Ordner.
In diesem Modus gibt sich das Plugin nicht als Benutzer aus, sondern liest den Ordner als Dienstkonto der App.
Daher müssen Sie das Dienstkonto als Mitbearbeiter zum Zielordner hinzufügen.
Die Ordner-ID ist die Zahl am Ende der URL, wenn Sie den Ordner in der Box-Weboberfläche öffnen.

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

Löschen Sie unbedingt ``{role}guest`` aus dem Feld „Berechtigungen“.
Bei Box wird der Feldwert mit ``file.roles`` zusammengeführt; bleibt er stehen, können auch nicht angemeldete Benutzer die Verträge finden.

Box-Gruppen werden als Gruppen-ID zu Rollen und stimmen daher nicht ohne Weiteres mit den Gruppennamen in Fess überein.
In diesem Beispiel macht ``default_permissions={group}legal`` alle Dateien für die Fess-Gruppe ``legal`` sichtbar.
Benutzer, für die eine Datei in Box einzeln freigegeben ist, können sie zusätzlich finden, sofern ihr Login (E-Mail-Adresse) mit dem Fess-Benutzernamen übereinstimmt.
Um Dateien mit einem unternehmensweiten Freigabelink eine Rolle hinzuzufügen, verwenden Sie ``company_shared_link_role``.

Die Dateien aller Benutzer lesen
--------------------------------

Lassen Sie ``root_folder_id`` weg, listet das Plugin alle Benutzer des Unternehmens auf und liest deren Dateien, indem es sich nacheinander als jeder von ihnen ausgibt.
Die betroffenen Benutzer lassen sich mit ``filter_term`` eingrenzen.
API-Aufrufe im Namen anderer Benutzer müssen in den App-Einstellungen bei Box erlaubt sein; prüfen Sie die Einstellungen in der Entwicklerdokumentation von Box.

Umgang mit Ratenbegrenzungen
----------------------------

Die Anzahl der Wiederholungen bei ``429``- und ``5xx``-Antworten ist ``max_retry_attempts`` (Standard 5).
``max_retry_count`` (Standard 10) ist die Anzahl, wie oft die Verbindung bei einer ``401``-Antwort neu aufgebaut wird, und hat mit Ratenbegrenzungen nichts zu tun.
Um API-Aufrufe zu drosseln, legen Sie mit ``readInterval`` (Millisekunden) eine Wartezeit pro Element fest.
``fess-ds-box`` bietet keine Option für inkrementelles Crawlen.

Hinweise für den Betrieb
========================

Ablauf von Zugangsdaten
-----------------------

- Ein Clientgeheimnis in Entra ID hat die bei der Erstellung festgelegte Gültigkeitsdauer. Nach Ablauf schlägt die Authentifizierung fehl und es wird nichts mehr importiert; erstellen Sie daher vor Ablauf ein neues Geheimnis und ersetzen Sie ``client_secret`` in den Parametern.
- Google-Zugriffstoken werden von der Bibliothek, die das Plugin verwendet, automatisch erneuert. In 15.9 wird ``refresh_token_interval`` ignoriert und eine Warnung protokolliert.
- Box-Zugriffstoken werden alle ``refresh_token_interval`` Sekunden (Standard 3540) automatisch erneuert.

Wenn nicht alles importiert wird
--------------------------------

Alle drei Plugins warten am Ende eines Crawls standardmäßig 60 Sekunden auf das Ende ihrer Arbeitsthreads; was bis dahin nicht fertig ist, wird nicht importiert.
Fehlen bei einem großen Mandanten Dokumente, verlängern Sie die Wartezeit.
Der Parameter heißt bei Google Drive ``thread_pool_timeout_seconds``, bei SharePoint ``executor_shutdown_timeout`` und bei Box ``thread_pool_await_timeout`` (jeweils in Sekunden).

Bei Google Drive werden die Antworten 429, 500, 502, 503 und 504 sowie durch Ratenbegrenzung verursachte 403-Antworten mit exponentiellem Backoff wiederholt.
Die Wiederholungen lassen sich mit ``max_retries`` (Standard 5), ``retry_initial_interval_ms`` (Standard 1000) und ``max_backoff_ms`` (Standard 32000) anpassen.

Ergebnisse prüfen
=================

Wie Sie Job-Ergebnisse und Logs lesen, ist in :doc:`datastore-basics` erklärt.
Beim Crawlen von Datenspeichern kann ein Job als „OK“ angezeigt werden, obwohl der Abruf von Dateien fehlgeschlagen ist; urteilen Sie daher anhand der Dokumentanzahl und der Logs.
Für die Konfiguration in diesem Artikel prüfen Sie zusätzlich die folgenden drei Punkte:

1. Abgemeldet nach einem Wort suchen, das in einer importierten Datei vorkommt, und bestätigen, dass kein Treffer erscheint (ob das Leeren des Felds „Berechtigungen“ vergessen wurde)
2. Als Benutzer anmelden, für den die Datei freigegeben ist, und bestätigen, dass dieselbe Datei erscheint
3. Bei der Google-Drive-Konfiguration prüfen, dass ``fess-crawler.log`` kein ``Skipped ... because no permission could be resolved`` enthält (das sind Dateien, die wegen leerer ACL nicht importiert wurden)

Erscheint die Datei in Schritt 2 nicht, prüfen Sie, ob Benutzername und Gruppennamen des Benutzers mit den Werten in ``file.roles`` übereinstimmen.

Zusammenfassung
===============

- Den Inhalt von SharePoint-Dateien importieren Sie mit ``OneDriveDataStore``; setzen Sie OneDrive und Gruppenlaufwerke auf ``false``, wenn Sie sie nicht benötigen.
- Löschen Sie bei allen drei Diensten ``{role}guest`` aus dem Feld „Berechtigungen“ und schreiben Sie ``role=file.roles`` in das Skript.
- ``default_permissions`` ersetzt bei Google Drive eine leere ACL und wird bei SharePoint und Box allen Dateien hinzugefügt.
- Inkrementelles Crawlen gibt es nur bei Google Drive (``incremental=true``). Wenn Sie es nutzen, kombinieren Sie es mit einer Konfiguration für vollständige Crawls und geben in beiden ``time_to_live`` an.

Referenzen
==========

- `Google Workspace-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-gsuite.html>`__
- `Microsoft 365-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-microsoft365.html>`__
- `Box-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-box.html>`__
- `Datenspeicher-Konfiguration <https://fess.codelibs.org/de/stable/admin/dataconfig-guide.html>`__
- `fess-ds-microsoft365 15.9.0 README (Liste der Graph-Berechtigungen) <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `fess-ds-box 15.9.0 README (file.roles und root_folder_id) <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
