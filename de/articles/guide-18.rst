============================================================
Teil 18: Grundlagen der KI-Suche -- Entwicklung von der Schluesselwortsuche zur semantischen Suche
============================================================

Einfuehrung
============

In den bisherigen Artikeln haben wir uns auf die schluesselwortbasierte Volltextsuche konzentriert.
Die Volltextsuche ist sehr effektiv, wenn Benutzer geeignete Schluesselwoerter eingeben koennen.
Es gibt jedoch Faelle, in denen die Schluesselwortsuche allein nicht ausreicht, etwa wenn Benutzer nicht wissen, nach welchen Schluesselwoertern sie suchen sollen, oder wenn sie Antworten auf konzeptuelle Fragen benoetigen.

In diesem Artikel ordnen wir das Spektrum der Suchtechnologien ein und erlaeutern, wie sich die Suche von der Schluesselwortsuche zur semantischen Suche weiterentwickelt.

Zielgruppe
==========

- Personen, die sich fuer KI-Suche interessieren und die Konzepte strukturieren moechten
- Personen, die die Einfuehrung einer semantischen Suche in Betracht ziehen
- Personen, die die KI-bezogenen Funktionen von Fess verstehen moechten

Spektrum der Suchtechnologien
==============================

Suchtechnologien bilden ein Spektrum von einfach bis fortgeschritten, wie im Folgenden dargestellt.

.. list-table:: Spektrum der Suchtechnologien
   :header-rows: 1
   :widths: 20 35 45

   * - Technologie
     - Mechanismus
     - Merkmale
   * - Schluesselwortsuche
     - Abgleich der Eingabebegriffe mit Begriffen in Dokumenten
     - Schnell und zuverlaessig. Erfordert Uebereinstimmung der Begriffe
   * - Fuzzy-Suche
     - Abgleich auch bei aehnlicher Schreibweise
     - Behandlung von Tippfehlern
   * - Synonymsuche
     - Erweiterung um Synonyme fuer den Abgleich
     - Behandlung von Schreibvarianten (manuelle Konfiguration)
   * - Semantische Suche
     - Abgleich basierend auf semantischer Aehnlichkeit
     - Findet verwandte Dokumente auch ohne Begriffsuebereinstimmung
   * - Hybridsuche
     - Kombination aus Schluesselwort- und semantischer Suche
     - Nutzt die Staerken beider Ansaetze

Grenzen der Schluesselwortsuche
================================

Die Schluesselwortsuche ist in vielen Situationen wirksam, stoesst jedoch in den folgenden Faellen an ihre Grenzen.

Vokabular-Diskrepanz
----------------------

Dies tritt auf, wenn die von Benutzern verwendeten Woerter von den in Dokumenten verwendeten Woertern abweichen.

Beispiel: Selbst wenn ein Benutzer nach "Ich moechte das Zielkonto fuer meine Gehaltsueberweisung aendern" sucht, stimmen die Schluesselwoerter moeglicherweise nicht ueberein, wenn im internen Dokument der Begriff "Verfahren zur Aenderung des Gehaltskontos" verwendet wird.

Dies kann teilweise mit Synonymen (siehe Teil 8) adressiert werden, aber es ist nicht praktikabel, alle moeglichen Vokabularkombinationen im Voraus zu registrieren.

Konzeptuelle Suche
-------------------

Dies ist der Fall, wenn Benutzer nach Konzepten statt nach bestimmten Schluesselwoertern suchen moechten, zum Beispiel "Interne Regeln zur Fernarbeit."
In diesem Fall koennen verschiedene verwandte Dokumente relevant sein, darunter solche ueber "Homeoffice", "Telearbeit", "Anwesenheitsregeln" und "Arbeitszeiterfassung".

Funktionsweise der semantischen Suche
=======================================

Vektordarstellung (Embedding)
-------------------------------

Die Grundlage der semantischen Suche ist die Umwandlung von Text in "Vektoren (Arrays von Zahlen)."
Diese Vektoren sind mathematische Darstellungen der "Bedeutung" des Textes.

Texte mit aehnlicher Bedeutung werden im Vektorraum nahe beieinander platziert.
Zum Beispiel liegen die Vektoren fuer "Hund" und "Haustier" nahe beieinander, waehrend die Vektoren fuer "Hund" und "Automobil" weit voneinander entfernt sind.

Funktionsweise der Suche
--------------------------

1. Der Benutzer gibt eine Suchanfrage ein
2. Die Anfrage wird in einen Vektor umgewandelt
3. Die Aehnlichkeit mit den Dokumentvektoren im Index wird berechnet
4. Dokumente werden in der Reihenfolge der hoechsten Aehnlichkeit zurueckgegeben

Dadurch koennen semantisch verwandte Dokumente gefunden werden, auch wenn die Schluesselwoerter nicht exakt uebereinstimmen.

Semantische Suche in Fess
===========================

Fess kann durch Plugins fuer semantische Suche eine vektorbasierte Suche realisieren.

Aktivierung der semantischen Suche
------------------------------------

1. Installieren Sie das Plugin fuer semantische Suche
2. Konfigurieren Sie das Embedding-Modell
3. Erstellen Sie den Index neu (Vektorisierung bestehender Dokumente)

Auswahl des Embedding-Modells
-------------------------------

Waehlen Sie ein Modell (Embedding-Modell) fuer die Umwandlung von Text in Vektoren.

Die wesentlichen Auswahlkriterien sind:

- **Sprachunterstuetzung**: Ob die Zielsprache angemessen verarbeitet werden kann
- **Genauigkeit**: Qualitaet der Vektoren (Genauigkeit der semantischen Erfassung)
- **Geschwindigkeit**: Fuer die Umwandlung benoetigte Zeit
- **Kosten**: API-Nutzungsgebuehren, Hardwareanforderungen

Hybridsuche: Rank Fusion
===========================

Die semantische Suche ist leistungsfaehig, aber nicht allmaechtig.
Fuer die Suche nach Eigennamen oder in Faellen, in denen eine exakte Uebereinstimmung erforderlich ist, ist die Schluesselwortsuche besser geeignet.

Das Konzept der Hybridsuche
------------------------------

Die Hybridsuche fuehrt sowohl eine Schluesselwortsuche als auch eine semantische Suche durch und integriert anschliessend die Ergebnisse.

Fess verwendet Rank Fusion, um Ergebnisse verschiedener Suchmethoden zusammenzufuehren.
Konkret sorgt der RRF-Algorithmus (Reciprocal Rank Fusion) dafuer, dass Dokumente, die in beiden Suchergebnissen hoch eingestuft werden, letztendlich an der Spitze stehen.

Vorteile der Hybridsuche
--------------------------

- Vereint die "Zuverlaessigkeit" der Schluesselwortsuche mit der "Flexibilitaet" der semantischen Suche
- Eigennamen werden durch die Schluesselwortsuche abgedeckt
- Konzeptuelle Suchen werden durch die semantische Suche abgedeckt
- Die Gesamtqualitaet der Suche verbessert sich im Vergleich zur alleinigen Verwendung einer der beiden Methoden

Kriterien fuer die Einfuehrung
================================

Die semantische Suche sollte nicht unbedingt in jeder Umgebung eingefuehrt werden.

Faelle, in denen eine Einfuehrung in Betracht gezogen werden sollte
----------------------------------------------------------------------

- Es gibt viele "Null-Treffer-Anfragen" in den Suchprotokollen
- Benutzer berichten, dass sie "die richtigen Schluesselwoerter nicht kennen"
- Sie moechten natuerlichsprachliche Fragen unterstuetzen (Voraussetzung fuer RAG in Teil 19)
- Sie moechten die sprachuebergreifende Suche fuer mehrsprachige Dokumente verbessern

Faelle, in denen sie noch nicht erforderlich ist
---------------------------------------------------

- Mit Schluesselwortsuche und Synonymen wird bereits eine ausreichende Suchqualitaet erzielt
- Die Anzahl der Dokumente ist gering und die Benutzer kennen die passenden Schluesselwoerter
- Rechenressourcen (GPU oder Cloud-API-Kosten) sind begrenzt

Schrittweise Einfuehrung
--------------------------

1. Verbessern Sie zunaechst die Qualitaet mit Schluesselwortsuche und Synonymen (Teil 8)
2. Wenn weiterhin viele Null-Treffer-Anfragen auftreten, ziehen Sie die semantische Suche in Betracht
3. Nutzen Sie die Hybridsuche, um von beiden Ansaetzen zu profitieren

Zusammenfassung
================

In diesem Artikel haben wir den Entwicklungspfad von der Schluesselwortsuche zur semantischen Suche dargestellt.

- Das Spektrum der Suchtechnologien (Schluesselwort -> Fuzzy -> Synonym -> Semantisch -> Hybrid)
- Funktionsweise der semantischen Suche (Vektordarstellung und Aehnlichkeitsberechnung)
- Semantische Suche und Hybridsuche in Fess (Rank Fusion)
- Kriterien fuer die Einfuehrung und ein schrittweiser Ansatz

Im naechsten Artikel werden wir die semantische Suche weiterentwickeln und einen KI-Assistenten mit RAG aufbauen.

Referenzen
==========

- `Fess KI-Suchfunktionen <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `OpenSearch Vektorsuche <https://opensearch.org/docs/latest/search-plugins/knn/>`__
