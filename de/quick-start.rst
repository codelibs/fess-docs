==============
Schnellstart-Anleitung
==============

Einführung
==========

Diese Anleitung richtet sich an Personen, die Fess schnell ausprobieren möchten.
Es werden die minimal erforderlichen Schritte zur Nutzung von Fess beschrieben.

Die hier beschriebene Vorgehensweise dient nur zum Ausprobieren. Für produktive Aufbau-Verfahren siehe die :doc:`Installationsanleitung <setup>` mit Docker.
(Die in dieser Anleitung gestartete Fess-Instanz ist für einfache Funktionstests gedacht; ein produktiver Betrieb dieser Umgebung wird nicht empfohlen)

Vorbereitung
============

Bevor Sie Fess starten, installieren Sie bitte Java 21.
Für Java 21 wird `Eclipse Temurin <https://adoptium.net/temurin>`__ empfohlen.

Download
========

Laden Sie das neueste Fess-ZIP-Paket von der `GitHub-Release-Seite <https://github.com/codelibs/fess/releases>`__ herunter.

Installation
============

Entpacken Sie die heruntergeladene Datei fess-x.y.z.zip.

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

Starten von Fess
================

Führen Sie das fess-Skript aus, um Fess zu starten.
(Unter Windows führen Sie bitte fess.bat aus)

::

    $ ./bin/fess

Zugriff auf die Verwaltungs-UI
===============================

Rufen Sie \http://localhost:8080/admin auf.
Der Standard-Benutzername/das Passwort für das Administratorkonto ist admin/admin.

.. warning::

   Ändern Sie unbedingt das Standardpasswort.
   In Produktionsumgebungen wird dringend empfohlen, das Passwort sofort nach der ersten Anmeldung zu ändern.

Erstellen einer Crawl-Konfiguration
====================================

Klicken Sie nach der Anmeldung im linken Menü auf „Crawler" > „Web".
Klicken Sie auf die Schaltfläche „Neu erstellen", um Informationen zur Web-Crawl-Konfiguration zu erstellen.

Geben Sie folgende Informationen ein:

- **Name**: Name der Crawl-Konfiguration (z. B. Firmen-Website)
- **URL**: Zu crawlende URL (z. B. https://www.example.com/)
- **Maximale Zugriffe**: Obergrenze für zu crawlende Seiten
- **Intervall**: Crawl-Intervall (Millisekunden)

Ausführen des Crawls
=====================

Klicken Sie im linken Menü auf „System" > „Scheduler".
Klicken Sie auf die Schaltfläche „Jetzt starten" für den Job „Default Crawler", um den Crawl sofort zu starten.

Für eine geplante Ausführung wählen Sie „Default Crawler" und konfigurieren Sie einen Zeitplan.
Wenn die Startzeit 10:35 Uhr sein soll, geben Sie 35 10 \* \* ? ein (Format: „Minute Stunde Tag Monat Wochentag Jahr").
Nach der Aktualisierung wird der Crawl nach dieser Zeit gestartet.

Sie können unter „Crawl-Informationen" überprüfen, ob der Crawl gestartet wurde.
Nach Abschluss des Crawls werden die WebIndexSize-Informationen in den Sitzungsinformationen angezeigt.

Suche
=====

Nach Abschluss des Crawls rufen Sie \http://localhost:8080/ auf und führen Sie eine Suche durch, um die Suchergebnisse anzuzeigen.

Stoppen von Fess
================

Stoppen Sie den Fess-Prozess mit Strg-C oder dem kill-Befehl.

Mehr erfahren
=============

Weitere Informationen finden Sie in den folgenden Dokumenten:

* `Dokumentationsübersicht <documentation>`__
* `[Serie] Einfache Einführung! Einführung in den OSS-Volltextsuchserver Fess <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* `Informationen für Entwickler <development>`__
* `Diskussionsforum <https://discuss.codelibs.org/c/fessja/>`__
