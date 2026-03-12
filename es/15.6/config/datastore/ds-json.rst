==================================
Conector JSON
==================================

Descripcion general
===================

El conector JSON proporciona la funcionalidad para obtener datos de archivos JSON o APIs JSON
y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-json``.

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere acceso a archivos JSON o APIs
3. Es necesario comprender la estructura del JSON

Instalacion del plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # Colocar
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Instalar desde la pantalla de administracion

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Configuracion
=============

Configure desde la pantalla de administracion en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuracion basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo
   * - Nombre
     - Products JSON
   * - Handler
     - JsonDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
---------------------------

Archivo local:

::

    file_path=/path/to/data.json
    encoding=UTF-8
    json_path=$

Archivo HTTP:

::

    file_path=https://api.example.com/products.json
    encoding=UTF-8
    json_path=$.data

API REST (con autenticacion):

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=your_api_token_here

Multiples archivos:

::

    file_path=/path/to/data1.json,https://api.example.com/data2.json
    encoding=UTF-8
    json_path=$

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``file_path``
     - Si
     - Ruta del archivo JSON o URL de API (multiples separados por comas)
   * - ``encoding``
     - No
     - Codificacion de caracteres (predeterminado: UTF-8)
   * - ``json_path``
     - No
     - Ruta de extraccion JSONPath (predeterminado: ``$``)
   * - ``http_method``
     - No
     - Metodo HTTP (GET, POST, etc., predeterminado: GET)
   * - ``auth_type``
     - No
     - Tipo de autenticacion (bearer, basic)
   * - ``auth_token``
     - No
     - Token de autenticacion (para autenticacion bearer)
   * - ``auth_username``
     - No
     - Nombre de usuario (para autenticacion basic)
   * - ``auth_password``
     - No
     - Contrasena (para autenticacion basic)
   * - ``http_headers``
     - No
     - Headers HTTP personalizados (formato JSON)

Configuracion de scripts
------------------------

Objeto JSON simple:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=data.price
    category=data.category

Objeto JSON anidado:

::

    url="https://example.com/product/" + data.id
    title=data.product.name
    content=data.product.description
    price=data.product.pricing.amount
    author=data.product.author.name

Procesamiento de elementos de array:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.body
    tags=data.tags.join(", ")
    categories=data.categories[0].name

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``data.<nombre_campo>`` - Campo del objeto JSON
- ``data.<padre>.<hijo>`` - Objeto anidado
- ``data.<array>[<indice>]`` - Elemento de array
- ``data.<array>.<metodo>`` - Metodos de array (join, length, etc.)

Detalles del formato JSON
=========================

Array simple
------------

::

    [
      {
        "id": 1,
        "name": "Product A",
        "description": "Description A",
        "price": 1000
      },
      {
        "id": 2,
        "name": "Product B",
        "description": "Description B",
        "price": 2000
      }
    ]

Parametros:

::

    json_path=$

Estructura anidada
------------------

::

    {
      "data": {
        "products": [
          {
            "id": 1,
            "name": "Product A",
            "details": {
              "description": "Description A",
              "price": 1000,
              "category": {
                "id": 10,
                "name": "Electronics"
              }
            }
          }
        ]
      }
    }

Parametros:

::

    json_path=$.data.products

Script:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.details.description
    price=data.details.price
    category=data.details.category.name

Array complejo
--------------

::

    {
      "articles": [
        {
          "id": 1,
          "title": "Article 1",
          "content": "Content 1",
          "tags": ["tag1", "tag2", "tag3"],
          "author": {
            "name": "John Doe",
            "email": "john@example.com"
          }
        }
      ]
    }

Parametros:

::

    json_path=$.articles

Script:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    author=data.author.name
    tags=data.tags.join(", ")

Uso de JSONPath
===============

Que es JSONPath
---------------

JSONPath es un lenguaje de consulta para especificar elementos dentro de JSON.
Es equivalente a XPath para XML.

Sintaxis basica
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Sintaxis
     - Descripcion
   * - ``$``
     - Elemento raiz
   * - ``$.field``
     - Campo de nivel superior
   * - ``$.parent.child``
     - Campo anidado
   * - ``$.array[0]``
     - Primer elemento del array
   * - ``$.array[*]``
     - Todos los elementos del array
   * - ``$..field``
     - Busqueda recursiva

Ejemplos de JSONPath
--------------------

Todos los elementos (raiz):

::

    json_path=$

Array especifico:

::

    json_path=$.data.items

Array anidado:

::

    json_path=$.response.results.products

Busqueda recursiva:

::

    json_path=$..products

Ejemplos de uso
===============

API de catalogo de productos
----------------------------

Respuesta de API:

::

    {
      "status": "success",
      "data": {
        "products": [
          {
            "product_id": "P001",
            "name": "Laptop",
            "description": "Laptop de alto rendimiento",
            "price": 120000,
            "category": "Computadoras",
            "in_stock": true
          }
        ]
      }
    }

Parametros:

::

    file_path=https://api.example.com/products
    encoding=UTF-8
    json_path=$.data.products

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Precio: " + data.price
    digest=data.category
    price=data.price

API de articulos de blog
------------------------

Respuesta de API:

::

    {
      "posts": [
        {
          "id": 1,
          "title": "Titulo del articulo",
          "body": "Cuerpo del articulo...",
          "author": {
            "name": "Juan Garcia",
            "email": "juan@example.com"
          },
          "tags": ["tecnologia", "programacion"],
          "published_at": "2024-01-15T10:00:00Z"
        }
      ]
    }

Parametros:

::

    file_path=https://blog.example.com/api/posts
    encoding=UTF-8
    json_path=$.posts

Script:

::

    url="https://blog.example.com/post/" + data.id
    title=data.title
    content=data.body
    author=data.author.name
    tags=data.tags.join(", ")
    created=data.published_at

API con autenticacion Bearer
----------------------------

Parametros:

::

    file_path=https://api.example.com/v1/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    auth_type=bearer
    auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.description

API con autenticacion Basic
---------------------------

Parametros:

::

    file_path=https://api.example.com/data
    encoding=UTF-8
    json_path=$.data
    http_method=GET
    auth_type=basic
    auth_username=apiuser
    auth_password=password123

Script:

::

    url="https://example.com/data/" + data.id
    title=data.name
    content=data.content

Uso de headers personalizados
-----------------------------

Parametros:

::

    file_path=https://api.example.com/items
    encoding=UTF-8
    json_path=$.items
    http_method=GET
    http_headers={"X-API-Key":"your-api-key","Accept":"application/json"}

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Integracion de multiples archivos JSON
--------------------------------------

Parametros:

::

    file_path=/var/data/data1.json,/var/data/data2.json,https://api.example.com/data3.json
    encoding=UTF-8
    json_path=$.items

Script:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Solicitud POST
--------------

Parametros:

::

    file_path=https://api.example.com/search
    encoding=UTF-8
    json_path=$.results
    http_method=POST
    http_headers={"Content-Type":"application/json"}
    post_body={"query":"search term","limit":100}

Script:

::

    url="https://example.com/result/" + data.id
    title=data.title
    content=data.content

Solucion de problemas
=====================

Archivo no encontrado
---------------------

**Sintoma**: ``FileNotFoundException`` o ``404 Not Found``

**Verificaciones**:

1. Verificar que la ruta del archivo o URL sea correcta
2. Confirmar que el archivo existe
3. Para URLs, confirmar que la API este funcionando
4. Verificar la conexion de red

Error de parseo JSON
--------------------

**Sintoma**: ``JsonParseException`` o ``Unexpected character``

**Verificaciones**:

1. Verificar que el archivo JSON tenga formato correcto:

   ::

       # Validar JSON
       cat data.json | jq .

2. Verificar que la codificacion de caracteres sea correcta
3. Verificar que no haya caracteres o saltos de linea invalidos
4. Verificar que no contenga comentarios (JSON estandar no permite comentarios)

Error de JSONPath
-----------------

**Sintoma**: No se obtienen datos o resultado vacio

**Verificaciones**:

1. Verificar que la sintaxis JSONPath sea correcta
2. Confirmar que el elemento objetivo existe
3. Validar JSONPath con herramientas de prueba:

   ::

       # Verificar usando jq
       cat data.json | jq '$.data.products'

4. Verificar que la ruta apunte a la jerarquia correcta

Error de autenticacion
----------------------

**Sintoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verificaciones**:

1. Verificar que el tipo de autenticacion sea correcto (bearer, basic)
2. Verificar que el token o nombre de usuario/contrasena sean correctos
3. Verificar la fecha de expiracion del token
4. Verificar la configuracion de permisos de la API

No se obtienen datos
--------------------

**Sintoma**: El crawl tiene exito pero el conteo es 0

**Verificaciones**:

1. Verificar que JSONPath apunte al elemento correcto
2. Verificar la estructura JSON
3. Verificar que la configuracion del script sea correcta
4. Verificar que los nombres de campo sean correctos (incluyendo mayusculas/minusculas)
5. Revisar los mensajes de error en el log

Procesamiento de arrays
-----------------------

Cuando JSON es un array:

::

    [
      {"id": 1, "name": "Item 1"},
      {"id": 2, "name": "Item 2"}
    ]

Parametros:

::

    json_path=$

Cuando JSON es un objeto que contiene un array:

::

    {
      "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"}
      ]
    }

Parametros:

::

    json_path=$.items

Archivo JSON grande
-------------------

**Sintoma**: Memoria insuficiente o timeout

**Solucion**:

1. Dividir el archivo JSON en varios
2. Extraer solo las partes necesarias con JSONPath
3. Para APIs, usar paginacion
4. Aumentar el tamano del heap de |Fess|

Limite de tasa de API
---------------------

**Sintoma**: ``429 Too Many Requests``

**Solucion**:

1. Aumentar el intervalo de crawl
2. Verificar el limite de tasa de la API
3. Usar multiples API keys para balancear la carga

Ejemplos avanzados de scripts
=============================

Procesamiento condicional
-------------------------

::

    if (data.status == "published" && data.price > 1000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Concatenacion de arrays
-----------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.map(function(c) { return c.name; }).join(", ")

Configuracion de valores predeterminados
----------------------------------------

::

    url="https://example.com/item/" + data.id
    title=data.title || "Sin titulo"
    content=data.description || data.summary || "Sin descripcion"
    price=data.price || 0

Formato de fecha
----------------

::

    url="https://example.com/post/" + data.id
    title=data.title
    content=data.body
    created=data.created_at
    last_modified=data.updated_at

Procesamiento de numeros
------------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseFloat(data.price)
    stock=parseInt(data.stock_quantity)

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
