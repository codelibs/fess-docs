==================================
JSONコネクタ
==================================

概要
====

JSONコネクタは、ローカルのJSONLファイル（JSON Lines形式）からデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-json`` プラグインが必要です。

前提条件
========

1. プラグインのインストールが必要です
2. JSONファイルへのアクセス権が必要です
3. JSONの構造を理解している必要があります

プラグインのインストール
------------------------

方法1: JARファイルを直接配置

::

    # Maven Centralからダウンロード
    wget https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 配置
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/lib/
    # または
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/lib/

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
     - Products JSON
   * - ハンドラ名
     - JsonDataStore
   * - 有効
     - オン

パラメーター設定
----------------

ローカルファイル:

::

    files=/path/to/data.json
    fileEncoding=UTF-8

複数ファイル:

::

    files=/path/to/data1.json,/path/to/data2.json
    fileEncoding=UTF-8

ディレクトリ指定:

::

    directories=/path/to/json_dir/
    fileEncoding=UTF-8

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - パラメーター
     - 必須
     - 説明
   * - ``files``
     - いいえ
     - 処理するJSONファイルのパス（複数指定可：カンマ区切り）。 ``.json`` または ``.jsonl`` 拡張子のファイルのみ処理されます。
   * - ``directories``
     - いいえ
     - JSONファイルを含むディレクトリのパス（複数指定可：カンマ区切り）
   * - ``fileEncoding``
     - いいえ
     - 文字エンコーディング（デフォルト: UTF-8）

.. warning::
   ``files`` または ``directories`` のいずれかを指定する必要があります。
   両方が未指定（空）の場合、 ``DataStoreException`` が発生します。
   両方を指定した場合、 ``files`` が優先され ``directories`` は無視されます。

.. note::
   パラメーター名はキャメルケースの ``fileEncoding`` です（スネークケースの ``file_encoding`` ではありません）。

ディレクトリ指定時の動作
~~~~~~~~~~~~~~~~~~~~~~~~~~

``directories`` を指定した場合、各ディレクトリ直下のファイルが以下の規則で処理されます。

- **サブディレクトリは走査されません**（再帰的な探索は行いません）。
- 拡張子が ``.json`` または ``.jsonl`` のファイルのみが対象です（大文字小文字は区別しません）。
- ファイルは更新日時（最終更新時刻）の昇順で処理されます。

.. note::
   このコネクタはローカルファイルシステム上のJSONファイルのみを対象とし、HTTPアクセスやAPI認証機能はサポートしていません。

スクリプト設定
--------------

各フィールドの値は、JSONオブジェクトの各フィールドの値を参照して組み立てます。
JSONオブジェクトのトップレベルのフィールドは、スクリプト内で **接頭辞なしの変数**
として直接参照できます（ ``data.`` のような接頭辞は付きません）。

単純なJSONオブジェクト:

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price
    category=category

ネストしたJSONオブジェクト（ネストしたオブジェクトはマップとして参照します）:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    author=product.author.name

配列要素の処理:

::

    url="https://example.com/article/" + id
    title=title
    content=body
    tags=tags.join(", ")
    categories=categories[0].name

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``<フィールド名>`` - JSONオブジェクトのトップレベルのフィールドを名前で直接参照します
- ``<親>.<子>`` - ネストしたオブジェクトのフィールド
- ``<配列>[<インデックス>]`` - 配列要素
- ``<配列>.<メソッド>`` - 配列のメソッド（ ``join``、``collect``、``size`` など）

.. note::

   フィールド名にスペースやハイフンなど、Groovyの識別子として無効な文字が含まれる場合は、
   そのフィールドを変数名として直接参照できません。

JSON形式の詳細
==============

JSONファイル形式
----------------

JSONコネクタは、JSONL（JSON Lines）形式のファイルを読み込みます。
1行に1つのJSONオブジェクトを記述する形式です。ファイルは1行ずつ読み込まれ、
各行が独立したJSONオブジェクトとして解析されます。

.. note::
   拡張子が ``.json`` のファイルも処理対象になりますが、内容はJSONL形式
   （1行1オブジェクト）である必要があります。
   配列形式のJSONファイル（ ``[{...}, {...}]`` ）や、複数行に整形された
   （pretty-printされた）JSONは直接読み込めません。JSONL形式に変換してください。

JSONL形式のファイル:

::

    {"id": 1, "name": "Product A", "description": "Description A"}
    {"id": 2, "name": "Product B", "description": "Description B"}

使用例
======

製品カタログ
--------------

パラメーター:

::

    files=/var/data/products.json
    fileEncoding=UTF-8

スクリプト:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description + " 価格: " + price + "円"
    digest=category
    price=price

複数JSONファイルの統合
----------------------

パラメーター:

::

    files=/var/data/data1.json,/var/data/data2.json
    fileEncoding=UTF-8

スクリプト:

::

    url="https://example.com/item/" + id
    title=title
    content=content

トラブルシューティング
======================

ファイルが見つからない
----------------------

**症状**: ログに ``... is not found.`` または ``Source file ... does not exist.`` と出力される

**確認事項**:

1. ファイルパスが正しいか確認
2. ファイルが存在するか確認
3. ファイルの拡張子が ``.json`` または ``.jsonl`` か確認
4. ファイルの読み取り権限があるか確認

JSON解析エラー
--------------

**症状**: ログに ``Crawling Access Exception`` と ``JsonParseException`` などが出力される

不正な行が含まれる場合、その行のみがスキップされて失敗URLとして記録され、
クロール自体は次の行から継続します。

**確認事項**:

1. JSONファイルが正しい形式（1行1オブジェクトのJSONL）か確認:

   ::

       # 各行が有効なJSONオブジェクトかを検証
       cat data.json | jq -c .

2. 文字エンコーディングが正しいか確認
3. 1つのオブジェクトが複数行に分かれていないか確認
4. コメントが含まれていないか確認（JSON標準ではコメント不可）

データが取得できない
--------------------

**症状**: クロールは成功するが件数が0

**確認事項**:

1. JSON構造を確認
2. スクリプト設定が正しいか確認（フィールド参照が ``data.`` 接頭辞なしになっているか）
3. フィールド名が正しいか確認（大文字小文字を含む）
4. ログでエラーメッセージを確認

大きなJSONファイル
------------------

**症状**: メモリ不足またはタイムアウト

ファイルは1行ずつ読み込まれるため、ファイル全体のサイズが直接メモリ使用量に
影響することはありません。ただし、1行（1オブジェクト）が極端に大きい場合や、
インデックス登録の負荷が高い場合に問題が発生することがあります。

**解決方法**:

1. JSONファイルを複数に分割
2. |Fess| のヒープサイズを増やす

スクリプトの高度な使用例
========================

条件付き処理
------------

各フィールドは独立した式として評価されます。条件付きの値は三項演算子を使用します:

::

    url=status == "published" ? "https://example.com/product/" + id : null
    title=status == "published" ? name : null
    content=status == "published" ? description : null
    price=status == "published" ? price : null

配列の結合
----------

::

    url="https://example.com/article/" + id
    title=title
    content=content
    tags=tags ? tags.join(", ") : ""
    categories=categories.collect { it.name }.join(", ")

デフォルト値の設定
------------------

::

    url="https://example.com/item/" + id
    title=title ?: "無題"
    content=description ?: (summary ?: "説明なし")
    price=price ?: 0

日付のフォーマット
------------------

::

    url="https://example.com/post/" + id
    title=title
    content=body
    created=created_at
    last_modified=updated_at

数値の処理
----------

::

    url="https://example.com/product/" + id
    title=name
    content=description
    price=price as Float
    stock=stock_quantity as Integer

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-csv` - CSVコネクタ
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
