=======================================
Fess mit Docker starten und durchsuchen
=======================================

Einführung
==========

Wer Fess in Betracht zieht, möchte zuerst wissen: „Welche Suchen sind möglich, wenn ich es selbst betreibe?“
In diesem Artikel starten wir Fess 15.9 mit Docker, crawlen etwa 20 Webseiten und probieren anschließend Schritt für Schritt die Suchsyntax aus.

Als Beispiel verwenden wir die deutschsprachige „Suchanleitung“ auf der offiziellen Fess-Website (eine Gruppe von Seiten, die die AND-Suche, die Wildcard-Suche usw. erklären).
Da sich das Ziel auf einen einzigen Ort beschränkt, ist das Crawling in wenigen Minuten erledigt, und Sie können den Inhalt der Suchergebnisse lesen und überprüfen.

Wenn Sie die Schritte dieses Artikels unverändert ausführen, können Sie anschließend Folgendes:

- Fess und OpenSearch mit Docker Compose starten, stoppen und wieder starten
- Die erste Anmeldung als Administrator und die dabei verlangte Passwortänderung erledigen
- Eine Web-Crawl-Konfiguration anlegen, das Crawling ausführen und seinen Abschluss prüfen
- AND-, OR-, Ausschluss-, Phrasen- und Feldsuche ausprobieren

Einstellungen für Produktionsumgebungen (Überwachung, Sicherung, SSO, Skalierung) werden nicht behandelt.
Wählen Sie unter „Weiterführende Artikel“ am Ende den Artikel, der zu Ihrem Ziel passt.

Die Umgebung in diesem Artikel
==============================

Mit den Compose-Dateien des Repositorys docker-fess werden die folgenden zwei Container gestartet.

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Dienst
     - Aufgabe
     - Speicherort der Daten
   * - ``fess01``
     - Fess selbst (Image ``ghcr.io/codelibs/fess:15.9.0``). Stellt auf Port 8080 die Suchseite und die Administrationsoberfläche bereit
     - Kein Volume (im Container)
   * - ``search01``
     - OpenSearch (Image ``ghcr.io/codelibs/fess-opensearch``). Port 9200 wird ebenfalls veröffentlicht
     - Volumes ``search01_data`` und ``search01_dictionary``

Index, Crawl-Konfigurationen, Benutzer, Jobprotokolle usw. werden alle in OpenSearch gespeichert und bleiben daher im Volume ``search01_data`` erhalten.
Einstellungen, die Sie in der Administrationsoberfläche unter [System] > [Allgemein] ändern, werden dagegen in ``system.properties`` im Container ``fess01`` gespeichert.
Dieser Unterschied wird später unter „Stoppen und Neustarten“ wichtig.

.. warning::

   In diesem Aufbau läuft OpenSearch mit deaktiviertem Sicherheits-Plugin und ist auf Port 9200 des Hosts erreichbar.
   Verwenden Sie ihn zum Ausprobieren auf Ihrem eigenen PC; wenn Sie ihn auf einem gemeinsam genutzten Server betreiben, lesen Sie zuerst :doc:`guide-10` und :doc:`guide-15`.

Voraussetzungen
===============

- Docker und Docker Compose (der Befehl ``docker compose``) sind verfügbar
- Docker stehen mindestens 4 GB Arbeitsspeicher zur Verfügung (allein der Heap von OpenSearch belegt 1 GB)
- Eine Internetverbindung besteht (für das Herunterladen der Images und das Crawling)

Unter Linux oder WSL2 erhöhen Sie ``vm.max_map_count``, das OpenSearch zum Starten benötigt.

::

    $ sudo sysctl -w vm.max_map_count=262144

Dieser Wert wird beim Neustart des Betriebssystems zurückgesetzt.
Wenn Sie die Umgebung weiter nutzen, tragen Sie ihn auch in ``/etc/sysctl.conf`` ein.

::

    $ echo 'vm.max_map_count=262144' | sudo tee -a /etc/sysctl.conf

Fess starten
============

Die Compose-Dateien für 15.9.0 herunterladen
--------------------------------------------

Die Compose-Dateien im Standard-Branch von docker-fess werden mit jeder neuen Version aktualisiert.
Um die Version auf 15.9.0 festzulegen, laden Sie die Dateien des Tags ``v15.9.0`` herunter.

::

    $ mkdir fess-docker
    $ cd fess-docker
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

``compose.yaml`` definiert nur ``fess01``; ``search01``, von dem ``fess01`` abhängt, befindet sich in ``compose-opensearch3.yaml``.
Deshalb geben Sie bei allen folgenden ``docker compose``-Befehlen jedes Mal beide Dateien mit ``-f`` an.
Wenn Sie nur eine der beiden angeben, funktionieren weder Starten noch Stoppen korrekt.

Starten und warten, bis Fess bereit ist
---------------------------------------

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Beim ersten Mal dauert es einige Minuten, weil die Images heruntergeladen werden.
Den Status prüfen Sie mit dem folgenden Befehl.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml ps

``fess01`` startet, sobald ``search01`` healthy ist.
Wenn der STATUS von ``fess01`` ``(healthy)`` lautet, ist Fess bereit.
Die Integritätsprüfung von ``fess01`` ruft ``/api/v2/health`` auf; die ersten 120 Sekunden nach dem Start gelten als Karenzzeit.

Wenn der Container lange nicht healthy wird, sehen Sie sich die Logs an.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

Wenn Port 8080 von einer anderen Anwendung belegt ist, ändern Sie ``ports`` in ``compose.yaml`` beispielsweise auf ``"9080:8080"``.
Zu anderen Startproblemen siehe `Fehlerbehebung bei der Installation <https://fess.codelibs.org/de/stable/install/troubleshooting.html>`__.

Wenn Sie ``http://localhost:8080/`` im Browser öffnen, erscheint die Suchseite von Fess.
Da noch nichts gecrawlt wurde, liefert eine Suche zu diesem Zeitpunkt keine Ergebnisse.

Bei der Administrationsoberfläche anmelden
==========================================

Öffnen Sie ``http://localhost:8080/admin/`` und melden Sie sich mit dem Benutzernamen ``admin`` und dem Passwort ``admin`` an.

Das Anfangspasswort ``admin`` darf nicht weiterverwendet werden; nach der Anmeldung gelangen Sie daher zu einer Seite mit der Meldung „Sie müssen Ihr Passwort aktualisieren“.

1. Geben Sie in „Neues Passwort“ und „Neues Passwort bestätigen“ dasselbe Passwort ein (mindestens 8 Zeichen)
2. Klicken Sie auf [Aktualisieren]

Nach der Aktualisierung öffnet sich das Dashboard der Administrationsoberfläche.
Ab jetzt melden Sie sich mit dem neuen Passwort an.
Dieses Passwort wird in OpenSearch gespeichert und bleibt daher auch erhalten, wenn Sie die Container neu erstellen (wenn Sie auch die Volumes löschen, gilt wieder ``admin``).

Eine Crawl-Konfiguration anlegen
================================

Das Ziel festlegen
------------------

Diesmal crawlen wir die deutschsprachige „Suchanleitung“ auf der offiziellen Fess-Website.
Sie umfasst etwa 20 Seiten unterhalb von ``https://fess.codelibs.org/de/stable/user/``; ``stable`` verweist auf die Dokumentation der aktuellen stabilen Version (15.9).

Eine Web-Crawl-Konfiguration registrieren
-----------------------------------------

1. Öffnen Sie im linken Menü der Administrationsoberfläche [Crawler] > [Web]
2. Klicken Sie auf [Neu erstellen]
3. Geben Sie die folgenden Felder ein. Alle anderen Felder bleiben auf ihren Standardwerten

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Feld
        - Wert
      * - Name
        - ``Fess Suchanleitung``
      * - URLs
        - ``https://fess.codelibs.org/de/stable/user/index.html``
      * - Eingeschlossene URLs
        - ``https://fess.codelibs.org/de/stable/user/.*``
      * - Maximale Zugriffsanzahl
        - ``50``

4. Klicken Sie auf [Erstellen]

Die Felder bedeuten Folgendes.

- „Name“ ist ein Pflichtfeld. Solange es leer ist, kann die Konfiguration nicht erstellt werden
- „URLs“ ist der Startpunkt des Crawlings
- „Eingeschlossene URLs“ ist ein regulärer Ausdruck; Links zu URLs, die nicht darauf passen, werden nicht verfolgt. Bleibt das Feld leer, folgt der Crawler den Links in den Seiten auch zu anderen Versionen, anderen Sprachen und sogar zu externen Websites
- „Maximale Zugriffsanzahl“ ist eine Obergrenze für den Fall, dass der reguläre Ausdruck fehlerhaft ist

Von den Feldern mit Standardwerten steht „Anzahl der Threads“ auf ``1`` und „Intervall“ auf ``10000`` Millisekunden.
Da der Crawler pro Seite 10 Sekunden wartet, bleibt die Last für die Zielwebsite gering.
In „Berechtigungen“ ist ``{role}guest`` eingetragen, sodass auch nicht angemeldete Benutzer die Suchergebnisse sehen können.
Wie Sie Ergebnisse je nach Abteilung unterschiedlich anzeigen, behandelt :doc:`guide-05`.

.. note::

   Wenn Sie URLs mit Versionsnummer wie ``/de/15.9/`` als Ziel angeben, wird keine einzige Seite registriert.
   Diese Seiten enthalten ein ``<link rel="canonical">``, das auf ``/de/stable/`` verweist.
   Der Crawler von Fess registriert eine solche Seite nicht, sondern folgt stattdessen der kanonischen URL.
   Diese URL liegt außerhalb des regulären Ausdrucks in „Eingeschlossene URLs“, daher wird nichts registriert.
   Prüfen Sie auch beim Crawlen Ihrer eigenen Unternehmenswebsite, ob die kanonischen URLs vom regulären Ausdruck erfasst werden.

.. tip::

   Auch unter [System] > [Assistent] können Sie eine Crawl-Konfiguration anlegen, indem Sie nur „Name“, „Crawl-Pfad“, „Maximale Zugriffsanzahl“ und „Tiefe“ eingeben, und direkt zu [Crawling starten] weitergehen.
   In einer mit dem Assistenten erstellten Konfiguration ist „Eingeschlossene URLs“ jedoch nicht gesetzt, sodass Sie den Bereich der verfolgten Links nicht eingrenzen können.
   Wenn Sie das Ziel wie hier eingrenzen möchten, legen Sie die Konfiguration wie oben beschrieben unter [Crawler] > [Web] an.

Das Crawling ausführen und den Abschluss prüfen
===============================================

Das Crawling starten
--------------------

Das Speichern der Konfiguration allein startet das Crawling nicht.

1. Öffnen Sie [System] > [Scheduler]
2. Klicken Sie in der Liste auf „Default Crawler“
3. Klicken Sie auf [Jetzt starten]

„Default Crawler“ ist der Job, der alle aktivierten Crawl-Konfigurationen für Web, Dateisystem und Datenspeicher gemeinsam ausführt.
Für diesen Job ist standardmäßig der Cron-Ausdruck ``0 0 * * *`` eingestellt, sodass er auch automatisch einmal täglich läuft.
Wenn Sie die Container laufen lassen, wird an den folgenden Tagen mit denselben Konfigurationen erneut gecrawlt.

Mit dieser Konfiguration werden etwa 20 Seiten im Abstand von 10 Sekunden abgerufen; rechnen Sie also mit einigen Minuten.

Den Abschluss prüfen
--------------------

Prüfen Sie in der folgenden Reihenfolge.

1. Öffnen Sie [Systeminformationen] > [Jobprotokoll]. Wenn der „Status“ in der Zeile „Default Crawler“ von „Wird ausgeführt“ auf „OK“ wechselt, ist der Job beendet. Bei „Fehlgeschlagen“ klicken Sie auf die Zeile, öffnen die Details und prüfen das „Ergebnis“
2. Öffnen Sie [Systeminformationen] > [Crawling-Informationen] und klicken Sie auf die oberste (neueste) Sitzung der Liste. „Indexgröße (Web/Datei)“ ist die Anzahl der Dokumente, die bei diesem Crawling registriert wurden. Diesmal sind es etwa 20
3. Wenn die Anzahl geringer als erwartet ist, öffnen Sie [Systeminformationen] > [Fehler-URL]. Dort sind URLs, die etwa wegen Verbindungsfehlern nicht abgerufen werden konnten, zusammen mit dem Grund aufgezeichnet

Auch wenn der Job „OK“ zeigt, kann die Anzahl registrierter Dokumente 0 sein.
URLs, die nicht auf den regulären Ausdruck in „Eingeschlossene URLs“ passen, gelten nicht als Fehler, sondern als außerhalb des Ziels, und werden daher auch nicht unter „Fehler-URL“ aufgezeichnet.
Wenn die Anzahl 0 und „Fehler-URL“ ebenfalls leer ist, überprüfen Sie die Schreibweise von URL und regulärem Ausdruck (``https`` oder ``http``, ob das abschließende ``.*`` vorhanden ist usw.).

Suchen ausprobieren
===================

Öffnen Sie ``http://localhost:8080/`` und suchen Sie.
Die Suchseite verwendet ``bootstrap``, das mit Fess mitgelieferte Theme.

Geben Sie zunächst ``Wildcard`` ein und suchen Sie.
In den Ergebnissen erscheinen Seiten wie „Wildcard-Suche“ und „Sonderzeichen“.
Wenn Sie auf den Titel eines Ergebnisses klicken, öffnet sich die Originalseite (fess.codelibs.org).

Geben Sie anschließend nacheinander die folgenden Suchbegriffe ein.
Die Ergebnisse aller Begriffe können Sie anhand der gerade gecrawlten Seiten überprüfen.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Einzugebende Suchbegriffe
     - Bedeutung
   * - ``Feld URL``
     - Durch Leerzeichen getrennte Begriffe ergeben eine AND-Suche; es erscheinen nur Seiten, die beide enthalten
   * - ``Wildcard OR unscharfe``
     - Es erscheinen Seiten, die einen der beiden Begriffe enthalten. ``OR`` muss in Großbuchstaben geschrieben werden, mit einem Leerzeichen davor und danach
   * - ``Suche -Label``
     - Entfernt Seiten, die „Label“ enthalten, aus den Ergebnissen. Setzen Sie ``-`` unmittelbar vor den auszuschließenden Begriff
   * - ``"Erweiterte Suche"``
     - Sucht Seiten, die den in Anführungszeichen gesetzten Ausdruck genau in dieser Reihenfolge enthalten (Phrasensuche)
   * - ``title:Sortierte``
     - Sucht nur Seiten, deren Titel „Sortierte“ enthält (Feldsuche)

Wenn Sie ``or`` oder ``and`` kleinschreiben, wirken sie nicht als Operatoren, sondern werden als gewöhnliche Suchbegriffe behandelt.

Die hier verwendete Syntax sowie die übrige Syntax wie Wildcard-Suche, unscharfe Suche und Bereichssuche wird in der gerade gecrawlten `Suchanleitung <https://fess.codelibs.org/de/stable/user/index.html>`__ erklärt.
Sie können auch eine Syntax, die Sie interessiert, in Ihrem eigenen Fess suchen und die gefundene Seite öffnen und lesen.

Stoppen und Neustarten
======================

Was erhalten bleibt, hängt davon ab, wie Sie stoppen.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Vorgang
     - Was erhalten bleibt
     - Was verloren geht
   * - ``stop`` → ``start``
     - Alles
     - Nichts
   * - ``down`` → ``up -d``
     - Alles, was in OpenSearch gespeichert ist (Index, Crawl-Konfigurationen, Benutzer und Passwörter, Jobprotokolle usw.)
     - Alles, was im Container ``fess01`` gespeichert ist (unter [System] > [Allgemein] geänderte Einstellungen usw.)
   * - ``down -v``
     - Nichts
     - Alles (auch das Administratorpasswort wird wieder zu ``admin``)

Für das alltägliche Stoppen verwenden Sie ``stop``, zum Neustarten ``start``.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

``down`` entfernt die Container.
Die Daten von OpenSearch bleiben in den Volumes erhalten, aber die Einstellungen unter [Allgemein] stehen in ``system.properties`` im Container ``fess01`` und verschwinden daher zusammen mit dem Container.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Wenn Sie den Test beenden und alles einschließlich der Daten aufräumen möchten, fügen Sie ``-v`` hinzu.
Dabei werden auch die Volumes gelöscht; dies lässt sich nicht rückgängig machen.

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down -v

Einige der unter [Allgemein] geänderten Einstellungen bleiben auch nach dem Neuerstellen der Container erhalten, wenn Sie sie in ``FESS_JAVA_OPTS`` in ``compose.yaml`` angeben (manche Einstellungen, etwa die SSO-Verbindungseinstellungen, lassen sich auf diese Weise nicht angeben).
Das Vorgehen beschreibt `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__.

Weiterführende Artikel
======================

Fahren Sie je nach Ziel mit dem passenden Artikel fort.

- Sie möchten den Aufbau von Fess und die Lesereihenfolge der Artikel kennenlernen: :doc:`guide-01`
- Sie möchten ein Suchfeld in eine bestehende interne Website oder ein Portal einbauen: :doc:`guide-03`
- Sie möchten interne Websites und Dateiserver gemeinsam durchsuchen: :doc:`guide-04`
- Sie möchten die sichtbaren Suchergebnisse je nach Abteilung oder Position ändern: :doc:`guide-05`
- Sie möchten auch Daten aus Slack, Confluence, Datenbanken usw. durchsuchen: zuerst :doc:`datastore-basics`, danach :doc:`guide-06`, :doc:`guide-07` und :doc:`guide-12`
- Sie möchten generative KI anhand interner Dokumente antworten lassen: :doc:`guide-19`
- Sie möchten Dokumente mit ähnlicher Bedeutung finden, auch wenn die Schlüsselwörter nicht übereinstimmen: :doc:`guide-18`
- Sie möchten Überwachung und Sicherung für den Produktivbetrieb einrichten: :doc:`guide-10`
- Sie möchten SSO und Zugriffsschutz konfigurieren: :doc:`guide-15`
- Sie möchten mit wachsender Zahl von Dokumenten und Benutzern skalieren: :doc:`guide-14`

Referenzen
==========

- `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__
- `docker-fess (GitHub) <https://github.com/codelibs/docker-fess>`__
- `Web-Crawl-Konfiguration <https://fess.codelibs.org/de/stable/admin/webconfig-guide.html>`__
- `Jobprotokoll <https://fess.codelibs.org/de/stable/admin/joblog-guide.html>`__
- `Suchanleitung <https://fess.codelibs.org/de/stable/user/index.html>`__
