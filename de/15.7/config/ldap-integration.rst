=====================================
LDAP-Integrationsleitfaden
=====================================

Übersicht
=========

|Fess| unterstützt die Integration mit LDAP-Servern (Lightweight Directory Access Protocol)
und ermöglicht damit Authentifizierung und Benutzerverwaltung in Unternehmensumgebungen.

Die LDAP-Integration ermöglicht:

- Benutzerauthentifizierung (Anmeldung) über Active Directory oder OpenLDAP
- Gruppen- und rollenbasierte Zugriffskontrolle
- Verwaltung von LDAP-Benutzern, -Rollen und -Gruppen über die Verwaltungsoberfläche (optional)

Unterstützte LDAP-Server
========================

|Fess| unterstützt die Integration mit folgenden LDAP-Servern:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Andere LDAP-v3-kompatible Server

Voraussetzungen
===============

- Netzwerkzugriff auf den LDAP-Server
- Dienstkonto für LDAP-Suchen (Bind-DN)
- Kenntnisse der LDAP-Struktur (Base-DN, Attributnamen usw.)

Übersicht der Konfigurationsmethoden
=====================================

Die LDAP-Konfiguration von |Fess| wird je nach Verwendungszweck an zwei Stellen verwaltet.

Verbindungs- und Authentifizierungseinstellungen (Verwaltungsoberfläche / ``system.properties``)
   Dies sind Einstellungen für die Verbindung zum LDAP-Server und die Anmeldeauthentifizierung.
   Sie können im Abschnitt „LDAP" auf der Seite **„System > Allgemein"** der Verwaltungsoberfläche
   konfiguriert werden und werden in ``app/WEB-INF/conf/system.properties`` gespeichert.

LDAP-Verwaltungsfunktionen und Verhaltenseinstellungen (``fess_config.properties``)
   Dies sind Einstellungen für die Funktion zur Verwaltung von LDAP-Benutzern, -Rollen und
   -Gruppen über die Verwaltungsoberfläche sowie für das Verhalten bei der Rollenauflösung.
   Diese sind in ``app/WEB-INF/classes/fess_config.properties`` definiert.
   Zum Ändern von Werten bearbeiten Sie diese Datei direkt.

.. note::

   Wenn Sie ausschließlich die Anmeldeauthentifizierung verwenden möchten, genügen die
   „Verbindungs- und Authentifizierungseinstellungen". Die „LDAP-Verwaltungsfunktion"
   (``ldap.admin.enabled``) ist nur erforderlich, wenn Sie LDAP-Benutzer, -Rollen oder
   -Gruppen über die Verwaltungsoberfläche erstellen, aktualisieren oder löschen möchten.

Verbindungs- und Authentifizierungseinstellungen
================================================

Diese Einstellungen können im Abschnitt „LDAP" unter „System > Allgemein" der
Verwaltungsoberfläche konfiguriert werden und werden in
``app/WEB-INF/conf/system.properties`` gespeichert. Sie können die Datei auch direkt
bearbeiten.

.. list-table:: Verbindungs- und Authentifizierungseigenschaften
   :header-rows: 1
   :widths: 30 15 55

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``ldap.provider.url``
     - (nicht gesetzt)
     - URL des LDAP-Servers. Beispiel: ``ldap://ldap.example.com:389``. Für LDAPS: ``ldaps://ldap.example.com:636``. Mehrere URLs durch Leerzeichen getrennt ermöglichen Failover.
   * - ``ldap.base.dn``
     - (nicht gesetzt)
     - Basis-DN für die LDAP-Suche. Beispiel: ``dc=example,dc=com``
   * - ``ldap.security.principal``
     - (nicht gesetzt)
     - DN-Vorlage für die Benutzerauthentifizierung (Bind). ``%s`` wird durch den Benutzernamen ersetzt. Beispiel: ``uid=%s,ou=People,dc=example,dc=com``
   * - ``ldap.security.authentication``
     - ``simple``
     - LDAP-Authentifizierungsmethode (JNDI ``java.naming.security.authentication``). In der Regel wird ``simple`` verwendet.
   * - ``ldap.initial.context.factory``
     - ``com.sun.jndi.ldap.LdapCtxFactory``
     - JNDI-Klasse für die initiale Kontextfabrik. In der Regel ist keine Änderung erforderlich.
   * - ``ldap.admin.security.principal``
     - (nicht gesetzt)
     - Bind-DN des Dienstkontos für LDAP-Suchen. Beispiel: ``cn=fess,ou=services,dc=example,dc=com``
   * - ``ldap.admin.security.credentials``
     - (nicht gesetzt)
     - Passwort des oben genannten Dienstkontos.
   * - ``ldap.account.filter``
     - (nicht gesetzt)
     - Filter zur Suche nach Benutzereinträgen bei der Rollenauflösung. ``%s`` wird durch den Benutzernamen ersetzt. Beispiel: ``uid=%s``
   * - ``ldap.group.filter``
     - (leer)
     - Suchfilter für die Gruppenauflösung. ``%s`` wird durch den DN des Benutzers o. Ä. ersetzt. Beispiel: ``(member=%s)``
   * - ``ldap.memberof.attribute``
     - ``memberOf``
     - Attributname für die Gruppenmitgliedschaft. Wird zur Rollenauflösung bei Active Directory und Servern mit diesem Attribut verwendet.

Konfigurationsbeispiel (bei direkter Bearbeitung von ``system.properties``):

::

    # URL des LDAP-Servers
    ldap.provider.url=ldap://ldap.example.com:389

    # Basis-DN
    ldap.base.dn=dc=example,dc=com

    # Bind-DN-Vorlage fuer die Benutzerauthentifizierung (%s wird durch den Benutzernamen ersetzt)
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Bind-DN und Passwort des Dienstkontos fuer Suchen
    ldap.admin.security.principal=cn=fess,ou=services,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Filter fuer die Rollenaufloesung
    ldap.account.filter=uid=%s
    ldap.group.filter=(member=%s)

.. note::

   Der ``%s``-Platzhalter wird durch Javas ``String.format()`` verarbeitet.
   ``ldap.security.principal``, ``ldap.account.filter``, ``ldap.group.filter`` und
   alle administrativen Filter verwenden das ``%s``-Format (nicht das ``{0}``-Format).
   Der an die Filter übergebene Benutzername wird in |Fess| intern automatisch
   gegen LDAP-Injection-Angriffe escapet.

LDAP-Verwaltungsfunktionen und Verhaltenseinstellungen
======================================================

Die folgenden Eigenschaften sind in ``app/WEB-INF/classes/fess_config.properties``
definiert. Zum Ändern von Werten bearbeiten Sie diese Datei.

Aktivierung der Verwaltungsfunktion
------------------------------------

.. list-table:: Eigenschaften der Verwaltungsfunktion
   :header-rows: 1
   :widths: 35 15 50

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``ldap.admin.enabled``
     - ``false``
     - Aktiviert die Funktion zum Erstellen, Aktualisieren und Löschen von LDAP-Benutzern, -Rollen und -Gruppen über die Verwaltungsoberfläche. **Nicht erforderlich für die Anmeldeauthentifizierung** — die LDAP-Anmeldung funktioniert auch ohne Aktivierung.
   * - ``ldap.admin.sync.password``
     - ``true``
     - Synchronisiert das |Fess|-Passwort mit LDAP, wenn ein Benutzer über die Verwaltungsoberfläche aktualisiert wird.
   * - ``ldap.auth.validation``
     - ``true``
     - Überprüft die LDAP-Authentifizierung beim Anmelden.

Filter und Basis-DNs für die Benutzer-/Rollen-/Gruppenverwaltung
-----------------------------------------------------------------

Wird verwendet, um LDAP-Einträge über die Verwaltungsoberfläche zu bearbeiten, wenn ``ldap.admin.enabled=true`` gesetzt ist.

.. list-table:: Administrative Filter und Basis-DNs
   :header-rows: 1
   :widths: 38 47 15

   * - Eigenschaft
     - Beschreibung
     - Standardwert
   * - ``ldap.admin.user.filter``
     - Benutzer-Suchfilter (``%s`` wird durch den Benutzernamen ersetzt)
     - ``uid=%s``
   * - ``ldap.admin.user.base.dn``
     - Basis-DN für die Benutzersuche
     - ``ou=People,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.user.object.classes``
     - objectClass bei der Benutzererstellung
     - ``organizationalPerson,top,person,inetOrgPerson``
   * - ``ldap.admin.role.filter``
     - Rollen-Suchfilter
     - ``cn=%s``
   * - ``ldap.admin.role.base.dn``
     - Basis-DN für die Rollensuche
     - ``ou=Role,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.role.object.classes``
     - objectClass bei der Rollenerstellung
     - ``groupOfNames``
   * - ``ldap.admin.group.filter``
     - Gruppen-Suchfilter
     - ``cn=%s``
   * - ``ldap.admin.group.base.dn``
     - Basis-DN für die Gruppensuche
     - ``ou=Group,dc=fess,dc=codelibs,dc=org``
   * - ``ldap.admin.group.object.classes``
     - objectClass bei der Gruppenerstellung
     - ``groupOfNames``

Steuerung der Rollenauflösung und des Verhaltens
-------------------------------------------------

Steuert das Verhalten bei der Rollen- und Gruppenauflösung nach der Anmeldung.

.. list-table:: Verhaltenssteuerungseigenschaften
   :header-rows: 1
   :widths: 40 15 45

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``ldap.role.search.user.enabled``
     - ``true``
     - Weist Rollen basierend auf dem Benutzernamen zu.
   * - ``ldap.role.search.group.enabled``
     - ``true``
     - Weist Rollen basierend auf Gruppen zu.
   * - ``ldap.role.search.role.enabled``
     - ``true``
     - Weist Rollen basierend auf Rollen zu.
   * - ``ldap.allow.empty.permission``
     - ``true``
     - Erlaubt die Anmeldung für Benutzer ohne Gruppen oder Rollen.
   * - ``ldap.ignore.netbios.name``
     - ``true``
     - Entfernt NetBIOS-Präfixe (Format ``DOMAIN\``) aus Gruppennamen u. Ä.
   * - ``ldap.group.name.with.underscores``
     - ``false``
     - Erlaubt Unterstriche in Gruppennamen.
   * - ``ldap.lowercase.permission.name``
     - ``false``
     - Konvertiert Berechtigungsnamen in Kleinbuchstaben.
   * - ``ldap.samaccountname.group``
     - ``false``
     - Verwendet das Attribut ``sAMAccountName`` als Gruppenname (für Active Directory).
   * - ``ldap.max.username.length``
     - ``-1``
     - Maximale Länge des Benutzernamens. ``-1`` bedeutet keine Einschränkung.

Attributzuordnung
-----------------

Die Zuordnung von LDAP-Attributen zu |Fess|-Benutzerattributen wird über
``ldap.attr.*``-Eigenschaften definiert. In der Regel ist keine Änderung erforderlich,
sie kann jedoch bei abweichendem Schema angepasst werden. Typische Beispiele:

::

    ldap.attr.surname=sn
    ldap.attr.givenName=givenName
    ldap.attr.mail=mail
    ldap.attr.displayName=displayName
    ldap.attr.telephoneNumber=telephoneNumber

.. note::

   Einige Eigenschaften stimmen nicht mit dem LDAP-Attributnamen überein, z. B. wird
   ``ldap.attr.state`` auf ``st`` und ``ldap.attr.city`` auf ``l`` gemappt.
   Die vollständige Liste finden Sie in ``fess_config.properties`` in den Zeilen,
   die mit ``ldap.attr.`` beginnen.

Active-Directory-Konfiguration
==============================

Konfigurationsbeispiel für Microsoft Active Directory (``system.properties`` oder Verwaltungsoberfläche).

::

    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Bind-DN-Vorlage fuer die Benutzerauthentifizierung (UPN-Format)
    ldap.security.principal=%s@example.com

    # Dienstkonto fuer Suchen
    ldap.admin.security.principal=cn=fess,cn=Users,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Kontofilter
    ldap.account.filter=sAMAccountName=%s

    # memberOf-Attribut verwenden
    ldap.memberof.attribute=memberOf

    # Gruppenfilter
    ldap.group.filter=(member=%s)

Zur Auflösung verschachtelter Gruppen (Nested Groups) kann die Active-Directory-spezifische
``LDAP_MATCHING_RULE_IN_CHAIN``-Regel verwendet werden.

::

    ldap.group.filter=(member:1.2.840.113556.1.4.1941:=%s)

OpenLDAP-Konfiguration
======================

Konfigurationsbeispiel für OpenLDAP.

::

    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Bind-DN-Vorlage fuer die Benutzerauthentifizierung
    ldap.security.principal=uid=%s,ou=People,dc=example,dc=com

    # Dienstkonto fuer Suchen
    ldap.admin.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Kontofilter
    ldap.account.filter=uid=%s

    # Gruppenfilter (fuer posixGroup)
    ldap.group.filter=(memberUid=%s)

.. note::

   Standard-OpenLDAP verfügt nicht über das Attribut ``memberOf``, daher werden
   Gruppen über ``ldap.group.filter`` aufgelöst. Wenn das ``memberof``-Overlay
   aktiviert ist, kann auch ``ldap.memberof.attribute`` verwendet werden.

Sicherheitseinstellungen
========================

LDAPS (SSL/TLS)
---------------

Verschlüsselte Verbindung verwenden:

::

    # LDAPS verwenden
    ldap.provider.url=ldaps://ldap.example.com:636

Bei selbstsignierten Zertifikaten importieren Sie das Zertifikat in den Java-Truststore.

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Passwortschutz
--------------

``ldap.admin.security.credentials`` wird in ``system.properties`` gespeichert.
Die über die Verwaltungsoberfläche eingegebenen Anmeldedaten werden intern
verschlüsselt abgelegt. Beschränken Sie die Dateizugriffsberechtigungen
entsprechend.

Failover
========

Um ein Failover auf mehrere LDAP-Server zu konfigurieren, geben Sie in
``ldap.provider.url`` mehrere URLs durch Leerzeichen getrennt an.

::

    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Fehlerbehebung
==============

Verbindungsfehler
-----------------

**Symptom**: LDAP-Verbindung schlägt fehl

**Zu prüfen**:

1. Ist der LDAP-Server gestartet?
2. Ist der Port in der Firewall geöffnet (389 oder 636)?
3. Ist ``ldap.provider.url`` korrekt (``ldap://`` oder ``ldaps://``)?
4. Sind ``ldap.admin.security.principal`` und das Passwort korrekt?

Authentifizierungsfehler
------------------------

**Symptom**: Benutzerauthentifizierung schlägt fehl

**Zu prüfen**:

1. Ist die Vorlage in ``ldap.security.principal`` korrekt (enthält sie ``%s``)?
2. Existiert der Benutzer innerhalb des angegebenen Basis-DN?
3. Ist ``ldap.account.filter`` korrekt?

Gruppen/Rollen können nicht abgerufen werden
--------------------------------------------

**Symptom**: Gruppen oder Rollen des Benutzers können nicht abgerufen werden

**Zu prüfen**:

1. Ist ``ldap.group.filter`` korrekt?
2. Ist ``ldap.memberof.attribute`` korrekt (bei Active Directory)?
3. Befinden sich die Gruppen innerhalb des Suche-Basis-DN?
4. Sind die ``ldap.role.search.*.enabled``-Einstellungen aktiviert?

Benutzerverwaltung über die Verwaltungsoberfläche nicht möglich
---------------------------------------------------------------

**Symptom**: LDAP-Benutzer können über die Verwaltungsoberfläche nicht erstellt, bearbeitet oder gelöscht werden

**Zu prüfen**:

1. Ist ``ldap.admin.enabled`` auf ``true`` gesetzt?
2. Sind die administrativen Basis-DNs wie ``ldap.admin.user.base.dn`` korrekt?
3. Hat das Dienstkonto von ``ldap.admin.security.principal`` Schreibrechte?

Debug-Einstellungen
-------------------

Um detaillierte Protokolle auszugeben, fügen Sie einen Logger in
``app/WEB-INF/classes/log4j2.xml`` hinzu.

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Referenzinformationen
=====================

- :doc:`security-role` - Rollenbasierte Zugriffskontrolle
- :doc:`sso-spnego` - SPNEGO (Kerberos)-Authentifizierung
- :doc:`../admin/user-guide` - Benutzerverwaltungsleitfaden
