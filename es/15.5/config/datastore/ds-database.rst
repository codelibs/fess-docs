==================================
Conector de Base de Datos
==================================

Descripcion General
===================

El conector de base de datos proporciona funcionalidad para obtener datos de bases de datos
relacionales compatibles con JDBC y registrarlos en el indice de |Fess|.

Esta funcionalidad esta incorporada en |Fess| y no requiere plugins adicionales.

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

1. Se requiere el controlador JDBC
2. Se requiere acceso de lectura a la base de datos
3. Para grandes volumenes de datos, es importante un diseno de consultas apropiado

Instalacion del Controlador JDBC
--------------------------------

Coloque el controlador JDBC en el directorio ``lib/``:

::

    # Ejemplo: Controlador MySQL
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

Reinicie |Fess| para cargar el controlador.

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
---------------------------

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
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``driver``
     - Si
     - Nombre de la clase del controlador JDBC
   * - ``url``
     - Si
     - URL de conexion JDBC
   * - ``username``
     - Si
     - Nombre de usuario de la base de datos
   * - ``password``
     - Si
     - Contrasena de la base de datos
   * - ``sql``
     - Si
     - Consulta SQL para obtener datos
   * - ``fetch.size``
     - No
     - Tamano de obtencion (predeterminado: 100)

Configuracion de Script
-----------------------

Mapee los nombres de columnas SQL a campos del indice:

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

Campos disponibles:

- ``data.<nombre_columna>`` - Columnas de resultado de la consulta SQL

Diseno de Consultas SQL
=======================

Consultas Eficientes
--------------------

Al manejar grandes cantidades de datos, el rendimiento de la consulta es importante:

::

    # Consulta eficiente usando indices
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
    ORDER BY id

Rastreo Incremental
-------------------

Metodo para obtener solo registros actualizados:

::

    # Filtrar por fecha de actualizacion
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Especificar rango por ID
    sql=SELECT * FROM articles WHERE id > 10000

Generacion de URLs
------------------

Las URLs de documentos se generan en el script:

::

    # Patron fijo
    url="https://example.com/article/" + data.id

    # Combinacion de multiples campos
    url="https://example.com/" + data.category + "/" + data.slug

    # Usar URL almacenada en la base de datos
    url=data.url

Soporte de Caracteres Multibyte
===============================

Al manejar datos con caracteres multibyte como espanol o japones:

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQL normalmente usa UTF-8 de forma predeterminada. Si es necesario:

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

Pooling de Conexiones
=====================

Para procesar grandes cantidades de datos, considere el pooling de conexiones:

::

    # Configuracion al usar HikariCP
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

Seguridad
=========

Proteccion de Credenciales de Base de Datos
-------------------------------------------

.. warning::
   Escribir contrasenas directamente en archivos de configuracion es un riesgo de seguridad.

Metodos recomendados:

1. Usar variables de entorno
2. Usar la funcion de cifrado de |Fess|
3. Usar usuarios de solo lectura

Principio de Minimo Privilegio
------------------------------

Otorgue solo los permisos minimos necesarios al usuario de la base de datos:

::

    -- Ejemplo MySQL
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Ejemplos de Uso
===============

Busqueda de Catalogo de Productos
---------------------------------

Parametros:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

Script:

::

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " Categoria: " + data.category + " Precio: " + data.price + " EUR"
    lastModified=data.updated_at

Articulos de Base de Conocimientos
----------------------------------

Parametros:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

Script:

::

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

Solucion de Problemas
=====================

Controlador JDBC No Encontrado
------------------------------

**Sintoma**: ``ClassNotFoundException`` o ``No suitable driver``

**Solucion**:

1. Verifique que el controlador JDBC este colocado en ``lib/``
2. Verifique que el nombre de la clase del controlador sea correcto
3. Reinicie |Fess|

Error de Conexion
-----------------

**Sintoma**: ``Connection refused`` o error de autenticacion

**Verifique**:

1. La base de datos esta en ejecucion
2. El nombre del host y numero de puerto son correctos
3. El nombre de usuario y contrasena son correctos
4. Configuracion del firewall

Error de Consulta
-----------------

**Sintoma**: ``SQLException`` o error de sintaxis SQL

**Verifique**:

1. Ejecute la consulta SQL directamente en la base de datos para probar
2. Verifique que los nombres de columna sean correctos
3. Verifique que los nombres de tabla sean correctos

Informacion de Referencia
=========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-json` - Conector JSON
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
