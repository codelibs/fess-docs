====================================
Open-Source-Volltextsuche-Server - |Fess| Entwicklerhandbuch
====================================

Dieses Handbuch bietet Informationen, die für die Mitarbeit an der Entwicklung von |Fess| erforderlich sind.
Es richtet sich an ein breites Publikum, von Personen, die zum ersten Mal an der Entwicklung von |Fess| arbeiten, bis hin zu erfahrenen Entwicklern.

.. contents:: Inhaltsverzeichnis
   :local:
   :depth: 2

Zielgruppe
========

Dieses Handbuch richtet sich an folgende Personen:

- Entwickler, die zur Hinzufügung oder Verbesserung von |Fess|-Funktionen beitragen möchten
- Techniker, die den |Fess|-Code verstehen möchten
- Personen, die |Fess| anpassen und verwenden möchten
- Personen, die an der Beteiligung an Open-Source-Projekten interessiert sind

Erforderliche Vorkenntnisse
============

Für die Mitarbeit an der Entwicklung von |Fess| sind folgende Kenntnisse hilfreich:

**Erforderlich**

- Grundkenntnisse in Java-Programmierung (Java 21 oder höher)
- Grundkenntnisse in Git und GitHub
- Grundkenntnisse in Maven

**Empfohlen**

- Kenntnisse des LastaFlute-Frameworks
- Kenntnisse von DBFlute
- Kenntnisse von OpenSearch/Elasticsearch
- Erfahrung in der Webanwendungsentwicklung

Aufbau des Entwicklerhandbuchs
==============

Dieses Handbuch besteht aus den folgenden Abschnitten.

:doc:`getting-started`
    Erläutert einen Überblick über die |Fess|-Entwicklung und die ersten Schritte zum Einstieg in die Entwicklung.
    Sie können den für die Entwicklung erforderlichen Technologie-Stack und einen Überblick über das Projekt verstehen.

:doc:`setup`
    Erklärt die Schritte zum Einrichten der Entwicklungsumgebung im Detail.
    Von der Installation der erforderlichen Tools wie Java, IDE und OpenSearch
    bis zum Abrufen und Ausführen des |Fess|-Quellcodes werden Schritt für Schritt erklärt.

:doc:`architecture`
    Erklärt die Architektur und Codestruktur von |Fess|.
    Durch das Verständnis der wichtigsten Pakete, Module und Entwurfsmuster
    können Sie effizient entwickeln.

:doc:`workflow`
    Erklärt den Standard-Workflow für die |Fess|-Entwicklung.
    Sie können den Ablauf von Entwicklungsarbeiten wie Funktionserweiterungen, Fehlerbehebungen, Code-Reviews und Tests lernen.

:doc:`building`
    Erklärt, wie |Fess| gebaut und getestet wird.
    Die Verwendung von Build-Tools, das Ausführen von Unit-Tests,
    und die Erstellung von Verteilungspaketen werden erläutert.

:doc:`contributing`
    Erklärt, wie Sie zum |Fess|-Projekt beitragen können.
    Sie können das Erstellen von Pull Requests, Codierungskonventionen
    und Kommunikation mit der Community lernen.

Schnellstart
==============

Wenn Sie sofort mit der |Fess|-Entwicklung beginnen möchten, folgen Sie diesen Schritten:

1. **Überprüfung der Systemanforderungen**

   Für die Entwicklung sind folgende Tools erforderlich:

   - Java 21 oder höher
   - Maven 3.x oder höher
   - Git
   - IDE (Eclipse, IntelliJ IDEA usw.)

2. **Abrufen des Quellcodes**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

3. **Herunterladen der OpenSearch-Plugins**

   .. code-block:: bash

       mvn antrun:run

4. **Ausführen**

   Führen Sie ``org.codelibs.fess.FessBoot`` von der IDE aus
   oder führen Sie es von Maven aus:

   .. code-block:: bash

       mvn compile exec:java

Weitere Informationen finden Sie unter :doc:`setup`.

Optionen für die Entwicklungsumgebung
==============

Die Entwicklung von |Fess| kann in einer der folgenden Umgebungen durchgeführt werden:

Lokale Entwicklungsumgebung
--------------

Dies ist die gängigste Entwicklungsumgebung. Sie installieren Entwicklungstools auf Ihrem Computer und
entwickeln mit einer IDE.

**Vorteile:**

- Schnelles Bauen und Ausführen
- Volle Nutzung der IDE-Funktionen
- Offline-Arbeit möglich

**Nachteile:**

- Zeitaufwändige Ersteinrichtung
- Mögliche Probleme aufgrund von Umgebungsunterschieden

Docker-basierte Entwicklungsumgebung
------------------------

Sie können eine konsistente Entwicklungsumgebung mit Docker-Containern aufbauen.

**Vorteile:**

- Konsistenz der Umgebung gewährleistet
- Einfaches Setup
- Leicht in einen sauberen Zustand zurückzusetzen

**Nachteile:**

- Docker-Kenntnisse erforderlich
- Leistung kann manchmal etwas niedriger sein

Weitere Informationen finden Sie unter :doc:`setup`.

Häufig gestellte Fragen
==========

F: Was sind die Mindestspezifikationen für die Entwicklung?
--------------------------------

A: Wir empfehlen Folgendes:

- CPU: 4 Kerne oder mehr
- Speicher: 8 GB oder mehr
- Festplatte: 20 GB oder mehr freier Speicherplatz

F: Welche IDE sollte ich verwenden?
---------------------------------

A: Sie können jede IDE Ihrer Wahl verwenden, wie Eclipse, IntelliJ IDEA oder VS Code.
Obwohl dieses Handbuch hauptsächlich Eclipse als Beispiel verwendet,
können Sie auch mit anderen IDEs entwickeln.

F: Sind Kenntnisse in LastaFlute oder DBFlute erforderlich?
------------------------------------------

A: Nicht erforderlich, aber hilfreich für einen reibungslosen Entwicklungsablauf.
Die grundlegende Verwendung wird auch in diesem Handbuch erklärt,
Details finden Sie jedoch in der offiziellen Dokumentation der jeweiligen Frameworks.

F: Wo sollte ich mit meinem ersten Beitrag beginnen?
------------------------------------------------------

A: Wir empfehlen, mit relativ einfachen Aufgaben zu beginnen, wie z. B.:

- Verbesserung der Dokumentation
- Hinzufügen von Tests
- Fehlerbehebungen
- Kleine Verbesserungen bestehender Funktionen

Weitere Informationen finden Sie unter :doc:`contributing`.

Verwandte Ressourcen
==========

Offizielle Ressourcen
----------

- `Offizielle Fess-Website <https://fess.codelibs.org/ja/>`__
- `GitHub-Repository <https://github.com/codelibs/fess>`__
- `Issue-Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__

Technische Dokumentation
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

Community
----------

- `Fess-Community-Forum <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__

Nächste Schritte
==========

Um mit der Entwicklung zu beginnen, empfehlen wir, mit :doc:`getting-started` zu beginnen.

.. toctree::
   :maxdepth: 2
   :caption: Inhaltsverzeichnis:

   getting-started
   setup
   architecture
   workflow
   building
   contributing
