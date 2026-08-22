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

方法1: 管理画面からインストール

1. 「システム」→「プラグイン」を開く
2. JARファイルをアップロード
3. |Fess| を再起動

方法2: JARファイルを直接配置

::

    # CodeLibsリポジトリからダウンロード
    wget https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-db/X.X.X/fess-ds-db-X.X.X.jar

    # 配置（管理画面からのインストール先と同じディレクトリ）
    cp fess-ds-db-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # または
    cp fess-ds-db-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

JDBCドライバーのインストール
----------------------------

JDBCドライバーはプラグインに含まれていません。接続先データベースに対応したドライバーを別途入手して配置してください。

データストアクロールはクローラープロセスで実行されるため、ドライバーは **クローラープロセスのクラスパス** に置く必要があります。次のいずれかのディレクトリが該当します:

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

::

    # 例: MySQLドライバー
    cp mysql-connector-j-9.x.x.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp mysql-connector-j-9.x.x.jar /usr/share/fess/app/WEB-INF/lib/

JDBCドライバーを配置したら |Fess| を再起動して読み込みます。

.. note::
   ドライバーが見つからない場合、クロールは
   ``The JDBC driver ... is not on the crawler classpath.`` というメッセージで失敗します。

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
     - JDBCフェッチサイズ。``MIN_VALUE`` はMySQLで結果セットを1行ずつ読み込ませるための指定で、他のドライバーは負の値を受け付けません（警告を出してドライバー既定値で継続します）。負の値や数値以外は警告を出して無視されます
   * - ``query_timeout``
     - いいえ
     - クエリのタイムアウト（秒）。``0`` は無制限（JDBCの既定）。未指定の場合はタイムアウトを設定しません
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

.. note::
   クエリがハングした場合、ジョブを停止してもクローラースレッドは解放されません。
   ジョブの停止は行と行の間でしか判定されないため、ドライバー内部でブロックしている
   呼び出しには効きません。長時間実行の可能性があるクエリには ``query_timeout``
   を設定してください。

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
- ``crawlingConfig`` - データストア設定
- ``crawlingContext`` - クロール中のコンテキスト。``crawlingContext.doc`` で構築中のドキュメントを参照できます

.. note::
   列名は ``SELECT`` 句のカラムラベル（別名）と一致させる必要があります。
   集計関数や式を使用する場合は ``AS`` で明示的に別名を付けてください
   （例: ``COUNT(*) AS total``）。

.. note::
   カラムラベルの大文字・小文字はデータベースによって異なります。PostgreSQLは
   引用符で囲まない識別子を小文字に、H2は大文字に変換し、MySQLは宣言どおりに
   返します。スクリプトで参照した名前が解決できない場合、そのフィールドは
   何も設定されずに終わります（エラーにはなりません）。移植性を重視する場合は
   ``AS`` で明示的に別名を付けてください。

.. warning::
   スクリプトからは、SQLの結果列だけでなく **データストアパラメーター全体** が
   同名の変数として参照できます。``driver`` ・ ``url`` ・ ``username`` ・
   ``password`` ・ ``sql`` なども変数として見えるため、これらと同じ名前の列を
   意図せず上書きしたり、逆に列が無いときにパラメーターの値が入り込んだり
   します。同名の列がある場合は列の値が優先されます。

BLOB・バイナリデータの取り込み
==============================

バイナリ列（BLOB・ ``BYTEA`` ・バイト配列・バイナリストリーム）は、コンテンツ抽出処理
（ファイルクロールと同じ抽出器）にかけられ、テキストとして取り込まれます。

一方、CLOB・NCLOB・文字ストリームは **抽出器を通らず** 、文字列としてそのまま
読み込まれます。MIMEタイプの指定（後述）はこれらには適用されません。

配列型の列は要素をスペースで連結した文字列になります。NULL値は空文字列になります。

.. note::
   同じBLOB列でも、JDBCドライバーによって ``java.sql.Blob`` を返すものと
   バイト配列を返すものがあります（MySQLとPostgreSQLはバイト配列）。
   どちらの場合も同じように抽出されます。

.. note::
   CLOB・NCLOBはサイズ上限なしでメモリに読み込まれます。非常に大きな
   テキスト列を扱う場合は、SQL側で ``SUBSTRING`` などを使って切り詰めることを
   検討してください。抽出器を通る経路にはクローラーの最大サイズ設定が適用されます。

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

.. warning::
   このようにクエリを絞り込んでも、差分クロールになるわけではありません。
   クロールが完了すると、|Fess| は今回のクロールに含まれなかった
   このデータストア設定のドキュメントをインデックスから削除するため、
   条件に一致した行だけがインデックスに残ります。

   以前のクロールで登録したドキュメントを残す場合は、データストアパラメーターに
   ``delete_old_docs=false`` を追加してください。この場合、データベースから削除された
   行に対応するドキュメントもインデックスから削除されなくなるため、定期的に
   全件クロールを実行してください。

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

.. warning::
   ``url=url`` は、``SELECT`` の結果に ``url`` というラベルの列がある場合にのみ
   意図どおりに動きます。該当する列が無いと、同名のデータストアパラメーター、
   すなわち **JDBC接続URL** がドキュメントのURLとして設定されます。
   列名が異なる場合は ``SELECT page_url AS url`` のように別名を付けるか、
   ``url=page_url`` のようにスクリプト側で列名を指定してください。

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

1. 自動暗号化を利用する

   ``app.encrypt.property.pattern`` （デフォルト ``.*password|.*key|.*token|.*secret`` ）
   に一致するパラメーター名の値は、管理画面から保存すると自動的に暗号化され、
   ``{cipher}`` 接頭辞付きで保存されます。``password`` はこのパターンに一致するため、
   管理画面から設定していれば平文では保存されません。

2. 環境変数を使用する

   ``FESS_ENV_`` で始まる環境変数は、データストアパラメーターの中で
   ``${環境変数名}`` として展開されます:

   ::

       password=${FESS_ENV_DB_PASSWORD}

   展開対象となる環境変数名のパターンは ``crawler.data.env.param.key.pattern``
   （デフォルト ``^FESS_ENV_.*`` ）で設定します。

3. 読み取り専用ユーザーを使用する

.. note::
   ``org.codelibs.fess.ds`` のログレベルをDEBUGにしても、パスワードなど
   ``app.encrypt.property.pattern`` に一致するパラメーターの値と、JDBC接続URLに
   埋め込まれた資格情報はマスクされて出力されます。

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

クロールが失敗したときは、まずログのメッセージで原因を切り分けます。

JDBCドライバーが見つからない
----------------------------

**症状**: ``The JDBC driver ... is not on the crawler classpath.``

**解決方法**:

1. JDBCドライバーが ``app/WEB-INF/lib/`` または ``app/WEB-INF/env/crawler/lib/`` に配置されているか確認
2. ``driver`` に指定したクラス名が正しいか確認
3. |Fess| を再起動

接続エラー
----------

**症状**: ``Failed to connect to <URL>.``

**確認事項**:

1. データベースが起動しているか
2. ホスト名、ポート番号が正しいか
3. ユーザー名、パスワードが正しいか
4. ファイアウォール設定

クエリエラー
------------

**症状**: ``Failed to execute the query.``

**確認事項**:

1. SQLクエリを直接データベースで実行してテスト
2. 列名が正しいか確認
3. テーブル名が正しいか確認

設定漏れ
--------

**症状**: ``The driver parameter is required.`` ・ ``The url parameter is required.`` ・ ``The sql parameter is required.``

必須パラメーターが設定されていません。パラメーター欄を確認してください。

一部の行だけ失敗する
--------------------

行単位の失敗はクロールを中断せず、「システム」→「障害URL」に記録されます。
スクリプトがURLを生成できていればそのURLで、生成前に失敗した場合は
``datastore://<データストア設定ID>/<行番号>`` として記録されます。

検索結果に出てこない
--------------------

1. スクリプトで ``url`` と ``title`` ・ ``content`` が設定されているか確認
2. カラムラベルの大文字・小文字がスクリプトと一致しているか確認（「スクリプト設定」を参照）
3. クロールジョブのログでドキュメント数を確認

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-csv` - CSVコネクタ
- :doc:`ds-json` - JSONコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../crawler-basic`
- :doc:`../search-basic`
