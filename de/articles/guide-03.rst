============================================================
Teil 3: Suche in ein internes Portal einbetten -- Szenario zur Integration einer Suchfunktion in bestehende Websites
============================================================

Einleitung
==========

Im vorherigen Teil haben wir Fess mit Docker Compose gestartet und die Suche ausprobiert.
In der Praxis besteht jedoch oft nicht nur der Wunsch, die Fess-Suchoberfläche direkt zu verwenden, sondern auch die Anforderung, eine Suchfunktion in bestehende interne Websites oder Portale zu integrieren.

In diesem Artikel stellen wir drei Ansätze vor, um die Suchfunktion von Fess in eine bestehende Website einzubinden, und erläutern die jeweiligen Merkmale und Auswahlkriterien.

Zielgruppe
==========

- Personen, die eine Suchfunktion in ein internes Portal oder eine Website integrieren möchten
- Personen mit Grundkenntnissen in der Frontend-Entwicklung
- Fess muss gemäß der Anleitung aus Teil 2 bereits gestartet sein

Voraussetzungen
===============

- Die in Teil 2 eingerichtete Fess-Umgebung (Docker Compose)
- Eine Test-Webseite (auch eine lokale HTML-Datei ist möglich)

Drei Integrationsansätze
========================

Es gibt im Wesentlichen drei Methoden, um die Suchfunktion von Fess in eine bestehende Website einzubinden.

.. list-table:: Vergleich der Integrationsansätze
   :header-rows: 1
   :widths: 15 30 25 30

   * - Ansatz
     - Übersicht
     - Entwicklungsaufwand
     - Geeignete Anwendungsfälle
   * - FSS (Fess Site Search)
     - Einfaches Einbetten eines JavaScript-Tags
     - Minimal (wenige Codezeilen)
     - Wenn Sie schnell und unkompliziert eine Suche hinzufügen möchten
   * - Suchformular-Integration
     - Weiterleitung von einem HTML-Formular zu Fess
     - Gering (nur HTML-Anpassung)
     - Wenn Sie die Fess-Suchoberfläche direkt verwenden möchten
   * - Such-API-Integration
     - Aufbau einer individuellen Oberfläche über die JSON API
     - Mittel bis hoch (Frontend-Entwicklung)
     - Wenn Sie Design und Verhalten vollständig anpassen möchten

Im Folgenden erläutern wir jede Methode anhand konkreter Szenarien.

Ansatz 1: Einfache Integration mit FSS (Fess Site Search)
==========================================================

Szenario
--------

Es existiert ein internes Portalsite, und Sie haben die Berechtigung, das HTML zu bearbeiten, möchten aber größere Umbauten vermeiden.
Mit minimalen Änderungen soll es möglich sein, interne Dokumente direkt über das Portal zu durchsuchen.

Was ist FSS?
------------

Fess Site Search (FSS) ist ein Mechanismus, mit dem Sie eine Suchfunktion hinzufügen können, indem Sie lediglich einen JavaScript-Tag in eine Webseite einbetten.
Da Suchfeld und Suchergebnisanzeige vollständig in JavaScript verarbeitet werden, ist es kaum notwendig, die bestehende Seitenstruktur zu ändern.

Implementierungsschritte
------------------------

1. Aktivieren Sie den API-Zugriff in der Fess-Administrationsoberfläche.
   Aktivieren Sie unter [System] > [Allgemein] die JSON-Antwort.

2. Betten Sie den folgenden Code in die Seite ein, der Sie die Suchfunktion hinzufügen möchten.

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

An der Stelle, an der Sie den ``<fess:search>``-Tag platzieren, werden das Suchfeld und die Suchergebnisse angezeigt.

Anpassung
---------

Das Erscheinungsbild von FSS kann mit CSS angepasst werden.
Indem Sie die von Fess bereitgestellten Standardstile überschreiben, können Sie das Design an Ihre bestehende Website anpassen.

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

Ansatz 2: Einfache Umsetzung mit Suchformular-Integration
==========================================================

Szenario
--------

Das interne Portal verfügt bereits über eine Navigationsleiste im Header.
Sie möchten dort ein Suchfeld hinzufügen und bei der Suchausführung zur Fess-Suchergebnisseite weiterleiten.
Dies soll ohne JavaScript, nur mit HTML umgesetzt werden.

Implementierungsschritte
------------------------

Fügen Sie der bestehenden Navigationsleiste ein HTML-Formular wie das folgende hinzu.

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="Interne Suche..." />
      <button type="submit">Suchen</button>
    </form>

Das ist alles -- bei der Suchausführung erfolgt eine Weiterleitung zur Fess-Suchergebnisseite.
Durch Anpassung des Designs der Fess-Suchoberfläche können Sie ein einheitliches Nutzungserlebnis bieten.

Anpassung der Fess-Suchoberfläche
----------------------------------

Die Fess-Suchoberfläche besteht aus JSP-Dateien und kann auch über die Administrationsoberfläche bearbeitet werden.

1. Wählen Sie in der Administrationsoberfläche [System] > [Seitendesign]
2. Passen Sie Header, Footer, CSS und weitere Elemente an

Beispielsweise können Sie durch Angleichung des Logos an das interne Portal oder Vereinheitlichung der Farbgebung ein nahtloses Sucherlebnis für die Nutzer schaffen.

Nutzung der Pfadzuordnung
--------------------------

Die in den Suchergebnissen angezeigten URLs können in benutzerfreundlichere URLs umgewandelt werden.
Wenn die URL beim Crawling beispielsweise ``http://internal-server:8888/docs/`` lautet, kann in den Suchergebnissen stattdessen ``https://portal.example.com/docs/`` angezeigt werden.

Diese Einstellung finden Sie in der Administrationsoberfläche unter [Crawler] > [Pfadzuordnung].

Ansatz 3: Vollständige Individualisierung mit der Such-API
===========================================================

Szenario
--------

Sie möchten eine Suchfunktion in eine interne Geschäftsanwendung integrieren.
Design und Darstellung der Suchergebnisse sollen vollständig kontrolliert werden.
Frontend-Entwicklungsressourcen stehen zur Verfügung.

Grundlagen der Such-API
------------------------

Fess bietet eine JSON-basierte Such-API.

::

    GET http://localhost:8080/api/v1/documents?q=Suchbegriff

Die Antwort erfolgt im folgenden JSON-Format.

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "Dokumenttitel",
          "url": "https://example.com/doc.html",
          "content_description": "...Auszug aus dem Text mit dem Suchbegriff..."
        }
      ]
    }

Implementierungsbeispiel in JavaScript
---------------------------------------

Im Folgenden ein grundlegendes Implementierungsbeispiel mit der Such-API.

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

Zusätzliche API-Parameter
--------------------------

Die Such-API ermöglicht die Anpassung des Suchverhaltens über verschiedene Parameter.

.. list-table:: Wichtige API-Parameter
   :header-rows: 1
   :widths: 20 50 30

   * - Parameter
     - Beschreibung
     - Beispiel
   * - ``q``
     - Suchbegriff
     - ``q=Fess``
   * - ``num``
     - Anzahl der Ergebnisse pro Seite
     - ``num=20``
   * - ``start``
     - Startposition der Suchergebnisse
     - ``start=20``
   * - ``fields.label``
     - Filterung nach Label
     - ``fields.label=intranet``
   * - ``sort``
     - Sortierreihenfolge
     - ``sort=last_modified.desc``

Durch die Nutzung der API sind eine detaillierte Steuerung der Suchergebnisse wie Filterung, Sortierung und Paginierung möglich.

Welchen Ansatz sollten Sie wählen?
===================================

Die drei Ansätze werden je nach Situation ausgewählt.

**Wann Sie FSS wählen sollten**

- Die Entwicklungsressourcen sind begrenzt
- Sie möchten eine Suche mit minimalen Änderungen an der bestehenden Seite hinzufügen
- Ein standardmäßiges Erscheinungsbild der Suchfunktion ist ausreichend

**Wann Sie die Suchformular-Integration wählen sollten**

- Das Design der Fess-Suchoberfläche ist ausreichend
- Sie möchten kein JavaScript verwenden
- Es genügt, ein Suchfeld im Header oder in der Seitenleiste hinzuzufügen

**Wann Sie die Such-API wählen sollten**

- Sie möchten die Darstellung der Suchergebnisse vollständig individualisieren
- Sie möchten die Suche in eine SPA (Single Page Application) integrieren
- Sie möchten eigene Logik (Filterung, Hervorhebung usw.) auf die Suchergebnisse anwenden
- Frontend-Entwicklungsressourcen stehen zur Verfügung

Kombinationen sind möglich
--------------------------

Diese Ansätze schließen sich nicht gegenseitig aus.
Beispielsweise können Sie auf der Startseite mit FSS unkompliziert eine Suchfunktion hinzufügen und auf einer dedizierten Suchseite eine individuelle Oberfläche über die API bereitstellen -- auch eine solche Kombination ist sinnvoll.

Zusammenfassung
===============

In diesem Artikel haben wir drei Ansätze vorgestellt, um die Suchfunktion von Fess in eine bestehende Website zu integrieren.

- **FSS**: Suchfunktion durch einfaches Einbetten eines JavaScript-Tags hinzufügen
- **Suchformular-Integration**: Weiterleitung von einem HTML-Formular zur Fess-Suchoberfläche
- **Such-API**: Aufbau eines vollständig individualisierten Sucherlebnisses über die JSON API

Unabhängig vom gewählten Ansatz können Sie die vom Fess-Backend bereitgestellte Suchqualität uneingeschränkt nutzen.
Wählen Sie die optimale Methode entsprechend Ihren Anforderungen und verfügbaren Entwicklungsressourcen.

Im nächsten Teil behandeln wir das Szenario der einheitlichen Suche über mehrere Datenquellen wie Dateiserver und Cloud-Speicher.

Referenzen
==========

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `Fess Such-API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
