======================================
Grundlagen des Datenspeicher-Crawlings
======================================

Einleitung
==========

Die Inhalte von Google Drive, Slack oder einer Datenbank lassen sich weder per Web-Crawling noch per Datei-Crawling durchsuchbar machen.
Auch eine CSV-Datei wird beim Datei-Crawling zu einem einzigen Dokument, sodass sich die einzelnen Zeilen nicht durchsuchen lassen.
Fess behandelt solche Quellen als „Datenspeicher“ und importiert sie über Plugins (Datenspeicher-Konnektoren) Datensatz für Datensatz.

Der Einstellungsbildschirm für Datenspeicher hat andere Felder als die Einstellungsbildschirme für Web und Dateisystem.
Welche Werte zur URL, zum Titel usw. werden, müssen Sie selbst angeben, und mit den Standardwerten werden die Dokumente so registriert, dass sie ohne Anmeldung durchsucht werden können.
Selbst wenn die Verarbeitung fehlschlägt, kann der Job als „OK“ angezeigt werden.

Dieser Artikel erklärt anhand von Fess 15.9 die Mechanismen, die allen Konnektoren gemeinsam sind.
An einem kleinen Beispiel mit einer CSV-Datei gehen wir den gesamten Ablauf durch: Installation des Plugins, Konfiguration, Ausführung und Prüfung der Ergebnisse.
Authentifizierung und Parameter der einzelnen Konnektoren finden Sie in den Artikeln und Referenzen, die am Ende aufgeführt sind.

Unterschiede zum Web- und Datei-Crawling
========================================

Beim Web- und Datei-Crawling folgt Fess Links und Ordnern und extrahiert Titel und Text automatisch aus den abgerufenen Dokumenten.
Beim Datenspeicher-Crawling liest ein Konnektor Datensätze aus einer API oder einer Datei.
Welcher Wert eines Datensatzes in welches Feld des Index kommt, legen Sie im „Skript“ der Konfiguration fest.

Fess selbst enthält keine Datenspeicher-Handler.
Die Auswahlliste „Handler-Name“ unter [Crawler] > [Datenspeicher] zeigt nur die Handler an, die von installierten ``fess-ds-*``-Plugins bereitgestellt werden.

Darüber hinaus unterscheiden sich Datenspeicher-Konfigurationen in folgenden Punkten (Erläuterung in späteren Abschnitten):

- Der Einstellungsbildschirm hat kein Feld „Label“
- Die Regeln unter [Crawler] > [Dokument-Boost] werden nicht angewendet

Das Plugin installieren
=======================

Als Beispiel verwenden wir hier den CSV-Konnektor ``fess-ds-csv``.
Die Plugin-Version muss zur Minor-Version des verwendeten Fess passen (für Fess 15.9 also 15.9.x).

Um es über die Administrationsoberfläche zu installieren, klicken Sie unter [System] > [Plugin] auf [Installieren].
Wählen Sie auf der Registerkarte [Remote] in der Auswahlliste ``fess-ds-csv`` aus und klicken Sie auf [Installieren].
Um eine vorhandene jar-Datei zu verwenden, nutzen Sie die Registerkarte [Lokal].

In Umgebungen, die aus dem ZIP-Paket oder per RPM / DEB installiert wurden, können Sie das Plugin auch über die Kommandozeile installieren.

.. code-block:: bash

    bin/fess-setup install plugin fess-ds-csv:15.9.0

Bei Docker fügen Sie ``FESS_PLUGINS`` zu ``environment`` von ``fess01`` in ``compose.yaml`` hinzu, damit das Plugin beim Start installiert wird.
Mehrere Plugins werden durch Leerzeichen getrennt aufgeführt (nicht durch Kommas).

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-csv:15.9.0"

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Bei Docker wird ein über die Administrationsoberfläche installiertes Plugin im Container abgelegt und verschwindet daher, wenn der Container neu erstellt wird.
Bei Docker ist ``FESS_PLUGINS`` daher der zuverlässigere Weg.
Wenn Sie eine Umgebungsvariable ändern und ``up -d`` ausführen, wird der Container neu erstellt.
Welche Einstellungen dabei verloren gehen, lesen Sie in :doc:`guide-02`.

Wenn Sie das Plugin über die Administrationsoberfläche oder mit ``fess-setup`` installiert haben, starten Sie Fess neu (``FESS_PLUGINS`` installiert die Plugins vor dem Start von Fess, daher ist dort kein Neustart nötig).
Erscheint nach dem Neustart unter [Crawler] > [Datenspeicher] > [Neu erstellen] im Feld „Handler-Name“ der Eintrag ``CsvDataStore``, ist das Plugin installiert.

Die drei zentralen Felder des Einstellungsbildschirms
=====================================================

Im Mittelpunkt einer Datenspeicher-Konfiguration stehen drei Felder: „Handler-Name“, „Parameter“ und „Skript“.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Feld
     - Inhalt
   * - Handler-Name
     - Der zu verwendende Konnektor. Beispiele: ``CsvDataStore``, ``SlackDataStore``
   * - Parameter
     - Anweisungen an den Konnektor. Ein ``Schlüssel=Wert`` pro Zeile (zu lesende Dateien, Verbindungsziel, Zugangsdaten usw.)
   * - Skript
     - Die Zuordnung zu Feldern des Index. Ein ``Feldname=Ausdruck`` pro Zeile

``script_type`` in den Parametern
---------------------------------

Auf dem Bildschirm zum Neuerstellen enthält das Feld „Parameter“ bereits ``script_type=javascript``.
Damit wird festgelegt, dass die Ausdrücke im Feld „Skript“ als JavaScript ausgewertet werden.
Lassen Sie diese Zeile stehen und ergänzen Sie die Konnektor-Parameter darunter.

Wenn Sie die Zeile ``script_type`` löschen, wird das Skript als Groovy ausgewertet (der Standardwert, damit vor 15.9 erstellte Konfigurationen weiter funktionieren).
Für die Auswertung mit Groovy ist das Plugin ``fess-script-groovy`` erforderlich.
Es ist im Standard-Docker-Image enthalten, im slim-Image jedoch nicht.
In einer Umgebung ohne das Plugin schlägt die Auswertung von Zeilen mit Ausdrücken mit dem Fehler ``groovy is not found`` fehl, und der Datensatz wird nicht registriert (eine Zeile, deren rechte Seite nur aus einem Elementnamen besteht, etwa ``title=subject``, verwendet den Wert direkt, ohne eine Skript-Engine zu durchlaufen).
Umgekehrt funktioniert die Konfiguration mit dem Standard-Docker-Image auch nach dem Löschen der Zeile weiter, weil sie mit Groovy ausgewertet wird – das macht das Problem schwer erkennbar.
Wenn Sie ein Beispiel aus der Referenz eines Konnektors in das Feld „Parameter“ einfügen, achten Sie darauf, die Zeile ``script_type=javascript`` nicht zu löschen.

Das Skript schreiben
--------------------

Jede Zeile im Feld „Skript“ hat links den Namen eines Indexfelds und rechts einen JavaScript-Ausdruck.
Zeichenketten werden in doppelte Anführungszeichen gesetzt.
Setzen Sie kein Semikolon an das Zeilenende.
Mit einem Semikolon wird der Wert des Ausdrucks ``null``, und das Feld wird nicht gesetzt.
Es erscheinen weder Fehler noch Logeinträge; Sie bemerken es nur daran, dass das Feld leer ist (Details im „JavaScript-Skripting-Leitfaden“ in den Referenzen am Ende).

Welche Elementnamen auf der rechten Seite verwendet werden können, hängt vom Konnektor ab.

- Die Konnektoren für CSV, JSON und Datenbanken verweisen direkt auf Spalten- bzw. Feldnamen (bei CSV auch über ``cell1``, ``cell2`` …)
- Viele Cloud-Konnektoren übergeben das abgerufene Objekt mit einem Präfix. Zum Beispiel verwenden Box, Google Drive und OneDrive ``file.*``, Slack ``message.*``, Jira ``issue.*`` und Salesforce ``object.*``

Die verfügbaren Elementnamen finden Sie in der Beschreibung des Skripts in der Referenz des jeweiligen Konnektors (``https://fess.codelibs.org/de/stable/config/datastore/ds-<Name>.html``).
Verweisen Sie auf einen nicht definierten Namen, schreiben also etwa ``url`` statt ``file.url``, schlägt die Auswertung des Ausdrucks fehl, und der Datensatz wird nicht registriert.

Beispiel: Eine CSV-Datei durchsuchbar machen
============================================

In diesem Beispiel wird eine interne FAQ als CSV-Datei gepflegt und durchsuchbar gemacht.
Speichern Sie den folgenden Inhalt in UTF-8 als ``faq.csv``.

.. code-block:: text

    faq_id,question,answer
    1,Bis wann muss ich Spesen abrechnen,Reichen Sie Ihre Spesen bis zum Monatsende ein.
    2,Wie verbinde ich mich von außerhalb mit internen Systemen,Stellen Sie die Verbindung über VPN her.
    3,Was tun bei Verlust des Hausausweises,Wenden Sie sich an die Verwaltung und beantragen Sie einen neuen Ausweis.

Eine mit Excel gespeicherte CSV-Datei ist oft nicht in UTF-8, sondern in einer älteren Windows-Codierung gespeichert, etwa windows-1252 bei deutschsprachigem Excel oder MS932 bei japanischem Excel.
Geben Sie in diesem Fall die Codierung in den unten gezeigten Parametern an, z. B. ``file_encoding=windows-1252`` oder ``file_encoding=MS932``.
Legen Sie die Datei unter einem Pfad ab, den der Fess-Crawler lesen kann.
Der Crawler läuft auf demselben Server wie Fess; in einer ZIP- oder RPM-/DEB-Umgebung legen Sie die Datei daher in ein Verzeichnis, das der Benutzer lesen kann, unter dem Fess läuft.
Wenn Sie es mit Docker nur ausprobieren möchten, ist das Kopieren in den Container am einfachsten (die Datei verschwindet, wenn der Container neu erstellt wird).

.. code-block:: bash

    docker cp faq.csv fess01:/tmp/faq.csv

Klicken Sie unter [Crawler] > [Datenspeicher] auf [Neu erstellen] und geben Sie Folgendes ein.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Feld
     - Wert
   * - Name
     - Interne FAQ
   * - Handler-Name
     - ``CsvDataStore``
   * - Parameter
     - Siehe unten
   * - Skript
     - Siehe unten
   * - Berechtigungen
     - ``{role}guest`` unverändert lassen (die FAQ darf ohne Anmeldung durchsucht werden)

Parameter:

.. code-block:: properties

    script_type=javascript
    files=/tmp/faq.csv
    file_encoding=UTF-8
    has_header_line=true

Skript:

.. code-block:: javascript

    url="https://intranet.example.com/faq/" + faq_id
    title=question
    content=question + " " + answer
    digest=answer
    label="faq"

Mit ``has_header_line=true`` können die Spaltennamen der ersten Zeile (``faq_id``, ``question``, ``answer``) im Skript verwendet werden.
Geben Sie für ``url`` die URL einer Seite an, die den Datensatz anzeigen kann; sie wird geöffnet, wenn auf den Link im Suchergebnis geklickt wird.
Die URL in diesem Beispiel ist fiktiv.
Ersetzen Sie sie durch die URL Ihrer tatsächlichen FAQ-Seite.

Nachdem Sie mit [Erstellen] gespeichert haben, erstellen und starten Sie einen Job wie im Abschnitt „Zeitplanung“ beschrieben und prüfen das Ergebnis wie im Abschnitt „Ergebnisse prüfen“ beschrieben.
Wenn alles funktioniert, finden Sie den zweiten FAQ-Eintrag, wenn Sie im abgemeldeten Zustand (oder in einem privaten Browserfenster) auf der Suchseite nach „VPN“ suchen.
Dokumente mit ``{role}guest`` werden nicht angemeldeten Benutzern sowie Benutzern mit der Rolle ``guest`` angezeigt (einschließlich des Anfangsbenutzers ``admin``). Sind Sie als ein anderer Benutzer angemeldet, werden sie nicht angezeigt.

Um das Label ``faq`` als Filter auf der Suchseite anzuzeigen, legen Sie unter [Crawler] > [Label] ein Label mit dem „Wert“ ``faq`` an (siehe den nächsten Abschnitt „Labels“).

Felder des Index
================

Die im Skript häufig gesetzten Felder sind:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Feld
     - Beschreibung
   * - ``url``
     - Pflichtfeld. Linkziel im Suchergebnis. Muss für jeden Datensatz eindeutig sein
   * - ``title``
     - Überschrift im Suchergebnis. Durchsuchbar
   * - ``content``
     - Text. Durchsuchbar
   * - ``digest``
     - Zusammenfassung, die im Suchergebnis angezeigt wird
   * - ``label``
     - Wert des Labels (siehe unten)
   * - ``role``
     - Rollen, die das Dokument sehen dürfen. Wird verwendet, wenn der Konnektor ACLs liefert (siehe unten)

Außerdem werden ``config_id``, ``boost``, ``role``, ``virtual_host``, ``mimetype`` und weitere Felder automatisch gesetzt (``boost``, ``role`` und ``virtual_host`` sind die Werte von „Boost“, „Berechtigungen“ und „Virtuelle Hosts“ auf dem Einstellungsbildschirm).
Gibt das Skript dasselbe Feld an, wird der Wert durch den Wert aus dem Skript überschrieben.

Beachten Sie bei ``url`` Folgendes:

- Ein Datensatz, dessen Ausdruck ``null`` ergibt, wird nicht registriert. Der CSV-Konnektor erfasst solche Zeilen nicht als Fehler-URL, sondern schreibt nur eine WARN-Zeile mit der Anzahl in ``fess-crawler.log``
- Die Dokument-ID wird aus URL, Rollen und virtuellem Host gebildet. Datensätze, deren ``url`` eine leere Zeichenkette ist, und Datensätze mit derselben ``url`` erhalten bei gleichen Rollen und gleichem virtuellen Host dieselbe Dokument-ID; sie überschreiben sich gegenseitig, und nur der letzte bleibt übrig

Berechtigungen
==============

Auf dem Bildschirm zum Neuerstellen enthält „Berechtigungen“ bereits ``{role}guest``.
Dieser Wert wird zur Rolle aller Dokumente, die aus diesem Datenspeicher registriert werden.
Die Gastrolle wird nicht angemeldeten Benutzern zugewiesen; so wie es ist, lassen sich die Dokumente also ohne Anmeldung durchsuchen.
Für Daten, die öffentlich sein dürfen, etwa eine interne FAQ, können Sie den Wert so belassen.

Für Daten, deren Leserkreis Sie einschränken möchten, steuern Sie den Zugriff auf eine der folgenden Arten:

- Ändern Sie das Feld „Berechtigungen“ in die Gruppen oder Rollen, die die Daten sehen sollen (z. B. ``{group}sales``). Alle Dokumente des Datenspeichers erhalten dieselben Berechtigungen
- Wenn der Konnektor Rollen aus den Freigabeeinstellungen (ACLs) des Quelldienstes bildet, ordnen Sie diese im Skript zu, etwa mit ``role=file.roles``. Der Elementname hängt vom Konnektor ab (bei Slack ``message.roles``), und manche Konnektoren benötigen zusätzliche Parameter, um ACLs abzurufen (etwa ``permission_sync=true`` bei Slack). Prüfen Sie die Referenz des jeweiligen Konnektors

Wenn Sie ACLs verwenden, löschen Sie ``{role}guest`` aus dem Feld „Berechtigungen“.
Konnektoren wie Box, Slack und Microsoft 365 (OneDrive) liefern den Wert des Felds „Berechtigungen“ zusätzlich in ``file.roles`` / ``message.roles`` mit.
Wenn Sie ``{role}guest`` stehen lassen, bleiben die Dokumente deshalb trotz konfigurierter ACLs ohne Anmeldung durchsuchbar.

Lassen Sie umgekehrt das Feld „Berechtigungen“ leer und setzen auch im Skript kein ``role``, erhalten die Dokumente überhaupt keine Rolle.
Solche Dokumente werden auf der Suchseite niemandem angezeigt.

Rollen werden beim Registrieren der Dokumente geschrieben.
Wenn Sie Berechtigungen oder Skript ändern, wirkt sich das erst nach erneutem Crawlen auf vorhandene Dokumente aus.
Der Entwurf von Rollen und Gruppen wird in :doc:`guide-05` erläutert.

Labels
======

Der Einstellungsbildschirm für Datenspeicher hat das Feld „Label“ nicht, das die Einstellungsbildschirme für Web und Dateisystem haben.
Um Labels zuzuweisen, verwenden Sie eine der folgenden Möglichkeiten:

- Schreiben Sie im Skript z. B. ``label="faq"``. Das Label wird allen Dokumenten dieses Datenspeichers zugewiesen
- Geben Sie unter [Crawler] > [Label] in „Eingeschlossene Pfade“ einen regulären Ausdruck an, der auf die URLs der Dokumente passt. Bei der Registrierung wird die URL mit diesem regulären Ausdruck verglichen, und passende Dokumente erhalten das Label

„Eingeschlossene Pfade“ wird als Übereinstimmung mit der gesamten URL ausgewertet; für einen Präfixvergleich hängen Sie daher ``.*`` an (z. B. ``https://intranet\.example\.com/faq/.*``).

Hinweis: Ein im Skript zugewiesenes Label geht verloren, sobald auch nur ein Label unter [Crawler] > [Label] auf die URL des Dokuments passt; dann bleiben nur die passenden Labels übrig.
Auch Labels, die für das Web-Crawling angelegt wurden (z. B. ``https://intranet\.example\.com/.*``), und Labels, bei denen nur „Ausgeschlossene Pfade“ gesetzt ist, werden in den Vergleich einbezogen.
Wenn Sie Labels im Skript zuweisen, stellen Sie sicher, dass kein Label auf die URLs der Dokumente passt.

Geben Sie den „Wert“ eines Labels nur mit alphanumerischen Zeichen und Unterstrichen an (Bindestriche und Nicht-ASCII-Zeichen wie Japanisch sind nicht zulässig).
Damit das Label in der Label-Auswahl der Suchseite erscheint, registrieren Sie auch bei Zuweisung im Skript ein Label mit demselben Wert unter [Crawler] > [Label].
„Eingeschlossene Pfade“ kann dabei leer bleiben.

Boost
=====

Der Wert „Boost“ auf dem Einstellungsbildschirm für Datenspeicher (Standard ``1.0``) wird für alle Dokumente gesetzt, die aus diesem Datenspeicher registriert werden.
Der Boost-Wert wird bei der Suche mit dem Score multipliziert.
Um Dokumente einer bestimmten Datenquelle weiter oben anzuzeigen, ändern Sie diesen Boost-Wert.

Die Regeln unter [Crawler] > [Dokument-Boost] gelten nur für Dokumente, die per Web- und Datei-Crawling registriert werden.
Auf Dokumente aus Datenspeichern werden sie nicht angewendet.

Zeitplanung
===========

Der standardmäßig vorhandene Job „Default Crawler“ läuft täglich um 0:00 Uhr und crawlt alle aktivierten Web-, Dateisystem- und Datenspeicher-Konfigurationen.
Wenn Datenspeicher unterschiedlich häufig ausgeführt werden sollen, erstellen Sie für jede Konfiguration einen eigenen Job.

1. Klicken Sie in der Liste unter [Crawler] > [Datenspeicher] auf den Namen der Konfiguration, um den Detailbildschirm zu öffnen
2. Klicken Sie auf [Neuen Job erstellen]. Der Bildschirm zum Erstellen eines Scheduler-Jobs öffnet sich; „Name“ (``Data Crawler - Interne FAQ``) und ein Skript, das nur diese Konfiguration crawlt, sind bereits ausgefüllt
3. Geben Sie unter „Zeitplan“ die Ausführungszeit im cron-Format ein (Minute Stunde Tag Monat Wochentag) und klicken Sie auf [Erstellen]. Beispiel: ``0 2 * * *`` (täglich um 2:00 Uhr)

Ein Job mit leerem „Zeitplan“ wird nicht regelmäßig ausgeführt, sondern nur manuell.
Um ihn sofort auszuprobieren, öffnen Sie den erstellten Job unter [System] > [Scheduler] und klicken auf [Jetzt starten].

Auch wenn Sie für eine Konfiguration einen eigenen Job anlegen, crawlt „Default Crawler“ diese Konfiguration weiterhin.
Um eine doppelte Ausführung zu vermeiden, deaktivieren Sie den „Status“ dieser Datenspeicher-Konfiguration.
„Default Crawler“ berücksichtigt nur aktivierte Konfigurationen, ein Job mit angegebener Konfigurations-ID crawlt dagegen auch deaktivierte.
Wenn Sie für jede Konfiguration einen eigenen Job anlegen, können Sie auch den „Zeitplan“ von „Default Crawler“ leeren (siehe :doc:`guide-04`).

Ablaufzeit von Dokumenten
=========================

Dokumente, die aus einem Datenspeicher registriert werden, erhalten eine Ablaufzeit.
Sie liegt die unter [System] > [Allgemein] in „Alte Dokumente löschen“ angegebene Anzahl von Tagen (Standard ``3`` Tage) nach dem Startzeitpunkt des Crawls.
Abgelaufene Dokumente werden vom minütlich laufenden Job „Doc Purger“ aus dem Index gelöscht.
Wird dasselbe Dokument beim nächsten Crawl erneut registriert, verlängert sich die Ablaufzeit.

Daher verschwinden Dokumente in den folgenden beiden Fällen aus den Suchergebnissen:

- Das Intervall zwischen den Jobausführungen ist länger als die Anzahl der Tage in „Alte Dokumente löschen“
- Beim inkrementellen Crawling, das nur geänderte Elemente liest (etwa ``incremental=true`` bei Git oder Google Drive), werden unveränderte Dokumente nicht erneut registriert

Um die Ablaufzeit pro Konfiguration zu ändern, geben Sie in den Parametern ``time_to_live`` in Minuten an (z. B. ``time_to_live=11520`` für 8 Tage).
Auch Elemente, die in den Quelldaten gelöscht wurden, verschwinden erst nach Ablauf dieser Zeit aus den Suchergebnissen.
Ist die Ablaufzeit zu lang, werden Löschungen erst sehr spät wirksam.

Ergebnisse prüfen
=================

Beim Datenspeicher-Crawling bedeutet der Jobstatus „OK“ nicht unbedingt, dass alles erfolgreich war.
Auch wenn im Konnektor eine Ausnahme auftritt, protokolliert Fess sie pro Konfiguration oder pro Datensatz und setzt die Verarbeitung fort.
Daher lautet der Status im Jobprotokoll „OK“, und auch der „Crawler-Status“ unter [Systeminformationen] > [Crawling-Informationen] ändert sich nicht.
Prüfen Sie Folgendes der Reihe nach:

1. Vergewissern Sie sich unter [Systeminformationen] > [Jobprotokoll], dass der Job beendet ist. Die Zeile ``Data Config Id:`` im „Ergebnis“ zeigt die ID der betreffenden Konfiguration
2. Prüfen Sie unter [Systeminformationen] > [Crawling-Informationen] die „Indexgröße (Datenspeicher)“ der Sitzung. Das ist die Anzahl der in dieser Sitzung registrierten Dokumente (bei „Default Crawler“ die Summe aller Datenspeicher)
3. Prüfen Sie unter [Systeminformationen] > [Fehler-URL], dass keine Fehler erfasst wurden
4. Laden Sie unter [Systeminformationen] > [Protokolldatei] die Datei ``fess-crawler.log`` herunter und prüfen Sie die Zeilen mit ERROR und WARN (sie liegt bei Docker und RPM / DEB in ``/var/log/fess/``, beim ZIP-Paket in ``logs/``)
5. Suchen Sie unter [Systeminformationen] > [Suche] z. B. nach ``label:faq`` und prüfen Sie die Trefferzahl

Wo Hinweise zurückbleiben, hängt von der Art des Fehlschlags ab.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Situation
     - Fehler-URL
     - fess-crawler.log
   * - Der Handler wird nicht gefunden (etwa wenn das Plugin nach dem Anlegen der Konfiguration entfernt wurde)
     - Kein Eintrag
     - ``DataStore(...) is not found.``
   * - Die gesamte Konfiguration schlägt fehl (ein Authentifizierungsfehler, bei dem der Konnektor nicht weiterarbeiten kann, ein fehlender Pflichtparameter usw.)
     - Ein Eintrag. Die URL-Spalte lautet ``D<Konfigurations-ID>:<Konfigurationsname>``
     - ``Failed to process a data crawling: <Konfigurationsname>``
   * - Ein einzelner Datensatz schlägt fehl (ein Fehler bei der Skriptauswertung usw.)
     - Ein Eintrag pro Datensatz. Bei CSV ``<Dateipfad>:<Zeilennummer>``
     - WARN-Zeilen

Beim CSV-Konnektor gibt es auch keinen Fehler, wenn die in ``files`` angegebene Datei nicht gefunden wird oder ihre Erweiterung nicht ``.csv`` / ``.tsv`` ist.
Der Konnektor gibt die WARN-Meldungen ``is not found.`` und ``No CSV file.`` aus und endet mit 0 Dokumenten.

[Systeminformationen] > [Suche] zeigt alle Dokumente ohne Filterung nach Berechtigungen an und eignet sich daher zum Prüfen der Dokumentanzahl.
Ob die Berechtigungen wie beabsichtigt sind, lässt sich damit dagegen nicht prüfen.
Prüfen Sie Berechtigungen auf der normalen Suchseite, während Sie als der betreffende Benutzer angemeldet sind (bei Dokumenten mit ``{role}guest`` im abgemeldeten Zustand) (:doc:`guide-05`).

Wenn Sie nicht wissen, welche Elementnamen ein Konnektor übergibt: Bei manchen Konnektoren werden die abgerufenen Werte protokolliert, wenn Sie die Protokollebene des Crawlers auf DEBUG setzen (der CSV-Konnektor gibt die Werte jeder Zeile aus).
Wie Sie das einstellen, steht unter „Debug-Einstellungen“ in der `Übersicht der Datenspeicher-Konnektoren <https://fess.codelibs.org/de/stable/config/datastore/ds-overview.html>`__.

Artikel und Referenzen zu den einzelnen Konnektoren
===================================================

Die Einstellungen der einzelnen Konnektoren werden in den folgenden Artikeln erläutert.

- :doc:`guide-06` - Git, Confluence, Jira, Slack
- :doc:`guide-07` - Google Drive, SharePoint Online / OneDrive, Box
- :doc:`guide-12` - Datenbanken, CSV, Salesforce

Referenzen:

- `Übersicht der Datenspeicher-Konnektoren <https://fess.codelibs.org/de/stable/config/datastore/ds-overview.html>`__ (Liste aller Konnektoren mit Plugin-Namen)
- `CSV-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-csv.html>`__ / `JSON-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-json.html>`__ / `Datenbank-Konnektor <https://fess.codelibs.org/de/stable/config/datastore/ds-database.html>`__
- `Google Drive <https://fess.codelibs.org/de/stable/config/datastore/ds-gsuite.html>`__ / `Microsoft 365 <https://fess.codelibs.org/de/stable/config/datastore/ds-microsoft365.html>`__ / `Box <https://fess.codelibs.org/de/stable/config/datastore/ds-box.html>`__
- `Atlassian <https://fess.codelibs.org/de/stable/config/datastore/ds-atlassian.html>`__ / `Slack <https://fess.codelibs.org/de/stable/config/datastore/ds-slack.html>`__ / `Git <https://fess.codelibs.org/de/stable/config/datastore/ds-git.html>`__ / `Salesforce <https://fess.codelibs.org/de/stable/config/datastore/ds-salesforce.html>`__
- `Datenspeicher-Crawl (Administrationsoberfläche) <https://fess.codelibs.org/de/stable/admin/dataconfig-guide.html>`__ / `Scheduler <https://fess.codelibs.org/de/stable/admin/scheduler-guide.html>`__ / `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__ / `Label <https://fess.codelibs.org/de/stable/admin/labeltype-guide.html>`__ / `JavaScript-Skripting-Leitfaden <https://fess.codelibs.org/de/stable/config/scripting-javascript.html>`__
