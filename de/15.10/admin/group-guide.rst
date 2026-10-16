======
Gruppe
======

Übersicht
=========

Sie können Gruppen verwalten, zu denen Benutzer gehören.
Dies kann beispielsweise bei der LDAP-Integration verwendet werden.

Verwaltung
==========

Anzeige
-------

Um die Übersichtsseite für die Gruppenkonfiguration zu öffnen, klicken Sie im linken Menü auf [Benutzer > Gruppe].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Gruppenkonfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Name
::::

Gruppenname.

gidNumber
:::::::::

Die gidNumber (die POSIX-Gruppen-ID in LDAP) der Gruppe als Zahl. Die Angabe ist optional. Die Eingabe eines Wertes, der keine Zahl ist, führt zu einem Fehler.
Ist |Fess| so konfiguriert, dass LDAP über die Verwaltungsoberfläche verwaltet wird (``ldap.admin.enabled=true``), wird der Wert in das Attribut ``gidNumber`` des Gruppeneintrags in LDAP geschrieben (der Attributname kann mit ``ldap.attr.gidNumber`` geändert werden). Wenn Sie LDAP nicht verwenden, müssen Sie nichts angeben.

Löschmethode
------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

.. |image0| image:: ../../../resources/images/en/15.10/admin/group-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/group-2.png
