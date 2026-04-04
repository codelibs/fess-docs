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

    files=/path/to/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

複数ファイル:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``files``
     - はい
     - CSVファイルのパス（ローカル、複数指定可：カンマ区切り）
   * - ``file_encoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）
   * - ``has_header_line``
     - いいえ
     - ヘッダー行の有無（デフォルト: false）
   * - ``separator_character``
     - いいえ
     - 区切り文字（デフォルト: カンマ ``,``）
   * - ``quote_character``
     - いいえ
     - 引用符（デフォルト: ダブルクォート ``"``）
   * - ``directories``
     - いいえ
     - CSVファイルを含むディレクトリのパス
   * - ``escape_character``
     - いいえ
     - エスケープ文字（デフォルト: バックスラッシュ ``\``）

高度なパラメーター
~~~~~~~~~~~~~~~~~~

以下のパラメーターはCSVの解析動作を細かく制御します:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 説明
   * - ``skip_lines``
     - スキップする先頭行数
   * - ``ignore_line_patterns``
     - 無視する行の正規表現パターン
   * - ``ignore_empty_lines``
     - 空行を無視するか（デフォルト: false）
   * - ``ignore_trailing_whitespaces``
     - 末尾の空白を無視するか（デフォルト: false）
   * - ``ignore_leading_whitespaces``
     - 先頭の空白を無視するか（デフォルト: false）
   * - ``null_string``
     - null値として扱う文字列
   * - ``break_string``
     - 改行の置換文字列
   * - ``escape_disabled``
     - エスケープ処理を無効にするか（デフォルト: false）
   * - ``quote_disabled``
     - 引用符処理を無効にするか（デフォルト: false）

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

    url="https://example.com/product/" + data.cell1
    title=data.cell2
    content=data.cell3
    price=data.cell4

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``data.<列名>`` - ヘッダー行の列名（has_header_line=true の場合）
- ``data.cell<N>`` - 列インデックス（has_header_line=false の場合、``cell1``、``cell2``...のように1始まり）
- ``data.csvfile`` - 処理中のCSVファイルのフルパス
- ``data.csvfilename`` - 処理中のCSVファイル名

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
    separator_character=\t

セミコロン区切り:

::

    # パラメーター
    separator_character=;

カスタム引用符
--------------

シングルクォート:

::

    # パラメーター
    quote_character='

エンコーディング
----------------

日本語ファイル（Shift_JIS）:

::

    file_encoding=Shift_JIS

日本語ファイル（EUC-JP）:

::

    file_encoding=EUC-JP

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

    files=/var/data/products.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

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

    files=/var/data/employees.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

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

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=false
    separator_character=,
    quote_character="

スクリプト:

::

    url="https://example.com/item/" + data.cell1
    title=data.cell2
    content=data.cell3
    price=data.cell4

複数CSVファイルの統合
---------------------

パラメーター:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

スクリプト:

::

    url="https://example.com/report/" + data.id
    title=data.title
    content=data.content
    timestamp=data.date

タブ区切り（TSV）ファイル
-------------------------

TSVファイル（data.tsv）:

::

    id	title	content	category
    1	記事1	これは記事1の内容です	ニュース
    2	記事2	これは記事2の内容です	ブログ

パラメーター:

::

    files=/var/data/data.tsv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=\t
    quote_character="

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
    file_encoding=UTF-8

    # Shift_JIS
    file_encoding=Shift_JIS

    # EUC-JP
    file_encoding=EUC-JP

    # Windows標準（CP932）
    file_encoding=Windows-31J

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
       separator_character=,

       # タブ
       separator_character=\t

       # セミコロン
       separator_character=;

2. 引用符の設定を確認
3. CSVファイルの形式を確認（RFC 4180準拠か）

ヘッダー行の扱い
----------------

**症状**: 1行目がデータとして認識される

**解決方法**:

ヘッダー行がある場合:

::

    has_header_line=true

ヘッダー行がない場合:

::

    has_header_line=false

データが取得できない
--------------------

**症状**: クロールは成功するが件数が0

**確認事項**:

1. CSVファイルが空でないか確認
2. スクリプト設定が正しいか確認
3. 列名が正しいか確認（has_header_line=true の場合）
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

    files=/var/data/data.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="

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
