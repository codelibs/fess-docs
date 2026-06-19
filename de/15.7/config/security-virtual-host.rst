================
Virtueller Host
================

Über virtuelle Hosts
====================

|Fess| kann Suchergebnisse basierend auf dem Hostnamen (dem Wert des HTTP-``Host``-Headers) differenzieren, mit dem auf |Fess| zugegriffen wird.
Ein einzelner |Fess|-Server kann unter mehreren Hostnamen veröffentlicht werden, wobei je nach Hostname unterschiedliche Suchziele (Crawl-Konfigurationen) und Seitendesigns bereitgestellt werden können.
Da Suchergebnisse in den jeweiligen JSPs des virtuellen Hosts angezeigt werden, kann auch das Design geändert werden.

Die Funktion für virtuelle Hosts ist standardmäßig deaktiviert (nicht konfiguriert). Die Einrichtung erfolgt mit den folgenden Schritten.

Systemkonfiguration
-------------------

Konfigurieren Sie unter :doc:`Administratorhandbuch > Allgemeine Einstellungen <../admin/general-guide>` im Abschnitt „Virtueller Host" die Zuordnung zwischen dem Hostnamen der Anfrage und dem virtuellen Hostnamen. Geben Sie den hier konfigurierten virtuellen Hostnamen in der Crawl-Konfiguration an.

**Format**

Tragen Sie einen virtuellen Host pro Zeile im folgenden Format ein:

::

   Headername:Headerwert=VirtuellerHostname

.. list-table::

   * - *Headername*
     - Name des HTTP-Request-Headers, der für die Auswertung verwendet wird. Normalerweise wird ``Host`` angegeben. Bei Zugriffen über einen Reverse-Proxy kann auch ``X-Forwarded-Host`` angegeben werden.
   * - *Headerwert*
     - Der im obigen Header enthaltene Hostname (bei Bedarf im Format ``Hostname:Portnummer``). Wenn der vom Client beim Zugriff gesendete Headerwert vollständig übereinstimmt (Groß-/Kleinschreibung wird nicht berücksichtigt), wird dieser virtuelle Host angewendet.
   * - *VirtuellerHostname*
     - Virtueller Hostname, der in der Crawl-Konfiguration angegeben wird

**Beispiel**

::

   Host:abc.example.com=host1
   Host:192.168.1.123:8080=host2

.. note::

   Die Auswertung erfolgt nicht durch Namensauflösung (DNS), sondern durch Zeichenkettenvergleich mit dem Wert des Request-Headers.
   Der vom Browser gesendete ``Host``-Header enthält bei Standardports (HTTP: 80, HTTPS: 443) keine Portnummer; bei anderen Ports wird die Portnummer im Format ``Hostname:Portnummer`` mitgesendet.
   Wenn der Dienst daher über einen Nicht-Standardport erreichbar ist, muss die Portnummer explizit angegeben werden, z. B. ``Host:abc.example.com:8080=host1``.

.. note::

   Für virtuelle Hostnamen können nur alphanumerische Zeichen und Unterstriche ( ``a-z`` , ``A-Z`` , ``0-9`` , ``_`` ) verwendet werden.
   Andere Zeichen werden automatisch entfernt.

   Die folgenden Namen sind reserviert und können nicht als virtuelle Hostnamen verwendet werden:
   ``admin`` , ``common`` , ``error`` , ``login`` , ``profile``

Nach dem Speichern der Konfiguration werden JSPs der Suchseite unter ``WEB-INF/view/VirtuellerHostname`` generiert.
Durch das Bearbeiten dieser Dateien können Sie das Seitendesign für jeden virtuellen Host anpassen. Die JSPs können auch über den Bildschirm :doc:`Administratorhandbuch > Design <../admin/design-guide>` bearbeitet werden.


Crawl-Konfiguration
-------------------

Geben Sie „Virtueller Host" in der Web-Crawl-Konfiguration, der Datei-Crawl-Konfiguration oder der Datenspeicher-Crawl-Konfiguration an.
Unter „Virtueller Host" wird einer der in der Systemkonfiguration definierten virtuellen Hostnamen angegeben. Einer Crawl-Konfiguration können auch mehrere virtuelle Hosts zugewiesen werden (ein Eintrag pro Zeile).

Suchanfragen, die über einen virtuellen Host eingehen, zeigen ausschließlich Dokumente aus den Crawl-Konfigurationen an, denen dieser virtuelle Host zugewiesen ist.
Bei Zugriffen, die keinem virtuellen Host entsprechen (normaler Zugriff ohne konfigurierte virtuelle Hosts), wird diese Einschränkung nicht angewendet, und alle Suchergebnisse werden wie gewohnt angezeigt.

**Beispiel**

.. list-table::

   * - *Virtueller Host*
     - ``host1``
