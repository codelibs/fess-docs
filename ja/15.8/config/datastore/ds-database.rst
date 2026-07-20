========================================
データベースコネクタ（データベース検索）
========================================

概要
====

データベースコネクタは、JDBC 対応のリレーショナルデータベース（MySQL・PostgreSQL・Oracle・SQL Server など）のレコードを |Fess| のインデックスに登録し、データベース検索（データベースの全文検索）を実現する機能です。SELECT 文で取得した各列を検索フィールドにマッピングして登録します。

データベースコネクタは、JDBC対応のリレーショナルデータベースからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-db`` プラグインが必要です。

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

1. ``fess-ds-db`` プラグインのインストールが必要です
2. 接続先データベースに対応したJDBCドライバーが必要です
3. データベースへの読み取りアクセス権が必要です
4. 大量のデータを取得する場合、適切なクエリ設計が重要です

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # 配置
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 管理画面からインストール

1. 「システム」→「プラグイン」を開く
2. JARファイルをアップロード
3. |Fess| を再起動

JDBCドライバーのインストール
----------------------------

接続先データベースに対応したJDBCドライバーを |Fess| のクラスパス（ ``app/WEB-INF/lib/`` ディレクトリ）に配置します:

::

    # 例: MySQLドライバー
    cp mysql-connector-j-8.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp mysql-connector-j-8.x.x.jar /usr/share/fess/app/WEB-INF/lib/

JDBCドライバーを配置したら |Fess| を再起動して読み込みます。

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
   :widths: 20 10 70

   * - パラメーター
     - 必須
     - 説明
   * - ``driver``
     - はい
     - JDBCドライバーのクラス名（未指定の場合 ``DataStoreException`` が発生）
   * - ``url``
     - はい
     - JDBC接続URL（接続に必須）
   * - ``sql``
     - はい
     - データ取得用のSQLクエリ（未指定の場合 ``DataStoreException`` が発生）
   * - ``username``
     - いいえ
     - データベースユーザー名
   * - ``password``
     - いいえ
     - データベースパスワード
   * - ``fetch_size``
     - いいえ
     - JDBCフェッチサイズ。MySQLのストリーミング結果セットには ``MIN_VALUE`` を指定
   * - ``default_mimetype``
     - いいえ
     - BLOB・バイナリ列のコンテンツ抽出時に使用するデフォルトMIMEタイプ
   * - ``column_label.mimetype``
     - いいえ
     - BLOB・バイナリ列の抽出に使用するMIMEタイプを格納した列名を指定（例: ``column_label.mimetype=content_type``）
   * - ``column_label.filename``
     - いいえ
     - BLOB・バイナリ列の抽出に使用するファイル名を格納した列名を指定（拡張子からMIMEタイプを推定）
   * - ``info.*``
     - いいえ
     - 追加のJDBC接続プロパティ（例: ``info.ssl=true``）。\ ``info.`` を除いたキーがJDBCドライバーへ渡されます
   * - ``readInterval``
     - いいえ
     - 各行の処理間の遅延（ミリ秒）。デフォルト: 0
   * - ``script_type``
     - いいえ
     - スクリプトエンジンの種類。デフォルト: groovy

スクリプト設定
--------------

SQLの列名をインデックスフィールドにマッピングします:

::

    url="https://example.com/articles/" + id
    title=title
    content=content
    lastModified=updated_at

利用可能なフィールド:

- ``<column_name>`` - SQLクエリの結果列（カラムラベル名で直接アクセスします。\ ``data.`` のような接頭辞は付きません）

.. note::
   列名は ``SELECT`` 句のカラムラベル（別名）と一致させる必要があります。
   集計関数や式を使用する場合は ``AS`` で明示的に別名を付けてください
   （例: ``COUNT(*) AS total``）。

BLOB・バイナリデータの取り込み
==============================

BLOB、CLOB、NCLOB、バイト配列、バイナリストリームなどの列は、自動的に
コンテンツ抽出処理（ファイルクロールと同じ抽出器）にかけられ、テキストとして
取り込まれます。配列型の列はスペース区切りの文字列に変換されます。NULL値は
空文字列になります。

BLOBやバイナリストリームから正しくテキストを抽出するには、データの種類（MIMEタイプ）を
判定する必要があります。判定には次の優先順位が使われます:

1. ``column_label.mimetype=<列名>`` - 指定した列の値をMIMEタイプとして使用
2. ``column_label.filename=<列名>`` - 指定した列の値をファイル名として扱い、拡張子からMIMEタイプを推定
3. ``default_mimetype`` - 上記で判定できない場合に使用するデフォルトMIMEタイプ

例（``file_data`` 列のBLOBを、``content_type`` 列のMIMEタイプを使って抽出）:

::

    sql=SELECT id, title, file_data, content_type FROM documents
    column_label.mimetype=content_type

SQLクエリの設計
===============

効率的なクエリ
--------------

大量のデータを扱う場合、クエリのパフォーマンスが重要です。
SQLはそのままデータベースに送信されます（パラメーターバインドは行われません）:

::

    SELECT id, title, content, url, updated_at
    FROM articles
    WHERE updated_at >= '2024-01-01 00:00:00'
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
    url="https://example.com/article/" + id

    # 複数フィールドの組み合わせ
    url="https://example.com/" + category + "/" + slug

    # データベースに格納されたURLを使用
    url=url

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

    url="https://shop.example.com/product/" + id
    title=name
    content=description + " カテゴリ: " + category + " 価格: " + price + "円"
    lastModified=updated_at

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

    url="https://kb.example.com/article/" + id
    title=title
    content=body
    digest=tags
    author=author
    created=created_at
    lastModified=updated_at

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
- :doc:`../crawler-basic`
- :doc:`../search-basic`
