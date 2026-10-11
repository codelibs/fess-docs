==================================
Wikipediaコネクタ
==================================

概要
====

Wikipediaコネクタは、Wikipediaのダンプファイルを読み込んで、そのページを
|Fess| のインデックスに登録する機能を提供します。
Wikipedia、その他のWikimediaプロジェクト、任意のMediaWikiサイトのダンプに対応しています。

この機能には ``fess-ds-wikipedia`` プラグインが必要です。

対応するダンプ
==============

ダンプの形式は ``source`` パラメーターで選択します。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ``source``
     - 説明
   * - ``cirrus``
     - CirrusSearchのインデックスダンプ。Wikimediaが各wikiについて
       ``https://dumps.wikimedia.org/other/cirrus_search_index/`` で公開しています。MediaWiki自身がテンプレートを展開してレンダリングしたテキストを含むため、
       wikitextのマークアップが索引に混入しません。Wikipediaやその他のWikimediaのwikiには、この形式を推奨します
   * - ``xml``
     - MediaWikiのXMLエクスポート（``*-pages-articles.xml.bz2``、または任意のMediaWikiの ``Special:Export`` や ``dumpBackup.php`` の出力）。
       wikitextを含み、コネクタがプレーンテキストに変換します（「XMLダンプのプレーンテキスト化」を参照）
   * - ``auto``
     - 既定値。``cirrus_search_index`` を含む場所、または ``.json.bz2`` か ``.json`` で終わる場所は ``cirrus`` として、それ以外の場所は ``xml`` として読み込みます

ダンプの圧縮形式（bzip2、gzipなど）は内容から自動的に判別され、圧縮されていないファイルも読み込めます。

前提条件
========

1. プラグインのインストールが必要です
2. HTTP(S)のURL、または |Fess| サーバー上のパスで、ダンプファイルにアクセスできる必要があります
3. クロールの時間が必要です。大きなWikipediaのダンプは数ギガバイトあります。まず ``limit`` を指定して設定を試してください

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールするか、``bin/fess-setup install plugin fess-ds-wikipedia`` を実行して
|Fess| を再起動します。
詳細は :doc:`../../admin/plugin-guide` を参照してください。

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
     - Japanese Wikipedia
   * - ハンドラ名
     - WikipediaDataStore
   * - 有効
     - オン

パラメーター設定
----------------

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    limit=10000

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``url``
     - いいえ
     - ダンプの場所。HTTP(S)のURL、``file:`` のURL、またはローカルのパス。既定値は英語版Wikipediaのダンプ
       （``http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2``）なので、必ず明示的に指定してください。
       ``source=cirrus`` で指定できる形式は「CirrusSearchダンプ」を参照してください
   * - ``source``
     - いいえ
     - ``auto``、``cirrus``、``xml`` のいずれか（デフォルト: ``auto``）
   * - ``limit``
     - いいえ
     - このページ数で処理を終了します。``0`` は無制限です（デフォルト: ``0``）。少数のページで設定を試すときに使用します
   * - ``user_agent``
     - いいえ
     - ダンプのダウンロード時に送信するUser-Agentヘッダー。指定しない場合は、|Fess| のクローラーのUser-Agent名を使用します
   * - ``max_digest_length``
     - いいえ
     - ``digest`` の最大文字数（デフォルト: ``100``）
   * - ``total_entity_size_limit``
     - いいえ
     - XMLパーサーが処理するエンティティの合計サイズの上限（バイト、デフォルト: ``100000000``）。``source=xml`` にのみ適用されます
   * - ``text_extractor``
     - いいえ
     - XMLダンプのwikitextをプレーンテキストに変換する方法。``sweble`` （デフォルト）または ``regex``。「XMLダンプのプレーンテキスト化」を参照してください
   * - ``drop_templates``
     - いいえ
     - XMLダンプの ``content`` から、テキストを除外するテンプレート名のカンマ区切りリスト。``*`` ですべてのテンプレートを除外します
   * - ``keep_templates``
     - いいえ
     - ``drop_templates`` に一致しても、テキストを残すテンプレート名のカンマ区切りリスト
   * - ``drop_captions``
     - いいえ
     - XMLダンプの ``content`` から、画像とギャラリーのキャプションを除外します（デフォルト: ``false``）

CirrusSearchダンプ
~~~~~~~~~~~~~~~~~~

CirrusSearchのダンプは、``jawiki_content-20261004-00000.json.bz2`` のような番号付きのチャンクとして公開されています。
``source=cirrus`` の場合、``url`` にはカンマ区切りのリストを指定でき、各要素には次のものを指定できます:

- 単一のファイル（HTTP(S)のURLまたはローカルのパス）
- ローカルのディレクトリ: 名前が ``.json.bz2`` または ``.json`` で終わるディレクトリ内のすべてのファイルを、名前順に読み込みます
- ``/`` で終わるHTTP(S)のURL: ディレクトリのリストを取得し、名前が ``.json.bz2`` または ``.json`` で終わるすべてのファイルを、名前順に読み込みます

たとえば、日本語版Wikipediaのコンテンツインデックスのすべてのチャンクを読み込むには、次のようにします:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

.. note::

   Wikimediaのサーバーからは、古い日付のダンプが削除されます。クロールを設定する前に、
   ``https://dumps.wikimedia.org/other/cirrus_search_index/`` の一覧で、存在する日付を確認してください。

スクリプト設定
--------------

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    anchor=
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

スクリプトからは、次の値を参照できます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - ページID
   * - ``title``
     - ページのタイトル
   * - ``encodedTitle``
     - MediaWikiのページURLで使われる形式のタイトル（空白は ``_`` になり、その他の文字はパーセントエンコードされます）
   * - ``content``
     - ページのプレーンテキスト
   * - ``digest``
     - ``max_digest_length`` 文字に切り詰めた ``content``
   * - ``contentLength``
     - ``content`` の長さ
   * - ``wikitext``
     - ページのwikitext（ダンプに含まれている場合）
   * - ``format``、``model``
     - ページの形式とコンテンツモデル
   * - ``timestamp``
     - ページのタイムスタンプ
   * - ``ns``
     - 名前空間の番号
   * - ``categories``、``links``
     - ページのカテゴリと、リンク先のページ
   * - ``redirect``、``redirectTitle``
     - ページがリダイレクトかどうかと、そのリダイレクト先
   * - ``stub``、``disambiguation``
     - ページがスタブかどうかと、曖昧さ回避ページかどうか
   * - ``lang``、``host``、``site``、``url``
     - ダンプの場所から導出されます。「ダンプの場所から導出される値」を参照してください

``source=cirrus`` では、次の値も利用できます:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``openingText``
     - ページの冒頭のテキスト
   * - ``headings``
     - 見出し
   * - ``externalLinks``
     - 外部リンク
   * - ``templates``
     - ページが使用しているテンプレート
   * - ``redirects``
     - このページにリダイレクトしているタイトル
   * - ``auxiliaryText``
     - 画像のキャプションなどの補助テキスト
   * - ``weightedTags``
     - 重み付きタグ
   * - ``wikibaseItem``
     - WikidataのアイテムID
   * - ``incomingLinks``
     - 被リンク数
   * - ``popularityScore``
     - 人気スコア
   * - ``revisionId``
     - リビジョンID

ダンプの場所から導出される値
----------------------------

``lang``、``host``、``site``、``url`` は、ダンプの名前から導出されます。``jawiki-latest-pages-articles.xml.bz2`` や
``index_name=jawiki_content`` のような名前からは、``lang`` が ``ja``、``host`` と ``site`` が ``ja.wikipedia.org``、
``url`` が ``https://ja.wikipedia.org/wiki/<エンコードしたタイトル>`` になります。
名前には、言語コードの直後に ``wiki``、さらにその直後に ``-``、``_``、``.`` のいずれかが続く部分が必要です。
Wikiquote（``jawikiquote-...``）などの姉妹プロジェクトは、誤ったホストがリンク切れを引き起こすため、意図的に導出しません。

.. warning::

   ダンプの名前が一致しない場合、``host``、``site``、``url`` は設定されず、``url`` には ``url`` パラメーターの値、つまりダンプの場所が残ります。
   スクリプトで ``url`` をそのまま使うと、すべてのページが同じURLになり、クロール全体が索引上では1件の文書になります。エラーも出力されません。
   名前を変更したダンプや他のWikimediaプロジェクトでは、上の例のように、スクリプトでURLを組み立ててください。例:
   ``url="https://ja.wikiquote.org/wiki/" + encodedTitle``

XMLダンプのプレーンテキスト化
-----------------------------

``source=xml`` では、wikitextをSwebleのwikitextパーサーでプレーンテキストに変換します。名前空間の名前はエクスポートの ``<siteinfo>`` から読み取るため、
画像やカテゴリの記述は、どの言語（``[[ファイル:...]]``、``[[Kategorie:...]]``）でも、独自の名前空間名を持つwikiでも認識されます。
Swebleで変換できないページは、正規表現で変換されます。

``text_extractor=regex`` は、すべてのページを正規表現で変換します。数倍高速ですが、入れ子になったテンプレート、表、複数行にわたるマークアップがテキストに残ります。

既定では、すべてのテンプレートの引数のテキスト（パラメーター名は除く）と、すべての画像およびギャラリーのキャプションが ``content`` に残るため、それらのテキストも検索できます。
``drop_templates``、``keep_templates``、``drop_captions`` で絞り込めます:

::

    # これらのテンプレートのテキストを除外する（入れ子の場合も。"*" ですべてのテンプレートを除外）
    drop_templates=Cite web,Cite news,Use dmy dates
    # drop_templates に一致しても、これらのテンプレートは残す
    # （drop_templates=* と keep_templates=Note,Warning で、その2つだけが残る）
    keep_templates=
    # 画像とギャラリーのキャプションを除外する
    drop_captions=false

テンプレート名は、MediaWikiが解決するのと同じ方法で照合されます。先頭の文字は大文字小文字を区別せず、``_`` は空白と同じで、``Template:`` プレフィックスは省略できます。
テンプレートは展開されないため、残したテンプレートが追加するのは引数のテキストであり、MediaWikiがレンダリングする内容ではありません。
CirrusSearchのダンプには、MediaWikiがレンダリングしたテキストがすでに含まれているため、これらのパラメーターは ``source=cirrus`` には適用されません。

使用例
======

CirrusSearchダンプから日本語版Wikipediaをクロール
-------------------------------------------------

パラメーター:

::

    url=https://dumps.wikimedia.org/other/cirrus_search_index/20261004/index_name=jawiki_content/
    source=cirrus

スクリプト:

::

    lang="ja"
    filetype=format
    filename=title
    url="https://ja.wikipedia.org/wiki/" + encodedTitle
    host="ja.wikipedia.org"
    site="ja.wikipedia.org"
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=timestamp
    timestamp=timestamp

XMLダンプから日本語版Wikipediaをクロール（出典テンプレートを除外）
------------------------------------------------------------------

パラメーター:

::

    url=https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
    source=xml
    drop_templates=Cite web,Cite news
    limit=10000

スクリプトは「スクリプト設定」と同じです。

他のWikimediaプロジェクト（Wikiquote）をクロール
------------------------------------------------

ダンプ名 ``jawikiquote-...`` からは ``host`` と ``url`` が導出されないため、スクリプトで組み立てます。

スクリプト:

::

    lang="ja"
    url="https://ja.wikiquote.org/wiki/" + encodedTitle
    host="ja.wikiquote.org"
    site="ja.wikiquote.org"
    title=title
    content=content
    digest=digest
    last_modified=timestamp
    timestamp=timestamp

トラブルシューティング
======================

索引化される文書が1件だけ
-------------------------

「ダンプの場所から導出される値」を参照してください。スクリプトがすべてのページに対して ``url`` を設定していることを確認します。

クロールに時間がかかりすぎる
----------------------------

1. まず ``limit`` を指定して、設定を確認します
2. ``source=cirrus`` を使用します。XMLダンプでは ``text_extractor=regex`` を使用します
3. ダンプを |Fess| サーバーに配置して、ローカルのパスを指定します

コンテンツにwikitextのマークアップが残る
----------------------------------------

CirrusSearchダンプ（``source=cirrus``）を使用してください。``source=xml`` では、``text_extractor=regex`` は入れ子のテンプレート、表、複数行のマークアップをテキストに残すため、``sweble`` （既定）を使用します。

ダンプを読み込めない
--------------------

1. URLまたはパスが正しいか確認します（CirrusSearchダンプの日付は、サーバーから削除されている場合があります）
2. ディレクトリのURLは、``/`` で終わっていること、およびその中のファイルが ``.json.bz2`` または ``.json`` で終わっていることを確認します
3. ログで正確なエラーを確認します

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../../admin/plugin-guide` - プラグイン管理ガイド
- `Wikimedia Downloads <https://dumps.wikimedia.org/>`_
- `CirrusSearch index dumps <https://dumps.wikimedia.org/other/cirrus_search_index/>`_
