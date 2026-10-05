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

コア
----

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - ログと表示に使用するドメインのタイトル。
    - ``Fess``

.. list-table:: 検索エンジン
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - 検索エンジンバックエンドの種類（例: default、opensearch）。
    - ``default``
  * - search_engine.http.url
    - 検索エンジンのHTTPエンドポイントのURL。IPv6環境では、IPv6アドレスを角括弧で囲みます（例: http://[::1]:9200）。
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - セキュアなHTTP接続に使用するSSL認証局へのパス。
    - (empty)
  * - search_engine.username
    - 検索エンジンへの認証に使用するユーザー名。
    - (empty)
  * - search_engine.password
    - 検索エンジンへの認証に使用するパスワード。
    - (empty)
  * - search_engine.heartbeat_interval
    - 検索エンジンへのハートビートチェックの間隔（ミリ秒）。
    - ``10000``
  * - app.cipher.algorithm
    - 暗号化に使用する暗号アルゴリズム。
    - ``aes``
  * - app.cipher.key
    - 暗号化用の秘密鍵（本番環境ではこの値を変更してください）。
    - ``___change__me___``
  * - app.digest.algorithm
    - ダイジェスト計算のアルゴリズム。
    - ``sha256``
  * - app.password.algorithm
    - パスワードのハッシュ化（新しい仕組み、Spring Security v5.8互換）。サポート: bcrypt（現時点ではbcryptのみ）。
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - BCryptのコスト（ログラウンド数）。10はSpring Security v5.8のデフォルトと一致します。範囲: 4-31。
    - ``10``
  * - app.password.upgrade.enabled
    - レガシーなハッシュに対する、ログイン成功時の遅延再ハッシュ。
    - ``true``
  * - app.encrypt.property.pattern
    - 注意: app.digest.algorithmはレガシーパスワードの検証専用に残されています（{id}プレフィックスを持たない、アップグレード前のハッシュ）。新しいパスワードには使用しないでください。暗号化するプロパティの正規表現パターン。
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - デバッグログでマスクする機密値の正規表現パターン（プロパティ/環境変数のキーに対する大文字小文字を区別しないマッチ）。
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - アプリケーションのカスタマイズ用の拡張名。
    - (empty)
  * - app.audit.log.format
    - 監査ログの形式。
    - (empty)
  * - script.audit.log.enabled
    - スクリプト監査ログの設定。
    - ``true``
  * - script.audit.log.max.length
    - スクリプト監査ログの1エントリに保持するスクリプトテキストの最大文字数。これより長いテキストは切り詰められます。
    - ``100``
  * - jvm.crawler.options
    - クローラープロセスのJVMオプション。
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
    - サジェスト作成の子プロセスに渡すJVMオプション（改行区切り）。
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
    - チャンクベクトルインデクサープロセスのJVMオプション。ヒープの予算。この子JVMは"Content Chunk Vector Indexer"ジョブの実行中にのみ起動されるため、コンテンツのチャンク化が無効の場合は、-Xmxを大きく設定してもコストはかかりません。使用中のメモリは処理中のバッチが大半を占め、各バッチはドキュメントごとに、_source全体、ドキュメントのチャンク文字列、ドキュメントの埋め込みベクトルを保持します: content_chunker.job.bulk_size（デフォルト 20）x content_chunker.max_chunks_per_document（デフォルト 1000）x content_chunker.embedding.dimension（デフォルト 768）x floatあたり4バイト x content_chunker.job.concurrency（デフォルト 2）= ベクトルだけで約117MB（チャンク文字列とドキュメントのソースを除く）。同梱のデフォルト値では最悪の場合の使用量は約190-250MBで（dimension=1536ではベクトルだけで約235MB）、GCの余裕を考慮すると256MBのヒープには収まりません。bulk_size、max_chunks_per_document、concurrency、または埋め込みの次元を増やす場合は、-Xmxをさらに大きくしてください。
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
    - サムネイルプロセスのJVMオプション。
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

.. list-table:: ジョブ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - スケジュールされたジョブのシステムジョブID。
    - ``default_crawler``
  * - job.template.title.web
    - Webクローラージョブのタイトルのテンプレート。
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - ファイルクローラージョブのタイトルのテンプレート。
    - ``File Crawler - {0}``
  * - job.template.title.data
    - データクローラージョブのタイトルのテンプレート。
    - ``Data Crawler - {0}``
  * - job.template.script
    - ジョブ実行用のスクリプトテンプレート。
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - クローラープロセスの最大数。
    - ``0``
  * - job.default.script
    - ジョブのデフォルトのスクリプト言語。
    - ``javascript``
  * - job.system.property.filter.pattern
    - ジョブ用のシステムプロパティを絞り込むパターン。
    - (empty)
  * - processors
    - 使用するプロセッサー数。
    - ``0``
  * - java.command.path
    - Javaコマンドのパス。
    - ``java``
  * - python.command.path
    - Pythonコマンドのパス。
    - ``python``
  * - path.encoding
    - ファイルパスのエンコーディング。
    - ``UTF-8``
  * - use.own.tmp.dir
    - 専用の一時ディレクトリを使用するかどうか。
    - ``true``
  * - max.log.output.length
    - ログ出力の最大長。
    - ``4000``
  * - adaptive.load.control
    - 適応型負荷制御の値。
    - ``50``
  * - web.load.control
    - Webリクエストの負荷制御におけるCPUの閾値（%）。CPUがこの値以上の場合は429を返します。（100: 無効）
    - ``100``
  * - api.load.control
    - APIリクエストの負荷制御におけるCPUの閾値（%）。CPUがこの値以上の場合は429を返します。（100: 無効）
    - ``100``
  * - load.control.monitor.interval
    - OpenSearchのCPU負荷を監視する間隔（秒）。
    - ``1``
  * - supported.languages
    - サポートする言語。
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - APIアクセストークンの長さ。
    - ``60``
  * - api.access.token.request.parameter
    - APIアクセストークンのリクエストパラメーター。
    - (empty)
  * - api.admin.access.permissions
    - API管理アクセスのパーミッション。
    - ``Radmin-api``
  * - api.search.accept.referers
    - API検索で受け付けるリファラー。
    - (empty)
  * - api.search.scroll
    - API検索でスクロールを有効にするかどうか。
    - ``false``
  * - api.search.export
    - /api/v2/documents/exportでの検索結果（CSV/JSON）のエンドユーザーによるエクスポートを有効にするかどうか。
    - ``false``
  * - api.search.export.max.size
    - 1回の検索結果エクスポートで書き出すドキュメントの最大数。
    - ``1000``
  * - api.search.export.fields
    - 検索結果エクスポートで書き出すフィールド（カンマ区切り）。APIレスポンスのフィールドではないフィールドは無視されます。
    - ``title,url_link,last_modified,content_length,filetype``
  * - api.search.export.rate.limit.per.minute
    - ユーザーごと（ゲストの場合はクライアントIPごと）の、1分あたりの検索結果エクスポートの最大数。0以下の場合は制限を無効にします。
    - ``10``
  * - api.json.response.headers
    - API JSONレスポンスのヘッダー。Access-Control-\*とTiming-Allow-Originはここでは無視されます（CORSはapi.cors.\* / CorsFilterで制御されます）。Varyは設定しないでください。
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - API JSONレスポンスに例外を含めるかどうか。
    - ``false``
  * - api.gsa.response.headers
    - API GSAレスポンスのヘッダー。Access-Control-\*とTiming-Allow-Originはここでは無視されます（CORSはapi.cors.\* / CorsFilterで制御されます）。Varyは設定しないでください。
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - API GSAレスポンスに例外を含めるかどうか。
    - ``false``
  * - api.dashboard.response.headers
    - APIダッシュボードレスポンスのヘッダー。Access-Control-\*とTiming-Allow-Originはここでは無視されます（CORSはapi.cors.\* / CorsFilterで制御されます）。Varyは設定しないでください。
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - CORSで許可するオリジン。"\*"はリテラルの"\*"を返し（リクエストのOriginは反映されません）、認証情報を無効にします。認証情報付きのクロスオリジンアクセスを許可するには、明示的なオリジン（改行区切りまたはカンマ区切り）を設定してください。
    - ``*``
  * - api.cors.allow.methods
    - CORSで許可するHTTPメソッド。
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - CORSプリフライトリクエストの最大有効期間。
    - ``3600``
  * - api.cors.allow.headers
    - CORSプリフライトで許可するリクエストヘッダー。静的なリストが返されます（Access-Control-Request-Headersは反映されません）。CSRFトークンを送信するクロスオリジンのSPA向けに、X-Fess-CSRF-Tokenを含みます。
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - CORSで認証情報を許可するかどうか。明示的なOriginと完全に一致する場合にのみ有効で、api.cors.allow.originが"\*"の場合は無視されます。
    - ``true``
  * - api.jsonp.enabled
    - APIでJSONPを有効にするかどうか。
    - ``false``
  * - api.ping.search_engine.fields
    - 検索エンジンへのAPI pingに使用するフィールド。
    - ``status,timed_out``

レート制限
----------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - レート制限が有効かどうか。
    - ``false``
  * - rate.limit.requests.per.window
    - ウィンドウあたりに許可されるリクエストの最大数。
    - ``100``
  * - rate.limit.window.ms
    - ウィンドウサイズ（ミリ秒）。
    - ``60000``
  * - rate.limit.block.duration.ms
    - 制限を超えた場合にIPをブロックする期間（ミリ秒）。
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Retry-Afterヘッダーの値（秒）。
    - ``60``
  * - rate.limit.whitelist.ips
    - ホワイトリストに登録するIPのカンマ区切りリスト（例: 127.0.0.1,::1）。
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - ブロックするIPのカンマ区切りリスト。
    - (empty)
  * - rate.limit.trusted.proxies
    - 信頼するプロキシIPのカンマ区切りリスト。これらのIPからのX-Forwarded-For/X-Real-IPのみを信頼します。
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - メモリリークを防ぐための、クリーンアップ操作の間のリクエスト数。
    - ``1000``
  * - virtual.host.headers
    - 仮想ホスト: Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - HTTPプロキシサーバーのホスト名。
    - (empty)
  * - http.proxy.port
    - HTTPプロキシサーバーのポート番号（例: 8080）。
    - ``8080``
  * - http.proxy.username
    - HTTPプロキシ認証のユーザー名。
    - (empty)
  * - http.proxy.password
    - HTTPプロキシ認証のパスワード。
    - (empty)
  * - http.fileupload.max.size
    - HTTPファイルアップロードの最大サイズ（バイト）。
    - ``262144000``
  * - http.fileupload.threshold.size
    - HTTPファイルアップロードのバッファリングの閾値サイズ（バイト）。
    - ``262144``
  * - http.fileupload.max.file.count
    - 1回のHTTPアップロードで許可されるファイルの最大数。
    - ``10``

インデックス
------------

.. list-table:: クローラー共通
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - HTTPクロールのスレッド数。
    - ``0``
  * - crawler.data.serializer
    - クローラーデータのシリアライザーの種類（例: kryo）。
    - ``kryo``
  * - crawler.document.max.site.length
    - ドキュメント内のサイト名の最大長。
    - ``100``
  * - crawler.document.site.encoding
    - ドキュメント内のサイト名のエンコーディング。
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - ドキュメントでホスト名が不明な場合に使用するホスト名。
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - 英語のドキュメントでサイトのエンコーディングを使用するかどうか。
    - ``false``
  * - crawler.document.append.data
    - ドキュメントにデータを追加するかどうか。
    - ``true``
  * - crawler.document.append.filename
    - ドキュメントにファイル名を追加するかどうか。
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - ドキュメント内の英数字単語の最大サイズ。
    - ``20``
  * - crawler.document.max.symbol.term.size
    - ドキュメント内の記号単語の最大サイズ。
    - ``10``
  * - crawler.document.duplicate.term.removed
    - ドキュメント内の重複した単語を削除するかどうか。
    - ``false``
  * - crawler.document.space.chars
    - ドキュメントの解析に使用するUnicodeの空白文字。
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - ドキュメントの解析に使用するUnicodeの句点文字。
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - クロールデータのエンコーディング。
    - ``UTF-8``
  * - crawler.web.protocols
    - クロールでサポートするWebプロトコル。
    - ``http,https``
  * - crawler.file.protocols
    - クロールでサポートするファイルプロトコル。
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - クロールデータ内の環境変数キーのパターン。
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - クロール時にrobots.txtを無視するかどうか。
    - ``false``
  * - crawler.ignore.robots.tags
    - クロール時にrobotsメタタグを無視するかどうか。
    - ``false``
  * - crawler.ignore.content.exception
    - クロール時にコンテンツ例外を無視するかどうか。
    - ``true``
  * - crawler.failure.url.status.codes
    - 障害URLとみなすHTTPステータスコード。
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - クロール中のシステム監視の間隔（秒）。
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - ホットスレッド監視でアイドルスレッドを無視するかどうか。
    - ``true``
  * - crawler.hotthread.interval
    - ホットスレッド監視の間隔（例: 500ms）。
    - ``500ms``
  * - crawler.hotthread.snapshots
    - ホットスレッド監視のスナップショット数。
    - ``10``
  * - crawler.hotthread.threads
    - ホットスレッド監視のスレッド数。
    - ``3``
  * - crawler.hotthread.timeout
    - ホットスレッド監視のタイムアウト（例: 30s）。
    - ``30s``
  * - crawler.hotthread.type
    - ホットスレッド監視の種類（例: cpu）。
    - ``cpu``
  * - crawler.metadata.content.excludes
    - ドキュメントのコンテンツから除外するメタデータフィールド。
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - ドキュメントのメタデータ名のマッピング。
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``
      | ``frontmatter.title=title:string``

.. list-table:: クローラーHTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - HTMLドキュメントからメインコンテンツを抽出するXPath。
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - HTMLドキュメントから言語属性を抽出するXPath。
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - HTMLドキュメントからダイジェスト（説明）を抽出するXPath。
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - HTMLドキュメントからカノニカルURLを抽出するXPath。
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - ドキュメント処理中に削除（プルーニング）するHTMLタグ。
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - HTMLドキュメントから抽出するダイジェストの最大長。
    - ``120``
  * - crawler.document.html.default.lang
    - HTMLドキュメントのデフォルト言語。
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - HTMLのインデックス処理に含めるパターン。
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - HTMLのインデックス処理から除外するパターン。
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - HTMLの検索処理に含めるパターン。
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - HTMLの検索処理から除外するパターン。
    - (empty)

.. list-table:: クローラーファイル
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - ドキュメント内のファイル名のエンコーディング。
    - (empty)
  * - crawler.document.file.no.title.label
    - ファイルにタイトルがない場合に使用するラベル。
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - コンテンツが空のファイルを無視するかどうか。
    - ``false``
  * - crawler.document.file.max.title.length
    - ドキュメント内のファイルタイトルの最大長。
    - ``100``
  * - crawler.document.file.max.digest.length
    - ドキュメント内のファイルダイジェストの最大長。
    - ``200``
  * - crawler.document.file.append.meta.content
    - ファイルのメタコンテンツを追加するかどうか。
    - ``true``
  * - crawler.document.file.append.body.content
    - ファイルの本文コンテンツを追加するかどうか。
    - ``true``
  * - crawler.document.file.default.lang
    - ファイルドキュメントのデフォルト言語。
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - ファイルのインデックス処理に含めるパターン。
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - ファイルのインデックス処理から除外するパターン。
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - ファイルの検索処理に含めるパターン。
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - ファイルの検索処理から除外するパターン。
    - (empty)
  * - crawler.document.file.owner.enabled
    - クロールしたファイル（SMB、ローカルファイルシステム、FTP）の所有者をインデックスするかどうか。クロール設定のパラメーターconfig.owner.enabledで上書きされます。
    - ``true``
  * - crawler.document.file.last.modifier.enabled
    - クロールしたファイルの最終更新者をインデックスするかどうか。ドキュメントのメタデータから読み取り、取得できない場合はファイルの所有者にフォールバックします。クロール設定のパラメーターconfig.last.modifier.enabledで上書きされます。
    - ``true``

.. list-table:: クローラーキャッシュ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - ドキュメントキャッシュが有効かどうか。
    - ``true``
  * - crawler.document.cache.max.size
    - ドキュメントキャッシュの最大サイズ（バイト）。
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - ドキュメントキャッシュでサポートするMIMEタイプ。
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation HTMLドキュメントキャッシュのMIMEタイプ。
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - MIMEタイプ検出用の、拡張子からMIMEタイプへのオーバーライドマッピング（1行に1つ: .ext=mime/type）。
    - (empty)
  * - crawler.document.ocr.enabled
    - Tesseract OCRで画像やスキャンしたPDFからテキストを抽出するかどうか（tesseractコマンドが必要）。
    - ``false``
  * - crawler.document.ocr.language
    - '+'で連結したTesseract OCRの言語（例: jpn+eng）。
    - ``eng``
  * - crawler.document.ocr.timeout
    - Tesseract OCRの1回の実行のタイムアウト（秒）。
    - ``120``

.. list-table:: インデクサー
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - インデクサーでスレッドダンプを有効にするかどうか。
    - ``true``
  * - indexer.unprocessed.document.size
    - インデクサーの未処理ドキュメントの最大数。
    - ``1000``
  * - indexer.click.count.enabled
    - インデクサーでクリック数の追跡を有効にするかどうか。
    - ``true``
  * - indexer.favorite.count.enabled
    - インデクサーでお気に入り数の追跡を有効にするかどうか。
    - ``true``
  * - indexer.webfs.commit.margin.time
    - インデクサーのwebfsのコミットマージン時間（ミリ秒）。
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - インデクサーのwebfsの空リストの最大数。
    - ``3600``
  * - indexer.webfs.update.interval
    - インデクサーのwebfsの更新間隔（ミリ秒）。
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - インデクサーのwebfsの最大ドキュメントキャッシュサイズ。
    - ``10``
  * - indexer.webfs.max.document.request.size
    - インデクサーのwebfsの最大ドキュメントリクエストサイズ（バイト）。
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - インデクサーのデータの最大ドキュメントキャッシュサイズ。
    - ``10000``
  * - indexer.data.max.document.request.size
    - インデクサーのデータの最大ドキュメントリクエストサイズ（バイト）。
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - インデクサーのデータの最大削除キャッシュサイズ。
    - ``100``
  * - indexer.data.max.redirect.count
    - インデクサーのデータの最大リダイレクト回数。
    - ``10``
  * - indexer.language.fields
    - インデクサーの言語検出に使用するフィールド。
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - インデクサーの言語検出に使用するテキストの長さ。
    - ``1000``
  * - indexer.max.result.window.size
    - インデクサーの最大結果ウィンドウサイズ。
    - ``10000``
  * - indexer.max.search.doc.size
    - インデクサーの検索ドキュメントの最大数。
    - ``50000``

.. list-table:: インデックス設定
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - インデックスのコーデックの種類。
    - ``default``
  * - index.number_of_shards
    - インデックスのプライマリシャード数。
    - ``5``
  * - index.auto_expand_replicas
    - インデックスのレプリカ自動拡張の設定。
    - ``0-1``
  * - index.id.digest.algorithm
    - インデックスIDのダイジェストアルゴリズム。
    - ``SHA-512``
  * - index.user.initial_password
    - インデックスユーザーの初期パスワード。
    - ``admin``

.. list-table:: フィールド名
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - インデックス内のお気に入り数のフィールド名。
    - ``favorite_count``
  * - index.field.click_count
    - インデックス内のクリック数のフィールド名。
    - ``click_count``
  * - index.field.config_id
    - インデックス内の設定IDのフィールド名。
    - ``config_id``
  * - index.field.expires
    - インデックス内の有効期限のフィールド名。
    - ``expires``
  * - index.field.url
    - インデックス内のURLのフィールド名。
    - ``url``
  * - index.field.doc_id
    - インデックス内のドキュメントIDのフィールド名。
    - ``doc_id``
  * - index.field.id
    - インデックス内の内部IDのフィールド名。
    - ``_id``
  * - index.field.version
    - インデックス内のバージョンのフィールド名。
    - ``_version``
  * - index.field.seq_no
    - インデックス内のシーケンス番号のフィールド名。
    - ``_seq_no``
  * - index.field.primary_term
    - インデックス内のプライマリタームのフィールド名。
    - ``_primary_term``
  * - index.field.lang
    - インデックス内の言語のフィールド名。
    - ``lang``
  * - index.field.has_cache
    - インデックス内のキャッシュ状態のフィールド名。
    - ``has_cache``
  * - index.field.last_modified
    - インデックス内の最終更新日のフィールド名。
    - ``last_modified``
  * - index.field.etag
    - インデックス内の、クロールしたドキュメントのETagレスポンスヘッダーのフィールド名。
    - ``etag``
  * - index.field.owner
    - インデックス内の、クロールしたファイルの所有者のフィールド名。
    - ``owner``
  * - index.field.last_modifier
    - インデックス内の、クロールしたファイルの最終更新者のフィールド名。
    - ``last_modifier``
  * - index.field.anchor
    - インデックス内のアンカーのフィールド名。
    - ``anchor``
  * - index.field.segment
    - インデックス内のセグメントのフィールド名。
    - ``segment``
  * - index.field.role
    - インデックス内のロールのフィールド名。
    - ``role``
  * - index.field.boost
    - インデックス内のブースト値のフィールド名。
    - ``boost``
  * - index.field.created
    - インデックス内の作成日のフィールド名。
    - ``created``
  * - index.field.timestamp
    - インデックス内のタイムスタンプのフィールド名。
    - ``timestamp``
  * - index.field.label
    - インデックス内のラベルのフィールド名。
    - ``label``
  * - index.field.tag
    - インデックス内のドキュメントのユーザータグのフィールド名。
    - ``tag``
  * - index.field.mimetype
    - インデックス内のMIMEタイプのフィールド名。
    - ``mimetype``
  * - index.field.parent_id
    - インデックス内の親IDのフィールド名。
    - ``parent_id``
  * - index.field.important_content
    - インデックス内の重要なコンテンツのフィールド名。
    - ``important_content``
  * - index.field.content
    - インデックス内のコンテンツのフィールド名。
    - ``content``
  * - index.field.content_minhash_bits
    - インデックス内のコンテンツのminhashビットのフィールド名。
    - ``content_minhash_bits``
  * - index.field.cache
    - インデックス内のキャッシュのフィールド名。
    - ``cache``
  * - index.field.digest
    - インデックス内のダイジェストのフィールド名。
    - ``digest``
  * - index.field.title
    - インデックス内のタイトルのフィールド名。
    - ``title``
  * - index.field.host
    - インデックス内のホストのフィールド名。
    - ``host``
  * - index.field.site
    - インデックス内のサイトのフィールド名。
    - ``site``
  * - index.field.content_length
    - インデックス内のコンテンツ長のフィールド名。
    - ``content_length``
  * - index.field.filetype
    - インデックス内のファイルタイプのフィールド名。
    - ``filetype``
  * - index.field.filename
    - インデックス内のファイル名のフィールド名。
    - ``filename``
  * - index.field.thumbnail
    - インデックス内のサムネイルのフィールド名。
    - ``thumbnail``
  * - index.field.virtual_host
    - インデックス内の仮想ホストのフィールド名。
    - ``virtual_host``
  * - response.field.content_title
    - レスポンス内のコンテンツタイトルのフィールド名。
    - ``content_title``
  * - response.field.content_description
    - レスポンス内のコンテンツ説明のフィールド名。
    - ``content_description``
  * - response.field.url_link
    - レスポンス内のURLリンクのフィールド名。
    - ``url_link``
  * - response.field.site_path
    - レスポンス内のサイトパスのフィールド名。
    - ``site_path``
  * - response.max.title.length
    - レスポンス内のコンテンツタイトルの最大長。
    - ``50``
  * - response.max.site.path.length
    - レスポンス内のサイトパスの最大長。
    - ``100``
  * - response.highlight.content_title.enabled
    - レスポンスでコンテンツタイトルのハイライトを有効にするかどうか。
    - ``true``
  * - response.inline.mimetypes
    - レスポンスのインラインMIMEタイプ。
    - ``application/pdf,text/plain``
  * - response.headers
    - レスポンスのHTTPヘッダー。Access-Control-\*とTiming-Allow-Originは無視されます（CORSはapi.cors.\* / CorsFilterで制御されます）。ここでVaryは設定しないでください。
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=Content-Security-Policy: reflected-xss block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: ドキュメントインデックス
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - 検索ドキュメントのインデックス名。
    - ``fess.search``
  * - index.document.update.index
    - 更新ドキュメントのインデックス名。
    - ``fess.update``
  * - index.document.suggest.index
    - サジェストドキュメントのインデックス名。
    - ``fess``
  * - index.document.crawler.index
    - クローラードキュメントのインデックス名。
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - クローラーキューインデックスのプライマリシャード数。
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - クローラーデータインデックスのプライマリシャード数。
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - クローラーフィルターインデックスのプライマリシャード数。
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - クローラーキューインデックスのレプリカ数。
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - クローラーデータインデックスのレプリカ数。
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - クローラーフィルターインデックスのレプリカ数。
    - ``1``
  * - index.config.index
    - 設定データのインデックス名。
    - ``fess_config``
  * - index.user.index
    - ユーザーデータのインデックス名。
    - ``fess_user``
  * - index.log.index
    - ログデータのインデックス名。
    - ``fess_log``
  * - index.dictionary.prefix
    - 辞書インデックス名のプレフィックス。
    - (empty)

.. list-table:: ドキュメント管理
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - インデックス内の管理用の配列型フィールド。
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - インデックス内の管理用の日付型フィールド。
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - インデックス内の管理用の整数型フィールド。
    - (empty)
  * - index.admin.long.fields
    - インデックス内の管理用のlong型フィールド。
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - インデックス内の管理用のfloat型フィールド。
    - ``boost``
  * - index.admin.double.fields
    - インデックス内の管理用のdouble型フィールド。
    - (empty)
  * - index.admin.required.fields
    - インデックス内の管理用の必須フィールド。
    - ``url,title,role,boost``

.. list-table:: タイムアウト
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - インデックス検索操作のタイムアウト。
    - ``3m``
  * - index.scroll.search.timeout
    - スクロール検索操作のタイムアウト。
    - ``3m``
  * - index.index.timeout
    - インデックス操作のタイムアウト。
    - ``3m``
  * - index.bulk.timeout
    - バルクインデックス操作のタイムアウト。
    - ``3m``
  * - index.delete.timeout
    - インデックス内の削除操作のタイムアウト。
    - ``3m``
  * - index.health.timeout
    - インデックスのヘルスチェックのタイムアウト。
    - ``10m``
  * - index.indices.timeout
    - インデックスのindices操作のタイムアウト。
    - ``1m``

.. list-table:: ファイルタイプ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - インデックス作成用の、MIMEタイプからファイルタイプラベルへのマッピング。
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
    - 1回の再インデックス操作で処理するドキュメント数。
    - ``100``
  * - index.reindex.body
    - 再インデックス操作のリクエストボディのテンプレート。
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - 再インデックス操作の1秒あたりのリクエスト数（自動の場合は"adaptive"）。
    - ``adaptive``
  * - index.reindex.refresh
    - 再インデックス後にインデックスをリフレッシュするかどうか。
    - ``false``
  * - index.reindex.timeout
    - 再インデックス操作のタイムアウト。
    - ``1m``
  * - index.reindex.scroll
    - 再インデックス操作のスクロールタイムアウト。
    - ``5m``
  * - index.reindex.max_docs
    - 再インデックス操作のドキュメントの最大数。
    - (empty)

.. list-table:: クエリ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - 検索クエリの最大長。
    - ``1000``
  * - query.timeout
    - 検索クエリのタイムアウト（ミリ秒）。
    - ``10000``
  * - query.timeout.logging
    - クエリのタイムアウトやシャードの障害により結果が不完全になった検索をログに記録するかどうか。
    - ``true``
  * - query.track.total.hits
    - クエリで追跡する総ヒット数の最大値。サポートされるのは正の数またはtrueのみです。falseを指定するとレスポンスにヒット数が含まれなくなり、ヒット数を要求する検索（ここでの設定または検索パラメーターのいずれによる場合も）は拒否されます。
    - ``10000``
  * - query.geo.fields
    - 位置情報検索クエリで使用するフィールド。
    - ``location``
  * - query.browser.lang.parameter.name
    - クエリでのブラウザーの言語のパラメーター名。
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - 単語をプレフィックスクエリに置き換えるかどうか。
    - ``true``
  * - query.orsearch.min.hit.count
    - OR検索クエリの最小ヒット数。
    - ``-1``
  * - query.highlight.terminal.chars
    - クエリのハイライトに使用するUnicodeの終端文字。
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - クエリのハイライトのフラグメントサイズ。
    - ``60``
  * - query.highlight.number.of.fragments
    - クエリのハイライトのフラグメント数。
    - ``2``
  * - query.highlight.type
    - クエリのハイライトの種類。
    - ``fvh``
  * - query.highlight.tag.pre
    - ハイライトされたテキストの前に使用するタグ。
    - ``<strong>``
  * - query.highlight.tag.post
    - ハイライトされたテキストの後に使用するタグ。
    - ``</strong>``
  * - query.highlight.boundary.chars
    - クエリのハイライトの境界文字。
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - クエリのハイライト境界の最大スキャン。
    - ``20``
  * - query.highlight.boundary.scanner
    - クエリのハイライト境界のスキャナーの種類。
    - ``chars``
  * - query.highlight.encoder
    - クエリのハイライトのエンコーダーの種類。
    - ``default``
  * - query.highlight.force.source
    - クエリのハイライトでソースを強制するかどうか。
    - ``false``
  * - query.highlight.fragmenter
    - クエリのハイライトのフラグメンターの種類。
    - ``span``
  * - query.highlight.fragment.offset
    - クエリのハイライトフラグメントのオフセット。
    - ``-1``
  * - query.highlight.no.match.size
    - 一致しない場合のクエリのハイライトのサイズ。
    - ``0``
  * - query.highlight.order
    - クエリのハイライトフラグメントの順序。
    - ``score``
  * - query.highlight.phrase.limit
    - クエリのハイライトのフレーズ上限。
    - ``256``
  * - query.highlight.content.description.fields
    - クエリのハイライトでコンテンツ説明に使用するフィールド。
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - クエリのハイライトで境界位置を検出するかどうか。
    - ``true``
  * - query.highlight.text.fragment.type
    - クエリのハイライトのテキストフラグメントの種類。
    - ``query``
  * - query.highlight.text.fragment.size
    - クエリのハイライトのテキストフラグメントのサイズ。
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - クエリのハイライトのテキストフラグメントのプレフィックス長。
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - クエリのハイライトのテキストフラグメントのサフィックス長。
    - ``5``
  * - query.max.search.result.offset
    - クエリの検索結果オフセットの最大値。
    - ``100000``
  * - query.additional.default.fields
    - クエリの追加のデフォルトフィールド。
    - (empty)
  * - query.additional.response.fields
    - 検索結果のためにインデックスから取得する追加フィールド。ここに追加したフィールドは、query.additional.api.response.fieldsにも記載されている場合にのみ、検索APIが返します。
    - (empty)
  * - query.additional.api.response.fields
    - クエリの追加のAPIレスポンスフィールド。このキーはv2 APIレスポンスの許可リストにフィールドを追加するだけ（追加のみ）で、フィールドを取得しません。フィールドは取得もされる必要があります。検索APIの場合はquery.additional.response.fieldsに、スクロールAPIの場合はquery.additional.scroll.response.fieldsに追加してください。ACLフィールドや内部フィールド（例: role、virtual_host）は追加しないでください。追加すると、検索APIのレスポンスにアクセス制御情報が公開されます。
    - (empty)
  * - query.additional.scroll.response.fields
    - スクロール検索結果のためにインデックスから取得する追加フィールド。ここに追加したフィールドは、query.additional.api.response.fieldsにも記載されている場合にのみ、スクロールAPIが返します。
    - (empty)
  * - query.additional.cache.response.fields
    - クエリの追加のキャッシュレスポンスフィールド。
    - (empty)
  * - query.additional.highlighted.fields
    - クエリの追加のハイライトフィールド。
    - (empty)
  * - query.additional.search.fields
    - クエリの追加の検索フィールド。
    - (empty)
  * - query.additional.facet.fields
    - クエリの追加のファセットフィールド。
    - (empty)
  * - query.additional.sort.fields
    - クエリの追加のソートフィールド。
    - (empty)
  * - query.additional.analyzed.fields
    - クエリの追加の解析対象フィールド。
    - (empty)
  * - query.additional.not.analyzed.fields
    - クエリの追加の解析対象外フィールド。
    - (empty)
  * - query.gsa.response.fields
    - クエリのGSAレスポンスのフィールド。
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - GSAクエリのデフォルト言語。
    - ``en``
  * - query.gsa.default.sort
    - GSAクエリのデフォルトのソート。
    - (empty)
  * - query.gsa.meta.prefix
    - GSAクエリのメタプレフィックス。
    - ``MT_``
  * - query.gsa.index.field.charset
    - GSAインデックスクエリの文字セットフィールド。
    - ``charset``
  * - query.gsa.index.field.content_type.
    - GSAインデックスクエリのコンテンツタイプフィールド。
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - 折りたたみクエリの最大同時グループ結果数。
    - ``4``
  * - query.collapse.inner.hits.name
    - 折りたたみクエリのinner hits名。
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - 折りたたみクエリのinner hitsのサイズ。
    - ``0``
  * - query.collapse.inner.hits.sorts
    - 折りたたみクエリのinner hitsのソート。
    - (empty)
  * - query.default.languages
    - クエリのデフォルト言語。
    - (empty)
  * - query.json.default.preference
    - JSONクエリのデフォルトのpreference。
    - ``_query``
  * - query.gsa.default.preference
    - GSAクエリのデフォルトのpreference。
    - ``_query``
  * - query.language.mapping
    - クエリの言語マッピング。
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

.. list-table:: ブースト
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - クエリのタイトルフィールドのブースト値。
    - ``0.5``
  * - query.boost.title.lang
    - クエリの言語付きタイトルフィールドのブースト値。
    - ``1.0``
  * - query.boost.content
    - クエリのコンテンツフィールドのブースト値。
    - ``0.05``
  * - query.boost.content.lang
    - クエリの言語付きコンテンツフィールドのブースト値。
    - ``0.1``
  * - query.boost.important_content
    - クエリの重要なコンテンツフィールドのブースト値。
    - ``-1.0``
  * - query.boost.important_content.lang
    - クエリの言語付きの重要なコンテンツフィールドのブースト値。
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - クエリのファジーブーストの最小長。
    - ``4``
  * - query.boost.fuzzy.title
    - ファジータイトルクエリのブースト値。
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - ファジータイトルクエリのファジネス。
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - ファジータイトルクエリの展開数。
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - ファジータイトルクエリのプレフィックス長。
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - ファジータイトルクエリで転置を許可するかどうか。
    - ``true``
  * - query.boost.fuzzy.content
    - ファジーコンテンツクエリのブースト値。
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - ファジーコンテンツクエリのファジネス。
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - ファジーコンテンツクエリの展開数。
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - ファジーコンテンツクエリのプレフィックス長。
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - ファジーコンテンツクエリで転置を許可するかどうか。
    - ``true``
  * - query.default.query_type
    - デフォルトのクエリタイプ。
    - ``bool``
  * - query.dismax.tie_breaker
    - dismaxクエリのタイブレーカー値。
    - ``0.1``
  * - query.bool.minimum_should_match
    - ブールクエリのminimum should matchの値。
    - (empty)
  * - query.prefix.expansions
    - プレフィックスクエリの展開数。
    - ``50``
  * - query.prefix.slop
    - プレフィックスクエリのスロップ値。
    - ``0``
  * - query.fuzzy.prefix_length
    - ファジークエリのプレフィックス長。
    - ``0``
  * - query.fuzzy.expansions
    - ファジークエリの展開数。
    - ``50``
  * - query.fuzzy.transpositions
    - ファジークエリで転置を許可するかどうか。
    - ``true``

.. list-table:: ファセット
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - ファセットクエリのフィールド。
    - ``label``
  * - query.facet.fields.size
    - ファセットフィールドのサイズ。
    - ``100``
  * - query.facet.fields.size.max
    - facet.sizeの上限クランプ（検索のチョークポイントで適用されます）。
    - ``1000``
  * - query.facet.fields.min_doc_count
    - ファセットフィールドの最小ドキュメント数。
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - facet.minDocCountの上限クランプ（検索のチョークポイントで適用されます）。
    - ``2147483647``
  * - query.facet.fields.sort
    - ファセットフィールドのソート順。
    - ``count.desc``
  * - query.facet.fields.missing
    - 欠落したファセットフィールドの値。
    - (empty)
  * - query.facet.queries
    - ファセットクエリの定義。
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: ランキング
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - ランクフュージョンのウィンドウサイズ。
    - ``200``
  * - rank.fusion.rank_constant
    - ランクフュージョンのランク定数。
    - ``20``
  * - rank.fusion.threads
    - ランクフュージョンのスレッド数。
    - ``-1``
  * - rank.fusion.timeout
    - Fessが結果を自分で融合する場合（rank.fusion.engine.enabled=false）に、メイン以外のサーチャーを待機する最大時間（ミリ秒）。それまでに応答しなかったサーチャーはその検索から除外され、結果は部分的かつタイムアウトとしてマークされます。メインのサーチャーは常に待機されます。0以下の場合は制限なしで待機します。
    - ``10000``
  * - rank.fusion.score_field
    - ランクフュージョンのスコアフィールド。
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - 検索エンジンがランクフュージョンを行うかどうか。trueの場合、参加できるサーチャーが単一のリクエストにクエリを提供するため、ファセットと総ヒット数は融合後の結果セットを表します。falseの場合、Fessがサーチャーの結果を自分で融合します。
    - ``false``
  * - rank.fusion.combination.technique
    - 検索エンジンが融合したスコアを結合する方法: rrf、arithmetic_mean、geometric_mean、harmonic_meanのいずれか。
    - ``rrf``
  * - rank.fusion.normalization.technique
    - 結合前にスコアを正規化する方法: min_max、l2、z_scoreのいずれか。rrfでは無視されます。z_scoreはarithmetic_meanとのみ組み合わせられます。それ以外の平均との組み合わせは拒否され、Fessが結果を自分で融合します。
    - ``min_max``
  * - rank.fusion.combination.weights
    - 検索エンジン側の融合におけるサーチャーごとの重み。name:weightのペアで指定します（例: default:0.7,semantic_chunk:0.3）。重みの合計は1.0でなければならず、参加するすべてのサーチャーを指定する必要があります。空の場合は均等に重み付けします。
    - (empty)
  * - rank.fusion.pagination_depth
    - 各サーチャーが検索エンジン側の融合にシャードごとに提供する結果の件数。これは、クライアントがページングできる深さと、エンジンが順位付けするドキュメントの集合の両方を制限します。融合した検索はこの件数までページングでき、indexer.max.result.window.sizeを超えることはありません。
    - ``1000``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - ファイルからSMBのロールを取得するかどうか。
    - ``true``
  * - smb.available.sid.types
    - SMBで利用可能なSIDタイプ。
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - ファイルからファイルのロールを取得するかどうか。
    - ``true``
  * - ftp.role.from.file
    - ファイルからFTPのロールを取得するかどうか。
    - ``true``

.. list-table:: バックアップ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - インデックスバックアップの対象ファイル。
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - インデックスバックアップの対象ログファイル。
    - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - インデックスバックアップログの読み込みのタイムアウト。
    - ``60000``

.. list-table:: ログ出力
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - ログ出力のアプリケーションパッケージ。
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - 検索ドキュメントのログ出力を有効にするかどうか。
    - ``true``
  * - logging.search.docs.fields
    - 検索ドキュメントのログに出力するフィールド。
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - 検索ログの記録にログファイルを使用するかどうか。
    - ``true``
  * - logging.search.max.queue.size
    - 検索ログの記録の最大キューサイズ。
    - ``10000``
  * - logging.click.max.queue.size
    - クリックログの記録の最大キューサイズ。
    - ``10000``
  * - logging.chat.max.queue.size
    - チャット利用状況の記録の最大キューサイズ。
    - ``10000``
  * - search.history.enabled
    - ログイン中のユーザーの検索条件を検索履歴用に記録するかどうか。
    - ``true``
  * - search.history.size
    - ユーザーごとに返される検索履歴エントリの最大数。
    - ``10``
  * - user.tag.enabled
    - ログイン中のユーザーがドキュメントにタグを付けられるかどうか。各タグは作成したユーザーに属します。
    - ``false``
  * - user.tag.name.max.length
    - タグ名の最大長（コードポイント単位）。
    - ``50``
  * - user.tag.max.tags
    - 1人のユーザーが所有できるタグの最大数。
    - ``1000``
  * - user.tag.max.paths
    - 1つのタグを付けられるURLの最大数。
    - ``10000``
  * - user.tag.queue.max.size
    - ドキュメントに反映されるまでメモリ上に保持する、保留中のタグ変更の最大数。
    - ``10000``
  * - user.tag.process.batch.size
    - タグの変更をドキュメントに反映するときに、1回のバルクリクエストで更新するURLの数。
    - ``100``
  * - user.tag.visible.max.size
    - 検索で1人のユーザーに見えるタグの最大数。
    - ``1000``

Web
---

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - 管理フォームの最大入力サイズ。
    - ``10000``
  * - form.admin.label.in.config.enabled
    - 管理設定フォームでラベルを有効にするかどうか。
    - ``false``
  * - form.admin.default.template.name
    - 管理フォームのデフォルトのテンプレート名。
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - OSDDリンク（OpenSearch Description Document）を有効にするかどうか。
    - ``auto``
  * - clipboard.copy.icon.enabled
    - クリップボードへのコピーアイコンを有効にするかどうか。
    - ``true``
  * - authentication.admin.users
    - 認証用の管理者ユーザー名。
    - ``admin``
  * - authentication.admin.users.ignore.case
    - authentication.admin.usersを大文字小文字を区別せずに照合するかどうか: auto、true、falseのいずれか。autoはldap.provider.urlが設定されている場合に大文字小文字を区別しません。
    - ``auto``
  * - authentication.admin.roles
    - 認証用の管理者ロール名。
    - ``admin``
  * - role.search.default.permissions
    - 検索ロールのデフォルトのパーミッション。
    - (empty)
  * - role.search.default.display.permissions
    - 検索ロールのデフォルトの表示パーミッション。
    - ``{role}guest``
  * - role.search.guest.permissions
    - role.search.guest.permissionsは空にしないでください。これは、匿名の検索ロールセットを空にしないためのゲストロールの初期値になります。解決されたロールセットが空の場合、ロールフィルターはスキップされ（フェイルオープン）、ロールベースのアクセス制御が無効になり、ドキュメントが匿名ユーザーに公開される可能性があります。検索ロールのゲスト用パーミッション。
    - ``{role}guest``
  * - role.search.user.prefix
    - 検索におけるユーザーロールのプレフィックス。
    - ``1``
  * - role.search.group.prefix
    - 検索におけるグループロールのプレフィックス。
    - ``2``
  * - role.search.role.prefix
    - 検索におけるroleロールのプレフィックス。
    - ``R``
  * - role.search.denied.prefix
    - 検索における拒否ロールのプレフィックス。
    - ``D``
  * - cookie.default.path
    - Cookieのデフォルトのパス（コンテキストパスがない場合は基本的に'/'）。
    - ``/``
  * - cookie.default.expire
    - Cookieのデフォルトの有効期限（秒）。例: 31556926: 1年、86400: 1日。
    - ``3600``
  * - session.tracking.modes
    - セッション追跡モード
    - ``cookie``
  * - session.cookie.secure
    - 起動時にセッションCookie（JSESSIONID）にSecure属性を追加するかどうか。空欄（デフォルト）の場合はTomcatの自動動作が使用されます（SecureはHTTPSリクエストにのみ追加されます）。本番のHTTPSデプロイでは、特にTLSをリバースプロキシで終端している場合は、trueに設定してください。trueの場合、CookieはHTTPでは送信されないため、平文のHTTPではセッションが確立されません。localhostでの開発では空欄のままにしてください。SameSite=noneを使用する場合も、Secure属性が必要です。この値を変更するには再起動が必要です。
    - (empty)
  * - cookie.search.parameter.keys
    - SSOログイン前にCookieに保存するリクエストパラメーターキーのカンマ区切りリスト。
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - Cookieに保存するために存在している必要がある必須パラメーターキーのカンマ区切りリスト。
    - ``q``
  * - cookie.search.parameter.max.length
    - Cookieに保存するエンコード済み検索パラメーターの最大長。
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - 保存された検索パラメーターを展開できる最大サイズ（バイト）。上記の上限はgzip圧縮されたCookieに適用されますが、これは展開後のサイズを制限するものではなく、Cookieはクライアントから送られてきます。
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - ログイン後に保存した検索パラメーターを復元するときに組み立てるクエリ文字列の最大長。復元は利便性のためのものですがログインはそうではないため、これを超える場合は、コンテナが拒否するLocationヘッダーに書き込まれず、破棄されます。パーセントエンコードによりCJKのクエリは9倍になるため、この値はクエリ自体が取りうる長さよりはるかに小さくなります。レスポンスヘッダーを制限するtomcat_config.propertiesのtomcat.maxHttpHeaderSizeと合わせて引き上げてください。
    - ``4096``
  * - cookie.search.parameter.name
    - SSOログイン前にエンコード済み検索パラメーターを保存するために使用するCookie名。
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - 検索パラメーターCookieにHttpOnly属性を設定するかどうか。
    - ``true``
  * - cookie.search.parameter.secure
    - 検索パラメーターCookieにSecure属性を設定するかどうか。HTTPSを使用する本番環境ではtrueにしてください。
    - (empty)
  * - cookie.search.parameter.max_age
    - 検索パラメーターCookieのMax-Age（秒）。セッション限りのCookieにするには-1を使用します。
    - ``60``
  * - cookie.search.parameter.domain
    - 検索パラメーターCookieのDomain属性。Cookieを利用可能にしたいドメインの範囲を設定します（例: example.com）。
    - (empty)
  * - cookie.search.parameter.path
    - 検索パラメーターCookieのPath属性。通常は"/"またはアプリケーションのコンテキストパスを設定します。
    - ``/``
  * - cookie.search.parameter.same_site
    - 検索パラメーターCookieのSameSite属性。有効な値: Lax、Strict、None
    - ``Lax``
  * - paging.page.size
    - ページングの1ページのサイズ
    - ``25``
  * - paging.page.range.size
    - ページングのページ範囲のサイズ
    - ``5``
  * - paging.page.range.fill.limit
    - ページングのページ範囲のオプション'fillLimit'
    - ``true``

.. list-table:: 取得ページサイズ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - 1ページあたりに取得するドキュメントブーストレコードの最大数。
    - ``1000``
  * - page.keymatch.max.fetch.size
    - 1ページあたりに取得するキーマッチレコードの最大数。
    - ``1000``
  * - page.labeltype.max.fetch.size
    - 1ページあたりに取得するラベルタイプレコードの最大数。
    - ``1000``
  * - page.tagtype.max.fetch.size
    - 1ページあたりに取得するタグタイプレコードの最大数。
    - ``1000``
  * - page.roletype.max.fetch.size
    - 1ページあたりに取得するロールタイプレコードの最大数。
    - ``1000``
  * - page.user.max.fetch.size
    - 1ページあたりに取得するユーザーレコードの最大数。
    - ``1000``
  * - page.role.max.fetch.size
    - 1ページあたりに取得するロールレコードの最大数。
    - ``1000``
  * - page.group.max.fetch.size
    - 1ページあたりに取得するグループレコードの最大数。
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - 1ページあたりに取得するクロール情報パラメーターの最大数。
    - ``100``
  * - page.crawling.info.max.fetch.size
    - 1ページあたりに取得するクロール情報レコードの最大数。
    - ``1000``
  * - page.data.config.max.fetch.size
    - 1ページあたりに取得するデータストア設定レコードの最大数。
    - ``100``
  * - page.web.config.max.fetch.size
    - 1ページあたりに取得するウェブ設定レコードの最大数。
    - ``100``
  * - page.file.config.max.fetch.size
    - 1ページあたりに取得するファイルシステム設定レコードの最大数。
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - 1ページあたりに取得する重複ホストレコードの最大数。
    - ``1000``
  * - page.failure.url.max.fetch.size
    - 1ページあたりに取得する障害URLレコードの最大数。
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - 1ページあたりに取得するお気に入りログレコードの最大数。
    - ``100``
  * - page.file.auth.max.fetch.size
    - 1ページあたりに取得するファイル認証レコードの最大数。
    - ``100``
  * - page.web.auth.max.fetch.size
    - 1ページあたりに取得するウェブ認証レコードの最大数。
    - ``100``
  * - page.path.mapping.max.fetch.size
    - 1ページあたりに取得するパスマッピングレコードの最大数。
    - ``1000``
  * - page.request.header.max.fetch.size
    - 1ページあたりに取得するリクエストヘッダーレコードの最大数。
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - 1ページあたりに取得するスケジュールジョブレコードの最大数。
    - ``100``
  * - page.elevate.word.max.fetch.size
    - 1ページあたりに取得する追加ワードレコードの最大数。
    - ``1000``
  * - page.bad.word.max.fetch.size
    - 1ページあたりに取得する除外ワードレコードの最大数。
    - ``1000``
  * - page.dictionary.max.fetch.size
    - 1ページあたりに取得する辞書レコードの最大数。
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - 1ページあたりに取得する関連コンテンツレコードの最大数。
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - 1ページあたりに取得する関連クエリーレコードの最大数。
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - 1ページあたりに取得するサムネイルキューレコードの最大数。
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - 1ページあたりに取得するサムネイルパージレコードの最大数。
    - ``100``
  * - page.score.booster.max.fetch.size
    - 1ページあたりに取得するスコアブースターレコードの最大数。
    - ``1000``
  * - page.searchlog.max.fetch.size
    - 1ページあたりに取得する検索ログレコードの最大数。
    - ``10000``
  * - page.searchlist.track.total.hits
    - 検索リストページで総ヒット数を追跡するかどうか。
    - ``true``
  * - page.searchlist.content.max.length
    - 検索リスト編集ページに表示するコンテンツ長の最大値（文字数）。
    - ``100000``

.. list-table:: 検索ページ
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - 検索結果のデフォルトの開始ページ。
    - ``0``
  * - paging.search.page.size
    - 1ページあたりの検索結果のデフォルトサイズ。
    - ``10``
  * - paging.search.page.max.size
    - 1ページあたりの検索結果の最大サイズ。
    - ``100``
  * - api.param.max.length
    - v2 APIの文字列クエリパラメーター（q、sort、sdh）の最大長。OWASP API4:2023。
    - ``1000``
  * - api.param.max.array.size
    - v2 APIの繰り返し指定可能なクエリパラメーターの値の最大数。
    - ``100``
  * - api.click.max.timestamp
    - v2クリックAPIが受け付けるクリックログのタイムスタンプ（rt、エポックミリ秒）の最大値。OWASP API4:2023。
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - 検索ログ
    - ``-1``
  * - searchlog.request.headers
    - 検索ログに含めるリクエストヘッダー。
    - (empty)
  * - searchlog.process.batch_size
    - 検索ログ処理のバッチサイズ。
    - ``100``
  * - related_query.generate.days
    - 検索ログから関連クエリーを生成するときに読み込む検索ログの日数。
    - ``30``
  * - related_query.generate.term.size
    - 仮想ホストごとに生成される語の最大数。
    - ``100``
  * - related_query.generate.query.size
    - 1つの語ごとに生成される関連クエリーの最大数。
    - ``5``
  * - related_query.generate.min.sessions
    - 語とその各関連クエリーに必要な、異なるユーザーセッションの最小数。
    - ``3``
  * - related_query.generate.session.interval
    - 検索後、同じセッションの後続の検索を言い換えとみなす間隔（分）。
    - ``10``
  * - related_query.generate.seed.log.size
    - その語を検索したセッションを見つけるために読み込む、語の検索ログの最大数。
    - ``1000``
  * - related_query.generate.seed.session.size
    - 後続の検索を読み込む、語ごとのセッションの最大数。
    - ``200``
  * - related_query.generate.log.fetch.size
    - 語ごとに読み込む後続の検索ログの最大数。
    - ``2000``
  * - related_query.generate.query.min.length
    - 生成される語または関連クエリーの最小の長さ（文字数）。
    - ``2``
  * - related_query.generate.query.max.length
    - 生成される語または関連クエリーの最大の長さ（文字数）。
    - ``50``
  * - docreport.duplicate.group.size
    - docreport ドキュメントレポート画面に表示する重複グループの最大数（大きい順）。
    - ``100``
  * - docreport.duplicate.docs.size
    - ドキュメントレポート画面で重複グループごとに一覧表示するドキュメントの最大数。
    - ``10``
  * - docreport.duplicate.export.page.size
    - 重複レポートをCSVとしてダウンロードするときに、1回のリクエストで読み込むコンテンツ署名の数。
    - ``10000``
  * - docreport.dormant.days
    - ドキュメントを休眠とみなす、最終更新からの日数のデフォルト値。
    - ``365``
  * - thumbnail.html.image.min.width
    - サムネイルに使用するHTML画像の最小幅。
    - ``100``
  * - thumbnail.html.image.min.height
    - サムネイルに使用するHTML画像の最小高さ。
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - サムネイルに使用するHTML画像の最大アスペクト比。
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - 生成されるサムネイル画像の幅。
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - 生成されるサムネイル画像の高さ。
    - ``100``
  * - thumbnail.html.image.format
    - 生成されるサムネイル画像の形式。
    - ``png``
  * - thumbnail.html.image.xpath
    - サムネイル用の画像を選択するXPath。
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - サムネイル生成から除外するファイル拡張子。
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - サムネイルジェネレーターの間隔。
    - ``0``
  * - thumbnail.generator.targets
    - サムネイルジェネレーターの対象（例: all）。
    - ``all``
  * - thumbnail.crawler.enabled
    - サムネイルクローラーが有効かどうか。
    - ``true``
  * - thumbnail.system.monitor.interval
    - サムネイル処理におけるシステム監視の間隔。
    - ``60``

.. list-table:: ユーザー
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - ユーザーコードの設定
    - ``userCode``
  * - user.code.min.length
    - ユーザーコードの最小長。
    - ``20``
  * - user.code.max.length
    - ユーザーコードの最大長。
    - ``100``
  * - user.code.pattern
    - ユーザーコードの検証用パターン。
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - メールのFromフィールドに表示する名前。
    - ``Administrator``
  * - mail.from.address
    - Fromフィールドに使用するメールアドレス。
    - ``root@localhost``
  * - mail.hostname
    - メールサーバーのホスト名。
    - (empty)
  * - scheduler.target.name
    - スケジューラーのターゲット名。
    - (empty)
  * - scheduler.job.class
    - スケジューラーのジョブクラス。
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - スケジューラーの並行実行のモード。
    - ``QUIT``
  * - scheduler.monitor.interval
    - スケジューラー監視の間隔。
    - ``30``
  * - coordinator.poll.interval
    - ハートビートとイベントをポーリングする間隔（秒）。
    - ``60``
  * - coordinator.heartbeat.ttl
    - インスタンスのハートビートドキュメントの有効期間（ミリ秒）。
    - ``180000``
  * - coordinator.operation.ttl
    - 操作ロックドキュメントの有効期間（ミリ秒）。
    - ``7200000``
  * - coordinator.operation.retry
    - 操作ロックの取得の最大リトライ回数。
    - ``3``
  * - coordinator.event.ttl
    - イベント通知ドキュメントの有効期間（ミリ秒）。
    - ``600000``
  * - online.help.base.link
    - オンラインヘルプのベースリンク。
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - オンラインヘルプのインストールガイドのリンク。
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - オンラインヘルプのサポート終了情報のリンク。
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - 障害URLのオンラインヘルプキー。
    - ``failureurl``
  * - online.help.name.elevateword
    - 追加ワードのオンラインヘルプキー。
    - ``elevateword``
  * - online.help.name.reqheader
    - リクエストヘッダーのオンラインヘルプキー。
    - ``reqheader``
  * - online.help.name.dict.synonym
    - 同義語辞書のオンラインヘルプキー。
    - ``synonym``
  * - online.help.name.dict
    - 辞書のオンラインヘルプキー。
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Kuromoji辞書のオンラインヘルプキー。
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - Protwords辞書のオンラインヘルプキー。
    - ``protwords``
  * - online.help.name.dict.stopwords
    - ストップワード辞書のオンラインヘルプキー。
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Stemmer上書き辞書のオンラインヘルプキー。
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - マッピング辞書のオンラインヘルプキー。
    - ``mapping``
  * - online.help.name.webconfig
    - ウェブ設定のオンラインヘルプキー。
    - ``webconfig``
  * - online.help.name.searchlist
    - 検索リストのオンラインヘルプキー。
    - ``searchlist``
  * - online.help.name.log
    - ログのオンラインヘルプキー。
    - ``log``
  * - online.help.name.general
    - 全般設定のオンラインヘルプキー。
    - ``general``
  * - online.help.name.role
    - ロールのオンラインヘルプキー。
    - ``role``
  * - online.help.name.joblog
    - ジョブログのオンラインヘルプキー。
    - ``joblog``
  * - online.help.name.keymatch
    - キーマッチのオンラインヘルプキー。
    - ``keymatch``
  * - online.help.name.relatedquery
    - 関連クエリーのオンラインヘルプキー。
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - 関連コンテンツのオンラインヘルプキー。
    - ``relatedcontent``
  * - online.help.name.wizard
    - ウィザードのオンラインヘルプキー。
    - ``wizard``
  * - online.help.name.badword
    - 除外ワードのオンラインヘルプキー。
    - ``badword``
  * - online.help.name.pathmap
    - パスマッピングのオンラインヘルプキー。
    - ``pathmap``
  * - online.help.name.boostdoc
    - ドキュメントブーストのオンラインヘルプキー。
    - ``boostdoc``
  * - online.help.name.dataconfig
    - データストア設定のオンラインヘルプキー。
    - ``dataconfig``
  * - online.help.name.systeminfo
    - システム情報のオンラインヘルプキー。
    - ``systeminfo``
  * - online.help.name.user
    - ユーザーのオンラインヘルプキー。
    - ``user``
  * - online.help.name.group
    - グループのオンラインヘルプキー。
    - ``group``
  * - online.help.name.dashboard
    - ダッシュボードのオンラインヘルプキー。
    - ``dashboard``
  * - online.help.name.webauth
    - ウェブ認証のオンラインヘルプキー。
    - ``webauth``
  * - online.help.name.fileconfig
    - ファイルシステム設定のオンラインヘルプキー。
    - ``fileconfig``
  * - online.help.name.fileauth
    - ファイル認証のオンラインヘルプキー。
    - ``fileauth``
  * - online.help.name.labeltype
    - ラベルタイプのオンラインヘルプキー。
    - ``labeltype``
  * - online.help.name.tagtype
    - タグタイプのオンラインヘルプキー。
    - ``tagtype``
  * - online.help.name.duplicatehost
    - 重複ホストのオンラインヘルプキー。
    - ``duplicatehost``
  * - online.help.name.scheduler
    - スケジューラーのオンラインヘルプキー。
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - クロール情報のオンラインヘルプキー。
    - ``crawlinginfo``
  * - online.help.name.backup
    - バックアップのオンラインヘルプキー。
    - ``backup``
  * - online.help.name.upgrade
    - アップグレードのオンラインヘルプキー。
    - ``upgrade``
  * - online.help.name.sereq
    - 検索リクエストのオンラインヘルプキー。
    - ``sereq``
  * - online.help.name.accesstoken
    - アクセストークンのオンラインヘルプキー。
    - ``accesstoken``
  * - online.help.name.suggest
    - サジェストのオンラインヘルプキー。
    - ``suggest``
  * - online.help.name.searchlog
    - 検索ログのオンラインヘルプキー。
    - ``searchlog``
  * - online.help.name.maintenance
    - メンテナンスのオンラインヘルプキー。
    - ``maintenance``
  * - online.help.name.plugin
    - プラグインのオンラインヘルプキー。
    - ``plugin``
  * - online.help.name.storage
    - ストレージのオンラインヘルプキー。
    - ``storage``
  * - online.help.supported.langs
    - オンラインヘルプでサポートする言語。
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - ユーザーサポート用のフォーラムのリンク。
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - フォーラムでサポートする言語。
    - ``en,ja``
  * - suggest.popular.word.seed
    - 人気ワードのサジェストのシード値。
    - ``0``
  * - suggest.popular.word.tags
    - 人気ワードのサジェストのタグ。
    - (empty)
  * - suggest.popular.word.fields
    - 人気ワードのサジェストのフィールド。
    - (empty)
  * - suggest.popular.word.excludes
    - 人気ワードのサジェストから除外する単語。
    - (empty)
  * - suggest.popular.word.size
    - サジェストする人気ワードの数。
    - ``10``
  * - suggest.popular.word.window.size
    - 人気ワードのサジェストのウィンドウサイズ。
    - ``30``
  * - suggest.popular.word.query.freq
    - 人気ワードのサジェストのクエリ頻度。
    - ``10``
  * - suggest.min.hit.count
    - サジェストの最小ヒット数。
    - ``1``
  * - suggest.field.contents
    - サジェストのコンテンツ用フィールド。
    - ``_default``
  * - suggest.field.tags
    - サジェストのタグ用フィールド。
    - ``label``
  * - suggest.field.roles
    - サジェストのロール用フィールド。
    - ``role``
  * - suggest.field.index.contents
    - サジェスト用のインデックスコンテンツ。
    - ``content,title``
  * - suggest.update.request.interval
    - サジェスト更新リクエストの間隔。
    - ``0``
  * - suggest.update.doc.per.request
    - サジェスト更新リクエストあたりのドキュメント数。
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - サジェスト更新コンテンツのパーセンテージ上限。
    - ``50%``
  * - suggest.update.contents.limit.num
    - サジェスト更新コンテンツの最大数。
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - サジェスト更新のドキュメントの最大サイズ。
    - ``50000``
  * - suggest.source.reader.scroll.size
    - サジェストソースリーダーのスクロールサイズ。
    - ``1``
  * - suggest.popular.word.cache.size
    - 人気ワードのサジェストのキャッシュサイズ。
    - ``1000``
  * - suggest.popular.word.cache.expire
    - 人気ワードのサジェストのキャッシュの有効期限（秒）。
    - ``60``
  * - suggest.search.log.permissions
    - サジェスト用検索ログのパーミッション。
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - サジェストにおけるシステム監視の間隔。
    - ``60``
  * - ldap.admin.enabled
    - LDAP管理が有効かどうか。
    - ``false``
  * - ldap.admin.user.filter
    - LDAP管理のユーザーフィルター。
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - LDAP管理ユーザーのベースDN。
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - LDAP管理ユーザーのオブジェクトクラス。
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - LDAP管理のロールフィルター。
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - LDAP管理ロールのベースDN。
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - LDAP管理ロールのオブジェクトクラス。
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - LDAP管理のグループフィルター。
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - LDAP管理グループのベースDN。
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - LDAP管理グループのオブジェクトクラス。
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - LDAP管理でパスワードを同期するかどうか。
    - ``true``
  * - ldap.auth.validation
    - LDAP認証を検証するかどうか。
    - ``true``
  * - ldap.connect.timeout
    - LDAP接続を確立するまでのタイムアウト（ミリ秒）。TLSハンドシェイクと最初のバインド応答も、この値が上限になります。0以下の場合はJDK/OSのデフォルトに任せます。
    - ``10000``
  * - ldap.read.timeout
    - 接続がバインドされた後にLDAPの応答を待つタイムアウト（ミリ秒）。0以下の場合は無期限に待機します。
    - ``30000``
  * - ldap.search.time.limit
    - LDAP検索のサーバー側の時間制限（ミリ秒）。0以下の場合は無制限です。
    - ``60000``
  * - ldap.max.username.length
    - LDAPのユーザー名の最大長。
    - ``-1``
  * - ldap.ignore.netbios.name
    - LDAPでNetBIOS名を無視するかどうか。
    - ``true``
  * - ldap.group.name.with.underscores
    - LDAPのグループ名でアンダースコアを許可するかどうか。
    - ``false``
  * - ldap.lowercase.permission.name
    - LDAPのパーミッション名を小文字にするかどうか。
    - ``false``
  * - ldap.allow.empty.permission
    - LDAPで空のパーミッションを許可するかどうか。
    - ``true``
  * - ldap.samaccountname.group
    - LDAPのグループにsamAccountNameを使用するかどうか。
    - ``false``
  * - ldap.role.search.user.enabled
    - ユーザーのLDAPロール検索が有効かどうか。
    - ``true``
  * - ldap.role.search.group.enabled
    - グループのLDAPロール検索が有効かどうか。
    - ``true``
  * - ldap.role.search.role.enabled
    - ロールのLDAPロール検索が有効かどうか。
    - ``true``
  * - ldap.attr.surname
    - 姓のLDAP属性。
    - ``sn``
  * - ldap.attr.givenName
    - 名のLDAP属性。
    - ``givenName``
  * - ldap.attr.employeeNumber
    - 従業員番号のLDAP属性。
    - ``employeeNumber``
  * - ldap.attr.mail
    - メールのLDAP属性。
    - ``mail``
  * - ldap.attr.telephoneNumber
    - 電話番号のLDAP属性。
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - 自宅電話のLDAP属性。
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - 自宅の郵便住所のLDAP属性。
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - ラベル付きURIのLDAP属性。
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - 部屋番号のLDAP属性。
    - ``roomNumber``
  * - ldap.attr.description
    - 説明のLDAP属性。
    - ``description``
  * - ldap.attr.title
    - 役職のLDAP属性。
    - ``title``
  * - ldap.attr.pager
    - ページャーのLDAP属性。
    - ``pager``
  * - ldap.attr.street
    - 番地のLDAP属性。
    - ``street``
  * - ldap.attr.postalCode
    - 郵便番号のLDAP属性。
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - 物理的な配達オフィス名のLDAP属性。
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - 宛先インジケーターのLDAP属性。
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - 国際ISDN番号のLDAP属性。
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - 都道府県のLDAP属性。
    - ``st``
  * - ldap.attr.employeeType
    - 従業員タイプのLDAP属性。
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - ファクシミリ番号のLDAP属性。
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - 私書箱のLDAP属性。
    - ``postOfficeBox``
  * - ldap.attr.initials
    - イニシャルのLDAP属性。
    - ``initials``
  * - ldap.attr.carLicense
    - 車両ナンバーのLDAP属性。
    - ``carLicense``
  * - ldap.attr.mobile
    - 携帯電話のLDAP属性。
    - ``mobile``
  * - ldap.attr.postalAddress
    - 郵便住所のLDAP属性。
    - ``postalAddress``
  * - ldap.attr.city
    - 市区町村のLDAP属性。
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - テレテックス端末識別子のLDAP属性。
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - X.121アドレスのLDAP属性。
    - ``x121Address``
  * - ldap.attr.businessCategory
    - 業種のLDAP属性。
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - 登録住所のLDAP属性。
    - ``registeredAddress``
  * - ldap.attr.displayName
    - 表示名のLDAP属性。
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - 優先言語のLDAP属性。
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - 部署番号のLDAP属性。
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - UID番号のLDAP属性。
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - GID番号のLDAP属性。
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - ホームディレクトリのLDAP属性。
    - ``homeDirectory``
  * - plugin.repositories
    - プラグインリポジトリのURL。
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - プラグインのバージョンフィルター。
    - (empty)
  * - storage.max.items.in.page
    - ストレージの1ページあたりの最大項目数。
    - ``1000``
  * - password.invalid.admin.passwords
    - 無効な管理者パスワードのリスト。
    - ``admin``
  * - password.min.length
    - パスワードの最小長（0で無効）。
    - ``8``
  * - password.max.length
    - パスワードフィールドの最大長。
    - ``100``
  * - password.require.uppercase
    - パスワードに大文字を必須にします。
    - ``false``
  * - password.require.lowercase
    - パスワードに小文字を必須にします。
    - ``false``
  * - password.require.digit
    - パスワードに数字を必須にします。
    - ``false``
  * - password.require.special.char
    - パスワードに特殊文字を必須にします。
    - ``false``
  * - rag.chat.enabled
    - RAGチャット機能が有効かどうか。
    - ``false``
  * - rag.chat.log.enabled
    - RAGチャットの各リクエストの利用状況（ユーザー、時刻、LLM呼び出しとトークン）をチャットログに記録するかどうか。質問と回答が記録されることはありません。
    - ``true``
  * - rag.chat.context.max.documents
    - チャット生成の設定。
    - ``5``
  * - rag.chat.query.regeneration.max.count
    - 検索でドキュメントが見つからなかった場合、またはストリーミングチャットでヒットしたものがどれも関連があると判断されなかった場合に、1回のチャットリクエストが検索クエリを再生成して再検索する最大回数。再生成のたびにLLM呼び出しが1回行われ、新しい検索にヒットがある場合はさらに関連性評価の呼び出しが1回行われます（0で無効）。
    - ``2``
  * - rag.chat.session.timeout.minutes
    - セッションの設定。
    - ``30``
  * - rag.chat.session.max.size
    - キャッシュするチャットセッションの最大数。これを超えると、最後にアクセスされたのが最も古いものから破棄されます（0以下の場合は100）。
    - ``10000``
  * - rag.chat.history.max.messages
    - 1つのチャットセッションに保持するメッセージの最大数。新しいメッセージのたびに、古いターンは切り詰められます。
    - ``30``
  * - rag.chat.content.fields
    - 拡張RAGフローの設定。ドキュメントの全コンテンツのために取得するフィールド。
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - RAG検索のハイライト設定。
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - RAGチャットのコンテキスト検索における、ドキュメントあたりのハイライトフラグメント数。
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - 回答生成における大きなドキュメントの扱い。content_lengthがこの値を超えるドキュメントは、回答コンテキストで全コンテンツの代わりにハイライトされた抜粋を使用します。
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - 回答コンテキスト用に大きなドキュメントから抜粋を取り出すときに使用するハイライト設定。
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - 回答コンテキスト用に、サイズの大きい各ドキュメントから取り出すハイライトフラグメント数。
    - ``5``
  * - rag.chat.history.assistant.content
    - アシスタントメッセージの履歴コンテンツモード。smart_summary - アシスタントの本文を破棄し、ターンごとに過去の検索クエリ + 参照したタイトルのみを保持（デフォルト、推奨） full - アシスタントの応答全体を送信 source_titles - 本文 + 参照したタイトルを末尾に付加 source_titles_and_urls - "[References: title (url), ...]" のみ truncated - history.assistant.max.charsでアシスタントの応答を切り詰める none - 履歴からアシスタントのターンを破棄
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - smart_summary履歴モードで、ターンごとに含める参照ドキュメントタイトルの最大数。
    - ``5``
  * - rag.chat.document.max.parts
    - LLMのコンテキスト予算より長い単一のドキュメントについてチャットするときに、ドキュメントを分割するパーツの最大数。各パーツは個別に要約され、要約は回答にまとめられます。この数を超えるパーツは使用されません。そのようなドキュメントに関するリクエストは、毎ターン、最大でこの数のLLM呼び出しに加えて回答用の1回のLLM呼び出しを行います。
    - ``10``
  * - rag.chat.response.language
    - LLMに回答を求める言語。browser - ユーザーのブラウザーまたはUIロケールの言語。英語の場合は指示なし（デフォルト） none - 言語の指示なし。LLMは通常、質問と同じ言語で回答する en, ja.. - 常にこの言語で回答する
    - ``browser``
  * - index.export.path
    - インデックスエクスポート
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - インデックスエクスポートジョブが書き出すファイルから除外する、ドキュメントフィールドのカンマ区切りリスト。
    - ``cache,tag``
  * - index.export.scroll.size
    - インデックスエクスポートジョブが1回のスクロールリクエストで取得するドキュメント数。
    - ``100``
  * - index.export.format
    - エクスポートするドキュメントの出力形式。受け付けるのはhtmlとjsonのみで、それ以外の場合はジョブが失敗します。
    - ``html``
  * - log.notification.flush.interval
    - ログ通知 ログ通知バッファを検索エンジンにフラッシュする間隔（秒）。
    - ``30``
  * - log.notification.max.details.length
    - 通知の詳細テキストの最大長。
    - ``3000``
  * - log.notification.max.display.events
    - 通知に表示するイベントの最大数。
    - ``50``
  * - log.notification.max.message.length
    - 通知内の各ログメッセージの最大長。
    - ``200``
  * - log.notification.search.size
    - 通知ジョブごとに検索エンジンから取得するイベントの最大数。
    - ``1000``
  * - log.notification.buffer.size
    - メモリ上にバッファするイベントの最大数。
    - ``1000``
  * - log.notification.interval
    - 通知ジョブのサイクルの間隔（秒）。通知メッセージで使用されます。
    - ``300``
  * - theme.directory.path
    - 静的テーマシステム（docs/superpowers/specs/2026-05-21-fess-static-theme-design.mdを参照）
    - ``themes``
  * - theme.upload.max.size
    - アップロードされたテーマアーカイブの最大サイズ（バイト）。
    - ``52428800``
  * - theme.upload.max.extracted.size
    - 展開後の合計サイズの最大値（バイト）。これを超えると展開は中止されます。
    - ``209715200``
  * - theme.upload.max.entries
    - アップロードされたテーマアーカイブで許可されるエントリの最大数。
    - ``1000``
  * - theme.upload.max.compression.ratio
    - テーマアーカイブの1つのエントリに対する、非圧縮/圧縮比の最大値。
    - ``100``
  * - theme.upload.zip.ratio.max
    - アーカイブ全体に対する、非圧縮/圧縮比の累積の最大値（zipボム対策）。
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - 累積zip比のチェックが適用されるまでに読み込む圧縮済みバイト数。これより小さいアーカイブはチェックをスキップします。
    - ``65536``
  * - theme.upload.attic.retention.days
    - 置き換えられたテーマディレクトリを、クリーンアップ処理が削除するまで保持する期間（日）。
    - ``7``
  * - theme.repositories
    - 静的テーマのダウンロード元のリポジトリURL（カンマ区切り）。
    - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
  * - theme.index.frame.ancestors
    - 静的テーマのHTMLページのContent-Security-Policyにおけるframe-ancestorsディレクティブの値。これらをフレームに埋め込むことができるオリジンです。デフォルトの'none'は、どのページにも埋め込みを許可しません。WebKit（Safari）は、テーマのファイルプレビューとキャッシュ表示が使用するblob:フレームにもframe-ancestorsを適用するため、値が'none'の間はそれらが空白で表示されます。ディレクティブを削除するには値を空のままにします。どちらの場合もX-Frame-Options: DENYが送信され、すべてのブラウザーでページがフレームに入らないようにします（frame-ancestorsを尊重するブラウザーはそのヘッダーを無視します）。
    - ``'none'``
  * - theme.api.csrf.server.origins
    - 任意: このFessインスタンスの正規の外部オリジン（カンマ/改行区切り）。例: https://fess.example.com。設定すると、これらはv2のCSRF Originチェックで、転送ヘッダーを信頼せずに同一オリジンとして扱われます。rate.limit.trusted.proxiesに記載されていないリバースプロキシの背後での利用を推奨します。空の場合、ターゲットオリジンは、信頼するプロキシのX-Forwarded-\*ヘッダーから、次にサーブレットリクエストから再構築されます。
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - クライアントIPごとに1分あたりに許可されるログイン試行回数。0以下の場合はこの制限を無効にします。
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - クライアントIPとユーザー名の組ごとに1分あたりに許可されるログイン試行回数。パスワード変更も制限します。
    - ``5``
  * - theme.api.login.lockout.seconds
    - ログインのレート制限を超えた時点で適用されるロックアウト（秒）。0以下の場合はロックアウトを無効にします。
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - メモリ上に保持するログインレート制限バケットの最大数。上限に達すると、アイドル状態のバケットは破棄されます。
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - /api/v2/chat/streamが送信するSSEキープアライブpingの間隔。pingはコメントのみの行（": keepalive\\n\\n"）で、イベントストリームには影響しませんが、長いLLMフェーズの間にアイドル接続を切断する中間装置（nginxのデフォルトのproxy_read_timeoutは60s）を回避します。<=0を設定すると無効になります。単位: ミリ秒。
    - ``15000``
.. GENERATED-END: properties
