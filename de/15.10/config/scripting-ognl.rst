====================
OGNL-Skriptleitfaden
====================

Überblick
=========

OGNL (Object-Graph Navigation Language) ist eine der in |Fess| verfügbaren Skript-Engines.
Sie wird vom Plugin ``fess-script-ognl`` bereitgestellt und hat den Bezeichner ``ognl``.

Ein OGNL-Skript ist ein einzelner Wertausdruck wie ``title + " - " + siteName`` oder
``content.length() > 0``. Es gibt keine Anweisungen, keine Kontrollstrukturen und kein
``return``. Verwenden Sie OGNL für kurze Ausdrücke, etwa bei Feldzuordnung, Dokument-Boost und
Pfadzuordnung. Für Skripte, die Anweisungen oder Schleifen benötigen, verwenden Sie
:doc:`scripting-javascript` oder :doc:`scripting-groovy`.

.. important::
   Das Plugin ist **nicht Teil der Distribution**. Installieren Sie es über die Seite
   System > Plugin in der Administrationsoberfläche oder mit
   ``bin/fess-setup install plugin fess-script-ognl``. Für eine manuelle Installation legen Sie
   die JAR-Datei (zum Beispiel ``fess-script-ognl-15.10.0.jar``) in ``app/WEB-INF/plugin/`` ab
   und starten |Fess| neu.

OGNL auswählen
==============

OGNL wird nur dort verwendet, wo der Skripttyp ausdrücklich ausgewählt wird.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Wo
     - So wählen Sie OGNL aus
   * - Datenspeicher
     - Fügen Sie ``script_type=ognl`` zu den Parametern der Datenspeicher-Konfiguration hinzu
   * - Web- und Datei-Crawling
     - Fügen Sie ``config.script.type=ognl`` zu den Konfigurationsparametern hinzu und schreiben
       Sie die Feldskripte als ``field.script.<Feld>=<Ausdruck>``
   * - Boost-Regel für Dokumente
     - Setzen Sie den Skripttyp der Regel auf ``ognl`` (jede Regel hat einen eigenen Skripttyp)
   * - Pfadzuordnung
     - Beginnen Sie den Ersatz mit ``ognl:``. Das Ergebnis des Ausdrucks wird zur Ersatz-URL; die
       ursprüngliche URL und der ``Matcher`` stehen als ``url`` und ``matcher`` zur Verfügung
   * - Geplanter Job
     - Setzen Sie den Skripttyp des Jobs auf ``ognl``. Ein Job ist normalerweise eine Prozedur,
       die sich nicht als einzelner Ausdruck formulieren lässt

Ausdrücke schreiben
===================

In Datenspeicher- und Feldskripten schreiben Sie pro Zeile ein ``Feld=Ausdruck``. Jeder Parameter
steht sowohl als ``name`` als auch als ``#name`` zur Verfügung.

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNL ist keine Teilmenge von Groovy. Beachten Sie beim Übertragen eines Skripts Folgendes:

- Es gibt kein ``return``, keine Anweisungen und kein ``if`` / ``for``. Verwenden Sie den
  ternären Operator ``cond ? a : b``.
- Der Elvis-Operator ``?:`` und der Safe-Navigation-Operator ``?.`` werden nicht unterstützt.
  Schreiben Sie ``a != null ? a.b : null``.
- ``"x${id}"`` ist kein Fehler und wird nicht interpoliert. Der Ausdruck ergibt die literale
  Zeichenkette ``x${id}``, sodass das Feld mit falschem Text indexiert wird. Verketten Sie
  stattdessen mit ``+``.

Einstellungen
=============

Die Engine liest die folgenden Schlüssel aus ``system.properties`` oder aus der
JVM-Systemeigenschaft ``-Dfess.system.<Schlüssel>``. Ist ein Schlüssel an beiden Stellen
gesetzt, hat ``system.properties`` Vorrang. ``system.properties`` ist im ZIP-Paket
``app/WEB-INF/conf/system.properties`` und in den RPM- und DEB-Paketen
``/etc/fess/system.properties``.

.. important::
   Die Schlüssel werden nur einmal gelesen, wenn die Engine beim Start initialisiert wird.
   Starten Sie |Fess| nach jeder Änderung neu; der laufende Prozess übernimmt die Änderung nicht.

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Schlüssel
     - Standard
     - Beschreibung
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` oder ``strict``. Siehe den nächsten Abschnitt. Jeder andere Wert wird als
       Warnung protokolliert und wie ``compat`` behandelt
   * - ``script.ognl.allowed.classes``
     - Siehe unten
     - Kommagetrennte Positivliste von Klassen. Wird nur im Modus ``strict`` verwendet
   * - ``script.ognl.denied.packages``
     - Siehe unten
     - Kommagetrennte Sperrliste deklarierender Klassen. Wird nur im Modus ``strict`` verwendet
   * - ``script.ognl.cache.size``
     - ``1000``
     - Maximale Anzahl zwischengespeicherter geparster Ausdrücke. Das Minimum ist ``1``
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - Maximale Zeichenanzahl eines Ausdrucks. Ein längerer Ausdruck wird nicht ausgewertet und
       schlägt fehl. Das Minimum ist ``1``
   * - ``script.ognl.max.log.length``
     - ``200``
     - Maximale Zeichenanzahl eines Ausdrucks in einer Protokollmeldung. Das Minimum ist ``3``

Ein Wert, der keine ganze Zahl ist, wird mit einer Warnung ignoriert, und der Standardwert wird
verwendet. Ein Wert unter dem Minimum wird mit einer Warnung auf das Minimum angehoben.

Die Modi compat und strict
==========================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` (Standard)
     - ``strict``
   * - DI-Container
     - Als ``container`` verfügbar
     - Nicht verfügbar (``container`` ergibt ``null``)
   * - Klassen
     - ``@beliebige.Klasse@methode(...)`` erreicht jede Klasse
     - Nur Klassen aus ``script.ognl.allowed.classes`` sind erreichbar
   * - Member
     - Keine Einschränkung
     - Member, die von einer Klasse aus ``script.ognl.denied.packages`` deklariert werden,
       können nicht aufgerufen werden. Nicht öffentliche Member werden immer abgelehnt

``compat`` behält das Verhalten bestehender Konfigurationen bei. Im Modus ``strict`` werden
Ausdrücke wie ``@java.lang.System@getProperty("user.name")`` oder
``new java.io.File("/etc/hosts")`` abgelehnt. Ein abgelehnter Ausdruck ergibt nicht ``null``;
stattdessen wird eine Warnung protokolliert, und die Auswertung schlägt mit einem Fehler fehl.

Beim Start protokolliert die Engine den wirksamen Modus auf der Stufe ``INFO``
(``ognl script engine: mode=strict, ...``). Prüfen Sie diese Zeile, um sicherzustellen, dass
``strict`` wirksam geworden ist.

Positivliste
------------

``script.ognl.allowed.classes`` vergleicht einen vollqualifizierten Klassennamen exakt oder einen
Paket- oder Klassennamen gefolgt von ``.``. So erlaubt ``java.time`` die Klasse
``java.time.LocalDate`` und alle Klassen unterhalb dieses Pakets. Der Standardwert lautet:

``java.lang.Math``, ``java.lang.String``, ``java.lang.Boolean``, ``java.lang.Integer``,
``java.lang.Long``, ``java.lang.Float``, ``java.lang.Double``, ``java.lang.Number``,
``java.util.Date``, ``java.util.Arrays``, ``java.util.List``, ``java.util.Map``,
``java.util.Set``, ``java.util.Collections``, ``java.math.BigDecimal``, ``java.time``,
``org.codelibs.core.lang.StringUtil``, ``org.codelibs.fess.util.DocumentUtil``,
``org.codelibs.fess.taglib.FessFunctions``

Der Name einer verschachtelten Klasse enthält ``$`` (zum Beispiel ``java.util.Map$Entry``) und
wird durch den Namen der umschließenden Klasse nicht erlaubt. Fügen Sie ihren Namen mit ``$`` zur
Liste hinzu, wenn Sie sie benötigen.

Sperrliste
----------

``script.ognl.denied.packages`` lehnt einen Member ab, wenn der Name der Klasse, die ihn
deklariert, mit einem der Einträge beginnt. Der Standardwert lautet:

``java.io``, ``java.nio``, ``java.net``, ``java.lang.reflect``, ``java.lang.invoke``,
``java.lang.System``, ``java.lang.Class``, ``java.lang.Runtime``, ``java.lang.ProcessBuilder``,
``java.lang.Process``, ``java.lang.Thread``, ``java.lang.ClassLoader``, ``javax.script``,
``jdk.``, ``sun.``, ``org.lastaflute.di``

.. note::
   Ein von Ihnen gesetzter Wert ersetzt die Standardliste; er wird nicht an sie angehängt. Um der
   Positivliste eine Klasse hinzuzufügen, schreiben Sie die Standardeinträge zusammen mit dem
   neuen Eintrag.

.. warning::
   Der Modus ``strict`` begrenzt, welche Klassen und Member ein Ausdruck erreichen kann. Er
   isoliert den Ausdruck nicht von den Objekten, die ihm übergeben werden. Wird ein |Fess|-Helper
   oder eine Entität als Parameter übergeben, können ihre öffentlichen Methoden in beiden Modi
   aus dem Ausdruck aufgerufen werden.
