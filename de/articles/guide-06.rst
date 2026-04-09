============================================================
Teil 6: Knowledge-Hub fuer Entwicklungsteams -- Integrierte Suche ueber Code, Wiki und Tickets
============================================================

Einfuehrung
============

In Softwareentwicklungsteams werden taeglich verschiedene Werkzeuge eingesetzt.
Code liegt in Git-Repositories, Spezifikationen in Confluence, Aufgaben in Jira und die taegliche Kommunikation laeuft ueber Slack.
Jedes dieser Werkzeuge verfuegt ueber eine eigene Suchfunktion, doch wenn die Frage auftaucht: "Wo wurde das nochmal diskutiert?", ist es ineffizient, jedes Tool einzeln zu durchsuchen.

In diesem Artikel zeigen wir, wie Sie die Informationen aus den Werkzeugen, die Ihr Entwicklungsteam taeglich nutzt, in Fess zusammenfuehren und einen Knowledge-Hub mit integrierter Suche aufbauen.

Zielgruppe
==========

- Teamleiter und Infrastrukturverantwortliche in Softwareentwicklungsteams
- Personen, die eine werkzeuguebergreifende Suche ueber entwicklungsrelevante Informationen wuenschen
- Personen, die die grundlegende Verwendung von Datastore-Plugins kennenlernen moechten

Szenario
========

Wir richten eine integrierte Suche fuer ein Entwicklungsteam (20 Personen) ein.

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

Beim Datastore-Crawling werden Daten ueber die API des jeweiligen Werkzeugs abgerufen und im Fess-Index registriert.
Fess stellt fuer jedes Werkzeug ein eigenes Datastore-Plugin bereit.

Plugin-Installation
====================

Datastore-Plugins koennen ueber die Fess-Verwaltungsoberflaeche installiert werden.

1. Waehlen Sie in der Verwaltungsoberflaeche [System] > [Plugins]
2. Ueberpruefen Sie die Liste der bereits installierten Plugins
3. Klicken Sie auf [Installieren], um zum Installationsbildschirm zu gelangen, und installieren Sie die benoetigten Plugins ueber den Tab [Remote]

Fuer das vorliegende Szenario werden die folgenden Plugins verwendet:

- ``fess-ds-git``: Crawling von Git-Repositories
- ``fess-ds-atlassian``: Crawling von Confluence / Jira
- ``fess-ds-slack``: Crawling von Slack-Nachrichten

Konfiguration der einzelnen Datenquellen
==========================================

Git-Repository-Konfiguration
------------------------------

Durch das Crawling von Git-Repositories werden Code und Dokumente durchsuchbar gemacht.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: GitDataStore auswaehlen
3. Parameter konfigurieren

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**Beispiel fuer die Skriptkonfiguration**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

Geben Sie unter ``uri`` die Repository-URL und unter ``username`` / ``password`` die Zugangsdaten an. Bei privaten Repositories setzen Sie einen Zugriffstoken als ``password``. Mit ``include_pattern`` koennen Sie die zu crawlenden Dateierweiterungen per regulaerem Ausdruck einschraenken.

Confluence-Konfiguration
--------------------------

Confluence-Seiten und Blog-Beitraege werden durchsuchbar gemacht.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: ConfluenceDataStore auswaehlen
3. Parameter konfigurieren

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**Beispiel fuer die Skriptkonfiguration**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

Geben Sie unter ``home`` die Confluence-URL an und waehlen Sie unter ``auth_type`` die Authentifizierungsmethode. Bei Confluence Cloud verwenden Sie die ``basic``-Authentifizierung und setzen einen API-Token unter ``basic.password``.

Jira-Konfiguration
--------------------

Jira-Tickets (Issues) werden durchsuchbar gemacht.

Hierfuer wird der JiraDataStore-Handler verwendet, der im selben ``fess-ds-atlassian``-Plugin enthalten ist.
Mit JQL (Jira Query Language) koennen Sie die zu crawlenden Tickets einschraenken.
Beispielsweise koennen Sie nur Tickets eines bestimmten Projekts oder nur Tickets mit einem bestimmten Status (ausser Closed) erfassen.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: JiraDataStore auswaehlen
3. Parameter konfigurieren

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**Beispiel fuer die Skriptkonfiguration**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

Mit ``issue.jql`` geben Sie eine JQL-Abfrage an, um die zu crawlenden Tickets einzuschraenken.

Slack-Konfiguration
--------------------

Slack-Nachrichten werden durchsuchbar gemacht.

1. [Crawler] > [Datastore] > [Neu erstellen]
2. Handler-Name: SlackDataStore auswaehlen
3. Parameter konfigurieren

**Beispiel fuer die Parameterkonfiguration**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**Beispiel fuer die Skriptkonfiguration**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

Geben Sie unter ``token`` den OAuth-Token des Slack-Bots an. Mit ``channels`` legen Sie die zu crawlenden Kanaele fest; um alle Kanaele zu erfassen, setzen Sie ``*all``. Wenn Sie private Kanaele einbeziehen moechten, setzen Sie ``include_private=true`` und stellen Sie sicher, dass der Bot in die entsprechenden Kanaele eingeladen wurde.

Verwendung von Labels
======================

Informationsquellen durch Labels unterscheiden
------------------------------------------------

Durch die Zuweisung von Labels zu den einzelnen Datenquellen koennen Benutzer bei der Suche zwischen den Informationsquellen wechseln.

- ``code``: Code aus Git-Repositories
- ``docs``: Dokumente aus Confluence
- ``tickets``: Tickets aus Jira
- ``discussions``: Nachrichten aus Slack

Benutzer koennen mit "Alle" eine uebergreifende Suche durchfuehren und bei Bedarf ueber Labels filtern.

Verbesserung der Suchqualitaet
================================

Verwendung von Document-Boost
-------------------------------

In einem Knowledge-Hub fuer Entwicklungsteams haben nicht alle Dokumente die gleiche Wichtigkeit.
Beispielsweise ist folgende Priorisierung denkbar:

1. Confluence-Dokumente (offizielle Spezifikationen und Anleitungen)
2. Jira-Tickets (aktuelle Probleme und laufende Aufgaben)
3. Git-Repository (Code und README)
4. Slack-Nachrichten (Diskussionsprotokolle)

Mit Document-Boost koennen Sie den Suchscore von Dokumenten erhoehen, die bestimmte Kriterien erfuellen.
Ueber [Crawler] > [Document-Boost] in der Verwaltungsoberflaeche koennen Sie Boost-Werte basierend auf URL-Mustern oder Labels konfigurieren.

Verwendung verwandter Inhalte
------------------------------

Durch die Anzeige von "verwandten Inhalten" in den Suchergebnissen koennen Sie Benutzer dabei unterstuetzen, die gesuchten Informationen schneller zu finden.
Wenn beispielsweise bei der Suche nach einem Confluence-Entwurfsdokument verwandte Jira-Tickets als "verwandte Inhalte" angezeigt werden, ist dies sehr hilfreich.

Betriebliche Hinweise
======================

Crawl-Zeitplan
---------------

Legen Sie fuer jede Datenquelle eine angemessene Crawl-Haeufigkeit fest.

.. list-table:: Beispiel fuer einen Zeitplan
   :header-rows: 1
   :widths: 25 25 50

   * - Datenquelle
     - Empfohlene Haeufigkeit
     - Begruendung
   * - Confluence
     - alle 4 Stunden
     - Dokumente werden in mittlerer Haeufigkeit aktualisiert
   * - Jira
     - alle 2 Stunden
     - Tickets werden haeufig aktualisiert
   * - Git
     - taeglich
     - Anpassung an den Release-Zyklus
   * - Slack
     - alle 4 Stunden
     - Echtzeit ist nicht erforderlich, aber Aktualitaet ist wichtig

Umgang mit API-Ratenbegrenzungen
---------------------------------

Die APIs von SaaS-Werkzeugen unterliegen Ratenbegrenzungen.
Stellen Sie die Crawl-Intervalle so ein, dass die API-Ratenbegrenzungen nicht ueberschritten werden.
Insbesondere die Slack API hat strenge Ratenbegrenzungen, weshalb es wichtig ist, grosszuegige Crawl-Intervalle einzuplanen.

Verwaltung von Zugriffstokens
-------------------------------

Fuer die Konfiguration der Datastore-Plugins werden API-Zugriffstokens der jeweiligen Werkzeuge benoetigt.
Beachten Sie aus Sicherheitsgruenden die folgenden Punkte:

- Prinzip der minimalen Berechtigung: Verwenden Sie Zugriffstokens mit ausschliesslich Lesezugriff
- Regelmaessige Rotation: Erneuern Sie Tokens in regelmaessigen Abstaenden
- Verwendung dedizierter Konten: Nutzen Sie Servicekonten anstelle persoenlicher Konten

Zusammenfassung
================

In diesem Artikel haben wir gezeigt, wie Sie die Informationen aus den Werkzeugen, die Ihr Entwicklungsteam taeglich nutzt, in Fess zusammenfuehren und einen Knowledge-Hub mit integrierter Suche aufbauen.

- Erfassung von Daten aus Git, Confluence, Jira und Slack mithilfe von Datastore-Plugins
- Bereitstellung einer benutzerfreundlichen Sucherfahrung fuer Entwickler durch Labels
- Steuerung der Informationspriorisierung durch Document-Boost
- Betriebliche Aspekte wie API-Ratenbegrenzungen und Token-Verwaltung

Mit dem Knowledge-Hub fuer Entwicklungsteams schaffen Sie eine Umgebung, in der Fragen wie "Wo wurde das diskutiert?" oder "Wo ist diese Spezifikation?" schnell beantwortet werden koennen.

Im naechsten Teil behandeln wir die uebergreifende Suche in Cloud-Speicherdiensten.

Referenzen
==========

- `Fess Datastore-Konfiguration <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess Plugin-Verwaltung <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
