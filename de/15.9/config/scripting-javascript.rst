==================================
JavaScript-Skripting-Leitfaden
==================================

Übersicht
==========

JavaScript ist ab |Fess| 15.9 die Standard-Skriptsprache.
Es läuft auf Sai (einem Nashorn-Fork von CodeLibs, den |Fess| bereits für DI-XML-Ausdrücke
verwendet), und Skripte werden als ECMAScript 6 ausgeführt. Der Bezeichner lautet
``javascript``; alternativ können auch die Aliase ``js`` und ``sai`` verwendet werden.

.. _javascript-statement-null:

Wie Skripte ausgewertet werden
================================

Die Skript-Engine von |Fess| versucht zunächst, den Skripttext als einzelnen „Ausdruck"
zu kompilieren. Nur wenn dies syntaktisch fehlschlägt, wird der Text erneut als Block von
„Anweisungen" kompiliert.

Deshalb funktioniert sowohl ein einfacher Ausdruck, der lediglich einen Wert zurückgibt:

::

    content.length()

als auch ein Skript mit einer ``return``-Anweisung auf oberster Ebene:

::

    return container.getComponent("crawlJob").execute();

Letzteres wäre in reinem JavaScript normalerweise ein Syntaxfehler, da ein ``return`` auf
oberster Ebene nicht zulässig ist. Da es sich jedoch nicht als Ausdruck kompilieren lässt,
wird es als Anweisungsblock neu interpretiert und als gültiges Skript ausgeführt.

An Stellen, an denen jede Zeile als einzelner Ausdruck behandelt wird — etwa bei
Datenspeicher-Skripten — kann ein Skript aus mehreren Anweisungen nicht verwendet werden.
An Stellen, an denen das gesamte Skript ausgewertet wird — etwa bei geplanten Aufgaben —
können Sie dagegen frei mehrzeilige Anweisungen, ``let`` / ``const``-Variablendeklarationen
und Kontrollstrukturen verwenden.

.. warning::

   Ein Skript, das als Anweisungsblock kompiliert wird, liefert nur dann einen Wert zurück,
   wenn es ein explizites ``return`` enthält. Lässt sich der Text nicht als Ausdruck parsen,
   wird er in eine Funktion eingebettet und als Block von Anweisungen ausgeführt — und ein
   Block ohne ``return`` wird zu ``null`` ausgewertet. Ein einziges abschließendes Semikolon
   genügt, um diese Grenze zu überschreiten:

   .. list-table::
      :header-rows: 1
      :widths: 40 15 45

      * - Skript
        - Ergebnis
        - Grund
      * - ``content.length()``
        - ``11``
        - Wird als Ausdruck geparst; der Wert des Ausdrucks ist das Ergebnis
      * - ``content.length();``
        - ``null``
        - Wird nur als Anweisungsblock geparst, der kein ``return`` enthält
      * - ``var x = 1; x + 2``
        - ``null``
        - Wird nur als Anweisungsblock geparst, der kein ``return`` enthält

   Unter Groovy lieferten alle drei einen Wert, da dort der Wert der zuletzt ausgewerteten
   Anweisung der Rückgabewert des Skripts ist. In JavaScript gibt es diese Regel nicht.

   Dies ist der einzige Unterschied bei der Migration, der weder einen Fehler noch eine
   Logzeile erzeugt und dessen einziges Symptom ein still leer bleibendes Feld ist: Ein
   Datenspeicher-Mapping, dessen Skript ``null`` zurückgibt, setzt dieses Feld schlicht nicht.
   Schreiben Sie jede ``Feldname=Ausdruck``-Zeile eines Datenspeichers als reinen Ausdruck ohne
   abschließendes Semikolon, und geben Sie jedem Skript einer geplanten Aufgabe ein explizites
   ``return``.

Grundlegende Syntax
===================

Eine Zeile ohne abschließendes Semikolon ist im Folgenden ein **Ausdruck** und kann überall
verwendet werden, auch in einer ``Feldname=Ausdruck``-Zeile eines Datenspeichers.
Deklarationen ( ``let`` / ``const`` ), ``if``-Blöcke und Schleifen sind **Anweisungen**: Sie
können nur dort verwendet werden, wo das gesamte Skript ausgewertet wird, etwa in einer
geplanten Aufgabe, und das Skript muss ein explizites ``return`` enthalten, um einen Wert zu
liefern. Siehe „Wie Skripte ausgewertet werden" oben.

Variablendeklaration
--------------------

::

    // let (neu zuweisbare Variable)
    let name = "Fess";
    let count = 100;

    // const (nicht neu zuweisbare Konstante)
    const title = "Dokumenttitel";
    const pageNum = 1;

Zeichenkettenoperationen
------------------------

::

    // Template-Literale (ES6)
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // Mehrzeilige Zeichenketten (Template-Literal)
    const content = `
    Dies ist eine
    mehrzeilige Zeichenkette
    `;

    // Ersetzung (mit regulärem Ausdruck; ECMAScript 6 kennt kein String#replaceAll)
    title.replace(/alt/g, "neu")
    title.replace(/\s+/g, " ")  // Aufeinanderfolgende Leerzeichen zusammenfassen

    // Teilen und Verbinden
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // Gross-/Kleinschreibung ändern
    title.toUpperCase()
    title.toLowerCase()

Collection-Operationen
-----------------------

::

    // Arrays
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // Objekte
    const map = { name: "Fess", version: "15.9" };
    map.name
    map["version"]

Bedingte Verzweigung
--------------------

::

    // if-else
    if (data.status === "active") {
        return "Aktiv";
    } else {
        return "Inaktiv";
    }

    // Ternärer Operator
    data.count > 0 ? "Vorhanden" : "Keine"

    // Standardwert (logischer OR-Operator; JavaScript kennt keinen Elvis-Operator)
    data.title || "Ohne Titel"

    // Optional Chaining (?.) ist ES2020-Syntax und unter ES6 nicht verfügbar.
    // Prüfen Sie stattdessen explizit auf null.
    (data.content != null) ? data.content.length() : 0

Schleifenverarbeitung
----------------------

::

    // for...of (ES6)
    for (const item of items) {
        // Verarbeitung jedes Elements
    }

    // forEach (Arrow-Funktion)
    items.forEach(item => {
        // Verarbeitung jedes Elements
    });

    // Für einen Bereich erzeugen Sie ein Array oder verwenden eine for-Schleife
    // (JavaScript kennt keinen Groovy-artigen Bereichsausdruck)
    for (let i = 1; i <= 10; i++) {
        // ...
    }

Datenspeicher-Skripte
=====================

Beispiele für Skripte zur Datenspeicher-Konfiguration.

.. note::
   In Datenspeicher-Skripten wird jede ``Feldname=Ausdruck``-Zeile unabhängig als einzelner Ausdruck ausgewertet.
   Daher können Variablendeklarationen wie ``let`` / ``const`` und mehrzeilige Kontrollstrukturen, die mehrere Felder gleichzeitig setzen (z. B. ``if``-Blöcke), nicht verwendet werden.
   Wenn Sie Java-Klassen verwenden, schreiben Sie diese als einzelnen Ausdruck mit vollständig qualifiziertem Klassennamen (FQCN), und verwenden Sie für bedingte Werte den Ternäroperator pro Feld (zum Beispiel ``url=data.published ? data.url : null`` ).
   Der hier verwendete Variablenname ``data`` ist nur ein Beispiel; der tatsächliche Variablenname hängt vom verwendeten Datenspeicher-Konnektor ab. Details finden Sie unter :doc:`../admin/dataconfig-guide`.
   Schreiben Sie den Ausdruck ohne abschließendes Semikolon: Eine Zeile, die nur als Anweisungsblock geparst werden kann, wird zu ``null`` ausgewertet und das Feld bleibt ungesetzt — siehe :ref:`javascript-statement-null`.

Grundlegendes Mapping
----------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URL-Generierung
----------------

::

    // URL-Generierung basierend auf ID
    url="https://example.com/article/" + data.id

    // Kombination mehrerer Felder
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // Bedingte URL
    url=data.external_url || "https://example.com/default/" + data.id

Inhaltsverarbeitung
--------------------

::

    // HTML-Tags entfernen
    content=data.html_content.replace(/<[^>]+>/g, "")

    // Mehrere Felder kombinieren
    content=data.title + "\n" + data.description + "\n" + data.body

    // Längenbeschränkung
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

Datumsverarbeitung
--------------------

::

    // Datum parsen (Einzelausdruck mit FQCN; Java-Interoperabilität nutzt dieselbe Notation wie Groovy)
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // Konvertierung von Epochensekunden (kein L-Suffix für long-Literale erforderlich)
    lastModified=new Date(data.timestamp * 1000)

Verfügbare Objekte
===================

Die in Skripten verfügbaren Objekte variieren je nach Ausführungskontext.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Kontext
     - Objekt
     - Beschreibung
   * - Alle Kontexte
     - ``container``
     - DI-Container. Wird für den Zugriff auf Komponenten über ``container.getComponent("...")`` verwendet
   * - Geplante Aufgaben
     - ``executor``
     - Job-Ausführungssteuerung ( ``JobExecutor`` ). Erforderlich für die Unterstützung des Jobstopps
   * - Datenspeicher
     - (Connector-spezifisch)
     - Von jedem Datenspeicher bereitgestellte Datensatzvariablen. Der Variablenname hängt vom Konnektor ab
   * - Pfad-Mapping
     - ``url`` , ``matcher``
     - Die zu konvertierende URL-Zeichenkette und das Ergebnis des Regulärausdruck-Abgleichs ( ``Matcher`` ). Verfügbar, wenn die Ersetzung mit dem Namen einer registrierten Engine vorangestellt ist, z. B. ``javascript:`` (Aliase ``js:``, ``sai:``)
   * - Dokument-Boost
     - (Dokumentfelder)
     - Jedes Feld des Zieldokuments ist als Variable verfügbar (wird in Bedingungs- und Boost-Wert-Ausdrücken verwendet)

Geplante Aufgaben-Skripte
==========================

Beispiele für JavaScript-Skripte in geplanten Aufgaben.
In geplanten Aufgaben sind ``container`` und ``executor`` verfügbar.
Durch Übergabe von ``executor`` an die ``execute()``-Methode des Jobs wird die Jobstoppsteuerung aktiviert.

.. note::
   Ein geplantes Aufgaben-Skript wird als vollständiges Skript in einem einzigen Durchlauf ausgewertet.
   Die Skript-Engine versucht zunächst, es als Ausdruck zu kompilieren, und interpretiert es nur bei einem Fehlschlag als Block von Anweisungen neu. Daher können mehrzeilige Anweisungen, ``let`` / ``const``-Deklarationen, Kontrollstrukturen und eine ``return``-Anweisung auf oberster Ebene verwendet werden (Details siehe „Wie Skripte ausgewertet werden" oben).
   Die nachfolgenden Beispiele unter „Java-Klassen verwenden", „Zugriff auf Fess-Komponenten", „Fehlerbehandlung" und „Debugging und Protokollausgabe" setzen ebenfalls diesen vollständigen Skript-Kontext voraus.

Crawl-Aufgabe ausführen
-------------------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Bedingtes Crawling
--------------------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // Nur außerhalb der Geschäftszeiten crawlen
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

Mehrere Aufgaben nacheinander ausführen
-----------------------------------------

::

    const results = [];

    // Suggest aktualisieren
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // Crawl ausführen
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

Java-Klassen verwenden
========================

Innerhalb von JavaScript-Skripten können Sie dank der Java-Interoperabilität von Sai
(Nashorn) Java-Standardbibliotheken und Fess-Klassen direkt verwenden. JavaScript kennt
keine ``import``-Anweisung, daher werden Klassen stets mit ihrem vollständig
qualifizierten Namen (FQCN) geschrieben.

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

Datum und Uhrzeit
-------------------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

Dateioperationen
------------------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/pfad/zur/datei.txt")));

HTTP-Kommunikation
--------------------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   Der Zugriff auf externe Ressourcen beeinträchtigt die Leistung,
   halten Sie ihn daher auf ein Minimum.

Zugriff auf Fess-Komponenten
==============================

Sie können mit ``container`` auf Fess-Komponenten zugreifen.

System-Helfer
---------------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

Konfigurationswerte abrufen
------------------------------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

Suchen ausführen
-------------------

::

    const searchHelper = container.getComponent("searchHelper");
    // Suchparameter festlegen und Suche ausführen

Fehlerbehandlung
==================

JavaScript kennt keine ``import``-Anweisung, sodass die Platzierungsregeln von Groovy
hier keine Rolle spielen. Mit ``try-catch`` können Ausnahmen abgefangen und Job-Fehler
gesteuert werden.

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

Debugging und Protokollausgabe
================================

Protokollausgabe
-------------------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

Debug-Ausgabe
----------------

Um den Inhalt einer Variablen schnell zu überprüfen, wandeln Sie sie mit
``JSON.stringify`` in eine Zeichenkette um und protokollieren Sie diese.

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

Migration von Groovy
======================

Beachten Sie beim Portieren eines vorhandenen Groovy-Skripts nach JavaScript die
folgenden Unterschiede.

Genauigkeit arithmetischer Operationen
-----------------------------------------

Zahlenoperationen in JavaScript arbeiten immer mit doppelter Gleitkommagenauigkeit.
Der folgende Ausdruck liefert beispielsweise in Groovy die Ganzzahl ``34``, in
JavaScript jedoch die Gleitkommazahl ``34.0``.

::

    10 * boost1 + boost2

Der Rückgabetyp einer über die Java-Interoperabilität aufgerufenen Methode bleibt
dagegen unverändert Java-seitig erhalten, sodass ``content.length()`` weiterhin eine
Ganzzahl liefert.

Groovy-spezifische Syntax umschreiben
-----------------------------------------

Die folgende Groovy-spezifische Syntax muss für JavaScript umgeschrieben werden.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - Beschreibung
   * - ``1000L``
     - ``1000``
     - Der ``L``-Suffix für long-Literale entfällt; die Zahl wird unverändert geschrieben
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - Ein JavaScript-Array wird beim Übergeben an eine Methode mit Parametertyp
       ``String[]`` automatisch in ein Java-Array umgewandelt; ein Cast ist nicht nötig

Java-Interoperabilität
-------------------------

Die Notation für die Java-Interoperabilität entspricht der von Nashorn und unterscheidet
sich kaum von Groovy. Vollständig qualifizierte Konstruktoraufrufe wie
``new java.io.File(...)``, ``java.lang.System.getProperty(...)`` und
``new org.codelibs.fess.job.IndexExportJob()`` werden unverändert aufgelöst.

ES6-Syntax
-------------

Da die JavaScript-Engine von |Fess| als ECMAScript 6 läuft, können Sie ES6-Syntax wie
``let`` / ``const``, Arrow-Funktionen, Template-Literale, Destrukturierung, ``for...of``
und ``class`` verwenden. Optional Chaining (``?.``) und der Nullish-Coalescing-Operator
(``??``) sind jedoch Syntax ab ES2020 und stehen nicht zur Verfügung.

Best Practices
================

1. **Einfach halten**: Komplexe Logik vermeiden und lesbaren Code schreiben
2. **Standardwerte**: Anstelle des Elvis-Operators den logischen OR-Operator (``||``) verwenden
3. **Ausnahmebehandlung**: Unerwartete Fehler mit geeignetem try-catch behandeln
4. **Protokollausgabe**: Protokolle für einfacheres Debugging ausgeben
5. **Leistung**: Zugriff auf externe Ressourcen minimieren
6. **Zahlenoperationen**: Wo eine Ganzzahl erwartet wird, das Ergebnis eines Java-Interop-Methodenaufrufs direkt verwenden oder bei Bedarf explizit konvertieren

Referenzinformationen
=======================

- `MDN JavaScript-Referenz <https://developer.mozilla.org/de/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - Skripting-Übersicht
- :doc:`scripting-groovy` - Groovy-Skripting-Leitfaden (Plugin)
- :doc:`../admin/dataconfig-guide` - Datenspeicher-Konfigurationsleitfaden
- :doc:`../admin/scheduler-guide` - Scheduler-Konfigurationsleitfaden
