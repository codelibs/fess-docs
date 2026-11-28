====================================================
Fess-Konfiguration als Code reproduzierbar verwalten
====================================================

Einleitung
==========

Bei Einstellungen, die über die Administrationsoberfläche angesammelt wurden, lässt sich später nicht nachvollziehen, wer wann was geändert hat.
Und wenn Sie in einer Testumgebung geprüfte Einstellungen in die Produktion übernehmen, wiederholen Sie dieselben Bildschirmschritte von Hand.

In diesem Artikel schreiben wir die Einstellungen von Fess 15.9 als Dateien in ein Git-Repository, wenden sie per Skript auf eine neu gestartete Docker-Umgebung an und prüfen, dass sie angewendet wurden.
Dazu verwenden wir die Compose-Dateien von docker-fess, die Admin API von Fess und deren Kommandozeilen-Client fessctl.

Den Umfang von Sicherungen und das Wiederherstellungsverfahren behandeln wir hier nicht.
Siehe dazu :doc:`guide-10`.

Verwaltungsweise je nach Speicherort festlegen
==============================================

Die Einstellungen von Fess liegen nicht an einem einzigen Ort.
Wie Sie sie als Code abbilden, hängt davon ab, wo sie gespeichert sind.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Einstellung
     - Speicherort
     - Abbildung als Code
   * - Fess-Version, Plugins
     - Docker-Image, Container
     - Image-Tag in der Compose-Datei und ``FESS_PLUGINS``
   * - Einträge in ``fess_config.properties`` (z. B. ``app.cipher.key``)
     - Datei im Container
     - ``-Dfess.config.<Schlüssel>`` in ``FESS_JAVA_OPTS``
   * - Einträge unter [System] > [Allgemein]
     - ``system.properties`` im Container
     - ``-Dfess.system.<Schlüssel>`` in ``FESS_JAVA_OPTS``
   * - Crawl-Konfigurationen, Labels, Scheduler, Benutzer usw.
     - Konfigurationsindizes in OpenSearch
     - Admin API (fessctl)
   * - Wörterbücher (Synonyme usw.)
     - ``FESS_DICTIONARY_PATH`` im OpenSearch-Container
     - Wörterbuch-Upload über die Admin API (fessctl)
   * - Zugriffstokens, Wert des Verschlüsselungsschlüssels
     - Tokens in OpenSearch, Verschlüsselungsschlüssel in den Startoptionen
     - Nicht in Git, sondern in ``.env`` oder in CI-Secrets ablegen

Der Container ``fess01`` von docker-fess hat kein Volume, daher verschwindet ``system.properties`` bei ``docker compose down`` zusammen mit dem Container.
In OpenSearch gespeicherte Einstellungen wie Crawl-Konfigurationen bleiben im Volume erhalten.

Aufbau des Repositorys
======================

In diesem Artikel verwalten wir die folgenden Dateien mit Git.

::

    fess-infra/
    ├── compose.yaml               Datei aus docker-fess v15.9.0
    ├── compose-opensearch3.yaml   Datei aus docker-fess v15.9.0
    ├── compose-site.yaml          Abweichungen für die eigene Umgebung
    ├── dict/
    │   └── synonym.txt            Synonym-Wörterbuch
    ├── apply.sh                   Skript, das die Einstellungen anwendet
    ├── .gitignore
    └── .env                       nicht in Git (Verschlüsselungsschlüssel und Token)

Docker-Aufbau auf eine Version festlegen
========================================

Compose-Dateien abrufen
-----------------------

Rufen Sie die Dateien des Tags ``v15.9.0`` von docker-fess ab.
``compose.yaml`` verweist auf das Image ``ghcr.io/codelibs/fess:15.9.0`` und ``compose-opensearch3.yaml`` auf ``ghcr.io/codelibs/fess-opensearch:3.9.0``, damit sind die Versionen festgelegt.

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

Bearbeiten Sie diese beiden Dateien nicht, sondern schreiben Sie die Abweichungen Ihrer Umgebung in eine separate Datei.
Bei einem Versionswechsel von docker-fess müssen Sie dann nur die Dateien neu abrufen.

Abweichungen der eigenen Umgebung schreiben
-------------------------------------------

Erstellen Sie ``compose-site.yaml``.

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- In ``FESS_PLUGINS`` geben Sie die beim Start herunterzuladenden Plugins im Format ``Name:Version`` durch Leerzeichen getrennt an. Verwenden Sie dieselbe Version 15.9.x wie Fess. Das Plugin ``fess-ds-git`` im Beispiel dient dazu, Git-Repositorys über einen Datenspeicher zu crawlen. Die Download-Quelle ist fest auf ``maven.codelibs.org`` eingestellt, daher können Sie hier nur veröffentlichte Plugins angeben, und der Container muss ins Internet gelangen können
- ``-Dfess.config.<Schlüssel>`` hat Vorrang vor dem gleichnamigen Eintrag in ``fess_config.properties``
- ``-Dfess.system.<Schlüssel>`` wird zum Standardwert eines Eintrags unter [Allgemein]. ``purge.searchlog.day`` im Beispiel ist die Anzahl der Tage bei „Alte Suchprotokolle löschen“ unter [Allgemein]

Compose führt ``environment`` pro Variablenname zusammen, daher bleiben ``SEARCH_ENGINE_HTTP_URL`` und die übrigen Variablen aus ``compose.yaml`` erhalten.
Wenn Sie jedoch dieselbe Variable in mehreren Dateien setzen, wird sie durch den Wert aus der späteren Datei ersetzt.
Overlays wie ``compose-openai.yaml`` setzen ebenfalls ``FESS_PLUGINS`` und ``FESS_JAVA_OPTS``; wenn Sie sie kombinieren, fassen Sie die Werte in einer Datei zusammen.

.. note::

   ``-Dfess.system.<Schlüssel>`` wird nur verwendet, wenn ``system.properties`` den Schlüssel nicht enthält.
   Sobald Sie [Allgemein] in der Administrationsoberfläche einmal speichern oder ``fessctl general update`` ausführen, werden alle Einträge dieses Bildschirms in ``system.properties`` geschrieben, und von da an haben diese Werte Vorrang.
   In diesem Zustand wirkt eine Änderung des Werts in ``compose-site.yaml`` erst, wenn Sie mit ``down`` den Container neu erstellen.

Verschlüsselungsschlüssel festlegen
-----------------------------------

``app.cipher.key`` ist der Schlüssel, mit dem die Passwörter der Web- und Dateiauthentifizierung sowie geheime Werte in den Parametern von Crawl- und Datenspeicher-Konfigurationen verschlüsselt werden.
Verwenden Sie nicht den Standardwert ``___change__me___``, sondern legen Sie den Schlüssel vor dem ersten Start fest.

Die Schlüsselzeichenkette wird unverändert als AES-Schlüssel verwendet und muss daher 16, 24 oder 32 Byte lang sein.
Die Ausgabe von ``openssl rand -hex 16`` (32 Hexadezimalzeichen) ist 32 Byte lang.

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

Wenn Sie den Schlüssel ändern, nachdem Anmeldedaten gespeichert wurden, lassen sich die gespeicherten Werte nicht mehr entschlüsseln, und Crawls, die diese Einstellungen verwenden, schlagen fehl.
Auch wenn Sie eine Sicherung in einer anderen Umgebung wiederherstellen, brauchen Sie denselben Schlüssel (:doc:`guide-10`).
Bewahren Sie ihn zusätzlich zu ``.env`` auch an anderer Stelle auf, etwa in einem Passwortmanager.

Der Wert von ``FESS_JAVA_OPTS`` ist über ``docker inspect`` sichtbar.
Wenn Sie das vermeiden möchten, mounten Sie stattdessen ``fess_config.properties`` unter ``/opt/fess`` (siehe „Anwendung von Konfigurationsdateien“ in `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__).

Starten
-------

Geben Sie bei jedem Compose-Befehl alle drei Dateien an.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

Der Health-Check von ``fess01`` ruft ``/api/v2/health`` auf; sobald ``docker compose ... ps`` für ``fess01`` den Status ``(healthy)`` anzeigt, ist alles bereit.

Zugriffstoken für die Admin API erstellen
=========================================

Für Aufrufe der Admin API ist ein Zugriffstoken erforderlich, und auch die API zum Erstellen von Tokens lässt sich nicht ohne Token aufrufen.
Daher erstellen Sie das erste Token in jeder neuen Umgebung einmalig über die Administrationsoberfläche.

1. Melden Sie sich unter ``http://localhost:8080/admin/`` mit ``admin`` / ``admin`` an und legen Sie das geforderte neue Passwort fest (mindestens 8 Zeichen)
2. Öffnen Sie [System] > [Zugriffstoken] und klicken Sie auf [Neu erstellen]
3. Geben Sie bei „Name“ ``fess-infra`` und bei „Berechtigungen“ ``{role}admin-api`` ein und klicken Sie auf [Erstellen]
4. Öffnen Sie das erstellte Token in der Liste und kopieren Sie den Wert von „Token“

Hängen Sie den kopierten Wert an ``.env`` an.

::

    $ echo 'FESS_ACCESS_TOKEN=<kopierter Wert>' >> .env

Ein Token mit ``{role}admin-api`` kann alle Operationen der Admin API ausführen.
Dazu gehören das Ändern von Einstellungen, das Anlegen von Benutzern und das Herunterladen von Sicherungen; ein auf einen bestimmten Zweck beschränktes Token lässt sich nicht erstellen.
Behandeln Sie es wie das Administratorpasswort und legen Sie es weder in Git noch in JavaScript ab, das im Browser läuft.

fessctl vorbereiten
===================

fessctl ist ein Kommandozeilenwerkzeug, das die Admin API aufruft.
Installieren Sie mit fester Version die Version 0.4.0, deren Standardwerte für Fess 15.9 ausgelegt sind.
Python 3.13 oder höher ist erforderlich.

::

    $ pipx install fessctl==0.4.0

``uv tool install fessctl==0.4.0`` funktioniert ebenfalls.
Die folgenden Skripte verwenden außerdem ``jq`` und ``curl``, um Werte aus den Antworten zu extrahieren.

fessctl liest den Endpunkt aus ``FESS_ENDPOINT`` (Standardwert ``http://localhost:8080``), das Token aus ``FESS_ACCESS_TOKEN`` und die Version des verbundenen Fess aus ``FESS_VERSION``.
Setzen Sie ``FESS_VERSION`` auf ``15.9.0``.
Der Grund ist, dass sich die Art der API-Aufrufe je nach Version unterscheidet.

Prüfen Sie die Verbindung.

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

``ping`` endet mit dem Exit-Code 0, wenn der Clusterstatus GREEN oder YELLOW ist.
Der Health-Check funktioniert auch ohne Token, prüfen Sie die Gültigkeit des Tokens daher mit ``webconfig list``.
Bei einem Authentifizierungsfehler überprüfen Sie den Wert des Tokens und seine Berechtigungen.
Mit ``-o json`` gibt jeder Befehl die Antwort der Admin API unverändert aus, sodass Sie Werte mit ``jq`` extrahieren können.

Ausgangsstand des Wörterbuchs in Git aufnehmen
----------------------------------------------

Das Hochladen eines Wörterbuchs ersetzt die gesamte Datei.
Damit der Standardinhalt nicht verloren geht, laden Sie zunächst das aktuelle Synonym-Wörterbuch herunter, nehmen es in das Repository auf und bearbeiten es dort.

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

Die heruntergeladene Datei enthält bereits die Standard-Synonymzeile ``fess,フエス``.
Fügen Sie am Ende der Datei eine Synonymzeile hinzu.
Durch Kommas getrennte Wörter sind austauschbar: Wer nach einem davon sucht, findet auch Dokumente, die die anderen enthalten (zum Format siehe `Synonym-Wörterbuch <https://fess.codelibs.org/de/stable/admin/synonym-guide.html>`__).

::

    einstellung,konfiguration

Japanische Wörter tragen Sie ein, indem Sie Hiragana als Katakana, kleine Katakana als normal große Katakana („フェス“ wird zu „フエス“) und Alphanumerik voller Breite als halbbreite Zeichen schreiben.

Skript zum Anwenden der Einstellungen
=====================================

In ``apply.sh`` schreiben Sie die Einstellungen, die die Umgebung erhalten soll, als fessctl-Befehle.
Das Skript ist dafür gedacht, auf eine neue Umgebung angewendet zu werden; existiert aber bereits eine Einstellung mit demselben Namen, überspringt es die Erstellung, sodass ein erneuter Lauf keine Duplikate erzeugt.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # Label: wird beim Crawlen an Dokumente vergeben, die zum Zielpfad passen
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Fess-Dokumentation" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/de/stable/.*' \
        --permission '{role}guest'
    fi

    # Web-Crawl-Konfiguration
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Fess-Suchanleitung")' > /dev/null; then
      fessctl webconfig create --name "Fess-Suchanleitung" \
        --url https://fess.codelibs.org/de/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/de/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # Synonym-Wörterbuch: ganze Datei ersetzen, Dokumentenindex neu öffnen, damit es geladen wird
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # Crawl starten und auf das Ende des Jobs warten
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

Die wichtigsten Punkte des Skripts sind:

- Mit der standardmäßigen Textausgabe endet fessctl mit einem Exit-Code ungleich 0, wenn die API einen Fehler zurückgibt, sodass ``set -e`` das Skript an dieser Stelle anhält. Mit ``-o json`` geben viele Befehle die Fehlerantwort aus und enden mit 0, daher wird der extrahierte Wert mit ``jq -e`` geprüft. Fehlt der Wert, schlägt jq fehl, und das Skript hält dort an
- ``--version-no`` von ``labeltype create`` ist in fessctl 0.4.0 Pflicht. Geben Sie bei einer Neuanlage ``1`` an
- Bei ``webconfig create`` weggelassene Einträge erhalten die Standardwerte von fessctl. ``--depth`` ist ``1`` und ``--max-access-count`` ist ``1000000``, schreiben Sie die gewünschten Werte also explizit aus. Der Standardwert von ``--permission`` ist ``{role}guest``
- Der Wert eines Labels darf nur alphanumerische Zeichen und ``_`` enthalten. Labels werden beim Crawlen vergeben, legen Sie sie daher vor der Crawl-Konfiguration an
- Ohne ``--yes`` hält der Wörterbuch-Upload an und fragt nach einer Bestätigung
- Das Synonym-Wörterbuch wirkt zur Suchzeit, OpenSearch erstellt Analyzer aber nur beim Öffnen eines Index. Deshalb wird das Wörterbuch zuerst mit ``_configsync/flush`` in eine Datei geschrieben und anschließend ``fess.update`` geschlossen und wieder geöffnet. Währenddessen ist keine Suche möglich; führen Sie das Skript in einer laufenden Umgebung daher zu einer Zeit mit wenig Zugriffen aus. Es ist dieselbe Operation wie „Dokumentenindex neu laden“ unter [Systeminformationen] > [Wartung] in der Administrationsoberfläche
- ``job_log_id`` in der Antwort von ``scheduler start`` ist direkt die ID im [Jobprotokoll]. Das Skript wartet, bis der Jobstatus ``ok`` oder ``fail`` ist, und endet als Fehlschlag, wenn er nicht ``ok`` ist. „Default Crawler“ führt alle aktivierten Crawl-Konfigurationen aus

Wenn Sie den Wert einer bereits vorhandenen Einstellung ändern, überspringt dieses Skript nur die Erstellung und überschreibt den Wert nicht.
Aktualisieren Sie die Einstellung entweder per ID, etwa mit ``fessctl webconfig update <ID> --max-access-count 100``, oder führen Sie das Skript erneut auf einer samt Volumes neu aufgebauten Umgebung aus.

Wenn Sie das Skript aus einer CI ausführen, legen Sie keine ``.env`` ab, sondern übergeben ``FESS_ACCESS_TOKEN`` und ``FESS_ENDPOINT`` als Umgebungsvariablen aus den CI-Secrets.
Ersetzen Sie in diesem Fall in den drei Zeilen mit ``localhost:9200`` das Ziel durch eine Adresse, unter der OpenSearch erreichbar ist.

Anwendung der Einstellungen prüfen
==================================

Wenn ``apply.sh`` mit dem Exit-Code 0 endet, prüfen Sie Folgendes in dieser Reihenfolge.

1. Das Plugin ist installiert

   ::

       $ fessctl plugin installed

   Wenn ``fess-ds-git`` 15.9.0 in der Liste steht, ist es installiert.
   Schlägt der Download eines Plugins aus ``FESS_PLUGINS`` fehl, startet Fess trotzdem, und in ``docker compose ... logs fess01`` erscheint lediglich ``Failed to download``; prüfen Sie es daher hier.

2. Der Wert unter [Allgemein] wurde übernommen

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   Wird ``180`` zurückgegeben, ist ``-Dfess.system.purge.searchlog.day`` wirksam.
   In der Admin API sind die Namen in snake_case wie ``purge_search_log_day`` geschrieben und unterscheiden sich von den Schlüsseln nach ``-Dfess.system.``.

3. Das Wörterbuch wurde ersetzt

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep 'konfiguration'

   Wird die hinzugefügte Zeile angezeigt, war der Upload erfolgreich.
   Sie können auch mit ``fessctl dict synonym list`` prüfen, standardmäßig werden aber 100 Einträge pro Seite angezeigt, sodass eine am Ende hinzugefügte Zeile möglicherweise nicht auf der ersten Seite erscheint.

4. Die Suche mit Label funktioniert

   ::

       $ curl -fsS --get --data-urlencode 'q=Suche' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   Wird 1 oder mehr zurückgegeben, funktioniert die gesamte Kette aus Crawlen, Labelvergabe und Suche.
   Bei 0 prüfen Sie in der Administrationsoberfläche [Systeminformationen] > [Fehler-URL] und das Ergebnis im [Jobprotokoll].

Admin API direkt aufrufen
=========================

fessctl ruft die Admin API unter ``/api/admin/`` auf.
Alle Ressourcen, die Einstellungen enthalten, etwa Crawl-Konfigurationen, haben die folgende Form (``<resource>`` ist ``webconfig``, ``fileconfig``, ``dataconfig``, ``labeltype``, ``keymatch`` usw.).

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Anfrage
     - Operation
   * - ``GET /api/admin/<resource>/settings``
     - Liste
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - Einen Eintrag abrufen
   * - ``POST /api/admin/<resource>/setting``
     - Erstellen
   * - ``PUT /api/admin/<resource>/setting``
     - Aktualisieren
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - Löschen

fessctl hat gleichnamige Unterbefehle (``create``, ``list``, ``get``, ``update``, ``delete``), und Sie können die Einträge etwa mit ``fessctl fileconfig create --help`` nachsehen.
Ein Wörterbuch-Upload wird als multipart an ``POST /api/admin/dict/<Typ>/upload/<Wörterbuch-ID>`` gesendet.
Der Name des Dateifelds unterscheidet sich je nach Typ; bei Synonymen ist es ``synonymFile``.
Die JSON-Feldnamen sind in snake_case geschrieben, z. B. ``max_access_count``.
Zu den einzelnen Feldern siehe die Seiten der jeweiligen Ressourcen, die von `Admin API Übersicht <https://fess.codelibs.org/de/stable/api/admin/api-admin-overview.html>`__ aus erreichbar sind.

Der folgende Befehl gibt die Anzahl der Web-Crawl-Konfigurationen zurück.

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

Ohne ``-f`` behandelt curl auch eine 404- oder 401-Antwort als Erfolg, und das Skript bemerkt den Fehler nicht.

Kopie der Einstellungen herunterladen
=====================================

Für Einstellungen, die nicht in Git stehen (etwa direkt in der Administrationsoberfläche geänderte), laden Sie zusätzlich regelmäßig Sicherungen herunter.
Die betroffenen Dateien und das Wiederherstellungsverfahren werden in :doc:`guide-10` beschrieben.
Hier zeigen wir nur ein Beispielskript, das mit derselben Vorbereitung wie ``apply.sh`` läuft.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_VERSION=15.9.0
    dest="backup/$(date +%Y%m%d)"
    umask 077
    mkdir -p "$dest"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      fessctl backup download "$id" --dest "$dest/$id" --force
    done

``fessctl backup download`` ruft ``/api/admin/backup/file/<ID>/`` mit dem abschließenden ``/`` auf, der nötig ist, wenn die ID einen Punkt enthält.
Wenn Sie den Aufruf mit curl machen, vergessen Sie das abschließende ``/`` und ``-f`` nicht.
Ohne das abschließende ``/`` erhalten Sie 404.

Über die Admin API ist nur das Herunterladen möglich; eine Wiederherstellung lässt sich nur über [Systeminformationen] > [Sicherung] in der Administrationsoberfläche durchführen.
Sicherungen ergeben also kein Verfahren, mit dem sich eine andere Umgebung neu aufbauen lässt; halten Sie die maßgebliche Fassung der Einstellungen daher in ``apply.sh``.

Was nicht in Git gehört
=======================

- ``.env`` (Verschlüsselungsschlüssel und Zugriffstoken)
- Sicherungsdateien. ``*.bulk`` enthält auch unverschlüsselte Werte und muss als vertrauliche Datei behandelt werden. Auch ``system.properties`` enthält unter [Allgemein] eingegebene Werte wie geheime Schlüssel für Speicher oder Client-Secrets für SSO

Aus diesem Grund wurden ``.env`` und ``backup/`` in ``.gitignore`` aufgenommen.
Bewahren Sie Sicherungen an einem Ort mit eingeschränktem Zugriff auf, etwa in verschlüsseltem Speicher.

Weiterführende Artikel
======================

- Sicherungsumfang, Wiederherstellung und Überwachung einrichten: :doc:`guide-10`
- Grundlagen zum Starten und Stoppen mit Docker nachlesen: :doc:`guide-02`
- Die Such-API aus Geschäftssystemen aufrufen: :doc:`guide-11`
- Die Administrationsoberfläche einschließlich Umgang mit Zugriffstokens und SSO absichern: :doc:`guide-15`
- Eigene Plugins entwickeln: :doc:`guide-17`

Referenzen
==========

- `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__
- `Admin API Übersicht <https://fess.codelibs.org/de/stable/api/admin/api-admin-overview.html>`__
- `Dict API <https://fess.codelibs.org/de/stable/api/admin/api-admin-dict.html>`__
- `Backup API <https://fess.codelibs.org/de/stable/api/admin/api-admin-backup.html>`__
- `Wörterbuch (Zeitpunkt der Übernahme) <https://fess.codelibs.org/de/stable/admin/dict-guide.html>`__
- `Zugriffstoken <https://fess.codelibs.org/de/stable/admin/accesstoken-guide.html>`__
- `fessctl (GitHub) <https://github.com/codelibs/fessctl>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
