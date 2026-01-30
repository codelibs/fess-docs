==================================
Multitenancy-Konfiguration
==================================

Uebersicht
==========

Die Multitenancy-Funktion von |Fess| ermoeglicht es Ihnen, mehrere Mandanten
(Organisationen, Abteilungen, Kunden usw.) separat innerhalb einer einzigen |Fess|-Instanz zu betreiben.

Mit der Virtual-Host-Funktion koennen Sie jedem Mandanten Folgendes bereitstellen:

- Unabhaengige Such-UI
- Getrennte Inhalte
- Angepasstes Design

Virtual-Host-Funktion
=====================

Virtual Host ist eine Funktion, die basierend auf dem HTTP-Anfrage-Hostnamen verschiedene Suchumgebungen bereitstellt.

Funktionsweise
--------------

1. Benutzer greift auf ``tenant1.example.com`` zu
2. |Fess| identifiziert den Hostnamen
3. Wendet die entsprechende Virtual-Host-Konfiguration an
4. Zeigt mandantenspezifische Inhalte und UI an

Virtual-Host-Konfiguration
==========================

Konfiguration ueber das Admin-Panel
-----------------------------------

1. Melden Sie sich im Admin-Panel an
2. Navigieren Sie zu "Crawler" -> "Virtual Host"
3. Klicken Sie auf "Neu erstellen"
4. Konfigurieren Sie Folgendes:

   - **Hostname**: ``tenant1.example.com``
   - **Pfad**: ``/tenant1`` (optional)

Integration mit Crawl-Konfiguration
-----------------------------------

Durch Angabe eines Virtual Hosts in den Web-Crawl-Einstellungen koennen Sie Inhalte trennen:

1. Erstellen Sie eine Crawl-Konfiguration unter "Crawler" -> "Web"
2. Waehlen Sie den Ziel-Virtual-Host im Feld "Virtual Host"
3. Mit dieser Konfiguration gecrawlte Inhalte sind nur vom angegebenen Virtual Host durchsuchbar

Zugriffskontrolle
=================

Kombination von Virtual Hosts und Rollen
----------------------------------------

Durch die Kombination von Virtual Hosts mit rollenbasierter Zugriffskontrolle
ist eine feinere Zugriffskontrolle moeglich:

::

    # Konfigurationsbeispiel
    virtual.host=tenant1.example.com
    permissions=role_tenant1_user

Rollenbasierte Suche
--------------------

Details finden Sie unter :doc:`security-role`.

UI-Anpassung
============

Sie koennen die UI fuer jeden Virtual Host anpassen.

Themes anwenden
---------------

Wenden Sie verschiedene Themes fuer jeden Virtual Host an:

1. Richten Sie Themes unter "System" -> "Design" ein
2. Geben Sie das Theme in der Virtual-Host-Konfiguration an

Benutzerdefiniertes CSS
-----------------------

Wenden Sie benutzerdefiniertes CSS fuer jeden Virtual Host an:

::

    # Virtual-Host-spezifische CSS-Datei
    /webapp/WEB-INF/view/tenant1/css/custom.css

Label-Einstellungen
-------------------

Beschraenken Sie angezeigte Labels fuer jeden Virtual Host:

1. Geben Sie den Virtual Host in den Label-Typ-Einstellungen an
2. Labels werden nur auf dem angegebenen Virtual Host angezeigt

API-Authentifizierung
=====================

Steuern Sie den API-Zugriff fuer jeden Virtual Host:

Zugriffstokens
--------------

Stellen Sie Zugriffstokens aus, die mit Virtual Hosts verknuepft sind:

1. Erstellen Sie ein Token unter "System" -> "Zugriffstoken"
2. Verknuepfen Sie das Token mit einem Virtual Host

API-Anfrage
-----------

::

    curl -H "Authorization: Bearer TENANT_TOKEN" \
         "https://tenant1.example.com/api/v1/search?q=keyword"

DNS-Konfiguration
=================

Beispiel-DNS-Konfiguration zur Umsetzung von Multitenancy:

Subdomains zum selben Server
----------------------------

::

    # DNS-Konfiguration
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # Oder Wildcard
    *.example.com          A    192.168.1.100

Reverse-Proxy-Konfiguration
---------------------------

Beispiel fuer Reverse-Proxy-Konfiguration mit Nginx:

::

    server {
        server_name tenant1.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        server_name tenant2.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

Datentrennung
=============

Wenn vollstaendige Datentrennung erforderlich ist, erwaegen Sie folgende Ansaetze:

Index-Level-Trennung
--------------------

Verwenden Sie separate Indizes fuer jeden Mandanten:

::

    # Index fuer Mandant 1
    index.document.search.index=fess_tenant1.search

    # Index fuer Mandant 2
    index.document.search.index=fess_tenant2.search

.. note::
   Die Trennung auf Index-Ebene erfordert moeglicherweise eine benutzerdefinierte Implementierung.

Best Practices
==============

1. **Klare Namenskonventionen**: Verwenden Sie konsistente Namenskonventionen fuer Virtual Hosts und Rollen
2. **Testen**: Testen Sie die Operationen auf jedem Mandanten gruendlich
3. **Ueberwachung**: Ueberwachen Sie die Ressourcennutzung fuer jeden Mandanten
4. **Dokumentation**: Dokumentieren Sie Mandantenkonfigurationen

Einschraenkungen
================

- Das Admin-Panel wird von allen Mandanten gemeinsam genutzt
- Systemeinstellungen betreffen alle Mandanten
- Einige Funktionen unterstuetzen moeglicherweise keine Virtual Hosts

Referenzinformationen
=====================

- :doc:`security-role` - Rollenbasierte Zugriffskontrolle
- :doc:`security-virtual-host` - Virtual-Host-Konfigurationsdetails
- :doc:`../admin/design-guide` - Design-Anpassung
