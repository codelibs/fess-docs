=====================
Produkt-Support-Frist
=====================

Produkte, die das End-of-Life-Datum (EOL) überschritten haben, erhalten keine Wartung oder Aktualisierungen mehr.
Das CodeLibs-Projekt empfiehlt dringend, auf ein unterstütztes Release zu migrieren.
So vermeiden Sie Situationen, in denen benötigte Dienste und Support nicht mehr verfügbar sind.
Das neueste Release kann von der `Download-Seite <downloads.html>`__ heruntergeladen werden.

Wenn Sie Support für Produkte benötigen, die die Support-Frist überschritten haben, wenden Sie sich bitte an den `kommerziellen Support <https://www.n2sm.net/products/n2search.html>`__.

.. warning::

   **Empfohlene Maßnahmen vor dem Support-Ende**

   Bitte planen und führen Sie vor dem Support-Enddatum folgende Maßnahmen durch:

   1. **Backups erstellen**: Sichern Sie Konfigurationsdateien und Indexdaten
   2. **In Staging-Umgebung testen**: Überprüfen Sie den Betrieb mit der neuen Version vor der Produktionsmigration
   3. **Release-Notes prüfen**: Prüfen Sie auf Breaking Changes und veraltete Funktionen
   4. **Migrationsplan erstellen**: Erstellen Sie einen Plan unter Berücksichtigung der Ausfallzeitanforderungen

Upgrade-Pfad
=============

Die folgende Tabelle zeigt den empfohlenen Upgrade-Pfad von Ihrer aktuellen Version zum neuesten Release.

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Aktuelle Version
     - Empfohlener Pfad
     - Hinweise
   * - 15.x auf 15.5
     - Direktes Upgrade möglich
     - Siehe `Upgrade-Anleitung <15.5/install/upgrade.html>`__
   * - 14.x auf 15.5
     - Direktes Upgrade möglich
     - Achten Sie auf Änderungen an Konfigurationsdateien
   * - 13.x auf 15.5
     - Über 14.x empfohlen
     - Upgrade in dieser Reihenfolge: 13.x auf 14.19 auf 15.5
   * - 12.x oder älter auf 15.5
     - Stufenweises Upgrade erforderlich
     - Führen Sie das Upgrade jeweils 1-2 Hauptversionen durch

.. note::

   Für detaillierte Upgrade-Verfahren siehe die `Upgrade-Anleitung <15.5/install/upgrade.html>`__.
   Für große Umgebungen oder komplexe Konfigurationen empfehlen wir die Beratung durch den `kommerziellen Support <support-services.html>`__.

Migrationsressourcen
====================

Nützliche Dokumente für das Upgrade:

- `Upgrade-Anleitung <15.5/install/upgrade.html>`__ - Detaillierte Schritte vom Backup bis zum Abschluss des Upgrades
- `Release-Notes <https://github.com/codelibs/fess/releases>`__ - Änderungen und Hinweise für jede Version
- `Fehlerbehebung <15.5/install/troubleshooting.html>`__ - Häufige Probleme und Lösungen
- `Docker-Upgrade <15.5/install/install-docker.html>`__ - Upgrade in Docker-Umgebungen

Wartungstabelle
===============

Das EOL-Datum von Fess liegt etwa 18 Monate nach der Veröffentlichung.

**Legende**:

- 🟢 **Unterstützt**: Sicherheitskorrekturen und Fehlerbehebungen werden bereitgestellt
- 🟡 **Support-Ende naht**: Support endet innerhalb von 6 Monaten
- 🔴 **Support beendet**: Keine Wartung wird bereitgestellt

Aktuell unterstützte Versionen
------------------------------

.. tabularcolumns:: |p{3cm}|p{4cm}|p{3cm}|
.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Fess
     - EOL-Datum
     - Status
   * - 15.5.x
     - 2027-08-01
     - 🟢 Neueste (Empfohlen)
   * - 15.4.x
     - 2027-06-01
     - 🟢 Unterstützt
   * - 15.3.x
     - 2027-04-01
     - 🟢 Unterstützt
   * - 15.2.x
     - 2027-03-01
     - 🟢 Unterstützt
   * - 15.1.x
     - 2027-01-01
     - 🟢 Unterstützt
   * - 15.0.x
     - 2026-12-01
     - 🟢 Unterstützt
   * - 14.19.x
     - 2026-08-01
     - 🟡 Support-Ende naht
   * - 14.18.x
     - 2026-05-01
     - 🟡 Support-Ende naht
   * - 14.17.x
     - 2026-03-01
     - 🔴 Support beendet
   * - 14.16.x
     - 2026-02-01
     - 🔴 Support beendet
   * - 14.15.x
     - 2026-01-01
     - 🔴 Support beendet

Nicht mehr unterstützte Versionen
---------------------------------

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - Fess
     - EOL-Datum
   * - 14.14.x
     - 2025-11-01
   * - 14.13.x
     - 2025-10-01
   * - 14.12.x
     - 2025-08-01
   * - 14.11.x
     - 2025-04-01
   * - 14.10.x
     - 2025-01-01
   * - 14.9.x
     - 2024-12-01
   * - 14.8.x
     - 2024-11-01
   * - 14.7.x
     - 2024-09-01
   * - 14.6.x
     - 2024-07-01
   * - 14.5.x
     - 2024-05-01
   * - 14.4.x
     - 2024-02-24
   * - 14.3.x
     - 2023-12-28
   * - 14.2.x
     - 2023-10-26
   * - 14.1.x
     - 2023-09-08
   * - 14.0.x
     - 2023-08-08
   * - 13.16.x
     - 2023-06-07
   * - 13.15.x
     - 2023-03-22
   * - 13.14.x
     - 2023-02-03
   * - 13.13.x
     - 2022-11-25
   * - 13.12.x
     - 2022-09-23
   * - 13.11.x
     - 2022-08-10
   * - 13.10.x
     - 2022-05-11
   * - 13.9.x
     - 2022-02-18
   * - 13.8.x
     - 2021-12-18
   * - 13.7.x
     - 2021-11-13
   * - 13.6.x
     - 2021-08-11
   * - 13.5.x
     - 2021-06-02
   * - 13.4.x
     - 2021-04-01
   * - 13.3.x
     - 2021-01-31
   * - 13.2.x
     - 2020-12-25
   * - 13.1.x
     - 2020-11-20
   * - 13.0.x
     - 2020-10-10
   * - 12.7.x
     - 2020-11-20
   * - 12.6.x
     - 2020-09-26
   * - 12.5.x
     - 2020-07-29
   * - 12.4.x
     - 2020-05-14
   * - 12.3.x
     - 2020-02-23
   * - 12.2.x
     - 2020-12-13
   * - 12.1.x
     - 2019-08-19
   * - 12.0.x
     - 2019-06-02
   * - 11.4.x
     - 2019-03-23
   * - 11.3.x
     - 2019-02-14
   * - 11.2.x
     - 2018-12-15
   * - 11.1.x
     - 2018-11-11
   * - 11.0.x
     - 2018-08-13
   * - 10.3.x
     - 2018-05-24
   * - 10.2.x
     - 2018-02-30
   * - 10.1.x
     - 2017-12-09
   * - 10.0.x
     - 2017-08-05
   * - 9.4.x
     - 2016-11-21
   * - 9.3.x
     - 2016-05-06
   * - 9.2.x
     - 2015-12-28
   * - 9.1.x
     - 2015-09-26
   * - 9.0.x
     - 2015-08-07
   * - 8.x
     - 2014-08-23
   * - 7.x
     - 2014-02-03
   * - 6.x
     - 2013-09-02
   * - 5.x
     - 2013-06-15
   * - 4.x
     - 2012-06-19
   * - 3.x
     - 2011-09-07
   * - 2.x
     - 2011-07-16
   * - 1.x
     - 2011-04-10

Häufig gestellte Fragen
========================

F: Kann ich Fess nach dem Ende der Support-Frist weiter verwenden?
-------------------------------------------------------------------

A: Technisch ist es möglich, aber Sicherheitskorrekturen und Fehlerbehebungen werden nicht mehr bereitgestellt.
Um Sicherheitsrisiken zu minimieren, empfehlen wir dringend ein Upgrade auf eine unterstützte Version.

F: Wie lange dauert ein Upgrade?
----------------------------------

A: Es hängt vom Umfang Ihrer Umgebung ab, aber in der Regel 2 bis 4 Stunden.
Für große Umgebungen oder komplexe Konfigurationen empfehlen wir, zuerst in einer Staging-Umgebung zu testen.
Siehe die `Upgrade-Anleitung <15.5/install/upgrade.html>`__ für Details.

F: Was soll ich tun, wenn ich ein Problem mit einer nicht mehr unterstützten Version habe?
-------------------------------------------------------------------------------------------

A: Sie haben folgende Möglichkeiten:

1. **Auf die neueste Version upgraden**: Die empfohlene Maßnahme
2. **In Community-Foren fragen**: Sie können möglicherweise Ratschläge von anderen Benutzern erhalten
3. **Kommerziellen Support konsultieren**: Der `kommerzielle Support von N2SM <support-services.html>`__ kann Wartung für bestimmte Versionen bereitstellen

F: Was sollte ich vor einem Upgrade prüfen?
---------------------------------------------

A: Bitte überprüfen Sie Folgendes:

1. Prüfen Sie die `Release-Notes <https://github.com/codelibs/fess/releases>`__ auf Breaking Changes
2. Überprüfen Sie die Kompatibilität der OpenSearch-Version
3. Wenn Sie Anpassungen haben, prüfen Sie die Kompatibilität von Einstellungen und Plugins
4. Erstellen Sie gründliche Backups

F: Erfordert ein Upgrade in einer Docker-Umgebung besondere Schritte?
----------------------------------------------------------------------

A: Sie müssen Docker-Volumes sichern und die neuen Docker-Compose-Dateien herunterladen.
Siehe die `Docker-Installationsanleitung <15.5/install/install-docker.html>`__ für Details.
