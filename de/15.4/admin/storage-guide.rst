========
Speicher
========

Übersicht
=========

Auf der Speicherseite können Sie Dateien auf Amazon S3, Google Cloud Storage oder S3-kompatiblem Speicher (wie MinIO) verwalten.

Verwaltung
==========

Konfiguration des Objektspeicher-Servers
-----------------------------------------

Öffnen Sie die Speicherkonfiguration unter [System > Allgemein] und konfigurieren Sie die folgenden Elemente entsprechend Ihrem Speichertyp.

Allgemeine Einstellungen
~~~~~~~~~~~~~~~~~~~~~~~~

- Typ: Speichertyp (Automatisch/S3/GCS)
- Bucket: Name des zu verwaltenden Buckets

S3-Einstellungen
~~~~~~~~~~~~~~~~

- Endpunkt: S3-Endpunkt (verwendet AWS-Standard, wenn leer)
- Zugriffsschlüssel: AWS-Zugriffsschlüssel
- Geheimer Schlüssel: AWS-Geheimschlüssel
- Region: AWS-Region

GCS-Einstellungen
~~~~~~~~~~~~~~~~~

- Endpunkt: GCS-Endpunkt (verwendet Google Cloud-Standard, wenn leer)
- Projekt-ID: Google Cloud-Projekt-ID
- Anmeldedaten-Pfad: Pfad zur Dienstkonto-Anmeldedaten-JSON-Datei

MinIO (S3-kompatibel) Einstellungen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Endpunkt: MinIO-Server-Endpunkt-URL
- Zugriffsschlüssel: MinIO-Zugriffsschlüssel
- Geheimer Schlüssel: MinIO-Geheimschlüssel


Anzeige
-------

Um die Objektübersichtsseite zu öffnen, klicken Sie im linken Menü auf [System > Speicher].

|image0|


Name
::::

Der Dateiname des Objekts


Größe
:::::

Die Größe des Objekts


Letztes Änderungsdatum
::::::::::::::::::::::

Das letzte Änderungsdatum des Objekts

Download
--------

Durch Klicken auf die Schaltfläche „Download" können Sie das Objekt herunterladen.


Löschen
-------

Durch Klicken auf die Schaltfläche „Löschen" können Sie das Objekt löschen.


Upload
------

Klicken Sie oben rechts auf die Schaltfläche „Datei hochladen", um das Datei-Upload-Fenster zu öffnen.


Ordner erstellen
----------------

Klicken Sie auf die Schaltfläche „Ordner erstellen" rechts neben der Pfadanzeige, um das Ordnererstellungsfenster zu öffnen. Beachten Sie, dass leere Ordner nicht erstellt werden können.


.. |image0| image:: ../../../resources/images/en/15.4/admin/storage-1.png
