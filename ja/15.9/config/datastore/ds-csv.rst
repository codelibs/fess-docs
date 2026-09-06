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

.. note::

   引用符（クォート）処理とエスケープ処理は、|Fess| 15.9 では **デフォルトで有効** になっています。
   引用符で囲まれたフィールド内に区切り文字や改行を含むCSV（RFC 4180準拠）は、
   パラメーターを指定しなくてもそのまま解析されます。
   以前のバージョンと同じ挙動（引用符処理を無効化する）に戻す方法や注意点は、
   後述の「引用符・エスケープ処理の無効化」を参照してください。

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
     - 引用符（デフォルト: ダブルクォート ``"``）。引用符処理はデフォルトで有効です（ ``quote_disabled`` を参照）。
   * - ``escape_character``
     - いいえ
     - エスケープ文字（デフォルト: ``quote_character`` と同じ文字。RFC 4180に従い引用符を二重にしてエスケープします）。エスケープ処理の有効・無効は ``quote_disabled`` の解決結果に従います（ ``escape_disabled`` を参照）。

.. note::

   ``files`` および ``directories`` の両方が空の場合はエラー（ ``DataStoreException`` ）となります。
   どちらか一方を必ず指定してください。

高度なパラメーター
~~~~~~~~~~~~~~~~~~

以下のパラメーターはCSVの解析動作やインデックス登録の挙動を細かく制御します:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 説明
   * - ``quote_disabled``
     - 引用符（クォート）処理を無効にするか（デフォルト: false）。デフォルトではRFC 4180準拠の引用符付きフィールドが正しく解析されます。以前の挙動（引用符を通常の文字として扱う）に戻す場合は ``true`` を指定します。
   * - ``escape_disabled``
     - エスケープ処理を無効にするか（デフォルト: ``quote_disabled`` の解決結果と同じ）。明示的に指定した場合はその値が優先されます。
   * - ``delete_old_docs``
     - このデータ設定に属し、かつ今回のクロールセッションで再登録されなかったドキュメントを、クロール完了後にインデックスから削除するか（デフォルト: true）。複数のCSVファイルを別々のタイミングで同じデータ設定に投入する場合、 ``false`` を指定しないと前回投入した分のドキュメントが削除されてしまいます（詳細は後述のトラブルシューティングを参照）。
   * - ``keep_expires_docs``
     - ``delete_old_docs`` による削除の際、有効期限（ ``time_to_live`` などで設定される expires ）が未到来のドキュメントを削除対象から除外するか（デフォルト: true）。 ``false`` にすると、有効期限内でも再登録されなかったドキュメントは削除されます。
   * - ``time_to_live``
     - ドキュメントの有効期限を、登録時刻から何分後に設定するか（分単位。デフォルト: 未設定＝無期限）。
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

   列名にスペースやハイフンなど、スクリプトの識別子として無効な文字が含まれる場合は、
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
   含めても、デフォルト（引用符処理が有効）のままそのまま1つのフィールドとして解析されます。
   以前の挙動（引用符を通常の文字として扱い、フィールドを区切り文字で分割する）に戻す場合は
   後述の「引用符・エスケープ処理の無効化」を参照してください。

引用符・エスケープ処理の無効化
------------------------------

引用符処理とエスケープ処理は |Fess| 15.9 ではデフォルトで有効です。
引用符文字はデフォルトでダブルクォート ``"`` 、エスケープ文字はデフォルトで引用符文字と同じ
（RFC 4180に従い引用符を二重にしてエスケープ）になっており、標準的なRFC 4180形式のCSVは
パラメーターなしでそのまま解析できます。

.. warning::

   引用符処理が有効な状態で、CSVファイル中に対応する閉じ引用符のない ``"`` が1つでも存在すると、
   その引用符以降のファイル全体（後続の行も含む）が1つのフィールド値として読み込まれてしまい、
   それ以降の行からはドキュメントが生成されません。以前のバージョンでは各行が独立して解析されていたため、
   この挙動はアップグレード後に初めて表面化することがあります。
   ``delete_old_docs`` （前述）はデフォルトで有効なため、生成されなかったドキュメントだけでなく、
   前回のクロールで登録済みだったドキュメントまで削除されてしまう場合があります。
   アップグレード前にCSVファイルに対応しない引用符が含まれていないか確認するか、
   ``quote_disabled=true`` を指定して以前の解析方法に戻すことを検討してください。

引用符処理を無効にする（以前の挙動に戻す）:

::

    # パラメーター
    quote_disabled=true

``quote_disabled=true`` を指定すると、エスケープ処理も同時に無効になります
（明示的に ``escape_disabled=false`` を指定した場合を除く）。

エスケープ処理だけを無効にする:

::

    # パラメーター
    escape_disabled=true

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

2. 引用符付きフィールド（フィールド内に区切り文字を含む）はデフォルトで正しく解析されます。
   意図せず ``quote_disabled=true`` を指定していないか確認してください。
3. CSVファイルの形式を確認（RFC 4180準拠か）。対応する閉じ引用符のない ``"`` が含まれていると、
   それ以降のファイル全体が1つのフィールド値として読み込まれてしまいます。

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
5. パラメーター名にタイプミスがないか確認（認識されないパラメーター名は警告なく無視されます。
   例えば ``has_headerline=true`` と書いても ``has_header_line`` はデフォルトの ``false`` のままです）

2回目のCSV投入で前回のインデックスが消える
------------------------------------------

**症状**: 1つ目のCSVファイルをクロールした後、日を改めて2つ目のCSVファイルを同じデータ設定で
クロールすると、1つ目のCSVファイルから登録されたはずのドキュメントが検索結果から消えている。

**原因**:

|Fess| はクロール完了後、そのデータ設定に属し、かつ今回のセッションで再登録されなかった
ドキュメントをインデックスから削除します（ ``delete_old_docs`` 、デフォルト: true）。
同じデータ設定に複数のCSVファイルを異なるタイミングで投入している場合、後から投入したファイルの
クロール時点では、先に投入したファイルの内容は「今回のセッションで再登録されなかった」
ドキュメントとして扱われ、削除されてしまいます。

**解決方法**:

複数のCSVファイルを別々のタイミングで同じデータ設定に投入し、それぞれの内容を蓄積したい場合は
以下を指定します。

::

    delete_old_docs=false

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
引用符処理はデフォルトで有効なため、パラメーターを指定しなくてもそのまま解析されます:

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
   * - ``delete_processed_file``
     - いいえ
     - 処理が完了したCSVファイルを削除するか（デフォルト: true）
   * - ``ignore_data_store_exception``
     - いいえ
     - 1つのCSVファイルの処理中に例外が発生しても、クロール全体を継続するか（デフォルト: true）

.. warning::

   ``CsvListDataStore`` は処理完了後にCSVファイルを自動的に **削除します** （ ``delete_processed_file`` のデフォルトは ``true`` ）。
   処理中にエラーが発生した場合、ファイルは ``.txt`` にリネームされます（リネームに失敗した場合は削除されます）。
   ファイルを削除したくない場合は ``delete_processed_file=false`` を指定してください。

CSVの行フォーマット（イベントタイプ）
-------------------------------------

``CsvListDataStore`` に渡すCSVファイルは、1行につき少なくとも「イベントタイプ」と「URL」の2列が必要です。
列をさらに追加し、 ``cell3`` 、 ``cell4`` ...として参照することもできます
（例えば ``timestamp.overwrite`` に値を渡す場合など）。

::

    <イベントタイプ>,<URL>

イベントタイプに指定できる値は次の3つです。

- ``create`` - ファイルが作成された
- ``modify`` - ファイルが更新された
- ``delete`` - ファイルが削除された

``create`` と ``modify`` は同じ処理（対象URLのクロールとインデックス登録）として扱われます。挙動に違いはありません。

列名（ヘッダーがある場合）や各イベントタイプの値は、以下のパラメーターで変更できます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 説明
   * - ``field.event_type``
     - イベントタイプが格納されている列名（デフォルト: ``event_type``）
   * - ``event.create``
     - 「作成」を表す値（デフォルト: ``create``）
   * - ``event.modify``
     - 「更新」を表す値（デフォルト: ``modify``）
   * - ``event.delete``
     - 「削除」を表す値（デフォルト: ``delete``）

CSVファイルの例:

::

    modify,smb://servername/data/testfile1.txt
    delete,smb://servername/data/testfile2.txt

スクリプトの例（ヘッダーなしの場合）:

::

    event_type=cell1
    url=cell2

フィールド値の上書き（.overwrite）
----------------------------------

スクリプトで組み立てるインデックスフィールド名の末尾に ``.overwrite`` を付けると、
そのフィールドの値はクロール結果（実際のファイルクロールが取得した値）ではなく、
CSVから設定した値で上書きされます。

::

    timestamp.overwrite=cell3

.. note::

   検索画面の日付ファセットは ``created`` ではなく ``timestamp`` フィールドで絞り込みを行います。
   タイムスタンプをCSVの値で上書きしたい場合は ``created.overwrite`` ではなく
   ``timestamp.overwrite`` を指定してください。

認証・プロキシ設定の引き継ぎ
----------------------------

``CsvListDataStore`` はCSVに書かれたURLを実際にクロールしますが、ファイルクロールやWebクロールの
データ設定に登録した認証情報・プロキシ設定は引き継がれません。必要な設定はデータストアの
パラメーターとして個別に指定してください。

SMB認証の例:

::

    crawler.file.auth=example
    crawler.file.auth.example.scheme=SAMBA
    crawler.file.auth.example.username=username
    crawler.file.auth.example.password=password

プロキシ設定の例:

::

    crawler.web.proxyHost=proxy.example.com
    crawler.web.proxyPort=8080

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

.. note::

   上記のように ``url`` に ``null`` を返す行は、失敗としては扱われず静かにスキップされます。
   スキップされた行数はCSVファイルごとに集計され、そのファイルの読み込みが終わるたびに
   1つのサマリーWARNログとして出力されます（行ごとに失敗URLが記録されるわけではありません。
   複数のCSVファイルを処理する場合はファイルの数だけWARNログが出力されます）。

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
