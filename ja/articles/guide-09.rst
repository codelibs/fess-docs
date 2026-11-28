============================================
日本語・英語・中国語が混在する文書を検索する
============================================

はじめに
========

日本語の議事録、英語の技術仕様書、中国語の市場レポートが同じファイルサーバーや社内サイトに並んでいると、「英語の文書は見つかるのに日本語の活用形で引っかからない」「中国語の文書だけを探したい」「英語で書かれた資料を日本語の言葉で見つけたい」といった声が出てきます。

Fess は特別な設定をしなくても、どの言語の文書も検索できます。
ただし、どの言語の解析がどこで効いているかを知らないまま辞書を足しても、結果は変わりません。
本記事では、Fess 15.9 が多言語の文書をどうインデックスし、どう検索しているかを、設定ファイルの実際の値をもとに説明します。
そのうえで、次のことができるようにします。

- 文書ごとに判定された言語を確かめ、``lang:`` で言語を絞り込んで検索する
- 検索時にどの言語の解析を使うかを ``query.default.languages`` などで決める
- 辞書（同義語・Kuromoji・ストップワードなど）を、効くフィールドに合わせて編集し、反映させる
- 変更が効いたことを検索結果と ``_analyze`` API で確かめる

検索ログを使った改善の進め方そのものは :doc:`guide-08` で扱います。

インデックスの仕組み：共通フィールドと言語別フィールド
======================================================

Fess のインデックスには、本文やタイトルが 2 種類の形で入ります。
定義は Fess に同梱の ``fess_indices/fess.json`` （アナライザー）と ``fess_indices/fess/doc.json`` （マッピング）にあります。

.. list-table::
   :header-rows: 1
   :widths: 28 32 40

   * - フィールド
     - アナライザー
     - 解析の内容
   * - ``content`` ・ ``title`` ・ ``important_content``
     - ``standard_analyzer`` （検索時は ``standard_search_analyzer``）
     - すべての文書に共通です。漢字・ひらがな・カタカナ・ハングルは 2 文字ずつ（bi-gram）に区切り、英語のストップワード除去と語幹化（stemming）をかけます。同義語は検索時だけ展開されます
   * - ``content_ja`` ・ ``title_ja`` など
     - ``japanese_analyzer``
     - Kuromoji による形態素解析です。動詞などを基本形にそろえ、助詞・助動詞・記号を取り除きます
   * - ``content_en`` ・ ``title_en`` など
     - ``english_analyzer``
     - 英語のストップワード除去と語幹化です
   * - ``content_zh-cn`` ・ ``title_zh-cn`` など
     - ``simplified_chinese_analyzer``
     - 中国語用のトークナイザーで単語に区切ります
   * - ``content_zh-tw`` ・ ``title_zh-tw`` など
     - ``traditional_chinese_analyzer``
     - 繁体字を簡体字に変換してから、簡体字と同じトークナイザーで区切ります

共通フィールドはすべての文書にあります。
言語別フィールドは、文書の言語が決まったときだけ作られます。
インデックス処理で ``lang`` フィールドに言語コードを入れ、``content`` ・ ``important_content`` ・ ``title`` （``indexer.language.fields``）の値を ``content_ja`` のような ``<フィールド>_<言語>`` にコピーします。
1 つの文書に付く言語は 1 つだけです。

文書の言語の決まり方
--------------------

``lang`` は、次の順に決まります。

1. Web クロールの HTML は ``<html lang="...">`` の値を使います（``crawler.document.html.lang.xpath=//HTML/@lang``）。クロール設定の「設定パラメーター」に ``field.xpath.default.lang=<XPath>`` を書くと、その設定だけ読み取る場所を変えられます
2. 1 で決まらない文書は、本文から自動判定します。``content``、``important_content``、``title`` の順に、先頭 1000 文字（``indexer.language.detect.length``）を見ます。ファイルクロールでは、抽出した本文だけから判定します
3. 判定結果が ``supported.languages`` にない言語のとき、または判定できないときは ``lang`` が付かず、言語別フィールドも作られません

``ja-JP`` や ``zh_CN`` のような値は、小文字とハイフンの形（``ja``、``zh-cn``）にそろえて保存されます。

データストアの文書も、インデックス時に同じ自動判定を受けます。
スクリプトで ``lang`` に ``supported.languages`` にある言語（``ja`` など）を入れると、自動判定より優先されます。

検索の仕組み：どの言語のフィールドを検索するか
==============================================

検索語は、常に共通フィールドに対して検索されます。
それに加えて、検索のたびに決まる「検索言語」ごとに、言語別フィールドが検索条件に加わります。
各フィールドの条件は OR（``bool`` クエリーの ``should``）で結ばれるので、どれか 1 つのフィールドに一致すれば検索結果に入ります。

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - フィールド
     - 設定キー
     - 既定値
   * - ``title``
     - ``query.boost.title``
     - ``0.5``
   * - ``content``
     - ``query.boost.content``
     - ``0.05``
   * - ``title_<検索言語>``
     - ``query.boost.title.lang``
     - ``1.0``
   * - ``content_<検索言語>``
     - ``query.boost.content.lang``
     - ``0.1``

検索言語は、次のうち最初に値があるものから決まります。

1. ``fess_config.properties`` の ``query.default.languages`` （既定は空）。値があると、ほかの指定はすべて無視されます
2. リクエストの ``lang`` パラメーター。検索画面の［オプション］>「優先する言語」や詳細検索の「優先する言語」で選んだ言語、または ``/api/v2/search`` の ``lang`` です
3. ブラウザーが送る ``Accept-Language`` ヘッダーの言語

たとえば日本語のブラウザーで「会議」と検索すると、検索言語は ``ja`` になり、``content`` に加えて ``content_ja`` も検索されます。
英語の文書には ``content_ja`` がないので、英語の文書は共通フィールドの bi-gram でだけ一致します。
逆に、日本語の文書は ``title_ja`` ・ ``content_ja`` でも一致すれば、そのぶんスコアが上がり上位に来やすくなります。
Kuromoji は活用形を基本形にそろえるため、「走った」で検索すると「走る」と書かれた日本語の文書も ``content_ja`` で一致します。

このため「優先する言語」は、その言語の文書を上位に寄せる指定であり、ほかの言語の文書を除く絞り込みではありません。

言語で絞り込む：``lang:`` 検索
==============================

言語で絞り込むには、``lang`` フィールドを指定して検索します。
``lang`` はキーワード型の検索可能なフィールドで、言語ごとにラベルを作る必要はありません。

::

    lang:en meeting
    lang:ja 会議
    lang:zh-cn 会议
    会議 -lang:ja

最後の例は、日本語と判定された文書を除いて「会議」を検索します。
API からは ``q`` に同じ式を書くか、``fields.lang=en`` を付けます（``lang:"en"`` の条件が加わります）。

::

    $ curl -s "http://localhost:8080/api/v2/search?q=meeting&fields.lang=en"

``lang`` が付いていない文書（言語を判定できなかった文書）は、どの ``lang:`` 条件にも一致しません。

言語の判定結果を確かめる
------------------------

辞書や設定を変える前に、文書にどの言語が付いているかを確かめます。

1. 検索画面で ``lang:ja``、``lang:en``、``lang:zh-cn``、``lang:zh-tw`` をそれぞれ検索し、件数を比べます。API なら ``response.record_count`` で件数を見られます

   ::

       $ curl -s "http://localhost:8080/api/v2/search?q=lang:zh-cn&num=1"

2. 個々の文書は、管理画面の［システム情報］>［検索］で URL などから探して開くと、``lang`` 欄で値を確認できます

判定が期待と違うときは、次の点を確認してください。

- HTML の ``<html lang>`` は自動判定より優先されます。サイトのテンプレートが日本語のページにも ``lang="en"`` を出力していると、そのページは英語として扱われます
- ``<html lang="zh">`` のように地域のない中国語は ``zh`` になります。``zh`` には中国語用アナライザーの言語別フィールドがないため、中国語の解析は共通フィールドの bi-gram だけになります
- 漢字が多くかなが少ない日本語の短い文書は、``zh-cn`` などと判定されることがあります

すべての HTML またはすべてのファイルを 1 つの言語として扱う設定もあります。
``crawler.document.html.default.lang`` と ``crawler.document.file.default.lang`` に値を入れると、``<html lang>`` も自動判定も使わず、Fess 全体のクロールでその言語に固定されます。
文書の言語が混在する環境では空のままにしてください。

検索言語を決める: ``query.default.languages``
=============================================

既定では、利用者ごとのブラウザーの言語で検索言語が変わります。
英語のブラウザーを使う社員が日本語の文書を検索すると ``content_ja`` が使われないなど、利用者によって結果の並びが変わります。
これを避けたい場合は、``query.default.languages`` で検索言語を固定します。

::

    query.default.languages=ja,en,zh-cn,zh-tw

この例では、だれがどの言語で検索しても、4 つの言語別フィールドがすべて検索条件に加わります。
各文書は自分の言語のフィールドを 1 つだけ持つので、どの言語の文書も同じ条件で言語別の解析の恩恵を受けます。
そのかわり、「優先する言語」で特定の言語を上位に寄せる操作は効かなくなります。
日本語の文書が中心なら ``query.default.languages=ja`` のように 1 言語だけにする方法もあります。

設定は ``fess_config.properties`` に書き、Fess を再起動します。
ファイルの場所は、ZIP 版では ``app/WEB-INF/classes/fess_config.properties`` 、RPM/DEB 版では ``/etc/fess/fess_config.properties`` です。
Docker では ``compose.yaml`` の ``fess01`` の ``environment`` に JVM オプションとして追加し、コンテナを作り直します。

::

    - "FESS_JAVA_OPTS=-Dfess.config.query.default.languages=ja,en,zh-cn,zh-tw"

``FESS_JAVA_OPTS`` は空白で区切られるため、値に空白を入れないでください。
コンテナを作り直すと、［システム］>［全般］で変えた設定はコンテナ内の ``system.properties`` とともに失われます（:doc:`guide-02`）。

言語別フィールドの一致をどれだけ重く見るかは、``query.boost.title.lang`` と ``query.boost.content.lang`` で調整できます。
変更したら、次の「確認する」の手順で検索結果の並びを比べてください。

辞書を言語に合わせて使い分ける
==============================

辞書は［システム］>［辞書］で編集します。
辞書ごとに効くフィールドが決まっているため、目的のフィールドに効く辞書を選ばないと検索結果は変わりません。

.. list-table::
   :header-rows: 1
   :widths: 24 36 40

   * - 辞書（ファイル）
     - 効くフィールド
     - 多言語環境での使いどころ
   * - 同義語（``synonym.txt``）
     - ``content`` ・ ``title`` （検索時のみ）
     - 言語をまたぐ言い換え（「会議」と「meeting」）、表記ゆれ。言語別フィールドには効きません
   * - Kuromoji（``ja/kuromoji.txt``）
     - ``_ja`` フィールドのみ
     - 社内用語や製品名を日本語の 1 語として扱わせる
   * - ストップワード（``ja/stopwords.txt``）
     - ``_ja`` フィールドのみ
     - 日本語の文書で検索に使わせない語
   * - ストップワード（``en/stopwords.txt``）
     - ``content`` ・ ``title`` と ``_en`` フィールド
     - 英語の不要語。共通フィールドに効くため全言語の文書に影響します
   * - Protwords（``en/protwords.txt``）
     - ``content`` ・ ``title`` と ``_en`` フィールド
     - 語幹化させたくない英単語（製品名など）
   * - Stemmer上書き（``en/stemmer_override.txt``）
     - ``content`` ・ ``title`` と ``_en`` フィールド
     - 英語の語幹化の結果を指定する
   * - マッピング（``mapping.txt``）
     - ``content`` ・ ``title``
     - 文字の置き換え。 ``ja/mapping.txt`` は ``_ja`` フィールド用の別ファイルです

日本語用の保護語（Protwords）の辞書はありません。
``japanese_analyzer`` には保護語を読むフィルターがないためです。
簡体字・繁体字の中国語のフィールドには、管理画面から編集できるユーザー辞書はありません（ストップワードは ``zh-cn/stopwords.txt`` ・ ``zh-tw/stopwords.txt``）。

言語をまたぐ同義語
------------------

日本語の言葉で英語の文書を見つけたい場合は、対訳を同義語として登録します。
アップロードするファイルの形式では、1 行に同じ意味の語をカンマ区切りで並べます。

::

    会議,ミーティング,meeting
    見積,quotation

同義語は検索時に共通フィールドで展開されるので、再クロールは不要です。
ひらがなはカタカナで、全角英数字は半角で登録するなど、登録時のルールは `同義語辞書 <https://fess.codelibs.org/ja/stable/admin/synonym-guide.html>`__ を参照してください。

Kuromoji ユーザー辞書
---------------------

Kuromoji の辞書には、トークン、分割したトークン、読み（カタカナ）、品詞を登録します。
Kuromoji が細かく分けてしまう社内用語や製品名を 1 語として扱わせたいときは、トークンと分割したトークンに同じ語を書きます。

::

    東京スカイツリー,東京スカイツリー,トウキョウスカイツリー,カスタム名詞

この辞書が効くのは ``_ja`` フィールドだけです。
共通フィールドの ``content`` は bi-gram で区切るため、Kuromoji の辞書を変えても ``content`` での一致は変わりません。
効果が出るのは、検索言語に ``ja`` が含まれる検索で、日本語と判定された文書に対してです。

辞書の変更を反映する
--------------------

辞書を保存しただけでは、検索結果は変わりません。

1. ［システム情報］>［メンテナンス］を開き、「ドキュメントインデックスのリロード」の［リロード］をクリックします。インデックスを閉じて開き直すため、その間は検索がエラーまたは 0 件になります。利用の少ない時間帯に実行してください
2. 同義語は検索時にだけ使われるので、リロードで反映は終わりです
3. 同義語以外の辞書（Kuromoji、マッピング、ストップワード、Protwords、Stemmer上書き）は、インデックスを作るときの解析も変えます。すでにインデックスにある文書は古い辞書で解析されたままなので、対象をクロールし直します

再クロールのとき、［システム］>［全般］の「最終更新日時の確認」が有効（既定）だと、更新されていないファイルやページは取り直されません。
一時的に無効にしてクロールを実行し、終わったら有効に戻します。

確認する
========

トークンの区切りを ``_analyze`` API で見る
------------------------------------------

辞書が反映されたかどうかを確かめるには、OpenSearch の ``_analyze`` API で、同じ文字列を共通フィールドと日本語フィールドのアナライザーにかけて比べるのが確実です。
:doc:`guide-02` の Docker 構成では、OpenSearch にホストの 9200 番ポートで接続できます。

::

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"japanese_analyzer","text":"全文検索エンジンを導入した"}'

    $ curl -s -X POST "http://localhost:9200/fess.search/_analyze" \
        -H "Content-Type: application/json" \
        -d '{"analyzer":"standard_analyzer","text":"全文検索エンジンを導入した"}'

``japanese_analyzer`` では語のまとまりで区切られ、「を」「た」が除かれます。
``standard_analyzer`` では「全文」「文検」「検索」のように 2 文字ずつ区切られます。
Kuromoji の辞書に「東京スカイツリー」を登録してリロードしたあとは、``japanese_analyzer`` でこの語を解析すると 1 つのトークンで返ります。
登録した同義語は、``"analyzer":"standard_search_analyzer"`` で「会議」を解析し、「meeting」から作られたトークン（語幹化されて ``meet``）が出てくることで確認できます。

検索結果で確かめる
------------------

1. 検索画面で、日本語と英語の両方の文書に出てくる語を検索します
2. ［オプション］の「優先する言語」を「日本語」と「英語」に切り替え、上位の文書の言語が変わることを確かめます。 ``query.default.languages`` を設定した場合は、切り替えても並びが変わらないことを確かめます
3. 対訳の同義語を登録してリロードしたら、``lang:en 会議`` で英語の文書が見つかることを確かめます
4. Kuromoji の辞書を変えて再クロールしたら、登録した語で検索し、その語を含む日本語の文書が見つかることを確かめます。区切りが変わったこと自体は、前の ``_analyze`` で確かめます

結果が変わらないときは、辞書の表で「効くフィールド」と文書の ``lang`` を照らし合わせてください。
たとえば ``en/stopwords.txt`` に 3 文字以上の日本語の語を足しても、共通フィールドでは 2 文字ずつのトークンになるため一致せず、効きません。

まとめ
======

- すべての文書は、bi-gram と英語の語幹化をかける共通フィールド（``content`` ・ ``title``）で検索できます
- 判定された言語の ``lang`` と、言語別フィールド（``content_ja`` など）が、言語に合った解析を足します
- 検索言語は ``query.default.languages`` 、リクエストの ``lang`` 、ブラウザーの言語の順に決まり、絞り込みではなく上位への寄せとして働きます
- 言語で絞り込むときは ``lang:en`` のように ``lang`` フィールドを指定します
- 辞書は効くフィールドを選んで編集し、ドキュメントインデックスのリロードと、必要なら再クロールで反映させます

次に読む記事
============

- 検索ログから改善点を見つけ、同義語やキーマッチで直したい: :doc:`guide-08`
- 社内の Web サイトとファイルサーバーをまとめてクロールしたい: :doc:`guide-04`
- キーワードが一致しなくても意味の近い文書を探したい: :doc:`guide-18`
- 検索 API を業務システムから呼び出したい: :doc:`guide-11`

参考資料
========

- `辞書 <https://fess.codelibs.org/ja/stable/admin/dict-guide.html>`__
- `Kuromoji辞書 <https://fess.codelibs.org/ja/stable/admin/kuromoji-guide.html>`__
- `同義語辞書 <https://fess.codelibs.org/ja/stable/admin/synonym-guide.html>`__
- `ストップワード辞書 <https://fess.codelibs.org/ja/stable/admin/stopwords-guide.html>`__
- `メンテナンス <https://fess.codelibs.org/ja/stable/admin/maintenance-guide.html>`__
- `検索関連の設定（検索対象のデフォルト言語） <https://fess.codelibs.org/ja/stable/config/search-advanced.html>`__
- `クローラー詳細設定 <https://fess.codelibs.org/ja/stable/config/crawler-advanced.html>`__
- `フィールド指定検索 <https://fess.codelibs.org/ja/stable/user/search-field.html>`__
- `検索API <https://fess.codelibs.org/ja/stable/api/api-search.html>`__
