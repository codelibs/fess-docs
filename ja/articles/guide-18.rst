==================================================
セマンティック検索を有効にして意味の近い文書を探す
==================================================

はじめに
========

利用者が「給料の振込先を変えたい」と検索しても、社内規程の表記が「給与口座の変更手続き」であれば、キーワード検索では見つかりません。
Fess 15.9 では、本文を意味のベクトルに変換して検索する「セマンティック検索」が本体に組み込まれており、プラグインなしで使えます（埋め込みモデルの接続先によってはプラグインを追加します）。

この記事の手順を実行すると、次のことができるようになります。

- セマンティック検索が役立つ場面と、キーワード検索で足りる場面を見分ける
- Docker で、セマンティック検索が設定済みの環境をすぐに動かす
- 既存の Fess で ``content_chunker.*`` を設定し、インデクサージョブでベクトルを作る
- 検索結果がベクトル検索で見つかったものかを ``searcher`` フィールドで確かめる

AI 検索モード（RAG）の設定は :doc:`guide-19` で扱います。

セマンティック検索が役立つ場面
==============================

Fess のセマンティック検索は、キーワード検索（BM25）を置き換えるものではありません。
キーワード検索とベクトル検索の両方を実行し、結果を Rank Fusion（RRF）で 1 つの順位にまとめる「ハイブリッド検索」として動きます。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - セマンティック検索が役立つ
     - キーワード検索で足りる
   * - 利用者と文書で言葉が違う（「振込先」と「給与口座」、「在宅勤務」と「テレワーク」）
     - 製品型番、エラーコード、人名など、文書と同じ文字列で探す
   * - 文章で質問する（「新しい PC を申請するには」）
     - 言い換えの組み合わせが少なく、同義語辞書に登録しきれる
   * - 日本語で検索して英語の文書を見つけたい（多言語対応の埋め込みモデルが必要）
     - フレーズ指定やワイルドカードなどの検索構文を使う（この場合はベクトル検索自体が実行されません）

言い換えの組み合わせが限られているなら、先に同義語辞書を試すほうが手軽です。
検索ログのゼロヒット語から同義語を登録する手順は :doc:`guide-08` を参照してください。

Fess の中での処理の流れ
=======================

#. クローラーが通常どおり文書をインデックスに登録します。この時点ではベクトルはありません。
#. スケジューラのジョブ ``Content Chunk Vector Indexer`` が未処理の文書を見つけ、本文をチャンク（断片）に分け、チャンクごとに埋め込みベクトルを作って ``content_chunk_vector`` フィールドに保存します。結果は ``content_chunk_status`` フィールドに記録されます。
#. ``content_chunker.search.enabled=true`` のとき、検索のたびにキーワード検索（サーチャー名 ``default``）とベクトル検索（サーチャー名 ``semantic_chunk``）が実行され、RRF で融合されます。

このジョブは初期状態で無効で、クロールとも連動しません。
設定を入れただけではベクトルが作られず、検索結果もキーワード検索のままになる点に注意してください。

前提条件
========

**k-NN プラグイン入りの OpenSearch**

Fess 15.9 が作る検索インデックスには、セマンティック検索を使うかどうかにかかわらず ``knn_vector`` 型のフィールドが含まれます。
Docker の ``ghcr.io/codelibs/fess-opensearch`` イメージや標準配布の OpenSearch には k-NN プラグインが入っています。
k-NN プラグインを含まない minimal 配布では、インデックスを作れず Fess が起動しません。

**埋め込みプロバイダー**

テキストをベクトルに変換するモデルの接続先を ``content_chunker.embedding.name`` で選びます。

.. list-table::
   :header-rows: 1
   :widths: 18 32 50

   * - 設定値
     - 必要なもの
     - 内容
   * - ``opensearch``\ （既定）
     - 追加プラグイン不要
     - OpenSearch の ML Commons にデプロイしたモデルを使います
   * - ``ollama``
     - プラグイン ``fess-llm-ollama``
     - Ollama の埋め込みモデルを使います（既定のモデルは ``embeddinggemma``）
   * - ``openai``
     - プラグイン ``fess-llm-openai``
     - OpenAI の埋め込み API を使います（既定のモデルは ``text-embedding-3-small``）
   * - ``gemini``
     - プラグイン ``fess-llm-gemini``
     - Google Gemini の埋め込み API を使います
   * - ``bedrock``
     - プラグイン ``fess-llm-bedrock``
     - Amazon Bedrock の埋め込みモデルを使います

プラグインは Fess と同じマイナーバージョン（15.9.x）を入れ、インストール後に Fess を再起動します。
OpenAI・Gemini・Bedrock は従量課金のため、初回のジョブ実行で既存の全文書分の利用料金が一度に発生します。

最短の方法：docker-semanticsearch で試す
========================================

docker-semanticsearch リポジトリは、セマンティック検索を設定済みの Fess 15.9 を Docker Compose で起動します。
OpenSearch の ML Commons に多言語の埋め込みモデル（``paraphrase-multilingual-MiniLM-L12-v2``、384 次元）を自動でデプロイし、インデクサージョブの有効化まで済ませます。

::

    $ git clone --branch v15.9.0 https://github.com/codelibs/docker-semanticsearch.git
    $ cd docker-semanticsearch
    $ FESS_THEMES_REF=15.9.x bash ./bin/setup.sh
    $ docker compose up -d
    $ docker compose logs -f init-semantic init-fess-chunk

``setup.sh`` は検索画面のテーマ ``semanticlens`` を ``fess-themes`` リポジトリから取得します。
``v15.9.0`` の既定の取得元 ``main`` にあるテーマは Fess 15.10 以降向け（``minFessVersion: 15.10``）のため、15.9 用のテーマがある ``15.9.x`` ブランチを ``FESS_THEMES_REF`` で指定しています。

初回はモデル（約 490MB）のダウンロードで数分かかります。
``docker compose ps -a`` で ``fess01`` が healthy になり、``init-semantic`` と ``init-fess-chunk`` が ``Exited (0)`` になったら準備完了です。

その後は通常の Fess と同じく、管理画面（\ ``http://localhost:8080/admin``\ ）でクロール設定を作り、クロールを実行します。
この構成ではインデクサージョブが 1 時間ごとに動きます。
すぐにベクトルを作りたいときは、［システム］>［スケジューラ］で ``Content Chunk Vector Indexer`` を開き、［今すぐ開始］をクリックします。

この構成は、本記事の後半で説明する設定のほかに次の値を使っています。

- 融合を OpenSearch 側で行う（\ ``rank.fusion.engine.enabled=true``\ ）
- チャンクの長さは 250 文字（モデルの入力上限が 128 トークンのため）
- 類似度の下限 ``content_chunker.search.min_score=0.5``
- 検索結果ごとに、キーワード・セマンティック・両方のどれで見つかったかを表示するテーマ ``semanticlens``

値の変更方法は、リポジトリの README の Configuration を参照してください。

既存の Fess でセマンティック検索を有効にする
============================================

ここでは、Ollama の ``embeddinggemma``\ （768 次元、多言語対応）を使う例で手順を示します。
内蔵の ``opensearch`` プロバイダーを使う場合は、手順 1・2 の代わりに ML Commons へモデルをデプロイし、``content_chunker.embedding.name=opensearch`` と ``content_chunker.embedding.opensearch.model.id`` を設定します。
手順は `セマンティック検索 <https://fess.codelibs.org/ja/stable/config/search-semantic.html>`__ の「セットアップ手順」にあります。

手順 1：プラグインを入れる
--------------------------

［システム］>［プラグイン］>［インストール］で ``fess-llm-ollama`` の 15.9.x を選んでインストールし、Fess を再起動します。
Docker の場合は ``compose.yaml`` の ``fess01`` に ``FESS_PLUGINS=fess-llm-ollama:15.9.0`` を指定します。

手順 2：埋め込みモデルを用意する
--------------------------------

Ollama を動かすサーバーでモデルを取得します。

::

    $ ollama pull embeddinggemma

手順 3：system.properties に設定を書く
--------------------------------------

``content_chunker.*`` の設定は ``system.properties`` からだけ読み込まれます。
``fess_config.properties`` や ``-Dfess.config.`` に書いても無視されます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - インストール形態
     - 書き込み先
   * - ZIP 版
     - ``app/WEB-INF/conf/system.properties``
   * - RPM/DEB 版
     - ``/etc/fess/system.properties``
   * - Docker（docker-fess）
     - ``compose.yaml`` の ``FESS_JAVA_OPTS`` に ``-Dfess.system.<キー名>=<値>`` の形で指定

Docker のコンテナ内の ``/opt/fess/system.properties`` も読み込まれますが、docker-fess の ``fess01`` にはボリュームがないため、``docker compose down`` で消えます。

次の内容を書きます。

::

    content_chunker.enabled=true
    content_chunker.embedding.name=ollama
    content_chunker.embedding.dimension=768
    content_chunker.embedding.ollama.api.url=http://localhost:11434
    content_chunker.embedding.ollama.model=embeddinggemma
    content_chunker.search.enabled=true

``api.url`` は Fess から見た Ollama のアドレスです。
Fess が Docker で動いている場合、``localhost`` はコンテナ自身を指すため、コンテナから到達できるアドレスに変えてください。

``content_chunker.embedding.dimension`` はモデルの出力次元数と必ず一致させます。
この値はインデックスを作る時点でマッピングに書き込まれ、後から変更できません。

手順 4：Fess を再起動する
-------------------------

``content_chunker.search.enabled`` を ``true`` にした変更は、再起動するまで反映されません（ほかの ``content_chunker.*`` は実行中に読み直されます）。

手順 5：既存のインデックスを作り直す
------------------------------------

一度でも Fess を起動したことがある環境では、新しい次元数のマッピングがインデックスに反映されていません。
［システム情報］>［メンテナンス］の「再インデクシング」で「エイリアスの更新」を有効にし、［開始］をクリックします。
初回起動の前に手順 3 を済ませた新規環境では不要です。

再インデクシングはバックグラウンドで非同期に進み、画面には完了が表示されません。
次の手順に進む前に、``fess.search`` と ``fess.update`` の両方のエイリアスが新しいインデックス（\ ``fess.<タイムスタンプ>``\ ）を指していることを確かめます。

::

    $ curl -s "http://localhost:9200/_cat/aliases/fess.search,fess.update?v"

古いインデックスは自動では削除されないため、確認が済んだら手動で削除します。
クロールのやり直しは不要です。
インデクサージョブは保存済みの本文からベクトルを作ります。

手順 6：インデクサージョブを有効にして実行する
----------------------------------------------

#. ［システム］>［スケジューラ］で ``Content Chunk Vector Indexer`` を開き、［編集］をクリックします。
#. 「状態」の「有効」にチェックを入れ、必要ならスケジュールを変えて［更新］をクリックします。既定のスケジュールは ``0 13 * * *``\ （毎日 13:00）です。
#. 詳細画面に戻ると［今すぐ開始］が表示されるので、クリックして 1 回実行します。

ジョブはクロールと連動しないため、クロールした文書はキーワードではすぐ検索できますが、ベクトル検索の対象になるのは次にこのジョブが動いた後です。
スケジュールは、クロールジョブが終わる時刻より後に設定してください。

動作を確認する
==============

ベクトルができたかを確かめる
----------------------------

文書ごとの処理結果を OpenSearch に集計させます。

::

    $ curl -s -XPOST "http://localhost:9200/fess.search/_search" \
        -H "Content-Type: application/json" -d '
    {"size": 0, "aggs": {"status": {"terms": {"field": "content_chunk_status", "missing": "pending"}}}}'

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 意味
   * - ``pending``
     - 未処理（次のジョブ実行で処理されます）。再クロールされた文書もここに戻ります
   * - ``done``
     - チャンク分割とベクトル生成が完了
   * - ``chunked``
     - チャンク分割のみ。プロバイダーのプラグインが入っていないときもこの状態になります
   * - ``skipped``
     - 本文が空、またはチャンク数が上限（既定 1000）を超えた
   * - ``fail``
     - 失敗。ログファイル ``fess-chunk.log`` で原因を確認します

ジョブを実行するたびに ``pending`` が減り、``done`` が増えていれば順調です。

ベクトル検索で見つかった結果かを確かめる
----------------------------------------

検索結果の ``searcher`` フィールドには、その文書を見つけたサーチャー名が入ります。
初期状態では検索 API の応答に含まれないため、``fess_config.properties`` に次の 1 行を追加して再起動します（Docker では ``-Dfess.config.query.additional.api.response.fields=searcher``）。

::

    query.additional.api.response.fields=searcher

キーワードが文書と一致しない言い換えで検索します。
「給与口座の変更手続き」を説明した文書があるなら、次のように検索します。

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=給料の振込先を変えたい" \
      | jq '.response.data[] | {title, searcher}'

``searcher`` が ``["semantic_chunk"]`` の結果はベクトル検索だけで見つかった文書、``["default", "semantic_chunk"]`` は両方で見つかった文書です。
すべての結果が ``["default"]`` だけなら、ベクトル検索が結果を返していません。
次の節を確認してください。

つまずきやすい点
================

**旧プラグイン時代の rank.fusion.searchers が残っている**

15.7 以前の ``fess-webapp-semantic-search`` プラグインでは ``-Drank.fusion.searchers=default,semantic`` を指定していました。
15.9 のサーチャー名は ``semantic_chunk`` なので、この設定が残っているとセマンティック検索が実行されず、キーワード検索の結果だけが返ります。
起動時に ``rank.fusion.searchers allows 'semantic' but not 'semantic_chunk'`` という WARN ログが出ます。
JVM オプションと［システム］>［全般］の「システムプロパティ」欄の両方を確認し、この設定を削除してください（指定しなければ全サーチャーが使われます）。
旧プラグインからの移行手順は `セマンティック検索 <https://fess.codelibs.org/ja/stable/config/search-semantic.html>`__ の「15.7 以前からアップグレードする場合の移行」を参照してください。

**検索構文を含むクエリではベクトル検索が実行されない**

次のクエリはキーワード検索だけで処理されます。

- フレーズ（\ ``"..."``\ ）、ワイルドカード、あいまい検索、範囲指定
- 半角の ``?`` で終わる文（「〜とは?」）。全角の「？」は対象外です
- 除外（\ ``-語``\ 、\ ``NOT 語``\ ）やブースト（\ ``語^2``\ ）
- 並び替えを指定した検索

``label:`` や ``site:``\ 、ファセットでの絞り込みは、ベクトル検索にもフィルタとして適用されるため問題ありません。

**次元数が合わない、または設定せずにインデックスを作った**

``content_chunker.embedding.dimension`` を設定しないままインデックスを作ると、マッピングは 768 次元になり、ジョブは文書を ``fail`` にします。
モデルの次元数が 768 以外なら、正しい値を設定してから手順 5 の再インデクシングをやり直します。
``fail`` と ``skipped`` はジョブを再実行しても処理し直されません。
原因を直した後、``content_chunker.job.retry_failed=true`` を一時的に設定してジョブを実行します。

**埋め込みモデルを変えた**

保存済みのベクトルは古いモデルで作られているため、モデルだけを変えると検索の精度が崩れます（次元数が同じでもエラーは出ません）。
``content_chunk_vector`` と ``content_chunk_status`` を削除してジョブを実行し直す手順が、リファレンスの「注意事項」にあります。

**関係の薄い文書まで上位に来る**

ベクトル検索は、類似度が低い文書も近い順に返します。
``content_chunker.search.min_score`` にコサイン類似度の下限（0〜1）を設定すると、それに届かない文書を除外できます。
適切な値はモデルと文書によって変わるため、ゼロヒットだった語と無関係な語の両方で検索しながら調整してください。

**2 ページ目以降の後半で結果の傾向が変わる**

Fess 側で融合する既定の構成では、融合されるのは各サーチャーの上位 200 件（\ ``rank.fusion.window_size``\ ）までで、101 件目以降はキーワード検索だけの結果になります。
ヒット件数も、ベクトル検索だけが見つけた文書の分だけ増えます。
融合の仕組みと調整項目（\ ``rank.fusion.rank_constant``\ 、OpenSearch 側での融合）は `ハイブリッド検索とランクフュージョン <https://fess.codelibs.org/ja/stable/config/rank-fusion.html>`__ を参照してください。

AI 検索モード・マルチモーダル検索との関係
=========================================

AI 検索モード（RAG）は、セマンティック検索を有効にしなくても使えます。
``content_chunker.enabled=true`` でベクトルが作られている文書については、回答に使う本文を質問に近いチャンクだけに絞り込むため、長い文書でも関連部分を LLM に渡せます。
AI 検索モードの設定は :doc:`guide-19` を参照してください。

画像とテキストをまとめて検索するマルチモーダル検索（\ ``fess-webapp-multimodal``\ ）は、同じ Fess で本記事のテキストのセマンティック検索と同時には使えません。
詳しくは :doc:`guide-21` を参照してください。

次に読む記事
============

- 検索ログのゼロヒット語を同義語やキーマッチで改善したい: :doc:`guide-08`
- 生成 AI に社内文書から回答させたい: :doc:`guide-19`
- 画像も含めて検索したい: :doc:`guide-21`
- 検索 API で業務システムから検索したい: :doc:`guide-11`

参考資料
========

- `セマンティック検索（コンテンツチャンク＋ベクトル検索） <https://fess.codelibs.org/ja/stable/config/search-semantic.html>`__
- `ハイブリッド検索とランクフュージョン <https://fess.codelibs.org/ja/stable/config/rank-fusion.html>`__
- `Ollama の設定 <https://fess.codelibs.org/ja/stable/config/llm-ollama.html>`__
- `スケジューラ <https://fess.codelibs.org/ja/stable/admin/scheduler-guide.html>`__
- `メンテナンス <https://fess.codelibs.org/ja/stable/admin/maintenance-guide.html>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `docker-semanticsearch（GitHub） <https://github.com/codelibs/docker-semanticsearch>`__
