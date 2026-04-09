===========================================================================
Aufbau eines Elasticsearch-basierten Suchservers mit Fess — FSS-Ausgabe
===========================================================================

Einleitung
==========

In diesem Artikel wird erläutert, wie Sie einen bereits eingerichteten Fess-Server nutzen können, um eine Suchfunktion in Ihre Website zu integrieren.
Durch die Verwendung der von Fess Site Search (FSS) bereitgestellten Tags und JavaScript-Dateien können Sie ein Suchfeld und Suchergebnisse in Ihre bestehende Website einbinden.


Zielgruppe
==========

- Personen, die eine Suchfunktion zu einer bestehenden Website hinzufügen möchten.

- Personen, die von Google Site Search oder der benutzerdefinierten Google-Suche migrieren möchten.


Was ist Fess Site Search (FSS)?
=================================

FSS ist eine Funktion, mit der der Suchserver Fess in eine bestehende Website integriert werden kann. Es wird vom CodeLibs-Projekt auf der FSS-Website bereitgestellt. Ähnlich wie bei der websiteinternen Suche von Google Site Search (GSS) können Sie den Dienst nutzen, indem Sie einfach ein JavaScript-Tag auf der Seite einbetten, auf der Sie die Suchfunktion verwenden möchten. Dadurch ist auch eine Migration von GSS problemlos möglich.

Was ist FSS JS?
=================

FSS JS ist eine JavaScript-Datei, die die Suchergebnisse von Fess anzeigt. Durch die Bereitstellung dieser JavaScript-Datei auf Ihrer Website können Suchergebnisse dargestellt werden.
FSS JS kann mit dem FSS JS Generator unter „https://fss-generator.codelibs.org/" generiert und heruntergeladen werden.
FSS JS ist mit Fess ab Version 11.3 kompatibel. Bitte installieren Sie daher bei der Einrichtung von Fess eine Version ab 11.3. Informationen zur Einrichtung von Fess finden Sie im\ `Einführungsartikel <https://fess.codelibs.org/ja/articles/article-1.html>`__\ .


Mit dem FSS JS Generator können Sie die Farbgebung des Suchformulars und die Schriftart festlegen.
Durch Klicken auf die Schaltfläche „Generate" wird eine JavaScript-Datei mit den angegebenen Einstellungen generiert.

|image0|

Wenn die Vorschau keine Probleme zeigt, klicken Sie bitte auf die Schaltfläche „Download JS", um die JavaScript-Datei herunterzuladen.

|image1|

Integration in die Website
=============================

In diesem Beispiel betrachten wir die Integration einer websiteinternen Suche in die statische HTML-Website „`www.n2sm.net`".

Die Suchergebnisse sollen auf der Seite search.html innerhalb der Website angezeigt werden, und der Fess-Server wird separat unter „nss833024.n2search.net" eingerichtet.

Die heruntergeladene FSS JS JavaScript-Datei wird unter /js/fess-ss.min.js auf der Website bereitgestellt.

Die oben genannten Informationen sind in der folgenden Tabelle zusammengefasst.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Bezeichnung
     - URL
   * - Zu durchsuchende Website
     - https://www.n2sm.net/
   * - Suchergebnisseite
     - https://www.n2sm.net/search.html
   * - FSS JS
     - https://www.n2sm.net/js/fess-ss.min.js
   * - Fess-Server
     - https://nss833024.n2search.net/

Zum Einbetten des JavaScript-Tags platzieren Sie den folgenden Code an der Stelle in search.html, an der die Suchergebnisse angezeigt werden sollen.

..
  <script>
    (function() {
      var fess = document.createElement('script');
      fess.type = 'text/javascript';
      fess.async = true;
      // Setzen Sie die URL der FSS JS-Datei als src
      fess.src = 'https://www.n2sm.net/js/fess-ss.min.js';
      fess.charset = 'utf-8';
      fess.setAttribute('id', 'fess-ss');
      // Setzen Sie die URL der Fess-Such-API als fess-url
      fess.setAttribute('fess-url', 'https://nss833024.n2search.net/json');
      var s = document.getElementsByTagName('script')[0];
      s.parentNode.insertBefore(fess, s);
    })();
  </script>
  <fess:search></fess:search>

Wenn Sie search.html aufrufen, wird das Suchformular angezeigt.

Nach Eingabe eines Suchbegriffs können die Suchergebnisse wie folgt dargestellt werden.

|image2|

Um ein Suchformular auf anderen Seiten zu platzieren und die Suchergebnisse anzuzeigen, fügen Sie das folgende Suchformular auf den jeweiligen Seiten ein und konfigurieren Sie es so, dass es zu „`https://www.n2sm.net/search.html?q=Suchbegriff`" weiterleitet.

..
  <form action="https://www.n2sm.net/search.html" method="get">
    <input type="text" name="q">
    <input type="submit" value="Suche">
  </form>


Zusammenfassung
================

In diesem Artikel wurde gezeigt, wie Sie die Suchergebnisse von Fess durch einfaches Platzieren eines JavaScript-Tags in Ihre Website einbetten können.
Mit FSS lässt sich auch eine Migration von GSS realisieren, indem Sie lediglich die vorhandenen JavaScript-Tags ersetzen.
FSS JS bietet darüber hinaus weitere Anzeigeoptionen sowie die Möglichkeit, Suchprotokolle mit Google Analytics zu verknüpfen. Informationen zu weiteren Einstellungsmöglichkeiten finden Sie im `FSS-[Handbuch] <https://fss-generator.codelibs.org/ja/docs/manual>`__.

Referenzmaterial
==================
- `Fess Site Search <https://fss-generator.codelibs.org/ja/>`__

.. |image0| image:: ../../resources/images/ja/article/5/FSS-JS-Generator1.png
.. |image1| image:: ../../resources/images/ja/article/5/FSS-JS-Generator2.png
.. |image2| image:: ../../resources/images/ja/article/5/N2Search-review.png
