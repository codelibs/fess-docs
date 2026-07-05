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
    quote_disabled=false

複数ファイル:

::

    files=/path/to/data1.csv,/path/to/data2.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,
    quote_character="
    quote_disabled=false

.. note::

   引用符（クォート）処理とエスケープ処理は、デフォルトでは **無効** になっています。
   引用符で囲まれたフィールド内に区切り文字や改行を含むCSV（RFC 4180準拠）を扱う場合は、
   ``quote_disabled=false`` を明示的に指定して引用符処理を有効にしてください。
   詳細は後述の「引用符・エスケープ処理の有効化」を参照してください。

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``files``
     - いいえ
     - CSVファイルのパス（ローカルパス、複数指定可：カンマ区切り）。 ``files`` または ``directories`` のいずれかの指定が必要です。両方指定した場合は ``files`` が優先されます。指定するファイルは拡張子が ``.csv`` または ``.tsv`` である必要があり、それ以外の拡張子のファイルはスキップされます。
   * - ``directories``
     - いいえ
     - CSVファイルを含むディレクトリのパス（複数指定可：カンマ区切り）。ディレクトリ内の ``.csv`` および ``.tsv`` ファイルのみが対象となります。 ``files`` が指定されていない場合に使用されます。
   * - ``file_encoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）
   * - ``has_header_line``
     - いいえ
     - ヘッダー行の有無（デフォルト: false）
   * - ``separator_character``
     - いいえ
     - 区切り文字（デフォルト: カンマ ``,``）。 ``\t`` のようなエスケープシーケンスを指定できます（タブ区切り）。
   * - ``quote_character``
     - いいえ
     - 引用符（デフォルト: ダブルクォート ``"``）。ただし引用符処理はデフォルトで無効です（ ``quote_disabled`` を参照）。
   * - ``escape_character``
     - いいえ
     - エスケープ文字（デフォルト: バックスラッシュ ``\``）。ただしエスケープ処理はデフォルトで無効です（ ``escape_disabled`` を参照）。

.. note::

   ``files`` および ``directories`` の両方が空の場合はエラー（ ``DataStoreException`` ）となります。
   どちらか一方を必ず指定してください。

高度なパラメーター
~~~~~~~~~~~~~~~~~~

以下のパラメーターはCSVの解析動作を細かく制御します:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 説明
   * - ``quote_disabled``
     - 引用符（クォート）処理を無効にするか（デフォルト: true）。RFC 4180準拠の引用符付きフィールドを扱う場合は ``false`` を指定します。
   * - ``escape_disabled``
     - エスケープ処理を無効にするか（デフォルト: true）。 ``escape_character`` によるエスケープを有効にする場合は ``false`` を指定します。
   * - ``skip_lines``
     - スキップする先頭行数（デフォルト: 0）
   * - ``ignore_line_patterns``
     - 無視する行の正規表現パターン（例: ``^#.*`` でコメント行を無視）
   * - ``ignore_empty_lines``
     - 空行を無視するか（デフォルト: false）
   * - ``ignore_trailing_whitespaces``
     - 末尾の空白を無視するか（デフォルト: false）
   * - ``ignore_leading_whitespaces``
     - 先頭の空白を無視するか（デフォルト: false）
   * - ``null_string``
     - null値として扱う文字列
   * - ``break_string``
     - フィールド値中の改行を置換する文字列
   * - ``readInterval``
     - 1レコードを処理するごとの待機時間（ミリ秒）（デフォルト: 0）

スクリプト設定
--------------

各フィールドの値は、CSVの各列の値を参照して組み立てます。CSVの列はスクリプト内で
**接頭辞なしの変数** として直接参照できます（ ``data.`` のような接頭辞は付きません）。

ヘッダーありの場合（列名で参照）:

::

    url="https://example.com/product/" + product_id
    title=product_name
    content=description
    digest=category
    price=price

ヘッダーなしの場合（列インデックスで参照）:

::

    url="https://example.com/product/" + cell1
    title=cell2
    content=cell3
    price=cell4

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``<列名>`` - ヘッダー行の列名で直接参照します（ ``has_header_line=true`` の場合のみ。列名が空白でない場合に有効）
- ``cell<N>`` - 列インデックスで参照します（ ``cell1``、``cell2``...のように1始まり。ヘッダーの有無に関わらず利用可能）
- ``csvfile`` - 処理中のCSVファイルのフルパス
- ``csvfilename`` - 処理中のCSVファイル名

.. note::

   列名にスペースやハイフンなど、Groovyの識別子として無効な文字が含まれる場合は、
   列名での参照ができません。その場合は ``cell<N>`` を使用してください。

CSV形式の詳細
=============

標準CSV（RFC 4180準拠）
-----------------------

::

    product_id,product_name,description,price,category
    1,Laptop,High-performance laptop,150000,Electronics
    2,Mouse,Wireless mouse,3000,Electronics
    3,"Book, Programming","Learn to code",2800,Books

.. note::

   上記の ``"Book, Programming"`` のように、引用符で囲んでフィールド内に区切り文字を
   含めるには ``quote_disabled=false`` を指定して引用符処理を有効にする必要があります。
   引用符処理が無効（デフォルト）の場合、引用符は通常の文字として扱われ、
   フィールドは区切り文字で分割されます。

引用符・エスケープ処理の有効化
------------------------------

引用符処理とエスケープ処理はデフォルトで無効です。以下のように明示的に有効化します。

引用符処理を有効にする:

::

    # パラメーター
    quote_disabled=false
    quote_character="

エスケープ処理を有効にする:

::

    # パラメーター
    escape_disabled=false
    escape_character=\

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

シングルクォート（引用符処理の有効化が必要）:

::

    # パラメーター
    quote_disabled=false
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

スクリプト:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " カテゴリ: " + category + " 価格: " + price + "円"
    digest=category
    price=price

在庫情報のフィルタリング:

::

    url=in_stock == "true" ? "https://shop.example.com/product/" + product_id : null
    title=in_stock == "true" ? name : null
    content=in_stock == "true" ? description : null
    price=in_stock == "true" ? price : null

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

スクリプト:

::

    url="https://intranet.example.com/employee/" + emp_id
    title=name + " (" + department + ")"
    content="部署: " + department + "\n役職: " + position + "\nメール: " + email + "\n電話: " + phone
    digest=department

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

スクリプト:

::

    url="https://example.com/item/" + cell1
    title=cell2
    content=cell3
    price=cell4

複数CSVファイルの統合
---------------------

パラメーター:

::

    files=/var/data/2024-01.csv,/var/data/2024-02.csv,/var/data/2024-03.csv
    file_encoding=UTF-8
    has_header_line=true
    separator_character=,

スクリプト:

::

    url="https://example.com/report/" + id
    title=title
    content=content
    timestamp=date

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

スクリプト:

::

    url="https://example.com/article/" + id
    title=title
    content=content
    digest=category

トラブルシューティング
======================

ファイルが見つからない
----------------------

**症状**: クロールが実行されるがファイルが処理されない、ログに ``is not found`` が出力される

**確認事項**:

1. ファイルパスが正しいか確認（絶対パス推奨）
2. ファイルが存在するか確認
3. ファイルの拡張子が ``.csv`` または ``.tsv`` であるか確認（それ以外の拡張子はスキップされます）
4. ファイルの読み取り権限があるか確認
5. |Fess| 実行ユーザーからアクセス可能か確認

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

**症状**: 列の区切りが正しく認識されない、または引用符で囲んだフィールドが分割される

**確認事項**:

1. 区切り文字が正しいか確認:

   ::

       # カンマ
       separator_character=,

       # タブ
       separator_character=\t

       # セミコロン
       separator_character=;

2. 引用符付きフィールド（フィールド内に区切り文字を含む）を扱う場合は、引用符処理を有効にする:

   ::

       quote_disabled=false

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
2. スクリプト設定が正しいか確認（列名・ ``cell<N>`` の参照が ``data.`` 接頭辞なしになっているか）
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

RFC 4180形式では、引用符で囲むことで改行を含むフィールドを扱えます。
引用符処理はデフォルトで無効のため、 ``quote_disabled=false`` の指定が必要です:

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
    quote_disabled=false
    quote_character="

CsvListDataStore
=================

``fess-ds-csv`` プラグインには、 ``CsvDataStore`` に加えて ``CsvListDataStore`` ハンドラも含まれています。

``CsvListDataStore`` は ``CsvDataStore`` を拡張し、以下の追加機能を提供します:

- マルチスレッド処理（ ``numOfThreads`` パラメーターで制御）
- 処理済みCSVファイルの自動削除
- タイムスタンプベースのファイルフィルタリング（書き込み中のファイルをスキップ）

``CsvDataStore`` のすべてのパラメーターおよびスクリプト設定がそのまま利用できます。

基本設定
--------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 設定例
   * - ハンドラ名
     - CsvListDataStore

追加パラメーター
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``timestamp_margin``
     - いいえ
     - ファイルの最終更新時刻からの経過時間（ミリ秒）。この時間が経過していないファイルは、書き込み中とみなしてスキップされます（デフォルト: 10000）
   * - ``numOfThreads``
     - いいえ
     - 処理スレッド数（デフォルト: 1）

.. note::

   ``CsvListDataStore`` は処理完了後にCSVファイルを自動的に削除します。処理中にエラーが発生した場合、ファイルは ``.txt`` にリネームされます（リネームに失敗した場合は削除されます）。

スクリプトの高度な使用例
========================

データの加工
------------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=Integer.parseInt(price)
    category=category.toLowerCase()

条件付きインデックス
--------------------

::

    // 価格が10000以上の商品のみインデックス
    url=Integer.parseInt(price) >= 10000 ? "https://example.com/product/" + id : null
    title=Integer.parseInt(price) >= 10000 ? name : null
    content=Integer.parseInt(price) >= 10000 ? description : null
    price=Integer.parseInt(price) >= 10000 ? price : null

複数列の結合
------------

::

    url="https://example.com/product/" + id
    title=name
    content=description + "\n\n仕様:\n" + specs + "\n\n注意事項:\n" + notes
    category=category

日付のフォーマット
------------------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    created=created_date
    // 日付形式の変換が必要な場合は追加処理

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-json` - JSONコネクタ
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `RFC 4180 - CSV形式 <https://datatracker.ietf.org/doc/html/rfc4180>`_
