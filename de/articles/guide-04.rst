==============================================
Websites und Dateiserver gemeinsam durchsuchen
==============================================

Einführung
==========

Interne Dokumente liegen oft verteilt an mehreren Orten: im Intranet-Portal, in den Freigabeordnern der Abteilungen, in einem Verzeichnis, in dem alte Unterlagen archiviert werden, und so weiter.
Wer etwas sucht, muss sich zuerst erinnern, wo es liegt, und dann an jedem Ort einzeln suchen.

In diesem Artikel crawlen wir mit Fess 15.9 die folgenden drei Orte, sodass sie sich über ein einziges Suchfeld durchsuchen lassen.
Auf der Suchseite sorgen wir dafür, dass sich die Ergebnisse mit Labels eingrenzen lassen, etwa auf „nur das Portal“ oder „nur den Freigabeordner“.

- Das Intranet-Portal (eine Website)
- Ein Freigabeordner auf einem Windows-Dateiserver (SMB)
- Ein Archivverzeichnis auf dem Server (lokale Dateien)

Die Schritte setzen die in :doc:`guide-02` gestartete Docker-Umgebung voraus (``fess01`` und ``search01``).
Cloud-Speicher wie Google Drive, SharePoint und Box werden in :doc:`guide-07` behandelt.
Was vor der Einführung einer Dateiserver-Suche zu prüfen ist, fasst :doc:`file-server-search` zusammen.

Was wir aufbauen
================

.. list-table::
   :header-rows: 1
   :widths: 18 40 14 28

   * - Ziel
     - Zu crawlender Pfad
     - Wert des Labels
     - Crawl-Ausführung
   * - Intranet-Portal
     - ``https://portal.example.com/``
     - ``portal``
     - Täglich um 2:00 Uhr
   * - Freigabeordner
     - ``smb://fileserver.example.com/shared/``
     - ``shared``
     - Täglich um 3:00 Uhr
   * - Archiv
     - ``file:/data/archive/`` (``/srv/archive`` auf dem Host)
     - ``archive``
     - Jeden Sonntag um 4:00 Uhr

Hostnamen und Verzeichnisse sind Beispiele.
Passen Sie sie an Ihre eigene Umgebung an.
Vorausgesetzt werden ein Dienstkonto, das den Freigabeordner lesen kann (Lesezugriff genügt), und dass der Container ``fess01`` den SMB-Port (445) des Dateiservers erreicht.

Labels werden beim Crawlen vergeben, deshalb legen Sie sie vor den Crawl-Konfigurationen an.
Gehen Sie in der Reihenfolge der Abschnitte dieses Artikels vor.

Das Archivverzeichnis im Container lesbar machen
================================================

In der ``compose.yaml`` von docker-fess v15.9.0 sind für ``fess01`` keine Volumes definiert.
Daher ist ``/srv/archive`` des Hosts im Container zunächst nicht sichtbar.
Fügen Sie in ``compose.yaml`` bei ``fess01`` den Eintrag ``volumes`` hinzu und ergänzen Sie unter ``environment`` außerdem eine Zeile ``FESS_JAVA_OPTS``.

.. code-block:: yaml

    services:
      fess01:
        image: ghcr.io/codelibs/fess:15.9.0
        container_name: fess01
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "FESS_DICTIONARY_PATH=${FESS_DICTIONARY_PATH:-/usr/share/opensearch/config/dictionary/}"
          - "FESS_JAVA_OPTS=-Duser.timezone=Asia/Tokyo -Dfess.system.day.for.cleanup=10"
        volumes:
          - /srv/archive:/data/archive:ro
        # ports und alles Weitere bleiben unverändert

- ``/srv/archive:/data/archive:ro`` bindet ``/srv/archive`` des Hosts schreibgeschützt unter ``/data/archive`` im Container ein
- ``-Duser.timezone=Asia/Tokyo`` sorgt dafür, dass die Ausführungszeiten der später eingerichteten Jobs in japanischer Zeit gelten. Weder compose.yaml noch das Image legen eine Zeitzone fest; ohne diese Angabe laufen die Jobs daher zu Zeiten, die von der japanischen Zeit abweichen
- ``-Dfess.system.day.for.cleanup=10`` setzt den Standardwert für die Ablauffrist von Dokumenten (in Tagen) auf 10 Tage. Der Grund wird später unter „Wöchentliche Jobs und Ablauf von Dokumenten“ erläutert

Erstellen Sie die Container nach der Änderung neu.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Da ``fess01`` neu erstellt wird, gehen alle Einstellungen verloren, die Sie bis dahin unter [System] > [Allgemein] geändert haben (siehe „Stoppen und Neustarten“ in :doc:`guide-02`).
Nehmen Sie Änderungen unter [Allgemein] erst nach diesem Schritt vor.

Fess läuft im Container als Benutzer ``fess`` (UID 1001).
Prüfen Sie, ob dieser Benutzer die Dateiliste sehen kann.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml exec -u fess fess01 ls /data/archive

Erhalten Sie ``Permission denied``, machen Sie alles unterhalb von ``/srv/archive`` auf dem Host für UID 1001 lesbar (zum Beispiel, indem Sie anderen Benutzern Leserechte und auf Verzeichnissen das Ausführungsrecht geben).

Labels anlegen
==============

Ein Label wird vergeben, wenn die URL eines Dokuments auf einen regulären Ausdruck passt.
In den Crawl-Konfigurationen gibt es kein Feld zur Auswahl eines Labels (es ist standardmäßig ausgeblendet), deshalb legen Sie den Geltungsbereich im Feld „Eingeschlossene Pfade“ des Labels fest.

Legen Sie unter [Crawler] > [Label] > [Neu erstellen] die folgenden drei Labels an.

.. list-table::
   :header-rows: 1
   :widths: 18 14 68

   * - Name
     - Wert
     - Eingeschlossene Pfade
   * - Portal
     - ``portal``
     - ``https://portal.example.com/.*``
   * - Freigabeordner
     - ``shared``
     - ``smb://fileserver.example.com/shared/.*``
   * - Archiv
     - ``archive``
     - ``file:/data/archive/.*``

- „Name“ ist der Text, der auf der Suchseite angezeigt wird; er darf auch Nicht-ASCII-Zeichen wie Umlaute oder Japanisch enthalten
- „Wert“ erlaubt nur alphanumerische Zeichen und Unterstriche (Bindestriche und Nicht-ASCII-Zeichen führen zu einem Eingabefehler)
- „Eingeschlossene Pfade“ muss auf die gesamte URL passen, lassen Sie das abschließende ``.*`` also nicht weg. Bleibt das Feld leer, wird das Label keinem Dokument zugewiesen
- In „Berechtigungen“ steht ``{role}guest``. Damit wird das Label auch nicht angemeldeten Benutzern angezeigt; lassen Sie es so

Dokumente, die vor dem Anlegen der Labels gecrawlt wurden, haben kein Label.
Wenn Sie Labels später hinzufügen oder ändern, übernehmen Sie sie für vorhandene Dokumente, indem Sie erneut crawlen oder unter [System] > [Scheduler] den Job „Label Updater“ mit [Jetzt starten] ausführen.

Crawl-Konfigurationen anlegen
=============================

Intranet-Portal (Web-Crawl)
---------------------------

Geben Sie unter [Crawler] > [Web] > [Neu erstellen] die folgenden Felder ein und klicken Sie auf [Erstellen].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Wert
   * - Name
     - ``Intranet-Portal``
   * - URLs
     - ``https://portal.example.com/``
   * - Eingeschlossene URLs
     - ``https://portal.example.com/.*``
   * - Ausgeschlossene URLs
     - ``https://portal.example.com/admin/.*`` unter den bereits vorhandenen Zeilen hinzufügen

„Ausgeschlossene URLs“ enthält von Anfang an reguläre Ausdrücke, die Bilder, CSS und Ähnliches ausschließen.
Löschen Sie diese nicht, sondern fügen Sie eine Zeile hinzu.
„Anzahl der Threads“ ist standardmäßig ``1`` und „Intervall“ ``10000`` Millisekunden – Einstellungen, die die Last auf dem Portal gering halten.

Freigabeordner (SMB) und Datei-Authentifizierung
------------------------------------------------

Legen Sie zunächst unter [Crawler] > [Dateisystem] > [Neu erstellen] die folgende Konfiguration an.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Wert
   * - Name
     - ``Freigabeordner``
   * - Pfade
     - ``smb://fileserver.example.com/shared/``
   * - Eingeschlossene Pfade
     - ``smb://fileserver.example.com/shared/.*``
   * - Ausgeschlossene Pfade
     - ``.*\.tmp$``

Beim Datei-Crawl ist „Anzahl der Threads“ standardmäßig ``5`` und „Intervall“ ``1000`` Millisekunden.

Verknüpfen Sie als Nächstes das Dienstkonto mit dieser Konfiguration.
Eine Datei-Authentifizierung wird angelegt, indem man eine Datei-Crawl-Konfiguration auswählt.
Solange noch keine Datei-Crawl-Konfiguration existiert, wird auf der Seite [Datei-Authentifizierung] kein [Neu erstellen] angezeigt.

Geben Sie unter [Crawler] > [Datei-Authentifizierung] > [Neu erstellen] die folgenden Felder ein und klicken Sie auf [Erstellen].

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Wert
   * - Hostname
     - ``fileserver.example.com`` (genau so geschrieben wie der Hostname im Pfad)
   * - Port
     - Leer lassen
   * - Schema
     - ``Samba``
   * - Benutzername / Passwort
     - Die des Dienstkontos
   * - Parameter
     - Bei einem Domänenkonto den Domänennamen angeben, etwa ``domain=EXAMPLE``
   * - Datei-Crawl-Konfiguration
     - ``Freigabeordner``

„Hostname“ muss buchstabengetreu mit dem Hostnamen im Pfad übereinstimmen.
Haben Sie den Pfad mit einer IP-Adresse angegeben, tragen Sie auch hier die IP-Adresse ein.
Eine Authentifizierung mit leerem „Port“ wird für Pfade ohne Portangabe verwendet, etwa ``smb://Hostname/Freigabename/``.

.. note::

   Über SMB gecrawlte Dateien erhalten standardmäßig Rollen, die aus den Zugriffsrechten (ACL) der Datei abgeleitet werden, und diese werden zu den „Berechtigungen“ der Crawl-Konfiguration hinzugefügt.
   Solange der Standardwert ``{role}guest`` in „Berechtigungen“ verbleibt, können alle danach suchen, auch nicht angemeldete Benutzer.
   Wenn Sie Suchergebnisse je nach Zugriffsrechten unterschiedlich anzeigen möchten, lesen Sie :doc:`file-server-search` und :doc:`guide-05`.

Archiv (lokale Dateien)
-----------------------

Legen Sie unter [Crawler] > [Dateisystem] > [Neu erstellen] die folgende Konfiguration an.
Geben Sie den Pfad so an, wie er im Container lautet.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Feld
     - Wert
   * - Name
     - ``Archiv``
   * - Pfade
     - ``file:/data/archive/``
   * - Eingeschlossene Pfade
     - ``file:/data/archive/.*``
   * - Ausgeschlossene Pfade
     - ``.*\.(log|bak)$``

Lokale Dateien schreiben Sie mit einem einzigen Schrägstrich nach ``file:``, also ``file:/data/archive/``.
Die URLs der Dateien, die der Crawler findet, haben die Form ``file:/data/archive/2020/report.pdf``, und „Eingeschlossene Pfade“ wird mit diesen URLs abgeglichen.
Schreiben Sie ``file:///data/archive/.*``, passt das auf keine Datei, und es wird kein einziges Dokument indexiert.

Einen Job pro Konfiguration anlegen
===================================

Der Job „Default Crawler“ im Scheduler führt alle aktivierten Crawl-Konfigurationen gemeinsam täglich um 0:00 Uhr aus.
Um jedes Ziel zu einer eigenen Uhrzeit auszuführen, legen Sie für jede Crawl-Konfiguration einen Job an.

1. Klicken Sie unter [Crawler] > [Web] auf „Intranet-Portal“ und dann auf der Detailseite auf [Neuen Job erstellen]
2. Die Seite zum Anlegen des Jobs öffnet sich; „Name“ enthält ``Web Crawler - Intranet-Portal`` und „Skript“ einen Inhalt, der nur diese Konfiguration crawlt
3. „Zeitplan“ ist leer; geben Sie einen Cron-Ausdruck ein und klicken Sie auf [Erstellen]
4. Gehen Sie unter [Crawler] > [Dateisystem] für „Freigabeordner“ und „Archiv“ genauso vor (die Namen lauten dann etwa ``File Crawler - Freigabeordner``)

.. list-table::
   :header-rows: 1
   :widths: 40 25 35

   * - Job
     - Zeitplan
     - Bedeutung
   * - ``Web Crawler - Intranet-Portal``
     - ``0 2 * * *``
     - Täglich um 2:00 Uhr
   * - ``File Crawler - Freigabeordner``
     - ``0 3 * * *``
     - Täglich um 3:00 Uhr
   * - ``File Crawler - Archiv``
     - ``0 4 * * 0``
     - Jeden Sonntag um 4:00 Uhr

Ein Cron-Ausdruck hat die Reihenfolge „Minute Stunde Tag Monat Wochentag“; der Wochentag ``0`` steht für Sonntag.

Verhindern Sie zum Schluss, dass „Default Crawler“ dieselben Konfigurationen um 0:00 Uhr noch einmal crawlt.
Klicken Sie unter [System] > [Scheduler] auf „Default Crawler“, leeren Sie mit [Bearbeiten] das Feld „Zeitplan“ und klicken Sie auf [Aktualisieren].
Lassen Sie unter „Status“ das Häkchen bei „Aktiviert“ gesetzt, können Sie den Job weiterhin mit [Jetzt starten] ausführen, wenn Sie alle Konfigurationen gemeinsam crawlen möchten (wird er deaktiviert, erscheint [Jetzt starten] nicht mehr).

Wöchentliche Jobs und Ablauf von Dokumenten
-------------------------------------------

Durch einen Crawl indexierte Dokumente erhalten eine Ablauffrist; ist sie überschritten, löscht der Job „Doc Purger“ (läuft jede Minute) sie aus dem Index.
Die Ablauffrist ist der Startzeitpunkt des Crawls plus die Anzahl Tage aus „Alte Dokumente löschen“ unter [System] > [Allgemein]; der Standardwert beträgt ``3`` Tage.
Findet der nächste Crawl dieselbe Datei, wird die Ablauffrist verlängert.

Mit dem Standardwert sind die Dokumente des Archivs, das nur sonntags gecrawlt wird, ab Mittwoch nicht mehr auffindbar.
Diese Anzahl Tage muss daher größer sein als das längste Crawl-Intervall (7 Tage).
In diesem Artikel verwenden wir ``10`` Tage, mit etwas Spielraum, damit die Dokumente auch dann nicht verschwinden, wenn ein Job einmal fehlschlägt.

- In der Docker-Umgebung wird das oben genannte ``-Dfess.system.day.for.cleanup=10`` zu diesem Standardwert. Werte unter [Allgemein] gehen verloren, wenn ``fess01`` neu erstellt wird; der Eintrag in compose.yaml ist daher zuverlässiger
- In Umgebungen ohne Docker setzen Sie unter [Allgemein] „Alte Dokumente löschen“ auf ``10`` und klicken auf [Aktualisieren]

Wenn Sie diese Anzahl Tage erhöhen, bleiben auch Dateien, die vom Dateiserver gelöscht wurden, nach dem letzten Crawl, der sie gefunden hat, bis zu dieser Anzahl Tage in den Suchergebnissen.

Ausführen und Ergebnisse prüfen
===============================

Jobs ausführen
--------------

Statt bis zum nächsten Tag zu warten, klicken Sie unter [System] > [Scheduler] nacheinander auf die drei Jobs und jeweils auf [Jetzt starten].

Abschluss prüfen
----------------

1. Warten Sie unter [Systeminformationen] > [Jobprotokoll], bis der „Status“ der drei Jobs von „Wird ausgeführt“ zu „OK“ wechselt. Bei „Fehlgeschlagen“ klicken Sie auf die Zeile und prüfen „Ergebnis“
2. Prüfen Sie unter [Systeminformationen] > [Crawling-Informationen] für jede Sitzung die „Indexgröße (Web/Datei)“ und ob die Zahl der indexierten Dokumente in etwa Ihren Erwartungen entspricht
3. Ist die Zahl zu niedrig, öffnen Sie [Systeminformationen] > [Fehler-URL]. Dort sind die URLs, die nicht abgerufen werden konnten, mit Fehlerart und Log verzeichnet

Häufige Ursachen sind:

- Der Freigabeordner hat 0 Dokumente, und unter Fehler-URL sind Pfade der Freigabe verzeichnet: Prüfen Sie den „Hostname“ der Datei-Authentifizierung und die Schreibweise des Pfads, die ausgewählte „Datei-Crawl-Konfiguration“ und das Passwort. Zeigt das Log Verbindungsfehler, prüfen Sie, ob der Container den Namen des Dateiservers auflösen und Port 445 erreichen kann
- Das Archiv hat 0 Dokumente, und Fehler-URL ist leer: Prüfen Sie, ob der Pfad nicht mit ``file:///`` geschrieben ist und ob „Eingeschlossene Pfade“ dieselbe Form wie der Pfad hat
- Beim Archiv treten Lesefehler auf: Prüfen Sie mit dem oben gezeigten Befehl ``exec -u fess``, ob der Container die Dateien lesen kann

Nach Label filtern
------------------

Suchen Sie unter ``http://localhost:8080/`` nach einem Wort, das wahrscheinlich an allen drei Orten vorkommt.
In den Ergebnissen erscheinen Seiten des Portals, Office-Dokumente aus dem Freigabeordner, PDFs aus dem Archiv usw. gemischt, nach Relevanz sortiert.

Auf der Suchseite von 15.9 (Theme ``bootstrap``) lässt sich an zwei Stellen nach Label filtern.

- Die Liste „Label“ neben den Suchergebnissen: Die in den Ergebnissen enthaltenen Labels werden mit ihrer Anzahl aufgeführt; ein Klick grenzt die Ergebnisse auf dieses Label ein
- Die Zahnrad-Schaltfläche rechts neben dem Suchfeld: Sie öffnet „Suchoptionen“; wählen Sie dort in der Liste „Etiketten“ einen oder mehrere Einträge aus und klicken Sie auf [Suche]. Bei Mehrfachauswahl werden Dokumente mit einem beliebigen der Labels berücksichtigt; ohne Auswahl wird alles durchsucht

Beim Filtern wird der URL ein Parameter wie ``fields.label=shared`` angehängt.
Erscheint „Label“ nicht neben den Suchergebnissen oder liefert das Filtern 0 Treffer, prüfen Sie, ob Sie vor dem Anlegen der Labels gecrawlt haben (das Ausführen von „Label Updater“ behebt das).
Erscheint die Liste „Etiketten“ nicht in „Suchoptionen“, prüfen Sie, ob die „Berechtigungen“ des Labels die Rolle der suchenden Person enthalten.

Links in Suchergebnissen und Pfadzuordnung
==========================================

Wenn Sie auf ein Suchergebnis aus dem Freigabeordner oder dem Archiv klicken, liest Fess die Datei und liefert sie an den Browser aus.
Dafür sorgt „Search File Proxy“ unter [Allgemein], das standardmäßig aktiviert ist.
So lassen sich die Dateien öffnen, obwohl der Browser URLs mit ``smb://`` oder ``file:`` nicht direkt öffnen kann.

Werden dieselben Dateien wie im Archiv auch auf einem internen Webserver veröffentlicht (hier ``https://archive.example.com/``) und sollen sie dort geöffnet werden, wandeln Sie die URLs mit einer Pfadzuordnung um.

Geben Sie unter [Crawler] > [Pfadzuordnung] > [Neu erstellen] die folgenden Felder ein und klicken Sie auf [Erstellen].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Wert
   * - Regulärer Ausdruck
     - ``^file:/data/archive/(.*)$``
   * - Ersetzung
     - ``https://archive.example.com/$1``
   * - Prozesstyp
     - Anzeige

Bei „Prozesstyp“ ist anfangs „Crawling“ ausgewählt; ändern Sie den Wert unbedingt auf „Anzeige“.

- Anzeige: Die URL im Index bleibt ``file:/data/archive/...``; nur das Ziel beim Klick auf einen Link in den Suchergebnissen ändert sich. Das wirkt sofort nach dem Anlegen, ein erneuter Crawl ist nicht nötig
- Crawling: Schreibt die im Index gespeicherte URL selbst um. Das wirkt erst nach einem erneuten Crawl, und auch „Eingeschlossene Pfade“ der Labels muss an die umgeschriebenen ``https://``-URLs angepasst werden

Suchen Sie nach dem Einrichten und klicken Sie auf ein Ergebnis aus dem Archiv, um zu prüfen, ob sich der Webserver ``https://archive.example.com/`` öffnet.

Weiterführende Artikel
======================

- Je nach Abteilung oder Position unterschiedliche Suchergebnisse anzeigen: :doc:`guide-05`
- Voraussetzungen der Dateiserver-Suche prüfen (unterstützte Formate, Übernahme von Zugriffsrechten): :doc:`file-server-search`
- Auch Dateien in Google Drive, SharePoint und Box durchsuchen: :doc:`guide-07`
- Anhand von Suchprotokollen die Suchqualität verbessern: :doc:`guide-08`
- Überwachung und Datensicherung für den Produktivbetrieb einrichten: :doc:`guide-10`

Referenzen
==========

- `Datei-Crawl (Dateiserver-Suche) <https://fess.codelibs.org/de/stable/admin/fileconfig-guide.html>`__
- `Dateiauthentifizierung <https://fess.codelibs.org/de/stable/admin/fileauth-guide.html>`__
- `Label <https://fess.codelibs.org/de/stable/admin/labeltype-guide.html>`__
- `Scheduler <https://fess.codelibs.org/de/stable/admin/scheduler-guide.html>`__
- `Allgemein <https://fess.codelibs.org/de/stable/admin/general-guide.html>`__
- `Pfad-Mapping <https://fess.codelibs.org/de/stable/admin/pathmap-guide.html>`__
- `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__
