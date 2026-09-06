==================================
Slack-Konnektor
==================================

Übersicht
=========

Der Slack-Konnektor bietet die Funktionalität, Channel-Nachrichten aus Slack-Workspaces abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-slack`` erforderlich.

Unterstützte Inhalte
====================

- Nachrichten in öffentlichen Kanälen
- Nachrichten in privaten Kanälen
- Antwortnachrichten in Threads (abgerufen über ``conversations.replies``)
- Dateianhänge (optional)

Folgendes ist nicht enthalten:

- Systemereignis-Nachrichten (``channel_join``, ``channel_topic``, ``pinned_item`` usw.) werden
  standardmäßig von der Indexierung ausgeschlossen (``ignore_system_events``)
- Direktnachrichten (DMs) und Gruppen-DMs
- Huddle-Transkripte und Clips (Slack bietet hierfür keine öffentliche API, daher können sie
  nicht gecrawlt werden)

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Eine Slack-App muss erstellt und Berechtigungen konfiguriert werden
3. Ein OAuth Access Token muss abgerufen werden

Plugin-Installation
-------------------

Installieren Sie über die Administrationsoberfläche unter "System" -> "Plugins":

1. Laden Sie ``fess-ds-slack-X.X.X.jar`` von Maven Central herunter
2. Laden Sie es über die Plugin-Verwaltungsoberfläche hoch und installieren Sie es
3. Starten Sie |Fess| neu

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
     - Company Slack
   * - Handler-Name
     - SlackDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

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
     - OAuth Access Token der Slack-App
   * - ``channels``
     - Nein
     - Zu crawlende Kanäle (kommagetrennt oder ``*all``). Wenn nicht angegeben, werden alle Kanäle abgerufen (gleiches Verhalten wie ``*all``)
   * - ``file_crawl``
     - Nein
     - Auch Dateien crawlen (Standard: ``false``)
   * - ``include_private``
     - Nein
     - Private Kanäle einschließen (Standard: ``false``)
   * - ``number_of_threads``
     - Nein
     - Anzahl der parallelen Verarbeitungs-Threads (Standard: ``1``)
   * - ``max_filesize``
     - Nein
     - Maximale Dateigröße in Bytes (Standard: ``10000000``)
   * - ``ignore_error``
     - Nein
     - Verarbeitung bei Fehler fortsetzen (Standard: ``true``)
   * - ``supported_mimetypes``
     - Nein
     - Regex für erlaubte MIME-Typen (Standard: ``.*``)
   * - ``include_pattern``
     - Nein
     - Regex-Muster für einzuschließende URLs
   * - ``exclude_pattern``
     - Nein
     - Regex-Muster für auszuschließende URLs
   * - ``proxy_host``
     - Nein
     - HTTP-Proxy-Host
   * - ``proxy_port``
     - Nein
     - HTTP-Proxy-Port (erforderlich, wenn ``proxy_host`` angegeben)
   * - ``file_types``
     - Nein
     - Dateitypfilter für die Slack-API (Standard: ``all``)
   * - ``channel_count``
     - Nein
     - Anzahl der Kanäle pro API-Seite (Standard: ``100``)
   * - ``message_count``
     - Nein
     - Anzahl der Nachrichten pro API-Seite (Standard: ``100``)
   * - ``file_count``
     - Nein
     - Anzahl der Dateien pro API-Seite (Standard: ``20``)
   * - ``user_count``
     - Nein
     - Anzahl der Benutzer pro API-Seite (Standard: ``100``)
   * - ``user_cache_size``
     - Nein
     - Maximale Anzahl von Einträgen im Benutzerinformations-Cache (Standard: ``10000``)
   * - ``bot_cache_size``
     - Nein
     - Maximale Anzahl von Einträgen im Bot-Informations-Cache (Standard: ``10000``)
   * - ``channel_cache_size``
     - Nein
     - Maximale Anzahl von Einträgen im Kanal-Informations-Cache (Standard: ``10000``)

Erweiterte Parameter
~~~~~~~~~~~~~~~~~~~~

Die folgenden Parameter steuern das Verbindungs- und Wiederholungsverhalten, die feingranulare
Steuerung des Crawling-Umfangs sowie die Berechtigungssynchronisierung:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parameter
     - Beschreibung
   * - ``connection_timeout``
     - Verbindungstimeout für jede Slack-API-Anfrage (Millisekunden, Standard: ``20000``)
   * - ``read_timeout``
     - Lesetimeout für jede Slack-API-Anfrage (Millisekunden, Standard: ``20000``)
   * - ``max_retry_count``
     - Maximale Anzahl an Wiederholungsversuchen nach einer ``429``-Antwort (Rate Limit) oder einer ``5xx``-Antwort (Standard: ``3``)
   * - ``retry_interval``
     - Wartezeit in Millisekunden bis zum ersten Wiederholungsversuch, wenn die Antwort keinen ``Retry-After``-Header enthält (Standard: ``3000``). Verdoppelt sich mit jedem weiteren Versuch, gedeckelt bei ``60000`` Millisekunden. Enthält die Antwort einen ``Retry-After``-Header, wird stattdessen dessen Wert (in Sekunden) verwendet
   * - ``executor_timeout``
     - Wartezeit in Sekunden am Ende eines Crawls, bis in der Warteschlange verbleibende Aufgaben abgeschlossen sind, bevor der Abbruch erzwungen wird (Standard: ``60``)
   * - ``exclude_archived``
     - Gibt an, ob archivierte Kanäle aus den Ergebnissen von ``conversations.list`` ausgeschlossen werden (Standard: ``false``). Bei ``true`` kann ein in ``channels`` per Name angegebener archivierter Kanal nicht mehr aufgelöst werden (Details siehe Fehlerbehebung)
   * - ``ignore_system_events``
     - Gibt an, ob von Slack automatisch erzeugte Kanalverwaltungsnachrichten (``channel_join``, ``channel_topic``, ``pinned_item`` usw.) von der Indexierung ausgeschlossen werden (Standard: ``true``)
   * - ``read_interval``
     - Wartezeit in Millisekunden nach der Verarbeitung jeder Nachricht oder Datei (Standard: ``0`` = keine Wartezeit). Damit lässt sich das Crawling bei einem Workspace mit strengem Rate Limit verlangsamen
   * - ``max_content_length``
     - Maximale Anzahl an Zeichen, die die Inhaltsextraktion (Tika) aus einer Datei extrahieren darf (Standard: nicht gesetzt, es gilt dann das MIME-Typ-spezifische Limit von |Fess|). ``max_filesize`` ist das übertragungsseitige Limit, das Dateien anhand ihrer Größe bereits vor dem Download ablehnt, während ``max_content_length`` das extraktionsseitige Limit für die nach dem Download extrahierte Textmenge ist; beide wirken unabhängig voneinander. Ein kleineres ``max_filesize`` ersetzt ``max_content_length`` nicht (z. B. kann ein 1-MB-Archiv nach der Extraktion in weit mehr Text resultieren)
   * - ``permission_sync``
     - Gibt an, ob die Mitgliedschaft in privaten Kanälen in Suchberechtigungen (Rollen) umgewandelt wird (Standard: ``false``). Details siehe Abschnitt "Berechtigungssynchronisierung (ACL)" weiter unten
   * - ``default_permissions``
     - Zusätzliche Berechtigungen, die unabhängig von der Kanalmitgliedschaft allen indexierten Dokumenten zugewiesen werden (Format ``{user}``/``{group}``/``{role}``, kommagetrennt, Standard: leer). Wird nur angewendet, wenn ``permission_sync`` aktiviert ist

.. note::

   ``ignore_system_events`` hat den Standardwert ``true``. Selbst eine bestehende Crawl-Konfiguration,
   die diesen Parameter nicht setzt, indexiert nach einem Upgrade von |Fess| keine
   Systemereignis-Nachrichten wie ``channel_join`` mehr -- die Anzahl indexierter Dokumente sinkt
   ohne Fehler oder Warnung. Setzen Sie ``ignore_system_events=false`` explizit, um diese
   Nachrichten wie bisher zu indexieren.

Skript-Einstellungen
--------------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Verfügbare Felder
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beschreibung
   * - ``message.title``
     - Titel (leerer String für Nachrichten, Dateiname und Titel für Dateieinträge)
   * - ``message.text``
     - Textinhalt der Nachricht (bei Dateieinträgen: Dateiname und der extrahierte Dateiinhalt)
   * - ``message.user``
     - Anzeigename des Nachrichtenabsenders (falls nicht gesetzt, wird in der Reihenfolge echter Name, Benutzername, dann Benutzer-ID aufgelöst)
   * - ``message.channel``
     - Kanalname, in dem die Nachricht gesendet wurde
   * - ``message.timestamp``
     - Sendezeitpunkt der Nachricht
   * - ``message.permalink``
     - Permalink der Nachricht
   * - ``message.attachments``
     - Fallback-Informationen zu Dateianhängen
   * - ``message.roles``
     - Liste der Suchberechtigungen (Rollen), die diese Nachricht oder Datei sehen dürfen. Nur vorhanden, wenn ``permission_sync=true``. Wird im Skript nicht ``role=message.roles`` zugewiesen, werden die berechneten Rollen nie in das indexierte Dokument übernommen

Slack-App konfigurieren
=======================

1. Slack-App erstellen
----------------------

Besuchen Sie https://api.slack.com/apps:

1. Klicken Sie auf "Create New App"
2. Wählen Sie "From scratch"
3. Geben Sie den App-Namen ein (z.B.: Fess Crawler)
4. Wählen Sie den Workspace
5. Klicken Sie auf "Create App"

2. OAuth & Permissions konfigurieren
------------------------------------

Im Menü "OAuth & Permissions":

**Fügen Sie zu den Bot Token Scopes hinzu**:

Basis-Scopes (immer erforderlich):

- ``channels:history`` - Lesen von Nachrichten in öffentlichen Kanälen
- ``channels:read`` - Lesen von Informationen zu öffentlichen Kanälen
- ``users:read`` - Lesen von Benutzerinformationen (erforderlich für die Auflösung von Anzeigenamen)
- ``team:read`` - Lesen von Workspace-Informationen. ``team.info`` wird bei jedem Crawl aufgerufen,
  daher ist dieser Scope erforderlich; ohne ihn weicht dieser Konnektor für jede Nachricht auf
  einen zusätzlichen ``chat.getPermalink``-Aufruf aus, was die Anzahl der API-Aufrufe deutlich
  erhöht

Bei zusätzlicher Einbeziehung privater Kanäle (``include_private=true``):

- ``groups:history`` - Lesen von Nachrichten in privaten Kanälen
- ``groups:read`` - Lesen von Informationen zu privaten Kanälen

Beim zusätzlichen Crawlen von Dateien (``file_crawl=true``):

- ``files:read`` - Lesen von Dateiinhalten

Bei zusätzlicher Synchronisierung von Berechtigungen privater Kanäle (``permission_sync=true``):

- ``users:read.email`` - Lesen der E-Mail-Adressen von Mitgliedern (erforderlich für die
  Berechtigungssynchronisierung)

3. App installieren
-------------------

Im Menü "Install App":

1. Klicken Sie auf "Install to Workspace"
2. Überprüfen Sie die Berechtigungen und klicken Sie auf "Zulassen"
3. Kopieren Sie das "Bot User OAuth Token" (beginnt mit ``xoxb-``)

.. note::
   Normalerweise wird das Bot User OAuth Token verwendet, das mit ``xoxb-`` beginnt,
   aber in den Parametern kann auch das User OAuth Token verwendet werden, das mit ``xoxp-`` beginnt.

4. Zu Kanälen hinzufügen
------------------------

Fügen Sie die App zu den zu crawlenden Kanälen hinzu:

1. Öffnen Sie den Kanal in Slack
2. Klicken Sie auf den Kanalnamen
3. Wählen Sie den Tab "Integrationen"
4. Klicken Sie auf "App hinzufügen"
5. Fügen Sie die erstellte App hinzu

Berechtigungssynchronisierung (ACL)
===================================

Der Slack-Konnektor kann die Mitgliedschaft eines privaten Kanals in |Fess|-Suchberechtigungen
(Rollen) umwandeln, sodass nur die Mitglieder dieses Kanals dessen Inhalt durchsuchen können.
Diese Funktion ist standardmäßig deaktiviert.

.. note::

   ``permission_sync`` berechnet Rollen lediglich; es wendet sie nicht automatisch an. Erst
   wenn Sie im Skript ``role=message.roles`` ergänzen, werden die berechneten Rollen in den
   indexierten Dokumenten übernommen. Wird diese Zuordnung vergessen, entstehen dennoch die
   zusätzlichen API-Aufrufe und übersprungenen privaten Kanäle, die ``permission_sync=true``
   verursacht -- ohne dass irgendeine Zugriffskontrolle stattfindet.

Aktivierung
-----------

1. Fügen Sie der Slack-App den Scope ``users:read.email`` hinzu (erforderlich zur Auflösung
   der E-Mail-Adressen der Mitglieder)
2. Setzen Sie in den Parametern ``permission_sync=true``
3. Fügen Sie im Skript ``role=message.roles`` hinzu

Parameter:

::

    include_private=true
    permission_sync=true

Skript:

::

    role=message.roles

Fail-Closed-Verhalten
---------------------

Ein privater Kanal wird in einem gegebenen Crawl überhaupt nicht indexiert, wenn einer der
folgenden Fälle zutrifft (dies ist ein "Fail-Closed"-Verhalten: das Risiko besteht in einer
Unter-Indexierung, niemals darin, Inhalte versehentlich für alle offenzulegen):

- Das Abrufen der Mitgliederliste des Kanals ist fehlgeschlagen
- Die Mitgliederliste kam leer zurück (dies passiert, wenn der Bot-Benutzer des crawlenden
  Tokens selbst kein Mitglied des privaten Kanals ist)
- Der Kanal hat Mitglieder, aber für keinen von ihnen konnte eine E-Mail-Adresse aufgelöst
  werden (meist weil der Scope ``users:read.email`` fehlt)

Öffentliche Kanäle rufen ``conversations.members`` niemals auf und gelten stets als für alle
sichtbar.

Übereinstimmung des Principal-Namens
------------------------------------

Die Berechtigungsprüfung zur Suchzeit verwendet den |Fess|-Anmeldenamen (den Principal-Namen).
Da die von dieser Funktion berechneten Rollen aus Slack-E-Mail-Adressen abgeleitet werden, muss
der |Fess|-Anmeldename mit der Slack-E-Mail-Adresse übereinstimmen. Slack normalisiert
E-Mail-Adressen auf Kleinschreibung, halten Sie daher auch die |Fess|-Anmeldenamen in
Kleinschreibung. Eine Abweichung legt nicht die Inhalte eines anderen Benutzers offen -- sie
führt lediglich dazu, dass die Suchergebnisse des betroffenen Benutzers stets leer sind, was
leicht mit einem unabhängigen Fehler verwechselt werden kann.

Weitere Hinweise
----------------

- Slack-Benutzergruppen (User Groups) werden nicht verwendet; Berechtigungen werden direkt aus
  der E-Mail-Adresse jedes einzelnen Mitglieds berechnet
- Mit ``default_permissions`` können Sie unabhängig von der Kanalmitgliedschaft zusätzliche
  Berechtigungen für jedes Dokument vergeben (wird nur angewendet, wenn ``permission_sync=true``)
- Bleibt ``permission_sync=false``, während ``include_private=true`` gesetzt ist, wird der
  Inhalt privater Kanäle ausschließlich anhand der im Feld "Berechtigung" der
  Datenspeicher-Konfiguration hinterlegten Berechtigungen indexiert; bleibt dieses Feld leer,
  ist der Inhalt de facto für alle öffentlich
- Wird ``permission_sync`` erst nachträglich aktiviert, werden bereits durch einen früheren,
  uneingeschränkten Crawl indexierte Inhalte nicht rückwirkend abgesichert. Um Rollen auf diese
  Inhalte anzuwenden, setzen Sie ``permission_sync=true`` und ``role=message.roles`` und
  crawlen Sie danach erneut. Ebenso entfernt eine spätere Deaktivierung von ``permission_sync``
  keine Rollen, die bereits auf zuvor indexierte Dokumente angewendet wurden

Anwendungsbeispiele
===================

Bestimmte Kanäle crawlen
------------------------

Parameter:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

Skript:

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Alle Kanäle crawlen
-------------------

Parameter:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

Skript:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Private Kanäle einschließen
---------------------------

Parameter:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

Skript:

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\nAnhang: " + message.attachments
    created=message.timestamp
    url=message.permalink

Mit Dateien crawlen
-------------------

Parameter:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

Skript:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

Detaillierte Nachrichteninformationen einschließen
--------------------------------------------------

Skript:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

Mit Berechtigungssynchronisierung crawlen
-----------------------------------------

Beschränkt den Inhalt privater Kanäle so, dass nur die Mitglieder dieses Kanals ihn durchsuchen
können. Fügen Sie der Slack-App vorher den Scope ``users:read.email`` hinzu.

Parameter:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

Skript:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::

   Vergessen Sie ``role=message.roles``, werden die berechneten Rollen nie in den indexierten
   Dokumenten übernommen. Details siehe "Berechtigungssynchronisierung (ACL)".

Fehlerbehebung
==============

Funktionsweise der Fehlerbehandlung
-----------------------------------

Der Slack-Konnektor unterscheidet bei Slack-API-Fehlern drei Arten:

- **Fatale Fehler**\ (``invalid_auth``, ``token_revoked``, ``account_inactive``,
  ``missing_scope``, ``not_authed``, ``token_expired``): Das Token selbst ist unbrauchbar,
  daher schlägt der gesamte Crawl-Job fehl
- **Vorübergehende Fehler**\ (``ratelimited``, ``internal_error``, ``fatal_error``,
  ``service_unavailable``, ``request_timeout``): Löst sich der Fehler auch durch
  Wiederholungsversuche nicht, schlägt der gesamte Crawl-Job fehl (zum Wiederholungsverhalten
  siehe "API-Ratenbegrenzung" weiter unten)
- **Kanalbezogene Fehler**\ (``channel_not_found``, ``not_in_channel`` usw.): Nur dieser Kanal
  wird mit einer Warnung übersprungen, das Crawling der übrigen Kanäle wird fortgesetzt

In früheren Versionen konnte ein fataler Fehler dennoch als "erfolgreicher" Crawl gemeldet
werden, der stillschweigend null oder nur einen Teil der Dokumente indexierte. Diese
Dreiteilung stellt nun sicher, dass fatale und vorübergehende Fehler stets als Job-Fehlschlag
gemeldet werden.

Authentifizierungsfehler
------------------------

**Symptom**: ``invalid_auth`` oder ``not_authed``

**Zu überprüfen**:

1. Überprüfen Sie, ob das Token korrekt kopiert wurde
2. Überprüfen Sie das Token-Format:

   - Bot User OAuth Token: beginnt mit ``xoxb-``
   - User OAuth Token: beginnt mit ``xoxp-``

3. Überprüfen Sie, ob die App im Workspace installiert ist
4. Überprüfen Sie, ob die erforderlichen Berechtigungen erteilt wurden

Kanal nicht gefunden
--------------------

**Symptom**: ``channel_not_found``

**Zu überprüfen**:

1. Überprüfen Sie, ob der Kanalname korrekt ist (# ist nicht erforderlich)
2. Überprüfen Sie, ob die App zum Kanal hinzugefügt wurde
3. Bei privaten Kanälen ``include_private=true`` setzen
4. Prüfen Sie, ob ``exclude_archived=true`` gesetzt ist. Standardmäßig
   (``exclude_archived=false``) werden auch archivierte Kanäle weiterhin aufgelistet und
   gecrawlt; nur bei ``true`` kann ein in ``channels`` per Name angegebener archivierter
   Kanal nicht mehr aufgelöst werden

Nachrichten können nicht abgerufen werden
-----------------------------------------

**Symptom**: Der Crawl ist erfolgreich, aber es werden nur wenige oder gar keine Dokumente
indexiert

**Zu überprüfen**:

1. ``ignore_system_events`` hat den Standardwert ``true``. Bestehen die Nachrichten eines
   Kanals ausschließlich aus Systemereignissen wie ``channel_join``, werden für ihn null
   Dokumente indexiert (siehe "Erweiterte Parameter")
2. Prüfen Sie, ob tatsächlich Nachrichten im Kanal vorhanden sind
3. Prüfen Sie, ob die App zum Kanal hinzugefügt wurde
4. Bei ``permission_sync=true`` wird ein privater Kanal, dessen Mitgliedschaft nicht
   aufgelöst werden kann, in diesem Crawl nicht indexiert (Fail-Closed; siehe
   "Berechtigungssynchronisierung (ACL)")

.. note::

   In früheren Versionen konnte ein fehlender Scope (``missing_scope``) den Crawl dennoch mit
   null Nachrichten "erfolgreich" abschließen lassen. Fatale Fehler, einschließlich
   ``missing_scope``, lassen den gesamten Crawl-Job jetzt fehlschlagen. Schlägt Ihr Job fehl,
   prüfen Sie stattdessen den folgenden Abschnitt "Fehler wegen fehlender Berechtigungen".

Fehler wegen fehlender Berechtigungen
-------------------------------------

**Symptom**: ``missing_scope`` (lässt den gesamten Crawl-Job fehlschlagen)

**Lösung**:

1. Fügen Sie die erforderlichen Scopes in den Slack-App-Einstellungen hinzu:

   **Basis**\ (immer erforderlich):

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **Private Kanäle**:

   - ``groups:history``
   - ``groups:read``

   **Dateien**:

   - ``files:read``

   **Berechtigungssynchronisierung**\ (``permission_sync=true``):

   - ``users:read.email``

2. Installieren Sie die App neu
3. Starten Sie |Fess| neu

Dateien werden nicht gecrawlt
-----------------------------

**Symptom**: Dateien werden trotz ``file_crawl=true`` nicht abgerufen

**Zu überprüfen**:

1. Überprüfen Sie, ob der Scope ``files:read`` erteilt wurde
2. Überprüfen Sie, ob tatsächlich Dateien im Kanal gepostet wurden
3. Überprüfen Sie die Zugriffsberechtigungen für die Dateien
4. Eine Datei, die größer als ``max_filesize`` ist, wird nicht heruntergeladen (prüfen Sie
   das Log auf eine Warnung)

API-Ratenbegrenzung
-------------------

**Symptom**: ``ratelimited`` (lässt den gesamten Crawl-Job fehlschlagen)

**Lösung**:

1. Erhöhen Sie ``max_retry_count`` und ``retry_interval``, falls die Standardwerte das
   Problem nicht lösen
2. Setzen Sie ``read_interval``, um das Crawling zu verlangsamen
3. Reduzieren Sie die Anzahl der Kanäle, oder teilen Sie in mehrere Datenspeicher auf und
   verteilen Sie die Zeitpläne

Ein ``ratelimited``-Fehler der Slack-API wird automatisch wiederholt: entweder unter
Verwendung des ``Retry-After``-Header-Werts in Sekunden, sofern vorhanden, oder andernfalls
mit einem exponentiellen Backoff ausgehend von ``retry_interval`` (bis zu
``max_retry_count`` Versuchen, gedeckelt bei 60 Sekunden). Besteht die Ratenbegrenzung nach
Ausschöpfen aller Wiederholungsversuche weiterhin, schlägt der gesamte Crawl-Job fehl.

Slack-API-Tiers (Obergrenzen für die Aufrufhäufigkeit):

- Tier 1: 1+ Anfragen/Minute
- Tier 2: 20+ Anfragen/Minute -- ``conversations.list``, ``users.list`` (werden zu Beginn
  jedes Crawls bedingungslos vollständig abgerufen, wodurch dieser Tier am ehesten
  ausgeschöpft wird)
- Tier 3: 50+ Anfragen/Minute -- ``conversations.history``, ``conversations.replies``,
  ``files.list``
- Tier 4: 100+ Anfragen/Minute -- ``conversations.members`` (nur bei
  ``permission_sync=true``), ``files.info`` (wird vom Crawling dieses Konnektors derzeit
  nicht aufgerufen)

.. note::

   Die Verschärfung der Slack-Ratenbegrenzung vom 29. Mai 2025 (Begrenzung von
   ``conversations.history`` und ``conversations.replies`` auf 50+ Anfragen/Minute) gilt nur
   für Apps, die außerhalb des Workspace verteilt werden, der sie erstellt hat, etwa über den
   Slack Marketplace. Sie gilt nicht für eine interne, für |Fess| erstellte App, die nur in
   dem Workspace installiert ist, der sie erstellt hat.

Bei großen Nachrichtenmengen
----------------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

1. Teilen Sie Kanäle auf und konfigurieren Sie mehrere Datenspeicher
2. Verteilen Sie die Crawl-Zeitplanung

Erweiterte Skript-Beispiele
===========================

Nachrichten formatieren
-----------------------

Zusammenfassung langer Nachrichten:

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

Kanalnamen formatieren:

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-atlassian` - Atlassian-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../security-role` - Leitfaden zur rollenbasierten Suchkonfiguration
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
