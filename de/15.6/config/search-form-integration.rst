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


Vorschläge
--------

Sie können auch Vorschlagsfunktion für platzierte Suchformulare konfigurieren.
Zur Konfiguration fügen Sie folgenden Code vor </body> hinzu:

::

    <script type="text/javascript" src="https://search.n2sm.co.jp/js/jquery-3.6.3.min.js"></script>
    <script type="text/javascript" src="https://search.n2sm.co.jp/js/suggestor.js"></script>
    <script>
    $(function() {
      $('#query').suggestor({
        ajaxinfo : {
          url : 'https://search.n2sm.co.jp/api/v1/suggest-words',
          fn :  ["_default", "content", "title"],
          num : 10
        },
        boxCssInfo: {
          border: "1px solid rgba(82, 168, 236, 0.5)",
          "-webkit-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
          "-moz-box-shadow":
            "0 1px 1px 0px rgba(0, 0, 0, 0.1), 0 3px 2px 0px rgba(82, 168, 236, 0.2)",
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

Geben Sie für "z-index" einen Wert an, der sich nicht mit anderen Elementen überschneidet.
