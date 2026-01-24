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

  .. |image0| image:: ../../../resources/images/en/15.5/admin/backup-1.png
