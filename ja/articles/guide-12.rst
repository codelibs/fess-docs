============================================================
第12回 SaaSデータを検索可能にする -- Salesforce・データベースとの連携シナリオ
============================================================

はじめに
========

企業の重要なデータは、ファイルサーバーやクラウドストレージだけでなく、SaaS アプリケーションやデータベースにも格納されています。
Salesforce の顧客情報、社内データベースの製品マスタ、CSV で管理されるリストデータ――これらのデータは通常、それぞれのシステム内でしか検索できません。

本記事では、SaaS やデータベースのデータを Fess のインデックスに取り込み、他のドキュメントと合わせて横断検索できるようにするシナリオを扱います。

対象読者
========

- SaaS やデータベースの情報も検索対象にしたい方
- データストアプラグインの活用方法を知りたい方
- 複数のデータソースを横断する検索基盤を構築したい方

シナリオ
========

ある営業組織では、以下のシステムにデータが分散しています。

.. list-table:: データソースの状況
   :header-rows: 1
   :widths: 20 35 45

   * - システム
     - 格納データ
     - 現状の課題
   * - Salesforce
     - 顧客情報、商談記録、活動履歴
     - Salesforce 内でしか検索できない
   * - 社内 DB
     - 製品マスタ、価格表、在庫情報
     - 専用の管理画面からしかアクセスできない
   * - CSV ファイル
     - 取引先リスト、イベント参加者リスト
     - Excel で開いて目視で探すしかない
   * - ファイルサーバー
     - 提案書、見積書、契約書
     - 既に Fess でクロール済み

目標は、これらすべてのデータを Fess で横断検索し、営業活動に必要な情報を一つの検索窓から見つけられるようにすることです。

Salesforce データの連携
========================

Salesforce のデータを Fess で検索可能にするには、Salesforce データストアプラグインを使用します。

プラグインのインストール
------------------------

1. 管理画面の ［システム］ > ［プラグイン］ を選択
2. ``fess-ds-salesforce`` をインストール

接続設定
--------

Salesforce との連携には、Connected App の設定が必要です。

**Salesforce 側の準備**

1. Salesforce の設定画面で Connected App を作成
2. OAuth 設定を有効化
3. コンシューマキーとシークレットを取得

**Fess 側の設定**

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: SalesforceDataStore を選択
3. パラメータとスクリプトの設定
4. ラベル: ``salesforce`` を設定

**パラメータの設定例**

.. code-block:: properties

    base_url=https://login.salesforce.com
    auth_type=oauth_password
    username=user@example.com
    password=your-password
    security_token=your-security-token
    client_id=your-consumer-key
    client_secret=your-consumer-secret

**スクリプトの設定例**

.. code-block:: properties

    url=url
    title=title
    content=content
    last_modified=last_modified

``auth_type`` は ``oauth_password``（ユーザー名・パスワード認証）または ``oauth_token``（JWT Bearer トークン認証）を指定します。JWT 認証の場合は ``private_key`` に RSA 秘密鍵を設定します。

対象データの選定
----------------

Salesforce には多数のオブジェクトがありますが、すべてを検索対象にする必要はありません。
営業チームが頻繁に検索するオブジェクトに絞りましょう。

.. list-table:: 対象オブジェクトの例
   :header-rows: 1
   :widths: 25 35 40

   * - オブジェクト
     - 検索対象フィールド
     - 用途
   * - Account（取引先）
     - 名前、業種、住所、説明
     - 取引先の基本情報を検索
   * - Opportunity（商談）
     - 名前、ステージ、説明、金額
     - 進行中の商談を検索
   * - Case（ケース）
     - 件名、説明、ステータス
     - 問い合わせ履歴を検索

データベースとの連携
=====================

社内データベースのデータを検索可能にするには、データベースデータストアプラグインを使用します。

プラグインのインストール
------------------------

``fess-ds-db`` プラグインをインストールします。
このプラグインは JDBC 経由で様々なデータベース（MySQL、PostgreSQL、Oracle、SQL Server など）に接続できます。

設定
----

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: DatabaseDataStore を選択
3. パラメータとスクリプトの設定
4. ラベル: ``database`` を設定

**パラメータの設定例**

.. code-block:: properties

    driver=com.mysql.cj.jdbc.Driver
    url=jdbc:mysql://db-server:3306/mydb?useSSL=true
    username=fess_reader
    password=your-password
    sql=SELECT product_id, product_name, description, price, CONCAT('https://internal-app/products/', product_id) AS url FROM products WHERE status = 'active'

**スクリプトの設定例**

.. code-block:: properties

    url=url
    title=product_name
    content=description

``sql`` に指定した SQL クエリの結果がクロールされます。スクリプトでは SQL のカラム名（またはカラムラベル）を使って Fess のインデックスフィールドにマッピングします。

SQL クエリの設計
----------------

``sql`` パラメータに指定する SQL クエリを設計する際のポイントは以下の通りです。

- 検索結果のリンク先となる ``url`` カラムを含める（例: ``CONCAT('https://.../', id) AS url``）
- 検索対象の本文となるカラムを含める
- ``WHERE`` 句で不要なデータを除外する（例: ``status = 'active'``）

スクリプトでは、SQL のカラム名をそのまま使って Fess のインデックスフィールドにマッピングします。

CSV ファイルの連携
===================

CSV ファイルのデータも検索対象にできます。

設定
----

``fess-ds-csv`` プラグインまたは CSV データストアの機能を使用します。

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: CsvDataStore を選択
3. パラメータとスクリプトの設定
4. ラベル: ``csv-data`` を設定

**パラメータの設定例**

.. code-block:: properties

    directories=/opt/fess/csv-data
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

**スクリプトの設定例**（ヘッダー行がある場合はカラム名を使用）

.. code-block:: properties

    url="https://internal-app/contacts/" + id
    title=company_name
    content=company_name + " " + contact_name + " " + email

``has_header_line=true`` の場合、ヘッダー行のカラム名をスクリプトで使用できます。ヘッダー行がない場合は ``cell1``、``cell2``、``cell3`` のように列番号で参照します。スクリプトには Groovy の式を記述でき、文字列の結合なども可能です。

CSV ファイルが定期的に更新される場合は、ファイルの配置場所を固定し、クロールスケジュールを設定することで、自動的に最新データがインデックスに反映されます。

データソースの横断検索
========================

すべてのデータソースの設定が完了したら、横断検索を体験しましょう。

検索例
------

「株式会社ABC」で検索すると、以下のような結果が返されます。

1. Salesforce の取引先情報（Account）
2. ファイルサーバーの提案書（PDF）
3. データベースの製品購入履歴
4. CSV の展示会参加者リスト

利用者は情報の所在を意識することなく、必要な情報にたどり着けます。

ラベルによる絞り込み
--------------------

検索結果が多い場合は、ラベルで絞り込みます。

- ``salesforce``: Salesforce のデータのみ
- ``database``: データベースのデータのみ
- ``csv-data``: CSV のデータのみ
- ``共有ファイル``: ファイルサーバーのドキュメントのみ

運用上の考慮点
===============

データの鮮度
------------

SaaS やデータベースのデータは頻繁に更新される可能性があります。
クロール頻度を適切に設定し、検索結果の鮮度を保ちましょう。

.. list-table:: クロール頻度の目安
   :header-rows: 1
   :widths: 25 25 50

   * - データソース
     - 推奨頻度
     - 理由
   * - Salesforce
     - 4〜6時間ごと
     - 商談・顧客情報は日中に更新される
   * - データベース
     - 2〜4時間ごと
     - 在庫情報など変動の大きいデータ
   * - CSV
     - 日次
     - 通常はバッチ処理で更新される

データベース接続のセキュリティ
------------------------------

データベースに直接接続する場合、セキュリティに十分注意してください。

- 読み取り専用のデータベースユーザーを使用
- 接続元を Fess サーバーの IP に制限
- 不要なテーブルへのアクセス権限を付与しない
- パスワードの管理に注意

まとめ
======

本記事では、Salesforce、データベース、CSV ファイルのデータを Fess で検索可能にするシナリオを扱いました。

- Salesforce データストアプラグインによる CRM データの連携
- データベースデータストアプラグインによる社内 DB の連携
- CSV データストアによるリストデータの連携
- フィールドマッピングと SQL クエリの設計
- 横断検索でのラベル活用

データサイロを解消し、あらゆる情報源を横断検索できる環境が実現します。
実践ソリューション編はここまでです。次回からはアーキテクチャ・スケーリング編として、マルチテナント設計を扱います。

参考資料
========

- `Fess データストア設定 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess プラグイン管理 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
