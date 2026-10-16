==================================
Backlog-Konnektor
==================================

Übersicht
=========

Der Backlog-Konnektor bietet die Funktionalität, Vorgänge, Wiki-Seiten, Dokumente und Dateien aus einem Backlog-Space abzurufen
und im |Fess|-Index zu registrieren.
Er authentifiziert sich mit einem API-Schlüssel am Space.
Jedes indexierte Dokument ist auf die Mitglieder des zugehörigen Backlog-Projekts beschränkt (siehe „Berechtigungen“ weiter unten).

Für diese Funktion ist das Plugin ``fess-ds-backlog`` erforderlich.

Unterstützte Inhalte
====================

- Vorgänge (mit ihren Kommentaren)
- Wiki-Seiten
- Dokumente
- Anhänge von Vorgängen, Wiki-Seiten und Dokumenten
- Freigegebene Dateien eines Projekts

Jeder Crawl ist ein vollständiger Crawl. Standardmäßig werden Dokumente, die aus Backlog verschwunden sind, am Ende des Crawls nicht gelöscht;
sie werden entfernt, wenn sie ablaufen (siehe „Gelöschte Inhalte und entzogener Zugriff“).

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Ein dedizierter Backlog-Benutzer und sein API-Schlüssel sind erforderlich
3. Der Benutzer muss Mitglied jedes zu crawlenden Projekts sein

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins" oder führen Sie ``bin/fess-setup install plugin fess-ds-backlog`` aus
und starten Sie |Fess| neu.
Weitere Details finden Sie unter :doc:`../../admin/plugin-guide`.

Einrichtung in Backlog
----------------------

1. Erstellen Sie einen dedizierten Backlog-Benutzer für das Crawlen und stellen Sie dafür einen API-Schlüssel aus („Persönliche Einstellungen“ -> „API“).
   Der Crawl sieht genau das, was dieser Benutzer sieht.
2. Fügen Sie den Benutzer zu jedem zu crawlenden Projekt hinzu. Der Konnektor fragt keine Projekte ab, denen der Benutzer nicht beigetreten ist,
   auch wenn der Benutzer Space-Administrator ist.
3. Weisen Sie dem Benutzer eine Rolle ohne Einschränkungen zu (Administrator oder Normaler Benutzer). Bei einer eingeschränkten Rolle
   antwortet Backlog bei einigen Funktionen mit HTTP 403: Ein Benutzer mit „Nur Ansicht“ kann keine Vorgangsanhänge herunterladen,
   und freigegebene Dateien können nur Benutzer ohne Einschränkungen herunterladen.
   Bei einem solchen 403 protokolliert der Konnektor pro Projekt und Funktion eine Warnung, überspringt diese Funktion für dieses Projekt
   (Vorgangsanhänge, Wiki-Anhänge, Dokumentanhänge oder freigegebene Dateien) und setzt den Rest fort.
4. Verlangt der Space eine Zwei-Faktor-Authentifizierung für den API-Zugriff, antwortet Backlog mit dem Fehlercode 12
   (RequiredMFAError) und der Crawl wird abgebrochen.

Der API-Schlüssel wird nur im Request-Header ``Backlog-API-Key`` gesendet. Er wird nicht an das Skript übergeben,
von diesem Konnektor nicht ins Log geschrieben, und HTTP-Weiterleitungen werden nicht verfolgt, sodass der Schlüssel den Space-Host nie verlässt.

.. warning::

   Aktivieren Sie kein ``FINE``-Logging für den Logger ``org.codelibs.curl``. Der HTTP-Client protokolliert auf dieser Stufe Request-Header
   und maskiert nur Header im Stil von ``Authorization`` und ``Cookie``, sodass der Header ``Backlog-API-Key`` ins Log geschrieben würde.

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
     - Company Backlog
   * - Handler-Name
     - BacklogDataStore
   * - Berechtigungen
     - (leer lassen; siehe „Berechtigungen“)
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    api_key=**********************************************
    space_url=https://example.backlog.com

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``api_key``
     - Ja
     - Der Backlog-API-Schlüssel. Er wird nicht an das Skript übergeben und nicht protokolliert
   * - ``space_url``
     - Ja
     - Die URL des Space, zum Beispiel ``https://example.backlog.com``. Nur ``https`` wird akzeptiert, und es dürfen nur Schema und Host angegeben werden (ein abschließender Schrägstrich wird ignoriert). Ein fehlender, fehlerhafter oder ``http``-Wert bricht den Crawl ab
   * - ``project_keys``
     - Nein
     - Kommagetrennte Projektschlüssel, die gecrawlt werden (Groß-/Kleinschreibung wird nicht unterschieden). Ist der Parameter leer, werden alle Projekte gecrawlt, die der Benutzer sehen kann. Ein Schlüssel, den der Benutzer nicht sehen kann, wird als Warnung protokolliert
   * - ``include_archived``
     - Nein
     - Auch archivierte Projekte crawlen (Standard: ``false``)
   * - ``include_issues``
     - Nein
     - Vorgänge indexieren (Standard: ``true``)
   * - ``include_comments``
     - Nein
     - Vorgangskommentare in das Vorgangsdokument aufnehmen (Standard: ``true``)
   * - ``include_wikis``
     - Nein
     - Wiki-Seiten in Projekten indexieren, in denen das Wiki aktiviert ist (Standard: ``true``)
   * - ``include_documents``
     - Nein
     - Dokumente in Projekten indexieren, in denen Dokumente aktiviert sind (Standard: ``true``)
   * - ``include_attachments``
     - Nein
     - Anhänge von Vorgängen, Wiki-Seiten und Dokumenten herunterladen und indexieren (Standard: ``true``)
   * - ``include_shared_files``
     - Nein
     - Freigegebene Dateien in Projekten herunterladen und indexieren, in denen die Dateifreigabe aktiviert ist (Standard: ``true``)
   * - ``permission_sync``
     - Nein
     - Jedem Dokument eines Projekts pro Projektmitglied eine ``{user}``-Rolle geben (Standard: ``true``). Siehe „Berechtigungen“
   * - ``default_permissions``
     - Nein
     - Kommagetrennte Berechtigungen (``{user}name``, ``{group}name`` oder ``{role}name``), die jedem Dokument hinzugefügt werden
   * - ``max_file_size``
     - Nein
     - Dateien, die größer als diese Anzahl Bytes sind, werden übersprungen und nicht indexiert (Standard: ``10485760``)
   * - ``include_pattern``
     - Nein
     - Regulärer Ausdruck, dem ``backlog.url`` entsprechen muss, damit indexiert wird
   * - ``exclude_pattern``
     - Nein
     - Regulärer Ausdruck, dem ``backlog.url`` nicht entsprechen darf. Wird ein Vorgang, eine Wiki-Seite oder ein Dokument ausgefiltert, werden auch seine Anhänge übersprungen
   * - ``request_interval``
     - Nein
     - Millisekunden Wartezeit vor jeder API-Anfrage (Standard: ``200``)
   * - ``search_request_interval``
     - Nein
     - Minimaler Abstand in Millisekunden zwischen zwei Anfragen vom Typ Suche (Vorgangsliste, Wiki-Liste). Backlog bittet Clients, mindestens eine Sekunde Abstand zu halten (Standard: ``1000``)
   * - ``max_retry_count``
     - Nein
     - Anzahl der Wiederholungen bei HTTP 429, 5xx und Verbindungsfehlern (Standard: ``5``)
   * - ``connection_timeout``
     - Nein
     - Verbindungs-Timeout in Millisekunden (Standard: ``10000``)
   * - ``read_timeout``
     - Nein
     - Lese-Timeout in Millisekunden (Standard: ``30000``)
   * - ``ignore_error``
     - Nein
     - Schlägt die Textextraktion einer heruntergeladenen Datei fehl, wird die Datei mit leerem Inhalt indexiert, statt einen Fehler aufzuzeichnen (Standard: ``true``)

.. note::

   Ein ungültiger Wert (eine Nichtzahl, ein negatives Intervall oder eine negative Wiederholungsanzahl, ein nicht positives Timeout oder ``max_file_size``
   oder ein anderer Wahrheitswert als ``true``/``false``) wird als Warnung protokolliert und der Standardwert verwendet.
   ``0`` ist für ``request_interval``, ``search_request_interval`` und ``max_retry_count`` gültig.

Skript-Einstellungen
--------------------

::

    title=backlog.title
    content=backlog.content
    url=backlog.url
    mimetype=backlog.mimetype
    created=backlog.created
    last_modified=backlog.updated
    role=backlog.roles

.. important::

   ``role=backlog.roles`` ist erforderlich, damit die Beschränkung auf Projektmitglieder wirksam wird.
   Ohne diese Zeile gelangt nur das Feld „Berechtigungen“ der Datenspeicher-Konfiguration in den Index.

Verfügbare Felder
~~~~~~~~~~~~~~~~~

Jedes Dokument steht dem Skript unter dem Objekt ``backlog`` zur Verfügung.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Feld
     - Typen
     - Beschreibung
   * - ``backlog.type``
     - alle
     - ``issue``, ``wiki``, ``document``, ``attachment`` oder ``file``
   * - ``backlog.id``
     - alle
     - Die Backlog-ID des Vorgangs, der Wiki-Seite, des Dokuments, des Anhangs oder der freigegebenen Datei
   * - ``backlog.project_key``, ``backlog.project_name``
     - alle
     - Das Projekt
   * - ``backlog.title``
     - alle
     - ``[KEY-1] Zusammenfassung`` bei einem Vorgang; sonst der Seitenname, der Dokumenttitel oder der Dateiname
   * - ``backlog.content``
     - alle
     - Vorgang: Beschreibung, Attribute, benutzerdefinierte Felder und Kommentare. Wiki-Seite: der Seiteninhalt. Dokument: Klartext. Anhang und Datei: der extrahierte Text
   * - ``backlog.url``
     - alle
     - Siehe „URLs“
   * - ``backlog.mimetype``
     - alle
     - ``text/plain`` für Vorgänge, Wiki-Seiten und Dokumente; der erkannte Typ bei Dateien
   * - ``backlog.created``, ``backlog.updated``
     - alle
     - Zeitstempel in ISO 8601 (UTC), sofern Backlog sie liefert
   * - ``backlog.created_by``, ``backlog.updated_by``
     - alle
     - Benutzernamen, sofern Backlog sie liefert
   * - ``backlog.roles``
     - alle
     - Die Suchrollen (siehe „Berechtigungen“)
   * - ``backlog.issue_key``, ``backlog.issue_type``, ``backlog.status``, ``backlog.priority``, ``backlog.assignee``
     - Vorgang
     - Vorgangsattribute (Namen)
   * - ``backlog.categories``, ``backlog.milestones``, ``backlog.versions``
     - Vorgang
     - Listen von Namen
   * - ``backlog.custom_fields``
     - Vorgang
     - Zuordnung von Name des benutzerdefinierten Felds zum Wertetext
   * - ``backlog.comments``
     - Vorgang
     - Kommentartext in der Form ``Autor: Inhalt``, durch Leerzeilen getrennt
   * - ``backlog.tags``
     - Wiki-Seite, Dokument
     - Liste der Tag-Namen
   * - ``backlog.parent_type``, ``backlog.parent_url``, ``backlog.parent_title``
     - Anhang
     - Der Vorgang, die Wiki-Seite oder das Dokument, zu dem der Anhang gehört
   * - ``backlog.size``
     - Anhang, Datei
     - Heruntergeladene Größe in Bytes
   * - ``backlog.path``
     - Datei
     - Pfad der freigegebenen Datei, zum Beispiel ``/docs/spec.pdf``

URLs
----

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Typ
     - URL
   * - Vorgang
     - ``{space_url}/view/{ISSUE-KEY}``
   * - Wiki-Seite
     - ``{space_url}/alias/wiki/{ID}``
   * - Dokument
     - ``{space_url}/document/{PROJECT}/{ID}``
   * - Datei
     - ``{space_url}/file/{PROJECT}{Verzeichnis}{Name}`` (jedes Pfadsegment wird prozentcodiert)
   * - Anhang
     - ``{URL des übergeordneten Elements}#attachment-{ID}``

.. note::

   Die URL-Formen von Dokumenten und freigegebenen Dateien sowie der Download-Endpunkt für Dokumentanhänge
   wurden nicht an einem echten Backlog-Space bestätigt. Öffnet ein Link nicht die erwartete Seite,
   ist das Dokument dennoch indexiert und durchsuchbar; nur das Linkziel ist falsch.

Berechtigungen
==============

Mit ``permission_sync=true`` (Standard) erhält jedes Dokument eines Projekts die folgenden Rollen:

- eine ``{user}``-Rolle für die ``mailAddress`` und eine für die ``userId`` jedes Projektmitglieds
  (leere Werte werden übersprungen), sodass sich ein Mitglied mit beiden bei |Fess| anmelden kann
- den Wert von ``default_permissions``
- den Wert des Felds „Berechtigungen“ der Datenspeicher-Konfiguration

Können die Projektmitglieder nicht abgerufen werden oder hat keines von ihnen eine verwendbare ``mailAddress`` oder ``userId``,
wird das gesamte Projekt übersprungen und unter "Crawler" -> "Fehler-URLs" aufgezeichnet. Es wird nie ohne seine Mitgliederrollen indexiert.

Mit ``permission_sync=false`` gelten nur ``default_permissions`` und das Feld „Berechtigungen“.

.. warning::

   Leeren Sie das Feld „Berechtigungen“ der Datenspeicher-Konfiguration. Die Administrationsoberfläche füllt es vorab mit ``{role}guest``,
   das jeder Benutzer einschließlich anonymer Suchender besitzt. Bleibt es stehen, wird es mit den Rollen jedes Dokuments zusammengeführt
   und alle Backlog-Inhalte werden für alle durchsuchbar.
   Bei ``permission_sync=true`` protokolliert der Konnektor pro Projekt eine Warnung, wenn eine Gastrolle unter seinen Rollen landet.

Was Sie wissen sollten, bevor Sie sich auf die Mitgliederrollen verlassen:

- Eine Mitglieder-Kennung ist ein |Fess|-Anmeldename. Eine Backlog-``userId`` wie ``tanaka`` gewährt den Zugriff dem |Fess|-Login ``tanaka``,
  der nicht dieselbe Person sein muss (zum Beispiel ein LDAP- oder Active-Directory-Kontoname). Die Rolle über die ``mailAddress`` hat dieses Problem nicht.
  Verwenden Sie ``permission_sync`` nur dort, wo die |Fess|-Anmeldenamen den Backlog-Benutzer-IDs oder E-Mail-Adressen entsprechen.
- Ein Mitglied, dessen Kennung auf die Gastrolle oder auf einen anderen Login abgebildet würde, wird mit einer Warnung ignoriert, die Projekt und Mitglieds-ID nennt:
  eine ``userId`` ``guest`` und jede Kennung mit einem Backslash (|Fess| entfernt aus einem Benutzernamen alles bis zum Backslash).
- Jedes Projektmitglied kann jedes indexierte Element des Projekts finden, einschließlich Anhängen und freigegebenen Dateien, auch wenn Backlog selbst
  diesem Mitglied den Download verweigern würde (ein Benutzer mit „Nur Ansicht“ kann keine Vorgangsanhänge herunterladen). Die Rollen gelten pro Projekt, nicht pro Funktion.

Gelöschte Inhalte und entzogener Zugriff
========================================

Standardmäßig versieht |Fess| jedes Dokument mit einem Ablaufdatum (die Einstellung „Alte Dokumente löschen“ unter „Allgemein“, standardmäßig drei Tage)
und löscht Dokumente, die eines haben, am Ende eines Crawls nicht. Abgelaufene Dokumente entfernt der Doc Purger. Standardmäßig gilt daher:

- In Backlog gelöschte Inhalte bleiben bis zu etwa drei Tage durchsuchbar
- Verlässt ein Mitglied ein Projekt, behält es bis zu etwa drei Tage den Zugriff auf die bereits indexierten Dokumente des Projekts.
  Der nächste Crawl indexiert sie unter neuen Dokument-IDs erneut (die ID enthält die Rollenliste), und die alten Kopien mit den alten Rollen
  bleiben bis zu ihrem Ablauf bestehen. In dieser Zeit sehen die übrigen Mitglieder doppelte Ergebnisse

Um solche Dokumente stattdessen am Ende des Crawls zu entfernen, fügen Sie ``keep_expires_docs=false`` zu den Parametern der Datenspeicher-Konfiguration hinzu.
|Fess| löscht dann jedes Dokument dieser Konfiguration, das der Crawl nicht erneut indexiert hat; das gilt auch für alles, was der Crawl nicht erreicht hat (siehe „Fehlerbehandlung“).

Anwendungsbeispiele
===================

Bestimmte Projekte crawlen
--------------------------

Parameter:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    project_keys=PROJ,DOCS
    include_shared_files=false

Nur Vorgänge und Wiki-Seiten, ohne Anhänge
------------------------------------------

Parameter:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    include_documents=false
    include_attachments=false
    include_shared_files=false

In Backlog gelöschte Dokumente am Ende des Crawls entfernen
-----------------------------------------------------------

Parameter:

::

    api_key=**********************************************
    space_url=https://example.backlog.com
    keep_expires_docs=false

Fehlerbehandlung
================

- Der Crawl wird nur bei HTTP ``401``, dem Backlog-Fehlercode 11 (AuthenticationError) oder 12 (RequiredMFAError),
  einem fehlenden oder fehlerhaften ``api_key`` oder ``space_url`` oder dem Fehlschlagen der Projektliste abgebrochen.
- Bei HTTP ``429`` wartet die Anfrage bis zu dem Zeitpunkt, den der Header ``X-RateLimit-Reset`` angibt (höchstens 120 Sekunden; 60 Sekunden, wenn der Header fehlt), und wird wiederholt.
  Bei HTTP ``5xx`` und Verbindungsfehlern wird die Anfrage mit exponentiellem Backoff wiederholt (1 Sekunde, 2 Sekunden, 4 Sekunden, bis zu 60 Sekunden).
  Sind ``max_retry_count`` Wiederholungen aufgebraucht, schlägt dieses Element fehl.
- Jeder andere Fehler (``403``, ``404``, aufgebrauchte Wiederholungen) wird für dieses eine Element aufgezeichnet und der Crawl läuft weiter.
- Ein fehlgeschlagenes Element lässt den Crawl-Job nicht fehlschlagen. Prüfen Sie nach einem Crawl "Crawler" -> "Fehler-URLs" und das Crawler-Log.
- Mit ``keep_expires_docs=false`` werden Inhalte unter einem Fehler nicht erneut indexiert und deshalb am Ende dieses Crawls gelöscht:
  alles unter einer fehlgeschlagenen Auflistung, einem übersprungenen Projekt oder einer bei einem 403 übersprungenen Funktion verschwindet aus dem Index, bis ein späterer Crawl ohne diesen Fehler abgeschlossen wird.
  Dasselbe gilt für einen abgebrochenen Crawl. Standardmäßig bleiben solche Inhalte bis zu ihrem Ablauf durchsuchbar.

Fehlerbehebung
==============

Der Crawl wird beim Start abgebrochen
-------------------------------------

1. Prüfen Sie, ob ``api_key`` korrekt und für einen Benutzer dieses Space ausgestellt ist
2. Prüfen Sie, ob ``space_url`` eine ``https``-URL nur mit dem Host ist, etwa ``https://example.backlog.com``
3. Verlangt der Space eine Zwei-Faktor-Authentifizierung für den API-Zugriff, wird der Crawl mit RequiredMFAError abgebrochen

Ein Projekt wird nicht indexiert
--------------------------------

1. Prüfen Sie, ob der API-Benutzer Mitglied des Projekts ist
2. Bei ``permission_sync=true`` wird ein Projekt übersprungen, dessen Mitglieder nicht abgerufen werden können oder von denen keines eine verwendbare E-Mail-Adresse oder Benutzer-ID hat. Siehe "Crawler" -> "Fehler-URLs"
3. Prüfen Sie ``project_keys`` und ``include_archived``

Anhänge oder freigegebene Dateien fehlen
----------------------------------------

Weisen Sie dem API-Benutzer eine Rolle ohne Einschränkungen zu. Das Log enthält pro Projekt und Funktion, die bei HTTP 403 übersprungen wurde, eine Warnung.

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-atlassian` - Atlassian-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../../admin/failureurl-guide` - Fehler-URLs
- :doc:`../../admin/plugin-guide` - Leitfaden zur Plugin-Verwaltung
- `Backlog API Documentation <https://developer.nulab.com/docs/backlog/>`_
