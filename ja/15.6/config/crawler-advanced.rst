========================
クローラー詳細設定
========================

概要
====

本ガイドでは、|Fess| クローラーの高度な設定について説明します。
基本的なクローラー設定については、:doc:`crawler-basic` を参照してください。

.. warning::
   本ページの設定は、システム全体に影響する可能性があります。
   設定を変更する際は、十分にテストを行ってから本番環境に適用してください。

全般設定
========

設定ファイルの場所
------------------

クローラーの詳細設定は、以下のファイルで行います。

- **メイン設定**: ``/etc/fess/fess_config.properties`` (または ``app/WEB-INF/classes/fess_config.properties``)
- **コンテンツ長設定**: ``app/WEB-INF/classes/crawler/contentlength.xml``
- **コンポーネント設定**: ``app/WEB-INF/classes/crawler/container.xml``

デフォルトスクリプト
--------------------

クローラーのデフォルトスクリプト言語を設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.default.script``
     - クローラースクリプトの言語
     - ``groovy``

::

    crawler.default.script=groovy

HTTPスレッドプール
------------------

HTTPクローラーのスレッドプール設定です。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.http.thread_pool.size``
     - HTTPスレッドプールサイズ
     - ``0``

::

    # 0の場合は自動設定
    crawler.http.thread_pool.size=0

ドキュメント処理設定
====================

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.max.site.length``
     - ドキュメントサイトの最大行数
     - ``100``
   * - ``crawler.document.site.encoding``
     - ドキュメントサイトのエンコーディング
     - ``UTF-8``
   * - ``crawler.document.unknown.hostname``
     - 不明なホスト名の代替値
     - ``unknown``
   * - ``crawler.document.use.site.encoding.on.english``
     - 英語ドキュメントでサイトエンコーディングを使用
     - ``false``
   * - ``crawler.document.append.data``
     - ドキュメントにデータを追加
     - ``true``
   * - ``crawler.document.append.filename``
     - ファイル名をドキュメントに追加
     - ``false``

設定例
~~~~~~

::

    crawler.document.max.site.length=100
    crawler.document.site.encoding=UTF-8
    crawler.document.unknown.hostname=unknown
    crawler.document.use.site.encoding.on.english=false
    crawler.document.append.data=true
    crawler.document.append.filename=false

単語処理設定
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.max.alphanum.term.size``
     - 英数字単語の最大長
     - ``20``
   * - ``crawler.document.max.symbol.term.size``
     - 記号単語の最大長
     - ``10``
   * - ``crawler.document.duplicate.term.removed``
     - 重複単語の削除
     - ``false``

設定例
~~~~~~

::

    # 英数字の最大長を50文字に変更
    crawler.document.max.alphanum.term.size=50

    # 記号の最大長を20文字に変更
    crawler.document.max.symbol.term.size=20

    # 重複単語を削除
    crawler.document.duplicate.term.removed=true

.. note::
   ``max.alphanum.term.size`` を大きくすると、長いID、トークン、URLなどを
   完全な形でインデックスできますが、インデックスサイズが増加します。

文字処理設定
------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.space.chars``
     - 空白文字の定義
     - ``\u0009\u000A...``
   * - ``crawler.document.fullstop.chars``
     - 句点文字の定義
     - ``\u002e\u06d4...``

設定例
~~~~~~

::

    # デフォルト値(Unicode文字を含む)
    crawler.document.space.chars=\u0009\u000A\u000B\u000C\u000D\u001C\u001D\u001E\u001F\u0020\u00A0\u1680\u180E\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200A\u200B\u200C\u202F\u205F\u3000\uFEFF\uFFFD\u00B6

    crawler.document.fullstop.chars=\u002e\u06d4\u2e3c\u3002

プロトコル設定
==============

対応プロトコル
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.web.protocols``
     - Webクロールのプロトコル
     - ``http,https``
   * - ``crawler.file.protocols``
     - ファイルクロールのプロトコル
     - ``file,smb,smb1,ftp,storage,s3,gcs``

設定例
~~~~~~

::

    crawler.web.protocols=http,https
    crawler.file.protocols=file,smb,smb1,ftp,storage,s3,gcs

環境変数パラメーター
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.data.env.param.key.pattern``
     - 環境変数パラメーターキーのパターン
     - ``^FESS_ENV_.*``

::

    # FESS_ENV_で始まる環境変数をクロール設定で使用可能
    crawler.data.env.param.key.pattern=^FESS_ENV_.*

robots.txt 設定
===============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.ignore.robots.txt``
     - robots.txtを無視
     - ``false``
   * - ``crawler.ignore.robots.tags``
     - robotsメタタグを無視
     - ``false``
   * - ``crawler.ignore.content.exception``
     - コンテンツ例外を無視
     - ``true``

設定例
~~~~~~

::

    # robots.txtを無視(推奨しません)
    crawler.ignore.robots.txt=false

    # 特定のrobotsタグを無視
    crawler.ignore.robots.tags=

    # コンテンツ例外を無視
    crawler.ignore.content.exception=true

.. warning::
   ``crawler.ignore.robots.txt=true`` に設定すると、サイトの利用規約に
   違反する可能性があります。外部サイトをクロールする際は注意してください。

エラー処理設定
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.failure.url.status.codes``
     - 失敗とみなすHTTPステータスコード
     - ``404``

設定例
~~~~~~

::

    # 404に加えて403もエラーとして扱う
    crawler.failure.url.status.codes=404,403

システム監視設定
================

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.system.monitor.interval``
     - システム監視間隔(秒)
     - ``60``

::

    # 30秒ごとにシステムをモニタリング
    crawler.system.monitor.interval=30

ホットスレッド設定
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.hotthread.ignore_idle_threads``
     - アイドルスレッドを無視
     - ``true``
   * - ``crawler.hotthread.interval``
     - スナップショット間隔
     - ``500ms``
   * - ``crawler.hotthread.snapshots``
     - スナップショット数
     - ``10``
   * - ``crawler.hotthread.threads``
     - 監視スレッド数
     - ``3``
   * - ``crawler.hotthread.timeout``
     - タイムアウト
     - ``30s``
   * - ``crawler.hotthread.type``
     - 監視タイプ
     - ``cpu``

設定例
~~~~~~

::

    crawler.hotthread.ignore_idle_threads=true
    crawler.hotthread.interval=500ms
    crawler.hotthread.snapshots=10
    crawler.hotthread.threads=3
    crawler.hotthread.timeout=30s
    crawler.hotthread.type=cpu

メタデータ設定
==============

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.metadata.content.excludes``
     - 除外するメタデータ
     - ``resourceName,X-Parsed-By...``
   * - ``crawler.metadata.name.mapping``
     - メタデータ名のマッピング
     - ``title=title:string...``

設定例
~~~~~~

::

    # 除外するメタデータ
    crawler.metadata.content.excludes=resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*

    # メタデータ名のマッピング
    crawler.metadata.name.mapping=\
        title=title:string\n\
        Title=title:string\n\
        dc:title=title:string

HTML クローラー設定
===================

XPath 設定
----------

HTML要素を抽出するためのXPath設定です。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.html.content.xpath``
     - コンテンツのXPath
     - ``//BODY``
   * - ``crawler.document.html.lang.xpath``
     - 言語のXPath
     - ``//HTML/@lang``
   * - ``crawler.document.html.digest.xpath``
     - ダイジェストのXPath
     - ``//META[@name='description']/@content``
   * - ``crawler.document.html.canonical.xpath``
     - カノニカルURLのXPath
     - ``//LINK[@rel='canonical'][1]/@href``

設定例
~~~~~~

::

    # デフォルト設定
    crawler.document.html.content.xpath=//BODY
    crawler.document.html.lang.xpath=//HTML/@lang
    crawler.document.html.digest.xpath=//META[@name='description']/@content
    crawler.document.html.canonical.xpath=//LINK[@rel='canonical'][1]/@href

カスタム XPath の例
~~~~~~~~~~~~~~~~~~~

::

    # 特定のdiv要素のみをコンテンツとして抽出
    crawler.document.html.content.xpath=//DIV[@id='main-content']

    # meta keywordsもダイジェストに含める
    crawler.document.html.digest.xpath=//META[@name='description']/@content|//META[@name='keywords']/@content

HTML タグ処理
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.html.pruned.tags``
     - 削除するHTMLタグ
     - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
   * - ``crawler.document.html.max.digest.length``
     - ダイジェストの最大長
     - ``120``
   * - ``crawler.document.html.default.lang``
     - デフォルト言語
     - (空)

設定例
~~~~~~

::

    # 削除するタグを追加
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,a[rel=nofollow],form

    # ダイジェストの長さを200文字に
    crawler.document.html.max.digest.length=200

    # デフォルト言語を日本語に
    crawler.document.html.default.lang=ja

URLパターンフィルター
---------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.html.default.include.index.patterns``
     - インデックスに含めるURLパターン
     - (空)
   * - ``crawler.document.html.default.exclude.index.patterns``
     - インデックスから除外するURLパターン
     - ``(?i).*(css|js|jpeg...)``
   * - ``crawler.document.html.default.include.search.patterns``
     - 検索結果に含めるURLパターン
     - (空)
   * - ``crawler.document.html.default.exclude.search.patterns``
     - 検索結果から除外するURLパターン
     - (空)

設定例
~~~~~~

::

    # デフォルトの除外パターン
    crawler.document.html.default.exclude.index.patterns=(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)

    # 特定のパスのみインデックス
    crawler.document.html.default.include.index.patterns=https://example\\.com/docs/.*

ファイルクローラー設定
======================

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.file.name.encoding``
     - ファイル名のエンコーディング
     - (空)
   * - ``crawler.document.file.no.title.label``
     - タイトルなしファイルのラベル
     - ``No title.``
   * - ``crawler.document.file.ignore.empty.content``
     - 空のコンテンツを無視
     - ``false``
   * - ``crawler.document.file.max.title.length``
     - タイトルの最大長
     - ``100``
   * - ``crawler.document.file.max.digest.length``
     - ダイジェストの最大長
     - ``200``

設定例
~~~~~~

::

    # Windows-31Jのファイル名を処理
    crawler.document.file.name.encoding=Windows-31J

    # タイトルなしファイルのラベル
    crawler.document.file.no.title.label=タイトルなし

    # 空のファイルを無視
    crawler.document.file.ignore.empty.content=true

    # タイトルとダイジェストの長さ
    crawler.document.file.max.title.length=200
    crawler.document.file.max.digest.length=500

コンテンツ処理
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.file.append.meta.content``
     - メタデータをコンテンツに追加
     - ``true``
   * - ``crawler.document.file.append.body.content``
     - 本文をコンテンツに追加
     - ``true``
   * - ``crawler.document.file.default.lang``
     - デフォルト言語
     - (空)

設定例
~~~~~~

::

    crawler.document.file.append.meta.content=true
    crawler.document.file.append.body.content=true
    crawler.document.file.default.lang=ja

ファイルURLパターンフィルター
------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.file.default.include.index.patterns``
     - インデックスに含めるパターン
     - (空)
   * - ``crawler.document.file.default.exclude.index.patterns``
     - インデックスから除外するパターン
     - (空)
   * - ``crawler.document.file.default.include.search.patterns``
     - 検索結果に含めるパターン
     - (空)
   * - ``crawler.document.file.default.exclude.search.patterns``
     - 検索結果から除外するパターン
     - (空)

設定例
~~~~~~

::

    # 特定の拡張子のみインデックス
    crawler.document.file.default.include.index.patterns=.*\\.(pdf|docx|xlsx|pptx)$

    # tempフォルダーを除外
    crawler.document.file.default.exclude.index.patterns=.*/temp/.*

MIMEタイプ検出オーバーライド
------------------------------

|Fess| はデフォルトで Apache Tika を使用してコンテンツベースのMIMEタイプ検出を行います。
しかし、一部のケースでコンテンツベースの検出が誤った結果を返すことがあります。
たとえば、``REM`` コメントで始まるOracle SQLファイルは、``REM`` キーワードが
バッチファイルのマジックパターンに一致するため、``application/x-bat`` として
誤検出される場合があります。

``crawler.document.mimetype.extension.overrides`` プロパティを使用すると、
ファイル拡張子に基づいてMIMEタイプ検出をオーバーライドし、
特定のファイルタイプに対するコンテンツベース検出をバイパスできます。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.mimetype.extension.overrides``
     - 拡張子からMIMEタイプへのオーバーライドマッピング（1行に1つ、形式: ``.ext=mime/type``）
     - (空)

設定例
~~~~~~

::

    # SQLファイルのMIMEタイプ検出をオーバーライド
    crawler.document.mimetype.extension.overrides=\
    .sql=text/x-sql\n\
    .plsql=text/x-plsql\n\
    .pls=text/x-plsql

各行は ``.拡張子=MIMEタイプ`` の形式で記述します。
複数のマッピングは ``\n``（改行）で区切ります。
拡張子のマッチングは大文字小文字を区別しません（``.SQL`` と ``.sql`` は同じ扱い）。

.. note::
   ファイル拡張子がこのマップのエントリに一致する場合、設定されたMIMEタイプが
   コンテンツベース検出を行わずに即座に返されます。
   マップにない拡張子のファイルは、通常のTika検出が使用されます。

キャッシュ設定
==============

ドキュメントキャッシュ
----------------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``crawler.document.cache.enabled``
     - ドキュメントキャッシュを有効化
     - ``true``
   * - ``crawler.document.cache.max.size``
     - キャッシュの最大サイズ(バイト)
     - ``2621440`` (2.5MB)
   * - ``crawler.document.cache.supported.mimetypes``
     - キャッシュ対象のMIMEタイプ
     - ``text/html``
   * - ``crawler.document.cache.html.mimetypes``
     - HTMLとして扱うMIMEタイプ
     - ``text/html``

設定例
~~~~~~

::

    # ドキュメントキャッシュを有効化
    crawler.document.cache.enabled=true

    # キャッシュサイズを5MBに
    crawler.document.cache.max.size=5242880

    # キャッシュ対象のMIMEタイプ
    crawler.document.cache.supported.mimetypes=text/html,application/xhtml+xml

    # HTMLとして扱うMIMEタイプ
    crawler.document.cache.html.mimetypes=text/html,application/xhtml+xml

.. note::
   キャッシュを有効にすると、検索結果にキャッシュリンクが表示され、
   ユーザーはクロール時点のコンテンツを参照できます。

JVM オプション
==============

クローラープロセスのJVMオプションを設定できます。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``jvm.crawler.options``
     - クローラーのJVMオプション
     - ``-Xms128m -Xmx512m...``

デフォルト設定
--------------

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000 \
        -XX:-HeapDumpOnOutOfMemoryError

主要なオプションの説明
----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 説明
   * - ``-Xms128m``
     - 初期ヒープサイズ(128MB)
   * - ``-Xmx512m``
     - 最大ヒープサイズ(512MB)
   * - ``-XX:MaxMetaspaceSize=128m``
     - Metaspaceの最大サイズ(128MB)
   * - ``-XX:+UseG1GC``
     - G1ガベージコレクターを使用
   * - ``-XX:MaxGCPauseMillis=60000``
     - GC停止時間の目標値(60秒)
   * - ``-XX:-HeapDumpOnOutOfMemoryError``
     - OutOfMemory時のヒープダンプを無効化

カスタム設定例
--------------

**大きなファイルをクロールする場合:**

::

    jvm.crawler.options=-Xms256m -Xmx2g \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        -XX:MaxGCPauseMillis=60000

**デバッグ時:**

::

    jvm.crawler.options=-Xms128m -Xmx512m \
        -XX:MaxMetaspaceSize=128m \
        -XX:+UseG1GC \
        -XX:+HeapDumpOnOutOfMemoryError \
        -XX:HeapDumpPath=/tmp/crawler_dump.hprof

詳細は :doc:`setup-memory` を参照してください。

パフォーマンスチューニング
==========================

クロール速度の最適化
--------------------

**1. スレッド数の調整**

並列クロール数を増やすことで、クロール速度を向上できます。

::

    # 管理画面のクロール設定でスレッド数を調整
    スレッド数: 10

ただし、対象サーバーへの負荷に注意してください。

**2. タイムアウトの調整**

応答が遅いサイトの場合、タイムアウトを調整します。

::

    # クロール設定の「設定パラメーター」に追加
    client.connectionTimeout=10000
    client.socketTimeout=30000

**3. 不要なコンテンツの除外**

画像、CSS、JavaScriptファイルなどを除外することで、クロール速度が向上します。

::

    # 除外URLパターン
    .*\.(jpg|jpeg|png|gif|css|js|ico)$

**4. リトライ設定**

エラー時のリトライ回数と間隔を調整します。

::

    # クロール設定の「設定パラメーター」に追加
    client.maxRetry=3
    client.retryInterval=1000

メモリ使用量の最適化
--------------------

**1. ヒープサイズの調整**

::

    jvm.crawler.options=-Xms256m -Xmx1g

**2. キャッシュサイズの調整**

::

    crawler.document.cache.max.size=1048576  # 1MB

**3. 大きなファイルの除外**

::

    # クロール設定の「設定パラメーター」に追加
    client.maxContentLength=10485760  # 10MB

詳細は :doc:`setup-memory` を参照してください。

インデックス品質の向上
----------------------

**1. XPathの最適化**

不要な要素(ナビゲーション、広告など)を除外します。

::

    crawler.document.html.content.xpath=//DIV[@id='main-content']
    crawler.document.html.pruned.tags=noscript,script,style,header,footer,aside,nav,form,iframe

**2. ダイジェストの最適化**

::

    crawler.document.html.max.digest.length=200

**3. メタデータマッピング**

::

    crawler.metadata.name.mapping=\
        title=title:string\n\
        description=digest:string\n\
        keywords=label:string

トラブルシューティング
======================

メモリ不足
----------

**症状:**

- ``OutOfMemoryError`` が ``fess_crawler.log`` に記録される
- クロールが途中で停止する

**対策:**

1. クローラーのヒープサイズを増やす

   ::

       jvm.crawler.options=-Xms256m -Xmx2g

2. 並列スレッド数を減らす

3. 大きなファイルを除外する

詳細は :doc:`setup-memory` を参照してください。

クロールが遅い
--------------

**症状:**

- クロールに時間がかかりすぎる
- タイムアウトが頻発する

**対策:**

1. スレッド数を増やす(対象サーバーの負荷に注意)

2. タイムアウトを調整する

   ::

       client.connectionTimeout=5000
       client.socketTimeout=10000

3. 不要なURLを除外する

特定のコンテンツが抽出できない
------------------------------

**症状:**

- ページのテキストが正しく抽出されない
- 重要な情報が検索結果に含まれない

**対策:**

1. XPathを確認・調整する

   ::

       crawler.document.html.content.xpath=//DIV[@class='content']

2. 削除タグを確認する

   ::

       crawler.document.html.pruned.tags=script,style

3. JavaScriptで動的に生成されるコンテンツの場合、別の方法(APIクロールなど)を検討

文字化けが発生する
------------------

**症状:**

- 検索結果で文字化けが発生する
- 特定の言語が正しく表示されない

**対策:**

1. エンコーディング設定を確認

   ::

       crawler.document.site.encoding=UTF-8
       crawler.crawling.data.encoding=UTF-8

2. ファイル名のエンコーディングを設定

   ::

       crawler.document.file.name.encoding=Windows-31J

3. ログでエンコーディングエラーを確認

   ::

       grep -i "encoding" /var/log/fess/fess_crawler.log

ベストプラクティス
==================

1. **テスト環境で検証**

   本番環境に適用する前に、テスト環境で十分に検証してください。

2. **段階的な調整**

   設定を一度に大きく変更せず、段階的に調整して効果を確認してください。

3. **ログの監視**

   設定変更後は、ログを監視してエラーやパフォーマンスの問題がないか確認してください。

   ::

       tail -f /var/log/fess/fess_crawler.log

4. **バックアップ**

   設定ファイルを変更する前に、必ずバックアップを取ってください。

   ::

       cp /etc/fess/fess_config.properties /etc/fess/fess_config.properties.bak

5. **ドキュメント化**

   変更した設定とその理由をドキュメント化してください。

S3/GCSクローラー設定
====================

S3クローラー
------------

S3およびS3互換ストレージ（MinIO等）をクロールするための設定です。
ファイルクロール設定の「設定パラメーター」に以下を記述します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - パラメーター
     - 説明
     - デフォルト
   * - ``client.endpoint``
     - S3エンドポイントURL
     - (必須)
   * - ``client.accessKey``
     - アクセスキー
     - (必須)
   * - ``client.secretKey``
     - シークレットキー
     - (必須)
   * - ``client.region``
     - AWSリージョン
     - ``us-east-1``
   * - ``client.connectTimeout``
     - 接続タイムアウト(ms)
     - ``10000``
   * - ``client.readTimeout``
     - 読み取りタイムアウト(ms)
     - ``10000``

設定例
~~~~~~

::

    client.endpoint=https://s3.ap-northeast-1.amazonaws.com
    client.accessKey=AKIAIOSFODNN7EXAMPLE
    client.secretKey=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    client.region=ap-northeast-1

GCSクローラー
-------------

Google Cloud Storageをクロールするための設定です。
ファイルクロール設定の「設定パラメーター」に以下を記述します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - パラメーター
     - 説明
     - デフォルト
   * - ``client.projectId``
     - Google CloudプロジェクトID
     - (必須)
   * - ``client.credentialsFile``
     - サービスアカウントJSONファイルパス
     - (オプション)
   * - ``client.endpoint``
     - カスタムエンドポイント
     - (オプション)
   * - ``client.connectTimeout``
     - 接続タイムアウト(ms)
     - ``10000``
   * - ``client.writeTimeout``
     - 書き込みタイムアウト(ms)
     - ``10000``
   * - ``client.readTimeout``
     - 読み取りタイムアウト(ms)
     - ``10000``

設定例
~~~~~~

::

    client.projectId=my-gcp-project
    client.credentialsFile=/etc/fess/gcs-credentials.json

.. note::
   ``credentialsFile`` を省略した場合、環境変数 ``GOOGLE_APPLICATION_CREDENTIALS`` が使用されます。

参考情報
========

- :doc:`crawler-basic` - クローラー基本設定
- :doc:`crawler-thumbnail` - サムネイル設定
- :doc:`setup-memory` - メモリ設定
- :doc:`admin-logging` - ログ設定
- :doc:`search-advanced` - 高度な検索設定
