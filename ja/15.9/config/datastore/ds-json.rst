==================================
JSONコネクタ
==================================

概要
====

JSONコネクタは、ローカルファイルシステム上のJSONファイルからデータを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-json`` プラグインが必要です。

次の3つの形式に対応しており、既定ではファイルの内容から自動的に判別されます。

- JSON Lines形式（1行に1つのJSONオブジェクト）
- JSONオブジェクトの配列（整形されたもの、1行にまとめられたもののどちらも可）
- 単一のJSONオブジェクト

レコードは1件ずつ読み込まれるため、大きな配列であってもファイル全体がメモリに
保持されることはありません。

.. note::

   このコネクタはローカルファイルシステム上のJSONファイルのみを対象とします。
   HTTPなどのリモート取得には対応しておらず、 ``urls`` パラメーターを指定した場合は
   無視されるのではなくエラーになります。

前提条件
========

1. プラグインのインストールが必要です
2. JSONファイルへのアクセス権が必要です
3. JSONの構造を理解している必要があります

プラグインのインストール
------------------------

方法1: 管理画面からインストール

1. 「システム」→「プラグイン」を開く
2. JARファイルをアップロード
3. |Fess| を再起動

方法2: JARファイルを直接配置

::

    # CodeLibsリポジトリからダウンロード
    wget https://maven.codelibs.org/org/codelibs/fess/fess-ds-json/X.X.X/fess-ds-json-X.X.X.jar

    # 配置
    cp fess-ds-json-X.X.X.jar $FESS_HOME/app/WEB-INF/plugin/
    # または
    cp fess-ds-json-X.X.X.jar /usr/share/fess/app/WEB-INF/plugin/

.. note::

   15.8.0以降のJARは `CodeLibsリポジトリ <https://maven.codelibs.org/release/org/codelibs/fess/fess-ds-json/>`_
   で配布しています。15.7.0以前は
   `Maven Central <https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-json/>`_ にあります。

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

    files=/var/data/products.jsonl
    file_encoding=UTF-8

複数ファイル:

::

    files=/var/data/data1.json,/var/data/data2.json
    file_encoding=UTF-8

ディレクトリ指定:

::

    directories=/var/data/json_dir/
    file_encoding=UTF-8

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - パラメーター
     - 既定値
     - 説明
   * - ``files``
     -
     - 処理するJSONファイルのパス（複数指定可：カンマ区切り）。指定した順に処理されます。
   * - ``directories``
     -
     - JSONファイルを含むディレクトリのパス（複数指定可：カンマ区切り）。
   * - ``recursive``
     - ``false``
     - ``directories`` をサブディレクトリまで走査するか。
   * - ``max_depth``
     - ``10``
     - ``recursive=true`` のときに、各ディレクトリの何階層下まで降りるか。 ``0`` を指定すると ``recursive=false`` と同じ動作になります。
   * - ``include_pattern``
     -
     - ファイルの絶対パスが完全一致しなければならない正規表現。
   * - ``exclude_pattern``
     -
     - ファイルの絶対パスが一致してはならない正規表現。
   * - ``file_suffixes``
     - ``.json,.jsonl``
     - 対象とするファイルの接尾辞（複数指定可：カンマ区切り）。大文字小文字は区別しません。
   * - ``file_encoding``
     - ``UTF-8``
     - ファイルの文字エンコーディング。
   * - ``format``
     - ``auto``
     - ドキュメントの形式。 ``auto`` 、 ``jsonl`` 、 ``json`` のいずれか。
   * - ``root_path``
     -
     - レコードを読み取る位置を指定するJSON Pointer（例: ``/data/items`` ）。

.. note::

   パラメーター名はスネークケースで記載していますが、キャメルケースの綴り
   （ ``file_encoding`` に対する ``fileEncoding`` など）も同じように使用できます。

.. note::

   ``files`` と ``directories`` の少なくとも一方を指定してください。
   両方が空の場合はエラーになります。
   両者は排他ではなく、両方を指定した場合は双方が処理されます。
   同じファイルが両方から到達する場合でも、読み込まれるのは1回だけです。

ファイルの探索順序
~~~~~~~~~~~~~~~~~~

- ``files`` で指定したファイルは、指定した順に処理されます。
- ``directories`` の下で見つかったファイルは、更新日時の古い順に処理されます。
- ``files`` で指定したファイルは ``directories`` の下のファイルより先に処理されます。

``file_suffixes`` による絞り込みは ``files`` で直接指定したファイルにも適用されます。
接尾辞が一致しないファイルはログに理由が出力されたうえでスキップされます。

存在しないパス、 ``files`` に指定されたディレクトリ、 ``directories`` に指定されたファイルは、
いずれも警告としてログに記録され、クロール自体は続行されます。

``format``
----------

``auto`` はドキュメントの先頭を読み、その文法から形式を判別します。3つの形式の
いずれであっても、正しく記述されたファイルであればこれで判別できます。

``format=jsonl`` を明示するのは、JSON Lines形式のファイルであって、かつ先頭付近の行が
壊れている可能性がある場合です（バナー行、進捗ログ、転送が途中で切れたレコードなど）。
自動判別はそうした行を読み飛ばして判断する必要があるためです。

この設定は、不正なレコードの影響範囲も決めます。

- **JSON Lines形式**: 各行が独立して解析されるため、不正な行のコストはその行だけです。
  失敗は ``<ファイルの絶対パス>@<行番号>`` というキーで失敗URLに記録され、
  次の行からそのまま処理が続きます。
- **それ以外の形式**: トークンストリームとして読み込むため、1つの失敗が後続のレコードを
  巻き込むことがあります。オブジェクトの途中で切れたドキュメントは復帰できず、
  一定回数連続して失敗するとそのファイルは警告を出して打ち切られます。

``root_path``
-------------

ネストした配列を指すJSON Pointerを指定すると、その要素がレコードとして登録されます。

::

    root_path=/data/items

.. code-block:: json

    { "meta": { "count": 2 }, "data": { "items": [ { "id": "1" }, { "id": "2" } ] } }

- 配列を指した場合は、その要素ごとに1レコードになります。
- オブジェクトを指した場合は、そのオブジェクトが1レコードになります。
- どこにも一致しない場合は、エラーにはならずレコードが0件になります。
- JSON Pointerのエスケープ（ ``~1`` が ``/`` 、 ``~0`` が ``~`` ）が使用できます。

``root_path`` は ``format`` より優先されます。JSON Pointerで到達したドキュメントは
行単位では読み込まれないためで、 ``format=jsonl`` と同時に指定した場合は
その旨の警告がログに出力されます。

.. warning::

   ``root_path`` は ``/`` で始まる必要があります。 ``data/items`` のように先頭の ``/`` を
   忘れると、JSON Pointerとして解釈できずデータ設定全体がエラーになります。
   このとき失敗URLはパラメーター名ではなくデータ設定として記録されるため、
   どのパラメーターが原因かはログの
   ``JSON Pointer expression must start with '/'`` から判断してください。

.. note::

   ``root_path`` を指定せずに、レコードが複数行にまたがって整形されたドキュメント
   （メタ情報と配列を含むいわゆるラッパー形式）を読み込むと、行単位での解析が
   試みられるため、意図したレコードが取得できず失敗が記録されます。
   そのようなドキュメントでは ``root_path`` を指定してください。

スクリプト設定
--------------

各フィールドの値は、JSONオブジェクトの各フィールドの値を参照して組み立てます。
JSONオブジェクトのトップレベルのフィールドは、スクリプト内で **接頭辞なしの変数**
として直接参照できます（ ``data.`` のような接頭辞は付きません）。

単純なJSONオブジェクト:

::

    url="https://shop.example.com/product/" + id
    title=name
    content=description
    digest=description
    host="shop.example.com"
    site="shop.example.com"

ネストしたオブジェクトはマップ、ネストした配列はリストとして参照できます:

::

    url="https://example.com/product/" + id
    title=product.name
    content=product.description
    price=product.pricing.amount
    first_tag=tags[0]

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

- ``<フィールド名>`` - JSONオブジェクトのトップレベルのフィールドを名前で直接参照します
- ``<親>.<子>`` - ネストしたオブジェクトのフィールド
- ``<配列>[<インデックス>]`` - 配列要素

.. note::

   フィールドの値が ``null`` の場合、そのフィールドはドキュメントに登録されません。

.. note::

   |Fess| 15.9 では、組み込みのスクリプトエンジンがJavaScriptになりました。
   Groovyは ``fess-script-groovy`` プラグインとして提供されます。
   使用するエンジンはデータストアのパラメーター ``script_type`` で指定します
   （ ``script_type=javascript`` など）。省略した場合は ``groovy`` が使用されます。
   上記の例のような単純な参照や文字列連結は、どちらのエンジンでも同じように動作しますが、
   それ以外の記法はエンジンによって異なります。

注意事項
========

``app.encrypt.property.pattern`` に一致する名前のパラメーター（既定では ``password`` 、
``key`` 、 ``token`` 、 ``secret`` で終わるもの）は、スクリプトからは ``null`` として
参照されます。データストアのパラメーターに記述した資格情報が、インデックスの
フィールドへコピーされることを防ぐためです。

同名のフィールドがレコード側にある場合は、他のパラメーターと同様にレコード側の値が
優先されます。

.. note::

   一致判定はパラメーター名に対する大文字小文字を区別した完全一致です。
   ``access_token`` は対象になりますが、キャメルケースの ``accessToken`` は
   対象になりません。資格情報をパラメーターに記述する場合はスネークケースで
   記述してください。

パラメーターの誤りとエラー
==========================

``format`` 、 ``include_pattern`` 、 ``exclude_pattern`` 、 ``urls`` に使用できない値を
指定した場合は、ファイルを読み込む前にクロールが終了し、そのパラメーター名を含む
失敗URL（例: ``JsonDataStore:format`` ）が記録されます。

``max_depth`` に数値以外を指定した場合は、ログに記録されたうえで既定値が使用されます。

.. note::

   データストアのクロールは、対象が1件も取得できなかった場合でもジョブとしては
   正常終了します。取得件数が想定と異なる場合は、インデックスの件数、失敗URL、
   および ``fess-crawler.log`` を確認してください。

使用例
======

製品カタログ
------------

パラメーター:

::

    files=/var/data/products.jsonl
    file_encoding=UTF-8

スクリプト:

::

    url="https://shop.example.com/product/" + product_id
    title=name
    content=description
    digest=category
    host="shop.example.com"
    site="shop.example.com"

APIレスポンスを保存したファイル
--------------------------------

パラメーター:

::

    files=/var/data/response.json
    root_path=/data/items

スクリプト:

::

    url="https://example.com/item/" + id
    title=title
    content=body
    host="example.com"
    site="example.com"

ディレクトリを再帰的に処理する
------------------------------

パラメーター:

::

    directories=/var/data/exports
    recursive=true
    max_depth=3
    include_pattern=.*\.jsonl
    file_encoding=UTF-8

トラブルシューティング
======================

ファイルが見つからない
----------------------

**症状**: ログに ``... does not exist.`` 、 ``... is not a file.`` 、
``... is skipped because its suffix is not one of ...`` と出力される

**確認事項**:

1. ファイルパスが正しいか確認
2. ファイルが存在するか確認
3. ファイルの接尾辞が ``file_suffixes`` （既定では ``.json`` または ``.jsonl`` ）に
   一致するか確認
4. |Fess| の実行ユーザーに読み取り権限があるか確認

JSON解析エラー
--------------

**症状**: ログに ``Failed to parse ...`` や ``Failed to read ...`` が出力される、
または失敗URLが記録される

**確認事項**:

1. ファイルが正しいJSONか検証する

   ::

       # JSON Lines形式の場合、各行が有効なJSONオブジェクトかを検証
       cat data.jsonl | jq -c .

       # 配列や単一オブジェクトの場合
       jq . data.json

2. 文字エンコーディングが正しいか確認
3. ファイルが途中で切れていないか確認
4. コメントが含まれていないか確認（JSON標準ではコメント不可）

データが取得できない
--------------------

**症状**: クロールは成功するが件数が0

**確認事項**:

1. ``root_path`` を指定している場合、そのJSON Pointerがドキュメントの構造と
   一致しているか確認（一致しない場合はエラーにならず0件になります）
2. ``include_pattern`` 、 ``exclude_pattern`` 、 ``file_suffixes`` で対象が
   すべて除外されていないか確認。この場合はログに ``No sources to process`` が
   出力されます
3. スクリプト設定が正しいか確認（フィールド参照が ``data.`` 接頭辞なしになっているか）
4. フィールド名が正しいか確認（大文字小文字を含む）
5. ``url`` が組み立てられているか確認。 ``url`` が空の場合はレコードごとに失敗になります

文字化けする
------------

**症状**: 登録されたドキュメントの文字が壊れている

``file_encoding`` に実在するが誤ったエンコーディングを指定した場合、エラーにはならず
文字化けしたまま登録されます。ファイルの実際のエンコーディングを確認してください。
存在しないエンコーディング名を指定した場合は、ファイルごとに失敗URLが記録されます。

大きなJSONファイル
------------------

**症状**: メモリ不足またはタイムアウト

レコードは1件ずつ読み込まれるため、ファイル全体のサイズが直接メモリ使用量に
影響することはありません。ただし、1つのレコードが極端に大きい場合や、
インデックス登録の負荷が高い場合に問題が発生することがあります。

**解決方法**:

1. JSONファイルを複数に分割
2. |Fess| のヒープサイズを増やす

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-csv` - CSVコネクタ
- :doc:`ds-database` - データベースコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- `JSON (JavaScript Object Notation) <https://www.json.org/>`_
- `JSON Lines <https://jsonlines.org/>`_
- `JSON Pointer (RFC 6901) <https://datatracker.ietf.org/doc/html/rfc6901>`_
- `jq - JSON processor <https://stedolan.github.io/jq/>`_
