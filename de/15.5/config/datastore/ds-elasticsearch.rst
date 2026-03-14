==================================
Elasticsearch/OpenSearch-Konnektor
==================================

Übersicht
=========

Der Elasticsearch/OpenSearch-Konnektor bietet die Funktionalität, Daten aus Elasticsearch- oder OpenSearch-Clustern abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-elasticsearch`` erforderlich.

Unterstützte Versionen
======================

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Lesezugriff auf den Elasticsearch/OpenSearch-Cluster ist erforderlich
3. Berechtigungen zum Ausführen von Abfragen sind erforderlich

Plugin-Installation
-------------------

Methode 1: JAR-Datei direkt platzieren

::

    # Von Maven Central herunterladen
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # Platzieren
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # oder
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Methode 2: Über die Administrationsoberfläche installieren

1. Öffnen Sie "System" -> "Plugins"
2. Laden Sie die JAR-Datei hoch
3. Starten Sie |Fess| neu

Konfiguration
=============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - External Elasticsearch
   * - Handler-Name
     - ElasticsearchDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

Einfache Verbindung:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    size=100
    scroll=5m

Verbindung mit Authentifizierung:

::

    settings.fesen.http.url=https://elasticsearch.example.com:9200
    index=myindex
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=100
    scroll=5m

Mehrere Hosts konfigurieren:

::

    settings.fesen.http.url=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    size=100
    scroll=5m

Parameterliste
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``settings.fesen.http.url``
     - Ja
     - Elasticsearch/OpenSearch-Hosts (mehrere kommagetrennt)
   * - ``index``
     - Ja
     - Name des Zielindexes
   * - ``settings.fesen.username``
     - Nein
     - Benutzername für Authentifizierung
   * - ``settings.fesen.password``
     - Nein
     - Passwort für Authentifizierung
   * - ``size``
     - Nein
     - Abrufgröße beim Scrollen (Standard: 100)
   * - ``scroll``
     - Nein
     - Scroll-Timeout (Standard: 1m)
   * - ``query``
     - Nein
     - Query-JSON (Standard: match_all)
   * - ``fields``
     - Nein
     - Abzurufende Felder (kommagetrennt)

Skript-Einstellungen
--------------------

Einfaches Mapping:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Zugriff auf verschachtelte Felder:

::

    url=data.metadata.url
    title=data.title
    content=data.body.content
    author=data.author.name
    created=data.created_at
    last_modified=data.updated_at

Verfügbare Felder
~~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - Felder des Elasticsearch-Dokuments
- ``data._id`` - Dokument-ID
- ``data._index`` - Indexname
- ``data._type`` - Dokumenttyp (Elasticsearch vor Version 7)
- ``data._score`` - Suchpunktzahl

Query-Konfiguration
===================

Alle Dokumente abrufen
----------------------

Standardmäßig werden alle Dokumente abgerufen.
Wenn der ``query``-Parameter nicht angegeben wird, wird ``match_all`` verwendet.

Nach bestimmten Bedingungen filtern
-----------------------------------

::

    query={"query":{"term":{"status":"published"}}}

Bereichsangabe:

::

    query={"query":{"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}}

Mehrere Bedingungen:

::

    query={"query":{"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}}

Sortierung angeben:

::

    query={"query":{"match_all":{}},"sort":[{"timestamp":{"order":"desc"}}]}

Nur bestimmte Felder abrufen
============================

Abruffelder mit fields-Parameter einschränken
---------------------------------------------

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

Um alle Felder abzurufen, ``fields`` nicht angeben oder leer lassen.

Anwendungsbeispiele
===================

Einfaches Index-Crawling
------------------------

Parameter:

::

    settings.fesen.http.url=http://localhost:9200
    index=articles
    size=100
    scroll=5m

Skript:

::

    url=data.url
    title=data.title
    content=data.content
    created=data.created_at
    last_modified=data.updated_at

Crawling von Cluster mit Authentifizierung
------------------------------------------

Parameter:

::

    settings.fesen.http.url=https://es.example.com:9200
    index=products
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=200
    scroll=10m

Skript:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " " + data.specifications
    digest=data.category
    last_modified=data.updated_at

Crawling aus mehreren Indizes
-----------------------------

Parameter:

::

    settings.fesen.http.url=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    size=100

Skript:

::

    url="https://logs.example.com/view/" + data._id
    title=data.message
    content=data.stack_trace
    digest=data.service + " - " + data.level
    last_modified=data.timestamp

OpenSearch-Cluster crawlen
--------------------------

Parameter:

::

    settings.fesen.http.url=https://opensearch.example.com:9200
    index=documents
    settings.fesen.username=admin
    settings.fesen.password=admin
    size=100
    scroll=5m

Skript:

::

    url=data.url
    title=data.title
    content=data.body
    last_modified=data.modified_date

Crawling mit eingeschränkten Feldern
------------------------------------

Parameter:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    size=100

Skript:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Lastverteilung über mehrere Hosts
---------------------------------

Parameter:

::

    settings.fesen.http.url=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=5m

Skript:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Fehlerbehebung
==============

Verbindungsfehler
-----------------

**Symptom**: ``Connection refused`` oder ``No route to host``

**Zu überprüfen**:

1. Überprüfen Sie, ob die Host-URL korrekt ist (Protokoll, Hostname, Port)
2. Überprüfen Sie, ob Elasticsearch/OpenSearch läuft
3. Überprüfen Sie die Firewall-Einstellungen
4. Bei HTTPS überprüfen Sie, ob das Zertifikat gültig ist

Authentifizierungsfehler
------------------------

**Symptom**: ``401 Unauthorized`` oder ``403 Forbidden``

**Zu überprüfen**:

1. Überprüfen Sie Benutzername und Passwort
2. Überprüfen Sie, ob der Benutzer die entsprechenden Berechtigungen hat:

   - Leseberechtigung auf den Index
   - Berechtigung zur Verwendung der Scroll-API

3. Bei Elasticsearch Security (X-Pack) überprüfen Sie, ob es korrekt konfiguriert ist

Index nicht gefunden
--------------------

**Symptom**: ``index_not_found_exception``

**Zu überprüfen**:

1. Überprüfen Sie den Indexnamen (einschließlich Groß-/Kleinschreibung)
2. Überprüfen Sie, ob der Index existiert:

   ::

       GET /_cat/indices

3. Überprüfen Sie, ob das Wildcard-Muster korrekt ist (z.B.: ``logs-*``)

Query-Fehler
------------

**Symptom**: ``parsing_exception`` oder ``search_phase_execution_exception``

**Zu überprüfen**:

1. Überprüfen Sie, ob das Query-JSON korrekt ist
2. Überprüfen Sie, ob die Query mit der Elasticsearch/OpenSearch-Version kompatibel ist
3. Überprüfen Sie, ob die Feldnamen korrekt sind
4. Testen Sie die Query direkt in Elasticsearch/OpenSearch:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

Scroll-Timeout
--------------

**Symptom**: ``No search context found`` oder ``Scroll timeout``

**Lösung**:

1. Erhöhen Sie ``scroll``:

   ::

       scroll=10m

2. Verringern Sie ``size``:

   ::

       size=50

3. Überprüfen Sie die Cluster-Ressourcen

Crawling großer Datenmengen
---------------------------

**Symptom**: Crawling ist langsam oder Timeout

**Lösung**:

1. Passen Sie ``size`` an (zu groß kann langsam sein):

   ::

       size=100  # Standard
       size=500  # Größer

2. Schränken Sie abzurufende Felder mit ``fields`` ein
3. Filtern Sie mit ``query`` nur benötigte Dokumente
4. Teilen Sie in mehrere Datenspeicher auf (nach Index, Zeitbereich usw.)

Speicherüberlauf
----------------

**Symptom**: OutOfMemoryError

**Lösung**:

1. Verringern Sie ``size``
2. Schränken Sie abzurufende Felder mit ``fields`` ein
3. Erhöhen Sie die Heap-Größe von |Fess|
4. Schließen Sie große Felder aus (Binärdaten usw.)

SSL/TLS-Verbindung
==================

Bei selbstsignierten Zertifikaten
---------------------------------

.. warning::
   Verwenden Sie in Produktionsumgebungen ordnungsgemäß signierte Zertifikate.

Bei selbstsignierten Zertifikaten fügen Sie das Zertifikat zum Java Keystore hinzu:

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Client-Zertifikatauthentifizierung
----------------------------------

Wenn ein Client-Zertifikat erforderlich ist, sind zusätzliche Parameter-Einstellungen erforderlich.
Details finden Sie in der Elasticsearch-Client-Dokumentation.

Erweiterte Query-Beispiele
==========================

Query mit Aggregationen
-----------------------

.. note::
   Aggregationsergebnisse werden nicht abgerufen, nur Dokumente.

::

    query={"query":{"match_all":{}},"aggs":{"categories":{"terms":{"field":"category"}}}}

Skript-Felder
-------------

::

    query={"query":{"match_all":{}},"script_fields":{"full_url":{"script":"doc['protocol'].value + '://' + doc['host'].value + doc['path'].value"}}}

Skript:

::

    url=data.full_url
    title=data.title
    content=data.content

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
