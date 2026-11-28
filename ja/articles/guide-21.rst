==================================================
画像とテキストをまとめて検索する（マルチモーダル）
==================================================

はじめに
========

ファイルサーバーや社内サイトには、製品写真や現場写真のように、ファイル名以外に手がかりのない画像が大量にあります。
キーワード検索では、ファイル名やメタデータに含まれる語でしか画像を見つけられません。

マルチモーダル検索プラグイン ``fess-webapp-multimodal`` を使うと、「山の夕日」や「犬」のような言葉で、写っている内容が近い画像を検索できます。
本記事では、Fess 15.9 で次のことを行います。

- 検証用の Docker 環境 ``docker-multimodalsearch`` を 15.9 の版で起動し、画像をクロールして検索する
- 画像がベクトルで見つかったことを、検索 API の応答で確かめる
- 既存の Fess に組み込むときに必要な設定と、つまずきやすい点を押さえる

できること・できないこと
========================

先に、15.9 の ``fess-webapp-multimodal`` の範囲を整理しておきます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 15.9 での動作
   * - 検索の向き
     - テキストで画像を探す方向だけです。画像をアップロードして似た画像を探す機能はありません
   * - ベクトル化される画像
     - MIME タイプが ``image/gif``\ 、\ ``image/jpeg``\ 、\ ``image/png`` のファイルだけです。BMP や TIFF はベクトル化されません
   * - PDF や Office 文書の中の画像
     - ベクトル化されません。画像内の文字を検索したい場合は OCR（別機能）を使います
   * - 画像以外の文書
     - 通常どおりキーワード検索（BM25）で検索されます。検索結果には画像とテキスト文書が混ざって並びます
   * - 日本語の検索語
     - 多言語対応の CLIP モデルを使います。\ ``docker-multimodalsearch`` の既定モデルは、README で日本語の検索語に対応すると説明されている多言語モデルです
   * - テキストのセマンティック検索
     - 同じ Fess で併用できません（後述）

OCR は `OCR（画像内の文字認識）の設定 <https://fess.codelibs.org/ja/stable/config/crawler-ocr.html>`__ を参照してください。

仕組み
======

CLIP は、テキストと画像を同じベクトル空間に変換するモデルです。
「犬」というテキストのベクトルは、犬が写った画像のベクトルの近くに置かれるため、ベクトル同士の近さで画像を検索できます。

Fess 15.8 以降、ベクトルの格納と検索は Fess 本体が担います。
プラグインが加えるのは、CLIP サーバーとのやり取りの部分だけです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - タイミング
     - 処理
   * - クロール時
     - GIF/JPEG/PNG の画像を CLIP サーバーに送ってベクトルに変換し、本体のベクトルフィールド ``content_chunk_vector`` に書き込みます
   * - 検索時
     - 検索語を CLIP サーバーでベクトルに変換し、近い画像を探します。この検索はキーワード検索と並行して実行され、Rank Fusion で 1 つの結果に統合されます
   * - 結果
     - ベクトル検索で見つかった文書には、``searcher`` フィールドに ``multi_modal`` が付きます。キーワード検索で見つかった文書は ``default`` です

Rank Fusion の仕組みは `ハイブリッド検索とランクフュージョン <https://fess.codelibs.org/ja/stable/config/rank-fusion.html>`__ を参照してください。

docker-multimodalsearch で試す
==============================

``docker-multimodalsearch`` は、マルチモーダル検索をすぐに試せるように、必要なコンテナと設定をまとめた Docker Compose 環境です。
``v15.9.0`` タグでは、次のサービスが起動します。

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - サービス
     - 役割
   * - ``fess01``
     - Fess 本体。イメージは ``ghcr.io/codelibs/fess:15.9.0-noble`` で、起動時にプラグイン ``fess-webapp-multimodal:15.9.0`` を取り込みます。検索画面には画像ギャラリー型のテーマ ``mosaic`` を使います
   * - ``search01``
     - OpenSearch 3.9.0。ポート 9200 はホストのループバック（127.0.0.1）にだけ公開されます
   * - ``clip_server``
     - CLIP サーバー。既定のモデルは多言語対応の ``xlm-roberta-base-ViT-B-32::laion5b-s13b-b90k``\ （512 次元）で、CPU で動きます
   * - ``content``
     - サンプル画像を ``http://content/`` で配信する nginx。コンテナ間のネットワークからだけアクセスできます
   * - ``init-fess-verify``
     - 起動時に一度だけ動き、インデックスのベクトルフィールドが設定どおりかを確認して終了します

準備
----

- Docker（``docker compose`` コマンド）、Git、bash
- インターネット接続（イメージと CLIP モデルの取得に使います。モデルは README によると約 1.6 GB です）
- Linux では、OpenSearch 用に ``vm.max_map_count`` を引き上げておきます（:doc:`guide-02` の「準備」と同じです）

15.9 の版を取得する
-------------------

``docker-multimodalsearch`` の既定ブランチは開発中の次の版に追従しているため、\ ``v15.9.0`` タグを指定して取得します。

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-multimodalsearch.git
    $ cd docker-multimodalsearch
    $ cp .env.example .env

``.env`` を開き、テーマの取得元を 15.9 用のブランチに変更します。

::

    FESS_THEMES_REF=15.9.x

``v15.9.0`` の ``.env.example`` は ``FESS_THEMES_REF=main`` のままですが、``fess-themes`` の ``main`` にある ``mosaic`` テーマは現在 Fess 15.10 以降向け（``minFessVersion: 15.10``）です。
15.9 用の ``mosaic`` は ``15.9.x`` ブランチにあります。

``.env`` の ``FESS_VERSION=15.9.0`` と ``FESS_PLUGINS=fess-webapp-multimodal:15.9.0`` はそのままにします。
プラグインの版は Fess の版とそろえる必要があります。

セットアップして起動する
------------------------

::

    $ bash bin/setup.sh
    $ docker compose up -d

``bin/setup.sh`` は、データ用ディレクトリの作成、テーマの取得、サムネイル生成スクリプトの準備を行います。
初回の ``docker compose up -d`` では ``clip_server`` のイメージをビルドし、CLIP モデルをダウンロードします。
``fess01`` は ``clip_server`` の準備が整うまで起動を待つため、初回は数分かかります。

状態は次のコマンドで確認します。

::

    $ docker compose ps -a
    $ docker compose logs init-fess-verify

``fess01`` が ``(healthy)`` になり、``init-fess-verify`` が ``Exited (0)`` で終わり、ログに次の行が出ていれば、ベクトルフィールドは設定どおりに作られています。

::

    [init-fess-verify] OK: dimension=512, engine=lucene, space_type=cosinesimil, index.knn=true

サンプル画像をクロールする
--------------------------

サンプル画像（動物・乗り物・食べ物・自然・建物）と HTML、PDF を取得します。

::

    $ bash bin/fetch-sample-images.sh

続けて管理画面でクロールします。

1. ``http://localhost:8080/admin/`` に ``admin`` / ``admin`` でログインし、求められたら新しいパスワードを設定します
2. ［クローラー］>［ウェブ］で［新規作成］をクリックし、「名前」に ``content``\ 、「URL」に ``http://content/`` を入力して［作成］をクリックします
3. ［システム］>［スケジューラ］で「Default Crawler」を開き、［今すぐ開始］をクリックします
4. ［システム情報］>［クロール情報］で、クロールが終わるのを待ちます

画像のベクトルは、このクロールの中で書き込まれます。
README によると、同梱のサンプルでは 43 件（画像 37 件、HTML 5 件、PDF 1 件）が登録されます。
件数は目安です。

検索する
--------

``http://localhost:8080/`` を開き、``犬`` や ``山の夕日``\ 、\ ``mountain sunset`` で検索します。
既定のモデルは多言語対応なので、日本語でも英語でも画像が返ります。

``mosaic`` テーマは結果をサムネイルのギャラリーで表示し、各結果に「キーワード」「ビジュアル」「ブレンド」のバッジを付けます。
「ビジュアル」は画像の類似度で、「ブレンド」はキーワードと画像の両方で見つかった結果です。

サムネイルは、クロール後にバックグラウンドのジョブで生成されます。
クロール直後に一部が表示されない場合は、少し待ってから再読み込みします。

停止するときは ``docker compose down`` を実行します。
データは ``./data`` 以下に残ります。

動作を確かめる
==============

検索 API の ``searcher`` を見る
-------------------------------

ベクトル検索が使われたかどうかは、検索 API の応答の ``searcher`` で確認できます。
``jq`` がある場合は、次のように実行します。

::

    $ curl -s -G 'http://localhost:8080/api/v2/search' --data-urlencode 'q=犬' | jq -c '.response.data[] | {url, searcher}'

``searcher`` の値の意味は次のとおりです。

- ``["multi_modal"]``\ ：画像の類似度で見つかった
- ``["default"]``\ ：キーワード検索で見つかった
- 両方を含む：両方で見つかった

すべての結果が ``["default"]`` だけなら、ベクトル検索は実行されていません。
次の「ベクトル検索が実行されない検索」に当てはまらないかを確認します。

``searcher`` は既定では API の応答に含まれません。
``docker-multimodalsearch`` は ``fess_config.properties`` の ``query.additional.api.response.fields=searcher`` を起動オプション（``-Dfess.config.query.additional.api.response.fields=searcher``）で設定しているため、応答に含まれます。
検索 API の詳細は `検索 API <https://fess.codelibs.org/ja/stable/api/api-search.html>`__ を参照してください。

ベクトルが書き込まれたかを見る
------------------------------

検索で画像がまったく返らない場合は、ベクトルを持つ文書の数を OpenSearch で数えます（この環境の 9200 番ポートはホストからだけ使えます）。

::

    $ curl -s 'http://localhost:9200/fess.search/_count' -H 'Content-Type: application/json' -d '{"query":{"nested":{"path":"content_chunk_vector","query":{"exists":{"field":"content_chunk_vector.vector"}}}}}'

``count`` が 0 なら、クロール時にベクトルが作られていません。
``docker compose logs fess01`` やクローラーのログで ``Failed to convert an image to a vector.`` という警告が出ていないかを確認します。

ベクトル検索が実行されない検索
------------------------------

次の場合、ベクトル検索は実行されず、キーワード検索だけの結果になります。
エラーにはならず気付きにくいので、注意してください。

- 並び順を指定した検索（``sort`` パラメーター）。［システム］>［全般］の「デフォルトのソート値」を設定すると、\ ``mosaic`` テーマはその値を ``sort`` として送るため、通常の検索もこれに当たります
- 検索語に検索構文を使った検索：フレーズ（``"山の夕日"``）、ワイルドカード（``dog*``）、ブースト（``dog^2``）、除外（``-dog``）、\ ``allintitle:``\ 、\ ``allinurl:``
- 検索語がなく、ラベルなどの絞り込み条件だけの検索
- 101 件目以降のページ（開始位置が ``rank.fusion.window_size``\ （既定値 200）の半分以上の場合）
- CLIP サーバーに接続できないとき（``fess.log`` に ``Embedding provider is unavailable`` などの WARN が出ます）

一方、検索語と一緒に ``filetype:jpg`` のようなフィールド指定やラベルの絞り込みを使っても、ベクトル検索は実行され、その条件で絞り込まれます。

既存の Fess に組み込む
======================

``docker-multimodalsearch`` を使わずに既存の Fess 15.9 に組み込む場合は、次の手順で行います。

1. プラグインをインストールする
-------------------------------

``fess-webapp-multimodal`` の 15.9.x を、次のいずれかの方法でインストールし、Fess を再起動します。

- 管理画面の［システム］>［プラグイン］>［インストール］
- ``bin/fess-setup install plugin fess-webapp-multimodal:15.9.0``
- Docker の場合は環境変数 ``FESS_PLUGINS`` に ``fess-webapp-multimodal:15.9.0`` を加える

詳細は `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__ を参照してください。

2. CLIP サーバーを用意する
--------------------------

プラグインは、Jina の CLIP サーバーと同じ形式の HTTP API に接続します。
ベクトル化には ``POST /post``\ 、接続確認には ``GET /health`` を使います。
``/health`` が 2xx を返さないと、ベクトル検索は無効のまま動きます。
接続先は ``content_chunker.embedding.clip.api.url`` で指定し、既定値は ``http://localhost:51000`` です。

- プラグインのリポジトリにある ``docker/compose.yaml`` は ``jinaai/clip-server`` を起動します。設定 ``docker/clip_config.yaml`` はモデルを指定しておらず、既定のモデル（README では ViT-B/32、512 次元）が使われます。また、この Compose ファイルは GPU を要求します
- 日本語の検索語を使う場合は、\ ``docker-multimodalsearch`` の ``docker/clip-server`` のように、多言語対応のモデルを動かすサーバーを用意します

3. system.properties に設定する
-------------------------------

マルチモーダル検索の設定は ``system.properties`` に書きます。
場所は、ZIP 版が ``app/WEB-INF/conf/system.properties``\ 、RPM/DEB 版が ``/etc/fess/system.properties``\ 、Docker 版が ``/opt/fess/system.properties`` です。

::

    content_chunker.enabled=true
    content_chunker.embedding.name=clip
    content_chunker.embedding.dimension=512
    content_chunker.embedding.clip.api.url=http://localhost:51000
    content_chunker.search.enabled=true

- ``content_chunker.embedding.dimension`` は、CLIP モデルが出力する次元数に合わせます（ViT-B/32 系は 512）
- ``content_chunker.search.enabled`` は起動時にだけ読まれるため、設定後に Fess を再起動します
- 起動オプションで渡す場合は ``-Dfess.system.<キー名>`` を使います。``fess_config.properties`` や ``-Dfess.config.<キー名>`` に書いても無視され、警告も出ません
- ``system.properties`` の値は ``-Dfess.system.*`` より優先されます。両方に書くと、ファイルの値が使われます
- docker-fess の Compose ファイルでは ``fess01`` にボリュームがなく、\ ``docker compose down`` で ``system.properties`` が失われます。Docker では、環境変数 ``FESS_JAVA_OPTS`` に ``-Dfess.system.<キー名>=<値>`` を並べる方法が確実です（\ ``docker-multimodalsearch`` の ``compose.yaml`` もこの方法です）

キーの一覧は `セマンティック検索 <https://fess.codelibs.org/ja/stable/config/search-semantic.html>`__ の「設定リファレンス」を参照してください。
マルチモーダルでも同じ ``content_chunker.*`` を使います。

4. インデックスを再作成する
---------------------------

ベクトルフィールド ``content_chunk_vector`` のマッピングは、インデックスが作られるときに設定した次元数で作られます。
上記を設定する前に一度でも Fess を起動していた場合は、［システム情報］>［メンテナンス］の「再インデクシング」を、「エイリアスの更新」を有効にして実行します。
詳細は `メンテナンス <https://fess.codelibs.org/ja/stable/admin/maintenance-guide.html>`__ を参照してください。

5. サムネイルを有効にする
-------------------------

画像検索では、サムネイルがないと結果を見分けられません。
サムネイルは既定で無効です。

- ［システム］>［全般］で「サムネイル表示」を有効にして保存します
- 画像・PDF・Office 文書のサムネイル生成には ImageMagick などの外部ツールが必要です。Docker の既定（Alpine）イメージには含まれていないため、``-noble`` イメージ（例: ``ghcr.io/codelibs/fess:15.9.0-noble``）を使います

必要なツールは `サムネイル画像の設定 <https://fess.codelibs.org/ja/stable/config/crawler-thumbnail.html>`__ を参照してください。

6. クロールして確認する
-----------------------

GIF/JPEG/PNG の画像を含むサイトやフォルダーをクロールします。
画像のベクトルはクロール時に書き込まれます。

検索 API で ``searcher`` を確認する場合は、\ ``fess_config.properties`` に ``query.additional.api.response.fields=searcher`` を設定します（起動オプションなら ``-Dfess.config.query.additional.api.response.fields=searcher``）。

スケジューラの「Content Chunk Vector Indexer」ジョブは無効のままにします（既定で無効です）。
画像のベクトルはクローラーが書き込むため、このジョブは不要です。
有効にすると、テキスト文書も CLIP のテキスト側でベクトル化され、``content`` フィールドが分割されます。

運用上の注意
============

テキストのセマンティック検索とは併用できない
--------------------------------------------

プラグインは、本体のセマンティック検索の検索処理（``semanticChunkSearcher``）を CLIP 用のものに置き換えます。
また、``content_chunker.embedding.name`` には 1 つの値しか設定できません。
そのため、:doc:`guide-18` のテキストのセマンティック検索と、マルチモーダル検索は、1 つの Fess で同時に使えません。
両方が必要な場合は、Fess を分けて構築します。

なお、``rank.fusion.searchers`` で使う検索処理を絞っている場合は、``multi_modal`` を含めないとベクトル検索が除外されます。
通常はこの設定を空のままにします。

モデルを変えるときは再クロールまで行う
--------------------------------------

モデルと次元数は必ず一緒に変更します。
次元数はインデックス作成時にマッピングに固定されるため、変更後は次の手順が必要です。

1. ［システム情報］>［メンテナンス］で「再インデクシング」（「エイリアスの更新」を有効）を実行し、新しい次元数でインデックスを作り直す
2. 再クロールする

再インデクシングは文書をコピーするだけで、ベクトルを計算し直しません。
次元数が同じでも、モデルや CLIP サーバーを替えるとベクトル空間が変わるため、文書を削除してから再クロールします。
``docker-multimodalsearch`` では ``.env`` の ``CLIP_MODEL_NAME`` と ``MULTIMODAL_DIMENSION`` を変更します。
手順は README の「Model swap」にあります。

CPU と GPU
----------

``docker-multimodalsearch`` の既定モデル（512 次元）は CPU で動作する前提で、``CLIP_DEVICE=cpu`` が既定です。
より大きな ``xlm-roberta-large-ViT-H-14::frozen_laion5b_s13b_b90k``\ （1024 次元）に替える場合は GPU が推奨され、``CLIP_DEVICE=auto`` にすると GPU があれば使います。

まとめ
======

- ``fess-webapp-multimodal`` は、テキストで GIF/JPEG/PNG の画像を探す機能です。画像による検索や、文書に埋め込まれた画像のベクトル化はできません
- 試すなら ``docker-multimodalsearch`` の ``v15.9.0`` を使い、``FESS_THEMES_REF=15.9.x`` を指定します
- 設定は ``content_chunker.*`` を ``system.properties``\ （または ``-Dfess.system.*``）に書きます
- ベクトル検索が使われたかは、検索 API の ``searcher`` の ``multi_modal`` で確認します
- 日本語の検索語には多言語モデルが必要で、テキストのセマンティック検索とは同じ Fess で併用できません

次に読む記事
============

- :doc:`guide-18` — テキスト文書をベクトルで検索する（マルチモーダルとは別の構成）
- :doc:`guide-02` — Docker で Fess を動かす基本
- :doc:`guide-11` — 検索 API で業務システムと連携する

参考資料
========

- `docker-multimodalsearch（v15.9.0） <https://github.com/codelibs/docker-multimodalsearch/tree/v15.9.0>`__
- `fess-webapp-multimodal（15.9.0） <https://github.com/codelibs/fess-webapp-multimodal/tree/fess-webapp-multimodal-15.9.0>`__
