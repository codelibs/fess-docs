==================================
LDAP-Integrationsleitfaden
==================================

Übersicht
==========

|Fess| unterstuetzt die Integration mit LDAP-Servern (Lightweight Directory Access Protocol),
was Authentifizierung und Benutzerverwaltung in Unternehmensumgebungen ermoeglicht.

Die LDAP-Integration ermoeglicht:

- Benutzerauthentifizierung mit Active Directory oder OpenLDAP
- Gruppenbasierte Zugriffskontrolle
- Automatische Benutzerinformations-Synchronisation

Unterstuetzte LDAP-Server
=========================

|Fess| unterstuetzt die Integration mit den folgenden LDAP-Servern:

- Microsoft Active Directory
- OpenLDAP
- 389 Directory Server
- Apache Directory Server
- Andere LDAP v3-kompatible Server

Voraussetzungen
===============

- Netzwerkzugriff auf den LDAP-Server
- Dienstkonto fuer LDAP-Suchen (Bind DN)
- Verstaendnis der LDAP-Struktur (Base DN, Attributnamen usw.)

Grundkonfiguration
==================

Fuegen Sie die folgende Konfiguration zu ``app/WEB-INF/conf/system.properties`` hinzu.

LDAP-Verbindungseinstellungen
-----------------------------

::

    # LDAP-Authentifizierung aktivieren
    ldap.admin.enabled=true

    # LDAP-Server-URL
    ldap.provider.url=ldap://ldap.example.com:389

    # Fuer sichere Verbindung (LDAPS)
    # ldap.provider.url=ldaps://ldap.example.com:636

    # Base DN
    ldap.base.dn=dc=example,dc=com

    # Bind DN (Dienstkonto)
    ldap.security.principal=cn=fess,ou=services,dc=example,dc=com

    # Bind-Passwort
    ldap.admin.security.credentials=your_password

Benutzersuche-Einstellungen
---------------------------

::

    # Benutzersuche Base DN
    ldap.user.search.base=ou=users,dc=example,dc=com

    # Benutzersuche-Filter
    ldap.user.search.filter=(uid={0})

    # Benutzername-Attribut
    ldap.user.name.attribute=uid

Gruppensuche-Einstellungen
--------------------------

::

    # Gruppensuche Base DN
    ldap.group.search.base=ou=groups,dc=example,dc=com

    # Gruppensuche-Filter
    ldap.group.search.filter=(member={0})

    # Gruppenname-Attribut
    ldap.group.name.attribute=cn

Active-Directory-Konfiguration
==============================

Konfigurationsbeispiel fuer Microsoft Active Directory.

Grundkonfiguration
------------------

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://ad.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Dienstkonto (UPN-Format)
    ldap.security.principal=fess@example.com
    ldap.admin.security.credentials=your_password

    # Benutzersuche
    ldap.user.search.base=ou=Users,dc=example,dc=com
    ldap.user.search.filter=(sAMAccountName={0})
    ldap.user.name.attribute=sAMAccountName

    # Gruppensuche
    ldap.group.search.base=ou=Groups,dc=example,dc=com
    ldap.group.search.filter=(member={0})
    ldap.group.name.attribute=cn

Active-Directory-spezifische Einstellungen
------------------------------------------

::

    # Verschachtelte Gruppenaufloesung
    ldap.memberof.enabled=true

    # memberOf-Attribut verwenden
    ldap.group.search.filter=(member:1.2.840.113556.1.4.1941:={0})

OpenLDAP-Konfiguration
======================

Konfigurationsbeispiel fuer OpenLDAP.

::

    ldap.admin.enabled=true
    ldap.provider.url=ldap://openldap.example.com:389
    ldap.base.dn=dc=example,dc=com

    # Dienstkonto
    ldap.security.principal=cn=admin,dc=example,dc=com
    ldap.admin.security.credentials=your_password

    # Benutzersuche
    ldap.user.search.base=ou=people,dc=example,dc=com
    ldap.user.search.filter=(uid={0})
    ldap.user.name.attribute=uid

    # Gruppensuche
    ldap.group.search.base=ou=groups,dc=example,dc=com
    ldap.group.search.filter=(memberUid={0})
    ldap.group.name.attribute=cn

Sicherheitseinstellungen
========================

LDAPS (SSL/TLS)
---------------

Verschluesselte Verbindungen verwenden:

::

    # LDAPS verwenden
    ldap.provider.url=ldaps://ldap.example.com:636

    # StartTLS verwenden
    ldap.start.tls=true

Fuer selbstsignierte Zertifikate importieren Sie das Zertifikat in den Java-Truststore:

::

    keytool -import -alias ldap-server -keystore $JAVA_HOME/lib/security/cacerts \
            -file ldap-server.crt

Passwortschutz
--------------

Passwoerter ueber Umgebungsvariablen festlegen:

::

    ldap.admin.security.credentials=${LDAP_PASSWORD}

Rollenzuordnung
===============

Sie koennen LDAP-Gruppen zu |Fess|-Rollen zuordnen.

Automatische Zuordnung
----------------------

Gruppennamen werden direkt als Rollennamen verwendet:

::

    # LDAP-Gruppe "fess-users" -> Fess-Rolle "fess-users"
    ldap.group.role.mapping.enabled=true

Benutzerdefinierte Zuordnung
----------------------------

::

    # Gruppennamen zu Rollen zuordnen
    ldap.group.role.mapping.Administrators=admin
    ldap.group.role.mapping.PowerUsers=editor
    ldap.group.role.mapping.Users=guest

Benutzerinformations-Synchronisation
====================================

Sie koennen Benutzerinformationen von LDAP zu |Fess| synchronisieren.

Automatische Synchronisation
----------------------------

Benutzerinformationen bei Anmeldung automatisch synchronisieren:

::

    ldap.user.sync.enabled=true

Zu synchronisierende Attribute
------------------------------

::

    # E-Mail-Adresse
    ldap.user.email.attribute=mail

    # Anzeigename
    ldap.user.displayname.attribute=displayName

Verbindungs-Pooling
===================

Verbindungspool-Einstellungen zur Leistungsverbesserung:

::

    # Verbindungspool aktivieren
    ldap.connection.pool.enabled=true

    # Minimale Verbindungen
    ldap.connection.pool.min=1

    # Maximale Verbindungen
    ldap.connection.pool.max=10

    # Verbindungs-Timeout (Millisekunden)
    ldap.connection.timeout=5000

Failover
========

Failover zu mehreren LDAP-Servern:

::

    # Mehrere URLs durch Leerzeichen getrennt angeben
    ldap.provider.url=ldap://ldap1.example.com:389 ldap://ldap2.example.com:389

Fehlerbehebung
==============

Verbindungsfehler
-----------------

**Symptom**: LDAP-Verbindung schlaegt fehl

**Pruefen**:

1. Ist der LDAP-Server gestartet?
2. Ist der Port in der Firewall geoeffnet (389 oder 636)?
3. Ist die URL korrekt (``ldap://`` oder ``ldaps://``)?
4. Sind Bind DN und Passwort korrekt?

Authentifizierungsfehler
------------------------

**Symptom**: Benutzerauthentifizierung schlaegt fehl

**Pruefen**:

1. Ist der Benutzersuche-Filter korrekt?
2. Existiert der Benutzer innerhalb des Suche-Base DN?
3. Ist das Benutzername-Attribut korrekt?

Gruppen koennen nicht abgerufen werden
--------------------------------------

**Symptom**: Benutzergruppen koennen nicht abgerufen werden

**Pruefen**:

1. Ist der Gruppensuche-Filter korrekt?
2. Ist das Gruppenmitgliedschafts-Attribut korrekt?
3. Existieren die Gruppen innerhalb des Suche-Base DN?

Debug-Einstellungen
-------------------

Detaillierte Protokolle ausgeben:

``app/WEB-INF/classes/log4j2.xml``:

::

    <Logger name="org.codelibs.fess.ldap" level="DEBUG"/>

Referenzinformationen
=====================

- :doc:`security-role` - Rollenbasierte Zugriffskontrolle
- :doc:`sso-spnego` - SPNEGO (Kerberos) Authentifizierung
- :doc:`../admin/user-guide` - Benutzerverwaltungsleitfaden
