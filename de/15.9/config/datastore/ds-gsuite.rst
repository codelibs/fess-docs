==================================
Google Workspace-Konnektor
==================================

Übersicht
=========

Der Google Workspace-Konnektor bietet die Funktionalität, Dateien aus Google Drive (ehemals G Suite) abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-gsuite`` erforderlich.

Änderungen in 15.9
==================

Der Konnektor wurde in |Fess| 15.9 grundlegend überarbeitet. Lesen Sie diesen Abschnitt,
bevor Sie eine bestehende Datenspeicher-Konfiguration aktualisieren.

.. warning::

   ``crawl_target`` hat jetzt den Standardwert ``shared_drives``, und jeder Wert außer
   ``legacy`` setzt ``impersonate_user`` voraus. Eine unverändert aktualisierte
   Konfiguration **schlägt daher beim Start mit einer ``DataStoreException`` fehl**,
   statt zu laufen.

   Das ist beabsichtigt: Das bisherige Verhalten erreichte nur die Dateien, die
   ausdrücklich für das Dienstkonto freigegeben waren, sodass die Alternative ein Crawl
   wäre, der stillschweigend nichts indiziert. Setzen Sie entweder ``impersonate_user``
   auf ein Domain-Administratorkonto, oder setzen Sie ``crawl_target=legacy``, um das
   bisherige Verhalten beizubehalten.

Verhaltensänderungen
--------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Änderung
     - Erforderliche Maßnahme
   * - ``crawl_target`` hat den Standardwert ``shared_drives`` und setzt ``impersonate_user`` voraus
     - Setzen Sie ``impersonate_user`` oder ``crawl_target=legacy``. Andernfalls schlägt der Crawl beim Start fehl.
   * - Der Standard-OAuth-Bereich wurde von ``https://www.googleapis.com/auth/drive`` auf ``https://www.googleapis.com/auth/drive.readonly`` eingeschränkt
     - Aktualisieren Sie den Eintrag für die Domain-weite Delegierung in der Google Workspace Admin-Konsole, da dieser die Bereiche ausdrücklich auflistet.
   * - ``crawl_target=users`` und ``crawl_target=both`` benötigen zusätzlich ``https://www.googleapis.com/auth/admin.directory.user.readonly``
     - Fügen Sie den Bereich sowohl dem Parameter ``scopes`` als auch dem Delegierungseintrag hinzu. Dies wird beim Start geprüft.
   * - Die indizierte URL ist jetzt ``webViewLink`` (der im Browser zu öffnende Link) statt des Download-Links
     - Führen Sie einen vollständigen erneuten Crawl durch, um die neuen URLs zu übernehmen.
   * - ``default_permissions`` ist jetzt ein Rückfallwert, keine Ergänzung
     - Ein Dokument mit auflösbarer ACL erhält nur diese ACL, nicht mehr die Vereinigung aus ACL und ``default_permissions``. Das Ergebnis ist strikt restriktiver.
   * - Eine reine Link-Freigabe vergibt keine Suchrolle mehr
     - Eine ``domain``- oder ``anyone``-Berechtigung mit ``allowFileDiscovery=false`` bedeutet "jeder, der über den Link verfügt"; Drive selbst macht solche Dateien ebenfalls nicht über die Suche auffindbar.
   * - Ein Dokument, dessen ACL nichts ergibt, wird übersprungen, statt ohne Rollen indiziert zu werden
     - Setzen Sie ``default_permissions``, um solche Dokumente weiterhin zu indizieren. Bisher waren sie für jeden Benutzer sichtbar, da eine leere Rollenliste den Berechtigungsfilter deaktiviert.
   * - ``fields`` hat nicht mehr den Standardwert ``*``, sondern eine explizite Feldliste
     - Ein Crawl-Skript, das ein ungewöhnliches Feld verwendet, liest jetzt null. Setzen Sie ``fields=*``, um die bisherige Projektion wiederherzustellen.
   * - Google Docs werden als Markdown statt als reiner Text exportiert, Google Tabellen als TSV statt als CSV
     - Der indizierte Text jedes Google-Dokuments enthält jetzt Markdown-Syntaxzeichen. Führen Sie einen vollständigen erneuten Crawl durch.
   * - ``refresh_token_interval`` wird ignoriert
     - Die Aktualisierung der Token übernimmt die Authentifizierungsbibliothek. Eine bestehende Konfiguration funktioniert weiter, und es wird eine Warnung protokolliert.
   * - Google Formulare und Google Sites werden nur mit ihren Metadaten indiziert
     - Für sie gibt es kein Exportformat in der Drive API. Bisher erzeugte jede dieser Dateien einen Crawl-Fehler.

Neue Funktionen
---------------

- ``crawl_target`` bestimmt, was gecrawlt wird: die Sicht des Dienstkontos selbst
  (``legacy``), jede freigegebene Ablage der Domain (``shared_drives``), die "Meine
  Ablage" jedes Verzeichnisbenutzers (``users``) oder beides (``both``). Siehe
  `Crawl-Ziel`_.
- Elemente in freigegebenen Ablagen erhalten jetzt die korrekte ACL. Siehe
  `Berechtigungen und Zugriffskontrolle`_.
- Inkrementelles Crawling über den Änderungs-Feed von Drive. Siehe
  `Inkrementelles Crawling`_.
- Ratenbegrenzung mit exponentiellem Backoff, der ``Retry-After`` berücksichtigt, sowie
  eine fehlschlagende freigegebene Ablage oder ein fehlschlagender Benutzer, die den
  gesamten Crawl nicht mehr abbrechen. Siehe `Ratenbegrenzung und Wiederholungen`_.
- ``proxy_username`` und ``proxy_password`` für einen Proxy mit Authentifizierung.

Unterstützte Dienste
====================

- Google Drive (Mein Drive, freigegebene Ablagen)
- Google Docs, Tabellen, Präsentationen, Zeichnungen, Apps Script
- Google Formulare und Google Sites (nur Metadaten; für sie gibt es kein Exportformat)

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Ein Google Cloud Platform-Projekt muss erstellt werden
3. Ein Dienstkonto muss erstellt und Anmeldedaten abgerufen werden
4. Domain-weite Delegierung für Google Workspace muss konfiguriert werden
5. Sofern nicht ``crawl_target=legacy`` verwendet wird, wird ein Google Workspace-Administratorkonto
   benötigt, dessen Identität übernommen wird

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
     - GoogleDriveDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com

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
   * - ``impersonate_user``
     - Bedingt
     - Das Google Workspace-Konto, dessen Identität über die Domain-weite Delegierung übernommen wird. Erforderlich, sofern nicht ``crawl_target=legacy`` gesetzt ist; ohne diesen Wert schlägt der Crawl beim Start fehl. ``shared_drives`` und ``both`` ermitteln die freigegebenen Ablagen mit Domain-Administratorzugriff, daher muss dieses Konto ein Domain-Administrator sein.
   * - ``crawl_target``
     - Nein
     - Was gecrawlt wird: ``legacy``, ``shared_drives``, ``users`` oder ``both``. Standard: ``shared_drives``. Siehe `Crawl-Ziel`_.
   * - ``scopes``
     - Nein
     - OAuth-Bereiche, kommagetrennt. Standard: ``https://www.googleapis.com/auth/drive.readonly``. ``crawl_target=users`` und ``crawl_target=both`` benötigen zusätzlich ``https://www.googleapis.com/auth/admin.directory.user.readonly``.
   * - ``user_query``
     - Nein
     - Admin SDK-``query``, mit der die von ``crawl_target=users`` und ``crawl_target=both`` ermittelten Benutzer eingegrenzt werden. Standard: nicht gesetzt (alle Benutzer des Kundenkontos).
   * - ``query``
     - Nein
     - Google Drive API-Suchabfragezeichenfolge. Wird nicht auf den Änderungs-Feed des inkrementellen Crawlings angewendet.
   * - ``corpora``
     - Nein
     - Zu durchsuchende Korpora. Standard: ``allDrives``. Wird nur von ``crawl_target=legacy`` ausgewertet und hat daher beim Standardziel keine Wirkung: ``shared_drives`` listet jede Ablage mit ``drive`` und ``users`` jede "Meine Ablage" mit ``user`` auf, beides fest vorgegeben.
   * - ``spaces``
     - Nein
     - Zu durchsuchende Bereiche (Google Drive API ``spaces``-Parameter, z.B. ``drive``, ``appDataFolder``). Standard: nicht gesetzt (API-Standard). Wird von ``crawl_target=legacy`` und ``users`` verwendet; bei ``shared_drives`` ignoriert.
   * - ``fields``
     - Nein
     - Von der Google Drive API anzufordernde Dateifelder. Standard ist **nicht** ``*``, sondern eine explizite Feldliste. Sie deckt jedes Feld ab, das der Skript-Kontext, die ACL-Auflösung, die Index-URL und der inkrementelle Crawl benötigen; ein Feld außerhalb dieser Liste liest im Crawl-Skript null. Setzen Sie ``fields=*``, um wie in früheren Versionen alle Felder anzufordern.
   * - ``default_permissions``
     - Nein
     - Berechtigungen, die verwendet werden, wenn die Drive-ACL eines Dokuments nichts ergibt (kommagetrennt, z.B. ``{role}drive-users``). Dies ist ein Rückfallwert, keine Ergänzung: Ein Dokument mit auflösbarer ACL erhält nur diese ACL.
   * - ``max_size``
     - Nein
     - Maximale Dateigröße (in Bytes) für die Indizierung. Standard: ``10000000`` (ca. 10MB)
   * - ``number_of_threads``
     - Nein
     - Anzahl der parallelen Verarbeitungs-Threads. Standard: ``1``
   * - ``incremental``
     - Nein
     - Ob über den Änderungs-Feed von Drive gecrawlt wird, statt alles aufzulisten. Standard: ``false``. Der Wert wird vor dem Start des Crawls direkt aus dem Parameterfeld der Datenspeicher-Konfiguration gelesen. Siehe `Inkrementelles Crawling`_.

Erweiterte Parameter
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Beschreibung
   * - ``domain_permission_format``
     - Rollenformat für eine Drive-Berechtigung des Typs ``domain``. ``{domain}`` wird durch den Domainnamen ersetzt. Standard: ``{group}{domain}``
   * - ``thread_pool_timeout_seconds``
     - Wie lange am Ende eines Crawls auf das Beenden der Worker-Threads gewartet wird (Sekunden). Standard: ``60``
   * - ``page_size``
     - Seitengröße für ``files.list`` und ``changes.list``. Standard: ``1000``; größere Werte werden auf ``1000`` begrenzt.
   * - ``permission_page_size``
     - Seitengröße für ``permissions.list`` und ``drives.list``. Standard: ``100``; größere Werte werden auf ``100`` begrenzt.
   * - ``max_cached_content_size``
     - Maximale Größe (in Bytes) des im Speicher gehaltenen Inhalts; größerer Inhalt wird in eine temporäre Datei ausgelagert. Standard: ``1048576`` (1MB).
   * - ``max_retries``
     - Maximale Anzahl von Wiederholungen bei einem durch Ratenbegrenzung oder vorübergehend fehlgeschlagenen Drive API-Aufruf. Standard: ``5``
   * - ``retry_initial_interval_ms``
     - Anfängliches Backoff-Intervall vor der ersten Wiederholung (Millisekunden). Standard: ``1000``
   * - ``max_backoff_ms``
     - Obergrenze für eine einzelne Wartezeit (Millisekunden). Standard: ``32000``
   * - ``read_timeout``
     - HTTP-Lese-Timeout (in Millisekunden). Standard: ``20000``
   * - ``connect_timeout``
     - HTTP-Verbindungs-Timeout (in Millisekunden). Standard: ``20000``
   * - ``proxy_host``
     - Hostname des Proxyservers. Der Proxy wird nur verwendet, wenn ``proxy_host`` und ``proxy_port`` beide gesetzt sind; einer allein bleibt wirkungslos.
   * - ``proxy_port``
     - Portnummer des Proxyservers. Siehe ``proxy_host``.
   * - ``proxy_username``
     - Benutzername für einen Proxy mit Authentifizierung. Ist er gesetzt, wird jeder Anfrage ein ``Proxy-Authorization``-Header hinzugefügt. Was damit authentifiziert wird und was nicht, steht unter `Einschränkungen`_.
   * - ``proxy_password``
     - Passwort für einen Proxy mit Authentifizierung
   * - ``ignore_folder``
     - Ob Ordner übersprungen werden sollen. Standard: ``true``
   * - ``ignore_error``
     - Ob die Verarbeitung bei Fehlern fortgesetzt werden soll. Standard: ``true``
   * - ``supported_mimetypes``
     - Zu indizierende MIME-Typen (regulärer Ausdruck, kommagetrennt). Standard: ``.*`` (alle Typen)
   * - ``include_pattern``
     - Regulärer Ausdruck für zu indizierende URLs
   * - ``exclude_pattern``
     - Regulärer Ausdruck für auszuschließende URLs
   * - ``refresh_token_interval``
     - Wird seit 15.9 ignoriert. Zugriffstoken werden von der Authentifizierungsbibliothek erneuert. Eine bestehende Einstellung funktioniert weiter, und es wird eine Warnung protokolliert.

.. note::

   ``private_key``, ``private_key_id``, ``client_email``, ``proxy_username`` und
   ``proxy_password`` werden aus dem Auswertungskontext des Skripts entfernt, sodass ein
   Crawl-Skript sie nicht indizieren kann und kein Suchergebnis sie preisgeben kann.

.. note::

   Bei aktiviertem inkrementellem Crawling schreibt der Konnektor ``start_page_tokens`` und
   ``crawl_signature`` in das Parameterfeld der Datenspeicher-Konfiguration zurück. Diese
   Werte werden vom Konnektor verwaltet und erscheinen neben den von Ihnen gesetzten
   Parametern; lassen Sie sie unverändert. Werden sie bearbeitet oder gelöscht, crawlt der
   nächste Lauf jeden Bereich vollständig.

Crawl-Ziel
----------

Ein Dienstkonto besitzt kein eigenes Drive und gehört keiner Google-Gruppe an. Ein Crawl,
der sich als das Dienstkonto selbst authentifiziert, erreicht daher nur die Dateien, die
ausdrücklich für die Adresse des Dienstkontos freigegeben wurden. ``crawl_target``
bestimmt deshalb, wessen Sicht auf Drive gecrawlt wird.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Wert
     - Beschreibung
   * - ``legacy``
     - Die Sicht des Dienstkontos selbst, wie in früheren Versionen. ``impersonate_user`` ist nicht erforderlich. Es werden nur die Dateien gefunden, die ausdrücklich für das Dienstkonto freigegeben sind.
   * - ``shared_drives``
     - Standard. Jede freigegebene Ablage der Domain wird ermittelt und einzeln durchlaufen.
   * - ``users``
     - Jeder Benutzer des Verzeichnisses wird über das Admin SDK ermittelt, und die "Meine Ablage" jedes Benutzers wird durch Übernahme seiner Identität durchlaufen.
   * - ``both``
     - ``shared_drives``, gefolgt von ``users``. Eine Datei, die in mehreren Bereichen erscheint, wird nur einmal indiziert.

Folgendes wird beim Start des Crawls geprüft; eine ungültige Kombination löst eine
``DataStoreException`` aus, statt zu laufen:

1. ``crawl_target`` muss ``legacy``, ``shared_drives``, ``users`` oder ``both`` sein.
2. ``impersonate_user`` muss gesetzt sein, sofern nicht ``crawl_target=legacy`` gilt.
3. ``scopes`` muss ``https://www.googleapis.com/auth/admin.directory.user.readonly``
   enthalten, wenn ``crawl_target`` ``users`` oder ``both`` ist.

.. note::

   ``shared_drives`` und ``both`` ermitteln die freigegebenen Ablagen mit
   Domain-Administratorzugriff, daher muss das unter ``impersonate_user`` genannte Konto
   ein Google Workspace-Domain-Administrator sein. Diese Auflistung bestimmt den gesamten
   Umfang des Crawls, sodass ein dauerhafter Fehler den Crawl abbricht, statt gemeldet und
   übersprungen zu werden: Ein Crawl, der keine einzige Ablage ermitteln konnte, ist nicht
   teilweise erfolgreich und darf nicht als erfolgreich gelten, während er nichts indiziert.

Inkrementelles Crawling
-----------------------

Mit ``incremental=true`` liest jeder Bereich -- eine freigegebene Ablage oder die Sicht
eines Benutzers, dessen Identität übernommen wird -- den Änderungs-Feed von Drive, statt
alles aufzulisten. Ein Bereich ohne gespeicherten Token wird vollständig aufgelistet, und
sein Änderungs-Feed wird für den nächsten Lauf verankert.

::

    crawl_target=shared_drives
    impersonate_user=admin@example.com
    incremental=true

.. warning::

   ``delete_old_docs`` wird bei jedem inkrementellen Lauf auf ``false`` erzwungen, und ein
   ausdrückliches ``delete_old_docs=true`` wird überschrieben statt berücksichtigt (es wird
   eine Warnung protokolliert). Das Entfernen veralteter Dokumente löscht jedes Dokument
   der Konfiguration, das der aktuelle Crawl nicht berührt hat, und setzt damit einen
   vollständigen Crawl voraus. Ein inkrementeller Lauf berührt nur die geänderten
   Dokumente, sodass dieser Vorgang den Rest des Index löschen würde.

   Um Dokumente zu entfernen, die aus Drive verschwunden sind, planen Sie eine separate
   Datenspeicher-Konfiguration mit ``incremental=false``.

Die Tokens werden nur gespeichert, wenn der Crawl abgeschlossen wurde und die
Worker-Threads beendet sind. Ein abgebrochener Crawl lässt die Tokens unverändert, und der
nächste Lauf liest dieselben Änderungen erneut.

Die Tokens werden ebenfalls verworfen und jeder Bereich vollständig gecrawlt, wenn sich
die Konfiguration geändert hat, die bestimmt, was ein Bereich liefert -- also eines von
``crawl_target``, ``impersonate_user``, ``user_query``, ``query``, ``corpora`` oder
``spaces``. Ein gespeicherter Token beschreibt nur den Bestand, über dem er genommen wurde;
ihn nach einer solchen Änderung fortzusetzen, würde eine dauerhafte Lücke im Index
hinterlassen.

Ratenbegrenzung und Wiederholungen
----------------------------------

Ein durch Ratenbegrenzung oder vorübergehend fehlgeschlagener Drive API-Aufruf wird mit
exponentiellem Backoff wiederholt, begrenzt durch ``max_retries``,
``retry_initial_interval_ms`` und ``max_backoff_ms``. Ein ``Retry-After``-Header hat
Vorrang vor der exponentiellen Wartezeit, wird aber durch ``max_backoff_ms`` begrenzt,
damit ein fehlerhafter Header den Crawl nicht stundenlang blockieren kann. Nur die
Sekundenform von ``Retry-After`` wird berücksichtigt; ein HTTP-Datum fällt auf die
exponentielle Wartezeit zurück.

``429``, ``500``, ``502``, ``503`` und ``504`` werden immer wiederholt. Ein ``403`` wird
nur wiederholt, wenn es sich um einen Fehler wegen Ratenbegrenzung handelt; jedes andere
``403`` ist ein Autorisierungsfehler, den eine Wiederholung nicht beheben kann, und wird
sofort gemeldet.

Eine Dateiauflistung, die nicht abgeschlossen werden konnte, bricht nicht mehr den gesamten
Crawl ab: Die übrigen freigegebenen Ablagen und Benutzer werden weiterhin gecrawlt, und der
Fehler wird im Crawler-Log und in der Liste der fehlgeschlagenen URLs in der
Administrationsoberfläche festgehalten.

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
     - URL der Datei. Dies ist ``webViewLink``; hat eine Datei keinen, wird stattdessen ``https://drive.google.com/open?id=<Datei-ID>`` verwendet.
   * - ``file.thumbnail_link``
     - Thumbnail-Link (kurze Gültigkeit)
   * - ``file.size``
     - Dateigröße (Bytes)
   * - ``file.roles``
     - Zugriffsberechtigungen

.. note::

   Nur die im Parameter ``fields`` aufgeführten Felder werden gefüllt. Ein nicht
   angefordertes Feld liest im Skript null. Setzen Sie ``fields=*``, um wie in früheren
   Versionen alle Felder anzufordern.

Weitere Details finden Sie unter `Google Drive Files API <https://developers.google.com/drive/api/v3/reference/files>`_.

Textextraktion nativer Google-Typen
-----------------------------------

Ein nativer Google-Typ kann nicht heruntergeladen, sondern muss exportiert werden. Das
Exportziel wird aus den Exportformaten gewählt, die die Drive API tatsächlich meldet, nicht
aus einer festen Tabelle, und ein Export ist auf 10MB begrenzt.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Typ
     - Exportiert als
   * - Google Docs
     - Markdown (``text/markdown``), ersatzweise reiner Text und dann HTML
   * - Google Tabellen
     - TSV (``text/tab-separated-values``), ersatzweise CSV
   * - Google Präsentationen
     - Reiner Text
   * - Google Zeichnungen
     - PNG. Es gibt keinen Text zu indizieren, daher werden nur die Metadaten indiziert.
   * - Apps Script
     - Das exportierte JSON-Paket, aus dem die Skriptquellen indiziert werden
   * - Google Formulare, Google Sites
     - Nicht exportierbar. Die Metadaten werden indiziert, und es wird kein Fehler gemeldet.

.. note::

   Da Google Docs jetzt als Markdown exportiert werden, enthält der indizierte Text jedes
   Google-Dokuments Markdown-Syntaxzeichen. Damit die Änderung bereits indizierte Dokumente
   erreicht, ist ein vollständiger erneuter Crawl erforderlich.

.. note::

   Die Exportziele werden einmal pro Crawl von der Drive API gelesen. Schlägt dieser Aufruf
   fehl, fällt der Konnektor auf die Konvertierungen zurück, die Drive schon immer
   unterstützt hat -- reiner Text für Google Docs und CSV für Google Tabellen -- und
   protokolliert eine Warnung.

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
3. Aktivieren Sie außerdem "Admin SDK API", wenn ``crawl_target`` ``users`` oder ``both`` ist

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

   Ist ``crawl_target`` gleich ``users`` oder ``both``, geben Sie beide Bereiche ein:

   ::

       https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

6. Klicken Sie auf "Autorisieren"

.. warning::

   Der Delegierungseintrag listet die Bereiche ausdrücklich auf, daher muss er beim
   Aktualisieren von einer früheren Version angepasst werden. Der Standardbereich wurde in
   15.9 von ``https://www.googleapis.com/auth/drive`` auf
   ``https://www.googleapis.com/auth/drive.readonly`` eingeschränkt, und die hier erteilten
   Bereiche müssen zum Parameter ``scopes`` der Datenspeicher-Konfiguration passen.

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

Alle freigegebenen Ablagen crawlen
----------------------------------

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com

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
    role=file.roles
    filename=file.name

Die "Meine Ablage" jedes Benutzers crawlen
------------------------------------------

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=users
    impersonate_user=admin@example.com
    scopes=https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/admin.directory.user.readonly

Um die Benutzer einzugrenzen, fügen Sie eine Admin SDK-Abfrage hinzu:

::

    user_query=orgUnitPath=/Sales

Das bisherige Verhalten beibehalten
-----------------------------------

``crawl_target=legacy`` behält den Durchlauf von vor 15.9 bei, bei dem nur die
ausdrücklich für das Dienstkonto freigegebenen Dateien gefunden werden.
``impersonate_user`` ist nicht erforderlich.

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=legacy

Crawlen mit Berechtigungen
--------------------------

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

``default_permissions`` wird nur für ein Dokument verwendet, dessen Drive-ACL nichts ergibt.

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

Der Crawl startet nicht
-----------------------

**Symptom**: Der Crawl endet sofort mit einer ``DataStoreException``

**Lösung**:

1. ``parameter 'crawl_target' must be one of ...``: Der Wert von ``crawl_target`` ist
   weder ``legacy`` noch ``shared_drives``, ``users`` oder ``both``.
2. ``parameter 'impersonate_user' is required when 'crawl_target' is not 'legacy'``:
   Setzen Sie ``impersonate_user`` auf ein Domain-Administratorkonto oder setzen Sie
   ``crawl_target=legacy``.
3. ``parameter 'scopes' must include 'https://www.googleapis.com/auth/admin.directory.user.readonly'``:
   Fügen Sie diesen Bereich zu ``scopes`` und zum Eintrag der Domain-weiten Delegierung hinzu.

Beim unveränderten Aktualisieren einer bestehenden Konfiguration ist dies das erwartete
Ergebnis. Siehe `Änderungen in 15.9`_.

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
5. Überprüfen Sie den OAuth-Bereich (``https://www.googleapis.com/auth/drive.readonly``,
   zusätzlich ``https://www.googleapis.com/auth/admin.directory.user.readonly`` bei
   ``crawl_target=users`` oder ``both``)

Fehler bei Domain-weiter Delegierung
------------------------------------

**Symptom**: ``Not Authorized to access this resource/api``

**Lösung**:

1. Überprüfen Sie die Genehmigung in der Google Workspace Admin-Konsole:

   - Ist die Client-ID korrekt registriert?
   - Sind die OAuth-Bereiche korrekt? Der Delegierungseintrag listet sie ausdrücklich auf,
     daher erfordert die in 15.9 eingeführte Einschränkung eine Anpassung.

2. Überprüfen Sie, ob die Domain-weite Delegierung beim Dienstkonto aktiviert ist
3. Überprüfen Sie, ob das unter ``impersonate_user`` genannte Konto ein
   Domain-Administrator ist, wenn ``crawl_target`` ``shared_drives`` oder ``both`` ist

Keine Dateien abrufbar
----------------------

**Symptom**: Crawling erfolgreich, aber 0 Dateien

**Zu überprüfen**:

1. Überprüfen Sie, ob ``crawl_target`` dem entspricht, was Sie beabsichtigen. Mit
   ``legacy`` werden nur die ausdrücklich für das Dienstkonto freigegebenen Dateien
   gefunden, da ein Dienstkonto kein eigenes Drive besitzt und keiner Gruppe angehört.
2. Überprüfen Sie, ob Dateien in Google Drive existieren
3. Überprüfen Sie, ob das Dienstkonto Leseberechtigung hat
4. Überprüfen Sie, ob die Domain-weite Delegierung korrekt konfiguriert ist
5. Überprüfen Sie, ob der Zugriff auf das Drive des Zielbenutzers möglich ist

Dokumente werden übersprungen
-----------------------------

**Symptom**: ``Skipped ... because no permission could be resolved`` im Crawler-Log

**Lösung**:

Die Drive-ACL des Dokuments ergab überhaupt keine Suchrolle, sodass es übersprungen statt
indiziert wurde. Ein Dokument ohne Rolle zu indizieren, deaktiviert den
|Fess|-Berechtigungsfilter für dieses Dokument und macht es für jeden Benutzer sichtbar --
deshalb wird es stattdessen übersprungen. Ein übersprungenes Dokument ist kein Crawl-Fehler
und erscheint daher nur im Crawler-Log, nicht in der Liste der fehlgeschlagenen URLs.

1. Setzen Sie ``default_permissions``, um solche Dokumente mit einer Rückfallberechtigung
   zu indizieren
2. Überprüfen Sie, ob das unter ``impersonate_user`` genannte Konto ein
   Domain-Administrator ist, damit die ACLs der freigegebenen Ablagen gelesen werden können
3. Prüfen Sie, ob das Dokument nur per Link freigegeben ist. Eine ``domain``- oder
   ``anyone``-Berechtigung mit ``allowFileDiscovery=false`` vergibt keine Suchrolle, da
   Drive selbst ein solches Dokument ebenfalls nicht über die Suche auffindbar macht.

API-Kontingentfehler
--------------------

**Symptom**: ``403 Rate Limit Exceeded`` oder ``429 Too Many Requests``

**Lösung**:

1. Ein solcher Fehler wird automatisch mit exponentiellem Backoff wiederholt. Erhöhen Sie
   ``max_retries`` oder ``max_backoff_ms``, wenn der Crawl weiterhin fehlschlägt.
2. Verringern Sie ``number_of_threads``, um die Anfragerate zu senken
3. Überprüfen Sie das Kontingent in der Google Cloud Platform
4. Verlängern Sie das Crawl-Intervall
5. Beantragen Sie bei Bedarf eine Kontingenterhöhung

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
   Mit ``crawl_target=shared_drives`` (dem Standard) werden die freigegebenen Ablagen mit
   Domain-Administratorzugriff ermittelt, sodass das Dienstkonto nicht Mitglied jeder
   einzelnen Ablage sein muss. Stattdessen muss ``impersonate_user`` einen
   Domain-Administrator benennen.

Mit ``crawl_target=legacy`` muss das Dienstkonto jeder freigegebenen Ablage hinzugefügt werden:

1. Öffnen Sie die freigegebene Ablage in Google Drive
2. Klicken Sie auf "Mitglieder verwalten"
3. Fügen Sie die E-Mail-Adresse des Dienstkontos hinzu
4. Setzen Sie die Berechtigungsstufe auf "Betrachter"

Bei großen Dateimengen
----------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

1. Aktivieren Sie ``incremental=true``, damit nur die Änderungen seit dem letzten Lauf
   gecrawlt werden
2. Teilen Sie freigegebene Ablagen und Benutzer auf getrennte Datenspeicher-Konfigurationen
   auf, statt ``crawl_target=both`` zu verwenden
3. Grenzen Sie den Umfang mit ``query``, ``user_query`` oder ``supported_mimetypes`` ein
4. Verteilen Sie die Last über Zeitplaneinstellungen
5. Passen Sie das Crawl-Intervall an

Berechtigungen und Zugriffskontrolle
====================================

Wie Drive-Berechtigungen zu Fess-Rollen werden
----------------------------------------------

Die ACL eines Dokuments wird in drei Stufen aufgelöst, damit die Anzahl zusätzlicher
API-Aufrufe proportional zur Anzahl der freigegebenen Ablagen bleibt und nicht zur Anzahl
der Dateien:

1. die in der Dateiauflistung enthaltenen Berechtigungen, die nichts zusätzlich kosten;
2. bei einem Element einer freigegebenen Ablage, für das die Drive API keine solchen
   Berechtigungen liefert, die ACL der freigegebenen Ablage selbst. Sie wird einmal pro
   Ablage mit Domain-Administratorzugriff abgerufen und zwischengespeichert;
3. bei einem Element mit eigenen zusätzlichen Berechtigungen diese Berechtigungen.

Jede Drive-Berechtigung wird zu einer |Fess|-Suchrolle:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Drive-Berechtigung
     - Suchrolle
   * - ``user``
     - Die Suchrolle der E-Mail-Adresse dieses Benutzers. Die Eigentümer der Datei werden immer auf diese Weise hinzugefügt.
   * - ``group``
     - Die Suchrolle der E-Mail-Adresse dieser Gruppe. Die Mitgliedschaft in Google-Gruppen wird nie aufgelöst; es wird erwartet, dass |Fess| sie auf Benutzerseite über SSO oder LDAP auflöst.
   * - ``domain``
     - ``domain_permission_format``, wobei ``{domain}`` durch den Domainnamen ersetzt wird. Standard: ``{group}{domain}``
   * - ``anyone``
     - Die Rolle ``guest``
   * - Eine der obigen mit ``allowFileDiscovery=false`` sowie eine gelöschte Berechtigung
     - Keine Rolle. Eine reine Link-Freigabe ist auch in Drive selbst nicht über die Suche auffindbar.

Ist das Ergebnis leer, wird stattdessen ``default_permissions`` verwendet -- als
Rückfallwert, nicht als Ergänzung. Ist auch ``default_permissions`` nicht gesetzt, wird das
Dokument übersprungen.

Google Drive-Freigabeberechtigungen abbilden
--------------------------------------------

Google Drive-Freigabeeinstellungen auf Fess-Berechtigungen abbilden:

Parameter:

::

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQE...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project-123456.iam.gserviceaccount.com
    crawl_target=shared_drives
    impersonate_user=admin@example.com
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

Einschränkungen
===============

- Das Signal "entfernt" von Drive umfasst neben einer Löschung auch den Verlust des
  Zugriffs. Mit ``crawl_target=users`` oder ``both`` führt der Entzug des Zugriffs eines
  Benutzers dazu, dass das Dokument aus dem Index entfernt wird, obwohl ein anderer
  Benutzer es weiterhin lesen kann. Es kehrt bei der nächsten Änderung dieser Datei oder
  beim nächsten vollständigen Crawl zurück.
- Fällt ein Bereich während eines inkrementellen Laufs auf einen vollständigen Crawl
  zurück, bleibt das Entfernen veralteter Dokumente weiterhin unterdrückt. Dokumente, die
  aus Drive gelöscht wurden, während ein Bereich nicht verankert war, bleiben daher im
  Index. Abhilfe schafft eine separate Konfiguration mit ``incremental=false``, deren
  vollständiger Crawl sie entfernt.
- Das Weitergeben einer Löschung setzt voraus, dass die indizierte URL die Drive-Datei-ID
  enthält, was für ``webViewLink`` und für die Ersatz-URL gilt. Bei einem Crawl-Skript, das
  ``url`` auf einen Wert ohne die Datei-ID umschreibt, werden Löschungen nicht weitergegeben.
- Der Änderungs-Feed wird nicht durch ``query`` gefiltert. Mit gesetztem ``query`` und
  ``incremental=true`` wird eine geänderte Datei auch dann indiziert, wenn sie der Abfrage
  nicht entspricht.
- ``crawl_target=both`` löst in einer großen Domain etwa
  ``2 + (Anzahl der freigegebenen Ablagen) + (Anzahl der Benutzer)`` Auflistungen aus. Die
  praktische Abhilfe besteht darin, freigegebene Ablagen und Benutzer auf getrennte
  Datenspeicher-Konfigurationen aufzuteilen.
- ``proxy_username`` und ``proxy_password`` werden als ``Proxy-Authorization``-Anfrageheader
  gesendet, der nur eine einfache HTTP-Anfrage authentifiziert. Der gesamte Google
  API-Verkehr läuft über HTTPS, und eine HTTPS-Verbindung über einen Proxy mit
  Authentifizierung wird durch einen ``CONNECT``-Austausch aufgebaut, den das JDK über
  ``java.net.Authenticator`` und nicht über einen Anfrageheader abwickelt. Eine solche
  Umgebung benötigt stattdessen die JVM-Option
  ``-Djdk.http.auth.tunneling.disabledSchemes=`` und einen ``Authenticator``.

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-microsoft365` - Microsoft 365-Konnektor
- :doc:`ds-box` - Box-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Google Drive API <https://developers.google.com/drive/api>`_
- `Google Cloud Platform <https://console.cloud.google.com/>`_
- `Google Workspace Admin <https://admin.google.com/>`_
