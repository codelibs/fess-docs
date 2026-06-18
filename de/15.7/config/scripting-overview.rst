=====================================
Skripting-Übersicht
=====================================

Übersicht
=========

|Fess| ermöglicht es, in verschiedenen Situationen benutzerdefinierte Logik mithilfe von Skripten zu implementieren.
Durch den Einsatz von Skripten lassen sich Datenverarbeitung beim Crawling, URL-Transformationen
und die Ausführung geplanter Aufgaben flexibel steuern.

Unterstützte Skriptsprachen
============================

|Fess| unterstützt die folgenden Skriptsprachen:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Sprache
     - Bezeichner
     - Beschreibung
   * - Groovy
     - ``groovy``
     - Die standardmäßig registrierte Skriptsprache. Java-kompatibel mit leistungsstarken Funktionen

.. note::
   Das einzige standardmäßig in |Fess| registrierte Skript-Engine ist Groovy.
   Die Standardskriptsprache ist ``groovy`` (``Constants.DEFAULT_SCRIPT``).
   Alle Skriptbeispiele in dieser Dokumentation sind in Groovy-Syntax verfasst.

Anwendungsfälle für Skripte
============================

Datenspeicher-Konfiguration
----------------------------

Datenspeicher-Konnektoren verwenden Skripte, um abgerufene Daten auf Indexfelder abzubilden.
Die Konfiguration wird im Format ``Feldname=Ausdruck`` zeilenweise angegeben;
jede Zeile wird als eigenständiger Groovy-Ausdruck ausgewertet.

::

    url=site_url
    title=name
    content=description
    last_modified=updated_at

Die im Datenspeicher-Skript verfügbaren Variablennamen hängen vom jeweiligen Konnektor ab.
Bei CSV- und JSON-Datenspeichern sind die Spalten- bzw. Feldnamen direkt als Variablen
verfügbar (es wird kein gemeinsames Präfix wie ``data`` vorangestellt).
Bei dateibasierten Konnektoren (Box, Google Drive, OneDrive usw.) lautet das Präfix ``file.*``,
bei Slack ``message.*`` — das Präfix variiert je nach Konnektor.
Details zu den verfügbaren Variablen entnehmen Sie bitte der Dokumentation des jeweiligen
Datenspeicher-Konnektors.

.. note::
   Da jede Zeile eines Datenspeicher-Skripts als einzelner Ausdruck ausgewertet wird, sind
   mehrzeilige ``if``-Blöcke, ``import``-Anweisungen und ``def``-Variablendeklarationen
   nicht zulässig.
   Für wertabhängige Felder verwenden Sie den ternären Operator
   (z. B. ``title=enabled == "true" ? name : null``). Klassen werden über ihren
   vollständig qualifizierten Namen (FQCN) inline referenziert.

Pfad-Mapping
------------

Pfad-Mapping dient zur Normalisierung und Transformation von Crawling-URLs.
Standardmäßig wird es als Paar aus „Regulärem Ausdruck" und „Ersetzungszeichenkette"
konfiguriert — dies ist kein Groovy-Skript.
Beispielsweise ersetzt der reguläre Ausdruck ``http://`` mit der Ersetzungszeichenkette
``https://`` das URL-Schema.

Nur wenn der Ersetzungszeichenkette das Präfix ``groovy:`` vorangestellt wird, wird der
nachfolgende Teil als Groovy-Skript ausgewertet. In diesem Skript stehen ``url``
(die zu transformierende URL-Zeichenkette) und ``matcher``
(der ``java.util.regex.Matcher`` des regulären Ausdrucks) zur Verfügung.

::

    groovy:url.replaceAll("http://", "https://")

Geplante Aufgaben
-----------------

Bei geplanten Aufgaben kann benutzerdefinierte Verarbeitungslogik als Groovy-Skript verfasst
werden. Das gesamte Skript wird als ein einziges Groovy-Skript ausgewertet, sodass
mehrzeilige Anweisungen, ``import``-Anweisungen und ``def``-Variablendeklarationen
verwendet werden können.

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

Methoden wie ``logLevel("info")`` gehören zur Job-Klasse (``ExecJob`` und deren
Unterklassen) und können per Method-Chaining aufgerufen werden. Informationen zur
``executor``-Variablen finden Sie im Abschnitt „Ausführungskontext und verfügbare Objekte".

Grundlegende Syntax
===================

Im Folgenden finden Sie grundlegende Groovy-Syntaxbeispiele. Kommentare werden mit ``//``
(Zeilenkommentar) oder ``/* */`` (Blockkommentar) angegeben. Beachten Sie, dass Kommentare
mit ``#`` in Groovy nicht verwendet werden können.

Variablenzugriff
----------------

::

    // Datenspeicher-Feld (bei CSV/JSON über Spalten- bzw. Feldnamen zugreifen)
    title

    // Komponente aus dem DI-Container abrufen
    container.getComponent("systemHelper")

Zeichenkettenoperationen
------------------------

::

    // Verkettung
    title + " - " + category

    // Ersetzung
    content.replaceAll("old", "new")

    // Aufteilung
    tags.split(",")

Bedingte Verzweigung
--------------------

::

    // Ternärer Operator
    status == "active" ? "Aktiv" : "Inaktiv"

    // Standardwert bei null/leer (Elvis-Operator)
    description ?: "Keine Beschreibung"

Datumsoperationen
-----------------

::

    // Aktuelles Datum/Uhrzeit
    new Date()

    // Formatierung
    new java.text.SimpleDateFormat("yyyy-MM-dd").format(updated_at)

Ausführungskontext und verfügbare Objekte
==========================================

Die in einem Skript verfügbaren Objekte hängen vom jeweiligen Ausführungskontext ab.
Nur ``container`` ist in allen Kontexten verfügbar.

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Ausführungskontext
     - Verfügbare Objekte
     - Beschreibung
   * - Alle Kontexte
     - ``container``
     - DI-Container. Zugriff auf einzelne Komponenten über
       ``container.getComponent("systemHelper")`` oder
       ``container.getComponent("fessConfig")``
   * - Datenspeicher-Skript
     - Konnektor-spezifische Feldvariablen
     - Die vom Datenspeicher abgerufenen Felder stehen als Variablen zur Verfügung
       (Variablennamen und Präfixe variieren je nach Konnektor; bei CSV/JSON werden
       Feldnamen direkt als Variablen verwendet)
   * - Pfad-Mapping
     - ``url`` ``matcher``
     - Die zu transformierende URL-Zeichenkette und der ``Matcher`` des regulären Ausdrucks
       (nur bei Ersetzungen mit dem Präfix ``groovy:``)
   * - Geplante Aufgaben
     - ``executor``
     - Job-Ausführungsinstanz (``JobExecutor``). Wird zur Steuerung des Job-Shutdowns verwendet

.. note::
   Andere Objekte als ``container`` werden nur in bestimmten Kontexten injiziert.
   Beispielsweise ist ``executor`` ausschließlich in geplanten Aufgaben verfügbar und
   steht in Datenspeicher-Skripten oder beim Pfad-Mapping nicht zur Verfügung.

Sicherheit
==========

.. warning::
   Skripte besitzen weitreichende Fähigkeiten — verwenden Sie sie daher ausschließlich
   aus vertrauenswürdigen Quellen.

- Skripte werden auf dem Server ausgeführt
- Zugriff auf das Dateisystem und Netzwerk ist möglich
- Stellen Sie sicher, dass nur Benutzer mit Administratorrechten Skripte bearbeiten können
- Die Skriptausführung wird im Audit-Log (``audit.log``) protokolliert.
  Die Protokollierung wird über ``script.audit.log.enabled`` gesteuert; der Standardwert
  ist ``true``. Die maximale Länge der protokollierten Skriptzeichenkette wird über
  ``script.audit.log.max.length`` gesteuert; der Standardwert beträgt ``100`` Zeichen.

Leistung
========

Hinweise zur Optimierung der Skript-Leistung:

1. **Komplexe Verarbeitung vermeiden**: Datenspeicher-Skripte werden für jedes Dokument ausgeführt
2. **Zugriff auf externe Ressourcen minimieren**: Netzwerkaufrufe verursachen Verzögerungen
3. **Caching nutzen**: Erwägen Sie das Zwischenspeichern von wiederholt verwendeten Werten

Debugging
=========

Da Skripte für geplante Aufgaben als ein einziges Groovy-Skript ausgewertet werden, können
Protokollausgaben zum Debugging eingesetzt werden.
(Datenspeicher-Skripte werden zeilenweise als einzelne Ausdrücke ausgewertet, daher sind
``import``-Anweisungen und mehrzeilige Verarbeitungslogik dort nicht möglich.)

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("fess.script")
    logger.info("executor = {}", executor)

Das obige Beispiel verwendet einen Logger mit dem Namen ``fess.script``.
Um diese Protokollausgabe zu aktivieren, fügen Sie die entsprechende Logger-Konfiguration
in ``app/WEB-INF/classes/log4j2.xml`` ein.

::

    <Logger name="fess.script" level="DEBUG"/>

Um Debug-Protokolle der Skript-Engine selbst zu aktivieren, setzen Sie den Protokolllevel
des Pakets ``org.codelibs.fess.script`` auf ``DEBUG``.

::

    <Logger name="org.codelibs.fess.script" level="DEBUG"/>

Referenzinformationen
=====================

- :doc:`scripting-groovy` - Groovy-Skripting-Leitfaden
- :doc:`../admin/dataconfig-guide` - Datenspeicher-Konfigurationsleitfaden
- :doc:`../admin/scheduler-guide` - Scheduler-Konfigurationsleitfaden
