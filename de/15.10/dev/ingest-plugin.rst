==================================
Ingest-Plugin
==================================

Übersicht
=========

Ingest-Plugins bieten eine Funktion zur Verarbeitung und Transformation von
Daten, unmittelbar bevor Dokumente im Index registriert werden. Jedes durch
den Crawl abgerufene Dokument durchläuft vor der Übermittlung an den Index
die registrierten Ingester.

Anwendungsfälle
===============

- Textnormalisierung (z. B. Konvertierung zwischen Vollbreiten- und
  Halbbreitenzeichen, Formatierung von Leerzeichen usw.)
- Hinzufügen von Metadaten oder benutzerdefinierten Feldern
- Maskierung sensibler Informationen
- Umwandlung von Werten (z. B. Dekodierung kodierter Vektor-Embeddings)

Ingester-Klasse
===============

Die Ingest-Funktion wird implementiert, indem die abstrakte Klasse
``org.codelibs.fess.ingest.Ingester`` erweitert wird. ``Ingester`` stellt
``process``-Methoden bereit, die je nach Crawl-Typ und Verarbeitungsphase
aufgerufen werden. Da alle Standardimplementierungen das empfangene
``target`` unverändert zurückgeben (also nichts tun), müssen nur die
benötigten Methoden überschrieben werden.

- ``protected Map<String, Object> process(Map<String, Object> target)``

  Dies ist das gemeinsame Delegationsziel der beiden ``Map``-Varianten der
  Methode. Wird diese Methode überschrieben, gilt sie sowohl für Dokumente
  aus dem Datenspeicher-Crawl als auch für Dokumente aus dem Web-/Datei-Crawl
  (bei der Indexregistrierung). Für die meisten Anwendungsfälle genügt es,
  nur diese Methode zu überschreiben.

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  Wird beim Datenspeicher-Crawl aufgerufen. Standardmäßig wird an
  ``process(target)`` delegiert.

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  Wird bei der Indexregistrierung im Web-/Datei-Crawl aufgerufen.
  Standardmäßig wird an ``process(target)`` delegiert.

- ``public ResultData process(ResultData target, ResponseData responseData)``

  Wird bei der Antwortverarbeitung im Web-/Datei-Crawl aufgerufen (bevor das
  Zugriffsergebnis gespeichert wird). Standardmäßig wird ``target``
  unverändert zurückgegeben.

Ausführungsreihenfolge (priority)
----------------------------------

Wenn mehrere Ingester registriert sind, werden sie in aufsteigender
Reihenfolge des Felds ``priority`` ausgeführt (kleinere Werte zuerst). Der
Standardwert ist ``99``. Er kann direkt im Konstruktor gesetzt oder über
``setPriority(int)`` geändert werden.

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

Implementierungsbeispiel
=========================

Ein Beispiel, bei dem ``process(Map<String, Object>)`` überschrieben wird,
um den Inhalt zu normalisieren und ein benutzerdefiniertes Feld
hinzuzufügen:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // Ausführungsreihenfolge festlegen (kleinere Werte werden zuerst ausgeführt; Standard ist 99)
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // Normalisierung des Inhalts
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // Hinzufügen eines benutzerdefinierten Felds
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // Das verarbeitete Dokument zurückgeben
            return target;
        }
    }

.. note::

    Wenn die ``process``-Methode ``null`` zurückgibt, schlägt die
    Indexregistrierung fehl. Da es keinen Mechanismus zum Überspringen von
    Dokumenten gibt, muss stets ``target`` zurückgegeben werden.

Registrierung
=============

Ingester werden über den DI-Container registriert. Das Plugin enthält dafür
die Datei ``fess_ingest++.xml``. Das ``++`` am Ende des Dateinamens ist eine
Merge-Konvention, mit der die Konfiguration an die Datei
``fess_ingest.xml`` (welche die ``ingestFactory``, die die Ingester
verwaltet, definiert) der |Fess|-Kernanwendung angehängt wird.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleIngester"
                   class="org.codelibs.fess.ingest.example.ExampleIngester">
            <postConstruct name="register"/>
        </component>
    </components>

Durch ``<postConstruct name="register"/>`` wird nach der Erzeugung der
Komponente ``Ingester#register()`` aufgerufen, wodurch sie sich selbst bei
der ``ingestFactory`` registriert.

Für die Ingest-Funktion gibt es keine Konfigurationseinträge in
``fess_config.properties``. Aktivierung bzw. Deaktivierung erfolgt durch das
Vorhandensein des Plugins, und die Ausführungsreihenfolge wird über
``priority`` gesteuert.

Ausführungsablauf
==================

Ingester werden unmittelbar bevor das verarbeitete Dokument an den Index
übermittelt wird, an den folgenden Stellen in aufsteigender Reihenfolge von
``priority`` aufgerufen:

- **Datenspeicher-Crawl**: Unmittelbar bevor das Dokument gesendet wird,
  wird ``process(Map, DataStoreParams)`` aufgerufen.
- **Web-/Datei-Crawl (bei der Antwortverarbeitung)**: Bevor das
  Crawl-Ergebnis gespeichert wird, wird ``process(ResultData, ResponseData)``
  aufgerufen.
- **Web-/Datei-Crawl (bei der Indexregistrierung)**: Unmittelbar bevor das
  Dokument gesendet wird, wird ``process(Map, AccessResult)`` aufgerufen.

In allen Fällen wird, wenn ein Ingester eine Ausnahme auslöst, eine
Warnmeldung protokolliert und die Verarbeitung fortgesetzt (die
Indexregistrierung des betreffenden Dokuments wird dadurch nicht
abgebrochen).

.. note::

    Da Ingester in der Ausführungsumgebung des Crawlers (``ingestFactory``)
    registriert werden, arbeiten sie als Teil des Crawl-Prozesses.

Referenzimplementierungen
==========================

Als Referenz für die Implementierung sind die folgenden Plugins auf GitHub
unter `CodeLibs <https://github.com/codelibs>`__ veröffentlicht:

- ``fess-ingest-example`` - Minimalistische Beispielimplementierung
- ``fess-webapp-multimodal`` - Plugin mit ``EmbeddingIngester``, der
  Vektor-Embeddings dekodiert

Referenzinformationen
======================

- :doc:`plugin-architecture` - Plugin-Architektur
