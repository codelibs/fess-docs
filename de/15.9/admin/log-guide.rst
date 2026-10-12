============
Protokolldatei
============

Übersicht
=========

Hier wird der Download von Protokolldateien erläutert, die von |Fess| ausgegeben werden.

Konfiguration
=============

Anzeige
-------

Um die Protokolldateiseite zu öffnen, klicken Sie im linken Menü auf [Systeminformationen > Protokolldatei].

|image0|

Download
--------

Sie können Protokolldateien herunterladen, indem Sie auf den angezeigten Protokolldateinamen klicken.

``server_*.log``
::::::::::::::::

Protokolliert werden die Protokolle von |Fess| als Anwendungsserver.

fess.log
::::::::

Protokolliert werden die Protokolle von |Fess| als Anwendung.

fess-crawler.log
::::::::::::::::

Protokolliert werden die Crawler-Protokolle.

audit.log
:::::::::

Protokolliert werden Anmeldeinformationen und Zugriffsprotokolle des Verwaltungsbildschirms.

fess-thumbnail.log
::::::::::::::::::

Protokolliert werden die Protokolle der Thumbnail-Funktion.

fess-suggest.log
::::::::::::::::

Protokolliert werden die Protokolle der Vorschlagsfunktion.

fess-urls.log
:::::::::::::

Protokolliert wird die Zeit, die für einen einzelnen Crawl benötigt wurde.

searchlog.log
:::::::::::::

Protokolliert werden die Suchprotokolle.
Wenn „Suchprotokoll" unter [System > Allgemein] aktiviert ist, wird in der Standardkonfiguration für jede Suche eine Zeile (JSON) angehängt.
Eine Zeile enthält die Felder der von dieser Suche zurückgegebenen Dokumente (``logging.search.docs.fields``); ihre Größe wächst daher mit der Zahl der zurückgegebenen Treffer (bei ``num=100`` kann eine Zeile etwa 70 KB groß werden).
Zu Rotation und Aufbewahrung siehe :doc:`../config/admin-logging`.
Um die Felder der zurückgegebenen Dokumente nicht ins Suchprotokoll aufzunehmen, setzen Sie in ``fess_config.properties`` ``logging.search.docs.enabled=false``; um nicht mehr in diese Datei zu schreiben, setzen Sie ``logging.search.use.logfile=false``.

gc-crawler.log
::::::::::::::

Protokolliert werden die GC-Protokolle des Crawler-Prozesses (vom Standard-Job „Default Crawler" geschrieben).

gc-fess.log
:::::::::::

Protokolliert werden die GC-Protokolle von |Fess| selbst. Sie werden nur geschrieben, wenn die Umgebungsvariable ``FESS_USE_GC_LOGGING`` auf einen nicht leeren Wert gesetzt ist (siehe :doc:`../install/run`).

.. |image0| image:: ../../../resources/images/en/15.9/admin/log-1.png
