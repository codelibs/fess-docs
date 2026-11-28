==============================================
Suchergebnisse nach Rollen und Gruppen steuern
==============================================

Einführung
==========

Sobald sich die Dokumente des Unternehmens mit einem einzigen Fess durchsuchen lassen, stellt sich als Nächstes die Frage, wer was sehen darf.
Die Beurteilungsunterlagen der Personalabteilung sollen nicht in den Suchergebnissen aller Mitarbeitenden auftauchen, und umgekehrt sollen unternehmensweite Richtlinien nicht nur für einige wenige sichtbar sein.

In Fess werden die Werte, die Sie im Feld „Berechtigungen“ einer Crawl-Konfiguration eintragen, bei jedem Dokument gespeichert und bei jeder Suche mit den Rechten des angemeldeten Benutzers abgeglichen.
In diesem Artikel richten wir in Fess 15.9 eine abteilungsbezogene Sichtbarkeit ein und prüfen am Ende, welche Dokumente jeder Benutzer sieht.

Wenn Sie die Schritte in diesem Artikel ausführen, können Sie Folgendes:

- Drei Arten von Sichtbarkeit (Abteilung, Geschäftsleitung, alle Mitarbeitenden) mit Gruppen und Berechtigungen einrichten
- Gruppen aus Active Directory direkt als Berechtigungen verwenden
- Die Sichtbarkeit von Labels an die der Dokumente angleichen
- Prüfen, welche Dokumente jeder Benutzer sieht und welche Rechte in einem Dokument gespeichert sind

Die SSO-Konfiguration wird in :doc:`guide-15` behandelt, die Trennung mehrerer Organisationen über virtuelle Hosts in :doc:`guide-13`.

Wie Berechtigungen funktionieren
================================

Berechtigungen schreiben
------------------------

In das Feld „Berechtigungen“ einer Crawl-Konfiguration tragen Sie Werte in den folgenden Formaten ein, einen pro Zeile.
Stimmt mindestens einer davon mit den Rechten des Benutzers überein, wird das Dokument in den Suchergebnissen angezeigt.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Format
     - Passende Benutzer
   * - ``{user}Benutzername``
     - Dieser Benutzer selbst
   * - ``{group}Gruppenname``
     - Benutzer, die dieser Gruppe angehören
   * - ``{role}Rollenname``
     - Benutzer, die diese Rolle haben
   * - ``(deny){group}Gruppenname``
     - Passenden Benutzern wird das Dokument nicht angezeigt, auch wenn ein anderer Wert es erlaubt (auch mit ``{user}`` und ``{role}`` verwendbar)

Rechte eines Benutzers
----------------------

Bei jeder Suche bestimmt Fess die Rechte des Benutzers wie folgt.

- Angemeldeter Benutzer: ``{user}`` mit dem eigenen Benutzernamen, ``{group}`` für jede Gruppe, der er angehört, und ``{role}`` für jede Rolle, die er hat
- Nicht angemeldeter Besucher: ``{role}guest``

Wichtig ist dabei, dass angemeldete Benutzer ``{role}guest`` nicht erhalten.
Das Feld „Berechtigungen“ einer neuen Crawl-Konfiguration enthält von Anfang an ``{role}guest``.
Lassen Sie es unverändert, sind die Dokumente für nicht angemeldete Besucher sichtbar, für angemeldete Benutzer jedoch nicht.
Für Dokumente, die alle Mitarbeitenden sehen sollen, tragen Sie in die Berechtigungen eine Gruppe (oder Rolle) ein, der alle Mitarbeitenden angehören.

Beachten Sie außerdem, dass der anfängliche Benutzer ``admin`` die Rollen ``admin`` und ``guest`` hat.
Suchen Sie in einem Browser, in dem Sie noch an der Administrationsoberfläche angemeldet sind, wird als ``admin`` gesucht; dann werden nur Dokumente mit ``{role}guest`` angezeigt, die Dokumente der Abteilungen dagegen nicht.

Rollen oder Gruppen?
--------------------

Rollen und Gruppen werden auf genau dieselbe Weise abgeglichen.
Der Unterschied liegt darin, woher die Werte stammen.
In der Benutzerverwaltung von Fess können Sie jedem Benutzer sowohl Rollen als auch Gruppen zuweisen.
Bei der LDAP-Anbindung (Active Directory) werden die Gruppen, denen ein Benutzer angehört (``memberOf``), zu ``{group}Gruppenname`` (nur Einträge, deren DN ``ou=Role`` enthält, werden zu ``{role}``).

In diesem Artikel werden alle Organisationseinheiten wie Abteilungen und die gesamte Belegschaft als Gruppen abgebildet, damit dieselben Berechtigungswerte sowohl für Fess-Benutzer als auch für Active Directory funktionieren.

Was wir aufbauen
================

Als Beispiel dient ein Unternehmen, dessen Intranetportal ``https://intra.example.com/`` Seiten für jede Abteilung und Seiten für das gesamte Unternehmen enthält.

.. list-table:: Gruppen und Benutzer
   :header-rows: 1
   :widths: 20 40 40

   * - Benutzer
     - Abteilung
     - Gruppen
   * - ``sato``
     - Vertrieb
     - ``Sales``, ``AllStaff``
   * - ``suzuki``
     - Entwicklung
     - ``Engineering``, ``AllStaff``
   * - ``tanaka``
     - Personalabteilung
     - ``HR``, ``AllStaff``
   * - ``yamada``
     - Geschäftsleitung
     - ``Executives``, ``AllStaff``

.. list-table:: Berechtigungen der Crawl-Konfigurationen
   :header-rows: 1
   :widths: 25 40 35

   * - Crawl-Konfiguration
     - URL
     - Berechtigungen
   * - Vertrieb
     - ``https://intra.example.com/sales/``
     - ``{group}Sales`` und ``{group}Executives``
   * - Entwicklung
     - ``https://intra.example.com/dev/``
     - ``{group}Engineering`` und ``{group}Executives``
   * - Personalabteilung
     - ``https://intra.example.com/hr/``
     - ``{group}HR`` und ``{group}Executives``
   * - Unternehmensweit
     - ``https://intra.example.com/common/``
     - ``{group}AllStaff``

Mit dieser Konfiguration sieht jeder Benutzer die folgenden Dokumente.

.. list-table:: Für jeden Benutzer sichtbare Dokumente
   :header-rows: 1
   :widths: 30 70

   * - Benutzer
     - Dokumente in den Suchergebnissen
   * - ``sato``
     - Vertrieb, Unternehmensweit
   * - ``suzuki``
     - Entwicklung, Unternehmensweit
   * - ``tanaka``
     - Personalabteilung, Unternehmensweit
   * - ``yamada``
     - Vertrieb, Entwicklung, Personalabteilung, Unternehmensweit
   * - Nicht angemeldete Besucher
     - Keine
   * - ``admin`` (Suchseite)
     - Keine

Sollen auch nicht angemeldete Besucher die unternehmensweiten Dokumente sehen, fügen Sie der unternehmensweiten Konfiguration zusätzlich ``{role}guest`` hinzu.
In diesem Fall sieht auch ``admin`` die unternehmensweiten Dokumente.

Gruppennamen werden unter Beachtung der Groß- und Kleinschreibung abgeglichen.
``{group}sales`` und ``{group}Sales`` gelten als unterschiedliche Gruppen; schreiben Sie den Gruppennamen und den Berechtigungswert daher in exakt derselben Schreibweise.

Einrichtung mit Fess-Benutzern
==============================

Gruppen und Benutzer anlegen
----------------------------

1. Klicken Sie in der Administrationsoberfläche unter [Benutzer] > [Gruppe] auf [Neu erstellen], geben Sie unter „Name“ ``Sales`` ein und klicken Sie auf [Erstellen]. Legen Sie ``Engineering``, ``HR``, ``Executives`` und ``AllStaff`` auf dieselbe Weise an
2. Klicken Sie unter [Benutzer] > [Benutzer] auf [Neu erstellen] und geben Sie „Benutzername“, „Passwort“ und „Passwort (bestätigen)“ ein. Das Passwort muss mindestens 8 Zeichen lang sein
3. Wählen Sie unter „Gruppen“ die Gruppen gemäß der obigen Tabelle aus und klicken Sie auf [Erstellen]

Benutzer, Gruppen und Rollen werden in OpenSearch gespeichert und bleiben daher erhalten, auch wenn Sie die Container in Docker neu erstellen.

Crawl-Konfigurationen anlegen
-----------------------------

Legen Sie für jede Abteilung unter [Crawler] > [Web] eine Crawl-Konfiguration an.
Die folgende Tabelle zeigt das Beispiel für den Vertrieb.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Wert
   * - Name
     - ``Vertriebsportal``
   * - URLs
     - ``https://intra.example.com/sales/``
   * - Eingeschlossene URLs
     - ``https://intra.example.com/sales/.*``
   * - Berechtigungen
     - Löschen Sie den Standardwert ``{role}guest`` und geben Sie die folgenden zwei Zeilen ein

::

    {group}Sales
    {group}Executives

Legen Sie Entwicklung, Personalabteilung und Unternehmensweit auf dieselbe Weise an und ändern Sie dabei URL und Berechtigungen gemäß der Tabelle.
Klicken Sie anschließend unter [System] > [Scheduler] bei „Default Crawler“ auf [Jetzt starten], um den Crawl auszuführen.
Wie Sie prüfen, ob der Crawl abgeschlossen ist, lesen Sie in :doc:`guide-02`.

.. note::

   Bei Crawl-Konfigurationen für Dateisysteme (SMB oder lokale Dateien) werden die aus der ACL der Datei gelesenen Rechte **zusätzlich** zu den Werten unter „Berechtigungen“ im Dokument gespeichert.
   Dieses Verhalten ist standardmäßig aktiviert.
   Dokumente auf einem Dateiserver können daher für einen größeren Kreis sichtbar sein, als unter „Berechtigungen“ angegeben.
   Wie sich dies mit ACLs kombinieren lässt, lesen Sie in :doc:`file-server-search`.
   Berechtigungen in Crawl-Konfigurationen für Datenspeicher werden in :doc:`datastore-basics` behandelt.

Gruppen aus Active Directory verwenden
======================================

Werden Ihre Benutzer in Active Directory verwaltet, richten Sie die LDAP-Anbindung ein, statt Benutzer und Gruppen in Fess anzulegen.
Die Gruppen im Attribut ``memberOf`` des angemeldeten Benutzers werden zu ``{group}``-Rechten.

LDAP-Verbindung konfigurieren
-----------------------------

Füllen Sie unter [System] > [Allgemein] den Abschnitt „LDAP“ aus und klicken Sie auf [Aktualisieren].

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Beispiel
   * - LDAP-URL
     - ``ldap://ad.example.com:389``
   * - Basis-DN
     - ``dc=example,dc=com``
   * - Bind-DN
     - ``cn=fess,cn=Users,dc=example,dc=com`` (Dienstkonto für die Suche)
   * - Passwort
     - Passwort des Dienstkontos
   * - Benutzer-DN
     - ``%s@example.com`` (``%s`` wird durch den Anmeldenamen ersetzt)
   * - Kontofilter
     - ``sAMAccountName=%s``
   * - memberOf-Attribut
     - ``memberOf``

Einzelheiten zu den Feldern und dazu, wie Sie einen „Gruppenfilter“ zum Auflösen verschachtelter Gruppen schreiben, finden Sie im `LDAP-Integrationsleitfaden <https://fess.codelibs.org/de/stable/config/ldap-integration.html>`__.

.. warning::

   Die Einstellungen unter [Allgemein] werden in ``system.properties`` gespeichert.
   Im Aufbau von docker-fess liegt diese Datei im Container ``fess01`` und geht daher verloren, wenn Sie den Container mit ``down`` → ``up`` neu erstellen (siehe den Abschnitt über das Stoppen und Neustarten in :doc:`guide-02`).

Zuordnung von Gruppennamen zu Berechtigungen
--------------------------------------------

Der Wert des innersten ``CN`` im DN der Gruppe wird zum Gruppennamen.

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - Wert von memberOf
     - Recht des Benutzers
   * - ``CN=Sales,OU=Groups,DC=example,DC=com``
     - ``{group}Sales``
   * - ``CN=AllStaff,OU=Groups,DC=example,DC=com``
     - ``{group}AllStaff``

Nennen Sie die Gruppen in Active Directory ``Sales``, ``Engineering``, ``HR``, ``Executives`` und ``AllStaff``, funktionieren die Crawl-Konfigurationen aus dem vorigen Kapitel unverändert.
Weichen die Namen ab, passen Sie die Berechtigungswerte an die Gruppennamen in Active Directory an.

Legen Sie für die gesamte Belegschaft eine Gruppe an, der alle direkt angehören.
Die primäre Gruppe in Active Directory (meist ``Domain Users``) ist nicht im Attribut ``memberOf`` enthalten; ``{group}Domain Users`` passt daher nicht.

Welche Rechte ein Benutzer erhalten hat, können Sie prüfen, indem Sie die Protokollstufe von ``org.codelibs.fess.ldap`` auf DEBUG setzen.
Werden die Rechte aus LDAP abgerufen, wird eine Zeile, die mit ``Roles:`` beginnt, in ``fess.log`` ausgegeben.
Wie Sie das einstellen, lesen Sie im Abschnitt „Debug-Einstellungen“ des LDAP-Integrationsleitfadens.
Die Werte in dieser Zeile erscheinen im weiter unten beschriebenen internen Format (etwa ``2Sales``).

Sollen sich Benutzer per SSO (Entra ID, OpenID Connect, SAML, SPNEGO) anmelden, benötigen Sie für das jeweilige Verfahren ein ``fess-sso-*``-Plugin.
Auch die Art, wie Gruppen und Rollen übernommen werden, unterscheidet sich je nach Verfahren; lesen Sie dazu :doc:`guide-15`.

Sichtbarkeit von Labels angleichen
==================================

Auch Labels haben „Berechtigungen“; sie bestimmen, ob das Label unter den Label-Optionen der Suchseite angezeigt wird.
Auf die Sichtbarkeit der Dokumente haben sie keinen Einfluss. Da aber auch neue Labels von Anfang an ``{role}guest`` enthalten, erscheinen sie unverändert nicht in den Optionen angemeldeter Benutzer.

Hier ein Beispiel für ein Label, das Dokumenten der Personalabteilung zugeordnet wird.
Klicken Sie unter [Crawler] > [Label] auf [Neu erstellen] und geben Sie Folgendes ein.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Wert
   * - Name
     - ``Personalabteilung``
   * - Wert
     - ``hr`` (nur alphanumerische Zeichen und Unterstriche)
   * - Eingeschlossene Pfade
     - ``https://intra.example.com/hr/.*``
   * - Berechtigungen
     - ``{group}HR`` und ``{group}Executives`` (derselbe Kreis wie bei den Dokumenten)

Die Berechtigungen eines Labels wirken sich auf die Optionen aus, sobald Sie es speichern.
Die Einstellung „Eingeschlossene Pfade“, über die das Label Dokumenten zugeordnet wird, wird dagegen beim Crawlen angewendet; führen Sie daher nach dem Anlegen des Labels einen Crawl aus.

Nach Änderung der Rechte neu crawlen
====================================

Berechtigungen werden beim Crawlen im Dokument gespeichert.
Ändern Sie die „Berechtigungen“ einer Crawl-Konfiguration, ändern sich die Rechte der bereits im Index befindlichen Dokumente nicht.
Führen Sie nach der Änderung einen Job aus, der diese Crawl-Konfiguration enthält (etwa „Default Crawler“).

Bei Crawl-Konfigurationen für Web und Dateisysteme werden Dokumente mit geänderten Rechten beim nächsten Crawl erneut abgerufen, und das alte Dokument mit derselben URL wird ersetzt.
Bis der erneute Crawl abgeschlossen ist, erscheinen die Dokumente weiterhin mit den alten Rechten in den Suchergebnissen.
Wenn Sie die Sichtbarkeit einschränken, führen Sie den Crawl sofort aus.

Um nur eine bestimmte Crawl-Konfiguration sofort neu zu crawlen, klicken Sie auf der Detailseite dieser Crawl-Konfiguration auf [Neuen Job erstellen] und führen den erstellten Job mit [Jetzt starten] aus.

Das Verhalten prüfen
====================

Als einzelne Benutzer suchen
----------------------------

1. Öffnen Sie ``http://localhost:8080/`` in einem privaten Browserfenster. In einem Fenster, das an der Administrationsoberfläche angemeldet ist, wird als ``admin`` gesucht
2. Suchen Sie ohne Anmeldung und prüfen Sie, dass weder Dokumente der Abteilungen noch unternehmensweite Dokumente angezeigt werden
3. Melden Sie sich über den Anmeldelink oben auf der Suchseite als ``sato`` an und prüfen Sie, dass nur Dokumente des Vertriebs und unternehmensweite Dokumente angezeigt werden
4. Klicken Sie oben auf der Seite auf den Benutzernamen, wählen Sie „Abmelden“ und prüfen Sie dasselbe mit ``suzuki``, ``tanaka`` und ``yamada``

Suchen Sie beim Prüfen nach einem Wort, das in allen Dokumenten vorkommt (etwa dem Firmennamen); so lässt sich der Umfang der angezeigten Dokumente leichter vergleichen.

Im Dokument gespeicherte Rechte ansehen
---------------------------------------

Werden Dokumente nicht wie erwartet angezeigt, prüfen Sie die im Dokument gespeicherten Rechte.

1. Öffnen Sie in der Administrationsoberfläche [Systeminformationen] > [Suche] und suchen Sie nach Wörtern aus der URL oder dem Titel des Dokuments. Diese Seite filtert nicht nach Rechten und zeigt alle Dokumente an
2. Klicken Sie beim betreffenden Dokument auf [Aktualisieren]; die Bearbeitungsseite öffnet sich und zeigt im Feld ``role`` die gespeicherten Rechte an. Sehen Sie sie nur an und speichern Sie nicht

Die Werte im Feld ``role`` werden im folgenden internen Format angezeigt.

.. list-table::
   :header-rows: 1
   :widths: 35 30 35

   * - Berechtigung
     - Anzeige im Feld role
     - Beispiel
   * - ``{user}Benutzername``
     - ``1`` + Name
     - ``1sato``
   * - ``{group}Gruppenname``
     - ``2`` + Name
     - ``2Sales``
   * - ``{role}Rollenname``
     - ``R`` + Name
     - ``Rguest``
   * - Mit ``(deny)``
     - ``D`` vorangestellt
     - ``D2Sales``

Enthält das Feld ``role`` eines Vertriebsdokuments ``2Sales`` und ``2Executives``, sind die Berechtigungen wie konfiguriert gespeichert.
Ist noch ``Rguest`` vorhanden, wurde nach der Änderung der Berechtigungen nicht neu gecrawlt, oder der Standardwert ``{role}guest`` wurde nicht gelöscht.

Nicht angemeldeten Benutzern nichts anzeigen
============================================

Wenn Sie Fess in einem Netzwerk betreiben, das auch Personen außerhalb des Unternehmens erreichen können, oder wenn Sie die Suche ohne Anmeldung grundsätzlich nicht zulassen, aktivieren Sie unter [System] > [Allgemein] die Option „Anmeldung erforderlich“.
Ist sie aktiviert, können nicht angemeldete Besucher nicht mehr suchen.

Diese Einstellung ist unabhängig von der Steuerung über Berechtigungen.
Selbst wenn noch Dokumente mit ``{role}guest`` vorhanden sind, werden sie nicht angemeldeten Besuchern nicht mehr angezeigt.
Auch diese Einstellung wird in ``system.properties`` gespeichert; unter Docker ist daher dieselbe Vorsicht geboten wie bei den LDAP-Einstellungen.

Weiterführende Artikel
======================

- Sichtbarkeit über die ACLs eines Dateiservers steuern: :doc:`file-server-search`
- Benutzer per SSO mit ihrem Firmenkonto anmelden lassen: :doc:`guide-15`
- Ein Fess für mehrere Organisationen nutzen: :doc:`guide-13`
- Auch Dokumenten aus Slack oder Cloud-Speichern Rechte zuweisen: :doc:`datastore-basics`
- Git, Confluence, Jira und Slack eines Entwicklungsteams durchsuchen: :doc:`guide-06`

Referenzen
==========

- `Konfiguration rollenbasierter Suche <https://fess.codelibs.org/de/stable/config/security-role.html>`__
- `Rollenbasierte Suche (für Benutzer) <https://fess.codelibs.org/de/stable/user/role-search.html>`__
- `LDAP-Integrationsleitfaden <https://fess.codelibs.org/de/stable/config/ldap-integration.html>`__
- `Benutzer <https://fess.codelibs.org/de/stable/admin/user-guide.html>`__
- `Gruppe <https://fess.codelibs.org/de/stable/admin/group-guide.html>`__
- `Label <https://fess.codelibs.org/de/stable/admin/labeltype-guide.html>`__
- `Suche (Administrationsoberfläche) <https://fess.codelibs.org/de/stable/admin/searchlist-guide.html>`__
