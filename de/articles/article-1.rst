===============================================
Fess Enterprise-Suchumgebung erstellen ~ Einführung
===============================================

Einleitung
========

Die Anzahl der zu verwaltenden Dokumente wächst täglich, und es wird erwartet, dass diese Dokumente effizient verwaltet und als Wissensressource genutzt werden.
Je mehr Dokumente verwaltet werden müssen, desto schwieriger wird es, bestimmte Informationen darin zu finden.
Eine Lösung für dieses Problem ist die Einführung eines Volltextsuchservers, mit dem große Informationsmengen durchsucht werden können.

Fess ist ein Java-basierter Open-Source-Volltextsuchserver, der einfach einzurichten ist.
Fess nutzt Elasticsearch als Suchmaschine.
Elasticsearch ist eine Lucene-basierte, skalierbare und flexible Hochleistungssuchmaschine.
Andererseits müssen Sie beim Aufbau eines Volltextsuchsystems mit Elasticsearch verschiedene Funktionen wie den Crawler-Teil selbst implementieren.
Fess verwendet Fess Crawler als Crawler-Teil und kann verschiedene Arten von Dokumenten im Web und in Dateisystemen sammeln, um sie als Suchziele zu verwenden.

In diesem Artikel stellen wir den Aufbau eines Suchservers mit Fess vor.

Zielgruppe
========

-  Personen, die ein Enterprise-Suchsystem aufbauen möchten

-  Personen, die bestehenden Systemen Suchfunktionen hinzufügen möchten

- Personen, die eine interne Suche implementieren möchten, um eine wissensbasierte Umgebung zu schaffen

-  Personen, die sich für Suchsoftware wie Lucene oder Elasticsearch interessieren

Erforderliche Umgebung
==========

Der Inhalt dieses Artikels wurde in folgender Umgebung getestet:

-  Ubuntu 22.04

-  OpenJDK 21

Was ist Fess
=========

Fess ist ein Open-Source-Volltextsuchsystem für Web und Dateisysteme.
Es wird vom CodeLibs-Projekt auf GitHub unter Apache-Lizenz von der `Fess-Website <https://fess.codelibs.org/ja/>`__ bereitgestellt.

Funktionen von Fess
-----------

Java-basiertes Suchsystem
~~~~~~~~~~~~~~~~~~~~~~~~~

Fess wurde unter Verwendung verschiedener Open-Source-Produkte aufgebaut.

Das Distributionspaket wird als ausführbare Anwendung bereitgestellt.
Fess bietet Suchoberflächen und Administrationsoberflächen.
Fess verwendet LastaFlute als Web-Framework.
Wenn Sie die Oberflächen anpassen müssen, können Sie dies daher einfach durch Ändern der JSP tun.
Konfigurationsdaten und Crawl-Daten werden in OpenSearch gespeichert, und der Zugriff auf diese Daten erfolgt über den O/R-Mapper DBFlute.

Da Fess als Java-basiertes System aufgebaut ist, kann es auf allen Plattformen ausgeführt werden, auf denen Java läuft.
Es verfügt über eine Benutzeroberfläche, mit der verschiedene Einstellungen einfach über einen Webbrowser vorgenommen werden können.

OpenSearch als Suchmaschine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch ist eine von AWS bereitgestellte Open-Source-Such- und Analysemaschine, die auf Lucene basiert.
Zu den Funktionen gehören Echtzeitsuche, Hervorhebung von Suchergebnissen und Aggregationsfunktionen.
Die Anzahl der Dokumente, die durchsucht werden können, kann je nach OpenSearch-Serverkonfiguration mehrere hundert Millionen betragen, wodurch die Suchmaschine auf große Websites skaliert werden kann.
Es gibt viele Implementierungen auch in Japan und ist eine der bemerkenswerten Suchmaschinen.

Fess verwendet OpenSearch als Suchmaschine.
Die Docker-Version von Fess enthält OpenSearch, kann aber auch auf einem separaten Server bereitgestellt werden.
Darüber hinaus können sowohl Fess als auch OpenSearch in redundanten Konfigurationen eingerichtet werden, was eine hochgradig erweiterbare Architektur ermöglicht.

Fess Crawler als Crawl-Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fess Crawler ist ein vom CodeLibs-Projekt bereitgestelltes Crawler-Framework.
Fess Crawler kann Dokumente im Web und in Dateisystemen durchsuchen und sammeln.
Die Dokumentensammlung kann auch mehrere Dokumente gleichzeitig mit mehreren Threads effizient verarbeiten.
Unterstützte Dokumente umfassen nicht nur HTML, sondern auch MS Office-Dateien wie Word und Excel, Archivdateien wie Zip sowie Bild- und Audiodateien (bei Bild- und Audiodateien werden Metainformationen abgerufen).

Fess verwendet Fess Crawler, um Dokumente im Web und in Dateisystemen zu durchsuchen und Textinformationen zu sammeln.
Unterstützte Dateiformate sind alle, die Fess Crawler verarbeiten kann.
Parameter zur Ausführung von Crawls mit Fess Crawler können über die Fess-Administrationsoberfläche konfiguriert werden.

Installation und Start
==================

Hier erklären wir die Schritte zum Starten von Fess und Durchführen einer Suche.
Die Erklärung basiert auf Ubuntu 22.04, aber Installation und Start sind unter macOS und Windows nahezu identisch.

Download und Installation
--------------------------

Fess-Download
^^^^^^^^^^^^^^^^^^^

Laden Sie das neueste Paket von https://github.com/codelibs/fess/releases herunter.
Zum Zeitpunkt des Verfassens dieses Artikels (November 2025) ist die neueste Version 15.3.0.
Nach Abschluss des Downloads entpacken Sie es in ein beliebiges Verzeichnis.

Fess-Download
|image1|

OpenSearch-Download
^^^^^^^^^^^^^^^^^^^^^^^^^

Laden Sie von der `OpenSearch-Download-Seite <https://opensearch.org/downloads.html>`__ herunter.
Auf der Fess-Download-Seite finden Sie die entsprechende OpenSearch-Version für jede Version. Überprüfen Sie daher die Version, bevor Sie sie herunterladen.
Die Version, die Fess 15.3.0 entspricht, ist 3.3.0, laden Sie daher diese Version herunter.
Nach Abschluss des Downloads entpacken Sie es in ein beliebiges Verzeichnis.

Konfiguration
----

Bevor Sie starten, konfigurieren Sie Fess für die Verbindung zum OpenSearch-Cluster.
Informationen zur Konfiguration von ZIP/TAR.GZ-Paketen finden Sie auf der Installationsseite unter `Installationsmethode <https://fess.codelibs.org/ja/15.3/install/install.html>`__.
Wenn Sie RPM/DEB-Pakete verwenden, lesen Sie ebenfalls die gleiche Installationsseite.

Start
----

Der Start ist einfach. Führen Sie die folgenden Befehle in den entpackten Verzeichnissen opensearch-<version> und fess-<version> aus.
Starten Sie in der Reihenfolge OpenSearch → Fess.

OpenSearch starten
::

    $ ./bin/opensearch

Fess starten
::

    $ ./bin/fess

Greifen Sie mit einem Browser auf http://localhost:8080/ zu. Wenn eine Seite wie folgt angezeigt wird, ist der Start erfolgreich.

Such-Startseite
|image2|

Stopp
----

Um den Fess-Server zu stoppen, beenden Sie den Fess-Prozess (kill).
Stoppen Sie in der Reihenfolge Fess → OpenSearch.

Verzeichnisstruktur
----------------

Die Verzeichnisstruktur ist wie folgt:

Fess-Verzeichnisstruktur
::

    fess-15.3.0
    ├── LICENSE
    ├── README.md
    ├── app
    │   ├── META-INF
    │   ├── WEB-INF
    │   │   ├── cachedirs
    │   │   ├── classes
    │   │   ├── conf
    │   │   ├── env
    │   │   ├── fe.tld
    │   │   ├── lib
    │   │   ├── logs
    │   │   ├── orig
    │   │   ├── plugin
    │   │   ├── project.properties
    │   │   ├── site
    │   │   ├── thumbnails
    │   │   ├── view
    │   ├── css
    │   │   ├── admin
    │   │   ├── fonts
    │   │   └── style.css
    │   ├── favicon.ico
    │   ├── images
    │   └── js
    ├── bin
    ├── extension
    ├── lib
    ├── logs
    └── temp


Fess basiert auf TomcatBoot, das von LastaFlute bereitgestellt wird.
Die Anwendungsdateien von Fess befinden sich im app-Verzeichnis.
Die JSP-Dateien für die Suchoberfläche können auch über die Administrationsoberfläche bearbeitet werden und sind unter app/WEB-INF/view gespeichert.
Die Dateien js, css und images direkt unter dem app-Verzeichnis werden für die Suchoberfläche verwendet.

OpenSearch-Verzeichnisstruktur
::

    opensearch-3.3.0
    ├── LICENSE.txt
    ├── NOTICE.txt
    ├── README.md
    ├── bin
    ├── config
    │   ├── opensearch.yml
    │   ├── jvm.options
    │   ├── jvm.options.d
    │   ├── log4j2.properties
    │   └── ...
    ├── data
    ├── lib
    ├── logs
    ├── modules
    └── plugins

Indexdaten werden im data-Verzeichnis gespeichert.

Von der Indexerstellung bis zur Suche
==============================

Direkt nach dem Start wurde kein Suchindex erstellt, sodass bei einer Suche keine Ergebnisse zurückgegeben werden.
Daher muss zunächst ein Index erstellt werden. Hier erklären wir als Beispiel, wie Sie einen Index für https://fess.codelibs.org/ja/ erstellen und eine Suche durchführen.

Anmeldung auf der Administrationsseite
----------------------

Greifen Sie zunächst auf die Administrationsseite http://localhost:8080/admin zu und melden Sie sich an.
Standardmäßig sind sowohl Benutzername als auch Passwort admin.

Anmeldung auf der Administrationsseite
|image3|

Registrierung von Crawl-Zielen
------------------

Als nächstes registrieren Sie die Crawl-Ziele. Da wir diesmal Webseiten durchsuchen, wählen Sie [Web] auf der linken Seite der Administrationsseite.
Im Ausgangszustand ist nichts registriert, wählen Sie daher [Neu erstellen].

[Neu erstellen] auswählen
|image4|

Als Web-Crawl-Konfiguration crawlen wir diesmal die Seiten unter https://fess.codelibs.org/ja/ mit 2 Threads in 10-Sekunden-Intervallen (etwa 2 Seiten in 10 Sekunden) und durchsuchen etwa 100 Seiten.
Die Konfigurationseinträge sind URL: \https://fess.codelibs.org/ja/, URLs zum Crawlen: \https://fess.codelibs.org/ja/.*, Maximale Zugriffe: 100, Threads: 2, Intervall: 10000 Millisekunden. Der Rest ist Standard.

Web-Crawl-Konfiguration
|image5|

Durch Klicken auf [Erstellen] können Sie das Crawl-Ziel registrieren.
Der registrierte Inhalt kann durch Klicken auf jede Konfiguration geändert werden.

Abgeschlossene Registrierung der Web-Crawl-Konfiguration
|image6|

Crawl starten
------------------

Als nächstes wählen Sie System > Scheduler > Default Crawler und klicken Sie auf [Jetzt starten].

Scheduler auswählen
|image7|

Ob der Crawl gestartet wurde und der Index erstellt wird, können Sie unter Systeminformationen > Crawl-Informationen überprüfen.
Wenn der Crawl abgeschlossen ist, wird die Anzahl der durchsuchten Dokumente in der Indexgröße (Web/Datei) der [Crawl-Informationen] angezeigt.

Crawl-Status überprüfen
|image8|

Beispiel bei abgeschlossenem Crawl
|image9|

Suchbeispiel
----------

Nach Abschluss des Crawls werden bei einer Suche Ergebnisse wie im folgenden Bild zurückgegeben.

Suchbeispiel
|image10|

Anpassung der Suchoberfläche
======================

Hier stellen wir vor, wie Sie die Such-Startseite und die Suchergebnisliste anpassen können, die von Benutzern am häufigsten angezeigt werden.

Diesmal zeigen wir, wie Sie den Logodateinamen ändern.
Wenn Sie das Design selbst ändern möchten, ist es in einfachen JSP-Dateien beschrieben, sodass Sie es mit HTML-Kenntnissen ändern können.

Die Such-Startseite ist die Datei „app/WEB-INF/view/index.jsp".

Teil der JSP-Datei der Such-Startseite
::

    <la:form action="/search" method="get" styleId="searchForm">
      ${fe:facetForm()}${fe:geoForm()}
      ・
      ・
      ・
      <main class="container">
        <div class="row">
          <div class="col text-center searchFormBox">
            <h1 class="mainLogo">
              <img src="${fe:url('/images/logo.png')}"
                alt="<la:message key="labels.index_title" />" />
            </h1>
            <div class="notification">${notification}</div>
            <div>
              <la:info id="msg" message="true">
                <div class="alert alert-info">${msg}</div>
              </la:info>
              <la:errors header="errors.front_header"
                footer="errors.front_footer" prefix="errors.front_prefix"
                suffix="errors.front_suffix" />
            </div>

Um das auf der Such-Startseite angezeigte Bild zu ändern, ändern Sie „logo.png" oben in den gewünschten Dateinamen.
Die Datei wird in „app/images" platziert.

<la:form> und <la:message> sind JSP-Tags.
Zum Beispiel wird <s:form> bei der tatsächlichen HTML-Anzeige in ein form-Tag konvertiert.
Ausführliche Erklärungen finden Sie auf der LastaFlute-Website oder JSP-bezogenen Websites.

Als nächstes ist der Header-Teil der Suchergebnisliste die Datei „app/WEB-INF/view/header.jsp".

Teil der Header-JSP-Datei
::

				<la:link styleClass="navbar-brand d-inline-flex" href="/">
					<img src="${fe:url('/images/logo-head.png')}"
						alt="<la:message key="labels.header_brand_name" />"
						class="align-items-center" />
				</la:link>

Um das oben in der Suchergebnisliste angezeigte Bild zu ändern, ändern Sie den Dateinamen von „logo-head.png" oben.
Wie bei „logo.png" wird es in „app/images" platziert.

Diese Einstellungen können auch über System > Seitendesign konfiguriert werden.

Wenn Sie die von der JSP-Datei verwendete CSS-Datei ändern möchten, bearbeiten Sie „style.css" in „app/css".

Zusammenfassung
======

Wir haben Fess, ein Volltextsuchsystem, von der Installation bis zur Suche und einfachen Anpassungsmethoden erklärt.
Wir hoffen, dass wir zeigen konnten, dass Sie ohne spezielle Umgebungseinrichtung ein Suchsystem einfach aufbauen können, wenn Sie eine Java-Laufzeitumgebung haben.
Es kann auch in bestehende Systeme integriert werden, wenn Sie Website-Suchfunktionen hinzufügen möchten. Probieren Sie es also bitte aus.

Referenzmaterialien
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `OpenSearch <https://opensearch.org/>`__

-  `LastaFlute <https://lastaflute.dbflute.org/>`__
.. |image1| image:: ../../resources/images/en/article/1/fess-download.png
.. |image2| image:: ../../resources/images/en/article/1/top.png
.. |image3| image:: ../../resources/images/en/article/1/login.png
.. |image4| image:: ../../resources/images/en/article/1/web-crawl-conf-1.png
.. |image5| image:: ../../resources/images/en/article/1/web-crawl-conf-2.png
.. |image6| image:: ../../resources/images/en/article/1/web-crawl-conf-3.png
.. |image7| image:: ../../resources/images/en/article/1/scheduler.png
.. |image8| image:: ../../resources/images/en/article/1/session-info-1.png
.. |image9| image:: ../../resources/images/en/article/1/session-info-2.png
.. |image10| image:: ../../resources/images/en/article/1/search-result.png
