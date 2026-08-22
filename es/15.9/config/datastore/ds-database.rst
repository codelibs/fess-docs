======================================================
Conector de Base de Datos (Búsqueda en Bases de Datos)
======================================================

Descripcion General
===================

El conector de base de datos permite registrar en el índice de |Fess| los registros de bases de datos relacionales compatibles con JDBC (MySQL, PostgreSQL, Oracle, SQL Server, etc.), haciendo posible la búsqueda en bases de datos (búsqueda de texto completo sobre el contenido de la base de datos). Cada columna obtenida mediante una sentencia SELECT se asigna a un campo de búsqueda durante el registro.

El conector de base de datos proporciona funcionalidad para obtener datos de bases de datos
relacionales compatibles con JDBC y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-db``.

Bases de Datos Compatibles
==========================

Compatible con todas las bases de datos que soporten JDBC. Ejemplos principales:

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

Requisitos Previos
==================

1. Se requiere instalar el plugin ``fess-ds-db``
2. Se requiere el controlador JDBC correspondiente a la base de datos de destino
3. Se requiere acceso de lectura a la base de datos
4. Para grandes volumenes de datos, es importante un diseno de consultas apropiado

Instalacion del Plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Colocar el archivo
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o bien
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Metodo 2: Instalar desde la consola de administracion

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Instalacion del Controlador JDBC
---------------------------------

Coloque el controlador JDBC correspondiente a la base de datos de destino en el classpath de |Fess| (directorio ``app/WEB-INF/lib/``):

::

    # Ejemplo: Controlador MySQL
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # o bien
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Despues de colocar el controlador JDBC, reinicie |Fess| para cargarlo.

Metodo de Configuracion
=======================

Configure desde la consola de administracion en "Rastreador" -> "Almacen de Datos" -> "Crear Nuevo".

Configuracion Basica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de Configuracion
   * - Nombre
     - Products Database
   * - Nombre del Manejador
     - DatabaseDataStore
   * - Habilitado
     - Activado

Configuracion de Parametros
----------------------------

Ejemplo MySQL/MariaDB:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

Ejemplo PostgreSQL:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

Lista de Parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Parametro
     - Requerido
     - Descripcion
   * - ``driver``
     - Si
     - Nombre de la clase del controlador JDBC (si no se especifica, se produce ``DataStoreException``)
   * - ``url``
     - Si
     - URL de conexion JDBC (obligatorio para la conexion)
   * - ``sql``
     - Si
     - Consulta SQL para obtener datos (si no se especifica, se produce ``DataStoreException``)
   * - ``username``
     - No
     - Nombre de usuario de la base de datos
   * - ``password``
     - No
     - Contrasena de la base de datos
   * - ``fetch_size``
     - No
     - Tamano de recuperacion JDBC. Para resultados en streaming con MySQL, especifique ``MIN_VALUE``
   * - ``default_mimetype``
     - No
     - Tipo MIME predeterminado utilizado al extraer contenido de columnas BLOB o binarias
   * - ``column_label.mimetype``
     - No
     - Nombre de la columna que contiene el tipo MIME utilizado para la extraccion de columnas BLOB o binarias (ej. ``column_label.mimetype=content_type``)
   * - ``column_label.filename``
     - No
     - Nombre de la columna que contiene el nombre de archivo utilizado para la extraccion de columnas BLOB o binarias (el tipo MIME se infiere a partir de la extension)
   * - ``info.*``
     - No
     - Propiedades adicionales de conexion JDBC (ej. ``info.ssl=true``). La clave sin el prefijo ``info.`` se pasa al controlador JDBC
   * - ``readInterval``
     - No
     - Retardo en milisegundos entre el procesamiento de cada fila. Predeterminado: 0
   * - ``script_type``
     - No
     - Tipo de motor de scripts. Predeterminado: groovy

Configuracion de Script
------------------------

Mapee los nombres de columnas SQL a campos del indice:

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

Campos disponibles:

- ``<nombre_columna>`` - Columnas de resultado de la consulta SQL (se accede directamente por el nombre de la etiqueta de columna; no se usa prefijo como ``data.``)

.. note::
   Los nombres de columna deben coincidir con la etiqueta de columna (alias) de la clausula ``SELECT``.
   Cuando se usen funciones de agregacion o expresiones, asigne un alias explicito con ``AS``
   (ej. ``COUNT(*) AS total``).

Carga de Datos BLOB o Binarios
================================

Las columnas de tipo BLOB, CLOB, NCLOB, arrays de bytes y flujos binarios se procesan
automaticamente mediante el extractor de contenido (el mismo que se usa en el rastreo de
archivos) y se incorporan como texto. Las columnas de tipo array se convierten en cadenas
separadas por espacios. Los valores NULL se convierten en cadenas vacias.

Para extraer correctamente el texto de datos BLOB o flujos binarios, es necesario
determinar el tipo de dato (tipo MIME). La determinacion sigue el siguiente orden de
prioridad:

1. ``column_label.mimetype=<nombre_columna>`` - Usa el valor de la columna indicada como tipo MIME
2. ``column_label.filename=<nombre_columna>`` - Trata el valor de la columna indicada como nombre de archivo e infiere el tipo MIME a partir de la extension
3. ``default_mimetype`` - Tipo MIME predeterminado usado cuando no se puede determinar con los metodos anteriores

Ejemplo (extraccion del BLOB de la columna ``file_data`` usando el tipo MIME de la columna ``content_type``):

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

Diseno de Consultas SQL
========================

Consultas Eficientes
---------------------

Al manejar grandes cantidades de datos, el rendimiento de la consulta es importante.
La consulta SQL se envia tal cual a la base de datos (no se realiza enlace de parametros):

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

Rastreo Incremental
--------------------

Metodo para obtener solo registros actualizados:

::

    # Filtrar por fecha de actualizacion
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Especificar rango por ID
    sql=SELECT * FROM articles WHERE id > 10000

Generacion de URLs
-------------------

Las URLs de documentos se generan en el script:

::

    # Patron fijo
    url="https://example.com/article/" + id

    # Combinacion de multiples campos
    url="https://example.com/" + category + "/" + slug

    # Usar URL almacenada en la base de datos
    url=url

Soporte de Caracteres Multibyte
================================

Al manejar datos con caracteres multibyte como japones u otros idiomas:

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL normalmente usa UTF-8 de forma predeterminada. Si es necesario:

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

Seguridad
=========

Proteccion de Credenciales de Base de Datos
--------------------------------------------

.. warning::
   Escribir contrasenas directamente en archivos de configuracion es un riesgo de seguridad.

Metodos recomendados:

1. Usar variables de entorno
2. Usar la funcion de cifrado de |Fess|
3. Usar usuarios de solo lectura

Principio de Minimo Privilegio
--------------------------------

Otorgue solo los permisos minimos necesarios al usuario de la base de datos:

::

    -- Ejemplo MySQL
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Ejemplos de Uso
===============

Busqueda de Catalogo de Productos
-----------------------------------

Parametros:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

Script:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " Categoria: " + category + " Precio: " + price + " EUR"
    lastModified=updated_at

Articulos de Base de Conocimientos
-------------------------------------

Parametros:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

Script:

::

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

Solucion de Problemas
======================

Controlador JDBC No Encontrado
--------------------------------

**Sintoma**: ``ClassNotFoundException`` o ``No suitable driver``

**Solucion**:

1. Verifique que el controlador JDBC este colocado en ``lib/``
2. Verifique que el nombre de la clase del controlador sea correcto
3. Reinicie |Fess|

Error de Conexion
------------------

**Sintoma**: ``Connection refused`` o error de autenticacion

**Verifique**:

1. La base de datos esta en ejecucion
2. El nombre del host y numero de puerto son correctos
3. El nombre de usuario y contrasena son correctos
4. Configuracion del firewall

Error de Consulta
------------------

**Sintoma**: ``SQLException`` o error de sintaxis SQL

**Verifique**:

1. Ejecute la consulta SQL directamente en la base de datos para probar
2. Verifique que los nombres de columna sean correctos
3. Verifique que los nombres de tabla sean correctos

Informacion de Referencia
==========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-json` - Conector JSON
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- :doc:`../crawler-basic`
- :doc:`../search-basic`
