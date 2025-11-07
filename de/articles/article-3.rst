========================================================
Fess Elasticsearch-basierter Suchserver erstellen ~ API-Edition
========================================================

Einleitung
========

Diesmal stellen wir vor, wie Sie die von Fess bereitgestellte API verwenden, um clientseitig (browserseitig) eine Suche durchzuführen und die Ergebnisse anzuzeigen.
Durch die Verwendung der API können Sie Fess als Suchserver in bestehende Websysteme integrieren und nur durch Änderung von HTML einbinden.

Dieser Artikel verwendet Fess 15.3.0 zur Erklärung.
Informationen zur Einrichtung von Fess finden Sie in der `Einführung <https://fess.codelibs.org/ja/articles/article-1.html>`__.

Zielgruppe
========

-  Personen, die bestehenden Websystemen Suchfunktionen hinzufügen möchten

Erforderliche Umgebung
==========

Der Inhalt dieses Artikels wurde in folgender Umgebung getestet:

-  Google Chrome 120 oder höher

JSON API
========

Fess kann neben der normalen HTML-basierten Suchdarstellung auch Suchergebnisse als JSON über eine API bereitstellen.
Mit der API können Sie einen Fess-Server einrichten und von bestehenden Systemen aus einfach nur Suchergebnisse abfragen.
Da Suchergebnisse in einem von der Entwicklungssprache unabhängigen Format verarbeitet werden können, sollte es einfach sein, Fess auch in Nicht-Java-Systeme zu integrieren.

Informationen darüber, welche Art von Antwort die von Fess bereitgestellte API zurückgibt, finden Sie unter `JSON-Antwort <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Fess verwendet OpenSearch als interne Suchmaschine.
OpenSearch bietet auch eine JSON-basierte API, aber die API von Fess ist davon verschieden.
Der Vorteil der Verwendung der Fess-API gegenüber der OpenSearch-API besteht darin, dass Sie durch die Verwendung der Fess-API verschiedene Fess-spezifische Funktionen wie die Verwaltung von Suchprotokollen und die Kontrolle von Zugriffsrechten nutzen können.
Wenn Sie einen Dokumenten-Crawl-Mechanismus von Grund auf neu entwickeln möchten, ist OpenSearch wahrscheinlich besser geeignet. Wenn Sie jedoch einfach Suchfunktionen hinzufügen möchten, können Sie mit Fess viele Entwicklungskosten einsparen.

Aufbau einer Suchseite mit JSON API
==================================

Diesmal erklären wir, wie Sie eine Website mit der Fess-API aufbauen.
Für die Kommunikation mit dem Fess-Server verwenden wir JSON-Antworten.
Der in diesem Fall verwendete Fess-Server ist ein vom Fess-Projekt öffentlich bereitgestellter Demo-Fess-Server.
Wenn Sie einen eigenen Fess-Server verwenden möchten, installieren Sie Fess 15.3.0 oder höher.

JSON und CORS
-----------

Beim Zugriff auf JSON müssen Sie die Same-Origin-Policy beachten.
Dadurch kann JSON verwendet werden, wenn der Server, der das im Browser anzuzeigende HTML ausgibt, und der Fess-Server sich in derselben Domain befinden. Wenn sie jedoch unterschiedlich sind, müssen Sie CORS (Cross-Origin Resource Sharing) verwenden.
Diesmal gehen wir von dem Fall aus, dass der Server, auf dem sich das HTML befindet, und der Fess-Server sich in unterschiedlichen Domains befinden.
Fess unterstützt CORS und die Konfigurationswerte können in app/WEB-INF/classes/fess_config.properties festgelegt werden. Standardmäßig ist Folgendes konfiguriert:

::

    api.cors.allow.origin=*
    api.cors.allow.methods=GET, POST, OPTIONS, DELETE, PUT
    api.cors.max.age=3600
    api.cors.allow.headers=Origin, Content-Type, Accept, Authorization, X-Requested-With
    api.cors.allow.credentials=true

Diesmal verwenden wir die Standardkonfiguration. Wenn Sie die Konfiguration ändern, starten Sie Fess neu.


Zu erstellende Dateien
----------------

Diesmal implementieren wir die Suchverarbeitung mit JavaScript in HTML.
Wir verwenden jQuery als JavaScript-Bibliothek.
Die zu erstellenden Dateien sind die folgenden:

-  HTML-Datei „index.html" zur Anzeige von Suchformular und Suchergebnissen

- JS-Datei „fess.js" zur Kommunikation mit dem Fess-Server

In diesem Aufbaubeispiel haben wir die folgenden Funktionen implementiert:

-  Senden von Suchanfragen über die Suchschaltfläche

-  Liste der Suchergebnisse

-  Paginierung der Suchergebnisse

HTML-Dateierstellung
------------------

Erstellen Sie zunächst HTML zur Anzeige von Suchformular und Suchergebnissen.
Diesmal ist die Tag-Struktur einfach gehalten, ohne CSS-Design-Anpassungen, um sie leicht verständlich zu machen.
Die zu verwendende HTML-Datei ist die folgende:

Inhalt von index.html
::

    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Suchseite</title>
    </head>
    <body>
    <div id="header">
      <form id="searchForm">
        <input id="searchQuery" type="text" name="query" size="30"/>
        <input id="searchButton" type="submit" value="Suche"/>
        <input id="searchStart" type="hidden" name="start" value="0"/>
        <input id="searchNum" type="hidden" name="num" value="20"/>
      </form>
    </div>
    <div id="subheader"></div>
    <div id="result"></div>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="fess.js"></script>
    </body>
    </html>

Betrachten wir den Bereich unterhalb des body-Tags: Zunächst werden im div-Tag mit dem id-Attribut header das Sucheingabefeld und die Suchschaltfläche platziert.
Außerdem werden die Anzeigestartposition (start) und die Anzahl der anzuzeigenden Ergebnisse (num) in versteckten Formularen gespeichert.
Die Werte von start und num werden nach dem Senden der Suchanfrage von JavaScript aktualisiert.
Die Anzahl der anzuzeigenden Ergebnisse ist jedoch die Anzahl pro Seite, und im heutigen Beispielcode gibt es keine Funktion zum Ändern der Anzahl der anzuzeigenden Ergebnisse, sodass der Wert von num nicht geändert wird.

Im nächsten subheader-div-Tag werden Informationen wie die Anzahl der Treffer angezeigt.
Im result-div-Tag werden Suchergebnisse und Paginierungslinks angezeigt.

Schließlich laden wir die jQuery-JS-Datei und das heute erstellte JavaScript „fess.js".
Sie können die jQuery-JS-Datei auch im selben Verzeichnis wie „index.html" speichern, aber diesmal rufen wir sie über das Google CDN ab.

JS-Dateierstellung
----------------

Als nächstes erstellen wir die JS-Datei „fess.js", die mit dem Fess-Server kommuniziert und Suchergebnisse anzeigt.
Erstellen Sie „fess.js" mit dem folgenden Inhalt und platzieren Sie es im selben Verzeichnis wie „index.html".

Inhalt von fess.js
::

    $(function(){
        // (1) Fess URL
        var baseUrl = "http://SERVERNAME:8080/api/v1/documents?q=";
        // (2) jQuery-Objekt der Suchschaltfläche
        var $searchButton = $('#searchButton');

        // (3) Suchverarbeitungsfunktion
        var doSearch = function(event){
          // (4) Anzeigestartposition, Anzahl der anzuzeigenden Ergebnisse abrufen
          var start = parseInt($('#searchStart').val()),
              num = parseInt($('#searchNum').val());
          // Prüfung der Anzeigestartposition
          if(start < 0) {
            start = 0;
          }
          // Prüfung der Anzahl der anzuzeigenden Ergebnisse
          if(num < 1 || num > 100) {
            num = 20;
          }
          // (5) Abrufen der Seiteninformationen
          switch(event.data.navi) {
            case -1:
              // Vorherige Seite
              start -= num;
              break;
            case 1:
              // Nächste Seite
              start += num;
              break;
            default:
            case 0:
              start = 0;
              break;
          }
          // Wert des Suchfelds trimmen und speichern
          var searchQuery = $.trim($('#searchQuery').val());
          // (6) Prüfung auf leeres Suchformular
          if(searchQuery.length != 0) {
            var urlBuf = [];
            // (7) Suchschaltfläche deaktivieren
            $searchButton.attr('disabled', true);
            // (8) URL-Konstruktion
            urlBuf.push(baseUrl, encodeURIComponent(searchQuery),
              '&start=', start, '&num=', num);
            // (9) Suchanfrage senden
            $.ajax({
              url: urlBuf.join(""),
              dataType: 'json',
            }).done(function(data) {
              // Suchergebnisverarbeitung
              var dataResponse = data.response;
              // (10) Statusprüfung
              if(dataResponse.status != 0) {
                alert("Bei der Suche ist ein Problem aufgetreten. Bitte wenden Sie sich an den Administrator.");
                return;
              }

              var $subheader = $('#subheader'),
                  $result = $('#result'),
                  record_count = dataResponse.record_count,
                  offset = 0,
                  buf = [];
              if(record_count == 0) { // (11) Keine Suchergebnisse
                // Ausgabe in den Subheader-Bereich
                $subheader[0].innerHTML = "";
                // Ausgabe in den Ergebnisbereich
                buf.push("<b>", dataResponse.q, "</b> - Keine übereinstimmenden Informationen gefunden.");
                $result[0].innerHTML = buf.join("");
              } else { // (12) Suchtreffer
                var page_number = dataResponse.page_number,
                    startRange = dataResponse.start_record_number,
                    endRange = dataResponse.end_record_number,
                    i = 0,
                    max;
                offset = startRange - 1;
                // (13) Ausgabe in den Subheader
                buf.push("<b>", dataResponse.q, "</b> - Suchergebnisse ",
                  record_count, " Treffer, ", startRange, " - ",
                  endRange, " angezeigt (", dataResponse.exec_time,
                    " Sekunden)");
                $subheader[0].innerHTML = buf.join("");

                // Ergebnisbereich leeren
                $result.empty();

                // (14) Ausgabe der Suchergebnisse
                var $resultBody = $("<ol/>");
                var results = dataResponse.result;
                for(i = 0, max = results.length; i < max; i++) {
                  buf = [];
                  buf.push('<li><h3 class="title">', '<a href="',
                    results[i].url_link, '">', results[i].title,
                    '</a></h3><div class="body">', results[i].content_description,
                    '<br/><cite>', results[i].site, '</cite></div></li>');
                  $(buf.join("")).appendTo($resultBody);
                }
                $resultBody.appendTo($result);

                // (15) Ausgabe der Seitenzahlinformationen
                buf = [];
                buf.push('<div id="pageInfo">', page_number, '. Seite<br/>');
                if(dataResponse.prev_page) {
                  // Link zur vorherigen Seite
                  buf.push('<a id="prevPageLink" href="#">&lt;&lt;Vorherige Seite</a> ');
                }
                if(dataResponse.next_page) {
                  // Link zur nächsten Seite
                  buf.push('<a id="nextPageLink" href="#">Nächste Seite&gt;&gt;</a>');
                }
                buf.push('</div>');
                $(buf.join("")).appendTo($result);
              }
              // (16) Aktualisierung der Seiteninformationen
              $('#searchStart').val(offset);
              $('#searchNum').val(num);
              // (17) Seitenanzeige nach oben verschieben
              $(document).scrollTop(0);
            }).always(function() {
              // (18) Suchschaltfläche aktivieren
              $searchButton.attr('disabled', false);
            });
          }
          // (19) False zurückgeben, um nicht zu submitten
          return false;
        };

        // (20) Verarbeitung, wenn Enter im Sucheingabefeld gedrückt wird
        $('#searchForm').submit({navi:0}, doSearch);
        // (21) Verarbeitung, wenn der Link zur vorherigen Seite gedrückt wird
        $('#result').on("click", "#prevPageLink", {navi:-1}, doSearch)
        // (22) Verarbeitung, wenn der Link zur nächsten Seite gedrückt wird
          .on("click", "#nextPageLink", {navi:1}, doSearch);
      });

Die Verarbeitung von „fess.js" wird nach dem Aufbau des DOM der HTML-Datei ausgeführt.
Zunächst wird bei 1 die URL des aufgebauten Fess-Servers angegeben.

Bei 2 wird das jQuery-Objekt der Suchschaltfläche gespeichert.
Da wir das jQuery-Objekt der Suchschaltfläche mehrmals verwenden, speichern wir es in einer Variablen zur Wiederverwendung.

Bei 3 wird die Suchverarbeitungsfunktion definiert. Der Inhalt dieser Funktion wird im nächsten Abschnitt erklärt.

Bei 20 wird das Ereignis registriert, wenn das Suchformular gesendet wird.
Die bei 20 registrierte Verarbeitung wird ausgeführt, wenn die Suchschaltfläche gedrückt wird oder wenn die Eingabetaste im Sucheingabefeld gedrückt wird.
Wenn das Ereignis auftritt, wird die Suchverarbeitungsfunktion doSearch aufgerufen.
Der Wert von navi wird beim Aufruf der Suchverarbeitungsfunktion übergeben und für die Paginierung verwendet.

Bei 21 und 22 werden Ereignisse registriert, wenn die in der Paginierung hinzugefügten Links angeklickt werden.
Diese Links werden dynamisch hinzugefügt, daher müssen die Ereignisse mit delegate registriert werden.
Bei diesen Ereignissen wird auch wie bei 20 die Suchverarbeitungsfunktion aufgerufen.

Suchverarbeitungsfunktion doSearch
--------------------

Erklärung der Suchverarbeitungsfunktion doSearch bei 3.

Bei 4 werden Anzeigestartposition und Anzahl der anzuzeigenden Ergebnisse abgerufen.
Diese Werte werden als versteckte Werte im Suchformular im Header-Bereich gespeichert.
Es wird erwartet, dass die Anzeigestartposition größer oder gleich 0 ist und die Anzahl der anzuzeigenden Ergebnisse zwischen 1 und 100 liegt. Wenn andere Werte abgerufen werden, werden Standardwerte festgelegt.

Bei 5 wird der beim Registrieren des doSearch-Ereignisses übergebene Parameter navi bewertet und die Anzeigestartposition korrigiert.
Hier bedeutet -1 Bewegung zur vorherigen Seite, 1 Bewegung zur nächsten Seite und alles andere Bewegung zur ersten Seite.

Bei 6 wird geprüft, ob der Wert im Sucheingabefeld eingegeben wurde. Wenn ja, wird die Suche ausgeführt. Wenn leer, wird die Verarbeitung ohne weitere Aktionen beendet.

Bei 7 wird die Suchschaltfläche während der Abfrage an den Fess-Server deaktiviert, um Doppelsubmits zu verhindern.

Bei 8 wird die URL für die Ajax-Anfrage zusammengestellt.
Suchbegriff, Anzeigestartposition und Anzahl der anzuzeigenden Ergebnisse werden mit der URL von 1 kombiniert.

Bei 9 wird die Ajax-Anfrage gesendet.
Wenn die Anfrage normal zurückkehrt, wird die success-Funktion ausgeführt.
Das Argument von success erhält das vom Fess-Server zurückgegebene Suchergebnisobjekt.

Zunächst wird bei 10 der Inhalt des Antwortstatus überprüft.
Wenn die Suchanfrage normal verarbeitet wurde, ist er auf 0 gesetzt.
Details zur JSON-Antwort von Fess finden Sie auf der `Fess-Website <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Wenn die Suchanfrage normal verarbeitet wurde, aber keine Suchergebnisse gefunden wurden, wird im Bedingungsblock 11 der Inhalt des subheader-Bereichs geleert und im result-Bereich eine Meldung angezeigt, dass keine Suchergebnisse gefunden wurden.

Wenn Suchergebnisse gefunden wurden, wird im Bedingungsblock 12 die Verarbeitung der Suchergebnisse durchgeführt.
Bei 13 werden Meldungen zur Anzahl der anzuzeigenden Ergebnisse und Ausführungszeit im subheader-Bereich festgelegt.
Bei 14 werden Suchergebnisse dem result-Bereich hinzugefügt.
Suchergebnisse sind als Array in data.response.result gespeichert.
Durch Zugriff auf results[i].〜 können Sie Feldwerte der Suchergebnisdokumente abrufen.

Bei 15 werden die aktuell angezeigte Seitenzahl und Links zur vorherigen und nächsten Seite dem result-Bereich hinzugefügt.
Bei 16 werden die aktuelle Anzeigestartposition und Anzahl der anzuzeigenden Ergebnisse im versteckten Feld des Suchformulars gespeichert.
Anzeigestartposition und Anzahl der anzuzeigenden Ergebnisse werden bei der nächsten Suchanfrage erneut verwendet.

Als nächstes wird bei 17 die Anzeigeposition der Seite geändert.
Wenn der Link zur nächsten Seite angeklickt wird, wird die Seite selbst nicht aktualisiert, daher wird mit scrollTop zum Seitenanfang verschoben.

Bei 18 wird die Suchschaltfläche nach Abschluss der Suchverarbeitung aktiviert.
Sie wird so eingestellt, dass sie mit complete aufgerufen wird, egal ob die Anfrage erfolgreich oder fehlgeschlagen ist.

Bei 19 wird false zurückgegeben, um zu verhindern, dass das Formular oder die Links nach dem Aufruf der Suchverarbeitungsfunktion gesendet werden.
Dadurch wird verhindert, dass eine Seitennavigation auftritt.

Ausführung
----

Greifen Sie mit einem Browser auf „index.html" zu.
Das Suchformular wird wie folgt angezeigt.

Suchformular
|image1|

Geben Sie einen beliebigen Suchbegriff ein und klicken Sie auf die Suchschaltfläche, um Suchergebnisse anzuzeigen.
Die Standardanzahl der anzuzeigenden Ergebnisse beträgt 20, aber wenn die Anzahl der Treffer groß ist, wird unter der Suchergebnisliste ein Link zur nächsten Seite angezeigt.

Suchergebnisse
|image2|

Zusammenfassung
======

Wir haben eine jQuery-basierte Client-Suchseite mit der JSON API von Fess aufgebaut.
Durch die Verwendung der JSON API können Sie Systeme aufbauen, die Fess nicht nur von browserbasierten Anwendungen, sondern auch von anderen Anwendungen aus nutzen.

Beachten Sie, dass der Beispielcode in diesem Artikel das herkömmliche API-Endpunkt-Format zeigt, aber für Fess 15.3 wird die Verwendung des ``/api/v1/documents``-Endpunkts empfohlen.
Details finden Sie in der `API-Spezifikation <https://fess.codelibs.org/ja/15.3/api/api-search.html>`__.

Referenzmaterialien
========

-  `Fess <https://fess.codelibs.org/ja/>`__

-  `jQuery <http://jquery.com/>`__

.. |image0| image:: ../../resources/images/ja/article/4/sameorigin.png
.. |image1| image:: ../../resources/images/ja/article/4/searchform.png
.. |image2| image:: ../../resources/images/ja/article/4/searchresult.png
