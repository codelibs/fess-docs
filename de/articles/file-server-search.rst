===============================================
Fileserver-Suche im Unternehmen mit Open Source
===============================================

Einleitung
==========

Wenn jede Abteilung eigene Fileserver hinzufügt, weiß irgendwann niemand mehr, wo ein bestimmtes Dokument liegt.
Die Windows-Suche funktioniert nur innerhalb einer einzelnen Freigabe und kann daher nicht mehrere Server übergreifend durchsuchen.
Auch die Volltextsuche eines NAS lässt sich nicht geräteübergreifend nutzen.

Eine Möglichkeit, dieses Problem zu lösen, ist ein eigener Volltextsuchserver für die Fileserver.
Diese Seite fasst zusammen, was Sie vor der Einführung prüfen sollten, wenn Sie Fileserver mit Fess, einem Open-Source-Volltextsuchserver, durchsuchbar machen möchten.
Der Inhalt bezieht sich auf Fess 15.9.

Zielgruppe
==========

- Alle, die mit der Suche auf internen Fileservern und NAS-Geräten Schwierigkeiten haben
- Alle, die eine Volltextsuche erwägen und wissen möchten, ob sie sich mit Open Source umsetzen lässt
- Alle, die eine Suche einführen möchten, ohne bestehende Zugriffsrechte zu verletzen

Fess wird unter der Apache License 2.0 veröffentlicht und kann ohne Lizenzkosten genutzt werden.

Welche Speicherorte durchsucht werden können
============================================

Das Datei-Crawling von Fess unterstützt die folgenden Protokolle.
Die Einstellung erfolgt in der Verwaltungsoberfläche unter [Crawler] > [Dateisystem]; in „Pfade“ geben Sie den Ort an, an dem das Crawling beginnt.

.. list-table:: Unterstützte Protokolle
   :header-rows: 1
   :widths: 12 33 55

   * - Protokoll
     - Pfadformat
     - Hauptverwendung
   * - ``file``
     - ``file:/home/share/documents/``
     - Verzeichnisse auf dem Server, auf dem Fess läuft, einschließlich eingehängter NAS-Volumes
   * - ``smb``
     - ``smb://fileserver.example.com/share/``
     - Windows-Dateifreigaben und NAS-Geräte, die Dateien über SMB freigeben
   * - ``smb1``
     - ``smb1://fileserver.example.com/share/``
     - Verbindungen über die ältere SMB1-Implementierung; eine Ausweichlösung für alte Geräte, zu denen ``smb`` keine Verbindung herstellen kann
   * - ``ftp``
     - ``ftp://fileserver.example.com/pub/``
     - FTP-Server
   * - ``s3``
     - ``s3://bucket-name/prefix/``
     - Amazon S3 und S3-kompatibler Objektspeicher (erfordert das Plugin ``fess-storage-s3``)
   * - ``gcs``
     - ``gcs://bucket-name/prefix/``
     - Google Cloud Storage (erfordert das Plugin ``fess-storage-gcs``)

Welche Protokolle Fess selbst verarbeitet, bestimmt die Einstellung ``crawler.file.protocols``; ihr Standardwert in 15.9 ist ``file,smb,smb1,ftp``.
``s3`` und ``gcs`` wurden in 15.9 aus Fess selbst in Plugins ausgelagert.
Im Docker-Image sind beide Plugins enthalten. Bei einer Installation aus dem ZIP oder den RPM/DEB-Paketen installieren Sie sie unter [System] > [Plugin] und starten Fess vor der Verwendung neu.

Zum Durchsuchen von Windows-Dateifreigaben verwenden Sie ``smb``.
Sofern Sie auf der Fess-Seite nichts anderes konfigurieren, handelt ``smb`` die Verbindungsversion mit dem Server im Bereich von SMB1 bis SMB 3.1.1 aus.
``smb1`` stellt die Verbindung über eine andere Implementierung (das ältere jcifs) her und ist für neue Konfigurationen nicht gedacht.

Bestehende Zugriffsrechte übernehmen
====================================

Bei der Einführung einer Suche auf Fileservern ist die größte Sorge, dass „Dokumente, die nicht sichtbar sein dürfen, in den Suchergebnissen erscheinen“.
Wenn die Freigaben von Personal- oder Buchhaltungsabteilung in den Suchergebnissen aller Mitarbeitenden auftauchen, ist das Suchsystem selbst unbrauchbar.

Fess löst dieses Problem, indem es die Zugriffsrechte des Fileservers in die Suche übernimmt.
Eine neu angelegte Crawl-Konfiguration filtert die Ergebnisse jedoch noch nicht nach Berechtigungen. Prüfen Sie unbedingt den folgenden Mechanismus und den nächsten Abschnitt „{role}guest aus den Berechtigungen entfernen“.

Funktionsweise
--------------

1. Beim Crawling liest Fess die ACL (Access Control List) jeder Datei
2. Die Konten und Gruppen, denen das Lesen erlaubt ist, sowie die Konten und Gruppen, denen es verweigert ist, werden als „Rollen“ des Dokuments im Feld ``role`` gespeichert
3. Die Werte, die in „Berechtigungen“ der Crawl-Konfiguration eingetragen sind, werden demselben Feld ``role`` hinzugefügt
4. Bei der Suche werden diese mit den Rollen des angemeldeten Benutzers abgeglichen, und es werden nur Dokumente zurückgegeben, für die der Benutzer berechtigt ist

Im Feld ``role`` werden Benutzer mit dem Präfix ``1`` und Gruppen mit dem Präfix ``2`` vor dem Namen gespeichert (zum Beispiel ``1taro`` und ``2sales``).
Verweigerungseinträgen wird zusätzlich ``D`` vorangestellt (zum Beispiel ``D2contractors``).
Ein in „Berechtigungen“ als ``{role}guest`` eingetragener Wert wird als ``Rguest`` gespeichert.
Die in der Verwaltungsoberfläche zu sehenden Angaben ``(allow)`` und ``(deny)`` sind Schreibweisen für die Eingabe in „Berechtigungen“, keine gespeicherten Werte.

Das Ableiten von Rollen aus ACLs ist standardmäßig aktiviert.

.. list-table:: Einstellungen für die Übernahme von Berechtigungen (fess_config.properties)
   :header-rows: 1
   :widths: 38 14 48

   * - Einstellung
     - Standard
     - Beschreibung
   * - ``smb.role.from.file``
     - ``true``
     - Ermittelt Rollen aus den ACLs von Dateien, die mit ``smb`` und ``smb1`` gecrawlt wurden
   * - ``file.role.from.file``
     - ``true``
     - Ermittelt Rollen aus den Zugriffsrechten von Dateien, die mit ``file`` gecrawlt wurden (siehe Hinweise weiter unten)
   * - ``ftp.role.from.file``
     - ``true``
     - Ermittelt Rollen aus Eigentümer und Gruppe von Dateien, die mit ``ftp`` gecrawlt wurden
   * - ``smb.available.sid.types``
     - ``1,2,4:2,5:1``
     - Die als Rollen übernommenen SID-Typen und der Typ, als der sie jeweils gespeichert werden. Standardmäßig werden Benutzer (1) und Domänengruppen (2) unverändert, lokale Gruppen (4) als Gruppen und integrierte SIDs wie Everyone (5) als Benutzer gespeichert

{role}guest aus den Berechtigungen entfernen
--------------------------------------------

Wenn Sie unter [Crawler] > [Dateisystem] eine neue Konfiguration anlegen, ist „Berechtigungen“ bereits mit ``{role}guest`` vorbelegt.
Speichern Sie sie so, erhält jedes Dokument neben den Rollen aus der ACL auch ``Rguest``.
Da nicht angemeldete Benutzer die Rolle ``guest`` erhalten, **werden auch per ACL eingeschränkte Dateien bei der Suche ohne Anmeldung vollständig angezeigt**.

Damit die ACL-basierte Filterung greift, löschen Sie ``{role}guest`` aus „Berechtigungen“ der Crawl-Konfiguration und speichern sie.
Bereits gecrawlte Dokumente werden beim nächsten Crawling mit den neuen Berechtigungen erneut registriert.

Angemeldete Benutzer erhalten die Rolle ``guest`` nicht.
Auch wenn ``{role}guest`` stehen bleibt, erhalten angemeldete Benutzer daher Ergebnisse gemäß den ACLs.
Prüfen Sie, wie in „Verhalten überprüfen“ beschrieben, unbedingt auch im nicht angemeldeten Zustand.

Namen auf der Anmeldeseite abgleichen
-------------------------------------

Damit dieser Mechanismus durchgängig funktioniert, müssen auch die suchenden Benutzer dieselben Rollen haben.
Auf der Dokumentseite ist „Mitglieder dieser Gruppe dürfen lesen“ gespeichert; ein Abgleich ist also nur möglich, wenn der suchende Benutzer Fess mitteilen kann, zu welchen Gruppen er gehört.

Eine berechtigungsbewusste Suche setzt deshalb die Anbindung an Active Directory oder LDAP voraus.
Dabei wird für die Anmeldung an Fess dasselbe Verzeichnis verwendet, mit dem sich auch die Fileserver authentifizieren.
LDAP wird unter [System] > [Allgemein] konfiguriert.
Das Vorgehen und das Konzept der Rollen werden in :doc:`guide-05` erläutert.

Da der Abgleich anhand von Namenszeichenfolgen erfolgt, beachten Sie Folgendes.

- Aus ACLs übernommene Namen werden als Kontonamen ohne Domänennamen gespeichert (aus ``EXAMPLE\taro`` wird ``1taro``)
- Bei Benutzern, die sich über LDAP anmelden, werden die Gruppennamen standardmäßig aus dem CN in ``memberOf`` übernommen. Weicht der Kontoname einer Gruppe auf dem Fileserver von ihrem CN ab, stimmen sie nicht überein
- Integrierte Gruppen wie Everyone werden als Rollen mit diesem Namen gespeichert. Benutzer, die sich über LDAP anmelden, haben diese Rollen normalerweise nicht, sodass Ordner, die nur für integrierte Gruppen freigegeben sind, möglicherweise niemandem angezeigt werden. Teilen Sie bei Bedarf die Crawl-Konfiguration auf und ergänzen Sie die Rollen in „Berechtigungen“

Wenn Sie umgekehrt nur Freigaben einbeziehen, die alle Mitarbeitenden gleichermaßen sehen dürfen, ist diese Anbindung nicht erforderlich.
Hier verläuft die Trennlinie bei der Festlegung des Einführungsumfangs.

Hinweise je Protokoll
---------------------

``smb`` / ``smb1``
   Das Crawl-Konto benötigt nicht nur Leserechte für die Dateiinhalte, sondern auch das Recht, die Zugriffsrechte der Datei (Sicherheitsinformationen) zu lesen.
   Dateien, deren Zugriffsrechte nicht gelesen werden können, werden nicht indiziert und unter [Systeminformationen] > [Fehler-URL] erfasst.

``file``
   Stellt das Dateisystem keine ACLs bereit (wie bei typischen Linux-Dateisystemen), werden nur zwei Rollen gespeichert: der besitzende Benutzer und die besitzende Gruppe.
   Leserechte für „andere“ werden nicht zu einer Rolle.
   Wenn Sie ein NAS auf dem Fess-Server einhängen und mit ``file`` crawlen, wird der am Einhängepunkt sichtbare Eigentümer gespeichert, nicht die ACLs des NAS.
   Crawlen Sie Fileserver, bei denen Sie nach ACLs filtern möchten, direkt mit ``smb``, ohne sie einzuhängen.

``ftp``
   Eigentümer und Gruppe, die der FTP-Server zurückgibt, werden als Rollen gespeichert.

Welche Dateiformate inhaltlich gelesen werden
=============================================

Fess extrahiert mit Apache Tika den Text aus dem Inhalt von Dateien.
Da nicht nur der Dateiname, sondern auch der Text durchsuchbar ist, finden Sie auch „Dokumente, an deren Titel Sie sich nicht erinnern“.

Die wichtigsten unterstützten Formate sind:

- MS Office (doc, xls, ppt, docx, xlsx, pptx usw.)
- PDF
- Text, HTML, XML
- Rich Text (rtf)
- Quellcode (js, c, h, java usw.)
- Archive (gz, tar, zip usw.)

Die vollständige Liste finden Sie unter `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__.

Dateien ohne Text, etwa Bild-PDFs und gescannte Dokumente, lassen sich so nicht im Volltext durchsuchen.
In Fess 15.9 können Sie OCR mit Tesseract aktivieren, um Text aus Bilddateien, aus in Office-Dokumente eingebetteten Bildern und aus PDFs ohne Text zu lesen.
OCR ist standardmäßig deaktiviert.
Installieren Sie ``tesseract`` auf dem Host, auf dem der Crawler läuft, und setzen Sie ``crawler.document.ocr.enabled=true``.
PDFs, bei denen nur einzelne Seiten gescannte Bilder sind, werden nicht erfasst.
Das Vorgehen beschreibt `OCR-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-ocr.html>`__.
Da OCR die Crawl-Dauer verlängert, empfiehlt es sich, vorab zu prüfen, wie viele gescannte Dokumente die Zielordner enthalten.

Architektur und Umfang
======================

Fess speichert den Suchindex in OpenSearch.
In kleinem Umfang können Fess und OpenSearch gemeinsam auf demselben Server laufen; wächst die Zahl der Zieldateien, können Sie OpenSearch als Cluster auslagern.

Bei der Abschätzung des Umfangs wird die Schätzung genauer, wenn Sie neben der Anzahl der Dateien auch Folgendes prüfen.

- Die Gesamtgröße der Zielordner und den Anteil der Dateien, die Text enthalten
- Die Änderungshäufigkeit (täglich oder einige Male im Monat). Sie beeinflusst die Planung des Crawl-Intervalls
- Die Größe pro Datei

Für die Größe indizierbarer Dateien gilt standardmäßig eine Obergrenze.
Die Standardwerte in ``app/WEB-INF/classes/crawler/contentlength.xml`` betragen 2,5 MB für HTML und 10 MB für alle anderen Dateien; größere Dateien werden nicht indiziert und unter [Fehler-URL] erfasst.
Unabhängig davon begrenzt ein Eintrag wie ``client.maxContentLength=10485760`` in „Konfigurationsparameter“ der Crawl-Konfiguration die Größe der abgerufenen Dateien selbst (standardmäßig unbegrenzt).
Legen Sie bei Ordnern mit vielen großen Dokumenten vor der Einführung fest, ob Sie diese Grenzen anpassen.
Die Konfiguration beschreibt der Abschnitt zu den Dateigrößeneinstellungen in `Crawler-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-basic.html>`__.

Auch das Crawl-Intervall erfordert Aufmerksamkeit.
Fess löscht Dokumente aus dem Index, die eine bestimmte Anzahl von Tagen lang durch kein Crawling aktualisiert wurden.
Diese Anzahl ist „Alte Dokumente löschen“ unter [System] > [Allgemein] und beträgt standardmäßig 3 Tage.
Der Standard-Job „Default Crawler“ läuft täglich, sodass dies kein Problem ist. Wenn Sie ihn aber etwa auf einmal pro Woche reduzieren, wählen Sie diese Anzahl von Tagen länger als das Ausführungsintervall.

Worauf Sie bei einem Suchwerkzeug für Fileserver achten sollten
===============================================================

Beim Vergleich von Suchwerkzeugen für Fileserver fällt die Wahl leichter, wenn Sie vor dem Vergleich der Produktnamen prüfen, ob die folgenden Punkte erfüllt sind.

.. list-table:: Prüfpunkte bei der Auswahl eines Suchwerkzeugs
   :header-rows: 1
   :widths: 30 70

   * - Prüfpunkt
     - Bei Fess
   * - Kann es mehrere Server und NAS-Geräte übergreifend durchsuchen?
     - Durch das Anlegen mehrerer Crawl-Konfigurationen können Sie über ein einziges Suchfeld übergreifend suchen
   * - Kann es den Text von Dateien durchsuchen?
     - Apache Tika extrahiert den Text von Office-Dokumenten und PDFs und macht ihn durchsuchbar. Gescannte Dokumente werden durchsuchbar, wenn OCR aktiviert ist
   * - Kann es bestehende Zugriffsrechte übernehmen?
     - Es ermittelt Rollen aus den ACLs von über SMB gecrawlten Dateien und filtert die Suchergebnisse entsprechend. Erforderlich sind die Anbindung an Active Directory oder LDAP sowie eine Überprüfung von „Berechtigungen“ in der Crawl-Konfiguration
   * - Fallen Lizenzkosten an?
     - Es wird unter der Apache License 2.0 veröffentlicht; es fallen keine Lizenzkosten an
   * - Lässt es sich lokal ausprobieren?
     - Sie können es mit Docker Compose starten und die Suche auf Ihrem eigenen Rechner ausprobieren

Ablauf der Einführung
=====================

1. **Zuerst in Betrieb nehmen** — Starten Sie Fess gemäß der `Schnellstart-Anleitung <https://fess.codelibs.org/de/quick-start.html>`__ oder :doc:`guide-02`
2. **Crawl-Konfiguration anlegen** — Registrieren Sie unter [Crawler] > [Dateisystem] einen Namen und Pfade. Wenn Sie nach ACLs filtern, löschen Sie vor dem Speichern ``{role}guest`` aus „Berechtigungen“
3. **Anmeldedaten einrichten** — Registrieren Sie das Konto für den Zugriff auf die Freigaben unter [Crawler] > [Datei-Authentifizierung] und wählen Sie in „Datei-Crawl-Konfiguration“ die Konfiguration aus Schritt 2
4. **Rechte des Crawl-Kontos prüfen** — Prüfen Sie auf dem Fileserver, ob das Konto sowohl die Inhalte als auch die Zugriffsrechte der Zielordner lesen kann
5. **Anmeldung anbinden** — Konfigurieren Sie LDAP (Active Directory) unter [System] > [Allgemein]
6. **Crawling ausführen und prüfen** — Öffnen Sie unter [System] > [Scheduler] den Job „Default Crawler“, klicken Sie auf [Jetzt starten] und prüfen Sie das Ergebnis wie im folgenden Abschnitt „Verhalten überprüfen“ beschrieben

Wenn Sie nach Abteilungen eingrenzen müssen, richten Sie zusätzlich unter [Crawler] > [Label] Labels ein.

Die konkreten Schritte, um mehrere Fileserver und interne Websites über ein einziges Suchfeld durchsuchbar zu machen, behandelt :doc:`guide-04`; den Entwurf der Ergebnisfilterung mit Rollen und Gruppen behandelt :doc:`guide-05`.

Verhalten überprüfen
====================

Prüfen Sie nach Abschluss des Crawlings Folgendes in dieser Reihenfolge.
Der integrierte Benutzer ``admin`` besitzt auch die Rolle ``guest``; verwenden Sie ihn daher nicht zur Prüfung der Filterung.

1. Öffnen Sie [Systeminformationen] > [Fehler-URL] und prüfen Sie, dass keine Dateien wegen Zugriffsfehlern oder Größenüberschreitung nicht übernommen wurden
2. Suchen Sie unter [Systeminformationen] > [Suche] nach einer Datei in einem eingeschränkten Ordner. Auf dieser Seite wird nicht nach Rollen gefiltert, daher werden alle Dokumente angezeigt
3. Klicken Sie beim Ergebnis auf [Aktualisieren], um die Bearbeitungsseite zu öffnen, und prüfen Sie das Feld ``role``. Stellen Sie sicher, dass es Werte aus der ACL wie ``1taro`` oder ``2sales`` enthält und dass ``Rguest`` nicht enthalten ist
4. Suchen Sie im abgemeldeten Zustand auf der Suchseite nach derselben Datei und stellen Sie sicher, dass sie nicht angezeigt wird
5. Melden Sie sich als Benutzer einer Gruppe an, die den Ordner lesen darf, suchen Sie und stellen Sie sicher, dass die Datei angezeigt wird
6. Melden Sie sich als Benutzer an, der nicht zu dieser Gruppe gehört, suchen Sie und stellen Sie sicher, dass die Datei nicht angezeigt wird

Wenn die Namen im Feld ``role`` in Schritt 3 von den Namen auf der LDAP-Seite abweichen, überprüfen Sie die einzelnen Punkte in „Namen auf der Anmeldeseite abgleichen“.

Zusammenfassung
===============

- Fess ist ein Open-Source-Suchserver, der Fileserver (SMB, FTP, lokal) im Volltext durchsuchbar macht. S3 und GCS werden über Plugins unterstützt
- Bei über SMB gecrawlten Dateien werden die in den ACLs gespeicherten Zugriffsrechte zur Filterung der Suchergebnisse verwendet. Das Lesen der ACLs ist standardmäßig aktiviert
- Solange Sie ``{role}guest`` nicht aus „Berechtigungen“ der Crawl-Konfiguration entfernen, sehen nicht angemeldete Benutzer alle Dokumente
- Eine berechtigungsbewusste Suche setzt die Anbindung an Active Directory oder LDAP und übereinstimmende Namen auf beiden Seiten voraus
- Mit Apache Tika wird auch der Text von Office-Dokumenten und PDFs durchsuchbar, und mit aktivierter OCR auch gescannte Dokumente
- Sie können klein anfangen und bei wachsendem Umfang durch ein OpenSearch-Cluster erweitern

Weiterführende Artikel
======================

- Schritte, um mehrere Fileserver und interne Websites gemeinsam zu durchsuchen: :doc:`guide-04`
- Entwurf der Ergebnisfilterung mit Rollen und Gruppen: :doc:`guide-05`
- Fess lokal mit Docker ausprobieren: :doc:`guide-02`

Referenzen
==========

- `Datei-Crawl (Dateiserver-Suche) <https://fess.codelibs.org/de/stable/admin/fileconfig-guide.html>`__
- `Dateiauthentifizierung <https://fess.codelibs.org/de/stable/admin/fileauth-guide.html>`__
- `Crawler-Konfiguration: Web-, Dateiserver- und Datenbank-Crawling <https://fess.codelibs.org/de/stable/config/crawler-basic.html>`__
- `OCR-Konfiguration <https://fess.codelibs.org/de/stable/config/crawler-ocr.html>`__
- `Konfiguration rollenbasierter Suche <https://fess.codelibs.org/de/stable/config/security-role.html>`__
- `LDAP-Integrationsleitfaden <https://fess.codelibs.org/de/stable/config/ldap-integration.html>`__
- `Fehler-URLs <https://fess.codelibs.org/de/stable/admin/failureurl-guide.html>`__
- `Durchsuchbare Dateien <https://fess.codelibs.org/de/supported-files.html>`__
- `Schnellstart-Anleitung <https://fess.codelibs.org/de/quick-start.html>`__
