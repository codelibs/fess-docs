=========================================
Suche in eine bestehende Website einbauen
=========================================

Einleitung
==========

Wenn Sie ein Intranetportal oder eine Produktwebsite mit einer Suche ausstatten möchten, ist es nicht realistisch, dass sich die Benutzer die URL von Fess merken.
Gefragt ist ein Suchfeld im Kopfbereich der Seiten, die ohnehin ständig geöffnet sind, und eine Ergebnisseite, die wie ein Teil dieser Website aussieht.

In diesem Artikel probieren wir mit Fess 15.9 nacheinander die folgenden drei Methoden aus, die sich alle allein auf der Browserseite umsetzen lassen.

- Ein HTML-Suchformular auf einer bestehenden Seite platzieren und die Ergebnisse auf der Suchseite von Fess anzeigen
- Mit Fess Site Search (FSS) die Suchergebnisse innerhalb einer Seite der bestehenden Website anzeigen
- Das Aussehen der Suchseite von Fess (das Theme) an die bestehende Website anpassen

Außerdem richten wir die „Pfadzuordnung“ ein, mit der die Linkziele der Suchergebnisse auf URLs umgestellt werden, die die Benutzer erreichen können.

Wie Sie vom Server eines Geschäftssystems aus die Such-API aufrufen und eigene Oberflächen bauen, wird in :doc:`guide-11` behandelt.

Voraussetzungen
===============

- Gemäß den Schritten in :doc:`guide-02` läuft Fess 15.9 mit Docker Compose unter ``http://localhost:8080/``, und es wurde bereits etwas gecrawlt
- Eine lokale HTML-Datei als Ersatz für die bestehende Website

Eine bestehende Website liegt normalerweise auf einem anderen Ursprung (der Kombination aus Schema, Host und Port) als Fess.
Um in diesem Artikel dieselbe Bedingung herzustellen, führen Sie im Verzeichnis mit der HTML-Datei den folgenden Befehl aus und öffnen die Datei unter ``http://localhost:8000/``.

::

    $ python3 -m http.server 8000

Die passende Methode wählen
===========================

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - Methode
     - Wo die Suchergebnisse angezeigt werden
     - Was auf der Fess-Seite nötig ist
   * - Suchformular
     - Wechsel zur Suchseite von Fess (``/search``) und Anzeige dort
     - Nichts
   * - Fess Site Search
     - Innerhalb einer Seite der bestehenden Website
     - Das Plugin ``fess-webapp-v1-api``
   * - Theme ändern
     - Suchseite von Fess (mit geändertem Aussehen)
     - Ein Theme-ZIP (oder die Einstellungen unter [Allgemein])

Suchformular und Theme-Änderung lassen sich kombinieren.
Soll auch die Seite, auf die die Benutzer von der bestehenden Website aus gelangen, gleich aussehen, richten Sie beides ein.

Ein Suchformular platzieren und an die Suchseite von Fess senden
================================================================

Das Formular platzieren
-----------------------

Schreiben Sie das folgende Formular an die Stelle der bestehenden Seite, an der das Suchfeld erscheinen soll.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">Suchen</button>
    </form>

Die Suchbegriffe werden als Parameter ``q`` an ``/search`` von Fess gesendet, und die Ergebnisse erscheinen auf der Suchseite von Fess.
``maxlength`` entspricht der Obergrenze für die Länge von Suchbegriffen auf der Fess-Seite, ``query.max.length`` (Standardwert ``1000``).
Ändern Sie die URL in ``action`` im Produktivbetrieb auf die Fess-URL, die die Benutzer aufrufen.

Sollen nur Dokumente mit einem bestimmten Label durchsucht werden, senden Sie den Wert des Labels zusätzlich als ``fields.label``.

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">Suchen</button>
    </form>

``intranet`` ist der Wert eines Labels, das unter [Crawler] > [Label] angelegt wurde.
Wird ein Wert gesendet, der nicht existiert, gibt es 0 Treffer.
Wie Sie Labels anlegen, lesen Sie in :doc:`guide-04`.

Überprüfen
----------

1. Öffnen Sie die HTML-Datei über ``http://localhost:8000/`` und suchen Sie nach einem Wort, das in einem gecrawlten Dokument vorkommt
2. Wechselt der Browser zu ``http://localhost:8080/search?q=...`` und werden die Ergebnisse auf der Suchseite von Fess angezeigt, ist die Einrichtung abgeschlossen

Gibt es 0 Treffer, suchen Sie dasselbe Wort im Suchfeld unter ``http://localhost:8080/`` und vergleichen Sie.
Gibt es auch dort 0 Treffer, liegt das Problem nicht am Formular, sondern am Crawling oder an den Berechtigungen.

Zu den Vorschlägen
------------------

Die Seite `Platzierung von Suchformularen <https://fess.codelibs.org/de/stable/config/search-form-integration.html>`__ enthält ein Beispiel, das das Formular mit Vorschlägen ausstattet.
Die von diesem Beispiel geladenen Dateien ``/js/suggestor.js`` und ``/js/jquery-3.7.1.min.js`` sind in Fess 15.9 jedoch nicht enthalten, sodass das Beispiel in 15.9 so nicht funktioniert.
Der Formularteil (``q`` an ``/search`` senden) lässt sich unverändert verwenden.

Wenn das Suchfeld der bestehenden Website Vorschläge anzeigen soll, verwenden Sie eine der folgenden Möglichkeiten.

- Die Vorschläge in Fess Site Search aus dem nächsten Abschnitt aktivieren
- ``/api/v2/suggest-words`` aus einem eigenen Skript aufrufen (zur Verwendung der API siehe :doc:`guide-11`)

Nach dem Wechsel zur Suchseite von Fess zeigt das mit Fess ausgelieferte Theme die Vorschläge an.

Ergebnisse mit Fess Site Search innerhalb der Seite anzeigen
============================================================

Fess Site Search (FSS) ist ein JavaScript, das ein Suchformular und Suchergebnisse auf einer Seite der bestehenden Website anzeigt.
Die Benutzer können suchen, ohne die bestehende Website zu verlassen.

Das JavaScript von FSS wird nicht von Fess ausgeliefert.
Laden Sie die mit dem FSS JS Generator (https://fss-generator.codelibs.org/) erzeugte Datei herunter und legen Sie sie auf dem Server der bestehenden Website ab.

Das Plugin für die v1-API installieren
--------------------------------------

FSS ruft ``/api/v1`` von Fess auf.
Fess 15.9 selbst stellt nur ``/api/v2`` bereit; ``/api/v1`` wird vom Plugin ``fess-webapp-v1-api`` bereitgestellt.
Dieses Plugin ist im Docker-Image nicht enthalten.

Fügen Sie bei Docker Compose unter ``environment`` von ``fess01`` in ``compose.yaml`` die folgende Zeile hinzu.

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

Wenn Sie bereits andere Plugins angeben, führen Sie sie im selben Wert durch Leerzeichen getrennt auf.
Führen Sie nach dem Speichern ``up -d`` mit beiden Compose-Dateien aus.
``fess01`` wird neu erstellt, und das Plugin wird beim Start installiert.
Da der Container neu erstellt wird, werden Einstellungen, die Sie unter [System] > [Allgemein] geändert haben, wie bei ``down`` zurückgesetzt (siehe den Abschnitt über das Stoppen und Neustarten in :doc:`guide-02`).

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Das Plugin lässt sich auch in der Administrationsoberfläche unter [System] > [Plugin] > [Installieren] installieren (nach der Installation muss Fess neu gestartet werden).
Unter Docker liegt das Plugin jedoch im Container und verschwindet daher, wenn der Container mit ``down`` neu erstellt wird.
Wenn Sie es in ``FESS_PLUGINS`` angeben, wird es bei jeder Neuerstellung erneut installiert.

Sobald ``fess01`` healthy ist, prüfen Sie, ob die API antwortet.

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

Wird JSON mit ``"record_count"`` zurückgegeben, ist alles bereit.
Wird 404 zurückgegeben, ist das Plugin nicht installiert.
In diesem Fall wird in ``fess.log`` einmalig eine WARN-Meldung ausgegeben, die mit ``No plugin serves the legacy API`` beginnt.
Ist das Plugin installiert, wird aber kein JSON zurückgegeben, prüfen Sie, ob „JSON-Antwort“ unter [System] > [Allgemein] ausgeschaltet ist.
Wenn „JSON-Antwort“ ausgeschaltet ist, antworten nicht nur ``/api/v1``, sondern auch ``/api/v2`` nicht mehr, und auch die Suchseite von Fess selbst ist nicht mehr nutzbar.

Das JavaScript erzeugen und ablegen
-----------------------------------

1. Öffnen Sie https://fss-generator.codelibs.org/, legen Sie im Generator Farben, Schriftarten usw. fest und klicken Sie auf [Generate]
2. Laden Sie die JavaScript-Datei mit [Download JS] herunter
3. Benennen Sie die Datei in ``fess-ss.js`` um und legen Sie sie in dasselbe Verzeichnis wie die HTML-Datei

Schreiben Sie auf der Seite, die die Suchergebnisse anzeigt (zum Beispiel ``result.html``), den folgenden Code.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="de"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="de"
      ></fess-search-result>
    </div>

``fess-url`` ist die Fess-URL für die Suche, ``suggest-url`` die Fess-URL für die Vorschläge.
Verwenden Sie im Produktivbetrieb eine Fess-URL, die von den Browsern der Benutzer aus erreichbar ist.

Im Kopfbereich der übrigen Seiten platzieren Sie nur das Suchformular.

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

Das Formular schreibt die Suchbegriffe in den Parameter ``fss.query`` und wechselt zu ``result.html``, und FSS auf ``result.html`` führt die Suche aus.
Auch von Seiten, die FSS nicht laden, funktioniert das genauso, wenn Sie ein Formular schreiben, das zu ``result.html?fss.query=Suchbegriff`` wechselt.

Weitere Attribute (Anzahl der Treffer pro Seite ``:page-size``, Eingrenzung nach Label ``:enable-label``, Öffnen von Links in einem neuen Tab ``link-target="_blank"`` usw.) finden Sie im Handbuch des FSS JS Generator.

Überprüfen
----------

1. Öffnen Sie ``http://localhost:8000/result.html`` und suchen Sie über das Suchformular
2. Werden die Suchergebnisse innerhalb der Seite angezeigt, ist die Einrichtung abgeschlossen
3. Werden sie nicht angezeigt, prüfen Sie im Netzwerk-Tab der Entwicklertools des Browsers die Anfrage an ``/api/v1/documents``. Bei 404 prüfen Sie das Plugin, bei einem CORS-Fehler den nächsten Abschnitt

Worauf Sie achten sollten
-------------------------

Aus Sicht des Browsers ist der Aufruf der API auf ``localhost:8080`` von einer Seite auf ``localhost:8000`` eine ursprungsübergreifende (Cross-Origin-)Kommunikation.
Fess ist standardmäßig auf ``api.cors.allow.origin=*`` eingestellt und nimmt Aufrufe von jedem Ursprung an.
Wie Sie die Aufrufer auf die bestehende Website beschränken, wird in :doc:`guide-11` behandelt.

Suchen, die FSS von einem anderen Ursprung aus sendet, werden als Suchen eines nicht angemeldeten Benutzers (Gast) behandelt, auch wenn der Benutzer bei Fess angemeldet ist.
Der Grund: FSS ruft die API ohne Cookies auf, und mit der Standardeinstellung ``api.cors.allow.origin=*`` ist ursprungsübergreifende Kommunikation mit Anmeldedaten ohnehin nicht erlaubt.
Daher erscheinen in den Ergebnissen nur Dokumente, deren Berechtigungen ``{role}guest`` enthalten.
Wenn jede Abteilung andere Dokumente sehen soll, lassen Sie die Benutzer sich auf der Suchseite von Fess anmelden (siehe :doc:`guide-05`).

Das Aussehen der Suchseite von Fess ändern
==========================================

In 15.9 wird die Suchseite durch ein „Theme“ dargestellt, das HTML, CSS und JavaScript bündelt.
Die Seite [Seitengestaltung] und das Bearbeiten von JSPs aus früheren Versionen gibt es nicht mehr.
Ist nichts eingestellt, wird das mitgelieferte Theme ``bootstrap`` verwendet.

Was sich ohne ZIP ändern lässt
------------------------------

Was Sie unter [System] > [Allgemein] im Bereich „Ankündigung“ in „Such-Startseite“ eintragen, wird im mitgelieferten Theme auf der Such-Startseite und auf der Suchergebnisseite angezeigt.
Sie können auch HTML schreiben, Elemente wie ``<script>`` und ``<style>`` werden jedoch entfernt.
Wenn Sie nur einen einzeiligen Hinweis für interne Benutzer anzeigen möchten, müssen Sie kein Theme erstellen.

Ein veröffentlichtes Theme verwenden
------------------------------------

Das Fess-Projekt veröffentlicht Themes wie ``docsearch``, das für die Dokumentensuche gedacht ist.

1. Öffnen Sie [System] > [Theme]
2. Wählen Sie unter „Theme installieren“ in „Name“ ein Theme aus und klicken Sie auf [Auswählen]
3. Wählen Sie in „Version“ die Version für 15.9 (``15.9.x``) und klicken Sie auf [Installieren]
4. Wählen Sie oberhalb der Liste in „Standard-Theme“ das installierte Theme aus und klicken Sie auf [Festlegen]

Wenn Sie ``http://localhost:8080/`` erneut öffnen, wird die Seite mit dem neuen Theme angezeigt.
Wählen Sie „(kein Standard)“ und klicken Sie auf [Festlegen], um zum mitgelieferten ``bootstrap`` zurückzukehren.

Das mitgelieferte Theme kopieren und Logo und Farben ändern
-----------------------------------------------------------

Das mitgelieferte Theme kann nicht direkt bearbeitet werden, und ein Theme namens ``bootstrap`` lässt sich auch nicht durch Hochladen ersetzen.
Kopieren Sie es unter einem anderen Namen und ändern Sie die Kopie.
Hier verwenden wir ``mytheme``.

1. Kopieren Sie das mitgelieferte Theme aus dem Container

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. Ändern Sie in ``mytheme/theme.yml`` den Wert von ``name`` in ``mytheme`` und den von ``displayName`` beispielsweise in ``My Theme``
3. Ändern Sie die folgenden Dateien

   - Farben und Layout: ``assets/styles.css``
   - Logo: ``assets/logo-head.png`` (Kopfbereich) und ``assets/logo.png`` (Such-Startseite)
   - Name der Organisation in der Fußzeile: ``footer.copyright_org`` in ``i18n/messages.de.json`` (für die englische Oberfläche ``messages.en.json``)

4. Packen Sie die Dateien so, dass ``theme.yml`` im Stammverzeichnis des ZIP liegt

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. Laden Sie ``mytheme.zip`` unter [System] > [Theme] über [Hochladen] hoch
6. Wählen Sie in „Standard-Theme“ ``mytheme`` aus und klicken Sie auf [Festlegen]

``index.html`` ändern Sie nicht.
Die mitgelieferte ``index.html`` verweist auf die Dateien im Theme in der Form ``{{themePath}}/assets/...``.
Da Fess ``{{themePath}}`` bei der Auslieferung durch ``themes/mytheme`` ersetzt, genügt die Umbenennung, damit die Dateien des kopierten Themes geladen werden.

Überprüfen
----------

Öffnen Sie ``http://localhost:8080/`` erneut und prüfen Sie, ob sich Logo und Farben geändert haben.
Falls nicht, prüfen Sie im Netzwerk-Tab der Entwicklertools, ob das Stylesheet von ``/themes/mytheme/assets/styles.css`` geladen wird.
Wird es von ``/themes/bootstrap/`` geladen, ist die Einstellung des Standard-Themes nicht wirksam.

Worauf Sie bei Themes achten sollten
------------------------------------

- Die Suchseite erhält einen ``Content-Security-Policy``-Header, der die Quellen von Skripten, Styles und Bildern auf Fess selbst beschränkt. Schriftarten und Skripte von externen CDNs werden nicht geladen; nehmen Sie sie daher in das Theme-ZIP auf
- Die Suchseite wird nicht im ``iframe`` einer anderen Seite angezeigt (weil der Standardwert von ``theme.index.frame.ancestors`` ``'none'`` ist). Um Suchergebnisse innerhalb eines Portals anzuzeigen, verwenden Sie FSS
- ``fess01`` unter Docker hat keine Volumes. Hochgeladene Themes liegen im Container, und die Einstellung des Standard-Themes wird in ``system.properties`` gespeichert; beides geht daher verloren, wenn der Container mit ``down`` neu erstellt wird. Verwenden Sie im Alltag ``stop``/``start`` und wiederholen Sie nach einer Neuerstellung das Hochladen und die Einstellung
- Das mitgelieferte Theme ist auf ``/api/v2`` der jeweiligen Fess-Version abgestimmt. Kopieren Sie nach einem Upgrade von Fess das neue mitgelieferte Theme erneut und übertragen Sie Ihre Änderungen darauf

Zum Aufbau von Themes und zu den Einträgen in ``theme.yml`` siehe den `Theme-Entwicklungsleitfaden <https://fess.codelibs.org/de/stable/dev/theme-development.html>`__.

Linkziele der Suchergebnisse auf URLs für die Benutzer umstellen
================================================================

Manchmal soll mit einem internen Hostnamen gecrawlt werden, während die Benutzer die Dokumente über die URL des Portals öffnen sollen.
Zum Beispiel crawlen Sie ``http://intranet-web01:8080/docs/`` und möchten, dass die Suchergebnisse ``https://portal.example.com/docs/`` öffnen.
In diesem Fall ersetzen Sie die URL mit der Pfadzuordnung nur für die Anzeige.

1. Öffnen Sie [Crawler] > [Pfadzuordnung] und klicken Sie auf [Neu erstellen]
2. Geben Sie Folgendes ein und klicken Sie auf [Erstellen]

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - Feld
        - Wert
      * - Regulärer Ausdruck
        - ``^http://intranet-web01:8080/docs/``
      * - Ersetzung
        - ``https://portal.example.com/docs/``
      * - Prozesstyp
        - Anzeige
      * - Sortierreihenfolge
        - ``0``

„Anzeige“ ersetzt nur die in den Suchergebnissen angezeigte URL und das Linkziel.
Die im Index gespeicherte URL ändert sich nicht; ein erneutes Crawlen ist daher nicht nötig, und die Änderung wirkt sich ab dem Speichern auf die Suchergebnisse aus.
Wenn Sie „Crawling“ oder „Crawling/Anzeige“ wählen, wird die ersetzte URL im Index gespeichert.
Beachten Sie, dass bei dieser Wahl auch die URLs späterer Crawls geändert werden, obwohl Sie nur die Anzeige ändern wollten.

Zur Überprüfung suchen Sie nach einem Wort, das das betreffende Dokument findet, und prüfen, ob URL und Linkziel in den Ergebnissen ``https://portal.example.com/docs/...`` lauten.
Wenn Sie Ergebnisse über die API erhalten, steht die ersetzte URL nicht in ``url``, sondern in ``url_link`` (siehe :doc:`guide-11`).

Ein Beispiel, das Pfade eines Dateiservers in URLs eines Webservers umwandelt, finden Sie unter `Pfad-Mapping <https://fess.codelibs.org/de/stable/admin/pathmap-guide.html>`__.

Weiterführende Artikel
======================

- Die Such-API vom Server eines Geschäftssystems aus aufrufen: :doc:`guide-11`
- Die im Portal angezeigten Dokumente je Abteilung unterscheiden: :doc:`guide-05`
- Websites und Dateiserver gemeinsam durchsuchen und mit Labels trennen: :doc:`guide-04`
- Jeder Organisation ein anderes Theme oder andere Suchziele zeigen: :doc:`guide-13`
- Für die Suchseite eine Anmeldung voraussetzen: :doc:`guide-15`

Referenzen
==========

- `Platzierung von Suchformularen <https://fess.codelibs.org/de/stable/config/search-form-integration.html>`__
- `Theme <https://fess.codelibs.org/de/stable/admin/theme-guide.html>`__
- `Theme-Entwicklungsleitfaden <https://fess.codelibs.org/de/stable/dev/theme-development.html>`__
- `Pfad-Mapping <https://fess.codelibs.org/de/stable/admin/pathmap-guide.html>`__
- `Plug-ins <https://fess.codelibs.org/de/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search (GitHub) <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api (GitHub) <https://github.com/codelibs/fess-webapp-v1-api>`__
