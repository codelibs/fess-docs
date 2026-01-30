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
- Dateianhänge (optional)

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

    token=xoxp-123456789012-123456789012-123456789012-abc123def456ghi789jkl012mno345pq
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
     - Ja
     - Zu crawlende Kanäle (kommagetrennt oder ``*all``)
   * - ``file_crawl``
     - Nein
     - Auch Dateien crawlen (Standard: ``false``)
   * - ``include_private``
     - Nein
     - Private Kanäle einschließen (Standard: ``false``)

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
   * - ``message.text``
     - Textinhalt der Nachricht
   * - ``message.user``
     - Anzeigename des Nachrichtenabsenders
   * - ``message.channel``
     - Kanalname, in dem die Nachricht gesendet wurde
   * - ``message.timestamp``
     - Sendezeitpunkt der Nachricht
   * - ``message.permalink``
     - Permalink der Nachricht
   * - ``message.attachments``
     - Fallback-Informationen zu Dateianhängen

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

**Bot Token Scopes** hinzufügen:

Nur für öffentliche Kanäle:

- ``channels:history`` - Lesen von Nachrichten in öffentlichen Kanälen
- ``channels:read`` - Lesen von Informationen öffentlicher Kanäle

Private Kanäle einschließen (``include_private=true``):

- ``channels:history``
- ``channels:read``
- ``groups:history`` - Lesen von Nachrichten in privaten Kanälen
- ``groups:read`` - Lesen von Informationen privater Kanäle

Auch Dateien crawlen (``file_crawl=true``):

- ``files:read`` - Lesen von Dateiinhalten

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

Fehlerbehebung
==============

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
4. Überprüfen Sie, ob der Kanal existiert und nicht archiviert ist

Keine Nachrichten abrufbar
--------------------------

**Symptom**: Crawling erfolgreich, aber 0 Nachrichten

**Zu überprüfen**:

1. Überprüfen Sie, ob die erforderlichen Scopes erteilt wurden:

   - ``channels:history``
   - ``channels:read``
   - Bei privaten Kanälen: ``groups:history``, ``groups:read``

2. Überprüfen Sie, ob Nachrichten im Kanal existieren
3. Überprüfen Sie, ob die App zum Kanal hinzugefügt wurde
4. Überprüfen Sie, ob die Slack-App aktiviert ist

Fehler wegen fehlender Berechtigungen
-------------------------------------

**Symptom**: ``missing_scope``

**Lösung**:

1. Fügen Sie die erforderlichen Scopes in den Slack-App-Einstellungen hinzu:

   **Öffentliche Kanäle**:

   - ``channels:history``
   - ``channels:read``

   **Private Kanäle**:

   - ``groups:history``
   - ``groups:read``

   **Dateien**:

   - ``files:read``

2. Installieren Sie die App neu
3. Starten Sie |Fess| neu

Dateien werden nicht gecrawlt
-----------------------------

**Symptom**: Dateien werden trotz ``file_crawl=true`` nicht abgerufen

**Zu überprüfen**:

1. Überprüfen Sie, ob der Scope ``files:read`` erteilt wurde
2. Überprüfen Sie, ob tatsächlich Dateien im Kanal gepostet wurden
3. Überprüfen Sie die Zugriffsberechtigungen für die Dateien

API-Ratenbegrenzung
-------------------

**Symptom**: ``rate_limited``

**Lösung**:

1. Verlängern Sie das Crawl-Intervall
2. Reduzieren Sie die Anzahl der Kanäle
3. Teilen Sie in mehrere Datenspeicher auf und verteilen Sie die Zeitplanung

Slack-API-Limits:

- Tier 3-Methoden: 50+ Anfragen/Minute
- Tier 4-Methoden: 100+ Anfragen/Minute

Bei großen Nachrichtenmengen
----------------------------

**Symptom**: Crawling dauert lange oder Timeout

**Lösung**:

1. Teilen Sie Kanäle auf und konfigurieren Sie mehrere Datenspeicher
2. Verteilen Sie die Crawl-Zeitplanung
3. Erwägen Sie Einstellungen zum Ausschließen alter Nachrichten

Erweiterte Skript-Beispiele
===========================

Nachrichten filtern
-------------------

Nur Nachrichten eines bestimmten Benutzers indizieren:

::

    if (message.user == "Max Mustermann") {
        title=message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

Nur Nachrichten mit bestimmten Schlüsselwörtern:

::

    if (message.text.contains("wichtig") || message.text.contains("Störung")) {
        title="[Wichtig] " + message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

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
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
