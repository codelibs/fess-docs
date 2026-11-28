==========================================
MCP で AI エージェントから Fess を検索する
==========================================

はじめに
========

Claude Code などの AI エージェントに社内文書を調べさせたいとき、エージェントが Fess の検索を直接呼び出せれば、インデックス済みの文書をそのまま根拠に使えます。
そのための仕組みが MCP（Model Context Protocol）です。
Fess では、プラグイン ``fess-webapp-mcp`` を入れると ``/mcp`` に MCP サーバーのエンドポイントが追加されます。

本記事では、Fess 15.9 にこのプラグインを導入し、認証を必須にしたうえで AI エージェントから接続し、動作を確かめるまでを説明します。

この記事の手順を終えると、次の状態になります。

- ``/mcp`` が動いていることを ``curl`` で確かめられる
- アクセストークンを持たない呼び出しは拒否される
- エージェントが検索できる文書の範囲を、トークンのパーミッションで決められる
- Claude Code から Fess の ``search`` ツールを呼び出せる

.. note::

   :doc:`guide-19` の AI 検索モードとは、呼び出しの向きが逆です。
   AI 検索モードでは、Fess が LLM（Ollama、OpenAI など）を呼び出して回答を作ります。Ollama はそのための LLM の実行環境で、MCP クライアントではありません。
   MCP では、外部の AI エージェントが Fess を検索ツールとして呼び出し、回答はエージェント側の LLM が作ります。

``/mcp`` が提供するもの
=======================

``/mcp`` は ``POST`` だけを受け付け、1 回のリクエストに 1 つの JSON を返します（セッションは持ちません）。
検索は検索画面と同じ処理を通るため、ロールによる検索結果の出し分けがそのまま効きます。

15.9.0 のプラグインが公開するものは次のとおりです。
すべて読み取り専用で、Fess のデータを書き換えるものはありません。

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - 名前
     - 内容
     - 利用できる条件
   * - ``search`` （ツール）
     - 全文検索。結果の各件に ``doc_id`` が付きます
     - 常に利用可
   * - ``suggest`` （ツール）
     - 入力途中の語に対するサジェスト候補
     - 常に利用可
   * - ``get_document`` （ツール）
     - ``doc_id`` を指定して 1 件の本文を取得します
     - 常に利用可
   * - ``get_index_stats`` （ツール）
     - インデックス名、文書数、JVM のメモリ使用量
     - 初期設定では使えません（後述）
   * - ``fess://document/{doc_id}`` （リソース）
     - ``get_document`` と同じ取得をリソースとして行います
     - 常に利用可
   * - ``fess://index/stats`` （リソース）
     - ``get_index_stats`` と同じ内容
     - ``get_index_stats`` と同じ
   * - ``basic_search`` / ``advanced_search`` （プロンプト）
     - 検索用のプロンプトのひな形。``advanced_search`` は ``sort`` と ``num`` も受け取ります
     - 常に利用可

``search`` で ``num`` を省略すると、返るのは 3 件だけです（``mcp.default.page.size`` の初期値）。
本文は ``search`` の抜粋も ``get_document`` の本文も最大 10000 文字に切り詰められ、``get_document`` では ``truncated`` が ``true`` になります（``mcp.content.max.length``）。

プラグインを導入する
====================

プラグインのバージョンは Fess のマイナーバージョンに合わせます。
Fess 15.9 には ``fess-webapp-mcp`` の 15.9.x を使います。
次のいずれかの方法で導入し、導入後は Fess を再起動します。

- 管理画面: ［システム］>［プラグイン］で［インストール］をクリックし、［リモート］タブで ``fess-webapp-mcp`` を選んでインストールします
- コマンドライン: ``bin/fess-setup install plugin fess-webapp-mcp:15.9.0``
- Docker: ``compose.yaml`` の ``fess01`` の ``environment`` に ``FESS_PLUGINS`` を追加します。Docker イメージにはこのプラグインは同梱されていません

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"

Docker 版で名前やバージョンの指定が誤っていると、そのプラグインは読み飛ばされ、コンテナはそのまま起動します。
追加した後は起動ログでプラグインの取得を確かめてください。

.. warning::

   Fess をアップグレードするときは、起動する前にこのプラグインも新しい版に入れ替えてください。
   古い版（例: 15.8 用）のプラグインの jar が ``WEB-INF/plugin`` に残ったままだと、Fess 15.9 は起動時の初期化に失敗し、``/mcp`` だけでなくすべての画面と API が 404 を返します。
   コマンドラインでは ``bin/fess-setup upgrade plugins`` で入れ替えられます。

再起動後、ログファイル ``fess.log`` に次の WARN が出ていれば、エンドポイントは有効になっています。

::

    [MCP] mcp.auth.mode=none - every /mcp caller is treated as anonymous. Set mcp.auth.mode=fess_token, ...

このメッセージは、次の節で説明する「認証なし」の状態で動いていることを示しています。

まず認証なしで動作を確かめる
============================

.. warning::

   導入した直後の ``/mcp`` は認証なしで動きます（``mcp.auth.mode=none``）。
   ``/mcp`` に届く人は誰でも、ログインしていない利用者（ゲスト）と同じ権限で検索し、``get_document`` で文書の本文まで取得できます。
   パーミッションを初期値の ``{role}guest`` のままにしたクロール設定の文書は、すべて対象になります。
   この状態で試すのは手元の環境にとどめ、次の節で認証を必須にしてください。
   なお、［システム］>［全般］で「ログインが必要」を有効にしている場合は、この状態の ``/mcp`` はすべての呼び出しを HTTP 403 で拒否します。その場合は次の節に進んでください。

Fess が ``http://localhost:8080`` で動いているとして、``server/discover`` を呼び出します。

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json, text/event-stream' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: server/discover' \
        -d '{"jsonrpc":"2.0","id":1,"method":"server/discover","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

応答の ``result.supportedVersions`` に ``2026-07-28`` が、``result.capabilities`` に ``tools`` などが入っていれば成功です。

続いて ``search`` ツールを呼び出します。
クロール済みの文書に含まれる語を ``q`` に指定してください。

::

    $ curl -sS -X POST http://localhost:8080/mcp \
        -H 'Content-Type: application/json' \
        -H 'MCP-Protocol-Version: 2026-07-28' \
        -H 'Mcp-Method: tools/call' \
        -H 'Mcp-Name: search' \
        -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search","arguments":{"q":"Fess","num":5},"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{}}}}'

``result.structuredContent.hits`` に検索結果が、``total`` にヒット件数が入ります。
ヘッダーの値は本文と一致している必要があります。
``MCP-Protocol-Version`` は ``params._meta`` のバージョンと、``Mcp-Method`` は ``method`` と、``Mcp-Name`` はツール名と同じ値にします。
食い違うと HTTP 400（エラーコード ``-32020``）になります。

認証を必須にする
================

Fess のアクセストークンで認証する ``fess_token`` モードに切り替えます。
外部の認可サーバーが発行する JWT で認証する ``oauth`` モードもあります。
設定は README の「OAuth 2.1 reference」を参照してください。

アクセストークンを作る
----------------------

1. 管理画面の［システム］>［アクセストークン］を開き、［新規作成］をクリックします
2. 「名前」に ``mcp-agent`` のような用途のわかる名前を入力します
3. 「パーミッション」に、エージェントに見せてよい文書のロールを 1 行に 1 つずつ入力します。ゲスト向けの文書だけでよければ ``{role}guest`` です（決め方は「トークンのパーミッションと検索結果」で説明します）
4. 必要に応じて「有効期限」を指定し、［作成］をクリックします
5. 一覧で作成したトークンの名前をクリックすると、詳細画面の「トークン」に値が表示されます

mcp.auth.mode を設定する
------------------------

``mcp.*`` の設定はすべて Fess のシステムプロパティ（``system.properties``）から読み込まれます。
``fess_config.properties`` や ``-Dfess.config.*`` に書いても無視され、エラーもログも出ません。

ZIP 版は ``app/WEB-INF/conf/system.properties``、RPM/DEB 版は ``/etc/fess/system.properties`` に次の行を追加します。

::

    mcp.auth.mode=fess_token

値は実行中に読み直されるため、数秒で反映され、再起動は不要です。

Docker 版の ``fess01`` コンテナにはボリュームがなく、コンテナ内のファイルに書いた設定はコンテナを作り直すと消えます。
``compose.yaml`` の ``FESS_JAVA_OPTS`` に ``-Dfess.system.`` を付けて指定してください（``fess.config.`` ではありません）。

::

    environment:
      - "FESS_PLUGINS=fess-webapp-mcp:15.9.0"
      - "FESS_JAVA_OPTS=-Dfess.system.mcp.auth.mode=fess_token"

``FESS_PLUGINS`` と ``FESS_JAVA_OPTS`` は、コンテナを作り直したときに反映されます。
``compose.yaml`` を編集したら、次のコマンドを実行します。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

``system.properties`` に同じキーがあれば、そちらが優先されます。

認証が効いていることを確かめる
------------------------------

前の節の ``server/discover`` を、そのままもう一度実行します。
トークンを付けていないので、HTTP 401 と ``WWW-Authenticate: Bearer realm="fess-mcp"`` ヘッダーが返ります（``curl -i`` でヘッダーを表示できます）。
``fess_token`` モードでは ``server/discover`` も認証の対象です。

次に、前の節の ``search`` の ``curl`` に ``-H 'Authorization: Bearer <トークン>'`` を加えて実行します。
``<トークン>`` は詳細画面に表示された値に置き換えます。
検索結果が返れば設定は完了です。
存在しないトークンや期限切れのトークンでは、HTTP 401 になります。

トークンのパーミッションと検索結果
==================================

``fess_token`` モードでは、トークンのパーミッションがそのまま検索のロールになります。
``search`` だけでなく ``get_document`` も同じロールで絞り込まれるため、``doc_id`` を知っていても権限のない文書は取得できません。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - トークンのパーミッション
     - 検索できる文書
   * - 空欄
     - ゲストと同じ（``{role}guest`` の文書）
   * - ``{role}guest``
     - ゲストと同じ
   * - ``{role}sales``
     - ``{role}sales`` の文書だけ。ゲスト向けの文書は含まれません
   * - ``{role}sales`` と ``{role}guest``
     - 両方の文書

ゲストのロールが補われるのは、パーミッションが空のトークンだけです。
部署の文書と全員向けの文書の両方を検索させたい場合は、``{role}guest`` も並べて指定します。
ロールとパーミッションの考え方は :doc:`guide-05` を参照してください。

確かめるには、パーミッションの異なる 2 つのトークンで同じ語を ``search`` し、``total`` を比べます。

.. warning::

   エージェント用のトークンに ``{role}admin-api`` を付けないでください。
   ``{role}admin-api`` を持つトークンは、Fess の Admin API をすべて呼び出せます。
   さらに、``{role}admin-api`` だけのトークンで ``search`` すると、このロールを持つ文書がないため 0 件になります。

``get_index_stats`` を使えるようにする
--------------------------------------

``get_index_stats`` と ``fess://index/stats`` は、``mcp.tools.index_stats.permissions`` に挙げたパーミッションのどれかを持つ呼び出し元にだけ表示されます。
初期値は ``Radmin-api`` （``{role}admin-api`` の内部表記）で、``none`` モードではどの呼び出し元もパーミッションを持たないため、誰にも表示されません。
権限のない呼び出し元には、存在しないツールと同じエラーが返ります。

検索だけならこのツールは不要です。
使う場合は、``{role}admin-api`` を渡す代わりに専用のロールを決め、そのロールをトークンのパーミッションに加えます。
``system.properties`` 側は内部表記（``{role}`` は ``R``）で書きます。

::

    mcp.tools.index_stats.permissions=Rmcp-stats

この例では、トークンのパーミッションに ``{role}mcp-stats`` を追加します。

そのほかの設定
==============

どれも ``system.properties`` に書きます（Docker 版は ``-Dfess.system.<キー>``）。
真偽値は ``true`` だけが真として扱われ、``1`` や ``yes`` は偽になります。

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - キー
     - 初期値
     - 内容
   * - ``mcp.allowed.origins``
     - （空）
     - ブラウザーから呼び出す場合に許可する ``Origin`` を ``https://app.example.com`` の形でカンマ区切りで指定します。空のときは ``Origin`` ヘッダー付きのリクエストをすべて HTTP 403 で拒否します。``curl`` や CLI のエージェントは ``Origin`` を送らないため影響を受けません
   * - ``mcp.rate.limit.per.minute``
     - ``60``
     - 呼び出し元（トークン、なければ IP アドレス）ごとの 1 分あたりの ``tools/call`` などの上限。超えると HTTP 429 と ``Retry-After`` が返ります。``0`` で無効
   * - ``mcp.content.max.length``
     - ``10000``
     - ``search`` と ``get_document`` が返す本文の最大文字数
   * - ``mcp.default.page.size``
     - ``3``
     - ``search`` で ``num`` を省略したときの件数
   * - ``mcp.enabled``
     - ``true``
     - ``false`` にすると ``/mcp`` はすべて HTTP 503 を返します
   * - ``mcp.legacy.protocol.enabled``
     - ``true``
     - ``initialize`` で接続する旧版（``2025-11-25`` / ``2025-06-18``）のクライアントも受け付けます

次の 2 つは ``mcp.*`` と異なり、Fess 本体の ``fess_config.properties`` の設定です（Docker 版は ``-Dfess.config.<キー>``）。

- 別のホストのリバースプロキシを経由させる場合は、``rate.limit.trusted.proxies``\ （初期値 ``127.0.0.1,::1``）にプロキシの IP アドレスを加えます。加えないと、プロキシ経由の呼び出し元がすべて同じ上限を共有します
- ブラウザーから別オリジンで呼び出す場合は、``mcp.allowed.origins`` のほかに ``api.cors.allow.headers`` へ ``MCP-Protocol-Version``・``Mcp-Method``・``Mcp-Name`` を加えます。詳しくは README の「Browser clients」を参照してください

AI エージェントから接続する
===========================

Claude Code
-----------

Claude Code は ``2026-07-28`` で直接接続できます。
``claude mcp add`` で HTTP の MCP サーバーとして登録し、``--header`` でトークンを渡します。

::

    $ claude mcp add --transport http fess http://localhost:8080/mcp \
        --header "Authorization: Bearer <トークン>"

``claude mcp list`` を実行すると、登録した ``fess`` が表示され、接続の状態も確かめられます。
Claude Code に「Fess で出張精算の手順を検索して」のように頼むと、エージェントは ``search`` ツールを次のような引数で呼び出し、結果の ``doc_id`` で ``get_document`` を呼んで本文を読みます。

.. code-block:: json

    {
      "name": "search",
      "arguments": {
        "q": "出張 精算",
        "num": 5,
        "fields": { "label": ["manual"] }
      }
    }

``fields`` の ``label`` には、Fess のラベルの値を指定します（ラベルで絞り込まない場合は省略します）。
``search`` の引数には、このほか ``start``\ （ページング）、``sort``\ （``last_modified.desc`` など）、``lang`` などがあります。

ほかのクライアント
------------------

OpenCode、Codex CLI、Gemini CLI などの旧版（``initialize``）で接続するクライアントも、``mcp.legacy.protocol.enabled`` が初期値の ``true`` であれば使えます。
``2025-03-26`` 以前の版しか話せないクライアントは接続できません。
stdio でしか MCP サーバーを起動できないデスクトップ向けクライアントは、stdio と HTTP を中継する ``mcp-remote`` を経由します。
クライアントごとの接続可否は README の「Client compatibility」にまとまっています。

検索結果の外部送信に注意する
----------------------------

エージェントが使う LLM がクラウドのサービスであれば、``search`` の抜粋や ``get_document`` の本文は、そのサービスに送られます。
トークンのパーミッションで送ってよい文書だけを選び、必要に応じて ``mcp.content.max.length`` を小さくすると、送られる範囲を絞れます。

うまくいかないとき
==================

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 症状
     - 原因と対処
   * - HTTP 400、エラーコード ``-32020``
     - ``MCP-Protocol-Version``・``Mcp-Method``・``Mcp-Name`` の欠落、または本文との不一致
   * - HTTP 401
     - ``fess_token`` モードでトークンがない、存在しない、または期限切れ
   * - すべてのリクエストが HTTP 403
     - ``Origin`` ヘッダーが ``mcp.allowed.origins`` にない。または ``none`` モードで「ログインが必要」が有効
   * - 最初の呼び出しが ``-32601`` で ``initialize`` に触れている
     - 旧版のクライアントで、``mcp.legacy.protocol.enabled`` が ``true`` でない
   * - ``search`` が 0 件
     - トークンのパーミッションに文書のロールがない。結果の ``partial`` が ``true`` なら、検索が完了しておらず（タイムアウトや OpenSearch の障害）、該当なしとは限りません
   * - ``Tool execution failed (error_code:...)``
     - 原因は ``fess.log`` に WARN で記録されています。``error_code`` の値でログを検索します

次に読む記事
============

- MCP 経由で見せる文書をロールで分けたい: :doc:`guide-05`
- Fess 自身に LLM で回答させたい: :doc:`guide-19`
- キーワードが一致しなくても意味の近い文書を探したい: :doc:`guide-18`
- 検索 API を業務システムから使いたい、アクセストークンを使い分けたい: :doc:`guide-11`
- SSO やアクセス保護をまとめて設定したい: :doc:`guide-15`

参考資料
========

- `fess-webapp-mcp README（15.9.0） <https://github.com/codelibs/fess-webapp-mcp/blob/fess-webapp-mcp-15.9.0/README.md>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `アクセストークン <https://fess.codelibs.org/ja/stable/admin/accesstoken-guide.html>`__
- `Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__
- `Model Context Protocol <https://modelcontextprotocol.io/>`__
