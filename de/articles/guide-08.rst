============================================================
Teil 8: Suchqualitat pflegen -- Ein Suchtuning-Zyklus auf Basis von Nutzerverhaltendaten
============================================================

Einleitung
==========

Mit der Einfuhrung eines Suchsystems ist die Arbeit noch nicht abgeschlossen.
Sobald die Benutzer die Suche in der Praxis verwenden, kann Feedback wie "Ich finde nicht die erwarteten Ergebnisse" oder "Irrelevante Ergebnisse erscheinen ganz oben" aufkommen.

In diesem Artikel wird ein Tuning-Zyklus fuer die Suchqualitaet vorgestellt, der die Analyse von Suchprotokollen, die Identifikation von Problemen, die Umsetzung von Verbesserungen und die Messung ihrer Wirksamkeit umfasst.
Anstatt eine perfekte Suchqualitaet auf einmal zu erreichen, handelt es sich um einen Ansatz der kontinuierlichen, datenbasierten Verbesserung.

Zielgruppe
==========

- Administratoren von Suchsystemen
- Personen, die die Suchqualitaet verbessern moechten
- Personen, die Fess bereits betreiben und Feedback von Benutzern erhalten haben

Der Tuning-Zyklus fuer die Suchqualitaet
=========================================

Die Verbesserung der Suchqualitaet folgt einem Vier-Schritte-Zyklus:

1. **Analysieren**: Suchprotokolle ueberpruefen und Probleme identifizieren
2. **Verbessern**: Loesungen fuer die identifizierten Probleme umsetzen
3. **Verifizieren**: Die Wirksamkeit der Verbesserungen bestaetigen
4. **Fortsetzen**: Den Zyklus wiederholen, um die Qualitaet kontinuierlich zu steigern

Schritt 1: Analyse der Suchprotokolle
======================================

So ueberpruefen Sie die Suchprotokolle
---------------------------------------

Fess zeichnet das Suchverhalten der Benutzer automatisch auf.
Sie koennen die Suchprotokolle ueber [Systeminformationen] > [Suchprotokoll] in der Administrationsoberflaeche einsehen.

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
Die gesuchte Information existiert moeglicherweise nicht, oder die Suchbegriffe stimmen nicht angemessen ueberein.

Zum Beispiel liefert eine Suche nach "Betriebsausflug" keine Treffer, obwohl ein Dokument mit dem Titel "Mitarbeiterveranstaltung" vorhanden ist.
Dies kann durch die Konfiguration von Synonymen geloest werden.

**Haeufige Abfragen**

Haeufig gesuchte Begriffe repraesentieren wichtige Informationsbeduerfnisse der Organisation.
Ueberpruefen Sie, ob fuer diese Abfragen geeignete Ergebnisse an oberster Stelle angezeigt werden.

**Klickprotokolle**

Dies sind Aufzeichnungen darueber, welche Links in den Suchergebnissen angeklickt wurden.
Wenn die oberen Ergebnisse nicht angeklickt werden und nur weiter unten platzierte Ergebnisse angeklickt werden, besteht Verbesserungspotenzial beim Ranking.

Schritt 2: Umsetzung von Verbesserungen
========================================

Setzen Sie basierend auf den Analyseergebnissen die folgenden Verbesserungen in Kombination um.

Synonyme konfigurieren
----------------------

Registrieren Sie Synonyme, um Variationen in der Schreibweise und Abkuerzungen abzudecken.

Konfigurieren Sie diese, indem Sie das Synonymwoerterbuch unter [System] > [Woerterbuch] in der Administrationsoberflaeche auswaehlen.

Konfigurationsbeispiel:

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

Durch die Konfiguration von Synonymen werden bei der Suche nach einem Begriff auch Dokumente gefunden, die seine Synonyme enthalten.

Key Match konfigurieren
-----------------------

Diese Funktion zeigt ein bestimmtes Dokument ganz oben in den Ergebnissen fuer ein bestimmtes Schluesselwort an.

Konfigurieren Sie dies ueber [Crawler] > [Key Match] in der Administrationsoberflaeche.

Beispielsweise koennen Sie konfigurieren, dass die Seite des Reisekostenabrechnungshandbuchs ganz oben erscheint, wenn Benutzer nach "Reisekostenabrechnung" suchen.

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

Konfigurieren Sie dies ueber [Crawler] > [Document Boost] in der Administrationsoberflaeche.

Beispielsweise koennen folgende Boost-Strategien in Betracht gezogen werden:

- Den Score offizieller Handbuecher (Portal-Seite) erhoehen
- Dokumente mit neuerem Aenderungsdatum priorisieren
- Den Score von Dokumenten mit einem bestimmten Label (offizielle Dokumente) erhoehen

Verwandte Abfragen konfigurieren
---------------------------------

Diese Funktion schlaegt verwandte Schluesselwoerter auf der Suchergebnisseite vor.
Sie hilft Benutzern, ihre Suche zu verfeinern oder aus einem anderen Blickwinkel zu suchen.

Konfigurieren Sie dies ueber [Crawler] > [Verwandte Abfrage] in der Administrationsoberflaeche.

Konfigurationsbeispiel:

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Stoppwoerter konfigurieren
----------------------------

Konfigurieren Sie Woerter, die bei der Suche ignoriert werden sollen.
Gaengige Partikel wie "no", "wa" und "wo" werden standardmaessig verarbeitet, aber Sie koennen branchenspezifische Stoerwoerter bei Bedarf hinzufuegen.

Konfigurieren Sie diese, indem Sie das Stoppwoerterwoerterbuch unter [System] > [Woerterbuch] in der Administrationsoberflaeche auswaehlen.

Schritt 3: Ueberpruefung der Wirksamkeit
==========================================

Ueberpruefen Sie nach der Umsetzung von Verbesserungen deren Wirksamkeit.

Ueberpruefungsmethoden
-----------------------

**Veraenderung der Null-Treffer-Rate**

Ueberpruefen Sie, wie sich der Anteil der Null-Treffer-Abfragen vor und nach der Verbesserung veraendert hat.
Wenn die Null-Treffer-Rate nach dem Hinzufuegen von Synonymen oder der Konfiguration von Key Matches gesunken ist, koennen Sie daraus schliessen, dass die Verbesserung wirksam war.

**Veraenderung der Klickposition**

Ueberpruefen Sie die Verteilung, an welcher Position in den Suchergebnissen geklickt wird.
Wenn der Anteil der Klicks auf die oberen Ergebnisse zugenommen hat, koennen Sie daraus schliessen, dass sich das Ranking verbessert hat.

**Ueberpruefung beliebter Suchbegriffe**

Ueberpruefen Sie die auf der Suchseite angezeigten beliebten Suchbegriffe und die aus den Suchprotokollen aggregierten haeufig gesuchten Schluesselwoerter.
Es ist ebenfalls effektiv, manuell zu ueberpruefen, ob bei der Suche nach beliebten Begriffen geeignete Ergebnisse zurueckgegeben werden.

Schritt 4: Kontinuierliche Verbesserung
========================================

Das Tuning der Suchqualitaet ist keine einmalige Angelegenheit.

Etablierung eines Betriebszyklus
---------------------------------

Wir empfehlen die Etablierung eines Betriebszyklus wie dem folgenden.

.. list-table:: Tuning-Zyklus-Beispiel
   :header-rows: 1
   :widths: 25 35 40

   * - Haeufigkeit
     - Aktion
     - Details
   * - Woechentlich
     - Null-Treffer-Abfragen pruefen
     - Pruefen, ob neue Null-Treffer-Abfragen vorliegen, und diese mit Synonymen oder Key Matches beheben
   * - Monatlich
     - Gesamtanalyse der Suchprotokolle
     - Trends bei haeufigen Abfragen, Klickraten und Null-Treffer-Raten ueberpruefen
   * - Vierteljaehrlich
     - Umfassende Ueberpruefung
     - Eine umfassende Bewertung der Suchqualitaet durchfuehren und einen Verbesserungsplan erstellen

Feedback von Benutzern
-----------------------

Neben der Protokollanalyse ist auch das Feedback der tatsaechlichen Benutzer ein wichtiger Input fuer Verbesserungen.
Richten Sie einen Mechanismus ein, um Feedback wie "Mit diesem Suchbegriff konnte ich nichts finden" oder "Dieses Ergebnis war hilfreich" zu sammeln.

Zusammenfassung
===============

In diesem Artikel wurde ein Tuning-Zyklus zur kontinuierlichen Verbesserung der Suchqualitaet vorgestellt.

- Analyse der Suchprotokolle (Null-Treffer, haeufige Abfragen, Klickprotokolle)
- Verbesserungen durch Synonyme, Key Match, Document Boost und verwandte Abfragen
- Methoden zur Ueberpruefung der Verbesserungswirksamkeit
- Etablierung eines kontinuierlichen Betriebszyklus

Lassen Sie uns die Suchqualitaet durch datenbasierte Verbesserung pflegen -- von "Suche, die genutzt wird" zu "Suche, die nuetzt."

Im naechsten Artikel wird der Aufbau einer Suchinfrastruktur in mehrsprachigen Umgebungen behandelt.

Referenzen
==========

- `Fess Suchprotokoll <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Woerterbuchverwaltung <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
