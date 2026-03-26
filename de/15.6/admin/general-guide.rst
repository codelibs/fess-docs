=========
Allgemein
=========

Übersicht
=========

Auf dieser Verwaltungsseite können Sie die Konfiguration von |Fess| verwalten.
Sie können verschiedene Konfigurationen von |Fess| ändern, ohne |Fess| neu zu starten.

|image0|

Konfigurationsinhalt
====================

System
------

JSON-Antwort
::::::::::::

Gibt an, ob die JSON-API aktiviert werden soll.

Anmeldung erforderlich
::::::::::::::::::::::

Gibt an, ob eine Anmeldung für die Suchfunktion erforderlich ist.

Anmeldelink anzeigen
::::::::::::::::::::

Konfiguriert, ob auf dem Suchbildschirm ein Link zur Anmeldeseite angezeigt werden soll.

Doppelte Ergebnisse ausblenden
:::::::::::::::::::::::::::::::

Konfiguriert, ob das Ausblenden doppelter Ergebnisse aktiviert werden soll.

Miniaturansicht anzeigen
::::::::::::::::::::::::

Konfiguriert, ob die Miniaturansicht aktiviert werden soll.

Standard-Labelwert
:::::::::::::::::::

Beschreiben Sie den Label-Wert, der standardmäßig zur Suchbedingung hinzugefügt werden soll.
Um ihn für Rollen oder Gruppen anzugeben, fügen Sie „role:" oder „group:" hinzu, wie z. B. „role:admin=label1".

Standard-Sortierwert
::::::::::::::::::::

Beschreiben Sie den Sortierwert, der standardmäßig zur Suchbedingung hinzugefügt werden soll.
Um ihn für Rollen oder Gruppen anzugeben, fügen Sie „role:" oder „group:" hinzu, wie z. B. „role:admin=content_length.desc".

Virtueller Host
:::::::::::::::

Konfigurieren Sie den virtuellen Host.
Weitere Details finden Sie unter :doc:`Virtueller Host im Konfigurationshandbuch <../config/virtual-host>`.

Antwort für beliebtes Wort
::::::::::::::::::::::::::

Gibt an, ob die API für beliebte Wörter aktiviert werden soll.

CSV-Dateikodierung
:::::::::::::::::::

Geben Sie die Kodierung für heruntergeladene CSV-Dateien an.

Suchparameter anhängen
::::::::::::::::::::::

Aktivieren Sie dies, wenn Sie Parameter an die Suchergebnisanzeige übergeben möchten.

Suchdatei-Proxy
:::::::::::::::

Gibt an, ob der Datei-Proxy für Suchergebnisse aktiviert werden soll.

Browser-Gebietsschema verwenden
::::::::::::::::::::::::::::::::

Gibt an, ob das Browser-Gebietsschema für die Suche verwendet werden soll.

SSO-Typ
:::::::

Gibt den Typ der Einmalanmeldung (Single Sign-On) an.

- **Keine**: SSO nicht verwenden
- **OpenID Connect**: OpenID Connect verwenden
- **SAML**: SAML verwenden
- **SPNEGO**: SPNEGO verwenden
- **Entra ID**: Microsoft Entra ID verwenden

Crawler
-------

Letzte Änderung prüfen
::::::::::::::::::::::

Aktivieren Sie dies für differenzielles Crawling.

Gleichzeitige Crawler-Konfiguration
:::::::::::::::::::::::::::::::::::::

Geben Sie die Anzahl der gleichzeitig auszuführenden Crawl-Konfigurationen an.

Benutzer-Agent
::::::::::::::

Geben Sie den Benutzer-Agent-Namen an, der vom Crawler verwendet wird.

Alte Dokumente löschen
::::::::::::::::::::::

Geben Sie die Anzahl der Tage für die Gültigkeitsdauer nach der Indizierung an.

Fehlertypen ignorieren
::::::::::::::::::::::

Fehler-URLs, die den Schwellenwert überschreiten, werden vom Crawlen ausgeschlossen, aber hier angegebene Ausnahmenamen werden auch dann gecrawlt, wenn sie den Schwellenwert überschreiten.

Fehleranzahlschwelle
::::::::::::::::::::

Wenn ein zu crawlendes Dokument mehr als die hier angegebene Anzahl in Fehler-URLs aufgezeichnet wurde, wird es beim nächsten Crawl ausgeschlossen.

Protokollierung
---------------

Suchprotokoll
:::::::::::::

Gibt an, ob die Suchprotokollierung aktiviert werden soll.

Benutzerprotokoll
:::::::::::::::::

Gibt an, ob die Benutzerprotokollierung aktiviert werden soll.

Favoritenprotokoll
::::::::::::::::::

Gibt an, ob die Favoritenprotokollierung aktiviert werden soll.

Alte Suchprotokolle löschen
:::::::::::::::::::::::::::

Löscht Suchprotokolle, die älter als die angegebene Anzahl von Tagen sind.

Alte Jobprotokolle löschen
::::::::::::::::::::::::::

Löscht Jobprotokolle, die älter als die angegebene Anzahl von Tagen sind.

Alte Benutzerprotokolle löschen
:::::::::::::::::::::::::::::::

Löscht Benutzerprotokolle, die älter als die angegebene Anzahl von Tagen sind.

Bot-Namen zum Löschen von Protokollen
::::::::::::::::::::::::::::::::::::::

Geben Sie Bot-Namen an, die aus Suchprotokollen ausgeschlossen werden sollen.

Protokollebene
::::::::::::::

Geben Sie die Protokollebene für fess.log an.

Protokollbenachrichtigung
:::::::::::::::::::::::::

Gibt an, ob die Protokollbenachrichtigungsfunktion aktiviert werden soll, die automatisch ERROR- und WARN-Protokollereignisse erfasst und Benachrichtigungen sendet.
Weitere Informationen finden Sie unter :doc:`Protokollbenachrichtigungskonfiguration <../config/admin-log-notification>`.

Protokollbenachrichtigungsebene
:::::::::::::::::::::::::::::::

Gibt die Protokollebene für Protokollbenachrichtigungen an.
Protokollereignisse auf der ausgewählten Ebene und darüber werden benachrichtigt.

- **ERROR**: Nur Fehler benachrichtigen (Standard)
- **WARN**: Warnungen und höher benachrichtigen
- **INFO**: Informationen und höher benachrichtigen
- **DEBUG**: Debug und höher benachrichtigen
- **TRACE**: Alle Protokolle benachrichtigen

Vorschlagen
-----------

Vorschläge aus Suchbegriffen
::::::::::::::::::::::::::::

Gibt an, ob Vorschlagskandidaten aus Suchprotokollen generiert werden sollen.

Vorschläge aus Dokumenten
:::::::::::::::::::::::::

Gibt an, ob Vorschlagskandidaten aus indizierten Dokumenten generiert werden sollen.

Alte Vorschlagsinformationen löschen
:::::::::::::::::::::::::::::::::::::

Löscht Vorschlagsdaten, die älter als die angegebene Anzahl von Tagen sind.

LDAP
----

LDAP-URL
::::::::

Geben Sie die URL des LDAP-Servers an.

Basis-DN
::::::::

Geben Sie den Basis-Distinguished-Name für die Anmeldung am Suchbildschirm an.

Bind-DN
:::::::

Geben Sie den Bind-DN des Administrators an.

Passwort
::::::::

Geben Sie das Passwort für den Bind-DN an.

Benutzer-DN
:::::::::::

Geben Sie den Distinguished-Name des Benutzers an.

Kontofilter
:::::::::::

Geben Sie den Common Name oder die UID des Benutzers an.

Gruppenfilter
:::::::::::::

Geben Sie die Filterbedingung für abzurufende Gruppen an.

memberOf-Attribut
:::::::::::::::::

Geben Sie den memberOf-Attributnamen an, der auf dem LDAP-Server verfügbar ist.
Für Active Directory ist es memberOf.
Für andere LDAP-Server kann es isMemberOf sein.

Sicherheitsauthentifizierung
::::::::::::::::::::::::::::

Gibt die LDAP-Sicherheitsauthentifizierungsmethode an (z.B. simple).

Initiale Kontextfabrik
::::::::::::::::::::::

Gibt die LDAP-Klasse der initialen Kontextfabrik an (z.B. com.sun.jndi.ldap.LdapCtxFactory).

OpenID Connect
--------------

Client-ID
:::::::::

Gibt die Client-ID des OpenID Connect-Anbieters an.

Client-Geheimnis
::::::::::::::::

Gibt das Client-Geheimnis des OpenID Connect-Anbieters an.

Autorisierungsserver-URL
::::::::::::::::::::::::

Gibt die URL des Autorisierungsservers für OpenID Connect an.

Token-Server-URL
::::::::::::::::

Gibt die URL des Token-Servers für OpenID Connect an.

Weiterleitungs-URL
::::::::::::::::::

Gibt die Weiterleitungs-URL für OpenID Connect an.

Geltungsbereich
:::::::::::::::

Gibt den Geltungsbereich für OpenID Connect an.

Basis-URL
:::::::::

Gibt die Basis-URL für OpenID Connect an.

Standardgruppen
:::::::::::::::

Gibt die Standardgruppen an, die Benutzern bei der OpenID Connect-Authentifizierung zugewiesen werden.

Standardrollen
::::::::::::::

Gibt die Standardrollen an, die Benutzern bei der OpenID Connect-Authentifizierung zugewiesen werden.

SAML
----

SP-Basis-URL
::::::::::::

Gibt die Basis-URL des SAML Service Providers an.

Gruppenattributname
:::::::::::::::::::

Gibt den Attributnamen zum Abrufen von Gruppen aus der SAML-Antwort an.

Rollenattributname
::::::::::::::::::

Gibt den Attributnamen zum Abrufen von Rollen aus der SAML-Antwort an.

Standardgruppen
:::::::::::::::

Gibt die Standardgruppen an, die Benutzern bei der SAML-Authentifizierung zugewiesen werden.

Standardrollen
::::::::::::::

Gibt die Standardrollen an, die Benutzern bei der SAML-Authentifizierung zugewiesen werden.

SPNEGO
------

Krb5-Konfiguration
::::::::::::::::::

Gibt den Pfad zur Kerberos 5-Konfigurationsdatei an.

Anmeldekonfiguration
::::::::::::::::::::

Gibt den Pfad zur JAAS-Anmeldekonfigurationsdatei (Java Authentication and Authorization Service) an.

Anmelde-Client-Modul
::::::::::::::::::::

Gibt den Namen des JAAS-Client-Anmeldemoduls an.

Anmelde-Server-Modul
::::::::::::::::::::

Gibt den Namen des JAAS-Server-Anmeldemoduls an.

Vorab-Authentifizierung Benutzername
::::::::::::::::::::::::::::::::::::

Gibt den Benutzernamen für die SPNEGO-Vorab-Authentifizierung an.

Vorab-Authentifizierung Passwort
::::::::::::::::::::::::::::::::

Gibt das Passwort für die SPNEGO-Vorab-Authentifizierung an.

Basic-Authentifizierung erlauben
::::::::::::::::::::::::::::::::

Gibt an, ob Basic-Authentifizierung als Fallback erlaubt werden soll.

Unsichere Basic-Authentifizierung erlauben
::::::::::::::::::::::::::::::::::::::::::

Gibt an, ob Basic-Authentifizierung über unsichere (HTTP) Verbindungen erlaubt werden soll.

NTLM-Aufforderung
::::::::::::::::::

Gibt an, ob die NTLM-Aufforderung aktiviert werden soll.

Localhost erlauben
::::::::::::::::::

Gibt an, ob der Zugriff vom Localhost erlaubt werden soll.

Delegation erlauben
:::::::::::::::::::

Gibt an, ob Kerberos-Delegation erlaubt werden soll.

Verzeichnisse ausschließen
::::::::::::::::::::::::::

Gibt Verzeichnisse an, die von der SPNEGO-Authentifizierung ausgeschlossen werden sollen.

Entra ID
--------

Client-ID
:::::::::

Gibt die Anwendungs-(Client-)ID für Microsoft Entra ID an.

Client-Geheimnis
::::::::::::::::

Gibt das Client-Geheimnis für Microsoft Entra ID an.

Mandant
:::::::

Gibt die Mandanten-ID für Microsoft Entra ID an.

Autorität
:::::::::

Gibt die Autoritäts-URL für Microsoft Entra ID an.

Antwort-URL
:::::::::::

Gibt die Antwort-(Weiterleitungs-)URL für Microsoft Entra ID an.

Status-TTL
::::::::::

Gibt die Gültigkeitsdauer (TTL) des Authentifizierungsstatus an.

Standardgruppen
:::::::::::::::

Gibt die Standardgruppen an, die Benutzern bei der Entra ID-Authentifizierung zugewiesen werden.

Standardrollen
::::::::::::::

Gibt die Standardrollen an, die Benutzern bei der Entra ID-Authentifizierung zugewiesen werden.

Berechtigungsfelder
:::::::::::::::::::

Gibt die Felder an, aus denen Berechtigungsinformationen von Entra ID abgerufen werden.

Domänendienst verwenden
:::::::::::::::::::::::

Gibt an, ob der Entra ID-Domänendienst verwendet werden soll.

Hinweis
-------

Anmeldeseite
::::::::::::

Beschreiben Sie die Nachricht, die auf dem Anmeldebildschirm angezeigt werden soll.

Such-Startseite
:::::::::::::::

Beschreiben Sie die Nachricht, die auf dem Such-Startbildschirm angezeigt werden soll.

Erweiterte Suchseite
::::::::::::::::::::

Beschreiben Sie die Nachricht, die auf dem erweiterten Suchbildschirm angezeigt werden soll.

Benachrichtigung
----------------

Benachrichtigungs-E-Mail
:::::::::::::::::::::::::

Geben Sie die E-Mail-Adresse an, die bei Abschluss des Crawls benachrichtigt werden soll.
Mehrere Adressen können durch Kommas getrennt angegeben werden. Ein E-Mail-Server ist erforderlich.

Slack Webhook URL
:::::::::::::::::

Gibt die Webhook-URL für Slack-Benachrichtigungen an.

Google Chat Webhook URL
:::::::::::::::::::::::

Gibt die Webhook-URL für Google Chat-Benachrichtigungen an.

Speicher
--------

Nach der Konfiguration dieser Elemente wird das Menü [System > Speicher] im linken Menü angezeigt.
Informationen zur Dateiverwaltung finden Sie unter :doc:`Speicher <../admin/storage-guide>`.

Typ
:::

Geben Sie den Speichertyp an.
Bei Auswahl von „Automatisch" wird der Speichertyp automatisch anhand des Endpunkts bestimmt.

- **Automatisch**: Automatische Erkennung vom Endpunkt
- **S3**: Amazon S3
- **GCS**: Google Cloud Storage

Bucket
::::::

Geben Sie den zu verwaltenden Bucket-Namen an.

Endpunkt
::::::::

Geben Sie die Endpunkt-URL des Speicherservers an.

- S3: Verwendet den AWS-Standard-Endpunkt, wenn leer
- GCS: Verwendet den Google Cloud-Standard-Endpunkt, wenn leer
- MinIO usw.: Die Endpunkt-URL des MinIO-Servers

Zugriffsschlüssel
:::::::::::::::::

Geben Sie den Zugriffsschlüssel für S3 oder S3-kompatiblen Speicher an.

Geheimer Schlüssel
::::::::::::::::::

Geben Sie den geheimen Schlüssel für S3 oder S3-kompatiblen Speicher an.

Region
::::::

Geben Sie die S3-Region an (z.B. ap-northeast-1).

Projekt-ID
::::::::::

Geben Sie die Google Cloud-Projekt-ID für GCS an.

Anmeldedaten-Pfad
:::::::::::::::::

Geben Sie den Pfad zur Dienstkonto-Anmeldedaten-JSON-Datei für GCS an.

Beispiele
=========

LDAP-Konfigurationsbeispiele
-----------------------------

.. tabularcolumns:: |p{4cm}|p{4cm}|p{4cm}|
.. list-table:: LDAP/Active Directory-Konfiguration
   :header-rows: 1

   * - Name
     - Wert (LDAP)
     - Wert (Active Directory)
   * - LDAP-URL
     - ldap://SERVERNAME:389
     - ldap://SERVERNAME:389
   * - Basis-DN
     - cn=Directory Manager
     - dc=fess,dc=codelibs,dc=org
   * - Bind-DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - manager@fess.codelibs.org
   * - Benutzer-DN
     - uid=%s,ou=People,dc=fess,dc=codelibs,dc=org
     - %s@fess.codelibs.org
   * - Kontofilter
     - cn=%s oder uid=%s
     - (&(objectClass=user)(sAMAccountName=%s))
   * - Gruppenfilter
     -
     - (member:1.2.840.113556.1.4.1941:=%s)
   * - memberOf
     - isMemberOf
     - memberOf


.. |image0| image:: ../../../resources/images/en/15.6/admin/general-1.png
.. pdf            :height: 940 px
