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

核心
----

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - 用于日志记录和显示的域标题。
    - ``Fess``

.. list-table:: 搜索引擎
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - 搜索引擎后端的类型（例如 default、opensearch）。
    - ``default``
  * - search_engine.http.url
    - 搜索引擎 HTTP 端点的 URL。在 IPv6 环境中，请用方括号括住 IPv6 地址（例如 http://[::1]:9200）
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - 用于安全 HTTP 连接的 SSL 证书颁发机构的路径。
    - (empty)
  * - search_engine.username
    - 用于向搜索引擎进行认证的用户名。
    - (empty)
  * - search_engine.password
    - 用于向搜索引擎进行认证的密码。
    - (empty)
  * - search_engine.heartbeat_interval
    - 对搜索引擎进行心跳检查的间隔（毫秒）。
    - ``10000``
  * - app.cipher.algorithm
    - 用于加密的密码算法。
    - ``aes``
  * - app.cipher.key
    - 加密用的密钥（生产环境请更改此值）。
    - ``___change__me___``
  * - app.digest.algorithm
    - 用于计算摘要的算法。
    - ``sha256``
  * - app.password.algorithm
    - 密码哈希（新机制，兼容 Spring Security v5.8）。支持：bcrypt（目前仅此一种）
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - BCrypt 的 cost（对数轮数）。10 与 Spring Security v5.8 的默认值一致。范围：4-31。
    - ``10``
  * - app.password.upgrade.enabled
    - 登录成功时对旧版哈希进行延迟重新哈希。
    - ``true``
  * - app.encrypt.property.pattern
    - 注意：app.digest.algorithm 仅为 旧版密码校验而保留（针对没有 {id} 前缀的升级前哈希）。请勿用于新密码。要加密的属性的正则表达式。
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - 调试日志中要遮蔽的敏感值的正则表达式（对属性/环境变量键进行不区分大小写的匹配）。
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - 用于应用程序定制的扩展名称。
    - (empty)
  * - app.audit.log.format
    - 审计日志格式。
    - (empty)
  * - script.audit.log.enabled
    - 脚本审计日志设置。
    - ``true``
  * - script.audit.log.max.length
    - 脚本审计日志条目中保留的脚本文本的最大字符数；更长的文本会被截断。
    - ``100``
  * - jvm.crawler.options
    - 爬虫进程的 JVM 选项。
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
    - 传递给建议创建器子进程的 JVM 选项（以换行分隔）。
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
    - 分块向量索引器进程的 JVM 选项。堆内存预算。该子 JVM 仅在 "Content Chunk Vector Indexer" 作业运行期间启动，因此在内容分块关闭时，设置较大的 -Xmx 不会产生任何开销。存活对象集主要由处理中的批次构成，每个批次对每个文档都会保留完整的 _source、该文档的分块字符串以及该文档的嵌入向量：content_chunker.job.bulk_size（默认 20）x content_chunker.max_chunks_per_document（默认 1000）x content_chunker.embedding.dimension（默认 768）x 每个 float 4 字节 x content_chunker.job.concurrency（默认 2）= 仅向量就约 117 MB，尚未计入分块字符串和文档源。在默认配置下，最坏情况下存活内存约为 190-250 MB（在 dimension=1536 时仅向量就约 235 MB），这无法装入 256 MB 的堆，且没有任何 GC 余量。如果提高 bulk_size、max_chunks_per_document、concurrency 或嵌入维度，请进一步提高 -Xmx。
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
    - 缩略图进程的 JVM 选项。
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

.. list-table:: 作业
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - 计划任务的系统作业 ID。
    - ``default_crawler``
  * - job.template.title.web
    - Web 爬虫作业标题的模板。
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - 文件爬虫作业标题的模板。
    - ``File Crawler - {0}``
  * - job.template.title.data
    - 数据存储爬虫作业标题的模板。
    - ``Data Crawler - {0}``
  * - job.template.script
    - 作业执行的脚本模板。
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - 爬虫进程的最大数量。
    - ``0``
  * - job.default.script
    - 作业的默认脚本语言。
    - ``javascript``
  * - job.system.property.filter.pattern
    - 用于过滤作业的系统属性的模式。
    - (empty)
  * - processors
    - 要使用的处理器数量。
    - ``0``
  * - java.command.path
    - Java 命令的路径。
    - ``java``
  * - python.command.path
    - Python 命令的路径。
    - ``python``
  * - path.encoding
    - 文件路径的编码。
    - ``UTF-8``
  * - use.own.tmp.dir
    - 是否使用专用临时目录。
    - ``true``
  * - max.log.output.length
    - 日志输出的最大长度。
    - ``4000``
  * - adaptive.load.control
    - 自适应负载控制值。
    - ``50``
  * - web.load.control
    - Web 请求负载控制的 CPU 阈值（%）。当 CPU >= 此值时返回 429。（100：禁用）
    - ``100``
  * - api.load.control
    - API 请求负载控制的 CPU 阈值（%）。当 CPU >= 此值时返回 429。（100：禁用）
    - ``100``
  * - load.control.monitor.interval
    - 监控 OpenSearch CPU 负载的间隔（秒）。
    - ``1``
  * - supported.languages
    - 支持的语言。
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - API 访问令牌的长度。
    - ``60``
  * - api.access.token.request.parameter
    - API 访问令牌的请求参数。
    - (empty)
  * - api.admin.access.permissions
    - API 管理访问的权限。
    - ``Radmin-api``
  * - api.search.accept.referers
    - API 搜索接受的 Referer。
    - (empty)
  * - api.search.scroll
    - 是否为 API 搜索启用滚动。
    - ``false``
  * - api.search.export
    - 是否在 /api/v2/documents/export 启用最终用户的搜索结果导出（CSV/JSON）。
    - ``false``
  * - api.search.export.max.size
    - 一次搜索结果导出写入的最大文档数。
    - ``1000``
  * - api.search.export.fields
    - 搜索结果导出写入的字段（逗号分隔）。不是 API 响应字段的字段会被忽略。
    - ``title,url_link,last_modified,content_length,filetype``
  * - api.search.export.rate.limit.per.minute
    - 每个用户每分钟的搜索结果导出最大次数（访客按每个客户端 IP 计算）。0 或更小的值表示禁用该限制。
    - ``10``
  * - api.json.response.headers
    - API JSON 响应的头信息。Access-Control-\* 和 Timing-Allow-Origin 在此处会被忽略（CORS 由 api.cors.\* / CorsFilter 控制）。请勿设置 Vary。
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - API JSON 响应中是否包含异常。
    - ``false``
  * - api.gsa.response.headers
    - API GSA 响应的头信息。Access-Control-\* 和 Timing-Allow-Origin 在此处会被忽略（CORS 由 api.cors.\* / CorsFilter 控制）。请勿设置 Vary。
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - API GSA 响应中是否包含异常。
    - ``false``
  * - api.dashboard.response.headers
    - API 仪表板响应的头信息。Access-Control-\* 和 Timing-Allow-Origin 在此处会被忽略（CORS 由 api.cors.\* / CorsFilter 控制）。请勿设置 Vary。
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - CORS 允许的来源。"\*" 会返回字面量 "\*"（请求的 Origin 不会被回显），并禁用凭据。设置明确的来源（以换行或逗号分隔）可允许带凭据的跨域访问。
    - ``*``
  * - api.cors.allow.methods
    - CORS 允许的 HTTP 方法。
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - CORS 预检请求的最大有效期。
    - ``3600``
  * - api.cors.allow.headers
    - CORS 预检允许的请求头。返回的是静态列表（不会回显 Access-Control-Request-Headers）。包含 X-Fess-CSRF-Token，供发送 CSRF 令牌的跨域 SPA 使用。
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - 是否允许 CORS 使用凭据。仅对明确指定的 Origin 的完全匹配生效；当 api.cors.allow.origin 为 "\*" 时会被忽略。
    - ``true``
  * - api.jsonp.enabled
    - 是否为 API 启用 JSONP。
    - ``false``
  * - api.ping.search_engine.fields
    - API 对搜索引擎执行 ping 时使用的字段。
    - ``status,timed_out``

速率限制
--------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - 是否启用速率限制。
    - ``false``
  * - rate.limit.requests.per.window
    - 每个窗口允许的最大请求数。
    - ``100``
  * - rate.limit.window.ms
    - 窗口大小（毫秒）。
    - ``60000``
  * - rate.limit.block.duration.ms
    - 超过限制时阻止 IP 的持续时间（毫秒）。
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Retry-After 头的值（秒）。
    - ``60``
  * - rate.limit.whitelist.ips
    - 白名单 IP 的逗号分隔列表（例如 127.0.0.1,::1）。
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - 被阻止的 IP 的逗号分隔列表。
    - (empty)
  * - rate.limit.trusted.proxies
    - 受信任代理 IP 的逗号分隔列表。仅信任来自这些 IP 的 X-Forwarded-For/X-Real-IP。
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - 为防止内存泄漏而执行清理操作之间的请求数。
    - ``1000``
  * - virtual.host.headers
    - 虚拟主机：Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - HTTP 代理服务器的主机名。
    - (empty)
  * - http.proxy.port
    - HTTP 代理服务器的端口号（例如 8080）。
    - ``8080``
  * - http.proxy.username
    - HTTP 代理认证的用户名。
    - (empty)
  * - http.proxy.password
    - HTTP 代理认证的密码。
    - (empty)
  * - http.fileupload.max.size
    - HTTP 文件上传的最大大小（字节）。
    - ``262144000``
  * - http.fileupload.threshold.size
    - HTTP 文件上传缓冲的阈值大小（字节）。
    - ``262144``
  * - http.fileupload.max.file.count
    - 每次 HTTP 上传允许的最大文件数。
    - ``10``

索引
----

.. list-table:: 爬虫通用
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - HTTP 爬取的线程数。
    - ``0``
  * - crawler.data.serializer
    - 爬虫数据的序列化器类型（例如 kryo）。
    - ``kryo``
  * - crawler.document.max.site.length
    - 文档中站点名称的最大长度。
    - ``100``
  * - crawler.document.site.encoding
    - 文档中站点名称的编码。
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - 文档中主机名未知时使用的主机名。
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - 是否对英文文档使用站点编码。
    - ``false``
  * - crawler.document.append.data
    - 是否向文档追加数据。
    - ``true``
  * - crawler.document.append.filename
    - 是否向文档追加文件名。
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - 文档中英数字单词的最大大小。
    - ``20``
  * - crawler.document.max.symbol.term.size
    - 文档中符号单词的最大大小。
    - ``10``
  * - crawler.document.duplicate.term.removed
    - 是否删除文档中的重复单词。
    - ``false``
  * - crawler.document.space.chars
    - 用于文档解析的 Unicode 空白字符。
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - 用于文档解析的 Unicode 句点字符。
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - 爬取数据的编码。
    - ``UTF-8``
  * - crawler.web.protocols
    - 爬取支持的 Web 协议。
    - ``http,https``
  * - crawler.file.protocols
    - 爬取支持的文件协议。
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - 爬取数据中环境变量键的模式。
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - 爬取时是否忽略 robots.txt。
    - ``false``
  * - crawler.ignore.robots.tags
    - 爬取时是否忽略 robots meta 标签。
    - ``false``
  * - crawler.ignore.content.exception
    - 爬取时是否忽略内容异常。
    - ``true``
  * - crawler.failure.url.status.codes
    - 被视为失败 URL 的 HTTP 状态码。
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - 爬取期间系统监控的间隔（秒）。
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - hot thread 监控中是否忽略空闲线程。
    - ``true``
  * - crawler.hotthread.interval
    - hot thread 监控的间隔（例如 500ms）。
    - ``500ms``
  * - crawler.hotthread.snapshots
    - hot thread 监控的快照数。
    - ``10``
  * - crawler.hotthread.threads
    - hot thread 监控的线程数。
    - ``3``
  * - crawler.hotthread.timeout
    - hot thread 监控的超时时间（例如 30s）。
    - ``30s``
  * - crawler.hotthread.type
    - hot thread 监控的类型（例如 cpu）。
    - ``cpu``
  * - crawler.metadata.content.excludes
    - 要从文档内容中排除的元数据字段。
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - 文档元数据名称的映射。
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``
      | ``frontmatter.title=title:string``

.. list-table:: 爬虫 HTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - 用于从 HTML 文档中提取主要内容的 XPath。
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - 用于从 HTML 文档中提取语言属性的 XPath。
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - 用于从 HTML 文档中提取摘要（描述）的 XPath。
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - 用于从 HTML 文档中提取规范 URL 的 XPath。
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - 文档处理时要裁剪（删除）的 HTML 标签。
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - 从 HTML 文档中提取的摘要的最大长度。
    - ``120``
  * - crawler.document.html.default.lang
    - HTML 文档的默认语言。
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - HTML 索引处理中要包含的模式。
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - HTML 索引处理中要排除的模式。
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - HTML 搜索处理中要包含的模式。
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - HTML 搜索处理中要排除的模式。
    - (empty)

.. list-table:: 爬虫文件
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - 文档中文件名的编码。
    - (empty)
  * - crawler.document.file.no.title.label
    - 文件没有标题时使用的标签。
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - 是否忽略内容为空的文件。
    - ``false``
  * - crawler.document.file.max.title.length
    - 文档中文件标题的最大长度。
    - ``100``
  * - crawler.document.file.max.digest.length
    - 文档中文件摘要的最大长度。
    - ``200``
  * - crawler.document.file.append.meta.content
    - 是否追加来自文件的元内容。
    - ``true``
  * - crawler.document.file.append.body.content
    - 是否追加来自文件的正文内容。
    - ``true``
  * - crawler.document.file.default.lang
    - 文件文档的默认语言。
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - 文件索引处理中要包含的模式。
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - 文件索引处理中要排除的模式。
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - 文件搜索处理中要包含的模式。
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - 文件搜索处理中要排除的模式。
    - (empty)
  * - crawler.document.file.owner.enabled
    - 是否为已爬取的文件（SMB、本地文件系统和 FTP）的所有者建立索引。爬取配置参数 config.owner.enabled 会覆盖该设置。
    - ``true``
  * - crawler.document.file.last.modifier.enabled
    - 是否为已爬取的文件的最后修改者建立索引，从文档元数据中读取，读取不到时回退到文件所有者。爬取配置参数 config.last.modifier.enabled 会覆盖该设置。
    - ``true``

.. list-table:: 爬虫缓存
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - 是否启用文档缓存。
    - ``true``
  * - crawler.document.cache.max.size
    - 文档缓存的最大大小（字节）。
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - 文档缓存支持的 MIME 类型。
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation HTML 文档缓存的 MIME 类型。
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - 用于 MIME 类型检测的扩展名到 MIME 类型的覆盖映射（每行一个：.ext=mime/type）。
    - (empty)
  * - crawler.document.ocr.enabled
    - 是否使用 Tesseract OCR 从图像和扫描版 PDF 中提取文本（需要 tesseract 命令）。
    - ``false``
  * - crawler.document.ocr.language
    - Tesseract OCR 的语言，用 '+' 连接（例如 jpn+eng）。
    - ``eng``
  * - crawler.document.ocr.timeout
    - Tesseract OCR 单次运行的超时时间（秒）。
    - ``120``

.. list-table:: 索引器
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - 是否为索引器启用线程转储。
    - ``true``
  * - indexer.unprocessed.document.size
    - 索引器的最大未处理文档数。
    - ``1000``
  * - indexer.click.count.enabled
    - 是否在索引器中启用点击数跟踪。
    - ``true``
  * - indexer.favorite.count.enabled
    - 是否在索引器中启用收藏数跟踪。
    - ``true``
  * - indexer.webfs.commit.margin.time
    - 索引器中 webfs 的提交余量时间（毫秒）。
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - 索引器中 webfs 的最大空列表数。
    - ``3600``
  * - indexer.webfs.update.interval
    - 索引器中 webfs 的更新间隔（毫秒）。
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - 索引器中 webfs 的最大文档缓存大小。
    - ``10``
  * - indexer.webfs.max.document.request.size
    - 索引器中 webfs 的最大文档请求大小（字节）。
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - 索引器中数据的最大文档缓存大小。
    - ``10000``
  * - indexer.data.max.document.request.size
    - 索引器中数据的最大文档请求大小（字节）。
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - 索引器中数据的最大删除缓存大小。
    - ``100``
  * - indexer.data.max.redirect.count
    - 索引器中数据的最大重定向次数。
    - ``10``
  * - indexer.language.fields
    - 索引器中用于语言检测的字段。
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - 索引器中用于语言检测的文本长度。
    - ``1000``
  * - indexer.max.result.window.size
    - 索引器的最大结果窗口大小。
    - ``10000``
  * - indexer.max.search.doc.size
    - 索引器的最大搜索文档数。
    - ``50000``

.. list-table:: 索引设置
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - 索引的编解码器类型。
    - ``default``
  * - index.number_of_shards
    - 索引的主分片数。
    - ``5``
  * - index.auto_expand_replicas
    - 索引的自动扩展副本设置。
    - ``0-1``
  * - index.id.digest.algorithm
    - 索引 ID 的摘要算法。
    - ``SHA-512``
  * - index.user.initial_password
    - 索引用户的初始密码。
    - ``admin``

.. list-table:: 字段名称
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - 索引中收藏数的字段名称。
    - ``favorite_count``
  * - index.field.click_count
    - 索引中点击数的字段名称。
    - ``click_count``
  * - index.field.config_id
    - 索引中配置 ID 的字段名称。
    - ``config_id``
  * - index.field.expires
    - 索引中过期日期的字段名称。
    - ``expires``
  * - index.field.url
    - 索引中 URL 的字段名称。
    - ``url``
  * - index.field.doc_id
    - 索引中文档 ID 的字段名称。
    - ``doc_id``
  * - index.field.id
    - 索引中内部 ID 的字段名称。
    - ``_id``
  * - index.field.version
    - 索引中版本的字段名称。
    - ``_version``
  * - index.field.seq_no
    - 索引中序列号的字段名称。
    - ``_seq_no``
  * - index.field.primary_term
    - 索引中 primary term 的字段名称。
    - ``_primary_term``
  * - index.field.lang
    - 索引中语言的字段名称。
    - ``lang``
  * - index.field.has_cache
    - 索引中缓存状态的字段名称。
    - ``has_cache``
  * - index.field.last_modified
    - 索引中最后修改日期的字段名称。
    - ``last_modified``
  * - index.field.etag
    - 索引中已爬取文档的 ETag 响应头的字段名称。
    - ``etag``
  * - index.field.owner
    - 索引中已爬取文件的所有者的字段名称。
    - ``owner``
  * - index.field.last_modifier
    - 索引中已爬取文件的最后修改者的字段名称。
    - ``last_modifier``
  * - index.field.anchor
    - 索引中锚点的字段名称。
    - ``anchor``
  * - index.field.segment
    - 索引中段的字段名称。
    - ``segment``
  * - index.field.role
    - 索引中角色的字段名称。
    - ``role``
  * - index.field.boost
    - 索引中提升值的字段名称。
    - ``boost``
  * - index.field.created
    - 索引中创建日期的字段名称。
    - ``created``
  * - index.field.timestamp
    - 索引中时间戳的字段名称。
    - ``timestamp``
  * - index.field.label
    - 索引中标签的字段名称。
    - ``label``
  * - index.field.tag
    - 索引中文档的用户标签的字段名称。
    - ``tag``
  * - index.field.mimetype
    - 索引中 MIME 类型的字段名称。
    - ``mimetype``
  * - index.field.parent_id
    - 索引中父 ID 的字段名称。
    - ``parent_id``
  * - index.field.important_content
    - 索引中重要内容的字段名称。
    - ``important_content``
  * - index.field.content
    - 索引中内容的字段名称。
    - ``content``
  * - index.field.content_minhash_bits
    - 索引中内容 minhash 位数的字段名称。
    - ``content_minhash_bits``
  * - index.field.cache
    - 索引中缓存的字段名称。
    - ``cache``
  * - index.field.digest
    - 索引中摘要的字段名称。
    - ``digest``
  * - index.field.title
    - 索引中标题的字段名称。
    - ``title``
  * - index.field.host
    - 索引中主机的字段名称。
    - ``host``
  * - index.field.site
    - 索引中站点的字段名称。
    - ``site``
  * - index.field.content_length
    - 索引中内容长度的字段名称。
    - ``content_length``
  * - index.field.filetype
    - 索引中文件类型的字段名称。
    - ``filetype``
  * - index.field.filename
    - 索引中文件名的字段名称。
    - ``filename``
  * - index.field.thumbnail
    - 索引中缩略图的字段名称。
    - ``thumbnail``
  * - index.field.virtual_host
    - 索引中虚拟主机的字段名称。
    - ``virtual_host``
  * - response.field.content_title
    - 响应中内容标题的字段名称。
    - ``content_title``
  * - response.field.content_description
    - 响应中内容描述的字段名称。
    - ``content_description``
  * - response.field.url_link
    - 响应中 URL 链接的字段名称。
    - ``url_link``
  * - response.field.site_path
    - 响应中站点路径的字段名称。
    - ``site_path``
  * - response.max.title.length
    - 响应中内容标题的最大长度。
    - ``50``
  * - response.max.site.path.length
    - 响应中站点路径的最大长度。
    - ``100``
  * - response.highlight.content_title.enabled
    - 是否在响应中启用内容标题高亮。
    - ``true``
  * - response.inline.mimetypes
    - 响应的内联 MIME 类型。
    - ``application/pdf,text/plain``
  * - response.headers
    - 响应的 HTTP 头信息。Access-Control-\* 和 Timing-Allow-Origin 会被忽略（CORS 由 api.cors.\* / CorsFilter 控制）。请勿在此处设置 Vary。
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=Content-Security-Policy: reflected-xss block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: 文档索引
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - 搜索文档的索引名称。
    - ``fess.search``
  * - index.document.update.index
    - 更新文档的索引名称。
    - ``fess.update``
  * - index.document.suggest.index
    - 建议文档的索引名称。
    - ``fess``
  * - index.document.crawler.index
    - 爬虫文档的索引名称。
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - 爬虫队列索引的主分片数。
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - 爬虫数据索引的主分片数。
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - 爬虫过滤器索引的主分片数。
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - 爬虫队列索引的副本数。
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - 爬虫数据索引的副本数。
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - 爬虫过滤器索引的副本数。
    - ``1``
  * - index.config.index
    - 配置数据的索引名称。
    - ``fess_config``
  * - index.user.index
    - 用户数据的索引名称。
    - ``fess_user``
  * - index.log.index
    - 日志数据的索引名称。
    - ``fess_log``
  * - index.dictionary.prefix
    - 字典索引名称的前缀。
    - (empty)

.. list-table:: 文档管理
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - 索引中管理用的数组类型字段。
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - 索引中管理用的日期类型字段。
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - 索引中管理用的整数类型字段。
    - (empty)
  * - index.admin.long.fields
    - 索引中管理用的长整数类型字段。
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - 索引中管理用的浮点类型字段。
    - ``boost``
  * - index.admin.double.fields
    - 索引中管理用的双精度浮点类型字段。
    - (empty)
  * - index.admin.required.fields
    - 索引中管理用的必填字段。
    - ``url,title,role,boost``

.. list-table:: 超时
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - 索引搜索操作的超时时间。
    - ``3m``
  * - index.scroll.search.timeout
    - 滚动搜索操作的超时时间。
    - ``3m``
  * - index.index.timeout
    - 索引操作的超时时间。
    - ``3m``
  * - index.bulk.timeout
    - 批量索引操作的超时时间。
    - ``3m``
  * - index.delete.timeout
    - 索引中删除操作的超时时间。
    - ``3m``
  * - index.health.timeout
    - 索引健康检查的超时时间。
    - ``10m``
  * - index.indices.timeout
    - 索引 indices 操作的超时时间。
    - ``1m``

.. list-table:: 文件类型
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - 用于索引的 MIME 类型到文件类型标签的映射。
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
    - 每次重新索引操作处理的文档数。
    - ``100``
  * - index.reindex.body
    - 重新索引操作的请求体模板。
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - 重新索引操作的每秒请求数（"adaptive" 表示自动）。
    - ``adaptive``
  * - index.reindex.refresh
    - 重新索引后是否刷新索引。
    - ``false``
  * - index.reindex.timeout
    - 重新索引操作的超时时间。
    - ``1m``
  * - index.reindex.scroll
    - 重新索引操作的滚动超时时间。
    - ``5m``
  * - index.reindex.max_docs
    - 重新索引操作的最大文档数。
    - (empty)

.. list-table:: 查询
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - 搜索查询的最大长度。
    - ``1000``
  * - query.timeout
    - 搜索查询的超时时间（毫秒）。
    - ``10000``
  * - query.timeout.logging
    - 是否记录因查询超时或分片失败而结果不完整的搜索。
    - ``true``
  * - query.track.total.hits
    - 查询中要跟踪的总命中数的最大值。仅支持正数或 true；false 会使响应中不含命中数，而要求使用 false 的搜索（无论是在此处还是作为搜索参数）会被拒绝。
    - ``10000``
  * - query.geo.fields
    - 位置信息搜索查询使用的字段。
    - ``location``
  * - query.browser.lang.parameter.name
    - 查询中浏览器语言的参数名称。
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - 是否将单词替换为前缀查询。
    - ``true``
  * - query.orsearch.min.hit.count
    - OR 搜索查询的最小命中数。
    - ``-1``
  * - query.highlight.terminal.chars
    - 查询高亮的 Unicode 终止字符。
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - 查询高亮的片段大小。
    - ``60``
  * - query.highlight.number.of.fragments
    - 查询高亮的片段数。
    - ``2``
  * - query.highlight.type
    - 查询高亮的类型。
    - ``fvh``
  * - query.highlight.tag.pre
    - 高亮文本之前使用的标签。
    - ``<strong>``
  * - query.highlight.tag.post
    - 高亮文本之后使用的标签。
    - ``</strong>``
  * - query.highlight.boundary.chars
    - 查询高亮的边界字符。
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - 查询高亮边界的最大扫描量。
    - ``20``
  * - query.highlight.boundary.scanner
    - 查询高亮边界的扫描器类型。
    - ``chars``
  * - query.highlight.encoder
    - 查询高亮的编码器类型。
    - ``default``
  * - query.highlight.force.source
    - 查询高亮是否强制使用 source。
    - ``false``
  * - query.highlight.fragmenter
    - 查询高亮的分段器类型。
    - ``span``
  * - query.highlight.fragment.offset
    - 查询高亮片段的偏移量。
    - ``-1``
  * - query.highlight.no.match.size
    - 查询高亮无匹配时的大小。
    - ``0``
  * - query.highlight.order
    - 查询高亮片段的顺序。
    - ``score``
  * - query.highlight.phrase.limit
    - 查询高亮的短语限制。
    - ``256``
  * - query.highlight.content.description.fields
    - 查询高亮中用于内容描述的字段。
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - 查询高亮中是否检测边界位置。
    - ``true``
  * - query.highlight.text.fragment.type
    - 查询高亮中文本片段的类型。
    - ``query``
  * - query.highlight.text.fragment.size
    - 查询高亮中文本片段的大小。
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - 查询高亮中文本片段的前缀长度。
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - 查询高亮中文本片段的后缀长度。
    - ``5``
  * - query.max.search.result.offset
    - 查询的最大搜索结果偏移量。
    - ``100000``
  * - query.additional.default.fields
    - 查询的附加默认字段。
    - (empty)
  * - query.additional.response.fields
    - 为搜索结果从索引中获取的附加字段。只有同时列在 query.additional.api.response.fields 中时，搜索 API 才会返回在此处添加的字段。
    - (empty)
  * - query.additional.api.response.fields
    - 查询的附加 API 响应字段。此键仅向 v2 API 响应允许列表追加字段（只增不减）；它不会获取这些字段。字段还必须被获取：对于搜索 API，请将其添加到 query.additional.response.fields；对于滚动 API，请将其添加到 query.additional.scroll.response.fields。请勿添加 ACL 或内部字段（例如 role、virtual_host）；添加它们会在搜索 API 响应中暴露访问控制信息。
    - (empty)
  * - query.additional.scroll.response.fields
    - 为滚动搜索结果从索引中获取的附加字段。只有同时列在 query.additional.api.response.fields 中时，滚动 API 才会返回在此处添加的字段。
    - (empty)
  * - query.additional.cache.response.fields
    - 查询的附加缓存响应字段。
    - (empty)
  * - query.additional.highlighted.fields
    - 查询的附加高亮字段。
    - (empty)
  * - query.additional.search.fields
    - 查询的附加搜索字段。
    - (empty)
  * - query.additional.facet.fields
    - 查询的附加分面字段。
    - (empty)
  * - query.additional.sort.fields
    - 查询的附加排序字段。
    - (empty)
  * - query.additional.analyzed.fields
    - 查询的附加已分析字段。
    - (empty)
  * - query.additional.not.analyzed.fields
    - 查询的附加未分析字段。
    - (empty)
  * - query.gsa.response.fields
    - 查询中 GSA 响应的字段。
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - GSA 查询的默认语言。
    - ``en``
  * - query.gsa.default.sort
    - GSA 查询的默认排序。
    - (empty)
  * - query.gsa.meta.prefix
    - GSA 查询的 meta 前缀。
    - ``MT_``
  * - query.gsa.index.field.charset
    - GSA 索引查询的字符集字段。
    - ``charset``
  * - query.gsa.index.field.content_type.
    - GSA 索引查询的内容类型字段。
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - 折叠查询的最大并发分组结果数。
    - ``4``
  * - query.collapse.inner.hits.name
    - 折叠查询的 inner hits 名称。
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - 折叠查询的 inner hits 大小。
    - ``0``
  * - query.collapse.inner.hits.sorts
    - 折叠查询中 inner hits 的排序。
    - (empty)
  * - query.default.languages
    - 查询的默认语言。
    - (empty)
  * - query.json.default.preference
    - JSON 查询的默认 preference。
    - ``_query``
  * - query.gsa.default.preference
    - GSA 查询的默认 preference。
    - ``_query``
  * - query.language.mapping
    - 查询的语言映射。
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

.. list-table:: 提升
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - 查询中标题字段的提升值。
    - ``0.5``
  * - query.boost.title.lang
    - 查询中带语言的标题字段的提升值。
    - ``1.0``
  * - query.boost.content
    - 查询中内容字段的提升值。
    - ``0.05``
  * - query.boost.content.lang
    - 查询中带语言的内容字段的提升值。
    - ``0.1``
  * - query.boost.important_content
    - 查询中重要内容字段的提升值。
    - ``-1.0``
  * - query.boost.important_content.lang
    - 查询中带语言的重要内容字段的提升值。
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - 查询中模糊提升的最小长度。
    - ``4``
  * - query.boost.fuzzy.title
    - 模糊标题查询的提升值。
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - 模糊标题查询的模糊度。
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - 模糊标题查询的扩展数。
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - 模糊标题查询的前缀长度。
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - 模糊标题查询中是否允许换位。
    - ``true``
  * - query.boost.fuzzy.content
    - 模糊内容查询的提升值。
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - 模糊内容查询的模糊度。
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - 模糊内容查询的扩展数。
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - 模糊内容查询的前缀长度。
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - 模糊内容查询中是否允许换位。
    - ``true``
  * - query.default.query_type
    - 默认查询类型。
    - ``bool``
  * - query.dismax.tie_breaker
    - dismax 查询的 tie breaker 值。
    - ``0.1``
  * - query.bool.minimum_should_match
    - 布尔查询的 minimum should match 值。
    - (empty)
  * - query.prefix.expansions
    - 前缀查询的扩展数。
    - ``50``
  * - query.prefix.slop
    - 前缀查询的 slop 值。
    - ``0``
  * - query.fuzzy.prefix_length
    - 模糊查询的前缀长度。
    - ``0``
  * - query.fuzzy.expansions
    - 模糊查询的扩展数。
    - ``50``
  * - query.fuzzy.transpositions
    - 模糊查询中是否允许换位。
    - ``true``

.. list-table:: 分面
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - 分面查询的字段。
    - ``label``
  * - query.facet.fields.size
    - 分面字段的大小。
    - ``100``
  * - query.facet.fields.size.max
    - facet.size 的上限（在搜索的统一入口处应用）。
    - ``1000``
  * - query.facet.fields.min_doc_count
    - 分面字段的最小文档数。
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - facet.minDocCount 的上限（在搜索的统一入口处应用）。
    - ``2147483647``
  * - query.facet.fields.sort
    - 分面字段的排序顺序。
    - ``count.desc``
  * - query.facet.fields.missing
    - 缺失分面字段的值。
    - (empty)
  * - query.facet.queries
    - 分面查询定义。
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: 排名
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Rank Fusion 的窗口大小。
    - ``200``
  * - rank.fusion.rank_constant
    - Rank Fusion 的排名常数。
    - ``20``
  * - rank.fusion.threads
    - Rank Fusion 的线程数。
    - ``-1``
  * - rank.fusion.timeout
    - 当 Fess 自行融合各搜索器的结果（rank.fusion.engine.enabled=false）时，等待主搜索器以外的搜索器的最长时间（毫秒）。到那时仍未应答的搜索器将被排除在该次搜索之外，并且结果会被标记为部分结果和已超时。始终会等待主搜索器。0 或更小的值表示无限期等待。
    - ``10000``
  * - rank.fusion.score_field
    - Rank Fusion 的分数字段。
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - 是否由搜索引擎执行 Rank Fusion。为 true 时，能够参与的搜索器会把各自的查询合并到同一个请求中，因此分面和总命中数描述的是融合后的结果集。为 false 时，由 Fess 自行融合各搜索器的结果。
    - ``false``
  * - rank.fusion.combination.technique
    - 搜索引擎组合融合分数的方式：rrf、arithmetic_mean、geometric_mean 或 harmonic_mean。
    - ``rrf``
  * - rank.fusion.normalization.technique
    - 分数在组合之前的归一化方式：min_max、l2 或 z_score。rrf 会忽略该设置。z_score 只能与 arithmetic_mean 组合；任何其他平均方式都会被拒绝，并由 Fess 自行融合结果。
    - ``min_max``
  * - rank.fusion.combination.weights
    - 引擎端融合中每个搜索器的权重，格式为 name:weight 对，例如 default:0.7,semantic_chunk:0.3。权重之和必须为 1.0，并且必须列出每个参与的搜索器。为空时各搜索器权重相等。
    - (empty)
  * - rank.fusion.pagination_depth
    - 每个搜索器针对每个分片向引擎端融合贡献的结果数。这既限制了客户端可以翻页的深度，也限制了引擎参与排名的文档集合：融合搜索最多可翻阅这么多条结果，并且绝不会超过 indexer.max.result.window.size。
    - ``1000``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - 是否从文件获取 SMB 角色。
    - ``true``
  * - smb.available.sid.types
    - SMB 可用的 SID 类型。
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - 是否从文件获取文件角色。
    - ``true``
  * - ftp.role.from.file
    - 是否从文件获取 FTP 角色。
    - ``true``

.. list-table:: 备份
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - 索引备份的目标文件。
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - 索引备份的目标日志文件。
    - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - 加载索引备份日志的超时时间。
    - ``60000``

.. list-table:: 日志
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - 日志记录的应用程序包。
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - 是否启用搜索文档日志记录。
    - ``true``
  * - logging.search.docs.fields
    - 搜索文档要记录的字段。
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - 搜索日志记录是否使用日志文件。
    - ``true``
  * - logging.search.max.queue.size
    - 搜索日志记录的最大队列大小。
    - ``10000``
  * - logging.click.max.queue.size
    - 点击日志记录的最大队列大小。
    - ``10000``
  * - logging.chat.max.queue.size
    - 聊天使用情况日志记录的最大队列大小。
    - ``10000``
  * - search.history.enabled
    - 是否为搜索历史记录已登录用户的搜索条件。
    - ``true``
  * - search.history.size
    - 每个用户返回的搜索历史条目的最大数量。
    - ``10``
  * - user.tag.enabled
    - 已登录用户是否可以为文档添加用户标签。每个用户标签属于创建它的用户。
    - ``false``
  * - user.tag.name.max.length
    - 用户标签名称的最大长度（以码点计）。
    - ``50``
  * - user.tag.max.tags
    - 一个用户可拥有的用户标签的最大数量。
    - ``1000``
  * - user.tag.max.paths
    - 一个用户标签可以添加到的 URL 的最大数量。
    - ``10000``
  * - user.tag.queue.max.size
    - 在应用到文档之前保存在内存中的待处理用户标签变更的最大数量。
    - ``10000``
  * - user.tag.process.batch.size
    - 将用户标签变更应用到文档时，每个批量请求更新的 URL 数。
    - ``100``
  * - user.tag.visible.max.size
    - 一次搜索中一个用户可见的用户标签的最大数量。
    - ``1000``

Web
---

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - 管理表单的最大输入大小。
    - ``10000``
  * - form.admin.label.in.config.enabled
    - 管理配置表单中是否启用标签。
    - ``false``
  * - form.admin.default.template.name
    - 管理表单的默认模板名称。
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - 是否启用 OSDD 链接（OpenSearch Description Document）。
    - ``auto``
  * - clipboard.copy.icon.enabled
    - 是否启用剪贴板复制图标。
    - ``true``
  * - authentication.admin.users
    - 用于认证的管理员用户名。
    - ``admin``
  * - authentication.admin.users.ignore.case
    - 是否不区分大小写地匹配 authentication.admin.users：auto、true 或 false。设置了 ldap.provider.url 时，auto 会忽略大小写。
    - ``auto``
  * - authentication.admin.roles
    - 用于认证的管理员角色名称。
    - ``admin``
  * - role.search.default.permissions
    - 搜索角色的默认权限。
    - (empty)
  * - role.search.default.display.permissions
    - 搜索角色的默认显示权限。
    - ``{role}guest``
  * - role.search.guest.permissions
    - 请保持 role.search.guest.permissions 非空。它用于初始化 guest 角色，使匿名搜索角色集合保持非空；如果解析出的角色集合为空，则会跳过角色过滤器（fail-open），这可能会禁用基于角色的访问控制，并将文档暴露给匿名用户。搜索角色的访客权限。
    - ``{role}guest``
  * - role.search.user.prefix
    - 搜索中用户角色的前缀。
    - ``1``
  * - role.search.group.prefix
    - 搜索中组角色的前缀。
    - ``2``
  * - role.search.role.prefix
    - 搜索中 role 角色的前缀。
    - ``R``
  * - role.search.denied.prefix
    - 搜索中被拒绝角色的前缀。
    - ``D``
  * - cookie.default.path
    - Cookie 的默认路径（没有上下文路径时基本上为 '/'）
    - ``/``
  * - cookie.default.expire
    - Cookie 的默认过期时间（秒），例如 31556926：一年，86400：一天
    - ``3600``
  * - session.tracking.modes
    - 会话跟踪模式
    - ``cookie``
  * - session.cookie.secure
    - 是否在启动时为会话 Cookie（JSESSIONID）添加 Secure 属性。留空（默认）时使用 Tomcat 的自动行为（仅对 HTTPS 请求添加 Secure）。生产环境的 HTTPS 部署请设置为 true，尤其是在反向代理处终止 TLS 时。为 true 时，Cookie 不会通过 HTTP 发送，因此纯 HTTP 下无法建立会话；本地主机开发时请保持留空。使用 SameSite=none 时也需要 Secure 属性。更改此值需要重启。
    - (empty)
  * - cookie.search.parameter.keys
    - SSO 登录前要存储到 Cookie 中的请求参数键的逗号分隔列表。
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - 必须存在才能存储到 Cookie 中的必需参数键的逗号分隔列表。
    - ``q``
  * - cookie.search.parameter.max.length
    - 存储在 Cookie 中的已编码搜索参数的最大长度。
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - 已存储的搜索参数解压后允许的最大字节数。上面的限制适用于经 gzip 压缩的 Cookie，而这并不能限制其展开后的大小，且 Cookie 来自客户端。
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - 登录后恢复已存储的搜索参数时所构建的查询字符串的最大长度。恢复它们只是一种便利，而登录则不是，因此过长的查询字符串会被丢弃，而不是写入容器会拒绝的 Location 头。百分号编码会使 CJK 查询膨胀到九倍，因此该值远小于查询本身可能达到的长度。请与 tomcat_config.properties 中的 tomcat.maxHttpHeaderSize 一起调高，后者限制响应头的大小。
    - ``4096``
  * - cookie.search.parameter.name
    - SSO 登录前用于存储已编码搜索参数的 Cookie 名称。
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - 是否为搜索参数 Cookie 设置 HttpOnly 属性。
    - ``true``
  * - cookie.search.parameter.secure
    - 是否为搜索参数 Cookie 设置 Secure 属性。在使用 HTTPS 的生产环境中应为 true。
    - (empty)
  * - cookie.search.parameter.max_age
    - 搜索参数 Cookie 的 Max-Age（秒）。仅会话 Cookie 请使用 -1。
    - ``60``
  * - cookie.search.parameter.domain
    - 搜索参数 Cookie 的 Domain 属性。设置为希望该 Cookie 生效的域范围（例如 example.com）。
    - (empty)
  * - cookie.search.parameter.path
    - 搜索参数 Cookie 的 Path 属性。通常设置为 "/" 或应用的上下文路径。
    - ``/``
  * - cookie.search.parameter.same_site
    - 搜索参数 Cookie 的 SameSite 属性。有效值：Lax、Strict、None
    - ``Lax``
  * - paging.page.size
    - 分页时每页的大小
    - ``25``
  * - paging.page.range.size
    - 分页时页面范围的大小
    - ``5``
  * - paging.page.range.fill.limit
    - 分页时页面范围的选项 'fillLimit'
    - ``true``

.. list-table:: 每页获取数量
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - 每页获取的文档提升记录的最大数量。
    - ``1000``
  * - page.keymatch.max.fetch.size
    - 每页获取的关键词匹配记录的最大数量。
    - ``1000``
  * - page.labeltype.max.fetch.size
    - 每页获取的标签类型记录的最大数量。
    - ``1000``
  * - page.tagtype.max.fetch.size
    - 每页获取的用户标签记录的最大数量。
    - ``1000``
  * - page.roletype.max.fetch.size
    - 每页获取的角色类型记录的最大数量。
    - ``1000``
  * - page.user.max.fetch.size
    - 每页获取的用户记录的最大数量。
    - ``1000``
  * - page.role.max.fetch.size
    - 每页获取的角色记录的最大数量。
    - ``1000``
  * - page.group.max.fetch.size
    - 每页获取的组记录的最大数量。
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - 每页获取的爬网信息参数的最大数量。
    - ``100``
  * - page.crawling.info.max.fetch.size
    - 每页获取的爬网信息记录的最大数量。
    - ``1000``
  * - page.data.config.max.fetch.size
    - 每页获取的数据存储配置记录的最大数量。
    - ``100``
  * - page.web.config.max.fetch.size
    - 每页获取的 Web 配置记录的最大数量。
    - ``100``
  * - page.file.config.max.fetch.size
    - 每页获取的文件配置记录的最大数量。
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - 每页获取的重复主机记录的最大数量。
    - ``1000``
  * - page.failure.url.max.fetch.size
    - 每页获取的失败 URL 记录的最大数量。
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - 每页获取的收藏日志记录的最大数量。
    - ``100``
  * - page.file.auth.max.fetch.size
    - 每页获取的文件认证记录的最大数量。
    - ``100``
  * - page.web.auth.max.fetch.size
    - 每页获取的 Web 认证记录的最大数量。
    - ``100``
  * - page.path.mapping.max.fetch.size
    - 每页获取的路径映射记录的最大数量。
    - ``1000``
  * - page.request.header.max.fetch.size
    - 每页获取的请求头记录的最大数量。
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - 每页获取的计划任务记录的最大数量。
    - ``100``
  * - page.elevate.word.max.fetch.size
    - 每页获取的提升词记录的最大数量。
    - ``1000``
  * - page.bad.word.max.fetch.size
    - 每页获取的屏蔽词记录的最大数量。
    - ``1000``
  * - page.dictionary.max.fetch.size
    - 每页获取的字典记录的最大数量。
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - 每页获取的相关内容记录的最大数量。
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - 每页获取的相关查询记录的最大数量。
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - 每页获取的缩略图队列记录的最大数量。
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - 每页获取的缩略图清除记录的最大数量。
    - ``100``
  * - page.score.booster.max.fetch.size
    - 每页获取的评分提升器记录的最大数量。
    - ``1000``
  * - page.searchlog.max.fetch.size
    - 每页获取的搜索日志记录的最大数量。
    - ``10000``
  * - page.searchlist.track.total.hits
    - 搜索列表页面中是否跟踪总命中数。
    - ``true``
  * - page.searchlist.content.max.length
    - 搜索列表编辑页面上渲染的内容的最大长度（字符数）。
    - ``100000``

.. list-table:: 搜索页面
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - 搜索结果的默认起始页。
    - ``0``
  * - paging.search.page.size
    - 每页搜索结果的默认大小。
    - ``10``
  * - paging.search.page.max.size
    - 每页搜索结果的最大大小。
    - ``100``
  * - api.param.max.length
    - v2 API 字符串查询参数（q、sort、sdh）的最大长度。OWASP API4:2023。
    - ``1000``
  * - api.param.max.array.size
    - v2 API 可重复查询参数的最大值个数。
    - ``100``
  * - api.click.max.timestamp
    - v2 点击 API 接受的点击日志时间戳（rt，epoch 毫秒）的最大值。OWASP API4:2023。
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - 搜索日志
    - ``-1``
  * - searchlog.request.headers
    - 要包含在搜索日志中的请求头。
    - (empty)
  * - searchlog.process.batch_size
    - 搜索日志处理的批处理大小。
    - ``100``
  * - related_query.generate.days
    - 从搜索日志生成相关查询时读取的搜索日志天数。
    - ``30``
  * - related_query.generate.term.size
    - 每个虚拟主机生成的单词的最大数量。
    - ``100``
  * - related_query.generate.query.size
    - 每个单词生成的相关查询的最大数量。
    - ``5``
  * - related_query.generate.min.sessions
    - 单词及其每个相关查询所需的最少不同用户会话数。
    - ``3``
  * - related_query.generate.session.interval
    - 一次搜索之后的间隔（分钟），在该间隔内同一会话的后续搜索算作细化。
    - ``10``
  * - related_query.generate.seed.log.size
    - 为找出搜索过某个单词的会话而读取的该单词的搜索日志的最大数量。
    - ``1000``
  * - related_query.generate.seed.session.size
    - 每个单词读取其后续搜索的会话的最大数量。
    - ``200``
  * - related_query.generate.log.fetch.size
    - 每个单词读取的后续搜索日志的最大数量。
    - ``2000``
  * - related_query.generate.query.min.length
    - 生成的单词或相关查询的最小长度（字符数）。
    - ``2``
  * - related_query.generate.query.max.length
    - 生成的单词或相关查询的最大长度（字符数）。
    - ``50``
  * - docreport.duplicate.group.size
    - docreport 文档报告页面显示的重复组的最大数量，按从大到小排列。
    - ``100``
  * - docreport.duplicate.docs.size
    - 文档报告页面为每个重复组列出的文档的最大数量。
    - ``10``
  * - docreport.duplicate.export.page.size
    - 将重复报告下载为 CSV 时，每个请求读取的内容签名数。
    - ``10000``
  * - docreport.dormant.days
    - 文档自最后一次修改起经过多少天后被视为休眠的默认天数。
    - ``365``
  * - thumbnail.html.image.min.width
    - 缩略图中 HTML 图像的最小宽度。
    - ``100``
  * - thumbnail.html.image.min.height
    - 缩略图中 HTML 图像的最小高度。
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - 缩略图中 HTML 图像的最大纵横比。
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - 生成的缩略图图像的宽度。
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - 生成的缩略图图像的高度。
    - ``100``
  * - thumbnail.html.image.format
    - 生成的缩略图图像的格式。
    - ``png``
  * - thumbnail.html.image.xpath
    - 用于为缩略图选择图像的 XPath。
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - 要从缩略图生成中排除的文件扩展名。
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - 缩略图生成器的间隔。
    - ``0``
  * - thumbnail.generator.targets
    - 缩略图生成器的目标（例如 all）。
    - ``all``
  * - thumbnail.crawler.enabled
    - 是否启用缩略图爬虫。
    - ``true``
  * - thumbnail.system.monitor.interval
    - 缩略图处理中系统监控的间隔。
    - ``60``

.. list-table:: 用户
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - 用户代码设置
    - ``userCode``
  * - user.code.min.length
    - 用户代码的最小长度。
    - ``20``
  * - user.code.max.length
    - 用户代码的最大长度。
    - ``100``
  * - user.code.pattern
    - 用于验证的用户代码模式。
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - 在电子邮件的 From 字段中显示的名称。
    - ``Administrator``
  * - mail.from.address
    - 在 From 字段中使用的电子邮件地址。
    - ``root@localhost``
  * - mail.hostname
    - 邮件服务器的主机名。
    - (empty)
  * - scheduler.target.name
    - 调度器的目标名称。
    - (empty)
  * - scheduler.job.class
    - 调度器的作业类。
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - 调度器中并发执行的模式。
    - ``QUIT``
  * - scheduler.monitor.interval
    - 调度器监控的间隔。
    - ``30``
  * - coordinator.poll.interval
    - 轮询心跳和事件的间隔（秒）。
    - ``60``
  * - coordinator.heartbeat.ttl
    - 实例心跳文档的存活时间（毫秒）。
    - ``180000``
  * - coordinator.operation.ttl
    - 操作锁文档的存活时间（毫秒）。
    - ``7200000``
  * - coordinator.operation.retry
    - 获取操作锁的最大重试次数。
    - ``3``
  * - coordinator.event.ttl
    - 事件通知文档的存活时间（毫秒）。
    - ``600000``
  * - online.help.base.link
    - 在线帮助的基础链接。
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - 在线帮助的安装指南链接。
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - 在线帮助的生命周期结束信息链接。
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - 失败 URL 的在线帮助键。
    - ``failureurl``
  * - online.help.name.elevateword
    - 提升词的在线帮助键。
    - ``elevateword``
  * - online.help.name.reqheader
    - 请求头的在线帮助键。
    - ``reqheader``
  * - online.help.name.dict.synonym
    - 同义词词典的在线帮助键。
    - ``synonym``
  * - online.help.name.dict
    - 字典的在线帮助键。
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Kuromoji 词典的在线帮助键。
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - Protwords 词典的在线帮助键。
    - ``protwords``
  * - online.help.name.dict.stopwords
    - 停用词词典的在线帮助键。
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Stemmer 覆盖词典的在线帮助键。
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - 映射词典的在线帮助键。
    - ``mapping``
  * - online.help.name.webconfig
    - Web 配置的在线帮助键。
    - ``webconfig``
  * - online.help.name.searchlist
    - 搜索列表的在线帮助键。
    - ``searchlist``
  * - online.help.name.log
    - 日志的在线帮助键。
    - ``log``
  * - online.help.name.general
    - 常规设置的在线帮助键。
    - ``general``
  * - online.help.name.role
    - 角色的在线帮助键。
    - ``role``
  * - online.help.name.joblog
    - 作业日志的在线帮助键。
    - ``joblog``
  * - online.help.name.keymatch
    - 关键词匹配的在线帮助键。
    - ``keymatch``
  * - online.help.name.relatedquery
    - 相关查询的在线帮助键。
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - 相关内容的在线帮助键。
    - ``relatedcontent``
  * - online.help.name.wizard
    - 向导的在线帮助键。
    - ``wizard``
  * - online.help.name.badword
    - 屏蔽词的在线帮助键。
    - ``badword``
  * - online.help.name.pathmap
    - 路径映射的在线帮助键。
    - ``pathmap``
  * - online.help.name.boostdoc
    - 文档提升的在线帮助键。
    - ``boostdoc``
  * - online.help.name.dataconfig
    - 数据存储配置的在线帮助键。
    - ``dataconfig``
  * - online.help.name.systeminfo
    - 系统信息的在线帮助键。
    - ``systeminfo``
  * - online.help.name.user
    - 用户的在线帮助键。
    - ``user``
  * - online.help.name.group
    - 组的在线帮助键。
    - ``group``
  * - online.help.name.dashboard
    - 仪表板的在线帮助键。
    - ``dashboard``
  * - online.help.name.webauth
    - Web 认证的在线帮助键。
    - ``webauth``
  * - online.help.name.fileconfig
    - 文件配置的在线帮助键。
    - ``fileconfig``
  * - online.help.name.fileauth
    - 文件认证的在线帮助键。
    - ``fileauth``
  * - online.help.name.labeltype
    - 标签类型的在线帮助键。
    - ``labeltype``
  * - online.help.name.tagtype
    - 用户标签的在线帮助键。
    - ``tagtype``
  * - online.help.name.duplicatehost
    - 重复主机的在线帮助键。
    - ``duplicatehost``
  * - online.help.name.scheduler
    - 调度器的在线帮助键。
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - 爬网信息的在线帮助键。
    - ``crawlinginfo``
  * - online.help.name.backup
    - 备份的在线帮助键。
    - ``backup``
  * - online.help.name.upgrade
    - 升级的在线帮助键。
    - ``upgrade``
  * - online.help.name.sereq
    - 搜索请求的在线帮助键。
    - ``sereq``
  * - online.help.name.accesstoken
    - 访问令牌的在线帮助键。
    - ``accesstoken``
  * - online.help.name.suggest
    - 建议的在线帮助键。
    - ``suggest``
  * - online.help.name.searchlog
    - 搜索日志的在线帮助键。
    - ``searchlog``
  * - online.help.name.maintenance
    - 维护的在线帮助键。
    - ``maintenance``
  * - online.help.name.plugin
    - 插件的在线帮助键。
    - ``plugin``
  * - online.help.name.storage
    - 存储的在线帮助键。
    - ``storage``
  * - online.help.supported.langs
    - 在线帮助支持的语言。
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - 用户支持的论坛链接。
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - 论坛支持的语言。
    - ``en,ja``
  * - suggest.popular.word.seed
    - 热门词建议的种子值。
    - ``0``
  * - suggest.popular.word.tags
    - 热门词建议的标签。
    - (empty)
  * - suggest.popular.word.fields
    - 热门词建议的字段。
    - (empty)
  * - suggest.popular.word.excludes
    - 热门词建议的排除词。
    - (empty)
  * - suggest.popular.word.size
    - 要建议的热门词数量。
    - ``10``
  * - suggest.popular.word.window.size
    - 热门词建议的窗口大小。
    - ``30``
  * - suggest.popular.word.query.freq
    - 热门词建议的查询频率。
    - ``10``
  * - suggest.min.hit.count
    - 建议的最小命中数。
    - ``1``
  * - suggest.field.contents
    - 建议内容的字段。
    - ``_default``
  * - suggest.field.tags
    - 建议标签的字段。
    - ``label``
  * - suggest.field.roles
    - 建议角色的字段。
    - ``role``
  * - suggest.field.index.contents
    - 建议的索引内容。
    - ``content,title``
  * - suggest.update.request.interval
    - 建议更新请求的间隔。
    - ``0``
  * - suggest.update.doc.per.request
    - 每个建议更新请求的文档数。
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - 建议更新内容的百分比限制。
    - ``50%``
  * - suggest.update.contents.limit.num
    - 建议更新内容的最大数量。
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - 建议更新的最大文档大小。
    - ``50000``
  * - suggest.source.reader.scroll.size
    - 建议源读取器的滚动大小。
    - ``1``
  * - suggest.popular.word.cache.size
    - 热门词建议的缓存大小。
    - ``1000``
  * - suggest.popular.word.cache.expire
    - 热门词建议的缓存过期时间（秒）。
    - ``60``
  * - suggest.search.log.permissions
    - 建议搜索日志的权限。
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - 建议中系统监控的间隔。
    - ``60``
  * - ldap.admin.enabled
    - 是否启用 LDAP 管理。
    - ``false``
  * - ldap.admin.user.filter
    - LDAP 管理的用户过滤器。
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - LDAP 管理用户的基础 DN。
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - LDAP 管理用户的对象类。
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - LDAP 管理的角色过滤器。
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - LDAP 管理角色的基础 DN。
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - LDAP 管理角色的对象类。
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - LDAP 管理的组过滤器。
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - LDAP 管理组的基础 DN。
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - LDAP 管理组的对象类。
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - 是否为 LDAP 管理同步密码。
    - ``true``
  * - ldap.auth.validation
    - 是否验证 LDAP 认证。
    - ``true``
  * - ldap.connect.timeout
    - 建立 LDAP 连接的超时时间（毫秒）。这同时也限制 TLS 握手和初始绑定响应。0 或更小的值表示交由 JDK/OS 的默认值处理。
    - ``10000``
  * - ldap.read.timeout
    - 连接绑定之后等待 LDAP 响应的超时时间（毫秒）。0 或更小的值表示无限期等待。
    - ``30000``
  * - ldap.search.time.limit
    - LDAP 搜索的服务器端时间限制（毫秒）。0 或更小的值表示无限制。
    - ``60000``
  * - ldap.max.username.length
    - LDAP 的最大用户名长度。
    - ``-1``
  * - ldap.ignore.netbios.name
    - LDAP 中是否忽略 NetBIOS 名称。
    - ``true``
  * - ldap.group.name.with.underscores
    - LDAP 组名中是否允许下划线。
    - ``false``
  * - ldap.lowercase.permission.name
    - LDAP 权限名称是否使用小写。
    - ``false``
  * - ldap.allow.empty.permission
    - LDAP 中是否允许空权限。
    - ``true``
  * - ldap.samaccountname.group
    - LDAP 组是否使用 samAccountName。
    - ``false``
  * - ldap.role.search.user.enabled
    - 是否启用针对用户的 LDAP 角色搜索。
    - ``true``
  * - ldap.role.search.group.enabled
    - 是否启用针对组的 LDAP 角色搜索。
    - ``true``
  * - ldap.role.search.role.enabled
    - 是否启用针对角色的 LDAP 角色搜索。
    - ``true``
  * - ldap.attr.surname
    - 姓氏的 LDAP 属性。
    - ``sn``
  * - ldap.attr.givenName
    - 名字的 LDAP 属性。
    - ``givenName``
  * - ldap.attr.employeeNumber
    - 员工编号的 LDAP 属性。
    - ``employeeNumber``
  * - ldap.attr.mail
    - 邮件的 LDAP 属性。
    - ``mail``
  * - ldap.attr.telephoneNumber
    - 电话号码的 LDAP 属性。
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - 家庭电话的 LDAP 属性。
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - 家庭邮寄地址的 LDAP 属性。
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - 带标签的 URI 的 LDAP 属性。
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - 房间号的 LDAP 属性。
    - ``roomNumber``
  * - ldap.attr.description
    - 描述的 LDAP 属性。
    - ``description``
  * - ldap.attr.title
    - 职位的 LDAP 属性。
    - ``title``
  * - ldap.attr.pager
    - 寻呼机的 LDAP 属性。
    - ``pager``
  * - ldap.attr.street
    - 街道的 LDAP 属性。
    - ``street``
  * - ldap.attr.postalCode
    - 邮政编码的 LDAP 属性。
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - 物理投递办公室名称的 LDAP 属性。
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - 目的地指示符的 LDAP 属性。
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - 国际 ISDN 号码的 LDAP 属性。
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - 州/省的 LDAP 属性。
    - ``st``
  * - ldap.attr.employeeType
    - 员工类型的 LDAP 属性。
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - 传真电话号码的 LDAP 属性。
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - 邮政信箱的 LDAP 属性。
    - ``postOfficeBox``
  * - ldap.attr.initials
    - 姓名首字母的 LDAP 属性。
    - ``initials``
  * - ldap.attr.carLicense
    - 车牌的 LDAP 属性。
    - ``carLicense``
  * - ldap.attr.mobile
    - 手机的 LDAP 属性。
    - ``mobile``
  * - ldap.attr.postalAddress
    - 邮寄地址的 LDAP 属性。
    - ``postalAddress``
  * - ldap.attr.city
    - 城市的 LDAP 属性。
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - Teletex 终端标识符的 LDAP 属性。
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - X.121 地址的 LDAP 属性。
    - ``x121Address``
  * - ldap.attr.businessCategory
    - 业务类别的 LDAP 属性。
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - 注册地址的 LDAP 属性。
    - ``registeredAddress``
  * - ldap.attr.displayName
    - 显示名称的 LDAP 属性。
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - 首选语言的 LDAP 属性。
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - 部门编号的 LDAP 属性。
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - UID 编号的 LDAP 属性。
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - GID 编号的 LDAP 属性。
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - 主目录的 LDAP 属性。
    - ``homeDirectory``
  * - plugin.repositories
    - 插件仓库的 URL。
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - 插件的版本过滤器。
    - (empty)
  * - storage.max.items.in.page
    - 存储中每页的最大项目数。
    - ``1000``
  * - password.invalid.admin.passwords
    - 无效管理员密码的列表。
    - ``admin``
  * - password.min.length
    - 最小密码长度（0 表示禁用）。
    - ``8``
  * - password.max.length
    - 密码字段的最大长度。
    - ``100``
  * - password.require.uppercase
    - 密码中要求包含大写字母。
    - ``false``
  * - password.require.lowercase
    - 密码中要求包含小写字母。
    - ``false``
  * - password.require.digit
    - 密码中要求包含数字。
    - ``false``
  * - password.require.special.char
    - 密码中要求包含特殊字符。
    - ``false``
  * - rag.chat.enabled
    - 是否启用 RAG 聊天功能。
    - ``false``
  * - rag.chat.log.enabled
    - 是否在聊天日志中记录每个 RAG 聊天请求的使用情况（用户、时间、LLM 调用次数和 token 数）。绝不会记录问题和答案。
    - ``true``
  * - rag.chat.context.max.documents
    - 聊天生成设置。
    - ``5``
  * - rag.chat.query.regeneration.max.count
    - 当搜索未找到任何文档，或在流式聊天中没有任何命中结果被判定为相关时，一个聊天请求重新生成其搜索查询并再次搜索的最大次数。每次重新生成会产生一次 LLM 调用，如果新的搜索有命中结果，还会额外产生一次相关性评估调用（0 表示禁用）。
    - ``2``
  * - rag.chat.session.timeout.minutes
    - 会话设置。
    - ``30``
  * - rag.chat.session.max.size
    - 缓存的聊天会话的最大数量；超过该数量时，最近最少访问的会话会被逐出（0 或更小的值表示 100）。
    - ``10000``
  * - rag.chat.history.max.messages
    - 一个聊天会话中保留的最大消息数；每收到新消息时，较早的轮次会被裁剪。
    - ``30``
  * - rag.chat.content.fields
    - 增强 RAG 流程设置。用于检索完整文档内容的字段。
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - RAG 搜索的高亮设置。
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - RAG 聊天上下文搜索中每个文档的高亮片段数。
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - 回答生成时对大型文档的处理。content_length 超过该值的文档，在回答上下文中使用高亮段落而不是完整内容。
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - 从大型文档中提取段落作为回答上下文时使用的高亮设置。
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - 从每个超大文档中获取并用于回答上下文的高亮片段数。
    - ``5``
  * - rag.chat.history.assistant.content
    - 助手消息的历史内容模式。smart_summary - 丢弃助手正文，每轮仅保留过去的搜索查询和参照标题（默认，推荐） full - 发送完整的助手响应 source_titles - 正文加参照标题后缀 source_titles_and_urls - 仅 "[References: title (url), ...]" truncated - 在 history.assistant.max.chars 处截断助手响应 none - 从历史中丢弃助手轮次
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - smart_summary 历史模式下每轮包含的参照文档标题的最大数量。
    - ``5``
  * - rag.chat.document.max.parts
    - 针对长于 LLM 上下文预算的单个文档进行聊天时，将该文档拆分成的最大部分数。每个部分会分别生成摘要，这些摘要会被合并为回答；超出该数量的部分不会被使用。针对此类文档的请求，每一轮最多产生这么多次 LLM 调用，外加一次用于生成回答的调用。
    - ``10``
  * - rag.chat.response.language
    - 要求 LLM 使用的回答语言。browser - 用户浏览器或 UI 区域设置的语言；英语时不添加指示（默认） none - 不添加语言指示；LLM 通常使用问题所用的语言回答 en, ja.. - 始终使用该语言回答
    - ``browser``
  * - index.export.path
    - 索引导出
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - 索引导出作业写入的文件中省略的文档字段（逗号分隔）。
    - ``cache,tag``
  * - index.export.scroll.size
    - 索引导出作业每次滚动请求获取的文档数。
    - ``100``
  * - index.export.format
    - 导出文档的输出格式；仅接受 html 和 json，其他任何值都会导致作业失败。
    - ``html``
  * - log.notification.flush.interval
    - 日志通知 将日志通知缓冲区刷新到搜索引擎的间隔（秒）。
    - ``30``
  * - log.notification.max.details.length
    - 通知详情文本的最大长度。
    - ``3000``
  * - log.notification.max.display.events
    - 通知中显示的事件的最大数量。
    - ``50``
  * - log.notification.max.message.length
    - 通知中每条日志消息的最大长度。
    - ``200``
  * - log.notification.search.size
    - 每个通知作业从搜索引擎获取的事件的最大数量。
    - ``1000``
  * - log.notification.buffer.size
    - 内存中缓冲的事件的最大数量。
    - ``1000``
  * - log.notification.interval
    - 通知作业周期的间隔（秒），用于通知消息中。
    - ``300``
  * - theme.directory.path
    - 静态主题系统（参见 docs/superpowers/specs/2026-05-21-fess-static-theme-design.md）
    - ``themes``
  * - theme.upload.max.size
    - 上传的主题归档文件的最大大小（字节）。
    - ``52428800``
  * - theme.upload.max.extracted.size
    - 解压后的最大总大小（字节）；一旦超出，解压即中止。
    - ``209715200``
  * - theme.upload.max.entries
    - 上传的主题归档文件中允许的最大条目数。
    - ``1000``
  * - theme.upload.max.compression.ratio
    - 单个主题归档条目的最大解压/压缩比。
    - ``100``
  * - theme.upload.zip.ratio.max
    - 整个归档的最大累计解压/压缩比（zip 炸弹防护）。
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - 应用累计 zip 压缩比检查之前读取的压缩字节数；更小的归档会跳过该检查。
    - ``65536``
  * - theme.upload.attic.retention.days
    - 被替换的主题目录在清理扫描将其删除之前的保留时间（天）。
    - ``7``
  * - theme.repositories
    - 下载静态主题的仓库 URL（逗号分隔）。
    - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
  * - theme.index.frame.ancestors
    - 静态主题的 HTML 页面的 Content-Security-Policy 中 frame-ancestors 指令的值：允许将这些页面嵌入框架的来源。默认值 'none' 表示任何页面都不能嵌入它们。WebKit（Safari）会将 frame-ancestors 应用于主题的文件预览和缓存视图所使用的 blob: 框架，因此当该值为 'none' 时，它会将这些框架显示为空白。将该值留空可去掉该指令；无论哪种情况都会发送 X-Frame-Options: DENY，并使这些页面在所有浏览器中都无法出现在框架内（遵循 frame-ancestors 的浏览器会忽略该头）。
    - ``'none'``
  * - theme.api.csrf.server.origins
    - 可选：此 Fess 实例的规范外部来源（逗号/换行分隔），例如 https://fess.example.com。设置后，这些来源在 v2 CSRF Origin 检查中被视为同源，且不会信任转发头。建议用于未列在 rate.limit.trusted.proxies 中的反向代理之后。为空时，目标来源将先根据受信任代理的 X-Forwarded-\* 头重建，然后再根据 Servlet 请求重建。
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - 每个客户端 IP 每分钟允许的登录尝试次数；0 或更小的值表示禁用该限制。
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - 每个客户端 IP 和用户名组合每分钟允许的登录尝试次数；同时也限制密码修改。
    - ``5``
  * - theme.api.login.lockout.seconds
    - 超过登录速率限制后实施的锁定时间（秒）；0 或更小的值表示禁用锁定。
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - 内存中保留的登录速率限制桶的最大数量；达到上限时，空闲的桶会被逐出。
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - /api/v2/chat/stream 发出的 SSE keep-alive ping 的间隔。该 ping 是仅含注释的一行（": keepalive\\n\\n"），不会影响事件流，但能够规避在长时间的 LLM 阶段断开空闲连接的中间设备（nginx 默认的 proxy_read_timeout 为 60s）。设置为 <=0 表示禁用。单位：毫秒。
    - ``15000``
.. GENERATED-END: properties
