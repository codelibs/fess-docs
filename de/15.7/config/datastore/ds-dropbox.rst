==================================
Dropbox-Konnektor
==================================

Übersicht
=========

Der Dropbox-Konnektor bietet die Funktionalität, Dateien aus dem Dropbox-Cloud-Speicher abzurufen
und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-dropbox`` erforderlich.

Unterstützte Dienste
====================

- Dropbox (Dateispeicher)
- Dropbox Paper (Dokumente)

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Ein Dropbox-Entwicklerkonto und eine Anwendung müssen erstellt werden
3. Ein Zugriffstoken muss abgerufen werden

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins":

1. Laden Sie ``fess-ds-dropbox-X.X.X.jar`` von Maven Central herunter
2. Laden Sie es über die Plugin-Verwaltungsoberfläche hoch und installieren Sie es
3. Starten Sie |Fess| neu

Weitere Details finden Sie unter :doc:`../../admin/plugin-guide`.

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
     - Company Dropbox
   * - Handler-Name
     - DropboxDataStore oder DropboxPaperDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``access_token``
     - Ja
     - Zugriffstoken von Dropbox (in der App Console generiert)
   * - ``basic_plan``
     - Nein
     - Bei Einzelkonto auf ``true``, bei Teamkonto auf ``false`` setzen (Standard: ``false``)
   * - ``max_size``
     - Nein
     - Maximale Dateigröße für die Indizierung in Bytes (Standard: ``10000000``)
   * - ``number_of_threads``
     - Nein
     - Anzahl der Threads für das Crawling (Standard: ``1``)
   * - ``ignore_folder``
     - Nein
     - Ordner-Metadaten überspringen (Standard: ``true``)
   * - ``ignore_error``
     - Nein
     - Fehler bei der Inhaltsextraktion ignorieren (Standard: ``true``)
   * - ``supported_mimetypes``
     - Nein
     - Regex-Muster für erlaubte MIME-Typen, kommagetrennt (Standard: ``.*``)
   * - ``include_pattern``
     - Nein
     - URL-Muster für einzuschließendes Crawling
   * - ``exclude_pattern``
     - Nein
     - URL-Muster für auszuschließendes Crawling
   * - ``default_permissions``
     - Nein
     - Standardberechtigungen für indizierte Dokumente, kommagetrennt
   * - ``max_cached_content_size``
     - Nein
     - Maximale im Speicher gecachte Inhaltsgröße in Bytes. Inhalte, die diesen Wert überschreiten, werden in eine temporäre Datei geschrieben (Standard: ``1048576``)
   * - ``readInterval``
     - Nein
     - Wartezeit in Millisekunden zwischen der Verarbeitung einzelner Datensätze (Standard: ``0``)

Skript-Einstellungen
--------------------

Für Dropbox-Dateien
~~~~~~~~~~~~~~~~~~~

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Verfügbare Felder:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``file.url``
     - Vorschau-Link der Datei
   * - ``file.contents``
     - Textinhalt der Datei
   * - ``file.mimetype``
     - MIME-Typ der Datei
   * - ``file.filetype``
     - Dateityp
   * - ``file.name``
     - Dateiname
   * - ``file.path_display``
     - Pfad der Datei
   * - ``file.size``
     - Dateigröße (Bytes)
   * - ``file.client_modified``
     - Letztes Änderungsdatum auf Client-Seite
   * - ``file.server_modified``
     - Letztes Änderungsdatum auf Server-Seite
   * - ``file.roles``
     - Zugriffsberechtigungen der Datei
   * - ``file.id``
     - Dropbox-Datei-ID
   * - ``file.path_lower``
     - Dateipfad in Kleinbuchstaben
   * - ``file.parent_shared_folder_id``
     - ID des übergeordneten freigegebenen Ordners
   * - ``file.content_hash``
     - Inhaltshash
   * - ``file.rev``
     - Dateirevision

Für Dropbox Paper
~~~~~~~~~~~~~~~~~

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Verfügbare Felder:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``paper.url``
     - Vorschau-Link des Paper-Dokuments
   * - ``paper.contents``
     - Textinhalt des Paper-Dokuments
   * - ``paper.mimetype``
     - MIME-Typ
   * - ``paper.filetype``
     - Dateityp
   * - ``paper.title``
     - Titel des Paper-Dokuments
   * - ``paper.owner``
     - Eigentümer des Paper-Dokuments
   * - ``paper.roles``
     - Zugriffsberechtigungen des Dokuments
   * - ``paper.revision``
     - Revision des Paper-Dokuments

Dropbox-Authentifizierung konfigurieren
=======================================

Kontotyp und Zugriffstoken
---------------------------

Dieser Konnektor schaltet über den Parameter ``basic_plan`` zwischen zwei Betriebsmodi um.
Da die Art der zu erstellenden App und des Zugriffstokens unterschiedlich ist, überprüfen Sie dies zuerst.

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Modus
     - ``basic_plan``
     - Beschreibung
   * - Teamkonto (Standard)
     - ``false``
     - Für Dropbox Business (Team)-Konten. Erfordert ein Zugriffstoken mit Teamadministrator-Rechten und crawlt kontoübergreifend Dateien von Teammitgliedern und Teamordnern.
   * - Einzelkonto
     - ``true``
     - Für persönliche (Nicht-Team)-Konten. Verwendet ein reguläres Zugriffstoken mit Bereichseinschränkung und crawlt Dateien direkt aus diesem Konto.

.. note::
   Im Standardmodus (``basic_plan=false``) werden Team-Verwaltungs-APIs verwendet (Teammitglieder-Liste, dateizugriff pro Mitglied, Teamordner).
   Daher sind ein Dropbox Business-Konto und ein Token mit Teamadministrator-Rechten zwingend erforderlich. Wenn Sie ein Einzelkonto verwenden, setzen Sie unbedingt ``basic_plan=true``.

Schritte zum Abrufen des Zugriffstokens
----------------------------------------

1. App in der Dropbox App Console erstellen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Besuchen Sie https://www.dropbox.com/developers/apps:

1. Klicken Sie auf "Create app"
2. Wählen Sie als API-Typ "Scoped access"
3. Wählen Sie den Zugriffstyp (bei kontoübergreifendem Crawling wird "Full Dropbox" empfohlen)
4. Geben Sie den App-Namen ein und erstellen Sie sie

2. Berechtigungen konfigurieren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Wählen Sie im Tab "Permissions" die erforderlichen Berechtigungen aus:

**Erforderliche Berechtigungen für das Crawlen von Dateien und Paper**:

- ``files.metadata.read`` - Lesen von Datei-Metadaten
- ``files.content.read`` - Lesen von Datei- und Paper-Dokumentinhalten
- ``sharing.read`` - Lesen von Freigabeinformationen

**Zusätzlich erforderliche Berechtigungen für Teamkonten (``basic_plan=false``)**:

- ``members.read`` - Lesen der Teammitgliederliste
- Zugriffsberechtigungen für Teamdaten/Teamspaces (erforderlich für das Crawling von Dateien einzelner Mitglieder und Teamordnern)

.. note::
   Im Teamkontomodus erfolgt der Zugriff auf einzelne Mitglieder und Teamordner als Teamadministrator.
   Aktivieren Sie die oben genannten teambezogenen Berechtigungen im Tab "Permissions" und generieren Sie ein Token mit Teamadministrator-Rechten.

3. Zugriffstoken generieren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Im Tab "Settings":

1. Scrollen Sie zum Abschnitt "Generated access token"
2. Klicken Sie auf die Schaltfläche "Generate"
3. Kopieren Sie das generierte Token (dieses Token wird nur einmal angezeigt)

.. warning::
   Bewahren Sie das Zugriffstoken sicher auf. Mit diesem Token kann auf das Dropbox-Konto zugegriffen werden.

4. Token konfigurieren
~~~~~~~~~~~~~~~~~~~~~~~

Setzen Sie das abgerufene Token in den Parametern:

::

    access_token=sl.your-dropbox-token-here

Einzelkonto-Einstellungen
=========================

Nutzung mit Einzelkonten
------------------------

Bei einem Einzelkonto (kein Teamkonto)
setzen Sie den Parameter ``basic_plan`` auf ``true``:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=true

Bei ``false`` (Standard) wird als Teamkonto gearbeitet und Dateien von Teammitgliedern und Teamordnern gecrawlt.
Bei ``true`` wird als Einzelkonto gearbeitet und Dateien direkt aus dem Konto gecrawlt.

Anwendungsbeispiele
===================

Alle Dropbox-Dateien crawlen
----------------------------

Parameter:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Skript:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified

Dropbox Paper-Dokumente crawlen
--------------------------------

Parameter:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false

Skript:

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype

Crawlen mit Berechtigungen
--------------------------

Parameter:

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    default_permissions={role}admin

Skript (Dropbox-Dateien):

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    content_length=file.size
    last_modified=file.client_modified
    role=file.roles

Skript (Dropbox Paper):

::

    title=paper.title
    content=paper.contents
    url=paper.url
    mimetype=paper.mimetype
    filetype=paper.filetype
    role=paper.roles

Nur bestimmte Dateitypen crawlen
---------------------------------

Um nur bestimmte MIME-Typen zu indizieren, geben Sie im Parameter ``supported_mimetypes``
die zulässigen MIME-Typen als kommagetrennte Regex-Ausdrücke an.

.. note::
   Skripte im Datenspeicher werden zeilenweise als eigenständige Ausdrücke der Form ``Feldname=Ausdruck`` ausgewertet.
   Daher ist es nicht möglich, mit einem mehrzeiligen ``if``-Block mehrere Felder gemeinsam zuzuweisen.
   Die Einschränkung nach MIME-Typ sollte über den Parameter ``supported_mimetypes`` und nicht über das Skript erfolgen.

Parameter (nur PDF- und Word-Dateien):

::

    access_token=sl.your-dropbox-token-here
    basic_plan=false
    supported_mimetypes=application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document

Skript:

::

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

Fehlerbehebung
==============

Authentifizierungsfehler
------------------------

**Symptom**: ``Invalid access token`` oder ``401 Unauthorized``

**Zu überprüfen**:

1. Überprüfen Sie, ob das Zugriffstoken korrekt kopiert wurde
2. Überprüfen Sie, ob das Token nicht abgelaufen ist (verwenden Sie ein langfristiges Token)
3. Überprüfen Sie, ob die erforderlichen Berechtigungen in der Dropbox App Console erteilt wurden
4. Überprüfen Sie, ob die App nicht deaktiviert wurde

Keine Dateien abrufbar
----------------------

**Symptom**: Crawling erfolgreich, aber 0 Dateien

**Zu überprüfen**:

1. Überprüfen Sie, ob der "Access type" der App korrekt ist:

   - "Full Dropbox": Zugriff auf gesamte Dropbox
   - "App folder": Zugriff nur auf bestimmten Ordner

2. Überprüfen Sie, ob die erforderlichen Berechtigungen erteilt wurden:

   - ``files.metadata.read``
   - ``files.content.read``
   - ``sharing.read``

3. Überprüfen Sie, ob Dateien im Dropbox-Konto existieren

API-Ratenbegrenzungsfehler
--------------------------

**Symptom**: ``429 Too Many Requests`` Fehler

**Lösung**:

1. ``readInterval`` setzen, um die Verarbeitungspause zwischen Dateien zu verlängern
2. ``number_of_threads`` verringern, um die Anzahl gleichzeitiger Anfragen zu reduzieren
3. Datenspeicher in mehrere aufteilen (z.B. nach Ordner) und die Ausführungszeiten versetzt planen

.. note::
   ``basic_plan`` ist ein Parameter zur Auswahl des Kontotyps (Team/Einzelkonto) und hat keinen Einfluss auf die Ratenbegrenzung. Setzen Sie ihn entsprechend Ihrem Konto korrekt.

Paper-Dokumente werden nicht abgerufen
--------------------------------------

**Symptom**: Paper-Dokumente werden nicht gecrawlt

**Zu überprüfen**:

1. Überprüfen Sie, ob der Handler-Name ``DropboxPaperDataStore`` ist
2. Überprüfen Sie, ob ``files.content.read`` in den Berechtigungen enthalten ist
3. Überprüfen Sie, ob Paper-Dokumente tatsächlich existieren

Bei großen Dateimengen
----------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

1. Datenspeicher in mehrere aufteilen (z.B. nach Ordner)
2. Last über Zeitplaneinstellungen verteilen
3. Bei Basic-Plan auf API-Ratenbegrenzung achten

Berechtigungen und Zugriffskontrolle
=====================================

Dropbox-Freigabeberechtigungen abbilden
-----------------------------------------

Dropbox-Freigabeeinstellungen können auf Fess-Berechtigungen abgebildet werden:

Parameter:

::

    access_token=sl.your-dropbox-token-here
    default_permissions={role}dropbox-users

Skript:

::

    url=file.url
    title=file.name
    content=file.contents
    role=file.roles
    mimetype=file.mimetype
    filename=file.name
    last_modified=file.client_modified

``file.roles`` oder ``paper.roles`` enthält die Dropbox-Freigabeinformationen.

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-box` - Box-Konnektor
- :doc:`ds-gsuite` - Google Workspace-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Dropbox Developers <https://www.dropbox.com/developers>`_
- `Dropbox API Documentation <https://www.dropbox.com/developers/documentation>`_
