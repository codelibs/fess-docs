==============================
Conector JSON
==============================

Descripcion general
===================

El conector JSON proporciona la funcionalidad para obtener datos de archivos JSONL
locales (formato JSON Lines) y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-json``.

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere permiso de acceso a los archivos JSON
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

Metodo de configuracion
=======================

Configure desde la pantalla de administracion en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuracion basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo de configuracion
   * - Nombre
     - Products JSON
   * - Nombre del handler
     - JsonDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
----------------------------

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
   :widths: 20 10 70

   * - Parametro
     - Requerido
     - Descripcion
   * - ``files``
     - No
     - Ruta de los archivos JSON a procesar (se pueden especificar varios separados por comas). Solo se procesan archivos con extension ``.json`` o ``.jsonl``.
   * - ``directories``
     - No
     - Ruta de los directorios que contienen archivos JSON (se pueden especificar varios separados por comas)
   * - ``fileEncoding``
     - No
     - Codificacion de caracteres (predeterminado: UTF-8)

.. warning::
   Es necesario especificar ``files`` o ``directories``.
   Si no se especifica ninguno (ambos vacios), se producira una ``DataStoreException``.
   Si se especifican ambos, ``files`` tiene prioridad y ``directories`` se ignora.

.. note::
   El nombre del parametro usa camelCase: ``fileEncoding`` (no snake_case ``file_encoding``).

Comportamiento al especificar directorios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando se especifica ``directories``, los archivos ubicados directamente en cada directorio se procesan segun las siguientes reglas.

- **Los subdirectorios no se recorren** (no se realiza busqueda recursiva).
- Solo se procesan archivos con extension ``.json`` o ``.jsonl`` (sin distinguir mayusculas de minusculas).
- Los archivos se procesan en orden ascendente por fecha de modificacion (hora de ultima modificacion).

.. note::
   Este conector solo admite archivos JSON en el sistema de archivos local. No es compatible con acceso HTTP ni funciones de autenticacion de API.

Configuracion de scripts
-------------------------

Los valores de cada campo se construyen referenciando los valores de los campos del objeto JSON.
Los campos del nivel superior del objeto JSON se pueden referenciar directamente dentro del script
como **variables sin prefijo** (no se usa ningun prefijo como ``data.``).

Objeto JSON simple:

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

Objeto JSON anidado (los objetos anidados se referencian como mapas):

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

Procesamiento de elementos de array:

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``<nombre_campo>`` - Referencia directa a un campo del nivel superior del objeto JSON por nombre
- ``<padre>.<hijo>`` - Campo de un objeto anidado
- ``<array>[<indice>]`` - Elemento de array
- ``<array>.<metodo>`` - Metodos de array (``join``, ``collect``, ``size``, etc.)

.. note::

   Si el nombre de un campo contiene caracteres invalidos como identificador de Groovy (espacios,
   guiones, etc.), ese campo no puede referenciarse directamente como nombre de variable.

Detalles del formato JSON
=========================

Formato de archivo JSON
------------------------

El conector JSON lee archivos en formato JSONL (JSON Lines).
Es un formato en el que se escribe un objeto JSON por linea. El archivo se lee linea a linea
y cada linea se analiza como un objeto JSON independiente.

.. note::
   Los archivos con extension ``.json`` tambien son procesados, pero su contenido debe estar
   en formato JSONL (un objeto por linea).
   Los archivos JSON en formato de array ( ``[{...}, {...}]`` ) o con formato de varias lineas
   (pretty-printed) no se pueden leer directamente. Conviertelos al formato JSONL.

Archivo en formato JSONL:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

Ejemplos de uso
===============

Catalogo de productos
----------------------

Parametros:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

Scripts:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Precio: " + price + " yenes"
    digest=category
    price=price

Integracion de multiples archivos JSON
---------------------------------------

Parametros:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

Scripts:

::

    url="https://example.com/item/" + id
    title=title
    content=content

Solucion de problemas
======================

Archivo no encontrado
----------------------

**Sintoma**: El registro muestra ``... is not found.`` o ``Source file ... does not exist.``

**Puntos a verificar**:

1. Verificar que la ruta del archivo sea correcta
2. Verificar que el archivo exista
3. Verificar que la extension del archivo sea ``.json`` o ``.jsonl``
4. Verificar que el archivo tenga permisos de lectura

Error de analisis JSON
-----------------------

**Sintoma**: El registro muestra ``Crawling Access Exception`` y ``JsonParseException``, entre otros

Si una linea contiene datos invalidos, solo esa linea se omite y se registra como URL fallida,
y el crawling continua desde la siguiente linea.

**Puntos a verificar**:

1. Verificar que el archivo JSON tenga el formato correcto (JSONL: un objeto por linea):

   ::

       # Validar que cada linea sea un objeto JSON valido
       cat data.json | jq -c .

2. Verificar la codificacion de caracteres
3. Verificar que un mismo objeto no este dividido en varias lineas
4. Verificar que no contenga comentarios (no permitidos en el estandar JSON)

No se obtienen datos
---------------------

**Sintoma**: El crawling se completa con exito pero el recuento es 0

**Puntos a verificar**:

1. Verificar la estructura JSON
2. Verificar que la configuracion de scripts sea correcta (que las referencias a campos no tengan el prefijo ``data.``)
3. Verificar los nombres de campo (incluyendo mayusculas y minusculas)
4. Verificar los mensajes de error en los registros

Archivos JSON grandes
----------------------

**Sintoma**: Falta de memoria o tiempo de espera agotado

El archivo se lee linea a linea, por lo que el tamano total del archivo no afecta directamente
al uso de memoria. Sin embargo, pueden surgir problemas si una sola linea (un objeto) es
extremadamente grande o si la carga de indexacion es elevada.

**Solucion**:

1. Dividir el archivo JSON en varios archivos
2. Aumentar el tamano del heap de |Fess|

Uso avanzado de scripts
========================

Procesamiento condicional
--------------------------

Cada campo se evalua como una expresion independiente. Para valores condicionales, utilice el operador ternario:

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

Union de arrays
----------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

Configuracion de valores predeterminados
-----------------------------------------

::

    url="https://example.com/item/" + id
    title=title ?: "Sin titulo"
    content=description ?: (summary ?: "Sin descripcion")
    price=price ?: 0

Formato de fechas
------------------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

Procesamiento de numeros
-------------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

Informacion de referencia
==========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
