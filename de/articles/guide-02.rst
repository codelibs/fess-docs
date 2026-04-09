============================================================
Teil 2: Das Sucherlebnis in 5 Minuten -- Erster Kontakt mit Fess per Docker Compose
============================================================

Einleitung
==========

Im vorherigen Teil haben wir die Notwendigkeit einer Suchinfrastruktur im Unternehmen und einen Überblick über Fess vorgestellt.
In diesem Artikel zeigen wir den kürzesten Weg, um Fess tatsächlich zu starten und eine Suche durchzuführen.

Das Ziel ist es, schnell zu verstehen, welches Sucherlebnis Fess bietet.
Mit Docker Compose starten Sie in wenigen Befehlszeilen eine Fess-Umgebung, crawlen eine Webseite und erleben die Suche in Aktion.

Zielgruppe
==========

- Personen, die Fess zum ersten Mal ausprobieren möchten
- Personen, die schnell einen PoC (Proof of Concept) zur Evaluierung durchführen möchten
- Personen, die grundlegende Docker-Kenntnisse besitzen

Voraussetzungen
================

- Eine Umgebung, in der Docker und Docker Compose verfügbar sind
- Mindestens 4 GB Arbeitsspeicher (empfohlen: 8 GB oder mehr)
- Internetverbindung

Vorbereitung (Linux / WSL2)
-------------------------------

OpenSearch, das von Fess verwendet wird, benötigt beim Start zahlreiche Memory-Map-Bereiche.
Unter Linux und WSL2 erhöhen Sie ``vm.max_map_count`` mit folgendem Befehl:

::

    $ sudo sysctl -w vm.max_map_count=262144

Diese Einstellung wird nach einem Neustart des Betriebssystems zurückgesetzt. Um sie dauerhaft zu machen, fügen Sie sie in ``/etc/sysctl.conf`` ein:

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

.. note::

   Wenn Sie Docker Desktop unter macOS verwenden, ist diese Einstellung nicht erforderlich.

Fess starten
=============

Docker Compose-Datei herunterladen
-----------------------------------

Die Docker Compose-Datei für Fess ist im GitHub-Repository öffentlich verfügbar.
Laden Sie sie mit den folgenden Befehlen herunter:

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess/compose

Im compose-Verzeichnis befinden sich mehrere Konfigurationsdateien.
Beginnen wir zunächst mit einer einfachen Konfiguration.

Start
-----

Starten Sie Fess und OpenSearch mit folgendem Befehl:

::

    $ docker compose up -d

Beim ersten Start werden die Docker-Images heruntergeladen, was einige Minuten dauern kann.
Den Startstatus können Sie mit folgendem Befehl überprüfen:

::

    $ docker compose ps

Sobald alle Container den Status „running" anzeigen, ist der Start abgeschlossen.

Zugriff auf die Suchoberfläche
-------------------------------

Öffnen Sie ``http://localhost:8080/`` in Ihrem Browser.
Wenn die Fess-Startseite angezeigt wird, ist der Dienst korrekt gestartet.

Zu diesem Zeitpunkt ist der Index noch leer, sodass eine Suche keine Ergebnisse liefert.
Im nächsten Schritt registrieren wir Crawl-Ziele und machen Inhalte durchsuchbar.

Administrationsoberfläche überprüfen
=====================================

Anmeldung an der Administrationsoberfläche
-------------------------------------------

Öffnen Sie ``http://localhost:8080/admin/`` und melden Sie sich an der Administrationsoberfläche an.
Die Standard-Anmeldedaten lauten:

- Benutzername: ``admin``
- Passwort: ``admin``

Das Dashboard der Administrationsoberfläche bietet eine Übersicht über den Systemstatus.

Aufbau der Administrationsoberfläche
-------------------------------------

Im linken Menü der Administrationsoberfläche sind die wichtigsten Verwaltungsfunktionen von Fess aufgelistet.
Verschaffen Sie sich hier zunächst einen Überblick.

**Crawler**

In diesem Bereich werden die Crawl-Ziele registriert. Sie können Crawl-Einstellungen für Web, Dateisystem und Datenspeicher verwalten.

**System**

Hier befinden sich systemweite Verwaltungsfunktionen wie Scheduler, Design und Wörterbücher. In den Wörterbüchern verwalten Sie Einstellungen zur Suchqualität, wie Synonyme und Stoppwörter.

**Systeminformationen**

Dieser Bereich bietet Zugang zu Such-Logs, Job-Logs, Crawl-Informationen, Backups und weiteren Wartungsfunktionen.

Eine Webseite crawlen
======================

Crawl-Ziel registrieren
-------------------------

Crawlen wir nun tatsächlich eine Webseite, um sie durchsuchbar zu machen.
Wir verwenden hier die offizielle Fess-Website als Ziel.

1. Wählen Sie im linken Menü der Administrationsoberfläche [Crawler] > [Web]
2. Klicken Sie auf [Neu erstellen]
3. Geben Sie folgende Informationen ein:

   - URL: ``https://fess.codelibs.org/ja/``
   - Zu crawlende URL: ``https://fess.codelibs.org/ja/.*``
   - Maximale Zugriffszahl: ``50``
   - Thread-Anzahl: ``2``
   - Intervall: ``10000``

4. Klicken Sie auf [Erstellen], um zu speichern

Damit ist die Einstellung abgeschlossen, die offizielle Fess-Website (japanische Seiten) mit maximal 50 Seiten und einem Intervall von 10 Sekunden zu crawlen.

Crawl-Vorgang starten
-----------------------

Das Speichern der Einstellungen allein startet den Crawl-Vorgang noch nicht.
Um den Crawl zu starten, führen Sie den Job über den Scheduler aus.

1. Wählen Sie [System] > [Scheduler]
2. Wählen Sie „Default Crawler"
3. Klicken Sie auf [Jetzt starten]

Der Crawl-Vorgang wird gestartet.
Den Fortschritt können Sie unter [Systeminformationen] > [Crawl-Informationen] verfolgen.
Bei etwa 50 Seiten ist der Crawl-Vorgang in wenigen Minuten abgeschlossen.

Die Suche erleben
==================

Suche durchführen
------------------

Kehren Sie nach Abschluss des Crawl-Vorgangs zur Suchoberfläche unter ``http://localhost:8080/`` zurück und probieren Sie die Suche aus.

Geben Sie zum Beispiel „インストール" ein und suchen Sie danach. Es werden Seiten der Fess-Website zum Thema Installation als Suchergebnisse angezeigt.

Elemente der Suchergebnisseite
-------------------------------

Die Suchergebnisseite enthält folgende Elemente:

**Suchergebnisliste**

Jedes Ergebnis zeigt Titel, URL und einen Textausschnitt (Snippet) an.
Übereinstimmungen mit dem Suchbegriff werden hervorgehoben dargestellt.

**Trefferanzahl und Antwortzeit**

Oberhalb der Suchergebnisse werden die Anzahl der Treffer und die benötigte Suchzeit angezeigt.

**Seitennavigation (Paginierung)**

Wenn die Ergebnisse mehrere Seiten umfassen, wird eine Seitennavigation angezeigt.

Weitere nützliche Suchfunktionen
---------------------------------

Fess bietet neben der einfachen Stichwortsuche weitere vielfältige Suchfunktionen.

**AND/OR-Suche**

Mehrere Stichwörter, die durch Leerzeichen getrennt werden, ergeben eine AND-Suche.
Mit ``OR`` können Sie eine OR-Suche durchführen.

::

    インストール Docker       # AND-Suche (enthält beide Begriffe)
    インストール OR Docker    # OR-Suche (enthält einen der Begriffe)

**Phrasensuche**

Setzen Sie den Suchbegriff in doppelte Anführungszeichen, um nach Dokumenten zu suchen, die die Wörter in genau dieser Reihenfolge enthalten.

::

    "全文検索サーバー"

**Ausschlusssuche**

Um Ergebnisse auszuschließen, die ein bestimmtes Stichwort enthalten, verwenden Sie ein Minuszeichen.

::

    インストール -Windows    # Ergebnisse ohne „Windows"

Umgebung stoppen und neu starten
=================================

Stoppen
--------

Wenn Sie die Sucherfahrung abgeschlossen haben, stoppen Sie die Umgebung mit folgendem Befehl:

::

    $ docker compose down

Die Daten (Index) bleiben erhalten, sodass Sie nach einem Neustart im gleichen Zustand weiterarbeiten können.

Vollständige Bereinigung einschließlich der Daten
--------------------------------------------------

Um auch die Volumes zu löschen, führen Sie folgenden Befehl aus:

::

    $ docker compose down -v

In diesem Fall wird auch der durch das Crawling erstellte Index gelöscht.

Erkenntnisse aus dem Sucherlebnis
==================================

Durch diese Übung konnten Sie die grundlegende Funktionsweise von Fess kennenlernen.
Wenn Sie an den praktischen Einsatz im Unternehmen denken, ergeben sich möglicherweise einige Fragen:

- „Können auch interne Dateiserver durchsucht werden?" → wird in **Teil 4** behandelt
- „Kann ein Suchfeld in eine bestehende interne Website eingebettet werden?" → wird in **Teil 3** behandelt
- „Können Informationen je nach Abteilung eingeschränkt werden?" → wird in **Teil 5** behandelt
- „Kann auch in Slack oder Confluence gesucht werden?" → wird in **Teil 6** behandelt
- „Kann eine KI Fragen beantworten?" → wird in **Teil 19** behandelt

Fess kann all diese Szenarien abdecken.
Im Verlauf dieser Serie stellen wir Ihnen schrittweise die Umsetzungsmöglichkeiten vor.

Zusammenfassung
================

In diesem Artikel haben wir Fess mit Docker Compose gestartet und den gesamten Ablauf vom Crawling einer Webseite bis zur Suche erlebt.

- Fess + OpenSearch mit einem einzigen Befehl über Docker Compose starten
- Crawl-Ziele in der Administrationsoberfläche registrieren und über den Scheduler ausführen
- Stichwortsuche, AND/OR-Suche und Phrasensuche auf der Suchoberfläche erleben
- Einfaches Stoppen und Neustarten der Umgebung

Im nächsten Teil zeigen wir, wie Sie die Suchfunktion von Fess in bestehende Webseiten oder Portale einbetten können.

Referenzen
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__

- `Fess インストールガイド <https://fess.codelibs.org/ja/15.5/install/index.html>`__
