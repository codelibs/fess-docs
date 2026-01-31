==================================
Groovyスクリプトガイド
==================================

概要
====

Groovyは |Fess| のデフォルトスクリプト言語です。
Java仮想マシン（JVM）上で動作し、Javaとの高い互換性を持ちながら、
より簡潔な構文でスクリプトを記述できます。

基本構文
========

変数宣言
--------

::

    // 型推論（def）
    def name = "Fess"
    def count = 100

    // 明示的な型指定
    String title = "Document Title"
    int pageNum = 1

文字列操作
----------

::

    // 文字列補間（GString）
    def id = 123
    def url = "https://example.com/doc/${id}"

    // 複数行文字列
    def content = """
    This is a
    multi-line string
    """

    // 置換
    title.replace("old", "new")
    title.replaceAll(/\s+/, " ")  // 正規表現

    // 分割・結合
    def tags = "tag1,tag2,tag3".split(",")
    def joined = tags.join(", ")

    // 大文字/小文字変換
    title.toUpperCase()
    title.toLowerCase()

コレクション操作
----------------

::

    // リスト
    def list = [1, 2, 3, 4, 5]
    list.each { println it }
    def doubled = list.collect { it * 2 }
    def filtered = list.findAll { it > 3 }

    // マップ
    def map = [name: "Fess", version: "15.5"]
    println map.name
    println map["version"]

条件分岐
--------

::

    // if-else
    if (data.status == "active") {
        return "有効"
    } else {
        return "無効"
    }

    // 三項演算子
    def result = data.count > 0 ? "あり" : "なし"

    // エルビス演算子（null合体演算子）
    def value = data.title ?: "無題"

    // セーフナビゲーション演算子
    def length = data.content?.length() ?: 0

ループ処理
----------

::

    // for-each
    for (item in items) {
        println item
    }

    // クロージャ
    items.each { item ->
        println item
    }

    // 範囲
    (1..10).each { println it }

データストアスクリプト
======================

データストア設定でのスクリプト例です。

基本的なマッピング
------------------

::

    url=data.url
    title=data.title
    content=data.content
    lastModified=data.updated_at

URLの生成
---------

::

    // ID基づくURL生成
    url="https://example.com/article/" + data.id

    // 複数フィールドの組み合わせ
    url="https://example.com/" + data.category + "/" + data.slug + ".html"

    // 条件付きURL
    url=data.external_url ?: "https://example.com/default/" + data.id

コンテンツの加工
----------------

::

    // HTMLタグの除去
    content=data.html_content.replaceAll(/<[^>]+>/, "")

    // 複数フィールドの結合
    content=data.title + "\n" + data.description + "\n" + data.body

    // 長さの制限
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

日付の処理
----------

::

    // 日付のパース
    import java.text.SimpleDateFormat
    def sdf = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
    lastModified=sdf.parse(data.date_string)

    // エポック秒からの変換
    lastModified=new Date(data.timestamp * 1000L)

スケジュールジョブスクリプト
============================

スケジュールジョブで使用するGroovyスクリプトの例です。

クロールジョブの実行
--------------------

::

    return container.getComponent("crawlJob").execute();

条件付きクロール
----------------

::

    import java.util.Calendar

    def cal = Calendar.getInstance()
    def hour = cal.get(Calendar.HOUR_OF_DAY)

    // 業務時間外のみクロール
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").execute()
    }
    return "Skipped during business hours"

複数のジョブを順番に実行
------------------------

::

    def results = []

    // インデックス最適化
    results << container.getComponent("optimizeJob").execute()

    // クロール実行
    results << container.getComponent("crawlJob").execute()

    return results.join("\n")

Javaクラスの使用
================

Groovyスクリプト内では、Javaの標準ライブラリやFessのクラスを使用できます。

日付・時刻
----------

::

    import java.time.LocalDateTime
    import java.time.format.DateTimeFormatter

    def now = LocalDateTime.now()
    def formatted = now.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)

ファイル操作
------------

::

    import java.nio.file.Files
    import java.nio.file.Paths

    def content = new String(Files.readAllBytes(Paths.get("/path/to/file.txt")))

HTTP通信
--------

::

    import java.net.URL

    def url = new URL("https://api.example.com/data")
    def response = url.text

.. warning::
   外部リソースへのアクセスはパフォーマンスに影響するため、
   必要最小限に抑えてください。

Fessコンポーネントへのアクセス
==============================

``container`` を使用してFessのコンポーネントにアクセスできます。

システムヘルパー
----------------

::

    def systemHelper = container.getComponent("systemHelper")
    def currentTime = systemHelper.getCurrentTimeAsLong()

設定値の取得
------------

::

    def fessConfig = container.getComponent("fessConfig")
    def indexName = fessConfig.getIndexDocumentUpdateIndex()

検索の実行
----------

::

    def searchHelper = container.getComponent("searchHelper")
    // 検索パラメーターを設定して検索実行

エラーハンドリング
==================

::

    try {
        def result = processData(data)
        return result
    } catch (Exception e) {
        import org.apache.logging.log4j.LogManager
        def logger = LogManager.getLogger("script")
        logger.error("Error processing data: {}", e.message, e)
        return "Error: " + e.message
    }

デバッグとログ出力
==================

ログ出力
--------

::

    import org.apache.logging.log4j.LogManager
    def logger = LogManager.getLogger("script")

    logger.debug("Debug message: {}", data.id)
    logger.info("Processing document: {}", data.title)
    logger.warn("Warning: {}", message)
    logger.error("Error: {}", e.message)

デバッグ用の出力
----------------

::

    // コンソール出力（開発時のみ）
    println "data.id = ${data.id}"
    println "data.title = ${data.title}"

ベストプラクティス
==================

1. **シンプルに保つ**: 複雑なロジックは避け、読みやすいコードを心がける
2. **nullチェック**: ``?.`` 演算子や ``?:`` 演算子を活用
3. **例外処理**: 適切なtry-catchで予期しないエラーに対応
4. **ログ出力**: デバッグしやすいようにログを出力
5. **パフォーマンス**: 外部リソースアクセスを最小化

参考情報
========

- `Groovy公式ドキュメント <https://groovy-lang.org/documentation.html>`__
- :doc:`scripting-overview` - スクリプティング概要
- :doc:`../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../admin/scheduler-guide` - スケジューラー設定ガイド
