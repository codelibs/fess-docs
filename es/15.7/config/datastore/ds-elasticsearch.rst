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
     - ElasticsearchDataStore
   * - Habilitado
     - Activado

Configuracion de parametros
---------------------------

Conexion basica:

::

    settings.fesen.http.url=http://localhost:9200
    index=myindex
    size=100
    scroll=5m

Conexion con autenticacion:

::

    settings.fesen.http.url=https://elasticsearch.example.com:9200
    index=myindex
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    size=100
    scroll=5m

Configuracion de multiples hosts:

::

    settings.fesen.http.url=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    size=100
    scroll=5m

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - Parametro
     - Requerido
     - Descripcion
   * - ``settings.fesen.http.url``
     - No
     - Host(s) de Elasticsearch/OpenSearch (multiples separados por comas). Error de conexion si no se especifica
   * - ``index``
     - No
     - Nombre del indice objetivo (predeterminado: ``_all``). Se pueden especificar multiples indices separados por comas
   * - ``settings.fesen.username``
     - No
     - Nombre de usuario para autenticacion
   * - ``settings.fesen.password``
     - No
     - Contrasena para autenticacion
   * - ``size``
     - No
     - Cantidad de registros por scroll (predeterminado: 100)
   * - ``scroll``
     - No
     - Timeout del scroll (predeterminado: 1m)
   * - ``query``
     - No
     - Query en JSON (predeterminado: match_all). Especificar solo el cuerpo de la query (el wrapper externo ``{"query":...}`` no es necesario)
   * - ``fields``
     - No
     - Campos a obtener (separados por comas)
   * - ``timeout``
     - No
     - Timeout de la solicitud (predeterminado: 1m)
   * - ``preference``
     - No
     - Preferencia de replica de shard para la ejecucion de busqueda (predeterminado: ``_local``)
   * - ``delete.processed.doc``
     - No
     - Si se eliminan los documentos procesados del indice fuente (predeterminado: false)
   * - ``readInterval``
     - No
     - Tiempo de espera entre el procesamiento de cada documento en milisegundos (predeterminado: 0)

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
------------------------------------------------

::

    settings.fesen.http.url=http://localhost:9200
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

    settings.fesen.http.url=http://localhost:9200
    index=articles
    size=100
    scroll=5m

Script:

::

    url=source.url
    title=source.title
    content=source.content
    created=source.created_at
    last_modified=source.updated_at

Crawl desde cluster con autenticacion
-------------------------------------

Parametros:

::

    settings.fesen.http.url=https://es.example.com:9200
    index=products
    settings.fesen.username=elastic
    settings.fesen.password=changeme
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
-----------------------------

Parametros:

::

    settings.fesen.http.url=http://localhost:9200
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
---------------------------

Parametros:

::

    settings.fesen.http.url=https://opensearch.example.com:9200
    index=documents
    settings.fesen.username=admin
    settings.fesen.password=admin
    size=100
    scroll=5m

Script:

::

    url=source.url
    title=source.title
    content=source.body
    last_modified=source.modified_date

Crawl con campos limitados
--------------------------

Parametros:

::

    settings.fesen.http.url=http://localhost:9200
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
-------------------------------------

Parametros:

::

    settings.fesen.http.url=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    size=100
    scroll=5m

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
-----------------------------------

**Sintoma**: El crawl es lento o tiene timeout

**Solucion**:

1. Ajustar ``size`` (demasiado grande puede hacerlo lento):

   ::

       size=100  # predeterminado
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
----------------------------------

.. warning::
   Use certificados firmados adecuadamente en entornos de produccion.

Si usa certificados autofirmados, agregue el certificado al keystore de Java:

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Autenticacion con certificado de cliente
----------------------------------------

Si se requiere certificado de cliente, se necesitan configuraciones de parametros adicionales.
Consulte la documentacion del cliente de Elasticsearch para mas detalles.

Ejemplos de consultas avanzadas
===============================

Consulta con agregacion
-----------------------

.. note::
   El parametro ``query`` solo acepta el cuerpo de la query. Agregaciones (aggs), ordenamiento y otras
   opciones a nivel de busqueda no pueden especificarse. Solo se obtienen los documentos.

Campos de script
----------------

.. note::
   Los campos de script de Elasticsearch/OpenSearch no estan incluidos en ``_source``, por lo que no se
   puede acceder a ellos mediante el prefijo ``source.*``. Para usar campos de script, acceda a ellos
   mediante el objeto ``hit`` usando ``hit.getFields()``.

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
