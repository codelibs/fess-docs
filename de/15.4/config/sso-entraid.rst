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
6. |Fess| verwendet die Microsoft Graph API, um die Gruppen- und Rolleninformationen des Benutzers abzurufen
7. Benutzer wird angemeldet und Gruppeninformationen werden auf die rollenbasierte Suche angewendet

Informationen zur Integration mit der rollenbasierten Suche finden Sie unter :doc:`security-role`.

Voraussetzungen
===============

Bevor Sie die Entra ID-Authentifizierung konfigurieren, überprüfen Sie die folgenden Voraussetzungen:

- |Fess| 15.4 oder höher ist installiert
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
   * - ``entraid.default.groups``
     - Standardgruppen (kommagetrennt)
     - (Keine)
   * - ``entraid.default.roles``
     - Standardrollen (kommagetrennt)
     - (Keine)

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

   - ``Group.Read.All`` - Erforderlich zum Abrufen von Benutzergruppeninformationen

6. Klicken Sie auf **Berechtigungen hinzufügen**

7. Klicken Sie auf **Administratorzustimmung für <Mandantenname> erteilen**

.. note::
   Die Administratorzustimmung erfordert Mandantenadministratorrechte.

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

|Fess| ruft nicht nur Gruppen ab, zu denen Benutzer direkt gehören, sondern auch übergeordnete Gruppen (verschachtelte Gruppen) rekursiv.
Diese Verarbeitung wird nach der Anmeldung asynchron ausgeführt, um die Auswirkungen auf die Anmeldezeit zu minimieren.

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

::

    # SSO aktivieren
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

Authentifizierungsfehler treten auf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob Mandanten-ID, Client-ID und Clientgeheimnis korrekt konfiguriert sind
- Überprüfen Sie, ob das Clientgeheimnis nicht abgelaufen ist
- Überprüfen Sie, ob die Administratorzustimmung für API-Berechtigungen erteilt wurde

Gruppeninformationen können nicht abgerufen werden
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Überprüfen Sie, ob die Berechtigung ``Group.Read.All`` erteilt wurde
- Überprüfen Sie, ob die Administratorzustimmung erteilt wurde
- Überprüfen Sie, ob der Benutzer in Entra ID zu Gruppen gehört

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
