=============================================
Anwendungsfälle und Einsatzszenarien für Fess
=============================================

Einleitung
==========

Diese Seite stellt typische Einsatzsituationen von Fess vor, gegliedert nach Branche, nach Größe und nach technischem Ziel.
Zu jedem Szenario werden das zu lösende Problem, die verwendeten Fess-Funktionen und Plugins sowie die Artikel genannt, die die Schritte erklären.
Die eigentlichen Konfigurationsschritte stehen in den jeweiligen Artikeln; wählen Sie also das Szenario, das Ihrer Situation am nächsten kommt, und lesen Sie die dort genannten Artikel.

Die Namen von Funktionen und Plugins in diesem Artikel entsprechen Fess 15.9.
In 15.9 werden der Import aus Datenbanken und SaaS-Diensten, SSO sowie das Crawlen von S3 und GCS durch Plugins bereitgestellt.
Verwenden Sie für Plugins dieselbe Version 15.9.x wie für Fess und starten Sie Fess nach der Installation neu.
Wie Sie Plugins installieren, lesen Sie unter `Plugins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__.

.. note::

   Die folgenden Abschnitte beschreiben allgemeine Einsatzmuster. Für konkrete Einführungsbeispiele wenden Sie sich bitte an den `kommerziellen Support <../support-services.html>`__.

Funktionen nach Ziel finden
===========================

.. list-table::
   :header-rows: 1
   :widths: 34 38 28

   * - Was Sie tun möchten
     - Funktionen und Plugins
     - Zu lesende Artikel
   * - Zuerst lokal ausprobieren
     - Docker Compose (docker-fess)
     - :doc:`guide-02`
   * - Intranet-Website und Dateiserver gemeinsam durchsuchen
     - Web-Crawling, Dateisystem-Crawling, Datei-Authentifizierung, Labels
     - :doc:`guide-04`, :doc:`file-server-search`
   * - Je nach Abteilung oder Position andere Dokumente anzeigen
     - Berechtigungen, Rollen und Gruppen, LDAP (Active Directory)
     - :doc:`guide-05`
   * - Ein Suchfeld in eine bestehende Website einbauen
     - Suchformular, Fess Site Search (``fess-webapp-v1-api``), Themes
     - :doc:`guide-03`
   * - Git, Confluence, Jira und Slack durchsuchen
     - ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack``
     - :doc:`datastore-basics`, :doc:`guide-06`
   * - Google Drive, SharePoint Online und Box durchsuchen
     - ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box``
     - :doc:`datastore-basics`, :doc:`guide-07`
   * - Datenbanken, CSV und Salesforce durchsuchen
     - ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce``
     - :doc:`datastore-basics`, :doc:`guide-12`
   * - Aus Geschäftsanwendungen heraus suchen
     - Such-API (``/api/v2``), Zugriffstoken
     - :doc:`guide-11`
   * - Mit der unternehmensweiten Anmeldung suchen lassen
     - ``fess-sso-entraid``, ``fess-sso-oidc``, ``fess-sso-saml``, ``fess-sso-spnego``
     - :doc:`guide-15`
   * - Eine Fess-Instanz für mehrere Organisationen nutzen
     - Virtuelle Hosts, Rollen, Labels
     - :doc:`guide-13`
   * - Begriffe ohne Treffer und das Suchverhalten untersuchen und verbessern
     - [Systeminformationen] > [Suchprotokoll]
     - :doc:`guide-08`
   * - Dokumente mit ähnlicher Bedeutung finden, Antworten von einer KI erhalten
     - Semantische Suche, KI-Suchmodus, ``fess-webapp-mcp``
     - :doc:`guide-18`, :doc:`guide-19`, :doc:`guide-20`
   * - Auf mehr Dokumente und Nutzer vorbereiten
     - OpenSearch auslagern und clustern, mehrere Fess-Server betreiben
     - :doc:`guide-14`
   * - Stabil im Produktivbetrieb laufen
     - ``/api/v2/health``, Sicherung, Protokolle
     - :doc:`guide-10`

Anwendungsfälle nach Branche
============================

Fertigung: Verstreute technische Dokumente finden
-------------------------------------------------

**Problem**: Konstruktionsunterlagen, Spezifikationen und Qualitätsaufzeichnungen liegen verteilt auf den Dateiservern der einzelnen Abteilungen, und es dauert lange, zugehörige Unterlagen anhand einer Zeichnungs- oder Modellnummer zu finden.

**Verwendete Funktionen**:

- Crawlen Sie die Dateiserver mit ``smb://``, damit der Text von PDFs und Office-Dokumenten durchsuchbar wird. Windows-Zugriffsrechte (ACLs) werden standardmäßig als Berechtigungen der Dokumente übernommen
- Legen Sie Labels mit Anzeigenamen wie „Konstruktion“ und „Qualität“ an, ordnen Sie die Dokumente über die erfassten Pfade zu und ermöglichen Sie so das Eingrenzen auf der Suchseite
- Eingescannte Papierunterlagen werden im Text durchsuchbar, wenn Sie OCR aktivieren. OCR ist standardmäßig deaktiviert und erfordert ``tesseract`` auf dem Host, auf dem der Crawler läuft (`OCR-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-ocr.html>`__)

Dateien in Formaten, aus denen Fess keinen Text extrahieren kann, werden nur über Dateinamen oder Pfad gefunden.
Welche Formate unterstützt werden, sehen Sie unter `Unterstützte Dateien <../supported-files.html>`__.

**Zu lesende Artikel**: Bauen Sie die Konfiguration mit :doc:`guide-04` auf, prüfen Sie die Voraussetzungen für ACLs in :doc:`file-server-search` und richten Sie die abteilungsabhängige Anzeige mit :doc:`guide-05` ein.

Finanzen und Versicherungen: Richtlinien und Verträge mit Berechtigungen finden
-------------------------------------------------------------------------------

**Problem**: Es gibt eine große Menge interner Richtlinien, Handbücher und Verträge, und bei jeder Anfrage oder Prüfung kostet die Suche Zeit. Gleichzeitig soll streng nach Abteilung getrennt werden, wer sie lesen darf.

**Verwendete Funktionen**:

- Mit Berechtigungen pro Dokument schränken Sie ein, wem ein Dokument in den Suchergebnissen angezeigt wird. Die Berechtigungen einer neuen Crawl-Konfiguration enthalten von Anfang an ``{role}guest``; entfernen Sie diesen Eintrag bei nicht öffentlichen Dokumenten
- Damit nicht angemeldete Nutzer nicht suchen können, aktivieren Sie unter [Allgemein] die Option „Anmeldung erforderlich“
- Für die Anmeldung über die unternehmensweite Identitätsplattform verwenden Sie SSO: ``fess-sso-saml`` für SAML, ``fess-sso-entraid`` für Entra ID (das Docker-Image enthält die vier SSO-Plugins)
- Wenn Sie aus Geschäftsanwendungen heraus suchen, hinterlegen Sie das Zugriffstoken auf der Serverseite und rufen die Such-API auf

**Zu lesende Artikel**: Entwerfen Sie die Berechtigungen mit :doc:`guide-05` und richten Sie SSO und HTTPS mit :doc:`guide-15` ein. Die Anbindung an Geschäftsanwendungen behandelt :doc:`guide-11`.

Bildungseinrichtungen: Hochschulwebsites und geteilte Laufwerke übergreifend durchsuchen
----------------------------------------------------------------------------------------

**Problem**: Die Websites der Fakultäten, Vorlesungsunterlagen und interne Hochschuldokumente liegen an verschiedenen Orten, und weder Studierende noch Mitarbeitende finden die gesuchten Informationen.

**Verwendete Funktionen**:

- Erfassen Sie die Hochschulwebsites per Web-Crawling. Für institutionelle Repositorien (etwa DSpace) gibt es keinen eigenen Connector; crawlen Sie daher deren öffentliche Seiten
- Erfassen Sie geteilte Ablagen in Google Drive mit ``fess-ds-gsuite`` und SharePoint Online mit ``fess-ds-microsoft365``
- Um Studierenden und Mitarbeitenden unterschiedliche Bereiche anzuzeigen, trennen Sie diese über Rollen und Berechtigungen. Wenn Sie die Website selbst aufteilen möchten, verwenden Sie virtuelle Hosts

**Zu lesende Artikel**: :doc:`guide-04`, :doc:`guide-07`, :doc:`guide-05`. Zum Aufteilen der Website :doc:`guide-13`.

IT und Software: Entwicklungsinformationen an einer Stelle finden
-----------------------------------------------------------------

**Problem**: Code liegt in Git, Entwürfe in Confluence, Tickets in Jira und Diskussionen in Slack oder Teams, sodass sich frühere Entscheidungen schwer nachvollziehen lassen.

**Verwendete Funktionen**:

- Erfassen Sie Repository-Dateien mit ``fess-ds-git``, Confluence und Jira mit ``fess-ds-atlassian`` und Slack-Nachrichten mit ``fess-ds-slack``
- Kanäle und Chats in Teams lassen sich mit dem ``TeamsDataStore`` von ``fess-ds-microsoft365`` erfassen (`Microsoft 365-Connector <https://fess.codelibs.org/de/stable/config/datastore/ds-microsoft365.html>`__)
- Als auf die Quellcodesuche spezialisierte Konfiguration ist `docker-codesearch <https://github.com/codelibs/docker-codesearch>`__ verfügbar
- Um die Suche in interne Werkzeuge einzubetten, verwenden Sie die Such-API; um KI-Agenten suchen zu lassen, verwenden Sie ``fess-webapp-mcp``

**Zu lesende Artikel**: :doc:`datastore-basics`, danach :doc:`guide-06`. Die Anbindung von KI-Agenten behandelt :doc:`guide-20`.

Anwendungsfälle nach Größe
==========================

Wie viele Server und wie viel Arbeitsspeicher Sie brauchen, hängt nicht allein von der Zahl der Nutzer oder Dokumente ab.
Die Last ändert sich mit der Länge der Texte, dem Anteil der Anhänge und damit, ob die Nutzer angemeldet suchen. Beginnen Sie daher klein, messen Sie und erweitern Sie, was fehlt.
Das Vorgehen bei der Entscheidung ist im Abschnitt über Richtwerte zur Größe in :doc:`guide-14` zusammengefasst.
Die empfohlenen Serveranforderungen für den Produktivbetrieb (4 oder mehr CPU-Kerne, 8 GB oder mehr Arbeitsspeicher usw.) finden Sie unter `Systemanforderungen <https://fess.codelibs.org/de/stable/install/prerequisites.html>`__.

Mit einem Server beginnen
-------------------------

Für die Einführung in einer Abteilung oder einen Testbetrieb lassen Sie Fess und OpenSearch auf einem einzigen Server laufen.
Mit Docker Compose starten Sie mit den zwei Dateien ``compose.yaml`` und ``compose-opensearch3.yaml``.
Die Schritte stehen in :doc:`guide-02`.

Auch bei einem einzelnen Server sollten Sie die folgenden zwei Punkte von Anfang an festlegen.

- Wie Sie Sicherungen erstellen. Die Einstellungen lassen sich unter [Systeminformationen] > [Sicherung] herunterladen, Wörterbücher sind jedoch nicht enthalten (:doc:`guide-10`)
- Bei Docker werden Einstellungen, die Sie unter [System] > [Allgemein] ändern, in ``system.properties`` im Container gespeichert und gehen beim Neuerstellen des Containers verloren (siehe den Abschnitt über Stoppen und Neustarten in :doc:`guide-02`)

Wenn weitere Abteilungen hinzukommen
------------------------------------

Wenn Suche oder Crawling langsam werden, klären Sie zuerst, ob die Ursache bei Fess selbst, beim Crawler oder bei OpenSearch liegt.
In den meisten Fällen erweitern Sie in der folgenden Reihenfolge.

1. Auf dem einzelnen Server die Heap-Größen von Fess, Crawler und OpenSearch sowie die Parallelität des Crawlings anpassen
2. OpenSearch auf einen eigenen Server auslagern
3. OpenSearch zu einem Cluster aus drei Knoten ausbauen
4. Mehrere Fess-Server betreiben und die Anfragen per Load Balancer verteilen

Bei mehreren Fess-Servern halten Sie die Einstellungen unter [Allgemein], ``app.cipher.key`` in ``fess_config.properties`` und die installierten Plugins auf allen Servern identisch.
In Fess 15.9 werden Anmeldesitzungen im Arbeitsspeicher des jeweiligen Servers gehalten. Wenn Sie Seiten verteilen, auf denen Nutzer angemeldet arbeiten, aktivieren Sie daher Sticky Sessions am Load Balancer.
Sitzungen in OpenSearch zu speichern und serverübergreifend zu teilen, ist ab 15.10 möglich.

**Zu lesende Artikel**: :doc:`guide-14`, :doc:`guide-10`.

Unternehmensweit einsetzen
--------------------------

Im unternehmensweiten Maßstab sollten Sie zusätzlich zur obigen Konfiguration Folgendes berücksichtigen.

- Legen Sie einen Fess-Server für das Crawling fest (``scheduler.target.name`` und „Ziel“ des Jobs). So belastet das Crawling nicht die Server, die Suchanfragen beantworten
- Verwenden Sie ``/api/v2/health`` für den Load Balancer und das Monitoring. Der Endpunkt liefert 503, wenn der OpenSearch-Cluster ``RED`` ist oder nicht erreichbar ist
- Um Suchseite oder Suchziele je Organisation zu trennen, verwenden Sie virtuelle Hosts oder getrennte Fess-Instanzen (:doc:`guide-13`)
- Prüfen Sie im Suchprotokoll regelmäßig Begriffe ohne Treffer und Begriffe, deren Ergebnisse nicht angeklickt werden (:doc:`guide-08`)

Fess lässt sich auch auf Kubernetes betreiben, ein offizielles Helm-Chart gibt es jedoch nicht.
Konvertieren Sie die Docker-Compose-Dateien oder erstellen Sie die Manifeste selbst (siehe die FAQ in `Docker-Installation (Details) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__).

Für Einführungen in großen Umgebungen ziehen Sie auch den `kommerziellen Support <../support-services.html>`__ in Betracht.

Technische Anwendungsfälle
==========================

Interne Wikis und Wissensdatenbanken übergreifend durchsuchen
-------------------------------------------------------------

Wie Inhalte erfasst werden, hängt von der Art des Wikis ab.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Ziel
     - Art der Erfassung
     - Referenz
   * - Confluence
     - ``fess-ds-atlassian`` (``ConfluenceDataStore``)
     - :doc:`guide-06`
   * - Notion
     - ``fess-ds-notion``
     - `Notion-Connector <https://fess.codelibs.org/de/stable/config/datastore/ds-notion.html>`__
   * - Backlog
     - ``fess-ds-backlog``
     - `Backlog-Connector <https://fess.codelibs.org/de/stable/config/datastore/ds-backlog.html>`__
   * - Im Web lesbare Wikis wie MediaWiki
     - Web-Crawling (bei erforderlicher Anmeldung zusätzlich Web-Authentifizierung einrichten)
     - :doc:`guide-04`

Auch Dokumente, die über einen Datenspeicher erfasst werden, enthalten von Anfang an ``{role}guest`` in ihren Berechtigungen.
Wenn Sie Bereiche erfassen, die nur ein eingeschränkter Personenkreis lesen darf, lesen Sie zuerst den Abschnitt in :doc:`guide-06` darüber, wem die Suchergebnisse angezeigt werden.

Dateiserver einheitlich durchsuchen
-----------------------------------

Das Datei-Crawling in Fess 15.9 unterstützt die folgenden Protokolle.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Pfadformat
     - Ziel
   * - ``smb://``
     - Freigegebene Windows-Ordner oder NAS-Geräte, die über SMB freigegeben sind
   * - ``smb1://``
     - Ältere Server, die nur SMB1 unterstützen
   * - ``file:``
     - Verzeichnisse, die vom Fess-Server aus sichtbar sind. NFS-Freigaben binden Sie zuerst im Betriebssystem ein und geben sie dann in diesem Format an
   * - ``ftp://``
     - FTP-Server
   * - ``s3://`` / ``gcs://``
     - Amazon-S3-kompatibler Speicher / Google Cloud Storage. Erfordert ``fess-storage-s3`` / ``fess-storage-gcs`` (im Docker-Image enthalten)

Standardmäßig aktiviert sind ``file``, ``smb``, ``smb1`` und ``ftp`` (``crawler.file.protocols``).
Damit SMB-ACLs in den Suchergebnissen berücksichtigt werden, müssen Sie ``{role}guest`` aus den Berechtigungen der Crawl-Konfiguration entfernen.
Den Grund und die Prüfmethode finden Sie in :doc:`file-server-search`, die konkreten Einstellungen in :doc:`guide-04`.

Suche innerhalb einer Website
-----------------------------

Es gibt drei Wege, eine öffentliche Website mit einer Suche auszustatten, und sie lassen sich kombinieren.

- Ein Suchformular platzieren, das auf die Suchseite von Fess weiterleitet. Auf der Fess-Seite ist keine zusätzliche Konfiguration nötig
- Mit Fess Site Search (FSS) die Suchergebnisse innerhalb einer bestehenden Seite anzeigen. FSS ruft ``/api/v1`` auf und benötigt daher in 15.9 das Plugin ``fess-webapp-v1-api``. Das JavaScript von FSS wird nicht von Fess ausgeliefert; erzeugen Sie es mit dem FSS JS Generator und legen Sie es auf Ihrer eigenen Website ab
- Die Suchseite von Fess per Theme an das Erscheinungsbild der bestehenden Website anpassen

Die Schritte stehen in :doc:`guide-03`.
Für eine eigene Suchseite verwenden Sie ``/api/v2/search`` (:doc:`guide-11`).

Datenbanken durchsuchen
-----------------------

Informationen aus Datenbanken, etwa Produktstammdaten oder FAQs, erfassen Sie mit ``fess-ds-db``.
Unterstützt werden JDBC-fähige Datenbanken (MySQL, PostgreSQL, Oracle, SQL Server usw.); einen zur Zieldatenbank passenden JDBC-Treiber stellen Sie separat bereit.
Ein Skript ordnet die per SELECT-Anweisung abgerufenen Spalten Feldern wie ``title`` und ``content`` zu.

Wenn Sie die URL der ursprünglichen Anwendungsseite zusammensetzen und in ``url`` speichern, können Nutzer die Originaldaten direkt über den Link im Suchergebnis öffnen.
Die Schritte stehen in :doc:`guide-12`.

Mit generativer KI kombinieren
------------------------------

- Dokumente mit ähnlicher Bedeutung finden, auch wenn die Stichwörter nicht übereinstimmen: semantische Suche (:doc:`guide-18`)
- Eine KI auf Grundlage interner Dokumente antworten lassen: KI-Suchmodus. Er funktioniert auch ohne Vektorsuche (:doc:`guide-19`)
- KI-Agenten wie Claude Code in Fess suchen lassen: ``fess-webapp-mcp`` (:doc:`guide-20`)

Bei allen Methoden werden die durchsuchten Dokumente mit denselben Berechtigungen gefiltert wie bei der normalen Suche (im KI-Suchmodus die des angemeldeten Nutzers, bei MCP die des Zugriffstokens bzw. Gastberechtigungen, wenn MCP ohne Authentifizierung verwendet wird).
Diese Berechtigungen bestimmen auch, welche Dokumente an die KI gelangen. Schließen Sie daher zuerst den Berechtigungsentwurf aus :doc:`guide-05` ab.

Vorgehen bei der Einführung
===========================

1. Fess mit :doc:`guide-02` starten, einen Teil der Ziele crawlen und die Suche ausprobieren
2. Aus der obigen Tabelle die zu Ihrem Problem passenden Artikel auswählen und die Konfiguration vornehmen
3. Berechtigungen (:doc:`guide-05`) und Betrieb (:doc:`guide-10`) festlegen, bevor Sie Fess für die Nutzer freigeben

Weiterführende Informationen
============================

- `Schnellstart <../quick-start.html>`__
- `Dokumentation <../documentation.html>`__
- `Plugins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `Leitfaden zu Datenspeicher-Connectoren <https://fess.codelibs.org/de/stable/config/datastore/index.html>`__
- `Diskussionsforum <https://discuss.codelibs.org/c/FessEN/>`__
- `GitHub <https://github.com/codelibs/fess>`__
