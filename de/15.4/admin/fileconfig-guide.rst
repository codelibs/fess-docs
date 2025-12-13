===========
Datei-Crawl
===========

Übersicht
=========

Auf der Datei-Crawl-Konfigurationsseite können Sie Konfigurationen zum Crawlen von Dateien im Dateisystem oder in freigegebenen Netzwerkordnern verwalten.

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite für die Datei-Crawl-Konfiguration zu öffnen, klicken Sie im linken Menü auf [Crawler > Dateisystem].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Datei-Crawl-Konfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Der Name der Konfiguration.

Pfad
::::

In diesem Pfad geben Sie an, wo das Crawlen beginnen soll (z. B. file:/, smb://, s3://, gcs://).

Zu crawlender Pfad
::::::::::::::::::

Pfade, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden vom |Fess| Crawler gecrawlt.

Vom Crawlen ausgeschlossener Pfad
::::::::::::::::::::::::::::::::::

Pfade, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden vom |Fess| Crawler nicht gecrawlt.

Zu durchsuchender Pfad
:::::::::::::::::::::::

Pfade, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden in die Suche einbezogen.

Von der Suche ausgeschlossener Pfad
::::::::::::::::::::::::::::::::::::

Pfade, die mit dem regulären Ausdruck (Java-Format) übereinstimmen, der in diesem Element angegeben ist, werden von der Suche ausgeschlossen.

Konfigurationsparameter
:::::::::::::::::::::::

Sie können Crawl-Konfigurationsinformationen angeben.

Tiefe
:::::

Geben Sie die Tiefe der zu crawlenden Dateisystemstruktur an.

Maximale Zugriffszahl
:::::::::::::::::::::

Geben Sie die Anzahl der zu indizierenden Pfade an.

Thread-Anzahl
:::::::::::::

Geben Sie die Anzahl der für diese Konfiguration zu verwendenden Threads an.

Intervall
:::::::::

Geben Sie die Wartezeit an, die jeder Thread nach dem Crawlen eines Pfads wartet.

Boost-Wert
::::::::::

Der Boost-Wert ist die Priorität von Dokumenten, die durch diese Konfiguration indiziert werden.

Berechtigung
::::::::::::

Geben Sie die Berechtigung für diese Konfiguration an.
Um beispielsweise Suchergebnisse für Benutzer anzuzeigen, die zur Gruppe „developer" gehören, geben Sie {group}developer an.
Für Benutzerebene geben Sie {user}Benutzername an, für Rollenebene {role}Rollenname und für Gruppenebene {group}Gruppenname.

Virtueller Host
:::::::::::::::

Geben Sie den Hostnamen des virtuellen Hosts an.
Weitere Details finden Sie unter :doc:`Virtueller Host im Konfigurationshandbuch <../config/virtual-host>`.

Status
::::::

Wenn diese Konfiguration aktiviert ist, enthält der Standard-Crawler-Job diese Konfiguration beim Crawlen.

Beschreibung
::::::::::::

Sie können eine Beschreibung eingeben.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt. Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

Beispiele
=========

Lokale Dateien crawlen
----------------------

Um Dateien unter /home/share zu crawlen, würde die Konfiguration wie folgt aussehen:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Wert
   * - Name
     - Freigabeverzeichnis
   * - Pfad
     - file:/home/share

Andere Parameter können mit Standardeinstellungen belassen werden.

Windows-Freigabeordner crawlen
-------------------------------

Um Dateien unter \\SERVER\SharedFolder zu crawlen, würde die Konfiguration wie folgt aussehen:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Wert
   * - Name
     - Freigabeordner
   * - Pfad
     - smb://SERVER/SharedFolder/

Wenn für den Zugriff auf den Freigabeordner ein Benutzername/Passwort erforderlich ist, müssen Sie eine Dateiauthentifizierungskonfiguration über [Crawler > Dateiauthentifizierung] im linken Menü erstellen.
Die Konfiguration dafür würde wie folgt aussehen:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Wert
   * - Hostname
     - SERVER
   * - Schema
     - SAMBA
   * - Benutzername
     - (Bitte eingeben)
   * - Passwort
     - (Bitte eingeben)

Amazon S3-Buckets crawlen
-------------------------

Um Dateien im Bucket my-bucket zu crawlen, würde die Konfiguration wie folgt aussehen:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Wert
   * - Name
     - S3-Bucket
   * - Pfad
     - s3://my-bucket/

Für den S3-Zugriff sind Anmeldeinformationen erforderlich. Fügen Sie Folgendes zu „Konfigurationsparameter" hinzu:

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=IHR_ZUGRIFFSSCHLÜSSEL
    client.secretKey=IHR_GEHEIMER_SCHLÜSSEL
    client.region=ap-northeast-1

Google Cloud Storage-Buckets crawlen
------------------------------------

Um Dateien im Bucket my-gcs-bucket zu crawlen, würde die Konfiguration wie folgt aussehen:

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::
   :header-rows: 1

   * - Name
     - Wert
   * - Name
     - GCS-Bucket
   * - Pfad
     - gcs://my-gcs-bucket/

Für den GCS-Zugriff sind Anmeldeinformationen erforderlich. Fügen Sie Folgendes zu „Konfigurationsparameter" hinzu:

::

    client.projectId=ihre-projekt-id
    client.credentialsFile=/pfad/zu/service-account.json


.. |image0| image:: ../../../resources/images/en/15.4/admin/fileconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/fileconfig-2.png
.. pdf            :height: 940 px
