============================
Teil 8: Suchqualitat pflegen
============================

Einleitung
==========

Mit der Einfuhrung eines Suchsystems ist die Arbeit noch nicht abgeschlossen.
Sobald die Benutzer die Suche in der Praxis verwenden, kann Feedback wie "Ich finde nicht die erwarteten Ergebnisse" oder "Irrelevante Ergebnisse erscheinen ganz oben" aufkommen.

In diesem Artikel wird ein Tuning-Zyklus für die Suchqualität vorgestellt, der die Analyse von Suchprotokollen, die Identifikation von Problemen, die Umsetzung von Verbesserungen und die Messung ihrer Wirksamkeit umfasst.
Anstatt eine perfekte Suchqualität auf einmal zu erreichen, handelt es sich um einen Ansatz der kontinuierlichen, datenbasierten Verbesserung.

Zielgruppe
==========

- Administratoren von Suchsystemen
- Personen, die die Suchqualität verbessern möchten
- Personen, die Fess bereits betreiben und Feedback von Benutzern erhalten haben

Der Tuning-Zyklus für die Suchqualität
=========================================

Die Verbesserung der Suchqualität folgt einem Vier-Schritte-Zyklus:

1. **Analysieren**: Suchprotokolle überprüfen und Probleme identifizieren
2. **Verbessern**: Lösungen für die identifizierten Probleme umsetzen
3. **Verifizieren**: Die Wirksamkeit der Verbesserungen bestätigen
4. **Fortsetzen**: Den Zyklus wiederholen, um die Qualität kontinuierlich zu steigern

Schritt 1: Analyse der Suchprotokolle
======================================

So überprüfen Sie die Suchprotokolle
---------------------------------------

Fess zeichnet das Suchverhalten der Benutzer automatisch auf.
Sie können die Suchprotokolle über [Systeminformationen] > [Suchprotokoll] in der Administrationsoberfläche einsehen.

Die Suchprotokolle enthalten die folgenden Informationen:

- Suchbegriffe
- Datum und Uhrzeit der Suche
- Anzahl der Suchergebnisse
- User Agent

Muster, auf die Sie achten sollten
-----------------------------------

Bei der Analyse der Suchprotokolle gibt es bestimmte Muster, auf die Sie besonders achten sollten.

**Null-Treffer-Abfragen**

Dies sind Abfragen, die keine Ergebnisse liefern.
Die gesuchte Information existiert möglicherweise nicht, oder die Suchbegriffe stimmen nicht angemessen überein.

Zum Beispiel liefert eine Suche nach "Betriebsausflug" keine Treffer, obwohl ein Dokument mit dem Titel "Mitarbeiterveranstaltung" vorhanden ist.
Dies kann durch die Konfiguration von Synonymen gelöst werden.

**Häufige Abfragen**

Häufig gesuchte Begriffe repräsentieren wichtige Informationsbedürfnisse der Organisation.
Überprüfen Sie, ob für diese Abfragen geeignete Ergebnisse an oberster Stelle angezeigt werden.

**Klickprotokolle**

Dies sind Aufzeichnungen darüber, welche Links in den Suchergebnissen angeklickt wurden.
Wenn die oberen Ergebnisse nicht angeklickt werden und nur weiter unten platzierte Ergebnisse angeklickt werden, besteht Verbesserungspotenzial beim Ranking.

Schritt 2: Umsetzung von Verbesserungen
========================================

Setzen Sie basierend auf den Analyseergebnissen die folgenden Verbesserungen in Kombination um.

Synonyme konfigurieren
----------------------

Registrieren Sie Synonyme, um Variationen in der Schreibweise und Abkürzungen abzudecken.

Konfigurieren Sie diese, indem Sie das Synonymwörterbuch unter [System] > [Wörterbuch] in der Administrationsoberfläche auswählen.

Konfigurationsbeispiel:

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

Durch die Konfiguration von Synonymen werden bei der Suche nach einem Begriff auch Dokumente gefunden, die seine Synonyme enthalten.

Key Match konfigurieren
-----------------------

Diese Funktion zeigt ein bestimmtes Dokument ganz oben in den Ergebnissen für ein bestimmtes Schlüsselwort an.

Konfigurieren Sie dies über [Crawler] > [Key Match] in der Administrationsoberfläche.

Beispielsweise können Sie konfigurieren, dass die Seite des Reisekostenabrechnungshandbuchs ganz oben erscheint, wenn Benutzer nach "Reisekostenabrechnung" suchen.

.. list-table:: Key-Match-Konfigurationsbeispiel
   :header-rows: 1
   :widths: 30 50 20

   * - Suchbegriff
     - Abfrage
     - Boost-Wert
   * - 経費精算
     - url:https://portal/manual/expense.html
     - 100
   * - 有給申請
     - url:https://portal/manual/paid-leave.html
     - 100
   * - VPN接続
     - url:https://portal/manual/vpn-setup.html
     - 100

Document Boost konfigurieren
-----------------------------

Hiermit wird der Gesamtscore von Dokumenten angepasst, die bestimmten Bedingungen entsprechen.

Konfigurieren Sie dies über [Crawler] > [Document Boost] in der Administrationsoberfläche.

Beispielsweise können folgende Boost-Strategien in Betracht gezogen werden:

- Den Score offizieller Handbücher (Portal-Seite) erhöhen
- Dokumente mit neuerem Änderungsdatum priorisieren
- Den Score von Dokumenten mit einem bestimmten Label (offizielle Dokumente) erhöhen

Verwandte Abfragen konfigurieren
---------------------------------

Diese Funktion schlägt verwandte Schlüsselwörter auf der Suchergebnisseite vor.
Sie hilft Benutzern, ihre Suche zu verfeinern oder aus einem anderen Blickwinkel zu suchen.

Konfigurieren Sie dies über [Crawler] > [Verwandte Abfrage] in der Administrationsoberfläche.

Konfigurationsbeispiel:

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Stoppwörter konfigurieren
----------------------------

Konfigurieren Sie Wörter, die bei der Suche ignoriert werden sollen.
Gängige Partikel wie "no", "wa" und "wo" werden standardmäßig verarbeitet, aber Sie können branchenspezifische Störwörter bei Bedarf hinzufügen.

Konfigurieren Sie diese, indem Sie das Stoppwörterbuch unter [System] > [Wörterbuch] in der Administrationsoberfläche auswählen.

Schritt 3: Überprüfung der Wirksamkeit
==========================================

Überprüfen Sie nach der Umsetzung von Verbesserungen deren Wirksamkeit.

Überprüfungsmethoden
-----------------------

**Veränderung der Null-Treffer-Rate**

Überprüfen Sie, wie sich der Anteil der Null-Treffer-Abfragen vor und nach der Verbesserung verändert hat.
Wenn die Null-Treffer-Rate nach dem Hinzufügen von Synonymen oder der Konfiguration von Key Matches gesunken ist, können Sie daraus schließen, dass die Verbesserung wirksam war.

**Veränderung der Klickposition**

Überprüfen Sie die Verteilung, an welcher Position in den Suchergebnissen geklickt wird.
Wenn der Anteil der Klicks auf die oberen Ergebnisse zugenommen hat, können Sie daraus schließen, dass sich das Ranking verbessert hat.

**Überprüfung beliebter Suchbegriffe**

Überprüfen Sie die auf der Suchseite angezeigten beliebten Suchbegriffe und die aus den Suchprotokollen aggregierten häufig gesuchten Schlüsselwörter.
Es ist ebenfalls effektiv, manuell zu überprüfen, ob bei der Suche nach beliebten Begriffen geeignete Ergebnisse zurückgegeben werden.

Schritt 4: Kontinuierliche Verbesserung
========================================

Das Tuning der Suchqualität ist keine einmalige Angelegenheit.

Etablierung eines Betriebszyklus
---------------------------------

Wir empfehlen die Etablierung eines Betriebszyklus wie dem folgenden.

.. list-table:: Tuning-Zyklus-Beispiel
   :header-rows: 1
   :widths: 25 35 40

   * - Häufigkeit
     - Aktion
     - Details
   * - Wöchentlich
     - Null-Treffer-Abfragen prüfen
     - Prüfen, ob neue Null-Treffer-Abfragen vorliegen, und diese mit Synonymen oder Key Matches beheben
   * - Monatlich
     - Gesamtanalyse der Suchprotokolle
     - Trends bei häufigen Abfragen, Klickraten und Null-Treffer-Raten überprüfen
   * - Vierteljährlich
     - Umfassende Überprüfung
     - Eine umfassende Bewertung der Suchqualität durchführen und einen Verbesserungsplan erstellen

Feedback von Benutzern
-----------------------

Neben der Protokollanalyse ist auch das Feedback der tatsächlichen Benutzer ein wichtiger Input für Verbesserungen.
Richten Sie einen Mechanismus ein, um Feedback wie "Mit diesem Suchbegriff konnte ich nichts finden" oder "Dieses Ergebnis war hilfreich" zu sammeln.

Zusammenfassung
===============

In diesem Artikel wurde ein Tuning-Zyklus zur kontinuierlichen Verbesserung der Suchqualität vorgestellt.

- Analyse der Suchprotokolle (Null-Treffer, häufige Abfragen, Klickprotokolle)
- Verbesserungen durch Synonyme, Key Match, Document Boost und verwandte Abfragen
- Methoden zur Überprüfung der Verbesserungswirksamkeit
- Etablierung eines kontinuierlichen Betriebszyklus

Lassen Sie uns die Suchqualität durch datenbasierte Verbesserung pflegen -- von "Suche, die genutzt wird" zu "Suche, die nützt."

Im nächsten Artikel wird der Aufbau einer Suchinfrastruktur in mehrsprachigen Umgebungen behandelt.

Referenzen
==========

- `Fess Suchprotokoll <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Wörterbuchverwaltung <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
