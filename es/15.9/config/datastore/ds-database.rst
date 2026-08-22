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

Metodo 1: Instalar desde la consola de administracion

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Metodo 2: Colocar el archivo JAR directamente

::

    # Descargar desde el repositorio de CodeLibs
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # Colocar el archivo (el mismo directorio en el que instala la consola de administracion)
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # o bien
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

Instalacion del Controlador JDBC
---------------------------------

El controlador JDBC no se incluye en el plugin. Obtenga por separado el controlador correspondiente a su base de datos y coloquelo usted mismo.

El rastreo del almacen de datos se ejecuta en el proceso del rastreador, por lo que el controlador debe estar en el **classpath del proceso del rastreador**. Sirve cualquiera de estos directorios:

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # Ejemplo: Controlador MySQL
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # o bien
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

Despues de colocar el controlador JDBC, reinicie |Fess| para cargarlo.

.. note::
   Cuando falta el controlador, el rastreo falla con el mensaje
   ``The JDBC driver ... is not on the crawler classpath.``

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
     - Tamano de recuperacion JDBC. ``MIN_VALUE`` indica a MySQL que lea el conjunto de resultados fila a fila; otros controladores rechazan los valores negativos y el rastreo continua con el valor predeterminado del controlador tras emitir una advertencia. Los valores negativos o no numericos se notifican y se ignoran
   * - ``query_timeout``
     - No
     - Tiempo de espera de la consulta en segundos. ``0`` significa sin limite (el valor predeterminado de JDBC). Si el parametro no se especifica, no se establece ningun tiempo de espera
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
   * - ``last_crawl_time``
     - No
     - Momento de referencia a partir del cual selecciona un rastreo incremental. Se reescribe automaticamente al finalizar el rastreo (vease "Rastreo Incremental")
   * - ``last_crawl_time_format``
     - No
     - Formato de ``last_crawl_time``. Predeterminado: ``yyyy-MM-dd HH:mm:ss``

.. note::
   Si una consulta se queda bloqueada, detener el trabajo no libera el hilo del rastreador.
   La solicitud de parada solo se comprueba entre filas, por lo que no puede interrumpir una
   llamada bloqueada dentro del controlador. Establezca ``query_timeout`` para las consultas
   que puedan tardar mucho.

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
- ``crawlingConfig`` - la configuracion del almacen de datos
- ``crawlingContext`` - el contexto del rastreo; ``crawlingContext.doc`` contiene el documento que se esta construyendo

.. note::
   Los nombres de columna deben coincidir con la etiqueta de columna (alias) de la clausula ``SELECT``.
   Cuando se usen funciones de agregacion o expresiones, asigne un alias explicito con ``AS``
   (ej. ``COUNT(*) AS total``).

.. note::
   El uso de mayusculas y minusculas en las etiquetas de columna varia segun la base de datos.
   PostgreSQL convierte a minusculas los identificadores sin comillas, H2 los convierte a
   mayusculas y MySQL los devuelve tal como se declararon. Un nombre que no se resuelve deja el
   campo sin asignar en lugar de generar un error, asi que asigne un alias explicito con ``AS``
   cuando la portabilidad sea importante.

.. warning::
   Los scripts pueden referenciar **todo el mapa de parametros del almacen de datos**, no solo
   las columnas de resultado de la consulta SQL. ``driver``, ``url``, ``username``, ``password``
   y ``sql`` son visibles como variables con el mismo nombre, por lo que una columna puede
   quedar ocultada de forma involuntaria, o el valor de un parametro puede aparecer donde se
   esperaba una columna inexistente. Cuando existen ambos, prevalece el valor de la columna.

Carga de Datos BLOB o Binarios
================================

Las columnas binarias (BLOB, ``BYTEA``, arrays de bytes y flujos binarios) se procesan
mediante el extractor de contenido (el mismo que se usa en el rastreo de archivos) y se
incorporan como texto.

CLOB, NCLOB y los flujos de caracteres **no** pasan por ningun extractor. Se leen tal cual
como texto, y las indicaciones de tipo MIME descritas a continuacion no se les aplican.

Las columnas de tipo array se convierten en sus elementos unidos por espacios. Los valores
NULL se convierten en cadenas vacias.

.. note::
   Que una columna BLOB llegue como ``java.sql.Blob`` o como array de bytes lo decide el
   controlador JDBC: MySQL y PostgreSQL devuelven un array de bytes. Ambos se extraen de la
   misma manera.

.. note::
   CLOB y NCLOB se leen enteros en memoria, sin limite de tamano. Para columnas de texto muy
   grandes, considere truncarlas en el SQL con ``SUBSTRING`` o similar. La ruta que pasa por
   el extractor si respeta la longitud maxima de contenido del rastreador.

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

Escriba ``${last_crawl_time}`` en ``sql`` y se sustituira por el momento en que se inicio el
rastreo anterior:

::

    sql=SELECT id, title, content, url, updated_at FROM articles WHERE updated_at > '${last_crawl_time}'

En la primera ejecucion se sustituye por ``1970-01-01 00:00:00``, por lo que se seleccionan
todos los registros. Una vez leido todo el conjunto de resultados, el momento de inicio de
este rastreo se reescribe como ``last_crawl_time`` en la configuracion del almacen de datos y
se usa en la siguiente ejecucion.

El formato se configura con ``last_crawl_time_format`` (predeterminado
``yyyy-MM-dd HH:mm:ss``). Debe producir algo que la base de datos acepte como literal de
marca de tiempo.

El valor es el momento en que el rastreo **se inicio**, de modo que una fila actualizada
mientras el rastreo esta en curso se recoge en la siguiente ejecucion. No se reescribe nada si
el rastreo se detiene a mitad.

.. warning::
   Un rastreo incremental no puede detectar las filas eliminadas.

   Al activarlo tambien se desactiva la limpieza que elimina los documentos que quedaron de
   rastreos anteriores (``delete_old_docs``). Sin ello, en cada ejecucion se eliminarian todos
   los documentos que no cambiaron, ya que una consulta incremental no los devuelve.

   Como resultado, un documento cuya fila se elimino de la base de datos permanece en el indice
   hasta que caduque. Ejecute periodicamente un rastreo completo, es decir, una configuracion
   sin ``${last_crawl_time}``.

   Un ``delete_old_docs`` indicado explicitamente en la configuracion del almacen de datos
   tiene prioridad.

Escribir la condicion directamente en ``sql`` sigue funcionando como antes:

::

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

.. warning::
   ``url=url`` solo hace lo que parece cuando el resultado de ``SELECT`` tiene una columna
   etiquetada como ``url``. Si no existe esa columna, el parametro del almacen de datos con el
   mismo nombre, es decir, la **URL de conexion JDBC**, se convierte en la URL del documento.
   Asigne un alias a la columna, como en ``SELECT page_url AS url``, o indiquela en el script,
   como en ``url=page_url``.

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

1. Aprovechar el cifrado automatico

   El valor de un parametro cuyo nombre coincide con ``app.encrypt.property.pattern``
   (predeterminado ``.*password|.*key|.*token|.*secret``) se cifra al guardarlo desde la
   consola de administracion y se almacena con el prefijo ``{cipher}``. ``password`` coincide
   con ese patron, por lo que no se almacena en texto plano cuando se establece desde la
   consola de administracion.

2. Usar variables de entorno

   Una variable de entorno cuyo nombre empieza por ``FESS_ENV_`` se expande dentro de un
   parametro del almacen de datos como ``${nombre de la variable}``:

   ::

       password=${FESS_ENV_DB_PASSWORD}

   Que nombres se expanden lo controla ``crawler.data.env.param.key.pattern``
   (predeterminado ``^FESS_ENV_.*``).

3. Usar usuarios de solo lectura

.. note::
   Subir ``org.codelibs.fess.ds`` a DEBUG no expone las credenciales: los valores de los
   parametros que coinciden con ``app.encrypt.property.pattern``, y las credenciales incrustadas
   en la URL JDBC, se enmascaran en el registro.

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

Cuando un rastreo falla, el mensaje del registro identifica que paso ha fallado.

Controlador JDBC No Encontrado
--------------------------------

**Sintoma**: ``The JDBC driver ... is not on the crawler classpath.``

**Solucion**:

1. Verifique que el controlador JDBC este colocado en ``app/WEB-INF/lib/`` o ``app/WEB-INF/env/crawler/lib/``
2. Verifique que el nombre de clase indicado en ``driver`` sea correcto
3. Reinicie |Fess|

Error de Conexion
------------------

**Sintoma**: ``Failed to connect to <URL>.``

**Verifique**:

1. La base de datos esta en ejecucion
2. El nombre del host y numero de puerto son correctos
3. El nombre de usuario y contrasena son correctos
4. Configuracion del firewall

Error de Consulta
------------------

**Sintoma**: ``Failed to execute the query.``

**Verifique**:

1. Ejecute la consulta SQL directamente en la base de datos para probar
2. Verifique que los nombres de columna sean correctos
3. Verifique que los nombres de tabla sean correctos

Parametros Faltantes
---------------------

**Sintoma**: ``The driver parameter is required.``, ``The url parameter is required.`` o ``The sql parameter is required.``

Falta un parametro obligatorio. Revise el campo de parametros.

Solo Fallan Algunas Filas
--------------------------

Una fila que falla no detiene el rastreo; queda registrada en "Sistema" -> "URL con Errores".
Se usa la URL del documento cuando los scripts la generaron, y
``datastore://<id de la configuracion del almacen de datos>/<numero de fila>`` cuando no.

Los Documentos No Aparecen en los Resultados de Busqueda
---------------------------------------------------------

1. Verifique que los scripts establezcan ``url``, ``title`` y ``content``
2. Verifique que el uso de mayusculas y minusculas de las etiquetas de columna coincida con el que usan los scripts (vease "Configuracion de Script")
3. Revise el numero de documentos en el registro del trabajo de rastreo

Informacion de Referencia
==========================

- :doc:`ds-overview` - Descripcion General de Conectores de Almacen de Datos
- :doc:`ds-csv` - Conector CSV
- :doc:`ds-json` - Conector JSON
- :doc:`../../admin/dataconfig-guide` - Guia de Configuracion de Almacen de Datos
- :doc:`../crawler-basic`
- :doc:`../search-basic`
