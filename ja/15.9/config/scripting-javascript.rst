==================================
JavaScriptスクリプトガイド
==================================

概要
====

JavaScriptは |Fess| 15.9以降の既定のスクリプト言語です。
Sai（|Fess| がDI XMLの式判定にも利用している、CodeLibsによるNashornフォーク）上で
動作し、スクリプトは ECMAScript 6 として実行されます。識別子は ``javascript`` で、
``js`` および ``sai`` というエイリアスでも指定できます。

スクリプトの評価方法
====================

|Fess| のスクリプトエンジンは、スクリプト文字列をまず1つの「式」としてコンパイルしようと
試み、それが構文エラーになった場合にのみ「文（ステートメント）」のブロックとして
コンパイルし直します。

このため、値を返すだけの単純な式:

::

    content.length()

も、トップレベルに ``return`` 文を含むスクリプト:

::

    return container.getComponent("crawlJob").execute();

も、どちらも問題なく動作します。後者は通常のJavaScriptとしてはトップレベルの
``return`` は構文エラーですが、式としてのコンパイルに失敗するため文ブロックとして
再解釈され、有効なスクリプトとして実行されます。

データストアスクリプトのように1行が1つの式として扱われる場面では、複数の文からなる
スクリプトは使用できません。一方、スケジュールジョブのようにスクリプト全体が評価される
場面では、複数行の文や ``let`` / ``const`` の変数宣言、制御構文を自由に使用できます。

基本構文
========

変数宣言
--------

::

    // let（再代入可能な変数）
    let name = "Fess";
    let count = 100;

    // const（再代入不可な定数）
    const title = "Document Title";
    const pageNum = 1;

文字列操作
----------

::

    // テンプレートリテラル（ES6）
    const id = 123;
    const url = `https://example.com/doc/${id}`;

    // 複数行文字列（テンプレートリテラル）
    const content = `
    This is a
    multi-line string
    `;

    // 置換（正規表現を使用。ECMAScript 6には String#replaceAll はありません）
    title.replace(/old/g, "new");
    title.replace(/\s+/g, " ");  // 連続する空白を1つにまとめる

    // 分割・結合
    const tags = "tag1,tag2,tag3".split(",");
    const joined = tags.join(", ");

    // 大文字/小文字変換
    title.toUpperCase();
    title.toLowerCase();

コレクション操作
----------------

::

    // 配列
    const list = [1, 2, 3, 4, 5];
    const doubled = list.map(item => item * 2);
    const filtered = list.filter(item => item > 3);
    const total = list.reduce((sum, item) => sum + item, 0);

    // オブジェクト
    const map = { name: "Fess", version: "15.9" };
    map.name;
    map["version"];

条件分岐
--------

::

    // if-else
    if (data.status === "active") {
        return "有効";
    } else {
        return "無効";
    }

    // 三項演算子
    const result = data.count > 0 ? "あり" : "なし";

    // デフォルト値（論理OR演算子。JavaScriptにElvis演算子はありません）
    const value = data.title || "無題";

    // オプショナルチェイニング（?.）はES2020の構文のためES6では使用できません。
    // 明示的にnullチェックしてください。
    const length = (data.content != null) ? data.content.length() : 0;

ループ処理
----------

::

    // for...of（ES6）
    for (const item of items) {
        // 各要素に対する処理
    }

    // forEach（アロー関数）
    items.forEach(item => {
        // 各要素に対する処理
    });

    // 範囲を扱う場合は配列やfor文を使います（JavaScriptにGroovyの範囲式はありません）
    for (let i = 1; i <= 10; i++) {
        // ...
    }

データストアスクリプト
======================

データストア設定でのスクリプト例です。

.. note::
   データストアスクリプトでは、 ``フィールド名=式`` の各行がそれぞれ独立した1つの式として評価されます。
   そのため、 ``let`` / ``const`` による変数宣言文や、複数フィールドをまとめて設定する複数行の制御構文（ ``if`` ブロックなど）は使用できません。
   Javaクラスを利用する場合は完全修飾クラス名（FQCN）を用いて1つの式で記述し、条件分岐はフィールドごとに三項演算子で記述します（例: ``url=data.published ? data.url : null`` ）。
   また、ここで使用している変数名 ``data`` は説明用の例であり、実際の変数名は利用するデータストアコネクタによって異なります。詳細は :doc:`../admin/dataconfig-guide` を参照してください。

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
    url=data.external_url || "https://example.com/default/" + data.id

コンテンツの加工
----------------

::

    // HTMLタグの除去
    content=data.html_content.replace(/<[^>]+>/g, "")

    // 複数フィールドの結合
    content=data.title + "\n" + data.description + "\n" + data.body

    // 長さの制限
    content=data.content.length() > 10000 ? data.content.substring(0, 10000) : data.content

日付の処理
----------

::

    // 日付のパース（FQCNを使用した単一式。Java相互運用はGroovyと同じ記法）
    lastModified=new java.text.SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss").parse(data.date_string)

    // エポック秒からの変換（long型の L サフィックスは不要）
    lastModified=new Date(data.timestamp * 1000)

利用可能なオブジェクト
======================

スクリプトの実行コンテキストによって、利用可能なオブジェクトが異なります。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - コンテキスト
     - オブジェクト
     - 説明
   * - 全コンテキスト
     - ``container``
     - DIコンテナ。 ``container.getComponent("...")`` でコンポーネントにアクセスする際に使用
   * - スケジュールジョブ
     - ``executor``
     - ジョブ実行制御（ ``JobExecutor`` ）。ジョブの停止サポートに必要
   * - データストア
     - （コネクタ固有）
     - 各データストアが提供するデータレコード変数。変数名はコネクタによって異なる
   * - パスマッピング
     - ``url`` , ``matcher``
     - 変換対象のURL文字列と正規表現のマッチ結果（ ``Matcher`` ）。置換文字列が ``javascript:`` （エイリアス ``js:`` , ``sai:`` ）のように登録済みエンジン名を前置した形式のときに利用可能
   * - ドキュメントブースト
     - （ドキュメントフィールド）
     - 対象ドキュメントの各フィールドが変数として利用可能（条件式・ブースト値式で使用）

スケジュールジョブスクリプト
============================

スケジュールジョブで使用するJavaScriptスクリプトの例です。
スケジュールジョブでは ``container`` と ``executor`` が利用可能です。
``executor`` をジョブの ``execute()`` メソッドに渡すことで、ジョブの停止制御が有効になります。

.. note::
   スケジュールジョブスクリプトは、スクリプト全体が1つのスクリプトとして評価されます。
   スクリプトエンジンはまず式としてのコンパイルを試み、失敗した場合に文（ステートメント）のブロックとして再解釈するため、複数行の文や ``let`` / ``const`` 宣言、制御構文、トップレベルの ``return`` 文を使用できます（詳細は「スクリプトの評価方法」を参照）。
   以降の「Javaクラスの使用」「Fessコンポーネントへのアクセス」「エラーハンドリング」「デバッグとログ出力」の例も、この完全なスクリプトのコンテキストを前提としています。

クロールジョブの実行
--------------------

::

    return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);

条件付きクロール
----------------

::

    const cal = java.util.Calendar.getInstance();
    const hour = cal.get(java.util.Calendar.HOUR_OF_DAY);

    // 業務時間外のみクロール
    if (hour < 9 || hour >= 18) {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    }
    return "Skipped during business hours";

複数のジョブを順番に実行
------------------------

::

    const results = [];

    // サジェスト更新
    results.push(container.getComponent("suggestJob").logLevel("info").sessionId("SUGGEST").execute(executor));

    // クロール実行
    results.push(container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor));

    return results.join("\n");

Javaクラスの使用
================

JavaScriptスクリプト内では、Sai（Nashorn）のJava相互運用の仕組みにより、Javaの標準ライブラリや
|Fess| のクラスを直接利用できます。JavaScriptには ``import`` 文がないため、クラスは常に
完全修飾名（FQCN）で記述します。

::

    new java.io.File("/var/log/fess/fess.log")
    java.lang.System.getProperty("user.home")
    new org.codelibs.fess.job.IndexExportJob()

日付・時刻
----------

::

    const now = java.time.LocalDateTime.now();
    const formatted = now.format(java.time.format.DateTimeFormatter.ISO_LOCAL_DATE_TIME);

ファイル操作
------------

::

    const content = new java.lang.String(
        java.nio.file.Files.readAllBytes(java.nio.file.Paths.get("/path/to/file.txt")));

HTTP通信
--------

::

    const client = java.net.http.HttpClient.newHttpClient();
    const request = java.net.http.HttpRequest.newBuilder()
        .uri(java.net.URI.create("https://api.example.com/data"))
        .build();
    const response = client.send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
    const body = response.body();

.. warning::
   外部リソースへのアクセスはパフォーマンスに影響するため、
   必要最小限に抑えてください。

Fessコンポーネントへのアクセス
==============================

``container`` を使用してFessのコンポーネントにアクセスできます。

システムヘルパー
----------------

::

    const systemHelper = container.getComponent("systemHelper");
    const currentTime = systemHelper.getCurrentTimeAsLong();

設定値の取得
------------

::

    const fessConfig = container.getComponent("fessConfig");
    const indexName = fessConfig.getIndexDocumentUpdateIndex();

検索の実行
----------

::

    const searchHelper = container.getComponent("searchHelper");
    // 検索パラメーターを設定して検索実行

エラーハンドリング
==================

JavaScriptには ``import`` 文がないため、Groovyのような配置制約はありません。
``try-catch`` で例外を捕捉し、ジョブのエラーを制御できます。

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    try {
        return container.getComponent("crawlJob").logLevel("info").gcLogging().execute(executor);
    } catch (e) {
        logger.error("Failed to execute crawl job: {}", e.getMessage(), e);
        return "Error: " + e.getMessage();
    }

デバッグとログ出力
==================

ログ出力
--------

::

    const logger = org.apache.logging.log4j.LogManager.getLogger("script");

    logger.debug("Debug message: {}", value);
    logger.info("Processing: {}", title);
    logger.warn("Warning: {}", message);
    logger.error("Error: {}", e.getMessage(), e);

デバッグ用の出力
----------------

変数の内容を手早く確認したい場合は、 ``JSON.stringify`` で文字列化してログに出力すると便利です。

::

    logger.debug("data = {}", JSON.stringify({ id: data.id, title: data.title }));

Groovyからの移行
================

既存のGroovyスクリプトをJavaScriptに移植する際は、次の違いに注意してください。

算術演算の精度
--------------

JavaScriptの数値演算は常に倍精度浮動小数点数として扱われます。たとえば次の式は、
Groovyでは整数 ``34`` を返しますが、JavaScriptでは浮動小数点数 ``34.0`` を返します。

::

    10 * boost1 + boost2

一方、Java相互運用で呼び出すメソッドの戻り値はJava側の型がそのまま維持されるため、
``content.length()`` は引き続き整数を返します。

Groovy専用構文の書き換え
------------------------

以下のGroovy専用構文は、JavaScriptでは書き換えが必要です。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Groovy
     - JavaScript
     - 説明
   * - ``1000L``
     - ``1000``
     - long型リテラルの ``L`` サフィックスは不要（数値リテラルをそのまま記述）
   * - ``["a", "b"] as String[]``
     - ``["a", "b"]``
     - JavaScriptの配列は ``String[]`` を引数に取るメソッドに渡すと自動的にJavaの配列に変換されるため、キャストは不要

Java相互運用
------------

Java相互運用の記法自体はNashornに準じており、Groovyとほぼ変わりません。
``new java.io.File(...)`` 、 ``java.lang.System.getProperty(...)`` 、
``new org.codelibs.fess.job.IndexExportJob()`` のような完全修飾コンストラクタ呼び出しは
そのまま解決されます。

ES6構文
-------

|Fess| のJavaScriptエンジンはECMAScript 6として動作するため、 ``let`` / ``const`` 、
アロー関数、テンプレートリテラル、分割代入、 ``for...of`` 、 ``class`` などのES6構文を
利用できます。ただし、オプショナルチェイニング（ ``?.`` ）やNull合体演算子（ ``??`` ）は
ES2020以降の構文のため使用できません。

ベストプラクティス
==================

1. **シンプルに保つ**: 複雑なロジックは避け、読みやすいコードを心がける
2. **デフォルト値**: Elvis演算子の代わりに論理OR演算子（ ``||`` ）を活用する
3. **例外処理**: 適切なtry-catchで予期しないエラーに対応
4. **ログ出力**: デバッグしやすいようにログを出力
5. **パフォーマンス**: 外部リソースアクセスを最小化
6. **数値演算**: 整数を期待する箇所では、Java相互運用のメソッド呼び出し結果をそのまま利用するか、必要に応じて明示的に変換する

参考情報
========

- `MDN JavaScript リファレンス <https://developer.mozilla.org/ja/docs/Web/JavaScript>`__
- :doc:`scripting-overview` - スクリプティング概要
- :doc:`scripting-groovy` - Groovyスクリプトガイド（プラグイン）
- :doc:`../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../admin/scheduler-guide` - スケジューラー設定ガイド
