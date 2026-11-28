=================================================
Unternehmensweite Einführung: Checkliste je Phase
=================================================

Einleitung
==========

Wenn der Test von Fess erfolgreich war und Fess im ganzen Unternehmen eingeführt werden soll, ist weniger der Funktionsumfang die Frage als die Reihenfolge.
Manche Einstellungen verursachen viel Nacharbeit, wenn man sie auf eine spätere Phase verschiebt.
Wird zum Beispiel der Verschlüsselungsschlüssel geändert, nachdem Zugangsdaten registriert wurden, lassen sich die gespeicherten Werte nicht mehr entschlüsseln, und werden die Berechtigungen von Dokumenten nachträglich geändert, ist ein erneutes Crawlen nötig.

Dieser Artikel zeigt Phase für Phase, in welcher Reihenfolge Fess 15.9 unternehmensweit eingeführt wird.
Für jede Phase nennt er, was einzurichten ist, was zu prüfen ist und an welchen Kennzahlen Sie erkennen, ob Sie zur nächsten Phase übergehen können.
Als Kennzahlen dienen die Analyseberichte unter [Systeminformationen] > [Suchprotokoll] in der Administrationsoberfläche.
Die Schritte für einzelne Funktionen werden hier nicht erklärt; stattdessen verweisen wir auf die Artikel, die diese Funktionen behandeln.

Komponenten und zuständige Artikel
==================================

Die Komponenten, um die es bei der unternehmensweiten Einführung geht, und die Artikel, die sie jeweils ausführlich behandeln, sind:

- Fess selbst: stellt Suchseite, Administrationsoberfläche, API und Scheduler bereit. Überblick in :doc:`guide-01`, Speicher und Skalierung in :doc:`guide-14`
- OpenSearch: speichert neben dem Dokumentindex auch Crawl-Konfigurationen, Benutzer, Jobprotokolle und Suchprotokolle. Auslagerung und Clusterbildung in :doc:`guide-14`, Snapshots in :doc:`guide-10`
- Kindprozesse wie der Crawler: Crawling, Erzeugung von Vorschlägen, Erzeugung von Vorschaubildern und Chunk-Verarbeitung laufen je Job in einer von Fess selbst getrennten JVM. Heap-Einstellungen in :doc:`guide-14`
- Plugins: Datenspeicher (``fess-ds-*``), SSO (``fess-sso-*``), LLM und Embeddings (``fess-llm-*``), MCP und multimodale Suche (``fess-webapp-*``) und andere. Installieren Sie dieselbe Minor-Version wie Fess (15.9.x) und starten Sie Fess nach dem Installieren oder Entfernen neu. Eigene Plugins schreiben: :doc:`guide-17`
- LLM und Embedding-Modelle (optional): externe Dienste oder Server wie Ollama, die der KI-Suchmodus und die semantische Suche nutzen. Konfiguration in :doc:`guide-18` und :doc:`guide-19`

Was nicht in OpenSearch gespeichert wird, verwalten Sie auf jedem Fess-Server einzeln.
Das sind drei Dinge: die Einstellungen unter [System] > [Allgemein] (``system.properties``), ``fess_config.properties`` (einschließlich des Verschlüsselungsschlüssels ``app.cipher.key``) und die installierten Plugins.
Wie Sie diese sichern, steht in :doc:`guide-10`; wie Sie sie als Code verwalten, in :doc:`guide-16`.

Die Phasen im Überblick
=======================

.. list-table::
   :header-rows: 1
   :widths: 22 40 38

   * - Phase
     - Ziel
     - Weiter, wenn
   * - 1. Test
     - Wenige Benutzer suchen lassen und herausfinden, wonach gesucht wird
     - Die häufigsten Suchbegriffe und die Suchbegriffe ohne Treffer sind festgehalten
   * - 2. Erste Quelle veröffentlichen
     - Die erste Quelle mit Berechtigungen veröffentlichen und die Grundlagen des Betriebs schaffen
     - Ausgangswerte für Benutzerzahl und Klickrate sind festgehalten
   * - 3. SSO und Anmeldung
     - Anmeldung mit der Unternehmens-ID und Suchergebnisse je Gruppe
     - Unter „Suchanfragen nach Rolle und Gruppe“ erscheinen die Gruppen des IdP
   * - 4. Weitere Quellen
     - SaaS, Cloud-Speicher und Datenbanken hinzufügen
     - Suchbegriffe ohne Treffer, die auf fehlende Dokumente zurückgingen, verschwinden
   * - 5. Zyklus der Qualitätsverbesserung
     - Problematische Suchbegriffe im Suchprotokoll finden und beheben
     - Die verbesserten Kennzahlen sind gegenüber dem vorherigen Zeitraum nicht schlechter
   * - 6. Skalierung und Automatisierung
     - Auf mehr Dokumente und Benutzer vorbereiten und die Umgebung reproduzierbar machen
     - Die Antwortzeiten auf dem Reiter [Leistung] sind trotz steigender Benutzerzahl nicht schlechter als vor der Skalierung
   * - 7. KI-Funktionen
     - KI-Suchmodus, semantische Suche und MCP hinzufügen
     - Auf dem Reiter [KI-Chat] werden Anfragen erfasst, und die Fehlerquote ist nicht höher als direkt nach der Einführung

Jede Phase setzt die Einstellungen der vorherigen Phasen voraus.
Insbesondere die Phasen 2 und 3 enthalten Einstellungen, deren spätere Änderung ein erneutes Crawlen erfordert; vertauschen Sie ihre Reihenfolge daher nicht.

Phase 1: Test
=============

Richten Sie eine Fess-Instanz zum Testen ein und lassen Sie sie von einigen Abteilungen nutzen.
Ziel dieser Phase ist es, als Suchprotokoll zu sammeln, wonach die Benutzer suchen.

**Was einzurichten ist**

- Starten Sie Fess nach :doc:`guide-02` mit den Compose-Dateien des Tags ``v15.9.0`` von docker-fess und ändern Sie bei der ersten Anmeldung das Passwort
- Legen Sie eine Crawl-Konfiguration an, die auf eine einzelne Website oder einen einzelnen Ordner beschränkt ist
- Prüfen Sie, dass „Suchprotokoll“ und „Benutzerprotokoll“ unter [System] > [Allgemein] aktiviert sind (beide sind standardmäßig aktiviert). Ist „Benutzerprotokoll“ deaktiviert, wird die Benutzerzahl nicht erfasst

**Was zu prüfen ist**

- Unter [Systeminformationen] > [Jobprotokoll] endet der Crawl-Job mit „OK“, und unter [Systeminformationen] > [Crawling-Informationen] ist die Zahl der registrierten Dokumente nicht 0
- Sind es wenige Dokumente, sehen Sie unter [Systeminformationen] > [Fehler-URL] nach (:doc:`guide-02`)

**Weiter, wenn**

- Auf dem Reiter [Übersicht] von [Suchprotokoll] werden Suchanfragen, Benutzer, häufigste Suchbegriffe und Suchbegriffe ohne Treffer für den Testzeitraum angezeigt
- Klicken Sie auf die Suchbegriffe ohne Treffer, prüfen Sie auf dem Reiter [Protokolle] die tatsächlichen Suchen und ordnen Sie die Ursachen anhand der Tabelle in :doc:`guide-08` den Kategorien „andere Formulierung“, „zur offiziellen Bezeichnung lenken“ und „kein Dokument vorhanden“ zu
- Begriffe der Kategorie „kein Dokument vorhanden“ sind Kandidaten für die Quellen, die Sie in den Phasen 2 und 4 hinzufügen. Laden Sie die Tabelle als CSV herunter und bewahren Sie sie auf

Phase 2: Erste Quelle veröffentlichen
=====================================

Wählen Sie eine Quelle aus, die Benutzer im ganzen Unternehmen nutzen, und veröffentlichen Sie sie mit Berechtigungen.
Gleichzeitig richten Sie die für den Produktivbetrieb nötige Überwachung und Datensicherung ein.

**Was einzurichten ist**

- Legen Sie den Verschlüsselungsschlüssel ``app.cipher.key`` fest, bevor Sie Zugangsdaten in der Web-Authentifizierung, der Datei-Authentifizierung oder in Parametern von Datenspeichern registrieren. Wird er danach geändert, lassen sich die gespeicherten Werte nicht mehr entschlüsseln (:doc:`guide-16`, :doc:`guide-10`)
- Legen Sie Crawl-Konfigurationen für Websites und freigegebene Ordner, die Datei-Authentifizierung und Labels an (:doc:`guide-04`). Sollen die ACLs eines Dateiservers in den Suchergebnissen berücksichtigt werden, siehe :doc:`file-server-search`
- Legen Sie das Berechtigungskonzept fest (:doc:`guide-05`). Neue Crawl-Konfigurationen und Labels enthalten die Berechtigung ``{role}guest`` und sind damit auch für nicht angemeldete Benutzer sichtbar. Bei Dokumenten, die nur bestimmten Abteilungen angezeigt werden sollen, löschen Sie diesen Wert und tragen dann ``{group}`` oder Ähnliches ein
- Stimmen Sie die Gruppennamen, die Sie unter ``{group}`` eintragen, auf die Namen ab, die in Phase 3 vom IdP kommen. Spätere Umbenennungen erfordern das Umschreiben der Berechtigungen und ein erneutes Crawlen
- Gibt es Crawl-Konfigurationen, die per Job etwa einmal pro Woche laufen, stellen Sie „Alte Dokumente löschen“ unter [Allgemein] (Standard: 3 Tage) länger als das Crawl-Intervall ein (:doc:`guide-04`)
- Richten Sie Überwachung, Benachrichtigungen und Datensicherung ein (:doc:`guide-10`). Rufen Sie ``/api/v2/health`` aus einem externen Überwachungswerkzeug auf, konfigurieren Sie unter [Allgemein] „Benachrichtigungs-E-Mail“ oder „Slack Webhook URLs“ und holen Sie die Dateien aus [Systeminformationen] > [Sicherung] täglich über die Admin-API ab
- Bei Docker werden die Einstellungen unter [Allgemein] in ``system.properties`` im Container ``fess01`` gespeichert und gehen verloren, wenn ``down`` den Container neu erstellt. Nehmen Sie sie in die Datensicherung auf oder übergeben Sie sie mit ``FESS_JAVA_OPTS`` (:doc:`guide-02`, :doc:`guide-16`)
- Platzieren Sie bei Bedarf ein Suchfeld im Unternehmensportal (:doc:`guide-03`)

**Was zu prüfen ist**

- Melden Sie sich als Benutzer verschiedener Abteilungen an; die sichtbaren Dokumente ändern sich. In den erfassten Berechtigungen abteilungsspezifischer Dokumente ist die standardmäßige guest-Rolle nicht mehr enthalten (Prüfverfahren in :doc:`guide-05`)
- ``/api/v2/health`` liefert 200, und mit [Test-E-Mail senden] unter [Allgemein] kommt eine E-Mail an
- Führen Sie das Sicherungsskript einmal von Hand aus; die abgerufene Datei ist nicht leer (:doc:`guide-10`)

**Weiter, wenn**

Den Zustand von Überwachung und Datensicherung in dieser Phase zeigt [Suchprotokoll] nicht an.
Diesen beurteilen Sie anhand von „Was zu prüfen ist“ oben.
Im Suchprotokoll erfassen Sie die Ausgangswerte der Nutzung nach der Veröffentlichung.

- Prüfen Sie auf dem Reiter [Übersicht] Suchanfragen, Benutzer, Quote ohne Treffer und Klickrate für den Zeitraum nach der Veröffentlichung und speichern Sie sie als CSV. In den folgenden Phasen vergleichen Sie mit „Mit vorherigem Zeitraum vergleichen“ gegen diese Werte
- Unter „Am häufigsten angeklickte URLs“ auf dem Reiter [Klicks] erscheinen URLs der veröffentlichten Quelle
- Ist unter [Allgemein] bei „Alte Suchprotokolle löschen“ eine Anzahl von Tagen angegeben, lassen sich ältere Protokolle nicht zum Vergleich verwenden (der Standardwert ``-1`` löscht nichts). Legen Sie eine Aufbewahrungsdauer fest

Phase 3: SSO und Anmeldung
==========================

Lassen Sie die Benutzer sich über den Identitätsanbieter (IdP) des Unternehmens anmelden, und zeigen Sie Suchergebnisse je nach IdP-Gruppe an.

SSO meint hier die vier Verfahren, die in Fess 15.9 als Plugins bereitgestellt werden.
Für Entra ID verwenden Sie ``fess-sso-entraid``, für OpenID Connect ``fess-sso-oidc`` („SSO Type“ ist ``oic``), für SAML ``fess-sso-saml`` und für SPNEGO ``fess-sso-spnego``.
Die Docker-Images enthalten alle vier, die ``-slim``-Images jedoch keines davon.
Bei den ZIP-, RPM- und DEB-Paketen installieren Sie sie unter [System] > [Plugin] oder mit ``bin/fess-setup``.

LDAP ist kein SSO.
Die LDAP-Einstellungen unter [Allgemein] prüfen die auf der Fess-Anmeldeseite eingegebene ID und das Passwort gegen Active Directory oder einen ähnlichen Verzeichnisdienst und ermitteln die Gruppenzugehörigkeit (:doc:`guide-05`).
SPNEGO nutzt diese LDAP-Einstellungen, um die Gruppen zu ermitteln.

**Was einzurichten ist**

- Installieren Sie das Plugin, starten Sie Fess neu und konfigurieren Sie unter [Allgemein] „SSO Type“ sowie die Angaben zum IdP. Die beim IdP zu registrierende Rücksprungadresse ist ``https://<Fess-Host>/sso/`` (:doc:`guide-15`)
- Steht Fess hinter einem Reverse-Proxy, der TLS terminiert, teilen Sie Fess das externe Schema und den externen Port mit (:doc:`guide-15`)
- Sollen nicht angemeldete Benutzer nicht suchen können, aktivieren Sie „Anmeldung erforderlich“ unter [Allgemein]

„Anmeldung erforderlich“ wirkt nicht nur auf die Suchseite.

- Die Such-API unter ``/api/v2/`` antwortet auf Aufrufe ohne Anmeldesitzung und ohne gültiges Zugriffstoken mit 401. Stellen Sie für Aufrufe aus Geschäftsanwendungen Tokens bereit (:doc:`guide-11`)
- Mit dem Standardwert ``mcp.auth.mode=none`` weist ``/mcp`` Aufrufe von KI-Agenten mit HTTP 403 ab. Wenn Sie MCP nutzen, stellen Sie auf Authentifizierung mit Zugriffstokens um (:doc:`guide-20`)

**Was zu prüfen ist**

- Über ``/sso/`` können Sie sich beim IdP anmelden, und die je Abteilung sichtbaren Dokumente ändern sich wie in Phase 2 geplant (:doc:`guide-15`)
- Wenn Fess auf mehreren Servern läuft, sind auf dem Load Balancer Sticky Sessions aktiviert. In 15.9 liegen die Anmeldesitzungen im Speicher der jeweiligen Fess-Instanz

**Weiter, wenn**

- Unter „Suchanfragen nach Rolle und Gruppe“ auf dem Reiter [Zielgruppe] von [Suchprotokoll] erscheinen Zeilen für die vom IdP übermittelten Gruppen in der Form ``{group}<Gruppenname>``
- Erscheinen keine Gruppenzeilen, suchen die Benutzer entweder ohne Anmeldung (sie werden in der Zeile ``{role}guest`` gezählt), oder die Gruppen kommen nicht bei Fess an
- Die Benutzerzahl auf dem Reiter [Übersicht] ist gegenüber dem Ausgangswert aus Phase 2 nicht deutlich gesunken. Prüfen Sie anhand der Spalte „Benutzer“ unter „Suchanfragen nach Rolle und Gruppe“, ob eine Abteilung die Suche wegen der Einführung der Anmeldung nicht mehr nutzt

Phase 4: Weitere Quellen
========================

Fügen Sie über Datenspeicher-Plugins Quellen außer Websites und Dateiservern hinzu.
Die für alle Quellen gemeinsamen Schritte (Plugin-Installation, Parameter und Skripte, Berechtigungen, Jobs und Prüfen der Ergebnisse) sind in :doc:`datastore-basics` zusammengefasst.
Lesen Sie diesen Artikel zuerst.

**Was einzurichten ist**

- Installieren Sie für jede Quelle das Plugin und starten Sie neu

  - Git, Confluence/Jira, Slack: ``fess-ds-git``, ``fess-ds-atlassian``, ``fess-ds-slack`` (:doc:`guide-06`)
  - Google Drive, SharePoint/OneDrive, Box: ``fess-ds-gsuite``, ``fess-ds-microsoft365``, ``fess-ds-box`` (:doc:`guide-07`)
  - Datenbanken, CSV, Salesforce: ``fess-ds-db``, ``fess-ds-csv``, ``fess-ds-salesforce`` (:doc:`guide-12`)
  - Für Quellen ohne passendes Plugin schreiben Sie selbst eines (:doc:`guide-17`)

- Auch Datenspeicher-Konfigurationen enthalten ``{role}guest``. Entscheiden Sie je Konfiguration, ob die Berechtigungen der Quelle übernommen oder mit den ``{group}``-Einträgen aus Phase 2 angegeben werden
- Legen Sie mit [Neuen Job erstellen] für jede Konfiguration einen eigenen Job an, damit sich API-Ratenlimits und der Ablauf von Zugangsdaten je Quelle behandeln lassen
- Versehen Sie jede Quelle mit einem Label, damit auf der Suchseite danach gefiltert werden kann. Datenspeicher-Konfigurationen haben kein Label-Feld; vergeben Sie Labels daher per Skript oder über „Eingeschlossene Pfade“ des Labels (:doc:`datastore-basics`)

**Was zu prüfen ist**

- Ein Datenspeicher-Job kann auch dann mit „OK“ enden, wenn im Connector ein Fehler auftritt. Prüfen Sie „Indexgröße (Datenspeicher)“ unter [Crawling-Informationen], [Fehler-URL] und ``fess-crawler.log`` gemeinsam (:doc:`datastore-basics`)
- Bei Quellen mit übernommenen Berechtigungen suchen Sie als Benutzer mit unterschiedlichen Rechten; die sichtbaren Dokumente ändern sich

**Weiter, wenn**

- Die Suchbegriffe ohne Treffer, die Sie in den Phasen 1 und 2 der Kategorie „kein Dokument vorhanden“ zugeordnet haben, verschwinden für den Zeitraum nach dem Hinzufügen der Quelle aus den Suchbegriffen ohne Treffer auf dem Reiter [Suchbegriffe]
- Unter „Am häufigsten angeklickte URLs“ auf dem Reiter [Klicks] erscheinen Dokumente der hinzugefügten Quellen. Erscheint eine Quelle nicht, wird entweder nicht nach ihr gesucht, oder sie steht nicht weit oben in den Ergebnissen. Letzteres behandelt Phase 5

Phase 5: Zyklus der Qualitätsverbesserung
=========================================

Sobald die Quellen vollständig sind, sehen Sie regelmäßig das Suchprotokoll durch und beheben problematische Suchbegriffe.
Wie Sie die passende Maßnahme wählen und anwenden, behandelt :doc:`guide-08`.

**Was einzurichten ist**

- Für Suchbegriffe ohne Treffer verwenden Sie Synonyme oder verwandte Abfragen, für weit unten vergrabene Dokumente die Schlüsselübereinstimmung oder den Dokument-Boost (:doc:`guide-08`). Nach einer Änderung am Synonymwörterbuch laden Sie unter [Systeminformationen] > [Wartung] den Dokumentenindex neu
- Werden Dokumente mit gemischtem Japanisch, Englisch und Chinesisch nicht vollständig gefunden, prüfen Sie die sprachspezifischen Felder und Wörterbücher (:doc:`guide-09`)
- Brauchen Sie Auswertungen, die die eingebauten Berichte nicht bieten (geöffnete URLs je Suchbegriff, Suchbegriffe ohne Treffer je Rolle, monatliche Verläufe über lange Zeiträume usw.), verwenden Sie OpenSearch Dashboards (:doc:`guide-22`)
- Wörterbücher und Einstellungen der Schlüsselübereinstimmung als Code verwalten: :doc:`guide-16`

**Was zu prüfen ist**

- Suchen Sie auf der Suchseite nach den bearbeiteten Begriffen; die gewünschten Dokumente werden gefunden oder erscheinen weit oben
- Bei der Schlüsselübereinstimmung wird das Zieldokument im Feld „URLs“ der Detailseite angezeigt (:doc:`guide-08`)

**Weiter, wenn**

Diese Phase endet nie; sie wird wiederholt.
Die Wirkung einer einzelnen Verbesserung prüfen Sie so:

- Setzen Sie den Zeitraum auf „Benutzerdefiniert“ ab dem Tag nach der Änderung und aktivieren Sie „Mit vorherigem Zeitraum vergleichen“
- Bei Korrekturen von Suchbegriffen ohne Treffer betrachten Sie die Quote ohne Treffer auf dem Reiter [Übersicht] und die Suchbegriffe ohne Treffer auf dem Reiter [Suchbegriffe]; bei Korrekturen der Rangfolge die durchschnittliche Klickposition auf dem Reiter [Suchbegriffe] und die Verteilung der Klickpositionen auf dem Reiter [Klicks]
- Sind die bearbeiteten Begriffe aus der Liste verschwunden und die Gesamtkennzahlen gegenüber dem vorherigen Zeitraum nicht schlechter, behalten Sie die Änderung bei

Phase 6: Skalierung und Automatisierung
=======================================

Wenn Dokumente und Benutzer zunehmen, stellen Sie vor der Skalierung fest, was knapp wird.
Gleichzeitig sorgen Sie dafür, dass sich dieselbe Umgebung neu aufbauen lässt.

**Was einzurichten ist**

- Stellen Sie anhand der Symptome fest, was knapp wird (:doc:`guide-14`). Ein OutOfMemoryError in ``fess-crawler.log`` bedeutet zu wenig Speicher in der JVM des Crawlers (``jvm.crawler.options``); eine Vergrößerung des Heaps von Fess selbst (``FESS_HEAP_SIZE``) hilft dagegen nicht
- Prüfen Sie in dieser Reihenfolge: OpenSearch auf einen eigenen Server auslagern, einen Cluster aus drei Knoten bilden, Fess auf mehreren Servern betreiben (:doc:`guide-14`)
- Betreiben Sie Fess auf mehreren Servern, überlassen Sie das Crawlen einem Server. Setzen Sie sowohl ``scheduler.target.name`` als auch „Ziel“ unter [System] > [Scheduler] (:doc:`guide-14`)
- Halten Sie bei mehreren Servern ``app.cipher.key``, ``fess_config.properties``, die Einstellungen unter [Allgemein] und die Plugins auf allen Servern gleich
- Legen Sie den Tag des Docker-Images und die Plugin-Versionen fest und machen Sie die Einstellungen mit fessctl und der Admin-API anwendbar (:doc:`guide-16`)
- Soll eine Fess-Instanz von mehreren Organisationen genutzt werden, kombinieren Sie virtuelle Hosts mit Rollen. Virtuelle Hosts allein sind keine Zugriffskontrolle (:doc:`guide-13`)

**Was zu prüfen ist**

- Vergleichen Sie vor und nach der Skalierung die Heap-Auslastung aus ``/api/admin/stats`` und die Crawl-Dauer unter [Systeminformationen] > [Jobprotokoll] (:doc:`guide-10`)
- Bei mehreren Servern erhalten Sie dieselben Suchergebnisse, egal über welchen Server Sie die Seite öffnen, und gecrawlt wird nur auf dem zuständigen Server. Ein Klick auf [Jetzt starten] auf einem anderen Server führt den Job nicht aus (:doc:`guide-14`)
- Die Einstellungen lassen sich aus einer Sicherung in eine neu aufgebaute Umgebung zurückspielen (:doc:`guide-10`)

**Weiter, wenn**

- Auf dem Reiter [Leistung] von [Suchprotokoll] sind Median, p95 und p99 der Antwortzeit niedriger als vor der Skalierung oder trotz steigender Benutzerzahl nicht gestiegen
- Suchen Sie nach den Begriffen unter „Langsamste Suchbegriffe“, um zu unterscheiden, ob nur bestimmte Begriffe oder alle Suchen langsam sind

Die Möglichkeit, Anmeldesitzungen in OpenSearch zu speichern und zwischen mehreren Servern zu teilen, gibt es ab 15.10.
In 15.9 arbeiten Sie mit den oben genannten Sticky Sessions.

Phase 7: KI-Funktionen
======================

Die KI-Funktionen erfordern jeweils unterschiedliche Vorbereitungen.
Fügen Sie zuerst die hinzu, die zu Ihrem Ziel passen.

**KI-Suchmodus (RAG)**

- Ein LLM beantwortet Fragen der Benutzer auf Grundlage interner Dokumente (:doc:`guide-19`)
- Eine Vektorsuche ist nicht nötig. Die Belegdokumente werden mit der normalen Suche gesammelt; die Berechtigungen aus den Phasen 2 und 3 gelten daher unverändert, und Dokumente, die ein Benutzer nicht sehen darf, fließen nicht in die Antwort ein
- Drei Dinge sind erforderlich: ``rag.chat.enabled=true`` in ``fess_config.properties`` (Standard ist ``false``, in der Administrationsoberfläche gibt es dafür keinen Eintrag), ein ``fess-llm-*``-Plugin und „LLM-Anbieter“ unter [Allgemein]
- Welche Benutzer die Funktion nutzen dürfen, schränken Sie mit „Chat-Berechtigungen“ unter [Allgemein] ein

**Semantische Suche und multimodale Suche**

- Die semantische Suche findet Dokumente mit ähnlicher Bedeutung, auch wenn die Schlüsselwörter nicht übereinstimmen (:doc:`guide-18`). Den Embedding-Anbieter wählen Sie mit ``content_chunker.embedding.name``. Der Standardwert ``opensearch`` nutzt ein Modell aus ML Commons von OpenSearch; ``ollama``, ``openai``, ``gemini`` und ``bedrock`` erfordern das jeweilige ``fess-llm-*``-Plugin
- Um sie in einer bestehenden Umgebung zu aktivieren, erstellen Sie den Index neu und erzeugen anschließend Vektoren für alle Dokumente. Bei nutzungsabhängig abgerechneten Modellen wie OpenAI fallen bei der ersten Verarbeitung Kosten für alle Dokumente an
- Die multimodale Suche verwendet das Plugin ``fess-webapp-multimodal`` und einen CLIP-Server und findet Bilder anhand von Text (:doc:`guide-21`)
- Beide lassen sich in einer Fess-Instanz nicht gleichzeitig nutzen. Brauchen Sie beide, bauen Sie getrennte Fess-Instanzen auf

**MCP**

- Damit können KI-Agenten in Fess suchen (:doc:`guide-20`). Nach Installation des Plugins ``fess-webapp-mcp`` steht ``/mcp`` zur Verfügung
- Mit dem Standardwert ``mcp.auth.mode=none`` kann jeder, der ``/mcp`` erreicht, als Gast suchen. Stellen Sie vor der Freigabe im Unternehmen auf Authentifizierung mit Zugriffstokens oder Ähnlichem um

**Was zu prüfen ist**

- KI-Suchmodus: Stellen Sie auf der Suchseite unter [KI-Suche] eine Frage; Antwort und Quellen werden angezeigt. Bei Benutzern mit anderen Berechtigungen erscheinen Dokumente, die sie nicht sehen dürfen, nicht unter den Quellen (:doc:`guide-19`)
- Semantische Suche und multimodale Suche: In die Dokumente werden Vektoren geschrieben, und die Antwort der Such-API zeigt, dass die Vektorsuche verwendet wird (:doc:`guide-18`, :doc:`guide-21`)
- MCP: Nach der Umstellung der Authentifizierung werden Aufrufe ohne Token abgewiesen (:doc:`guide-20`)

**Weiter, wenn**

- Für den KI-Suchmodus betrachten Sie auf dem Reiter [KI-Chat] von [Suchprotokoll] Anfragen, Benutzer, Fehlerquote und durchschnittliche Antwortzeit. Tokenzahlen werden nur erfasst, wenn das LLM-Plugin sie meldet, und der Inhalt von Fragen und Antworten wird nicht erfasst
- Für die semantische Suche aktivieren Sie „Mit vorherigem Zeitraum vergleichen“ für einen Zeitraum ab dem Tag nach der Einführung und vergleichen Quote ohne Treffer, Klickrate und die Antwortzeiten auf dem Reiter [Leistung]
- Für MCP und multimodale Suche gibt es in [Suchprotokoll] keine eigenen Kennzahlen. Beurteilen Sie sie anhand von „Was zu prüfen ist“ oben und der Rückmeldungen der nutzenden Abteilungen

Weiterführende Artikel
======================

- Test beginnen: :doc:`guide-02`
- Erste Quelle mit Berechtigungen veröffentlichen: :doc:`guide-04`, :doc:`guide-05`, :doc:`file-server-search`
- Überwachung und Datensicherung: :doc:`guide-10`
- SSO: :doc:`guide-15`
- Weitere Quellen hinzufügen: :doc:`datastore-basics`
- Qualität mit dem Suchprotokoll verbessern: :doc:`guide-08`
- Skalierung und Konfiguration als Code: :doc:`guide-14`, :doc:`guide-16`
- KI-Funktionen: :doc:`guide-19`, :doc:`guide-18`, :doc:`guide-20`

Referenzen
==========

- `Suchprotokoll <https://fess.codelibs.org/de/stable/admin/searchlog-guide.html>`__
- `Allgemein <https://fess.codelibs.org/de/stable/admin/general-guide.html>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `Systemanforderungen <https://fess.codelibs.org/de/stable/install/prerequisites.html>`__
- `Fess-Diskussionsforum <https://discuss.codelibs.org/c/FessEN/>`__
