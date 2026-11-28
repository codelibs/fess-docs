=================================================
Datenbank-, CSV- und Salesforce-Daten durchsuchen
=================================================

Einleitung
==========

Der Produktstamm liegt in einer internen Datenbank, die Kundenliste in einer CSV-Datei, die das Kernsystem jede Nacht exportiert, und die Aufzeichnungen zu Verkaufschancen und Anfragen in Salesforce.
Solche Geschäftsdaten lassen sich oft nur über die Oberfläche des jeweiligen Systems finden.
Mit den Datenspeicher-Plugins von Fess können Sie diese Daten datensatzweise importieren und auf derselben Suchseite finden wie die Dokumente auf Dateiservern und internen Websites.

Dieser Artikel erklärt die Konfiguration für den Import jeder der drei Quellen sowie das Eingrenzen nach Quelle, die Ausführungszeitpläne und die Prüfung der Ergebnisse.
Die für alle Datenspeicher gemeinsamen Schritte, etwa die Installation der Plugins, das Schreiben von Handler-Name, Parametern und Skript sowie das Anlegen von Jobs, sind in :doc:`datastore-basics` zusammengefasst.
Lesen Sie diesen Artikel zuerst.
Die Einstellungen in diesem Artikel beziehen sich auf Fess 15.9 und die Version 15.9.0 der einzelnen Plugins.

Der Aufbau in diesem Artikel
============================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Quelle
     - Plugin
     - Handler-Name
     - Vorab bereitzustellen
   * - Datenbank (Produktstamm)
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - Die JAR-Datei des JDBC-Treibers und ein DB-Benutzer, der nur SELECT ausführen darf
   * - CSV (Kundenliste)
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - Ein Verzeichnis, in das die CSV-Dateien geschrieben werden (ein Ort, den der Crawler lesen kann)
   * - Salesforce (Accounts, Opportunities, Cases)
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - Eine Connected App und ein Schlüsselpaar zum Signieren des JWT

Wenn Sie Fess mit Docker betreiben, geben Sie die drei Plugins durch Leerzeichen getrennt unter ``environment`` von ``fess01`` in ``compose.yaml`` an.

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

Wenn Sie die Plugins über die Administrationsoberfläche oder mit ``fess-setup`` installieren, müssen Sie Fess neu starten.

Vorab festlegen: Wer die Suchergebnisse sehen darf
==================================================

Keines der drei Plugins übernimmt die Zugriffsrechte (ACL) des Quellsystems nach Fess.
Die Rollen der importierten Dokumente werden allein durch den Wert im Feld „Berechtigungen“ der Datenspeicher-Konfiguration bestimmt.
Dieses Feld enthält von Anfang an ``{role}guest``; unverändert können also auch nicht angemeldete Benutzer suchen.

Bei Daten mit Preisen oder Kundeninformationen ersetzen Sie den Wert durch die Gruppen, die die Daten sehen sollen (z. B. ``{group}sales``).
Alle Dokumente, die über eine Konfiguration registriert werden, erhalten dieselben Berechtigungen.
Verteilen Sie Daten für unterschiedliche Zielgruppen auf getrennte Datenspeicher-Konfigurationen.
Zum Entwurf der Gruppen siehe :doc:`guide-05`.

Datenbank: Den Produktstamm importieren
=======================================

Den JDBC-Treiber ablegen
------------------------

``fess-ds-db`` enthält keinen JDBC-Treiber.
Besorgen Sie die zur Datenbank passende Treiber-JAR-Datei (``postgresql-<Version>.jar`` für PostgreSQL, ``mysql-connector-j-<Version>.jar`` für MySQL) und legen Sie sie in den Klassenpfad des Crawlers.
Das Datenspeicher-Crawling läuft in einem vom Fess-Hauptprozess getrennten Crawler-Prozess, dessen Klassenpfad die JAR-Dateien der folgenden zwei Verzeichnisse enthält.

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

Beim ZIP-Paket liegen sie unter dem Verzeichnis, in das Fess entpackt wurde, bei RPM / DEB unter ``/usr/share/fess/``.
Starten Sie Fess nach dem Ablegen neu.

Auch im Docker-Image liegt Fess unter ``/usr/share/fess/``.
Eine in den Container kopierte JAR-Datei geht verloren, wenn der Container neu erstellt wird. Mounten Sie deshalb nur die eine JAR-Datei in ``fess01`` in ``compose.yaml``.

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

Wenn Sie das ganze Verzeichnis mounten, werden die JAR-Dateien, die das Image dort ablegt, unsichtbar, und der Crawler kann nicht mehr starten.
Mounten Sie immer einzelne Dateien.
Erstellen Sie die Container nach der Änderung mit ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d`` neu.

Parameter und SQL
-----------------

Als Beispiel dient hier die PostgreSQL-Tabelle ``products``.
Als Linkziel der Suchergebnisse verwenden wir die Detailansicht des Produktstamms (z. B. ``https://erp.example.com/products/<Produkt-ID>``).
Wählen Sie unter [Crawler] > [Datenspeicher] > [Neu erstellen] als Handler-Name ``DatabaseDataStore`` und setzen Sie die Parameter wie folgt.

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

Das Skript sieht so aus.

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

Schreiben Sie ``sql`` in eine einzige Zeile.
Das SQL wird unverändert an die Datenbank gesendet, und jede Zeile des Ergebnisses wird zu einem Dokument.
Wenn Sie die Link-URL und den Text bereits im SQL zusammensetzen, muss das Skript nur noch Spaltennamen enthalten.
``concat_ws`` überspringt beim Verketten NULL-Spalten, sodass der Text auch bei Produkten ohne Beschreibung nicht NULL wird.
In MySQL verhält sich ``CONCAT_WS`` genauso, ``CONCAT`` liefert dagegen insgesamt NULL, sobald ein Argument NULL ist.

Wenn Sie Fess mit Docker betreiben, bezeichnet ``localhost`` in ``url`` nicht den Datenbankserver, sondern den Fess-Container selbst.
Geben Sie den Hostnamen oder die IP-Adresse der Datenbank an.

Zuordnung von Spaltennamen und Skript
-------------------------------------

Auf der rechten Seite des Skripts geben Sie die Spaltenbezeichnungen des SELECT-Ergebnisses (die mit ``AS`` vergebenen Aliasnamen) unverändert an.
Beachten Sie die folgenden drei Punkte.

- Die Groß- und Kleinschreibung der Spaltenbezeichnungen hängt von der Datenbank ab. Aliasnamen ohne Anführungszeichen wandelt PostgreSQL in Kleinbuchstaben um, Oracle und H2 in Großbuchstaben, und MySQL gibt sie so zurück, wie sie geschrieben wurden. Schreiben Sie sie im Skript genau in der Schreibweise, die die Datenbank zurückgibt. Stimmt sie nicht überein, erhält das Feld keinen Wert
- Auch die Werte des Parameterfelds sind im Skript als gleichnamige Variablen sichtbar. Wenn Sie ``url=url`` schreiben, obwohl das Ergebnis keine Spalte ``url`` hat, wird die JDBC-Verbindungs-URL zur URL des Dokuments. Geben Sie der Spalte für das Linkziel einen Namen, der sich nicht mit einem Parameter überschneidet, etwa ``page_url``
- Eine hängende Abfrage endet nicht, wenn Sie den Job stoppen. Setzen Sie unbedingt ``query_timeout`` (in Sekunden)

``fess-ds-db`` bietet keine Option für inkrementelles Crawling.
Bei jedem Lauf wird das gesamte ``sql`` ausgeführt und alle Zeilen werden neu registriert.
Führen Sie den Job bei Tabellen mit vielen Zeilen zu einer Zeit mit geringer Datenbanklast aus (siehe „Einen Job pro Quelle anlegen“ weiter unten).

CSV: Die vom Kernsystem exportierte Kundenliste importieren
===========================================================

Die grundlegende Verwendung des CSV-Konnektors wird im Abschnitt mit dem CSV-Beispiel in :doc:`datastore-basics` erklärt.
Hier ergänzen wir nur die Punkte, die beim Import von CSV-Dateien wichtig sind, die das Kernsystem regelmäßig exportiert.

Nehmen wir als Beispiel an, dass ein japanisches Kernsystem jede Nacht um 2:00 Uhr eine Datei ``customers_20261128.csv`` wie die folgende exportiert.
Die Zeichenkodierung ist MS932 (die Windows-Variante von Shift_JIS), und die erste Zeile enthält japanische Überschriften (Kundennummer, Kundenname, Standort, zuständige Abteilung, Geschäftsstatus).

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

Ablageort der Dateien
---------------------

Exportieren Sie die CSV-Dateien in einen Pfad, der vom Server lesbar ist, auf dem der Fess-Crawler läuft.
Bei Docker mounten Sie das Exportverzeichnis schreibgeschützt in ``fess01``.

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

Parameter und Skript
--------------------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- Wenn Sie ``directories`` angeben, werden alle Dateien mit der Endung ``.csv`` / ``.tsv`` in diesem Verzeichnis gelesen, die mit dem ältesten Änderungszeitpunkt zuerst. Wird täglich eine Datei mit Datum im Namen exportiert, müssen Sie die Parameter nicht anpassen. Bleiben alte Dateien liegen, werden auch deren Zeilen jedes Mal gelesen
- CSV-Dateien aus japanischem Excel oder aus Systemen für japanisches Windows sind meist in MS932 kodiert. Geben Sie ``Shift_JIS`` an, werden Zeichen wie ``①`` oder ``㈱`` zu Ersatzzeichen; geben Sie daher ``MS932`` an
- Auch wenn die Überschriften Nicht-ASCII-Zeichen enthalten, wie hier die japanischen, überspringt ``has_header_line=true`` die erste Zeile. Im Skript ist der Zugriff über die Spaltennummer (``cell1``, ``cell2`` …) am zuverlässigsten. Spalten, deren Überschrift Leerzeichen oder Sonderzeichen enthält, lassen sich nicht über den Überschriftennamen ansprechen
- Für tabulatorgetrennte Dateien ergänzen Sie ``separator_character=\t``
- Zeilen, bei denen ``url`` zu ``null`` wird, werden nicht registriert. In diesem Beispiel werden Kunden mit dem Status 取引終了 (beendet) ausgeschlossen; nur die mit 取引中 (aktiv) werden registriert. Die Anzahl der ausgeschlossenen Zeilen erscheint in ``fess-crawler.log`` als WARN: ``Skipped 1 row(s) in ... because the script did not set the url field.``

Wird eine Datei gelesen, die gerade noch geschrieben wird, werden nur die bis dahin geschriebenen Zeilen registriert.
Führen Sie den Job nach dem Zeitpunkt aus, zu dem der CSV-Export abgeschlossen ist.

Salesforce: Accounts, Opportunities und Cases importieren
=========================================================

Vorbereitung in Salesforce
--------------------------

``fess-ds-salesforce`` unterstützt zwei Authentifizierungsmethoden: ``auth_type=oauth_token`` (JWT-Bearer-Flow) und ``auth_type=oauth_password`` (Benutzername und Passwort).
Hier verwenden wir ``oauth_token``, bei dem kein Passwort gespeichert werden muss.
Der OAuth-Flow mit Benutzername und Passwort, den ``oauth_password`` nutzt, kann je nach Einstellungen der Salesforce-Organisation deaktiviert sein.

1. Erzeugen Sie ein Schlüsselpaar und ein Zertifikat

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. Legen Sie im Salesforce Setup eine Connected App an, aktivieren Sie die OAuth-Einstellungen und laden Sie unter „Digitale Signatur verwenden“ ``certificate.crt`` hoch. Wählen Sie die OAuth-Bereiche wie in der Referenz beschrieben
3. Setzen Sie in den Richtlinien der Connected App „Zulässige Benutzer“ auf „Vom Administrator genehmigte Benutzer sind vorab genehmigt“ und weisen Sie das Profil oder den Berechtigungssatz des Benutzers zu, mit dem gecrawlt wird
4. Notieren Sie den Consumer Key der Connected App

Bildschirme und Bezeichnungen in Salesforce können sich ändern; prüfen Sie für Details daher auch die Beschreibung des JWT-Bearer-Flows in der Salesforce-Hilfe.

Fess kann nur die Datensätze und Felder importieren, die der zum Crawlen verwendete Benutzer lesen darf.
Geben Sie im weiter unten beschriebenen ``contents`` ein Feld an, das dieser Benutzer nicht lesen darf, schlägt der Abruf des betreffenden Objekts fehl.

Parameter und Skript
--------------------

Für ``private_key`` schreiben Sie den Inhalt von ``private_key.pem`` in eine einzige Zeile und ersetzen die Zeilenumbrüche durch ``\n``.
Das Plugin kann nur das PKCS#8-Format lesen (das Format, das mit ``-----BEGIN PRIVATE KEY-----`` beginnt).
Einen mit älterem OpenSSL erzeugten Schlüssel, der mit ``-----BEGIN RSA PRIVATE KEY-----`` beginnt, konvertieren Sie vorher mit ``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem``.

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

Für eine Sandbox setzen Sie ``base_url=https://test.salesforce.com``.

Alle Angaben auf der rechten Seite beginnen mit ``object.``.
Schreiben Sie sie ohne Präfix, etwa ``url=url``, schlägt die Auswertung des Ausdrucks fehl; der Datensatz wird nicht registriert, sondern als Fehler-URL erfasst.
``object.url`` hat die Form ``<Instanz-URL>/<Datensatz-ID>``; ein Klick darauf öffnet die Datensatzseite in Salesforce.

Den Importumfang eingrenzen
---------------------------

``fess-ds-salesforce`` liest immer alle 23 Arten von Standardobjekten, darunter Account, Contact, Lead, Opportunity, Case, Task und User.
Eine Einstellung, um nur ausgewählte Objekte zu lesen, gibt es nicht.
Um den Umfang einzugrenzen, kombinieren Sie die folgenden drei Mittel.

- ``include_pattern`` / ``exclude_pattern``: reguläre Ausdrücke, die auf das gesamte ``object.url`` passen müssen und festlegen, welche Datensätze registriert werden. Die ersten drei Zeichen einer Salesforce-Datensatz-ID sind je Objekt festgelegt (Account ``001``, Opportunity ``006``, Case ``500`` usw.). Das obige Beispiel registriert nur diese drei Arten. Abgerufen werden trotzdem alle Objekte; die übrigen Datensätze werden lediglich vor der Registrierung verworfen
- ``<Objektname>.title`` / ``<Objektname>.contents``: legen die Felder für Titel und Text über ihre API-Namen fest. Die Namen der Standardobjekte sind in Großbuchstaben mit Unterstrichen geschrieben, etwa ``ACCOUNT``, ``OPPORTUNITY`` oder ``CASE``. Ohne Angabe verwendet das Plugin seine Standardfelder
- ``custom``: Geben Sie die API-Namen benutzerdefinierter Objekte kommagetrennt an, werden diese zusätzlich zu den Standardobjekten gelesen

Benutzerdefinierte Objekte haben keine Standardfelder; geben Sie daher immer ``.title`` und ``.contents`` an.
Nehmen Sie das Titelfeld auch in die Textfelder auf.
Das Plugin ruft nur die Felder ab, die in ``.contents`` und ähnlichen Angaben stehen. Ein Feld, das nur in ``.title`` steht, wird nicht abgerufen, und der Titel bleibt leer.

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

Mit Labels nach Quelle eingrenzen
=================================

In den bisherigen Beispielen vergibt das ``label`` im Skript die Werte ``products``, ``customers`` und ``salesforce``.
Damit sie auf der Suchseite als Label zur Auswahl stehen, legen Sie unter [Crawler] > [Label] Labels mit demselben „Wert“ an („Eingeschlossene Pfade“ kann leer bleiben).
Label-Werte dürfen nur alphanumerische Zeichen und ``_`` enthalten.

Wenn Sie die Salesforce-Daten nach Objekt aufteilen möchten, legen Sie statt des ``label`` im Skript Labels an, deren „Eingeschlossene Pfade“ die ersten drei Zeichen der Datensatz-ID prüfen.
Ein Label mit dem Wert ``sf_case`` und dem eingeschlossenen Pfad ``https://example\.my\.salesforce\.com/500.*`` wird beispielsweise nur Cases zugewiesen.
Passt ein Label auf die URL, geht das vom Skript vergebene Label verloren.
Verwenden Sie in einer Datenspeicher-Konfiguration nur eine der beiden Methoden (Details im Abschnitt über Labels in :doc:`datastore-basics`).

Einen Job pro Quelle anlegen
============================

Im Ausgangszustand crawlt der „Default Crawler“ täglich um 0:00 Uhr alle Konfigurationen zusammen.
Jede Quelle hat ihre eigene günstige Uhrzeit; legen Sie daher für jede Datenspeicher-Konfiguration einen Job an.
Klicken Sie auf der Detailseite jeder Konfiguration auf [Neuen Job erstellen] und tragen Sie die Uhrzeit im Cron-Format unter „Zeitplan“ ein (Schritte im Abschnitt über die Zeitplanung in :doc:`datastore-basics`).

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Quelle
     - Beispiel-Zeitplan
     - Zu beachten
   * - Datenbank
     - ``0 3 * * *``
     - Da jedes Mal alle Zeilen gelesen werden, eine Zeit mit geringer Datenbanklast wählen
   * - CSV
     - ``30 2 * * *``
     - Nach dem Zeitpunkt einplanen, zu dem der Export abgeschlossen ist
   * - Salesforce
     - ``0 7,12,18 * * *``
     - Jeder Lauf erzeugt so viele Bulk-API-Jobs, wie es Standard- und benutzerdefinierte Objekte gibt. Die Häufigkeit nach dem verbleibenden API-Limit der Organisation festlegen

Der Default Crawler crawlt diese Konfigurationen weiterhin ebenfalls.
Wenn sie nicht doppelt laufen sollen, setzen Sie den „Status“ der Datenspeicher-Konfiguration auf „Deaktiviert“ (ein Job, der eine Konfigurations-ID angibt, crawlt die Konfiguration auch dann, wenn sie deaktiviert ist).

Umgang mit Zeilen, die aus den Quelldaten verschwinden
======================================================

Auch wenn Sie eine Zeile in der Datenbank löschen oder eine Zeile aus der CSV-Datei verschwindet, wird das Dokument beim nächsten Crawl nicht gelöscht.
Über einen Datenspeicher registrierte Dokumente erhalten ein Ablaufdatum, das sich bei jeder Registrierung verlängert.
Ein Dokument, das nicht mehr registriert wird, wird automatisch gelöscht, wenn seit der letzten Registrierung die Anzahl der Tage aus „Alte Dokumente löschen“ unter [System] > [Allgemein] (Standard: 3 Tage) verstrichen ist.

Dieser Mechanismus hat auch eine Seite, die Aufmerksamkeit erfordert.
Ist die Datenbank mehrere Tage in Folge nicht erreichbar und wird diese Anzahl von Tagen überschritten, verschwinden alle Dokumente dieser Konfiguration aus den Suchergebnissen.
Erkennen Sie Importfehler frühzeitig mit den Methoden aus dem nächsten Abschnitt.

Funktion prüfen
===============

Wie Sie das Jobprotokoll, [Systeminformationen] > [Crawling-Informationen], die Fehler-URLs und ``fess-crawler.log`` lesen, ist im Abschnitt über die Prüfung der Ergebnisse in :doc:`datastore-basics` erklärt.
Beim Datenspeicher-Crawling kann der Job auch dann „OK“ anzeigen, wenn der Import fehlgeschlagen ist. Beurteilen Sie das Ergebnis daher anhand der Anzahl und der Protokolle.

1. Suchen Sie unter [Systeminformationen] > [Suche] nach ``label:products``, ``label:customers`` und ``label:salesforce`` und vergleichen Sie die Anzahl mit den Quelldaten (bei einer Datenbank mit einem ``SELECT count(*)`` mit denselben Bedingungen wie in ``sql``)
2. Prüfen Sie die WARN- und ERROR-Einträge in ``fess-crawler.log``. Beim Aufbau in diesem Artikel treten am ehesten folgende Meldungen auf

   - ``The JDBC driver ... is not on the crawler classpath.``: Ablageort des Treibers oder Klassenname in ``driver`` ist falsch
   - ``Failed to connect to ...``: Hostname, Port, Benutzername und Passwort der Datenbank prüfen
   - ``is not a directory.`` oder ``No CSV file.``: Unter dem Pfad in ``directories`` gibt es keine CSV-Datei, die der Crawler lesen kann
   - ``Batch:... Failed caused by ...``: Einige Salesforce-Objekte konnten nicht abgerufen werden. Feldnamen in ``.contents`` und die Feldberechtigungen des zum Crawlen verwendeten Benutzers prüfen
   - ``Failed to process a data crawling: <Konfigurationsname>``: Die gesamte Konfiguration ist fehlgeschlagen. Bei Salesforce fallen Authentifizierungsfehler darunter. Die Ursache im nachfolgenden Stacktrace prüfen

3. Bei Konfigurationen, deren Feld „Berechtigungen“ Sie geändert haben, melden Sie sich als Benutzer der Zielgruppe an und prüfen, dass die Dokumente in den Suchergebnissen erscheinen und im abgemeldeten Zustand nicht

Zusammenfassung
===============

- Keines der drei Plugins übernimmt die Berechtigungen des Quellsystems; ersetzen Sie daher ``{role}guest`` im Feld „Berechtigungen“ durch die Gruppen, die die Daten sehen sollen
- Bei einer Datenbank legen Sie den JDBC-Treiber in den Klassenpfad des Crawlers und setzen Link-URL und Text im SQL zusammen. Es werden jedes Mal alle Zeilen gelesen
- CSV-Dateien des Kernsystems lesen Sie mit ``directories`` und ``file_encoding=MS932`` und sprechen die Spalten mit ``cellN`` an. Zeilen, bei denen ``url`` auf ``null`` gesetzt wird, werden nicht registriert
- Das Salesforce-Skript schreiben Sie mit ``object.*``. Standardobjekte lassen sich nicht auswählen; grenzen Sie daher mit ``include_pattern`` und ``<Objektname>.contents`` ein
- Legen Sie pro Quelle einen Job an und planen Sie den Betrieb so, dass aus den Quelldaten entfernte Zeilen nach der Anzahl der Tage in „Alte Dokumente löschen“ verschwinden

Weiterführende Artikel
======================

- Die gemeinsamen Mechanismen der Datenspeicher (Skripte, Berechtigungen, Labels, Prüfung der Ergebnisse): :doc:`datastore-basics`
- Git, Confluence, Jira und Slack importieren: :doc:`guide-06`
- Google Drive, SharePoint und Box importieren: :doc:`guide-07`
- Suchergebnisse je nach Abteilung unterschiedlich anzeigen: :doc:`guide-05`
- Importfehler überwachen: :doc:`guide-10`

Referenzen
==========

- `Datenbank-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-database.html>`__
- `CSV-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-csv.html>`__
- `Salesforce-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-salesforce.html>`__
- `Datenspeicher-Konfiguration <https://fess.codelibs.org/de/stable/admin/dataconfig-guide.html>`__
- `Scheduler <https://fess.codelibs.org/de/stable/admin/scheduler-guide.html>`__
- `Label <https://fess.codelibs.org/de/stable/admin/labeltype-guide.html>`__
- `Allgemein <https://fess.codelibs.org/de/stable/admin/general-guide.html>`__
