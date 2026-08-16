=====================================
SSO-Konfiguration mit Entra ID
=====================================

Übersicht
=========

|Fess| unterstützt Single Sign-On (SSO)-Authentifizierung mit Microsoft Entra ID (ehemals Azure AD).
Durch die Verwendung der Entra ID-Authentifizierung können Benutzerinformationen und Gruppeninformationen aus Ihrer Microsoft 365-Umgebung mit der rollenbasierten Suche von |Fess| integriert werden.

Wie die Entra ID-Authentifizierung funktioniert
-----------------------------------------------

Bei der Entra ID-Authentifizierung fungiert |Fess| als OAuth 2.0/OpenID Connect-Client und arbeitet mit Microsoft Entra ID für die Authentifizierung zusammen.

1. Benutzer greift auf den |Fess| SSO-Endpunkt (``/sso/``) zu
2. |Fess| leitet zum Entra ID-Autorisierungsendpunkt weiter
3. Benutzer authentifiziert sich bei Entra ID (Microsoft-Anmeldung)
4. Entra ID leitet den Autorisierungscode an |Fess| weiter
5. |Fess| verwendet den Autorisierungscode, um ein Zugriffstoken zu erhalten
6. Benutzer wird angemeldet
7. Im Hintergrund verwendet |Fess| die Microsoft Graph API, um die Gruppen- und Rolleninformationen des Benutzers abzurufen, und wendet sie nach Abschluss der Auflösung auf die rollenbasierte Suche an

.. note::
   Ab |Fess| 15.8 wird die Autorisierungsantwort in Schritt 4 als GET-Anfrage zurückgegeben, da
   |Fess| beim Autorisierungsendpunkt ``response_mode=query`` anfordert. Bis 15.7 erfolgte dies
   über einen websiteübergreifenden POST, bei dem der ausgelieferte Standardwert
   ``tomcat.sameSiteCookies = lax`` das Sitzungscookie nicht mitsendet; deshalb war
   ``tomcat.sameSiteCookies = none`` als Umgehungslösung erforderlich. Wenn Sie ``none`` nur aus
   diesem Grund gesetzt haben, können Sie zum Standardwert zurückkehren.

Informationen zur Integration mit der rollenbasierten Suche finden Sie unter :doc:`security-role`.

Voraussetzungen
===============

Bevor Sie die Entra ID-Authentifizierung konfigurieren, überprüfen Sie die folgenden Voraussetzungen:

- |Fess| 15.8 oder höher ist installiert
- Ein Microsoft Entra ID (Azure AD)-Mandant ist verfügbar
- |Fess| ist über HTTPS erreichbar (für Produktionsumgebungen erforderlich)
- Sie haben die Berechtigung, Anwendungen in Entra ID zu registrieren

Grundkonfiguration
==================

SSO aktivieren
--------------

Um die Entra ID-Authentifizierung zu aktivieren, fügen Sie die folgende Einstellung in ``app/WEB-INF/conf/system.properties`` hinzu:

::

    sso.type=entraid

Erforderliche Einstellungen
---------------------------

Konfigurieren Sie die von Entra ID erhaltenen Informationen.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``entraid.tenant``
     - Mandanten-ID (z.B. ``xxx.onmicrosoft.com``)
     - (Erforderlich)
   * - ``entraid.client.id``
     - Anwendungs-(Client-)ID
     - (Erforderlich)
   * - ``entraid.client.secret``
     - Wert des Clientgeheimnisses
     - (Erforderlich)
   * - ``entraid.reply.url``
     - Umleitungs-URI (Callback-URL)
     - Verwendet Anfrage-URL

.. note::
   Anstelle des Präfixes ``entraid.*`` können Sie für die Abwärtskompatibilität auch das Legacy-Präfix ``aad.*`` verwenden.

Optionale Einstellungen
-----------------------

Die folgenden Einstellungen können bei Bedarf hinzugefügt werden.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``entraid.authority``
     - Authentifizierungsserver-URL
     - ``https://login.microsoftonline.com/``
   * - ``entraid.state.ttl``
     - State-Lebensdauer (Sekunden)
     - ``3600``
   * - ``entraid.response.mode``
     - Art, wie die Autorisierungsantwort zurückgegeben wird. Entweder ``query`` oder ``form_post``.
     - ``query``
   * - ``entraid.default.groups``
     - Standardgruppen (kommagetrennt). Werden auf jeden Entra ID-Benutzer angewendet.
     - (Keine)
   * - ``entraid.default.roles``
     - Standardrollen (kommagetrennt). Werden auf jeden Entra ID-Benutzer angewendet.
     - (Keine)
   * - ``entraid.permission.fields``
     - Gruppen-/Rollenfelder (kommagetrennt), die zusätzlich als Berechtigungswerte verwendet werden. Die Gruppen-/Rollen-ID (GUID) wird stets als Berechtigung verwendet; die hier angegebenen Felder (z.B. ``mail``) werden zusätzlich hinzugefügt. Verwendbar sind nur Felder, deren Wert eine Zeichenkette ist. Microsoft Graph liefert ein Feld wie ``securityEnabled`` als booleschen Wert und ``groupTypes`` als Liste; keines von beiden kann ein Berechtigungswert werden, ein solches Feld wird daher ignoriert und eine Warnung mit seinem Namen ins Protokoll geschrieben.
     - ``mail``
   * - ``entraid.use.ds``
     - Domänendienst-Integration. Bei ``true`` wird für Berechtigungswerte im Format ``name@domain`` auch der lokale Teil (``name``) ohne den Domänenanteil als Berechtigung hinzugefügt. Das gilt nicht nur für Gruppen und Rollen, sondern auch für den angemeldeten Benutzer selbst: Der lokale Teil seines Benutzerprinzipalnamens (UPN) wird als benutzerbezogene Berechtigung hinzugefügt. Mit ``false`` entfällt daher auch diese benutzerbezogene Berechtigung, nicht nur die der Gruppen.
     - ``true``

.. note::

   Die Gruppen-/Rollen-ID (GUID) wird stets als Berechtigung verwendet, aber nur E-Mail-aktivierte
   Gruppen besitzen einen ``mail``-Wert. Microsoft-365-Gruppen sind E-Mail-aktiviert, daher wird
   auch ihr Name als Berechtigung registriert. **Sicherheitsgruppen sind nicht E-Mail-aktiviert;
   mit dem Standardwert wird daher nur ihre GUID zu einer Berechtigung.** Wenn die Zugriffsrechte
   im Dateisystem eine Sicherheitsgruppe benennen, stimmen die Berechtigungen nicht überein und
   diese Dokumente erscheinen nicht in den Suchergebnissen.

   Fügen Sie in diesem Fall ``displayName`` hinzu, das jede Gruppe besitzt:

   .. code-block:: properties

      entraid.permission.fields=mail,displayName

   ``displayName`` ist nicht domänenqualifiziert und nicht eindeutig und deshalb nicht Teil des
   Standardwerts. Existiert in Entra ID beispielsweise eine Gruppe namens ``Administrators``, so
   passt sie auch auf Dokumente, deren Zugriffsrechte die integrierte Windows-Gruppe
   ``Administrators`` benennen. Prüfen Sie vor dem Hinzufügen, dass die Namen nicht mit den bereits
   in Ihren Zugriffsrechten verwendeten kollidieren.

.. note::
   Beim Standardwert ``query`` steht der Autorisierungscode in der Query-Zeichenfolge der
   Callback-URL. ``form_post`` hält den Code aus der URL heraus und damit auch aus dem
   Browserverlauf und den Zugriffsprotokollen vorgelagerter Proxys oder einer WAF. Allerdings wird
   der Callback dadurch zu einem websiteübergreifenden POST und erfordert
   ``tomcat.sameSiteCookies = none``. Ohne diese Einstellung wird das Sitzungscookie nicht
   zurückgesendet und die Anmeldung schlägt fehl. Browser akzeptieren ``none`` zudem nur bei einem
   Cookie, das auch das Attribut ``Secure`` trägt; ``form_post`` setzt daher voraus, dass |Fess|
   über HTTPS bereitgestellt wird. Über einfaches HTTP speichert der Browser das Sitzungscookie
   überhaupt nicht und die Anmeldung schlägt weiterhin fehl. Die meisten Installationen sollten
   daher beim Standardwert bleiben. Andere Werte werden mit einer Warnung ignoriert und ``query``
   wird verwendet.

.. warning::

   ``entraid.default.groups`` und ``entraid.default.roles`` sind einzelne globale Werte ohne
   benutzerbezogene Abgrenzung. |Fess| wendet sie bei der Anmeldung auf jeden Entra ID-Benutzer an
   und wendet sie bei jeder späteren Auflösung erneut an, sodass Microsoft Graph sie nie wieder
   entzieht. Tragen Sie insbesondere niemals die |Fess|-Administratorrolle — bei ausgeliefertem
   ``authentication.admin.roles`` also ``admin`` — in ``entraid.default.roles`` ein: Das gewährt
   jedem Benutzer im Mandanten dauerhaften Zugriff auf die Verwaltungsseiten.

Konfiguration auf der Entra ID-Seite
====================================

App-Registrierung im Azure Portal
---------------------------------

1. Melden Sie sich beim `Azure Portal <https://portal.azure.com/>`_ an

2. Wählen Sie **Microsoft Entra ID**

3. Gehen Sie zu **Verwalten** → **App-Registrierungen** → **Neue Registrierung**

4. Registrieren Sie die Anwendung:

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Einstellung
        - Wert
      * - Name
        - Beliebiger Name (z.B. Fess SSO)
      * - Unterstützte Kontotypen
        - "Nur Konten in diesem Organisationsverzeichnis"
      * - Plattform
        - Web
      * - Umleitungs-URI
        - ``https://<Fess-Host>/sso/``

5. Klicken Sie auf **Registrieren**

Erstellen eines Clientgeheimnisses
----------------------------------

1. Klicken Sie auf der App-Detailseite auf **Zertifikate & Geheimnisse**

2. Klicken Sie auf **Neues Clientgeheimnis**

3. Legen Sie eine Beschreibung und ein Ablaufdatum fest und klicken Sie auf **Hinzufügen**

4. Kopieren und speichern Sie den generierten **Wert** (dieser Wert wird nicht erneut angezeigt)

.. warning::
   Der Wert des Clientgeheimnisses wird nur unmittelbar nach der Erstellung angezeigt.
   Stellen Sie sicher, dass Sie ihn notieren, bevor Sie die Seite verlassen.

Konfigurieren der API-Berechtigungen
------------------------------------

1. Klicken Sie im linken Menü auf **API-Berechtigungen**

2. Klicken Sie auf **Berechtigung hinzufügen**

3. Wählen Sie **Microsoft Graph**

4. Wählen Sie **Delegierte Berechtigungen**

5. Fügen Sie die folgende Berechtigung hinzu:

   - ``User.Read`` - Erforderlich zum Abrufen der Gruppenmitgliedschaften des angemeldeten Benutzers (``/me/memberOf``). Wird beim Erstellen der App-Registrierung standardmäßig erteilt
   - ``GroupMember.Read.All`` - Erforderlich zum Lesen von Gruppenattributen wie dem Gruppennamen und zum Auflösen verschachtelter Gruppen

6. Klicken Sie auf **Berechtigungen hinzufügen**

7. Klicken Sie auf **Administratorzustimmung für <Mandantenname> erteilen**

.. note::
   Die Administratorzustimmung erfordert Mandantenadministratorrechte.

.. note::
   Anstelle von ``GroupMember.Read.All`` können auch ``Group.Read.All`` oder
   ``Directory.Read.All`` erteilt werden; das Abrufen der Gruppenattribute und das Auflösen
   verschachtelter Gruppen funktioniert damit ebenfalls. ``/me/memberOf`` wird durch
   ``Group.Read.All`` jedoch nicht autorisiert, sodass ``User.Read`` in jedem Fall erforderlich
   ist.

.. note::
   |Fess| fordert beim Token-Abruf den Scope ``https://graph.microsoft.com/.default`` an.
   Ab 15.8 wird zusätzlich ``openid profile offline_access https://graph.microsoft.com/.default`` an den Autorisierungsendpunkt gesendet, sodass die Zustimmung für denselben Umfang eingeholt wird.
   Das bedeutet, dass alle in der App-Registrierung konfigurierten und genehmigten Zugriffsberechtigungen verwendet werden.
   Um Gruppeninformationen abzurufen, müssen daher die oben genannten Berechtigungen zur App-Registrierung hinzugefügt und die Administratorzustimmung erteilt werden.

Zu erhaltende Informationen
---------------------------

Die folgenden Informationen werden für die Fess-Konfiguration verwendet:

- **Anwendungs-(Client-)ID**: Auf der Übersichtsseite als "Anwendungs-(Client-)ID" aufgeführt
- **Mandanten-ID**: Auf der Übersichtsseite als "Verzeichnis-(Mandanten-)ID" oder im Format ``xxx.onmicrosoft.com`` aufgeführt
- **Clientgeheimniswert**: Der in Zertifikate & Geheimnisse erstellte Wert

Gruppen- und Rollenzuordnung
============================

Mit der Entra ID-Authentifizierung ruft |Fess| automatisch die Gruppen und Rollen ab, zu denen ein Benutzer gehört, unter Verwendung der Microsoft Graph API.
Die abgerufenen Gruppen-IDs und Gruppennamen können für die rollenbasierte Suche von |Fess| verwendet werden.

Verschachtelte Gruppen
----------------------

|Fess| ruft nicht nur Gruppen ab, zu denen Benutzer direkt gehören, sondern auch die übergeordneten Gruppen, zu denen diese wiederum gehören (verschachtelte Gruppen).
Sowohl die direkte Mitgliedschaftsabfrage als auch die Suche nach übergeordneten Gruppen laufen nach der Anmeldung in derselben Hintergrundaufgabe, sodass die Anmeldung selbst nie durch Microsoft Graph verzögert wird.
Die Suche nach übergeordneten Gruppen verwendet den Microsoft Graph-Vorgang ``getMemberGroups``, der transitiv auflöst: Ein Aufruf je direkt zugewiesener Gruppe liefert alle darüberliegenden Gruppen, unabhängig davon, wie tief die Verschachtelung reicht. Die abgerufenen Ergebnisse werden für einen bestimmten Zeitraum zwischengespeichert.
Sobald diese Hintergrundaufgabe abgeschlossen ist, werden die Berechtigungen des Benutzers neu berechnet.

Standardgruppeneinstellungen
----------------------------

Um allen Entra ID-Benutzern gemeinsame Gruppen zuzuweisen:

::

    entraid.default.groups=authenticated_users,entra_users

Konfigurationsbeispiele
=======================

Minimale Konfiguration (zum Testen)
-----------------------------------

Das Folgende ist ein minimales Konfigurationsbeispiel zur Verifizierung in einer Testumgebung.

::

    # SSO aktivieren
    sso.type=entraid

    # Entra ID-Einstellungen
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=http://localhost:8080/sso/

Empfohlene Konfiguration (für Produktion)
-----------------------------------------

Das Folgende ist ein empfohlenes Konfigurationsbeispiel für Produktionsumgebungen.

::

    # SSO aktivieren
    sso.type=entraid

    # Entra ID-Einstellungen
    entraid.tenant=yourcompany.onmicrosoft.com
    entraid.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    entraid.client.secret=your-client-secret-value
    entraid.reply.url=https://fess.example.com/sso/

    # Standardgruppen (optional)
    entraid.default.groups=authenticated_users

Legacy-Konfiguration (Abwärtskompatibilität)
--------------------------------------------

Für die Kompatibilität mit früheren Versionen kann auch das Präfix ``aad.*`` verwendet werden.
Wenn eine ``entraid.*``-Eigenschaft nicht gesetzt ist, wird der Wert der entsprechenden ``aad.*``-Eigenschaft verwendet.
Außerdem wird ``sso.type=aad`` genauso behandelt wie ``sso.type=entraid``.

::

    # SSO aktivieren (sso.type=aad kann ebenfalls verwendet werden)
    sso.type=entraid

    # Legacy-Konfigurationsschlüssel
    aad.tenant=yourcompany.onmicrosoft.com
    aad.client.id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    aad.client.secret=your-client-secret-value
    aad.reply.url=https://fess.example.com/sso/

Fehlerbehebung
==============

Häufige Probleme und Lösungen
-----------------------------

Kann nach der Authentifizierung nicht zu Fess zurückkehren
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Umleitungs-URI in der Azure Portal-App-Registrierung korrekt konfiguriert ist
- Stellen Sie sicher, dass der Wert von ``entraid.reply.url`` genau mit der Azure Portal-Konfiguration übereinstimmt
- Überprüfen Sie, ob das Protokoll (HTTP/HTTPS) übereinstimmt
- Überprüfen Sie, ob die Umleitungs-URI mit ``/`` endet
- Wenn ``entraid.response.mode`` auf ``form_post`` gesetzt ist, prüfen Sie sowohl, ob
  ``tomcat.sameSiteCookies = none`` konfiguriert ist, als auch, ob |Fess| über HTTPS bereitgestellt
  wird. Beim ausgelieferten Standardwert ``lax`` sendet der Browser das Sitzungscookie nicht mit dem
  websiteübergreifenden POST des Callbacks; mit ``none`` über einfaches HTTP speichert der Browser
  dieses Cookie überhaupt nicht, da ``none`` das Attribut ``Secure`` voraussetzt. In beiden Fällen
  schlägt die Anmeldung genau einmal fehl: Der Browser kehrt zur Anmeldeseite zurück und zeigt
  "SSO-Anmeldevorgang fehlgeschlagen.", und im Protokoll erscheint eine Warnung mit dem Wortlaut
  ``Failed to process SSO login: could not validate state``

Authentifizierungsfehler treten auf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob Mandanten-ID, Client-ID und Clientgeheimnis korrekt konfiguriert sind
- Überprüfen Sie, ob das Clientgeheimnis nicht abgelaufen ist
- Überprüfen Sie, ob die Administratorzustimmung für API-Berechtigungen erteilt wurde

Gruppeninformationen können nicht abgerufen werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Berechtigungen ``User.Read`` und ``GroupMember.Read.All`` erteilt wurden
  (``GroupMember.Read.All`` kann durch ``Group.Read.All`` oder ``Directory.Read.All`` ersetzt
  werden, ``/me/memberOf`` benötigt jedoch weiterhin ``User.Read``)
- Überprüfen Sie, ob die Administratorzustimmung erteilt wurde
- Überprüfen Sie, ob der Benutzer in Entra ID zu Gruppen gehört
- Wenn verschachtelte übergeordnete Gruppen nicht aufgelöst werden können, wird die Warnung
  ``Not allowed to read the parent groups of ...`` protokolliert. Erteilen Sie in diesem Fall
  ``GroupMember.Read.All``
- |Fess| löst die Gruppen- und Rollenmitgliedschaft des Benutzers im Hintergrund auf, nachdem die
  Anmeldung abgeschlossen ist; die Anmeldung selbst wartet also nie auf Microsoft Graph. Bis die
  Auflösung abgeschlossen ist, besitzt der Benutzer nur seine eigene benutzerbezogene Berechtigung
  sowie die in ``entraid.default.groups`` und ``entraid.default.roles`` konfigurierten Gruppen und
  Rollen. Ist beides nicht gesetzt — der ausgelieferte Standard —, liefert eine Suche in diesem
  Zeitfenster überhaupt keine Dokumente: ``role.search.default.permissions`` ist ab Werk leer, und
  eine mit dem ausgelieferten ``role.search.default.display.permissions`` angelegte
  Crawl-Konfiguration vergibt ``{role}guest``, was ein angemeldeter Benutzer nicht besitzt. Das
  Zeitfenster umfasst bis zu etwa eine Sekunde Planungsverzögerung zuzüglich der Aufrufe von
  Microsoft Graph selbst — einer für die direkten Mitgliedschaften, dann je einer pro dieser
  Gruppen für den Durchlauf der verschachtelten Gruppen, nacheinander und bei kaltem Cache
  abgesetzt —, es wächst also mit der Anzahl der Gruppen des Benutzers. Währenddessen teilt die
  Suchseite dem Benutzer mit, dass seine Gruppen- und Rollenberechtigungen noch geladen werden,
  und bittet ihn, die Suche in einem Moment zu wiederholen
- Gelingt die Auflösung nicht vollständig, teilt die Suchseite dem Benutzer mit, dass seine
  Gruppen- und Rollenberechtigungen nicht vollständig geladen werden konnten, und bittet ihn, sich
  ab- und wieder anzumelden sowie bei wiederholtem Auftreten den Administrator zu kontaktieren.
  „Nicht vollständig“ ist bewusst gewählt: Die Auflösung gilt nur dann als erfolgreich, wenn sowohl
  die Abfrage der direkten Mitgliedschaften als auch der Durchlauf der verschachtelten Gruppen
  gelungen ist — ein Benutzer, der seine direkten Gruppen, aber nicht seine übergeordneten Gruppen
  besitzt, erhält diesen Hinweis also ebenfalls. Ein Fall ist davon ausgenommen, und zwar genau
  der aus dem vorherigen Punkt: Verweigert Microsoft Graph die Abfrage der verschachtelten Gruppen
  mit ``Authorization_RequestDenied``, weil ``GroupMember.Read.All`` nie erteilt wurde, wertet
  |Fess| das nicht als Fehlschlag, sondern als Antwort, die besagt, dass die Gruppe keine
  übergeordneten Gruppen hat. Die Auflösung gilt dann als erfolgreich und **es wird kein Hinweis
  angezeigt**, obwohl die Berechtigungen der übergeordneten Gruppen fehlen. Das einzige Anzeichen
  ist die Warnung ``Not allowed to read the parent groups of ...`` im Protokoll; prüfen Sie das
  Protokoll deshalb darauf, wann immer verschachtelte Gruppen im Einsatz sind. Häufigste Ursache des
  Teilfalls ist Drosselung:
  Ein einziges HTTP 429 oder 503 von Microsoft Graph lässt |Fess| so lange pausieren, wie es der
  Header ``Retry-After`` verlangt (60 Sekunden, wenn er nichts Verwertbares nennt, höchstens 60
  Minuten), und in dieser Zeit wird in der gesamten |Fess|-Instanz jede Abfrage verschachtelter
  Gruppen übersprungen, während die direkten Abfragen weiter beantwortet werden. Der Fehlschlag ist nicht zwangsläufig endgültig: Die Auflösung wird
  bei jeder Erneuerung des Zugriffstokens erneut angestoßen, und ein späterer Erfolg lässt den
  Hinweis verschwinden und stellt die fehlenden Berechtigungen wieder her. Abmelden und erneut
  anmelden versucht es sofort erneut — wird die SSO-Anmelde-URL im angemeldeten Zustand
  aufgerufen, erfolgt lediglich eine Umleitung zurück zur Suchseite

Debug-Einstellungen
-------------------

Um Probleme zu untersuchen, können Sie detaillierte Entra ID-bezogene Protokolle ausgeben, indem Sie die |Fess|-Protokollebene anpassen.

In ``app/WEB-INF/classes/log4j2.xml`` können Sie den folgenden Logger hinzufügen, um die Protokollebene zu ändern:

::

    <Logger name="org.codelibs.fess.sso.entraid" level="DEBUG"/>

Referenz
========

- :doc:`security-role` - Konfiguration der rollenbasierten Suche
- :doc:`sso-saml` - SSO-Konfiguration mit SAML-Authentifizierung
- :doc:`sso-oidc` - SSO-Konfiguration mit OpenID Connect-Authentifizierung
