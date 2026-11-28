==================================================
Git, Confluence, Jira, Slack des Teams durchsuchen
==================================================

Einleitung
==========

Die Informationen eines Entwicklungsteams sind auf verschiedene Werkzeuge verteilt: Code und READMEs in Git, Designdokumente in Confluence, Tickets in Jira und Diskussionen in Slack.
Jedes Mal, wenn man herausfinden will, „wo diese Spezifikation eigentlich beschlossen wurde“, nacheinander in vier Werkzeugen zu suchen, ist mühsam.
Mit den Datenspeicher-Plugins von Fess lassen sich die Informationen aller vier Werkzeuge über eine einzige Suchseite finden.

Ist die Konfiguration jedoch fehlerhaft, kommt es zu Zuständen wie diesen:

- Alle Git-Dateien werden mit leerer URL registriert, sodass sich die Originaldatei aus den Suchergebnissen nicht öffnen lässt
- Alle Slack-Nachrichten werden ohne Titel angezeigt
- Beiträge aus privaten Kanälen erscheinen auch in den Suchergebnissen nicht angemeldeter Benutzer
- Git-Dateien verschwinden nach einigen Tagen aus dem Index

Dieser Artikel zeigt für jedes Werkzeug eine minimale Konfiguration, die unverändert übernommen funktioniert, und erklärt, wie die jeweiligen Einstellungen die oben genannten Fallstricke vermeiden.
Die für alle Datenspeicher gemeinsamen Schritte wie die Installation der Plugins, die Angabe von Handler-Name, Parametern und Skript sowie das Anlegen von Jobs sind in :doc:`datastore-basics` zusammengefasst.
Lesen Sie diesen Artikel zuerst, bevor Sie fortfahren.
Die Einstellungen in diesem Artikel beziehen sich auf Fess 15.9 und die Version 15.9.0 der jeweiligen Plugins.

Was wir aufbauen
================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - Werkzeug
     - Plugin
     - Handler-Name
     - Was im Werkzeug vorzubereiten ist
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - Ein Zugriffstoken mit Leserechten (Klonen über HTTPS muss möglich sein)
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - Ein API-Token des Crawl-Kontos
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - Das Bot User OAuth Token (``xoxb-``) einer Slack-App

Wenn Sie Fess mit Docker betreiben, können Sie alle Plugins beim Start auf einmal installieren, indem Sie Plugin-Namen und Versionen durch Leerzeichen getrennt in der Umgebungsvariablen ``FESS_PLUGINS`` aufführen.

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

Wenn Sie die Plugins über die Administrationsoberfläche oder mit ``fess-setup`` installieren, starten Sie Fess nach der Installation neu.

Vorab festlegen: Wer die Suchergebnisse sehen darf
==================================================

Wenn Sie eine neue Datenspeicher-Konfiguration anlegen, ist das Feld „Berechtigungen“ bereits mit ``{role}guest`` vorbelegt.
Belassen Sie es so, können auch nicht angemeldete Benutzer die importierten Informationen finden.

Die Plugins für Git, Confluence und Jira übernehmen die Zugriffsrechte des Ursprungswerkzeugs nicht in Fess.
Alles, was das Crawl-Konto lesen kann, wird importiert und ist für alle sichtbar, die eine der im Feld „Berechtigungen“ eingetragenen Rollen oder Gruppen besitzen.
Den Sichtbarkeitsbereich legen Sie daher durch die Kombination der folgenden zwei Punkte fest:

- Ersetzen Sie ``{role}guest`` im Feld „Berechtigungen“ durch die Personen, die die Inhalte sehen sollen (z. B. ``{group}developers``)
- Beschränken Sie den importierten Umfang über die Rechte des Crawl-Kontos sowie über die später beschriebenen ``jira.jql`` und ``include_pattern`` auf das, was diese Personen sehen dürfen

Nur das Slack-Plugin kann die Mitglieder privater Kanäle als Berechtigungen übernehmen (siehe unten).
Wie Gruppen und Rollen funktionieren, erfahren Sie in :doc:`guide-05`.

Git-Repositories
================

Vorbereitung
------------

``fess-ds-git`` klont über HTTPS.
SSH-URIs (in der Form ``git@...``) werden nicht unterstützt.
Für private Repositories erstellen Sie ein Zugriffstoken zum Lesen.
Bei einem klassischen GitHub-Token ist das der Scope ``repo``, bei GitLab der Scope ``read_repository``.

Parameter und Skript
--------------------

Wählen Sie unter [Crawler] > [Datenspeicher] > [Neu erstellen] als „Handler-Name“ ``GitDataStore`` aus.

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

Die einzelnen Zeilen bedeuten Folgendes:

- ``base_url``: Die ``url`` im Skript ist ``base_url``, unverändert mit dem Pfad innerhalb des Repositorys verkettet. Fehlt die Angabe, ist ``url`` eine leere Zeichenkette; alle Dateien erhalten dann dieselbe Dokument-ID und überschreiben sich gegenseitig. Beenden Sie den Wert mit ``/`` und passen Sie den Branch-Namen an den gecrawlten Branch an (standardmäßig der Standard-Branch des Remotes; zum Ändern ``commit_id`` verwenden).
- ``username`` / ``password``: werden nur zur Authentifizierung verwendet, wenn beide angegeben sind. Betten Sie das Token nicht in ``uri`` ein, sondern tragen Sie es in ``password`` ein (``password`` wird beim Speichern verschlüsselt, ``uri`` nicht).
- ``include_pattern``: ein regulärer Ausdruck, der auf den gesamten Pfad innerhalb des Repositorys (z. B. ``docs/setup.md``) passen muss. Es ist keine URL.
- ``title=path``: Mit ``name``, das nur den Dateinamen enthält, lassen sich gleichnamige Dateien wie ``README.md`` in den Suchergebnissen nicht unterscheiden; deshalb wird der Pfad verwendet.

Differenzielles Crawlen und Ablauffrist
---------------------------------------

Nach einem erfolgreichen Crawl schreibt ``fess-ds-git`` die Commit-ID in ``prev_commit_id`` im Feld „Parameter“ zurück.
Ab dem zweiten Durchlauf registriert es nur die Dateien aus dem Diff zum vorherigen Commit und löscht die Dokumente gelöschter oder umbenannter Dateien (für das Übernehmen von Löschungen ist ``base_url`` erforderlich).

Dieses differenzielle Crawlen verträgt sich schlecht mit der Ablauffrist von Dokumenten in Fess; deshalb ist im obigen Beispiel ``time_to_live`` angegeben.
Dokumente aus Datenspeichern erhalten bei der Registrierung eine Ablauffrist.
Standardmäßig wird sie durch „Alte Dokumente löschen“ unter [System] > [Allgemein] bestimmt (Standardwert 3 Tage), und Dokumente mit überschrittener Frist löscht der jede Minute laufende Job „Doc Purger“.
Beim differenziellen Crawlen werden unveränderte Dateien nicht erneut registriert; ihre Ablauffrist verlängert sich daher nicht, und sie verschwinden wenige Tage nach dem ersten Crawl.
``time_to_live`` ist ein Parameter, der die Ablauffrist der Dokumente dieser Konfiguration in Minuten angibt; ``5256000`` entspricht etwa 10 Jahren.

Aus demselben Grund wirken sich Änderungen an Skript, ``base_url``, ``include_pattern`` oder dem Feld „Berechtigungen“ nicht auf unveränderte Dateien aus.
Um alle Dateien neu zu registrieren, gehen Sie wie folgt vor:

1. Suchen Sie unter [Systeminformationen] > [Suche] nach ``label:code`` und löschen Sie die alten Dokumente mit [Alle mit dieser Abfrage löschen]
2. Entfernen Sie den Wert von ``prev_commit_id=`` im Feld „Parameter“ und speichern Sie
3. Führen Sie den Job aus

Wenn Sie das Feld „Berechtigungen“ oder ``base_url`` geändert haben, ändern sich die Dokument-IDs; lassen Sie Schritt 1 aus, bleiben alte Dokumente bestehen.
Auch wenn Sie diese Datenspeicher-Konfiguration löschen, entfernen Sie zuvor die Dokumente mit Schritt 1.

Confluence
==========

Erstellen Sie in Atlassian Cloud mit dem Crawl-Konto ein API-Token und verwenden Sie es als Passwort für die Basic-Authentifizierung.
Importiert werden die Seiten und Blogbeiträge der Bereiche, die dieses Konto anzeigen kann.
Wählen Sie als „Handler-Name“ ``ConfluenceDataStore`` aus.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home`` funktioniert mit und ohne ``/wiki``. In der Cloud wird für Confluence ``/wiki`` ergänzt.
- Fehlt ``deployment``, wird ``cloud`` angenommen, wenn der Hostname auf ``.atlassian.net`` endet, andernfalls ``datacenter``.
- Mit ``content.comments`` werden auch die Kommentare einer Seite als Teil des Textes durchsuchbar. Die Kommentare sind durch Leerzeilen getrennt aneinandergehängt.
- ``include_pattern`` wird mit der gesamten URL des Dokuments abgeglichen. In der Cloud haben Seiten-URLs die Form ``https://<Site>/wiki/spaces/<Bereichsschlüssel>/pages/<Seiten-ID>``, sodass Sie nach dem Bereichsschlüssel filtern können. Data-Center-URLs (``/pages/viewpage.action?pageId=...``) enthalten keinen Bereichsschlüssel, daher funktioniert diese Methode dort nicht.

Setzen Sie bei Data Center ``deployment=datacenter``; für ein persönliches Zugriffstoken geben Sie ``auth_type=pat`` und ``pat.token`` an.

Jira
====

Die Authentifizierung entspricht der von Confluence.
Wählen Sie als „Handler-Name“ ``JiraDataStore`` aus und schränken Sie die zu importierenden Tickets per JQL ein.

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

Der Parameter für JQL heißt ``jira.jql``.
Der alte Name ``issue.jql`` funktioniert noch, im Log erscheint dann jedoch die Warnung ``Parameter "issue.jql" is deprecated``.
Der alte Name soll in 16.0 entfernt werden.
Fehlt ``jira.jql``, gilt ``created is not empty``, also alle Tickets, die das Konto anzeigen kann.

Mit ``issue.comments`` werden auch die Kommentare eines Tickets, durch Leerzeilen getrennt, in den Text übernommen und durchsuchbar.
Die Kommentare werden pro Ticket über die API abgerufen, wodurch die Zahl der Aufrufe steigt (siehe die Ratenbegrenzung weiter unten).

Slack
=====

Slack-App vorbereiten
---------------------

Erstellen Sie unter https://api.slack.com/apps eine App, fügen Sie unter [OAuth & Permissions] bei Bot Token Scopes die folgenden Scopes hinzu und installieren Sie die App im Workspace.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Scope
     - Wann erforderlich
   * - ``channels:read``, ``channels:history``, ``users:read``, ``team:read``
     - Immer
   * - ``groups:read``, ``groups:history``
     - Private Kanäle importieren (``include_private=true``)
   * - ``users:read.email``
     - Mitglieder privater Kanäle als Berechtigungen verwenden (``permission_sync=true``)
   * - ``files:read``
     - Auch Dateien importieren (``file_crawl=true``)

Ohne ``team:read`` ruft das Plugin für jede Nachricht ``chat.getPermalink`` auf, wodurch die Zahl der API-Aufrufe stark steigt.
Fügen Sie die App nach der Installation jedem zu importierenden Kanal hinzu.
Kanäle, denen die App nicht beigetreten ist, werden mit einer Warnung übersprungen.

Legen Sie für öffentliche und private Kanäle zwei getrennte Datenspeicher-Konfigurationen an.
Den Grund erläutert der Abschnitt „Private Kanäle“.

Öffentliche Kanäle
------------------

Wählen Sie als „Handler-Name“ ``SlackDataStore`` aus und tragen Sie im Feld „Berechtigungen“ die Personen ein, die die öffentlichen Kanäle sehen sollen.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

``message.title`` ist bei Nachrichten immer eine leere Zeichenkette; mit ``title=message.title`` sind daher alle Ergebnisse ohne Titel.
Bilden Sie den Titel wie im obigen Beispiel aus Verfasser und Kanalname.
Antworten in Threads werden ebenfalls als einzelne Dokumente registriert.
Systemnachrichten wie ``channel_join`` werden standardmäßig (``ignore_system_events=true``) ausgeschlossen.

Private Kanäle
--------------

Mit ``permission_sync=true`` erzeugt das Plugin aus den E-Mail-Adressen der Mitglieder eines privaten Kanals für jedes Mitglied eine Benutzerrolle und legt sie in ``message.roles`` ab.
Diesem Wert werden allerdings auch die Werte von ``default_permissions`` und des Felds „Berechtigungen“ hinzugefügt.
Öffentliche Kanäle haben keine eigenen Rollen; sind beide Angaben leer, sind die Dokumente öffentlicher Kanäle für niemanden sichtbar.
Tragen Sie umgekehrt in einer der beiden Angaben die Zielgruppe der öffentlichen Kanäle ein, sieht diese Zielgruppe auch die Dokumente der privaten Kanäle.
Da eine einzige Konfiguration nicht beides korrekt abbilden kann, erhalten private Kanäle eine eigene Konfiguration.

Entfernen Sie in der zweiten Datenspeicher-Konfiguration ``{role}guest`` aus dem Feld „Berechtigungen“, sodass es leer ist, und führen Sie in ``channels`` die Namen der zu importierenden privaten Kanäle auf.

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- Ohne ``role=message.roles`` werden die berechneten Rollen nicht verwendet. In diesem Fall erscheint beim Start des Crawls die Warnung ``no script value references message.roles``.
- Mischen Sie öffentliche Kanäle in ``channels``, haben deren Dokumente leere Rollen und sind für niemanden sichtbar.
- Bei dieser Konfiguration erscheint beim Start des Crawls die Warnung ``default_permissions is not set and this crawl's DataConfig permission field is empty``. Solange keine öffentlichen Kanäle enthalten sind, ist das unproblematisch.
- Kanäle, deren Mitglieder nicht abgerufen werden konnten oder für die keine einzige E-Mail-Adresse aufgelöst werden konnte (etwa weil ``users:read.email`` vergessen wurde), werden in diesem Crawl nicht importiert. Sie werden unter [Systeminformationen] > [Fehler-URL] mit Kanal-ID und Kanalname protokolliert.

Bei der Suche wird der Benutzername der bei Fess angemeldeten Person mit diesen E-Mail-Adressen abgeglichen.
Der Benutzername in Fess muss daher mit der E-Mail-Adresse in Slack übereinstimmen.
Slack behandelt E-Mail-Adressen in Kleinbuchstaben, daher sollten auch die Benutzernamen in Fess kleingeschrieben sein.
Benutzer ohne Übereinstimmung sehen lediglich die Dokumente der privaten Kanäle nicht; die Dokumente anderer bekommen sie nie zu sehen.
Welcher Wert bei einer Anmeldung per SSO zum Benutzernamen wird, erfahren Sie in :doc:`guide-15`.

Haben Sie private Kanäle bereits ohne ``permission_sync`` importiert, bleiben diese Dokumente bis zum Ablauf ihrer Frist ohne Berechtigungen bestehen.
Löschen Sie die betreffenden Dokumente unter [Systeminformationen] > [Suche], bevor Sie mit dieser Konfiguration crawlen.

Labels, Boost und Zeitpläne
===========================

Die Labels werden in den obigen Skripten jeweils mit der Zeile ``label="..."`` vergeben.
Um sie auf der Suchseite als Filter anzuzeigen, legen Sie unter [Crawler] > [Label] Labels mit denselben Werten (``code``, ``docs``, ``tickets``, ``slack``) an.
Beachten Sie: Gibt es ein Label, dessen „Eingeschlossene Pfade“ auf die URL des Dokuments passen, geht das Label aus dem Skript verloren (:doc:`datastore-basics`).

Regeln unter [Crawler] > [Dokument-Boost] werden auf Dokumente aus Datenspeichern nicht angewendet.
Wenn Designdokumente aus Confluence vor Slack-Nachrichten erscheinen sollen, erhöhen Sie den „Boost“ (Anfangswert ``1.0``) der Datenspeicher-Konfiguration für Confluence.
Der Wert wird mit der Suchbewertung multipliziert; ändern Sie ihn daher schrittweise und vergleichen Sie die Suchergebnisse.

Um die Werkzeuge unterschiedlich oft zu crawlen, verwenden Sie auf der Detailseite der jeweiligen Datenspeicher-Konfiguration [Neuen Job erstellen] (:doc:`datastore-basics`).

Ratenbegrenzung der APIs
========================

Die Plugins für Slack und Atlassian wiederholen Anfragen bei Antworten mit ``429`` und ``5xx`` automatisch und warten bei vorhandenem ``Retry-After``-Header die dort angegebene Anzahl Sekunden (bei Slack höchstens 60 Sekunden).

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Plugin
     - Einstellbare Parameter
   * - Slack
     - ``read_interval`` (Wartezeit pro Nachricht in Millisekunden, Standard ``0``), ``max_retry_count`` (Standard ``3``), ``retry_interval`` (Wartezeit bis zum ersten Wiederholungsversuch in Millisekunden, Standard ``3000``; verdoppelt sich bei jedem Versuch, höchstens 60 Sekunden)
   * - Atlassian
     - ``read_interval`` (Mindestabstand zwischen API-Aufrufen in Millisekunden, Standard ``0``; von allen Threads gemeinsam genutzt). Anzahl und Abstand der Wiederholungsversuche sind fest

Sind bei Slack alle Wiederholungsversuche erschöpft, wird der Crawl abgebrochen.
Der Status im Job-Log bleibt dabei „OK“; prüfen Sie das Ergebnis daher mit den Schritten im nächsten Abschnitt.

Funktion prüfen
===============

Wie Sie Job-Ergebnisse und Logs lesen, ist in :doc:`datastore-basics` beschrieben.
Ein Datenspeicher-Crawl kann fehlschlagen, während der Job trotzdem als „OK“ angezeigt wird; beurteilen Sie das Ergebnis daher anhand der Dokumentanzahl und der Logs.
Für den Aufbau in diesem Artikel prüfen Sie zusätzlich Folgendes:

1. Suchen Sie unter [Systeminformationen] > [Suche] nacheinander nach ``label:code``, ``label:docs``, ``label:tickets`` und ``label:slack`` und vergewissern Sie sich, dass die Anzahl nicht 0 ist
2. Öffnen Sie die URL eines Git-Dokuments und prüfen Sie, dass die Datei aus dem Repository angezeigt wird. Enthält ``fess-crawler.log`` die Warnung ``base_url is blank``, überprüfen Sie ``base_url``
3. Öffnen Sie die Detailseite der Git-Konfiguration und prüfen Sie, dass ``prev_commit_id`` in die Parameter zurückgeschrieben wurde
4. Suchen Sie im abgemeldeten Zustand nach einem Wort, das nur in einem privaten Kanal vorkommt, und prüfen Sie, dass kein Treffer erscheint
5. Melden Sie sich als Mitglied dieses Kanals an und prüfen Sie, dass dasselbe Wort gefunden wird

Wird es in Schritt 5 nicht gefunden, prüfen Sie, ob der Benutzername in Fess mit der E-Mail-Adresse in Slack übereinstimmt und ob ``fess-crawler.log`` die Warnung ``private channel(s) skipped`` enthält.
Schlägt eine ganze Konfiguration fehl, etwa wegen eines Authentifizierungsfehlers, wird dies pro Konfiguration unter [Systeminformationen] > [Fehler-URL] protokolliert.

Zusammenfassung
===============

- Geben Sie für Git immer ``base_url`` an und setzen Sie ``time_to_live``, damit Dokumente beim differenziellen Crawlen nicht ablaufen.
- Importieren Sie bei Confluence und Jira mit ``content.comments`` / ``issue.comments`` auch die Kommentare und schreiben Sie JQL in ``jira.jql``.
- Bilden Sie den Titel bei Slack aus ``message.user`` und ``message.channel``.
- Git, Confluence und Jira übernehmen die ursprünglichen Berechtigungen nicht; legen Sie den Sichtbarkeitsbereich daher über das Feld „Berechtigungen“ und den Importumfang fest.
- Legen Sie für private Slack-Kanäle eine eigene Konfiguration an und importieren Sie sie mit ``permission_sync=true``, ``role=message.roles`` und leerem Feld „Berechtigungen“.
- Die Priorität der einzelnen Informationsquellen steuern Sie über den „Boost“ der jeweiligen Datenspeicher-Konfiguration.

Referenzen
==========

- `Git-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-git.html>`__
- `Atlassian-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-atlassian.html>`__
- `Slack-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-slack.html>`__
- `Datenspeicher-Crawl <https://fess.codelibs.org/de/stable/admin/dataconfig-guide.html>`__
- `Allgemein <https://fess.codelibs.org/de/stable/admin/general-guide.html>`__
- `fess-ds-slack 15.9.0 README (Scopes und Berechtigungssynchronisierung) <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
