==================================
データベースコネクタ
==================================

概要
====

データベースコネクタは、JDBC対応のリレーショナルデータベースからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能は |Fess| に組み込まれており、追加のプラグインは不要です。

対応データベース
================

JDBC対応のすべてのデータベースに対応しています。主な例:

- MySQL / MariaDB
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
- SQLite
- H2 Database

前提条件
========

1. JDBCドライバーが必要です
2. データベースへの読み取りアクセス権が必要です
3. 大量のデータを取得する場合、適切なクエリ設計が重要です

JDBCドライバーのインストール
----------------------------

JDBCドライバーを ``lib/`` ディレクトリに配置します:

::

    # 例: MySQLドライバー
    cp mysql-connector-java-8.0.33.jar /path/to/fess/lib/

|Fess| を再起動してドライバーを読み込みます。

設定方法
========

管理画面から「クローラー」→「データストア」→「新規作成」で設定します。

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 設定例
   * - 名前
     - Products Database
   * - ハンドラ名
     - DatabaseDataStore
   * - 有効
     - オン

パラメーター設定
----------------

MySQL/MariaDBの例:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=UTC
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = 0

PostgreSQLの例:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/mydb
    username=fess_user
    password=your_password
    sql=SELECT id, title, content, url, updated_at FROM articles WHERE deleted = false

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``driver``
     - はい
     - JDBCドライバーのクラス名
   * - ``url``
     - はい
     - JDBC接続URL
   * - ``username``
     - はい
     - データベースユーザー名
   * - ``password``
     - はい
     - データベースパスワード
   * - ``sql``
     - はい
     - データ取得用のSQLクエリ
   * - ``fetch.size``
     - いいえ
     - フェッチサイズ（デフォルト: 100）

スクリプト設定
--------------

SQLの列名をインデックスフィールドにマッピングします:

::

    url="https://example.com/articles/" + data.id
    title=data.title
    content=data.content
    lastModified=data.updated_at

利用可能なフィールド:

- ``data.<column_name>`` - SQLクエリの結果列

SQLクエリの設計
===============

効率的なクエリ
--------------

大量のデータを扱う場合、クエリのパフォーマンスが重要です:

::

    # インデックスを使用した効率的なクエリ
    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= :last_crawl_date
    ORDER BY id

差分クロール
------------

更新されたレコードのみを取得する方法:

::

    # 更新日時でフィルタリング
    sql=SELECT * FROM articles WHERE updated_at >= '2024-01-01 00:00:00'

    # IDによる範囲指定
    sql=SELECT * FROM articles WHERE id > 10000

URLの生成
---------

ドキュメントのURLはスクリプトで生成します:

::

    # 固定パターン
    url="https://example.com/article/" + data.id

    # 複数フィールドの組み合わせ
    url="https://example.com/" + data.category + "/" + data.slug

    # データベースに格納されたURLを使用
    url=data.url

マルチバイト文字対応
====================

日本語などのマルチバイト文字を含むデータを扱う場合:

MySQL
-----

::

    url=jdbc:mysql://localhost:3306/mydb?useUnicode=true&characterEncoding=UTF-8

PostgreSQL
----------

PostgreSQLは通常UTF-8がデフォルトです。必要に応じて:

::

    url=jdbc:postgresql://localhost:5432/mydb?charSet=UTF-8

接続プーリング
==============

大量のデータを処理する場合、接続プーリングを検討してください:

::

    # HikariCP使用時の設定
    datasource.class=com.zaxxer.hikari.HikariDataSource
    pool.size=5

セキュリティ
============

データベース認証情報の保護
--------------------------

.. warning::
   パスワードを設定ファイルに直接記述することはセキュリティリスクがあります。

推奨される方法:

1. 環境変数を使用
2. |Fess| の暗号化機能を使用
3. 読み取り専用ユーザーを使用

最小権限の原則
--------------

データベースユーザーには必要最小限の権限のみを付与します:

::

    -- MySQLの例
    CREATE USER 'fess_user'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT ON mydb.articles TO 'fess_user'@'localhost';

使用例
======

製品カタログの検索
------------------

パラメーター:

::

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://localhost:3306/shop
    username=fess_user
    password=password
    sql=SELECT p.id, p.name, p.description, p.price, c.name as category, p.updated_at FROM products p JOIN categories c ON p.category_id = c.id WHERE p.active = 1

スクリプト:

::

    url="https://shop.example.com/product/" + data.id
    title=data.name
    content=data.description + " カテゴリ: " + data.category + " 価格: " + data.price + "円"
    lastModified=data.updated_at

ナレッジベース記事
------------------

パラメーター:

::

    driver=org.postgresql.Driver
    url=jdbc:postgresql://localhost:5432/knowledge
    username=fess_user
    password=password
    sql=SELECT id, title, body, tags, author, created_at, updated_at FROM articles WHERE published = true ORDER BY id

スクリプト:

::

    url="https://kb.example.com/article/" + data.id
    title=data.title
    content=data.body
    digest=data.tags
    author=data.author
    created=data.created_at
    lastModified=data.updated_at

トラブルシューティング
======================

JDBCドライバーが見つからない
----------------------------

**症状**: ``ClassNotFoundException`` または ``No suitable driver``

**解決方法**:

1. JDBCドライバーが ``lib/`` に配置されているか確認
2. ドライバーのクラス名が正しいか確認
3. |Fess| を再起動

接続エラー
----------

**症状**: ``Connection refused`` または認証エラー

**確認事項**:

1. データベースが起動しているか
2. ホスト名、ポート番号が正しいか
3. ユーザー名、パスワードが正しいか
4. ファイアウォール設定

クエリエラー
------------

**症状**: ``SQLException`` やSQLシンタックスエラー

**確認事項**:

1. SQLクエリを直接データベースで実行してテスト
2. 列名が正しいか確認
3. テーブル名が正しいか確認

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-csv` - CSVコネクタ
- :doc:`ds-json` - JSONコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
