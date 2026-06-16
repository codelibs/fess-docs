====================================
Konfiguration rollenbasierter Suche
====================================

Über rollenbasierte Suche
=========================

|Fess| kann Suchergebnisse basierend auf den Authentifizierungsinformationen von Benutzern differenzieren, die durch beliebige Authentifizierungssysteme authentifiziert wurden.
Beispielsweise werden für Benutzer A mit Rolle a Suchergebnisse mit Informationen zur Rolle a angezeigt, während Benutzer B ohne Rolle a diese bei der Suche nicht sieht.
Mit dieser Funktion können Sie in Portal- oder Single-Sign-On-Umgebungen eine abteilungs- oder positionsbezogene Suche für angemeldete Benutzer realisieren.

Bei rollenbasierter Suche in |Fess| können Rolleninformationen aus folgenden Quellen abgerufen werden:

-  Request-Parameter

-  Request-Header

-  Cookie

-  |Fess|-Authentifizierungsinformationen

Bei Portal- oder Agent-basierten Single-Sign-On-Systemen können Rolleninformationen abgerufen werden, indem bei der Authentifizierung Authentifizierungsinformationen per Cookie für die Domain und den Pfad gespeichert werden, auf dem |Fess| läuft.
Bei Reverse-Proxy-basierten Single-Sign-On-Systemen können Rolleninformationen abgerufen werden, indem beim Zugriff auf |Fess| Authentifizierungsinformationen zu Request-Parametern oder Request-Headern hinzugefügt werden.

.. note::
    Der Abruf von Rolleninformationen aus Request-Parametern, Request-Headern und Cookies ist standardmäßig deaktiviert.
    Wenn Sie diese verwenden möchten, müssen Sie im ``roleQueryHelper``-Komponenten in ``app/WEB-INF/classes/fess.xml`` den zu referenzierenden Schlüsselnamen (``parameterKey``, ``headerKey``, ``cookieKey``), die Verschlüsselung der Werte (``encryptedParameterValue`` usw.) sowie die Trennzeichen (``valueSeparator``, ``roleSeparator``) konfigurieren.
    Standardmäßig ist nur die rollenbasierte Suche unter Verwendung der |Fess|-Authentifizierungsinformationen aktiviert.

Konfiguration rollenbasierter Suche
=====================================

Hier wird die Konfiguration der rollenbasierten Suche unter Verwendung der |Fess|-Authentifizierungsinformationen erläutert.

Konfiguration in der |Fess|-Verwaltungsoberfläche
--------------------------------------------------

Starten Sie |Fess| und melden Sie sich als Administrator an.
Erstellen Sie Rollen und Benutzer.
Erstellen Sie beispielsweise im Rollen-Verwaltungsbildschirm die Rolle Role1 und legen Sie im Benutzer-Verwaltungsbildschirm einen Benutzer an, der zu Role1 gehört.
Wenn Sie die Zuweisung auf Gruppenebene vornehmen möchten, erstellen Sie im Gruppen-Verwaltungsbildschirm eine Gruppe und weisen Sie den Benutzer der Gruppe zu.

Tragen Sie anschließend in der Crawl-Konfiguration im Berechtigungsfeld ``{role}Role1`` ein und speichern Sie die Einstellung.
Für benutzerspezifische Angaben verwenden Sie ``{user}username``, für gruppenspezifische Angaben ``{group}groupname``.
Wenn mehrere Berechtigungen angegeben werden sollen, trennen Sie diese durch Zeilenumbrüche.

Durch das Crawlen mit dieser Crawl-Konfiguration wird ein Index erstellt, der nur für Benutzer durchsuchbar ist, die der angegebenen Rolle, dem Benutzer oder der Gruppe angehören.
Angemeldeten Benutzern werden automatisch die Berechtigungen für ihre eigene Person (``{user}username``), ihre zugehörigen Rollen (``{role}``) und ihre zugehörigen Gruppen (``{group}``) zugewiesen und mit den am Dokument gesetzten Berechtigungen abgeglichen.

.. note::
    Wenn Sie den Zugriff von bestimmten Rollen, Benutzern oder Gruppen explizit verweigern möchten, fügen Sie ``(deny)`` vor dem Eintrag ein, z. B. ``(deny){role}Role1`` (mit ``(allow)`` wird der Zugriff erlaubt, was dem Standardverhalten ohne Angabe entspricht).

.. note::
    Bei der Anbindung an LDAP oder Single Sign-On werden die Rollen- und Gruppeninformationen des Benutzers vom Authentifizierungsanbieter abgerufen und ebenfalls als Berechtigungen behandelt.
    Das Verhalten bei der LDAP-Integration kann über ``ldap.role.search.user.enabled``, ``ldap.role.search.group.enabled`` und ``ldap.role.search.role.enabled`` in ``fess_config.properties`` gesteuert werden (Standardwert jeweils ``true``).

Anmeldung
---------

Melden Sie sich von der Verwaltungsoberfläche ab.
Melden Sie sich mit einem Benutzer an, der zu Role1 gehört.
Bei erfolgreicher Anmeldung werden Sie zur Startseite des Suchbildschirms weitergeleitet.

Bei einer normalen Suche werden nur Ergebnisse angezeigt, für die in der Crawl-Konfiguration die Rolle Role1 gesetzt wurde.

Suchanfragen ohne Anmeldung werden als Suche des Gastbenutzers (guest) ausgeführt.
Für Dokumente, die auch nicht angemeldeten Benutzern angezeigt werden sollen, tragen Sie im Berechtigungsfeld der Crawl-Konfiguration ``{role}guest`` ein (der Standardwert ist unter ``role.search.guest.permissions`` definiert).

Abmeldung
---------

Wenn Sie mit einem anderen Benutzer als dem Administrator angemeldet sind, können Sie sich im Suchbildschirm über die Abmelden-Option abmelden.
