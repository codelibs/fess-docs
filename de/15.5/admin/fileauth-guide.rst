==================
Dateiauthentifizierung
==================

Übersicht
=========

Hier wird die Konfigurationsmethode erläutert, wenn Dateiauthentifizierung für das Crawlen von Dateien erforderlich ist.
|Fess| unterstützt die Authentifizierung für FTP oder Windows-Freigabeordner.

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite für die Dateiauthentifizierungskonfiguration zu öffnen, klicken Sie im linken Menü auf [Crawler > Dateiauthentifizierung].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Dateiauthentifizierungskonfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Hostname
::::::::

Geben Sie den Hostnamen der Site an, die Authentifizierung erfordert.

Port
::::

Geben Sie den Port der Site an, die Authentifizierung erfordert.

Schema
::::::

Wählen Sie die Authentifizierungsmethode aus.
Sie können FTP oder SAMBA (Windows-Freigabeordnerauthentifizierung) verwenden.

Benutzername
::::::::::::

Geben Sie den Benutzernamen für die Anmeldung bei der Authentifizierungssite an.

Passwort
::::::::

Geben Sie das Passwort für die Anmeldung bei der Authentifizierungssite an.

Parameter
:::::::::

Konfigurieren Sie dies, wenn Konfigurationswerte für die Anmeldung bei der Authentifizierungssite erforderlich sind. Für SAMBA können Sie den Domänenwert konfigurieren. Geben Sie ihn wie folgt an:

::

    domain=FUGA

Datei-Crawl-Konfiguration
:::::::::::::::::::::::::

Geben Sie die Crawl-Konfiguration an, die diese Authentifizierungskonfiguration verwenden soll.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

.. |image0| image:: ../../../resources/images/en/15.5/admin/fileauth-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/fileauth-2.png
