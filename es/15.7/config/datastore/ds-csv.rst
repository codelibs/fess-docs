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
   * - Nombre del handler
     - CsvDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
---------------------------

Archivo local:

::

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

Multiples archivos:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   El procesamiento de comillas (quote) y el procesamiento de escape estan **deshabilitados** por defecto.
   Si desea manejar CSV con caracteres separadores o saltos de linea dentro de campos entrecomillados
   (compatible con RFC 4180), especifique explicitamente ``quote_disabled=false`` para habilitar
   el procesamiento de comillas.
   Consulte la seccion "Habilitacion del procesamiento de comillas y escape" mas adelante para mas detalles.

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``files``
     - No
     - Ruta del archivo CSV (ruta local, multiples rutas separadas por comas). Se requiere especificar ``files`` o ``directories``. Si se especifican ambos, ``files`` tiene prioridad. Los archivos deben tener extension ``.csv`` o ``.tsv``; los archivos con otras extensiones son omitidos.
   * - ``directories``
     - No
     - Ruta del directorio que contiene archivos CSV (multiples rutas separadas por comas). Solo se procesan los archivos ``.csv`` y ``.tsv`` dentro del directorio. Se utiliza cuando no se especifica ``files``.
   * - ``file_encoding``
     - No
     - Codificacion de caracteres (predeterminado: UTF-8)
   * - ``has_header_line``
     - No
     - Si tiene fila de encabezado (predeterminado: false)
   * - ``separator_character``
     - No
     - Caracter separador (predeterminado: coma ``,``). Se pueden especificar secuencias de escape como ``\t`` (separador de tabulador).
   * - ``quote_character``
     - No
     - Caracter de comillas (predeterminado: comillas dobles ``"``). Sin embargo, el procesamiento de comillas esta deshabilitado por defecto (consulte ``quote_disabled``).
   * - ``escape_character``
     - No
     - Caracter de escape (predeterminado: barra invertida ``\``). Sin embargo, el procesamiento de escape esta deshabilitado por defecto (consulte ``escape_disabled``).

.. note::

   Si tanto ``files`` como ``directories`` estan vacios, se producira un error (``DataStoreException``).
   Debe especificar al menos uno de los dos.

Parametros avanzados
~~~~~~~~~~~~~~~~~~~~

Los siguientes parametros controlan de forma detallada el comportamiento del analisis del CSV:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Parametro
     - Descripcion
   * - ``quote_disabled``
     - Si deshabilitar el procesamiento de comillas (predeterminado: true). Especifique ``false`` para manejar campos entrecomillados compatibles con RFC 4180.
   * - ``escape_disabled``
     - Si deshabilitar el procesamiento de escape (predeterminado: true). Especifique ``false`` para habilitar el escape mediante ``escape_character``.
   * - ``skip_lines``
     - Numero de lineas iniciales a omitir (predeterminado: 0)
   * - ``ignore_line_patterns``
     - Patron de expresion regular para ignorar lineas (por ejemplo: ``^#.*`` para ignorar lineas de comentario)
   * - ``ignore_empty_lines``
     - Si ignorar las lineas vacias (predeterminado: false)
   * - ``ignore_trailing_whitespaces``
     - Si ignorar los espacios en blanco al final (predeterminado: false)
   * - ``ignore_leading_whitespaces``
     - Si ignorar los espacios en blanco al inicio (predeterminado: false)
   * - ``null_string``
     - Cadena que se trata como valor nulo
   * - ``break_string``
     - Cadena que reemplaza los saltos de linea dentro de los valores de campo
   * - ``readInterval``
     - Tiempo de espera por cada registro procesado (milisegundos) (predeterminado: 0)

Configuracion de scripts
------------------------

Los valores de cada campo se construyen referenciando los valores de cada columna del CSV. Las columnas
del CSV pueden referenciarse directamente en el script como **variables sin prefijo**
(no se usa ningun prefijo como ``data.``).

Con encabezado (referenciando por nombre de columna):

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

Sin encabezado (referenciando por indice de columna):

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``<nombre_columna>`` - Referencia directa por nombre de columna del encabezado (solo cuando ``has_header_line=true`` y el nombre de columna no esta en blanco)
- ``cell<N>`` - Referencia por indice de columna (empezando desde 1: ``cell1``, ``cell2``...; disponible independientemente de si hay encabezado)
- ``csvfile`` - Ruta completa del archivo CSV que se esta procesando
- ``csvfilename`` - Nombre del archivo CSV que se esta procesando

.. note::

   Si el nombre de columna contiene caracteres invalidos como identificadores de Groovy (espacios,
   guiones, etc.), no se puede referenciar por nombre de columna. En ese caso, use ``cell<N>``.

Detalles del formato CSV
=========================

CSV estandar (compatible con RFC 4180)
---------------------------------------

::

    product_id,product_name,description,price,category
    1,Laptop,Laptop de alto rendimiento,150000,Electronica
    2,Mouse,Mouse inalambrico,3000,Electronica
    3,"Book, Programming","Aprende a programar",2800,Libros

.. note::

   Para incluir el caracter separador dentro de un campo entrecomillado como ``"Book, Programming"``
   arriba, es necesario especificar ``quote_disabled=false`` para habilitar el procesamiento de comillas.
   Cuando el procesamiento de comillas esta deshabilitado (valor predeterminado), las comillas se tratan
   como caracteres normales y los campos se dividen por el caracter separador.

Habilitacion del procesamiento de comillas y escape
----------------------------------------------------

El procesamiento de comillas y el procesamiento de escape estan deshabilitados por defecto.
Habilitelos explicitamente de la siguiente manera.

Habilitar el procesamiento de comillas:

::

    # Parametros
    quote_disabled=false
    quote_character="

Habilitar el procesamiento de escape:

::

    # Parametros
    escape_disabled=false
    escape_character=\

Cambiar el separador
--------------------

Delimitado por tabulador (TSV):

::

    # Parametros
    separator_character=\t

Delimitado por punto y coma:

::

    # Parametros
    separator_character=;

Comillas personalizadas
-----------------------

Comillas simples (requiere habilitar el procesamiento de comillas):

::

    # Parametros
    quote_disabled=false
    quote_character='

Codificacion
------------

Archivo en espanol con codificacion Shift_JIS:

::

    file_encoding=Shift_JIS

Archivo con codificacion EUC-JP:

::

    file_encoding=EUC-JP

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

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " Categoria: " + category + " Precio: " + price
    digest=category
    price=price

Filtrado por informacion de stock:

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

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

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script:

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="Departamento: " + department + "\nCargo: " + position + "\nEmail: " + email + "\nTelefono: " + phone
    digest=department

CSV sin encabezado
------------------

Archivo CSV (data.csv):

::

    1,Producto A,Este es el producto A,1000
    2,Producto B,Este es el producto B,2000
    3,Producto C,Este es el producto C,3000

Parametros:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,

Script:

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

Integracion de multiples archivos CSV
-------------------------------------

Parametros:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

Script:

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

Archivo delimitado por tabulador (TSV)
--------------------------------------

Archivo TSV (data.tsv):

::

    id	title	content	category
    1	Articulo1	Este es el contenido del articulo 1	Noticias
    2	Articulo2	Este es el contenido del articulo 2	Blog

Parametros:

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t

Script:

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

Solucion de problemas
=====================

Archivo no encontrado
---------------------

**Sintoma**: El crawl se ejecuta pero el archivo no se procesa; el log muestra ``is not found``

**Verificaciones**:

1. Verificar que la ruta del archivo sea correcta (se recomienda ruta absoluta)
2. Confirmar que el archivo existe
3. Verificar que la extension del archivo sea ``.csv`` o ``.tsv`` (los archivos con otras extensiones son omitidos)
4. Verificar que tiene permisos de lectura
5. Confirmar que es accesible desde el usuario que ejecuta |Fess|

Caracteres ilegibles
--------------------

**Sintoma**: Los caracteres no se muestran correctamente

**Solucion**:

Especificar la codificacion correcta:

::

    # UTF-8
    file_encoding=UTF-8

    # Shift_JIS
    file_encoding=Shift_JIS

    # EUC-JP
    file_encoding=EUC-JP

    # Windows estandar (CP932)
    file_encoding=Windows-31J

Verificar la codificacion del archivo:

::

    file -i data.csv
    # o
    nkf -g data.csv

Las columnas no se reconocen correctamente
------------------------------------------

**Sintoma**: El delimitador de columnas no se reconoce correctamente, o los campos entrecomillados se dividen incorrectamente

**Verificaciones**:

1. Verificar que el caracter separador sea correcto:

   ::

       # Coma
       separator_character=,

       # Tabulador
       separator_character=\t

       # Punto y coma
       separator_character=;

2. Para manejar campos entrecomillados (campos que contienen el caracter separador), habilitar el procesamiento de comillas:

   ::

       quote_disabled=false

3. Verificar el formato del archivo CSV (si cumple con RFC 4180)

Manejo de la fila de encabezado
--------------------------------

**Sintoma**: La primera fila se reconoce como datos

**Solucion**:

Cuando hay fila de encabezado:

::

    has_header_line=true

Cuando no hay fila de encabezado:

::

    has_header_line=false

No se obtienen datos
--------------------

**Sintoma**: El crawl tiene exito pero el conteo es 0

**Verificaciones**:

1. Verificar que el archivo CSV no este vacio
2. Verificar que la configuracion del script sea correcta (comprobar que las referencias a nombres de columna o ``cell<N>`` no llevan el prefijo ``data.``)
3. Verificar que los nombres de columna sean correctos (cuando has_header_line=true)
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
--------------------------

En formato RFC 4180, los campos con saltos de linea pueden manejarse entrecomillandolos.
Como el procesamiento de comillas esta deshabilitado por defecto, es necesario especificar ``quote_disabled=false``:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

Parametros:

::

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_disabled=false
    quote_character="

CsvListDataStore
=================

El plugin ``fess-ds-csv`` incluye, ademas de ``CsvDataStore``, el handler ``CsvListDataStore``.

``CsvListDataStore`` extiende ``CsvDataStore`` y proporciona las siguientes funciones adicionales:

- Procesamiento multihilo (controlado mediante el parametro ``numOfThreads``)
- Eliminacion automatica de archivos CSV procesados
- Filtrado de archivos basado en marca de tiempo (omite archivos que aun se estan escribiendo)

Todos los parametros y configuraciones de script de ``CsvDataStore`` pueden utilizarse sin cambios.

Configuracion basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Campo
     - Ejemplo
   * - Nombre del handler
     - CsvListDataStore

Parametros adicionales
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``timestamp_margin``
     - No
     - Tiempo transcurrido desde la ultima modificacion del archivo (milisegundos). Los archivos que no hayan superado este tiempo se consideran en proceso de escritura y son omitidos (predeterminado: 10000)
   * - ``numOfThreads``
     - No
     - Numero de hilos de procesamiento (predeterminado: 1)

.. note::

   ``CsvListDataStore`` elimina automaticamente los archivos CSV tras procesarlos. Si se produce un error durante el procesamiento, el archivo se renombra con extension ``.txt`` (si el renombrado falla, el archivo se elimina).

Ejemplos avanzados de scripts
==============================

Procesamiento de datos
-----------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

Indexado condicional
--------------------

::

    // Solo productos con precio mayor o igual a 10000
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

Concatenacion de multiples columnas
------------------------------------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\nEspecificaciones:\n" + specs + "\n\nNotas:\n" + notes
    category=category

Formato de fecha
----------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // Si se necesita conversion de formato de fecha, agregar procesamiento adicional

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-json` - Conector JSON
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `RFC 4180 - Formato CSV <https://datatracker.ietf.org/doc/html/rfc4180>`_
