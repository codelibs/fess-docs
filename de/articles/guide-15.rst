==================================
Teil 15: Sichere Suchinfrastruktur
==================================

Einleitung
==========

Die Anforderungen an die Informationssicherheit in Unternehmen werden von Jahr zu Jahr strenger.
Da Suchsysteme eine große Menge vertraulicher Dokumente zusammenführen, sind geeignete Authentifizierungs- und Autorisierungsmechanismen unerlässlich.

In diesem Artikel bauen wir auf der in Teil 5 vorgestellten rollenbasierten Suche auf und entwerfen eine Sicherheitsarchitektur mit Schwerpunkt auf SSO-Integration (Single Sign-On).

Zielgruppe
==========

- Personen, die Fess in einer Unternehmensumgebung betreiben
- Personen, die eine SSO-Integration (OIDC, SAML) planen
- Personen, die mit den Konzepten der Zero-Trust-Sicherheit vertraut sind

Übersicht der Sicherheitsanforderungen
==========================================

Im Folgenden werden die typischen Sicherheitsanforderungen für Unternehmen zusammengefasst.

.. list-table:: Sicherheitsanforderungen
   :header-rows: 1
   :widths: 30 70

   * - Anforderung
     - Beschreibung
   * - Single Sign-On
     - Integration mit einem bestehenden IdP, um zusätzliche Anmeldevorgänge zu vermeiden
   * - Rollenbasierter Zugriff
     - Steuerung der Suchergebnisse basierend auf Zugehörigkeit und Berechtigungen des Benutzers
   * - Verschlüsselung der Kommunikation
     - Verschlüsselung der gesamten Kommunikation über HTTPS
   * - API-Zugriffskontrolle
     - Tokenbasierte API-Authentifizierung und Berechtigungsverwaltung
   * - Audit-Protokolle
     - Aufzeichnung, wer was gesucht hat

SSO-Integrationsoptionen
==========================

Im Folgenden werden die von Fess unterstützten SSO-Protokolle und deren jeweilige Einsatzszenarien dargestellt.

.. list-table:: Vergleich der SSO-Protokolle
   :header-rows: 1
   :widths: 20 30 50

   * - Protokoll
     - Typische IdPs
     - Einsatzszenarien
   * - OpenID Connect
     - Entra ID, Keycloak, Google
     - Cloud-Umgebungen, moderne Authentifizierungsinfrastruktur
   * - SAML 2.0
     - Entra ID, Okta, OneLogin
     - Unternehmensumgebungen, wenn ein bestehender SAML-IdP vorhanden ist
   * - SPNEGO/Kerberos
     - Active Directory
     - Windows-Umgebungen mit integrierter Authentifizierung

SSO-Integration über OpenID Connect / Entra ID
==================================================

Dies ist der modernste und empfohlene Ansatz.
Neben der generischen OpenID-Connect-Integration bietet Fess auch eine dedizierte Integrationsfunktion für Entra ID (Azure AD).
Im Folgenden wird die Integration am Beispiel von Entra ID erläutert.

Übersicht des Authentifizierungsablaufs
------------------------------------------

1. Ein Benutzer greift auf Fess zu
2. Fess leitet den Benutzer zur Authentifizierungsseite von Entra ID weiter
3. Der Benutzer authentifiziert sich bei Entra ID (einschließlich MFA)
4. Entra ID gibt ein Authentifizierungstoken an Fess zurück
5. Fess ruft Benutzer- und Gruppeninformationen aus dem Token ab
6. Rollen werden basierend auf Gruppeninformationen zugewiesen
7. Suchergebnisse werden basierend auf den Rollen bereitgestellt

Konfiguration auf der Entra-ID-Seite
--------------------------------------

1. Registrieren Sie eine Anwendung in Entra ID
2. Konfigurieren Sie die Weiterleitungs-URI (Fess OIDC-Callback-URL)
3. Erteilen Sie die erforderlichen API-Berechtigungen (User.Read, GroupMember.Read.All usw.)
4. Erhalten Sie die Client-ID und das Geheimnis

Konfiguration auf der Fess-Seite
----------------------------------

Konfigurieren Sie die SSO-Verbindungsinformationen auf der Seite [System] > [Allgemein] in der Verwaltungsoberfläche.
Die wichtigsten Konfigurationselemente sind:

- URL des OpenID-Connect-Anbieters (Entra-ID-Endpunkt)
- Client-ID
- Client-Geheimnis
- Scopes (openid, profile, email usw.)
- Gruppenanspruchseinstellungen

Zuordnung von Gruppen zu Rollen
---------------------------------

Ordnen Sie Entra-ID-Gruppen Fess-Rollen zu.
Dadurch wird die Gruppenverwaltung in Entra ID direkt in die Steuerung der Suchergebnisse übernommen.

Beispiel: Entra-ID-Gruppe „Engineering" -> Fess-Rolle „engineering_role"

SSO-Integration über SAML
============================

SAML-Integration ist für Umgebungen geeignet, in denen ein bestehender SAML-IdP vorhanden ist.

Übersicht des Authentifizierungsablaufs
------------------------------------------

Bei SAML werden SAML Assertions zwischen dem SP (Service Provider = Fess) und dem IdP ausgetauscht.

1. Ein Benutzer greift auf Fess zu
2. Fess sendet einen SAML AuthnRequest an den IdP
3. Der IdP authentifiziert den Benutzer
4. Der IdP gibt eine SAML Response (mit Benutzerattributen) an Fess zurück
5. Fess weist Rollen basierend auf den Benutzerattributen zu

Konfiguration auf der Fess-Seite
----------------------------------

Für die SAML-Integration sind folgende Einstellungen erforderlich:

- Metadaten-URL oder XML-Datei des IdP
- Entitäts-ID des SP
- Assertion Consumer Service URL
- Attributzuordnung (Benutzername, E-Mail-Adresse, Gruppen)

SPNEGO-/Kerberos-Integration
===============================

In Windows-Active-Directory-Umgebungen kann die integrierte Windows-Authentifizierung über SPNEGO/Kerberos verwendet werden.
Wenn Sie über einen Browser von einem PC aus zugreifen, der der Domäne beigetreten ist, erfolgt die Authentifizierung automatisch ohne zusätzliche Anmeldevorgänge.

Diese Methode ist für die Benutzer am transparentesten, die Konfiguration ist jedoch am komplexesten.
Eine Active-Directory-Domänenumgebung ist Voraussetzung.

Verschlüsselung der Kommunikation
=====================================

SSL/TLS-Konfiguration
-----------------------

In Produktionsumgebungen wird empfohlen, alle Zugriffe auf Fess über HTTPS durchzuführen.

**Reverse-Proxy-Methode (empfohlen)**

Setzen Sie Nginx oder Apache HTTP Server als Reverse-Proxy ein und führen Sie die SSL-Terminierung durch.
Fess selbst arbeitet über HTTP, und der Reverse-Proxy übernimmt HTTPS.

::

    [Client] --HTTPS--> [Nginx] --HTTP--> [Fess]

Der Vorteil dieser Methode besteht darin, dass die Zertifikatsverwaltung beim Reverse-Proxy zentralisiert wird.

**Direkte Fess-Konfigurationsmethode**

Es ist auch möglich, SSL-Zertifikate direkt im Tomcat von Fess zu konfigurieren.
Dies eignet sich für kleine Umgebungen oder wenn kein Reverse-Proxy eingesetzt wird.

API-Zugriffssicherheit
========================

Im Folgenden wird die Sicherheit der in Teil 11 vorgestellten API-Integration verstärkt.

Berechtigungsdesign für Token
-------------------------------

Konfigurieren Sie geeignete Berechtigungen für Zugriffstoken.

.. list-table:: Beispiel für das Token-Design
   :header-rows: 1
   :widths: 25 25 50

   * - Verwendungszweck
     - Berechtigungen
     - Hinweise
   * - Such-Widget
     - Nur Suche (schreibgeschützt)
     - Wird im Frontend verwendet
   * - Stapelverarbeitung
     - Suche + Indizierung
     - Wird serverseitig verwendet
   * - Verwaltungsautomatisierung
     - Zugriff auf die Admin-API
     - Wird in Betriebsskripten verwendet

Token-Verwaltung
-----------------

- Regelmäßige Rotation (alle 3 bis 6 Monate)
- Sofortige Deaktivierung nicht mehr benötigter Token
- Überwachung der Token-Nutzung

Auditierung und Protokolle
============================

Audit-Protokolle in einem Suchsystem sind wichtig für die Untersuchung von Sicherheitsvorfällen und die Einhaltung von Compliance-Anforderungen.

Von Fess aufgezeichnete Protokolle
------------------------------------

- **Suchprotokolle**: Wer hat was gesucht (einsehbar unter [Systeminformationen] > [Suchprotokoll] in der Verwaltungsoberfläche)
- **Audit-Protokolle** (``audit.log``): Vorgänge wie Anmeldung, Abmeldung, Zugriff und Berechtigungsänderungen werden einheitlich aufgezeichnet

Aufbewahrung von Protokollen
------------------------------

Konfigurieren Sie die Aufbewahrungsdauer der Protokolle entsprechend den Sicherheitsanforderungen.
Wenn Compliance-Anforderungen bestehen, sollten Sie auch die Weiterleitung an ein externes Protokollverwaltungssystem (SIEM) in Betracht ziehen.

Zusammenfassung
================

In diesem Artikel haben wir eine Sicherheitsarchitektur für Fess in einer Unternehmensumgebung entworfen.

- Drei SSO-Integrationsoptionen (OIDC, SAML, SPNEGO) und deren jeweilige Einsatzszenarien
- Entwurf der Entra-ID-Integration über OpenID Connect
- Verschlüsselung der Kommunikation über SSL/TLS
- Berechtigungsdesign für API-Zugriffstoken
- Verwaltung von Audit-Protokollen

Bauen Sie eine sichere Suchinfrastruktur auf und finden Sie dabei die richtige Balance zwischen Sicherheit und Benutzerfreundlichkeit.

Im nächsten Artikel wird die Automatisierung der Suchinfrastruktur behandelt.

Referenzen
==========

- `Fess SSO-Konfiguration <https://fess.codelibs.org/ja/15.5/config/sso.html>`__

- `Fess Sicherheitskonfiguration <https://fess.codelibs.org/ja/15.5/config/security.html>`__
