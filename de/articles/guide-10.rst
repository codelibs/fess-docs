===================================================
Fess im Betrieb: Monitoring, Backup, Fehlerbehebung
===================================================

Einleitung
==========

Sobald Fess im Unternehmen freigegeben ist, geraten die Betreuer typischerweise in Situationen wie diese:
Dass die Suche nicht mehr funktioniert, erfährt man erst durch Anfragen der Benutzer; dass der nächtliche Crawl fehlschlägt, bemerkt man tagelang nicht; und nach dem Neuaufbau eines Servers fehlen die Einstellungen.

Dieser Artikel beschreibt, wie Sie sich mit den in Fess 15.9 vorhandenen Mechanismen auf solche Situationen vorbereiten.

- Den Zustand von Fess und OpenSearch mit ``/api/v2/health`` und ``/api/admin/stats`` von einem externen Monitoring-Werkzeug aus prüfen
- Das Ende von Crawls, Statusänderungen von OpenSearch und Fehlerprotokolle per E-Mail, Slack oder Google Chat melden lassen
- Wissen, welche Protokolldatei was enthält und wo sie liegt
- Sicherungen der Einstellungen per cron erstellen und auf einem anderen Server wiederherstellen
- Wissen, welche Bildschirme und Protokolle von Fess bei einer Störung zu prüfen sind

Wie Sie Einstellungen als Code verwalten, behandelt :doc:`guide-16`; die Skalierung bei wachsender Zahl von Dokumenten und Benutzern (einschließlich der Heap-Anpassung) behandelt :doc:`guide-14`.
Die Beispielbefehle setzen die Docker-Umgebung aus :doc:`guide-02` voraus (``fess01`` und ``search01``).
Unterschiede bei der ZIP-Version und den RPM/DEB-Paketen werden jeweils an Ort und Stelle erwähnt.

Überwachen
==========

Verfügbarkeitsüberwachung: /api/v2/health
-----------------------------------------

Fess bietet eine Health-Check-API, die ohne Authentifizierung aufgerufen werden kann.

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

Die HTTP-Statuscodes bedeuten Folgendes.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status
     - Zustand
   * - 200
     - Fess antwortet, und der OpenSearch-Cluster ist ``GREEN`` oder ``YELLOW``
   * - 503
     - Der OpenSearch-Cluster ist ``RED``, oder Fess kann keine Verbindung zu OpenSearch herstellen (``error.details.engine.status`` ist ``UNAVAILABLE``)
   * - Keine Antwort / Zeitüberschreitung
     - Der Fess-Prozess ist gestoppt, oder Fess wartet auf ein OpenSearch, das nicht antwortet

Ihr Monitoring-Werkzeug sollte diesen Statuscode für die Bewertung verwenden.
Bei ``curl`` sorgt ``-f`` dafür, dass der Exit-Code bei 503 ungleich 0 ist.
Antwortet OpenSearch nicht mehr, ohne dass der Prozess beendet ist, wartet diese API bis zu ``index.health.timeout`` (Standard ``10m``) auf die Antwort von OpenSearch.
Legen Sie auf der Monitoring-Seite eine Zeitüberschreitung fest, wie ``--max-time 10`` im obigen Beispiel, und werten Sie auch eine Zeitüberschreitung als Fehler.
Beachten Sie, dass das in früheren Fassungen dieses Artikels vorgestellte ``/api/v1/health`` in einer Standardinstallation von 15.9 nicht verfügbar ist (``/api/v1`` wird nur bereitgestellt, wenn das Plugin ``fess-webapp-v1-api`` installiert ist).

Unter Docker nutzt ``fess01`` diese API über zwei Mechanismen.

- Der ``healthcheck`` in ``compose.yaml`` ruft sie alle 30 Sekunden auf; das Ergebnis erscheint als ``(healthy)`` in ``docker compose ps``
- Auch das Startskript im Container ruft sie alle 60 Sekunden auf und beendet den Container, wenn nach dem Start 5-mal in Folge kein 200 zurückkommt. Durch ``restart: unless-stopped`` wird der Container anschließend neu gestartet

Bleibt OpenSearch daher einige Minuten lang ``RED``, startet ``fess01`` immer wieder neu.
Wenn ``fess01`` ständig neu startet, prüfen Sie zuerst ``search01``.

Ressourcenüberwachung: /api/admin/stats
---------------------------------------

Heap-Auslastung und freien Speicherplatz liefert die Admin-API ``GET /api/admin/stats``.
[Systeminformationen] > [Konfigurationsinformationen] enthält nur eine Liste der Eigenschaften und zeigt keine Speichernutzung an.

Für die Admin-API benötigen Sie ein Zugriffstoken.

1. Öffnen Sie [System] > [Zugriffstoken] und klicken Sie auf [Neu erstellen]
2. Geben Sie unter „Name“ den Verwendungszweck (z. B. ``monitoring``) und unter „Berechtigungen“ ``{role}admin-api`` ein und klicken Sie auf [Erstellen]
3. Öffnen Sie das erstellte Token in der Liste und notieren Sie den Wert von „Token“

.. warning::

   Mit einem ``{role}admin-api``-Token lassen sich alle Admin-APIs nutzen, auch solche, die Einstellungen ändern oder löschen.
   Eine Einstellung, die es auf Lesezugriff beschränkt, gibt es nicht.
   Bewahren Sie es – etwa in einer Datei auf dem Monitoring-Server – mit derselben Sorgfalt auf wie das Administratorpasswort.

Übergeben Sie das Token im ``Authorization``-Header.
Das folgende Beispiel liest die Heap-Auslastung (%) und die Auslastung jedes Dateisystems aus.

::

    $ curl -fsS -H "Authorization: Bearer <Token>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

Außerdem enthält die Antwort Anzahl und kumulierte Dauer der GC-Läufe (``jvm.gc``), CPU-Auslastung und Load Average des Betriebssystems (``os``) sowie Clusterzustand und Shard-Anzahl von OpenSearch (``engine``).
Die vollständige Liste der Felder finden Sie unter `Stats API <https://fess.codelibs.org/de/stable/api/admin/api-admin-stats.html>`__.

Beachten Sie beim Lesen der Werte die folgenden zwei Punkte.

- ``jvm`` sind die Werte der JVM von Fess selbst (der Webanwendung). Crawls laufen in einem separaten JVM-Prozess, daher zeigt sich Speichermangel des Crawlers hier nicht. Prüfen Sie dafür ``fess-crawler.log`` (siehe unten)
- ``fs`` sind die Dateisysteme des Hosts, auf dem Fess läuft (unter Docker: des Containers). Den freien Platz im Datenbereich von OpenSearch fragen Sie direkt bei OpenSearch ab

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

Wie Sie die Heap-Größe ändern, lesen Sie in :doc:`guide-14`.

Benachrichtigungen empfangen
----------------------------

Die Benachrichtigungsziele von Fess legen Sie mit drei Feldern im Abschnitt „Benachrichtigung“ unter [System] > [Allgemein] fest.

- „Benachrichtigungs-E-Mail“: E-Mail-Adressen der Empfänger (mehrere durch Kommas getrennt)
- „Slack Webhook URLs“: die Incoming-Webhook-URL von Slack
- „Google Chat Webhook URLs“: die Webhook-URL von Google Chat

Sobald eines davon gesetzt ist, werden die folgenden drei Arten von Benachrichtigungen an dieselben Ziele gesendet.

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - Benachrichtigung
     - Wann sie gesendet wird
     - Zusätzlich erforderliche Einstellungen
   * - Crawl abgeschlossen (Betreff ``[FESS] Crawler completed``)
     - Wird nach jedem Ende eines Crawl-Jobs gesendet, unabhängig vom Erfolg. Enthält den Status (OK/FAIL) und die Anzahl der indexierten Dokumente
     - Keine
   * - Statusänderung von OpenSearch (Betreff ``[FESS] Status Change``)
     - Der Scheduler-Job „Search Engine Monitor“ fragt OpenSearch jede Minute ab und sendet eine Benachrichtigung, wenn der Cluster ``RED`` wird und wenn er sich von ``RED`` erholt
     - Keine
   * - Protokollbenachrichtigung (Betreff ``[FESS] ERROR Log Alert``)
     - Der Job „Log Notification“ sammelt alle 5 Minuten die von Fess, dem Crawler und weiteren Prozessen geschriebenen ERROR-Protokolle (oder Protokolle ab der angegebenen Ebene) und sendet sie gebündelt
     - Unter [Allgemein] „Log Notification“ aktivieren und eine „Log Notification Level“ wählen

Kann Fess keine Verbindung zu OpenSearch herstellen, schlägt der Job „Search Engine Monitor“ selbst fehl, und es wird keine Statusänderung gemeldet.
Einen Verbindungsabbruch erkennen Sie, indem Sie ``/api/v2/health`` wie im vorigen Abschnitt beschrieben von außen überwachen.

Die Standardebene der Protokollbenachrichtigung ist ``ERROR``.
Fehlgeschlagene geplante Jobs werden mit ``WARN`` protokolliert (``Failed to execute job: ...``). Wenn Sie auch über Job-Fehler informiert werden möchten, setzen Sie „Log Notification Level“ daher auf ``WARN``.
Dann werden allerdings auch alle anderen ``WARN``-Meldungen gesendet.

Für den Empfang per E-Mail tragen Sie den SMTP-Server in zwei Dateien ein und starten Fess neu.

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties``: wird für Protokollbenachrichtigungen, Statusänderungen und die Schaltfläche [Test-E-Mail senden] verwendet
- ``fess_env_crawler.properties``: wird für die Benachrichtigung über abgeschlossene Crawls verwendet (weil Crawls in einem separaten Prozess laufen)

Die Dateien liegen bei der ZIP-Version in ``app/WEB-INF/classes/`` und bei den RPM/DEB-Paketen in ``/etc/fess/``.
Prüfen Sie nach der Einrichtung mit [Test-E-Mail senden] unter [Allgemein], ob die E-Mail ankommt.

Wenn Sie unter Docker schnell Benachrichtigungen erhalten möchten, ist ein Webhook für Slack oder Google Chat am einfachsten, da keine Dateien bearbeitet werden müssen.
Die Einstellungen unter [Allgemein] werden jedoch in ``system.properties`` im Container ``fess01`` gespeichert und gehen daher verloren, wenn der Container mit ``docker compose down`` neu erstellt wird (siehe den Abschnitt zum Stoppen und Neustarten in :doc:`guide-02`).
Nehmen Sie ``system.properties`` in die weiter unten beschriebene Sicherung auf.

Antwortzeiten der Suche und Crawl-Ergebnisse prüfen
---------------------------------------------------

Prüfen Sie zusätzlich zur externen Überwachung regelmäßig die folgenden drei Bildschirme der Administration.

- [Systeminformationen] > [Jobprotokoll]: Status (OK/Fehlgeschlagen) und Ergebnis von Jobs wie „Default Crawler“. Jobs, die jede Minute oder alle paar Minuten laufen, wie „Search Engine Monitor“ und „Log Notification“, werden hier nicht erfasst
- [Systeminformationen] > [Crawling-Informationen]: „Crawler-Status“, „Indexgröße (Web/Datei)“ und „Indexgröße (Datenspeicher)“ für jede Sitzung. Prüfen Sie, ob die Werte gegenüber dem vorherigen Lauf stark gesunken sind
- Die Registerkarte [Leistung] unter [Systeminformationen] > [Suchprotokoll]: Median, p95 und p99 der Antwortzeiten sowie Suchbegriffe mit langsamen Antworten. Wie Sie Suchprotokolle auswerten, lesen Sie in :doc:`guide-08`

Protokolle lesen
================

Arten von Protokolldateien
--------------------------

Fess schreibt die Protokolle für jede Art von Verarbeitung in eine eigene Datei.
Wählen Sie die Datei je nachdem, was Sie untersuchen möchten.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Datei
     - Inhalt
   * - ``fess.log``
     - Protokoll von Fess selbst (Suchseite, Administration, APIs, Scheduler). Fehlgeschlagene Starts, Verbindungsfehler zu OpenSearch, fehlgeschlagene Importe von Sicherungen usw.
   * - ``fess-crawler.log``
     - Protokoll des Crawler-Prozesses. Abruffehler pro URL, fehlgeschlagene Authentifizierungen, Speichermangel des Crawlers usw.
   * - ``audit.log``
     - Audit-Protokoll von An- und Abmeldungen sowie administrativen Vorgängen
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - Protokolle der Erzeugung von Vorschlägen und Miniaturansichten
   * - ``fess-llm.log``
     - Protokoll des KI-Suchmodus (RAG) und der LLM-Anbindung
   * - ``searchlog.log``
     - Ein Eintrag pro Suche (wenn „Suchprotokoll“ unter [Allgemein] aktiviert ist)
   * - ``server_*.log``
     - Tomcat-Protokolle

Der Speicherort hängt von der Installationsart ab.

- ZIP-Version: ``logs/`` im Verzeichnis, in das Fess entpackt wurde
- RPM/DEB-Pakete: ``/var/log/fess/``
- Docker: ``/var/log/fess/`` im Container. ``fess.log``, ``fess-crawler.log``, ``audit.log`` und weitere werden auch auf die Standardausgabe geschrieben und lassen sich daher mit ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01`` lesen. Wird der Container neu erstellt, gehen sie verloren

Unabhängig von der Installationsart können Sie eine Datei unter [Systeminformationen] > [Protokolldatei] durch Klick auf ihren Namen herunterladen.
So können auch Mitarbeitende ohne Anmeldung am Server die Protokolle prüfen.

Jedes Protokoll wird beim Datumswechsel oder ab 100 MB zu ``.log.gz`` komprimiert und rotiert.
Die komprimierten Dateien werden bei ``fess.log`` und ``searchlog.log`` nach 90 Tagen, bei ``audit.log`` nach 360 Tagen automatisch gelöscht.
Die komprimierten Dateien der Protokolle des Crawlers und der Kindprozesse, etwa ``fess-crawler.log``, ``fess-suggest.log`` und ``fess-thumbnail.log``, werden dagegen nicht automatisch gelöscht.
Überwachen Sie den Platzbedarf des Protokollverzeichnisses und löschen Sie alte Dateien regelmäßig.

Genauer untersuchen
-------------------

Standardmäßig schreibt ``fess.log`` Einträge ab WARN und ``fess-crawler.log`` ab INFO.
Für ein ausführlicheres ``fess.log`` setzen Sie „Protokollebene“ unter [System] > [Allgemein] auf ``INFO`` oder ``DEBUG``.
Diese Änderung wird beim Neustart von Fess zurückgesetzt.
Die Protokollebene des Crawlers wird durch das Skript des Jobs bestimmt.
Das Skript von „Default Crawler“ enthält ``logLevel("info")``; ändern Sie es unter [System] > [Scheduler] in ``logLevel("debug")``, werden ab dem nächsten Crawl ausführliche Protokolle geschrieben.
Setzen Sie es nach der Untersuchung wieder zurück.
Wie Sie die Ebene dauerhaft ändern, lesen Sie unter `Protokollkonfiguration <https://fess.codelibs.org/de/stable/config/admin-logging.html>`__.

Wenn Sie in einem Forum o. Ä. um Rat fragen, ist [Protokolle herunterladen] unter „Diagnose“ in [Systeminformationen] > [Wartung] hilfreich.
Damit wird eine ZIP-Datei heruntergeladen, die die Protokolle, ``system.properties``, ``fess_config.properties``, den Inhalt der Konfigurationsindizes und den Zustand von OpenSearch enthält.
Werte wie API-Schlüssel und ``app.cipher.key`` werden durch ``XXXXXXXX`` ersetzt, die Protokolle selbst und der Inhalt der Konfigurationsindizes werden jedoch nicht maskiert.
Prüfen Sie den Inhalt, bevor Sie die Datei an Externe weitergeben.

Sichern
=======

Was wo liegt
------------

Die Daten von Fess verteilen sich auf drei Orte.
Unter [Systeminformationen] > [Sicherung] erhalten Sie nur den ersten davon.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Daten
     - Speicherort
     - Sicherungsmethode
   * - Crawl-Konfigurationen, Scheduler, Labels, Benutzer, Einstellungen unter [Allgemein]
     - Konfigurationsindizes in OpenSearch und ``system.properties``
     - [Systeminformationen] > [Sicherung] oder die Admin-API
   * - Gecrawlte Dokumente, Wörterbücher (Synonyme, Stoppwörter usw.)
     - Die Indizes ``fess.*`` und der Index ``configsync`` in OpenSearch
     - Snapshots von OpenSearch (für Wörterbücher allein genügt auch das Kopieren der Dateien)
   * - ``fess_config.properties`` (einschließlich ``app.cipher.key``), Starteinstellungen, installierte Plugins
     - Dateien auf dem Fess-Server
     - Kopieren der Dateien oder Konfigurationsmanagement

Gecrawlte Dokumente lassen sich durch erneutes Crawlen wiederherstellen, sofern die Einstellungen zurückgespielt sind.
Erstellen Sie Snapshots nur, wenn ein erneuter Crawl zu lange dauern würde.

Über [Sicherung] erhältliche Dateien
------------------------------------

Unter [Systeminformationen] > [Sicherung] sind die folgenden Dateien aufgeführt.
Durch Klick auf einen Namen laden Sie die jeweilige Datei herunter.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Datei
     - Inhalt
   * - ``fess_basic_config.bulk``
     - Einstellungen wie Crawl-Konfigurationen, Scheduler, Labels, Key Matches sowie Web-/Datei-Authentifizierung
   * - ``fess_config.bulk``
     - Alles oben Genannte, zusätzlich Crawling-Informationen, Fehler-URLs, Jobprotokolle, Benutzer-Tags usw.
   * - ``fess_user.bulk``
     - Benutzer, Rollen und Gruppen
   * - ``system.properties``
     - Die Einstellungen unter [System] > [Allgemein]
   * - ``fess.json`` / ``doc.json``
     - Einstellungen und Mapping des Dokumentindex
   * - ``*.ndjson``
     - Suchprotokolle, Klickprotokolle, Favoriten, KI-Chat-Protokolle und Suchbenutzer. Sie lassen sich herunterladen, aber nicht zum Wiederherstellen hochladen

Zum Wiederherstellen der Einstellungen dienen die drei Dateien ``fess_basic_config.bulk``, ``fess_user.bulk`` und ``system.properties``.
Wenn Sie Benutzer-Tags verwenden, sichern Sie auch ``fess_config.bulk``.

Abgesehen von den weiter unten beschriebenen Anmeldedaten enthalten ``*.bulk``-Dateien die Einstellungswerte unverschlüsselt.
Bewahren Sie sie als vertrauliche Dateien auf.

Tägliche Sicherung per cron
---------------------------

Die Admin-API ``GET /api/admin/backup/file/<Dateiname>/`` liefert dieselben Dateien wie der Bildschirm.
Erstellen Sie ein Token wie im Abschnitt „Ressourcenüberwachung“ oben beschrieben und speichern Sie es in einer Datei, die nur der Benutzer lesen kann, der das Skript ausführt.

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<Token>" > /etc/fess-backup/token'

Das folgende Skript speichert die Dateien in einem Verzeichnis pro Datum und löscht Verzeichnisse, die älter als 30 Tage sind (die Aufbewahrungsdauer ist ein Beispiel).

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Docker-Umgebung: auch die Wörterbuchdateien kopieren
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

Die wichtigsten Punkte:

- Der abschließende ``/`` in der URL darf nicht fehlen. Da die Dateinamen einen Punkt enthalten, wird eine Anfrage ohne ``/`` als Anfrage nach einer statischen Datei behandelt und liefert 404
- Ohne ``-f`` speichert ``curl`` auch 404- und andere Fehlerantworten in der Datei, und das Skript scheint erfolgreich zu sein. ``-f`` und ``set -e`` sorgen dafür, dass es bei einem Fehler abbricht
- Bei der ZIP-Version und den RPM/DEB-Paketen kopieren Sie statt der Zeile mit ``docker cp`` das Wörterbuchverzeichnis auf der OpenSearch-Seite (den Ort, auf den ``FESS_DICTIONARY_PATH`` von Fess verweist)

Speichern Sie das Skript als ``/usr/local/bin/fess-backup.sh``, machen Sie es ausführbar und tragen Sie es in die crontab von root ein (im Beispiel täglich um 2:30 Uhr).

::

    30 2 * * * /usr/local/bin/fess-backup.sh

Führen Sie es nach dem Eintragen einmal manuell aus.
Öffnen Sie ``fess_basic_config.bulk`` und prüfen Sie, ob sich Zeilen, die mit ``{"index":{"_index":`` beginnen, mit JSON-Zeilen der Einstellungen abwechseln.
Derselbe Ablauf lässt sich auch mit ``fessctl`` umsetzen (siehe :doc:`guide-16`).

app.cipher.key festhalten
-------------------------

Fess 15.9 verschlüsselt die Passwörter der Web- und Datei-Authentifizierung sowie Passwörter und Secrets, die in den Parametern von Crawl- und Datenspeicher-Konfigurationen gespeichert sind, mit ``app.cipher.key`` aus ``fess_config.properties``.
Auch in ``*.bulk``-Dateien bleiben sie verschlüsselt.
Für die Wiederherstellung auf einem anderen Server muss dort derselbe ``app.cipher.key`` gesetzt sein.
Mit einem anderen Schlüssel lassen sich die Werte nicht entschlüsseln: In ``fess-crawler.log`` wird ``CipherFailureException`` protokolliert, und Crawls, die diese Anmeldedaten verwenden, schlagen fehl.

``fess_config.properties`` liegt bei der ZIP-Version in ``app/WEB-INF/classes/`` und bei den RPM/DEB-Paketen in ``/etc/fess/``.
Wenn Sie den Wert geändert haben, behandeln Sie diese Datei wie die ``*.bulk``-Dateien als vertraulich und bewahren Sie sie an einem separaten Ort auf.
Um den Wert unter Docker zu ändern, geben Sie ``-Dfess.config.app.cipher.key=<Wert>`` in ``FESS_JAVA_OPTS`` in ``compose.yaml`` an.
So wird auch nach dem Neuerstellen des Containers derselbe Schlüssel verwendet.

.. warning::

   Wenn Sie ``app.cipher.key`` ändern, nachdem Anmeldedaten gespeichert wurden, lassen sich die bis dahin gespeicherten Werte nicht mehr entschlüsseln.
   Ändern Sie ihn gegebenenfalls, bevor Sie Anmeldedaten für Web- und Datei-Authentifizierung oder Datenspeicher eintragen.
   In einer bereits laufenden Umgebung lassen Sie den Wert unverändert und notieren ihn.

Snapshots des Dokumentindex
---------------------------

Um Dokumente ohne erneutes Crawlen wiederherzustellen, verwenden Sie Snapshots von OpenSearch.
Nehmen Sie zusätzlich zu ``fess*`` unbedingt den Index ``configsync`` auf, der die Wörterbücher enthält.
Ohne ``configsync`` fehlen beim Wiederherstellen in ein neues OpenSearch die Wörterbuchdateien, und der Dokumentindex lässt sich nicht öffnen.

Für Snapshots muss auf der OpenSearch-Seite der Repository-Pfad (``path.repo``) konfiguriert sein.
In ``compose-opensearch3.yaml`` von docker-fess ist er nicht gesetzt; fügen Sie ihn hinzu, wenn Sie Snapshots verwenden.
Die Schritte zum Registrieren eines Repositorys, zum Erstellen und zum Wiederherstellen finden Sie unter `Index-Verwaltung <https://fess.codelibs.org/de/stable/config/admin-index-backup.html>`__.
Stellen Sie bei gestopptem Fess wieder her, und spielen Sie ``configsync`` zuerst zurück.

Wiederherstellen
================

Was Sie vor dem Wiederherstellen wissen sollten
-----------------------------------------------

Die Wiederherstellung über [Sicherung] ersetzt den Inhalt von OpenSearch nicht vollständig.

- Wiederhergestellt wird nur per Hochladen. Die Admin-API dient nur zum Herunterladen; eine API zum Wiederherstellen gibt es nicht
- Jede Einstellung in einer ``*.bulk``-Datei wird nur geschrieben, wenn dieselbe Einstellung auf dem Server nicht existiert oder neuer ist als die auf dem Server. Einstellungen, die nach der Sicherung geändert wurden, werden nicht auf den alten Stand zurückgesetzt
- Einstellungen, die nach der Sicherung angelegt wurden, werden nicht gelöscht und bleiben bestehen

Daher eignet sich das Verfahren nicht dazu, „eine versehentlich geänderte Einstellung auf den Stand von gestern zurückzusetzen“.
Verwenden Sie es für den Umzug auf einen neuen Server oder für die Wiederherstellung einer neu aufgebauten Umgebung.

Einstellungen auf einem anderen Server wiederherstellen
-------------------------------------------------------

1. Installieren Sie auf dem Zielserver dieselbe Version von Fess und setzen Sie ``app.cipher.key`` in ``fess_config.properties`` auf denselben Wert wie auf dem Quellserver
2. Installieren Sie die auf dem Quellserver verwendeten Plugins (Datenspeicher, SSO usw.) und starten Sie Fess neu
3. Melden Sie sich an der Administration an und öffnen Sie [Systeminformationen] > [Sicherung]
4. Wählen Sie unter „Bulk-Datei“ ``fess_basic_config.bulk`` aus und klicken Sie auf [Hochladen]. Es erscheint „Massenprozess gestartet.“
5. Laden Sie ebenso ``fess_user.bulk`` und ``system.properties`` hoch. Wenn Sie Benutzer-Tags verwenden, laden Sie auch ``fess_config.bulk`` hoch (dabei werden auch die Crawling-Informationen und Jobprotokolle des Quellservers übernommen)

Der Import läuft im Hintergrund.
Warten Sie einen Moment und prüfen Sie dann Folgendes.

- Unter [Crawler] > [Web], [Dateisystem] und [Datenspeicher] sowie unter [System] > [Scheduler] erscheinen die Einstellungen des Quellservers
- Unter [Benutzer] > [Benutzer] erscheinen die Benutzer des Quellservers
- Benachrichtigungsziele und andere Einstellungen unter [System] > [Allgemein] haben die Werte des Quellservers

Stellen Sie zum Schluss die Wörterbücher wieder her und bauen Sie die Dokumente neu auf.

- Wörterbücher: Öffnen Sie unter [System] > [Wörterbuch] den Bildschirm des jeweiligen Typs und laden Sie die gesicherte Wörterbuchdatei hoch. Führen Sie anschließend „Dokumentenindex neu laden“ unter [Systeminformationen] > [Wartung] aus. Während des Neuladens ist die Suche kurzzeitig nicht verfügbar
- Dokumente: Klicken Sie unter [System] > [Scheduler] bei „Default Crawler“ auf [Jetzt starten], um neu zu crawlen. Für die Wiederherstellung aus einem Snapshot folgen Sie den oben beschriebenen Schritten

Prüfen Sie nach Abschluss des Crawls die Anzahl der indexierten Dokumente unter [Systeminformationen] > [Crawling-Informationen].
Zeigt eine Crawl-Konfiguration mit Authentifizierung 0 Dokumente, prüfen Sie, ob ``fess-crawler.log`` ``CipherFailureException`` enthält.
Wenn ja, stimmt ``app.cipher.key`` nicht mit dem Quellserver überein.

Störungen beheben
=================

Hier sind häufige Symptome und die Stellen zusammengefasst, an denen Sie sie in Fess prüfen.

Die Suchseite öffnet sich nicht, oder /api/v2/health liefert 503
----------------------------------------------------------------

1. Prüfen Sie den Zustand von OpenSearch. Ist ``status`` in ``curl -s "http://localhost:9200/_cluster/health?pretty"`` ``red``, liegt das Problem bei OpenSearch. Unter Docker prüfen Sie ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01``
2. Ist OpenSearch in Ordnung, Fess antwortet aber nicht, prüfen Sie ``fess.log`` auf Fehler beim Start
3. Wird der Cluster direkt nach der Wiederherstellung aus einem Snapshot ``red``, wurde ``configsync`` möglicherweise nicht wiederhergestellt (siehe oben)

Crawls schlagen fehl, oder die Zahl der indexierten Dokumente ist gesunken
--------------------------------------------------------------------------

1. Öffnen Sie unter [Systeminformationen] > [Jobprotokoll] die Zeile des betreffenden Jobs und prüfen Sie „Ergebnis“
2. Vergleichen Sie unter [Systeminformationen] > [Crawling-Informationen] „Crawler-Status“ und die Indexgrößen der letzten Sitzung mit der vorherigen
3. Prüfen Sie unter [Systeminformationen] > [Fehler-URL] „Typ“, „Protokoll“ und „Fehleranzahl“ der URLs, die nicht abgerufen werden konnten. Auch HTTP 404, 403, 410 und 401 werden hier erfasst
4. Details stehen in ``fess-crawler.log``. Wenn Sie nach dem „Thread-Name“ aus den Details der Fehler-URL suchen, können Sie die Protokolleinträge rund um diesen Zeitpunkt verfolgen

Enthält ``fess-crawler.log`` ``OutOfMemoryError``, reicht der Heap des Crawler-Prozesses nicht aus.
Der Heap des Crawlers wird durch ``jvm.crawler.options`` in ``fess_config.properties`` bestimmt (Standard ``-Xmx512m``) und ist vom Heap von Fess selbst getrennt.
Wie Sie ihn anpassen, lesen Sie in :doc:`guide-14`.

Benachrichtigungen kommen nicht an
----------------------------------

Prüfen Sie bei E-Mail zunächst mit [Test-E-Mail senden] unter [Allgemein], ob E-Mails ankommen.
Kommt nur die E-Mail über abgeschlossene Crawls nicht an, prüfen Sie den SMTP-Server in ``fess_env_crawler.properties``.
Prüfen Sie unter Docker außerdem, ob die Einstellungen unter [Allgemein] verloren gegangen sind, weil der Container mit ``down`` und ``up`` neu erstellt wurde.
Kommen nur Protokollbenachrichtigungen nicht an, prüfen Sie, ob „Log Notification“ aktiviert ist, ob der Job „Log Notification“ aktiviert ist und ob „Log Notification Level“ passend gewählt ist (``WARN`` für Job-Fehler).
Weitere Prüfpunkte finden Sie unter „Fehlerbehebung“ in `Protokollbenachrichtigung <https://fess.codelibs.org/de/stable/config/admin-log-notification.html>`__.

Die Suche ist langsam
---------------------

1. Prüfen Sie auf der Registerkarte [Leistung] unter [Systeminformationen] > [Suchprotokoll], ob bestimmte Suchbegriffe langsam sind oder die Suche insgesamt
2. Vergleichen Sie ``jvm.memory.heap.percent`` und die kumulierte Dauer in ``jvm.gc`` aus ``/api/admin/stats`` mit den Werten von vor der Verlangsamung

Weiterführende Artikel
======================

- Einstellungen mit Skripten oder ``fessctl`` verwalten: :doc:`guide-16`
- Den Heap anpassen oder OpenSearch und Fess auf mehrere Server verteilen: :doc:`guide-14`
- Den Zugriffsschutz mit SSO, Audit-Protokollen usw. stärken: :doc:`guide-15`
- Die Suchqualität anhand der Suchprotokolle verbessern: :doc:`guide-08`

Referenzen
==========

- `Health-API <https://fess.codelibs.org/de/stable/api/api-health.html>`__
- `Stats API <https://fess.codelibs.org/de/stable/api/admin/api-admin-stats.html>`__
- `Protokollbenachrichtigung <https://fess.codelibs.org/de/stable/config/admin-log-notification.html>`__
- `Protokollkonfiguration <https://fess.codelibs.org/de/stable/config/admin-logging.html>`__
- `Protokolldatei <https://fess.codelibs.org/de/stable/admin/log-guide.html>`__
- `Sicherung <https://fess.codelibs.org/de/stable/admin/backup-guide.html>`__
- `Backup API <https://fess.codelibs.org/de/stable/api/admin/api-admin-backup.html>`__
- `Index-Verwaltung <https://fess.codelibs.org/de/stable/config/admin-index-backup.html>`__
- `Fehler-URLs <https://fess.codelibs.org/de/stable/admin/failureurl-guide.html>`__
- `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__
