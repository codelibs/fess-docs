===========================================================================
Teil 10: Stabiler Betrieb eines Suchsystems -- Monitoring, Backup und Störungsbehebung in der Praxis
===========================================================================

Einleitung
==========

Sobald Sie ein Suchsystem aufgebaut und den Benutzern zur Verfügung gestellt haben, wird es zu einem System, das „nicht mehr gestoppt werden kann".
Wenn Benutzer sich im Arbeitsalltag auf die Suche verlassen, führt jede Ausfallzeit direkt zu Geschäftsunterbrechungen.

Dieser Artikel bietet ein praxisnahes Playbook für Monitoring, Backup und Störungsbehebung, um Fess zuverlässig zu betreiben.

Zielgruppe
==========

- Administratoren, die Fess in einer Produktionsumgebung betreiben
- Personen, die einen stabilen Betrieb des Suchsystems sicherstellen möchten
- Personen mit grundlegenden Kenntnissen im Systembetrieb

Betriebsübersicht
==================

Der stabile Betrieb von Fess basiert auf den folgenden drei Säulen:

1. **Monitoring**: Probleme frühzeitig erkennen
2. **Backup**: Daten schützen
3. **Störungsbehebung**: Bei Problemen schnell wiederherstellen

Monitoring
==========

Health Check
--------------

Fess stellt über die REST API einen Health-Check-Endpunkt bereit.

::

    GET http://localhost:8080/api/v1/health

Im Normalbetrieb wird HTTP 200 zurückgegeben.
Durch regelmäßiges Aufrufen dieses Endpunkts mit einem externen Monitoring-Tool (wie Nagios, Zabbix oder Datadog) können Sie den Betriebszustand von Fess überwachen.

Systeminformationen prüfen
---------------------------

Über [Systeminformationen] in der Administrationsoberfläche können Sie die folgenden Informationen einsehen.

**Crawl-Informationen**

Sie können die Ergebnisse der letzten Crawl-Ausführung überprüfen (Anzahl verarbeiteter Dokumente, Anzahl der Fehler usw.).
Verwenden Sie diese Funktion, um zu prüfen, ob Crawls erfolgreich abgeschlossen wurden.

**Systeminformationen**

Sie können die Versionen von Fess und OpenSearch, die JVM-Speicherauslastung, die Anzahl der Dokumente im Index und weitere Informationen einsehen.

Zu überwachende Kennzahlen
---------------------------

.. list-table:: Monitoring-Kennzahlen und Schwellenwertrichtlinien
   :header-rows: 1
   :widths: 25 35 40

   * - Kennzahl
     - Prüfmethode
     - Warnbedingung
   * - Fess-Prozess
     - Health API
     - Keine Antwort oder HTTP 500
   * - OpenSearch-Cluster
     - Cluster Health API
     - Status ist yellow / red
   * - JVM-Heap-Auslastung
     - Systeminformationen
     - Dauerhaft über 80 %
   * - Festplattenauslastung
     - OS-Befehle
     - Über 85 %
   * - Crawl-Ergebnisse
     - Crawl-Informationen
     - Plötzlicher Anstieg der Fehler, drastischer Rückgang der verarbeiteten Anzahl
   * - Suchantwort
     - Suchprotokoll
     - Erhebliche Zunahme der Antwortzeit

Benachrichtigung bei Crawl-Abschluss
--------------------------------------

Fess verfügt über eine Funktion, die Benachrichtigungen sendet, wenn Fehlerprotokolle oder Suchmaschinen-Störungen erkannt werden.
Durch die Konfiguration eines Webhooks für Slack oder Google Chat können Sie sofort über Anomalien informiert werden.

Backup
=======

Backup-Objekte
----------------

Die Backup-Objekte einer Fess-Umgebung lassen sich in zwei Hauptkategorien unterteilen.

**1. Konfigurationsdaten**

Dazu gehören Crawl-Einstellungen, Benutzerinformationen, Wörterbuchdaten und weitere über die Administrationsoberfläche konfigurierte Informationen.
Sie können ein Backup der Konfigurationsdaten über [Systeminformationen] > [Backup] in der Fess-Administrationsoberfläche erstellen.

**2. Indexdaten**

Dies ist der Index der durch Crawling gesammelten Dokumente.
Verwenden Sie die OpenSearch-Snapshot-Funktion, um den Index zu sichern.

Backup-Strategie
-----------------

.. list-table:: Backup-Strategie
   :header-rows: 1
   :widths: 20 25 25 30

   * - Objekt
     - Häufigkeit
     - Aufbewahrungszeitraum
     - Methode
   * - Konfigurationsdaten
     - Täglich
     - 30 Generationen
     - Fess-Backup-Funktion
   * - Index
     - Täglich
     - 7 Generationen
     - OpenSearch-Snapshot
   * - Docker-Konfiguration
     - Bei Änderung
     - Git-verwaltet
     - Versionsverwaltung von compose.yaml

Automatisierung des Konfigurationsdaten-Backups
-------------------------------------------------

Sie können das Backup der Konfigurationsdaten mithilfe der Fess-Administrations-API automatisieren.
Richten Sie es als Scheduler-Job ein oder führen Sie es als externen Cron-Job aus.

Wiederherstellungsverfahren
----------------------------

Es ist wichtig, das Wiederherstellungsverfahren im Voraus zu überprüfen, um für den Fall einer Störung vorbereitet zu sein.

1. Fess stoppen
2. Konfigurationsdaten wiederherstellen (über Administrationsoberfläche oder API)
3. Bei Bedarf aus einem OpenSearch-Snapshot wiederherstellen
4. Fess starten
5. Funktionsprüfung durchführen

Führen Sie das Wiederherstellungsverfahren regelmäßig als Übung durch, um seine Korrektheit zu bestätigen und den Zeitbedarf zu kennen.

Störungsbehebung
=================

Häufige Störungen und Lösungen
-------------------------------

**Fess startet nicht**

- Prüfen Sie die Logdatei (logs/fess.log)
- JVM-Speichermangel: Passen Sie den ``-Xmx``-Parameter an
- Port-Konflikt: Prüfen Sie, ob Port 8080 von einem anderen Prozess belegt wird
- Verbindung zu OpenSearch fehlgeschlagen: Stellen Sie sicher, dass OpenSearch läuft

**Crawl schlägt fehl**

- Prüfen Sie das Job-Protokoll ([Systeminformationen] > [Job-Protokoll])
- Netzwerkverbindung: Überprüfen Sie die Erreichbarkeit des Crawl-Ziels
- Authentifizierungsfehler: Prüfen Sie die Gültigkeit der Anmeldedaten (Passwort, Token)
- Fehler-URLs: Prüfen Sie die Details unter [Systeminformationen] > [Fehler-URL]

**Suche ist langsam**

- Prüfen Sie den OpenSearch-Cluster-Status (bei yellow/red ist Handlungsbedarf)
- Prüfen Sie die Indexgröße (ob sie übermäßig gewachsen ist)
- Prüfen Sie den JVM-Heap (ob Garbage Collection häufig auftritt)
- Falls ein Crawl läuft, prüfen Sie, ob sich die Leistung nach Abschluss des Crawls verbessert

**Suchergebnisse sind veraltet**

- Prüfen Sie den Crawl-Zeitplan (ob er ordnungsgemäß ausgeführt wird)
- Prüfen Sie, ob die maximale Zugriffszahl in den Crawl-Einstellungen ausreichend ist
- Prüfen Sie, ob die Zielseite Crawls blockiert (robots.txt)

Verwaltung von Fehler-URLs
----------------------------

URLs, auf die beim Crawling nicht zugegriffen werden konnte, werden als „Fehler-URLs" erfasst.
Sie können diese unter [Systeminformationen] > [Fehler-URL] in der Administrationsoberfläche einsehen.

Wenn viele Fehler-URLs vorhanden sind, prüfen Sie Folgendes:

- Ob der Zielserver ausgefallen ist
- Ob es Probleme mit dem Netzwerkpfad gibt
- Ob die Anmeldedaten noch gültig sind
- Ob das Crawl-Intervall zu kurz ist und den Zielserver überlastet

Protokollverwaltung
--------------------

Die Logdateien von Fess werden an den folgenden Orten ausgegeben:

- **Fess-Protokoll**: ``logs/fess.log`` (Anwendungsprotokoll)
- **Crawl-Informationen**: [Systeminformationen] > [Crawl-Informationen] in der Administrationsoberfläche
- **Job-Protokoll**: [Systeminformationen] > [Job-Protokoll] in der Administrationsoberfläche
- **Suchprotokoll**: [Systeminformationen] > [Suchprotokoll] in der Administrationsoberfläche

Stellen Sie sicher, dass die Logrotation konfiguriert ist, um ein übermäßiges Anwachsen der Logdateien zu verhindern.

Betriebs-Checkliste
=====================

Hier ist eine Checkliste der Punkte, die im täglichen Betrieb zu überprüfen sind.

**Tägliche Prüfungen**

- Wurde der Crawl erfolgreich abgeschlossen?
- Liefert der Health Check normale Ergebnisse?
- Liegt die Festplattenauslastung unter dem Schwellenwert?

**Wöchentliche Prüfungen**

- Null-Treffer-Rate in den Suchprotokollen (siehe Teil 8)
- Überprüfung und Behandlung von Fehler-URLs
- Werden Backups erfolgreich erstellt?

**Monatliche Prüfungen**

- Entwicklung der Indexgröße
- Trends der JVM-Speicherauslastung
- Wörterbuch-Aktualisierungen (siehe Teil 9)
- Überprüfung von Sicherheitspatches

Zusammenfassung
================

Dieser Artikel behandelte Monitoring, Backup und Störungsbehebung für den stabilen Betrieb von Fess.

- Überwachung mit der Health API und der Administrationsoberfläche
- Backup-Strategie für Konfigurationsdaten und Indexdaten
- Häufige Störungsmuster und Lösungen
- Tägliche, wöchentliche und monatliche Betriebs-Checklisten

Um die Erwartung aufrechtzuerhalten, dass „die Suche einfach funktioniert", sollten Sie ein proaktives Betriebskonzept etablieren.

Im nächsten Artikel werden Integrationsmuster mit bestehenden Systemen unter Verwendung der Such-API behandelt.

Referenzen
==========

- `Fess Systemverwaltung <https://fess.codelibs.org/ja/15.5/admin/systeminfo.html>`__

- `Fess Backup <https://fess.codelibs.org/ja/15.5/admin/backup.html>`__
