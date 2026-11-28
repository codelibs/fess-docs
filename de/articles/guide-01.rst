======================================
Was Fess kann und wie Sie es einführen
======================================

Einführung
==========

Interne Dokumente sind auf Websites, Dateiserver, Cloud-Speicher, SaaS-Dienste wie Chat- und Ticketsysteme sowie Datenbanken verteilt.
Auch wenn jedes dieser Werkzeuge eine eigene Suche hat, lässt sich nicht über alle Orte hinweg auf einmal suchen.
Fess ist ein Suchserver, der die Dokumente aus diesen Quellen in einem einzigen Index zusammenführt, sodass sie sich über eine Suchseite oder eine API durchsuchen lassen.

Dieser Artikel richtet sich an IT-Verantwortliche und Entwickler, die die Einführung von Fess erwägen, und erklärt Folgendes:

- Woraus Fess besteht und wie es funktioniert
- Welche Funktionen von Haus aus verfügbar sind und welche zusätzliche Plugins benötigen
- Welche Artikel Sie je nach Ziel als Nächstes lesen sollten

Die Einrichtungsschritte der einzelnen Funktionen werden in den jeweiligen Artikeln behandelt.

Von diesem Praxisleitfaden abgedeckte Version
=============================================

Alle Artikel dieses Praxisleitfadens beziehen sich auf Fess 15.9.
Feldnamen in der Oberfläche, Konfigurationsschlüssel und Standardwerte wurden mit 15.9 überprüft.
Wenn ein Artikel eine Funktion vorstellt, die erst ab 15.10 verfügbar ist, weist er ausdrücklich darauf hin.

Links auf die Referenzdokumentation beginnen mit ``https://fess.codelibs.org/de/stable/`` und verweisen auf die Dokumentation der aktuellen stabilen Version.
Wenn Sie eine andere Version verwenden, ersetzen Sie ``stable`` in der URL durch die Versionsnummer (z. B. ``15.9``) und prüfen Sie Feldnamen und Standardwerte auf dieser Seite.

Was ist Fess?
=============

Fess ist ein in Java geschriebener Open-Source-Volltextsuchserver.
Er steht unter der Apache License 2.0 und kann auch in kommerziellen Umgebungen kostenlos verwendet werden.

Zum Speichern und Durchsuchen der Dokumente verwendet Fess OpenSearch.
Fess 15.9 prüft beim Start das verbundene System und bricht den Start ab, wenn es sich nicht um OpenSearch 3 oder höher handelt.
Mit OpenSearch 2 oder älter sowie mit Elasticsearch kann Fess keine Verbindung herstellen.
In 15.9 wurde die bisher in Fess eingebettete Suchmaschine entfernt, daher müssen Sie OpenSearch immer separat bereitstellen (in der Docker-Konfiguration wird ein OpenSearch-Container zusammen mit Fess gestartet).

Eine einzelne Fess-Instanz umfasst Folgendes:

- Crawler, die Dokumente sammeln (Web, Dateiserver und verschiedene Dienste über Plugins)
- Eine Administrationsoberfläche, in der Sie Crawl-Einstellungen, Benutzer, Berechtigungen, Wörterbücher, Zeitpläne und mehr konfigurieren
- Eine Suchseite für die Benutzer
- APIs (``/api/v2/``), mit denen externe Systeme Suche und Vorschläge aufrufen können

Die Suchseite wird von einem statischen Theme dargestellt, das HTML, CSS und JavaScript bündelt.
Fess wird mit dem Theme ``bootstrap`` ausgeliefert; weitere Themes fügen Sie als ZIP-Datei unter [System] > [Theme] hinzu.

Aufbau von Fess
===============

Beim Betrieb von Fess sind die folgenden Komponenten beteiligt.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Komponente
     - Aufgabe
   * - Fess selbst (Webanwendung)
     - Stellt die Suchseite, die Administrationsoberfläche und die APIs bereit. Hier läuft auch der Scheduler, der Jobs wie Crawls zu den eingestellten Zeiten startet
   * - Crawler (separater Prozess)
     - Crawl-Jobs werden als von Fess getrennte Java-Prozesse gestartet. Sie rufen Webseiten und Dateien ab, extrahieren den Text und registrieren ihn in OpenSearch. Auch die Jobs zum Erstellen von Vorschlägen, zum Erzeugen von Miniaturansichten und zum Erstellen von Vektoren für die semantische Suche laufen auf dieselbe Weise als separate Prozesse
   * - OpenSearch
     - Hält den Index der zu durchsuchenden Dokumente und führt die Suchen aus. Auch ein Großteil der in der Administrationsoberfläche registrierten Informationen, etwa Crawl-Einstellungen, Benutzer, Job-Logs und Suchlogs, wird hier gespeichert

Da der Crawler ein separater Java-Prozess ist, wird sein Arbeitsspeicher getrennt von Fess selbst konfiguriert (behandelt in :doc:`guide-14`).

Bis Dokumente durchsuchbar sind, läuft Folgendes ab:

1. Sie registrieren in der Administrationsoberfläche eine Crawl-Konfiguration (Ziel-URLs oder -Pfade, die Berechtigungen, die festlegen, wer die Ergebnisse sehen darf, usw.)
2. Der Scheduler startet den Crawl-Job. Sie können ihn auch manuell in der Administrationsoberfläche mit [Jetzt starten] starten
3. Der Crawler ruft die Dokumente ab, extrahiert den Text und registriert ihn zusammen mit den Berechtigungen in OpenSearch
4. Wenn ein Benutzer sucht, filtert Fess die Ergebnisse nach den Rollen und Gruppen des Benutzers, bevor es sie zurückgibt

Den gesamten Ablauf vom Start mit Docker über das Crawlen bis zur Suche können Sie in :doc:`guide-02` selbst ausprobieren.

Kernfunktionen und Plugins
==========================

In Fess 15.9 werden viele Funktionen als von Fess getrennte Plugins bereitgestellt.
Ob die benötigten Plugins bereits installiert sind, hängt von der Installationsart ab.

- Ein aus ZIP, RPM oder DEB installiertes Fess enthält keinerlei Plugins
- Das Standard-Docker-Image (z. B. ``ghcr.io/codelibs/fess:15.9.0``) enthält die folgenden sieben Plugins vorinstalliert: ``fess-script-groovy``, ``fess-storage-s3``, ``fess-storage-gcs``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``, ``fess-sso-oidc``
- Das schlanke Docker-Image (z. B. ``15.9.0-slim``) enthält keine Plugins

Die folgende Tabelle fasst die wichtigsten Funktionen und die dafür nötigen Plugins zusammen.

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Funktion
     - Mit Fess allein verfügbar
     - Benötigt ein Plugin
   * - Crawlen
     - Web (http und https), Dateisysteme, Dateiserver (SMB), FTP
     - Amazon S3 (``fess-storage-s3``), Google Cloud Storage (``fess-storage-gcs``), Web-Crawling, das JavaScript in einem Browser ausführt, um Seiten abzurufen (``fess-crawler-playwright``)
   * - SaaS, Datenbanken usw.
     - Die Konfigurationsseite für Datenspeicher und der Mechanismus zu ihrer Ausführung
     - Ein Datenspeicher-Plugin (``fess-ds-*``) für jede einzubindende Quelle. Slack, Confluence und Jira, Google Drive, Microsoft 365, Box, Datenbanken, CSV, Git und mehr
   * - Anmeldung und Berechtigungen
     - In Fess registrierte Benutzer, Rollen und Gruppen sowie die Anbindung an LDAP / Active Directory
     - SSO (``fess-sso-oidc`` für OpenID Connect, ``fess-sso-saml`` für SAML, ``fess-sso-entraid`` für Entra ID, ``fess-sso-spnego`` für SPNEGO)
   * - Skripte
     - JavaScript
     - Groovy (``fess-script-groovy``), OGNL (``fess-script-ognl``)
   * - Suchseite
     - Das mitgelieferte Theme ``bootstrap``
     - Statt eines Plugins fügen Sie eine Theme-ZIP-Datei hinzu
   * - APIs
     - ``/api/v2/`` (Suche, Labels, Vorschläge, beliebte Wörter, Health Check und mehr) und die Admin-API
     - ``/api/v1/`` (``fess-webapp-v1-api``), ``/json`` und ``/suggest`` (``fess-webapp-classic-api``). Fess Site Search verwendet ``/api/v1/`` und benötigt daher ``fess-webapp-v1-api``
   * - KI
     - Die Mechanismen für die semantische Suche und den KI-Suchmodus (RAG). Wenn Sie ein in OpenSearch bereitgestelltes Embedding-Modell verwenden, braucht die semantische Suche kein Plugin
     - Anbindung an LLMs und externe Embedding-Modelle (``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``), MCP-Server (``fess-webapp-mcp``), Bildsuche (``fess-webapp-multimodal``)

Von den Einträgen der Spalte „Benötigt ein Plugin“ sind im Standard-Docker-Image nur S3 und GCS, die vier SSO-Arten und Groovy enthalten.
Alles andere muss unabhängig von der Installationsart zusätzlich installiert werden.

Konfigurationen, deren Skripttyp auf Groovy gesetzt ist, sowie aus früheren Versionen übernommene Konfigurationen ohne gespeicherten Skripttyp werden als Groovy ausgeführt.
Dafür ist ``fess-script-groovy`` erforderlich.
Bei neu angelegten Datenspeicher-Konfigurationen ist der Skripttyp standardmäßig JavaScript.

Plugins installieren Sie auf eine der folgenden Arten.
Starten Sie Fess nach dem Installieren oder Entfernen eines Plugins neu.
Die Plugin-Version richtet sich nach der Fess-Version (15.9.x für Fess 15.9).

- In der Administrationsoberfläche unter [System] > [Plugin] auf [Installieren] klicken und das Plugin aus der Liste auswählen
- Auf der Kommandozeile ``bin/fess-setup install plugin <Plugin-Name>:<Version>`` ausführen
- Bei Docker die Umgebungsvariable ``FESS_PLUGINS`` mit einer durch Leerzeichen getrennten Liste wie ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0`` setzen

Die Verwendung von Datenspeicher-Plugins wird in :doc:`datastore-basics` erklärt, das Schreiben eigener Plugins in :doc:`guide-17`.

Durchsuchbare Dateiformate
==========================

Der Text wird mit Extraktionsverfahren wie Apache Tika aus den Dateien gewonnen.
Durchsuchbar sind unter anderem HTML, PDF, Microsoft-Office-Dokumente, Text und der Inhalt von Archivdateien.
Eine Liste der geprüften Formate finden Sie unter `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__.

Text in Bildern und in eingescannten PDFs ist standardmäßig nicht durchsuchbar.
Er wird durchsuchbar, wenn Sie ``tesseract`` auf dem Host installieren, auf dem der Crawler läuft, und OCR aktivieren.
Die Schritte finden Sie unter `OCR-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-ocr.html>`__.

Die Installationsart wählen
===========================

Fess wird als Docker-Image sowie als ZIP-, RPM- und DEB-Paket verteilt.
Zum Ausprobieren ist Docker am schnellsten, weil Fess und OpenSearch gemeinsam gestartet werden.
Die Schritte sind in :doc:`guide-02` beschrieben.

Im Produktivbetrieb können Sie OpenSearch auch als separaten Server oder Cluster bereitstellen.
Die erforderlichen Java- und OpenSearch-Versionen sowie Richtwerte für CPU, Arbeitsspeicher und Festplatte finden Sie unter `Systemanforderungen <https://fess.codelibs.org/de/stable/install/prerequisites.html>`__.

Lesewege nach Ziel
==================

Die Artikel sind so gegliedert, dass Sie sie entsprechend Ihrem Ziel lesen können.
Wählen Sie die Zeile, die Ihrem Ziel am nächsten kommt, und lesen Sie die Artikel von links nach rechts.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Ziel
     - Zu lesende Artikel
   * - Fess zuerst ausprobieren
     - :doc:`guide-02`
   * - Dateiserver durchsuchen
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - Daten aus der Cloud und aus SaaS-Diensten durchsuchen
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - Suche in eine bestehende Website oder ein bestehendes System einbinden
     - :doc:`guide-03` → :doc:`guide-11`
   * - Je nach Abteilung oder Benutzer unterschiedliche Informationen anzeigen
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - Die Suche mit KI erweitern
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - Den Produktivbetrieb aufnehmen
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

Außerdem gibt es die folgenden Artikel:

- Suchqualität verbessern: :doc:`guide-08`, :doc:`guide-09`, :doc:`guide-22`
- Bilder und Text gemeinsam durchsuchen: :doc:`guide-21`
- Eigene Plugins schreiben: :doc:`guide-17`
- Den unternehmensweiten Rollout planen: :doc:`guide-23`
- Anwendungsfälle und Vergleiche mit anderen Produkten: :doc:`use-cases`, :doc:`comparison`

Eine Liste aller Artikel finden Sie auch auf der Seite :doc:`../guide`.

Referenzen
==========

- `Fess-Dokumentation (stabile Version) <https://fess.codelibs.org/de/stable/>`__
- `Systemanforderungen <https://fess.codelibs.org/de/stable/install/prerequisites.html>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `Plugin-Architektur <https://fess.codelibs.org/de/stable/dev/plugin-architecture.html>`__
- `Theme <https://fess.codelibs.org/de/stable/admin/theme-guide.html>`__
- `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess (GitHub) <https://github.com/codelibs/fess>`__
