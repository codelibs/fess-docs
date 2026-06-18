==================================
Conector Elasticsearch/OpenSearch
==================================

Descripcion general
===================

El conector Elasticsearch/OpenSearch proporciona la funcionalidad para obtener datos
de un cluster de Elasticsearch u OpenSearch y registrarlos en el indice de |Fess|.

Esta funcionalidad requiere el plugin ``fess-ds-elasticsearch``.

Versiones compatibles
=====================

- Elasticsearch 7.x / 8.x
- OpenSearch 1.x / 2.x

Requisitos previos
==================

1. Es necesario instalar el plugin
2. Se requiere acceso de lectura al cluster de Elasticsearch/OpenSearch
3. Se necesitan permisos para ejecutar consultas

Instalacion del plugin
----------------------

Metodo 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # Colocar
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - External Elasticsearch
   * - Handler
     - ElasticsearchDataStore / ElasticsearchListDataStore
   * - Habilitado
     - Activado

.. note::
   ``ElasticsearchListDataStore`` es una extension de ``ElasticsearchDataStore`` que procesa los datos obtenidos como una lista de archivos y soporta el registro en el indice con multiples hilos.
   El numero de hilos se puede especificar con el parametro ``numOfThreads`` (predeterminado: 1).

Configuracion de parametros
---------------------------

Conexion basica:

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    size=100
    scroll=1m

Conexion con autenticacion:

::

    settings.http.hosts=https://elasticsearch.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=myindex
    size=100
    scroll=1m

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Parametro
     - Requerido
     - Descripcion
   * - ``settings.http.hosts``
     - No
     - URL del host de Elasticsearch/OpenSearch. Se pueden especificar multiples hosts separados por comas (ej: ``http://host1:9200,http://host2:9200``). Si no se especifica, se produce un error de conexion
   * - ``settings.fesen.username``
     - No
     - Nombre de usuario para autenticacion
   * - ``settings.fesen.password``
     - No
     - Contrasena para autenticacion
   * - ``index``
     - No
     - Nombre del indice objetivo (predeterminado: ``_all``). Se pueden especificar multiples indices separados por comas
   * - ``size``
     - No
     - Cantidad de registros obtenidos por scroll (si no se especifica, se usa el valor predeterminado del servidor Elasticsearch/OpenSearch)
   * - ``scroll``
     - No
     - Timeout del scroll (predeterminado: 1m)
   * - ``timeout``
     - No
     - Timeout de la solicitud (predeterminado: 1m)
   * - ``query``
     - No
     - Query en JSON (predeterminado: match_all). Especificar solo el cuerpo de la query (el wrapper externo ``{"query":...}`` no es necesario)
   * - ``fields``
     - No
     - Campos a obtener (separados por comas)
   * - ``preference``
     - No
     - Preferencia de replica de shard para la ejecucion de busqueda (predeterminado: ``_local``)
   * - ``delete.processed.doc``
     - No
     - Si se eliminan los documentos procesados del indice fuente (predeterminado: false)
   * - ``readInterval``
     - No
     - Tiempo de espera entre el procesamiento de cada documento en milisegundos (predeterminado: 0)
   * - ``numOfThreads``
     - No
     - Numero de hilos para el registro en el indice (valido solo para ``ElasticsearchListDataStore``, predeterminado: 1)

Parametros adicionales de conexion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los parametros con el prefijo ``settings.`` se pasan como configuracion del cliente interno de Elasticsearch/OpenSearch (cliente HTTP de fesen).
Las principales configuraciones adicionales son las siguientes.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Parametro
     - Descripcion
   * - ``settings.http.ssl.certificate_authorities``
     - Ruta al archivo de certificado CA de confianza (formato X.509) para conexiones HTTPS
   * - ``settings.http.compression``
     - Si se habilita la compresion HTTP (predeterminado: true)
   * - ``settings.http.proxy_host``
     - Nombre de host del servidor proxy (tambien se puede especificar ``settings.https.proxy_host``)
   * - ``settings.http.proxy_port``
     - Numero de puerto del servidor proxy (tambien se puede especificar ``settings.https.proxy_port``)
   * - ``settings.http.proxy_username``
     - Nombre de usuario para autenticacion del proxy (tambien se puede especificar ``settings.https.proxy_username``)
   * - ``settings.http.proxy_password``
     - Contrasena para autenticacion del proxy (tambien se puede especificar ``settings.https.proxy_password``)

Configuracion de scripts
------------------------

Mapeo basico:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Acceso a campos anidados:

::

    url=source.metadata.url
    title=source.title
    content=source.body.content
    author=source.author.name
    created=source.created_at
    last_modified=source.updated_at

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``source.<field_name>`` - Campo ``_source`` del documento de Elasticsearch
- ``id`` - ID del documento
- ``index`` - Nombre del indice
- ``score`` - Puntuacion de busqueda
- ``version`` - Version del documento
- ``seqNo`` - Numero de secuencia
- ``primaryTerm`` - Termino primario
- ``clusterAlias`` - Alias del cluster (para busqueda entre clusters)
- ``hit`` - Objeto SearchHit (uso avanzado)

Configuracion de consultas
==========================

Obtener todos los documentos
----------------------------

Por defecto se obtienen todos los documentos.
Si no se especifica el parametro ``query``, se usa ``match_all``.

Filtrado con condiciones especificas
------------------------------------

::

    query={"term":{"status":"published"}}

Especificacion de rango:

::

    query={"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}

Multiples condiciones:

::

    query={"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}

.. note::
   El parametro ``query`` solo acepta el cuerpo de la query. El wrapper externo ``{"query":...}`` no es necesario.
   Las opciones a nivel de busqueda como ordenamiento no pueden especificarse en este parametro.

Obtener solo campos especificos
===============================

Limitar campos a obtener con el parametro fields
-------------------------------------------------

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

Para obtener todos los campos, no especifique ``fields`` o dejelo vacio.

Ejemplos de uso
===============

Crawl basico de indice
----------------------

Parametros:

::

    settings.http.hosts=http://localhost:9200
    index=articles
    size=100
    scroll=1m

Script:

::

    url=source.url
    title=source.title
    content=source.content
    created=source.created_at
    last_modified=source.updated_at

Crawl desde cluster con autenticacion
--------------------------------------

Parametros:

::

    settings.http.hosts=https://es.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=products
    size=200
    scroll=10m

Script:

::

    url="https://shop.example.com/product/" + source.product_id
    title=source.name
    content=source.description + " " + source.specifications
    digest=source.category
    last_modified=source.updated_at

Crawl desde multiples indices
------------------------------

Parametros:

::

    settings.http.hosts=http://localhost:9200
    index=logs-2024-*
    query={"term":{"level":"error"}}
    size=100

Script:

::

    url="https://logs.example.com/view/" + id
    title=source.message
    content=source.stack_trace
    digest=source.service + " - " + source.level
    last_modified=source.timestamp

Crawl de cluster OpenSearch
----------------------------

Parametros:

::

    settings.http.hosts=https://opensearch.example.com:9200
    settings.fesen.username=admin
    settings.fesen.password=admin
    index=documents
    size=100
    scroll=1m

Script:

::

    url=source.url
    title=source.title
    content=source.body
    last_modified=source.modified_date

Crawl con campos limitados
---------------------------

Parametros:

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    size=100

Script:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Balanceo de carga con multiples hosts
--------------------------------------

Al especificar multiples hosts separados por comas en ``settings.http.hosts``, las solicitudes se distribuyen entre cada host.

Parametros:

::

    settings.http.hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=1m

Script:

::

    url=source.url
    title=source.title
    content=source.content
    last_modified=source.timestamp

Solucion de problemas
=====================

Error de conexion
-----------------

**Sintoma**: ``Connection refused`` o ``No route to host``

**Verificaciones**:

1. Verificar que la URL del host sea correcta (protocolo, nombre de host, puerto)
2. Confirmar que Elasticsearch/OpenSearch este ejecutandose
3. Verificar la configuracion del firewall
4. En caso de HTTPS, verificar que el certificado sea valido

Error de autenticacion
----------------------

**Sintoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verificaciones**:

1. Verificar que el nombre de usuario y contrasena sean correctos
2. Confirmar que el usuario tenga los permisos apropiados:

   - Permisos de lectura en el indice
   - Permisos para usar la API de scroll

3. Si Elasticsearch Security (X-Pack) esta habilitado, verificar la configuracion correcta

Indice no encontrado
--------------------

**Sintoma**: ``index_not_found_exception``

**Verificaciones**:

1. Verificar que el nombre del indice sea correcto (incluyendo mayusculas/minusculas)
2. Confirmar que el indice existe:

   ::

       GET /_cat/indices

3. Verificar que el patron de comodin sea correcto (ej: ``logs-*``)

Error de consulta
-----------------

**Sintoma**: ``parsing_exception`` o ``search_phase_execution_exception``

**Verificaciones**:

1. Verificar que el JSON de la consulta sea correcto
2. Confirmar que la consulta sea compatible con la version de Elasticsearch/OpenSearch
3. Verificar que los nombres de campo sean correctos
4. Probar ejecutando la consulta directamente en Elasticsearch/OpenSearch:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

Timeout de scroll
-----------------

**Sintoma**: ``No search context found`` o ``Scroll timeout``

**Solucion**:

1. Aumentar el ``scroll``:

   ::

       scroll=10m

2. Reducir el ``size``:

   ::

       size=50

3. Verificar los recursos del cluster

Crawl de grandes volumenes de datos
------------------------------------

**Sintoma**: El crawl es lento o tiene timeout

**Solucion**:

1. Ajustar ``size`` (demasiado grande puede hacerlo lento):

   ::

       size=100
       size=500  # mas grande

2. Limitar los campos a obtener con ``fields``
3. Filtrar solo los documentos necesarios con ``query``
4. Dividir en multiples data stores (por indice, por rango de tiempo, etc.)

Memoria insuficiente
--------------------

**Sintoma**: OutOfMemoryError

**Solucion**:

1. Reducir ``size``
2. Limitar los campos a obtener con ``fields``
3. Aumentar el tamano del heap de |Fess|
4. Excluir campos grandes (datos binarios, etc.)

Conexion SSL/TLS
================

En caso de certificado autofirmado
------------------------------------

.. warning::
   Use certificados firmados adecuadamente en entornos de produccion.

Metodo 1: Especificar el certificado CA con el parametro ``settings.http.ssl.certificate_authorities`` (recomendado)

Especifique la ruta al archivo de certificado CA de confianza (formato X.509). Este metodo no afecta al keystore global de |Fess|.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.ssl.certificate_authorities=/path/to/es-cert.crt
    index=myindex

Metodo 2: Agregar el certificado al keystore de Java

Agregue el certificado al almacen de confianza de la JVM que inicia |Fess|.

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Conexion a traves de proxy
---------------------------

Para conectarse a traves de un servidor proxy, especifique ``settings.http.proxy_host`` y ``settings.http.proxy_port``.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.proxy_host=proxy.example.com
    settings.http.proxy_port=8080
    index=myindex

Ejemplos de consultas avanzadas
================================

Consulta con agregacion
------------------------

.. note::
   El parametro ``query`` solo acepta el cuerpo de la query. Agregaciones (aggs), ordenamiento y otras
   opciones a nivel de busqueda no pueden especificarse. Solo se obtienen los documentos.

Campos de script
-----------------

.. note::
   Los campos de script de Elasticsearch/OpenSearch no estan incluidos en ``_source``, por lo que no se
   puede acceder a ellos mediante el prefijo ``source.*``. Para usar campos de script, acceda a ellos
   mediante el objeto ``hit`` usando ``hit.getFields()``.

Informacion de referencia
==========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
