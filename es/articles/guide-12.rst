==========================================
Buscar en bases de datos, CSV y Salesforce
==========================================

Introducción
============

El maestro de productos está en una base de datos interna; la lista de clientes, en un CSV que el sistema de gestión exporta cada noche; y el historial de oportunidades y consultas, en Salesforce.
Con frecuencia, estos datos de negocio solo se pueden buscar desde las pantallas de cada sistema.
Con los plugins de almacén de datos de Fess, puede importarlos registro a registro y encontrarlos desde la misma página de búsqueda que los documentos de los servidores de archivos y los sitios internos.

En este artículo se explica cómo configurar la importación de cada una de las tres fuentes y cómo filtrar por fuente, programar las ejecuciones y comprobar los resultados.
Los pasos comunes a todos los almacenes de datos, como la instalación de plugins, la escritura del nombre del manejador, los parámetros y el script, y la creación de trabajos, se reúnen en :doc:`datastore-basics`.
Léalo antes de continuar.
Los valores de configuración de este artículo corresponden a Fess 15.9 y a la versión 15.9.0 de cada plugin.

La configuración que crearemos
==============================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - Fuente
     - Plugin
     - Nombre del manejador
     - Qué preparar de antemano
   * - Base de datos (maestro de productos)
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - El archivo jar del controlador JDBC y un usuario de base de datos que solo pueda ejecutar SELECT
   * - CSV (lista de clientes)
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - Un directorio donde se exporten los CSV (una ubicación que el rastreador pueda leer)
   * - Salesforce (cuentas, oportunidades, casos)
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - Una aplicación conectada y un par de claves para firmar el JWT

Si ejecuta Fess con Docker, indique los tres plugins, separados por espacios, en ``environment`` de ``fess01`` en ``compose.yaml``.

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

Si los instala desde la consola de administración o con ``fess-setup``, debe reiniciar Fess.

Decida primero: quién puede ver los resultados
==============================================

Ninguno de los tres plugins traslada a Fess los permisos de acceso (ACL) del sistema de origen.
Los roles de los documentos importados se determinan únicamente por el valor del campo "Permisos" de la configuración del almacén de datos.
Este campo contiene ``{role}guest`` desde el principio, por lo que, tal cual, incluso los usuarios que no han iniciado sesión pueden buscar.

Para datos que incluyen precios o información de clientes, sustituya el valor por los grupos que deben verlos (por ejemplo, ``{group}sales``).
Todos los documentos registrados desde una misma configuración reciben los mismos permisos.
Separe los datos destinados a públicos distintos en configuraciones de almacén de datos diferentes.
Para el diseño de los grupos, consulte :doc:`guide-05`.

Base de datos: importar el maestro de productos
===============================================

Colocar el controlador JDBC
---------------------------

``fess-ds-db`` no incluye ningún controlador JDBC.
Obtenga el archivo jar del controlador adecuado para su base de datos (``postgresql-<versión>.jar`` para PostgreSQL, ``mysql-connector-j-<versión>.jar`` para MySQL) y colóquelo en el classpath del rastreador.
El rastreo de almacenes de datos se ejecuta en un proceso de rastreador independiente del propio Fess, y su classpath incluye los jar de los dos directorios siguientes.

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

En el paquete ZIP se encuentran bajo el directorio donde se descomprimió Fess; con RPM / DEB, bajo ``/usr/share/fess/``.
Después de colocar el archivo, reinicie Fess.

En la imagen de Docker, Fess también se encuentra en ``/usr/share/fess/``.
Un jar copiado dentro del contenedor desaparece cuando se vuelve a crear el contenedor, así que monte solo ese archivo jar en ``fess01`` de ``compose.yaml``.

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

Si monta el directorio completo, los jar que la imagen coloca en él dejan de verse y el rastreador no puede arrancar.
Monte siempre archivos individuales.
Tras el cambio, vuelva a crear los contenedores con ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d``.

Parámetros y SQL
----------------

Aquí usamos como ejemplo la tabla ``products`` de PostgreSQL.
Como destino de los enlaces de los resultados de búsqueda, usamos la pantalla de consulta del maestro de productos (por ejemplo, ``https://erp.example.com/products/<ID de producto>``).
En [Rastreador] > [Almacén de datos] > [Crear nuevo], seleccione ``DatabaseDataStore`` como nombre del manejador y configure los parámetros de la siguiente manera.

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

El script es el siguiente.

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

Escriba ``sql`` en una sola línea.
El SQL se envía tal cual a la base de datos, y cada fila del resultado se convierte en un documento.
Si construye la URL del enlace y el cuerpo dentro del SQL, el script solo tiene que indicar nombres de columnas.
``concat_ws`` omite las columnas NULL al concatenar, por lo que el cuerpo no queda en NULL aunque un producto no tenga descripción.
En MySQL, ``CONCAT_WS`` se comporta igual, pero ``CONCAT`` devuelve NULL para todo el resultado si algún argumento es NULL.

Si ejecuta Fess con Docker, ``localhost`` en ``url`` no apunta al servidor de base de datos, sino al propio contenedor de Fess.
Escriba el nombre de host o la dirección IP de la base de datos.

Correspondencia entre nombres de columna y script
-------------------------------------------------

En el lado derecho del script, escriba tal cual las etiquetas de columna del resultado del SELECT (los alias asignados con ``AS``).
Tenga en cuenta los tres puntos siguientes.

- Las mayúsculas y minúsculas de las etiquetas de columna dependen de la base de datos. PostgreSQL convierte a minúsculas los alias sin comillas, Oracle y H2 los convierten a mayúsculas y MySQL los devuelve tal como se escribieron. En el script, escríbalos exactamente con las mayúsculas y minúsculas que devuelve la base de datos. Si no coinciden, el campo no recibe ningún valor
- Los valores del campo de parámetros también son visibles en el script como variables con el mismo nombre. Si escribe ``url=url`` y el resultado no tiene una columna ``url``, la URL de conexión JDBC se convierte en la URL del documento. Dé a la columna del destino del enlace un nombre que no coincida con ningún parámetro, como ``page_url``
- Una consulta bloqueada no se detiene aunque detenga el trabajo. Configure siempre ``query_timeout`` (en segundos)

``fess-ds-db`` no tiene ninguna opción de rastreo incremental.
Cada ejecución lanza todo el ``sql`` y vuelve a registrar todas las filas.
En tablas con muchas filas, ejecute el trabajo en un horario en que la carga de la base de datos sea baja (consulte "Crear un trabajo para cada fuente" más adelante).

CSV: importar la lista de clientes que exporta el sistema de gestión
====================================================================

El uso básico del conector CSV se explica en la sección del ejemplo con un archivo CSV de :doc:`datastore-basics`.
Aquí solo añadimos los puntos necesarios para importar archivos CSV que el sistema de gestión exporta periódicamente.

Como ejemplo, supongamos que un sistema de gestión japonés exporta cada noche a las 2:00 un archivo ``customers_20261128.csv`` como el siguiente.
La codificación es MS932 (la variante de Windows de Shift_JIS), y la primera fila contiene encabezados en japonés (código de cliente, nombre del cliente, ubicación, departamento responsable, estado comercial).

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

Ubicación de los archivos
-------------------------

Exporte los CSV a una ruta que pueda leerse desde el servidor donde se ejecuta el rastreador de Fess.
Con Docker, monte el directorio de exportación en ``fess01`` en modo de solo lectura.

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

Parámetros y script
-------------------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- Si especifica ``directories``, se leen todos los archivos con extensión ``.csv`` / ``.tsv`` de ese directorio, empezando por el de fecha de modificación más antigua. Si cada día se exporta un archivo con la fecha en el nombre, no es necesario modificar los parámetros. Si deja los archivos antiguos, sus filas también se leen cada vez
- Los CSV exportados por Excel en japonés o por sistemas pensados para Windows en japonés suelen estar en MS932. Si especifica ``Shift_JIS``, caracteres como ``①`` o ``㈱`` se convierten en caracteres de reemplazo, así que especifique ``MS932``
- Aunque los encabezados contengan caracteres no ASCII, como aquí en japonés, ``has_header_line=true`` omite la primera fila. En el script, lo más fiable es referirse a las columnas por su número (``cell1``, ``cell2`` …). Las columnas cuyo encabezado contiene espacios o símbolos no se pueden referenciar por el nombre del encabezado
- Para archivos separados por tabulaciones, añada ``separator_character=\t``
- Las filas cuyo ``url`` resulta ser ``null`` no se registran. En este ejemplo se excluyen los clientes con estado 取引終了 (relación finalizada); solo se registran los que tienen 取引中 (activo). El número de filas excluidas aparece en ``fess-crawler.log`` como un WARN: ``Skipped 1 row(s) in ... because the script did not set the url field.``

Si se lee un archivo mientras todavía se está escribiendo, solo se registran las filas escritas hasta ese momento.
Ejecute el trabajo después de la hora en que termina la exportación del CSV.

Salesforce: importar cuentas, oportunidades y casos
===================================================

Preparación en Salesforce
-------------------------

``fess-ds-salesforce`` admite dos métodos de autenticación: ``auth_type=oauth_token`` (flujo JWT bearer) y ``auth_type=oauth_password`` (nombre de usuario y contraseña).
Aquí usamos ``oauth_token``, que no requiere guardar ninguna contraseña.
El flujo OAuth con nombre de usuario y contraseña que usa ``oauth_password`` puede estar deshabilitado, según la configuración de la organización de Salesforce.

1. Cree un par de claves y un certificado

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. En Salesforce Setup, cree una aplicación conectada, habilite la configuración de OAuth y suba ``certificate.crt`` en "Use digital signatures". Seleccione los OAuth Scopes como se indica en la referencia
3. En las políticas de la aplicación conectada, establezca "Permitted Users" en "Admin approved users are pre-authorized" y asigne el perfil o el conjunto de permisos del usuario que se usa para el rastreo
4. Anote el Consumer Key de la aplicación conectada

Las pantallas y los nombres de Salesforce pueden cambiar, así que consulte también la descripción del flujo JWT bearer en la ayuda de Salesforce para más detalles.

Fess solo puede importar los registros y campos que puede leer el usuario que se usa para el rastreo.
Si indica en ``contents`` (que se describe más adelante) un campo que ese usuario no puede leer, la obtención de ese objeto falla.

Parámetros y script
-------------------

En ``private_key``, escriba el contenido de ``private_key.pem`` en una sola línea, sustituyendo los saltos de línea por ``\n``.
El plugin solo puede leer el formato PKCS#8 (el formato que empieza por ``-----BEGIN PRIVATE KEY-----``).
Una clave que empieza por ``-----BEGIN RSA PRIVATE KEY-----``, creada con versiones antiguas de OpenSSL, debe convertirse primero con ``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem``.

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

Para usar un sandbox, configure ``base_url=https://test.salesforce.com``.

Todos los elementos del lado derecho empiezan por ``object.``.
Si los escribe sin el prefijo, como ``url=url``, la evaluación de la expresión falla y el registro no se indexa, sino que queda anotado como URL de fallo.
``object.url`` tiene la forma ``<URL de la instancia>/<ID del registro>``, y al hacer clic se abre la página del registro en Salesforce.

Limitar el alcance de la importación
------------------------------------

``fess-ds-salesforce`` siempre lee los 23 tipos de objetos estándar, entre ellos Account, Contact, Lead, Opportunity, Case, Task y User.
No hay ninguna opción para leer solo los objetos seleccionados.
Para limitar el alcance, combine los tres mecanismos siguientes.

- ``include_pattern`` / ``exclude_pattern``: expresiones regulares que deben coincidir con todo el ``object.url`` y que seleccionan los registros que se indexan. Los tres primeros caracteres de un ID de registro de Salesforce son fijos para cada objeto (Account ``001``, Opportunity ``006``, Case ``500``, etc.). El ejemplo anterior registra solo estos tres tipos. La obtención se realiza igualmente para todos los objetos; los demás registros simplemente se descartan antes de indexarse
- ``<nombre del objeto>.title`` / ``<nombre del objeto>.contents``: indican, por su nombre de API, los campos que se usan para el título y el cuerpo. Los nombres de los objetos estándar están en mayúsculas con guiones bajos, como ``ACCOUNT``, ``OPPORTUNITY`` o ``CASE``. Si no se indican, se usan los campos predeterminados del plugin
- ``custom``: indique los nombres de API de los objetos personalizados, separados por comas, para leerlos además de los objetos estándar

Los objetos personalizados no tienen campos predeterminados, así que indique siempre ``.title`` y ``.contents``.
Incluya también el campo del título entre los campos del cuerpo.
El plugin solo obtiene los campos escritos en ``.contents`` y similares, por lo que un campo que solo figure en ``.title`` no se obtiene y el título queda vacío.

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

Filtrar por fuente con etiquetas
================================

En los ejemplos anteriores, el ``label`` del script asigna ``products``, ``customers`` y ``salesforce``.
Para que aparezcan entre las opciones de etiqueta de la página de búsqueda, cree en [Rastreador] > [Etiqueta] etiquetas con el mismo "Valor" ("Rutas incluidas" puede quedar vacío).
Los valores de etiqueta solo pueden contener caracteres alfanuméricos y ``_``.

Si quiere separar los datos de Salesforce por objeto, en lugar del ``label`` del script, cree etiquetas cuyas "Rutas incluidas" comprueben los tres primeros caracteres del ID de registro.
Por ejemplo, una etiqueta con el valor ``sf_case`` y la ruta incluida ``https://example\.my\.salesforce\.com/500.*`` solo se asigna a los casos.
Si una etiqueta coincide con la URL, se pierde la etiqueta asignada por el script.
En una misma configuración de almacén de datos, use solo uno de los dos métodos (para más detalles, consulte la sección sobre etiquetas de :doc:`datastore-basics`).

Crear un trabajo para cada fuente
=================================

En el estado inicial, "Default Crawler" rastrea todas las configuraciones juntas cada día a las 0:00.
Cada fuente tiene su propio horario conveniente, así que cree un trabajo para cada configuración de almacén de datos.
En la pantalla de detalles de cada configuración, haga clic en [Crear nuevo trabajo] e introduzca la hora en formato cron en "Programación" (para el procedimiento, consulte la sección sobre programación de :doc:`datastore-basics`).

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fuente
     - Ejemplo de programación
     - Qué tener en cuenta
   * - Base de datos
     - ``0 3 * * *``
     - Como se leen todas las filas cada vez, elegir un horario en que la carga de la base de datos sea baja
   * - CSV
     - ``30 2 * * *``
     - Programarlo después de la hora en que termina la exportación
   * - Salesforce
     - ``0 7,12,18 * * *``
     - Cada ejecución crea tantos trabajos de Bulk API como objetos estándar y personalizados haya. Decidir la frecuencia según el margen que queda del límite de API de la organización

Default Crawler también sigue rastreando estas configuraciones.
Si no quiere que se ejecuten dos veces, establezca el "Estado" de la configuración del almacén de datos en "Deshabilitado" (un trabajo que especifica un ID de configuración rastrea esa configuración aunque esté deshabilitada).

Qué ocurre con las filas que desaparecen de los datos de origen
===============================================================

Aunque elimine una fila de la base de datos o una fila desaparezca del CSV, el documento correspondiente no se elimina en el siguiente rastreo.
Los documentos registrados por un almacén de datos reciben una fecha de caducidad, que se amplía cada vez que se registran.
Un documento que deja de registrarse se elimina automáticamente cuando, desde su último registro, ha pasado el número de días de "Eliminar documentos anteriores" en [Sistema] > [General] (3 días de forma predeterminada).

Este mecanismo también tiene un aspecto que requiere atención.
Si la base de datos no está accesible durante varios días seguidos y se supera ese número de días, todos los documentos de esa configuración desaparecen de los resultados de búsqueda.
Detecte pronto los fallos de importación con los métodos de la sección siguiente.

Comprobar el funcionamiento
===========================

Cómo leer el registro de trabajo, [Información del sistema] > [Información de rastreo], las URL de fallo y ``fess-crawler.log`` se explica en la sección sobre la comprobación de resultados de :doc:`datastore-basics`.
En el rastreo de almacenes de datos, el trabajo puede mostrar "OK" aunque la importación haya fallado, así que juzgue por el número de documentos y los registros.

1. En [Información del sistema] > [Búsqueda], busque ``label:products``, ``label:customers`` y ``label:salesforce``, y compare el número de resultados con los datos de origen (en una base de datos, un ``SELECT count(*)`` con las mismas condiciones que ``sql``)
2. Revise las entradas WARN y ERROR de ``fess-crawler.log``. Con la configuración de este artículo, los mensajes más habituales son los siguientes

   - ``The JDBC driver ... is not on the crawler classpath.``: la ubicación del controlador o el nombre de clase de ``driver`` no es correcto
   - ``Failed to connect to ...``: compruebe el nombre de host, el puerto, el nombre de usuario y la contraseña de la base de datos
   - ``is not a directory.`` o ``No CSV file.``: en la ruta de ``directories`` no hay ningún CSV que el rastreador pueda leer
   - ``Batch:... Failed caused by ...``: no se pudieron obtener algunos objetos de Salesforce. Compruebe los nombres de campo de ``.contents`` y los permisos sobre los campos del usuario que se usa para el rastreo
   - ``Failed to process a data crawling: <nombre de la configuración>``: falló toda la configuración. En Salesforce, los fallos de autenticación entran en este caso. Compruebe la causa en el seguimiento de pila que aparece a continuación

3. En las configuraciones cuyo campo "Permisos" haya cambiado, inicie sesión con un usuario del grupo destinatario y compruebe que los documentos aparecen en los resultados de búsqueda y que no aparecen tras cerrar la sesión

Resumen
=======

- Ninguno de los tres plugins traslada los permisos del sistema de origen, así que sustituya ``{role}guest`` en el campo "Permisos" por los grupos que deben ver los datos
- En una base de datos, coloque el controlador JDBC en el classpath del rastreador y construya la URL del enlace y el cuerpo en el SQL. Se leen todas las filas cada vez
- Lea los CSV del sistema de gestión con ``directories`` y ``file_encoding=MS932``, y refiérase a las columnas con ``cellN``. Las filas cuyo ``url`` se establece en ``null`` no se registran
- Escriba el script de Salesforce con ``object.*``. Los objetos estándar no se pueden seleccionar, así que limite el alcance con ``include_pattern`` y ``<nombre del objeto>.contents``
- Cree un trabajo para cada fuente y opere asumiendo que las filas eliminadas de los datos de origen desaparecen tras el número de días de "Eliminar documentos anteriores"

Artículos recomendados a continuación
=====================================

- Los mecanismos comunes de los almacenes de datos (scripts, permisos, etiquetas, comprobación de resultados): :doc:`datastore-basics`
- Importar Git, Confluence, Jira y Slack: :doc:`guide-06`
- Importar Google Drive, SharePoint y Box: :doc:`guide-07`
- Mostrar resultados de búsqueda distintos según el departamento: :doc:`guide-05`
- Supervisar los fallos de importación: :doc:`guide-10`

Referencias
===========

- `Conector de base de datos <https://fess.codelibs.org/es/stable/config/datastore/ds-database.html>`__
- `Conector CSV <https://fess.codelibs.org/es/stable/config/datastore/ds-csv.html>`__
- `Conector Salesforce <https://fess.codelibs.org/es/stable/config/datastore/ds-salesforce.html>`__
- `Configuración del almacén de datos <https://fess.codelibs.org/es/stable/admin/dataconfig-guide.html>`__
- `Programador <https://fess.codelibs.org/es/stable/admin/scheduler-guide.html>`__
- `Etiqueta <https://fess.codelibs.org/es/stable/admin/labeltype-guide.html>`__
- `General <https://fess.codelibs.org/es/stable/admin/general-guide.html>`__
