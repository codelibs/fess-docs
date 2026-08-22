============================
AI検索（RAG）とLLM統合の概要
============================

概要
====

|Fess| は、大規模言語モデル（LLM）を活用したAI検索モード（RAG: Retrieval-Augmented Generation）機能をサポートしています。
この機能により、ユーザーは検索結果を基にしたAIアシスタントとの対話形式で情報を取得でき、自然言語による質問に対して社内の検索インデックスから引用元付きで直接回答します。

LLM連携機能は ``fess-llm-*`` プラグインとして提供されます。利用するLLMプロバイダーに対応するプラグインを導入してください。

AI検索モードは、専用のベクトルインデックスではなく |Fess| の標準の検索パイプライン（Rank Fusion）を通じてドキュメントを取得し、
デフォルトではキーワード（BM25）検索が使用されます。この標準パイプラインを再利用しているため、コア内蔵の
セマンティック検索（コンテンツチャンク＋ベクトル検索）を有効にすると、そのセマンティックサーチャーは
AI検索モードの検索ステップを含むすべての検索でRank Fusionに参加します。
セマンティックサーチャーを参加させるためのAI検索モード専用の設定は不要です。ただし、回答生成に渡すチャンク数は
``content_chunker.chat.top_k`` で調整できます。詳細は :doc:`rank-fusion` および :doc:`search-semantic` を参照してください。

対応プロバイダー
================

|Fess| は以下のLLMプロバイダーをサポートしています。

.. list-table::
   :header-rows: 1
   :widths: 20 20 30 30

   * - プロバイダー
     - 設定値
     - プラグイン
     - 説明
   * - Ollama
     - ``ollama``
     - ``fess-llm-ollama``
     - ローカル環境で動作するオープンソースのLLMサーバー。Llama、Mistral、Gemmaなどのモデルを実行可能。デフォルト設定。
   * - OpenAI
     - ``openai``
     - ``fess-llm-openai``
     - OpenAI社のクラウドAPI。GPT-5などのモデルを利用可能。
   * - Google Gemini
     - ``gemini``
     - ``fess-llm-gemini``
     - Google社のクラウドAPI。Geminiモデルを利用可能。

プロバイダー比較
----------------

.. list-table::
   :header-rows: 1

   * - プロバイダー（ ``rag.llm.name`` ）
     - デフォルトモデル
     - エンドポイント
     - 認証
     - データの保存場所
   * - Ollama（ ``ollama`` ）
     - ``gemma4:e4b``
     - ``http://localhost:11434``
     - なし（ローカル）
     - ローカル / セルフホスト — 質問とドキュメントはホスト内に留まります
   * - OpenAI（ ``openai`` ）
     - ``gpt-5-mini``
     - ``https://api.openai.com/v1``
     - ``Authorization: Bearer`` （ ``rag.llm.openai.api.key`` ）
     - クラウド — 質問と取得されたドキュメントがOpenAIに送信されます
   * - Google Gemini（ ``gemini`` ）
     - ``gemini-3.1-flash-lite-preview``
     - ``https://generativelanguage.googleapis.com/v1beta``
     - ``x-goog-api-key`` （ ``rag.llm.gemini.api.key`` ）
     - クラウド — 質問と取得されたドキュメントがGoogleに送信されます

.. note::

   ``rag.llm.name`` の既定値は ``ollama`` です。この値は、読み込むDIコンポーネント名（ ``{rag.llm.name}LlmClient`` ）の決定に使用されます。
   そのため、 ``rag.llm.name`` を既定値のままにして ``fess-llm-ollama`` 以外のプラグインだけを導入した場合、LLMクライアントは1つも有効になりません。
   このとき、ログに ``[LLM] LlmClient not found. componentName=ollamaLlmClient`` という警告が出力され、AI検索モードは利用できません。
   導入したプラグインに合わせて、必ず ``rag.llm.name`` を設定してください。 ``none`` を指定すると、LLM連携を明示的に無効化できます。

プラグイン導入
==============

LLM機能はプラグインとして提供されます。利用するプロバイダーに対応する ``fess-llm-{provider}`` プラグインを導入してください。

管理画面の「システム > プラグイン」ページからインストールできます。 ``fess-llm-*`` プラグインはインストール可能なプラグインの一覧に表示されます。

手動で導入する場合は、対応するJARファイル（例: OpenAIプロバイダーの場合は ``fess-llm-openai-15.9.0.jar`` ）を以下のディレクトリに配置します。

::

    app/WEB-INF/plugin/

いずれの方法の場合も、導入後に |Fess| を再起動するとプラグインが読み込まれます。

アーキテクチャ
==============

AI検索モード機能は以下のフローで動作します。

1. **ユーザー入力**: ユーザーがチャットインターフェースで質問を入力
2. **意図解析（intent）**: LLMがユーザーの質問を分析し、検索キーワードを抽出
3. **検索実行（search）**: |Fess| の検索エンジンで関連ドキュメントを検索
4. **結果評価（evaluate）**: LLMが検索結果の関連性を評価し、最適なドキュメントを選択
5. **クエリ再生成（必要に応じて）**: 検索結果が得られない場合、または評価で関連するドキュメントが見つからない場合、LLMがクエリを再生成して再検索
6. **コンテンツ取得（fetch）**: 選択されたドキュメントの本文を取得
7. **回答生成（answer）**: 取得したドキュメントを基にLLMが回答を生成（Markdownレンダリング対応）
8. **ソース引用**: 回答には参照元ドキュメントへのリンクが含まれる

.. note::

   内部処理は ``intent`` 、 ``search`` 、 ``evaluate`` 、 ``fetch`` 、 ``answer`` の5つのフェーズで構成され、各フェーズの進行状況はストリーミング（SSE）でクライアントに通知されます。
   クエリ再生成は独立したフェーズではなく、 ``search`` フェーズのフォールバックとして通知され、その後 ``search`` が再実行されます。

.. note::

   上記の流れは、ストリーミングAPIで意図が「検索」と判定された場合のものです。意図の判定結果によって経路は変わります。
   質問が不明確と判定された場合は検索を行わずに応答を生成し、URLの要約を求められた場合はURL検索を行い評価フェーズを実行しません。
   また、非ストリーミングの ``POST /api/v2/chat`` は評価フェーズを実行せず、フェーズ単位の進捗通知も行いません。

基本設定
========

LLM機能の設定は、以下の2つの場所で行います。

管理画面の全般設定 / system.properties
--------------------------------------

管理画面の全般設定、または ``system.properties`` で設定します。LLMプロバイダーの選択に使用します。

::

    # LLMプロバイダーを指定（ollama, openai, gemini）
    rag.llm.name=ollama

fess_config.properties
----------------------

``app/WEB-INF/classes/fess_config.properties`` （パッケージ版では ``/etc/fess/fess_config.properties`` ）で設定します。
AI検索モードの有効化、セッション・履歴関連の設定に加え、プロバイダー固有の設定（接続先URLやAPIキー、生成パラメーターなど）もこのファイルに記述します。

::

    # AI検索モード機能を有効にする（デフォルトは false）
    rag.chat.enabled=true

    # プロバイダー固有設定の例（OpenAIの場合）
    rag.llm.openai.api.key=sk-...
    rag.llm.openai.answer.temperature=0.7

各プロバイダーの詳細な設定については、以下のドキュメントを参照してください。

- :doc:`llm-ollama` - Ollamaの設定
- :doc:`llm-openai` - OpenAIの設定
- :doc:`llm-gemini` - Google Geminiの設定

共通設定
========

すべてのLLMプロバイダーで共通して使用される設定項目です。これらは ``fess_config.properties`` で設定します。

コンテキスト設定
----------------

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.context.max.documents``
     - コンテキストに含める最大ドキュメント数
     - ``5``
   * - ``rag.chat.content.fields``
     - ドキュメントから取得するフィールド
     - ``title,url,content,doc_id,content_title,content_description``

.. note::

   コンテキストの最大文字数（ ``context.max.chars`` ）はプロバイダーおよびプロンプトタイプごとの設定に変更されました。 ``fess_config.properties`` で ``rag.llm.{provider}.{promptType}.context.max.chars`` として設定してください。

システムプロンプト
------------------

システムプロンプトはプロパティファイルではなく、各プラグインのDI XMLファイルで管理されます。

各 ``fess-llm-*`` プラグインのJARファイル内に含まれる ``fess_llm++.xml`` ファイルでシステムプロンプトが定義されています。
プロンプトをカスタマイズするためにJARファイルを展開して編集し直す必要はありません。LastaDiのコンポーネント再定義の仕組みにより、
``app/WEB-INF/classes/`` に ``fess_llm+{コンポーネント名}.xml`` という名前のファイルを配置すると、プラグイン側のコンポーネント定義を置き換えられます。

コンポーネント名はプロバイダーごとに次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロバイダー
     - コンポーネント名
   * - Ollama
     - ``ollamaLlmClient``
   * - OpenAI
     - ``openaiLlmClient``
   * - Google Gemini
     - ``geminiLlmClient``

例として、OpenAIプロバイダーの回答生成プロンプトを変更する場合は、 ``app/WEB-INF/classes/fess_llm+openaiLlmClient.xml`` を作成します。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="openaiLlmClient" class="org.codelibs.fess.llm.openai.OpenAiLlmClient">
            <postConstruct name="register"/>
            <postConstruct name="init"/>
            <preDestroy name="destroy"/>
            <property name="answerGenerationSystemPrompt">"独自の回答生成プロンプト"</property>
            <!-- 変更しないプロンプトプロパティもすべて記述する -->
        </component>
    </components>

.. warning::

   再定義ファイルはコンポーネント定義を置き換えます。そのため、元の ``fess_llm++.xml`` に記述されている内容（クラス名、 ``postConstruct`` 、
   ``preDestroy`` 、および変更しないプロンプトプロパティ）をすべて含めてください。記述しなかったプロパティは未設定に戻ります。

.. warning::

   ``fess_llm++.xml`` そのものをコピーして ``app/WEB-INF/classes/`` に配置しないでください。
   ファイル名が ``++`` で終わるDI XMLはクラスパス上のすべてが「追加」として読み込まれるため、同じ名前のコンポーネントが二重に登録され、
   ``TooManyRegistrationComponentException`` が発生して |Fess| が起動しなくなります。

可用性チェック
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.{provider}.availability.check.interval``
     - LLMの可用性を定期的にチェックする間隔（秒）
     - ``60``

この設定は ``fess_config.properties`` で行います。 |Fess| は定期的にLLMプロバイダーの接続状態を確認します。

.. note::

   このプロパティに ``0`` 以下の値や数値以外の値を指定した場合、その値は無視されデフォルト値（ ``60`` ）が使用されます。
   このプロパティで可用性チェックを無効化することはできません。
   なお可用性チェックは、 ``rag.chat.enabled`` が ``false`` の場合、および ``rag.llm.name`` で選択されていないプロバイダーでは実行されません。

セッション管理
==============

チャットセッションに関する設定です。これらは ``fess_config.properties`` で設定します。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.chat.session.timeout.minutes``
     - セッションのタイムアウト時間（分）
     - ``30``
   * - ``rag.chat.session.max.size``
     - セッションの最大数
     - ``10000``
   * - ``rag.chat.history.max.messages``
     - 会話履歴に保持する最大メッセージ数
     - ``30``

同時実行制御
============

LLMへのリクエストの同時実行数を制御する設定です。 ``fess_config.properties`` で設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.{provider}.max.concurrent.requests``
     - プロバイダーへの最大同時リクエスト数
     - ``5``
   * - ``rag.llm.{provider}.concurrency.wait.timeout``
     - 同時実行数の上限に達した際、空きを待機する最大時間（ミリ秒）。この時間内に空きが得られない場合はレート制限エラーになります
     - ``30000``

例えば、OpenAIプロバイダーの同時実行数を設定する場合は以下のようになります。

::

    rag.llm.openai.max.concurrent.requests=10

評価設定
========

検索結果の評価に関する設定です。 ``fess_config.properties`` で設定します。

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - プロパティ
     - 説明
     - デフォルト
   * - ``rag.llm.{provider}.chat.evaluation.max.relevant.docs``
     - 評価フェーズで選択する関連ドキュメントの最大数
     - ``3``

プロンプトタイプ別設定
======================

生成パラメーターをプロンプトタイプごとに設定できます。これにより、用途に応じた細かな調整が可能です。設定は ``fess_config.properties`` で行います。

プロンプトタイプ一覧
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - プロンプトタイプ
     - 設定値
     - 説明
   * - 意図解析
     - ``intent``
     - ユーザーの質問を分析し、検索キーワードを抽出する
   * - 評価
     - ``evaluation``
     - 検索結果の関連性を評価する
   * - 不明確な質問
     - ``unclear``
     - 質問が不明確な場合の応答を生成する
   * - 検索結果なし
     - ``noresults``
     - 検索結果が見つからない場合の応答を生成する
   * - ドキュメント不在
     - ``docnotfound``
     - 該当するドキュメントが存在しない場合の応答を生成する
   * - 回答生成
     - ``answer``
     - 検索結果を基に回答を生成する
   * - 要約
     - ``summary``
     - ドキュメントの要約を生成する
   * - FAQ
     - ``faq``
     - FAQ形式の回答を生成する
   * - 直接回答
     - ``direct``
     - 検索を介さずに直接回答を生成する（現在のバージョンでは呼び出されません）
   * - クエリ再生成
     - ``queryregeneration``
     - 検索結果が得られない場合にクエリを再生成する

設定パターン
------------

プロンプトタイプごとの設定は以下のパターンで指定します。

::

    rag.llm.{provider}.{promptType}.temperature
    rag.llm.{provider}.{promptType}.max.tokens
    rag.llm.{provider}.{promptType}.context.max.chars

設定例（OpenAIプロバイダーの場合）:

::

    # 回答生成の温度を低めに設定
    rag.llm.openai.answer.temperature=0.5
    # 回答生成の最大トークン数
    rag.llm.openai.answer.max.tokens=4096
    # 意図解析は短い応答で十分なため低く設定
    rag.llm.openai.intent.max.tokens=256
    # 要約のコンテキスト最大文字数
    rag.llm.openai.summary.context.max.chars=8000

.. note::

   ``temperature`` 、 ``max.tokens`` 、 ``context.max.chars`` はすべてのプロバイダーで共通して使用できます。ただし、これらのデフォルト値はプロバイダーおよびプロンプトタイプごとに異なります。

これに加えて、各プロバイダーは固有のパラメーターをサポートしています。対応状況は以下のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - パラメーター
     - Ollama
     - OpenAI
     - Gemini
   * - ``thinking.budget``
     - 対応
     - 非対応
     - 対応
   * - ``thinking.level``
     - 対応
     - 非対応
     - 非対応
   * - ``top.p``
     - 対応
     - 対応
     - 非対応
   * - ``top.k`` 、 ``num.ctx``
     - 対応
     - 非対応
     - 非対応
   * - ``reasoning.effort``
     - 非対応
     - 対応
     - 非対応
   * - ``frequency.penalty`` 、 ``presence.penalty``
     - 非対応
     - 対応
     - 非対応

.. note::

   「非対応」のパラメーターを指定してもエラーにはならず、単に無視されます。各パラメーターの意味や設定可能な値の詳細は、各プロバイダーのドキュメントを参照してください。

.. note::

   Ollamaプロバイダーのみ、プロンプトタイプ別の設定が存在しない場合に ``rag.llm.ollama.default.{パラメーター}`` を参照するフォールバックがあります
   （ ``context.max.chars`` を除く）。OpenAIプロバイダーとGeminiプロバイダーにはこのフォールバックはなく、
   プロンプトタイプ別の設定がない場合はプラグイン組み込みのデフォルト値が使用されます。

次のステップ
============

- :doc:`llm-ollama` - Ollamaの詳細設定
- :doc:`llm-openai` - OpenAIの詳細設定
- :doc:`llm-gemini` - Google Geminiの詳細設定
- :doc:`rag-chat` - AI検索モード機能の詳細設定
- :doc:`rank-fusion` - Rank Fusion設定（ハイブリッド検索の結果統合）
- :doc:`../user/chat-search` - AI検索モードの使い方
- :doc:`../api/api-chat` - チャットAPIリファレンス
