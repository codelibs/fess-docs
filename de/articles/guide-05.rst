===========================================================================
Teil 5: Informationen personenbezogen bereitstellen -- Abteilungs- und berechtigungsbasierte Steuerung der Suchergebnisse
===========================================================================

Einleitung
==========

Im vorherigen Teil haben wir gezeigt, wie mehrere Datenquellen integriert und eine übergreifende Suche ermöglicht werden kann.
Sobald eine solche übergreifende Suche verfügbar ist, ergibt sich jedoch eine neue Herausforderung:
die Steuerung, welche Informationen angezeigt werden dürfen und welche nicht.

Es wäre problematisch, wenn vertrauliche Unterlagen der Personalabteilung in den Suchergebnissen aller Mitarbeiter erscheinen würden.
In diesem Artikel erläutern wir, wie Sie mithilfe der rollenbasierten Suche von Fess die Suchergebnisse entsprechend der Zugehörigkeit und den Berechtigungen der Benutzer steuern können.

Zielgruppe
==========

- Personen, die eine Zugriffskontrolle für Suchergebnisse benötigen
- Personen, die eine Suchinfrastruktur unter Berücksichtigung der Informationssicherheit im Unternehmen aufbauen möchten
- Personen mit grundlegenden Kenntnissen in Active Directory oder LDAP

Szenario
========

Ein Unternehmen verfügt über drei Abteilungen:

- **Vertrieb**: Verwaltung von Kundeninformationen, Angeboten und Präsentationen
- **Entwicklung**: Verwaltung von Entwurfsdokumenten, Quellcode-Spezifikationen und Besprechungsprotokollen
- **Personalabteilung**: Verwaltung von Leistungsbeurteilungen, Gehaltsinformationen und Betriebsordnungen

Darüber hinaus gibt es Dokumente, die allen Abteilungen gemeinsam zur Verfügung stehen (z. B. interne Richtlinien, Informationen zu Sozialleistungen).

Folgendes Sucherlebnis soll realisiert werden:

- Mitarbeiter des Vertriebs können nur Dokumente des Vertriebs und gemeinsame Dokumente durchsuchen
- Mitarbeiter der Entwicklung können nur Dokumente der Entwicklung und gemeinsame Dokumente durchsuchen
- Mitarbeiter der Personalabteilung können nur Dokumente der Personalabteilung und gemeinsame Dokumente durchsuchen
- Die Geschäftsleitung kann alle Dokumente durchsuchen

Funktionsweise der rollenbasierten Suche
==========================================

Die rollenbasierte Suche von Fess funktioniert nach folgendem Prinzip:

1. **Beim Crawling**: Dokumente werden mit Rolleninformationen versehen (welche Rollen Zugriff haben)
2. **Beim Login**: Die Rolleninformationen des Benutzers werden abgerufen (interne Fess-Authentifizierung oder externe Authentifizierungsanbindung)
3. **Bei der Suche**: Nur Dokumente, die mit den Rollen des Benutzers übereinstimmen, werden in den Suchergebnissen angezeigt

Durch dieses Verfahren wird die Zugriffskontrolle auf der Ebene der Suchmaschine durchgesetzt.

Rollendesign
=============

Benutzer- und Gruppendesign
----------------------------

Zunächst werden die Zusammenhänge zwischen Benutzern, Gruppen und Rollen in Fess erläutert.

.. list-table:: Rollendesign
   :header-rows: 1
   :widths: 20 30 50

   * - Gruppe
     - Rolle
     - Zugängliche Dokumente
   * - sales (Vertrieb)
     - sales_role
     - Dokumente des Vertriebs + gemeinsame Dokumente
   * - engineering (Entwicklung)
     - engineering_role
     - Dokumente der Entwicklung + gemeinsame Dokumente
   * - hr (Personalabteilung)
     - hr_role
     - Dokumente der Personalabteilung + gemeinsame Dokumente
   * - management (Geschäftsleitung)
     - management_role
     - Alle Dokumente

Gruppen- und Rollenkonfiguration in Fess
------------------------------------------

**Rollen erstellen**

1. Wählen Sie in der Verwaltungsoberfläche [Benutzer] > [Rollen]
2. Erstellen Sie die folgenden Rollen:

   - ``sales_role``
   - ``engineering_role``
   - ``hr_role``
   - ``management_role``

**Gruppen erstellen**

1. Wählen Sie [Benutzer] > [Gruppen]
2. Erstellen Sie die folgenden Gruppen:

   - ``sales``
   - ``engineering``
   - ``hr``
   - ``management``

**Benutzer erstellen und Rollen zuweisen**

1. Wählen Sie [Benutzer] > [Benutzer]
2. Weisen Sie jedem Benutzer Gruppen und Rollen zu

Berechtigungen in der Crawling-Konfiguration zuweisen
======================================================

Um Dokumenten Zugriffskontrollinformationen zuzuweisen, geben Sie Berechtigungen in der Crawling-Konfiguration an.
Berechtigungen werden im Format ``{role}Rollenname``, ``{group}Gruppenname``, ``{user}Benutzername`` eingegeben, jeweils durch einen Zeilenumbruch getrennt.

Crawling-Konfiguration pro Abteilung
--------------------------------------

**Dateiserver des Vertriebs**

1. [Crawler] > [Dateisystem] > [Neu erstellen]
2. Konfigurieren Sie Folgendes:

   - Pfad: ``smb://fileserver/sales/``
   - Berechtigungen: ``{role}sales_role`` und ``{role}management_role``, jeweils in einer separaten Zeile eingeben

Durch diese Konfiguration können nur Benutzer mit ``sales_role`` und ``management_role`` die vom Dateiserver des Vertriebs gecrawlten Dokumente in den Suchergebnissen sehen.

**Dateiserver der Entwicklung**

1. [Crawler] > [Dateisystem] > [Neu erstellen]
2. Konfigurieren Sie Folgendes:

   - Pfad: ``smb://fileserver/engineering/``
   - Berechtigungen: ``{role}engineering_role`` und ``{role}management_role``, jeweils in einer separaten Zeile eingeben

**Dateiserver der Personalabteilung**

1. [Crawler] > [Dateisystem] > [Neu erstellen]
2. Konfigurieren Sie Folgendes:

   - Pfad: ``smb://fileserver/hr/``
   - Berechtigungen: ``{role}hr_role`` und ``{role}management_role``, jeweils in einer separaten Zeile eingeben

**Gemeinsame Dokumente**

1. [Crawler] > [Web] oder [Dateisystem] > [Neu erstellen]
2. Berechtigungen: Belassen Sie den Standardwert ``{role}guest``

Standardmäßig wird ``{role}guest`` automatisch eingetragen. Da alle Benutzer, einschließlich Gastbenutzer, die Rolle ``guest`` besitzen, können alle Benutzer die Suchergebnisse einsehen.

Anbindung an externe Authentifizierung
========================================

In realen Unternehmensumgebungen ist es üblich, nicht die interne Benutzerverwaltung von Fess zu verwenden, sondern eine Anbindung an bestehende Verzeichnisdienste herzustellen.

Active Directory / LDAP-Anbindung
-----------------------------------

Fess unterstützt die LDAP-Anbindung und kann die Benutzerinformationen von Active Directory für Authentifizierung und Rollenzuweisung verwenden.

Um die LDAP-Anbindung zu aktivieren, konfigurieren Sie die LDAP-Verbindungsinformationen in der Konfigurationsdatei von Fess.

Die wichtigsten Konfigurationsparameter sind:

- URL des LDAP-Servers
- Bind-DN (Konto für die Verbindung)
- Suchbasis-DN für Benutzer
- Suchbasis-DN für Gruppen
- Zuordnung der Benutzerattribute

Wenn die LDAP-Anbindung aktiviert ist, können sich Benutzer mit ihrem Active Directory-Konto bei Fess anmelden.
Da die Informationen zur Gruppenzugehörigkeit automatisch als Rollen übernommen werden, ist eine manuelle Rollenzuweisung pro Benutzer in Fess nicht erforderlich.

SSO-Anbindung
--------------

Als weitergehende Konfiguration ist auch eine Anbindung an Single Sign-On (SSO) möglich.
Fess unterstützt die folgenden SSO-Protokolle:

- **OpenID Connect (OIDC)**: Entra ID (Azure AD), Keycloak und weitere
- **SAML**: Anbindung an verschiedene Identity Provider
- **SPNEGO/Kerberos**: Integrierte Windows-Authentifizierung

Durch die SSO-Anbindung können Benutzer mit ihren gewohnten Anmeldedaten automatisch auf Fess zugreifen, wobei die Rolleninformationen ebenfalls automatisch übernommen werden.
Details zur SSO-Anbindung werden in Teil 15 „Sichere Suchinfrastruktur" ausführlich behandelt.

Funktionsprüfung
==================

Nachdem die Konfiguration der rollenbasierten Suche abgeschlossen ist, sollten Sie die Funktionsweise überprüfen.

Prüfungsschritte
------------------

1. Melden Sie sich als Benutzer des Vertriebs an und suchen Sie nach „Angebot"
   → Überprüfen Sie, dass nur Dokumente des Vertriebs und gemeinsame Dokumente angezeigt werden

2. Melden Sie sich als Benutzer der Entwicklung an und suchen Sie mit demselben Suchbegriff
   → Überprüfen Sie, dass keine Dokumente des Vertriebs angezeigt werden

3. Melden Sie sich als Benutzer der Geschäftsleitung an und suchen Sie mit demselben Suchbegriff
   → Überprüfen Sie, dass Dokumente aller Abteilungen angezeigt werden

Prüfungskriterien
-------------------

- Dokumente, für die keine Berechtigung vorliegt, dürfen in den Suchergebnissen überhaupt nicht erscheinen
- Gemeinsame Dokumente werden für alle Benutzer angezeigt
- Suchverhalten im nicht angemeldeten Zustand (Umfang der Gastanzeige)

Designüberlegungen
====================

Granularität der Rollen
------------------------

Die Granularität der Rollen wird entsprechend der Organisationsstruktur und den Sicherheitsanforderungen festgelegt.

**Grobe Granularität**: Rollen auf Abteilungsebene (Szenario dieses Artikels)

- Vorteil: Einfache Konfiguration, leichte Verwaltung
- Nachteil: Keine feingranulare Zugriffskontrolle innerhalb einer Abteilung möglich

**Feine Granularität**: Rollen auf Projekt- oder Teamebene

- Vorteil: Feingranulare Zugriffskontrolle möglich
- Nachteil: Die Anzahl der Rollen steigt und die Verwaltung wird komplexer

Es wird empfohlen, zunächst mit grober Granularität zu beginnen und bei Bedarf feiner zu untergliedern.

Anbindung an die ACL des Dateiservers
---------------------------------------

Beim Crawlen eines Dateiservers ist es auch möglich, die ACL-Informationen (Access Control List) der Dateien für die Berechtigungssteuerung zu nutzen.
In diesem Fall werden die Berechtigungseinstellungen des Dateisystems direkt in der Anzeigekontrolle der Suchergebnisse widergespiegelt.

Wenn Sie die ACL des Dateiservers nutzen möchten, überprüfen Sie die berechtigungsrelevanten Konfigurationsoptionen in der Crawling-Konfiguration.

Zusammenfassung
================

In diesem Artikel haben wir die abteilungsbezogene Steuerung der Suchergebnisse mithilfe der rollenbasierten Suche von Fess konzipiert und aufgebaut.

- Design und Registrierung von Rollen, Gruppen und Benutzern
- Rollenzuweisung in der Crawling-Konfiguration
- Automatische Rollenübernahme durch Active Directory / LDAP-Anbindung
- SSO-Anbindungsoptionen (OIDC, SAML, SPNEGO)

Durch die rollenbasierte Suche können Sie die Informationssicherheit gewährleisten und gleichzeitig den Komfort einer übergreifenden Suche bieten.
Damit endet der Grundlagenteil. Ab dem nächsten Teil behandeln wir im Praxislösungsteil den Aufbau eines Wissens-Hubs für Entwicklungsteams.

Referenzen
==========

- `Fess Rollenkonfiguration <https://fess.codelibs.org/ja/15.5/admin/role.html>`__

- `Fess LDAP-Anbindung <https://fess.codelibs.org/ja/15.5/config/ldap.html>`__
