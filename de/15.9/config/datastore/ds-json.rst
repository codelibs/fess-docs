================
JSON-Konnektor
================

Übersicht
===========

Der JSON-Konnektor bietet die Funktionalität, Daten aus JSON-Dateien im lokalen
Dateisystem abzurufen und im |Fess|-Index zu registrieren.

Für diese Funktion ist das Plugin ``fess-ds-json`` erforderlich.

Es werden die folgenden drei Formate unterstützt; standardmäßig wird das Format
automatisch anhand des Dateiinhalts erkannt.

- JSON-Lines-Format (ein JSON-Objekt pro Zeile)
- Array von JSON-Objekten (sowohl formatiert/eingerückt als auch in einer einzigen
  Zeile möglich)
- ein einzelnes JSON-Objekt

Da die Datensätze einzeln eingelesen werden, wird selbst bei einem großen Array
niemals die gesamte Datei im Speicher gehalten.

.. note::

   Dieser Konnektor verarbeitet ausschließlich JSON-Dateien im lokalen Dateisystem.
   Ein entfernter Abruf, etwa über HTTP, wird nicht unterstützt; wird der Parameter
   ``urls`` angegeben, wird dieser nicht ignoriert, sondern führt zu einem Fehler.

Voraussetzungen
==================

1. Die Installation des Plugins ist erforderlich
2. Zugriffsrechte auf die JSON-Dateien sind erforderlich
3. Die Struktur der JSON-Daten muss bekannt sein

Plugin-Installation
----------------------

Methode 1: Installation über die Administrationsoberfläche

1. Öffnen Sie "System" -> "Plugins"
2. Laden Sie die JAR-Datei hoch
3. Starten Sie |Fess| neu

Methode 2: JAR-Datei direkt platzieren

::

    # Vom CodeLibs-Repository herunterladen
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Platzieren
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # oder
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   Ab Version 15.8.0 werden die JAR-Dateien über das
   `CodeLibs-Repository <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_
   bereitgestellt. Für Version 15.7.0 und früher finden Sie sie auf
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_.

Konfiguration
===============

Konfigurieren Sie über die Administrationsoberfläche unter "Crawler" -> "Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - Products JSON
   * - Handler-Name
     - JsonDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
---------------------------

Lokale Datei:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Mehrere Dateien:

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

Verzeichnisangabe:

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

Parameterliste
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - Parameter
     - Standardwert
     - Beschreibung
   * - ``files``
     -
     - Pfad zu den zu verarbeitenden JSON-Dateien (mehrere Angaben möglich: kommagetrennt). Die Dateien werden in der angegebenen Reihenfolge verarbeitet.
   * - ``directories``
     -
     - Pfad zu Verzeichnissen, die JSON-Dateien enthalten (mehrere Angaben möglich: kommagetrennt).
   * - ``recursive``
     - ``false``
     - Gibt an, ob ``directories`` auch in Unterverzeichnissen durchsucht wird.
   * - ``max_depth``
     - ``10``
     - Bei ``recursive=true`` die Anzahl der Verzeichnisebenen, bis zu der jeweils hinabgestiegen wird. Bei ``0`` entspricht das Verhalten ``recursive=false``.
   * - ``include_pattern``
     -
     - Regulärer Ausdruck, dem der absolute Pfad einer Datei vollständig entsprechen muss.
   * - ``exclude_pattern``
     -
     - Regulärer Ausdruck, dem der absolute Pfad einer Datei nicht entsprechen darf.
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - Zu verarbeitende Dateiendungen (mehrere Angaben möglich: kommagetrennt). Groß-/Kleinschreibung wird nicht unterschieden.
   * - ``file_encoding``
     - ``UTF-8``
     - Zeichenkodierung der Datei.
   * - ``format``
     - ``auto``
     - Format des Dokuments. Einer von ``auto``, ``jsonl`` oder ``json``.
   * - ``root_path``
     -
     - JSON Pointer, der die Position angibt, ab der Datensätze gelesen werden (Beispiel: ``/data/items``).

.. note::

   Die Parameternamen sind hier in snake_case angegeben; die entsprechende Schreibweise
   in camelCase (z. B. ``fileEncoding`` für ``file_encoding``) kann jedoch ebenso
   verwendet werden.

.. note::

   Geben Sie mindestens einen der Parameter ``files`` oder ``directories`` an.
   Sind beide leer, führt dies zu einem Fehler.
   Die beiden Parameter schließen sich nicht gegenseitig aus; werden beide angegeben,
   werden beide verarbeitet. Ist dieselbe Datei über beide Parameter erreichbar, wird
   sie dennoch nur einmal eingelesen.

Verarbeitungsreihenfolge der Dateien
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Die mit ``files`` angegebenen Dateien werden in der angegebenen Reihenfolge
  verarbeitet.
- Die unter ``directories`` gefundenen Dateien werden in aufsteigender Reihenfolge
  nach Änderungsdatum (älteste zuerst) verarbeitet.
- Die mit ``files`` angegebenen Dateien werden vor den Dateien unter ``directories``
  verarbeitet.

Die Einschränkung durch ``file_suffixes`` gilt auch für die direkt über ``files``
angegebenen Dateien. Dateien, deren Endung nicht übereinstimmt, werden übersprungen,
wobei der Grund im Log ausgegeben wird.

Ein nicht vorhandener Pfad, ein bei ``files`` angegebenes Verzeichnis oder eine bei
``directories`` angegebene Datei werden jeweils als Warnung im Log protokolliert;
das Crawling selbst wird fortgesetzt.

``format``
-------------

``auto`` liest den Anfang des Dokuments und bestimmt das Format anhand seiner Syntax.
Bei einer korrekt geschriebenen Datei lässt sich das Format so unabhängig davon
erkennen, um welches der drei Formate es sich handelt.

``format=jsonl`` sollten Sie explizit angeben, wenn es sich um eine Datei im
JSON-Lines-Format handelt, bei der die Zeilen nahe dem Dateianfang möglicherweise
beschädigt sind (z. B. Banner-Zeilen, Fortschrittsprotokolle oder durch einen
abgebrochenen Transfer unvollständige Datensätze). Die automatische Erkennung müsste
solche Zeilen überspringen, um das Format zu bestimmen.

Diese Einstellung bestimmt zugleich, wie weit sich ein fehlerhafter Datensatz
auswirkt.

- **JSON-Lines-Format**: Da jede Zeile unabhängig geparst wird, betrifft eine
  fehlerhafte Zeile ausschließlich diese Zeile selbst. Der Fehler wird unter dem
  Schlüssel ``<absoluter Dateipfad>@<Zeilennummer>`` als Fehler-URL erfasst, und die
  Verarbeitung wird ab der nächsten Zeile unverändert fortgesetzt.
- **Alle anderen Formate**: Da die Datei als Token-Stream eingelesen wird, kann ein
  einzelner Fehler nachfolgende Datensätze in Mitleidenschaft ziehen. Ein Dokument,
  das mitten in einem Objekt abbricht, kann sich davon nicht mehr erholen; schlägt die
  Verarbeitung eine bestimmte Anzahl Mal in Folge fehl, wird die betreffende Datei mit
  einer Warnung abgebrochen.

``root_path``
----------------

Geben Sie einen JSON Pointer an, der auf ein verschachteltes Array zeigt, werden
dessen Elemente als Datensätze registriert.

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- Zeigt der Pointer auf ein Array, wird jedes seiner Elemente zu einem Datensatz.
- Zeigt der Pointer auf ein Objekt, wird dieses Objekt zu einem einzigen Datensatz.
- Trifft der Pointer auf nichts zu, führt dies nicht zu einem Fehler, sondern zu
  0 Datensätzen.
- Die JSON-Pointer-Escape-Sequenzen (``~1`` für ``/`` und ``~0`` für ``~``) können
  verwendet werden.

``root_path`` hat Vorrang vor ``format``. Ein über einen JSON Pointer erreichtes
Dokument wird nicht zeilenweise eingelesen; wird ``root_path`` zusammen mit
``format=jsonl`` angegeben, wird dazu eine entsprechende Warnung im Log ausgegeben.

.. warning::

   ``root_path`` muss mit ``/`` beginnen. Fehlt das führende ``/`` wie bei
   ``data/items``, kann der Wert nicht als JSON Pointer interpretiert werden, und die
   gesamte Datenspeicher-Konfiguration schlägt mit einem Fehler fehl. Die Fehler-URL
   wird in diesem Fall nicht unter dem Parameternamen, sondern unter der
   Datenspeicher-Konfiguration selbst erfasst; welcher Parameter die Ursache ist,
   lässt sich daher nur anhand von
   ``JSON Pointer expression must start with '/'`` im Log erkennen.

.. note::

   Wird ein über mehrere Zeilen formatiertes Dokument (ein sogenanntes
   Wrapper-Format, das Metainformationen und ein Array enthält) ohne Angabe von
   ``root_path`` eingelesen, wird versucht, es zeilenweise zu parsen; die
   beabsichtigten Datensätze werden dabei nicht erfasst, und es wird ein Fehler
   aufgezeichnet. Geben Sie für solche Dokumente ``root_path`` an.

Skript-Einstellungen
------------------------

Die Werte der einzelnen Felder werden unter Bezugnahme auf die Werte der Felder des
JSON-Objekts zusammengesetzt. Auf die Felder der obersten Ebene des JSON-Objekts kann
im Skript direkt als **Variablen ohne Präfix** zugegriffen werden (es wird kein
Präfix wie ``data.`` verwendet).

Einfaches JSON-Objekt:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

Verschachtelte Objekte können als Map, verschachtelte Arrays als Liste referenziert
werden:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

Verfügbare Felder
~~~~~~~~~~~~~~~~~~~~

- ``<Feldname>`` - direkter Zugriff auf ein Feld der obersten Ebene des
  JSON-Objekts über seinen Namen
- ``<Elternteil>.<Kind>`` - Feld eines verschachtelten Objekts
- ``<Array>[<Index>]`` - Array-Element

.. note::

   Ist der Wert eines Feldes ``null``, wird dieses Feld nicht im Dokument
   registriert.

.. note::

   In |Fess| 15.9 ist JavaScript die eingebaute Skript-Engine. Groovy wird als
   Plugin ``fess-script-groovy`` bereitgestellt. Welche Engine verwendet wird, geben
   Sie über den Datenspeicher-Parameter ``script_type`` an (z. B.
   ``script_type=javascript``). Wird der Parameter weggelassen, wird ``groovy``
   verwendet. Einfache Verweise und Zeichenkettenverkettungen wie in den obigen
   Beispielen funktionieren mit beiden Engines auf dieselbe Weise; darüber
   hinausgehende Notationen unterscheiden sich jedoch je nach Engine.

Hinweise
==========

Parameter, deren Name auf ``app.encrypt.property.pattern`` passt (standardmäßig
Namen, die auf ``password``, ``key``, ``token`` oder ``secret`` enden), werden im
Skript als ``null`` referenziert. Dies verhindert, dass in den
Datenspeicher-Parametern hinterlegte Zugangsdaten in ein Indexfeld kopiert werden.

Existiert auf Seiten des Datensatzes ein Feld mit demselben Namen, hat wie bei den
übrigen Parametern der Wert aus dem Datensatz Vorrang.

.. note::

   Der Abgleich erfolgt als vollständige, groß-/kleinschreibungssensitive
   Übereinstimmung mit dem Parameternamen. ``access_token`` wird erfasst, das in
   camelCase geschriebene ``accessToken`` hingegen nicht. Notieren Sie Zugangsdaten
   in Parametern daher in snake_case.

Fehlerhafte Parameter und Fehler
===================================

Wird für ``format``, ``include_pattern``, ``exclude_pattern`` oder ``urls`` ein
ungültiger Wert angegeben, endet das Crawling bereits vor dem Einlesen der Dateien,
und es wird eine Fehler-URL erfasst, die den Parameternamen enthält (Beispiel:
``JsonDataStore:format``).

Wird für ``max_depth`` ein nicht-numerischer Wert angegeben, wird dies im Log
vermerkt, und es wird der Standardwert verwendet.

.. note::

   Ein Datenspeicher-Crawling wird als Job selbst dann erfolgreich beendet, wenn
   kein einziger Datensatz abgerufen werden konnte. Weicht die Anzahl der
   abgerufenen Datensätze von der Erwartung ab, überprüfen Sie die Anzahl der
   Dokumente im Index, die Fehler-URLs sowie ``fess-crawler.log``.

Anwendungsbeispiele
======================

Produktkatalog
------------------

Parameter:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

Skript:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

Als Datei gespeicherte API-Antwort
--------------------------------------

Parameter:

::

    files=/var/data/response.json
    root_path=/data/items

Skript:

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

Rekursive Verarbeitung eines Verzeichnisses
-----------------------------------------------

Parameter:

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

Fehlerbehebung
================

Datei nicht gefunden
------------------------

**Symptom**: Im Log wird ``... does not exist.``, ``... is not a file.`` oder
``... is skipped because its suffix is not one of ...`` ausgegeben

**Zu überprüfen**:

1. Überprüfen Sie, ob der Dateipfad korrekt ist
2. Überprüfen Sie, ob die Datei existiert
3. Überprüfen Sie, ob die Dateiendung mit ``file_suffixes`` (standardmäßig
   ``.json`` oder ``.jsonl``) übereinstimmt
4. Überprüfen Sie, ob der |Fess|-Ausführungsbenutzer über Leserechte verfügt

JSON-Analysefehler
----------------------

**Symptom**: Im Log wird ``Failed to parse ...`` oder ``Failed to read ...``
ausgegeben, oder es wird eine Fehler-URL erfasst

**Zu überprüfen**:

1. Prüfen Sie, ob die Datei gültiges JSON enthält

   ::

       # Bei JSON-Lines-Format: prüfen, ob jede Zeile ein gültiges JSON-Objekt ist
       cat data.jsonl | jq -c .

       # Bei Array oder einzelnem Objekt
       jq . data.json

2. Überprüfen Sie, ob die Zeichenkodierung korrekt ist
3. Überprüfen Sie, ob die Datei nicht abgeschnitten ist
4. Überprüfen Sie, ob Kommentare enthalten sind (Kommentare sind im JSON-Standard
   nicht zulässig)

Keine Daten abrufbar
------------------------

**Symptom**: Das Crawling ist erfolgreich, die Anzahl beträgt jedoch 0

**Zu überprüfen**:

1. Wenn ``root_path`` angegeben ist, überprüfen Sie, ob der JSON Pointer mit der
   Struktur des Dokuments übereinstimmt (bei fehlender Übereinstimmung entsteht kein
   Fehler, sondern es werden 0 Datensätze erzeugt)
2. Überprüfen Sie, ob durch ``include_pattern``, ``exclude_pattern`` oder
   ``file_suffixes`` sämtliche Dateien ausgeschlossen wurden. In diesem Fall wird im
   Log ``No sources to process`` ausgegeben
3. Überprüfen Sie die Skript-Einstellungen (ob Feldverweise ohne ``data.``-Präfix
   angegeben sind)
4. Überprüfen Sie die Feldnamen (einschließlich Groß-/Kleinschreibung)
5. Überprüfen Sie, ob ``url`` korrekt zusammengesetzt wird. Ist ``url`` leer,
   schlägt der jeweilige Datensatz fehl

Zeichenkodierungsprobleme
-----------------------------

**Symptom**: Die Zeichen im registrierten Dokument sind verstümmelt

Geben Sie bei ``file_encoding`` eine existierende, aber falsche Kodierung an, tritt
kein Fehler auf, und das Dokument wird mit verstümmelten Zeichen registriert.
Überprüfen Sie die tatsächliche Zeichenkodierung der Datei. Geben Sie einen nicht
existierenden Kodierungsnamen an, wird für jede Datei eine Fehler-URL erfasst.

Große JSON-Dateien
----------------------

**Symptom**: Speichermangel oder Zeitüberschreitung

Da die Datensätze einzeln eingelesen werden, wirkt sich die Gesamtgröße der Datei
nicht direkt auf den Speicherverbrauch aus. Probleme können jedoch auftreten, wenn
ein einzelner Datensatz extrem groß ist oder die Last bei der Indexierung sehr hoch
ist.

**Lösung**:

1. Teilen Sie die JSON-Datei in mehrere Dateien auf
2. Erhöhen Sie die Heap-Größe von |Fess|

Weiterführende Informationen
===============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-csv` - CSV-Konnektor
- :doc:`ds-database` - Datenbank-Konnektor
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
