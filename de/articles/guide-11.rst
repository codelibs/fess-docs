======================================================
Teil 11: Bestehende Systeme mit der Such-API erweitern
======================================================

Einführung
============

Fess kann nicht nur als eigenständiges Suchsystem eingesetzt werden, sondern auch als "Such-Microservice", der bestehenden Geschäftssystemen Suchfunktionen bereitstellt.

In diesem Artikel werden konkrete Muster für die Integration mit bestehenden Systemen unter Verwendung der Fess-API vorgestellt.
Es werden praxisnahe Integrationsszenarien behandelt, wie z. B. die Einbettung einer Kundendokumentensuche in ein CRM, der Aufbau eines FAQ-Such-Widgets und die Erstellung eines Dokumentenportals.

Zielgruppe
==========

- Personen, die bestehenden Geschäftssystemen Suchfunktionen hinzufügen möchten
- Personen, die sich für Systemintegration mit der Fess-API interessieren
- Personen mit Grundkenntnissen in der Webanwendungsentwicklung

Überblick über die Fess-API
===============================

Im Folgenden finden Sie eine Zusammenfassung der wichtigsten von Fess bereitgestellten APIs.

.. list-table:: Fess-API-Uebersicht
   :header-rows: 1
   :widths: 25 45 30

   * - API
     - Verwendungszweck
     - Endpunkt
   * - Such-API
     - Volltextsuche von Dokumenten
     - ``/api/v1/documents``
   * - Label-API
     - Abruf verfügbarer Labels
     - ``/api/v1/labels``
   * - Suggest-API
     - Abruf von Autovervollständigungs-Kandidaten
     - ``/api/v1/suggest-words``
   * - Beliebte-Wörter-API
     - Abruf beliebter Suchbegriffe
     - ``/api/v1/popular-words``
   * - Health-API
     - Prüfung des Systemstatus
     - ``/api/v1/health``
   * - Admin-API
     - Konfigurationsoperationen (CRUD)
     - ``/api/admin/*``

Zugriffstoken
----------------

Bei der Nutzung der API wird die Authentifizierung über Zugriffstoken empfohlen.

1. Erstellen Sie unter [System] > [Zugriffstoken] in der Verwaltungsoberfläche ein Zugriffstoken
2. Fügen Sie das Token in den Header der API-Anfrage ein

::

    Authorization: Bearer {Zugriffstoken}

Token können Rollen zugewiesen werden, und die rollenbasierte Steuerung der Suchergebnisse wird auch auf Suchen angewendet, die über die API ausgeführt werden.

Muster 1: Suchintegration in ein CRM
======================================

Szenario
--------

Fügen Sie dem CRM-System, das vom Vertriebsteam genutzt wird, eine Suchfunktion für kundenbezogene Dokumente hinzu.
Ermöglichen Sie die dokumentenübergreifende Suche nach Angeboten, Besprechungsprotokollen, Verträgen und mehr direkt aus der Kundenansicht im CRM.

Implementierungsansatz
----------------------

Betten Sie ein Such-Widget in die CRM-Kundenansicht ein.
Senden Sie den Kundennamen als Suchanfrage an die Fess-API und zeigen Sie die Ergebnisse innerhalb der CRM-Oberfläche an.

.. code-block:: javascript

    // Such-Widget innerhalb der CRM-Oberflaeche
    async function searchCustomerDocs(customerName) {
      const params = new URLSearchParams({
        q: customerName,
        num: '5',
        'fields.label': 'sales-docs'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Wichtige Punkte
----------------

- Verwenden Sie ``fields.label``, um die Ergebnisse auf vertriebsbezogene Dokumente einzugrenzen
- Verwenden Sie ``num``, um die Anzahl der angezeigten Ergebnisse zu begrenzen (angepasst an den verfügbaren Platz in der CRM-Oberfläche)
- Es ist hilfreich, nicht nur nach Kundennamen, sondern auch nach Projektnamen oder Projektnummern suchen zu können

Muster 2: FAQ-Such-Widget
============================

Szenario
--------

Fügen Sie dem internen Anfragensystem ein FAQ-Such-Widget hinzu.
Bevor Mitarbeitende eine Anfrage einreichen, sollen sie durch die Suche nach relevanten FAQs zur Selbstlösung angeregt werden.

Implementierungsansatz
----------------------

Kombinieren Sie die Suggest-API und die Such-API, um während der Eingabe in Echtzeit Vorschläge anzuzeigen.

.. code-block:: javascript

    // Vorschlaege waehrend der Eingabe
    async function getSuggestions(query) {
      const params = new URLSearchParams({ q: query, num: '5' });
      const url = `https://fess.example.com/api/v1/suggest-words?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

Die Suggest-API wird verwendet, um Kandidaten anzuzeigen, während der Benutzer Suchbegriffe eingibt.
Wenn der Benutzer einen Suchbegriff bestätigt und die Suche ausführt, werden über die Such-API detaillierte Suchergebnisse abgerufen.

Wichtige Punkte
----------------

- Da bei der Suggest-API die Echtzeitfähigkeit entscheidend ist, überprüfen Sie die Antwortgeschwindigkeit
- Verwalten Sie FAQ-Kategorien mit Labels und bieten Sie eine kategoriebasierte Filterung an
- Zeigen Sie "häufig gesuchte Begriffe" über die Beliebte-Wörter-API an, um die Benutzer bei der Suche zu unterstützen

Muster 3: Dokumentenportal
=============================

Szenario
--------

Erstellen Sie ein internes Dokumentenverwaltungsportal.
Stellen Sie eine Oberfläche bereit, die kategoriebasiertes Durchsuchen mit Volltextsuche kombiniert.

Implementierungsansatz
----------------------

Verwenden Sie die Label-API, um die Kategorieliste abzurufen, und die Such-API, um Dokumente innerhalb jeder Kategorie abzurufen.

.. code-block:: javascript

    // Abruf der Label-Liste
    async function getLabels() {
      const url = 'https://fess.example.com/api/v1/labels';
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      const data = await response.json();
      return data.data;
    }

    // Nach Label gefilterte Suche
    async function searchByLabel(query, label) {
      const params = new URLSearchParams({
        q: query || '*',
        'fields.label': label,
        num: '20',
        sort: 'last_modified.desc'
      });
      const url = `https://fess.example.com/api/v1/documents?${params}`;
      const response = await fetch(url, {
        headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
      });
      return await response.json();
    }

Wichtige Punkte
----------------

- Die Label-API ruft die Kategorieliste dynamisch ab (Hinzufügungen und Löschungen von Labels werden sofort auf API-Seite widergespiegelt)
- Verwenden Sie ``sort=last_modified.desc``, um die neuesten Dokumente oben anzuzeigen
- Das Durchsuchen ohne Suchbegriffe (Abruf aller Einträge) ist mit ``q=*`` ebenfalls möglich

Muster 4: Content-Indexing-API
=================================

Szenario
--------

Registrieren Sie Daten, die von externen Systemen generiert werden (Protokolle, Berichte, Chatbot-Antwortaufzeichnungen usw.), im Fess-Index, um sie durchsuchbar zu machen.

Implementierungsansatz
----------------------

Mit der Fess-Admin-API können Dokumente von externen Quellen im Index registriert werden.

Verwenden Sie den Dokument-Endpunkt der Admin-API, um Informationen wie Titel, URL und Textinhalt per POST-Anfrage zu senden.

Wichtige Punkte
----------------

- Effektiv für die Integration von Datenquellen, die nicht durch Crawling erfasst werden können
- Stapelverarbeitung kann ebenfalls verwendet werden, um mehrere Dokumente auf einmal zu registrieren
- Setzen Sie die Zugriffstoken-Berechtigungen angemessen und beschränken Sie die Schreibberechtigungen

Best Practices für die API-Integration
=========================================

Fehlerbehandlung
------------------

Bei der API-Integration ist eine Fehlerbehandlung wichtig, die Netzwerkausfälle und Wartungsarbeiten am Fess-Server berücksichtigt.

- Timeout-Einstellungen: Setzen Sie angemessene Timeouts für Such-API-Aufrufe
- Retry-Logik: Implementieren Sie Wiederholungsversuche für vorübergehende Fehler (maximal ca. 3 Wiederholungen)
- Fallback: Stellen Sie eine alternative Anzeige bereit, wenn Fess nicht antwortet (z. B. "Der Suchdienst ist derzeit nicht verfügbar")

Leistungsaspekte
--------------------

- Antwort-Caching: Ergebnisse für dieselbe Abfrage kurzzeitig zwischenspeichern
- Begrenzung der Ergebnisanzahl: Nur die benötigte Anzahl von Ergebnissen abrufen (``num``-Parameter)
- Feldspezifikation: Nur die benötigten Felder abrufen, um die Antwortgröße zu reduzieren

Sicherheit
------------

- Verwendung von HTTPS-Kommunikation
- Rotation der Zugriffstoken
- Token-Berechtigungen auf das Minimum beschränken (z. B. nur Lesezugriff)
- CORS angemessen konfigurieren

Zusammenfassung
================

In diesem Artikel wurden Integrationsmuster mit bestehenden Systemen unter Verwendung der Fess-API vorgestellt.

- **CRM-Integration**: Suche nach zugehörigen Dokumenten aus der Kundenansicht
- **FAQ-Widget**: Echtzeit-Kandidatenanzeige mit Suggest + Suche
- **Dokumentenportal**: Kategorie-Browsing über die Label-API
- **Content-Indexing**: Registrierung externer Daten über die API

Die Fess-API ist REST-basiert und einfach gehalten, was die Integration mit verschiedenen Systemen erleichtert.
Die Möglichkeit, bestehenden Systemen nachträglich Suchfunktionen hinzuzufügen, ist eine der größten Stärken von Fess.

Im nächsten Artikel werden Szenarien behandelt, in denen SaaS- und Datenbankdaten durchsuchbar gemacht werden.

Referenzen
==========

- `Fess Such-API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__

- `Fess Admin-API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__
