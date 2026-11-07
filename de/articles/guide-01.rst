========================================================
Teil 1 Warum Unternehmen eine Suchinfrastruktur brauchen
========================================================

Einleitung
==========

"Wo war diese Datei noch gleich?"

Mit dieser Frage sehen sich viele Berufstätige täglich konfrontiert.
Dateiserver im Unternehmen, Cloud-Speicher, Chat-Tools, Wikis, Ticketmanagementsysteme -- die Informationsmenge wächst täglich und ist über zahlreiche Orte verstreut.
Man weiß, dass die benötigte Information vorhanden ist, doch es dauert Minuten, manchmal sogar Dutzende von Minuten, bis man sie gefunden hat.
Diese "Zeit für die Informationssuche" ist eine der großen Herausforderungen, mit denen Unternehmen heute konfrontiert sind.

In dieser Artikelserie "Strategien zur Wissensnutzung mit Fess" erläutern wir praxisnah, wie Sie diese Herausforderung mit dem Open-Source-Volltextsuchserver Fess lösen können.
In diesem ersten Teil klären wir zunächst, warum Unternehmen eine Suchinfrastruktur benötigen, und stellen vor, welche Rolle Fess als Software einnimmt.

Zielgruppe
==========

- Personen, die Herausforderungen bei der unternehmensinternen Informationsnutzung sehen
- Personen, die die Einführung einer Enterprise-Search-Lösung in Erwägung ziehen
- Personen, die Fess zum ersten Mal kennenlernen

Herausforderungen im Zeitalter der Informationsflut
=====================================================

Informationsexplosion und das Problem des "Nicht-Findens"
----------------------------------------------------------

Die Menge an digitalen Daten in Unternehmen nimmt von Jahr zu Jahr zu.
Berichte, Protokolle, technische Dokumentationen, E-Mails, Chat-Protokolle, Quellcode, Kundendaten -- all diese Informationen bilden das Wissen einer Organisation.
Doch je mehr Informationen vorhanden sind, desto schwieriger wird es, die benötigten Informationen zu finden.

Zahlreiche Studien zeigen, dass Wissensarbeiter 20 bis 30 Prozent ihrer Arbeitszeit mit der Informationssuche verbringen.
In einer Organisation mit 50 Mitarbeitenden bedeutet das, dass täglich die Arbeitsleistung von 10 bis 15 Personen für das "Suchen" aufgewendet wird.

Informationssilos als strukturelles Problem
--------------------------------------------

Der Grund dafür, dass Informationen nicht gefunden werden, liegt nicht allein in der großen Menge.
In vielen Unternehmen bilden sich "Informationssilos", in denen Informationen nach Abteilungen oder Tools voneinander getrennt sind.

- Das Vertriebsteam nutzt Salesforce und gemeinsame Ordner
- Das Entwicklungsteam nutzt Confluence und Git-Repositories
- Die Verwaltung nutzt das Unternehmensportal und Dateiserver

Jedes dieser Tools verfügt über eine eigene Suchfunktion, aber es gibt keine Möglichkeit, toolübergreifend zu suchen.
Das führt dazu, dass Dokumente, die ein anderes Team erstellt hat, nicht gefunden werden und ähnliche Unterlagen von Grund auf neu erstellt werden -- ein alltägliches Phänomen.

Lösung durch eine Suchinfrastruktur
--------------------------------------

Die Lösung für diese Herausforderungen ist eine "Enterprise Search (unternehmensweite Suchinfrastruktur)".
Enterprise Search bietet die Möglichkeit, verschiedene Datenquellen innerhalb einer Organisation übergreifend zu durchsuchen.

Durch die Einführung von Enterprise Search können folgende Vorteile erzielt werden:

- **Verkürzung der Suchzeit**: Verstreute Informationen über eine zentrale Anlaufstelle durchsuchen
- **Förderung der Wissenswiederverwendung**: Frühere Arbeitsergebnisse und Erkenntnisse lassen sich leichter auffinden
- **Schnellere Entscheidungsfindung**: Schneller Zugriff auf benötigte Informationen für fundierte Entscheidungen
- **Abbau von Wissensmonopolen**: Den Zustand "Das weiß nur diese eine Person" reduzieren

Was ist Fess?
==============

Fess ist ein Open-Source-Volltextsuchserver.
Er wird unter der Apache-Lizenz bereitgestellt und kann einschließlich kommerzieller Nutzung kostenlos verwendet werden.
Fess ist Java-basiert entwickelt und nutzt OpenSearch als Suchmaschine.

Gesamtüberblick über Fess
-----------------------------

Fess ist nicht nur eine Suchmaschine, sondern bietet sämtliche Funktionen, die für ein vollständiges "Suchsystem" erforderlich sind.

**Crawler**

Der Crawler sammelt automatisch Dokumente aus verschiedenen Datenquellen wie Websites, Dateiservern, Cloud-Speichern und SaaS-Anwendungen.
Er unterstützt über 100 Dateiformate, darunter HTML, PDF, Word, Excel und PowerPoint.

**Suchmaschine**

Mit OpenSearch als Backend bietet Fess eine leistungsstarke Volltextsuche.
Er unterstützt über 20 Sprachen, einschließlich Japanisch, und skaliert auch bei großen Dokumentenmengen.

**Such-UI**

Eine browserbasierte Suchoberfläche ist standardmäßig enthalten.
Hervorhebung von Suchergebnissen, Facetten (Filterung), Vorschläge (Autovervollständigung) und weitere Funktionen sorgen für ein benutzerfreundliches Sucherlebnis.

**Administrationsoberfläche**

Crawling-Einstellungen, Benutzerverwaltung, Wörterbuchverwaltung und weitere für den Betrieb notwendige Konfigurationen können über den Browser vorgenommen werden.
Auch ohne Kenntnisse der Kommandozeile lässt sich das Suchsystem über die Administrationsoberfläche betreiben.

**API**

Fess stellt eine JSON-basierte Such-API bereit, mit der sich Suchfunktionen in bestehende Systeme integrieren lassen.

Warum Fess wählen?
--------------------

Für Enterprise Search gibt es verschiedene Optionen.
Sie können OpenSearch oder Elasticsearch direkt verwenden oder auf kommerzielle Suchlösungen zurückgreifen.
Im Folgenden werden die Gründe für die Wahl von Fess zusammengefasst.

**Vergleich mit Eigenentwicklung**

OpenSearch und Elasticsearch sind leistungsstarke Suchmaschinen, aber allein damit ist noch kein vollständiges Suchsystem aufgebaut.
Ein Crawler, die Verarbeitung von Dokumenten, die Entwicklung einer Such-UI, ein Berechtigungssystem und vieles mehr müssen eigenständig implementiert werden.
Fess bietet all dies als All-in-One-Lösung und reduziert den Entwicklungsaufwand für den Aufbau eines Suchsystems erheblich.

**Vergleich mit kommerziellen Produkten**

Kommerzielle Enterprise-Search-Produkte sind funktionsreich, aber die Lizenzkosten können erheblich sein.
Da Fess Open Source ist, fallen keine Softwarekosten an.
Zudem ist der Quellcode öffentlich zugänglich, sodass kein Risiko eines Vendor-Lock-in besteht.
Bei Bedarf an Anpassungen können Sie Fess frei erweitern.

**Erweiterbarkeit durch Plugins**

Fess basiert auf einer Plugin-Architektur.
Es stehen Plugins für verschiedene Datenquellen bereit, darunter Slack, SharePoint, Box, Dropbox, Confluence und Jira.
Darüber hinaus sind Erweiterungen für das KI-Zeitalter möglich, beispielsweise LLM-Plugins zur Anbindung an große Sprachmodelle (LLM).

Suchszenarien mit Fess
========================

Welche konkreten Suchumgebungen lassen sich mit Fess aufbauen?
Im Folgenden geben wir einen Überblick über die Szenarien, die in dieser Artikelserie behandelt werden.

Übergreifende Suche in Unternehmensdokumenten
------------------------------------------------

Dateiserver, Cloud-Speicher, Websites und weitere Datenquellen lassen sich von einem zentralen Punkt aus durchsuchen.
Selbst wenn verschiedene Abteilungen unterschiedliche Tools nutzen, können Benutzer über ein einziges Suchfeld die benötigten Informationen finden.

Abteilungsbezogene Zugriffskontrolle
--------------------------------------

Die in den Suchergebnissen angezeigten Dokumente können basierend auf der Zugehörigkeit und den Berechtigungen der Benutzer gesteuert werden.
Vertrauliche Dokumente der Personalabteilung werden nicht in den Suchergebnissen des Vertriebsteams angezeigt.
Durch die Integration mit bestehenden Verzeichnisdiensten (Active Directory, LDAP) können Berechtigungsinformationen automatisch übernommen werden.

Suchfunktion in bestehende Systeme integrieren
-------------------------------------------------

Die Suchfunktion von Fess kann in Unternehmensportale und Geschäftsanwendungen eingebettet werden.
Sie können zwischen verschiedenen Ansätzen wählen: der einfachen Einbindung per JavaScript über Fess Site Search (FSS) oder einer individuellen Integration über die API.

KI-gestützte Sucherfahrung
-----------------------------

Die derzeit viel beachtete RAG-Technologie (Retrieval-Augmented Generation) lässt sich mit Fess umsetzen.
Wenn Benutzer eine Frage in natürlicher Sprache stellen, durchsucht Fess die Unternehmensdokumente nach relevanten Informationen und ein LLM generiert die Antwort.
Als "unternehmensinterner KI-Assistent" lässt sich die Wissensnutzung so auf ein neues Niveau heben.

Aufbau der Artikelserie
========================

Diese Artikelserie umfasst insgesamt 23 Teile.
Sie ist so konzipiert, dass sowohl Einsteiger als auch fortgeschrittene Anwender ihr Verständnis schrittweise vertiefen können.

**Grundlagen (Teil 1 bis 5)**

In den ersten fünf Teilen, einschließlich dieses Artikels, werden die Einführung von Fess und grundlegende Szenarien behandelt.
Sie lernen den Schnellstart mit Docker Compose, das Hinzufügen einer Suchfunktion zu Websites, den Aufbau einer Multiquellen-Suche und die berechtigungsbasierte Suchsteuerung.

**Praxislösungen (Teil 6 bis 12)**

Aufbau eines Wissenshubs für Entwicklungsteams, übergreifende Suche in Cloud-Speichern, Optimierung der Suchqualität, Mehrsprachigkeit, Betriebsmanagement, API-Integration und weitere praxisnahe Inhalte basierend auf realen Geschäftsszenarien.

**Architektur und Skalierung (Teil 13 bis 17)**

Mandantenfähiges Design, Skalierung für große Umgebungen, Sicherheitsarchitektur, DevOps-orientierte Betriebsautomatisierung, Plugin-Entwicklung und weitere fortgeschrittene Architekturthemen.

**KI und Suche der nächsten Generation (Teil 18 bis 22)**

Von den Grundlagen der semantischen Suche über den Aufbau eines KI-Assistenten mit RAG, die Nutzung als MCP-Server, multimodale Suche bis hin zu Suchanalysen -- die neuesten Suchtechnologien werden behandelt.

**Zusammenfassung (Teil 23)**

Die Erkenntnisse der gesamten Serie werden zusammengefasst und eine Referenzarchitektur für eine wissensbasierte Plattform mit Fess als Kernkomponente wird vorgestellt.

Fazit
=====

In diesem Artikel haben wir die Notwendigkeit einer Suchinfrastruktur in Unternehmen und die Positionierung von Fess vorgestellt.

- Informationsflut und Informationssilos sind Herausforderungen, die viele Unternehmen gemeinsam haben
- Mit Enterprise Search lassen sich verstreute Informationen übergreifend durchsuchen
- Fess ist Open Source und bietet sämtliche Funktionen, die für ein Suchsystem erforderlich sind
- Erweiterung durch Plugins und KI-Integration werden unterstützt

Im nächsten Teil zeigen wir, wie Sie Fess mit Docker Compose starten und die Sucherfahrung schnellstmöglich ausprobieren können.

Referenzen
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `OpenSearch <https://opensearch.org/>`__

- `GitHub - codelibs/fess <https://github.com/codelibs/fess>`__
