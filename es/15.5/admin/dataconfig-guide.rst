=======================
Rastreo de Almacén de Datos
=======================

Descripción general
===================

|Fess| puede rastrear fuentes de datos como bases de datos y CSV.
Aquí se explica la configuración del almacén de datos necesaria para ello.

Método de gestión
==================

Método de visualización
-----------------------

Para abrir la página de lista para configurar el almacén de datos que se muestra a continuación, haga clic en [Rastreador > Almacén de datos] en el menú izquierdo.

|image0|

Para editar, haga clic en el nombre de la configuración.

Crear configuración
-------------------

Para abrir la página de configuración del almacén de datos, haga clic en el botón de nueva creación.

|image1|

Parámetros de configuración
----------------------------

Nombre
::::::

Especifique el nombre de la configuración de rastreo.

Nombre del controlador
::::::::::::::::::::::

Es el nombre del controlador que procesa el almacén de datos.

* DatabaseDataStore: Rastrea bases de datos
* CsvDataStore: Rastrea archivos CSV/TSV
* CsvListDataStore: Rastrea archivos CSV que describen rutas de archivos a indexar

Parámetros
::::::::::

Especifique los parámetros relacionados con el almacén de datos.

Script
::::::

Especifique en qué campos configurar los valores obtenidos del almacén de datos, etc.
Las expresiones se pueden describir en Groovy.

Valor de impulso
::::::::::::::::

Especifique el valor de impulso de los documentos al rastrear con esta configuración.

Permisos
::::::::

Especifique el permiso para esta configuración.
La forma de especificar permisos es, por ejemplo, para mostrar resultados de búsqueda a usuarios que pertenecen al grupo developer, especifique {group}developer.
La especificación por usuario es {user}nombre_usuario, la especificación por rol es {role}nombre_rol, y la especificación por grupo es {group}nombre_grupo.

Host virtual
::::::::::::

Especifique el nombre de host del host virtual.
Para más detalles, consulte :doc:`Host virtual en la guía de configuración <../config/virtual-host>`.

Estado
::::::

Especifique si desea utilizar esta configuración de rastreo.

Descripción
:::::::::::

Puede ingresar una descripción.

Eliminar configuración
----------------------

Haga clic en el nombre de la configuración en la página de lista y haga clic en el botón de eliminar para que aparezca una pantalla de confirmación.
Al presionar el botón de eliminar, se eliminará la configuración.

Ejemplo
=======

DatabaseDataStore
-----------------

Se explicará el rastreo de bases de datos.

Como ejemplo, se explicará asumiendo que existe la siguiente tabla en una base de datos llamada testdb en MySQL, y que se puede conectar con el nombre de usuario hoge y la contraseña fuga.

::

    CREATE TABLE doc (
        id BIGINT NOT NULL AUTO_INCREMENT,
        title VARCHAR(100) NOT NULL,
        content VARCHAR(255) NOT NULL,
        latitude VARCHAR(20),
        longitude VARCHAR(20),
        versionNo INTEGER NOT NULL,
        PRIMARY KEY (id)
    );

Aquí, se insertarán los siguientes datos.

::

    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 1', 'コンテンツ 1 です．', '37.77493', ' -122.419416', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 2', 'コンテンツ 2 です．', '34.701909', '135.494977', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 3', 'コンテンツ 3 です．', '-33.868901', '151.207091', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 4', 'コンテンツ 4 です．', '51.500152', '-0.113736', 1);
    INSERT INTO doc (title, content, latitude, longitude, versionNo) VALUES ('タイトル 5', 'コンテンツ 5 です．', '35.681137', '139.766084', 1);

Parámetros
::::::::::

Un ejemplo de configuración de parámetros sería el siguiente.

::

    driver=com.mysql.jdbc.Driver
    url=jdbc:mysql://localhost:3306/testdb?useUnicode=true&characterEncoding=UTF-8
    username=hoge
    password=fuga
    sql=select * from doc

Los parámetros están en formato "clave=valor". La descripción de las claves es la siguiente.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - driver
     - Nombre de la clase del controlador
   * - url
     - URL
   * - username
     - Nombre de usuario para conectarse a la BD
   * - password
     - Contraseña para conectarse a la BD
   * - sql
     - Sentencia SQL para obtener el objeto del rastreo

Tabla: Ejemplo de parámetros de configuración de BD


Script
::::::

Un ejemplo de configuración de script sería el siguiente.

::

    url="http://SERVERNAME/" + id
    host="SERVERNAME"
    site="SERVERNAME"
    title=title
    content=content
    cache=content
    digest=content
    anchor=
    content_length=content.length()
    last_modified=new java.util.Date()
    location=latitude + "," + longitude
    latitude=latitude
    longitude=longitude

Los parámetros están en formato "clave=valor". La descripción de las claves es la siguiente.

En el lado del valor, se describe en Groovy.
Las cadenas deben encerrarse entre comillas dobles. Si accede por nombre de columna de la base de datos, será ese valor.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - url
     - URL (Configure una URL que pueda acceder a los datos según su entorno)
   * - host
     - Nombre de host
   * - site
     - Ruta del sitio
   * - title
     - Título
   * - content
     - Contenido del documento (cadena objeto de indexación)
   * - cache
     - Caché del documento (no es objeto de indexación)
   * - digest
     - Parte del resumen que se muestra en los resultados de búsqueda
   * - anchor
     - Enlaces contenidos en el documento (normalmente no es necesario especificarlo)
   * - content_length
     - Longitud del documento
   * - last_modified
     - Fecha de última actualización del documento

Tabla: Contenido de configuración del script


Controlador
:::::::::::

Se necesita un controlador para conectarse a la base de datos. Coloque el archivo jar en app/WEB-INF/lib.

CsvDataStore
------------

Se explicará el rastreo de archivos CSV.

Por ejemplo, genere el archivo test.csv en el directorio /home/taro/csv con el siguiente contenido.
La codificación del archivo debe ser Shift_JIS.

::

    1,タイトル 1,テスト1です。
    2,タイトル 2,テスト2です。
    3,タイトル 3,テスト3です。
    4,タイトル 4,テスト4です。
    5,タイトル 5,テスト5です。
    6,タイトル 6,テスト6です。
    7,タイトル 7,テスト7です。
    8,タイトル 8,テスト8です。
    9,タイトル 9,テスト9です。


Parámetros
::::::::::

Un ejemplo de configuración de parámetros sería el siguiente.

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

Los parámetros están en formato "clave=valor". La descripción de las claves es la siguiente.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - directories
     - Directorio que contiene archivos CSV (.csv o .tsv)
   * - files
     - Archivo CSV (si se especifica directamente)
   * - fileEncoding
     - Codificación del archivo CSV
   * - separatorCharacter
     - Carácter separador


Tabla: Ejemplo de parámetros de configuración de archivo CSV


Script
::::::

Un ejemplo de configuración de script sería el siguiente.

::

    url="http://SERVERNAME/" + cell1
    host="SERVERNAME"
    site="SERVERNAME"
    title=cell2
    content=cell3
    cache=cell3
    digest=cell3
    anchor=
    content_length=cell3.length()
    last_modified=new java.util.Date()

Los parámetros están en formato "clave=valor".
Las claves son las mismas que en el caso del rastreo de bases de datos.
Los datos dentro del archivo CSV se mantienen en cell[número] (el número comienza desde 1).
Si no hay datos en una celda del archivo CSV, puede ser nulo.

EsDataStore
-----------

La fuente de obtención de datos es elasticsearch, pero el uso básico es el mismo que CsvDataStore.

Parámetros
::::::::::

Un ejemplo de configuración de parámetros sería el siguiente.

::

    settings.cluster.name=elasticsearch
    hosts=SERVERNAME:9300
    index=logindex
    type=data

Los parámetros están en formato "clave=valor". La descripción de las claves es la siguiente.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - settings.*
     - Información de configuración de elasticsearch
   * - hosts
     - elasticsearch de destino de conexión
   * - index
     - Nombre del índice
   * - type
     - Nombre del tipo
   * - query
     - Consulta de condiciones para obtener

Tabla: Ejemplo de parámetros de configuración de elasticsearch


Script
::::::

Un ejemplo de configuración de script sería el siguiente.

::

    url=source.url
    host="SERVERNAME"
    site="SERVERNAME"
    title=source.title
    content=source.content
    digest=
    anchor=
    content_length=source.size
    last_modified=new java.util.Date()

Los parámetros están en formato "clave=valor".
Las claves son las mismas que en el caso del rastreo de bases de datos.
Puede obtener y configurar valores mediante source.*.

CsvListDataStore
----------------

Se utiliza al rastrear una gran cantidad de archivos.
Al colocar un archivo CSV que describe las rutas de los archivos actualizados y rastrear solo las rutas especificadas, puede acortar el tiempo de ejecución del rastreo.

El formato para describir las rutas es el siguiente.

::

    [acción]<carácter separador>[ruta]

Especifique una de las siguientes acciones:

* create: Se creó el archivo
* modify: Se actualizó el archivo
* delete: Se eliminó el archivo

Por ejemplo, genere el archivo test.csv en el directorio /home/taro/csv con el siguiente contenido.
La codificación del archivo debe ser Shift_JIS.

Describa las rutas con la misma notación que cuando especifica rutas objetivo de rastreo en el rastreo de archivos.
Especifique como "file:/[ruta]" o "smb://[ruta]" de la siguiente manera.

::

    modify,smb://servername/data/testfile1.txt
    modify,smb://servername/data/testfile2.txt
    modify,smb://servername/data/testfile3.txt
    modify,smb://servername/data/testfile4.txt
    modify,smb://servername/data/testfile5.txt
    modify,smb://servername/data/testfile6.txt
    modify,smb://servername/data/testfile7.txt
    modify,smb://servername/data/testfile8.txt
    modify,smb://servername/data/testfile9.txt
    modify,smb://servername/data/testfile10.txt


Parámetros
::::::::::

Un ejemplo de configuración de parámetros sería el siguiente.

::

    directories=/home/taro/csv
    fileEncoding=Shift_JIS

Los parámetros están en formato "clave=valor". La descripción de las claves es la siguiente.

.. tabularcolumns:: |p{4cm}|p{8cm}|
.. list-table::

   * - directories
     - Directorio que contiene archivos CSV (.csv o .tsv)
   * - fileEncoding
     - Codificación del archivo CSV
   * - separatorCharacter
     - Carácter separador


Tabla: Ejemplo de parámetros de configuración de archivo CSV


Script
::::::

Un ejemplo de configuración de script sería el siguiente.

::

    event_type=cell1
    url=cell2

Los parámetros están en formato "clave=valor".
Las claves son las mismas que en el caso del rastreo de bases de datos.

Si se requiere autenticación en el destino del rastreo, también es necesario configurar lo siguiente.

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

.. |image0| image:: ../../../resources/images/en/15.5/admin/dataconfig-1.png
.. |image1| image:: ../../../resources/images/en/15.5/admin/dataconfig-2.png
