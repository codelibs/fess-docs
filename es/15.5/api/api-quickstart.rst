===================
Inicio rapido de API
===================

Esta pagina proporciona una guia practica para comenzar a utilizar rapidamente la API de |Fess|.

Comience en 5 minutos
=====================

Requisitos previos
------------------

- |Fess| esta en ejecucion (accesible en http://localhost:8080/)
- La respuesta JSON esta habilitada en Panel de administracion > Sistema > General

Pruebe la API de busqueda
-------------------------

**Ejemplos de comandos curl:**

.. code-block:: bash

    # Busqueda basica
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # Obtener 20 resultados de busqueda
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # Obtener la pagina 2 (comenzando desde el resultado 21)
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # Busqueda con filtro de etiquetas
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # Busqueda con facetas (agregaciones)
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # Busqueda con caracteres especiales (codificados en URL)
    curl "http://localhost:8080/api/v1/documents?q=search%20engine"

**Ejemplo de respuesta (formateada):**

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

Pruebe la API de sugerencias
-----------------------------

.. code-block:: bash

    # Obtener sugerencias
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # Ejemplo de respuesta
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

Pruebe la API de etiquetas
---------------------------

.. code-block:: bash

    # Obtener etiquetas disponibles
    curl "http://localhost:8080/api/v1/labels"

Pruebe la API de verificacion de estado
----------------------------------------

.. code-block:: bash

    # Verificar el estado del servidor
    curl "http://localhost:8080/api/v1/health"

    # Ejemplo de respuesta
    # {"data":{"status":"green","cluster_name":"fess"}}

Uso con Postman
===============

La API de |Fess| se puede utilizar facilmente con Postman.

Configuracion de la coleccion
-----------------------------

1. Abra Postman y cree una nueva coleccion
2. Agregue las siguientes solicitudes:

**API de busqueda:**

- Metodo: ``GET``
- URL: ``http://localhost:8080/api/v1/documents``
- Parametros de consulta:
  - ``q``: Palabra clave de busqueda
  - ``num``: Numero de resultados (opcional)
  - ``start``: Posicion inicial (opcional)

**API de sugerencias:**

- Metodo: ``GET``
- URL: ``http://localhost:8080/api/v1/suggest``
- Parametros de consulta:
  - ``q``: Cadena de entrada

**API de etiquetas:**

- Metodo: ``GET``
- URL: ``http://localhost:8080/api/v1/labels``

Variables de entorno
--------------------

Recomendamos usar variables de entorno de Postman para gestionar las URL del servidor.

1. Cree un nuevo entorno en "Environments"
2. Agregue la variable: ``fess_url`` = ``http://localhost:8080``
3. Cambie la URL de la solicitud a ``{{fess_url}}/api/v1/documents``

Ejemplos de codigo por lenguaje de programacion
================================================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # URL del servidor Fess
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Llamar a la API de busqueda de Fess"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # Ejemplo de uso
    results = search("enterprise search")
    print(f"Total de resultados: {results['record_count']}")
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

    // Ejemplo de uso
    search('enterprise search').then(results => {
      console.log(`Total de resultados: ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

JavaScript (Navegador)
----------------------

.. code-block:: javascript

    // Usando JSONP
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // Funcion de callback
    function handleResults(results) {
      console.log(`Total de resultados: ${results.record_count}`);
    }

    // Ejemplo de uso
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

Compatibilidad de versiones de API
====================================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Version de Fess
     - Version de API
     - Notas
   * - 15.x
     - v1
     - Ultima version. Soporte completo de funciones
   * - 14.x
     - v1
     - API similar. Pueden existir algunas diferencias en los parametros
   * - 13.x
     - v1
     - Soporte basico de API

.. note::

   Se mantiene la compatibilidad de la API, pero las nuevas funciones solo estan disponibles en la ultima version.
   Para diferencias detalladas entre versiones, consulte las `Notas de la version <https://github.com/codelibs/fess/releases>`__.

Solucion de problemas
=====================

La API no funciona
------------------

1. **Verifique que la respuesta JSON este habilitada**

   Compruebe que "Respuesta JSON" este habilitada en Panel de administracion > Sistema > General.

2. **Errores CORS desde el navegador**

   Si obtiene errores CORS al acceder desde un navegador, use JSONP o
   configure los ajustes de CORS en el servidor.

   Ejemplo de JSONP:

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **Se requiere autenticacion**

   Si los tokens de acceso estan configurados, incluyalos en el encabezado de la solicitud:

   .. code-block:: bash

       curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
            "http://localhost:8080/api/v1/documents?q=fess"

Proximos pasos
==============

- :doc:`api-search` - Detalles de la API de busqueda
- :doc:`api-suggest` - Detalles de la API de sugerencias
- :doc:`admin/index` - Uso de la API de administracion
