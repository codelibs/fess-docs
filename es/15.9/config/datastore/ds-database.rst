======================================================
Conector de Base de Datos (Búsqueda en Bases de Datos)
======================================================

Descripción General
===================

El conector de base de datos permite registrar en el índice de |Fess| los registros de bases de datos relacionales compatibles con JDBC (MySQL, PostgreSQL, Oracle, SQL Server, etc.), haciendo posible la búsqueda en bases de datos (búsqueda de texto completo sobre el contenido de la base de datos). Cada columna obtenida mediante una sentencia SELECT se asigna a un campo de búsqueda durante el registro.

El conector de base de datos proporciona funcionalidad para obtener datos de bases de datos
relacionales compatibles con JDBC y registrarlos en el índice de |Fess|.

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
4. Para grandes volúmenes de datos, es importante un diseño de consultas apropiado

Instalación del Plugin
----------------------

Método 1: Instalar desde la consola de administración

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Método 2: Colocar el archivo JAR directamente

::

    # Descargar desde el repositorio de CodeLibs
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Colocar el archivo (el mismo directorio en el que instala la consola de administracion)
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # o bien
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

Instalación del Controlador JDBC
---------------------------------

El controlador JDBC no se incluye en el plugin. Obtenga por separado el controlador correspondiente a su base de datos y colóquelo usted mismo.

El rastreo del almacén de datos se ejecuta en el proceso del rastreador, por lo que el controlador debe estar en el **classpath del proceso del rastreador**. Sirve cualquiera de estos directorios:

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # Ejemplo: Controlador MySQL
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # o bien
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Después de colocar el controlador JDBC, reinicie |Fess| para cargarlo.

.. note::
   Cuando falta el controlador, el rastreo falla con el mensaje
   ``The JDBC driver ... is not on the crawler classpath.``

Método de Configuración
=======================

Configure desde la consola de administración en "Rastreador" -> "Almacén de Datos" -> "Crear Nuevo".

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Elemento
     - Ejemplo de Configuración
   * - Nombre
     - Products Database
   * - Nombre del Manejador
     - DatabaseDataStore
   * - Habilitado
     - Activado

Configuración de Parámetros
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

Lista de Parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - Parámetro
     - Requerido
     - Descripción
   * - ``driver``
     - Si
     - Nombre de la clase del controlador JDBC (si no se especifica, se produce ``DataStoreException``)
   * - ``url``
     - Si
     - URL de conexión JDBC (obligatorio para la conexión)
   * - ``sql``
     - Si
     - Consulta SQL para obtener datos (si no se especifica, se produce ``DataStoreException``)
   * - ``username``
     - No
     - Nombre de usuario de la base de datos
   * - ``password``
     - No
     - Contraseña de la base de datos
   * - ``fetch_size``
     - No
     - Tamaño de recuperación JDBC. ``MIN_VALUE`` indica a MySQL que lea el conjunto de resultados fila a fila; otros controladores rechazan los valores negativos y el rastreo continúa con el valor predeterminado del controlador tras emitir una advertencia. Los valores negativos o no numéricos se notifican y se ignoran
   * - ``query_timeout``
     - No
     - Tiempo de espera de la consulta en segundos. ``0`` significa sin límite (el valor predeterminado de JDBC). Si el parámetro no se especifica, no se establece ningún tiempo de espera
   * - ``default_mimetype``
     - No
     - Tipo MIME predeterminado utilizado al extraer contenido de columnas BLOB o binarias
   * - ``column_label.mimetype``
     - No
     - Nombre de la columna que contiene el tipo MIME utilizado para la extracción de columnas BLOB o binarias (ej. ``column_label.mimetype=content_type``)
   * - ``column_label.filename``
     - No
     - Nombre de la columna que contiene el nombre de archivo utilizado para la extracción de columnas BLOB o binarias (el tipo MIME se infiere a partir de la extensión)
   * - ``info.*``
     - No
     - Propiedades adicionales de conexión JDBC (ej. ``info.ssl=true``). La clave sin el prefijo ``info.`` se pasa al controlador JDBC
   * - ``readInterval``
     - No
     - Retardo en milisegundos entre el procesamiento de cada fila. Predeterminado: 0
   * - ``script_type``
     - No
     - Tipo de motor de scripts. Predeterminado: groovy

.. note::
   Si una consulta se queda bloqueada, detener el trabajo no libera el hilo del rastreador.
   La solicitud de parada solo se comprueba entre filas, por lo que no puede interrumpir una
   llamada bloqueada dentro del controlador. Establezca ``query_timeout`` para las consultas
   que puedan tardar mucho.

Configuración de Script
------------------------

Mapee los nombres de columnas SQL a campos del índice:

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

Campos disponibles:

- ``<nombre_columna>`` - Columnas de resultado de la consulta SQL (se accede directamente por el nombre de la etiqueta de columna; no se usa prefijo como ``data.``)
- ``crawlingConfig`` - la configuración del almacén de datos
- ``crawlingContext`` - el contexto del rastreo; ``crawlingContext.doc`` contiene el documento que se está construyendo

.. note::
   Los nombres de columna deben coincidir con la etiqueta de columna (alias) de la cláusula ``SELECT``.
   Cuando se usen funciones de agregación o expresiones, asigne un alias explícito con ``AS``
   (ej. ``COUNT(*) AS total``).

.. note::
   El uso de mayúsculas y minúsculas en las etiquetas de columna varía según la base de datos.
   PostgreSQL convierte a minúsculas los identificadores sin comillas, H2 los convierte a
   mayúsculas y MySQL los devuelve tal como se declararon. Un nombre que no se resuelve deja el
   campo sin asignar en lugar de generar un error, así que asigne un alias explícito con ``AS``
   cuando la portabilidad sea importante.

.. warning::
   Los scripts pueden referenciar **todo el mapa de parámetros del almacén de datos**, no solo
   las columnas de resultado de la consulta SQL. ``driver``, ``url``, ``username``, ``password``
   y ``sql`` son visibles como variables con el mismo nombre, por lo que una columna puede
   quedar ocultada de forma involuntaria, o el valor de un parámetro puede aparecer donde se
   esperaba una columna inexistente. Cuando existen ambos, prevalece el valor de la columna.

Carga de Datos BLOB o Binarios
================================

Las columnas binarias (BLOB, ``BYTEA``, arrays de bytes y flujos binarios) se procesan
mediante el extractor de contenido (el mismo que se usa en el rastreo de archivos) y se
incorporan como texto.

CLOB, NCLOB y los flujos de caracteres **no** pasan por ningún extractor. Se leen tal cual
como texto, y las indicaciones de tipo MIME descritas a continuación no se les aplican.

Las columnas de tipo array se convierten en sus elementos unidos por espacios. Los valores
NULL se convierten en cadenas vacías.

.. note::
   Que una columna BLOB llegue como ``java.sql.Blob`` o como array de bytes lo decide el
   controlador JDBC: MySQL y PostgreSQL devuelven un array de bytes. Ambos se extraen de la
   misma manera.

.. note::
   CLOB y NCLOB se leen enteros en memoria, sin límite de tamaño. Para columnas de texto muy
   grandes, considere truncarlas en el SQL con ``SUBSTRING`` o similar. La ruta que pasa por
   el extractor si respeta la longitud máxima de contenido del rastreador.

Para extraer correctamente el texto de datos BLOB o flujos binarios, es necesario
determinar el tipo de dato (tipo MIME). La determinación sigue el siguiente orden de
prioridad:

1. ``column_label.mimetype=<nombre_columna>`` - Usa el valor de la columna indicada como tipo MIME
2. ``column_label.filename=<nombre_columna>`` - Trata el valor de la columna indicada como nombre de archivo e infiere el tipo MIME a partir de la extensión
3. ``default_mimetype`` - Tipo MIME predeterminado usado cuando no se puede determinar con los métodos anteriores

Ejemplo (extracción del BLOB de la columna ``file_data`` usando el tipo MIME de la columna ``content_type``):

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

Diseño de Consultas SQL
========================

Consultas Eficientes
---------------------

Al manejar grandes cantidades de datos, el rendimiento de la consulta es importante.
La consulta SQL se envía tal cual a la base de datos (no se realiza enlace de parámetros):

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
    ORDER BY id

Rastreo Incremental
--------------------

Método para obtener solo registros actualizados:

::

    # Filtrar por fecha de actualizacion
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # Especificar rango por ID
    sql=SELECT * FROM articles WHERE id > 10000

.. warning::
   Restringir la consulta de esta manera no convierte el rastreo en incremental. Cuando
   un rastreo termina, |Fess| elimina los documentos de esta configuración del almacén
   de datos que no formaron parte del rastreo que acaba de ejecutarse, de modo que una
   consulta filtrada deja en el índice únicamente las filas coincidentes.

   Añada ``delete_old_docs=false`` a los parámetros del almacén de datos para conservar
   los documentos indexados por rastreos anteriores. Las filas eliminadas de la base de
   datos dejan entonces de eliminarse también del índice, así que ejecute periódicamente
   un rastreo completo.

Generación de URLs
-------------------

Las URLs de documentos se generan en el script:

::

    # Patron fijo
    url="https://example.com/article/" + id

    # Combinacion de multiples campos
    url="https://example.com/" + category + "/" + slug

    # Usar URL almacenada en la base de datos
    url=url

.. warning::
   ``url=url`` solo hace lo que parece cuando el resultado de ``SELECT`` tiene una columna
   etiquetada como ``url``. Si no existe esa columna, el parámetro del almacén de datos con el
   mismo nombre, es decir, la **URL de conexión JDBC**, se convierte en la URL del documento.
   Asigne un alias a la columna, como en ``SELECT page_url AS url``, o indíquela en el script,
   como en ``url=page_url``.

Soporte de Caracteres Multibyte
================================

Al manejar datos con caracteres multibyte como japonés u otros idiomas:

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

Protección de Credenciales de Base de Datos
--------------------------------------------

.. warning::
   Escribir contraseñas directamente en archivos de configuración es un riesgo de seguridad.

Métodos recomendados:

1. Aprovechar el cifrado automático

   El valor de un parámetro cuyo nombre coincide con ``app.encrypt.property.pattern``
   (predeterminado ``.*password|.*key|.*token|.*secret``) se cifra al guardarlo desde la
   consola de administración y se almacena con el prefijo ``{cipher}``. ``password`` coincide
   con ese patrón, por lo que no se almacena en texto plano cuando se establece desde la
   consola de administración.

2. Usar variables de entorno

   Una variable de entorno cuyo nombre empieza por ``FESS_ENV_`` se expande dentro de un
   parámetro del almacén de datos como ``${nombre de la variable}``:

   ::

       password=${FESS_ENV_DB_PASSWORD}

   Qué nombres se expanden lo controla ``crawler.data.env.param.key.pattern``
   (predeterminado ``^FESS_ENV_.*``).

3. Usar usuarios de solo lectura

.. note::
   Subir ``org.codelibs.fess.ds`` a DEBUG no expone las credenciales: los valores de los
   parámetros que coinciden con ``app.encrypt.property.pattern``, y las credenciales incrustadas
   en la URL JDBC, se enmascaran en el registro.

Principio de Mínimo Privilegio
--------------------------------

Otorgue solo los permisos mínimos necesarios al usuario de la base de datos:

::

    -- Ejemplo MySQL
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

Ejemplos de Uso
===============

Búsqueda de Catálogo de Productos
-----------------------------------

Parámetros:

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

Artículos de Base de Conocimientos
-------------------------------------

Parámetros:

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

Solución de Problemas
======================

Cuando un rastreo falla, el mensaje del registro identifica qué paso ha fallado.

Controlador JDBC No Encontrado
--------------------------------

**Síntoma**: ``The JDBC driver ... is not on the crawler classpath.``

**Solución**:

1. Verifique que el controlador JDBC esté colocado en ``app/WEB-INF/lib/`` o ``app/WEB-INF/env/crawler/lib/``
2. Verifique que el nombre de clase indicado en ``driver`` sea correcto
3. Reinicie |Fess|

Error de Conexión
------------------

**Síntoma**: ``Failed to connect to <URL>.``

**Verifique**:

1. La base de datos está en ejecución
2. El nombre del host y número de puerto son correctos
3. El nombre de usuario y contraseña son correctos
4. Configuración del firewall

Error de Consulta
------------------

**Síntoma**: ``Failed to execute the query.``

**Verifique**:

1. Ejecute la consulta SQL directamente en la base de datos para probar
2. Verifique que los nombres de columna sean correctos
3. Verifique que los nombres de tabla sean correctos

Parámetros Faltantes
---------------------

**Síntoma**: ``The driver parameter is required.``, ``The url parameter is required.`` o ``The sql parameter is required.``

Falta un parámetro obligatorio. Revise el campo de parámetros.

Solo Fallan Algunas Filas
--------------------------

Una fila que falla no detiene el rastreo; queda registrada en "Sistema" -> "URL con Errores".
Se usa la URL del documento cuando los scripts la generaron, y
``datastore://<id de la configuracion del almacen de datos>/<numero de fila>`` cuando no.

Los Documentos No Aparecen en los Resultados de Búsqueda
---------------------------------------------------------

1. Verifique que los scripts establezcan ``url``, ``title`` y ``content``
2. Verifique que el uso de mayúsculas y minúsculas de las etiquetas de columna coincida con el que usan los scripts (véase "Configuración de Script")
3. Revise el número de documentos en el registro del trabajo de rastreo

Información de Referencia
==========================

- :doc:`ds-overview` - Descripción General de Conectores de Almacén de Datos
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-json` - Conector JSON
- :doc:`../../admin/dataconfig-guide` - Guía de Configuración de Almacén de Datos
- :doc:`../crawler-basic`
- :doc:`../search-basic`
