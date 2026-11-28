=================================================
Suchqualität anhand der Suchprotokolle verbessern
=================================================

Einführung
==========

Sobald die Suche genutzt wird, hört man Aussagen wie „Das gesuchte Dokument wird nicht gefunden“ oder „Das gewünschte Dokument steht ganz unten in der Trefferliste“.
Was bei welchem Suchbegriff geschieht, zeigen die Such- und Klickprotokolle, die Fess aufzeichnet.

In Fess 15.9 enthält die Verwaltungsoberfläche unter [Systeminformationen] > [Suchprotokoll] einen Analysebericht, der Kennzahlen wie die Quote ohne Treffer und die Klickpositionen auswertet.
Dieser Artikel zeigt, wie Sie auf diesem Bildschirm problematische Suchbegriffe finden, entscheiden, ob Sie sie mit Synonymen, Schlüsselübereinstimmung, Dokument-Boost, verwandten Abfragen oder Stoppwörtern beheben, die Änderung übernehmen und ihre Wirkung auf demselben Bildschirm überprüfen.

Wie Sie Suchprotokolle in OpenSearch Dashboards selbst auswerten, behandelt :doc:`guide-22`; wie Dokumente mit gemischtem japanischem, englischem und chinesischem Text analysiert werden, behandelt :doc:`guide-09`.

Worauf Sie im Suchprotokoll achten sollten
==========================================

Öffnen Sie im linken Menü [Systeminformationen] > [Suchprotokoll]; angezeigt wird die Registerkarte [Übersicht].
Für die Anzeige ist die Rolle ``admin-searchlog`` oder ``admin-searchlog-view`` erforderlich.

Wählen Sie oben auf jeder Registerkarte den Zeitraum („Heute“, „Gestern“, „Letzte 7 Tage“, „Letzte 28 Tage“, „Letzte 90 Tage“, „Benutzerdefiniert“) und den Zugriffstyp, und klicken Sie auf [Anwenden].
Wenn Sie „Mit vorherigem Zeitraum vergleichen“ aktivieren, werden die Werte des davorliegenden Zeitraums mit gleicher Anzahl Tage daneben angezeigt.
Damit vergleichen Sie den Stand vor und nach einer Verbesserung.

Die Kennzahlen, die Hinweise für Verbesserungen liefern, und die jeweils wirksamen Maßnahmen sind:

.. list-table::
   :header-rows: 1
   :widths: 24 22 30 24

   * - Kennzahl
     - Wo sie angezeigt wird
     - Was sie zeigt
     - Wichtigste Maßnahmen
   * - Quote ohne Treffer, Suchbegriffe ohne Treffer
     - Registerkarten [Übersicht] und [Suchbegriffe]
     - Der Anteil der Suchen ohne einen einzigen Treffer und die zugehörigen Suchbegriffe
     - Synonyme, verwandte Abfragen, Dokumente ergänzen
   * - Suchbegriffe ohne Klicks
     - Registerkarte [Suchbegriffe]
     - Suchbegriffe mit Treffern, deren Ergebnisse aber nie angeklickt wurden
     - Schlüsselübereinstimmung, Dokument-Boost
   * - Durchschn. Klickposition
     - Registerkarte [Suchbegriffe] (je Suchbegriff), Registerkarte [Klicks] (gesamt)
     - An welcher Position die angeklickten Ergebnisse standen (der erste Treffer ist 1)
     - Schlüsselübereinstimmung, Dokument-Boost
   * - Verteilung der Klickpositionen, Aufrufrate weiterer Seiten
     - Registerkarte [Klicks]
     - Ob sich die Klicks auf die Positionen 1–10, 11–20 oder ab 21 konzentrieren, und der Anteil der Suchen, bei denen Seite 2 oder später aufgerufen wurde
     - Schlüsselübereinstimmung, Dokument-Boost
   * - Häufigste Suchbegriffe, am häufigsten angeklickte URLs
     - Registerkarte [Übersicht], Registerkarte [Klicks]
     - Häufig gesuchte Begriffe und die tatsächlich geöffneten Dokumente
     - Die Ergebnisse der Begriffe von oben nach unten prüfen

Als Grundlage für die Auswertung sollten Sie Folgendes wissen.

- Die Aufzeichnung wird unter [System] > [Allgemein] mit „Suchprotokoll“ und „Benutzerprotokoll“ aktiviert (beide sind standardmäßig aktiviert). Ist „Benutzerprotokoll“ deaktiviert, wird die Anzahl der Benutzer nicht erfasst.
- Ein Klick wird aufgezeichnet, wenn „Suchprotokoll“ aktiviert ist und ein Link in den Suchergebnissen über ``/go/`` geöffnet wird. Die Suchseite des Standard-Themes (bootstrap) erzeugt ihre Links auf diese Weise.
- Die Klickkennzahlen je Suchbegriff und die Suchbegriffe ohne Klicks berücksichtigen nur Klicks ab 15.9, der Version, ab der Klicks zusammen mit dem Suchbegriff aufgezeichnet werden.
- Ist unter [Allgemein] bei „Alte Suchprotokolle löschen“ eine Anzahl Tage angegeben, lassen sich ältere Protokolle nicht zum Vergleich heranziehen (der Standardwert ``-1`` löscht nichts).
- Protokolle werden gesammelt geschrieben; es kann daher etwas dauern, bis eine Suche auf dem Bildschirm erscheint.

Ursachen für Suchbegriffe ohne Treffer unterscheiden
====================================================

Wenn Sie auf der Registerkarte [Übersicht] oder [Suchbegriffe] auf einen Suchbegriff ohne Treffer klicken, zeigt die Registerkarte [Protokolle] die Suchprotokolle dieses Begriffs, gefiltert mit „Trefferzahl“ = „Nur ohne Treffer“.
Prüfen Sie, wann und mit welchem Zugriffstyp gesucht wurde, suchen Sie dann auf der Suchseite selbst nach dem Begriff und ordnen Sie die Ursache einem der folgenden drei Fälle zu.

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Situation
     - Maßnahme
     - Erforderlicher Schritt zur Übernahme
   * - Die Dokumente sind vorhanden, verwenden aber andere Wörter (z. B. suchen Benutzer nach „Homeoffice“, die Dokumente sprechen von „Telearbeit“)
     - Synonyme
     - Dokumentenindex neu laden
   * - Benutzer sollen zur offiziellen Bezeichnung geführt werden (Abkürzungen, frühere Namen, Schreibfehler)
     - Verwandte Abfragen
     - Keiner (wirksam beim Speichern)
   * - Passende Dokumente sind nicht im Index
     - Crawl-Ziele ergänzen (:doc:`guide-04`)
     - Crawl ausführen

Schlüsselübereinstimmung und Dokument-Boost helfen bei Suchbegriffen ohne Treffer nicht.
Beide heben die Position von Dokumenten an, die zum Suchbegriff passen, und fügen den Ergebnissen keine Dokumente hinzu, die nicht zum Suchbegriff passen.

Praxisbeispiel: Suchbegriff „Homeoffice“ ohne Treffer mit einem Synonym beheben
===============================================================================

Angenommen, „Homeoffice“ taucht auf der Registerkarte [Suchbegriffe] immer wieder unter den Suchbegriffen ohne Treffer auf, während die internen Richtlinien das Wort „Telearbeit“ verwenden.
An diesem Beispiel gehen wir alles von der Korrektur bis zur Überprüfung durch.

1. Ursache bestätigen
---------------------

Suchen Sie auf der Suchseite nach „Telearbeit“ und vergewissern Sie sich, dass die Dokumente gefunden werden, nach denen die Benutzer vermutlich gesucht haben.
Werden sie hier nicht gefunden, liegt es nicht an der Wortwahl, sondern die Dokumente fehlen im Index.
Überprüfen Sie dann die Crawl-Ziele statt eines Synonyms.

2. Synonym registrieren
-----------------------

1. Öffnen Sie [System] > [Wörterbuch] und klicken Sie in der Liste auf die Zeile, deren „Typ“ ``synonym`` ist (deren Name auf ``synonym.txt`` endet).
2. Klicken Sie auf [Neu erstellen].
3. Geben Sie sowohl unter „Quelle“ als auch unter „Ziel“ die folgenden zwei Zeilen ein und klicken Sie auf [Erstellen].

::

    Homeoffice
    Telearbeit

Stehen unter „Quelle“ und „Ziel“ dieselben Wörter, wird im Wörterbuch die einzelne Zeile ``Homeoffice,Telearbeit`` gespeichert, und die Suche nach einem der beiden Wörter findet auch Dokumente, die das andere enthalten.
Soll nur die Suche nach „Homeoffice“ erweitert werden, tragen Sie unter „Quelle“ nur die Zeile „Homeoffice“ und unter „Ziel“ die beiden obigen Zeilen ein (daraus wird ``Homeoffice=>Homeoffice,Telearbeit``).
Beachten Sie: Enthält „Ziel“ das ursprüngliche Wort nicht, wird nach dem ursprünglichen Wort selbst nicht mehr gesucht.

Schreiben Sie in die Eingabefelder ein Wort pro Zeile.
Wörter, die ein Komma (,) oder ``=>`` enthalten, können nicht registriert werden.
Die Referenz zum Synonym-Wörterbuch nennt folgende Regeln für die Registrierung.

- Hiragana als Katakana, kleine Katakana als normal große Katakana und Alphanumerik in voller Breite als Alphanumerik in halber Breite registrieren
- Japanischer und anderer CJK-Text wird standardmäßig als Bi-Gramme indexiert, also in Einheiten von je zwei Zeichen; daher keine Wörter aus nur einem Zeichen registrieren
- Dasselbe Wort nicht mehrfach registrieren

Synonyme wirken auf die Felder ``content`` und ``title`` und erweitern die Wörter zum Zeitpunkt der Suche.
Eine Neuindexierung ist nicht erforderlich.

3. Wörterbuchänderung übernehmen
--------------------------------

Allein durch das Speichern des Wörterbuchs ändern sich die Suchergebnisse nicht.
Der geöffnete Index arbeitet weiter mit dem alten Wörterbuch.

1. Öffnen Sie [Systeminformationen] > [Wartung].
2. Klicken Sie unter „Dokumentenindex neu laden“ auf [Neu laden].

Diese Schaltfläche schreibt die gespeicherten Wörterbücher in Dateien, schließt dann den Dokumentenindex und öffnet ihn erneut.

.. warning::

   Solange der Index geschlossen ist und nach dem Öffnen, bis die Shards zugewiesen sind, ist keine Suche möglich; Suchen liefern Fehler oder 0 Treffer.
   Je größer der Index, desto länger dauert dies; führen Sie es daher zu einer Zeit mit geringer Nutzung aus.

4. Wirkung überprüfen
---------------------

Suchen Sie zuerst auf der Suchseite nach „Homeoffice“ und vergewissern Sie sich, dass Dokumente mit „Telearbeit“ gefunden werden.

Filtern Sie dann unter [Systeminformationen] > [Suchprotokoll] auf der Registerkarte [Protokolle] mit „Homeoffice“ als „Suchbegriff“ und „Mindestens ein Treffer“ als „Trefferzahl“.
Werden die Suchen der Benutzer nach der Änderung mit Treffern aufgezeichnet, wirkt die Korrektur.

Stellen Sie nach einigen Tagen auf der Registerkarte [Übersicht] den Zeitraum auf „Benutzerdefiniert“, setzen Sie das Startdatum auf den Tag nach der Änderung und aktivieren Sie „Mit vorherigem Zeitraum vergleichen“.
Zeiträume werden tageweise abgegrenzt (Datum in der Zeitzone des Servers); schließen Sie den Tag der Änderung ein, werden auch die Suchen ohne Treffer von vor der Änderung mitgezählt.
Prüfen Sie, dass die Quote ohne Treffer niedriger ist als im vorherigen Zeitraum und dass „Homeoffice“ aus der Liste der Suchbegriffe ohne Treffer verschwunden ist.
Belassen Sie den Zeitraum etwa bei „Letzte 7 Tage“, bleiben die Suchen ohne Treffer von vor der Änderung im Zeitraum enthalten, sodass der Begriff nicht sofort aus der Liste verschwindet.

Den Inhalt des Wörterbuchs können Sie auf dem Listenbildschirm mit [Herunterladen] als Datei speichern.
Speichern Sie ihn vor und nach einer Änderung, um ihn bei Bedarf wiederherstellen zu können.

Bestimmte Dokumente nach oben holen: Schlüsselübereinstimmung
=============================================================

Bei Begriffen mit hoher durchschnittlicher Klickposition auf der Registerkarte [Suchbegriffe] oder bei Suchbegriffen ohne Klicks wird das richtige Dokument womöglich gefunden, steht aber weit unten.
Die am häufigsten angeklickten URLs auf der Registerkarte [Klicks] zeigen, welche Dokumente die Benutzer letztlich öffnen.
Die Schlüsselübereinstimmung holt ein solches Dokument bei einem bestimmten Suchbegriff nach oben.

Klicken Sie unter [Crawler] > [Schlüsselübereinstimmung] auf [Neu erstellen], geben Sie Folgendes ein und klicken Sie auf [Erstellen].

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feld
     - Beispiel
     - Beschreibung
   * - Begriff
     - ``Reisekosten``
     - Wird angewendet, wenn ein Wort der Suchbegriffe mit diesem Wert übereinstimmt (ohne Unterscheidung von Groß- und Kleinschreibung). Geben Sie ein einzelnes Wort an
   * - Abfrage
     - ``url:"https://portal.example.com/manual/expense.html"``
     - Suchabfrage, die die nach oben zu holenden Dokumente auswählt
   * - Größe
     - ``10`` (Standardwert)
     - Höchstzahl der zur Abfrage passenden Dokumente, die berücksichtigt werden
   * - Boost
     - ``100`` (Standardwert)
     - Gewicht, mit dem der Score der Zieldokumente multipliziert wird

Setzen Sie die URL in der Abfrage immer in ``"``.
Ohne Anführungszeichen wie in ``url:https://...`` scheitert das Parsen der Abfrage am ``:`` in der URL; die Schlüsselübereinstimmung wird nicht geladen und bewirkt nichts (es erscheint lediglich eine WARN-Meldung in ``fess.log``).
Das Feld ``url`` erfordert eine exakte Übereinstimmung; der Wert muss Zeichen für Zeichen mit der indexierten URL übereinstimmen.
Führen Sie vor der Registrierung dieselbe Abfrage auf der Suchseite aus und vergewissern Sie sich, dass genau das eine Zieldokument gefunden wird.

Ein Neuladen wie bei den Wörterbüchern ist nicht nötig.
Das Speichern startet im Hintergrund das erneute Laden der Schlüsselübereinstimmungen; umgeschaltet wird, sobald alle Einträge gelesen sind.
Zwischen zwei Einträgen wird beim Laden jeweils eine Sekunde gewartet; bei vielen Einträgen dauert es daher eine Weile, bis die Änderung wirkt.

Prüfen Sie das Ergebnis auf dem Detailbildschirm der registrierten Schlüsselübereinstimmung, den Sie aus der Liste öffnen.
Wird im Feld „URLs“ die URL des Zieldokuments angezeigt, ist sie wirksam.
Direkt nach dem Speichern ist das erneute Laden womöglich noch nicht abgeschlossen, sodass das Feld leer sein kann.
Ist es auch nach kurzem Warten und erneutem Öffnen des Detailbildschirms leer, passt die Abfrage auf kein Dokument.
Die zur Abfrage passenden Dokumente werden beim Speichern und nach jedem abgeschlossenen Crawl-Job neu ermittelt.
Noch nicht gecrawlte Dokumente werden daher nach dem nächsten Crawl berücksichtigt.

Beachten Sie außerdem, dass nur Dokumente berücksichtigt werden, die zum Suchbegriff passen.
Wird das Zieldokument bei einer Suche nach „Reisekosten“ gar nicht gefunden, erscheint es auch mit einer Schlüsselübereinstimmung nicht in den Ergebnissen.

Eine Website oder Dokumentgruppe insgesamt anheben: Dokument-Boost
==================================================================

Wenn Sie eine bestimmte Dokumentgruppe, etwa die Website mit den offiziellen Handbüchern, unabhängig vom Suchbegriff anheben möchten, verwenden Sie [Crawler] > [Dokument-Boost].

Klicken Sie auf [Neu erstellen] und geben Sie Folgendes ein.

- Bedingung: ``url.startsWith("https://portal.example.com/manual/")``
- Boost-Ausdruck: ``10``
- Skripttyp: ``javascript`` (beim Neuanlegen vorausgefüllt)
- Sortierreihenfolge: ``0``

Bedingung und Boost-Ausdruck werden als Skriptausdrücke ausgewertet; die Felder des Dokuments stehen als Variablen zur Verfügung.
Bei Dokumenten, für die die Bedingung ``true`` zurückgibt, wird der Wert des Boost-Ausdrucks in das Feld ``boost`` geschrieben.
Es ist dasselbe Feld wie „Boost“ in den Crawl-Konfigurationen für Web und Dateisystem (Standardwert 1.0); bei Dokumenten, die zu einer Regel passen, wird der Wert der Regel verwendet.
Passt ein Dokument zu mehreren Regeln, wird die Regel mit der kleinsten Sortierreihenfolge verwendet.
Setzen Sie in JavaScript kein Semikolon an das Ende eines Ausdrucks.
Mit Semikolon wird der Wert ``null``, und die Regel wirkt nicht.

Dokument-Boost wird anders wirksam als Schlüsselübereinstimmung und Synonyme.

- Die Regeln werden ausgewertet, wenn Dokumente beim Web- oder Datei-Crawl im Index registriert werden. Auf Dokumente aus Datenspeicher-Crawls werden sie nicht angewendet.
- Das Hinzufügen oder Ändern einer Regel ändert die Werte bereits indexierter Dokumente nicht.
- Ist unter [Allgemein] „Letzte Änderung prüfen“ aktiviert (Standard), werden Dokumente mit unverändertem Inhalt beim erneuten Crawlen nicht neu registriert. Um die Regel auf vorhandene Dokumente anzuwenden, löschen Sie die Zieldokumente unter [Systeminformationen] > [Suche] und crawlen Sie erneut.

Suchen Sie nach der Übernahme mit Wörtern, die zu dieser Dokumentgruppe passen, und prüfen Sie, ob die Position gestiegen ist; vergleichen Sie nach einiger Zeit die durchschnittliche Klickposition auf der Registerkarte [Suchbegriffe] mit dem vorherigen Zeitraum.

Andere Formulierungen vorschlagen: verwandte Abfragen
=====================================================

Wenn Sie eine Suche mit einem anderen Wort vorschlagen möchten, ohne den Suchbegriff der Benutzer zu erweitern, verwenden Sie verwandte Abfragen.
Klicken Sie unter [Crawler] > [Verwandte Abfrage] auf [Neu erstellen], geben Sie unter „Begriff“ das Wort der Benutzer ein (z. B. ``VPN``) und unter „Abfragen“ die vorgeschlagenen Wörter, eines pro Zeile (z. B. ``Fernzugriff``, ``externer Zugang``).

Im Standard-Theme (bootstrap) erscheinen bei passendem Suchbegriff über den Suchergebnissen Schaltflächen unter „Ähnliche Suchanfragen:“.
Sie werden auch auf einer Ergebnisseite mit 0 Treffern angezeigt und eignen sich daher, um Benutzer von Suchbegriffen ohne Treffer wegzuführen.
Der Begriff wird mit der gesamten eingegebenen Suchzeichenfolge verglichen (ohne Unterscheidung von Groß- und Kleinschreibung).
Die Änderung wirkt beim Speichern; ein Neuladen ist nicht nötig.

Mit [Aus Suchprotokollen generieren] auf dem Listenbildschirm lassen sich verwandte Abfragen automatisch aus Wortpaaren erzeugen, nach denen derselbe Benutzer in kurzem Abstand erneut gesucht hat.
Dazu müssen unter [Allgemein] sowohl „Suchprotokoll“ als auch „Benutzerprotokoll“ aktiviert sein.
Begriffe, für die bereits eine verwandte Abfrage existiert, werden nicht geändert.
Die Bedingungen der Erzeugung und die Einstellungen zu ihrer Anpassung finden Sie unter `Verwandte Abfragen <https://fess.codelibs.org/de/stable/admin/relatedquery-guide.html>`__.

Bevor Sie Stoppwörter einsetzen
===============================

Wenn ein Wort, das in allen Dokumenten vorkommt (zum Beispiel ein englisches Wort in der Fußzeile jeder Seite), in Suchbegriffe gerät und die Ergebnisse zu stark ausweitet, können Sie es mit Stoppwörtern aus der Analyse entfernen.
Jede Stoppwort-Wörterbuchdatei wirkt jedoch nur auf bestimmte Felder.

- ``en/stopwords.txt`` wird für die Analyse von ``content``, ``title`` und den Feldern verwendet, die auf ``_en`` enden.
- ``ja/stopwords.txt`` wird nur für die auf ``_ja`` endenden Felder wie ``content_ja`` und ``title_ja`` von Dokumenten verwendet, die als Japanisch erkannt wurden. Standardmäßig ist die Datei leer.

Am Beispiel japanischer Texte: Partikeln wie „の“ und „は“ werden in den ``_ja``-Feldern durch den Wortartfilter entfernt, in ``content`` und ``title`` jedoch nicht.
Japanischer Text in ``content`` und ``title`` wird in Einheiten von je zwei Zeichen zerlegt, und Hiragana werden vor dem Abgleich in Katakana umgewandelt („VPNとは“ wird zu ``vpn`` und ``トハ``).
Ein japanisches Wort in ``en/stopwords.txt`` wird daher nur entfernt, wenn es genau einer der durch die Zerlegung entstandenen Zwei-Zeichen-Einheiten entspricht.
Verwenden Sie Stoppwörter vor allem für englische Wörter und prüfen Sie mit der OpenSearch-API ``_analyze``, ob sie wirken.

.. code-block:: bash

    curl -X POST "localhost:9200/fess.search/_analyze" -H "Content-Type: application/json" \
      -d '{"analyzer": "standard_search_analyzer", "text": "VPNとは"}'

Stoppwörter wirken sowohl bei der Indexierung als auch bei der Suche.
Laden Sie nach dem Speichern des Wörterbuchs wie bei Synonymen den Dokumentenindex neu, und crawlen Sie erneut, um die Wörter auch aus bereits indexierten Dokumenten zu entfernen.
Wie die sprachspezifischen Felder funktionieren, erfahren Sie in :doc:`guide-09`.

Fehlerbehebung
==============

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Symptom
     - Zu prüfen
   * - Synonym registriert, aber die Ergebnisse ändern sich nicht
     - Wurde der Dokumentenindex neu geladen? Entspricht der Eintrag den Registrierungsregeln (Hiragana, Wörter aus einem Zeichen usw.)?
   * - Schlüsselübereinstimmung wirkt nicht
     - Ist das Feld „URLs“ auf dem Detailbildschirm leer? Steht die URL in der Abfrage in ``"``? Enthalten die Suchbegriffe der Benutzer genau dasselbe Wort wie der Begriff als eigenständiges Wort (getrennte Eingaben wie „Reise Kosten“ passen nicht)? Wird das Zieldokument mit diesem Wort gefunden?
   * - Dokument-Boost wirkt nicht
     - Handelt es sich um Dokumente aus einem Datenspeicher? Wurden die Dokumente nach dem Hinzufügen der Regel neu registriert? Endet die Bedingung mit einem Semikolon?
   * - Verwandte Abfragen werden nicht angezeigt
     - Stimmt der Begriff mit der gesamten Suchzeichenfolge überein? Ist ein eigenes Theme so gebaut, dass es verwandte Abfragen anzeigt?
   * - Klickkennzahlen sind leer
     - Ist unter [Allgemein] „Suchprotokoll“ aktiviert? Führen die Links der Suchergebnisse über ``/go/``? Enthält der Zeitraum nur Klicks, die vor 15.9 aufgezeichnet wurden?

Weiterführende Artikel
======================

- Suchprotokolle in OpenSearch Dashboards selbst auswerten: :doc:`guide-22`
- Suche in Dokumenten mit gemischtem japanischem, englischem und chinesischem Text verbessern: :doc:`guide-09`
- Die Ursache für fehlende Treffer waren fehlende Dokumente: :doc:`guide-04`
- Inhaltlich ähnliche Dokumente auch ohne übereinstimmende Wörter anzeigen: :doc:`guide-18`
- Wörterbuch- und Schlüsselübereinstimmungs-Einstellungen als Code verwalten: :doc:`guide-16`

Referenzen
==========

- `Suchprotokoll <https://fess.codelibs.org/de/stable/admin/searchlog-guide.html>`__
- `Wörterbuch <https://fess.codelibs.org/de/stable/admin/dict-guide.html>`__
- `Synonym-Wörterbuch <https://fess.codelibs.org/de/stable/admin/synonym-guide.html>`__
- `Stoppwort-Wörterbuch <https://fess.codelibs.org/de/stable/admin/stopwords-guide.html>`__
- `Schlüsselübereinstimmung <https://fess.codelibs.org/de/stable/admin/keymatch-guide.html>`__
- `Dokument-Boosting <https://fess.codelibs.org/de/stable/admin/boostdoc-guide.html>`__
- `Verwandte Abfragen <https://fess.codelibs.org/de/stable/admin/relatedquery-guide.html>`__
- `Wartung <https://fess.codelibs.org/de/stable/admin/maintenance-guide.html>`__
