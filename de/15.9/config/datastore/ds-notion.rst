==================================
Notion-Konnektor
==================================

Übersicht
=========

Der Notion-Konnektor bietet die Funktionalität, Seiten und Datenbankzeilen aus Notion abzurufen
und im |Fess|-Index zu registrieren.
Er authentifiziert sich als interne Notion-Integration und indexiert alles, was für diese Integration freigegeben wurde.

Für diese Funktion ist das Plugin ``fess-ds-notion`` erforderlich.

Unterstützte Inhalte
====================

- Seiten (der Text ihrer Blöcke)
- Datenbankzeilen samt ihren Eigenschaftswerten
- In Notion gehostete Dateianhänge von Datei- und PDF-Blöcken (jeweils als eigenes Dokument indexiert)
- Ungelöste Seitenkommentare (in das Dokument der Seite aufgenommen)

Nicht unterstützt werden:

- Dateien, auf die in Notion nur verwiesen wird (externe Dateien); heruntergeladen werden nur in Notion gehostete ``file``- und ``pdf``-Blöcke
- Seiten und Datenbankzeilen im Papierkorb von Notion
- Zugriffskontrolle pro Seite (siehe „Berechtigungen“ weiter unten)

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Eine interne Notion-Integration muss erstellt werden
3. Die Integration muss für die zu crawlenden Seiten und Datenbanken freigegeben werden

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins" oder führen Sie ``bin/fess-setup install plugin fess-ds-notion`` aus
und starten Sie |Fess| neu.
Weitere Details finden Sie unter :doc:`../../admin/plugin-guide`.

Einrichtung der Notion-Integration
----------------------------------

1. Erstellen Sie in Notion eine interne Integration und kopieren Sie das „Internal Integration Secret“.
2. Aktivieren Sie auf der Seite „Configuration“ der Integration die folgenden Fähigkeiten:

   .. list-table::
      :header-rows: 1
      :widths: 25 25 50

      * - Fähigkeit
        - Erforderlich
        - Verwendung
      * - Read content
        - Immer
        - Lesen von Seiten, Blöcken, Datenbanken und Datenbankzeilen. Ohne sie schlägt jede Anfrage mit ``401 unauthorized`` fehl und der Crawl wird sofort abgebrochen
      * - Read comments
        - Nur bei ``include_comments=true`` (Standard)
        - Abrufen der Seitenkommentare. Fehlt die Fähigkeit, wird einmal eine Warnung protokolliert und das Crawlen von Kommentaren für den Rest dieses Crawls deaktiviert; der Crawl selbst schlägt nicht fehl
      * - Read user information
        - Optional
        - Auflösen von Benutzer-IDs (``created_by``, ``last_edited_by`` und ``people``-Eigenschaften) in Anzeigenamen. Ohne sie wird statt des Namens die Benutzer-ID indexiert

3. Geben Sie die Integration in Notion für jede Seite oder Datenbank frei, die gecrawlt werden soll.
   Das Hinzufügen einer Fähigkeit allein gewährt keinen Zugriff auf Inhalte.

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
     - Company Notion
   * - Handler-Name
     - NotionDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    token=secret_************************************

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``token``
     - Ja
     - Das Internal Integration Secret. Es wird nicht an das Skript übergeben und nicht protokolliert
   * - ``root_page_ids``
     - Nein
     - Kommagetrennte IDs der Seiten, von denen aus gecrawlt wird. Sind dieser Parameter und ``database_ids`` beide leer, werden alle für die Integration freigegebenen Seiten und Datenbanken über die Suche von Notion ermittelt
   * - ``database_ids``
     - Nein
     - Kommagetrennte IDs der Datenbanken, von denen aus gecrawlt wird. Jede Zeile jeder Datenbank wird indexiert
   * - ``include_comments``
     - Nein
     - Ungelöste Kommentare jeder Seite abrufen und deren Text in ``notion.content`` und ``notion.comments`` aufnehmen (Standard: ``true``)
   * - ``include_files``
     - Nein
     - In Notion gehostete Anhänge von ``file``- und ``pdf``-Blöcken herunterladen, ihren Text extrahieren und jeden als eigenes Dokument indexieren (Standard: ``true``)
   * - ``max_file_size``
     - Nein
     - Ein Anhang, der größer als diese Anzahl Bytes ist, wird vollständig übersprungen und auch nicht mit leerem Inhalt indexiert (Standard: ``10485760``)
   * - ``include_pattern``
     - Nein
     - Regulärer Ausdruck, dem die ``notion.url`` eines Dokuments entsprechen muss, damit es indexiert wird (siehe „Crawl-Umfang“)
   * - ``exclude_pattern``
     - Nein
     - Regulärer Ausdruck, dem die ``notion.url`` eines Dokuments nicht entsprechen darf (siehe „Crawl-Umfang“)
   * - ``request_interval``
     - Nein
     - Millisekunden Wartezeit vor jeder Notion-API-Anfrage, um unter dem Ratenlimit von Notion (etwa 3 Anfragen pro Sekunde) zu bleiben (Standard: ``350``)
   * - ``max_retry_count``
     - Nein
     - Maximale Anzahl von Wiederholungen für eine Anfrage, die mit ``429``, ``5xx`` oder ``529`` oder mit einem Übertragungsfehler wie einem Timeout endet (Standard: ``5``)
   * - ``connection_timeout``
     - Nein
     - Verbindungs-Timeout jeder API-Anfrage in Millisekunden (Standard: ``10000``)
   * - ``read_timeout``
     - Nein
     - Lese-Timeout jeder API-Anfrage in Millisekunden (Standard: ``30000``)
   * - ``ignore_error``
     - Nein
     - Schlägt die Textextraktion bei einem heruntergeladenen Anhang fehl, wird der Anhang mit leerem Inhalt indexiert, statt das Dokument fehlschlagen zu lassen (Standard: ``true``). Ein fehlgeschlagener Download lässt das Dokument unabhängig von dieser Einstellung immer fehlschlagen

.. note::

   Bei einem numerischen Parameter fällt ein leerer oder nicht numerischer Wert mit einer Warnung im Log auf den Standardwert zurück.
   Dasselbe gilt für ein negatives ``request_interval`` oder ``max_retry_count`` (``0`` ist für beide gültig) und für einen
   ``true``/``false``-Parameter, der auf einen anderen Wert gesetzt wurde.

Skript-Einstellungen
--------------------

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time
    created=notion.created_time

Verfügbare Felder
~~~~~~~~~~~~~~~~~

Jedes Dokument, ob Seite, Datenbankzeile oder Anhang, steht dem Skript unter dem Objekt ``notion`` zur Verfügung.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``notion.type``
     - ``page`` für eine Seite oder Datenbankzeile, ``file`` für einen Anhang
   * - ``notion.id``
     - Die Seiten-ID, bei einem Anhang die Block-ID
   * - ``notion.title``
     - Der Seitentitel (die Eigenschaft vom Typ ``title``, unabhängig von ihrem Namen) oder der Dateiname eines Anhangs
   * - ``notion.content``
     - Bei einer Seite: die Eigenschaftswerte außer dem Titel (nur Datenbankzeilen), der Text der Blöcke und der Kommentartext, zusammengefügt. Bei einem Anhang: der extrahierte Text
   * - ``notion.url``
     - Die Notion-URL der Seite. Bei einem Anhang die URL der enthaltenden Seite mit angehängtem ``#<Block-ID>``
   * - ``notion.mimetype``
     - ``text/html`` für eine Seite, der erkannte MIME-Typ für einen Anhang
   * - ``notion.created_time``
     - Erstellungszeitpunkt der Seite. Für einen Anhang nicht verfügbar
   * - ``notion.last_edited_time``
     - Zeitpunkt der letzten Bearbeitung der Seite bzw. des Anhangsblocks
   * - ``notion.created_by``
     - Ersteller der Seite: der Name, falls Notion einen geliefert hat, sonst die Benutzer-ID. Für einen Anhang nicht verfügbar
   * - ``notion.last_edited_by``
     - Letzter Bearbeiter im selben Format. Für einen Anhang nicht verfügbar
   * - ``notion.parent_id``
     - ID der übergeordneten Seite, Datenbank, Datenquelle oder des Blocks. Leer bei einer Seite direkt im Workspace. Für einen Anhang nicht verfügbar
   * - ``notion.properties``
     - Zuordnung von Datenbankspaltenname zu formatiertem Text für eine Datenbankzeile. Bei einer normalen Seite leer. Für einen Anhang nicht verfügbar
   * - ``notion.comments``
     - Der Kommentartext der Seite, zusammengefügt. Leer bei ``include_comments=false`` oder wenn die Seite keine Kommentare hat. Für einen Anhang nicht verfügbar
   * - ``notion.page_url``
     - URL der enthaltenden Seite. Nur bei Anhängen
   * - ``notion.page_title``
     - Titel der enthaltenden Seite. Nur bei Anhängen
   * - ``notion.size``
     - Größe des Anhangs in Bytes, sofern Notion sie geliefert hat. Nur bei Anhängen

Crawl-Umfang
============

- Ist weder ``root_page_ids`` noch ``database_ids`` gesetzt, ermittelt der Konnektor über die Suche von Notion alle für die Integration freigegebenen Seiten und Datenbanken.
  Notion garantiert nicht, dass die Suche vollständig ist; fehlen Inhalte im Index, setzen Sie ``root_page_ids`` oder ``database_ids`` explizit.
- Von jedem Ausgangspunkt aus werden auch alle erreichbaren Unterseiten und Unterdatenbanken gecrawlt, sodass meist eine einzige Stammseite genügt, um einen ganzen Bereich eines Workspace zu erreichen.
- ``include_pattern`` und ``exclude_pattern`` entscheiden nur darüber, ob das Dokument dieser Seite (oder dieses Anhangs) indexiert wird.
  Sie verhindern nie, dass die Nachfolger entdeckt werden: Die Blöcke einer Seite werden immer durchlaufen, bevor das Muster gegen die eigene URL der Seite geprüft wird,
  sodass auch die Unterseiten einer ausgeschlossenen Seite weiterhin gecrawlt und unter ihren eigenen URLs indexiert werden.
  Um einen ganzen Teilbaum auszuschließen, muss das Muster auf jede URL darunter passen, nicht nur auf die Wurzel.
- Eine Seite oder Datenbankzeile im Papierkorb von Notion wird übersprungen.

Berechtigungen
==============

Die Notion-API stellt die Freigabeeinstellungen einer Seite nicht bereit, daher kann dieser Konnektor die Zugriffskontrolle pro Seite nicht synchronisieren.
Jedes Dokument wird nur mit den Berechtigungen indexiert, die im Feld „Berechtigungen“ der Datenspeicher-Konfiguration festgelegt sind.

.. warning::

   Alles, was für die Integration freigegeben ist, kann von den Rollen durchsucht werden, die in diesem Feld gewährt werden, unabhängig davon, wer es in Notion sehen kann.
   Geben Sie die Integration nur für die Seiten und Datenbanken frei, die diese Rollen durchsuchen dürfen.

Fehlerbehandlung
================

- Der Crawl wird nur bei HTTP ``401`` (das Token kann sich nicht authentifizieren) oder bei einer ``429``-Antwort mit ``public_api_request_blocked`` (das Ratenlimit von Notion blockiert die Integration) abgebrochen.
  Der Crawl wird auch abgebrochen, wenn die Suche von Notion fehlschlägt, während weder ``root_page_ids`` noch ``database_ids`` gesetzt ist, da es keinen Ausgangspunkt gibt.
- Jeder andere Fehler wird pro Dokument behandelt: ein ``404`` oder ``403`` für eine Seite, Datenbank, einen Kommentar-Thread oder Block oder das Erschöpfen von ``max_retry_count`` bei einer Anfrage wird protokolliert und übersprungen, der Crawl läuft weiter.
- Jeder Fehler pro Dokument wird unter "Crawler" -> "Fehler-URLs" mit der URL dieses Dokuments aufgezeichnet (die Notion-URL einer Seite, ``<Seiten-URL>#<Block-ID>`` bei einem Anhang).
  Die signierte Download-URL eines Anhangs wird weder aufgezeichnet noch protokolliert.
- Mit ``keep_expires_docs=false`` in den Parametern werden Dokumente des Datenspeichers, die in einem Crawl nicht erneut indexiert wurden, am Ende des Crawls gelöscht; das gilt auch für einen abgebrochenen Crawl.
  Standardmäßig tragen die Dokumente ein Ablaufdatum und bleiben bis zu dessen Ablauf im Index.

Anwendungsbeispiele
===================

Einen bestimmten Seitenbaum crawlen
-----------------------------------

Parameter:

::

    token=secret_************************************
    root_page_ids=0123456789abcdef0123456789abcdef
    include_comments=false

Skript:

::

    title=notion.title
    content=notion.content
    url=notion.url
    mimetype=notion.mimetype
    last_modified=notion.last_edited_time

Eine Datenbank crawlen
----------------------

Parameter:

::

    token=secret_************************************
    database_ids=fedcba9876543210fedcba9876543210
    include_files=false

Skript:

::

    title=notion.title
    content=notion.content
    url=notion.url
    created=notion.created_time
    last_modified=notion.last_edited_time

Alles crawlen, was für die Integration freigegeben ist
------------------------------------------------------

Parameter:

::

    token=secret_************************************
    request_interval=500

Fehlerbehebung
==============

Der Crawl wird sofort mit ``401`` abgebrochen
---------------------------------------------

Prüfen Sie, ob das Token das „Internal Integration Secret“ der Integration ist und die Fähigkeit „Read content“ aktiviert ist.

Seiten fehlen im Index
----------------------

1. Prüfen Sie, ob die Integration für die Seite oder Datenbank freigegeben wurde
2. Wenn Sie sich auf die automatische Ermittlung verlassen, setzen Sie ``root_page_ids`` oder ``database_ids`` explizit, da die Suche von Notion nicht garantiert vollständig ist
3. Prüfen Sie ``include_pattern`` und ``exclude_pattern``
4. Prüfen Sie unter "Crawler" -> "Fehler-URLs" auf Dokumente, die einzeln fehlgeschlagen sind

Kommentare werden nicht indexiert
---------------------------------

Aktivieren Sie die Fähigkeit „Read comments“ der Integration. Ohne sie wird einmal eine Warnung protokolliert und Kommentare werden für diesen Crawl übersprungen.
Es werden nur ungelöste Kommentare indexiert.

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-slack` - Slack-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../../admin/failureurl-guide` - Fehler-URLs
- :doc:`../../admin/plugin-guide` - Leitfaden zur Plugin-Verwaltung
- `Notion API Documentation <https://developers.notion.com/>`_
