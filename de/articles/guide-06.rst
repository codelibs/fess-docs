============================================
Teil 6: Knowledge-Hub für Entwicklungsteams
============================================

Einführung
============

In Softwareentwicklungsteams werden täglich verschiedene Werkzeuge eingesetzt.
Code liegt in Git-Repositories, Spezifikationen in Confluence, Aufgaben in Jira und die tägliche Kommunikation läuft über Slack.
Jedes dieser Werkzeuge verfügt über eine eigene Suchfunktion, doch wenn die Frage auftaucht: "Wo wurde das nochmal diskutiert?", ist es ineffizient, jedes Tool einzeln zu durchsuchen.

In diesem Artikel zeigen wir, wie Sie die Informationen aus den Werkzeugen, die Ihr Entwicklungsteam täglich nutzt, in Fess zusammenführen und einen Knowledge-Hub mit integrierter Suche aufbauen.

Zielgruppe
==========

- Teamleiter und Infrastrukturverantwortliche in Softwareentwicklungsteams
- Personen, die eine werkzeugübergreifende Suche über entwicklungsrelevante Informationen wünschen
- Personen, die die grundlegende Verwendung von Datastore-Plugins kennenlernen möchten

Szenario
========

Wir richten eine integrierte Suche für ein Entwicklungsteam (20 Personen) ein.

.. list-table:: Ziel-Datenquellen
   :header-rows: 1
   :widths: 20 30 50

   * - Werkzeug
     - Verwendungszweck
     - Zu durchsuchende Informationen
   * - Git-Repository
     - Quellcodeverwaltung
     - Code, README, Konfigurationsdateien
   * - Confluence
     - Dokumentenverwaltung
     - Entwurfsdokumente, Besprechungsprotokolle, Anleitungen
   * - Jira
     - Ticketverwaltung
     - Fehlerberichte, Aufgaben, Stories
   * - Slack
     - Kommunikation
     - Technische Diskussionen, Entscheidungsprotokolle

Was ist Datastore-Crawling?
============================

Beim Web-Crawling und Datei-Crawling werden Dokumente anhand von URLs oder Dateipfaden gesammelt.
Um hingegen Informationen aus SaaS-Werkzeugen zu erfassen, wird das "Datastore-Crawling" verwendet.

Beim Datastore-Crawling werden Daten über die API des jeweiligen Werkzeugs abgerufen und im Fess-Index registriert.
Fess stellt für jedes Werkzeug ein eigenes Datastore-Plugin bereit.

Plugin-Installation
====================

Datastore-Plugins können über die Fess-Verwaltungsoberfläche installiert werden.

1. Wählen Sie in der Verwaltungsoberfläche [System] > [Plugins]
2. Überprüfen Sie die Liste der bereits installierten Plugins
3. Klicken Sie auf [Installieren], um zum Installationsbildschirm zu gelangen, und installieren Sie die benötigten Plugins über den Tab [Remote]

Für das vorliegende Szenario werden die folgenden Plugins verwendet:

- ``fess-ds-git``: Crawling von Git-Repositories
- ``fess-ds-atlassian``: Crawling von Confluence / Jira
- ``fess-ds-slack``: Crawling von Slack-Nachrichten

Konfiguration der einzelnen Datenquellen
==========================================

Git-Repository-Konfiguration
------------------------------

Durch das Crawling von Git-Repositories werden Code und Dokumente durchsuchbar gemacht.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: GitDataStore auswählen
3. Parameter konfigurieren

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

Geben Sie unter ``uri`` die Repository-URL und unter ``username`` / ``password`` die Zugangsdaten an. Bei privaten Repositories setzen Sie einen Zugriffstoken als ``password``. Mit ``include_pattern`` können Sie die zu crawlenden Dateierweiterungen per regulärem Ausdruck einschränken.

Confluence-Konfiguration
--------------------------

Confluence-Seiten und Blog-Beiträge werden durchsuchbar gemacht.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: ConfluenceDataStore auswählen
3. Parameter konfigurieren

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

Geben Sie unter ``home`` die Confluence-URL an und wählen Sie unter ``auth_type`` die Authentifizierungsmethode. Bei Confluence Cloud verwenden Sie die ``basic``-Authentifizierung und setzen einen API-Token unter ``basic.password``.

Jira-Konfiguration
--------------------

Jira-Tickets (Issues) werden durchsuchbar gemacht.

Hierfür wird der JiraDataStore-Handler verwendet, der im selben ``fess-ds-atlassian``-Plugin enthalten ist.
Mit JQL (Jira Query Language) können Sie die zu crawlenden Tickets einschränken.
Beispielsweise können Sie nur Tickets eines bestimmten Projekts oder nur Tickets mit einem bestimmten Status (außer Closed) erfassen.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: JiraDataStore auswählen
3. Parameter konfigurieren

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

Mit ``issue.jql`` geben Sie eine JQL-Abfrage an, um die zu crawlenden Tickets einzuschränken.

Slack-Konfiguration
--------------------

Slack-Nachrichten werden durchsuchbar gemacht.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: SlackDataStore auswählen
3. Parameter konfigurieren

**Beispiel für die Parameterkonfiguration**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**Beispiel für die Skriptkonfiguration**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

Geben Sie unter ``token`` den OAuth-Token des Slack-Bots an. Mit ``channels`` legen Sie die zu crawlenden Kanäle fest; um alle Kanäle zu erfassen, setzen Sie ``*all``. Wenn Sie private Kanäle einbeziehen möchten, setzen Sie ``include_private=true`` und stellen Sie sicher, dass der Bot in die entsprechenden Kanäle eingeladen wurde.

Verwendung von Labels
======================

Informationsquellen durch Labels unterscheiden
------------------------------------------------

Durch die Zuweisung von Labels zu den einzelnen Datenquellen können Benutzer bei der Suche zwischen den Informationsquellen wechseln.

- ``code``: Code aus Git-Repositories
- ``docs``: Dokumente aus Confluence
- ``tickets``: Tickets aus Jira
- ``discussions``: Nachrichten aus Slack

Benutzer können mit "Alle" eine übergreifende Suche durchführen und bei Bedarf über Labels filtern.

Verbesserung der Suchqualität
================================

Verwendung von Document-Boost
-------------------------------

In einem Knowledge-Hub für Entwicklungsteams haben nicht alle Dokumente die gleiche Wichtigkeit.
Beispielsweise ist folgende Priorisierung denkbar:

1. Confluence-Dokumente (offizielle Spezifikationen und Anleitungen)
2. Jira-Tickets (aktuelle Probleme und laufende Aufgaben)
3. Git-Repository (Code und README)
4. Slack-Nachrichten (Diskussionsprotokolle)

Mit Document-Boost können Sie den Suchscore von Dokumenten erhöhen, die bestimmte Kriterien erfüllen.
Über [Crawler] > [Document-Boost] in der Verwaltungsoberfläche können Sie Boost-Werte basierend auf URL-Mustern oder Labels konfigurieren.

Verwendung verwandter Inhalte
------------------------------

Durch die Anzeige von "verwandten Inhalten" in den Suchergebnissen können Sie Benutzer dabei unterstützen, die gesuchten Informationen schneller zu finden.
Wenn beispielsweise bei der Suche nach einem Confluence-Entwurfsdokument verwandte Jira-Tickets als "verwandte Inhalte" angezeigt werden, ist dies sehr hilfreich.

Betriebliche Hinweise
======================

Crawl-Zeitplan
---------------

Legen Sie für jede Datenquelle eine angemessene Crawl-Häufigkeit fest.

.. list-table:: Beispiel fuer einen Zeitplan
   :header-rows: 1
   :widths: 25 25 50

   * - Datenquelle
     - Empfohlene Häufigkeit
     - Begründung
   * - Confluence
     - alle 4 Stunden
     - Dokumente werden in mittlerer Häufigkeit aktualisiert
   * - Jira
     - alle 2 Stunden
     - Tickets werden häufig aktualisiert
   * - Git
     - täglich
     - Anpassung an den Release-Zyklus
   * - Slack
     - alle 4 Stunden
     - Echtzeit ist nicht erforderlich, aber Aktualität ist wichtig

Umgang mit API-Ratenbegrenzungen
---------------------------------

Die APIs von SaaS-Werkzeugen unterliegen Ratenbegrenzungen.
Stellen Sie die Crawl-Intervalle so ein, dass die API-Ratenbegrenzungen nicht überschritten werden.
Insbesondere die Slack API hat strenge Ratenbegrenzungen, weshalb es wichtig ist, großzügige Crawl-Intervalle einzuplanen.

Verwaltung von Zugriffstokens
-------------------------------

Für die Konfiguration der Datastore-Plugins werden API-Zugriffstokens der jeweiligen Werkzeuge benötigt.
Beachten Sie aus Sicherheitsgründen die folgenden Punkte:

- Prinzip der minimalen Berechtigung: Verwenden Sie Zugriffstokens mit ausschließlich Lesezugriff
- Regelmäßige Rotation: Erneuern Sie Tokens in regelmäßigen Abständen
- Verwendung dedizierter Konten: Nutzen Sie Servicekonten anstelle persönlicher Konten

Zusammenfassung
================

In diesem Artikel haben wir gezeigt, wie Sie die Informationen aus den Werkzeugen, die Ihr Entwicklungsteam täglich nutzt, in Fess zusammenführen und einen Knowledge-Hub mit integrierter Suche aufbauen.

- Erfassung von Daten aus Git, Confluence, Jira und Slack mithilfe von Datastore-Plugins
- Bereitstellung einer benutzerfreundlichen Sucherfahrung für Entwickler durch Labels
- Steuerung der Informationspriorisierung durch Document-Boost
- Betriebliche Aspekte wie API-Ratenbegrenzungen und Token-Verwaltung

Mit dem Knowledge-Hub für Entwicklungsteams schaffen Sie eine Umgebung, in der Fragen wie "Wo wurde das diskutiert?" oder "Wo ist diese Spezifikation?" schnell beantwortet werden können.

Im nächsten Teil behandeln wir die übergreifende Suche in Cloud-Speicherdiensten.

Referenzen
==========

- `Fess Datastore-Konfiguration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin-Verwaltung <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
