======================================
既存サイトに検索窓と検索画面を組み込む
======================================

はじめに
========

社内ポータルや製品サイトに検索を付けたいとき、利用者に Fess の URL を覚えてもらうのは現実的ではありません。
いつも開いているページのヘッダーに検索窓があり、結果の画面もそのサイトの一部に見えることが求められます。

本記事では、Fess 15.9 を使い、ブラウザー側だけで完結する次の 3 つの方法を順に試します。

- 既存ページに HTML の検索フォームを置き、Fess の検索画面に結果を表示する
- Fess Site Search（FSS）を使い、既存サイトのページの中に検索結果を表示する
- Fess の検索画面（テーマ）の見た目を、既存サイトに合わせて変える

あわせて、検索結果のリンク先を利用者がアクセスできる URL に変える「パスマッピング」も設定します。

業務システムのサーバーから検索 API を呼び出して独自の画面を作る方法は、:doc:`guide-11` で扱います。

前提
====

- :doc:`guide-02` の手順で、Docker Compose の Fess 15.9 が ``http://localhost:8080/`` で動いており、何か 1 つクロール済みであること
- 既存サイトの代わりに使う、手元の HTML ファイル

既存サイトは Fess と別のオリジン（スキーム・ホスト・ポートの組）にあるのがふつうです。
本記事でも同じ条件にするため、HTML ファイルを置いたディレクトリで次のコマンドを実行し、``http://localhost:8000/`` で開きます。

::

    $ python3 -m http.server 8000

方法の選び方
============

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - 方法
     - 検索結果を表示する場所
     - Fess 側で必要なもの
   * - 検索フォーム
     - Fess の検索画面（``/search``）に移動して表示
     - なし
   * - Fess Site Search
     - 既存サイトのページの中
     - プラグイン ``fess-webapp-v1-api``
   * - テーマの変更
     - Fess の検索画面（見た目を変える）
     - テーマの ZIP（または［全般］の設定）

検索フォームとテーマの変更は組み合わせて使えます。
既存サイトから移動した先の画面も同じ見た目にしたい場合は、両方を設定します。

検索フォームを置いて Fess の検索画面に送る
==========================================

フォームを置く
--------------

既存ページの検索窓を置きたい場所に、次のフォームを書きます。

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <button type="submit">検索</button>
    </form>

検索語は ``q`` パラメーターとして Fess の ``/search`` に送られ、Fess の検索画面に結果が表示されます。
``maxlength`` は、Fess 側の検索語の長さの上限 ``query.max.length``\ （初期値 ``1000``）に合わせています。
本番では ``action`` の URL を、利用者がアクセスする Fess の URL に変えてください。

特定のラベルの文書だけを検索させたい場合は、ラベルの値を ``fields.label`` として一緒に送ります。

.. code-block:: html

    <form method="get" action="http://localhost:8080/search">
      <input type="text" name="q" maxlength="1000" autocomplete="off">
      <input type="hidden" name="fields.label" value="intranet">
      <button type="submit">検索</button>
    </form>

``intranet`` は［クローラー］>［ラベル］で作ったラベルの値です。
存在しない値を送ると、結果は 0 件になります。
ラベルの作り方は :doc:`guide-04` を参照してください。

確かめる
--------

1. ``http://localhost:8000/`` から HTML ファイルを開き、クロール済みの文書に含まれる語で検索します
2. ブラウザーが ``http://localhost:8080/search?q=...`` に移動し、Fess の検索画面に結果が表示されれば完了です

結果が 0 件の場合は、同じ語を ``http://localhost:8080/`` の検索窓で検索して比べます。
こちらでも 0 件なら、フォームではなくクロールやパーミッションの問題です。

サジェストについて
------------------

`検索フォームの配置 <https://fess.codelibs.org/ja/stable/config/search-form-integration.html>`__ のページには、フォームにサジェストを付ける例があります。
ただし、この例が読み込む ``/js/suggestor.js`` と ``/js/jquery-3.7.1.min.js`` は 15.9 の Fess に含まれていないため、15.9 ではこの例のままでは動きません。
フォームの部分（``q`` を ``/search`` に送る）はそのまま使えます。

既存サイトの検索窓にサジェストを出したい場合は、次のどちらかを使います。

- 次の節の Fess Site Search で、サジェストを有効にする
- 自分のスクリプトから ``/api/v2/suggest-words`` を呼ぶ（API の使い方は :doc:`guide-11` を参照）

Fess の検索画面に移動した後は、Fess 同梱のテーマがサジェストを表示します。

Fess Site Search でページの中に結果を表示する
=============================================

Fess Site Search（FSS）は、既存サイトのページに検索フォームと検索結果を表示する JavaScript です。
利用者は既存サイトから移動せずに検索できます。

FSS の JavaScript は Fess からは配信されません。
FSS JS Generator（https://fss-generator.codelibs.org/）で生成したファイルをダウンロードし、既存サイトのサーバーに置きます。

v1 API のプラグインを入れる
---------------------------

FSS は Fess の ``/api/v1`` を呼び出します。
15.9 の Fess 本体が提供するのは ``/api/v2`` だけで、``/api/v1`` はプラグイン ``fess-webapp-v1-api`` が提供します。
このプラグインは Docker イメージに同梱されていません。

Docker Compose では、``compose.yaml`` の ``fess01`` の ``environment`` に次の行を加えます。

.. code-block:: yaml

    - "FESS_PLUGINS=fess-webapp-v1-api:15.9.0"

すでにほかのプラグインを指定している場合は、同じ値の中にスペースで区切って並べます。
保存したら、2 つの Compose ファイルを指定して ``up -d`` を実行します。
``fess01`` が作り直され、起動時にプラグインがインストールされます。
コンテナが作り直されるので、［システム］>［全般］で変えた設定は ``down`` したときと同じく元に戻ります（:doc:`guide-02` の「停止と再開」を参照）。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

管理画面の［システム］>［プラグイン］>［インストール］からも入れられます（インストール後に Fess の再起動が必要です）。
ただし、Docker ではプラグインがコンテナの中に置かれるため、``down`` でコンテナを作り直すと消えます。
``FESS_PLUGINS`` で指定しておけば、作り直すたびに入れ直されます。

``fess01`` が healthy になったら、API が応答するかを確かめます。

::

    $ curl 'http://localhost:8080/api/v1/documents?q=fess'

``"record_count"`` を含む JSON が返れば準備完了です。
404 が返る場合は、プラグインが入っていません。
このとき ``fess.log`` には ``No plugin serves the legacy API`` で始まる WARN が 1 度だけ出ます。
プラグインが入っているのに JSON が返らない場合は、［システム］>［全般］の「JSONレスポンス」がオフになっていないかを確認します。
「JSONレスポンス」をオフにすると ``/api/v1`` だけでなく ``/api/v2`` も応答しなくなり、Fess 自身の検索画面も使えなくなります。

JavaScript を生成して置く
-------------------------

1. https://fss-generator.codelibs.org/ を開き、ジェネレーターで配色やフォントを指定して［Generate］をクリックします
2. ［Download JS］で JavaScript ファイルをダウンロードします
3. ファイル名を ``fess-ss.js`` に変え、HTML ファイルと同じディレクトリに置きます

検索結果を表示するページ（例: ``result.html``）に、次のコードを書きます。

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form
        language="ja"
        :enable-suggest="true"
        suggest-url="http://localhost:8080"
      ></fess-search-form>
      <fess-search-result
        fess-url="http://localhost:8080"
        language="ja"
      ></fess-search-result>
    </div>

``fess-url`` が検索に使う Fess の URL、``suggest-url`` がサジェストに使う Fess の URL です。
本番では、利用者のブラウザーからアクセスできる Fess の URL にします。

ほかのページのヘッダーには、検索フォームだけを置きます。

.. code-block:: html

    <script src="fess-ss.js"></script>

    <div class="fess-site-search">
      <fess-search-form result-page="result.html"></fess-search-form>
    </div>

フォームは検索語を ``fss.query`` パラメーターに入れて ``result.html`` に移動し、``result.html`` の FSS が検索を実行します。
FSS を読み込まないページから送る場合も、``result.html?fss.query=検索語`` の形で移動するフォームを書けば同じように動きます。

ほかの属性（1 ページの件数 ``:page-size``、ラベルでの絞り込み ``:enable-label``、リンクを別タブで開く ``link-target="_blank"`` など）は、FSS JS Generator のマニュアルを参照してください。

確かめる
--------

1. ``http://localhost:8000/result.html`` を開き、検索フォームで検索します
2. ページの中に検索結果が表示されれば完了です
3. 表示されない場合は、ブラウザーの開発者ツールのネットワークタブで ``/api/v1/documents`` へのリクエストを確認します。404 ならプラグイン、CORS のエラーなら次の項目を確認します

注意すること
------------

ブラウザーから見ると、``localhost:8000`` のページから ``localhost:8080`` の API を呼ぶのはクロスオリジン通信です。
Fess は初期設定で ``api.cors.allow.origin=*`` としており、どのオリジンからの呼び出しも受け付けます。
呼び出し元を既存サイトに限りたい場合の設定は :doc:`guide-11` で扱います。

FSS が別オリジンから呼び出す検索は、利用者が Fess にログインしていても、ログインしていない利用者（ゲスト）の検索として扱われます。
FSS は Cookie を付けずに API を呼び出し、初期設定の ``api.cors.allow.origin=*`` では資格情報を付けたクロスオリジン通信も許可されないためです。
そのため、結果に出るのはパーミッションに ``{role}guest`` を持つ文書だけです。
部署ごとに見せる文書を変える場合は、利用者に Fess の検索画面でログインしてもらいます（:doc:`guide-05` を参照）。

Fess の検索画面の見た目を変える
===============================

15.9 の検索画面は、HTML・CSS・JavaScript をまとめた「テーマ」で表示されます。
以前のバージョンにあった［ページのデザイン］や JSP の編集はありません。
何も設定していなければ、同梱のテーマ ``bootstrap`` が使われます。

ZIP を作らずに変えられること
----------------------------

［システム］>［全般］の「お知らせ表示」にある「検索トップページ」に書いた内容は、同梱のテーマの検索トップと検索結果の画面に表示されます。
HTML も書けますが、``<script>`` や ``<style>`` などは取り除かれます。
社内向けの案内を 1 行出したいだけなら、テーマを作る必要はありません。

公開されているテーマを使う
--------------------------

Fess プロジェクトは、文書検索向けの ``docsearch`` などのテーマを公開しています。

1. ［システム］>［テーマ］を開きます
2. 「テーマのインストール」の「名前」でテーマを選び、［選択］をクリックします
3. 「バージョン」で 15.9 用のバージョン（``15.9.x``）を選び、［インストール］をクリックします
4. 一覧の上の「デフォルトテーマ」で、インストールしたテーマを選んで［設定］をクリックします

``http://localhost:8080/`` を開き直すと、新しいテーマで表示されます。
「（デフォルトなし）」を選んで［設定］をクリックすると、同梱の ``bootstrap`` に戻ります。

同梱のテーマを複製して、ロゴと配色を変える
------------------------------------------

同梱のテーマは直接編集できず、``bootstrap`` という名前のテーマをアップロードで置き換えることもできません。
別の名前で複製して変更します。
ここでは ``mytheme`` とします。

1. コンテナから同梱のテーマを取り出します

   ::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml cp fess01:/usr/share/fess/app/themes/bootstrap ./mytheme

2. ``mytheme/theme.yml`` の ``name`` を ``mytheme`` に、``displayName`` を ``My Theme`` などに変えます
3. 次のファイルを変更します

   - 配色・レイアウト: ``assets/styles.css``
   - ロゴ: ``assets/logo-head.png``\ （ヘッダー）と ``assets/logo.png``\ （検索トップ）
   - フッターの組織名: ``i18n/messages.ja.json`` の ``footer.copyright_org``\ （英語の画面は ``messages.en.json``）

4. ``theme.yml`` が ZIP のルートに来るようにまとめます

   ::

       $ cd mytheme && zip -r ../mytheme.zip . && cd ..

5. ［システム］>［テーマ］の［アップロード］から ``mytheme.zip`` をアップロードします
6. 「デフォルトテーマ」で ``mytheme`` を選び、［設定］をクリックします

``index.html`` は変更しません。
同梱の ``index.html`` は、テーマ内のファイルを ``{{themePath}}/assets/...`` の形で参照しています。
Fess が配信時に ``{{themePath}}`` を ``themes/mytheme`` に置き換えるため、名前を変えるだけで複製したテーマのファイルが読み込まれます。

確かめる
--------

``http://localhost:8080/`` を開き直し、ロゴと配色が変わっていることを確かめます。
変わらない場合は、開発者ツールのネットワークタブで、スタイルシートが ``/themes/mytheme/assets/styles.css`` から読み込まれているかを見ます。
``/themes/bootstrap/`` から読み込まれていれば、デフォルトテーマの設定が反映されていません。

テーマで気をつけること
----------------------

- 検索画面には、スクリプト・スタイル・画像の取得元を Fess 自身に限る ``Content-Security-Policy`` ヘッダーが付きます。外部の CDN のフォントやスクリプトは読み込まれないので、テーマの ZIP に入れてください
- 検索画面は、ほかのページの ``iframe`` には表示されません（``theme.index.frame.ancestors`` の初期値が ``'none'`` のためです）。ポータルの中に検索結果を出したい場合は、FSS を使います
- Docker の ``fess01`` にはボリュームがありません。アップロードしたテーマはコンテナ内に置かれ、デフォルトテーマの設定は ``system.properties`` に保存されるため、``down`` でコンテナを作り直すとどちらも消えます。ふだんは ``stop``／``start`` を使い、作り直した後はアップロードと設定をやり直します
- 同梱のテーマは、その版の Fess の ``/api/v2`` に合わせて作られています。Fess をアップグレードしたら、新しい同梱のテーマから複製し直して、変更を当て直してください

テーマの構造や ``theme.yml`` の項目は、`テーマ開発ガイド <https://fess.codelibs.org/ja/stable/dev/theme-development.html>`__ を参照してください。

検索結果のリンク先を利用者向けの URL にする
===========================================

クロールには社内向けのホスト名を使い、利用者にはポータルの URL で開いてもらいたい場合があります。
たとえば ``http://intranet-web01:8080/docs/`` をクロールし、検索結果では ``https://portal.example.com/docs/`` を開かせる場合です。
このときは、パスマッピングで表示するときだけ URL を置き換えます。

1. ［クローラー］>［パスマッピング］を開き、［新規作成］をクリックします
2. 次のように入力し、［作成］をクリックします

   .. list-table::
      :header-rows: 1
      :widths: 25 75

      * - 項目
        - 値
      * - 正規表現
        - ``^http://intranet-web01:8080/docs/``
      * - 置換
        - ``https://portal.example.com/docs/``
      * - 処理の種別
        - 表示
      * - 表示順序
        - ``0``

「表示」は、検索結果に表示する URL とリンク先だけを置き換えます。
インデックスに保存された URL は変わらないので、再クロールは不要で、保存した時点から検索結果に反映されます。
「クロール」や「クロール/表示」を選ぶと、置き換えた URL がインデックスに保存されます。
表示だけを変えたいのにこれらを選ぶと、その後のクロールの URL まで変わるので注意してください。

確かめるには、対象の文書が出る語で検索し、結果の URL とリンク先が ``https://portal.example.com/docs/...`` になっていることを見ます。
API で結果を受け取る場合、置き換えた URL が入るのは ``url`` ではなく ``url_link`` です（:doc:`guide-11` を参照）。

ファイルサーバーのパスを Web サーバーの URL に変える例は、`パスマッピング <https://fess.codelibs.org/ja/stable/admin/pathmap-guide.html>`__ を参照してください。

次に読む記事
============

- 業務システムのサーバーから検索 API を呼び出したい: :doc:`guide-11`
- ポータルに出す文書を部署ごとに変えたい: :doc:`guide-05`
- Web サイトとファイルサーバーをまとめて検索し、ラベルで分けたい: :doc:`guide-04`
- 組織ごとに別のテーマや検索対象を見せたい: :doc:`guide-13`
- 検索画面にログインを必須にしたい: :doc:`guide-15`

参考資料
========

- `検索フォームの配置 <https://fess.codelibs.org/ja/stable/config/search-form-integration.html>`__
- `テーマ <https://fess.codelibs.org/ja/stable/admin/theme-guide.html>`__
- `テーマ開発ガイド <https://fess.codelibs.org/ja/stable/dev/theme-development.html>`__
- `パスマッピング <https://fess.codelibs.org/ja/stable/admin/pathmap-guide.html>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `FSS JS Generator <https://fss-generator.codelibs.org/>`__
- `fess-site-search（GitHub） <https://github.com/codelibs/fess-site-search>`__
- `fess-webapp-v1-api（GitHub） <https://github.com/codelibs/fess-webapp-v1-api>`__
