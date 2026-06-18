============================
Multitenancy-Konfiguration
============================

Übersicht
=========

Die Multitenancy-Funktion von |Fess| ermöglicht es, mehrere Mandanten
(Organisationen, Abteilungen, Kunden usw.) separat innerhalb einer einzigen |Fess|-Instanz zu betreiben.

Mit der Virtueller-Host-Funktion können Sie jedem Mandanten Folgendes bereitstellen:

- Unabhängige Such-Oberfläche
- Getrennte Inhalte
- Angepasstes Design

Der aktuelle virtuelle Host wird neben der Filterung von Suchergebnissen auch in anderen |Fess|-Funktionen wie Labels, verwandten Inhalten, verwandten Abfragen und Design (Themes) berücksichtigt.

Virtueller-Host-Funktion
========================

Ein virtueller Host ist eine Funktion, die basierend auf dem Hostnamen einer HTTP-Anfrage verschiedene Suchumgebungen bereitstellt.

Funktionsweise
--------------

1. Benutzer greift auf ``tenant1.example.com`` zu
2. |Fess| identifiziert den Hostnamen
3. Wendet die entsprechende Konfiguration des virtuellen Hosts an
4. Zeigt mandantenspezifische Inhalte und Oberfläche an

Konfiguration des Virtueller-Host-Headers
==========================================

Um die Virtueller-Host-Funktion zu aktivieren, konfigurieren Sie die Zuordnung zwischen den HTTP-Anfrage-Headern und den virtuellen Host-Keys. Es gibt zwei Konfigurationsmethoden:

- **Verwaltungsoberfläche (empfohlen)**: Geben Sie den Wert im Feld „Virtueller Host" unter „System" → „Allgemein" ein.
  Dieser Wert wird als Systemeinstellung gespeichert und bleibt auch nach einem Neustart erhalten. Er hat Vorrang vor
  ``virtual.host.headers`` in ``fess_config.properties``.
- **Konfigurationsdatei**: Geben Sie den Wert in der Eigenschaft ``virtual.host.headers`` in ``fess_config.properties`` an.

Unabhängig von der gewählten Methode ist das Format der Konfigurationswerte identisch.

Konfigurationsformat
--------------------

Geben Sie jeden Eintrag im Format ``Headername:Headerwert=VirtuellerHostKey`` an, einen pro Zeile:

::

    # fess_config.properties
    virtual.host.headers=Host:tenant1.example.com=tenant1\n\
    Host:tenant2.example.com=tenant2

Für mehrere virtuelle Hosts trennen Sie die Einträge durch Zeilenumbrüche.

Matching-Verhalten
------------------

Bei jeder eingehenden Anfrage vergleicht |Fess| den Wert des in der jeweiligen Zeile angegebenen Header-Namens mit dem konfigurierten Headerwert.

- Beim Vergleich von Headerwerten wird nicht zwischen Groß- und Kleinschreibung unterschieden.
- Die konfigurierten Zeilen werden von oben nach unten ausgewertet; der virtuelle Host-Key der ersten übereinstimmenden Zeile wird angewendet.
- Wenn keine Zeile übereinstimmt, wird die Anfrage ohne virtuellen Host (gemeinsame Umgebung) behandelt.
- Das Auswertungsergebnis wird pro Anfrage zwischengespeichert.

Einschränkungen für virtuelle Host-Keys
----------------------------------------

Für virtuelle Host-Keys gelten folgende Einschränkungen:

- Nur alphanumerische Zeichen und Unterstriche (``a-zA-Z0-9_``) sind erlaubt. Andere Zeichen werden automatisch entfernt.
- Folgende Key-Namen sind reserviert und können nicht verwendet werden: ``admin``, ``common``, ``error``, ``login``, ``profile``

Konfiguration über die Verwaltungsoberfläche
=============================================

Crawl-Konfiguration
--------------------

Durch Angabe eines virtuellen Hosts in den Web-Crawl-Einstellungen können Sie Inhalte trennen:

1. Melden Sie sich in der Verwaltungsoberfläche an
2. Erstellen Sie eine Crawl-Konfiguration unter „Crawler" → „Web"
3. Wählen Sie im Feld „Virtueller Host" einen oder mehrere bereits konfigurierte virtuelle Host-Keys aus
4. Mit dieser Konfiguration gecrawlte Inhalte sind nur über den angegebenen virtuellen Host durchsuchbar

.. note::
   Das Feld „Virtueller Host" ist in den Crawl-Konfigurationen für Web, Dateisystem und Datenspeicher verfügbar. Der hier ausgewählte virtuelle Host-Key wird jedem gecrawlten Dokument zugewiesen und bei der Suche nach dem aktuellen virtuellen Host gefiltert.

Zugriffskontrolle
=================

Kombination von virtuellem Host und Rollen
------------------------------------------

Durch die Kombination von virtuellem Host mit rollenbasierter Zugriffskontrolle ist eine detailliertere Zugriffskontrolle möglich.

Konfigurieren Sie virtuellen Host und Berechtigungen gemeinsam in der Crawl-Konfiguration:

::

    # Virtueller Host in der Crawl-Konfiguration
    tenant1

    # Berechtigungen in der Crawl-Konfiguration
    {role}tenant1_user

Rollenbasierte Suche
--------------------

Details finden Sie unter :doc:`security-role`.

UI-Anpassung
============

Sie können die Oberfläche für jeden virtuellen Host anpassen.

Themes anwenden
---------------

Wenden Sie verschiedene Themes für jeden virtuellen Host an:

1. Richten Sie Themes unter „System" → „Design" ein
2. Geben Sie das Theme in der Konfiguration des virtuellen Hosts an

Benutzerdefiniertes CSS
-----------------------

Um benutzerdefiniertes CSS pro virtuellem Host anzuwenden, bearbeiten Sie CSS-Dateien in der Verwaltungsoberfläche unter „System" → „Design". Sie können auch benutzerdefinierte Templates im View-Verzeichnis des entsprechenden virtuellen Host-Keys ablegen.

Label-Einstellungen
-------------------

Schränken Sie die angezeigten Labels für jeden virtuellen Host ein:

1. Geben Sie den virtuellen Host in den Label-Typ-Einstellungen an
2. Labels werden nur für den angegebenen virtuellen Host angezeigt

API-Zugriff
===========

Auch API-Anfragen an die Such-API werden – ebenso wie bei der Oberfläche – anhand des Hostnamens der Anfrage (dem konfigurierten Header, in der Regel dem ``Host``-Header) dem virtuellen Host zugeordnet. Eine Anfrage an ``tenant1.example.com`` wird beispielsweise automatisch dem virtuellen Host ``tenant1`` zugeordnet, sodass nur Inhalte dieses virtuellen Hosts durchsucht werden.

API-Anfrage
-----------

::

    curl "https://tenant1.example.com/api/v2/search?q=keyword"

Bei der Authentifizierung mit einem Zugriffstoken wird dieses im ``Authorization``-Header im ``Bearer``-Format angegeben:

::

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "https://tenant1.example.com/api/v2/search?q=keyword"

.. note::
   Zugriffstokens sind nicht an einen bestimmten virtuellen Host gebunden. Ein Token ist für alle virtuellen Hosts gültig; der Ziel-virtuelle-Host wird durch den Hostnamen des Anfragziels bestimmt. Wird dasselbe Token an einen anderen Hostnamen gesendet, wird es einem anderen virtuellen Host zugeordnet. Wenn Sie den Zugriffsbereich unabhängig vom virtuellen Host steuern möchten, kombinieren Sie dies mit der rollenbasierten Zugriffskontrolle (:doc:`security-role`).

DNS-Konfiguration
=================

Beispiel-DNS-Konfiguration zur Umsetzung von Multitenancy:

Subdomains zum selben Server
-----------------------------

::

    # DNS-Konfiguration
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # Oder Wildcard
    *.example.com          A    192.168.1.100

Reverse-Proxy-Konfiguration
----------------------------

Beispiel für eine Reverse-Proxy-Konfiguration mit Nginx:

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

Wenn eine vollständige Datentrennung erforderlich ist, erwägen Sie folgende Ansätze:

Trennung auf Index-Ebene
------------------------

Verwenden Sie für jeden Mandanten separate |Fess|-Instanzen und Indizes:

::

    # Fess-Instanz für Mandant 1 (fess_config.properties)
    index.document.search.index=fess_tenant1.search

    # Fess-Instanz für Mandant 2 (fess_config.properties)
    index.document.search.index=fess_tenant2.search

.. note::
   ``index.document.search.index`` kann pro Instanz nur auf einen Wert gesetzt werden.
   Für eine vollständige Trennung auf Index-Ebene müssen Sie für jeden Mandanten eine separate |Fess|-Instanz betreiben oder eine benutzerdefinierte Implementierung vornehmen. Für typisches Multitenancy ist die logische Trennung über die Virtueller-Host-Funktion ausreichend.

Best Practices
==============

1. **Klare Namenskonventionen**: Verwenden Sie konsistente Namenskonventionen für virtuelle Hosts und Rollen
2. **Tests**: Testen Sie das Verhalten für jeden Mandanten gründlich
3. **Überwachung**: Überwachen Sie die Ressourcennutzung pro Mandant
4. **Dokumentation**: Dokumentieren Sie die Mandantenkonfigurationen

Einschränkungen
===============

- Die Verwaltungsoberfläche wird von allen Mandanten gemeinsam genutzt
- Systemeinstellungen betreffen alle Mandanten
- Einige Funktionen unterstützen möglicherweise keine virtuellen Hosts

Referenzinformationen
=====================

- :doc:`security-role` - Rollenbasierte Zugriffskontrolle
- :doc:`security-virtual-host` - Details zur Konfiguration virtueller Hosts
- :doc:`../admin/design-guide` - Design-Anpassung
