==============================
Inicio rápido de la API
==============================

Esta página proporciona una guía práctica para comenzar a utilizar rápidamente la API (v2) de |Fess|.

Comience la API en 5 minutos
============================

Requisitos previos
------------------

- |Fess| está en ejecución (accesible en http://localhost:8080/)

Pruebe la API de búsqueda
--------------------------

El endpoint de búsqueda v2 es ``GET /api/v2/search``.

**Ejemplos de comandos curl:**

.. code-block:: bash

    # Búsqueda básica
    curl "http://localhost:8080/api/v2/search?q=fess"

    # Obtener 20 resultados de búsqueda (num es el tamaño de página; el valor predeterminado es 10)
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # Omitir los primeros 20 resultados (start es la posición inicial basada en 0)
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # Búsqueda con filtro de etiquetas
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # Búsqueda con facetas (agregaciones)
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # Búsqueda en japonés (codificada en URL)
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**Ejemplo de respuesta (formateada):**

La respuesta de v2 se devuelve en el sobre ``response``.

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
            "title": "Fess - Servidor de búsqueda de texto completo de código abierto",
            "url": "https://fess.codelibs.org/ja/",
            "content_description": "<strong>Fess</strong> es fácil de implementar...",
            "host": "fess.codelibs.org",
            "mimetype": "text/html"
          }
        ]
      }
    }

.. note::

   El ejemplo anterior es representativo. Los campos de documento incluidos en ``data`` dependen
   de la configuración del servidor (la lista de campos de respuesta permitidos). Para la lista
   completa de parámetros de solicitud y campos de respuesta disponibles, consulte :doc:`api-search`.
   Para el sobre de respuesta común, el modelo de error y CSRF, consulte :doc:`api-overview`.

Pruebe la API de sugerencias
-----------------------------

El endpoint de sugerencias es ``GET /api/v2/suggest-words``.

.. code-block:: bash

    # Obtener sugerencias
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**Ejemplo de respuesta (formateada):**

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

Pruebe la API de etiquetas
---------------------------

.. code-block:: bash

    # Obtener la lista de etiquetas disponibles
    curl "http://localhost:8080/api/v2/labels"

Pruebe la API de verificación de estado
-----------------------------------------

El endpoint de verificación de estado es ``GET /api/v2/health``.

.. code-block:: bash

    # Verificar el estado del servidor (clúster del motor de búsqueda)
    curl "http://localhost:8080/api/v2/health"

**Ejemplo de respuesta (formateada):**

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

Uso con Postman
===============

La API de |Fess| se puede utilizar fácilmente con Postman.

Configuración de la colección
------------------------------

1. Abra Postman y cree una nueva colección
2. Agregue las siguientes solicitudes:

**API de búsqueda:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query Parameters:
  - ``q``: Palabra clave de búsqueda
  - ``num``: Número de resultados (opcional)
  - ``start``: Posición inicial (opcional)

**API de sugerencias:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query Parameters:
  - ``q``: Cadena de entrada

**API de etiquetas:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

Variables de entorno
--------------------

Recomendamos usar variables de entorno de Postman para gestionar las URL del servidor.

1. Cree un nuevo entorno en "Environments"
2. Agregue la variable: ``fess_url`` = ``http://localhost:8080``
3. Cambie la URL de la solicitud a ``{{fess_url}}/api/v2/search``

Ejemplos de código por lenguaje de programación
================================================

Todos los ejemplos llaman a ``GET /api/v2/search`` y hacen referencia al sobre ``response``.

Python
------

.. code-block:: python

    import requests

    # URL del servidor Fess
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Llamar a la API de búsqueda de Fess"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # Ejemplo de uso
    results = search("Fess búsqueda")
    print(f"Número de resultados: {results['response']['record_count']}")
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

    // Ejemplo de uso
    search('Fess búsqueda').then(results => {
      console.log(`Número de resultados: ${results.response.record_count}`);
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
            String result = client.search("Fess búsqueda");
            System.out.println(result);
        }
    }

Tabla de compatibilidad de versiones de la API
===============================================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Versión de Fess
     - Versión de API
     - Notas
   * - 15.x
     - v2
     - Última versión. Soporte completo de funciones
   * - 14.x
     - v1
     - Solo soporte de la API antigua
   * - 13.x
     - v1
     - Soporte de la API básica

.. note::

   En |Fess| 15.8, la API de búsqueda JSON y la API de chat de ``/api/v1`` han sido eliminadas.
   Los clientes que utilizaban ``/api/v1`` deben migrar a ``/api/v2``.
   Para diferencias detalladas entre versiones, consulte las `Notas de la versión <https://github.com/codelibs/fess/releases>`__.

Solución de problemas
=====================

La API no funciona
------------------

1. **Verifique que |Fess| esté en ejecución**

   Compruebe que puede acceder a http://localhost:8080/.

2. **Verifique que el endpoint sea v2**

   Compruebe que la ruta de la solicitud sea ``/api/v2/...``.
   Los endpoints del antiguo ``/api/v1`` han sido eliminados.

3. **Cuando se requiere autenticación**

   Para los endpoints que requieren autenticación, consulte :doc:`api-auth`.

Próximos pasos
==============

- :doc:`api-overview` - Especificaciones comunes de la API (sobre de respuesta, modelo de error, autenticación/CSRF)
- :doc:`api-search` - Detalles de la API de búsqueda
- :doc:`api-suggest` - Detalles de la API de sugerencias
- :doc:`api-label` - Detalles de la API de etiquetas
- :doc:`api-health` - Detalles de la API de verificación de estado
- :doc:`admin/index` - Uso de la API de administración
