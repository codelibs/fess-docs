========
Virtueller Host
========

Über virtuelle Hosts
==============

|Fess| kann Suchergebnisse basierend auf dem Hostnamen (Hostteil der URL) differenzieren, mit dem auf |Fess| zugegriffen wird.
Da Suchergebnisse in jeweiligen JSPs angezeigt werden, kann auch das Design geändert werden.

Systemkonfiguration
----------

Konfigurieren Sie "Virtueller Host" unter :doc:`Administratorhandbuch > Allgemeine Einstellungen <../admin/general-guide>`. Geben Sie den hier konfigurierten virtuellen Hostnamen in der Crawl-Konfiguration an.

**Format**

::

   Host:Hostname[:Portnummer]=Virtueller Hostname

.. list-table::

   * - *Hostname*
     - Hostname oder IP-Adresse, die im System aufgelöst werden kann (DNS)
   * - *Portnummer*
     - Optional. Standard ist 80.
   * - *Virtueller Hostname*
     - Virtueller Hostname, der in Crawl-Konfiguration angegeben wird

**Beispiel**

::

   Host:abc.example.com:8080=host1
   Host:192.168.1.123:8080=host2

Nach Konfiguration werden JSPs der Suchseite unter ``WEB-INF/view/Virtueller Hostname`` generiert.
Durch Bearbeitung dieser können Sie Seitendesign für jeden virtuellen Host ändern.


Crawl-Konfiguration
---------

Geben Sie "Virtueller Host" in Web-Crawl-Konfiguration, Datei-Crawl-Konfiguration oder Datenspeicher-Crawl-Konfiguration an.
"Virtueller Host" gibt einen der in Systemkonfiguration konfigurierten virtuellen Hostnamen an.

**Beispiel**

.. list-table::

   * - *Virtueller Host*
     - ``host1``
