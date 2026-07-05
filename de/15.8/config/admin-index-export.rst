============================
Index-Export-Funktion
============================

Übersicht
=========

Die Index-Export-Funktion exportiert in OpenSearch indizierte Suchdokumente als HTML- oder JSON-Dateien in das lokale Dateisystem. Diese Funktionalität ist nützlich für:

- Erstellung statischer Backups von indizierten Inhalten
- Generierung von Offline-Kopien von Dokumenten für Archivierungszwecke
- Erstellung statischer Suchergebnisseiten
- Migration von Inhalten zu anderen Systemen

Die exportierten Dateien behalten die ursprüngliche URL-Pfadstruktur der Quelldokumente bei, was die Verwaltung der exportierten Inhalte erleichtert.

Funktionsweise
==============

Wenn der Index-Export-Job ausgeführt wird, erfolgt folgender Prozess:

1. **Dokumente abrufen**: Abrufen von Dokumenten aus OpenSearch mittels Scroll-API für effiziente Stapelverarbeitung
2. **Inhalt verarbeiten**: Extrahieren von Dokumentfeldern (Titel, Inhalt, URL usw.) und Entfernen ausgeschlossener Felder
3. **Verzeichnisstruktur erstellen**: Replizieren der URL-Pfadstruktur im Export-Verzeichnis basierend auf dem ``url``-Feld des Dokuments
4. **Dateien generieren**: Erstellen von Dateien (HTML oder JSON) mit dem Dokumentinhalt
5. **Bis zur Fertigstellung fortfahren**: Stapelverarbeitung fortsetzen, bis der Index vollständig exportiert ist

Die Scroll-API gewährleistet eine effiziente Verarbeitung großer Dokumentenmengen ohne Speicherprobleme.

.. note::

   Exportiert werden Dokumente aus dem Suchindex (``fess.search``). Dokumente ohne ``url``-Feld werden übersprungen.

Konfigurationseigenschaften
============================

Konfigurieren Sie die Index-Export-Funktion in ``fess_config.properties``:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Eigenschaft
     - Standardwert
     - Beschreibung
   * - ``index.export.path``
     - ``/var/lib/fess/export``
     - Verzeichnis zum Speichern der exportierten Dateien
   * - ``index.export.exclude.fields``
     - ``cache``
     - Kommagetrennte Liste der vom Export auszuschließenden Felder
   * - ``index.export.scroll.size``
     - ``100``
     - Anzahl der pro Stapel verarbeiteten Dokumente
   * - ``index.export.format``
     - ``html``
     - Exportdateiformat (``html`` oder ``json``)

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
3. Suchen Sie **Index Exporter** in der Job-Liste
4. Klicken Sie, um die Job-Einstellungen zu bearbeiten
5. Legen Sie den Zeitplan mit einem Cron-Ausdruck fest
6. Speichern Sie die Einstellungen

Beispiele für Cron-Ausdrücke:

- ``0 0 2 * * ?`` - Täglich um 2:00 Uhr ausführen
- ``0 0 3 ? * SUN`` - Jeden Sonntag um 3:00 Uhr ausführen
- ``0 0 0 1 * ?`` - Am ersten Tag jedes Monats um Mitternacht ausführen

Benutzerdefinierte Abfragefilterung
====================================

Durch Anpassen des Job-Skripts kann der Export auf bestimmte Dokumente eingeschränkt werden.

Das Standardskript des **Index Exporter**-Jobs exportiert alle Dokumente:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.matchAllQuery())
        .execute()

So fügen Sie einen benutzerdefinierten Abfragefilter hinzu:

1. Navigieren Sie zu **System** > **Scheduler**
2. Bearbeiten Sie den **Index Exporter**
3. Ändern Sie das Job-Skript, um einen Abfragefilter hinzuzufügen

Beispiel mit Datumsfilter (nur Dokumente der letzten 7 Tage exportieren):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.rangeQuery("created").gte("now-7d"))
        .execute()

Beispiel mit Website-Filter (nur Dokumente einer bestimmten Website exportieren):

::

    return new org.codelibs.fess.job.IndexExportJob()
        .query(org.opensearch.index.query.QueryBuilders.wildcardQuery("url", "*example.com*"))
        .execute()

Beispiel für Export im JSON-Format:

::

    return new org.codelibs.fess.job.IndexExportJob()
        .format("json")
        .execute()

Exportierte Dateistruktur
==========================

Exportierte Dateien sind so organisiert, dass sie die ursprüngliche URL-Struktur widerspiegeln.

Beispielsweise wird ein Dokument mit der URL ``https://example.com/docs/guide/intro.html`` exportiert nach:

::

    /var/lib/fess/export/
    └── example.com/
        └── docs/
            └── guide/
                └── intro.html

Der Dateipfad wird aus dem ``url``-Feld des Dokuments nach folgenden Regeln ermittelt:

- Der Hostname wird zum Verzeichnis der obersten Ebene. Enthält die URL keinen Hostnamen, wird ``_local`` verwendet.
- Endet der Pfad mit einem Schrägstrich oder besitzt er keinen Pfad, wird eine Indexdatei (``index.html`` oder ``index.json``) erstellt.
- Enthält der Pfad keine Dateiendung, wird die dem Format entsprechende Endung (``.html`` oder ``.json``) angehängt.
- Im Dateinamen unzulässige Zeichen (``< > : " | ? * \``) werden durch ``_`` ersetzt; jede Pfadkomponente wird auf maximal 200 Zeichen gekürzt.
- Kann die URL nicht geparst werden oder wird ein Pfad-Traversal-Angriff erkannt, wird ein Hash-Wert der URL als Dateiname im Verzeichnis ``_invalid`` gespeichert.

Im HTML-Format wird jede Datei nach folgender Struktur erzeugt:

- Feld ``title`` → ``<title>``-Element
- Feld ``lang`` → ``lang``-Attribut des ``<html>``-Elements
- Feld ``content`` → Hauptinhalt des ``<body>``-Elements
- Alle übrigen nicht ausgeschlossenen Felder → ``<meta name="fess:Feldname" content="Wert">``-Tags im ``<head>``

::

    <!DOCTYPE html>
    <html lang="de">
    <head>
    <meta charset="UTF-8">
    <title>Beispieldokument</title>
    <meta name="fess:url" content="https://example.com/docs/guide/intro.html">
    <meta name="fess:last_modified" content="2024-01-01T00:00:00.000Z">
    <meta name="fess:content_type" content="text/html">
    </head>
    <body>
    Hauptinhalt des Dokuments
    </body>
    </html>

Im JSON-Format enthält jede Datei ein JSON-Objekt mit allen nicht ausgeschlossenen Feldern:

::

    {
      "url": "https://example.com/docs/guide/intro.html",
      "title": "Beispieldokument",
      "content": "Hauptinhalt des Dokuments",
      "last_modified": "2024-01-01T00:00:00.000Z",
      "content_type": "text/html"
    }

Best Practices
==============

Speicherüberlegungen
--------------------

- Stellen Sie ausreichend Speicherplatz im Export-Verzeichnis sicher
- Erwägen Sie dedizierten Speicher für große Dokumentenmengen
- Implementieren Sie bei regelmäßigen Exporten eine periodische Bereinigung alter Exporte

Leistungstipps
--------------

- Passen Sie ``index.export.scroll.size`` je nach Dokumentgröße an:
  - Kleinere Dokumente: größere Stapelgröße (200-500)
  - Größere Dokumente: kleinere Stapelgröße (50-100)
- Planen Sie Exporte in Zeiten geringer Auslastung
- Überwachen Sie die Festplatten-E/A während Export-Vorgängen

Sicherheitsempfehlungen
------------------------

- Legen Sie angemessene Dateiberechtigungen für das Export-Verzeichnis fest
- Stellen Sie das Export-Verzeichnis nicht direkt im Web bereit
- Erwägen Sie die Verschlüsselung exportierter Inhalte bei sensiblen Daten
- Überprüfen Sie regelmäßig den Zugriff auf exportierte Dateien

Fehlerbehebung
==============

Export-Job wird nicht ausgeführt
---------------------------------

1. Überprüfen Sie, ob der Job im Scheduler aktiviert ist
2. Prüfen Sie die Syntax des Cron-Ausdrucks
3. Überprüfen Sie die |Fess|-Protokolle auf Fehlermeldungen:

::

    tail -f /var/log/fess/fess.log | grep IndexExport

Leeres Export-Verzeichnis
--------------------------

1. Stellen Sie sicher, dass Dokumente im Index vorhanden sind
2. Prüfen Sie die Berechtigungen des Export-Pfads
3. Überprüfen Sie, ob der Abfragefilter (bei benutzerdefinierter Konfiguration) mit Dokumenten übereinstimmt

::

    # Dokumentanzahl im Index prüfen
    curl -X GET "localhost:9201/fess.search/_count?pretty"

Export schlägt mittendrin fehl
--------------------------------

1. Prüfen Sie den verfügbaren Speicherplatz
2. Überprüfen Sie die Protokolle auf Speicher- oder Timeout-Fehler
3. Erwägen Sie die Reduzierung von ``scroll.size`` bei großen Dokumenten
4. Prüfen Sie die Timeout-Einstellungen des OpenSearch-Scroll-Kontexts

Dateien nicht zugänglich
-------------------------

1. Überprüfen Sie die Dateiberechtigungen: ``ls -la /var/lib/fess/export``
2. Prüfen Sie, ob der Verzeichnisbesitzer mit dem |Fess|-Prozessbenutzer übereinstimmt
3. Stellen Sie sicher, dass SELinux- oder AppArmor-Richtlinien den Zugriff erlauben

Verwandte Themen
================

- :doc:`admin-index-backup` - Verfahren zur Index-Sicherung und -Wiederherstellung
- :doc:`admin-logging` - Konfiguration der Protokolleinstellungen zur Fehlerbehebung
