================================
Teil 18: Grundlagen der KI-Suche
================================

Einführung
============

In den bisherigen Artikeln haben wir uns auf die schlüsselwortbasierte Volltextsuche konzentriert.
Die Volltextsuche ist sehr effektiv, wenn Benutzer geeignete Schlüsselwörter eingeben können.
Es gibt jedoch Fälle, in denen die Schlüsselwortsuche allein nicht ausreicht, etwa wenn Benutzer nicht wissen, nach welchen Schlüsselwörtern sie suchen sollen, oder wenn sie Antworten auf konzeptuelle Fragen benötigen.

In diesem Artikel ordnen wir das Spektrum der Suchtechnologien ein und erläutern, wie sich die Suche von der Schlüsselwortsuche zur semantischen Suche weiterentwickelt.

Zielgruppe
==========

- Personen, die sich für KI-Suche interessieren und die Konzepte strukturieren möchten
- Personen, die die Einführung einer semantischen Suche in Betracht ziehen
- Personen, die die KI-bezogenen Funktionen von Fess verstehen möchten

Spektrum der Suchtechnologien
==============================

Suchtechnologien bilden ein Spektrum von einfach bis fortgeschritten, wie im Folgenden dargestellt.

.. list-table:: Spektrum der Suchtechnologien
   :header-rows: 1
   :widths: 20 35 45

   * - Technologie
     - Mechanismus
     - Merkmale
   * - Schlüsselwortsuche
     - Abgleich der Eingabebegriffe mit Begriffen in Dokumenten
     - Schnell und zuverlässig. Erfordert Übereinstimmung der Begriffe
   * - Fuzzy-Suche
     - Abgleich auch bei ähnlicher Schreibweise
     - Behandlung von Tippfehlern
   * - Synonymsuche
     - Erweiterung um Synonyme für den Abgleich
     - Behandlung von Schreibvarianten (manuelle Konfiguration)
   * - Semantische Suche
     - Abgleich basierend auf semantischer Ähnlichkeit
     - Findet verwandte Dokumente auch ohne Begriffsübereinstimmung
   * - Hybridsuche
     - Kombination aus Schlüsselwort- und semantischer Suche
     - Nutzt die Stärken beider Ansätze

Grenzen der Schlüsselwortsuche
================================

Die Schlüsselwortsuche ist in vielen Situationen wirksam, stößt jedoch in den folgenden Fällen an ihre Grenzen.

Vokabular-Diskrepanz
----------------------

Dies tritt auf, wenn die von Benutzern verwendeten Wörter von den in Dokumenten verwendeten Wörtern abweichen.

Beispiel: Selbst wenn ein Benutzer nach "Ich möchte das Zielkonto für meine Gehaltsüberweisung ändern" sucht, stimmen die Schlüsselwörter möglicherweise nicht überein, wenn im internen Dokument der Begriff "Verfahren zur Änderung des Gehaltskontos" verwendet wird.

Dies kann teilweise mit Synonymen (siehe Teil 8) adressiert werden, aber es ist nicht praktikabel, alle möglichen Vokabularkombinationen im Voraus zu registrieren.

Konzeptuelle Suche
-------------------

Dies ist der Fall, wenn Benutzer nach Konzepten statt nach bestimmten Schlüsselwörtern suchen möchten, zum Beispiel "Interne Regeln zur Fernarbeit."
In diesem Fall können verschiedene verwandte Dokumente relevant sein, darunter solche über "Homeoffice", "Telearbeit", "Anwesenheitsregeln" und "Arbeitszeiterfassung".

Funktionsweise der semantischen Suche
=======================================

Vektordarstellung (Embedding)
-------------------------------

Die Grundlage der semantischen Suche ist die Umwandlung von Text in "Vektoren (Arrays von Zahlen)."
Diese Vektoren sind mathematische Darstellungen der "Bedeutung" des Textes.

Texte mit ähnlicher Bedeutung werden im Vektorraum nahe beieinander platziert.
Zum Beispiel liegen die Vektoren für "Hund" und "Haustier" nahe beieinander, während die Vektoren für "Hund" und "Automobil" weit voneinander entfernt sind.

Funktionsweise der Suche
--------------------------

1. Der Benutzer gibt eine Suchanfrage ein
2. Die Anfrage wird in einen Vektor umgewandelt
3. Die Ähnlichkeit mit den Dokumentvektoren im Index wird berechnet
4. Dokumente werden in der Reihenfolge der höchsten Ähnlichkeit zurückgegeben

Dadurch können semantisch verwandte Dokumente gefunden werden, auch wenn die Schlüsselwörter nicht exakt übereinstimmen.

Semantische Suche in Fess
===========================

Fess kann durch Plugins für semantische Suche eine vektorbasierte Suche realisieren.

Aktivierung der semantischen Suche
------------------------------------

1. Installieren Sie das Plugin für semantische Suche
2. Konfigurieren Sie das Embedding-Modell
3. Erstellen Sie den Index neu (Vektorisierung bestehender Dokumente)

Auswahl des Embedding-Modells
-------------------------------

Wählen Sie ein Modell (Embedding-Modell) für die Umwandlung von Text in Vektoren.

Die wesentlichen Auswahlkriterien sind:

- **Sprachunterstützung**: Ob die Zielsprache angemessen verarbeitet werden kann
- **Genauigkeit**: Qualität der Vektoren (Genauigkeit der semantischen Erfassung)
- **Geschwindigkeit**: Für die Umwandlung benötigte Zeit
- **Kosten**: API-Nutzungsgebühren, Hardwareanforderungen

Hybridsuche: Rank Fusion
===========================

Die semantische Suche ist leistungsfähig, aber nicht allmächtig.
Für die Suche nach Eigennamen oder in Fällen, in denen eine exakte Übereinstimmung erforderlich ist, ist die Schlüsselwortsuche besser geeignet.

Das Konzept der Hybridsuche
------------------------------

Die Hybridsuche führt sowohl eine Schlüsselwortsuche als auch eine semantische Suche durch und integriert anschließend die Ergebnisse.

Fess verwendet Rank Fusion, um Ergebnisse verschiedener Suchmethoden zusammenzuführen.
Konkret sorgt der RRF-Algorithmus (Reciprocal Rank Fusion) dafür, dass Dokumente, die in beiden Suchergebnissen hoch eingestuft werden, letztendlich an der Spitze stehen.

Vorteile der Hybridsuche
--------------------------

- Vereint die "Zuverlässigkeit" der Schlüsselwortsuche mit der "Flexibilität" der semantischen Suche
- Eigennamen werden durch die Schlüsselwortsuche abgedeckt
- Konzeptuelle Suchen werden durch die semantische Suche abgedeckt
- Die Gesamtqualität der Suche verbessert sich im Vergleich zur alleinigen Verwendung einer der beiden Methoden

Kriterien für die Einführung
================================

Die semantische Suche sollte nicht unbedingt in jeder Umgebung eingeführt werden.

Fälle, in denen eine Einführung in Betracht gezogen werden sollte
----------------------------------------------------------------------

- Es gibt viele "Null-Treffer-Anfragen" in den Suchprotokollen
- Benutzer berichten, dass sie "die richtigen Schlüsselwörter nicht kennen"
- Sie möchten natürlichsprachliche Fragen unterstützen (Voraussetzung für RAG in Teil 19)
- Sie möchten die sprachübergreifende Suche für mehrsprachige Dokumente verbessern

Fälle, in denen sie noch nicht erforderlich ist
---------------------------------------------------

- Mit Schlüsselwortsuche und Synonymen wird bereits eine ausreichende Suchqualität erzielt
- Die Anzahl der Dokumente ist gering und die Benutzer kennen die passenden Schlüsselwörter
- Rechenressourcen (GPU oder Cloud-API-Kosten) sind begrenzt

Schrittweise Einführung
--------------------------

1. Verbessern Sie zunächst die Qualität mit Schlüsselwortsuche und Synonymen (Teil 8)
2. Wenn weiterhin viele Null-Treffer-Anfragen auftreten, ziehen Sie die semantische Suche in Betracht
3. Nutzen Sie die Hybridsuche, um von beiden Ansätzen zu profitieren

Zusammenfassung
================

In diesem Artikel haben wir den Entwicklungspfad von der Schlüsselwortsuche zur semantischen Suche dargestellt.

- Das Spektrum der Suchtechnologien (Schlüsselwort -> Fuzzy -> Synonym -> Semantisch -> Hybrid)
- Funktionsweise der semantischen Suche (Vektordarstellung und Ähnlichkeitsberechnung)
- Semantische Suche und Hybridsuche in Fess (Rank Fusion)
- Kriterien für die Einführung und ein schrittweiser Ansatz

Im nächsten Artikel werden wir die semantische Suche weiterentwickeln und einen KI-Assistenten mit RAG aufbauen.

Referenzen
==========

- `Fess KI-Suchfunktionen <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `OpenSearch Vektorsuche <https://opensearch.org/docs/latest/search-plugins/knn/>`__
