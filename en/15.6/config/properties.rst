=============================
Fess Configuration Properties
=============================

This document describes the configuration properties of Fess.
The default values can be found in ``fess_config.properties``

See table bellow for the list of configuration
properties and their descriptions:

Core
----

.. list-table:: Search Engine Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.tile
    - The domain name of the tile server.
    - Fess
  * - search_engine.type
    - The type of search engine.
    - default
  * - search_engine.http.url
    - The URL of the search engine.
    - http://localhost:9201
  * - search_engine.http.ssl.certificate_authorities
    - The path to the certificate authorities file.
    - (empty)
  * - search_engine.username
    - The username for the search engine.
    - (empty)
  * - search_engine.password
    - The password for the search engine.
    - (empty)
  * - search_engine.heartbeat_interval
    - The interval of the heartbeat. (in milliseconds)
    - 10000

.. list-table:: Cryptographer
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - app.cipher.algorism
    - The algorithm for the cipher.
    - aes
  * - app.cipher.key
    - The key for the cipher.
    - (empty)
  * - app.digest.algorism
    - The initialization vector for the cipher.
    - sha256
  * - app.encrypt.key
    - The key for the encryption.
    - (empty)
  * - app.encrypt.property.patterns
    - The patterns for the encryption.
    - ``.*password|.*key|.*token|.*secret``
  * - app.extension.names
    - The names of the extensions.
    - (empty)
  * - app.audit.log.format
    - The format of the audit log.
    - (empty)

.. list-table:: Custom JVM Options
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - jvm.crawler.options
    - The options for the Fess crawler.
    - | -Djava.awt.headless=true\n\
      | -Dfile.encoding=UTF-8\n\
      | -Djna.nosys=true\n\
      | -Djdk.io.permissionsUseCanonicalPath=true\n\
      | -Dhttp.maxConnections=20\n\
      | -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager\n\
      | -server\n\
      | -Xms128m\n\
      | -Xmx512m\n\
      | -XX:MaxMetaspaceSize=128m\n\
      | -XX:CompressedClassSpaceSize=32m\n\
      | -XX:-UseGCOverheadLimit\n\
      | -XX:+UseTLAB\n\
      | -XX:+DisableExplicitGC\n\
      | -XX:-HeapDumpOnOutOfMemoryError\n\
      | -XX:-OmitStackTraceInFastThrow\n\
      | -XX:+UnlockExperimentalVMOptions\n\
      | -XX:+UseG1GC\n\
      | -XX:InitiatingHeapOccupancyPercent=45\n\
      | -XX:G1HeapRegionSize=1m\n\
      | -XX:MaxGCPauseMillis=60000\n\
      | -XX:G1NewSizePercent=5\n\
      | -XX:G1MaxNewSizePercent=5\n\
      | -Djcifs.smb.client.responseTimeout=30000\n\
      | -Djcifs.smb.client.soTimeout=35000\n\
      | -Djcifs.smb.client.connTimeout=60000\n\
      | -Djcifs.smb.client.sessionTimeout=60000\n\
      | -Djcifs.smb1.smb.client.connTimeout=60000\n\
      | -Djcifs.smb1.smb.client.soTimeout=35000\n\
      | -Djcifs.smb1.smb.client.responseTimeout=30000\n\
      | -Dio.netty.noUnsafe=true\n\
      | -Dio.netty.noKeySetOptimization=true\n\
      | -Dio.netty.recycler.maxCapacityPerThread=0\n\
      | -Dlog4j.shutdownHookEnabled=false\n\
      | -Dlog4j2.formatMsgNoLookups=true\n\
      | -Dlog4j2.disable.jmx=true\n\
      | -Dlog4j.skipJansi=true\n\
      | -Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider\n\
      | -Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true\n\
  * - jvm.suggest.options
    - The options for the Fess suggest.
    - | -Djava.awt.headless=true\n\
      | -Dfile.encoding=UTF-8\n\
      | -Djna.nosys=true\n\
      | -Djdk.io.permissionsUseCanonicalPath=true\n\
      | -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager\n\
      | -server\n\
      | -Xms128m\n\
      | -Xmx256m\n\
      | -XX:MaxMetaspaceSize=128m\n\
      | -XX:CompressedClassSpaceSize=32m\n\
      | -XX:-UseGCOverheadLimit\n\
      | -XX:+UseTLAB\n\
      | -XX:+DisableExplicitGC\n\
      | -XX:-HeapDumpOnOutOfMemoryError\n\
      | -XX:+UnlockExperimentalVMOptions\n\
      | -XX:+UseG1GC\n\
      | -XX:InitiatingHeapOccupancyPercent=45\n\
      | -XX:G1HeapRegionSize=1m\n\
      | -XX:MaxGCPauseMillis=60000\n\
      | -XX:G1NewSizePercent=5\n\
      | -XX:G1MaxNewSizePercent=30\n\
      | -Dio.netty.noUnsafe=true\n\
      | -Dio.netty.noKeySetOptimization=true\n\
      | -Dio.netty.recycler.maxCapacityPerThread=0\n\
      | -Dlog4j.shutdownHookEnabled=false\n\
      | -Dlog4j2.disable.jmx=true\n\
      | -Dlog4j2.formatMsgNoLookups=true\n\
      | -Dlog4j.skipJansi=true\n\
  * - jvm.thumbnail.options
    - The options for the Fess thumbnail.
    - | -Djava.awt.headless=true\n\
      | -Dfile.encoding=UTF-8\n\
      | -Djna.nosys=true\n\
      | -Djdk.io.permissionsUseCanonicalPath=true\n\
      | -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager\n\
      | -server\n\
      | -Xms128m\n\
      | -Xmx256m\n\
      | -XX:MaxMetaspaceSize=128m\n\
      | -XX:CompressedClassSpaceSize=32m\n\
      | -XX:-UseGCOverheadLimit\n\
      | -XX:+UseTLAB\n\
      | -XX:+DisableExplicitGC\n\
      | -XX:-HeapDumpOnOutOfMemoryError\n\
      | -XX:-OmitStackTraceInFastThrow\n\
      | -XX:+UnlockExperimentalVMOptions\n\
      | -XX:+UseG1GC\n\
      | -XX:InitiatingHeapOccupancyPercent=45\n\
      | -XX:G1HeapRegionSize=4m\n\
      | -XX:MaxGCPauseMillis=60000\n\
      | -XX:G1NewSizePercent=5\n\
      | -XX:G1MaxNewSizePercent=50\n\
      | -Djcifs.smb.client.responseTimeout=30000\n\
      | -Djcifs.smb.client.soTimeout=35000\n\
      | -Djcifs.smb.client.connTimeout=60000\n\
      | -Djcifs.smb.client.sessionTimeout=60000\n\
      | -Djcifs.smb1.smb.client.connTimeout=60000\n\
      | -Djcifs.smb1.smb.client.soTimeout=35000\n\
      | -Djcifs.smb1.smb.client.responseTimeout=30000\n\
      | -Dio.netty.noUnsafe=true\n\
      | -Dio.netty.noKeySetOptimization=true\n\
      | -Dio.netty.recycler.maxCapacityPerThread=0\n\
      | -Dlog4j.shutdownHookEnabled=false\n\
      | -Dlog4j2.disable.jmx=true\n\
      | -Dlog4j2.formatMsgNoLookups=true\n\
      | -Dlog4j.skipJansi=true\n\
      | -Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider\n\
      | -Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true\n\

.. list-table:: Job Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - The IDs of the system jobs.
    - default_crawler
  * - job.template.title.web
    - The title template for web crawlers.
    - Web Crawler - {0}
  * - job.template.title.file
    - The title template for file crawlers.
    - File Crawler - {0}
  * - job.template.title.data
    - The title template for data crawlers.
    - Data Crawler - {0}
  * - job.template.script
    - The script template for jobs.
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}] as String[]).fileConfigIds([{1}] as String[]).dataConfigIds([{2}] as String[]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - The maximum number of crawler processes.
    - 0
  * - job.default.script
    - The default script for jobs.
    - groovy
  * - job.system.property.filter.pattern
    - The pattern for system property filters.
    - (empty)
  * - processors
    - The processors for the job.
    - 0
  * - java.command.path
    - The path to the Java command.
    - java
  * - python.command.path
    - The path to the Python command.
    - python
  * - path.encoding
    - The encoding for the path.
    - UTF-8
  * - use.own.tmp.dir
    - Whether to use own temporary directory.
    - true
  * - max.log.output.length
    - The maximum length of log output.
    - 4000
  * - adaptive.load.control
    - The adaptive load control value.
    - 50
  * - supported.uploaded.js.extentions
    - The supported extensions for uploaded JavaScript files.
    - js
  * - supported.uploaded.css.extentions
    - The supported extensions for uploaded CSS files.
    - css
  * - supported.uploaded.media.extentions
    - The supported extensions for uploaded media files.
    - jpg,jpeg,gif,png,swf
  * - supported.uploaded.files
    - The supported uploaded files.
    - license.properties
  * - supported.languages
    - The supported languages.
    - ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - api.access.token.length
    - The length of the API access token.
    - 60
  * - api.access.token.required
    - Whether the API access token is required.
    - false
  * - api.access.token.request.parameter
    - The request parameter for the API access token.
    - (empty)
  * - api.search.accept.referers
    - The accepted referers for API search.
    - (empty)
  * - api.search.scroll
    - Enable scroll feature for Search API
    - false
  * - api.json.response.headers
    - The headers for JSON responses in the API.
    - (empty)
  * - api.json.response.exception.included
    - Whether to include exceptions in JSON responses.
    - false
  * - api.gsa.response.headers
    - The headers for GSA responses in the API.
    - (empty)
  * - api.gsa.response.exception.included
    - Whether to include exceptions in GSA responses.
    - false
  * - api.dashboard.response.headers
    - The headers for dashboard responses in the API.
    - (empty)
  * - api.cors.allow.origin
    - The allowed origins for CORS.
    - *
  * - api.cors.allow.methods
    - The allowed methods for CORS.
    - GET, POST, OPTIONS, DELETE, PUT
  * - api.cors.max.age
    - The maximum age for CORS preflight requests.
    - 3600
  * - api.cors.allow.headers
    - The allowed headers for CORS.
    - Origin, Content-Type, Accept, Authorization, X-Requested-With
  * - api.cors.allow.credentials
    - Whether to allow credentials for CORS.
    - true
  * - api.jsonp.enabled
    - Whether JSONP is enabled.
    - false
  * - api.ping.search_engine.fields
    - The fields for pinging the search engine.
    - status,timed_out

.. list-table:: Virtual Host
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - virtual.host.headers
    - The headers for virtual hosts.
    - (empty)

.. list-table:: HTTP Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - http.proxy.Host
    - The host for the HTTP proxy. Leave blank if not using a proxy.
    - (empty)
  * - http.proxy.port
    - The port for the HTTP proxy.
    - 8080
  * - http.proxy.username
    - The username for the HTTP proxy authentication.
    - (empty)
  * - http.proxy.password
    - The password for the HTTP proxy authentication.
    - (empty)
  * - http.fileupload.max.size
    - The maximum size for file uploads.
    - 262144000
  * - http.fileupload.threshold.size
    - The threshold size for file uploads.
    - 262144
  * - http.fileupload.max.file.count
    - The maximum number of files for file uploads at one time.
    - 10

Index
-----

.. list-table:: Crawler Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.default.script
    - The default script for the crawler.
    - groovy
  * - crawler.http.thread_pool.size
    - The size of the HTTP thread pool.
    - 0
  * - crawler.document.max.site.length
    - The maximum length for document sites in lines.
    - 100
  * - crawler.document.site.encoding
    - The encoding for document sites.
    - UTF-8
  * - crawler.document.unknown.hostname
    - The hostname for unknown documents.
    - unknown
  * - crawler.document.use.site.encoding.on.english
    - Whether to use site encoding on English documents.
    - false
  * - crawler.document.append.data
    - Whether to append data to documents.
    - true
  * - crawler.document.append.filename
    - The filename for appending data to documents.
    - false
  * - crawler.document.alphanum.term.size
    - The size for alphanumeric terms in documents.
    - 20
  * - crawler.document.max.symbol.term.size
    - The maximum size for symbol terms in documents.
    - 10
  * - crawler.document.duplicate.term.removed
    - Whether to remove duplicate terms in documents.
    - false
  * - crawler.document.space.chars
    - The space characters for documents.
    - u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6
  * - crawler.document.fullstop.chars
    - The full stop characters for documents.
    - u002eu06d4u2e3cu3002
  * - crawler.crawling.data.encoding
    - The encoding for crawling data.
    - UTF-8
  * - crawler.web.protocols
    - The protocols for web crawling.
    - http,http
  * - crawler.file.protocols
    - The protocols for file crawling.
    - file,smb,smb1,ftp,storage
  * - crawler.data.env.param.key.pattern
    - The regex pattern for Fess environment parameter keys.
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - Whether to ignore robots.txt.
    - false
  * - crawler.ignore.robots.tags
    - The tags to ignore in robots.txt.
    - (empty)
  * - crawler.ignore.content.exception
    - Whether to ignore content exceptions.
    - true
  * - crawler.failure.url.status.codes
    - The status codes for failed URLs.
    - 404
  * - crawler.system.monitor.interval
    - The interval for system monitoring.
    - 60
  * - crawler.hotthread.ignore_idle_threads
    - Whether to ignore idle threads.
    - true
  * - crawler.hotthread.interval
    - The interval for hot threads.
    - 500ms
  * - crawler.hotthread.snapshots
    - The number of snapshots for hot threads.
    - 10
  * - crawler.hotthread.threads
    - The number of threads for hot threads.
    - 3
  * - crawler.hotthread.timeout
    - The timeout for hot threads.
    - 30s
  * - crawler.hotthread.type
    - The type of hot threads.
    - cpu
  * - crawler.metadata.content.excludes
    - The metadata content to exclude.
    - resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*
  * - crawler.metadata.name.mapping
    - The name mapping for metadata.
    - | title=title:string
      | Title=title:string
      | dc:title=title:string

.. list-table:: Crawler HTML Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - The XPath for HTML content.
    - //BODY
  * - crawler.document.html.lang.xpath
    - The XPath for HTML language.
    - //HTML/@lang
  * - crawler.document.html.digest.xpath
    - The XPath for HTML digest.
    - //META[@name='description']/@content
  * - crawler.document.html.canonical.xpath
    - The XPath for HTML canonical link.
    - //LINK[@rel='canonical'][1]/@href
  * - crawler.document.html.pruned.tags
    - The tags to prune from HTML documents.
    - noscript,script,style,header,footer,aside,nav,a[rel=nofollow]
  * - crawler.document.html.max.digest.length
    - The maximum length for HTML digest.
    - 120
  * - crawler.document.html.default.lang
    - The default language for HTML documents.
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - The include index patterns for HTML documents.
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - The exclude index patterns for HTML documents.
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - The include search patterns for HTML documents.
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - The exclude search patterns for HTML documents.
    - (empty)

.. list-table:: Crawler File Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - The encoding for file names.
    - (empty)
  * - crawler.document.file.no.title.label
    - The label for files with no title.
    - No title.
  * - crawler.document.file.ignore.empty.content
    - Whether to ignore empty content in files.
    - false
  * - crawler.document.file.max.title.length
    - The maximum length for file titles.
    - 100
  * - crawler.document.file.max.digest.length
    - The maximum length for file digests.
    - 200
  * - crawler.document.file.append.meta.content
    - Whether to append meta content to files.
    - true
  * - crawler.document.file.append.body.content
    - Whether to append body content to files.
    - true
  * - crawler.document.file.default.lang
    - The default language for files.
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - The include index patterns for files.
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - The exclude index patterns for files.
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - The include search patterns for files.
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - The exclude search patterns for files.
    - (empty)

.. list-table:: Crawler Cache Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - Whether to enable document cache.
    - true
  * - crawler.document.cache.max.size
    - The maximum size for document cache.
    - 2621440
  * - crawler.document.cache.supported.mimetypes
    - The supported MIME types for document cache.
    - text/html
  * - crawler.document.cache.html.mimetypes
    - The HTML MIME types for document cache.
    - text/html

.. list-table:: Indexer Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - Whether to enable thread dump for the indexer.
    - true
  * - indexer.unprocessed.document.size
    - The size of unprocessed documents for the indexer.
    - 1000
  * - indexer.click.count.enabled
    - Whether to enable click count for the indexer.
    - true
  * - indexer.favorite.count.enabled
    - Whether to enable favorite count for the indexer.
    - true
  * - indexer.webfs.commit.margin.time
    - The commit margin time for webfs indexer.
    - 5000
  * - indexer.webfs.max.empty.list.count
    - The maximum empty list count for webfs indexer.
    - 3600
  * - indexer.webfs.update.interval
    - The update interval for webfs indexer.
    - 10000
  * - indexer.webfs.max.document.cache.size
    - The maximum document cache size for webfs indexer.
    - 10
  * - indexer.webfs.max.document.request.size
    - The maximum document request size for webfs indexer.
    - 1048576
  * - indexer.data.max.document.cache.size
    - The maximum document cache size for data indexer.
    - 10000
  * - indexer.data.max.document.request.size
    - The maximum document request size for data indexer.
    - 1048576
  * - indexer.data.max.delete.cache.size
    - The maximum delete cache size for data indexer.
    - 100
  * - indexer.data.max.redirect.count
    - The maximum redirect count for data indexer.
    - 10
  * - indexer.language.fields
    - The language fields for the indexer.
    - content,important_content,title
  * - indexer.language.detect.length
    - The language detect length for the indexer.
    - 1000
  * - indexer.max.result.window.size
    - The maximum result window size for the indexer.
    - 10000
  * - indexer.max.search.doc.size
    - The maximum search document size for the indexer.
    - 50000

.. list-table:: Index Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - The codec for the index.
    - default
  * - index.number_of_shards
    - The number of shards for the index.
    - 5
  * - index.auto_expand_replicas
    - The auto-expand replicas setting for the index.
    - 0-1
  * - index.id.digest.algorithm
    - The digest algorithm for the index ID.
    - SHA-512
  * - index.user.initial_password
    - The initial password for the index user.
    - admin

.. list-table:: Field Names Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - The field for storing the favorite count.
    - favorite_count
  * - index.field.click_count
    - The field for storing the click count.
    - click_count
  * - index.field.config_id
    - The field for storing the configuration ID.
    - config_id
  * - index.field.expires
    - The field for storing the expiration date.
    - expires
  * - index.field.url
    - The field for storing the URL.
    - url
  * - index.field.doc_id
    - The field for storing the document ID.
    - doc_id
  * - index.field.id
    - The field for storing the ID.
    - _id
  * - index.field.version
    - The field for storing the version.
    - _version
  * - index.field.seq_no
    - The field for storing the sequence number.
    - _seq_no
  * - index.field.primary_term
    - The field for storing the primary term.
    - _primary_term
  * - index.field.lang
    - The field for storing the language.
    - lang
  * - index.field.has_cache
    - The field for indicating if the document has cache.
    - has_cache
  * - index.field.last_modified
    - The field for storing the last modified date.
    - last_modified
  * - index.field.anchor
    - The field for storing the anchor.
    - anchor
  * - index.field.segment
    - The field for storing the segment.
    - segment
  * - index.field.role
    - The field for storing the role.
    - role
  * - index.field.boost
    - The field for storing the boost.
    - boost
  * - index.field.created
    - The field for storing the creation date.
    - created
  * - index.field.timestamp
    - The field for storing the timestamp.
    - timestamp
  * - index.field.label
    - The field for storing the label.
    - label
  * - index.field.mimetype
    - The field for storing the MIME type.
    - mimetype
  * - index.field.parent_id
    - The field for storing the parent ID.
    - parent_id
  * - index.field.important_content
    - The field for storing important content.
    - important_content
  * - index.field.content
    - The field for storing the content.
    - content
  * - index.field.content_minhash_bits
    - The field for storing the content minhash bits.
    - content_minhash_bits
  * - index.field.cache
    - The field for storing the cache.
    - cache
  * - index.field.digest
    - The field for storing the digest.
    - digest
  * - index.field.site
    - The field for storing the site.
    - site
  * - index.field.content_length
    - The field for storing the content length.
    - content_length
  * - index.field.filetype
    - The field for storing the file type.
    - filetype
  * - index.field.filename
    - The field for storing the file name.
    - filename
  * - index.field.thumbnail
    - The field for storing the thumbnail.
    - thumbnail
  * - index.field.virtual_host
    - The field for storing the virtual host.
    - virtual_host
  * - response.field.content_title
    - The field for storing the content title.
    - content_title
  * - response.field.content_description
    - The field for storing the content description.
    - content_description
  * - response.field.url_link
    - The field for storing the URL link.
    - url_link
  * - response.field.site_path
    - The field for storing the site path.
    - site_path
  * - response.max.title.length
    - The maximum length for the title.
    - 50
  * - response.max.site.path.length
    - The maximum length for the site path.
    - 100
  * - response.highlight.content_title.enabled
    - Whether to enable highlighting for the content title.
    - true
  * - response.inline.mimetypes
    - The inline MIME types for the response.
    - application/pdf,text/plain

.. list-table:: Document Index Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - The index for document search.
    - fess.search
  * - index.document.update.index
    - The index for document update.
    - fess.update
  * - index.document.suggest.index
    - The index for document suggestions.
    - fess
  * - index.document.crawler.index
    - The index for document crawler.
    - fess_crawler
  * - index.document.crawler.queue.number_of_shards
    - The number of shards for the crawler queue.
    - 10
  * - index.document.crawler.data.number_of_shards
    - The number of shards for the crawler data.
    - 10
  * - index.document.crawler.filter.number_of_shards
    - The number of shards for the crawler filter.
    - 10
  * - index.document.crawler.queue.number_of_replicas
    - The number of replicas for the crawler queue.
    - 1
  * - index.document.crawler.data.number_of_replicas
    - The number of replicas for the crawler data.
    - 1
  * - index.document.crawler.filter.number_of_replicas
    - The number of replicas for the crawler filter.
    - 1
  * - index.config.index
    - The index configuration.
    - fess_config
  * - index.user.index
    - The user index.
    - fess_user
  * - index.log.index
    - The log index.
    - fess_log
  * - index.dictionary.prefix
    - The prefix for the dictionary index.
    - (empty)

.. list-table:: Document Management Configuration
  :header-rows: 1

  * - index.admin.array.fields
    - The array fields for the admin index.
    - lang,role,label,anchor,virtual_host
  * - index.admin.date.fields
    - The date fields for the admin index.
    - expires,created,timestamp,last_modified
  * - index.admin.integer.fields
    - The integer fields for the admin index.
    - (empty)
  * - index.admin.long.fields
    - The long fields for the admin index.
    - content_length,favorite_count,click_count
  * - index.admin.float.fields
    - The float fields for the admin index.
    - boost
  * - index.admin.double.fields
    - The double fields for the admin index.
    - (empty)
  * - index.admin.required.fields
    - The required fields for the admin index.
    - url,title,role,boost

.. list-table:: Timeout Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - The timeout for search in minutes.
    - 3m
  * - index.scroll.search.timeout
    - The timeout for search scroll in minutes.
    - 3m
  * - index.index.timeout
    - The timeout for indexing in minutes.
    - 3m
  * - index.bulk.timeout
    - The timeout for bulk indexing in minutes.
    - 3m
  * - index.delete.timeout
    - The timeout for deleting in minutes.
    - 3m
  * - index.health.timeout
    - The timeout for health check in minutes.
    - 10m
  * - index.indices.timeout
    - The timeout for indices in minutes.
    - 3m

.. list-table:: Filetype Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - The different files types and associated extensions to exclude.
    - | text/html=html\n\
      | application/msword=word\n\
      | application/vnd.openxmlformats-officedocument.wordprocessingml.document=word\n\
      | application/vnd.ms-excel=excel\n\
      | application/vnd.ms-excel.sheet.2=excel\n\
      | application/vnd.ms-excel.sheet.3=excel\n\
      | application/vnd.ms-excel.sheet.4=excel\n\
      | application/vnd.ms-excel.workspace.3=excel\n\
      | application/vnd.ms-excel.workspace.4=excel\n\
      | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet=excel\n\
      | application/vnd.ms-powerpoint=powerpoint\n\
      | application/vnd.openxmlformats-officedocument.presentationml.| presentation=powerpoint\n\
      | application/vnd.oasis.opendocument.text=odt\n\
      | application/vnd.oasis.opendocument.spreadsheet=ods\n\
      | application/vnd.oasis.opendocument.presentation=odp\n\
      | application/pdf=pdf\n\
      | application/x-fictionbook+xml=fb2\n\
      | application/e-pub+zip=epub\n\
      | application/x-ibooks+zip=ibooks\n\
      | text/plain=txt\n\
      | application/rtf=rtf\n\
      | application/vnd.ms-htmlhelp=chm\n\
      | application/zip=zip\n\
      | application/x-7z-comressed=7z\n\
      | application/x-bzip=bz\n\
      | application/x-bzip2=bz2\n\
      | application/x-tar=tar\n\
      | application/x-rar-compressed=rar\n\
      | video/3gp=3gp\n\
      | video/3g2=3g2\n\
      | video/x-msvideo=avi\n\
      | video/x-flv=flv\n\
      | video/mpeg=mpeg\n\
      | video/mp4=mp4\n\
      | video/ogv=ogv\n\
      | video/quicktime=qt\n\
      | video/x-m4v=m4v\n\
      | audio/x-aif=aif\n\
      | audio/midi=midi\n\
      | audio/mpga=mpga\n\
      | audio/mp4=mp4a\n\
      | audio/ogg=oga\n\
      | audio/x-wav=wav\n\
      | image/webp=webp\n\
      | image/bmp=bmp\n\
      | image/x-icon=ico\n\
      | image/x-icon=ico\n\
      | image/png=png\n\
      | image/svg+xml=svg\n\
      | image/tiff=tiff\n\
      | image/jpeg=jpg\n\

.. list-table:: Reindex Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.reindex.size
    - The size for re-indexing.
    - 100
  * - index.reindex.body
    - The body for re-indexing. In in bulk format.
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - The requests per second for re-indexing.
    - adaptive
  * - index.reindex.refresh
    - The refresh for re-indexing.
    - false
  * - index.reindex.timeout
    - The timeout for re-indexing.
    - 1m
  * - index.reindex.scroll
    - The scroll for re-indexing.
    - 5m
  * - index.reindex.max_docs
    - The maximum documents for re-indexing.
    - (empty)

.. list-table:: Query Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - The maximum length of a query string.
    - 1000
  * - query.timeout
    - The timeout for a query.
    - 10000
  * - query.timeout.logging
    - Enable or disable query timeout logging.
    - true
  * - query.track.total.hits
    - The total number of hits to track.
    - 10000
  * - query.geo.fields
    - The fields used for geo queries.
    - location
  * - query.browser.lang.parameter.name
    - The name of the browser language parameter.
    - browser_lang
  * - query.replace.term.with.prefix.query
    - Replace term with prefix query.
    - true
  * - query.orsearch.min.hit.count
    - The minimum hit count for OR search.
    - 0
  * - query.highlight.terminal.chars
    - Characters used for highlighting terminals.
    - u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61
  * - query.highlight.fragment.size
    - The size of the highlight fragment.
    - 60
  * - query.highlight.number.of.fragments
    - The number of fragments for highlighting.
    - 2
  * - query.highlight.type
    - The type of highlighter.
    - fvh
  * - query.highlight.tag.pre
    - The opening tag for highlighted text.
    - <strong>
  * - query.highlight.tag.post
    - The closing tag for highlighted text.
    - </strong>
  * - query.highlight.boundary.chars
    - Characters used for boundary scanning.
    - u0009u000Au0013u0020
  * - query.highlight.boundary.max.scan
    - The maximum number of characters to scan for boundary.
    - 20
  * - query.highlight.boundary.scanner
    - The type of boundary scanner.
    - chars
  * - query.highlight.encoder
    - The encoder for highlighted text.
    - default
  * - query.highlight.force.source
    - Force source retrieval for highlighting.
    - false
  * - query.highlight.fragmenter
    - The type of fragmenter.
    - span
  * - query.highlight.fragment.offset
    - The offset for fragments.
    - -1
  * - query.highlight.no.match.size
    - The size of the fragment when no match is found.
    - 0
  * - query.highlight.order
    - The order of highlighted fragments.
    - score
  * - query.highlight.phrase.limit
    - The limit for phrase highlighting.
    - 256
  * - query.highlight.content.description.fields
    - Fields used for content description in highlighting.
    - hl_content,digest
  * - query.highlight.boundary.position.detect
    - Detect boundary position.
    - true
  * - query.highlight.text.fragment.type
    - The type of text fragment.
    - query
  * - query.highlight.text.fragment.size
    - The size of the text fragment.
    - 3
  * - query.highlight.text.fragment.prefix.length
    - The prefix length for text fragments.
    - 5
  * - query.highlight.text.fragment.suffix.length
    - The suffix length for text fragments.
    - 5
  * - query.additional.default.fields
    - Additional default fields for queries.
    - (empty)
  * - query.additional.response.fields
    - Additional response fields for queries.
    - (empty)
  * - query.additional.api.response.fields
    - Additional API response fields for queries.
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
    - Additional not analyzed fields for queries.
    - (empty)
  * - query.gsa.response.fields
    - Fields for GSA response.
    - UE,U,T,RK,S,LANG
  * - query.gsa.default.lang
    - Default language for GSA.
    - en
  * - query.gsa.default.sort
    - Default sort for GSA.
    - (empty)
  * - query.gsa.meta.prefix
    - Meta prefix for GSA.
    - ``MT_``
  * - query.gsa.index.field.charset
    - Charset for GSA index field.
    - charset
  * - query.gsa.index.field.content_type
    - Content type for GSA index field.
    - content_type
  * - query.collapse.max.concurrent.group.results
    - Maximum concurrent group results for collapse.
    - 4
  * - query.collapse.inner.hits.name
    - Name for inner hits in collapse.
    - similar_docs
  * - query.collapse.inner.hits.size
    - Size for inner hits in collapse.
    - 0
  * - query.collapse.inner.hits.sorts
    - Sorts for inner hits in collapse.
    - (empty)
  * - query.default.languages
    - Default languages for queries.
    - (empty)
  * - query.json.default.preference
    - Default preference for JSON queries.
    - _query
  * - query.gsa.default.preference
    - Default preference for GSA queries.
    - _query
  * - query.language.mapping
    - Mapping for languages.
    - | ar=ar\n\
      | bg=bg\n\
      | bn=bn\n\
      | ca=ca\n\
      | ckb-iq=ckb-iq\n\
      | ckb_IQ=ckb-iq\n\
      | cs=cs\n\
      | da=da\n\
      | de=de\n\
      | el=el\n\
      | en=en\n\
      | en-ie=en-ie\n\
      | en_IE=en-ie\n\
      | es=es\n\
      | et=et\n\
      | eu=eu\n\
      | fa=fa\n\
      | fi=fi\n\
      | fr=fr\n\
      | gl=gl\n\
      | gu=gu\n\
      | he=he\n\
      | hi=hi\n\
      | hr=hr\n\
      | hu=hu\n\
      | hy=hy\n\
      | id=id\n\
      | it=it\n\
      | ja=ja\n\
      | ko=ko\n\
      | lt=lt\n\
      | lv=lv\n\
      | mk=mk\n\
      | ml=ml\n\
      | nl=nl\n\
      | no=no\n\
      | pa=pa\n\
      | pl=pl\n\
      | pt=pt\n\
      | pt-br=pt-br\n\
      | pt_BR=pt-br\n\
      | ro=ro\n\
      | ru=ru\n\
      | si=si\n\
      | sq=sq\n\
      | sv=sv\n\
      | ta=ta\n\
      | te=te\n\
      | th=th\n\
      | tl=tl\n\
      | tr=tr\n\
      | uk=uk\n\
      | ur=ur\n\
      | vi=vi\n\
      | zh-cn=zh-cn\n\
      | zh_CN=zh-cn\n\
      | zh-tw=zh-tw\n\
      | zh_TW=zh-tw\n\
      | zh=zh\n\

.. list-table:: Boost Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - Boost for title
    - 0.5
  * - query.boost.title.lang
    - Boost for title language
    - 1.0
  * - query.boost.content
    - Boost for content
    - 0.05
  * - query.boost.content.lang
    - Boost for content language
    - 0.1
  * - query.boost.important_content
    - Boost for important content
    - -1.0
  * - query.boost.important_content.lang
    - Boost for important content language
    - -1.0
  * - query.boost.fuzzy.min.length
    - Minimum length for fuzzy matching
    - 4
  * - query.boost.fuzzy.title
    - Fuzzy boost for title
    - 0.01
  * - query.boost.fuzzy.title.fuzziness
    - Fuzziness for title
    - AUTO
  * - query.boost.fuzzy.title.expansions
    - Expansions for fuzzy title
    - 10
  * - query.boost.fuzzy.title.prefix_length
    - Prefix length for fuzzy title
    - 0
  * - query.boost.fuzzy.title.transpositions
    - Allow transpositions for fuzzy title
    - true
  * - query.boost.fuzzy.content
    - Fuzzy boost for content
    - 0.005
  * - query.boost.fuzzy.content.fuzziness
    - Fuzziness for content
    - AUTO
  * - query.boost.fuzzy.content.expansions
    - Expansions for fuzzy content
    - 10
  * - query.boost.fuzzy.content.prefix_length
    - Prefix length for fuzzy content
    - 0
  * - query.boost.fuzzy.content.transpositions
    - Allow transpositions for fuzzy content
    - true
  * - query.default.query_type
    - Default query type
    - bool
  * - query.dismax.tie_breaker
    - Tie breaker for dismax queries
    - 0.1
  * - query.bool.minimum_should_match
    - Minimum should match for boolean queries
    - (empty)
  * - query.prefix.expansions
    - Expansions for prefix queries
    - 50
  * - query.prefix.slop
    - Slop for prefix queries
    - 0
  * - query.fuzzy.prefix_length
    - Prefix length for fuzzy queries
    - 0
  * - query.fuzzy.expansions
    - Expansions for fuzzy queries
    - 50
  * - query.fuzzy.transpositions
    - Allow transpositions for fuzzy queries
    - true

.. list-table:: Facet Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - The fields to be used for faceting.
    - label
  * - query.facet.fields.size
    - The maximum number of facet entries to be returned.
    - 100
  * - query.facet.fields.min_doc_count
    - The minimum document count for a facet entry to be included.
    - 1
  * - query.facet.fields.sort
    - The sort order of the facet entries.
    - count.desc
  * - query.facet.fields.missing
    - The value to be used for missing fields.
    - (empty)
  * - query.facet.queries
    - The custom facet queries.
    - | labels.facet_timestamp_title:\
      | labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]\t\
      | labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]\t\
      | labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]\t\
      | labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]\n\
      | labels.facet_contentLength_title:\
      | labels.facet_contentLength_10k=content_length:[0 TO 9999]\t\
      | labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]\t\
      | labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]\t\
      | labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]\t\
      | labels.facet_contentLength_1m=content_length:[1000000 TO *]\n\
      | labels.facet_filetype_title:\
      | labels.facet_filetype_html=filetype:html\t\
      | labels.facet_filetype_word=filetype:word\t\
      | labels.facet_filetype_excel=filetype:excel\t\
      | labels.facet_filetype_powerpoint=filetype:powerpoint\t\
      | labels.facet_filetype_odt=filetype:odt\t\
      | labels.facet_filetype_ods=filetype:ods\t\
      | labels.facet_filetype_odp=filetype:odp\t\
      | labels.facet_filetype_pdf=filetype:pdf\t\
      | labels.facet_filetype_txt=filetype:txt\t\
      | labels.facet_filetype_others=filetype:others\n\

.. list-table:: Ranking Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Window size for rank fusion.
    - 200
  * - rank.fusion.rank_constant
    - Rank constant for fusion.
    - 20
  * - rank.fusion.threads
    - Number of threads for rank fusion.
    - -1
  * - rank.fusion.score_field
    - Field used for rank fusion score.
    - rf_score

.. list-table:: ACL Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - Enable role mapping from file for SMB.
    - true
  * - smb.available.sid.types
    - Available SID types for SMB.
    - 1,2,4:2,5:1
  * - file.role.from.file
    - Enable role mapping from file for file system.
    - true
  * - ftp.role.from.file
    - Enable role mapping from file for FTP.
    - true

.. list-table:: Backup Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - Targets for index backup
    - fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json
  * - index.backup.log.targets
    - Targets for log backup
    - click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson
  * - index.backup.log.load.timeout
    - Timeout for loading log backup
    - 60000

.. list-table:: Logging Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.search.docs.enabled
    - Enable logging of search documents.
    - true
  * - logging.search.docs.fields
    - Fields to log for search documents.
    - filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp
  * - logging.search.use.logfile
    - Use logfile for logging.
    - true
  * - logging.app.packages
    - Application packages to log.
    - org.codelibs,org.dbflute,org.lastaflute

Web
---

.. list-table:: Web Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - Maximum input size for admin forms
    - 10000
  * - form.admin.label.in.config.enabled
    - Enable labels in admin config
    - false
  * - form.admin.default.template.name
    - Default template name for admin forms
    - __TEMPLATE__
  * - osdd.link.enabled
    - Enable OSDD link
    - auto
  * - clipboard.copy.icon.enabled
    - Enable clipboard copy icon
    - true

Permission
----------

.. list-table:: Permission Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - authentication.admin.users
    - Admin users for authentication
    - admin
  * - authentication.admin.roles
    - Admin roles for authentication
    - admin
  * - role.search.default.permissions
    - Default search permissions
    - (empty)
  * - role.search.default.display.permissions
    - Default display permissions for search
    - {role}guest
  * - role.search.guest.permissions
    - Guest permissions for search
    - {role}guest
  * - role.search.user.prefix
    - Prefix for user roles in search
    - 1
  * - role.search.group.prefix
    - Prefix for group roles in search
    - 2
  * - role.search.role.prefix
    - Prefix for roles in search
    - R
  * - role.search.denied.prefix
    - Prefix for denied roles in search
    - D

Cookie
------

.. list-table:: Cookie Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - cookie.default.path
    - The default path of cookie (basically '/' if no context path)
    - ``/``
  * - cookie.default.expires
    -  The default expire of cookie in seconds e.g. 31556926: one year, 86400: one day
    - 3600
  * - session.tracking.modes
    - The tracking modes for session
    - cookie

Paging
------

.. list-table:: Paging Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.page.size
    - The size of one page for paging
    - 25
  * - paging.page.range.fill.limit
    - The option ``fillLimit`` of page range for paging
    - true

.. list-table:: Fetch Page Size Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - Maximum fetch size for document boost
    - 1000
  * - page.keymatch.max.fetch.size
    - Maximum fetch size for key match
    - 1000
  * - page.labeltype.max.fetch.size
    - Maximum fetch size for label type
    - 1000
  * - page.roletype.max.fetch.size
    - Maximum fetch size for role type
    - 1000
  * - page.user.max.fetch.size
    - Maximum fetch size for user
    - 1000
  * - page.role.max.fetch.size
    - Maximum fetch size for role
    - 1000
  * - page.group.max.fetch.size
    - Maximum fetch size for group
    - 1000
  * - page.crawling.info.param.max.fetch.size
    - Maximum fetch size for crawling info parameters
    - 100
  * - page.crawling.info.max.fetch.size
    - Maximum fetch size for crawling info
    - 1000
  * - page.data.config.max.fetch.size
    - Maximum fetch size for data configuration
    - 100
  * - page.web.config.max.fetch.size
    - Maximum fetch size for web configuration
    - 100
  * - page.file.config.max.fetch.size
    - Maximum fetch size for file configuration
    - 100
  * - page.duplicate.host.max.fetch.size
    - Maximum fetch size for duplicate host
    - 1000
  * - page.failure.url.max.fetch.size
    - Maximum fetch size for failure URL
    - 1000
  * - page.favorite.log.max.fetch.size
    - Maximum fetch size for favorite log
    - 100
  * - page.file.auth.max.fetch.size
    - Maximum fetch size for file authentication
    - 100
  * - page.web.auth.max.fetch.size
    - Maximum fetch size for web authentication
    - 100
  * - page.path.mapping.max.fetch.size
    - Maximum fetch size for path mapping
    - 1000
  * - page.request.header.max.fetch.size
    - Maximum fetch size for request header
    - 1000
  * - page.scheduled.job.max.fetch.size
    - Maximum fetch size for scheduled job
    - 100
  * - page.elevate.word.max.fetch.size
    - Maximum fetch size for elevate word
    - 1000
  * - page.bad.word.max.fetch.size
    - Maximum fetch size for bad word
    - 1000
  * - page.dictionary.max.fetch.size
    - Maximum fetch size for dictionary
    - 1000
  * - page.relatedcontent.max.fetch.size
    - Maximum fetch size for related content
    - 5000
  * - page.relatedquery.max.fetch.size
    - Maximum fetch size for related query
    - 5000
  * - page.thumbnail.queue.max.fetch.size
    - Maximum fetch size for thumbnail queue
    - 100
  * - page.thumbnail.purge.max.fetch.size
    - Maximum fetch size for thumbnail purge
    - 100
  * - page.score.booster.max.fetch.size
    - Maximum fetch size for score booster
    - 1000
  * - page.searchlog.max.fetch.size
    - Maximum fetch size for search log
    - 10000
  * - page.searchlist.track.total.hits
    - Track total hits in search list
    - true

.. list-table:: Search Page Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default Value
  * - paging.search.page.start
    - Starting page number for search results
    - 0
  * - paging.search.page.size
    - Number of search results per page
    - 10
  * - paging.search.page.max.size
    - Maximum number of search results per page
    - 100
  * - searchlog.agg.shard.size
    - Aggregation shard size for search logs
    - -1
  * - searchlog.request.headers
    - Headers to include in search log requests
    - (empty)
  * - searchlog.process.batch_size
    - Batch size for processing search logs
    - 100
  * - thumbnail.html.image.min.width
    - Minimum width for HTML image thumbnails
    - 100
  * - thumbnail.html.image.min.height
    - Minimum height for HTML image thumbnails
    - 100
  * - thumbnail.html.image.max.aspect.ratio
    - Maximum aspect ratio for HTML image thumbnails
    - 3.0
  * - thumbnail.html.image.thumbnail.width
    - Width of the HTML image thumbnail
    - 100
  * - thumbnail.html.image.thumbnail.height
    - Height of the HTML image thumbnail
    - 100
  * - thumbnail.html.image.format
    - Format of the HTML image thumbnail
    - png
  * - thumbnail.html.image.xpath
    - XPath to select images for thumbnails
    - //IMG
  * - thumbnail.html.image.exclude.extensions
    - File extensions to exclude from thumbnails
    - svg,html,css,js
  * - thumbnail.generator.interval
    - Interval for generating thumbnails
    - 0
  * - thumbnail.generator.targets
    - Targets for thumbnail generation
    - all
  * - thumbnail.crawler.enabled
    - Enable or disable the thumbnail crawler
    - true
  * - thumbnail.system.monitor.interval
    - Interval for system monitoring
    - 60

.. list-table:: User Page Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - Request parameter for user code
    - userCode
  * - user.code.min.length
    - Minimum length for user code
    - 20
  * - user.code.max.length
    - Maximum length for user code
    - 100
  * - user.code.pattern
    - Pattern for user code
    - [a-zA-Z0-9_]+

Mail
----

.. list-table:: Mail Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - mail.from.name
    - The name displayed in the "From" field of outgoing emails.
    - Administrator
  * - mail.from.address
    - The email address displayed in the "From" field of outgoing emails.
    - root@localhost
  * - mail.hostname
    - The hostname of the mail server.
    - (empty)

Scheduler
---------

.. list-table:: Scheduler Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - scheduler.target.name
    - (Description for scheduler.target.name)
    - (empty)
  * - scheduler.job.class
    - Class name for the job to be executed
    - org.codelibs.fess.app.job.ScriptExecutorJob
  * - scheduler.concurrent.exec.mode
    - Mode for concurrent execution
    - QUIT
  * - scheduler.monitor.interval
    - Interval for monitoring in seconds
    - 30


Online Help
-----------

.. list-table:: Online Help Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - online.help.base.link
    - Base link for online help
    - https://fess.codelibs.org/{lang}/{version}/admin/
  * - online.help.installation
    - Installation help link
    - https://fess.codelibs.org/{lang}/{version}/install/install.html
  * - online.help.eol
    - End of life help link
    - https://fess.codelibs.org/{lang}/eol.html
  * - online.help.name.failureurl
    - Failure URL help name
    - failureurl
  * - online.help.name.elevateword
    - Elevate word help name
    - elevateword
  * - online.help.name.reqheader
    - Request header help name
    - reqheader
  * - online.help.name.dict.synonym
    - Synonym dictionary help name
    - synonym
  * - online.help.name.dict
    - Dictionary help name
    - dict
  * - online.help.name.dict.kuromoji
    - Kuromoji dictionary help name
    - kuromoji
  * - online.help.name.dict.protwords
    - Protected words dictionary help name
    - protwords
  * - online.help.name.dict.stopwords
    - Stopwords dictionary help name
    - stopwords
  * - online.help.name.dict.stemmeroverride
    - Stemmer override dictionary help name
    - stemmeroverride
  * - online.help.name.dict.mapping
    - Mapping dictionary help name
    - mapping
  * - online.help.name.webconfig
    - Web configuration help name
    - webconfig
  * - online.help.name.searchlist
    - Search list help name
    - searchlist
  * - online.help.name.log
    - Log help name
    - log
  * - online.help.name.general
    - General help name
    - general
  * - online.help.name.role
    - Role help name
    - role
  * - online.help.name.joblog
    - Job log help name
    - joblog
  * - online.help.name.keymatch
    - Key match help name
    - keymatch
  * - online.help.name.relatedquery
    - Related query help name
    - relatedquery
  * - online.help.name.relatedcontent
    - Related content help name
    - relatedcontent
  * - online.help.name.wizard
    - Wizard help name
    - wizard
  * - online.help.name.badword
    - Bad word help name
    - badword
  * - online.help.name.pathmap
    - Path map help name
    - pathmap
  * - online.help.name.boostdoc
    - Boost document help name
    - boostdoc
  * - online.help.name.dataconfig
    - Data configuration help name
    - dataconfig
  * - online.help.name.systeminfo
    - System information help name
    - systeminfo
  * - online.help.name.user
    - User help name
    - user
  * - online.help.name.group
    - Group help name
    - group
  * - online.help.name.design
    - Design help name
    - design
  * - online.help.name.dashboard
    - Dashboard help name
    - dashboard
  * - online.help.name.webauth
    - Web authentication help name
    - webauth
  * - online.help.name.fileconfig
    - File configuration help name
    - fileconfig
  * - online.help.name.fileauth
    - File authentication help name
    - fileauth
  * - online.help.name.labeltype
    - Label type help name
    - labeltype
  * - online.help.name.duplicatehost
    - Duplicate host help name
    - duplicatehost
  * - online.help.name.scheduler
    - Scheduler help name
    - scheduler
  * - online.help.name.crawlinginfo
    - Crawling information help name
    - crawlinginfo
  * - online.help.name.backup
    - Backup help name
    - backup
  * - online.help.name.upgrade
    - Upgrade help name
    - upgrade
  * - online.help.name.esreq
    - OpenSearch request help name
    - esreq
  * - online.help.name.accesstoken
    - Access token help name
    - accesstoken
  * - online.help.name.suggest
    - Suggest help name
    - suggest
  * - online.help.name.searchlog
    - Search log help name
    - searchlog
  * - online.help.name.maintenance
    - Maintenance help name
    - maintenance
  * - online.help.name.plugin
    - Plugin help name
    - plugin
  * - online.help.name.storage
    - Storage help name
    - storage
  * - online.help.supported.langs
    - Supported languages
    - ja

Forum
-----

.. list-table:: Forum Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - forum.link
    - Base link for forum
    - https://discuss.codelibs.org/c/Fess{lang}/
  * - forum.supported.langs
    - Supported languages
    - en,ja

Suggest
-------

.. list-table:: Suggest Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - suggest.popular.word.seed
    - Seed value for popular word suggestions
    - 0
  * - suggest.popular.word.tags
    - Tags for popular word suggestions
    - (empty)
  * - suggest.popular.word.fields
    - Fields for popular word suggestions
    - (empty)
  * - suggest.popular.word.excludes
    - Excluded words for popular word suggestions
    - (empty)
  * - suggest.popular.word.size
    - Size of popular word suggestions
    - 10
  * - suggest.popular.word.window.size
    - Window size for popular word suggestions
    - 30
  * - suggest.popular.word.query.freq
    - Query frequency for popular word suggestions
    - 10
  * - suggest.min.hit.count
    - Minimum hit count for suggestions
    - 1
  * - suggest.field.contents
    - Contents field for suggestions
    - _default
  * - suggest.field.tags
    - Tags field for suggestions
    - label
  * - suggest.field.roles
    - Roles field for suggestions
    - role
  * - suggest.field.index.contents
    - Index contents field for suggestions
    - content,title
  * - suggest.update.request.interval
    - Interval for update requests
    - 0
  * - suggest.update.doc.per.request
    - Number of documents per update request
    - 2
  * - suggest.update.contents.limit.num
    - Limit number for update contents
    - 10000
  * - suggest.update.contents.limit.doc.size
    - Limit document size for update contents
    - 50000
  * - suggest.source.reader.scroll.size
    - Scroll size for source reader
    - 1
  * - suggest.popular.word.cache.size
    - Cache size for popular word suggestions
    - 1000
  * - suggest.popular.word.cache.expire
    - Cache expiration time for popular word suggestions
    - 60
  * - suggest.search.log.permissions
    - Permissions for search log
    - {user}guest,{role}guest
  * - suggest.system.monitor.interval
    - Interval for system monitoring
    - 60

LDAP
----

.. list-table:: LDAP Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - ldap.admin.enabled
    - Enable or disable LDAP admin
    - false
  * - ldap.admin.user.filter
    - Filter for LDAP admin user
    - uid=%s
  * - ldap.admin.user.base.dn
    - Base DN for LDAP admin user
    - ou=People,dc=fess,dc=codelibs,dc=org
  * - ldap.admin.user.object.classes
    - Object classes for LDAP admin user
    - organizationalPerson,top,person,inetOrgPerson
  * - ldap.admin.role.filter
    - Filter for LDAP admin role
    - cn=%s
  * - ldap.admin.role.base.dn
    - Base DN for LDAP admin role
    - ou=Role,dc=fess,dc=codelibs,dc=org
  * - ldap.admin.role.object.classes
    - Object classes for LDAP admin role
    - groupOfNames
  * - ldap.admin.group.filter
    - Filter for LDAP admin group
    - cn=%s
  * - ldap.admin.group.base.dn
    - Base DN for LDAP admin group
    - ou=Group,dc=fess,dc=codelibs,dc=org
  * - ldap.admin.group.object.classes
    - Object classes for LDAP admin group
    - groupOfNames
  * - ldap.admin.sync.password
    - Sync password for LDAP admin
    - true
  * - ldap.auth.validation
    - Enable or disable LDAP auth validation
    - true
  * - ldap.max.username.length
    - Maximum username length for LDAP
    - -1
  * - ldap.ignore.netbios.name
    - Ignore NetBIOS name for LDAP
    - true
  * - ldap.group.name.with.underscores
    - Use underscores in group names for LDAP
    - false
  * - ldap.lowercase.permission.name
    - Use lowercase for permission names in LDAP
    - false
  * - ldap.allow.empty.permission
    - Allow empty permissions in LDAP
    - true
  * - ldap.role.search.user.enabled
    - Enable role search for user in LDAP
    - true
  * - ldap.role.search.group.enabled
    - Enable role search for group in LDAP
    - true
  * - ldap.role.search.role.enabled
    - Enable role search for role in LDAP
    - true
  * - ldap.attr.surname
    - LDAP attribute for surname
    - sn
  * - ldap.attr.givenName
    - LDAP attribute for given name
    - givenName
  * - ldap.attr.employeeNumber
    - LDAP attribute for employee number
    - employeeNumber
  * - ldap.attr.mail
    - LDAP attribute for mail
    - mail
  * - ldap.attr.telephoneNumber
    - LDAP attribute for telephone number
    - telephoneNumber
  * - ldap.attr.homePhone
    - LDAP attribute for home phone
    - homePhone
  * - ldap.attr.homePostalAddress
    - LDAP attribute for home postal address
    - homePostalAddress
  * - ldap.attr.labeledURI
    - LDAP attribute for labeled URI
    - labeledURI
  * - ldap.attr.roomNumber
    - LDAP attribute for room number
    - roomNumber
  * - ldap.attr.description
    - LDAP attribute for description
    - description
  * - ldap.attr.title
    - LDAP attribute for title
    - title
  * - ldap.attr.pager
    - LDAP attribute for pager
    - pager
  * - ldap.attr.street
    - LDAP attribute for street
    - street
  * - ldap.attr.postalCode
    - LDAP attribute for postal code
    - postalCode
  * - ldap.attr.physicalDeliveryOfficeName
    - LDAP attribute for physical delivery office name
    - physicalDeliveryOfficeName
  * - ldap.attr.destinationIndicator
    - LDAP attribute for destination indicator
    - destinationIndicator
  * - ldap.attr.internationaliSDNNumber
    - LDAP attribute for international ISDN number
    - internationaliSDNNumber
  * - ldap.attr.state
    - LDAP attribute for state
    - st
  * - ldap.attr.employeeType
    - LDAP attribute for employee type
    - employeeType
  * - ldap.attr.facsimileTelephoneNumber
    - LDAP attribute for facsimile telephone number
    - facsimileTelephoneNumber
  * - ldap.attr.postOfficeBox
    - LDAP attribute for post office box
    - postOfficeBox
  * - ldap.attr.initials
    - LDAP attribute for initials
    - initials
  * - ldap.attr.carLicense
    - LDAP attribute for car license
    - carLicense
  * - ldap.attr.mobile
    - LDAP attribute for mobile
    - mobile
  * - ldap.attr.postalAddress
    - LDAP attribute for postal address
    - postalAddress
  * - ldap.attr.city
    - LDAP attribute for city
    - l
  * - ldap.attr.teletexTerminalIdentifier
    - LDAP attribute for teletex terminal identifier
    - teletexTerminalIdentifier
  * - ldap.attr.x121Address
    - LDAP attribute for X.121 address
    - x121Address
  * - ldap.attr.businessCategory
    - LDAP attribute for business category
    - businessCategory
  * - ldap.attr.registeredAddress
    - LDAP attribute for registered address
    - registeredAddress
  * - ldap.attr.displayName
    - LDAP attribute for display name
    - displayName
  * - ldap.attr.preferredLanguage
    - LDAP attribute for preferred language
    - preferredLanguage
  * - ldap.attr.departmentNumber
    - LDAP attribute for department number
    - departmentNumber
  * - ldap.attr.uidNumber
    - LDAP attribute for UID number
    - uidNumber
  * - ldap.attr.gidNumber
    - LDAP attribute for GID number
    - gidNumber
  * - ldap.attr.homeDirectory
    - LDAP attribute for home directory
    - homeDirectory

Maven Repository
----------------

.. list-table:: Maven Repository Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - plugin.repositories
    - URLs for plugin repositories
    - https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml
  * - plugin.version.filter
    - Filter for plugin versions
    - (empty)

Storage
-------

.. list-table:: Storage Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - storage.max.items.in.page
    - Maximum items in a page
    - 1000

Password
--------

.. list-table:: Password Configuration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - password.invalid.admin.passwords
    - Invalid passwords a user can use as their password
    - | admin
