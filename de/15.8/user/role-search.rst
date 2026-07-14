====================
Rollenbasierte Suche
====================

|Fess| bietet eine Benutzerverwaltungsfunktion, mit der angemeldete Benutzer basierend auf den Rollen suchen können, denen sie angehören. Benutzer, die von |Fess| verwaltet werden, können nach der Anmeldung die Rollensuche nutzen und ihr eigenes Passwort ändern.

Bei der Rollensuche werden die für einen Inhalt festgelegten Berechtigungen (Rolle, Gruppe, Benutzer) mit den Berechtigungen des suchenden Benutzers abgeglichen, sodass in den Suchergebnissen nur Inhalte angezeigt werden, für die der Zugriff erlaubt ist. Informationen zur Konfiguration der rollenbasierten Suche, einschließlich der Erstellung von Rollen und Benutzern sowie der Zuweisung von Berechtigungen zu Inhalten, finden Sie unter :doc:`../config/security-role`.


Suchmethode
-----------

Wenn Rollen festgelegt sind und die entsprechenden Inhalte gecrawlt und indiziert wurden, können die Suchergebnisse nur Benutzern angezeigt werden, die über die jeweilige Rolle verfügen.
Wenn ein Benutzer angemeldet ist, erfolgt die Suche basierend auf den Rollen und Gruppen, denen dieser Benutzer angehört.
Ist der Benutzer nicht angemeldet, erfolgt die Suche als guest-Benutzer, wobei nur die für guest freigegebenen Inhalte angezeigt werden.

Anmeldung
---------

Wenn Sie auf den Link „Anmelden“ oben im Suchbildschirm klicken, wird der Anmeldebildschirm angezeigt. Nach Eingabe von Benutzername und Passwort und der Anmeldung kehren Sie zum Suchbildschirm zurück, und alle weiteren Suchen erfolgen basierend auf den Rollen, denen dieser Benutzer angehört.

.. note::
    Bei einer Integration mit Single Sign-On oder LDAP erfolgt die Anmeldung über das jeweilige Authentifizierungsverfahren. Außerdem kann die Anzeige des Anmeldelinks je nach Konfiguration geändert werden.

Passwort ändern
---------------

Wenn Sie nach der Anmeldung auf den oben im Suchbildschirm angezeigten Benutzernamen klicken, wird ein Menü angezeigt.

|image0|

Wenn Sie im Menü auf „Passwort ändern“ klicken, wird der Bildschirm zur Passwortänderung angezeigt.

|image1|

Geben Sie im Feld „Aktuelles Passwort“ Ihr aktuelles Passwort, im Feld „Neues Passwort“ das neue Passwort und im Feld „Neues Passwort bestätigen“ das neue Passwort zur Bestätigung (erneut) ein und klicken Sie auf die Schaltfläche „Aktualisieren“, um das Passwort zu aktualisieren.
Nach der Passwortänderung können Sie durch Klicken auf die Schaltfläche „Zurück“ zum Suchbildschirm zurückkehren.

.. note::
    Das Menü „Passwort ändern“ wird nur für Benutzer angezeigt, die von |Fess| verwaltet werden (sowie für LDAP-Benutzer, deren Bearbeitung erlaubt ist). Für Benutzer, die per Single Sign-On authentifiziert wurden, wird es nicht angezeigt.
    Für das neue Passwort können Passwortrichtlinien gelten, die sich beispielsweise auf die Länge oder die zulässigen Zeichenarten beziehen.

Abmelden
--------

Wenn Sie angemeldet sind, können Sie sich abmelden, indem Sie auf den oben im Suchbildschirm angezeigten Benutzernamen klicken und im Menü „Abmelden“ auswählen.
Benutzer mit Administratorrechten können über dasselbe Menü auch „Verwaltung“ auswählen, um zum Verwaltungsbildschirm zu wechseln.



.. |image0| image:: ../../../resources/images/en/15.8/user/role-search-1.png
.. pdf   :width: 200 px
.. |image1| image:: ../../../resources/images/en/15.8/user/role-search-2.png
.. pdf   :width: 300 px
