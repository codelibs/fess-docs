===================
API-Schnellstart
===================

Diese Seite bietet eine praktische Anleitung, um schnell mit der |Fess|-API zu beginnen.

In 5 Minuten starten
=====================

Voraussetzungen
---------------

- |Fess| läuft (erreichbar unter http://localhost:8080/)
- JSON-Antwort ist im Admin-Panel unter System > Allgemein aktiviert

Die Such-API ausprobieren
-------------------------

**curl-Befehlsbeispiele:**

.. code-block:: bash

    # Einfache Suche
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # 20 Suchergebnisse abrufen
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # Seite 2 abrufen (ab Ergebnis 21)
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # Suche mit Label-Filter
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # Suche mit Facetten (Aggregationen)
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # Suche mit Sonderzeichen (URL-kodiert)
    curl "http://localhost:8080/api/v1/documents?q=search%20engine"

**Beispielantwort (formatiert):**

.. code-block:: json

    {
      "q": "fess",
      "exec_time": 0.15,
      "record_count": 125,
      "page_size": 20,
      "page_number": 1,
      "data": [
        {
          "title": "Fess - Open Source Enterprise Search Server",
          "url": "https://fess.codelibs.org/",
          "content_description": "<strong>Fess</strong> is an easy to deploy...",
          "host": "fess.codelibs.org",
          "mimetype": "text/html"
        }
      ]
    }

Die Suggest-API ausprobieren
-----------------------------

.. code-block:: bash

    # Vorschläge abrufen
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # Beispielantwort
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

Die Label-API ausprobieren
--------------------------

.. code-block:: bash

    # Verfügbare Labels abrufen
    curl "http://localhost:8080/api/v1/labels"

Die Health-Check-API ausprobieren
---------------------------------

.. code-block:: bash

    # Serverstatus prüfen
    curl "http://localhost:8080/api/v1/health"

    # Beispielantwort
    # {"data":{"status":"green","cluster_name":"fess"}}

Postman verwenden
=================

Die |Fess|-API kann einfach mit Postman verwendet werden.

Collection-Einrichtung
----------------------

1. Öffnen Sie Postman und erstellen Sie eine neue Collection
2. Fügen Sie die folgenden Requests hinzu:

**Such-API:**

- Methode: ``GET``
- URL: ``http://localhost:8080/api/v1/documents``
- Query-Parameter:
  - ``q``: Suchbegriff
  - ``num``: Anzahl der Ergebnisse (optional)
  - ``start``: Startposition (optional)

**Suggest-API:**

- Methode: ``GET``
- URL: ``http://localhost:8080/api/v1/suggest``
- Query-Parameter:
  - ``q``: Eingabestring

**Label-API:**

- Methode: ``GET``
- URL: ``http://localhost:8080/api/v1/labels``

Umgebungsvariablen
------------------

Wir empfehlen, Postman-Umgebungsvariablen zur Verwaltung von Server-URLs zu verwenden.

1. Erstellen Sie eine neue Umgebung unter "Environments"
2. Variable hinzufügen: ``fess_url`` = ``http://localhost:8080``
3. Request-URL ändern zu ``{{fess_url}}/api/v1/documents``

Codebeispiele nach Programmiersprache
=====================================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # Fess-Server-URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess-Such-API aufrufen"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # Anwendungsbeispiel
    results = search("enterprise search")
    print(f"Gesamttreffer: {results['record_count']}")
    for doc in results['data']:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v1/documents?${params}`);
      return response.json();
    }

    // Anwendungsbeispiel
    search('enterprise search').then(results => {
      console.log(`Gesamttreffer: ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

JavaScript (Browser)
--------------------

.. code-block:: javascript

    // JSONP verwenden
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // Callback-Funktion
    function handleResults(results) {
      console.log(`Gesamttreffer: ${results.record_count}`);
    }

    // Anwendungsbeispiel
    search('Fess', 'handleResults');

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
                .uri(URI.create(FESS_URL + "/api/v1/documents?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("enterprise search");
            System.out.println(result);
        }
    }

API-Versionskompatibilität
==========================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess-Version
     - API-Version
     - Hinweise
   * - 15.x
     - v1
     - Neueste Version. Vollständige Funktionsunterstützung
   * - 14.x
     - v1
     - Ähnliche API. Einige Parameterunterschiede möglich
   * - 13.x
     - v1
     - Grundlegende API-Unterstützung

.. note::

   Die API-Kompatibilität wird beibehalten, aber neue Funktionen sind nur in der neuesten Version verfügbar.
   Für detaillierte Unterschiede zwischen Versionen siehe die `Release-Notes <https://github.com/codelibs/fess/releases>`__.

Fehlerbehebung
==============

API funktioniert nicht
----------------------

1. **Überprüfen, ob JSON-Antwort aktiviert ist**

   Stellen Sie sicher, dass "JSON-Antwort" im Admin-Panel unter System > Allgemein aktiviert ist.

2. **CORS-Fehler vom Browser**

   Wenn Sie CORS-Fehler beim Zugriff vom Browser erhalten, verwenden Sie JSONP oder
   konfigurieren Sie die CORS-Einstellungen auf dem Server.

   JSONP-Beispiel:

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **Authentifizierung erforderlich**

   Wenn Zugriffstoken konfiguriert sind, fügen Sie diese im Request-Header hinzu:

   .. code-block:: bash

       curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
            "http://localhost:8080/api/v1/documents?q=fess"

Nächste Schritte
================

- :doc:`api-search` - Details zur Such-API
- :doc:`api-suggest` - Details zur Suggest-API
- :doc:`admin/index` - Verwendung der Admin-API
