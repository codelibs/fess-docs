=========
Sicherung
=========

Übersicht
=========

Auf der Sicherungsseite können Sie Konfigurationsinformationen von |Fess| herunterladen und hochladen.

Download
--------

|Fess| speichert Konfigurationsinformationen als Index.
Klicken Sie zum Herunterladen auf den Indexnamen.

|image0|

fess_config.bulk
::::::::::::::::

fess_config.bulk enthält die Konfigurationsinformationen von |Fess|.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk enthält die Konfigurationsinformationen von |Fess| ohne Fehler-URLs.

fess_user.bulk
::::::::::::::

fess_user.bulk enthält Informationen zu Benutzern, Rollen und Gruppen.

system.properties
:::::::::::::::::

system.properties enthält allgemeine Konfigurationsinformationen.

fess.json
:::::::::

fess.json enthält die Konfigurationsinformationen des Fess-Index.

doc.json
::::::::

doc.json enthält die Mapping-Informationen des Fess-Index.

chat_log.ndjson
:::::::::::::::

chat_log.ndjson enthält die Nutzungsprotokolle des KI-Chats.

click_log.ndjson
::::::::::::::::

click_log.ndjson enthält Klick-Protokollinformationen.

favorite_log.ndjson
:::::::::::::::::::

favorite_log.ndjson enthält Favoriten-Protokollinformationen.

search_log.ndjson
:::::::::::::::::

search_log.ndjson enthält Such-Protokollinformationen.

user_info.ndjson
::::::::::::::::

user_info.ndjson enthält Informationen zu Suchbenutzern.

Upload
------

Sie können Konfigurationsinformationen hochladen und importieren.
Dateien, die wiederhergestellt werden können, sind \*.bulk und system.properties.

Ein Dokument in einer \*.bulk-Datei, das ein ``updatedTime`` hat, wird nur geschrieben, wenn das
gespeicherte Dokument nicht existiert, kein ``updatedTime`` hat oder älter ist. Ein Dokument, das
nicht neuer ist, wird übersprungen und in ``fess.log`` auf INFO-Ebene protokolliert. So macht eine
Wiederherstellung Änderungen nach der Sicherung nicht rückgängig, und die mit der installierten
Version gelieferten geplanten Jobs (``updatedTime`` 0) bleiben unverändert. Dokumente ohne
``updatedTime`` werden immer geschrieben.

.. note::

   |Fess| 15.9 speichert das ``password`` der Web- und Datei-Authentifizierung mit dem Anwendungsschlüssel
   (``app.cipher.key`` in ``fess_config.properties``) verschlüsselt, sodass ``fess_basic_config.bulk`` und
   ``fess_config.bulk`` die verschlüsselten Werte enthalten. Übernehmen Sie beim Wiederherstellen einer Sicherung auf
   einer anderen Installation denselben ``app.cipher.key``. Mit einem anderen Schlüssel schlagen Crawls, die diese
   Zugangsdaten verwenden, mit einem Fehler fehl. Eine Sicherung, die vor 15.9 erstellt wurde, enthält sie im
   Klartext und funktioniert weiterhin.

   Andere Werte in einer ``*.bulk``-Datei sind nicht verschlüsselt. Bewahren Sie diese Dateien daher als sensible
   Dateien auf.

  .. |image0| image:: ../../../resources/images/en/15.9/admin/backup-1.png
