==================================
Conector Elasticsearch/OpenSearch
==================================

Descripción general
===================

El conector Elasticsearch/OpenSearch proporciona la funcionalidad para obtener datos
de un cluster de Elasticsearch u OpenSearch y registrarlos en el índice de |Fess|.

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

Instalación del plugin
----------------------

Método 1: Colocar el archivo JAR directamente

::

    # Descargar desde Maven Central
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-elasticsearch/X.X.X/fess-ds-elasticsearch-X.X.X.jar

    # Colocar
    cp fess-ds-elasticsearch-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # o
    cp fess-ds-elasticsearch-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

Método 2: Instalar desde la pantalla de administración

1. Abrir "Sistema" -> "Plugins"
2. Subir el archivo JAR
3. Reiniciar |Fess|

Configuración
=============

Configure desde la pantalla de administración en "Crawler" -> "Data Store" -> "Crear nuevo".

Configuración básica
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
   ``ElasticsearchListDataStore`` es una extensión de ``ElasticsearchDataStore`` que procesa los datos obtenidos como una lista de archivos y soporta el registro en el índice con múltiples hilos.
   El número de hilos se puede especificar con el parámetro ``numOfThreads`` (predeterminado: 1).

Configuración de parámetros
---------------------------

Conexión básica:

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    size=100
    scroll=1m

Conexión con autenticación:

::

    settings.http.hosts=https://elasticsearch.example.com:9200
    settings.fesen.username=elastic
    settings.fesen.password=changeme
    index=myindex
    size=100
    scroll=1m

Lista de parámetros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parámetro
     - Requerido
     - Descripción
   * - ``settings.http.hosts``
     - No
     - URL del host de Elasticsearch/OpenSearch. Se pueden especificar múltiples hosts separados por comas (ej: ``http://host1:9200,http://host2:9200``). Si no se especifica, se produce un error de conexión
   * - ``settings.fesen.username``
     - No
     - Nombre de usuario para autenticación
   * - ``settings.fesen.password``
     - No
     - Contraseña para autenticación
   * - ``index``
     - No
     - Nombre del índice objetivo (predeterminado: ``_all``). Se pueden especificar múltiples indices separados por comas
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
     - Preferencia de réplica de shard para la ejecución de búsqueda (predeterminado: ``_local``)
   * - ``delete.processed.doc``
     - No
     - Si se eliminan los documentos procesados del índice fuente (predeterminado: false)
   * - ``readInterval``
     - No
     - Tiempo de espera entre el procesamiento de cada documento en milisegundos (predeterminado: 0)
   * - ``numOfThreads``
     - No
     - Número de hilos para el registro en el índice (válido solo para ``ElasticsearchListDataStore``, predeterminado: 1)

Parámetros adicionales de conexión
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los parámetros con el prefijo ``settings.`` se pasan como configuración del cliente interno de Elasticsearch/OpenSearch (cliente HTTP de fesen).
Las principales configuraciones adicionales son las siguientes.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Parámetro
     - Descripción
   * - ``settings.http.ssl.certificate_authorities``
     - Ruta al archivo de certificado CA de confianza (formato X.509) para conexiones HTTPS
   * - ``settings.http.compression``
     - Si se habilita la compresión HTTP (predeterminado: true)
   * - ``settings.http.proxy_host``
     - Nombre de host del servidor proxy (también se puede especificar ``settings.https.proxy_host``)
   * - ``settings.http.proxy_port``
     - Número de puerto del servidor proxy (también se puede especificar ``settings.https.proxy_port``)
   * - ``settings.http.proxy_username``
     - Nombre de usuario para autenticación del proxy (también se puede especificar ``settings.https.proxy_username``)
   * - ``settings.http.proxy_password``
     - Contraseña para autenticación del proxy (también se puede especificar ``settings.https.proxy_password``)

Configuración de scripts
------------------------

Mapeo básico:

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
- ``index`` - Nombre del índice
- ``score`` - Puntuación de búsqueda
- ``versión`` - Versión del documento
- ``seqNo`` - Número de secuencia
- ``primaryTerm`` - Término primario
- ``clusterAlias`` - Alias del cluster (para búsqueda entre clusters)
- ``hit`` - Objeto SearchHit (uso avanzado)

Configuración de consultas
==========================

Obtener todos los documentos
----------------------------

Por defecto se obtienen todos los documentos.
Si no se especifica el parámetro ``query``, se usa ``match_all``.

Filtrado con condiciones específicas
------------------------------------

::

    query={"term":{"status":"published"}}

Especificación de rango:

::

    query={"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}

Múltiples condiciones:

::

    query={"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}

.. note::
   El parámetro ``query`` solo acepta el cuerpo de la query. El wrapper externo ``{"query":...}`` no es necesario.
   Las opciones a nivel de búsqueda como ordenamiento no pueden especificarse en este parámetro.

Obtener solo campos específicos
===============================

Limitar campos a obtener con el parámetro fields
-------------------------------------------------

::

    settings.http.hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    size=100

Para obtener todos los campos, no especifique ``fields`` o déjelo vacio.

Ejemplos de uso
===============

Crawl básico de índice
----------------------

Parámetros:

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

Crawl desde cluster con autenticación
--------------------------------------

Parámetros:

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

Crawl desde múltiples indices
------------------------------

Parámetros:

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

Parámetros:

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

Parámetros:

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

Balanceo de carga con múltiples hosts
--------------------------------------

Al especificar múltiples hosts separados por comas en ``settings.http.hosts``, las solicitudes se distribuyen entre cada host.

Parámetros:

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

Solución de problemas
=====================

Error de conexión
-----------------

**Síntoma**: ``Connection refused`` o ``No route to host``

**Verificaciones**:

1. Verificar que la URL del host sea correcta (protocolo, nombre de host, puerto)
2. Confirmar que Elasticsearch/OpenSearch esté ejecutándose
3. Verificar la configuración del firewall
4. En caso de HTTPS, verificar que el certificado sea válido

Error de autenticación
----------------------

**Síntoma**: ``401 Unauthorized`` o ``403 Forbidden``

**Verificaciones**:

1. Verificar que el nombre de usuario y contraseña sean correctos
2. Confirmar que el usuario tenga los permisos apropiados:

   - Permisos de lectura en el índice
   - Permisos para usar la API de scroll

3. Si Elasticsearch Security (X-Pack) está habilitado, verificar la configuración correcta

Índice no encontrado
--------------------

**Síntoma**: ``index_not_found_exception``

**Verificaciones**:

1. Verificar que el nombre del índice sea correcto (incluyendo mayúsculas/minúsculas)
2. Confirmar que el índice existe:

   ::

       GET /_cat/indices

3. Verificar que el patrón de comodín sea correcto (ej: ``logs-*``)

Error de consulta
-----------------

**Síntoma**: ``parsing_exception`` o ``search_phase_execution_exception``

**Verificaciones**:

1. Verificar que el JSON de la consulta sea correcto
2. Confirmar que la consulta sea compatible con la versión de Elasticsearch/OpenSearch
3. Verificar que los nombres de campo sean correctos
4. Probar ejecutando la consulta directamente en Elasticsearch/OpenSearch:

   ::

       POST /myindex/_search
       {
         "query": {...}
       }

Timeout de scroll
-----------------

**Síntoma**: ``No search context found`` o ``Scroll timeout``

**Solución**:

1. Aumentar el ``scroll``:

   ::

       scroll=10m

2. Reducir el ``size``:

   ::

       size=50

3. Verificar los recursos del cluster

Crawl de grandes volúmenes de datos
------------------------------------

**Síntoma**: El crawl es lento o tiene timeout

**Solución**:

1. Ajustar ``size`` (demasiado grande puede hacerlo lento):

   ::

       size=100
       size=500  # mas grande

2. Limitar los campos a obtener con ``fields``
3. Filtrar solo los documentos necesarios con ``query``
4. Dividir en múltiples data stores (por índice, por rango de tiempo, etc.)

Memoria insuficiente
--------------------

**Síntoma**: OutOfMemoryError

**Solución**:

1. Reducir ``size``
2. Limitar los campos a obtener con ``fields``
3. Aumentar el tamaño del heap de |Fess|
4. Excluir campos grandes (datos binarios, etc.)

Conexión SSL/TLS
================

En caso de certificado autofirmado
------------------------------------

.. warning::
   Use certificados firmados adecuadamente en entornos de producción.

Método 1: Especificar el certificado CA con el parámetro ``settings.http.ssl.certificate_authorities`` (recomendado)

Especifique la ruta al archivo de certificado CA de confianza (formato X.509). Este método no afecta al keystore global de |Fess|.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.ssl.certificate_authorities=/path/to/es-cert.crt
    index=myindex

Método 2: Agregar el certificado al keystore de Java

Agregue el certificado al almacén de confianza de la JVM que inicia |Fess|.

::

    keytool -import -alias es-cert -file es-cert.crt -keystore $JAVA_HOME/lib/security/cacerts

Conexión a través de proxy
---------------------------

Para conectarse a través de un servidor proxy, especifique ``settings.http.proxy_host`` y ``settings.http.proxy_port``.

::

    settings.http.hosts=https://es.example.com:9200
    settings.http.proxy_host=proxy.example.com
    settings.http.proxy_port=8080
    index=myindex

Ejemplos de consultas avanzadas
================================

Consulta con agregación
------------------------

.. note::
   El parámetro ``query`` solo acepta el cuerpo de la query. Agregaciones (aggs), ordenamiento y otras
   opciones a nivel de búsqueda no pueden especificarse. Solo se obtienen los documentos.

Campos de script
-----------------

.. note::
   Los campos de script de Elasticsearch/OpenSearch no están incluidos en ``_source``, por lo que no se
   puede acceder a ellos mediante el prefijo ``source.*``. Para usar campos de script, acceda a ellos
   mediante el objeto ``hit`` usando ``hit.getFields()``.

Información de referencia
==========================

- :doc:`ds-overview` - Descripción general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guía de configuración de Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
