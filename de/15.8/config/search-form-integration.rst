==============
Platzierung von Suchformularen
==============

Methode zur Platzierung von Suchformularen
=================

Durch Platzierung eines Suchformulars auf einer bestehenden Website können Sie zu |Fess|-Suchergebnissen leiten.
Hier wird am Beispiel erklärt, wie |Fess| unter https://search.n2sm.co.jp/ aufgebaut wird und Suchformulare auf einzelnen Seiten einer bestehenden Website platziert werden.

Suchformular
---------

Platzieren Sie an der Stelle auf der Seite, wo Sie das Suchformular einfügen möchten, folgenden Code:

::

    <form id="searchForm" method="get" action="https://search.n2sm.co.jp/search/">
    <input id="query" type="text" name="q" maxlength="1000" autocomplete="off">
    <input type="submit" name="search" value="Suche">
    </form>

Passen Sie das Design entsprechend Ihrer Website an, indem Sie z. B. Klassennamen per class-Attribut hinzufügen und mit CSS nach Bedarf anpassen.
Ändern Sie die URL https://search.n2sm.co.jp/ zur URL Ihres aufgebauten |Fess|-Servers.

Das Suchwort wird als Parameter ``q`` an die Suchseite von |Fess| (``/search/``) gesendet.
Setzen Sie ``maxlength`` auf einen Wert, der ``query.max.length`` (Standardwert ``1000``) entspricht, der maximalen Suchwortlänge auf der |Fess|-Seite.


Vorschläge
--------

Sie können auch Vorschlagsfunktion für platzierte Suchformulare konfigurieren.
Zur Konfiguration fügen Sie folgenden Code vor </body> hinzu:

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.7.1.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v2/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "background-color": "#fff",
          "z-index": "10000"
        },
        minterm: 2,
        adjustWidthVal : 11,
        searchForm : $('#searchForm')
      });
    });
    </script>

Falls Ihre Website bereits jQuery verwendet, müssen Sie das jQuery-script-Element nicht hinzufügen.

Die Vorschlagsfunktion verwendet die Vorschlags-API von |Fess| (``/api/v2/suggest-words``).
Ändern Sie ``url`` entsprechend der URL Ihres aufgebauten |Fess|-Servers.

Die wichtigsten Optionen, die für ``suggestor`` angegeben werden können, sind die folgenden.

.. list-table:: Wichtigste suggestor-Optionen
   :header-rows: 1
   :widths: 25 75

   * - Option
     - Beschreibung
   * - ``ajaxinfo.url``
     - Die URL der Vorschlags-API. Geben Sie ``/api/v2/suggest-words`` Ihres |Fess|-Servers an.
   * - ``ajaxinfo.fn``
     - Ein Array von Feldnamen, aus denen Vorschläge bezogen werden. Sie können den Standardwert ``["_default", "content", "title"]`` unverändert verwenden.
   * - ``ajaxinfo.num``
     - Die maximale Anzahl der angezeigten Vorschlagskandidaten.
   * - ``ajaxinfo.lang``
     - Die Sprache zum Eingrenzen der Vorschlagskandidaten (optional).
   * - ``minterm``
     - Die minimale Anzahl von Eingabezeichen, bevor Vorschläge angefordert werden.
   * - ``adjustWidthVal``
     - Der Wert (in Pixeln), der zur Breite des Eingabefelds addiert wird, um die Breite des Vorschlagsbereichs anzupassen.
   * - ``searchForm``
     - Das Suchformular-Element, das gesendet wird, wenn ein Kandidat ausgewählt wird.
   * - ``boxCssInfo``
     - Das auf den Vorschlagsbereich angewendete CSS.
   * - ``listSelectedCssInfo``
     - Das auf den ausgewählten Kandidaten angewendete CSS (optional).
   * - ``listDeselectedCssInfo``
     - Das auf nicht ausgewählte Kandidaten angewendete CSS (optional).

Geben Sie für "z-index" einen Wert an, der sich nicht mit anderen Elementen überschneidet.

.. note::
    Wenn das Suchformular auf einer Seite platziert wird, deren Domain sich vom |Fess|-Server unterscheidet, wird die Anfrage an die Vorschlags-API zu einer Cross-Origin-Anfrage.
    |Fess| erlaubt standardmäßig alle Ursprünge (``api.cors.allow.origin=*``), sodass es ohne Anpassung funktioniert.
    Um den Zugriff einzuschränken, ändern Sie ``api.cors.allow.origin`` in ``fess_config.properties``.

.. note::
    ``/api/v2/suggest-words`` ist die von |Fess| selbst bereitgestellte API.
    Der in früheren Versionen verwendete Endpunkt ``/api/v1/suggest-words`` wird vom |Fess|-Kern nicht mehr bereitgestellt, und das Plugin ``fess-webapp-v1-api`` muss installiert werden, um ihn zu verwenden.
    Verwenden Sie für neue Installationen ``/api/v2/suggest-words``.
