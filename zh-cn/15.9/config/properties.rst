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

Core
----

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - The title of the domain for logging and display.
    - ``Fess``

.. list-table:: Search Engine
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - The type of search engine backend (e.g., default, opensearch).
    - ``default``
  * - search_engine.http.url
    - The URL of the search engine HTTP endpoint. For IPv6 environments, use brackets around the IPv6 address (e.g., http://[::1]:9200)
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - Path to SSL certificate authorities for secure HTTP connections.
    - (empty)
  * - search_engine.username
    - Username for authenticating to the search engine.
    - (empty)
  * - search_engine.password
    - Password for authenticating to the search engine.
    - (empty)
  * - search_engine.heartbeat_interval
    - Interval (ms) for heartbeat checks to the search engine.
    - ``10000``
  * - app.cipher.algorithm
    - Cipher algorithm used for encryption.
    - ``aes``
  * - app.cipher.key
    - Secret key for encryption (change this value for production).
    - ``___change__me___``
  * - app.digest.algorithm
    - Algorithm for digest calculation.
    - ``sha256``
  * - app.password.algorithm
    - Password hashing (new mechanism, Spring Security v5.8 compatible) Supported: bcrypt (only, as of now)
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - BCrypt cost (log rounds). 10 matches Spring Security v5.8 default. Range: 4-31.
    - ``10``
  * - app.password.upgrade.enabled
    - Lazy re-hashing on successful login for legacy hashes.
    - ``true``
  * - app.encrypt.property.pattern
    - NOTE: app.digest.algorithm is kept for LEGACY password verification only (pre-upgrade hashes that have no {id} prefix). Do not use for new passwords. Regex pattern for properties to encrypt.
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - Regex pattern for sensitive values to mask in debug logs (case-insensitive match against property/env keys).
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - Extension names for application customization.
    - (empty)
  * - app.audit.log.format
    - Audit log format.
    - (empty)
  * - script.audit.log.enabled
    - Script audit log settings.
    - ``true``
  * - script.audit.log.max.length
    - Maximum characters of script text kept in a script audit log entry; longer text is truncated.
    - ``100``
  * - jvm.crawler.options
    - JVM options for the crawler process.
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
    - JVM options (newline-separated) passed to the suggest creator child process.
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
    - JVM options for the chunk vector indexer process. Heap budget. This child JVM is only started while the "Content Chunk Vector Indexer" job runs, so a generous -Xmx costs nothing when content chunking is off. The live set is dominated by the in-flight batches, each of which retains, per document, the full _source, the document's chunk strings, and the document's embedding vectors: content_chunker.job.bulk_size          (default   20) x content_chunker.max_chunks_per_document (default 1000) x content_chunker.embedding.dimension  (default  768) x 4 bytes per float x content_chunker.job.concurrency      (default    2) = ~117 MB of vectors alone, before chunk strings and document sources. With the shipped defaults the worst case is roughly 190-250 MB live (and ~235 MB of vectors alone at dimension=1536), which does not fit a 256 MB heap with any GC headroom. Raise -Xmx further if you raise bulk_size, max_chunks_per_document, concurrency, or the embedding dimension.
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
    - JVM options for the thumbnail process.
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

.. list-table:: Job
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - System job IDs for scheduled jobs.
    - ``default_crawler``
  * - job.template.title.web
    - Template for web crawler job title.
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - Template for file crawler job title.
    - ``File Crawler - {0}``
  * - job.template.title.data
    - Template for data crawler job title.
    - ``Data Crawler - {0}``
  * - job.template.script
    - Script template for job execution.
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - Maximum number of crawler processes.
    - ``0``
  * - job.default.script
    - Default script language for jobs.
    - ``javascript``
  * - job.system.property.filter.pattern
    - Pattern to filter system properties for jobs.
    - (empty)
  * - processors
    - Number of processors to use.
    - ``0``
  * - java.command.path
    - Path to Java command.
    - ``java``
  * - python.command.path
    - Path to Python command.
    - ``python``
  * - path.encoding
    - Encoding for file paths.
    - ``UTF-8``
  * - use.own.tmp.dir
    - Whether to use a dedicated temporary directory.
    - ``true``
  * - max.log.output.length
    - Maximum length of log output.
    - ``4000``
  * - adaptive.load.control
    - Adaptive load control value.
    - ``50``
  * - web.load.control
    - CPU threshold (%) for web request load control. Returns 429 when CPU >= this value. (100: disabled)
    - ``100``
  * - api.load.control
    - CPU threshold (%) for API request load control. Returns 429 when CPU >= this value. (100: disabled)
    - ``100``
  * - load.control.monitor.interval
    - Interval (seconds) for monitoring OpenSearch CPU load.
    - ``1``
  * - supported.uploaded.js.extentions
    - Supported JavaScript file extensions for upload.
    - ``js``
  * - supported.uploaded.css.extentions
    - Supported CSS file extensions for upload.
    - ``css``
  * - supported.uploaded.media.extentions
    - Supported media file extensions for upload.
    - ``jpg,jpeg,gif,png,swf``
  * - supported.uploaded.files
    - Supported files for upload.
    - ``license.properties``
  * - supported.languages
    - Supported languages.
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - Length of API access token.
    - ``60``
  * - api.access.token.required
    - Whether API access token is required.
    - ``false``
  * - api.access.token.request.parameter
    - API access token request parameter.
    - (empty)
  * - api.admin.access.permissions
    - Permissions for API admin access.
    - ``Radmin-api``
  * - api.search.accept.referers
    - Accepted referers for API search.
    - (empty)
  * - api.search.scroll
    - Whether to enable scroll for API search.
    - ``false``
  * - api.json.response.headers
    - Headers for API JSON response. Access-Control-\* and Timing-Allow-Origin are ignored here (CORS is controlled by api.cors.\* / CorsFilter). Do not set Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - Whether to include exceptions in API JSON response.
    - ``false``
  * - api.gsa.response.headers
    - Headers for API GSA response. Access-Control-\* and Timing-Allow-Origin are ignored here (CORS is controlled by api.cors.\* / CorsFilter). Do not set Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - Whether to include exceptions in API GSA response.
    - ``false``
  * - api.dashboard.response.headers
    - Headers for API dashboard response. Access-Control-\* and Timing-Allow-Origin are ignored here (CORS is controlled by api.cors.\* / CorsFilter). Do not set Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - Allowed origins for CORS. "\*" returns a literal "\*" (the request Origin is NOT reflected) and disables credentials. Set explicit origins (newline- or comma-separated) to allow credentialed cross-origin access.
    - ``*``
  * - api.cors.allow.methods
    - Allowed HTTP methods for CORS.
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - Max age for CORS preflight requests.
    - ``3600``
  * - api.cors.allow.headers
    - Allowed request headers for CORS preflight. A static list is returned (Access-Control-Request-Headers is not reflected). Includes X-Fess-CSRF-Token for cross-origin SPAs sending the CSRF token.
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - Whether to allow credentials for CORS. Honored only for an exact match of an explicit Origin; ignored when api.cors.allow.origin is "\*".
    - ``true``
  * - api.jsonp.enabled
    - Whether to enable JSONP for API.
    - ``false``
  * - api.ping.search_engine.fields
    - Fields for API ping to search engine.
    - ``status,timed_out``

Rate Limiting
-------------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - Whether rate limiting is enabled.
    - ``false``
  * - rate.limit.requests.per.window
    - Maximum number of requests allowed per window.
    - ``100``
  * - rate.limit.window.ms
    - Window size in milliseconds.
    - ``60000``
  * - rate.limit.block.duration.ms
    - Duration in milliseconds to block IP when limit exceeded.
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Retry-After header value in seconds.
    - ``60``
  * - rate.limit.whitelist.ips
    - Comma-separated list of whitelisted IPs (e.g., 127.0.0.1,::1).
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - Comma-separated list of blocked IPs.
    - (empty)
  * - rate.limit.trusted.proxies
    - Comma-separated list of trusted proxy IPs. Only trust X-Forwarded-For/X-Real-IP from these IPs.
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - Number of requests between cleanup operations to prevent memory leaks.
    - ``1000``
  * - virtual.host.headers
    - Virtual Host: Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - Hostname for the HTTP proxy server.
    - (empty)
  * - http.proxy.port
    - Port number for the HTTP proxy server (e.g., 8080).
    - ``8080``
  * - http.proxy.username
    - Username for HTTP proxy authentication.
    - (empty)
  * - http.proxy.password
    - Password for HTTP proxy authentication.
    - (empty)
  * - http.fileupload.max.size
    - Maximum size (bytes) for HTTP file uploads.
    - ``262144000``
  * - http.fileupload.threshold.size
    - Threshold size (bytes) for HTTP file upload buffering.
    - ``262144``
  * - http.fileupload.max.file.count
    - Maximum number of files allowed per HTTP upload.
    - ``10``

Index
-----

.. list-table:: Crawler Common
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - Number of threads for HTTP crawling.
    - ``0``
  * - crawler.data.serializer
    - Serializer type for crawler data (e.g., kryo).
    - ``kryo``
  * - crawler.document.max.site.length
    - Maximum length of site name in documents.
    - ``100``
  * - crawler.document.site.encoding
    - Encoding for site names in documents.
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - Hostname to use when unknown in documents.
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - Whether to use site encoding for English documents.
    - ``false``
  * - crawler.document.append.data
    - Whether to append data to documents.
    - ``true``
  * - crawler.document.append.filename
    - Whether to append filename to documents.
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - Maximum size of alphanumeric terms in documents.
    - ``20``
  * - crawler.document.max.symbol.term.size
    - Maximum size of symbol terms in documents.
    - ``10``
  * - crawler.document.duplicate.term.removed
    - Whether to remove duplicate terms in documents.
    - ``false``
  * - crawler.document.space.chars
    - Unicode space characters for document parsing.
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - Unicode full stop characters for document parsing.
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - Encoding for crawling data.
    - ``UTF-8``
  * - crawler.web.protocols
    - Supported web protocols for crawling.
    - ``http,https``
  * - crawler.file.protocols
    - Supported file protocols for crawling.
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - Pattern for environment variable keys in crawling data.
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - Whether to ignore robots.txt during crawling.
    - ``false``
  * - crawler.ignore.robots.tags
    - Whether to ignore robots meta tags during crawling.
    - ``false``
  * - crawler.ignore.content.exception
    - Whether to ignore content exceptions during crawling.
    - ``true``
  * - crawler.failure.url.status.codes
    - HTTP status codes considered as failure URLs.
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - Interval (seconds) for system monitor during crawling.
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - Whether to ignore idle threads in hot thread monitoring.
    - ``true``
  * - crawler.hotthread.interval
    - Interval for hot thread monitoring (e.g., 500ms).
    - ``500ms``
  * - crawler.hotthread.snapshots
    - Number of snapshots for hot thread monitoring.
    - ``10``
  * - crawler.hotthread.threads
    - Number of threads for hot thread monitoring.
    - ``3``
  * - crawler.hotthread.timeout
    - Timeout for hot thread monitoring (e.g., 30s).
    - ``30s``
  * - crawler.hotthread.type
    - Type of hot thread monitoring (e.g., cpu).
    - ``cpu``
  * - crawler.metadata.content.excludes
    - Metadata fields to exclude from document content.
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - Mapping for document metadata names.
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``

.. list-table:: Crawler HTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - XPath to extract main content from HTML documents.
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - XPath to extract language attribute from HTML documents.
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - XPath to extract digest (description) from HTML documents.
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - XPath to extract canonical URL from HTML documents.
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - HTML tags to prune (remove) during document processing.
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - Maximum length of digest extracted from HTML documents.
    - ``120``
  * - crawler.document.html.default.lang
    - Default language for HTML documents.
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - Patterns to include for HTML index processing.
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - Patterns to exclude for HTML index processing.
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - Patterns to include for HTML search processing.
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - Patterns to exclude for HTML search processing.
    - (empty)

.. list-table:: Crawler File
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - Encoding for file names in documents.
    - (empty)
  * - crawler.document.file.no.title.label
    - Label to use when a file has no title.
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - Whether to ignore files with empty content.
    - ``false``
  * - crawler.document.file.max.title.length
    - Maximum length of file title in documents.
    - ``100``
  * - crawler.document.file.max.digest.length
    - Maximum length of file digest in documents.
    - ``200``
  * - crawler.document.file.append.meta.content
    - Whether to append meta content from files.
    - ``true``
  * - crawler.document.file.append.body.content
    - Whether to append body content from files.
    - ``true``
  * - crawler.document.file.default.lang
    - Default language for file documents.
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - Patterns to include for file index processing.
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - Patterns to exclude for file index processing.
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - Patterns to include for file search processing.
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - Patterns to exclude for file search processing.
    - (empty)

.. list-table:: Crawler Cache
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - Whether document cache is enabled.
    - ``true``
  * - crawler.document.cache.max.size
    - Maximum size (bytes) for document cache.
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - Supported MIME types for document cache.
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation MIME types for HTML document cache.
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - Extension-to-MIME-type override mappings for MIME type detection (one per line: .ext=mime/type).
    - (empty)

.. list-table:: Indexer
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - Whether to enable thread dump for the indexer.
    - ``true``
  * - indexer.unprocessed.document.size
    - Maximum number of unprocessed documents for the indexer.
    - ``1000``
  * - indexer.click.count.enabled
    - Whether to enable click count tracking in the indexer.
    - ``true``
  * - indexer.favorite.count.enabled
    - Whether to enable favorite count tracking in the indexer.
    - ``true``
  * - indexer.webfs.commit.margin.time
    - Commit margin time (ms) for webfs in the indexer.
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - Maximum number of empty lists for webfs in the indexer.
    - ``3600``
  * - indexer.webfs.update.interval
    - Update interval (ms) for webfs in the indexer.
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - Maximum document cache size for webfs in the indexer.
    - ``10``
  * - indexer.webfs.max.document.request.size
    - Maximum document request size (bytes) for webfs in the indexer.
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - Maximum document cache size for data in the indexer.
    - ``10000``
  * - indexer.data.max.document.request.size
    - Maximum document request size (bytes) for data in the indexer.
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - Maximum delete cache size for data in the indexer.
    - ``100``
  * - indexer.data.max.redirect.count
    - Maximum redirect count for data in the indexer.
    - ``10``
  * - indexer.language.fields
    - Fields used for language detection in the indexer.
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - Length of text for language detection in the indexer.
    - ``1000``
  * - indexer.max.result.window.size
    - Maximum result window size for the indexer.
    - ``10000``
  * - indexer.max.search.doc.size
    - Maximum number of search documents for the indexer.
    - ``50000``

.. list-table:: Index Settings
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - Codec type for the index.
    - ``default``
  * - index.number_of_shards
    - Number of primary shards for the index.
    - ``5``
  * - index.auto_expand_replicas
    - Auto expand replicas setting for the index.
    - ``0-1``
  * - index.id.digest.algorithm
    - Digest algorithm for index IDs.
    - ``SHA-512``
  * - index.user.initial_password
    - Initial password for the index user.
    - ``admin``

.. list-table:: Field Names
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - Field name for favorite count in the index.
    - ``favorite_count``
  * - index.field.click_count
    - Field name for click count in the index.
    - ``click_count``
  * - index.field.config_id
    - Field name for config ID in the index.
    - ``config_id``
  * - index.field.expires
    - Field name for expiration date in the index.
    - ``expires``
  * - index.field.url
    - Field name for URL in the index.
    - ``url``
  * - index.field.doc_id
    - Field name for document ID in the index.
    - ``doc_id``
  * - index.field.id
    - Field name for internal ID in the index.
    - ``_id``
  * - index.field.version
    - Field name for version in the index.
    - ``_version``
  * - index.field.seq_no
    - Field name for sequence number in the index.
    - ``_seq_no``
  * - index.field.primary_term
    - Field name for primary term in the index.
    - ``_primary_term``
  * - index.field.lang
    - Field name for language in the index.
    - ``lang``
  * - index.field.has_cache
    - Field name for cache status in the index.
    - ``has_cache``
  * - index.field.last_modified
    - Field name for last modified date in the index.
    - ``last_modified``
  * - index.field.anchor
    - Field name for anchor in the index.
    - ``anchor``
  * - index.field.segment
    - Field name for segment in the index.
    - ``segment``
  * - index.field.role
    - Field name for role in the index.
    - ``role``
  * - index.field.boost
    - Field name for boost value in the index.
    - ``boost``
  * - index.field.created
    - Field name for creation date in the index.
    - ``created``
  * - index.field.timestamp
    - Field name for timestamp in the index.
    - ``timestamp``
  * - index.field.label
    - Field name for label in the index.
    - ``label``
  * - index.field.mimetype
    - Field name for MIME type in the index.
    - ``mimetype``
  * - index.field.parent_id
    - Field name for parent ID in the index.
    - ``parent_id``
  * - index.field.important_content
    - Field name for important content in the index.
    - ``important_content``
  * - index.field.content
    - Field name for content in the index.
    - ``content``
  * - index.field.content_minhash_bits
    - Field name for content minhash bits in the index.
    - ``content_minhash_bits``
  * - index.field.cache
    - Field name for cache in the index.
    - ``cache``
  * - index.field.digest
    - Field name for digest in the index.
    - ``digest``
  * - index.field.title
    - Field name for title in the index.
    - ``title``
  * - index.field.host
    - Field name for host in the index.
    - ``host``
  * - index.field.site
    - Field name for site in the index.
    - ``site``
  * - index.field.content_length
    - Field name for content length in the index.
    - ``content_length``
  * - index.field.filetype
    - Field name for file type in the index.
    - ``filetype``
  * - index.field.filename
    - Field name for file name in the index.
    - ``filename``
  * - index.field.thumbnail
    - Field name for thumbnail in the index.
    - ``thumbnail``
  * - index.field.virtual_host
    - Field name for virtual host in the index.
    - ``virtual_host``
  * - response.field.content_title
    - Field name for content title in the response.
    - ``content_title``
  * - response.field.content_description
    - Field name for content description in the response.
    - ``content_description``
  * - response.field.url_link
    - Field name for URL link in the response.
    - ``url_link``
  * - response.field.site_path
    - Field name for site path in the response.
    - ``site_path``
  * - response.max.title.length
    - Maximum length of content title in the response.
    - ``50``
  * - response.max.site.path.length
    - Maximum length of site path in the response.
    - ``100``
  * - response.highlight.content_title.enabled
    - Whether to enable content title highlighting in the response.
    - ``true``
  * - response.inline.mimetypes
    - Inline MIME types for the response.
    - ``application/pdf,text/plain``
  * - response.headers
    - HTTP headers for the response. Access-Control-\* and Timing-Allow-Origin are ignored (CORS is controlled by api.cors.\* / CorsFilter). Do not set Vary here.
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=Content-Security-Policy: reflected-xss block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: Document Index
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - Index name for search documents.
    - ``fess.search``
  * - index.document.update.index
    - Index name for update documents.
    - ``fess.update``
  * - index.document.suggest.index
    - Index name for suggest documents.
    - ``fess``
  * - index.document.crawler.index
    - Index name for crawler documents.
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - Number of primary shards for crawler queue index.
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - Number of primary shards for crawler data index.
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - Number of primary shards for crawler filter index.
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - Number of replicas for crawler queue index.
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - Number of replicas for crawler data index.
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - Number of replicas for crawler filter index.
    - ``1``
  * - index.config.index
    - Index name for configuration data.
    - ``fess_config``
  * - index.user.index
    - Index name for user data.
    - ``fess_user``
  * - index.log.index
    - Index name for log data.
    - ``fess_log``
  * - index.dictionary.prefix
    - Prefix for dictionary index names.
    - (empty)

.. list-table:: Document Management
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - Array-type fields for admin in the index.
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - Date-type fields for admin in the index.
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - Integer-type fields for admin in the index.
    - (empty)
  * - index.admin.long.fields
    - Long-type fields for admin in the index.
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - Float-type fields for admin in the index.
    - ``boost``
  * - index.admin.double.fields
    - Double-type fields for admin in the index.
    - (empty)
  * - index.admin.required.fields
    - Required fields for admin in the index.
    - ``url,title,role,boost``

.. list-table:: Timeouts
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - Timeout for index search operations.
    - ``3m``
  * - index.scroll.search.timeout
    - Timeout for scroll search operations.
    - ``3m``
  * - index.index.timeout
    - Timeout for index operations.
    - ``3m``
  * - index.bulk.timeout
    - Timeout for bulk index operations.
    - ``3m``
  * - index.delete.timeout
    - Timeout for delete operations in the index.
    - ``3m``
  * - index.health.timeout
    - Timeout for index health checks.
    - ``10m``
  * - index.indices.timeout
    - Timeout for index indices operations.
    - ``1m``

.. list-table:: File Types
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - Mapping of MIME types to filetype labels for indexing.
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
    - Number of documents to process per reindex operation.
    - ``100``
  * - index.reindex.body
    - Request body template for reindex operations.
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - Requests per second for reindex operations ("adaptive" for auto).
    - ``adaptive``
  * - index.reindex.refresh
    - Whether to refresh the index after reindexing.
    - ``false``
  * - index.reindex.timeout
    - Timeout for reindex operations.
    - ``1m``
  * - index.reindex.scroll
    - Scroll timeout for reindex operations.
    - ``5m``
  * - index.reindex.max_docs
    - Maximum number of documents for reindex operations.
    - (empty)

.. list-table:: Query
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - Maximum length of search queries.
    - ``1000``
  * - query.timeout
    - Timeout (ms) for search queries.
    - ``10000``
  * - query.timeout.logging
    - Whether to enable logging for query timeouts.
    - ``true``
  * - query.track.total.hits
    - Maximum number of total hits to track in queries. Only a positive number or true is supported: false leaves the response without a hit count, and a search that asks for it, here or as a search parameter, is refused.
    - ``10000``
  * - query.geo.fields
    - Fields used for geo search queries.
    - ``location``
  * - query.browser.lang.parameter.name
    - Parameter name for browser language in queries.
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - Whether to replace term with prefix query.
    - ``true``
  * - query.orsearch.min.hit.count
    - Minimum hit count for OR search queries.
    - ``-1``
  * - query.highlight.terminal.chars
    - Unicode terminal characters for query highlighting.
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - Fragment size for query highlighting.
    - ``60``
  * - query.highlight.number.of.fragments
    - Number of fragments for query highlighting.
    - ``2``
  * - query.highlight.type
    - Type of query highlighting.
    - ``fvh``
  * - query.highlight.tag.pre
    - Tag to use before highlighted text.
    - ``<strong>``
  * - query.highlight.tag.post
    - Tag to use after highlighted text.
    - ``</strong>``
  * - query.highlight.boundary.chars
    - Boundary characters for query highlighting.
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - Maximum scan for query highlight boundaries.
    - ``20``
  * - query.highlight.boundary.scanner
    - Scanner type for query highlight boundaries.
    - ``chars``
  * - query.highlight.encoder
    - Encoder type for query highlighting.
    - ``default``
  * - query.highlight.force.source
    - Whether to force source for query highlighting.
    - ``false``
  * - query.highlight.fragmenter
    - Fragmenter type for query highlighting.
    - ``span``
  * - query.highlight.fragment.offset
    - Offset for query highlight fragments.
    - ``-1``
  * - query.highlight.no.match.size
    - Size for no-match query highlight.
    - ``0``
  * - query.highlight.order
    - Order for query highlight fragments.
    - ``score``
  * - query.highlight.phrase.limit
    - Phrase limit for query highlighting.
    - ``256``
  * - query.highlight.content.description.fields
    - Fields for content description in query highlighting.
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - Whether to detect boundary position in query highlighting.
    - ``true``
  * - query.highlight.text.fragment.type
    - Type for text fragment in query highlighting.
    - ``query``
  * - query.highlight.text.fragment.size
    - Size for text fragment in query highlighting.
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - Prefix length for text fragment in query highlighting.
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - Suffix length for text fragment in query highlighting.
    - ``5``
  * - query.max.search.result.offset
    - Maximum search result offset for queries.
    - ``100000``
  * - query.additional.default.fields
    - Additional default fields for queries.
    - (empty)
  * - query.additional.response.fields
    - Additional response fields for queries.
    - (empty)
  * - query.additional.api.response.fields
    - Additional API response fields for queries. This key only appends fields to the v2 API response allow-list (add-only). Do not add ACL or internal fields (for example role, virtual_host); adding them would expose access-control information in the search API response.
    - (empty)
  * - query.additional.scroll.response.fields
    - Additional scroll response fields for queries.
    - (empty)
  * - query.additional.cache.response.fields
    - Additional cache response fields for queries.
    - (empty)
  * - query.additional.highlighted.fields
    - Additional highlighted fields for queries.
    - (empty)
  * - query.additional.search.fields
    - Additional search fields for queries.
    - (empty)
  * - query.additional.facet.fields
    - Additional facet fields for queries.
    - (empty)
  * - query.additional.sort.fields
    - Additional sort fields for queries.
    - (empty)
  * - query.additional.analyzed.fields
    - Additional analyzed fields for queries.
    - (empty)
  * - query.additional.not.analyzed.fields
    - Additional not-analyzed fields for queries.
    - (empty)
  * - query.gsa.response.fields
    - Fields for GSA response in queries.
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - Default language for GSA queries.
    - ``en``
  * - query.gsa.default.sort
    - Default sort for GSA queries.
    - (empty)
  * - query.gsa.meta.prefix
    - Meta prefix for GSA queries.
    - ``MT_``
  * - query.gsa.index.field.charset
    - Charset field for GSA index queries.
    - ``charset``
  * - query.gsa.index.field.content_type.
    - Content type field for GSA index queries.
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - Maximum concurrent group results for collapse queries.
    - ``4``
  * - query.collapse.inner.hits.name
    - Inner hits name for collapse queries.
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - Inner hits size for collapse queries.
    - ``0``
  * - query.collapse.inner.hits.sorts
    - Sorts for inner hits in collapse queries.
    - (empty)
  * - query.default.languages
    - Default languages for queries.
    - (empty)
  * - query.json.default.preference
    - Default preference for JSON queries.
    - ``_query``
  * - query.gsa.default.preference
    - Default preference for GSA queries.
    - ``_query``
  * - query.language.mapping
    - Language mapping for queries.
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

.. list-table:: Boost
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - Boost value for title field in queries.
    - ``0.5``
  * - query.boost.title.lang
    - Boost value for title field with language in queries.
    - ``1.0``
  * - query.boost.content
    - Boost value for content field in queries.
    - ``0.05``
  * - query.boost.content.lang
    - Boost value for content field with language in queries.
    - ``0.1``
  * - query.boost.important_content
    - Boost value for important content field in queries.
    - ``-1.0``
  * - query.boost.important_content.lang
    - Boost value for important content field with language in queries.
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - Minimum length for fuzzy boosting in queries.
    - ``4``
  * - query.boost.fuzzy.title
    - Boost value for fuzzy title queries.
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - Fuzziness for fuzzy title queries.
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - Number of expansions for fuzzy title queries.
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - Prefix length for fuzzy title queries.
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - Whether to allow transpositions in fuzzy title queries.
    - ``true``
  * - query.boost.fuzzy.content
    - Boost value for fuzzy content queries.
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - Fuzziness for fuzzy content queries.
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - Number of expansions for fuzzy content queries.
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - Prefix length for fuzzy content queries.
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - Whether to allow transpositions in fuzzy content queries.
    - ``true``
  * - query.default.query_type
    - Default query type.
    - ``bool``
  * - query.dismax.tie_breaker
    - Tie breaker value for dismax queries.
    - ``0.1``
  * - query.bool.minimum_should_match
    - Minimum should match value for boolean queries.
    - (empty)
  * - query.prefix.expansions
    - Number of expansions for prefix queries.
    - ``50``
  * - query.prefix.slop
    - Slop value for prefix queries.
    - ``0``
  * - query.fuzzy.prefix_length
    - Prefix length for fuzzy queries.
    - ``0``
  * - query.fuzzy.expansions
    - Number of expansions for fuzzy queries.
    - ``50``
  * - query.fuzzy.transpositions
    - Whether to allow transpositions in fuzzy queries.
    - ``true``

.. list-table:: Facet
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - Fields for facet queries.
    - ``label``
  * - query.facet.fields.size
    - Size of facet fields.
    - ``100``
  * - query.facet.fields.size.max
    - Upper clamp for facet.size (applied at the search chokepoint).
    - ``1000``
  * - query.facet.fields.min_doc_count
    - Minimum document count for facet fields.
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - Upper clamp for facet.minDocCount (applied at the search chokepoint).
    - ``2147483647``
  * - query.facet.fields.sort
    - Sort order for facet fields.
    - ``count.desc``
  * - query.facet.fields.missing
    - Value for missing facet fields.
    - (empty)
  * - query.facet.queries
    - Facet queries definition.
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: Ranking
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Window size for rank fusion.
    - ``200``
  * - rank.fusion.rank_constant
    - Rank constant for rank fusion.
    - ``20``
  * - rank.fusion.threads
    - Number of threads for rank fusion.
    - ``-1``
  * - rank.fusion.score_field
    - Score field for rank fusion.
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - Whether the search engine performs rank fusion. When true, the searchers that can take part contribute their queries to a single request, so facets and total hits describe the fused result set. When false, Fess fuses the searchers' results itself.
    - ``false``
  * - rank.fusion.combination.technique
    - How the search engine combines the fused scores: rrf, arithmetic_mean, geometric_mean or harmonic_mean.
    - ``rrf``
  * - rank.fusion.normalization.technique
    - How scores are normalized before they are combined: min_max, l2 or z_score. Ignored by rrf.
    - ``min_max``
  * - rank.fusion.combination.weights
    - Weight per searcher for engine-side fusion, as name:weight pairs, e.g. default:0.7,semantic_chunk:0.3. The weights must sum to 1.0 and must name every searcher taking part. Empty weights them equally.
    - (empty)
  * - rank.fusion.pagination_depth
    - How many results each searcher contributes per shard to engine-side fusion. This bounds both how deep a client can page and the set of documents the engine ranks.
    - ``200``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - Whether to get SMB roles from a file.
    - ``true``
  * - smb.available.sid.types
    - Available SID types for SMB.
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - Whether to get file roles from a file.
    - ``true``
  * - ftp.role.from.file
    - Whether to get FTP roles from a file.
    - ``true``

.. list-table:: Backup
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - Target files for index backup.
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - Target log files for index backup.
    - ``click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - Timeout for loading index backup logs.
    - ``60000``

.. list-table:: Logging
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - Application packages for logging.
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - Whether to enable search docs logging.
    - ``true``
  * - logging.search.docs.fields
    - Fields to log for search docs.
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - Whether to use a log file for search logging.
    - ``true``
  * - logging.search.max.queue.size
    - Maximum queue size for search logging.
    - ``10000``
  * - logging.click.max.queue.size
    - Maximum queue size for click logging.
    - ``10000``

Web
---

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - Maximum input size for admin forms.
    - ``10000``
  * - form.admin.label.in.config.enabled
    - Whether to enable label in admin config forms.
    - ``false``
  * - form.admin.default.template.name
    - Default template name for admin forms.
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - Whether to enable OSDD link (OpenSearch Description Document).
    - ``auto``
  * - clipboard.copy.icon.enabled
    - Whether to enable the clipboard copy icon.
    - ``true``
  * - authentication.admin.users
    - Admin user names for authentication.
    - ``admin``
  * - authentication.admin.users.ignore.case
    - Whether to match authentication.admin.users without regard to case: auto, true or false. auto ignores case when ldap.provider.url is set.
    - ``auto``
  * - authentication.admin.roles
    - Admin role names for authentication.
    - ``admin``
  * - role.search.default.permissions
    - Default permissions for search roles.
    - (empty)
  * - role.search.default.display.permissions
    - Default display permissions for search roles.
    - ``{role}guest``
  * - role.search.guest.permissions
    - Keep role.search.guest.permissions non-empty. It seeds the guest role that keeps the anonymous search role set non-empty; if the resolved role set is empty the role filter is skipped (fail-open), which can disable role-based access control and expose documents to anonymous users. Guest permissions for search roles.
    - ``{role}guest``
  * - role.search.user.prefix
    - Prefix for user roles in search.
    - ``1``
  * - role.search.group.prefix
    - Prefix for group roles in search.
    - ``2``
  * - role.search.role.prefix
    - Prefix for role roles in search.
    - ``R``
  * - role.search.denied.prefix
    - Prefix for denied roles in search.
    - ``D``
  * - cookie.default.path
    - The default path of cookie (basically '/' if no context path)
    - ``/``
  * - cookie.default.expire
    - The default expire of cookie in seconds e.g. 31556926: one year, 86400: one day
    - ``3600``
  * - session.tracking.modes
    - Session tracking modes
    - ``cookie``
  * - session.cookie.secure
    - Whether to add the Secure attribute to the session cookie (JSESSIONID) at startup. When blank (default), Tomcat's automatic behavior is used (Secure is added only for HTTPS requests). Set to true for production HTTPS deployments, especially when TLS is terminated at a reverse proxy. When true, the cookie is not sent over HTTP, so sessions will not be established for plain HTTP; keep it blank for localhost development. The Secure attribute is also required when SameSite=none is used. Changing this value requires a restart.
    - (empty)
  * - cookie.search.parameter.keys
    - Comma-separated list of request parameter keys to store in cookies before SSO login.
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - Comma-separated list of required parameter keys that must be present to store in cookies.
    - ``q``
  * - cookie.search.parameter.max.length
    - Maximum length of the encoded search parameters stored in cookies.
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - Maximum size in bytes the stored search parameters may decompress to. The bound above applies to the gzipped cookie, which is no bound on what it expands to, and the cookie comes from the client.
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - Maximum length of the query string built when restoring the stored search parameters after login. Restoring them is a convenience and the login is not, so a longer one is dropped rather than written to a Location header the container would refuse. Percent-encoding multiplies a CJK query by nine, so this is far smaller than the query itself may be. Raise it together with tomcat.maxHttpHeaderSize in tomcat_config.properties, which bounds the response headers.
    - ``4096``
  * - cookie.search.parameter.name
    - Cookie name used to store encoded search parameters before SSO login.
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - Whether to set HttpOnly attribute to the search parameter cookie.
    - ``true``
  * - cookie.search.parameter.secure
    - Whether to set Secure attribute to the search parameter cookie. Should be true in production environments using HTTPS.
    - (empty)
  * - cookie.search.parameter.max_age
    - Max-Age (in seconds) for the search parameter cookie. Use -1 for session-only cookies.
    - ``60``
  * - cookie.search.parameter.domain
    - Domain attribute for the search parameter cookie. Set to the domain scope you want the cookie to be available on (e.g., example.com).
    - (empty)
  * - cookie.search.parameter.path
    - Path attribute for the search parameter cookie. Typically set to "/" or the context path of the app.
    - ``/``
  * - cookie.search.parameter.same_site
    - SameSite attribute for the search parameter cookie. Valid values: Lax, Strict, None
    - ``Lax``
  * - paging.page.size
    - The size of one page for paging
    - ``25``
  * - paging.page.range.size
    - The size of page range for paging
    - ``5``
  * - paging.page.range.fill.limit
    - The option 'fillLimit' of page range for paging
    - ``true``

.. list-table:: Fetch Page Size
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - Maximum number of docboost records to fetch per page.
    - ``1000``
  * - page.keymatch.max.fetch.size
    - Maximum number of keymatch records to fetch per page.
    - ``1000``
  * - page.labeltype.max.fetch.size
    - Maximum number of labeltype records to fetch per page.
    - ``1000``
  * - page.roletype.max.fetch.size
    - Maximum number of roletype records to fetch per page.
    - ``1000``
  * - page.user.max.fetch.size
    - Maximum number of user records to fetch per page.
    - ``1000``
  * - page.role.max.fetch.size
    - Maximum number of role records to fetch per page.
    - ``1000``
  * - page.group.max.fetch.size
    - Maximum number of group records to fetch per page.
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - Maximum number of crawling info parameters to fetch per page.
    - ``100``
  * - page.crawling.info.max.fetch.size
    - Maximum number of crawling info records to fetch per page.
    - ``1000``
  * - page.data.config.max.fetch.size
    - Maximum number of data config records to fetch per page.
    - ``100``
  * - page.web.config.max.fetch.size
    - Maximum number of web config records to fetch per page.
    - ``100``
  * - page.file.config.max.fetch.size
    - Maximum number of file config records to fetch per page.
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - Maximum number of duplicate host records to fetch per page.
    - ``1000``
  * - page.failure.url.max.fetch.size
    - Maximum number of failure URL records to fetch per page.
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - Maximum number of favorite log records to fetch per page.
    - ``100``
  * - page.file.auth.max.fetch.size
    - Maximum number of file auth records to fetch per page.
    - ``100``
  * - page.web.auth.max.fetch.size
    - Maximum number of web auth records to fetch per page.
    - ``100``
  * - page.path.mapping.max.fetch.size
    - Maximum number of path mapping records to fetch per page.
    - ``1000``
  * - page.request.header.max.fetch.size
    - Maximum number of request header records to fetch per page.
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - Maximum number of scheduled job records to fetch per page.
    - ``100``
  * - page.elevate.word.max.fetch.size
    - Maximum number of elevate word records to fetch per page.
    - ``1000``
  * - page.bad.word.max.fetch.size
    - Maximum number of bad word records to fetch per page.
    - ``1000``
  * - page.dictionary.max.fetch.size
    - Maximum number of dictionary records to fetch per page.
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - Maximum number of related content records to fetch per page.
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - Maximum number of related query records to fetch per page.
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - Maximum number of thumbnail queue records to fetch per page.
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - Maximum number of thumbnail purge records to fetch per page.
    - ``100``
  * - page.score.booster.max.fetch.size
    - Maximum number of score booster records to fetch per page.
    - ``1000``
  * - page.searchlog.max.fetch.size
    - Maximum number of search log records to fetch per page.
    - ``10000``
  * - page.searchlist.track.total.hits
    - Whether to track total hits in search list page.
    - ``true``
  * - page.searchlist.content.max.length
    - Maximum content length (in characters) rendered on the search list edit page.
    - ``100000``

.. list-table:: Search Page
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - Default start page for search results.
    - ``0``
  * - paging.search.page.size
    - Default size of search results per page.
    - ``10``
  * - paging.search.page.max.size
    - Maximum size of search results per page.
    - ``100``
  * - api.param.max.length
    - Maximum length of a v2 API string query parameter (q, sort, sdh). OWASP API4:2023.
    - ``1000``
  * - api.param.max.array.size
    - Maximum number of values for a v2 API repeatable query parameter.
    - ``100``
  * - api.click.max.timestamp
    - Maximum click-log timestamp (rt, epoch ms) accepted by the v2 click API. OWASP API4:2023.
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - searchlog
    - ``-1``
  * - searchlog.request.headers
    - Request headers to include in search log.
    - (empty)
  * - searchlog.process.batch_size
    - Batch size for search log processing.
    - ``100``
  * - thumbnail.html.image.min.width
    - Minimum width for HTML images in thumbnails.
    - ``100``
  * - thumbnail.html.image.min.height
    - Minimum height for HTML images in thumbnails.
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - Maximum aspect ratio for HTML images in thumbnails.
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - Width of generated thumbnail images.
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - Height of generated thumbnail images.
    - ``100``
  * - thumbnail.html.image.format
    - Format of generated thumbnail images.
    - ``png``
  * - thumbnail.html.image.xpath
    - XPath to select images for thumbnails.
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - File extensions to exclude from thumbnail generation.
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - Interval for thumbnail generator.
    - ``0``
  * - thumbnail.generator.targets
    - Targets for thumbnail generator (e.g., all).
    - ``all``
  * - thumbnail.crawler.enabled
    - Whether the thumbnail crawler is enabled.
    - ``true``
  * - thumbnail.system.monitor.interval
    - Interval for system monitor in thumbnail processing.
    - ``60``

.. list-table:: User
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - User code settings
    - ``userCode``
  * - user.code.min.length
    - User code minimum length.
    - ``20``
  * - user.code.max.length
    - User code maximum length.
    - ``100``
  * - user.code.pattern
    - User code pattern for validation.
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - Name to display in the From field of emails.
    - ``Administrator``
  * - mail.from.address
    - Email address to use in the From field.
    - ``root@localhost``
  * - mail.hostname
    - Hostname for the mail server.
    - (empty)
  * - scheduler.target.name
    - Target name for the scheduler.
    - (empty)
  * - scheduler.job.class
    - Job class for the scheduler.
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - Mode for concurrent execution in the scheduler.
    - ``QUIT``
  * - scheduler.monitor.interval
    - Interval for scheduler monitoring.
    - ``30``
  * - coordinator.poll.interval
    - Interval (seconds) for polling heartbeats and events.
    - ``60``
  * - coordinator.heartbeat.ttl
    - Time-to-live (ms) for instance heartbeat documents.
    - ``180000``
  * - coordinator.operation.ttl
    - Time-to-live (ms) for operation lock documents.
    - ``7200000``
  * - coordinator.operation.retry
    - Maximum number of retries for acquiring an operation lock.
    - ``3``
  * - coordinator.event.ttl
    - Time-to-live (ms) for event notification documents.
    - ``600000``
  * - online.help.base.link
    - Base link for online help.
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - Installation guide link for online help.
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - End-of-life information link for online help.
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - Online help key for failure URL.
    - ``failureurl``
  * - online.help.name.elevateword
    - Online help key for elevate word.
    - ``elevateword``
  * - online.help.name.reqheader
    - Online help key for request header.
    - ``reqheader``
  * - online.help.name.dict.synonym
    - Online help key for synonym dictionary.
    - ``synonym``
  * - online.help.name.dict
    - Online help key for dictionary.
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Online help key for Kuromoji dictionary.
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - Online help key for protected words dictionary.
    - ``protwords``
  * - online.help.name.dict.stopwords
    - Online help key for stopwords dictionary.
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Online help key for stemmer override dictionary.
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - Online help key for mapping dictionary.
    - ``mapping``
  * - online.help.name.webconfig
    - Online help key for web config.
    - ``webconfig``
  * - online.help.name.searchlist
    - Online help key for search list.
    - ``searchlist``
  * - online.help.name.log
    - Online help key for log.
    - ``log``
  * - online.help.name.general
    - Online help key for general settings.
    - ``general``
  * - online.help.name.role
    - Online help key for role.
    - ``role``
  * - online.help.name.joblog
    - Online help key for job log.
    - ``joblog``
  * - online.help.name.keymatch
    - Online help key for keymatch.
    - ``keymatch``
  * - online.help.name.relatedquery
    - Online help key for related query.
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - Online help key for related content.
    - ``relatedcontent``
  * - online.help.name.wizard
    - Online help key for wizard.
    - ``wizard``
  * - online.help.name.badword
    - Online help key for bad word.
    - ``badword``
  * - online.help.name.pathmap
    - Online help key for path mapping.
    - ``pathmap``
  * - online.help.name.boostdoc
    - Online help key for boost document.
    - ``boostdoc``
  * - online.help.name.dataconfig
    - Online help key for data config.
    - ``dataconfig``
  * - online.help.name.systeminfo
    - Online help key for system info.
    - ``systeminfo``
  * - online.help.name.user
    - Online help key for user.
    - ``user``
  * - online.help.name.group
    - Online help key for group.
    - ``group``
  * - online.help.name.design
    - Online help key for design.
    - ``design``
  * - online.help.name.dashboard
    - Online help key for dashboard.
    - ``dashboard``
  * - online.help.name.webauth
    - Online help key for web authentication.
    - ``webauth``
  * - online.help.name.fileconfig
    - Online help key for file config.
    - ``fileconfig``
  * - online.help.name.fileauth
    - Online help key for file authentication.
    - ``fileauth``
  * - online.help.name.labeltype
    - Online help key for label type.
    - ``labeltype``
  * - online.help.name.duplicatehost
    - Online help key for duplicate host.
    - ``duplicatehost``
  * - online.help.name.scheduler
    - Online help key for scheduler.
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - Online help key for crawling info.
    - ``crawlinginfo``
  * - online.help.name.backup
    - Online help key for backup.
    - ``backup``
  * - online.help.name.upgrade
    - Online help key for upgrade.
    - ``upgrade``
  * - online.help.name.sereq
    - Online help key for search request.
    - ``sereq``
  * - online.help.name.accesstoken
    - Online help key for access token.
    - ``accesstoken``
  * - online.help.name.suggest
    - Online help key for suggest.
    - ``suggest``
  * - online.help.name.searchlog
    - Online help key for search log.
    - ``searchlog``
  * - online.help.name.maintenance
    - Online help key for maintenance.
    - ``maintenance``
  * - online.help.name.plugin
    - Online help key for plugin.
    - ``plugin``
  * - online.help.name.storage
    - Online help key for storage.
    - ``storage``
  * - online.help.supported.langs
    - Supported languages for online help.
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - Forum link for user support.
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - Supported languages for the forum.
    - ``en,ja``
  * - suggest.popular.word.seed
    - Seed value for popular word suggestion.
    - ``0``
  * - suggest.popular.word.tags
    - Tags for popular word suggestion.
    - (empty)
  * - suggest.popular.word.fields
    - Fields for popular word suggestion.
    - (empty)
  * - suggest.popular.word.excludes
    - Excluded words for popular word suggestion.
    - (empty)
  * - suggest.popular.word.size
    - Number of popular words to suggest.
    - ``10``
  * - suggest.popular.word.window.size
    - Window size for popular word suggestion.
    - ``30``
  * - suggest.popular.word.query.freq
    - Query frequency for popular word suggestion.
    - ``10``
  * - suggest.min.hit.count
    - Minimum hit count for suggestion.
    - ``1``
  * - suggest.field.contents
    - Field for suggestion contents.
    - ``_default``
  * - suggest.field.tags
    - Field for suggestion tags.
    - ``label``
  * - suggest.field.roles
    - Field for suggestion roles.
    - ``role``
  * - suggest.field.index.contents
    - Index contents for suggestion.
    - ``content,title``
  * - suggest.update.request.interval
    - Interval for suggestion update requests.
    - ``0``
  * - suggest.update.doc.per.request
    - Number of documents per suggestion update request.
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - Percentage limit for suggestion update contents.
    - ``50%``
  * - suggest.update.contents.limit.num
    - Maximum number of suggestion update contents.
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - Maximum document size for suggestion update.
    - ``50000``
  * - suggest.source.reader.scroll.size
    - Scroll size for suggestion source reader.
    - ``1``
  * - suggest.popular.word.cache.size
    - Cache size for popular word suggestion.
    - ``1000``
  * - suggest.popular.word.cache.expire
    - Cache expiration (seconds) for popular word suggestion.
    - ``60``
  * - suggest.search.log.permissions
    - Permissions for suggestion search log.
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - Interval for system monitor in suggestion.
    - ``60``
  * - ldap.admin.enabled
    - Whether LDAP admin is enabled.
    - ``false``
  * - ldap.admin.user.filter
    - User filter for LDAP admin.
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - Base DN for LDAP admin user.
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - Object classes for LDAP admin user.
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - Role filter for LDAP admin.
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - Base DN for LDAP admin role.
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - Object classes for LDAP admin role.
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - Group filter for LDAP admin.
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - Base DN for LDAP admin group.
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - Object classes for LDAP admin group.
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - Whether to sync password for LDAP admin.
    - ``true``
  * - ldap.auth.validation
    - Whether to validate LDAP authentication.
    - ``true``
  * - ldap.connect.timeout
    - Timeout (milliseconds) to establish an LDAP connection. This also bounds the TLS handshake and the initial bind response. 0 or less leaves it to the JDK/OS default.
    - ``10000``
  * - ldap.read.timeout
    - Timeout (milliseconds) to wait for an LDAP response after the connection is bound. 0 or less waits indefinitely.
    - ``30000``
  * - ldap.search.time.limit
    - Server side time limit (milliseconds) for an LDAP search. 0 or less means no limit.
    - ``60000``
  * - ldap.max.username.length
    - Maximum username length for LDAP.
    - ``-1``
  * - ldap.ignore.netbios.name
    - Whether to ignore NetBIOS name in LDAP.
    - ``true``
  * - ldap.group.name.with.underscores
    - Whether to allow underscores in LDAP group names.
    - ``false``
  * - ldap.lowercase.permission.name
    - Whether to use lowercase for LDAP permission names.
    - ``false``
  * - ldap.allow.empty.permission
    - Whether to allow empty permissions in LDAP.
    - ``true``
  * - ldap.samaccountname.group
    - Whether to use samAccountName for LDAP group.
    - ``false``
  * - ldap.role.search.user.enabled
    - Whether LDAP role search for user is enabled.
    - ``true``
  * - ldap.role.search.group.enabled
    - Whether LDAP role search for group is enabled.
    - ``true``
  * - ldap.role.search.role.enabled
    - Whether LDAP role search for role is enabled.
    - ``true``
  * - ldap.attr.surname
    - LDAP attribute for surname.
    - ``sn``
  * - ldap.attr.givenName
    - LDAP attribute for given name.
    - ``givenName``
  * - ldap.attr.employeeNumber
    - LDAP attribute for employee number.
    - ``employeeNumber``
  * - ldap.attr.mail
    - LDAP attribute for mail.
    - ``mail``
  * - ldap.attr.telephoneNumber
    - LDAP attribute for telephone number.
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - LDAP attribute for home phone.
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - LDAP attribute for home postal address.
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - LDAP attribute for labeled URI.
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - LDAP attribute for room number.
    - ``roomNumber``
  * - ldap.attr.description
    - LDAP attribute for description.
    - ``description``
  * - ldap.attr.title
    - LDAP attribute for title.
    - ``title``
  * - ldap.attr.pager
    - LDAP attribute for pager.
    - ``pager``
  * - ldap.attr.street
    - LDAP attribute for street.
    - ``street``
  * - ldap.attr.postalCode
    - LDAP attribute for postal code.
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - LDAP attribute for physical delivery office name.
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - LDAP attribute for destination indicator.
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - LDAP attribute for international ISDN number.
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - LDAP attribute for state.
    - ``st``
  * - ldap.attr.employeeType
    - LDAP attribute for employee type.
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - LDAP attribute for facsimile telephone number.
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - LDAP attribute for post office box.
    - ``postOfficeBox``
  * - ldap.attr.initials
    - LDAP attribute for initials.
    - ``initials``
  * - ldap.attr.carLicense
    - LDAP attribute for car license.
    - ``carLicense``
  * - ldap.attr.mobile
    - LDAP attribute for mobile.
    - ``mobile``
  * - ldap.attr.postalAddress
    - LDAP attribute for postal address.
    - ``postalAddress``
  * - ldap.attr.city
    - LDAP attribute for city.
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - LDAP attribute for teletex terminal identifier.
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - LDAP attribute for X.121 address.
    - ``x121Address``
  * - ldap.attr.businessCategory
    - LDAP attribute for business category.
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - LDAP attribute for registered address.
    - ``registeredAddress``
  * - ldap.attr.displayName
    - LDAP attribute for display name.
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - LDAP attribute for preferred language.
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - LDAP attribute for department number.
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - LDAP attribute for UID number.
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - LDAP attribute for GID number.
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - LDAP attribute for home directory.
    - ``homeDirectory``
  * - plugin.repositories
    - Plugin repository URLs.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - Version filter for plugins.
    - (empty)
  * - storage.max.items.in.page
    - Maximum number of items per page in storage.
    - ``1000``
  * - password.invalid.admin.passwords
    - List of invalid admin passwords.
    - ``admin``
  * - password.min.length
    - Minimum password length (0 to disable).
    - ``8``
  * - password.max.length
    - Maximum length of a password field.
    - ``100``
  * - password.require.uppercase
    - Require uppercase letters in password.
    - ``false``
  * - password.require.lowercase
    - Require lowercase letters in password.
    - ``false``
  * - password.require.digit
    - Require digits in password.
    - ``false``
  * - password.require.special.char
    - Require special characters in password.
    - ``false``
  * - rag.chat.enabled
    - Whether RAG chat feature is enabled.
    - ``false``
  * - rag.chat.context.max.documents
    - Chat generation settings.
    - ``5``
  * - rag.chat.session.timeout.minutes
    - Session settings.
    - ``30``
  * - rag.chat.session.max.size
    - Maximum cached chat sessions; least recently accessed are evicted above it (0 or less means 100).
    - ``10000``
  * - rag.chat.history.max.messages
    - Maximum messages kept in one chat session; older turns are trimmed on each new message.
    - ``30``
  * - rag.chat.content.fields
    - Enhanced RAG flow settings. Fields to retrieve for full document content.
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - Highlight settings for RAG search.
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - Number of highlight fragments per document in the RAG chat context search.
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - Large-document handling for answer generation. Documents whose content_length exceeds this value use highlighted passages instead of full content in the answer context.
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - Highlight settings used when extracting passages from large documents for the answer context.
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - Number of highlight fragments taken from each oversized document for the answer context.
    - ``5``
  * - rag.chat.history.assistant.content
    - History content mode for assistant messages. smart_summary           - drop assistant body, keep only past search query + referenced titles per turn (default, recommended) full                    - send the whole assistant response source_titles           - body + referenced titles suffix source_titles_and_urls  - "[References: title (url), ...]" only truncated               - truncate assistant response at history.assistant.max.chars none                    - drop assistant turns from history
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - Maximum number of referenced document titles included per turn in smart_summary history mode.
    - ``5``
  * - index.export.path
    - Index Export
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - Comma-separated document fields omitted from files written by the index export job.
    - ``cache``
  * - index.export.scroll.size
    - Number of documents fetched per scroll request by the index export job.
    - ``100``
  * - index.export.format
    - Output format for exported documents; only html and json are accepted, anything else fails the job.
    - ``html``
  * - log.notification.flush.interval
    - Log Notification Interval (seconds) for flushing log notification buffer to search engine.
    - ``30``
  * - log.notification.max.details.length
    - Maximum length of notification details text.
    - ``3000``
  * - log.notification.max.display.events
    - Maximum number of events to display in notification.
    - ``50``
  * - log.notification.max.message.length
    - Maximum length of each log message in notification.
    - ``200``
  * - log.notification.search.size
    - Maximum number of events to fetch from search engine per notification job.
    - ``1000``
  * - log.notification.buffer.size
    - Maximum number of events to buffer in memory.
    - ``1000``
  * - log.notification.interval
    - Interval (seconds) for the notification job cycle, used in notification messages.
    - ``300``
  * - theme.directory.path
    - Static theme system (see docs/superpowers/specs/2026-05-21-fess-static-theme-design.md)
    - ``themes``
  * - theme.upload.max.size
    - Maximum size (bytes) of an uploaded theme archive.
    - ``52428800``
  * - theme.upload.max.extracted.size
    - Maximum total extracted size (bytes); extraction aborts once it is exceeded.
    - ``209715200``
  * - theme.upload.max.entries
    - Maximum number of entries allowed in an uploaded theme archive.
    - ``1000``
  * - theme.upload.max.compression.ratio
    - Maximum uncompressed/compressed ratio for a single theme archive entry.
    - ``100``
  * - theme.upload.zip.ratio.max
    - Maximum cumulative uncompressed/compressed ratio for the whole archive (zip-bomb guard).
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - Compressed bytes read before the cumulative zip ratio check applies; smaller archives skip it.
    - ``65536``
  * - theme.upload.attic.retention.days
    - Retention (days) for a replaced theme directory before the cleanup sweep removes it.
    - ``7``
  * - theme.api.csrf.server.origins
    - Optional: canonical external origin(s) of this Fess instance (comma/newline separated), e.g. https://fess.example.com. When set, these are treated as same-origin for the v2 CSRF Origin check WITHOUT trusting forwarded headers. Recommended behind reverse proxies that are not listed in rate.limit.trusted.proxies. When empty, the target origin is reconstructed from trusted-proxy X-Forwarded-\* headers, then from the servlet request.
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - Login attempts allowed per client IP each minute; 0 or less disables the gate.
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - Login attempts allowed per client IP and user name each minute; also gates password change.
    - ``5``
  * - theme.api.login.lockout.seconds
    - Lockout (seconds) applied once a login rate limit is exceeded; 0 or less disables the lockout.
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - Maximum login rate-limit buckets held in memory; idle buckets are evicted at the cap.
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - Interval between SSE keep-alive pings emitted by /api/v2/chat/stream. The ping is a comment-only line (": keepalive\\n\\n") that does not affect the event stream but defeats intermediaries (nginx default proxy_read_timeout is 60s) that drop idle connections during long LLM phases. Set <=0 to disable. Unit: milliseconds.
    - ``15000``
.. GENERATED-END: properties
