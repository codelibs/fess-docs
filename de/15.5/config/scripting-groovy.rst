==================================
Groovy-Skripting-Leitfaden
==================================

Uebersicht
==========

Groovy ist die Standard-Skriptsprache fuer |Fess|.
Sie laeuft auf der Java Virtual Machine (JVM) und ermoeglicht es Ihnen,
bei hoher Kompatibilitaet mit Java Skripte mit einer praeganteren Syntax zu schreiben.

Grundlegende Syntax
===================

Variablendeklaration
--------------------

::

    // Typinferenz (def)
    def name = "Fess"
    def count = 100

    // Explizite Typangabe
    String title = "Dokumenttitel"
    int pageNum = 1

Zeichenkettenoperationen
------------------------

::

    // Zeichenketteninterpolation (GString)
    def id = 123
    def url = "https://example.com/doc/${id}"

    // Mehrzeilige Zeichenketten
    def content = """
    Dies ist eine
    mehrzeilige Zeichenkette
    """

    // Ersetzung
    title.replace("alt", "neu")
    title.replaceAll(/\s+/, " ")  // Regulaerer Ausdruck

    // Teilen und Verbinden
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // Gross-/Kleinschreibung aendern
    title.toUpperCase()
    title.toLowerCase()

Collection-Operationen
----------------------

::

    // Listen
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // Maps
    def map = [name: "Fess", version: "15.5"]
    println map.name
    println map["version"]

Bedingte Verzweigung
--------------------

::

    // if-else
    if (data.status == "active") {
        return "Aktiv"
    } else {
        return "Inaktiv"
    }

    // Ternaerer Operator
    def result = data.count > 0 ? "Vorhanden" : "Keine"

    // Elvis-Operator (Null-Koaleszenz-Operator)
    def value = data.title ?: "Ohne Titel"

    // Sichere Navigationsoperator
    def length = data.content?.length() ?: 0

Schleifenverarbeitung
---------------------

::

    // for-each
    for (item in items) {
        println item
    }

    // Closure
    items.each { item ->
        println item
    }

    // Bereich
    (1..10).each { println it }

Datenspeicher-Skripte
=====================

Beispiele fuer Skripte zur Datenspeicher-Konfiguration.

Grundlegendes Mapping
---------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL-Generierung
---------------

::

    // URL-Generierung basierend auf ID
    url="https://example.com/article/" + data.id

    // Kombination mehrerer Felder
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // Bedingte URL
    url=data.external_url ?: "https://example.com/default/" + data.id

Inhaltsverarbeitung
-------------------

::

    // HTML-Tags entfernen
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // Mehrere Felder kombinieren
    content=data.title + "\n" + data.description + "\n" + data.body

    // Laengenbeschraenkung
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Datumsverarbeitung
------------------

::

    // Datum parsen
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // Konvertierung von Epochensekunden
    lastModified=new Date(data.timestamp * 1000L)

Geplante Aufgaben-Skripte
=========================

Beispiele fuer Groovy-Skripte in geplanten Aufgaben.

Crawl-Aufgabe ausfuehren
------------------------

::

    return container.getComponent("crawlJob").execute();

Bedingtes Crawling
------------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // Nur ausserhalb der Geschaeftszeiten crawlen
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Waehrend der Geschaeftszeiten uebersprungen"

Mehrere Aufgaben nacheinander ausfuehren
----------------------------------------

::

    def results = []

    // Indexoptimierung
    results << container.getComponent("optimizeJob").execute()

    // Crawl ausfuehren
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

Java-Klassen verwenden
======================

Innerhalb von Groovy-Skripten koennen Sie Java-Standardbibliotheken und Fess-Klassen verwenden.

Datum und Uhrzeit
-----------------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

Dateioperationen
----------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/pfad/zur/datei.txt")))

HTTP-Kommunikation
------------------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   Der Zugriff auf externe Ressourcen beeintraechtigt die Leistung,
   halten Sie ihn daher auf ein Minimum.

Zugriff auf Fess-Komponenten
============================

Sie koennen mit ``container`` auf Fess-Komponenten zugreifen.

System-Helfer
-------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

Konfigurationswerte abrufen
---------------------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

Suchen ausfuehren
-----------------

::

    def searchHelper = container.getComponent("searchHelper")
    // Suchparameter festlegen und Suche ausfuehren

Fehlerbehandlung
================

::

    try {
        def result = processData(data)
        return result
    } catch (Exception e) {
        import org.apache.logging.log4j.LogManager
        def logger = LogManager.getLogger("script")
        logger.error("Fehler bei der Datenverarbeitung: {}", e.message, e)
        return "Fehler: " + e.message
    }

Debugging und Protokollausgabe
==============================

Protokollausgabe
----------------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug-Nachricht: {}", data.id)
    logger.info("Dokument verarbeiten: {}", data.title)
    logger.warn("Warnung: {}", message)
    logger.error("Fehler: {}", e.message)

Debug-Ausgabe
-------------

::

    // Konsolenausgabe (nur Entwicklung)
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

Best Practices
==============

1. **Einfach halten**: Komplexe Logik vermeiden und lesbaren Code schreiben
2. **Null-Pruefungen**: ``?.`` und ``?:`` Operatoren nutzen
3. **Ausnahmebehandlung**: Unerwartete Fehler mit geeignetem try-catch behandeln
4. **Protokollausgabe**: Protokolle fuer einfacheres Debugging ausgeben
5. **Leistung**: Zugriff auf externe Ressourcen minimieren

Referenzinformationen
=====================

- `Groovy Offizielle Dokumentation <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - Skripting-Uebersicht
- :doc:`../admin/dataconfig-guide` - Datenspeicher-Konfigurationsleitfaden
- :doc:`../admin/scheduler-guide` - Scheduler-Konfigurationsleitfaden
