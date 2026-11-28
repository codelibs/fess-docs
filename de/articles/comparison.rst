=========================================
Fess im Vergleich zu anderen Suchlösungen
=========================================

Einleitung
==========

Wenn Sie eine Suche für interne Dokumente oder eine Website einrichten, kommen neben Suchsystemen wie Fess auch eine Eigenentwicklung auf Basis einer Suchmaschine wie OpenSearch oder Apache Solr, externe Websuchdienste und kommerzielle Enterprise-Search-Produkte infrage.
Dieser Artikel stellt zunächst übersichtlich zusammen, was Fess 15.9 bereitstellt, und vergleicht anschließend, wie sich seine Rolle von den anderen Optionen unterscheidet.

.. note::

   Die Angaben zu Fess beziehen sich auf Version 15.9.
   Bei anderen Produkten und Diensten behandelt dieser Artikel nur architektonische Unterschiede, die sich kaum ändern. Funktionen, Preise und Verfügbarkeit können sich ändern; prüfen Sie daher die aktuelle Dokumentation des jeweiligen Produkts.

Was Fess bereitstellt
=====================

Fess ist ein Suchsystem, das OpenSearch als Suchmaschine verwendet.
Crawler, Administrationsoberfläche, Suchoberfläche und APIs werden als eine einzige Anwendung bereitgestellt; Index und Crawl-Einstellungen werden in OpenSearch gespeichert.
Elasticsearch oder Solr können nicht als Suchmaschine verwendet werden.
Die Lizenz ist die Apache License 2.0.

Viele Funktionen werden als Plugins bereitgestellt, und Sie installieren nur die, die Sie benötigen.
Einträge, deren Spalte „Voraussetzung“ in der folgenden Tabelle leer ist, funktionieren mit Fess allein.

.. list-table::
   :header-rows: 1
   :widths: 22 48 30

   * - Bereich
     - Was 15.9 bereitstellt
     - Voraussetzung
   * - Web-Crawling
     - Crawlt HTTP/HTTPS-Sites. Web-Authentifizierung, Request-Header und Pfadzuordnungen lassen sich konfigurieren
     -
   * - Datei-Crawling
     - Crawlt Pfade mit ``file``, ``smb``, ``smb1`` und ``ftp``
     -
   * - Crawling von Cloud-Speicher
     - ``s3://`` (Amazon S3 und S3-kompatibler Speicher), ``gcs://`` (Google Cloud Storage)
     - ``fess-storage-s3``, ``fess-storage-gcs``
   * - Datenbanken und SaaS
     - Werden über Datenspeicher-Konnektoren übernommen (Liste im nächsten Abschnitt)
     - ``fess-ds-*``-Plugins
   * - Dokumentformate
     - Office-Dokumente, PDF, HTML, Text, Archivdateien und mehr. OCR für Bilder und gescannte PDFs ist standardmäßig deaktiviert
     - Für OCR der Befehl ``tesseract``
   * - Zugriffskontrolle
     - Zeigt Suchergebnisse je nach Rolle, Gruppe und Benutzer unterschiedlich an. Beim SMB- und Datei-Crawling werden die Dateiberechtigungen als Rollen übernommen. Die Anbindung an LDAP (einschließlich Active Directory) ist eine Kernfunktion
     -
   * - Single Sign-on
     - OpenID Connect, SAML, SPNEGO (Kerberos), Microsoft Entra ID
     - ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``, ``fess-sso-entraid``
   * - Suchoberfläche
     - Wird über ein statisches Theme (HTML, CSS und JavaScript als ZIP gepackt) dargestellt. Das mitgelieferte Theme ist ``bootstrap``
     -
   * - API
     - ``/api/v2`` für Suche, Labels, Vorschläge, beliebte Wörter, Health-Check, KI-Suchmodus und mehr; ``/api/admin`` für die Administration
     -
   * - Ältere APIs
     - ``/api/v1``, ``/json`` und ``/suggest``
     - ``fess-webapp-v1-api``, ``fess-webapp-classic-api``
   * - Semantische Suche
     - Teilt den Inhalt in Chunks auf, vektorisiert sie und führt die Ergebnisse per Rank Fusion mit den Ergebnissen der Stichwortsuche zusammen. Standardmäßig deaktiviert
     - Ein Embedding-Modell (OpenSearch ML Commons oder ein ``fess-llm-*``-Plugin)
   * - KI-Suchmodus (RAG)
     - Ein LLM beantwortet Fragen auf Grundlage der Suchergebnisse. Standardmäßig deaktiviert
     - Eines von ``fess-llm-ollama``, ``fess-llm-openai``, ``fess-llm-gemini``, ``fess-llm-bedrock``
   * - MCP-Server
     - Ermöglicht KI-Agenten, Fess über ``/mcp`` zu durchsuchen
     - ``fess-webapp-mcp``
   * - Bildsuche
     - Multimodale Suche, die Bilder (GIF, JPEG, PNG) anhand einer Textbeschreibung findet
     - ``fess-webapp-multimodal`` und ein CLIP-Server

Das Docker-Image enthält die vier SSO-Plugins, ``fess-storage-s3``, ``fess-storage-gcs`` und ``fess-script-groovy``.
Andere Plugins installieren Sie unter [System] > [Plugin] und starten Fess anschließend neu.
Wählen Sie die Plugin-Version passend zur Minor-Version von Fess (15.9.x für 15.9).

Datenspeicher-Konnektoren
-------------------------

Für 15.9 sind die folgenden Datenspeicher-Plugins veröffentlicht.
Die Konfiguration ist in der Referenz des jeweiligen Konnektors beschrieben.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Kategorie
     - Plugin (Ziel)
   * - Cloud-Speicher
     - ``fess-ds-box`` (Box), ``fess-ds-dropbox`` (Dropbox), ``fess-ds-gsuite`` (Google Drive), ``fess-ds-microsoft365`` (OneDrive, SharePoint Online, Teams und mehr)
   * - Zusammenarbeit
     - ``fess-ds-atlassian`` (Confluence, Jira), ``fess-ds-slack`` (Slack), ``fess-ds-notion`` (Notion), ``fess-ds-backlog`` (Backlog), ``fess-ds-sharepoint`` (lokal betriebener SharePoint Server)
   * - Entwicklung und Geschäftssysteme
     - ``fess-ds-git`` (Git-Repositorys), ``fess-ds-salesforce`` (Salesforce)
   * - Daten
     - ``fess-ds-db`` (über JDBC erreichbare Datenbanken), ``fess-ds-csv`` (CSV), ``fess-ds-json`` (JSON), ``fess-ds-wikipedia`` (Wikipedia-Dumps)

Eine hier nicht aufgeführte Datenquelle können Sie durchsuchbar machen, indem Sie ein eigenes Datenspeicher-Plugin schreiben (:doc:`guide-17`) oder Dokumente über die Admin-API registrieren (:doc:`guide-11`).

Vergleich mit einer Eigenentwicklung auf Basis einer Suchmaschine (OpenSearch, Apache Solr)
===========================================================================================

OpenSearch und Apache Solr sind Suchmaschinen.
Sie übernehmen Indexierung und Suche, enthalten aber weder einen Crawler zum Sammeln der Daten noch eine Suchoberfläche für die Benutzer noch eine Zugriffskontrolle pro Dokument.
Diese Teile entwickeln Sie selbst oder kombinieren andere Software.
Für das Web-Crawling gibt es zum Beispiel eigenständige Projekte wie Apache Nutch.

Fess ist eine Anwendung, die diese Teile auf Basis von OpenSearch bereitstellt.
Die Unterschiede sind wie folgt.

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * - Aspekt
     - Fess
     - Eigenentwicklung auf Basis einer Suchmaschine
   * - Datenerfassung
     - Web-, Datei- und Datenspeicher-Crawls werden in der Administrationsoberfläche konfiguriert
     - Crawler und Import-Prozesse selbst bauen oder andere Software kombinieren
   * - Suchoberfläche
     - Wird über ein Theme dargestellt. Um das Aussehen zu ändern, erstellen Sie ein Theme oder bauen über die API eine eigene Oberfläche
     - Frei gestaltbar, aber alles muss entwickelt werden
   * - Zugriffskontrolle
     - Rollen und Dateiberechtigungen werden an jedem Dokument gespeichert, und die Suche wird nach dem angemeldeten Benutzer gefiltert
     - Die Übernahme der Dokumentberechtigungen und die Filterung bei der Suche entwerfen und implementieren
   * - Index-Design
     - Verwendet den von Fess definierten Index. Analyzer für viele Sprachen, darunter Deutsch, sind vorkonfiguriert
     - Frei nach Einsatzzweck gestaltbar
   * - Was Sie betreiben
     - Fess und OpenSearch
     - Die Suchmaschine und alle selbst entwickelten Teile

Wenn Sie den Suchmechanismus von Grund auf entwerfen oder eigene Datenstrukturen durchsuchen möchten, ist die direkte Nutzung einer Suchmaschine besser geeignet.
Wenn das Ziel dagegen ist, Dokumente zu sammeln und im Unternehmen durchsuchbar zu machen, hält ein Start mit Fess, dessen Lücken Sie mit der API oder mit Plugins schließen, den Entwicklungsumfang kleiner.

Fess kann auch an einen bestehenden OpenSearch-Cluster angebunden werden.
Bei Diensten wie Amazon OpenSearch Service, in denen sich die CodeLibs-Plugins nicht installieren lassen, setzen Sie ``search_engine.type`` auf ``aws`` oder ``vanilla``.
In diesem Fall stehen einige Funktionen wie die Wörterbuchverwaltung und die Erkennung doppelter Dokumente nicht zur Verfügung (siehe `Suchmaschinentyp <https://fess.codelibs.org/de/stable/config/search-engine-type.html>`__).

Vergleich mit einer Site-Suche über einen externen Websuchdienst
================================================================

Eine Site-Suche lässt sich auch mit dem Index eines Suchdienstanbieters bereitstellen.
Bei diesem Ansatz sind nur öffentliche Seiten durchsuchbar, die der Crawler des Anbieters abgerufen hat.
Seiten mit Anmeldung und interne Dateiserver lassen sich nicht einbeziehen, und wann gecrawlt wird und in welcher Reihenfolge die Ergebnisse erscheinen, hängt ebenfalls vom Anbieter ab.

Mit Fess legen Sie selbst fest, was wann gecrawlt wird, und der Index liegt in Ihrer eigenen Umgebung.
Zur Feinabstimmung der Suchergebnisse können Sie unter anderem Schlüsselübereinstimmung (bestimmte Dokumente für bestimmte Begriffe weiter oben anzeigen), Dokument-Boost und Verwandte Abfrage verwenden.
Es gibt zwei Möglichkeiten, Fess in eine bestehende Website einzubinden.

- Ein Suchformular platzieren, das zur Suchoberfläche (Theme) von Fess weiterleitet
- Das JavaScript von Fess Site Search (FSS) einbetten, um die Suchergebnisse innerhalb der Seite anzuzeigen

FSS ruft ``/api/v1`` auf; in 15.9 ist daher das Plugin ``fess-webapp-v1-api`` erforderlich.
Die Schritte finden Sie in :doc:`guide-03`.

Vergleich mit kommerziellen Enterprise-Search-Produkten
=======================================================

Beim Vergleich mit kommerziellen Produkten unterscheidet sich der Funktionsumfang von Produkt zu Produkt stark, sodass sich keine allgemeine Aussage darüber treffen lässt, was besser ist.
Wir empfehlen, die infrage kommenden Produkte und Fess unter denselben Bedingungen anhand der folgenden Aspekte zu prüfen.

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Aspekt
     - Bei Fess
   * - Unterstützte Datenquellen
     - Prüfen Sie die Tabelle im vorherigen Abschnitt und die Liste der Datenspeicher-Konnektoren. Fehlt etwas, können Sie ein eigenes Plugin schreiben
   * - Zugriffskontrolle
     - Pro Rolle, Gruppe und Benutzer, mit Unterstützung für LDAP und vier SSO-Verfahren
   * - Generative KI
     - KI-Suchmodus (RAG), semantische Suche und MCP-Server. Das LLM wählen Sie aus Ollama (selbst betrieben), OpenAI, Gemini und Amazon Bedrock
   * - Speicherort der Daten
     - Der Index liegt in einem selbst betriebenen OpenSearch. Wenn Sie externe Dienste für das LLM oder die Embeddings nutzen, werden Fragen und Dokumentinhalte an diese Dienste gesendet
   * - Betriebsmodell
     - Selbst betriebene Software. Installierbar mit Docker, unter Linux (ZIP, RPM, DEB) und unter Windows. Läuft auch auf Kubernetes, es gibt aber kein offizielles Helm-Chart
   * - Kosten und Support
     - Es fallen keine Lizenzkosten an. Die Kosten sind Server und Betriebsaufwand. Kommerziellen Support finden Sie unter `Kommerzieller Support <https://fess.codelibs.org/de/support-services.html>`__
   * - Anpassbarkeit
     - Der Quellcode ist öffentlich, und Fess lässt sich mit Themes, Plugins und der API erweitern

Kommerzielle Produkte eignen sich, wenn das Produkt die benötigten Konnektoren und Verwaltungsfunktionen bereits mitbringt und Sie den Betrieb dem Hersteller überlassen möchten.
Fess eignet sich, wenn Sie eine Suchplattform aus den benötigten Funktionen zusammenstellen und die Daten dabei in Ihrer eigenen Umgebung behalten möchten.

Entscheidungshilfe
==================

Beantworten Sie die folgenden Fragen der Reihe nach, um zu entscheiden, ob Fess infrage kommt.

1. Sind die Daten, die Sie durchsuchen möchten, durch die Crawl-Ziele oder Datenspeicher-Konnektoren von Fess abgedeckt?

   - Falls nicht, schätzen Sie den Entwicklungsaufwand für ein eigenes Plugin (:doc:`guide-17`) oder für die Registrierung über die API (:doc:`guide-11`) ab.

2. Müssen verschiedenen Benutzern unterschiedliche Dokumente angezeigt werden?

   - Zur Nutzung der Berechtigungen des Dateiservers siehe :doc:`file-server-search`, zum Rollendesign :doc:`guide-05` und zu SSO :doc:`guide-15`.

3. Reicht das Theme von Fess für Ihre Suchoberfläche aus?

   - Um die Suche in eine eigene Anwendung einzubinden, verwenden Sie ``/api/v2`` (:doc:`guide-11`).

4. Können Sie Fess und OpenSearch selbst betreiben?

   - Falls nicht, oder wenn Sie den Betrieb einem Hersteller überlassen möchten, ziehen Sie kommerziellen Support für Fess oder ein kommerzielles Produkt in Betracht.

5. Benötigen Sie Antworten durch generative KI oder eine semantische Suche?

   - Legen Sie das zu verwendende LLM fest und prüfen Sie die erforderliche Konfiguration in :doc:`guide-19` und :doc:`guide-18`.

Lauten die Antworten auf 1 und 4 „Ja“, ist es am zuverlässigsten, Fess auszuprobieren und die Suchergebnisse mit Ihren tatsächlichen Dokumenten zu prüfen.

Ausprobieren
============

Eine Vergleichstabelle allein zeigt nicht, wie gut sich Ihre eigenen Dokumente durchsuchen lassen.
Starten Sie Fess mit Docker nach den Schritten in :doc:`guide-02`, crawlen Sie einen Teil der Inhalte, die Sie durchsuchen möchten, und prüfen Sie Folgendes.

- Ob die Zieldokumente indexiert wurden (prüfen Sie unter [Systeminformationen] > [Jobprotokoll] und [Fehler-URL], ob URLs mit Fehlern beendet wurden)
- Ob eine Suche nach häufig verwendeten Begriffen die erwarteten Dokumente oben anzeigt
- Ob Dokumente, die nicht sichtbar sein sollen, beim Wechsel des angemeldeten Benutzers verborgen bleiben (wenn Sie Zugriffskontrolle benötigen)

Weiterführende Artikel
======================

- Aufbau von Fess und Wegweiser durch die Artikel: :doc:`guide-01`
- Fess zuerst lokal ausprobieren: :doc:`guide-02`
- Suche in eine bestehende Website einbinden: :doc:`guide-03`
- Daten aus Datenbanken oder SaaS durchsuchen: :doc:`datastore-basics`
- Berechtigungen des Dateiservers in den Suchergebnissen berücksichtigen: :doc:`file-server-search`
- Generative KI auf Grundlage interner Dokumente antworten lassen: :doc:`guide-19`
- Auf wachsende Datenmengen vorbereiten: :doc:`guide-14`
- Anwendungsbeispiele kennenlernen: :doc:`use-cases`

Referenzen
==========

- `Übersicht der Datenspeicher-Konnektoren <https://fess.codelibs.org/de/stable/config/datastore/ds-overview.html>`__
- `Datei-Crawl (Dateiserver-Suche) <https://fess.codelibs.org/de/stable/admin/fileconfig-guide.html>`__
- `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__
- `OCR-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-ocr.html>`__
- `Theme <https://fess.codelibs.org/de/stable/admin/theme-guide.html>`__
- `API-Übersicht <https://fess.codelibs.org/de/stable/api/api-overview.html>`__
- `Semantische Suche <https://fess.codelibs.org/de/stable/config/search-semantic.html>`__
- `Übersicht über KI-Suchmodus (RAG) und LLM-Integration <https://fess.codelibs.org/de/stable/config/llm-overview.html>`__
- `Suchmaschinentyp <https://fess.codelibs.org/de/stable/config/search-engine-type.html>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
