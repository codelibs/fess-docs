=============================
Fess Configuration Properties
=============================

Every configuration property Fess reads, with its description and its default value.
The values themselves live in ``fess_config.properties``; see :doc:`crawler-advanced`
for how to override them.

The tables below are generated from ``fess_config.properties``. To correct a
description, change the comment above the property in the Fess repository. To translate
one, fill in ``properties.po`` beside this file.

.. GENERATED-BEGIN: properties -- from fess_config.properties via tools/update_properties_doc.sh
.. DO NOT EDIT. Descriptions and headings come from fess_config.properties in the
.. fess repository; translations come from properties.po beside this file.
.. Regenerate with tools/update_properties_doc.sh.

Núcleo
------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - Título del dominio para el registro y la visualización.
    - ``Fess``

.. list-table:: Motor de búsqueda
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - Tipo de backend del motor de búsqueda. Valores válidos: default (OpenSearch con los plugins de CodeLibs), vanilla (OpenSearch sin los plugins de CodeLibs), aws (vanilla con tratamiento específico para AWS). cloud es un alias obsoleto de vanilla.
    - ``default``
  * - search_engine.http.url
    - URL del endpoint HTTP del motor de búsqueda. En entornos IPv6, use corchetes alrededor de la dirección IPv6 (p. ej., http://[::1]:9200)
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - Ruta a las autoridades de certificación SSL para las conexiones HTTP seguras.
    - (empty)
  * - search_engine.username
    - Nombre de usuario para autenticarse en el motor de búsqueda.
    - (empty)
  * - search_engine.password
    - Contraseña para autenticarse en el motor de búsqueda.
    - (empty)
  * - search_engine.heartbeat_interval
    - Intervalo (ms) de las comprobaciones de heartbeat al motor de búsqueda.
    - ``10000``
  * - app.cipher.algorithm
    - Algoritmo de cifrado utilizado para el cifrado.
    - ``aes``
  * - app.cipher.key
    - Clave secreta para el cifrado (cambie este valor en producción).
    - ``___change__me___``
  * - app.digest.algorithm
    - Algoritmo para el cálculo del digest.
    - ``sha256``
  * - app.password.algorithm
    - Hash de contraseñas (nuevo mecanismo, compatible con Spring Security v5.8) Admitido: bcrypt (únicamente, por ahora)
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - Costo de BCrypt (rondas logarítmicas). 10 coincide con el valor predeterminado de Spring Security v5.8. Rango: 4-31.
    - ``10``
  * - app.password.upgrade.enabled
    - Re-hash diferido al iniciar sesión correctamente para los hashes heredados.
    - ``true``
  * - app.encrypt.property.pattern
    - NOTA: app.digest.algorithm se conserva únicamente para la verificación HEREDADA de contraseñas (hashes anteriores a la actualización que no tienen el prefijo {id}). No lo utilice para contraseñas nuevas. Patrón de expresión regular de las propiedades que se cifran.
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - Patrón de expresión regular de los valores sensibles que se enmascaran en los registros de depuración (coincidencia sin distinguir mayúsculas y minúsculas con las claves de propiedades y de variables de entorno).
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - Nombres de extensiones para la personalización de la aplicación.
    - (empty)
  * - app.audit.log.format
    - Formato del registro de auditoría.
    - (empty)
  * - script.audit.log.enabled
    - Configuración del registro de auditoría de scripts.
    - ``true``
  * - script.audit.log.max.length
    - Número máximo de caracteres del texto del script que se conservan en una entrada del registro de auditoría de scripts; el texto más largo se trunca.
    - ``100``
  * - jvm.crawler.options
    - Opciones de JVM para el proceso del rastreador.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Dhttp.maxConnections=20``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx512m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:-OmitStackTraceInFastThrow``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=5``
      | ``-Djcifs.client.responseTimeout=30000``
      | ``-Djcifs.client.soTimeout=35000``
      | ``-Djcifs.client.connTimeout=60000``
      | ``-Djcifs.client.sessionTimeout=60000``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j.skipJansi=true``
      | ``-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider``
      | ``-Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true``
  * - jvm.suggest.options
    - Opciones de JVM (separadas por saltos de línea) que se pasan al proceso hijo del creador de sugerencias.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx256m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=30``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
  * - jvm.chunk.options
    - Opciones de JVM para el proceso del indexador de vectores de chunks. Presupuesto de heap. Esta JVM hija solo se inicia mientras se ejecuta el trabajo "Content Chunk Vector Indexer", por lo que un -Xmx generoso no cuesta nada cuando la división del contenido en chunks está desactivada. El conjunto vivo está dominado por los lotes en curso, cada uno de los cuales conserva, por documento, el _source completo, las cadenas de chunks del documento y los vectores de embedding del documento: content_chunker.job.bulk_size (valor predeterminado 20) x content_chunker.max_chunks_per_document (valor predeterminado 1000) x content_chunker.embedding.dimension (valor predeterminado 768) x 4 bytes por float x content_chunker.job.concurrency (valor predeterminado 2) = ~117 MB solo de vectores, antes de las cadenas de chunks y los documentos de origen. Con los valores predeterminados incluidos, el peor caso es de aproximadamente 190-250 MB vivos (y ~235 MB solo de vectores con dimension=1536), lo que no cabe en un heap de 256 MB con ningún margen para el GC. Aumente -Xmx todavía más si aumenta bulk_size, max_chunks_per_document, concurrency o la dimensión del embedding.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx1g``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=30``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
  * - jvm.thumbnail.options
    - Opciones de JVM para el proceso de miniaturas.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx256m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:-OmitStackTraceInFastThrow``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=4m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=50``
      | ``-Djcifs.client.responseTimeout=30000``
      | ``-Djcifs.client.soTimeout=35000``
      | ``-Djcifs.client.connTimeout=60000``
      | ``-Djcifs.client.sessionTimeout=60000``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
      | ``-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider``
      | ``-Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true``

.. list-table:: Trabajo
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - IDs de trabajos del sistema para los trabajos programados.
    - ``default_crawler``
  * - job.template.title.web
    - Plantilla del título del trabajo del rastreador web.
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - Plantilla del título del trabajo del rastreador de archivos.
    - ``File Crawler - {0}``
  * - job.template.title.data
    - Plantilla del título del trabajo del rastreador de almacén de datos.
    - ``Data Crawler - {0}``
  * - job.template.script
    - Plantilla de script para la ejecución de trabajos.
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - Número máximo de procesos del rastreador.
    - ``0``
  * - job.default.script
    - Lenguaje de script predeterminado para los trabajos.
    - ``javascript``
  * - job.system.property.filter.pattern
    - Patrón para filtrar las propiedades del sistema para los trabajos.
    - (empty)
  * - processors
    - Número de procesadores que se utilizan.
    - ``0``
  * - java.command.path
    - Ruta del comando Java.
    - ``java``
  * - python.command.path
    - Ruta del comando Python.
    - ``python``
  * - path.encoding
    - Codificación de las rutas de archivo.
    - ``UTF-8``
  * - use.own.tmp.dir
    - Indica si se utiliza un directorio temporal dedicado.
    - ``true``
  * - max.log.output.length
    - Longitud máxima de la salida del registro.
    - ``4000``
  * - adaptive.load.control
    - Valor del control de carga adaptativo.
    - ``50``
  * - web.load.control
    - Umbral de CPU (%) para el control de carga de las solicitudes web. Devuelve 429 cuando la CPU >= este valor. (100: deshabilitado)
    - ``100``
  * - api.load.control
    - Umbral de CPU (%) para el control de carga de las solicitudes de API. Devuelve 429 cuando la CPU >= este valor. (100: deshabilitado)
    - ``100``
  * - load.control.monitor.interval
    - Intervalo (segundos) para monitorear la carga de CPU de OpenSearch.
    - ``1``
  * - supported.languages
    - Idiomas admitidos.
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - Longitud del token de acceso de la API.
    - ``60``
  * - api.access.token.request.parameter
    - Parámetro de solicitud del token de acceso de la API.
    - (empty)
  * - api.admin.access.permissions
    - Permisos para el acceso de administración de la API.
    - ``Radmin-api``
  * - api.search.accept.referers
    - Referers aceptados para la búsqueda por API.
    - (empty)
  * - api.search.scroll
    - Indica si se habilita scroll para la búsqueda por API.
    - ``false``
  * - api.search.export
    - Indica si se habilita la exportación por parte del usuario final de los resultados de búsqueda (CSV/JSON) en /api/v2/documents/export.
    - ``false``
  * - api.search.export.max.size
    - Número máximo de documentos que escribe una exportación de resultados de búsqueda.
    - ``1000``
  * - api.search.export.fields
    - Campos que escribe la exportación de resultados de búsqueda (separados por comas). Se ignora un campo que no es un campo de respuesta de la API.
    - ``title,url_link,last_modified,content_length,filetype``
  * - api.search.export.rate.limit.per.minute
    - Número máximo de exportaciones de resultados de búsqueda por minuto para cada usuario (cada IP de cliente en el caso de un invitado). 0 o menos deshabilita el límite.
    - ``10``
  * - api.json.response.headers
    - Encabezados de la respuesta JSON de la API. Access-Control-\* y Timing-Allow-Origin se ignoran aquí (CORS se controla mediante api.cors.\* / CorsFilter). No establezca Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - Indica si se incluyen excepciones en la respuesta JSON de la API.
    - ``false``
  * - api.gsa.response.headers
    - Encabezados de la respuesta GSA de la API. Access-Control-\* y Timing-Allow-Origin se ignoran aquí (CORS se controla mediante api.cors.\* / CorsFilter). No establezca Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - Indica si se incluyen excepciones en la respuesta GSA de la API.
    - ``false``
  * - api.dashboard.response.headers
    - Encabezados de la respuesta del panel de control de la API. Access-Control-\* y Timing-Allow-Origin se ignoran aquí (CORS se controla mediante api.cors.\* / CorsFilter). No establezca Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - Orígenes permitidos para CORS. "\*" devuelve un "\*" literal (el Origin de la solicitud NO se refleja) y deshabilita las credenciales. Establezca orígenes explícitos (separados por saltos de línea o comas) para permitir el acceso entre orígenes con credenciales.
    - ``*``
  * - api.cors.allow.methods
    - Métodos HTTP permitidos para CORS.
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - Edad máxima (max age) de las solicitudes preflight de CORS.
    - ``3600``
  * - api.cors.allow.headers
    - Encabezados de solicitud permitidos para el preflight de CORS. Se devuelve una lista estática (Access-Control-Request-Headers no se refleja). Incluye X-Fess-CSRF-Token para las SPA de origen cruzado que envían el token CSRF.
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - Indica si se permiten las credenciales para CORS. Solo se respeta cuando coincide exactamente con un Origin explícito; se ignora cuando api.cors.allow.origin es "\*".
    - ``true``
  * - api.jsonp.enabled
    - Indica si se habilita JSONP para la API.
    - ``false``
  * - api.ping.search_engine.fields
    - Campos para el ping de la API al motor de búsqueda.
    - ``status,timed_out``

Límite de tasa
--------------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - Indica si el límite de tasa está habilitado.
    - ``false``
  * - rate.limit.requests.per.window
    - Número máximo de solicitudes permitidas por ventana.
    - ``100``
  * - rate.limit.window.ms
    - Tamaño de la ventana en milisegundos.
    - ``60000``
  * - rate.limit.block.duration.ms
    - Duración en milisegundos del bloqueo de una IP cuando se excede el límite.
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Valor del encabezado Retry-After en segundos.
    - ``60``
  * - rate.limit.whitelist.ips
    - Lista de IPs incluidas en la lista de permitidos, separadas por comas (p. ej., 127.0.0.1,::1).
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - Lista de IPs bloqueadas, separadas por comas.
    - (empty)
  * - rate.limit.trusted.proxies
    - Lista de IPs de proxies de confianza, separadas por comas. Solo se confía en X-Forwarded-For/X-Real-IP procedentes de estas IPs.
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - Número de solicitudes entre las operaciones de limpieza para evitar fugas de memoria.
    - ``1000``
  * - virtual.host.headers
    - Host virtual: Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - Nombre de host del servidor proxy HTTP.
    - (empty)
  * - http.proxy.port
    - Número de puerto del servidor proxy HTTP (p. ej., 8080).
    - ``8080``
  * - http.proxy.username
    - Nombre de usuario para la autenticación del proxy HTTP.
    - (empty)
  * - http.proxy.password
    - Contraseña para la autenticación del proxy HTTP.
    - (empty)
  * - http.fileupload.max.size
    - Tamaño máximo (bytes) de las cargas de archivos HTTP.
    - ``262144000``
  * - http.fileupload.threshold.size
    - Tamaño umbral (bytes) para el almacenamiento en búfer de las cargas de archivos HTTP.
    - ``262144``
  * - http.fileupload.max.file.count
    - Número máximo de archivos permitidos por carga HTTP.
    - ``10``

Índice
------

.. list-table:: Rastreador común
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - Número de hilos para el rastreo HTTP.
    - ``0``
  * - crawler.data.serializer
    - Tipo de serializador para los datos del rastreador (p. ej., kryo).
    - ``kryo``
  * - crawler.document.max.site.length
    - Longitud máxima del nombre del sitio en los documentos.
    - ``100``
  * - crawler.document.site.encoding
    - Codificación de los nombres de sitio en los documentos.
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - Nombre de host que se utiliza cuando es desconocido en los documentos.
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - Indica si se utiliza la codificación del sitio para los documentos en inglés.
    - ``false``
  * - crawler.document.append.data
    - Indica si se anexan datos a los documentos.
    - ``true``
  * - crawler.document.append.filename
    - Indica si se anexa el nombre de archivo a los documentos.
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - Tamaño máximo de los términos alfanuméricos en los documentos.
    - ``20``
  * - crawler.document.max.symbol.term.size
    - Tamaño máximo de los términos de símbolos en los documentos.
    - ``10``
  * - crawler.document.duplicate.term.removed
    - Indica si se eliminan los términos duplicados en los documentos.
    - ``false``
  * - crawler.document.space.chars
    - Caracteres de espacio Unicode para el análisis de documentos.
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - Caracteres de punto final Unicode para el análisis de documentos.
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - Codificación de los datos de rastreo.
    - ``UTF-8``
  * - crawler.web.protocols
    - Protocolos web admitidos para el rastreo.
    - ``http,https``
  * - crawler.file.protocols
    - Protocolos de archivo admitidos para el rastreo.
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - Patrón de las claves de variables de entorno en los datos de rastreo.
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - Indica si se ignora robots.txt durante el rastreo.
    - ``false``
  * - crawler.ignore.robots.tags
    - Indica si se ignoran las etiquetas meta robots durante el rastreo.
    - ``false``
  * - crawler.ignore.content.exception
    - Indica si se ignoran las excepciones de contenido durante el rastreo.
    - ``true``
  * - crawler.failure.url.status.codes
    - Códigos de estado HTTP considerados como URLs de fallo.
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - Intervalo (segundos) del monitor del sistema durante el rastreo.
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - Indica si se ignoran los hilos inactivos en el monitoreo de hot threads.
    - ``true``
  * - crawler.hotthread.interval
    - Intervalo del monitoreo de hot threads (p. ej., 500ms).
    - ``500ms``
  * - crawler.hotthread.snapshots
    - Número de instantáneas del monitoreo de hot threads.
    - ``10``
  * - crawler.hotthread.threads
    - Número de hilos del monitoreo de hot threads.
    - ``3``
  * - crawler.hotthread.timeout
    - Tiempo de espera del monitoreo de hot threads (p. ej., 30s).
    - ``30s``
  * - crawler.hotthread.type
    - Tipo de monitoreo de hot threads (p. ej., cpu).
    - ``cpu``
  * - crawler.metadata.content.excludes
    - Campos de metadatos que se excluyen del contenido del documento.
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - Mapeo de los nombres de metadatos del documento.
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``
      | ``frontmatter.title=title:string``

.. list-table:: Rastreador HTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - XPath para extraer el contenido principal de los documentos HTML.
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - XPath para extraer el atributo de idioma de los documentos HTML.
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - XPath para extraer el digest (descripción) de los documentos HTML.
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - XPath para extraer la URL canónica de los documentos HTML.
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - Etiquetas HTML que se podan (eliminan) durante el procesamiento de documentos.
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - Longitud máxima del digest extraído de los documentos HTML.
    - ``120``
  * - crawler.document.html.default.lang
    - Idioma predeterminado de los documentos HTML.
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - Patrones que se incluyen en el procesamiento de indexación HTML.
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - Patrones que se excluyen del procesamiento de indexación HTML.
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - Patrones que se incluyen en el procesamiento de búsqueda HTML.
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - Patrones que se excluyen del procesamiento de búsqueda HTML.
    - (empty)

.. list-table:: Rastreador de archivos
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - Codificación de los nombres de archivo en los documentos.
    - (empty)
  * - crawler.document.file.no.title.label
    - Etiqueta que se utiliza cuando un archivo no tiene título.
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - Indica si se ignoran los archivos con contenido vacío.
    - ``false``
  * - crawler.document.file.max.title.length
    - Longitud máxima del título de archivo en los documentos.
    - ``100``
  * - crawler.document.file.max.digest.length
    - Longitud máxima del digest de archivo en los documentos.
    - ``200``
  * - crawler.document.file.append.meta.content
    - Indica si se anexa el contenido meta de los archivos.
    - ``true``
  * - crawler.document.file.append.body.content
    - Indica si se anexa el contenido del cuerpo de los archivos.
    - ``true``
  * - crawler.document.file.default.lang
    - Idioma predeterminado de los documentos de archivo.
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - Patrones que se incluyen en el procesamiento de indexación de archivos.
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - Patrones que se excluyen del procesamiento de indexación de archivos.
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - Patrones que se incluyen en el procesamiento de búsqueda de archivos.
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - Patrones que se excluyen del procesamiento de búsqueda de archivos.
    - (empty)
  * - crawler.document.file.owner.enabled
    - Indica si se indexa el propietario de los archivos rastreados (SMB, sistema de archivos local y FTP). El parámetro de configuración de rastreo config.owner.enabled lo sobrescribe.
    - ``true``
  * - crawler.document.file.last.modifier.enabled
    - Indica si se indexa el último modificador de los archivos rastreados, leído de los metadatos del documento y, en su defecto, del propietario del archivo. El parámetro de configuración de rastreo config.last.modifier.enabled lo sobrescribe.
    - ``true``

.. list-table:: Caché del rastreador
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - Indica si la caché de documentos está habilitada.
    - ``true``
  * - crawler.document.cache.max.size
    - Tamaño máximo (bytes) de la caché de documentos.
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - Tipos MIME admitidos para la caché de documentos.
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation Tipos MIME para la caché de documentos HTML.
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - Mapeos de anulación de extensión a tipo MIME para la detección del tipo MIME (uno por línea: .ext=mime/type).
    - (empty)
  * - crawler.document.ocr.enabled
    - Indica si se extrae texto de imágenes y de PDF escaneados con Tesseract OCR (requiere el comando tesseract).
    - ``false``
  * - crawler.document.ocr.language
    - Idiomas de Tesseract OCR, unidos con '+' (p. ej. jpn+eng).
    - ``eng``
  * - crawler.document.ocr.timeout
    - Tiempo de espera en segundos de una ejecución de Tesseract OCR.
    - ``120``

.. list-table:: Indexador
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - Indica si se habilita el volcado de hilos (thread dump) para el indexador.
    - ``true``
  * - indexer.unprocessed.document.size
    - Número máximo de documentos sin procesar para el indexador.
    - ``1000``
  * - indexer.click.count.enabled
    - Indica si se habilita el seguimiento del recuento de clics en el indexador.
    - ``true``
  * - indexer.favorite.count.enabled
    - Indica si se habilita el seguimiento del recuento de favoritos en el indexador.
    - ``true``
  * - indexer.webfs.commit.margin.time
    - Margen de tiempo de commit (ms) para webfs en el indexador.
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - Número máximo de listas vacías para webfs en el indexador.
    - ``3600``
  * - indexer.webfs.update.interval
    - Intervalo de actualización (ms) para webfs en el indexador.
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - Tamaño máximo de la caché de documentos para webfs en el indexador.
    - ``10``
  * - indexer.webfs.max.document.request.size
    - Tamaño máximo de solicitud de documentos (bytes) para webfs en el indexador.
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - Tamaño máximo de la caché de documentos para datos en el indexador.
    - ``10000``
  * - indexer.data.max.document.request.size
    - Tamaño máximo de solicitud de documentos (bytes) para datos en el indexador.
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - Tamaño máximo de la caché de eliminación para datos en el indexador.
    - ``100``
  * - indexer.data.max.redirect.count
    - Número máximo de redirecciones para datos en el indexador.
    - ``10``
  * - indexer.language.fields
    - Campos utilizados para la detección de idioma en el indexador.
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - Longitud del texto para la detección de idioma en el indexador.
    - ``1000``
  * - indexer.max.result.window.size
    - Tamaño máximo de la ventana de resultados para el indexador.
    - ``10000``
  * - indexer.max.search.doc.size
    - Número máximo de documentos de búsqueda para el indexador.
    - ``50000``

.. list-table:: Configuración del índice
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - Tipo de códec del índice.
    - ``default``
  * - index.number_of_shards
    - Número de shards primarios del índice.
    - ``5``
  * - index.auto_expand_replicas
    - Configuración de expansión automática de réplicas (auto expand replicas) del índice.
    - ``0-1``
  * - index.id.digest.algorithm
    - Algoritmo de digest para los ID del índice.
    - ``SHA-512``
  * - index.user.initial_password
    - Contraseña inicial del usuario del índice.
    - ``admin``

.. list-table:: Nombres de campos
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - Nombre del campo del recuento de favoritos en el índice.
    - ``favorite_count``
  * - index.field.click_count
    - Nombre del campo del recuento de clics en el índice.
    - ``click_count``
  * - index.field.config_id
    - Nombre del campo del ID de configuración en el índice.
    - ``config_id``
  * - index.field.expires
    - Nombre del campo de la fecha de expiración en el índice.
    - ``expires``
  * - index.field.url
    - Nombre del campo de la URL en el índice.
    - ``url``
  * - index.field.doc_id
    - Nombre del campo del ID de documento en el índice.
    - ``doc_id``
  * - index.field.id
    - Nombre del campo del ID interno en el índice.
    - ``_id``
  * - index.field.version
    - Nombre del campo de la versión en el índice.
    - ``_version``
  * - index.field.seq_no
    - Nombre del campo del número de secuencia en el índice.
    - ``_seq_no``
  * - index.field.primary_term
    - Nombre del campo del primary term en el índice.
    - ``_primary_term``
  * - index.field.lang
    - Nombre del campo del idioma en el índice.
    - ``lang``
  * - index.field.has_cache
    - Nombre del campo del estado de la caché en el índice.
    - ``has_cache``
  * - index.field.last_modified
    - Nombre del campo de la fecha de última modificación en el índice.
    - ``last_modified``
  * - index.field.etag
    - Nombre del campo del encabezado de respuesta ETag del documento rastreado en el índice.
    - ``etag``
  * - index.field.owner
    - Nombre del campo del propietario del archivo rastreado en el índice.
    - ``owner``
  * - index.field.last_modifier
    - Nombre del campo del último modificador del archivo rastreado en el índice.
    - ``last_modifier``
  * - index.field.anchor
    - Nombre del campo del ancla (anchor) en el índice.
    - ``anchor``
  * - index.field.segment
    - Nombre del campo del segmento en el índice.
    - ``segment``
  * - index.field.role
    - Nombre del campo del rol en el índice.
    - ``role``
  * - index.field.boost
    - Nombre del campo del valor de impulso en el índice.
    - ``boost``
  * - index.field.created
    - Nombre del campo de la fecha de creación en el índice.
    - ``created``
  * - index.field.timestamp
    - Nombre del campo de la marca de tiempo en el índice.
    - ``timestamp``
  * - index.field.label
    - Nombre del campo de la etiqueta en el índice.
    - ``label``
  * - index.field.tag
    - Nombre del campo de las etiquetas de usuario del documento en el índice.
    - ``tag``
  * - index.field.mimetype
    - Nombre del campo del tipo MIME en el índice.
    - ``mimetype``
  * - index.field.parent_id
    - Nombre del campo del ID padre en el índice.
    - ``parent_id``
  * - index.field.important_content
    - Nombre del campo del contenido importante en el índice.
    - ``important_content``
  * - index.field.content
    - Nombre del campo del contenido en el índice.
    - ``content``
  * - index.field.content_minhash_bits
    - Nombre del campo de los bits minhash del contenido en el índice.
    - ``content_minhash_bits``
  * - index.field.cache
    - Nombre del campo de la caché en el índice.
    - ``cache``
  * - index.field.digest
    - Nombre del campo del digest en el índice.
    - ``digest``
  * - index.field.title
    - Nombre del campo del título en el índice.
    - ``title``
  * - index.field.host
    - Nombre del campo del host en el índice.
    - ``host``
  * - index.field.site
    - Nombre del campo del sitio en el índice.
    - ``site``
  * - index.field.content_length
    - Nombre del campo de la longitud del contenido en el índice.
    - ``content_length``
  * - index.field.filetype
    - Nombre del campo del tipo de archivo en el índice.
    - ``filetype``
  * - index.field.filename
    - Nombre del campo del nombre de archivo en el índice.
    - ``filename``
  * - index.field.thumbnail
    - Nombre del campo de la miniatura en el índice.
    - ``thumbnail``
  * - index.field.virtual_host
    - Nombre del campo del host virtual en el índice.
    - ``virtual_host``
  * - response.field.content_title
    - Nombre del campo del título del contenido en la respuesta.
    - ``content_title``
  * - response.field.content_description
    - Nombre del campo de la descripción del contenido en la respuesta.
    - ``content_description``
  * - response.field.url_link
    - Nombre del campo del enlace URL en la respuesta.
    - ``url_link``
  * - response.field.site_path
    - Nombre del campo de la ruta del sitio en la respuesta.
    - ``site_path``
  * - response.max.title.length
    - Longitud máxima del título del contenido en la respuesta.
    - ``50``
  * - response.max.site.path.length
    - Longitud máxima de la ruta del sitio en la respuesta.
    - ``100``
  * - response.highlight.content_title.enabled
    - Indica si se habilita el resaltado del título del contenido en la respuesta.
    - ``true``
  * - response.inline.mimetypes
    - Tipos MIME en línea (inline) para la respuesta.
    - ``application/pdf,text/plain``
  * - response.headers
    - Encabezados HTTP de la respuesta. Access-Control-\* y Timing-Allow-Origin se ignoran (CORS se controla mediante api.cors.\* / CorsFilter). No establezca Vary aquí.
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: Índice de documentos
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - Nombre del índice de los documentos de búsqueda.
    - ``fess.search``
  * - index.document.update.index
    - Nombre del índice de los documentos de actualización.
    - ``fess.update``
  * - index.document.suggest.index
    - Nombre del índice de los documentos de sugerencia.
    - ``fess``
  * - index.document.crawler.index
    - Nombre del índice de los documentos del rastreador.
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - Número de shards primarios del índice de cola del rastreador.
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - Número de shards primarios del índice de datos del rastreador.
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - Número de shards primarios del índice de filtros del rastreador.
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - Número de réplicas del índice de cola del rastreador.
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - Número de réplicas del índice de datos del rastreador.
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - Número de réplicas del índice de filtros del rastreador.
    - ``1``
  * - index.config.index
    - Nombre del índice de los datos de configuración.
    - ``fess_config``
  * - index.user.index
    - Nombre del índice de los datos de usuario.
    - ``fess_user``
  * - index.log.index
    - Nombre del índice de los datos de registro.
    - ``fess_log``
  * - index.dictionary.prefix
    - Prefijo de los nombres de los índices de diccionario.
    - (empty)

.. list-table:: Gestión de documentos
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - Campos de tipo array para la administración en el índice.
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - Campos de tipo fecha para la administración en el índice.
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - Campos de tipo entero para la administración en el índice.
    - (empty)
  * - index.admin.long.fields
    - Campos de tipo long para la administración en el índice.
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - Campos de tipo float para la administración en el índice.
    - ``boost``
  * - index.admin.double.fields
    - Campos de tipo double para la administración en el índice.
    - (empty)
  * - index.admin.required.fields
    - Campos obligatorios para la administración en el índice.
    - ``url,title,role,boost``

.. list-table:: Tiempos de espera
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - Tiempo de espera de las operaciones de búsqueda del índice.
    - ``3m``
  * - index.scroll.search.timeout
    - Tiempo de espera de las operaciones de búsqueda con scroll.
    - ``3m``
  * - index.index.timeout
    - Tiempo de espera de las operaciones del índice.
    - ``3m``
  * - index.bulk.timeout
    - Tiempo de espera de las operaciones de indexación masiva (bulk).
    - ``3m``
  * - index.delete.timeout
    - Tiempo de espera de las operaciones de eliminación en el índice.
    - ``3m``
  * - index.health.timeout
    - Tiempo de espera de las comprobaciones de estado del índice.
    - ``10m``
  * - index.indices.timeout
    - Tiempo de espera de las operaciones de índices del índice.
    - ``1m``

.. list-table:: Tipos de archivo
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - Mapeo de tipos MIME a etiquetas de tipo de archivo para la indexación.
    - | ``text/html=html``
      | ``application/msword=word``
      | ``application/vnd.openxmlformats-officedocument.wordprocessingml.document=word``
      | ``application/vnd.ms-excel=excel``
      | ``application/vnd.ms-excel.sheet.2=excel``
      | ``application/vnd.ms-excel.sheet.3=excel``
      | ``application/vnd.ms-excel.sheet.4=excel``
      | ``application/vnd.ms-excel.workspace.3=excel``
      | ``application/vnd.ms-excel.workspace.4=excel``
      | ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet=excel``
      | ``application/vnd.ms-powerpoint=powerpoint``
      | ``application/vnd.openxmlformats-officedocument.presentationml.presentation=powerpoint``
      | ``application/vnd.oasis.opendocument.text=odt``
      | ``application/vnd.oasis.opendocument.spreadsheet=ods``
      | ``application/vnd.oasis.opendocument.presentation=odp``
      | ``application/pdf=pdf``
      | ``application/x-fictionbook+xml=fb2``
      | ``application/e-pub+zip=epub``
      | ``application/x-ibooks+zip=ibooks``
      | ``text/plain=txt``
      | ``application/rtf=rtf``
      | ``application/vnd.ms-htmlhelp=chm``
      | ``application/zip=zip``
      | ``application/x-7z-comressed=7z``
      | ``application/x-bzip=bz``
      | ``application/x-bzip2=bz2``
      | ``application/x-tar=tar``
      | ``application/x-rar-compressed=rar``
      | ``video/3gp=3gp``
      | ``video/3g2=3g2``
      | ``video/x-msvideo=avi``
      | ``video/x-flv=flv``
      | ``video/mpeg=mpeg``
      | ``video/mp4=mp4``
      | ``video/ogv=ogv``
      | ``video/quicktime=qt``
      | ``video/x-m4v=m4v``
      | ``audio/x-aif=aif``
      | ``audio/midi=midi``
      | ``audio/mpga=mpga``
      | ``audio/mp4=mp4a``
      | ``audio/ogg=oga``
      | ``audio/x-wav=wav``
      | ``image/webp=webp``
      | ``image/bmp=bmp``
      | ``image/x-icon=ico``
      | ``image/x-icon=ico``
      | ``image/png=png``
      | ``image/svg+xml=svg``
      | ``image/tiff=tiff``
      | ``image/jpeg=jpg``
  * - index.reindex.size
    - Número de documentos que se procesan por operación de reindexación.
    - ``100``
  * - index.reindex.body
    - Plantilla del cuerpo de la solicitud para las operaciones de reindexación.
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - Solicitudes por segundo para las operaciones de reindexación ("adaptive" para automático).
    - ``adaptive``
  * - index.reindex.refresh
    - Indica si se actualiza (refresh) el índice después de la reindexación.
    - ``false``
  * - index.reindex.timeout
    - Tiempo de espera de las operaciones de reindexación.
    - ``1m``
  * - index.reindex.scroll
    - Tiempo de espera de scroll de las operaciones de reindexación.
    - ``5m``
  * - index.reindex.max_docs
    - Número máximo de documentos para las operaciones de reindexación.
    - (empty)

.. list-table:: Consulta
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - Longitud máxima de las consultas de búsqueda.
    - ``1000``
  * - query.timeout
    - Tiempo de espera (ms) de las consultas de búsqueda.
    - ``10000``
  * - query.timeout.logging
    - Indica si se registran las búsquedas cuyos resultados están incompletos porque la consulta agotó el tiempo de espera o falló un shard.
    - ``true``
  * - query.track.total.hits
    - Número máximo de resultados totales (total hits) que se contabilizan en las consultas. Solo se admite un número positivo o true: false deja la respuesta sin recuento de resultados, y una búsqueda que lo solicite, aquí o como parámetro de búsqueda, se rechaza.
    - ``10000``
  * - query.geo.fields
    - Campos utilizados para las consultas de búsqueda geográfica.
    - ``location``
  * - query.browser.lang.parameter.name
    - Nombre del parámetro del idioma del navegador en las consultas.
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - Indica si se reemplaza el término por una consulta de prefijo.
    - ``true``
  * - query.orsearch.min.hit.count
    - Número mínimo de resultados para las consultas de búsqueda OR.
    - ``-1``
  * - query.highlight.terminal.chars
    - Caracteres terminales Unicode para el resaltado de consultas.
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - Tamaño de fragmento para el resaltado de consultas.
    - ``60``
  * - query.highlight.number.of.fragments
    - Número de fragmentos para el resaltado de consultas.
    - ``2``
  * - query.highlight.type
    - Tipo de resaltado de consultas.
    - ``fvh``
  * - query.highlight.tag.pre
    - Etiqueta que se utiliza antes del texto resaltado.
    - ``<strong>``
  * - query.highlight.tag.post
    - Etiqueta que se utiliza después del texto resaltado.
    - ``</strong>``
  * - query.highlight.boundary.chars
    - Caracteres de límite para el resaltado de consultas.
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - Escaneo máximo de los límites de resaltado de consultas.
    - ``20``
  * - query.highlight.boundary.scanner
    - Tipo de escáner para los límites de resaltado de consultas.
    - ``chars``
  * - query.highlight.encoder
    - Tipo de codificador para el resaltado de consultas.
    - ``default``
  * - query.highlight.force.source
    - Indica si se fuerza la fuente (force source) para el resaltado de consultas.
    - ``false``
  * - query.highlight.fragmenter
    - Tipo de fragmentador (fragmenter) para el resaltado de consultas.
    - ``span``
  * - query.highlight.fragment.offset
    - Desplazamiento (offset) de los fragmentos de resaltado de consultas.
    - ``-1``
  * - query.highlight.no.match.size
    - Tamaño para el resaltado de consultas sin coincidencia (no-match).
    - ``0``
  * - query.highlight.order
    - Orden de los fragmentos de resaltado de consultas.
    - ``score``
  * - query.highlight.phrase.limit
    - Límite de frases para el resaltado de consultas.
    - ``256``
  * - query.highlight.content.description.fields
    - Campos para la descripción del contenido en el resaltado de consultas.
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - Indica si se detecta la posición del límite en el resaltado de consultas.
    - ``true``
  * - query.highlight.text.fragment.type
    - Tipo del fragmento de texto en el resaltado de consultas.
    - ``query``
  * - query.highlight.text.fragment.size
    - Tamaño del fragmento de texto en el resaltado de consultas.
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - Longitud del prefijo del fragmento de texto en el resaltado de consultas.
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - Longitud del sufijo del fragmento de texto en el resaltado de consultas.
    - ``5``
  * - query.max.search.result.offset
    - Desplazamiento máximo de los resultados de búsqueda para las consultas.
    - ``100000``
  * - query.additional.default.fields
    - Campos predeterminados adicionales para las consultas.
    - (empty)
  * - query.additional.response.fields
    - Campos adicionales que se obtienen del índice para los resultados de búsqueda. La API de búsqueda devuelve un campo agregado aquí solo si también figura en query.additional.api.response.fields.
    - (empty)
  * - query.additional.api.response.fields
    - Campos de respuesta de la API adicionales para las consultas. Esta clave solo añade campos a la lista de permitidos de la respuesta de la API v2 (solo añade); no los obtiene. Un campo también debe obtenerse: añádalo a query.additional.response.fields para la API de búsqueda, o a query.additional.scroll.response.fields para la API de scroll. No añada campos de ACL ni internos (por ejemplo role, virtual_host); añadirlos expondría información de control de acceso en la respuesta de la API de búsqueda.
    - (empty)
  * - query.additional.scroll.response.fields
    - Campos adicionales que se obtienen del índice para los resultados de búsqueda con scroll. La API de scroll devuelve un campo agregado aquí solo si también figura en query.additional.api.response.fields.
    - (empty)
  * - query.additional.cache.response.fields
    - Campos de respuesta de caché adicionales para las consultas.
    - (empty)
  * - query.additional.highlighted.fields
    - Campos resaltados adicionales para las consultas.
    - (empty)
  * - query.additional.search.fields
    - Campos de búsqueda adicionales para las consultas.
    - (empty)
  * - query.additional.facet.fields
    - Campos de faceta adicionales para las consultas.
    - (empty)
  * - query.additional.sort.fields
    - Campos de ordenación adicionales para las consultas.
    - (empty)
  * - query.additional.analyzed.fields
    - Campos analizados adicionales para las consultas.
    - (empty)
  * - query.additional.not.analyzed.fields
    - Campos no analizados adicionales para las consultas.
    - (empty)
  * - query.gsa.response.fields
    - Campos de la respuesta GSA en las consultas.
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - Idioma predeterminado de las consultas GSA.
    - ``en``
  * - query.gsa.default.sort
    - Ordenación predeterminada de las consultas GSA.
    - (empty)
  * - query.gsa.meta.prefix
    - Prefijo meta de las consultas GSA.
    - ``MT_``
  * - query.gsa.index.field.charset
    - Campo de juego de caracteres (charset) de las consultas de índice GSA.
    - ``charset``
  * - query.gsa.index.field.content_type.
    - Campo de tipo de contenido de las consultas de índice GSA.
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - Número máximo de resultados de grupo simultáneos para las consultas de colapso (collapse).
    - ``4``
  * - query.collapse.inner.hits.name
    - Nombre de los inner hits para las consultas de colapso.
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - Tamaño de los inner hits para las consultas de colapso.
    - ``0``
  * - query.collapse.inner.hits.sorts
    - Ordenaciones de los inner hits en las consultas de colapso.
    - (empty)
  * - query.default.languages
    - Idiomas predeterminados de las consultas.
    - (empty)
  * - query.json.default.preference
    - Preferencia predeterminada para las consultas JSON.
    - ``_query``
  * - query.gsa.default.preference
    - Preferencia predeterminada para las consultas GSA.
    - ``_query``
  * - query.language.mapping
    - Mapeo de idiomas para las consultas.
    - | ``ar=ar``
      | ``bg=bg``
      | ``bn=bn``
      | ``ca=ca``
      | ``ckb-iq=ckb-iq``
      | ``ckb_IQ=ckb-iq``
      | ``cs=cs``
      | ``da=da``
      | ``de=de``
      | ``el=el``
      | ``en=en``
      | ``en-ie=en-ie``
      | ``en_IE=en-ie``
      | ``es=es``
      | ``et=et``
      | ``eu=eu``
      | ``fa=fa``
      | ``fi=fi``
      | ``fr=fr``
      | ``gl=gl``
      | ``gu=gu``
      | ``he=he``
      | ``hi=hi``
      | ``hr=hr``
      | ``hu=hu``
      | ``hy=hy``
      | ``id=id``
      | ``it=it``
      | ``ja=ja``
      | ``ko=ko``
      | ``lt=lt``
      | ``lv=lv``
      | ``mk=mk``
      | ``ml=ml``
      | ``nl=nl``
      | ``no=no``
      | ``pa=pa``
      | ``pl=pl``
      | ``pt=pt``
      | ``pt-br=pt-br``
      | ``pt_BR=pt-br``
      | ``ro=ro``
      | ``ru=ru``
      | ``si=si``
      | ``sq=sq``
      | ``sv=sv``
      | ``ta=ta``
      | ``te=te``
      | ``th=th``
      | ``tl=tl``
      | ``tr=tr``
      | ``uk=uk``
      | ``ur=ur``
      | ``vi=vi``
      | ``zh-cn=zh-cn``
      | ``zh_CN=zh-cn``
      | ``zh-tw=zh-tw``
      | ``zh_TW=zh-tw``
      | ``zh=zh``

.. list-table:: Impulso
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - Valor de impulso del campo de título en las consultas.
    - ``0.5``
  * - query.boost.title.lang
    - Valor de impulso del campo de título con idioma en las consultas.
    - ``1.0``
  * - query.boost.content
    - Valor de impulso del campo de contenido en las consultas.
    - ``0.05``
  * - query.boost.content.lang
    - Valor de impulso del campo de contenido con idioma en las consultas.
    - ``0.1``
  * - query.boost.important_content
    - Valor de impulso del campo de contenido importante en las consultas.
    - ``-1.0``
  * - query.boost.important_content.lang
    - Valor de impulso del campo de contenido importante con idioma en las consultas.
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - Longitud mínima para el impulso fuzzy en las consultas.
    - ``4``
  * - query.boost.fuzzy.title
    - Valor de impulso de las consultas fuzzy de título.
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - Fuzziness de las consultas fuzzy de título.
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - Número de expansiones de las consultas fuzzy de título.
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - Longitud del prefijo de las consultas fuzzy de título.
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - Indica si se permiten transposiciones en las consultas fuzzy de título.
    - ``true``
  * - query.boost.fuzzy.content
    - Valor de impulso de las consultas fuzzy de contenido.
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - Fuzziness de las consultas fuzzy de contenido.
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - Número de expansiones de las consultas fuzzy de contenido.
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - Longitud del prefijo de las consultas fuzzy de contenido.
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - Indica si se permiten transposiciones en las consultas fuzzy de contenido.
    - ``true``
  * - query.default.query_type
    - Tipo de consulta predeterminado.
    - ``bool``
  * - query.dismax.tie_breaker
    - Valor de tie breaker para las consultas dismax.
    - ``0.1``
  * - query.bool.minimum_should_match
    - Valor de minimum should match para las consultas booleanas.
    - (empty)
  * - query.prefix.expansions
    - Número de expansiones de las consultas de prefijo.
    - ``50``
  * - query.prefix.slop
    - Valor de slop de las consultas de prefijo.
    - ``0``
  * - query.fuzzy.prefix_length
    - Longitud del prefijo de las consultas fuzzy.
    - ``0``
  * - query.fuzzy.expansions
    - Número de expansiones de las consultas fuzzy.
    - ``50``
  * - query.fuzzy.transpositions
    - Indica si se permiten transposiciones en las consultas fuzzy.
    - ``true``

.. list-table:: Faceta
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - Campos para las consultas de faceta.
    - ``label``
  * - query.facet.fields.size
    - Tamaño de los campos de faceta.
    - ``100``
  * - query.facet.fields.size.max
    - Límite superior (clamp) de facet.size (se aplica en el punto de paso único de la búsqueda).
    - ``1000``
  * - query.facet.fields.min_doc_count
    - Recuento mínimo de documentos para los campos de faceta.
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - Límite superior (clamp) de facet.minDocCount (se aplica en el punto de paso único de la búsqueda).
    - ``2147483647``
  * - query.facet.fields.sort
    - Criterio de ordenación de los campos de faceta.
    - ``count.desc``
  * - query.facet.fields.missing
    - Valor para los campos de faceta ausentes.
    - (empty)
  * - query.facet.queries
    - Definición de las consultas de faceta.
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: Ranking
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Tamaño de ventana para rank fusion.
    - ``200``
  * - rank.fusion.rank_constant
    - Constante de rango para rank fusion.
    - ``20``
  * - rank.fusion.threads
    - Número de hilos para rank fusion.
    - ``-1``
  * - rank.fusion.timeout
    - Tiempo máximo (milisegundos) de espera de los buscadores distintos del principal cuando Fess fusiona por sí mismo sus resultados (rank.fusion.engine.enabled=false). Un buscador que no ha respondido para entonces se deja fuera de esa búsqueda, y los resultados se marcan como parciales y con el tiempo de espera agotado. Siempre se espera al buscador principal. 0 o menos espera sin límite.
    - ``10000``
  * - rank.fusion.score_field
    - Campo de puntuación para rank fusion.
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - Indica si el motor de búsqueda realiza la rank fusion. Cuando es true, los buscadores que pueden participar aportan sus consultas a una única solicitud, de modo que las facetas y el total de resultados describen el conjunto de resultados fusionado. Cuando es false, Fess fusiona por sí mismo los resultados de los buscadores.
    - ``false``
  * - rank.fusion.combination.technique
    - Cómo combina el motor de búsqueda las puntuaciones fusionadas: rrf, arithmetic_mean, geometric_mean o harmonic_mean.
    - ``rrf``
  * - rank.fusion.normalization.technique
    - Cómo se normalizan las puntuaciones antes de combinarlas: min_max, l2 o z_score. rrf lo ignora. z_score solo se puede combinar con arithmetic_mean; cualquier otra media se rechaza y Fess fusiona por sí mismo los resultados.
    - ``min_max``
  * - rank.fusion.combination.weights
    - Peso por buscador para la fusión en el motor, como pares nombre:peso, p. ej. default:0.7,semantic_chunk:0.3. Los pesos deben sumar 1.0 y deben nombrar a todos los buscadores que participan. Si está vacío, se ponderan por igual.
    - (empty)
  * - rank.fusion.pagination_depth
    - Cuántos resultados aporta cada buscador por shard a la fusión en el motor. Esto limita tanto la profundidad hasta la que un cliente puede paginar como el conjunto de documentos que clasifica el motor: una búsqueda fusionada pagina a través de esta cantidad de resultados, y nunca más de indexer.max.result.window.size.
    - ``1000``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - Indica si se obtienen los roles SMB desde un archivo.
    - ``true``
  * - smb.available.sid.types
    - Tipos de SID disponibles para SMB.
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - Indica si se obtienen los roles de archivo desde un archivo.
    - ``true``
  * - ftp.role.from.file
    - Indica si se obtienen los roles FTP desde un archivo.
    - ``true``

.. list-table:: Copia de seguridad
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - Archivos de destino de la copia de seguridad del índice.
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - Archivos de registro de destino de la copia de seguridad del índice.
    - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - Tiempo de espera para cargar los registros de la copia de seguridad del índice.
    - ``60000``

.. list-table:: Registro
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - Paquetes de aplicación para el registro.
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - Indica si se habilita el registro de los documentos de búsqueda (search docs).
    - ``true``
  * - logging.search.docs.fields
    - Campos que se registran para los documentos de búsqueda.
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - Indica si se utiliza un archivo de registro para el registro de búsquedas.
    - ``true``
  * - logging.search.max.queue.size
    - Tamaño máximo de la cola del registro de búsquedas.
    - ``10000``
  * - logging.click.max.queue.size
    - Tamaño máximo de la cola del registro de clics.
    - ``10000``
  * - logging.chat.max.queue.size
    - Tamaño máximo de la cola del registro de uso del chat.
    - ``10000``
  * - search.history.enabled
    - Indica si se registran las condiciones de búsqueda de los usuarios que han iniciado sesión para el historial de búsqueda.
    - ``true``
  * - search.history.size
    - Número máximo de entradas del historial de búsqueda que se devuelven por usuario.
    - ``10``
  * - user.tag.enabled
    - Indica si los usuarios que han iniciado sesión pueden etiquetar documentos. Cada etiqueta pertenece al usuario que la creó.
    - ``false``
  * - user.tag.name.max.length
    - Longitud máxima del nombre de una etiqueta, en puntos de código.
    - ``50``
  * - user.tag.max.tags
    - Número máximo de etiquetas que puede poseer un usuario.
    - ``1000``
  * - user.tag.max.paths
    - Número máximo de URLs en las que se puede poner una etiqueta.
    - ``10000``
  * - user.tag.queue.max.size
    - Número máximo de cambios de etiquetas pendientes que se mantienen en memoria hasta que se aplican a los documentos.
    - ``10000``
  * - user.tag.process.batch.size
    - Número de URLs que se actualizan por solicitud masiva (bulk) cuando los cambios de etiquetas se aplican a los documentos.
    - ``100``
  * - user.tag.visible.max.size
    - Número máximo de etiquetas visibles para un usuario en una búsqueda.
    - ``1000``

Web
---

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - Tamaño máximo de entrada de los formularios de administración.
    - ``10000``
  * - form.admin.label.in.config.enabled
    - Indica si se habilita la etiqueta en los formularios de configuración de administración.
    - ``false``
  * - form.admin.default.template.name
    - Nombre de plantilla predeterminado de los formularios de administración.
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - Indica si se habilita el enlace OSDD (OpenSearch Description Document).
    - ``auto``
  * - clipboard.copy.icon.enabled
    - Indica si se habilita el icono de copia al portapapeles.
    - ``true``
  * - authentication.admin.users
    - Nombres de los usuarios administradores para la autenticación.
    - ``admin``
  * - authentication.admin.users.ignore.case
    - Indica si authentication.admin.users se compara sin distinguir mayúsculas y minúsculas: auto, true o false. auto ignora las mayúsculas y minúsculas cuando ldap.provider.url está establecido.
    - ``auto``
  * - authentication.admin.roles
    - Nombres de los roles de administrador para la autenticación.
    - ``admin``
  * - role.search.default.permissions
    - Permisos predeterminados de los roles de búsqueda.
    - (empty)
  * - role.search.default.display.permissions
    - Permisos de visualización predeterminados de los roles de búsqueda.
    - ``{role}guest``
  * - role.search.guest.permissions
    - Mantenga role.search.guest.permissions no vacío. Inicializa el rol de invitado que mantiene no vacío el conjunto de roles de búsqueda anónimo; si el conjunto de roles resuelto está vacío, se omite el filtro de roles (fail-open), lo que puede deshabilitar el control de acceso basado en roles y exponer documentos a usuarios anónimos. Permisos de invitado de los roles de búsqueda.
    - ``{role}guest``
  * - role.search.user.prefix
    - Prefijo de los roles de usuario en la búsqueda.
    - ``1``
  * - role.search.group.prefix
    - Prefijo de los roles de grupo en la búsqueda.
    - ``2``
  * - role.search.role.prefix
    - Prefijo de los roles de rol en la búsqueda.
    - ``R``
  * - role.search.denied.prefix
    - Prefijo de los roles denegados en la búsqueda.
    - ``D``
  * - cookie.default.path
    - La ruta predeterminada de la cookie (básicamente '/' si no hay ruta de contexto)
    - ``/``
  * - cookie.default.expire
    - La caducidad predeterminada de la cookie en segundos, p. ej. 31556926: un año, 86400: un día
    - ``3600``
  * - session.tracking.modes
    - Modos de seguimiento de sesión
    - ``cookie``
  * - session.cookie.secure
    - Indica si se añade el atributo Secure a la cookie de sesión (JSESSIONID) al iniciar. Cuando está en blanco (valor predeterminado), se usa el comportamiento automático de Tomcat (Secure solo se añade en las solicitudes HTTPS). Establézcalo en true para los despliegues de producción con HTTPS, especialmente cuando TLS termina en un proxy inverso. Cuando es true, la cookie no se envía por HTTP, por lo que no se establecerán sesiones con HTTP plano; manténgalo en blanco para el desarrollo en localhost. El atributo Secure también es obligatorio cuando se usa SameSite=none. Cambiar este valor requiere un reinicio.
    - (empty)
  * - cookie.search.parameter.keys
    - Lista separada por comas de las claves de parámetros de solicitud que se almacenan en cookies antes del inicio de sesión SSO.
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - Lista separada por comas de las claves de parámetros obligatorios que deben estar presentes para almacenarse en cookies.
    - ``q``
  * - cookie.search.parameter.max.length
    - Longitud máxima de los parámetros de búsqueda codificados que se almacenan en cookies.
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - Tamaño máximo en bytes al que pueden descomprimirse los parámetros de búsqueda almacenados. El límite anterior se aplica a la cookie comprimida con gzip, lo que no limita su tamaño una vez expandida, y la cookie proviene del cliente.
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - Longitud máxima de la cadena de consulta que se construye al restaurar los parámetros de búsqueda almacenados tras el inicio de sesión. Restaurarlos es una comodidad, mientras que el inicio de sesión no lo es, por lo que una cadena más larga se descarta en lugar de escribirse en un encabezado Location que el contenedor rechazaría. La codificación porcentual multiplica por nueve una consulta CJK, por lo que este valor es mucho menor de lo que puede ser la propia consulta. Auméntelo junto con tomcat.maxHttpHeaderSize en tomcat_config.properties, que limita los encabezados de la respuesta.
    - ``4096``
  * - cookie.search.parameter.name
    - Nombre de la cookie que se utiliza para almacenar los parámetros de búsqueda codificados antes del inicio de sesión SSO.
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - Indica si se establece el atributo HttpOnly en la cookie de los parámetros de búsqueda.
    - ``true``
  * - cookie.search.parameter.secure
    - Indica si se establece el atributo Secure en la cookie de los parámetros de búsqueda. Debería ser true en los entornos de producción que usan HTTPS.
    - (empty)
  * - cookie.search.parameter.max_age
    - Max-Age (en segundos) de la cookie de los parámetros de búsqueda. Use -1 para cookies solo de sesión.
    - ``60``
  * - cookie.search.parameter.domain
    - Atributo Domain de la cookie de los parámetros de búsqueda. Establézcalo en el ámbito de dominio en el que desea que esté disponible la cookie (p. ej., example.com).
    - (empty)
  * - cookie.search.parameter.path
    - Atributo Path de la cookie de los parámetros de búsqueda. Normalmente se establece en "/" o en la ruta de contexto de la aplicación.
    - ``/``
  * - cookie.search.parameter.same_site
    - Atributo SameSite de la cookie de los parámetros de búsqueda. Valores válidos: Lax, Strict, None
    - ``Lax``
  * - paging.page.size
    - El tamaño de una página para la paginación
    - ``25``
  * - paging.page.range.size
    - El tamaño del rango de páginas para la paginación
    - ``5``
  * - paging.page.range.fill.limit
    - La opción 'fillLimit' del rango de páginas para la paginación
    - ``true``

.. list-table:: Tamaño de página de obtención
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - Número máximo de registros de impulso de documento (docboost) que se obtienen por página.
    - ``1000``
  * - page.keymatch.max.fetch.size
    - Número máximo de registros de coincidencia de clave (keymatch) que se obtienen por página.
    - ``1000``
  * - page.labeltype.max.fetch.size
    - Número máximo de registros de tipo de etiqueta (labeltype) que se obtienen por página.
    - ``1000``
  * - page.tagtype.max.fetch.size
    - Número máximo de registros de tipo de etiqueta de usuario (tagtype) que se obtienen por página.
    - ``1000``
  * - page.roletype.max.fetch.size
    - Número máximo de registros de tipo de rol (roletype) que se obtienen por página.
    - ``1000``
  * - page.user.max.fetch.size
    - Número máximo de registros de usuario que se obtienen por página.
    - ``1000``
  * - page.role.max.fetch.size
    - Número máximo de registros de rol que se obtienen por página.
    - ``1000``
  * - page.group.max.fetch.size
    - Número máximo de registros de grupo que se obtienen por página.
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - Número máximo de parámetros de información de rastreo que se obtienen por página.
    - ``100``
  * - page.crawling.info.max.fetch.size
    - Número máximo de registros de información de rastreo que se obtienen por página.
    - ``1000``
  * - page.data.config.max.fetch.size
    - Número máximo de registros de configuración de almacén de datos que se obtienen por página.
    - ``100``
  * - page.web.config.max.fetch.size
    - Número máximo de registros de configuración web que se obtienen por página.
    - ``100``
  * - page.file.config.max.fetch.size
    - Número máximo de registros de configuración de archivos que se obtienen por página.
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - Número máximo de registros de host duplicado que se obtienen por página.
    - ``1000``
  * - page.failure.url.max.fetch.size
    - Número máximo de registros de URL de fallo que se obtienen por página.
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - Número máximo de registros del registro de favoritos que se obtienen por página.
    - ``100``
  * - page.file.auth.max.fetch.size
    - Número máximo de registros de autenticación de archivos que se obtienen por página.
    - ``100``
  * - page.web.auth.max.fetch.size
    - Número máximo de registros de autenticación web que se obtienen por página.
    - ``100``
  * - page.path.mapping.max.fetch.size
    - Número máximo de registros de mapeo de rutas que se obtienen por página.
    - ``1000``
  * - page.request.header.max.fetch.size
    - Número máximo de registros de encabezado de solicitud que se obtienen por página.
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - Número máximo de registros de trabajo programado que se obtienen por página.
    - ``100``
  * - page.elevate.word.max.fetch.size
    - Número máximo de registros de palabra adicional que se obtienen por página.
    - ``1000``
  * - page.bad.word.max.fetch.size
    - Número máximo de registros de palabra no deseada que se obtienen por página.
    - ``1000``
  * - page.dictionary.max.fetch.size
    - Número máximo de registros de diccionario que se obtienen por página.
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - Número máximo de registros de contenido relacionado que se obtienen por página.
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - Número máximo de registros de consulta relacionada que se obtienen por página.
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - Número máximo de registros de la cola de miniaturas que se obtienen por página.
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - Número máximo de registros de purga de miniaturas que se obtienen por página.
    - ``100``
  * - page.score.booster.max.fetch.size
    - Número máximo de registros de impulso de puntuación (score booster) que se obtienen por página.
    - ``1000``
  * - page.searchlog.max.fetch.size
    - Número máximo de registros del registro de búsqueda que se obtienen por página.
    - ``10000``
  * - page.searchlist.track.total.hits
    - Indica si se contabiliza el total de resultados (total hits) en la página de lista de búsqueda.
    - ``true``
  * - page.searchlist.content.max.length
    - Longitud máxima del contenido (en caracteres) que se muestra en la página de edición de la lista de búsqueda.
    - ``100000``

.. list-table:: Página de búsqueda
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - Página de inicio predeterminada de los resultados de búsqueda.
    - ``0``
  * - paging.search.page.size
    - Tamaño predeterminado de los resultados de búsqueda por página.
    - ``10``
  * - paging.search.page.max.size
    - Tamaño máximo de los resultados de búsqueda por página.
    - ``100``
  * - api.param.max.length
    - Longitud máxima de un parámetro de consulta de tipo cadena de la API v2 (q, sort, sdh). OWASP API4:2023.
    - ``1000``
  * - api.param.max.array.size
    - Número máximo de valores de un parámetro de consulta repetible de la API v2.
    - ``100``
  * - api.click.max.timestamp
    - Marca de tiempo máxima del registro de clics (rt, epoch ms) que acepta la API de clics v2. OWASP API4:2023.
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - Registro de búsqueda
    - ``-1``
  * - searchlog.request.headers
    - Encabezados de solicitud que se incluyen en el registro de búsqueda.
    - (empty)
  * - searchlog.process.batch_size
    - Tamaño de lote para el procesamiento del registro de búsqueda.
    - ``100``
  * - related_query.generate.days
    - Número de días de registros de búsqueda que se leen al generar consultas relacionadas a partir de los registros de búsqueda.
    - ``30``
  * - related_query.generate.term.size
    - Número máximo de términos que se generan por host virtual.
    - ``100``
  * - related_query.generate.query.size
    - Número máximo de consultas relacionadas que se generan por término.
    - ``5``
  * - related_query.generate.min.sessions
    - Número mínimo de sesiones de usuario distintas que se requieren para un término y para cada una de sus consultas relacionadas.
    - ``3``
  * - related_query.generate.session.interval
    - Intervalo (minutos) tras una búsqueda dentro del cual una búsqueda posterior de la misma sesión cuenta como refinamiento.
    - ``10``
  * - related_query.generate.seed.log.size
    - Número máximo de registros de búsqueda de un término que se leen para encontrar las sesiones que lo buscaron.
    - ``1000``
  * - related_query.generate.seed.session.size
    - Número máximo de sesiones por término cuyas búsquedas posteriores se leen.
    - ``200``
  * - related_query.generate.log.fetch.size
    - Número máximo de registros de búsqueda posteriores que se leen por término.
    - ``2000``
  * - related_query.generate.query.min.length
    - Longitud mínima (en caracteres) de un término generado o de una consulta relacionada.
    - ``2``
  * - related_query.generate.query.max.length
    - Longitud máxima (en caracteres) de un término generado o de una consulta relacionada.
    - ``50``
  * - docreport.duplicate.group.size
    - docreport Número máximo de grupos duplicados que muestra la pantalla del informe de documentos, empezando por los más grandes.
    - ``100``
  * - docreport.duplicate.docs.size
    - Número máximo de documentos que la pantalla del informe de documentos lista para cada grupo duplicado.
    - ``10``
  * - docreport.duplicate.export.page.size
    - Número de firmas de contenido que se leen por solicitud cuando el informe de duplicados se descarga como CSV.
    - ``10000``
  * - docreport.dormant.days
    - Número predeterminado de días desde la última modificación a partir del cual un documento se considera inactivo.
    - ``365``
  * - thumbnail.html.image.min.width
    - Ancho mínimo de las imágenes HTML en las miniaturas.
    - ``100``
  * - thumbnail.html.image.min.height
    - Alto mínimo de las imágenes HTML en las miniaturas.
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - Relación de aspecto máxima de las imágenes HTML en las miniaturas.
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - Ancho de las imágenes de miniatura generadas.
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - Alto de las imágenes de miniatura generadas.
    - ``100``
  * - thumbnail.html.image.format
    - Formato de las imágenes de miniatura generadas.
    - ``png``
  * - thumbnail.html.image.xpath
    - XPath para seleccionar las imágenes de las miniaturas.
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - Extensiones de archivo que se excluyen de la generación de miniaturas.
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - Intervalo del generador de miniaturas.
    - ``0``
  * - thumbnail.generator.targets
    - Destinos del generador de miniaturas (p. ej., all).
    - ``all``
  * - thumbnail.crawler.enabled
    - Indica si el rastreador de miniaturas está habilitado.
    - ``true``
  * - thumbnail.system.monitor.interval
    - Intervalo del monitor del sistema en el procesamiento de miniaturas.
    - ``60``

.. list-table:: Usuario
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - Configuración del código de usuario
    - ``userCode``
  * - user.code.min.length
    - Longitud mínima del código de usuario.
    - ``20``
  * - user.code.max.length
    - Longitud máxima del código de usuario.
    - ``100``
  * - user.code.pattern
    - Patrón de validación del código de usuario.
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - Nombre que se muestra en el campo De de los correos electrónicos.
    - ``Administrator``
  * - mail.from.address
    - Dirección de correo electrónico que se utiliza en el campo De.
    - ``root@localhost``
  * - mail.hostname
    - Nombre de host del servidor de correo.
    - (empty)
  * - scheduler.target.name
    - Nombre de destino (target) del programador.
    - (empty)
  * - scheduler.job.class
    - Clase de trabajo del programador.
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - Modo de ejecución concurrente en el programador.
    - ``QUIT``
  * - scheduler.monitor.interval
    - Intervalo del monitoreo del programador.
    - ``30``
  * - coordinator.poll.interval
    - Intervalo (segundos) del sondeo (polling) de heartbeats y eventos.
    - ``60``
  * - coordinator.heartbeat.ttl
    - Tiempo de vida (ms) de los documentos de heartbeat de instancia.
    - ``180000``
  * - coordinator.operation.ttl
    - Tiempo de vida (ms) de los documentos de bloqueo de operación.
    - ``7200000``
  * - coordinator.operation.retry
    - Número máximo de reintentos para adquirir un bloqueo de operación.
    - ``3``
  * - coordinator.event.ttl
    - Tiempo de vida (ms) de los documentos de notificación de eventos.
    - ``600000``
  * - online.help.base.link
    - Enlace base de la ayuda en línea.
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - Enlace de la guía de instalación de la ayuda en línea.
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - Enlace de la información de fin de vida (end-of-life) de la ayuda en línea.
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - Clave de ayuda en línea para la URL de fallo.
    - ``failureurl``
  * - online.help.name.elevateword
    - Clave de ayuda en línea para la palabra adicional.
    - ``elevateword``
  * - online.help.name.reqheader
    - Clave de ayuda en línea para el encabezado de solicitud.
    - ``reqheader``
  * - online.help.name.dict.synonym
    - Clave de ayuda en línea para el diccionario de sinónimos.
    - ``synonym``
  * - online.help.name.dict
    - Clave de ayuda en línea para el diccionario.
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Clave de ayuda en línea para el diccionario Kuromoji.
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - Clave de ayuda en línea para el diccionario de palabras protegidas.
    - ``protwords``
  * - online.help.name.dict.stopwords
    - Clave de ayuda en línea para el diccionario de palabras vacías.
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Clave de ayuda en línea para el diccionario de anulación de stemmer.
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - Clave de ayuda en línea para el diccionario de mapeo.
    - ``mapping``
  * - online.help.name.webconfig
    - Clave de ayuda en línea para la configuración web.
    - ``webconfig``
  * - online.help.name.searchlist
    - Clave de ayuda en línea para la lista de búsqueda.
    - ``searchlist``
  * - online.help.name.log
    - Clave de ayuda en línea para el registro.
    - ``log``
  * - online.help.name.general
    - Clave de ayuda en línea para la configuración general.
    - ``general``
  * - online.help.name.role
    - Clave de ayuda en línea para el rol.
    - ``role``
  * - online.help.name.joblog
    - Clave de ayuda en línea para el registro de trabajos.
    - ``joblog``
  * - online.help.name.keymatch
    - Clave de ayuda en línea para la coincidencia de clave.
    - ``keymatch``
  * - online.help.name.relatedquery
    - Clave de ayuda en línea para la consulta relacionada.
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - Clave de ayuda en línea para el contenido relacionado.
    - ``relatedcontent``
  * - online.help.name.wizard
    - Clave de ayuda en línea para el asistente.
    - ``wizard``
  * - online.help.name.badword
    - Clave de ayuda en línea para la palabra no deseada.
    - ``badword``
  * - online.help.name.pathmap
    - Clave de ayuda en línea para el mapeo de rutas.
    - ``pathmap``
  * - online.help.name.boostdoc
    - Clave de ayuda en línea para el impulso de documento.
    - ``boostdoc``
  * - online.help.name.dataconfig
    - Clave de ayuda en línea para la configuración de almacén de datos.
    - ``dataconfig``
  * - online.help.name.systeminfo
    - Clave de ayuda en línea para la información del sistema.
    - ``systeminfo``
  * - online.help.name.user
    - Clave de ayuda en línea para el usuario.
    - ``user``
  * - online.help.name.group
    - Clave de ayuda en línea para el grupo.
    - ``group``
  * - online.help.name.dashboard
    - Clave de ayuda en línea para el panel de control.
    - ``dashboard``
  * - online.help.name.webauth
    - Clave de ayuda en línea para la autenticación web.
    - ``webauth``
  * - online.help.name.fileconfig
    - Clave de ayuda en línea para la configuración de archivos.
    - ``fileconfig``
  * - online.help.name.fileauth
    - Clave de ayuda en línea para la autenticación de archivos.
    - ``fileauth``
  * - online.help.name.labeltype
    - Clave de ayuda en línea para el tipo de etiqueta.
    - ``labeltype``
  * - online.help.name.tagtype
    - Clave de ayuda en línea para el tipo de etiqueta de usuario.
    - ``tagtype``
  * - online.help.name.duplicatehost
    - Clave de ayuda en línea para el host duplicado.
    - ``duplicatehost``
  * - online.help.name.scheduler
    - Clave de ayuda en línea para el programador.
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - Clave de ayuda en línea para la información de rastreo.
    - ``crawlinginfo``
  * - online.help.name.backup
    - Clave de ayuda en línea para la copia de seguridad.
    - ``backup``
  * - online.help.name.upgrade
    - Clave de ayuda en línea para la actualización.
    - ``upgrade``
  * - online.help.name.sereq
    - Clave de ayuda en línea para la solicitud de búsqueda.
    - ``sereq``
  * - online.help.name.accesstoken
    - Clave de ayuda en línea para el token de acceso.
    - ``accesstoken``
  * - online.help.name.suggest
    - Clave de ayuda en línea para la sugerencia.
    - ``suggest``
  * - online.help.name.searchlog
    - Clave de ayuda en línea para el registro de búsqueda.
    - ``searchlog``
  * - online.help.name.maintenance
    - Clave de ayuda en línea para el mantenimiento.
    - ``maintenance``
  * - online.help.name.plugin
    - Clave de ayuda en línea para el plugin.
    - ``plugin``
  * - online.help.name.storage
    - Clave de ayuda en línea para el almacenamiento.
    - ``storage``
  * - online.help.name.docreport
    - Clave de ayuda en línea para el informe de documentos.
    - ``docreport``
  * - online.help.supported.langs
    - Idiomas admitidos para la ayuda en línea.
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - Enlace del foro de soporte para usuarios.
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - Idiomas admitidos para el foro.
    - ``en,ja``
  * - suggest.popular.word.seed
    - Valor semilla (seed) para la sugerencia de palabras populares.
    - ``0``
  * - suggest.popular.word.tags
    - Etiquetas para la sugerencia de palabras populares.
    - (empty)
  * - suggest.popular.word.fields
    - Campos para la sugerencia de palabras populares.
    - (empty)
  * - suggest.popular.word.excludes
    - Palabras excluidas de la sugerencia de palabras populares.
    - (empty)
  * - suggest.popular.word.size
    - Número de palabras populares que se sugieren.
    - ``10``
  * - suggest.popular.word.window.size
    - Tamaño de ventana para la sugerencia de palabras populares.
    - ``30``
  * - suggest.popular.word.query.freq
    - Frecuencia de consulta para la sugerencia de palabras populares.
    - ``10``
  * - suggest.min.hit.count
    - Número mínimo de resultados para la sugerencia.
    - ``1``
  * - suggest.field.contents
    - Campo del contenido de la sugerencia.
    - ``_default``
  * - suggest.field.tags
    - Campo de las etiquetas de la sugerencia.
    - ``label``
  * - suggest.field.roles
    - Campo de los roles de la sugerencia.
    - ``role``
  * - suggest.field.index.contents
    - Contenido del índice para la sugerencia.
    - ``content,title``
  * - suggest.update.request.interval
    - Intervalo de las solicitudes de actualización de sugerencias.
    - ``0``
  * - suggest.update.doc.per.request
    - Número de documentos por solicitud de actualización de sugerencias.
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - Límite porcentual del contenido de actualización de sugerencias.
    - ``50%``
  * - suggest.update.contents.limit.num
    - Número máximo de contenidos de actualización de sugerencias.
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - Tamaño máximo de documento para la actualización de sugerencias.
    - ``50000``
  * - suggest.source.reader.scroll.size
    - Tamaño de scroll del lector de la fuente de sugerencias.
    - ``1``
  * - suggest.popular.word.cache.size
    - Tamaño de la caché para la sugerencia de palabras populares.
    - ``1000``
  * - suggest.popular.word.cache.expire
    - Caducidad de la caché (segundos) para la sugerencia de palabras populares.
    - ``60``
  * - suggest.search.log.permissions
    - Permisos del registro de búsqueda para la sugerencia.
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - Intervalo del monitor del sistema en la sugerencia.
    - ``60``
  * - ldap.admin.enabled
    - Indica si la administración LDAP está habilitada.
    - ``false``
  * - ldap.admin.user.filter
    - Filtro de usuarios para la administración LDAP.
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - DN base del usuario de la administración LDAP.
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - Clases de objeto del usuario de la administración LDAP.
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - Filtro de roles para la administración LDAP.
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - DN base del rol de la administración LDAP.
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - Clases de objeto del rol de la administración LDAP.
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - Filtro de grupos para la administración LDAP.
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - DN base del grupo de la administración LDAP.
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - Clases de objeto del grupo de la administración LDAP.
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - Indica si se sincroniza la contraseña para la administración LDAP.
    - ``true``
  * - ldap.auth.validation
    - Indica si se valida la autenticación LDAP.
    - ``true``
  * - ldap.connect.timeout
    - Tiempo de espera (milisegundos) para establecer una conexión LDAP. También limita el handshake TLS y la respuesta del bind inicial. 0 o menos lo deja en el valor predeterminado del JDK/OS.
    - ``10000``
  * - ldap.read.timeout
    - Tiempo de espera (milisegundos) de una respuesta LDAP una vez que la conexión está enlazada (bound). 0 o menos espera indefinidamente.
    - ``30000``
  * - ldap.search.time.limit
    - Límite de tiempo del lado del servidor (milisegundos) para una búsqueda LDAP. 0 o menos significa sin límite.
    - ``60000``
  * - ldap.max.username.length
    - Longitud máxima del nombre de usuario para LDAP.
    - ``-1``
  * - ldap.ignore.netbios.name
    - Indica si se ignora el nombre NetBIOS en LDAP.
    - ``true``
  * - ldap.group.name.with.underscores
    - Indica si se permiten guiones bajos en los nombres de grupo de LDAP.
    - ``false``
  * - ldap.lowercase.permission.name
    - Indica si se usan minúsculas para los nombres de permisos de LDAP.
    - ``false``
  * - ldap.allow.empty.permission
    - Indica si se permiten permisos vacíos en LDAP.
    - ``true``
  * - ldap.samaccountname.group
    - Indica si se usa samAccountName para el grupo de LDAP.
    - ``false``
  * - ldap.role.search.user.enabled
    - Indica si la búsqueda de roles LDAP para el usuario está habilitada.
    - ``true``
  * - ldap.role.search.group.enabled
    - Indica si la búsqueda de roles LDAP para el grupo está habilitada.
    - ``true``
  * - ldap.role.search.role.enabled
    - Indica si la búsqueda de roles LDAP para el rol está habilitada.
    - ``true``
  * - ldap.attr.surname
    - Atributo LDAP del apellido.
    - ``sn``
  * - ldap.attr.givenName
    - Atributo LDAP del nombre de pila.
    - ``givenName``
  * - ldap.attr.employeeNumber
    - Atributo LDAP del número de empleado.
    - ``employeeNumber``
  * - ldap.attr.mail
    - Atributo LDAP del correo.
    - ``mail``
  * - ldap.attr.telephoneNumber
    - Atributo LDAP del número de teléfono.
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - Atributo LDAP del teléfono particular.
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - Atributo LDAP de la dirección postal particular.
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - Atributo LDAP del URI etiquetado.
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - Atributo LDAP del número de sala.
    - ``roomNumber``
  * - ldap.attr.description
    - Atributo LDAP de la descripción.
    - ``description``
  * - ldap.attr.title
    - Atributo LDAP del título.
    - ``title``
  * - ldap.attr.pager
    - Atributo LDAP del pager.
    - ``pager``
  * - ldap.attr.street
    - Atributo LDAP de la calle.
    - ``street``
  * - ldap.attr.postalCode
    - Atributo LDAP del código postal.
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - Atributo LDAP del nombre de la oficina de entrega física.
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - Atributo LDAP del indicador de destino.
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - Atributo LDAP del número ISDN internacional.
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - Atributo LDAP del estado.
    - ``st``
  * - ldap.attr.employeeType
    - Atributo LDAP del tipo de empleado.
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - Atributo LDAP del número de teléfono de facsímil.
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - Atributo LDAP del apartado de correos.
    - ``postOfficeBox``
  * - ldap.attr.initials
    - Atributo LDAP de las iniciales.
    - ``initials``
  * - ldap.attr.carLicense
    - Atributo LDAP de la licencia del automóvil.
    - ``carLicense``
  * - ldap.attr.mobile
    - Atributo LDAP del móvil.
    - ``mobile``
  * - ldap.attr.postalAddress
    - Atributo LDAP de la dirección postal.
    - ``postalAddress``
  * - ldap.attr.city
    - Atributo LDAP de la ciudad.
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - Atributo LDAP del identificador de terminal teletex.
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - Atributo LDAP de la dirección X.121.
    - ``x121Address``
  * - ldap.attr.businessCategory
    - Atributo LDAP de la categoría de negocio.
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - Atributo LDAP de la dirección registrada.
    - ``registeredAddress``
  * - ldap.attr.displayName
    - Atributo LDAP del nombre para mostrar.
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - Atributo LDAP del idioma preferido.
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - Atributo LDAP del número de departamento.
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - Atributo LDAP del número UID.
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - Atributo LDAP del número GID.
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - Atributo LDAP del directorio personal.
    - ``homeDirectory``
  * - plugin.repositories
    - URLs de los repositorios de plugins.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - Filtro de versión de los plugins.
    - (empty)
  * - storage.max.items.in.page
    - Número máximo de elementos por página en el almacenamiento.
    - ``1000``
  * - password.invalid.admin.passwords
    - Lista de contraseñas de administrador no válidas.
    - ``admin``
  * - password.min.length
    - Longitud mínima de la contraseña (0 para deshabilitar).
    - ``8``
  * - password.max.length
    - Longitud máxima de un campo de contraseña.
    - ``100``
  * - password.require.uppercase
    - Exigir letras mayúsculas en la contraseña.
    - ``false``
  * - password.require.lowercase
    - Exigir letras minúsculas en la contraseña.
    - ``false``
  * - password.require.digit
    - Exigir dígitos en la contraseña.
    - ``false``
  * - password.require.special.char
    - Exigir caracteres especiales en la contraseña.
    - ``false``
  * - rag.chat.enabled
    - Indica si la funcionalidad de chat RAG está habilitada.
    - ``false``
  * - rag.chat.log.enabled
    - Indica si se registra el uso de cada solicitud de chat RAG (usuario, hora, llamadas al LLM y tokens) en el registro del chat. La pregunta y la respuesta nunca se registran.
    - ``true``
  * - rag.chat.context.max.documents
    - Configuración de la generación del chat.
    - ``5``
  * - rag.chat.query.regeneration.max.count
    - Número máximo de veces que una solicitud de chat regenera su consulta de búsqueda y vuelve a buscar cuando la búsqueda no encuentra documentos o, en el chat en streaming, ninguno de los resultados se considera relevante. Cada regeneración realiza una llamada al LLM, más una llamada de evaluación de relevancia cuando la nueva búsqueda tiene resultados (0 lo deshabilita).
    - ``2``
  * - rag.chat.session.timeout.minutes
    - Configuración de sesiones.
    - ``30``
  * - rag.chat.session.max.size
    - Número máximo de sesiones de chat en caché; las de acceso menos reciente se desalojan cuando se supera (0 o menos significa 100).
    - ``10000``
  * - rag.chat.history.max.messages
    - Número máximo de mensajes que se conservan en una sesión de chat; los turnos más antiguos se recortan con cada mensaje nuevo.
    - ``30``
  * - rag.chat.content.fields
    - Configuración del flujo RAG mejorado. Campos que se recuperan para el contenido completo del documento.
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - Configuración de resaltado para la búsqueda RAG.
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - Número de fragmentos de resaltado por documento en la búsqueda de contexto del chat RAG.
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - Manejo de documentos grandes para la generación de respuestas. Los documentos cuyo content_length supera este valor usan pasajes resaltados en lugar del contenido completo en el contexto de la respuesta.
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - Configuración de resaltado que se usa al extraer pasajes de documentos grandes para el contexto de la respuesta.
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - Número de fragmentos de resaltado que se toman de cada documento sobredimensionado para el contexto de la respuesta.
    - ``5``
  * - rag.chat.history.assistant.content
    - Modo de contenido del historial para los mensajes del asistente. smart_summary - descarta el cuerpo del asistente y conserva solo la consulta de búsqueda pasada y los títulos referenciados por turno (predeterminado, recomendado) full - envía la respuesta completa del asistente source_titles - cuerpo + sufijo de títulos referenciados source_titles_and_urls - solo "[References: title (url), ...]" truncated - trunca la respuesta del asistente en history.assistant.max.chars none - descarta los turnos del asistente del historial
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - Número máximo de títulos de documentos referenciados que se incluyen por turno en el modo de historial smart_summary.
    - ``5``
  * - rag.chat.document.max.parts
    - Número máximo de partes en que se divide un documento cuando se chatea sobre un único documento más largo que el presupuesto de contexto del LLM. Cada parte se resume por separado y los resúmenes se combinan en la respuesta; las partes que superan este número no se usan. Una solicitud sobre un documento así realiza hasta este número de llamadas al LLM más una para la respuesta, en cada turno.
    - ``10``
  * - rag.chat.response.language
    - Idioma en el que se pide al LLM que responda. browser - el idioma del navegador del usuario o de la configuración regional de la UI; sin instrucción para el inglés (predeterminado) none - sin instrucción de idioma; el LLM suele responder en el idioma de la pregunta en, ja.. - responder siempre en este idioma
    - ``browser``
  * - index.export.path
    - Exportación de índice
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - Campos de documento, separados por comas, que se omiten en los archivos que escribe el trabajo de exportación del índice.
    - ``cache,tag``
  * - index.export.scroll.size
    - Número de documentos que se obtienen por solicitud de scroll en el trabajo de exportación del índice.
    - ``100``
  * - index.export.format
    - Formato de salida de los documentos exportados; solo se aceptan html y json, cualquier otro hace fallar el trabajo.
    - ``html``
  * - log.notification.flush.interval
    - Notificación de registros Intervalo (segundos) para vaciar el búfer de notificaciones de registros al motor de búsqueda.
    - ``30``
  * - log.notification.max.details.length
    - Longitud máxima del texto de detalles de la notificación.
    - ``3000``
  * - log.notification.max.display.events
    - Número máximo de eventos que se muestran en la notificación.
    - ``50``
  * - log.notification.max.message.length
    - Longitud máxima de cada mensaje de registro en la notificación.
    - ``200``
  * - log.notification.search.size
    - Número máximo de eventos que se obtienen del motor de búsqueda por trabajo de notificación.
    - ``1000``
  * - log.notification.buffer.size
    - Número máximo de eventos que se almacenan en búfer en memoria.
    - ``1000``
  * - log.notification.interval
    - Intervalo (segundos) del ciclo del trabajo de notificación, que se usa en los mensajes de notificación.
    - ``300``
  * - theme.directory.path
    - Sistema de temas estáticos (consulte docs/superpowers/specs/2026-05-21-fess-static-theme-design.md)
    - ``themes``
  * - theme.upload.max.size
    - Tamaño máximo (bytes) de un archivo comprimido de tema cargado.
    - ``52428800``
  * - theme.upload.max.extracted.size
    - Tamaño total extraído máximo (bytes); la extracción se aborta cuando se supera.
    - ``209715200``
  * - theme.upload.max.entries
    - Número máximo de entradas permitidas en un archivo comprimido de tema cargado.
    - ``1000``
  * - theme.upload.max.compression.ratio
    - Relación máxima descomprimido/comprimido para una única entrada de un archivo comprimido de tema.
    - ``100``
  * - theme.upload.zip.ratio.max
    - Relación acumulada máxima descomprimido/comprimido para todo el archivo comprimido (protección contra zip bombs).
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - Bytes comprimidos leídos antes de que se aplique la comprobación acumulada de la relación zip; los archivos comprimidos más pequeños la omiten.
    - ``65536``
  * - theme.upload.attic.retention.days
    - Retención (días) de un directorio de tema reemplazado antes de que el barrido de limpieza lo elimine.
    - ``7``
  * - theme.repositories
    - URLs de repositorios (separadas por comas) desde las que se descargan los temas estáticos.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
  * - theme.index.frame.ancestors
    - Valor de la directiva frame-ancestors de Content-Security-Policy en las páginas HTML del tema estático: los orígenes que pueden incrustarlas en un frame. El valor predeterminado 'none' no permite que ninguna página las incruste. WebKit (Safari) aplica frame-ancestors a los frames blob: que usan la vista previa de archivos y la vista de caché de un tema, por lo que los muestra en blanco mientras el valor es 'none'. Deje el valor vacío para eliminar la directiva; X-Frame-Options: DENY se envía en cualquier caso y entonces mantiene las páginas fuera de los frames en todos los navegadores (un navegador que respeta frame-ancestors ignora ese encabezado).
    - ``'none'``
  * - theme.api.csrf.server.origins
    - Opcional: origen(es) externo(s) canónico(s) de esta instancia de Fess (separados por comas o saltos de línea), p. ej. https://fess.example.com. Cuando se establece, se tratan como del mismo origen para la comprobación de Origin CSRF de v2 SIN confiar en los encabezados reenviados. Recomendado detrás de proxies inversos que no figuran en rate.limit.trusted.proxies. Cuando está vacío, el origen de destino se reconstruye a partir de los encabezados X-Forwarded-\* de los proxies de confianza y, después, de la solicitud de servlet.
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - Intentos de inicio de sesión permitidos por IP de cliente cada minuto; 0 o menos deshabilita el control.
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - Intentos de inicio de sesión permitidos por IP de cliente y nombre de usuario cada minuto; también controla el cambio de contraseña.
    - ``5``
  * - theme.api.login.lockout.seconds
    - Bloqueo (segundos) que se aplica una vez que se supera un límite de tasa de inicio de sesión; 0 o menos deshabilita el bloqueo.
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - Número máximo de buckets de límite de tasa de inicio de sesión que se mantienen en memoria; los buckets inactivos se desalojan al alcanzar el tope.
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - Intervalo entre los pings de keep-alive de SSE que emite /api/v2/chat/stream. El ping es una línea de solo comentario (": keepalive\\n\\n") que no afecta al flujo de eventos pero neutraliza a los intermediarios (el proxy_read_timeout predeterminado de nginx es 60s) que descartan las conexiones inactivas durante las fases largas del LLM. Establezca <=0 para deshabilitarlo. Unidad: milisegundos.
    - ``15000``
.. GENERATED-END: properties
