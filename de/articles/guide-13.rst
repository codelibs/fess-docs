============================================================
Teil 13: Multi-Tenant-Suchplattform -- Eine einzelne Fess-Instanz fuer mehrere Organisationen
============================================================

Einfuehrung
============

Wenn Sie Fess mehreren internen Abteilungen oder als MSP (Managed Service Provider) mehreren Kunden bereitstellen moechten, ist es ineffizient, fuer jeden Mandanten eine eigene Fess-Instanz aufzubauen.

In diesem Artikel wird ein Multi-Tenant-Design erlaeutert, das mit einer einzigen Fess-Instanz mehrere Mandanten (Organisationen, Abteilungen oder Kunden) bedient.

Zielgruppe
==========

- Personen, die Suchdienste fuer mehrere Organisationen oder Abteilungen bereitstellen moechten
- Personen, die sich fuer Multi-Tenant-Design mit Fess interessieren
- Personen, die erfahren moechten, wie die Virtual-Host-Funktion genutzt wird

Szenario
========

Wir gehen von einem Szenario aus, in dem die IT-Abteilung eines Konzerns Suchdienste fuer drei Tochtergesellschaften bereitstellt.

.. list-table:: Mandantenkonfiguration
   :header-rows: 1
   :widths: 25 35 40

   * - Mandant
     - Domain
     - Suchziel
   * - Unternehmen A (Fertigung)
     - search-a.example.com
     - Produktspezifikationen, Qualitaetsmanagement-Dokumente
   * - Unternehmen B (Einzelhandel)
     - search-b.example.com
     - Filialhandbuecher, Produktinformationen
   * - Unternehmen C (Dienstleistung)
     - search-c.example.com
     - Kundenservice-Handbuecher, FAQ

Jeder Mandant hat die folgenden Anforderungen:

- Daten duerfen zwischen Mandanten nicht sichtbar sein (Datenisolation)
- Jeder Mandant benoetigt ein eigenes Design (Branding)
- Jeder Mandant benoetigt unabhaengige Crawl-Einstellungen

Virtual-Host-Funktion
======================

Mit der Virtual-Host-Funktion von Fess koennen Sie je nach Hostname, ueber den zugegriffen wird, unterschiedliche Sucherlebnisse bereitstellen.

Virtual-Host-Konfiguration
----------------------------

Legen Sie den Virtual-Host-Wert in der Administrationsoberflaeche fest.
Indem Sie diesen Wert mit Crawl-Einstellungen und Labels verknuepfen, koennen Sie die Datenisolation fuer jeden Mandanten realisieren.

Designueberlegungen
---------------------

**DNS- / Load-Balancer-Konfiguration**

Konfigurieren Sie DNS so, dass die Domain jedes Mandanten auf denselben Fess-Server verweist.

::

    search-a.example.com → Fess-Server (192.168.1.100)
    search-b.example.com → Fess-Server (192.168.1.100)
    search-c.example.com → Fess-Server (192.168.1.100)

Fess untersucht die HTTP-Header der Anfrage, um festzustellen, auf welchen Virtual Host zugegriffen wird.
Standardmaessig wird der Host-Header verwendet. Sie koennen jedoch mit der Einstellung ``virtual.host.headers`` einen beliebigen Header angeben.
Das Konfigurationsformat ist ``Headername:Wert=VirtualHostKey`` (z. B. ``Host:search-a.example.com=tenant-a``).

Mandantenisolation
===================

Datenisolation
--------------

Die Datenisolation zwischen Mandanten wird ueber das Feld ``virtual_host`` der Dokumente realisiert, das durch die Virtual-Host-Funktion bereitgestellt wird.

**Isolation ueber Virtual Host**

Wenn Sie den Virtual-Host-Schluessel im Feld "Virtual Host" der Crawl-Einstellungen festlegen, erhalten gecrawlte Dokumente ein ``virtual_host``-Feld.
Bei der Suche wird dieses Feld automatisch zum Filtern verwendet, sodass Benutzer, die ueber die Domain eines Mandanten zugreifen, nur die Dokumente dieses Mandanten in den Suchergebnissen sehen.

- ``tenant-a``: Dokumente von Unternehmen A
- ``tenant-b``: Dokumente von Unternehmen B
- ``tenant-c``: Dokumente von Unternehmen C

Darueber hinaus koennen Sie durch Festlegen des Feldes "Virtual Host" bei Labels auch die fuer jeden Mandanten angezeigten Labels trennen.

**Isolation ueber Rollen**

Wenn eine strengere Isolation erforderlich ist, kombinieren Sie die rollenbasierte Suche (siehe Teil 5).
Erstellen Sie Rollen fuer jeden Mandanten und weisen Sie diese den Crawl-Einstellungen und Benutzern zu.

Crawl-Konfiguration
---------------------

Die Crawl-Konfiguration jedes Mandanten wird unabhaengig verwaltet.

.. list-table:: Crawl-Einstellungen nach Mandant
   :header-rows: 1
   :widths: 15 30 25 30

   * - Mandant
     - Crawl-Ziel
     - Zeitplan
     - Label
   * - Unternehmen A
     - smb://fs-a/docs/
     - Taeglich um 1:00
     - tenant-a
   * - Unternehmen B
     - https://portal-b.example.com/
     - Taeglich um 2:00
     - tenant-b
   * - Unternehmen C
     - smb://fs-c/manuals/
     - Taeglich um 3:00
     - tenant-c

Mandantenspezifische Themes
=============================

Mit der Theme-Funktion von Fess koennen Sie fuer jeden Mandanten ein unterschiedliches Design bereitstellen.

Theme-Design
-------------

Bereiten Sie Themes vor, die zu den Markenfarben und dem Logo jedes Mandanten passen.

- Unternehmen A: Ein solides Design fuer ein Fertigungsunternehmen (Blautoene)
- Unternehmen B: Ein helles Design fuer den Einzelhandel (Gruentoene)
- Unternehmen C: Ein freundliches Design fuer ein Dienstleistungsunternehmen (Orangetoene)

Verknuepfung von Virtual Hosts und Themes
-------------------------------------------

Durch den Wechsel der Themes fuer jeden Virtual Host wird den Benutzern jedes Mandanten eine Suchoberflaeche mit dem eigenen Unternehmensbranding angezeigt.

Fess bietet integrierte Themes wie ``simple``, ``docsearch`` und ``codesearch`` sowie die Moeglichkeit, benutzerdefinierte Themes zu verwenden.

API-Zugriffsisolation
======================

API-Zugriffstoken pro Mandant
-------------------------------

Stellen Sie fuer jeden Mandanten individuelle Zugriffstoken aus.
Durch die Zuordnung von Rollen zu den Token wird die Mandantenisolation auch auf den API-Zugriff angewendet.

.. list-table:: Zugriffstoken-Konfiguration
   :header-rows: 1
   :widths: 20 30 50

   * - Mandant
     - Tokenname
     - Zugewiesene Rolle
   * - Unternehmen A
     - tenant-a-api-token
     - tenant-a-role
   * - Unternehmen B
     - tenant-b-api-token
     - tenant-b-role
   * - Unternehmen C
     - tenant-c-api-token
     - tenant-c-role

Wenn das System eines Mandanten eine API-Integration nutzt (siehe Teil 11), stellt die Verwendung mandantenspezifischer Token sicher, dass kein Zugriff auf Daten anderer Mandanten moeglich ist.

Betriebliche Hinweise
======================

Ressourcenmanagement
--------------------

Da eine einzelne Fess-Instanz mehrere Mandanten bedient, ist eine sorgfaeltige Ressourcenzuweisung erforderlich.

- **Crawl-Lastverteilung**: Staffeln Sie die Crawl-Zeitplaene der Mandanten, um gleichzeitige Ausfuehrung zu vermeiden
- **Indexgroesse**: Ueberwachen Sie die gesamte Indexgroesse aller Mandanten
- **Arbeitsspeicher**: Passen Sie den JVM-Heap entsprechend der Anzahl der Mandanten und Dokumente an

Hinzufuegen und Entfernen von Mandanten
-----------------------------------------

Standardisieren Sie das Verfahren zum Hinzufuegen neuer Mandanten.

1. Label erstellen
2. Rolle erstellen
3. Crawl-Einstellungen registrieren
4. Virtual Host konfigurieren
5. Zugriffstoken ausstellen
6. DNS-Einstellungen hinzufuegen

Beim Entfernen eines Mandanten vergessen Sie nicht, die zugehoerigen Indexdaten zu loeschen.

Skalierungskriterien
---------------------

Wenn Sie die folgenden Symptome beobachten, sollten Sie eine Aufteilung oder Skalierung der Fess-Instanzen in Betracht ziehen (siehe Teil 14).

- Verschlechterung der Suchantwortzeiten
- Crawls werden nicht innerhalb des geplanten Zeitfensters abgeschlossen
- Haeufige Speichermangel-Fehler
- Die Anzahl der Mandanten uebersteigt 10

Zusammenfassung
================

In diesem Artikel wurde das Multi-Tenant-Design unter Verwendung der Virtual-Host-Funktion von Fess erlaeutert.

- Mandantenspezifischer Zugriff ueber Virtual Hosts
- Datenisolation durch Labels und Rollen
- Mandantenspezifisches Branding durch Themes
- Mandantenisolation ueber API-Zugriffstoken
- Ressourcenmanagement und Skalierungskriterien

Mit einer einzigen Fess-Instanz koennen Sie effizient mehrere Mandanten bedienen, die Verwaltungskosten niedrig halten und gleichzeitig die Anforderungen jedes Mandanten erfuellen.

Im naechsten Artikel werden Skalierungsstrategien fuer Suchsysteme behandelt.

Referenzen
==========

- `Fess Virtual Host <https://fess.codelibs.org/ja/15.5/config/virtual-host.html>`__

- `Fess Label-Einstellungen <https://fess.codelibs.org/ja/15.5/admin/labeltype.html>`__
