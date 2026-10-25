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

.. note::

   Wörterbuchdateien (Synonyme, Stoppwörter usw.) sind nicht Teil der Sicherung.
   Sie liegen im Wörterbuchverzeichnis der Suchmaschine (``FESS_DICTIONARY_PATH``);
   kopieren Sie sie bei Bedarf separat.

fess_config.bulk
::::::::::::::::

fess_config.bulk enthält die Konfigurationsinformationen von |Fess|.

fess_basic_config.bulk
::::::::::::::::::::::

fess_basic_config.bulk enthält die Konfigurationsinformationen von |Fess| ohne Crawl-Informationen, Fehler-URLs, Job-Protokolle, Thumbnail-Warteschlange, Benutzer-Tags und Ähnliches.

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
Folgende Dateien können wiederhergestellt werden:

- ``*.bulk``
- ``system.properties``
- ``fess.json`` und ``doc.json``: Sie ersetzen die Indexdefinitionsdateien, die |Fess| verwendet. Einstellungen und Mapping eines bestehenden Index werden dadurch nicht sofort geändert.
- ``gsa*.xml``: eine Konfigurationsdatei der Google Search Appliance. Sie wird als Web-Crawl-Konfiguration, Dateisystem-Crawl-Konfiguration und als Labels importiert.

``*.ndjson``-Dateien (Suchprotokolle und andere Protokolle) können nicht hochgeladen und wiederhergestellt werden.

Ein Dokument in einer \*.bulk-Datei, das ein ``updatedTime`` hat, wird nur geschrieben, wenn das
gespeicherte Dokument nicht existiert, kein ``updatedTime`` hat oder älter ist. Ein Dokument, das
nicht neuer ist, wird übersprungen und in ``fess.log`` auf INFO-Ebene protokolliert. So macht eine
Wiederherstellung Änderungen nach der Sicherung nicht rückgängig, und die mit der installierten
Version gelieferten geplanten Jobs (``updatedTime`` 0) bleiben unverändert. Dokumente ohne
``updatedTime`` werden immer geschrieben.

.. note::

   Das Überspringen wird auf INFO-Ebene protokolliert und erscheint daher mit der Standard-Protokollebene (``warn``) nicht in ``fess.log``. Um diese Einträge zu sehen, setzen Sie die Protokollebene vor der Wiederherstellung auf ``info``. Sie können sie in der Verwaltungsoberfläche unter [System > Allgemein] bei „Protokollebene" ändern (nach einem Neustart von |Fess| gilt wieder der konfigurierte Wert) oder unter Linux mit ``FESS_LOG_LEVEL=info``. Details finden Sie unter :doc:`../config/admin-logging`.

.. note::

   |Fess| 15.9 speichert das ``password`` der Web- und Datei-Authentifizierung mit dem Anwendungsschlüssel
   (``app.cipher.key`` in ``fess_config.properties``) verschlüsselt, sodass ``fess_basic_config.bulk`` und
   ``fess_config.bulk`` die verschlüsselten Werte enthalten. Übernehmen Sie beim Wiederherstellen einer Sicherung auf
   einer anderen Installation denselben ``app.cipher.key``. Mit einem anderen Schlüssel schlagen Crawls, die diese
   Zugangsdaten verwenden, mit einem Fehler fehl. Eine Sicherung, die vor 15.9 erstellt wurde, enthält sie im
   Klartext und funktioniert weiterhin.

   Andere Werte in einer ``*.bulk``-Datei sind nicht verschlüsselt. Bewahren Sie diese Dateien daher als sensible
   Dateien auf.

  .. |image0| image:: ../../../resources/images/en/15.10/admin/backup-1.png
