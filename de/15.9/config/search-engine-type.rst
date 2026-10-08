================
Suchmaschinentyp
================

Übersicht
=========

|Fess| speichert seine Daten in OpenSearch. Die Einstellung ``search_engine.type`` teilt |Fess| mit, mit welcher Art von OpenSearch es verbunden ist. Davon hängt ab, welche Indexdefinitionen |Fess| erstellt und welche Funktionen es bietet.

Beim Standardwert ``default`` erwartet |Fess| ein OpenSearch, in dem die vier CodeLibs-Plugins installiert sind (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash`` und ``opensearch-configsync``; siehe :doc:`../install/install`). Um sich mit einem reinen OpenSearch ohne diese Plugins zu verbinden, zum Beispiel mit einem verwalteten Dienst, auf dem Sie keine eigenen Plugins installieren können, setzen Sie den Wert auf ``vanilla``.

Typen
=====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Wert
     - Beschreibung
   * - ``default``
     - OpenSearch mit den CodeLibs-Plugins. Dies ist der Standardwert.
   * - ``vanilla``
     - Ein reines OpenSearch ohne die CodeLibs-Plugins. Neu in 15.9. Die Indexdefinitionen werden aus ``fess_indices/_vanilla/`` gelesen. |Fess| 15.8 und früher kennen diesen Wert nicht; verwenden Sie dort ``cloud``.
   * - ``aws``
     - Wie ``vanilla``, vorgesehen für Amazon OpenSearch Service. Siehe :ref:`search-engine-type-aws`.
   * - ``cloud``
     - Ein veralteter Alias für ``vanilla``. |Fess| schreibt beim Start eine Warnung ins Log. Ändern Sie den Wert auf ``vanilla``.
   * - Jeder andere Wert
     - Wird wie ``default`` behandelt, mit dem Unterschied, dass Definitionsdateien unter ``fess_indices/_<Typ>/`` Vorrang vor den gleichnamigen Dateien unter ``fess_indices/`` haben.

|Fess| erkennt die Plugins nicht automatisch; Sie legen den Typ selbst fest. Legen Sie ihn vor dem ersten Start fest. Die Indexdefinitionen werden beim Erstellen eines Index angewendet. Eine spätere Änderung des Werts ändert daher die bereits vorhandenen Indizes nicht.

Ohne die Plugins nicht verfügbare Funktionen
============================================

Mit ``vanilla`` und ``aws`` (einschließlich des veralteten ``cloud``) stehen die folgenden Funktionen nicht zur Verfügung. Die davon abhängigen Einträge der Administrationsoberfläche werden ausgeblendet.

* **Wörterbuchverwaltung**: [System > Wörterbuch] wird ausgeblendet. Die Wörterbuchseiten und die Wörterbuch-Administrations-API (``/api/admin/dict/``) können nicht verwendet werden. Auch „Wörterbücher zurücksetzen“ und „Dokumentenindex neu laden“ auf der Seite Wartung werden ausgeblendet. Die Analyzer verwenden die in der Indexdefinition enthaltenen Regeln, keine Wörterbuchdateien.
* **Zusammenfassen von Ergebnissen**: „Doppelte Ergebnisse ausblenden“ unter Allgemein wird ausgeblendet; das Zusammenfassen ist immer ausgeschaltet.
* **Duplikaterkennung**: Die Inhaltssignatur, mit der Dokumente mit gleichem Inhalt gefunden werden, wird nicht berechnet. Die Registerkarte „Duplikate“ des Dokumentberichts wird ausgeblendet (der Bericht über inaktive Dokumente bleibt verfügbar), und der Suchparameter ``sdh`` (ähnliche Dokumente) wird ignoriert.
* **Analyzer**: Japanisch, Koreanisch und vereinfachtes Chinesisch werden statt mit den CodeLibs-Tokenizern mit den OpenSearch-Analyzern Kuromoji, Nori und SmartCN zerlegt, sodass sich die Tokens von denen bei ``default`` unterscheiden. Für Vietnamesisch (Felder ``*_vi``) und traditionelles Chinesisch (Felder ``*_zh-tw``) wird ein leerer Analyzer verwendet, der keine Terme registriert. Dokumente in diesen Sprachen werden weiterhin in den sprachunabhängigen Feldern ``content`` und ``title`` indexiert.

Erforderliche OpenSearch-Plugins
================================

Die Indexdefinitionen für ``vanilla`` und ``aws`` verwenden Analyzer und einen Vektor-Feldtyp, die von offiziellen OpenSearch-Plugins bereitgestellt werden. Das OpenSearch, mit dem Sie sich verbinden, muss diese Plugins enthalten:

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` (k-NN)

Die CodeLibs-Plugins sind nicht erforderlich. Bei einem OpenSearch, das Sie selbst betreiben, installieren Sie ein Plugin mit ``opensearch-plugin install``, zum Beispiel ``bin/opensearch-plugin install analysis-nori``. Zu Amazon OpenSearch Service siehe :ref:`search-engine-type-aws`.

Ist der Typ ``vanilla`` oder ``aws``, listet |Fess| beim Start die installierten Plugins auf (``GET /_cat/plugins``). Fehlt eines der oben genannten Plugins, schreibt es eine Warnung ins Log, die die fehlenden Plugins nennt, und startet weiter. Schlägt die Anfrage fehl, zum Beispiel weil der Dienst sie nicht zulässt, wird die Prüfung übersprungen.

Typ festlegen
=============

Docker
------

Setzen Sie die Umgebungsvariable ``SEARCH_ENGINE_TYPE`` für den Dienst ``fess01`` in ``compose.yaml``::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` kann mit Images ab |Fess| 15.9 verwendet werden. Setzen Sie bei einem älteren Image ``SEARCH_ENGINE_TYPE=cloud``. Zu den übrigen Docker-Einstellungen siehe :doc:`../install/install-docker`.

Installationen ohne Docker
--------------------------

``bin/fess.in.sh`` liest ``SEARCH_ENGINE_TYPE`` nicht. Verwenden Sie stattdessen eine der folgenden Möglichkeiten.

* Schreiben Sie ``search_engine.type`` in ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` bei der ZIP-Variante, ``/etc/fess/fess_config.properties`` bei den RPM- und DEB-Varianten).
* Hängen Sie in ``bin/fess.in.sh`` der ZIP-Variante (unter Windows ``bin\fess.in.bat``) eine JVM-Option an ``FESS_JAVA_OPTS`` an.

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

Starten Sie |Fess| nach der Änderung neu. Der Crawler und die übrigen Job-Prozesse erhalten die Einstellung von |Fess|; Sie müssen sie dafür nicht gesondert setzen.

Verbindungseinstellungen
========================

Die Verbindung zu OpenSearch wird wie bei jedem anderen Typ konfiguriert.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Einstellung
     - Beschreibung
   * - ``search_engine.http.url``
     - Der HTTP-Endpunkt von OpenSearch. Ist die Umgebungsvariable ``SEARCH_ENGINE_HTTP_URL`` gesetzt, hat sie Vorrang.
   * - ``search_engine.username`` / ``search_engine.password``
     - Benutzername und Passwort für die HTTP-Basic-Authentifizierung. Sie werden nur verwendet, wenn beide gesetzt sind. In Docker verwenden Sie die Umgebungsvariablen ``SEARCH_ENGINE_USERNAME`` und ``SEARCH_ENGINE_PASSWORD``.
   * - ``search_engine.http.ssl.certificate_authorities``
     - Der Pfad einer CA-Zertifikatsdatei (X.509), mit der das Serverzertifikat eines HTTPS-Endpunkts geprüft wird. Sie wird nicht benötigt, wenn das Zertifikat von einer CA ausgestellt wurde, der Java bereits vertraut.

Ein Eintrag aus ``fess_config.properties`` kann auch als ``-Dfess.config.<Eintragsname>`` in ``FESS_JAVA_OPTS`` angegeben werden (siehe :doc:`../install/install-docker`).

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

Um eine Domain von Amazon OpenSearch Service zu verwenden, setzen Sie ``search_engine.type`` auf ``aws`` (``vanilla`` verhält sich genauso).

Voraussetzungen
---------------

* Die Domain führt OpenSearch 3.x aus. |Fess| prüft die Engine beim Start und startet mit allem anderen als OpenSearch 3 nicht.
* Die unter „Erforderliche OpenSearch-Plugins“ aufgeführten Plugins sind in der Domain verfügbar. In Amazon OpenSearch Service ist Nori ein optionales Paket: Ordnen Sie es der Domain zu, bevor Sie |Fess| starten.
* Der Endpunkt verwendet HTTPS.
* Die differenzierte Zugriffssteuerung (Fine-Grained Access Control) ist aktiviert und enthält einen internen Benutzer, mit dem sich |Fess| anmeldet (HTTP-Basic-Authentifizierung). Das Signieren von Anfragen mit AWS-IAM-Anmeldedaten (SigV4) wird noch nicht unterstützt; eine Domain, die nur IAM-signierte Anfragen akzeptiert, kann daher nicht verwendet werden.

Beispielkonfiguration
---------------------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

Prüfungen beim Start
--------------------

* Die unter „Erforderliche OpenSearch-Plugins“ beschriebene Plugin-Prüfung läuft auch bei ``aws``. Haben Sie vergessen, Nori zuzuordnen, erscheint in ``fess.log`` eine Warnung.
* Weist die Domain eine Anfrage mit HTTP 401 oder 403 ab, schreibt |Fess| eine Warnung ins Log. Führt dies zu einem fehlgeschlagenen Start, verweist die Fehlermeldung auf Benutzername, Passwort und Zugriffsrichtlinie der Domain.

DNS-Cache-TTL
-------------

Der Endpunkt eines verwalteten Dienstes kann sich im Lauf der Zeit auf andere IP-Adressen auflösen, und die JVM speichert das Ergebnis einer DNS-Abfrage im Cache. Eine kurze Cache-Dauer ermöglicht es |Fess|, einer solchen Änderung zu folgen. Setzen Sie ``-Dsun.net.inetaddr.ttl=5`` (Sekunden) an den folgenden beiden Stellen.

1. Der |Fess|-Prozess: Hängen Sie die Option an ``FESS_JAVA_OPTS`` an.

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. Die Job-Prozesse: Die Prozesse für Crawler, Suggest, Chunk und Miniaturansichten werden von |Fess| als eigene JVMs gestartet und erben ``FESS_JAVA_OPTS`` nicht. Fügen Sie dieselbe Option am Ende von ``jvm.crawler.options``, ``jvm.suggest.options``, ``jvm.chunk.options`` und ``jvm.thumbnail.options`` in ``fess_config.properties`` hinzu. Jeder dieser Werte enthält eine Option pro Zeile, und jede Zeile endet mit ``\n\``.

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   Fügen Sie die Zeile nach den vorhandenen Zeilen an, und verfahren Sie bei den anderen drei Einträgen ebenso.

In Docker geben Sie ``FESS_JAVA_OPTS`` in den Umgebungsvariablen der Compose-Datei an. Um die Einträge ``jvm.*.options`` zu ändern, binden Sie eine geänderte ``fess_config.properties`` ein (siehe :doc:`../install/install-docker`).
