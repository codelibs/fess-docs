============================================================
Teil 1 Warum Unternehmen eine Suchinfrastruktur brauchen -- Herausforderungen der Wissensnutzung im Zeitalter der Informationsflut
============================================================

Einleitung
==========

"Wo war diese Datei noch gleich?"

Mit dieser Frage sehen sich viele Berufstaetige taeglich konfrontiert.
Dateiserver im Unternehmen, Cloud-Speicher, Chat-Tools, Wikis, Ticketmanagementsysteme -- die Informationsmenge waechst taeglich und ist ueber zahlreiche Orte verstreut.
Man weiss, dass die benoetigte Information vorhanden ist, doch es dauert Minuten, manchmal sogar Dutzende von Minuten, bis man sie gefunden hat.
Diese "Zeit fuer die Informationssuche" ist eine der grossen Herausforderungen, mit denen Unternehmen heute konfrontiert sind.

In dieser Artikelserie "Strategien zur Wissensnutzung mit Fess" erlaeutern wir praxisnah, wie Sie diese Herausforderung mit dem Open-Source-Volltextsuchserver Fess loesen koennen.
In diesem ersten Teil klaeren wir zunaechst, warum Unternehmen eine Suchinfrastruktur benoetigen, und stellen vor, welche Rolle Fess als Software einnimmt.

Zielgruppe
==========

- Personen, die Herausforderungen bei der unternehmensinternen Informationsnutzung sehen
- Personen, die die Einfuehrung einer Enterprise-Search-Loesung in Erwaegung ziehen
- Personen, die Fess zum ersten Mal kennenlernen

Herausforderungen im Zeitalter der Informationsflut
=====================================================

Informationsexplosion und das Problem des "Nicht-Findens"
----------------------------------------------------------

Die Menge an digitalen Daten in Unternehmen nimmt von Jahr zu Jahr zu.
Berichte, Protokolle, technische Dokumentationen, E-Mails, Chat-Protokolle, Quellcode, Kundendaten -- all diese Informationen bilden das Wissen einer Organisation.
Doch je mehr Informationen vorhanden sind, desto schwieriger wird es, die benoetigten Informationen zu finden.

Zahlreiche Studien zeigen, dass Wissensarbeiter 20 bis 30 Prozent ihrer Arbeitszeit mit der Informationssuche verbringen.
In einer Organisation mit 50 Mitarbeitenden bedeutet das, dass taeglich die Arbeitsleistung von 10 bis 15 Personen fuer das "Suchen" aufgewendet wird.

Informationssilos als strukturelles Problem
--------------------------------------------

Der Grund dafuer, dass Informationen nicht gefunden werden, liegt nicht allein in der grossen Menge.
In vielen Unternehmen bilden sich "Informationssilos", in denen Informationen nach Abteilungen oder Tools voneinander getrennt sind.

- Das Vertriebsteam nutzt Salesforce und gemeinsame Ordner
- Das Entwicklungsteam nutzt Confluence und Git-Repositories
- Die Verwaltung nutzt das Unternehmensportal und Dateiserver

Jedes dieser Tools verfuegt ueber eine eigene Suchfunktion, aber es gibt keine Moeglichkeit, tooluebergreifend zu suchen.
Das fuehrt dazu, dass Dokumente, die ein anderes Team erstellt hat, nicht gefunden werden und aehnliche Unterlagen von Grund auf neu erstellt werden -- ein alltaegliches Phaenomen.

Loesung durch eine Suchinfrastruktur
--------------------------------------

Die Loesung fuer diese Herausforderungen ist eine "Enterprise Search (unternehmensweite Suchinfrastruktur)".
Enterprise Search bietet die Moeglichkeit, verschiedene Datenquellen innerhalb einer Organisation uebergreifend zu durchsuchen.

Durch die Einfuehrung von Enterprise Search koennen folgende Vorteile erzielt werden:

- **Verkuerzung der Suchzeit**: Verstreute Informationen ueber eine zentrale Anlaufstelle durchsuchen
- **Foerderung der Wissenswiederverwendung**: Fruehere Arbeitsergebnisse und Erkenntnisse lassen sich leichter auffinden
- **Schnellere Entscheidungsfindung**: Schneller Zugriff auf benoetigte Informationen fuer fundierte Entscheidungen
- **Abbau von Wissensmonopolen**: Den Zustand "Das weiss nur diese eine Person" reduzieren

Was ist Fess?
==============

Fess ist ein Open-Source-Volltextsuchserver.
Er wird unter der Apache-Lizenz bereitgestellt und kann einschliesslich kommerzieller Nutzung kostenlos verwendet werden.
Fess ist Java-basiert entwickelt und nutzt OpenSearch als Suchmaschine.

Gesamtueberblick ueber Fess
-----------------------------

Fess ist nicht nur eine Suchmaschine, sondern bietet saemtliche Funktionen, die fuer ein vollstaendiges "Suchsystem" erforderlich sind.

**Crawler**

Der Crawler sammelt automatisch Dokumente aus verschiedenen Datenquellen wie Websites, Dateiservern, Cloud-Speichern und SaaS-Anwendungen.
Er unterstuetzt ueber 100 Dateiformate, darunter HTML, PDF, Word, Excel und PowerPoint.

**Suchmaschine**

Mit OpenSearch als Backend bietet Fess eine leistungsstarke Volltextsuche.
Er unterstuetzt ueber 20 Sprachen, einschliesslich Japanisch, und skaliert auch bei grossen Dokumentenmengen.

**Such-UI**

Eine browserbasierte Suchoberflaeche ist standardmaessig enthalten.
Hervorhebung von Suchergebnissen, Facetten (Filterung), Vorschlaege (Autovervollstaendigung) und weitere Funktionen sorgen fuer ein benutzerfreundliches Sucherlebnis.

**Administrationsoberflaeche**

Crawling-Einstellungen, Benutzerverwaltung, Woerterbuchverwaltung und weitere fuer den Betrieb notwendige Konfigurationen koennen ueber den Browser vorgenommen werden.
Auch ohne Kenntnisse der Kommandozeile laesst sich das Suchsystem ueber die Administrationsoberflaeche betreiben.

**API**

Fess stellt eine JSON-basierte Such-API bereit, mit der sich Suchfunktionen in bestehende Systeme integrieren lassen.

Warum Fess waehlen?
--------------------

Fuer Enterprise Search gibt es verschiedene Optionen.
Sie koennen OpenSearch oder Elasticsearch direkt verwenden oder auf kommerzielle Suchloesungen zurueckgreifen.
Im Folgenden werden die Gruende fuer die Wahl von Fess zusammengefasst.

**Vergleich mit Eigenentwicklung**

OpenSearch und Elasticsearch sind leistungsstarke Suchmaschinen, aber allein damit ist noch kein vollstaendiges Suchsystem aufgebaut.
Ein Crawler, die Verarbeitung von Dokumenten, die Entwicklung einer Such-UI, ein Berechtigungssystem und vieles mehr muessen eigenstaendig implementiert werden.
Fess bietet all dies als All-in-One-Loesung und reduziert den Entwicklungsaufwand fuer den Aufbau eines Suchsystems erheblich.

**Vergleich mit kommerziellen Produkten**

Kommerzielle Enterprise-Search-Produkte sind funktionsreich, aber die Lizenzkosten koennen erheblich sein.
Da Fess Open Source ist, fallen keine Softwarekosten an.
Zudem ist der Quellcode oeffentlich zugaenglich, sodass kein Risiko eines Vendor-Lock-in besteht.
Bei Bedarf an Anpassungen koennen Sie Fess frei erweitern.

**Erweiterbarkeit durch Plugins**

Fess basiert auf einer Plugin-Architektur.
Es stehen Plugins fuer verschiedene Datenquellen bereit, darunter Slack, SharePoint, Box, Dropbox, Confluence und Jira.
Darueber hinaus sind Erweiterungen fuer das KI-Zeitalter moeglich, beispielsweise LLM-Plugins zur Anbindung an grosse Sprachmodelle (LLM).

Suchszenarien mit Fess
========================

Welche konkreten Suchumgebungen lassen sich mit Fess aufbauen?
Im Folgenden geben wir einen Ueberblick ueber die Szenarien, die in dieser Artikelserie behandelt werden.

Uebergreifende Suche in Unternehmensdokumenten
------------------------------------------------

Dateiserver, Cloud-Speicher, Websites und weitere Datenquellen lassen sich von einem zentralen Punkt aus durchsuchen.
Selbst wenn verschiedene Abteilungen unterschiedliche Tools nutzen, koennen Benutzer ueber ein einziges Suchfeld die benoetigten Informationen finden.

Abteilungsbezogene Zugriffskontrolle
--------------------------------------

Die in den Suchergebnissen angezeigten Dokumente koennen basierend auf der Zugehoerigkeit und den Berechtigungen der Benutzer gesteuert werden.
Vertrauliche Dokumente der Personalabteilung werden nicht in den Suchergebnissen des Vertriebsteams angezeigt.
Durch die Integration mit bestehenden Verzeichnisdiensten (Active Directory, LDAP) koennen Berechtigungsinformationen automatisch uebernommen werden.

Suchfunktion in bestehende Systeme integrieren
-------------------------------------------------

Die Suchfunktion von Fess kann in Unternehmensportale und Geschaeftsanwendungen eingebettet werden.
Sie koennen zwischen verschiedenen Ansaetzen waehlen: der einfachen Einbindung per JavaScript ueber Fess Site Search (FSS) oder einer individuellen Integration ueber die API.

KI-gestuetzte Sucherfahrung
-----------------------------

Die derzeit viel beachtete RAG-Technologie (Retrieval-Augmented Generation) laesst sich mit Fess umsetzen.
Wenn Benutzer eine Frage in natuerlicher Sprache stellen, durchsucht Fess die Unternehmensdokumente nach relevanten Informationen und ein LLM generiert die Antwort.
Als "unternehmensinterner KI-Assistent" laesst sich die Wissensnutzung so auf ein neues Niveau heben.

Aufbau der Artikelserie
========================

Diese Artikelserie umfasst insgesamt 23 Teile.
Sie ist so konzipiert, dass sowohl Einsteiger als auch fortgeschrittene Anwender ihr Verstaendnis schrittweise vertiefen koennen.

**Grundlagen (Teil 1 bis 5)**

In den ersten fuenf Teilen, einschliesslich dieses Artikels, werden die Einfuehrung von Fess und grundlegende Szenarien behandelt.
Sie lernen den Schnellstart mit Docker Compose, das Hinzufuegen einer Suchfunktion zu Websites, den Aufbau einer Multiquellen-Suche und die berechtigungsbasierte Suchsteuerung.

**Praxisloesungen (Teil 6 bis 12)**

Aufbau eines Wissenshubs fuer Entwicklungsteams, uebergreifende Suche in Cloud-Speichern, Optimierung der Suchqualitaet, Mehrsprachigkeit, Betriebsmanagement, API-Integration und weitere praxisnahe Inhalte basierend auf realen Geschaeftsszenarien.

**Architektur und Skalierung (Teil 13 bis 17)**

Mandantenfaehiges Design, Skalierung fuer grosse Umgebungen, Sicherheitsarchitektur, DevOps-orientierte Betriebsautomatisierung, Plugin-Entwicklung und weitere fortgeschrittene Architekturthemen.

**KI und Suche der naechsten Generation (Teil 18 bis 22)**

Von den Grundlagen der semantischen Suche ueber den Aufbau eines KI-Assistenten mit RAG, die Nutzung als MCP-Server, multimodale Suche bis hin zu Suchanalysen -- die neuesten Suchtechnologien werden behandelt.

**Zusammenfassung (Teil 23)**

Die Erkenntnisse der gesamten Serie werden zusammengefasst und eine Referenzarchitektur fuer eine wissensbasierte Plattform mit Fess als Kernkomponente wird vorgestellt.

Fazit
=====

In diesem Artikel haben wir die Notwendigkeit einer Suchinfrastruktur in Unternehmen und die Positionierung von Fess vorgestellt.

- Informationsflut und Informationssilos sind Herausforderungen, die viele Unternehmen gemeinsam haben
- Mit Enterprise Search lassen sich verstreute Informationen uebergreifend durchsuchen
- Fess ist Open Source und bietet saemtliche Funktionen, die fuer ein Suchsystem erforderlich sind
- Erweiterung durch Plugins und KI-Integration werden unterstuetzt

Im naechsten Teil zeigen wir, wie Sie Fess mit Docker Compose starten und die Sucherfahrung schnellstmoeglich ausprobieren koennen.

Referenzen
==========

- `Fess <https://fess.codelibs.org/ja/>`__

- `OpenSearch <https://opensearch.org/>`__

- `GitHub - codelibs/fess <https://github.com/codelibs/fess>`__
