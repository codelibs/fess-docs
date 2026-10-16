================
Kuromoji-Wörterbuch
================

Übersicht
=========

Personennamen, Eigennamen, Fachbegriffe usw. können für die morphologische Analyse registriert werden.

Dieses Wörterbuch gilt für Japanisch (``ja/kuromoji.txt``) und wird nur bei der Analyse der ``_ja``-Felder wie ``content_ja`` verwendet.
Das Speichern allein wirkt sich noch nicht auf die Suche aus. Wie Sie eine Änderung übernehmen, steht unter :ref:`dict-apply-changes`. Da dieses Wörterbuch beim Indizieren wirkt, sind bereits indizierte Dokumente erst nach erneutem Crawlen betroffen.

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

.. warning::

   Beim Hochladen wird der Inhalt des Wörterbuchs durch den Inhalt der hochgeladenen Datei ersetzt. Wörter, die nicht in der Datei stehen, werden entfernt, auch solche, die über die Oberfläche registriert wurden. Laden Sie das Wörterbuch bei Bedarf zuerst herunter und nehmen Sie dessen Inhalt in die hochzuladende Datei auf.

.. note::

   Das mitgelieferte Wörterbuch enthält die beiden obigen Beispiele („朝青龍" und „関西国際空港") bereits.
   Bei der Analyse von ``content_ja`` werden Zeichen vor der morphologischen Analyse durch das Zeichenersetzungs-Wörterbuch ``ja/mapping.txt`` ersetzt (siehe :doc:`mapping-guide`). Das mitgelieferte ``ja/mapping.txt`` enthält ``龍 => 竜``; daher wird „朝青龍" vor der Analyse durch ``朝青竜`` ersetzt; es stimmt nicht mit „朝青龍" im Wörterbuch überein und wird in ``朝 青 竜`` zerlegt.
   Um die Wirkung einer Registrierung zu prüfen, verwenden Sie ein Wort, das nicht im Wörterbuch steht und kein durch ``ja/mapping.txt`` ersetztes Zeichen enthält.


.. |image0| image:: ../../../resources/images/en/15.10/admin/kuromoji-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/kuromoji-2.png
