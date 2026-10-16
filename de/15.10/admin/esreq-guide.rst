=======================
Anfrage an OpenSearch
=======================

Übersicht
=========

Auf dieser Seite können Sie eine in einer JSON-Datei beschriebene Anfrage an OpenSearch senden.

|image0|

Diese Seite ist nicht im Menü enthalten.
Um sie anzuzeigen, melden Sie sich als Administrator an und geben ``/admin/sereq/`` als URL-Pfad ein.
Zum Senden einer Anfrage ist die Rolle ``admin`` (Administratoren) oder die Rolle ``admin-sereq`` erforderlich.

Bedienung
=========

Anforderung senden
------------------

Erstellen Sie die Anfrage, die Sie an OpenSearch senden möchten, als JSON-Datei, wählen Sie diese Datei als „Anforderungsdatei" aus und klicken Sie auf die Schaltfläche „Senden", um die Anfrage an OpenSearch zu senden.
Die Antwort wird als Datei heruntergeladen.

Konfigurationsparameter
-----------------------

Anforderungsdatei
:::::::::::::::::

Geben Sie die Datei an, die die Anfrage enthält.

Schreiben Sie in die erste Zeile ``<Methode> <Pfad>``, getrennt durch genau ein Leerzeichen, und in die folgenden Zeilen den Anfragekörper (zum Beispiel eine Abfrage-DSL).
Als Methode sind GET, POST, PUT und DELETE möglich. Der Pfad ist der Pfad auf OpenSearch; das führende ``/`` kann weggelassen werden.
Zum Beispiel könnte der Inhalt der Datei wie folgt aussehen.

::

    POST /_search
    {
      "query": {
        "match_all": {}
      }
    }

Zeilenumbrüche im Körper werden entfernt, und die Zeilen werden vor dem Senden zusammengefügt. Eine Anfrage, deren Körper pro Zeile ein JSON-Dokument enthält, wie ``_bulk``, kann daher nicht gesendet werden.

.. warning::

   Auch eine Anfrage mit der Methode PUT oder DELETE wird unverändert an OpenSearch gesendet.
   Je nach Inhalt der Datei können dadurch die von |Fess| verwendeten Indizes geändert oder gelöscht werden und Daten verloren gehen. Prüfen Sie den Inhalt vor dem Senden sorgfältig.

.. |image0| image:: ../../../resources/images/en/15.10/admin/esreq-1.png
