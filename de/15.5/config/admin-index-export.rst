======================
Index-Export-Funktion
======================

Übersicht
=========

Die Index-Export-Funktion ermöglicht den Export von in OpenSearch indizierten Suchdokumenten als HTML-Dateien in das lokale Dateisystem. Diese Funktionalität ist nützlich für:

- Erstellung statischer Backups von indizierten Inhalten
- Generierung von Offline-Kopien von Dokumenten für Archivierungszwecke
- Erstellung statischer Suchergebnisseiten
- Migration von Inhalten zu anderen Systemen

Die exportierten Dateien behalten die ursprüngliche URL-Pfadstruktur der Quelldokumente bei, was die Navigation und Verwaltung der exportierten Inhalte erleichtert.

Funktionsweise
==============

Wenn der Index-Export-Job ausgeführt wird, erfolgt folgender Prozess:

1. **Dokumente abfragen**: Abrufen von Dokumenten aus OpenSearch mittels Scroll-API für effiziente Stapelverarbeitung
2. **Inhalt verarbeiten**: Extrahieren von Dokumentfeldern (Titel, Inhalt, URL usw.)
3. **Verzeichnisstruktur erstellen**: Replizieren der URL-Pfadstruktur im Export-Verzeichnis
4. **HTML-Dateien generieren**: Erstellen von HTML-Dateien mit dem Dokumentinhalt
5. **Bis zur Fertigstellung fortfahren**: Verarbeitung aller Dokumente in Stapeln bis der Index vollständig exportiert ist

Die Scroll-API gewährleistet eine effiziente Verarbeitung großer Dokumentenmengen ohne Speicherprobleme.

Konfigurationseigenschaften
===========================

Konfigurieren Sie die Index-Export-Funktion in ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``index.export.path``
     - ``/var/fess/export``
     - Verzeichnis für exportierte Dateien
   * - ``index.export.exclude.fields``
     - ``cache``
     - Kommagetrennte Liste der auszuschließenden Felder
   * - ``index.export.scroll.size``
     - ``100``
     - Anzahl der pro Stapel verarbeiteten Dokumente

Konfigurationsbeispiel:

::

    index.export.path=/data/fess/export
    index.export.exclude.fields=cache,boost,role
    index.export.scroll.size=200

Job aktivieren
==============

Der Index-Export-Job ist als geplanter Job registriert, aber standardmäßig deaktiviert.

So aktivieren Sie den Job:

1. Melden Sie sich bei der |Fess|-Administrationskonsole an
2. Navigieren Sie zu **System** > **Scheduler**
3. Suchen Sie **Index Export Job** in der Job-Liste
4. Klicken Sie, um die Job-Einstellungen zu bearbeiten
5. Legen Sie den Zeitplan mit einem Cron-Ausdruck fest
6. Speichern Sie die Einstellungen

Beispiele für Cron-Ausdrücke:

- ``0 0 2 * * ?`` - Täglich um 2:00 Uhr ausführen
- ``0 0 3 ? * SUN`` - Jeden Sonntag um 3:00 Uhr ausführen
- ``0 0 0 1 * ?`` - Am ersten Tag jedes Monats um Mitternacht ausführen

Benutzerdefinierte Abfragefilterung
===================================

Sie können den Export-Job anpassen, um nur bestimmte Dokumente zu exportieren, indem Sie das Job-Skript ändern.

So fügen Sie einen benutzerdefinierten Abfragefilter hinzu:

1. Navigieren Sie zu **System** > **Scheduler**
2. Bearbeiten Sie den **Index Export Job**
3. Ändern Sie das Job-Skript, um einen Abfragefilter hinzuzufügen

Beispielskript mit Datumsfilter:

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "created:>=now-7d"
    job.execute()

Beispielskript mit Website-Filter:

::

    import org.codelibs.fess.exec.IndexExportJob
    
    def job = new IndexExportJob()
    job.query = "url:*example.com*"
    job.execute()

Exportierte Dateistruktur
=========================

Exportierte Dateien sind so organisiert, dass sie die ursprüngliche URL-Struktur widerspiegeln.

Beispielsweise würde ein Dokument mit der URL ``https://example.com/docs/guide/intro.html`` exportiert nach:

::

    /var/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

Jede exportierte HTML-Datei enthält:

- Dokumenttitel
- Hauptinhaltstext
- Metadaten (Datum der letzten Änderung, Inhaltstyp usw.)
- Referenz zur ursprünglichen URL

Best Practices
==============

Speicherüberlegungen
--------------------

- Stellen Sie ausreichend Speicherplatz im Export-Verzeichnis sicher
- Erwägen Sie dedizierten Speicher für große Dokumentenmengen
- Implementieren Sie regelmäßige Bereinigung alter Exporte bei periodischen Exporten

Leistungstipps
--------------

- Passen Sie ``index.export.scroll.size`` basierend auf der Dokumentgröße an:
  - Kleinere Dokumente: größere Stapelgröße (200-500)
  - Größere Dokumente: kleinere Stapelgröße (50-100)
- Planen Sie Exporte während Zeiten geringer Nutzung
- Überwachen Sie Festplatten-I/O während Export-Operationen

Sicherheitsempfehlungen
-----------------------

- Legen Sie angemessene Dateiberechtigungen für das Export-Verzeichnis fest
- Stellen Sie das Export-Verzeichnis nicht direkt im Web bereit
- Erwägen Sie die Verschlüsselung exportierter Inhalte bei sensiblen Informationen
- Überprüfen Sie regelmäßig den Zugriff auf exportierte Dateien

Fehlerbehebung
==============

Export-Job wird nicht ausgeführt
--------------------------------

1. Überprüfen Sie, ob der Job im Scheduler aktiviert ist
2. Prüfen Sie die Syntax des Cron-Ausdrucks
3. Überprüfen Sie |Fess|-Protokolle auf Fehlermeldungen:

::

    tail -f /var/log/fess/fess.log | grep IndexExport

Leeres Export-Verzeichnis
-------------------------

1. Bestätigen Sie, dass Dokumente im Index vorhanden sind
2. Prüfen Sie die Berechtigungen des Export-Pfads
3. Überprüfen Sie, ob der Abfragefilter (falls benutzerdefiniert) mit Dokumenten übereinstimmt

::

    # Dokumentanzahl im Index prüfen
    curl -X GET "localhost:9201/fess.YYYYMMDD/_count?pretty"

Export schlägt mittendrin fehl
------------------------------

1. Prüfen Sie den verfügbaren Speicherplatz
2. Überprüfen Sie Protokolle auf Speicher- oder Timeout-Fehler
3. Erwägen Sie die Reduzierung von ``scroll.size`` für große Dokumente
4. Prüfen Sie die Timeout-Einstellungen des OpenSearch-Scroll-Kontexts

Dateien nicht zugänglich
------------------------

1. Überprüfen Sie Dateiberechtigungen: ``ls -la /var/fess/export``
2. Prüfen Sie, ob der Verzeichnisbesitzer mit dem |Fess|-Prozessbenutzer übereinstimmt
3. Bestätigen Sie, dass SELinux- oder AppArmor-Richtlinien den Zugriff erlauben

Verwandte Themen
================

- :doc:`admin-index-backup` - Verfahren zur Index-Sicherung und -Wiederherstellung
- :doc:`admin-logging` - Konfiguration der Protokolleinstellungen zur Fehlerbehebung
