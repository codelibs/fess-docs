======
Nutzung
======

Diese Seite erklärt die grundlegende Nutzung von Fess.
Wenn Sie Fess noch nicht installiert haben, lesen Sie bitte :doc:`setup` oder :doc:`quick-start`.

Über die Benutzeroberfläche von Fess
=====================================

Fess bietet die folgenden Benutzeroberflächen:

-  Browser-basierte Such- und Suchergebnis-UI (für allgemeine Benutzer)
-  Browser-basierte Verwaltungs-UI (für Administratoren)

Suchoberfläche (für allgemeine Benutzer)
=========================================

Zugriff auf die Suchoberfläche
-------------------------------

Dies ist die Benutzeroberfläche, mit der allgemeine Benutzer Dokumente durchsuchen können, die von Fess indiziert wurden.

Rufen Sie http://localhost:8080/ auf, um das Sucheingabefeld und den Suchbutton anzuzeigen.

Grundlegende Suche
------------------

Geben Sie ein Suchwort ein und klicken Sie auf den Suchbutton, um die Suchergebnisse anzuzeigen.

|Browser-basierte Anzeige von Suchergebnissen|

Die Suchergebnisse zeigen folgende Informationen:

- Titel
- URL
- Auszug aus dem Haupttext (Suchbegriffe werden hervorgehoben)
- Datum der letzten Aktualisierung
- Dateigröße (bei Dokumenten)

Erweiterte Suche
----------------

**UND-Suche**

Geben Sie mehrere Schlüsselwörter getrennt durch Leerzeichen ein, um Dokumente zu finden, die alle Schlüsselwörter enthalten.

Beispiel: ``Fess Suche`` → Dokumente, die sowohl „Fess" als auch „Suche" enthalten

**ODER-Suche**

Geben Sie ``OR`` zwischen Schlüsselwörtern ein, um Dokumente zu finden, die eines der Schlüsselwörter enthalten.

Beispiel: ``Fess OR Elasticsearch`` → Dokumente, die „Fess" oder „Elasticsearch" enthalten

**NICHT-Suche**

Fügen Sie ``-`` vor einem Schlüsselwort hinzu, um Dokumente auszuschließen, die dieses Schlüsselwort enthalten.

Beispiel: ``Fess -Elasticsearch`` → Dokumente, die „Fess" enthalten, aber nicht „Elasticsearch"

**Phrasensuche**

Umschließen Sie Schlüsselwörter mit ``""``, um nach einer exakten Phrase zu suchen.

Beispiel: ``"Volltextsuche"`` → Dokumente, die das Wort „Volltextsuche" enthalten

Suchoptionen
------------

Auf der Suchoberfläche sind folgende Optionen verfügbar:

- **Label-Suche**: Suche nur in Dokumenten mit bestimmten Labels
- **Zeitraum festlegen**: Suche nur in Dokumenten, die in einem bestimmten Zeitraum aktualisiert wurden
- **Dateiformate festlegen**: Suche nur in bestimmten Dateiformaten (PDF, Word usw.)

Verwaltungsoberfläche (für Administratoren)
============================================

Zugriff auf die Verwaltungsoberfläche
--------------------------------------

Dies ist die Benutzeroberfläche für Administratoren zur Verwaltung von Fess.

Rufen Sie http://localhost:8080/admin/ auf, um die Anmeldeseite anzuzeigen.

Standard-Administratorkonto:

- **Benutzername**: ``admin``
- **Passwort**: ``admin``

.. warning::

   **Wichtiger Sicherheitshinweis**

   Ändern Sie unbedingt das Standardpasswort.
   Besonders in Produktionsumgebungen wird dringend empfohlen, das Passwort sofort nach der ersten Anmeldung zu ändern.

.. note::

   Die Verwaltungs-UI unterstützt kein Responsive Web Design.
   Der Zugriff über einen PC-Browser wird empfohlen.

Hauptverwaltungsfunktionen
---------------------------

Nach der Anmeldung haben Sie Zugriff auf folgende Einstellungs- und Verwaltungsfunktionen:

**Crawler-Einstellungen**

- Web-Crawl-Einstellungen
- Dateisystem-Crawl-Einstellungen
- Data Store-Crawl-Einstellungen

**Systemeinstellungen**

- Allgemeine Einstellungen (Zeitzone, E-Mail-Einstellungen usw.)
- Benutzer- und Rollenverwaltung
- Scheduler-Einstellungen
- Design-Einstellungen

**Sucheinstellungen**

- Label-Verwaltung
- Keyword-Relevanz-Anpassung
- Synonyme und Wörterbuchverwaltung

Weitere Informationen zur detaillierten Verwaltung finden Sie im Benutzerhandbuch.

Nächste Schritte
================

Nachdem Sie die grundlegende Nutzung verstanden haben, können Sie die folgenden Dokumente konsultieren, um mehr zu erfahren:

- **Benutzerhandbuch**: Details zu Crawl-Einstellungen und Sucheinstellungen
- **API-Dokumentation**: Integration der Suche über REST-API
- **Entwicklerhandbuch**: Entwicklung von Anpassungen und Erweiterungen

.. |Browser-basierte Anzeige von Suchergebnissen| image:: ../resources/images/en/fess_search_result.png
