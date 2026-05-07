==================================
Conector JSON
==================================

Descripcion general
===================

El conector JSON proporciona la funcionalidad para obtener datos de archivos JSON
o archivos JSONL locales y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-json``.

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere acceso a los archivos JSON
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

    files=/path/to/data.json
    fileEncoding=UTF-8

Multiples archivos:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

Especificacion de directorio:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Parametro
     - Requerido
     - Descripcion
   * - ``files``
     - No
     - Ruta del archivo JSON (multiples separados por comas)
   * - ``directories``
     - No
     - Ruta del directorio que contiene archivos JSON
   * - ``fileEncoding``
     - No
     - Codificacion de caracteres (predeterminado: UTF-8)

.. warning::
   Es necesario especificar ``files`` o ``directories``.
   Si no se especifica ninguno, se producira un ``DataStoreException``.
   Si se especifican ambos, ``files`` tiene prioridad y ``directories`` se ignora.

.. note::
   Este conector solo admite archivos JSON en el sistema de archivos local. No es compatible con acceso HTTP ni funciones de autenticacion de API.

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

Formato de archivo JSON
-----------------------

El conector JSON lee archivos en formato JSONL (JSON Lines).
Es un formato en el que se escribe un objeto JSON por linea.

.. note::
   Los archivos JSON en formato de array ( ``[{...}, {...}]`` ) no se pueden leer directamente.
   Convierta al formato JSONL.

Archivo en formato JSONL:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

Ejemplos de uso
===============

Catalogo de productos
---------------------

Parametros:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

Scripts:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Precio: " + data.price + " EUR"
    digest=data.category
    price=data.price

Integracion de multiples archivos JSON
--------------------------------------

Parametros:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Scripts:

::

    url="https://example.com/item/" + data.id
    title=data.title
    content=data.content

Solucion de problemas
=====================

Archivo no encontrado
---------------------

**Sintoma**: ``FileNotFoundException``

**Verificar**:

1. Verificar que la ruta del archivo sea correcta
2. Verificar que el archivo exista
3. Verificar los permisos de lectura del archivo

Error de analisis JSON
----------------------

**Sintoma**: ``JsonParseException`` o ``Unexpected character``

**Verificar**:

1. Verificar que el archivo JSON tenga el formato correcto:

   ::

       # Validacion de JSON
       cat data.json | jq .

2. Verificar la codificacion de caracteres
3. Verificar que no haya caracteres o saltos de linea no validos
4. Verificar que no contenga comentarios (no permitidos en el estandar JSON)

No se obtienen datos
--------------------

**Sintoma**: El crawl se completa con exito pero el recuento es 0

**Verificar**:

1. Verificar la estructura JSON
2. Verificar la configuracion de scripts
3. Verificar los nombres de campo (incluyendo mayusculas y minusculas)
4. Verificar los mensajes de error en los registros

Archivos JSON grandes
---------------------

**Sintoma**: Falta de memoria o tiempo de espera agotado

**Solucion**:

1. Dividir el archivo JSON en varios archivos
2. Aumentar el tamano del heap de |Fess|

Uso avanzado de scripts
=======================

Procesamiento condicional
-------------------------

Cada campo se evalua como una expresion independiente. Para valores condicionales, utilice el operador ternario:

::

    url=data.status == "published" ? "https://example.com/product/" + data.id : null
    title=data.status == "published" ? data.name : null
    content=data.status == "published" ? data.description : null
    price=data.status == "published" ? data.price : null

Union de arrays
---------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    tags=data.tags ? data.tags.join(", ") : ""
    categories=data.categories.collect { it.name }.join(", ")

Configuracion de valores predeterminados
----------------------------------------

::

    url="https://example.com/item/" + data.id
    title=data.title ?: "Sin titulo"
    content=data.description ?: (data.summary ?: "Sin descripcion")
    price=data.price ?: 0

Formato de fechas
-----------------

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
    price=data.price as Float
    stock=data.stock_quantity as Integer

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSONPath <https://goessner.net/articles/JsonPath/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
