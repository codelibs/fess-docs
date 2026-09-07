=============================================
Volltextsuche für Dateiserver mit Open Source
=============================================

Einführung
==========

Je mehr Dateiserver die einzelnen Abteilungen aufstellen, desto weniger weiß irgendjemand noch, wo ein bestimmtes Dokument liegt. Die Windows-Suche arbeitet immer nur in einem freigegebenen Ordner und reicht nicht über Servergrenzen hinweg, und die Volltextsuche eines NAS endet an dessen Gehäuse.

Ein Ausweg ist ein eigener Volltextsuchserver vor den Dateiservern. Diese Seite sammelt, was vor dem Einsatz von Fess, einem quelloffenen Volltextsuchserver, an dieser Stelle zu prüfen ist.

Für wen diese Seite gedacht ist
===============================

- Alle, die mit der Suche auf einem internen Dateiserver oder NAS zu kämpfen haben
- Alle, die Volltextsuche prüfen und wissen möchten, ob Open Source dafür ausreicht
- Alle, die Suche einführen wollen, ohne bestehende Zugriffsrechte anzutasten

Fess steht unter der Apache License 2.0 und verursacht keine Lizenzkosten.

Wo die Dateien liegen dürfen
============================

Der Datei-Crawler von Fess beherrscht die folgenden Protokolle. Eingerichtet werden sie in der Verwaltungsoberfläche unter [Crawler] > [Dateisystem] als Start-URL des Crawls.

.. list-table:: Unterstützte Protokolle
   :header-rows: 1
   :widths: 12 33 55

   * - Protokoll
     - URL-Form
     - Typischer Einsatz
   * - ``file``
     - ``file:///home/share/documents/``
     - Ein Verzeichnis auf dem Rechner, der Fess ausführt, einschließlich eines bereits eingehängten NAS
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Windows-Dateifreigaben, von SMB 2.0.2 bis SMB 3.1.1
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Ältere Geräte, die nur SMB1/CIFS sprechen
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - FTP-Server
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 und S3-kompatibler Objektspeicher
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage

Welche Protokolle aktiv sind, steht in ``crawler.file.protocols``; der Standardwert ist ``file,smb,smb1,ftp,s3,gcs``.

Für Windows-Dateifreigaben ist normalerweise ``smb`` die richtige Wahl. ``smb1`` bleibt für alte NAS-Geräte und Druckserver erhalten, die nichts anderes können; SMB1 ist in Windows aus Sicherheitsgründen standardmäßig deaktiviert und daher für eine neue Installation keine Option.

Bestehende Zugriffsrechte bleiben erhalten
==========================================

Die größte Sorge bei einer Suche über einen Dateiserver ist, dass Dokumente in den Treffern auftauchen, die jemand nicht sehen darf. Erscheinen die Ordner von Personal und Buchhaltung bei allen, ist das Suchsystem unbrauchbar, wie gut das Ranking auch sein mag.

Fess löst das, indem es **die Zugriffsrechte des Dateiservers selbst in die Suche übernimmt**.

Funktionsweise
--------------

1. Beim Crawlen liest Fess die ACL jeder Datei
2. Die erlaubten und die verweigerten Konten und Gruppen werden als Rollen des Dokuments gespeichert
3. Bei der Suche werden diese Rollen mit denen des angemeldeten Benutzers abgeglichen, und nur zulässige Dokumente kommen zurück

Sowohl Erlauben als auch Verweigern wird behandelt, intern unterschieden durch die Präfixe ``(allow)`` und ``(deny)``. Das Auslesen der Rollen aus der ACL ist standardmäßig aktiv.

.. list-table:: Einstellungen für die Übernahme der Rechte
   :header-rows: 1
   :widths: 38 14 48

   * - Einstellung
     - Standard
     - Wirkung
   * - ``smb.role.from.file``
     - ``true``
     - Übernimmt Rollen aus der ACL von über SMB gecrawlten Dateien
   * - ``file.role.from.file``
     - ``true``
     - Übernimmt Rollen aus den Rechten des lokalen Dateisystems
   * - ``ftp.role.from.file``
     - ``true``
     - Übernimmt Rollen aus über FTP gecrawlten Dateien
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Welche SID-Typen zu Rollen werden; steuert die Behandlung von Benutzern und Gruppen

Die Voraussetzung, die zuerst zu klären ist
-------------------------------------------

Damit das durchgängig funktioniert, **muss die suchende Person dieselben Rollen tragen**. Im Dokument steht "diese Gruppe darf mich lesen"; solange der suchende Benutzer Fess nicht mitteilen kann, in welchen Gruppen er ist, gibt es nichts abzugleichen.

Damit ist **die Anbindung an Active Directory oder LDAP eine Voraussetzung** für eine rechtebewusste Suche: Fess meldet Benutzer an demselben Verzeichnis an, an dem sie auch der Dateiserver authentifiziert.

Werden dagegen nur freigegebene Ordner indiziert, die im Unternehmen ohnehin alle lesen dürfen, ist die Anbindung nicht nötig. An dieser Unterscheidung entscheidet sich meist der Umfang einer ersten Einführung.

Welche Dateiformate gelesen werden
==================================

Fess gewinnt den Text mit Apache Tika aus dem Dateiinhalt, sodass nicht nur der Name, sondern der Inhalt durchsuchbar ist. Genau das findet ein Dokument, an dessen Titel sich niemand mehr erinnert.

Die wichtigsten Formate sind:

- MS Office (doc, xls, ppt, docx, xlsx, pptx und weitere)
- PDF
- Reiner Text, HTML, XML
- Rich Text (rtf)
- Quelltext (js, c, h, java und weitere)
- Archive (gz, tar, zip und weitere; der Inhalt wird entpackt und mit indiziert)

Die vollständige Liste steht unter `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__.

Dateien ganz ohne Text, etwa gescannte Dokumente und reine Bild-PDFs, lassen sich auf diesem Weg nicht lesen. Ob OCR nötig wird, klärt man am besten vorab an den tatsächlichen Inhalten der Zielordner.

Dimensionierung und Aufbau
==========================

Fess legt seinen Index in OpenSearch ab. Kleine Installationen laufen problemlos mit Fess und OpenSearch auf demselben Rechner; wächst der Bestand, lässt sich OpenSearch als Cluster herauslösen.

Für die Dimensionierung ist die reine Dateizahl ein schlechter Anhaltspunkt. Diese drei Punkte wiegen schwerer:

- Die Gesamtgröße der Zielordner und welcher Anteil davon überhaupt Text enthält
- Wie oft sich Inhalte ändern, täglich oder monatlich, denn das bestimmt den Crawl-Zeitplan
- Die Größe einzelner Dateien, da sehr große Dateien per Konfiguration vom Crawl ausgenommen werden können

Erste Schritte
==============

1. **Zuerst laufen lassen** — der `Schnellstart-Anleitung <https://fess.codelibs.org/de/quick-start.html>`__ folgen. Mit Docker Compose ist in wenigen Minuten etwas Durchsuchbares da
2. **Crawl-Konfiguration anlegen** — Ziel-URL und Crawl-Intervall unter [Crawler] > [Dateisystem] eintragen
3. **Zugangsdaten hinterlegen** — das Konto für die Freigabe unter [Crawler] > [Dateiauthentifizierung] eintragen
4. **Rollen und Labels entwerfen** — Labels für die Filterung nach Abteilung, Rollen für rechteabhängige Treffer

Ein durchgearbeitetes Beispiel steht in `Teil 4 Verstreute Dateien zentral durchsuchen <https://fess.codelibs.org/de/articles/guide-04.html>`__, das ein einziges Suchfeld über mehrere Dateiserver und eine Intranet-Seite aufbaut.

Zusammenfassung
===============

- Fess ist ein quelloffener Suchserver, der Dateiserver über SMB/CIFS, FTP, lokale Pfade, S3 und GCS indizieren kann
- Bei über SMB gecrawlten Dateien filtern die in der ACL hinterlegten Zugriffsrechte die Treffer, und zwar standardmäßig
- Rechtebewusste Suche setzt die Anbindung an Active Directory oder LDAP voraus
- Apache Tika macht den Inhalt von Office-Dokumenten und PDFs durchsuchbar
- Klein anfangen und durch Auslagerung von OpenSearch in ein Cluster wachsen

Weiterführende Hinweise
=======================

- `Crawler-Konfiguration: Web-, Dateiserver- und Datenbank-Crawling <https://fess.codelibs.org/de/stable/config/crawler-basic.html>`__
- `Zugriffssteuerung über Rollen <https://fess.codelibs.org/de/stable/config/security-role.html>`__
- `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__
- `Schnellstart-Anleitung <https://fess.codelibs.org/de/quick-start.html>`__
- `Administrationsleitfaden <https://fess.codelibs.org/de/stable/admin/index.html>`__
