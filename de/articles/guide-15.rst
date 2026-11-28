==========================================
Suche mit SSO und Zugriffsschutz absichern
==========================================

Einführung
==========

In einer unternehmensinternen Suchplattform laufen Dokumente zusammen, die durch Berechtigungen geschützt sind.
In den meisten Einführungsprojekten lautet die Anforderung: Statt Fess-eigene Passwörter zu verteilen, sollen sich die Benutzer über den Identitätsanbieter (IdP) des Unternehmens anmelden, und die Suchergebnisse sollen anhand ihrer Gruppen eingeschränkt werden.

In diesem Artikel nehmen wir in Fess 15.9 die folgenden Einstellungen vor und prüfen jeweils, dass sie funktionieren.

- Single Sign-On (SSO) mit Entra ID, OpenID Connect, SAML oder SPNEGO
- Mit „Anmeldung erforderlich“ verhindern, dass nicht angemeldete Benutzer suchen
- Fess hinter einem Reverse-Proxy, der TLS terminiert, HTTPS korrekt erkennen lassen
- Zugriffstoken sowie die Aufbewahrungsfristen von Audit-Protokoll und Suchprotokoll überprüfen

Wie Sie Rollen und Gruppen entwerfen und in den Berechtigungen der Crawl-Konfigurationen angeben, behandelt :doc:`guide-05`.

SSO wird durch Plugins bereitgestellt
=====================================

In Fess 15.9 wurde die SSO-Authentifizierung aus dem Kern in vier Plugins ausgelagert.

.. list-table::
   :header-rows: 1
   :widths: 16 18 18 22 26

   * - Verfahren
     - Plugin
     - „SSO Type“ (``sso.type``)
     - Herkunft des Benutzernamens
     - Herkunft von Gruppen und Rollen
   * - Microsoft Entra ID
     - ``fess-sso-entraid``
     - Entra ID (``entraid``)
     - Benutzername des angemeldeten Kontos (in der Regel der UPN)
     - Über Microsoft Graph abgerufene Gruppen und Rollen
   * - OpenID Connect
     - ``fess-sso-oidc``
     - OpenID Connect (``oic``)
     - Claim ``email`` des ID-Tokens
     - Claim ``groups`` des ID-Tokens. Rollen nur aus „Standardrollen“
   * - SAML 2.0
     - ``fess-sso-saml``
     - SAML (``saml``)
     - NameID der Assertion
     - Werte der Attribute aus „Name des Gruppenattributs“ (Standard ``memberOf``) und „Name des Rollenattributs“
   * - SPNEGO (Kerberos)
     - ``fess-sso-spnego``
     - SPNEGO (``spnego``)
     - Teil des Kerberos-Prinzipals vor dem ``@``
     - Über die LDAP-Einstellungen unter [Allgemein] abgerufene Gruppen

Nur bei OpenID Connect unterscheiden sich der Plugin-Name (``oidc``) und der Wert von ``sso.type`` (``oic``).

Das Vorgehen ist bei allen Verfahren gleich.

1. Plugin installieren und Fess neu starten
2. Fess beim IdP registrieren. Die Rücksprungadresse (Umleitungs-URI bzw. ACS-URL) ist ``https://<Fess-Host>/sso/``
3. In der Administrationsoberfläche unter [System] > [Allgemein] die Angaben des IdP im Abschnitt des jeweiligen Verfahrens eintragen, „SSO Type“ auswählen und aktualisieren
4. ``https://<Fess-Host>/sso/`` im Browser öffnen und prüfen, dass die Anmeldung über den IdP gelingt

Plugin installieren
-------------------

Das Docker-Image (``ghcr.io/codelibs/fess:15.9.0``) enthält die vier SSO-Plugins (Images mit ``-slim`` im Namen enthalten sie nicht).
Den ZIP-, DEB- und RPM-Paketen liegen sie nicht bei; installieren Sie sie daher unter [System] > [Plugin] über [Installieren] oder mit dem folgenden Befehl.

::

    $ bin/fess-setup install plugin fess-sso-entraid

Starten Sie Fess nach dem Installieren oder Entfernen neu.
Verwenden Sie Plugins derselben Minor-Version wie Fess (15.9.x).

Wählen Sie „SSO Type“ aus, ohne dass das Plugin installiert ist, führt ``/sso/`` nur zurück zum Anmeldebildschirm, und in ``fess.log`` erscheint einmalig die WARN-Meldung ``No SSO authenticator is registered as ...``.

Speicherort der Einstellungen
-----------------------------

Die unter [Allgemein] eingegebenen Werte werden in ``system.properties`` gespeichert (beim ZIP-Paket in ``app/WEB-INF/conf/``, bei DEB und RPM in ``/etc/fess/``).
Die Einstellungen für OpenID Connect, SAML und Entra ID werden bei jeder Anmeldung gelesen und gelten daher sofort nach dem Speichern, ohne Neustart.
Die SPNEGO-Einstellungen werden im gesamten Prozess gemeinsam genutzt; nach einer Änderung ist daher ein Neustart erforderlich.

Der Container ``fess01`` in Docker hat kein Volume, sodass die Einstellungen unter [Allgemein] verloren gehen, wenn Sie nach ``docker compose down`` wieder ``up`` ausführen.
Laden Sie vor dem Neuerstellen des Containers ``system.properties`` unter [Systeminformationen] > [Sicherung] herunter und stellen Sie die Datei nach dem Neuerstellen über denselben Bildschirm per Upload wieder her.

SSO mit Entra ID
================

In Organisationen, die Microsoft 365 nutzen, ist ``fess-sso-entraid`` der einfachste Weg.
Die Gruppen werden nach der Anmeldung über Microsoft Graph abgerufen, daher müssen beim IdP keine Gruppen-Claims konfiguriert werden.

Einstellungen in Entra ID
-------------------------

Legen Sie im Azure Portal unter „App-Registrierungen“ eine neue Registrierung an und konfigurieren Sie sie wie folgt.

- Unterstützte Kontotypen: Nur Konten in diesem Organisationsverzeichnis
- Umleitungs-URI: ``https://fess.example.com/sso/`` mit der Plattform „Web“ (muss einschließlich des abschließenden ``/`` übereinstimmen)
- Unter „Zertifikate & Geheimnisse“ ein Clientgeheimnis erstellen und den Wert notieren (er wird nur direkt nach dem Erstellen angezeigt)
- Unter „API-Berechtigungen“ die delegierten Microsoft-Graph-Berechtigungen ``User.Read`` und ``GroupMember.Read.All`` hinzufügen und die Administratorzustimmung erteilen

Ohne ``GroupMember.Read.All`` können verschachtelte übergeordnete Gruppen nicht abgerufen werden, und in ``fess.log`` erscheint die Warnung ``Not allowed to read the parent groups of ...``.

Einstellungen in Fess
---------------------

Tragen Sie die Werte im Abschnitt „Entra ID“ unter [System] > [Allgemein] ein.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Feld
     - Schlüssel
     - Wert
   * - Mandant (ID oder Domäne)
     - ``entraid.tenant``
     - Verzeichnis-ID (Mandanten-ID) oder ``yourcompany.onmicrosoft.com``
   * - Client-ID
     - ``entraid.client.id``
     - Anwendungs-ID (Client-ID)
   * - Geheimer Clientschlüssel
     - ``entraid.client.secret``
     - Wert des erstellten Geheimnisses
   * - Antwort-URL
     - ``entraid.reply.url``
     - ``https://fess.example.com/sso/``

Wählen Sie zum Schluss im Abschnitt „System“ unter „SSO Type“ den Eintrag „Entra ID“ aus und klicken Sie auf [Aktualisieren].

Gruppen und Dokumentberechtigungen in Einklang bringen
------------------------------------------------------

Bei den aus Entra ID erhaltenen Gruppen und Rollen wird stets ihre ID (GUID) zu einer Berechtigung.
Zusätzlich werden die Werte der in „Berechtigungsfelder“ (``entraid.permission.fields``, Standard ``mail``) aufgeführten Attribute zu Berechtigungen.

Sicherheitsgruppen sind nicht E-Mail-aktiviert, daher wird mit dem Standardwert nur ihre GUID zu einer Berechtigung.
Wenn die ACLs des Dateiservers mit Gruppennamen geschrieben sind, setzen Sie „Berechtigungsfelder“ auf ``mail,displayName``.
``displayName`` ist jedoch nicht eindeutig: Gibt es eine Gruppe mit demselben Namen wie eine integrierte Windows-Gruppe (etwa ``Administrators``), stimmt sie auch mit den Dokumenten dieser integrierten Gruppe überein.

Tragen Sie in den Berechtigungen der Crawl-Konfiguration den abgerufenen Wert unverändert mit dem Präfix ``{group}`` ein (z. B. ``{group}sales@example.com``).

.. warning::

   „Standardrollen“ (``entraid.default.roles``) erhalten alle Benutzer des Mandanten.
   Tragen Sie hier ``admin`` ein, kann jeder die Administrationsoberfläche betreten.

SSO mit OpenID Connect, SAML oder SPNEGO
========================================

OpenID Connect
--------------

Mit OpenID-Connect-Anbietern wie Keycloak oder Okta wird Fess über ``fess-sso-oidc`` angebunden.
Registrieren Sie Fess beim Anbieter als Webanwendung (Client) und setzen Sie die Umleitungs-URI auf ``https://fess.example.com/sso/``.

Die wichtigsten Felder im Abschnitt „OpenID Connect“ unter [Allgemein] sind:

- Autorisierungsserver-URL (``oic.auth.server.url``) und Token-Server-URL (``oic.token.server.url``): Tragen Sie die jeweiligen Werte aus ``/.well-known/openid-configuration`` des Anbieters einzeln ein. Die Token-Server-URL muss ``https`` verwenden (nur für ``localhost``, ``127.x.x.x`` und ``::1`` ist ``http`` erlaubt)
- Client-ID und Geheimer Clientschlüssel
- Scope: ``openid email``. Der Benutzername wird aus dem Claim ``email`` gelesen, daher ist ``email`` erforderlich
- Basis-URL (``oic.base.url``): ``https://fess.example.com``. Bleibt die Weiterleitungs-URL leer, gilt ``{Basis-URL}/sso/``

Bei den Gruppen werden die Werte des Claims ``groups`` im ID-Token unverändert zu Berechtigungen.
Anders als bei Entra ID werden übergeordnete Gruppen nicht verfolgt; benötigen Sie verschachtelte Gruppen, nehmen Sie diese beim Anbieter in den Claim auf.
Rollen werden nicht aus Claims übernommen; es werden nur die Werte aus „Standardrollen“ vergeben.

``oic.issuer``, mit dem der Aussteller (``iss``) geprüft wird, hat kein Feld unter [Allgemein] und wird direkt in ``system.properties`` eingetragen.

SAML
----

Mit ``fess-sso-saml`` arbeitet Fess als SP.
Der IdP sendet die Assertion per Cross-Site-POST zurück, daher wird die Anmeldung mit dem Standardwert ``tomcat.sameSiteCookies = lax`` nicht abgeschlossen.
Ändern Sie den Wert in ``tomcat_config.properties`` wie folgt und starten Sie Fess neu.

::

    tomcat.sameSiteCookies = none

``none`` funktioniert nur mit HTTPS.
Über reines HTTP ist dann keine Anmeldung mehr möglich; nehmen Sie daher zuerst die weiter unten beschriebene HTTPS-Konfiguration vor.

Tragen Sie im Abschnitt „SAML“ unter [Allgemein] Folgendes ein.

- SP-Basis-URL (``saml.sp.base.url``): ``https://fess.example.com``. Daraus ergeben sich die Entity ID des SP (``{SP-Basis-URL}/sso/metadata``) und die ACS-URL (``{SP-Basis-URL}/sso/``)
- IdP Entity ID, IdP SSO URL und IdP-X.509-Zertifikat: aus der Verwaltungsoberfläche des IdP übernehmen. Das Zertifikat als Base64 in einer einzigen Zeile eingeben, ohne die Zeilen ``-----BEGIN CERTIFICATE-----``
- Name des Gruppenattributs (Standard ``memberOf``) und Name des Rollenattributs: an die vom IdP gesendeten Attributnamen anpassen

Eine Funktion zum Einlesen der Metadaten-URL des IdP gibt es nicht.
Umgekehrt lassen sich die SP-Metadaten von Fess unter ``https://fess.example.com/sso/metadata`` abrufen und in den IdP einlesen.
Der Benutzername ist die NameID; das NameID-Format ist standardmäßig das E-Mail-Adressformat.
Unterstützt wird nur die SP-initiierte Anmeldung, die bei ``/sso/`` von Fess beginnt; Anmeldungen, die über eine Kachel im Portal des IdP gestartet werden, werden abgewiesen.

Fügen Sie im Produktivbetrieb ``saml.security.want_assertions_signed=true`` zu ``system.properties`` hinzu, um signierte Assertions zu erzwingen.
Für die Signatur- und Verschlüsselungseinstellungen gibt es keine Felder unter [Allgemein], und sie lassen sich auch nicht als JVM-Systemeigenschaften angeben; tragen Sie sie daher direkt in die Datei ein.

.. warning::

   Ist „Name des Rollenattributs“ gesetzt, werden die vom IdP gesendeten Werte unverändert zu Fess-Rollen.
   Die Administratorrolle ist ``authentication.admin.roles=admin``; ein Benutzer, für den der IdP ``admin`` sendet, wird also zum Administrator.

SPNEGO (Windows-integrierte Authentifizierung)
----------------------------------------------

Damit sich Benutzer an domänenangehörigen Windows-Rechnern ohne Passworteingabe anmelden können, verwenden Sie ``fess-sso-spnego``.
Erforderlich sind die Registrierung eines SPN im AD (``setspn -S HTTP/<Fess-Hostname> <Dienstkonto>``), das Anlegen von ``krb5.conf`` und ``auth_login.conf`` in ``app/WEB-INF/classes/`` sowie die Intranet-Einstellungen des Browsers.
Die Gruppen werden über die Einstellungen im Abschnitt „LDAP“ unter [Allgemein] aus dem AD abgerufen.
Gehen Sie nach `SSO-Konfiguration mit Windows-integrierter Authentifizierung <https://fess.codelibs.org/de/stable/config/sso-spnego.html>`__ vor und starten Sie Fess neu, nachdem Sie die SPNEGO-Felder unter [Allgemein] geändert haben.

Prüfen, ob SSO funktioniert
===========================

Öffnen Sie zunächst im abgemeldeten Zustand ``https://fess.example.com/sso/`` und prüfen Sie, dass Sie zum Anmeldebildschirm des IdP weitergeleitet werden.

Öffnen Sie nach der Anmeldung im selben Browser ``https://fess.example.com/api/v2/auth/me``.

::

    {"response":{"status":0,"authenticated":true,"user":{"user_id":"taro@example.com", ...
      "groups":[...],"permissions":[...],"admin":false,"permission_state":"RESOLVED"}}}

Prüfen Sie, ob ``groups`` die erwarteten Gruppen enthält und ob ``admin`` wie beabsichtigt gesetzt ist.
Bei Entra ID werden die Gruppen erst nach der Anmeldung abgerufen; unmittelbar danach steht ``permission_state`` daher auf ``PENDING`` und wechselt nach Abschluss des Abrufs auf ``RESOLVED``.

Auch im Audit-Protokoll ``audit.log`` wird eine ``LOGIN``-Zeile mit Benutzername und Berechtigungen aufgezeichnet.

Schlägt die Anmeldung fehl, kehren Sie zum Anmeldebildschirm zurück, und es wird „SSO-Anmeldevorgang fehlgeschlagen.“ angezeigt.
Die Ursache steht in ``fess.log`` als WARN-Meldung (etwa ``Failed to process SSO login``).

Auch bei fehlerhaften SSO-Einstellungen können Sie sich über ``/login/`` mit dem lokalen Benutzer ``admin`` anmelden und sie korrigieren.

.. note::

   Angemeldete Benutzer erhalten ``{role}guest`` nicht.
   Dokumente aus Crawl-Konfigurationen, die nur das standardmäßige ``{role}guest`` haben, verschwinden aus den Suchergebnissen von Benutzern, die sich per SSO angemeldet haben.
   Wie Sie Berechtigungen zusammenstellen, lesen Sie in :doc:`guide-05`.

Nicht angemeldete Benutzer von der Suche ausschließen
=====================================================

Wenn Sie unter [System] > [Allgemein] „Anmeldung erforderlich“ aktivieren, können nicht angemeldete Benutzer nicht mehr suchen.

- Ist SSO verfügbar (Plugin installiert und „SSO Type“ ausgewählt), werden Benutzer, die den Suchbildschirm des mitgelieferten Themes ``bootstrap`` öffnen, automatisch zu ``/sso/`` geleitet und kehren nach der Anmeldung beim IdP zu ihrer ursprünglichen Suche zurück
- Ohne SSO wird auf dem Suchbildschirm ein Anmeldedialog angezeigt
- Auch die Such-API unter ``/api/v2/`` ist nicht mehr anonym nutzbar; nur Aufrufe mit Zugriffstoken werden angenommen

Auch ohne „Anmeldung erforderlich“ zeigt der Anmeldelink auf dem Suchbildschirm auf ``/sso/``, wenn SSO verfügbar und „Anmeldelink anzeigen“ aktiviert ist.

Über HTTPS veröffentlichen
==========================

TLS am Reverse-Proxy terminieren
--------------------------------

Terminiert Nginx o. Ä. TLS und leitet die Anfragen per HTTP an Fess weiter, sehen die bei Fess eingehenden Anfragen wie ``http://`` aus.
In diesem Zustand schlägt die Prüfung der SAML-Assertion (Abgleich von ``Destination``) fehl, und SPNEGO bietet keinen Rückfall auf die Basic-Authentifizierung an.

Teilen Sie Fess in ``tomcat_config.properties`` das von außen sichtbare Schema und den Port mit.
Diese Datei liegt beim ZIP-Paket in ``lib/classes/``, bei DEB, RPM und im Docker-Image in ``/etc/fess/``.

::

    tomcat.secure=true
    tomcat.scheme=https
    tomcat.proxyPort=443

Reichen Sie auf der Proxy-Seite den ursprünglichen ``Host``-Header unverändert an Fess weiter (bei Nginx ``proxy_set_header Host $host;``).
Fess setzt den Hostnamen der Anfrage-URL nämlich aus dem ``Host``-Header zusammen.

Setzen Sie außerdem in ``fess_config.properties`` ``session.cookie.secure=true``, damit das Sitzungscookie das Attribut ``Secure`` erhält.
Standardmäßig (leer) entscheidet Tomcat; in Produktivumgebungen, in denen ein Proxy TLS terminiert, geben Sie ``true`` jedoch explizit an.
Auch wenn Sie für SAML ``tomcat.sameSiteCookies = none`` verwenden, benötigen Cookies mit ``SameSite=None`` das Attribut ``Secure``.

Nach Änderungen an beiden Dateien muss Fess neu gestartet werden.

TLS direkt in Fess annehmen
---------------------------

Ohne Proxy setzen Sie in ``tomcat_config.properties`` ``tomcat.SSLEnabled=true``, ``tomcat.certificateKeystoreFile``, ``tomcat.certificateKeystorePassword``, ``tomcat.certificateKeyAlias`` usw.
Ein Konfigurationsbeispiel finden Sie unter `Sicherheitseinstellungen <https://fess.codelibs.org/de/stable/install/security.html>`__.

OpenSearch-Port schließen
-------------------------

Die ``compose-opensearch3.yaml`` von docker-fess veröffentlicht OpenSearch mit deaktiviertem Security-Plugin auf Port 9200 des Hosts.
Fess verbindet sich über das Netzwerk zwischen den Containern (``http://search01:9200``); auf einem gemeinsam genutzten Server können Sie daher ``ports`` bei ``search01`` entfernen.

Zugriffstoken verwalten
=======================

Token, mit denen Geschäftssysteme die API aufrufen, erstellen Sie unter [System] > [Zugriffstoken].
Wie die API aufgerufen wird, behandelt :doc:`guide-11`; hier führen wir nur die Punkte für einen sicheren Betrieb auf.

- Geben Sie einem Such-Token nur die Berechtigungen der Dokumente, die das jeweilige System sehen darf (z. B. ``{group}sales``)
- Ein Token mit ``{role}admin-api`` kann nicht nur Dokumente registrieren, sondern alle Endpunkte der Admin API nutzen. Eine engere Berechtigung wie „nur Registrierung“ gibt es nicht
- Setzen Sie „Läuft ab“ und erstellen Sie das Token nach Ablauf neu. Löschen Sie nicht mehr benötigte Token
- Bewahren Sie Token auf der Serverseite auf und betten Sie sie nicht in JavaScript ein, das im Browser läuft
- Lassen Sie „Parametername“ leer. Ist er gesetzt, lassen sich über einen URL-Parameter Berechtigungen hinzufügen
- Behandeln Sie die Rolle ``admin-accesstoken``, die Token ausstellen kann, und die Rolle ``admin-accesstoken-view``, die deren Werte anzeigen kann, wie Administratoren

Aufbewahrungsdauer der Protokolle festlegen
===========================================

Speicherort und Überwachung der Protokolldateien behandelt :doc:`guide-10`.
Hier ordnen wir die Aufzeichnungen, die für Sicherheitsprüfungen dienen, und ihre Aufbewahrungsfristen.

Im Audit-Protokoll (``audit.log``) werden zeilenweise unter anderem Anmeldungen (``LOGIN``), fehlgeschlagene Anmeldungen (``LOGIN_FAILURE``), Abmeldungen (``LOGOUT``), Zugriffe auf die Administrationsoberfläche und die Admin API (``ACCESS``) sowie Ablehnungen wegen fehlender Rechte (``ACCESS_DENIED``) aufgezeichnet.
Die Datei wird beim ZIP-Paket in ``logs/``, bei DEB, RPM und im Docker-Image in ``/var/log/fess/`` geschrieben und kann auch unter [Systeminformationen] > [Protokolldatei] heruntergeladen werden.
Das Standardformat ist LTSV, im Docker-Image JSON im ECS-Format.
Rotierte Dateien werden nach 360 Tagen gelöscht (``backup.audit.max.age`` in ``log4j2.xml``).

Wer was gesucht hat, steht im in OpenSearch gespeicherten Suchprotokoll, das Sie unter [Systeminformationen] > [Suchprotokoll] einsehen können.
Der Standardwert von „Alte Suchprotokolle löschen“ unter [Allgemein] ist ``-1``; Suchprotokolle werden also nicht gelöscht, sondern dauerhaft behalten.
Diese Anzahl Tage gilt auch für Klickprotokoll, Favoritenprotokoll und Chatprotokoll.
Ist die Aufbewahrungsfrist durch interne Vorgaben festgelegt, tragen Sie diese Anzahl Tage ein.

Betrieb mit mehreren Instanzen
==============================

In Fess 15.9 liegen die Anmeldesitzungen im Arbeitsspeicher des jeweiligen Fess-Prozesses.
Auch die während des SSO verwendeten Werte (``state`` bei OpenID Connect, die AuthnRequest-ID bei SAML) werden in der Sitzung abgelegt; wenn Sie mehrere Instanzen hinter einen Load Balancer stellen, aktivieren Sie daher Sticky Sessions, damit derselbe Benutzer immer an dasselbe Fess geleitet wird.
Zum Aufbau mit mehreren Instanzen selbst siehe :doc:`guide-14`.

Das Speichern von Sitzungen in OpenSearch zur gemeinsamen Nutzung durch mehrere Instanzen sowie die Passkey-Anmeldung lokaler Benutzer sind Funktionen ab 15.10.

Weiterführende Artikel
======================

- Rollen und Gruppen entwerfen und Berechtigungen in Crawl-Konfigurationen angeben: :doc:`guide-05`
- API-Anbindung mit Zugriffstoken: :doc:`guide-11`
- Speicherort der Protokolle, Überwachung und Sicherung: :doc:`guide-10`
- Erweiterung auf mehrere Instanzen: :doc:`guide-14`
- ACLs des Dateiservers in den Suchergebnissen berücksichtigen: :doc:`file-server-search`

Referenzen
==========

- `SSO-Konfiguration mit Entra ID <https://fess.codelibs.org/de/stable/config/sso-entraid.html>`__
- `SSO-Konfiguration mit OpenID Connect <https://fess.codelibs.org/de/stable/config/sso-oidc.html>`__
- `SAML-Authentifizierung SSO-Einrichtung <https://fess.codelibs.org/de/stable/config/sso-saml.html>`__
- `SSO-Konfiguration mit Windows-integrierter Authentifizierung <https://fess.codelibs.org/de/stable/config/sso-spnego.html>`__
- `Allgemein <https://fess.codelibs.org/de/stable/admin/general-guide.html>`__
- `Zugriffstoken <https://fess.codelibs.org/de/stable/admin/accesstoken-guide.html>`__
- `Sicherheitseinstellungen <https://fess.codelibs.org/de/stable/install/security.html>`__
- `Protokollkonfiguration <https://fess.codelibs.org/de/stable/config/admin-logging.html>`__
