==================================
CSVコネクタ
==================================

概要
====

CSVコネクタは、CSVファイルからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-csv`` プラグインが必要です。

前提条件
========

1. プラグインのインストールが必要です
2. CSVファイルへのアクセス権が必要です
3. CSVファイルの文字エンコーディングを把握している必要があります

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-csv/X.X.X/fess-ds-csv-X.X.X.jar

    # 配置
    cp fess-ds-csv-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-csv-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

方法2: 管理画面からインストール

1. 「システム」→「プラグイン」を開く
2. JARファイルをアップロード
3. |Fess| を再起動

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
     - Products CSV
   * - ハンドラ名
     - CsvDataStore
   * - 有効
     - オン

パラメーター設定
----------------

ローカルファイル:

::

    file_path=/path/to/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

HTTPファイル:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

複数ファイル:

::

    file_path=/path/to/data1.csv,/path/to/data2.csv,https://example.com/data3.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``file_path``
     - はい
     - CSVファイルのパス（ローカル、HTTP、複数指定可：カンマ区切り）
   * - ``encoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）
   * - ``has_header``
     - いいえ
     - ヘッダー行の有無（デフォルト: true）
   * - ``separator``
     - いいえ
     - 区切り文字（デフォルト: カンマ ``,``）
   * - ``quote``
     - いいえ
     - 引用符（デフォルト: ダブルクォート ``"``）

スクリプト設定
--------------

ヘッダーありの場合:

::

    url="https://example.com/product/" + data.product_id
    title=data.product_name
    content=data.description
    digest=data.category
    price=data.price

ヘッダーなしの場合（列インデックス指定）:

::

    url="https://example.com/product/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``data.<列名>`` - ヘッダー行の列名（has_header=true の場合）
- ``data.col<N>`` - 列インデックス（has_header=false の場合、0始まり）

CSV形式の詳細
=============

標準CSV（RFC 4180準拠）
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

セパレーターの変更
------------------

タブ区切り（TSV）:

::

    # パラメーター
    separator=\t

セミコロン区切り:

::

    # パラメーター
    separator=;

カスタム引用符
--------------

シングルクォート:

::

    # パラメーター
    quote='

エンコーディング
----------------

日本語ファイル（Shift_JIS）:

::

    encoding=Shift_JIS

日本語ファイル（EUC-JP）:

::

    encoding=EUC-JP

使用例
======

製品カタログのCSV
-----------------

CSVファイル（products.csv）:

::

    product_id,name,description,price,category,in_stock
    1001,ノートPC,高性能ノートパソコン,120000,パソコン,true
    1002,マウス,ワイヤレスマウス,2500,周辺機器,true
    1003,キーボード,メカニカルキーボード,8500,周辺機器,false

パラメーター:

::

    file_path=/var/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

スクリプト:

::

    url="https://shop.example.com/product/" + data.product_id
    title=data.name
    content=data.description + " カテゴリ: " + data.category + " 価格: " + data.price + "円"
    digest=data.category
    price=data.price

在庫情報のフィルタリング:

::

    if (data.in_stock == "true") {
        url="https://shop.example.com/product/" + data.product_id
        title=data.name
        content=data.description
        price=data.price
    }

社員名簿のCSV
-------------

CSVファイル（employees.csv）:

::

    emp_id,name,department,email,phone,position
    E001,山田太郎,営業部,yamada@example.com,03-1234-5678,部長
    E002,佐藤花子,開発部,sato@example.com,03-2345-6789,マネージャー
    E003,鈴木一郎,総務部,suzuki@example.com,03-3456-7890,担当者

パラメーター:

::

    file_path=/var/data/employees.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

スクリプト:

::

    url="https://intranet.example.com/employee/" + data.emp_id
    title=data.name + " (" + data.department + ")"
    content="部署: " + data.department + "\n役職: " + data.position + "\nメール: " + data.email + "\n電話: " + data.phone
    digest=data.department

ヘッダーなしのCSV
-----------------

CSVファイル（data.csv）:

::

    1,商品A,これは商品Aです,1000
    2,商品B,これは商品Bです,2000
    3,商品C,これは商品Cです,3000

パラメーター:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=false
    separator=,
    quote="

スクリプト:

::

    url="https://example.com/item/" + data.col0
    title=data.col1
    content=data.col2
    price=data.col3

複数CSVファイルの統合
---------------------

パラメーター:

::

    file_path=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

スクリプト:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

HTTPからCSVを取得
-----------------

パラメーター:

::

    file_path=https://example.com/data/products.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

スクリプト:

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description

タブ区切り（TSV）ファイル
-------------------------

TSVファイル（data.tsv）:

::

    id	title	content	category
    1	記事1	これは記事1の内容です	ニュース
    2	記事2	これは記事2の内容です	ブログ

パラメーター:

::

    file_path=/var/data/data.tsv
    encoding=UTF-8
    has_header=true
    separator=\t
    quote="

スクリプト:

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    digest=data.category

トラブルシューティング
======================

ファイルが見つからない
----------------------

**症状**: ``FileNotFoundException`` または ``No such file``

**確認事項**:

1. ファイルパスが正しいか確認（絶対パス推奨）
2. ファイルが存在するか確認
3. ファイルの読み取り権限があるか確認
4. |Fess| 実行ユーザーからアクセス可能か確認

文字化けが発生する
------------------

**症状**: 日本語が正しく表示されない

**解決方法**:

正しい文字エンコーディングを指定:

::

    # UTF-8
    encoding=UTF-8

    # Shift_JIS
    encoding=Shift_JIS

    # EUC-JP
    encoding=EUC-JP

    # Windows標準（CP932）
    encoding=Windows-31J

ファイルのエンコーディングを確認:

::

    file -i data.csv
    # または
    nkf -g data.csv

列が正しく認識されない
----------------------

**症状**: 列の区切りが正しく認識されない

**確認事項**:

1. 区切り文字が正しいか確認:

   ::

       # カンマ
       separator=,

       # タブ
       separator=\t

       # セミコロン
       separator=;

2. 引用符の設定を確認
3. CSVファイルの形式を確認（RFC 4180準拠か）

ヘッダー行の扱い
----------------

**症状**: 1行目がデータとして認識される

**解決方法**:

ヘッダー行がある場合:

::

    has_header=true

ヘッダー行がない場合:

::

    has_header=false

データが取得できない
--------------------

**症状**: クロールは成功するが件数が0

**確認事項**:

1. CSVファイルが空でないか確認
2. スクリプト設定が正しいか確認
3. 列名が正しいか確認（has_header=true の場合）
4. ログでエラーメッセージを確認

大きなCSVファイル
-----------------

**症状**: メモリ不足またはタイムアウト

**解決方法**:

1. CSVファイルを複数に分割
2. 必要な列のみをスクリプトで使用
3. |Fess| のヒープサイズを増やす
4. 不要な行をフィルタリング

改行を含むフィールド
--------------------

RFC 4180形式では、引用符で囲むことで改行を含むフィールドを扱えます:

::

    id,title,description
    1,"Product A","This is
    a multi-line
    description"
    2,"Product B","Single line"

パラメーター:

::

    file_path=/var/data/data.csv
    encoding=UTF-8
    has_header=true
    separator=,
    quote="

スクリプトの高度な使用例
========================

データの加工
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description
    price=parseInt(data.price)
    category=data.category.toLowerCase()

条件付きインデックス
--------------------

::

    # 価格が10000以上の商品のみ
    if (parseInt(data.price) >= 10000) {
        url="https://example.com/product/" + data.id
        title=data.name
        content=data.description
        price=data.price
    }

複数列の結合
------------

::

    url="https://example.com/product/" + data.id
    title=data.name
    content=data.description + "\n\n仕様:\n" + data.specs + "\n\n注意事項:\n" + data.notes
    category=data.category

日付のフォーマット
------------------

::

    url="https://example.com/article/" + data.id
    title=data.title
    content=data.content
    created=data.created_date
    # 日付形式の変換が必要な場合は追加処理

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-json` - JSONコネクタ
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `RFC 4180 - CSV形式 <https://datatracker.ietf.org/doc/html/rfc4180>`_
