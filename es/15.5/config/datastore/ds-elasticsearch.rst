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

    hosts=http://localhost:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

Conexion con autenticacion:

::

    hosts=https://elasticsearch.example.com:9200
    index=myindex
    username=elastic
    password=changeme
    scroll_size=100
    scroll_timeout=5m

Configuracion de multiples hosts:

::

    hosts=http://es-node1:9200,http://es-node2:9200,http://es-node3:9200
    index=myindex
    scroll_size=100
    scroll_timeout=5m

Lista de parametros
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parametro
     - Requerido
     - Descripcion
   * - ``hosts``
     - Si
     - Host(s) de Elasticsearch/OpenSearch (multiples separados por comas)
   * - ``index``
     - Si
     - Nombre del indice objetivo
   * - ``username``
     - No
     - Nombre de usuario para autenticacion
   * - ``password``
     - No
     - Contrasena para autenticacion
   * - ``scroll_size``
     - No
     - Cantidad de registros por scroll (predeterminado: 100)
   * - ``scroll_timeout``
     - No
     - Timeout del scroll (predeterminado: 5m)
   * - ``query``
     - No
     - Query en JSON (predeterminado: match_all)
   * - ``fields``
     - No
     - Campos a obtener (separados por comas)

Configuracion de scripts
------------------------

Mapeo basico:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Acceso a campos anidados:

::

    url=data.metadata.url
    title=data.title
    content=data.body.content
    author=data.author.name
    created=data.created_at
    last_modified=data.updated_at

Campos disponibles
~~~~~~~~~~~~~~~~~~

- ``data.<field_name>`` - Campo del documento de Elasticsearch
- ``data._id`` - ID del documento
- ``data._index`` - Nombre del indice
- ``data._type`` - Tipo de documento (Elasticsearch anterior a 7)
- ``data._score`` - Puntuacion de busqueda

Configuracion de consultas
==========================

Obtener todos los documentos
----------------------------

Por defecto se obtienen todos los documentos.
Si no se especifica el parametro ``query``, se usa ``match_all``.

Filtrado con condiciones especificas
------------------------------------

::

    query={"query":{"term":{"status":"published"}}}

Especificacion de rango:

::

    query={"query":{"range":{"timestamp":{"gte":"2024-01-01","lte":"2024-12-31"}}}}

Multiples condiciones:

::

    query={"query":{"bool":{"must":[{"term":{"category":"news"}},{"range":{"views":{"gte":100}}}]}}}

Especificacion de ordenamiento:

::

    query={"query":{"match_all":{}},"sort":[{"timestamp":{"order":"desc"}}]}

Obtener solo campos especificos
===============================

Limitar campos a obtener con el parametro fields
------------------------------------------------

::

    hosts=http://localhost:9200
    index=myindex
    fields=title,content,url,timestamp
    scroll_size=100

Para obtener todos los campos, no especifique ``fields`` o dejelo vacio.

Ejemplos de uso
===============

Crawl basico de indice
----------------------

Parametros:

::

    hosts=http://localhost:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

Script:

::

    url=data.url
    title=data.title
    content=data.content
    created=data.created_at
    last_modified=data.updated_at

Crawl desde cluster con autenticacion
-------------------------------------

Parametros:

::

    hosts=https://es.example.com:9200
    index=products
    username=elastic
    password=changeme
    scroll_size=200
    scroll_timeout=10m

Script:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " " + data.specifications
    digest=data.category
    last_modified=data.updated_at

Crawl desde multiples indices
-----------------------------

Parametros:

::

    hosts=http://localhost:9200
    index=logs-2024-*
    query={"query":{"term":{"level":"error"}}}
    scroll_size=100

Script:

::

    url="https://logs.example.com/view/" + data._id
    title=data.message
    content=data.stack_trace
    digest=data.service + " - " + data.level
    last_modified=data.timestamp

Crawl de cluster OpenSearch
---------------------------

Parametros:

::

    hosts=https://opensearch.example.com:9200
    index=documents
    username=admin
    password=admin
    scroll_size=100
    scroll_timeout=5m

Script:

::

    url=data.url
    title=data.title
    content=data.body
    last_modified=data.modified_date

Crawl con campos limitados
--------------------------

Parametros:

::

    hosts=http://localhost:9200
    index=myindex
    fields=id,title,content,url,timestamp
    scroll_size=100

Script:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

Balanceo de carga con multiples hosts
-------------------------------------

Parametros:

::

    hosts=http://es1.example.com:9200,http://es2.example.com:9200,http://es3.example.com:9200
    index=articles
    scroll_size=100
    scroll_timeout=5m

Script:

::

    url=data.url
    title=data.title
    content=data.content
    last_modified=data.timestamp

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

1. Aumentar el ``scroll_timeout``:

   ::

       scroll_timeout=10m

2. Reducir el ``scroll_size``:

   ::

       scroll_size=50

3. Verificar los recursos del cluster

Crawl de grandes volumenes de datos
-----------------------------------

**Sintoma**: El crawl es lento o tiene timeout

**Solucion**:

1. Ajustar ``scroll_size`` (demasiado grande puede hacerlo lento):

   ::

       scroll_size=100  # predeterminado
       scroll_size=500  # mas grande

2. Limitar los campos a obtener con ``fields``
3. Filtrar solo los documentos necesarios con ``query``
4. Dividir en multiples data stores (por indice, por rango de tiempo, etc.)

Memoria insuficiente
--------------------

**Sintoma**: OutOfMemoryError

**Solucion**:

1. Reducir ``scroll_size``
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
   Los resultados de agregacion no se obtienen, solo se obtienen los documentos.

::

    query={"query":{"match_all":{}},"aggs":{"categories":{"terms":{"field":"category"}}}}

Campos de script
----------------

::

    query={"query":{"match_all":{}},"script_fields":{"full_url":{"script":"doc['protocol'].value + '://' + doc['host'].value + doc['path'].value"}}}

Script:

::

    url=data.full_url
    title=data.title
    content=data.content

Informacion de referencia
=========================

- :doc:`ds-overview` - Descripcion general de conectores de Data Store
- :doc:`ds-database` - Conector de base de datos
- :doc:`../../admin/dataconfig-guide` - Guia de configuracion de Data Store
- `Elasticsearch Documentation <https://www.elastic.co/guide/>`_
- `OpenSearch Documentation <https://opensearch.org/docs/>`_
- `Elasticsearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_
