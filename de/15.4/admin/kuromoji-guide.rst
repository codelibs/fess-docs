================
Kuromoji-Wörterbuch
================

Übersicht
=========

Personennamen, Eigennamen, Fachbegriffe usw. können für die morphologische Analyse registriert werden.

Verwaltung
==========

Anzeige
-------

Um die Kuromoji-Konfigurationsübersichtsseite zu öffnen, wählen Sie im linken Menü [System > Wörterbuch] aus und klicken Sie dann auf kuromoji.

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfigurationsmethode
---------------------

Um die Kuromoji-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Token
:::::

Geben Sie das Wort ein, das in der morphologischen Analyse verarbeitet werden soll.

Segmentierung
:::::::::::::

Wenn das Wort aus zusammengesetzten Wörtern besteht, kann es so konfiguriert werden, dass es auch bei der Suche nach segmentierten Wörtern gefunden wird.
Zum Beispiel können Sie „全文検索エンジン" als „全文 検索 エンジン" eingeben, damit auch nach segmentierten Wörtern gesucht werden kann.

Lesung
::::::

Geben Sie die Lesung des als Token eingegebenen Worts in Katakana ein.
Wenn Sie segmentiert haben, geben Sie die Lesung segmentiert ein.
Zum Beispiel geben Sie „ゼンブン ケンサク エンジン" ein.

Wortart
:::::::

Geben Sie die Wortart des eingegebenen Worts ein.

Download
========

Sie können im Kuromoji-Wörterbuchformat herunterladen.

Upload
======

Sie können im Kuromoji-Wörterbuchformat hochladen.
Das Kuromoji-Wörterbuchformat ist durch Kommas (,) getrennt: „Token,Segmentiertes Token,Lesung des segmentierten Tokens,Wortart".
Segmentierte Token werden durch Leerzeichen getrennt.
Wenn keine Segmentierung erforderlich ist, sind Token und segmentiertes Token gleich.
Zum Beispiel:

::

    朝青龍,朝青龍,アサショウリュウ,カスタム名詞
    関西国際空港,関西 国際 空港,カンサイ コクサイ クウコウ,カスタム名詞


.. |image0| image:: ../../../resources/images/en/15.4/admin/kuromoji-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/kuromoji-2.png
