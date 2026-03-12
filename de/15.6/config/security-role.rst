=================
Konfiguration rollenbasierter Suche
=================

Über rollenbasierte Suche
==================

|Fess| kann Suchergebnisse basierend auf Authentifizierungsinformationen von Benutzern differenzieren, die durch beliebige Authentifizierungssysteme authentifiziert wurden.
Beispielsweise werden für Benutzer A mit Rolle a Suchergebnisse mit Informationen für Rolle a angezeigt, aber Benutzer B ohne Rolle a sieht diese bei Suche nicht.
Mit dieser Funktion können Sie Suche nach Abteilung, Position usw. in Portalen oder Single-Sign-On-Umgebungen für angemeldete Benutzer realisieren.

Bei rollenbasierter Suche in |Fess| können Rolleninformationen aus folgenden Quellen abgerufen werden:

-  Request-Parameter

-  Request-Header

-  Cookie

-  |Fess|-Authentifizierungsinformationen

Bei Portal- oder Agent-basierten Single-Sign-On-Systemen können Rolleninformationen abgerufen werden, indem bei Authentifizierung Authentifizierungsinformationen per Cookie für Domain und Pfad gespeichert werden, auf dem |Fess| läuft.
Bei Reverse-Proxy-basierten Single-Sign-On-Systemen können Rolleninformationen abgerufen werden, indem bei Zugriff auf |Fess| Authentifizierungsinformationen zu Request-Parametern oder Request-Headern hinzugefügt werden.

Konfiguration rollenbasierter Suche
=================

Hier wird die Konfigurationsmethode für rollenbasierte Suche unter Verwendung von |Fess|-Authentifizierungsinformationen erklärt.

Konfiguration in |Fess|-Verwaltungsoberfläche
---------------------

Starten Sie |Fess| und melden Sie sich als Administrator an.
Erstellen Sie Rollen und Benutzer.
Erstellen Sie beispielsweise Role1 im Rollen-Verwaltungsbildschirm und erstellen Sie im Benutzer-Verwaltungsbildschirm einen Benutzer, der zu Role1 gehört.
Beschreiben Sie als nächstes in der Crawl-Konfiguration im Berechtigungsfeld {role}Role1 und speichern Sie.
Für Benutzer-spezifische Angabe können Sie {user}Benutzername schreiben, für Gruppen-spezifische Angabe {group}Gruppenname.
Danach wird durch Crawlen mit dieser Crawl-Konfiguration ein Index erstellt, der nur für erstellte Benutzer durchsuchbar ist.

Anmeldung
------

Melden Sie sich von der Verwaltungsoberfläche ab.
Melden Sie sich mit Benutzer an, der zu Role1 gehört.
Bei erfolgreicher Anmeldung werden Sie zur Startseite des Suchbildschirms weitergeleitet.

Bei normaler Suche werden nur Einträge angezeigt, für die in der Crawl-Konfiguration Rolleneinstellung Role1 konfiguriert wurde.

Bei Suche ohne Anmeldung erfolgt Suche als Gastbenutzer (guest).

Abmeldung
--------

Im angemeldeten Zustand mit Benutzer außer Administrator wählen Sie Abmeldung im Suchbildschirm, um sich abzumelden.
