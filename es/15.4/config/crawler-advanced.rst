======================================
Configuración Avanzada del Rastreador
======================================

Descripción General
===================

Esta guía explica la configuración avanzada del rastreador de |Fess|.
Para la configuración básica del rastreador, consulte :doc:`crawler-basic`.

.. warning::
   Las configuraciones de esta página pueden afectar al sistema completo.
   Al modificar la configuración, realice pruebas exhaustivas antes de aplicarlas en el entorno de producción.

Configuración General
=====================

Ubicación de los Archivos de Configuración
-------------------------------------------

La configuración avanzada del rastreador se realiza en los siguientes archivos:

- **Configuración principal**: ``/etc/fess/fess_config.properties`` (o ``app/WEB-INF/classes/fess_config.properties``)
- **Configuración de longitud de contenido**: ``app/WEB-INF/classes/crawler/contentlength.xml``
- **Configuración de componentes**: ``app/WEB-INF/classes/crawler/container.xml``

Script Predeterminado
---------------------

Configura el lenguaje de script predeterminado del rastreador.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.default.script``
     - Lenguaje de script del rastreador
     - ``groovy``

::

    crawler.default.script=groovy

Pool de Hilos HTTP
------------------

Configuración del pool de hilos del rastreador HTTP.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.http.thread_pool.size``
     - Tamaño del pool de hilos HTTP
     - ``0``

::

    # 0 para configuración automática
    crawler.http.thread_pool.size=0

Configuración de Procesamiento de Documentos
=============================================

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.max.site.length``
     - Número máximo de líneas del sitio del documento
     - ``100``
   * - ``crawler.document.site.encoding``
     - Codificación del sitio del documento
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - Valor alternativo para nombres de host desconocidos
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - Usar codificación del sitio en documentos en inglés
     - ``false``
   * - ``crawler.document.append.data``
     - Agregar datos al documento
     - ``true``
   * - ``crawler.document.append.filename``
     - Agregar nombre de archivo al documento
     - ``false``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

Configuración de Procesamiento de Palabras
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.max.alphanum.term.size``
     - Longitud máxima de palabras alfanuméricas
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - Longitud máxima de palabras con símbolos
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - Eliminar palabras duplicadas
     - ``false``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Cambiar la longitud máxima alfanumérica a 50 caracteres
    crawler.document.max.alphanum.term.size=50

    # Cambiar la longitud máxima de símbolos a 20 caracteres
    crawler.document.max.symbol.term.size=20

    # Eliminar palabras duplicadas
    crawler.document.duplicate.term.removed=true

.. note::
   Aumentar ``max.alphanum.term.size`` permite indexar IDs largos, tokens, URLs, etc.
   en su forma completa, pero aumentará el tamaño del índice.

Configuración de Procesamiento de Caracteres
---------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.space.chars``
     - Definición de caracteres de espacio
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - Definición de caracteres de punto final
     - ``\u002e\u06d4...``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Valores predeterminados (incluyendo caracteres Unicode)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

Configuración de Protocolos
============================

Protocolos Compatibles
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.web.protocols``
     - Protocolos para rastreo web
     - ``http,https``
   * - ``crawler.file.protocols``
     - Protocolos para rastreo de archivos
     - ``file,smb,smb1,ftp,storage,s3,gcs``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage,s3,gcs

Parámetros de Variables de Entorno
-----------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.data.env.param.key.pattern``
     - Patrón de clave de parámetro de variable de entorno
     - ``^FESS_ENV_.*``

::

    # Variables de entorno que comienzan con FESS_ENV_ están disponibles en la configuración de rastreo
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

Configuración de robots.txt
============================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.ignore.robots.txt``
     - Ignorar robots.txt
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - Etiquetas robots a ignorar
     - (vacío)
   * - ``crawler.ignore.content.exception``
     - Ignorar excepción de contenido
     - ``true``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Ignorar robots.txt (no recomendado)
    crawler.ignore.robots.txt=false

    # Ignorar etiquetas robots específicas
    crawler.ignore.robots.tags=

    # Ignorar excepciones de contenido
    crawler.ignore.content.exception=true

.. warning::
   Configurar ``crawler.ignore.robots.txt=true`` puede violar los términos de servicio del sitio.
   Tenga cuidado al rastrear sitios externos.

Configuración de Manejo de Errores
===================================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.failure.url.status.codes``
     - Códigos de estado HTTP considerados como fallo
     - ``404``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Tratar también 403 como error además de 404
    crawler.failure.url.status.codes=404,403

Configuración de Monitoreo del Sistema
=======================================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.system.monitor.interval``
     - Intervalo de monitoreo del sistema (segundos)
     - ``60``

::

    # Monitorear el sistema cada 30 segundos
    crawler.system.monitor.interval=30

Configuración de Hot Threads
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.hotthread.ignore_idle_threads``
     - Ignorar hilos inactivos
     - ``true``
   * - ``crawler.hotthread.interval``
     - Intervalo de instantáneas
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - Número de instantáneas
     - ``10``
   * - ``crawler.hotthread.threads``
     - Número de hilos a monitorear
     - ``3``
   * - ``crawler.hotthread.timeout``
     - Tiempo de espera
     - ``30s``
   * - ``crawler.hotthread.type``
     - Tipo de monitoreo
     - ``cpu``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

Configuración de Metadatos
===========================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.metadata.content.excludes``
     - Metadatos a excluir
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - Mapeo de nombres de metadatos
     - ``title=title:string...``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Metadatos a excluir
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # Mapeo de nombres de metadatos
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

Configuración del Rastreador HTML
==================================

Configuración de XPath
----------------------

Configuración de XPath para extraer elementos HTML.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.html.content.xpath``
     - XPath del contenido
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - XPath del idioma
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - XPath del resumen
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - XPath de URL canónica
     - ``//LINK[@rel='canonical'][1]/@href``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Configuración predeterminada
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

Ejemplos de XPath Personalizados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Extraer solo un elemento div específico como contenido
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # Incluir también meta keywords en el resumen
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

Procesamiento de Etiquetas HTML
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.html.pruned.tags``
     - Etiquetas HTML a eliminar
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - Longitud máxima del resumen
     - ``120``
   * - ``crawler.document.html.default.lang``
     - Idioma predeterminado
     - (vacío)

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Agregar etiquetas a eliminar
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # Longitud del resumen a 200 caracteres
    crawler.document.html.max.digest.length=200

    # Idioma predeterminado a japonés
    crawler.document.html.default.lang=ja

Filtros de Patrón de URL
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.html.default.include.index.patterns``
     - Patrones de URL a incluir en el índice
     - (vacío)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - Patrones de URL a excluir del índice
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - Patrones de URL a incluir en resultados de búsqueda
     - (vacío)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - Patrones de URL a excluir de resultados de búsqueda
     - (vacío)

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Patrón de exclusión predeterminado
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # Indexar solo rutas específicas
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

Configuración del Rastreador de Archivos
=========================================

Configuración Básica
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.file.name.encoding``
     - Codificación del nombre de archivo
     - (vacío)
   * - ``crawler.document.file.no.title.label``
     - Etiqueta para archivos sin título
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - Ignorar contenido vacío
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - Longitud máxima del título
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - Longitud máxima del resumen
     - ``200``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Procesar nombres de archivo en Windows-31J
    crawler.document.file.name.encoding=Windows-31J

    # Etiqueta para archivos sin título
    crawler.document.file.no.title.label=Sin título

    # Ignorar archivos vacíos
    crawler.document.file.ignore.empty.content=true

    # Longitud de título y resumen
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

Procesamiento de Contenido
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.file.append.meta.content``
     - Agregar metadatos al contenido
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - Agregar cuerpo al contenido
     - ``true``
   * - ``crawler.document.file.default.lang``
     - Idioma predeterminado
     - (vacío)

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=ja

Filtros de Patrón de URL de Archivos
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.file.default.include.index.patterns``
     - Patrones a incluir en el índice
     - (vacío)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - Patrones a excluir del índice
     - (vacío)
   * - ``crawler.document.file.default.include.search.patterns``
     - Patrones a incluir en resultados de búsqueda
     - (vacío)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - Patrones a excluir de resultados de búsqueda
     - (vacío)

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Indexar solo extensiones específicas
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # Excluir carpetas temp
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

Configuración de Caché
======================

Caché de Documentos
-------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``crawler.document.cache.enabled``
     - Habilitar caché de documentos
     - ``true``
   * - ``crawler.document.cache.max.size``
     - Tamaño máximo de caché (bytes)
     - ``2621440`` (2.5MB)
   * - ``crawler.document.cache.supported.mimetypes``
     - Tipos MIME a almacenar en caché
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - Tipos MIME a tratar como HTML
     - ``text/html``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # Habilitar caché de documentos
    crawler.document.cache.enabled=true

    # Tamaño de caché a 5MB
    crawler.document.cache.max.size=5242880

    # Tipos MIME a almacenar en caché
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # Tipos MIME a tratar como HTML
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   Al habilitar la caché, se muestra un enlace de caché en los resultados de búsqueda,
   lo que permite a los usuarios ver el contenido en el momento del rastreo.

Opciones de JVM
===============

Puede configurar las opciones de JVM para el proceso del rastreador.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Propiedad
     - Descripción
     - Valor Predeterminado
   * - ``jvm.crawler.options``
     - Opciones de JVM del rastreador
     - ``-Xms128m -Xmx512m...``

Configuración Predeterminada
-----------------------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

Descripción de las Opciones Principales
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Opción
     - Descripción
   * - ``-Xms128m``
     - Tamaño inicial del heap (128MB)
   * - ``-Xmx512m``
     - Tamaño máximo del heap (512MB)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Tamaño máximo del Metaspace (128MB)
   * - ``-XX:+UseG1GC``
     - Usar recolector de basura G1
   * - ``-XX:MaxGCPauseMillis=60000``
     - Objetivo de tiempo de pausa del GC (60 segundos)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - Deshabilitar heap dump en OutOfMemory

Ejemplos de Configuración Personalizada
----------------------------------------

**Al rastrear archivos grandes:**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**Durante depuración:**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

Para más detalles, consulte :doc:`setup-memory`.

Optimización del Rendimiento
=============================

Optimización de la Velocidad de Rastreo
----------------------------------------

**1. Ajuste del Número de Hilos**

Puede mejorar la velocidad de rastreo aumentando el número de rastreos paralelos.

::

    # Ajustar el número de hilos en la configuración de rastreo de la interfaz administrativa
    Número de hilos: 10

Sin embargo, tenga cuidado con la carga en el servidor objetivo.

**2. Ajuste de Tiempos de Espera**

Para sitios con respuesta lenta, ajuste los tiempos de espera.

::

    # Agregar a "Parámetros de configuración" en la configuración de rastreo
    client.connectionTimeout=10000
    client.socketTimeout=30000

**3. Exclusión de Contenido Innecesario**

Excluir imágenes, CSS, archivos JavaScript, etc. puede mejorar la velocidad de rastreo.

::

    # Patrón de URL de exclusión
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. Configuración de Reintentos**

Ajuste el número de reintentos y el intervalo en caso de error.

::

    # Agregar a "Parámetros de configuración" en la configuración de rastreo
    client.maxRetry=3
    client.retryInterval=1000

Optimización del Uso de Memoria
--------------------------------

**1. Ajuste del Tamaño del Heap**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. Ajuste del Tamaño de Caché**

::

    crawler.document.cache.max.size=1048576  # 1MB

**3. Exclusión de Archivos Grandes**

::

    # Agregar a "Parámetros de configuración" en la configuración de rastreo
    client.maxContentLength=10485760  # 10MB

Para más detalles, consulte :doc:`setup-memory`.

Mejora de la Calidad del Índice
--------------------------------

**1. Optimización de XPath**

Excluya elementos innecesarios (navegación, publicidad, etc.).

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. Optimización del Resumen**

::

    crawler.document.html.max.digest.length=200

**3. Mapeo de Metadatos**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

Solución de Problemas
=====================

Falta de Memoria
----------------

**Síntomas:**

- Se registra ``OutOfMemoryError`` en ``fess_crawler.log``
- El rastreo se detiene a mitad de camino

**Soluciones:**

1. Aumentar el tamaño del heap del rastreador

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. Reducir el número de hilos paralelos

3. Excluir archivos grandes

Para más detalles, consulte :doc:`setup-memory`.

Rastreo Lento
-------------

**Síntomas:**

- El rastreo tarda demasiado tiempo
- Se producen tiempos de espera frecuentes

**Soluciones:**

1. Aumentar el número de hilos (tenga cuidado con la carga del servidor objetivo)

2. Ajustar los tiempos de espera

   ::

       client.connectionTimeout=5000
       client.socketTimeout=10000

3. Excluir URLs innecesarias

No se Puede Extraer Contenido Específico
-----------------------------------------

**Síntomas:**

- El texto de la página no se extrae correctamente
- La información importante no se incluye en los resultados de búsqueda

**Soluciones:**

1. Verificar y ajustar el XPath

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. Verificar las etiquetas eliminadas

   ::

       crawler.document.html.pruned.tags=script,style

3. Para contenido generado dinámicamente con JavaScript, considere métodos alternativos (como rastreo de API)

Caracteres Corruptos
--------------------

**Síntomas:**

- Se producen caracteres corruptos en los resultados de búsqueda
- Ciertos idiomas no se muestran correctamente

**Soluciones:**

1. Verificar la configuración de codificación

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. Configurar la codificación de nombres de archivo

   ::

       crawler.document.file.name.encoding=Windows-31J

3. Verificar errores de codificación en los registros

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

Mejores Prácticas
=================

1. **Verificar en Entorno de Prueba**

   Realice pruebas exhaustivas en un entorno de prueba antes de aplicar en producción.

2. **Ajuste Gradual**

   No realice cambios grandes a la configuración de una sola vez, ajuste gradualmente y verifique los efectos.

3. **Monitoreo de Registros**

   Después de cambiar la configuración, monitoree los registros para verificar que no haya errores o problemas de rendimiento.

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **Respaldo**

   Siempre realice una copia de seguridad antes de modificar archivos de configuración.

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **Documentación**

   Documente los cambios realizados en la configuración y su justificación.

Configuración del Rastreador S3/GCS
====================================

Rastreador S3
-------------

Configuración para rastrear Amazon S3 y almacenamiento compatible con S3 (MinIO, etc.).

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Parámetro
     - Descripción
     - Valor Predeterminado
   * - ``client.endpoint``
     - URL del endpoint de S3
     - (obligatorio)
   * - ``client.accessKey``
     - Clave de acceso
     - (obligatorio)
   * - ``client.secretKey``
     - Clave secreta
     - (obligatorio)
   * - ``client.region``
     - Región de AWS
     - ``us-east-1``
   * - ``client.connectTimeout``
     - Tiempo de espera de conexión (ms)
     - ``10000``
   * - ``client.readTimeout``
     - Tiempo de espera de lectura (ms)
     - ``10000``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

Escriba lo siguiente en "Parámetros de configuración" de la configuración de rastreo de archivos.

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=AKIAIOSFODNN7EXAMPLE
    client.secretKey=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    client.region=ap-northeast-1

Rastreador GCS
--------------

Configuración para rastrear Google Cloud Storage.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Parámetro
     - Descripción
     - Valor Predeterminado
   * - ``client.projectId``
     - ID del proyecto de Google Cloud
     - (obligatorio)
   * - ``client.credentialsFile``
     - Ruta del archivo JSON de la cuenta de servicio
     - (opcional)
   * - ``client.endpoint``
     - Endpoint personalizado
     - (opcional)
   * - ``client.connectTimeout``
     - Tiempo de espera de conexión (ms)
     - ``10000``
   * - ``client.writeTimeout``
     - Tiempo de espera de escritura (ms)
     - ``10000``
   * - ``client.readTimeout``
     - Tiempo de espera de lectura (ms)
     - ``10000``

Ejemplo de Configuración
~~~~~~~~~~~~~~~~~~~~~~~~~

Escriba lo siguiente en "Parámetros de configuración" de la configuración de rastreo de archivos.

::

    client.projectId=my-gcp-project
    client.credentialsFile=/etc/fess/gcs-credentials.json

.. note::
   Si omite ``credentialsFile``, se usará la variable de entorno ``GOOGLE_APPLICATION_CREDENTIALS``.

Información de Referencia
==========================

- :doc:`crawler-basic` - Configuración básica del rastreador
- :doc:`crawler-thumbnail` - Configuración de miniaturas
- :doc:`setup-memory` - Configuración de memoria
- :doc:`admin-logging` - Configuración de registros
- :doc:`search-advanced` - Configuración avanzada de búsqueda
