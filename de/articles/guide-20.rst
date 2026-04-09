============================================================
Teil 20: KI-Agenten mit der Suche verbinden -- Fess über MCP-Server in externe KI-Tools integrieren
============================================================

Einführung
==========

Im vorherigen Artikel haben wir einen KI-Assistenten mit dem integrierten KI-Suchmodus von Fess erstellt.
Doch das ist nicht die einzige Möglichkeit, KI zu nutzen.
Es gibt eine Methode, Fess als „Suchwerkzeug" von Claude Desktop und anderen KI-Agenten aus zu verwenden.

In diesem Artikel richten wir Fess als MCP-Server (Model Context Protocol) ein und bauen eine Umgebung auf, in der externe KI-Tools nahtlos interne Dokumente durchsuchen können.

Zielgruppe
==========

- Personen, die sich für die Integration von KI-Agenten mit Suchsystemen interessieren
- Personen, die das Konzept von MCP verstehen möchten
- Personen, die KI-Tools wie Claude Desktop im Geschäftsalltag einsetzen

Was ist MCP?
============

MCP (Model Context Protocol) ist ein Protokoll, das KI-Anwendungen den Zugriff auf externe Datenquellen und Werkzeuge ermöglicht.
Es erlaubt KI-Modellen, Operationen wie „Suchen", „Datei lesen" und „API aufrufen" auf standardisierte Weise durchzuführen.

Wenn Sie Fess als MCP-Server bereitstellen, können KI-Agenten Operationen wie „interne Dokumente durchsuchen" in einem natürlichen Kontext ausführen.

Ein Paradigmenwechsel
---------------------

Die herkömmliche Suche folgte dem Modell „ein Mensch gibt Schlüsselwörter ein und liest die Ergebnisse".
Mit MCP wird ein neues Modell verwirklicht: „Ein KI-Agent sucht autonom, interpretiert die Ergebnisse und integriert sie in seine Antworten."

Dies ist ein Wandel von „Menschen suchen" zu „KI sucht im Auftrag von Menschen".

Aufbau des Fess-MCP-Servers
=============================

Installation des Plugins
------------------------

Die MCP-Server-Funktionalität von Fess wird als Webapp-Plugin bereitgestellt.

1. Wählen Sie in der Administrationsoberfläche [System] > [Plugins]
2. Installieren Sie ``fess-webapp-mcp``
3. Starten Sie Fess neu

Vom MCP-Server bereitgestellte Funktionen
-------------------------------------------

Der Fess-MCP-Server stellt KI-Agenten die folgenden Funktionen zur Verfügung.

**Tools**

- **search**: Volltextsuche in internen Dokumenten
- **get_index_stats**: Abruf der Dokumentenanzahl im Index und JVM-Speicherinformationen

KI-Agenten können diese Tools aufrufen, um den Fess-Index zu durchsuchen oder den Systemstatus zu überprüfen.

**Resources**

- **fess://index/stats**: Indexstatistiken (Dokumentenanzahl, Konfigurationsinformationen, JVM-Speicher)

**Prompts**

- **basic_search**: Generierung grundlegender Suchabfragen
- **advanced_search**: Generierung detaillierter Suchabfragen einschließlich Sortierung und Ergebnisanzahl

Integration mit Claude Desktop
================================

Konfiguration von Claude Desktop
----------------------------------

Um den Fess-MCP-Server mit Claude Desktop zu verbinden, fügen Sie die MCP-Server-Informationen zur Konfigurationsdatei von Claude Desktop hinzu.

Fügen Sie die folgende Konfiguration zur Konfigurationsdatei (claude_desktop_config.json) hinzu.

.. code-block:: json

    {
      "mcpServers": {
        "fess": {
          "url": "http://localhost:8080/mcp"
        }
      }
    }

Anwendungsbeispiele
--------------------

Sobald Fess als MCP-Server in Claude Desktop verbunden ist, werden Interaktionen wie die folgenden möglich.

**Beispiel 1: Suche in internen Dokumenten**

    Benutzer: „Bitte informieren Sie mich über das Verfahren zur Reisekostenabrechnung."

    Claude: (Ruft das Fess-Suchwerkzeug auf)
    Ich habe die internen Dokumente zur Reisekostenabrechnung durchsucht.
    Das Verfahren zur Reisekostenabrechnung ist wie folgt:
    1. Erstellen Sie einen Reisebericht...
    [Aus dem Reisekostenabrechnungshandbuch (portal/manual/travel-expense.html)]

**Beispiel 2: Dokumentenübergreifende Recherche**

    Benutzer: „Bitte fassen Sie die Passwortbestimmungen in unserer Sicherheitsrichtlinie zusammen."

    Claude: (Sucht in Fess nach „Passwort Sicherheitsrichtlinie" und integriert mehrere Ergebnisse)
    Die Passwortbestimmungen sind in den folgenden Dokumenten dokumentiert:
    - Grundlegende Informationssicherheitsrichtlinie: Passwörter müssen mindestens 12 Zeichen lang sein...
    - Kontoverwaltungsvorschriften: Müssen alle 90 Tage geändert werden...
    - Fernzugriffsvorschriften: Multi-Faktor-Authentifizierung ist Pflicht...

KI-Agenten interpretieren die Suchergebnisse und generieren Antworten, die Informationen aus mehreren Dokumenten zusammenführen.

Integration mit anderen KI-Tools
==================================

Da MCP ein Standardprotokoll ist, kann Fess auch von anderen MCP-kompatiblen KI-Tools als Claude Desktop verwendet werden.

Nutzung durch eigene KI-Agenten
---------------------------------

Es ist auch möglich, sich über das MCP-Protokoll von selbst entwickelten KI-Agenten mit Fess zu verbinden.
Sie können die Suchfunktionalität von Fess programmatisch über MCP-Client-Bibliotheken aufrufen.

Sicherheitsaspekte
===================

Im Folgenden finden Sie Sicherheitshinweise für die Bereitstellung des MCP-Servers.

Zugriffskontrolle
------------------

- Beschränken Sie den Zugriff auf den MCP-Server auf vertrauenswürdige Clients
- Einschränkungen auf Netzwerkebene (Firewall, VPN)
- Authentifizierung über API-Token

Berechtigungskontrolle für Suchergebnisse
-------------------------------------------

Die rollenbasierte Suche in Fess (behandelt in Teil 5) gilt auch für Suchen über MCP.
Indem Sie API-Token mit Rollen verknüpfen, können Sie den Umfang der Dokumente steuern, auf die KI-Agenten zugreifen können.

Umgang mit Daten
-----------------

Bei der Integration mit cloudbasierten KI-Diensten beachten Sie bitte, dass Suchergebnistexte extern übertragen werden.
Wenn hochvertrauliche Dokumente enthalten sind, sollten Sie die Kombination mit einem lokalen LLM (Ollama) oder die Filterung von Suchergebnissen in Betracht ziehen.

Zusammenfassung
================

In diesem Artikel haben wir erläutert, wie Sie Fess als MCP-Server bereitstellen und mit KI-Agenten integrieren.

- Das Konzept des MCP-Protokolls und das Paradigma „KI sucht"
- Installation und Konfiguration des fess-webapp-mcp-Plugins
- Beispiele für die Integration mit Claude Desktop
- Sicherheitsaspekte (Zugriffskontrolle, Berechtigungen, Umgang mit Daten)

Indem KI-Agenten direkt auf internes Wissen zugreifen können, erweitern sich die Möglichkeiten der Wissensnutzung erheblich.

Im nächsten Artikel behandeln wir die multimodale Suche.

Referenzen
==========

- `Fess MCP Server <https://github.com/codelibs/fess-webapp-mcp>`__

- `Model Context Protocol <https://modelcontextprotocol.io/>`__
