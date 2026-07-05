====================
API-Schnellstart
====================

Diese Seite bietet eine praktische Anleitung, um die |Fess|-API (v2) schnell auszuprobieren.

In 5 Minuten starten
====================

Voraussetzungen
---------------

- |Fess| läuft (erreichbar unter http://localhost:8080/)

Die Such-API ausprobieren
-------------------------

Der v2-Such-Endpunkt ist ``GET /api/v2/search``.

**curl-Befehlsbeispiele:**

.. code-block:: bash

    # Einfache Suche
    curl "http://localhost:8080/api/v2/search?q=fess"

    # 20 Suchergebnisse abrufen (num ist die Seitengröße; Standard ist 10)
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # Die ersten 20 Ergebnisse überspringen (start ist die 0-basierte Startposition)
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # Suche mit Label-Filter
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # Suche mit Facetten (Aggregationen)
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # Suche mit URL-Kodierung
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**Beispielantwort (formatiert):**

v2-Antworten werden im ``response``-Envelope zurückgegeben.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fess",
        "record_count": 125,
        "page_size": 10,
        "page_number": 1,
        "data": [
          {
            "title": "Fess - オープンソース全文検索サーバー",
            "url": "https://fess.codelibs.org/ja/",
            "content_description": "<strong>Fess</strong>は簡単に構築できる...",
            "host": "fess.codelibs.org",
            "mimetype": "text/html"
          }
        ]
      }
    }

.. note::

   Das obige Beispiel ist repräsentativ. Die in ``data`` enthaltenen Dokumentfelder hängen von
   der Serverkonfiguration ab (der Allowlist für Antwortfelder). Eine vollständige Liste der
   verfügbaren Anfrageparameter und Antwortfelder finden Sie unter :doc:`api-search`. Für den
   gemeinsamen Antwort-Envelope, das Fehlermodell und CSRF siehe :doc:`api-overview`.

Die Vorschlags-API ausprobieren
---------------------------------

Der Vorschlags-Endpunkt ist ``GET /api/v2/suggest-words``.

.. code-block:: bash

    # Vorschläge abrufen
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**Beispielantwort (formatiert):**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fes",
        "suggest_words": [
          { "text": "fess", "types": ["document"] }
        ]
      }
    }

Die Label-API ausprobieren
--------------------------

.. code-block:: bash

    # Verfügbare Labels abrufen
    curl "http://localhost:8080/api/v2/labels"

Die Health-Check-API ausprobieren
----------------------------------

Der Health-Check-Endpunkt ist ``GET /api/v2/health``.

.. code-block:: bash

    # Status des Servers (Suchmaschinenclusters) prüfen
    curl "http://localhost:8080/api/v2/health"

**Beispielantwort (formatiert):**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess",
          "status": "green",
          "ping_status": 200
        }
      }
    }

Postman verwenden
=================

Die |Fess|-API kann einfach mit Postman verwendet werden.

Collection-Einrichtung
----------------------

1. Öffnen Sie Postman und erstellen Sie eine neue Collection.
2. Fügen Sie die folgenden Requests hinzu:

**Such-API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query-Parameter:
  - ``q``: Suchbegriff
  - ``num``: Anzahl der Ergebnisse (optional)
  - ``start``: Startposition (optional)

**Vorschlags-API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query-Parameter:
  - ``q``: Eingabezeichenkette

**Label-API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

Umgebungsvariablen
------------------

Es wird empfohlen, Postman-Umgebungsvariablen zur Verwaltung der Server-URL zu verwenden.

1. Erstellen Sie eine neue Umgebung unter „Environments".
2. Variable hinzufügen: ``fess_url`` = ``http://localhost:8080``
3. Request-URL ändern zu ``{{fess_url}}/api/v2/search``

Codebeispiele nach Programmiersprache
======================================

Alle folgenden Beispiele rufen ``GET /api/v2/search`` auf und greifen auf den ``response``-Envelope zu.

Python
------

.. code-block:: python

    import requests

    # Fess サーバーのURL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess検索APIを呼び出す"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # 使用例
    results = search("Fess 検索")
    print(f"ヒット件数: {results['response']['record_count']}")
    for doc in results["response"]["data"]:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v2/search?${params}`);
      return response.json();
    }

    // 使用例
    search('Fess 検索').then(results => {
      console.log(`ヒット件数: ${results.response.record_count}`);
      results.response.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

Java
----

.. code-block:: java

    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.net.URLEncoder;
    import java.nio.charset.StandardCharsets;

    public class FessApiClient {
        private static final String FESS_URL = "http://localhost:8080";
        private final HttpClient client = HttpClient.newHttpClient();

        public String search(String query) throws Exception {
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(FESS_URL + "/api/v2/search?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("Fess 検索");
            System.out.println(result);
        }
    }

API-Versionskompatibilität
===========================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess-Version
     - API-Version
     - Hinweise
   * - 15.x
     - v2
     - Neueste Version. Unterstützt alle Funktionen.
   * - 14.x
     - v1
     - Nur ältere API unterstützt.
   * - 13.x
     - v1
     - Grundlegende API-Unterstützung.

.. note::

   In |Fess| 15.8 wurden die bisherige JSON-Such-API und die Chat-API unter ``/api/v1`` abgekündigt.
   Clients, die ``/api/v1`` verwenden, sollten auf ``/api/v2`` migrieren.
   Detaillierte Unterschiede zwischen den Versionen finden Sie in den `Release-Notes <https://github.com/codelibs/fess/releases>`__.

Fehlerbehebung
==============

API funktioniert nicht
----------------------

1. **Überprüfen, ob |Fess| läuft**

   Stellen Sie sicher, dass http://localhost:8080/ erreichbar ist.

2. **Überprüfen, ob der Endpunkt v2 ist**

   Stellen Sie sicher, dass der Anfragepfad ``/api/v2/...`` lautet.
   Die alten ``/api/v1``-Endpunkte wurden abgekündigt.

3. **Wenn Authentifizierung erforderlich ist**

   Für Endpunkte, die Authentifizierung erfordern, siehe :doc:`api-auth`.

Nächste Schritte
================

- :doc:`api-overview` - Allgemeine API-Spezifikationen (Antwort-Envelope, Fehlermodell, Authentifizierung/CSRF)
- :doc:`api-search` - Details zur Such-API
- :doc:`api-suggest` - Details zur Vorschlags-API
- :doc:`api-label` - Details zur Label-API
- :doc:`api-health` - Details zur Health-Check-API
- :doc:`admin/index` - Verwendung der Verwaltungs-API
