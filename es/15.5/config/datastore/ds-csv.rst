==================================
Conector CSV
==================================

Descripcion general
===================

El conector CSV proporciona la funcionalidad para obtener datos de archivos CSV
y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-csv``.

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere acceso a los archivos CSV
3. Es necesario conocer la codificacion de caracteres del archivo CSV

Instalacion del plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # Colocar
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products CSV
   * - Handler
     - CsvDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
---------------------------

Archivo local:

::

    file_path=/path/to/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Archivo HTTP:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Multiples archivos:

::

    file_path=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

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
     - Ruta del archivo CSV (local, HTTP, multiples separados por comas)
   * - ``encoding``
     - No
     - Codificacion de caracteres (predeterminado: UTF-8)
   * - ``has_header``
     - No
     - Si tiene fila de encabezado (predeterminado: true)
   * - ``separator``
     - No
     - Caracter separador (predeterminado: coma ``,``)
   * - ``quote``
     - No
     - Caracter de comillas (predeterminado: comillas dobles ``"``)

Configuracion de scripts
------------------------

Con encabezado:

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

Sin encabezado (especificando indice de columna):

::

    url="https://example.com/product/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``data.<nombre_columna>`` - Nombre de columna del encabezado (cuando has_header=true)
- ``data.col<N>`` - Indice de columna (cuando has_header=false, comenzando desde 0)

Detalles del formato CSV
========================

CSV estandar (compatible con RFC 4180)
--------------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

Cambiar el separador
--------------------

Delimitado por tabulador (TSV):

::

    # Parametro
    separator=\t

Delimitado por punto y coma:

::

    # Parametro
    separator=;

Comillas personalizadas
-----------------------

Comillas simples:

::

    # Parametro
    quote='

Codificacion
------------

Archivo en japones (Shift_JIS):

::

    encoding=Shift_JIS

Archivo en japones (EUC-JP):

::

    encoding=EUC-JP

Ejemplos de uso
===============

CSV de catalogo de productos
----------------------------

Archivo CSV (products.csv):

::

    product_id,name,description,price,category,in_stock
    1001,Laptop,Laptop de alto rendimiento,120000,Computadoras,true
    1002,Mouse,Mouse inalambrico,2500,Perifericos,true
    1003,Teclado,Teclado mecanico,8500,Perifericos,false

Parametros:

::

    file_path=/var/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " Categoria: " + data.category + " Precio: " + data.price
    digest=data.category
    price=data.price

Filtrado por informacion de stock:

::

    if (data.in_stock == "true") {
        url="https://shop.example.com/product/" + data.product_id
        title=data.name
        content=data.description
        price=data.price
    }

CSV de directorio de empleados
------------------------------

Archivo CSV (employees.csv):

::

    emp_id,name,department,email,phone,position
    E001,Juan Garcia,Ventas,juan@example.com,03-1234-5678,Director
    E002,Maria Lopez,Desarrollo,maria@example.com,03-2345-6789,Gerente
    E003,Pedro Rodriguez,Administracion,pedro@example.com,03-3456-7890,Encargado

Parametros:

::

    file_path=/var/data/employees.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="Departamento: " + data.department + "\nCargo: " + data.position + "\nEmail: " + data.email + "\nTelefono: " + data.phone
    digest=data.department

CSV sin encabezado
------------------

Archivo CSV (data.csv):

::

    1,Producto A,Este es el producto A,1000
    2,Producto B,Este es el producto B,2000
    3,Producto C,Este es el producto C,3000

Parametros:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=false
    separator=,
    quote="

Script:

::

    url="https://example.com/item/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

Integracion de multiples archivos CSV
-------------------------------------

Parametros:

::

    file_path=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

Obtener CSV desde HTTP
----------------------

Parametros:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Script:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description

Archivo delimitado por tabulador (TSV)
--------------------------------------

Archivo TSV (data.tsv):

::

    id	title	content	category
    1	Articulo1	Este es el contenido del articulo 1	Noticias
    2	Articulo2	Este es el contenido del articulo 2	Blog

Parametros:

::

    file_path=/var/data/data.tsv
    encoding=UTF-8
    has_header=true
    separator=\t
    quote="

Script:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

Solucion de problemas
=====================

Archivo no encontrado
---------------------

**Sintoma**: ``FileNotFoundException`` o ``No such file``

**Verificaciones**:

1. Verificar que la ruta del archivo sea correcta (se recomienda ruta absoluta)
2. Confirmar que el archivo existe
3. Verificar que tiene permisos de lectura
4. Confirmar que es accesible desde el usuario que ejecuta |Fess|

Caracteres ilegibles
--------------------

**Sintoma**: Los caracteres no se muestran correctamente

**Solucion**:

Especificar la codificacion correcta:

::

    # UTF-8
    encoding=UTF-8

    # Shift_JIS
    encoding=Shift_JIS

    # EUC-JP
    encoding=EUC-JP

    # Windows estandar (CP932)
    encoding=Windows-31J

Verificar la codificacion del archivo:

::

    file -i data.csv
    # o
    nkf -g data.csv

Las columnas no se reconocen correctamente
------------------------------------------

**Sintoma**: El delimitador de columnas no se reconoce correctamente

**Verificaciones**:

1. Verificar que el caracter separador sea correcto:

   ::

       # Coma
       separator=,

       # Tabulador
       separator=\t

       # Punto y coma
       separator=;

2. Verificar la configuracion de comillas
3. Verificar el formato del archivo CSV (si cumple con RFC 4180)

Manejo de la fila de encabezado
-------------------------------

**Sintoma**: La primera fila se reconoce como datos

**Solucion**:

Cuando hay fila de encabezado:

::

    has_header=true

Cuando no hay fila de encabezado:

::

    has_header=false

No se obtienen datos
--------------------

**Sintoma**: El crawl tiene exito pero el conteo es 0

**Verificaciones**:

1. Verificar que el archivo CSV no este vacio
2. Verificar que la configuracion del script sea correcta
3. Verificar que los nombres de columna sean correctos (cuando has_header=true)
4. Revisar los mensajes de error en el log

Archivo CSV grande
------------------

**Sintoma**: Memoria insuficiente o timeout

**Solucion**:

1. Dividir el archivo CSV en varios
2. Usar solo las columnas necesarias en el script
3. Aumentar el tamano del heap de |Fess|
4. Filtrar filas innecesarias

Campo con saltos de linea
-------------------------

En formato RFC 4180, los campos con saltos de linea pueden manejarse encerrandolos en comillas:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Parametros:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

Ejemplos avanzados de scripts
=============================

Procesamiento de datos
----------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseInt(data.price)
    category=data.category.toLowerCase()

Indexado condicional
--------------------

::

    # Solo productos con precio mayor o igual a 10000
    if (parseInt(data.price) >= 10000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

Concatenacion de multiples columnas
-----------------------------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\nEspecificaciones:\n" + data.specs + "\n\nNotas:\n" + data.notes
    category=data.category

Formato de fecha
----------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # Si se necesita conversion de formato de fecha, agregar procesamiento adicional

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-json` - Conector JSON
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `RFC 4180 - Formato CSV <https://datatracker.ietf.org/doc/html/rfc4180>`_
