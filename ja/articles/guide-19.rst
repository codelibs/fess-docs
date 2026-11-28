==========================================
AI 検索モード（RAG）で社内文書に答えさせる
==========================================

はじめに
========

検索結果を 1 件ずつ開いて読み比べる代わりに、「経費精算の締め日は？」と質問して社内文書に基づく答えを受け取りたい、という要望はよくあります。
Fess の AI 検索モード（RAG チャット）は、質問に関係する文書を Fess 自身が検索し、その内容を LLM（大規模言語モデル）に渡して回答を作らせ、根拠にした文書へのリンクを添えて返します。

本記事では、Fess 15.9 で AI 検索モードを動かし、使える人と参照する文書を絞り、画面と API で動作を確かめるところまでを扱います。
記事の手順を終えると、次のことができるようになります。

- 4 種類の LLM プロバイダーから 1 つを選び、対応するプラグインと設定を入れる
- Docker の Fess に、docker-fess が用意している重ね合わせ用の Compose ファイルで LLM をつなぐ
- チャットを使える利用者と、回答の根拠にする文書の範囲を絞る
- 検索画面、``/api/v2/chat``\ 、検索ログで、動いていることを確かめる

前提として、Fess が起動していて、文書がクロール済みである必要があります。
まだの場合は :doc:`guide-02` の手順で準備してください。
意味の近い文書を探すセマンティック検索は :doc:`guide-18`\ 、AI エージェントから Fess を検索させる MCP は :doc:`guide-20` で扱います。

AI 検索モードの仕組み
=====================

AI 検索モードは、専用のベクトルインデックスを使いません。
ふだんの検索と同じ検索処理（既定ではキーワード検索）で文書を探すため、埋め込みモデルやチャンク分割の準備なしで始められます。
セマンティック検索を有効にしている場合は、AI 検索モードの検索にも自動で加わります。

処理の流れは、呼び出すエンドポイントによって異なります。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - エンドポイント
     - 処理の流れ
   * - ``POST /api/v2/chat/stream``\ （検索画面の AI 検索が使う）
     - 意図の判定 → 検索 → LLM による関連度の評価 → 本文の取得 → 回答の生成。各段階の進み具合と回答の断片を Server-Sent Events で順に返します
   * - ``POST /api/v2/chat``
     - 意図の判定 → 検索 → 回答の生成。関連度の評価はなく、結果は 1 つの JSON で返ります

どちらも、検索結果が 0 件のときは LLM が検索語を作り直して検索し直します（既定で最大 2 回、``rag.chat.query.regeneration.max.count``\ ）。
1 つの質問で LLM を複数回呼び出すため、通常の検索より応答に時間がかかり、クラウドの LLM では呼び出しごとに料金がかかります。

LLM には、利用者の質問と、検索で見つかった文書の本文やその抜粋が送られます。
プロバイダーを選ぶときは、この送り先を確認してください。

会話は ``session_id`` で識別され、Fess のメモリ上に保持されます。
既定では 30 分操作がないと消え（``rag.chat.session.timeout.minutes``\ ）、1 つの会話に残すメッセージは 30 件までです（``rag.chat.history.max.messages``\ ）。
会話は Fess を再起動しても消えます。

LLM プロバイダーを選ぶ
======================

Fess 15.9 では、LLM との接続はプロバイダーごとの ``fess-llm-*`` プラグインで提供されます。
どのプロバイダーを使うかは ``rag.llm.name`` で指定します。

.. list-table::
   :header-rows: 1
   :widths: 14 12 18 22 34

   * - プロバイダー
     - ``rag.llm.name``
     - プラグイン
     - 既定のモデル
     - 接続に必要な設定と、質問・文書の送り先
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ``gemma4:e4b``
     - ``rag.llm.ollama.api.url``\ （既定 ``http://localhost:11434``\ ）。送り先は自分で動かす Ollama サーバーです
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - ``gpt-5-mini``
     - ``rag.llm.openai.api.key``\ 。送り先は OpenAI です
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - ``gemini-3.1-flash-lite-preview``
     - ``rag.llm.gemini.api.key``\ 。送り先は Google です
   * - Amazon Bedrock
     - ``bedrock``
     - ``fess-llm-bedrock``
     - ``us.amazon.nova-2-lite-v1:0``
     - ``rag.llm.bedrock.region``\ （既定 ``us-east-1``\ ）と、``rag.llm.bedrock.api.key`` または AWS 認証情報。送り先は指定したリージョンの Amazon Bedrock です

モデルは ``rag.llm.<プロバイダー>.model`` で変えられます。

OpenAI と Gemini は API キーを用意するだけで始められますが、質問と文書がそれぞれのサービスに送られます。
Ollama は質問と文書を自分のサーバーの外に出しませんが、モデルを動かすサーバーが必要です。
docker-fess の Ollama 用 Compose ファイルは NVIDIA の GPU を前提にしています。
Bedrock は AWS の認証情報とリージョンの設定が必要です。
設定方法は `Amazon Bedrock の設定 <https://fess.codelibs.org/ja/stable/config/llm-bedrock.html>`__ を参照してください。

必要な設定は 3 つ
=================

AI 検索モードを動かすには、次の 3 つがそろっている必要があります。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 設定
     - 設定する場所
     - Docker での渡し方
   * - ``rag.chat.enabled=true``\ （既定は ``false``\ ）
     - ``fess_config.properties``\ 。管理画面には項目がありません
     - ``FESS_JAVA_OPTS`` に ``-Dfess.config.rag.chat.enabled=true``
   * - ``fess-llm-*`` プラグイン
     - ［システム］>［プラグイン］、または ``bin/fess-setup``
     - ``FESS_PLUGINS=fess-llm-openai:15.9.0`` など
   * - ``rag.llm.name`` と、プロバイダーごとの接続設定
     - ``rag.llm.name`` は［システム］>［全般］、接続設定（``rag.llm.<プロバイダー>.*``\ ）は ``fess_config.properties``
     - ``-Dfess.system.rag.llm.name=openai``\ 、``-Dfess.config.rag.llm.openai.api.key=...`` など

``rag.llm.name`` の既定値は ``ollama`` です。
OpenAI のプラグインだけを入れて ``rag.llm.name`` を変えないと、Fess は存在しない Ollama 用のクライアントを探し続け、AI 検索モードは使えません。
このとき、ログに ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` という警告が出ます。

``-Dfess.system.rag.llm.name`` は、``system.properties`` に値がないときだけ使われる初期値です。
［全般］で保存した値が ``system.properties`` に書かれると、そちらが優先されます。

Docker で動かす（OpenAI・Gemini）
=================================

docker-fess には、LLM をつなぐための重ね合わせ用 Compose ファイルが用意されています。
:doc:`guide-02` で Compose ファイルを置いたディレクトリで、v15.9.0 のファイルを取得します。

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-openai.yaml

API キーをシェルの環境変数に入れて、3 つのファイルを指定して起動します。

::

    $ export OPENAI_API_KEY="sk-..."
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml up -d

``compose-openai.yaml`` は ``fess01`` に次の環境変数を足します。
API キーとモデル名は、シェルの ``OPENAI_API_KEY`` と ``OPENAI_MODEL``\ （未設定なら ``gpt-5-mini``\ ）から設定されるため、ファイルにキーを書く必要はありません。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-llm-openai:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.rag.chat.enabled=true -Dfess.config.rag.llm.openai.api.key=${OPENAI_API_KEY:-} -Dfess.config.rag.llm.openai.model=${OPENAI_MODEL:-gpt-5-mini} -Dfess.system.rag.llm.name=openai"

``FESS_PLUGINS`` のプラグインは、コンテナの起動時に Fess より先に導入されるため、別途再起動する必要はありません。
すでに ``fess01`` が動いている場合、このコマンドで ``fess01`` は作り直され、［全般］で変更していた設定はコンテナと一緒に消えます。
以降の ``ps``\ ・``logs``\ ・``down`` などのコマンドにも、同じ 3 つのファイルを指定してください。

Gemini の場合は ``compose-gemini.yaml`` を取得し、``GEMINI_API_KEY`` を設定して、同じように 3 つ目のファイルとして指定します。
このファイルはモデルを ``GEMINI_MODEL``\ （未設定なら ``gemini-2.5-flash``\ ）から設定するので、プラグインの既定モデルではなく ``gemini-2.5-flash`` が使われます。

.. note::

   ``FESS_JAVA_OPTS`` を設定する重ね合わせ用ファイルを 2 つ以上指定すると、最後のファイルの値だけが使われます（OCR 用の設定などと組み合わせる場合）。
   その場合は、必要な ``-D`` オプションをすべて 1 つの ``FESS_JAVA_OPTS`` にまとめた Compose ファイルを自分で用意します。
   ``FESS_JAVA_OPTS`` は空白で区切られるため、値に空白を含むオプションは書けません。

``-Dfess.config.rag.llm.openai.api.key`` のように渡した API キーは、［システム情報］>［設定情報］ではマスクされて表示されます。
社内のプロキシを通して外部に出る必要がある場合は、``-Dfess.config.http.proxy.host=...`` と ``-Dfess.config.http.proxy.port=...`` を追加します。
LLM プラグインは Fess 共通のプロキシ設定を使います。

Docker で動かす（Ollama）
=========================

``compose-ollama.yaml`` は、Ollama のコンテナ ``ollama01`` を追加し、``fess01`` をそこにつなぎます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 対象
     - 設定される内容
   * - ``fess01``
     - ``FESS_PLUGINS=fess-llm-ollama:15.9.0``\ 、``-Dfess.config.rag.chat.enabled=true``\ 、``-Dfess.config.rag.llm.ollama.api.url=http://ollama01:11434``
   * - ``ollama01``
     - イメージ ``ollama/ollama:latest``\ 、ネットワーク ``search_net``\ 、ポート 11434、ボリューム ``ollama-data``\ 、NVIDIA GPU 1 基の割り当て

``rag.llm.name`` とモデルは設定されないため、既定値の ``ollama`` と ``gemma4:e4b`` が使われます。
URL を ``ollama01`` に向けているのは、既定の ``http://localhost:11434`` が ``fess01`` コンテナ自身を指してしまうためです。

::

    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-ollama.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-ollama.yaml up -d
    $ docker exec -it ollama01 ollama pull gemma4:e4b

このファイルを使うには、NVIDIA Container Toolkit が入った環境が必要です。
GPU のない環境で試す場合は、取得したファイルから ``ollama01`` の ``deploy:`` 以下を削除します。
CPU で動くため、回答には時間がかかります。

Fess は、設定されたモデルが Ollama のモデル一覧（``/api/tags``\ ）にあるときだけ Ollama を利用可能と判断し、この確認を既定で 60 秒ごとに行います。
そのため、モデルを取得してから 1 分ほどで AI 検索モードが使えるようになります。
ファイル冒頭のコメントには別のファイル名と ``gpt-oss:20b`` の取得手順が書かれていますが、上記の手順に従ってください。
別のモデルを使う場合は、そのモデルを ``ollama pull`` したうえで、``FESS_JAVA_OPTS`` に ``-Dfess.config.rag.llm.ollama.model=<モデル名>`` を追加します。

Docker 以外（ZIP・RPM・DEB）で設定する
======================================

1. プラグインを導入します。［システム］>［プラグイン］>［インストール］から選ぶか、コマンドで導入します

   ::

       $ bin/fess-setup install plugin fess-llm-openai:15.9.0

2. ``fess_config.properties`` に設定を追加します。ZIP 版は ``app/WEB-INF/classes/fess_config.properties``\ 、RPM/DEB 版は ``/etc/fess/fess_config.properties`` です

   ::

       rag.chat.enabled=true
       rag.llm.openai.api.key=sk-...
       rag.llm.openai.model=gpt-5-mini

3. Fess を再起動します。プラグインも ``fess_config.properties`` の変更も、再起動で読み込まれます
4. ［システム］>［全般］を開き、「AI検索」欄の「LLMプロバイダー」で ``openai`` を選んで［更新］をクリックします

「AI検索」欄は、``rag.chat.enabled=true`` で、かつ LLM プラグインが 1 つ以上読み込まれているときだけ表示されます。
「LLMプロバイダー」の選択肢は、導入済みのプラグインに対応するプロバイダーだけです。
欄が見当たらない場合は、手順 1〜3 を見直してください。

動作を確かめる
==============

検索画面で確かめる
------------------

1. ``http://localhost:8080/`` を開きます。上部のナビゲーションバーに、ロボットのアイコンが付いた［AI 検索］が表示されます
2. ［AI 検索］をクリックすると、チャットの画面（``/chat``\ ）が開きます
3. クロール済みの文書に答えがありそうな質問を入力します。:doc:`guide-02` で検索ガイドをクロールした場合は、「ワイルドカード検索で使える記号を教えてください」などで試せます

回答の生成中は、意図・検索・評価・取得・回答の各段階が順に表示されます。
回答の下には根拠にした文書が「出典」として番号付きで並び、本文中の ``[1]`` のような番号と対応します。
話題を変えるときは［新しいチャット］をクリックすると、会話の履歴が消えます。

［AI 検索］が表示されない場合は、後述の「つまずきやすい点」を確認してください。

API で確かめる
--------------

画面を使わずに確かめるには、``/api/v2/ui/config`` を呼びます。
``response.features.rag_chat_enabled`` が ``true`` なら、その利用者は AI 検索モードを使えます。

``/api/v2/chat`` などの状態を変えるリクエストには、セッションに結び付いた CSRF トークンを ``X-Fess-CSRF-Token`` ヘッダーで送る必要があります。
``/api/v2/ui/config`` の応答にトークンが含まれるので、Cookie を保存しながら取得し、同じ Cookie で呼び出します（例では ``jq`` を使います）。

::

    $ curl -s -c cookies.txt http://localhost:8080/api/v2/ui/config > ui-config.json
    $ jq '.response.features.rag_chat_enabled' ui-config.json
    true
    $ TOKEN=$(jq -r '.response.csrf_token' ui-config.json)
    $ curl -s -b cookies.txt -X POST http://localhost:8080/api/v2/chat \
        -H 'Content-Type: application/json' \
        -H "X-Fess-CSRF-Token: $TOKEN" \
        -d '{"message":"ワイルドカード検索で使える記号を教えてください"}' | jq '.response'

応答の ``content`` が回答、``sources`` が根拠にした文書（``rank``\ 、``title``\ 、``url`` など）、``session_id`` が会話の ID です。
続けて質問するときは、``{"message":"...","session_id":"<前回の session_id>"}`` のように ``session_id`` を送り返します。

この例はログインしない匿名の利用者として呼ぶため、``{role}guest`` が付いた文書だけが検索対象になります。
ログインした利用者として呼ぶ方法、ストリーミング版の ``/api/v2/chat/stream`` のイベント、エラーコードは `Chat API <https://fess.codelibs.org/ja/stable/api/api-chat.html>`__ と `API の概要 <https://fess.codelibs.org/ja/stable/api/api-overview.html>`__ を参照してください。
``/api/v1/chat`` は ``fess-webapp-v1-api`` プラグインを導入した場合だけ使える旧形式の API です。
新しく作る連携には ``/api/v2/chat`` を使ってください。

管理画面とログで確かめる
------------------------

［システム情報］>［検索ログ］の［AIチャット］タブに、リクエスト数、利用者数、合計トークン数、平均応答時間、エラー率と、利用者別・意図別・モデル別の件数が表示されます。
この記録は ``rag.chat.log.enabled``\ （既定 ``true``\ ）で有効になっており、質問と回答の本文は記録されません。
トークン数は LLM プラグインが報告した場合だけ記録されます。

Docker の場合、プラグインが導入されたかどうかはコンテナのログで確かめられます。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-openai.yaml logs fess01 | grep -E 'Installing|\[LLM\]'

``Installing fess-llm-openai-15.9.0.jar`` があれば導入済みです。
``[LLM] LlmClient not found`` が続けて出ている場合は、``rag.llm.name`` と導入したプラグインが合っていません。

利用者と参照する文書を絞る
==========================

AI 検索モードの検索には、ふだんの検索と同じロールによる絞り込みがかかります。
利用者が検索結果で見られない文書は、回答の根拠にも出典にも使われません。
文書ごとの見せ分けは、クロール設定の「パーミッション」で決まります。
設計の考え方は :doc:`guide-05` を参照してください。

そのうえで、［システム］>［全般］の「AI検索」欄で、チャットそのものの利用範囲を絞れます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 内容
   * - 「チャット権限」（``rag.chat.permissions``\ ）
     - チャットを使える利用者を ``{role}rag_user,{group}sales,{user}taro`` のようにカンマ区切りで指定します。空のときは全員が使えます。ログインしていない利用者にも使わせる場合は ``{role}guest`` を含めます
   * - 「チャットラベル」（``rag.chat.labels``\ ）
     - 回答の根拠にする文書を、指定したラベル値のいずれかが付いた文書に限ります。``faq,policy`` のようにカンマ区切りで指定し、空のときは利用者が見られるすべての文書が対象です

「チャット権限」の対象外の利用者には［AI 検索］が表示されず、API はログインしていなければ 401、ログインしていれば 403 を返します。
ログインした利用者には ``{role}guest`` が付かないため、``{role}guest`` だけを指定すると、ログインした利用者はチャットを使えなくなります。
有効な項目が 1 つもない値（``{role}`` だけ、など）を保存すると、誰も使えなくなります。

「チャットラベル」は、たとえば社内規程と FAQ のように、回答の根拠として信頼できる文書にラベルを付けておき、そこだけから答えさせたい場合に使います。
ラベルの作り方と付け方は :doc:`guide-04` を参照してください。

つまずきやすい点
================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 症状
     - 確認すること
   * - ［AI 検索］が表示されない
     - 次の順に確認します。(1) ``rag.chat.enabled=true`` が渡っているか。(2) プラグインが導入されているか（ログの ``Installing``\ ）。(3) ``rag.llm.name`` が導入したプラグインと合っているか（``LlmClient not found`` の警告）。(4) API キーが空でないか、Ollama ではモデルを取得したか。(5) 「チャット権限」から自分が外れていないか
   * - ［全般］に「AI検索」欄がない
     - ``rag.chat.enabled`` が ``false`` のままか、LLM プラグインが読み込まれていません。設定とプラグインの導入後に Fess を再起動したか確認します
   * - ``down`` と ``up -d`` の後に「LLMプロバイダー」が元に戻った
     - ［全般］の値は ``fess01`` コンテナ内の ``system.properties`` に保存されるため、コンテナを作り直すと消えます。``FESS_JAVA_OPTS`` の ``-Dfess.system.rag.llm.name`` で指定しておきます
   * - API が ``403`` を返す
     - CSRF トークンを ``X-Fess-CSRF-Token`` で送っているか、トークンを取得したときの Cookie を送っているかを確認します。ログインした利用者が「チャット権限」から外れている場合も 403 です
   * - API が ``429`` を返す
     - 利用者ごとに 1 分あたり 30 回までの制限があります（``api.chat.rate.limit.per.user.per.minute``\ ）
   * - クラウドの LLM に接続できない
     - コンテナから外部に出られるかを確認し、プロキシが必要なら ``http.proxy.host`` と ``http.proxy.port`` を設定します

回答の質を上げたいときは、まず検索の質を確かめます。
AI 検索モードは、通常の検索で上位に来た文書（既定 5 件、``rag.chat.context.max.documents``\ ）を根拠にするため、同じ質問の言葉で検索して関係のない文書が上位に来るなら、回答もそれに引きずられます。
検索の改善は :doc:`guide-08` で扱います。
プロンプトタイプごとの温度や最大トークン数、プロンプトの差し替えは `LLM 統合の概要 <https://fess.codelibs.org/ja/stable/config/llm-overview.html>`__ を参照してください。

次に読む記事
============

- キーワードが一致しなくても意味の近い文書を検索に加えたい: :doc:`guide-18`
- Claude などの AI エージェントから Fess を検索させたい: :doc:`guide-20`
- 部署やロールによって検索できる文書を分けたい: :doc:`guide-05`
- 検索ログを見て検索の質を改善したい: :doc:`guide-08`
- SSO でログインさせて、利用者ごとに見せ分けたい: :doc:`guide-15`

参考資料
========

- `AI検索モード機能の設定 <https://fess.codelibs.org/ja/stable/config/rag-chat.html>`__
- `AI検索（RAG）と LLM 統合の概要 <https://fess.codelibs.org/ja/stable/config/llm-overview.html>`__
- `Ollama の設定 <https://fess.codelibs.org/ja/stable/config/llm-ollama.html>`__
- `OpenAI の設定 <https://fess.codelibs.org/ja/stable/config/llm-openai.html>`__
- `Google Gemini の設定 <https://fess.codelibs.org/ja/stable/config/llm-gemini.html>`__
- `Amazon Bedrock の設定 <https://fess.codelibs.org/ja/stable/config/llm-bedrock.html>`__
- `Chat API <https://fess.codelibs.org/ja/stable/api/api-chat.html>`__
- `AI検索モード（利用者向け） <https://fess.codelibs.org/ja/stable/user/chat-search.html>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `docker-fess の compose ディレクトリ（v15.9.0） <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose>`__
