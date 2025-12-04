============
Zugriffstoken
============

Übersicht
=========

Die Konfigurationsseite für Zugriffstoken verwaltet Zugriffstoken.

Verwaltung
==========

Anzeige
-------

Um die Konfigurationsübersichtsseite für Zugriffstoken zu öffnen, klicken Sie im linken Menü auf [System > Zugriffstoken].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Konfigurationsseite für Zugriffstoken zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Geben Sie einen Namen an, um dieses Zugriffstoken zu beschreiben.

Berechtigung
::::::::::::

Legen Sie die Berechtigung für das Zugriffstoken fest.
Geben Sie diese im Format „{user|group|role}name" an.
Um beispielsweise Suchergebnisse für Benutzer anzuzeigen, die zur Gruppe „developer" gehören, legen Sie die Berechtigung auf „{group}developer" fest.

Parametername
:::::::::::::

Geben Sie den Namen des Anforderungsparameters an, wenn Sie die Berechtigung als Suchabfrage angeben.

.. warning::

   Die Parametername-Funktion ist ausschließlich für die Verwendung in vertrauenswürdigen internen Umgebungen konzipiert.
   Wenn diese Funktion aktiviert ist, können zusätzliche Berechtigungen über URL-Parameter angegeben werden.
   In extern zugänglichen Umgebungen oder bei Bereitstellung als öffentliche API können jedoch
   böswillige Benutzer URL-Parameter manipulieren, um sich Berechtigungen zu verschaffen, die sie nicht haben sollten.

   Bitte beachten Sie Folgendes:

   * Verwenden Sie diese Funktion nur, wenn Fess in eine andere Anwendung oder einen Dienst eingebettet ist, der eingehende Anfragen vollständig kontrolliert.
   * Konfigurieren Sie keinen Parameternamen, wenn Fess für nicht vertrauenswürdige Netzwerke zugänglich ist.
   * Stellen Sie sicher, dass URL-Parameter bei Verwendung von Zugriffstoken nicht von externen Benutzern manipuliert werden können.

Ablaufdatum
:::::::::::

Geben Sie das Ablaufdatum des Zugriffstokens an.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.



.. |image0| image:: ../../../resources/images/en/15.4/admin/accesstoken-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/accesstoken-2.png
