==================================
Slackコネクタ
==================================

概要
====

Slackコネクタは、Slackワークスペースのチャンネルメッセージを取得して
|Fess| のインデックスに登録する機能を提供します。

この機能には ``fess-ds-slack`` プラグインが必要です。

対応コンテンツ
==============

- パブリックチャンネルのメッセージ
- プライベートチャンネルのメッセージ
- スレッドの返信メッセージ（``conversations.replies`` で取得します）
- ファイル添付（オプション）

以下は対象外です:

- システムイベントメッセージ（``channel_join``、``channel_topic``、``pinned_item`` など）は
  既定で索引対象から除外されます（``ignore_system_events``）
- ダイレクトメッセージ（DM）およびグループDM
- Huddleの文字起こしとClips（Slackに公式APIが存在しないため対応できません）

前提条件
========

1. プラグインのインストールが必要です
2. Slack Appの作成と権限設定が必要です
3. OAuth Access Tokenの取得が必要です

プラグインのインストール
------------------------

管理画面の「システム」→「プラグイン」からインストールします:

1. Maven Centralから ``fess-ds-slack-X.X.X.jar`` をダウンロード
2. プラグイン管理画面からアップロードしてインストール
3. |Fess| を再起動

または、詳細は :doc:`../../admin/plugin-guide` を参照してください。

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
     - Company Slack
   * - ハンドラ名
     - SlackDataStore
   * - 有効
     - オン

パラメーター設定
----------------

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=false
    include_private=false

パラメーター一覧
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - パラメーター
     - 必須
     - 説明
   * - ``token``
     - はい
     - SlackアプリのOAuth Access Token
   * - ``channels``
     - いいえ
     - クロール対象チャンネル（カンマ区切り、または ``*all``）。未指定の場合はすべてのチャンネルを取得（ ``*all`` と同じ動作）
   * - ``file_crawl``
     - いいえ
     - ファイルもクロールする（デフォルト: ``false``）
   * - ``include_private``
     - いいえ
     - プライベートチャンネルも含める（デフォルト: ``false``）
   * - ``number_of_threads``
     - いいえ
     - 並列処理スレッド数（デフォルト: ``1``）
   * - ``max_filesize``
     - いいえ
     - クロールするファイルの最大サイズ（バイト単位、デフォルト: ``10000000``）
   * - ``ignore_error``
     - いいえ
     - エラー発生時に処理を継続する（デフォルト: ``true``）
   * - ``supported_mimetypes``
     - いいえ
     - クロール対象のMIMEタイプ（正規表現、デフォルト: ``.*``）
   * - ``include_pattern``
     - いいえ
     - クロール対象URLの正規表現パターン
   * - ``exclude_pattern``
     - いいえ
     - クロール除外URLの正規表現パターン
   * - ``proxy_host``
     - いいえ
     - HTTPプロキシホスト
   * - ``proxy_port``
     - いいえ
     - HTTPプロキシポート（ ``proxy_host`` 指定時は必須）
   * - ``file_types``
     - いいえ
     - クロール対象のファイルタイプ（Slack APIのファイルタイプフィルター、デフォルト: ``all``）
   * - ``channel_count``
     - いいえ
     - チャンネル一覧のページあたり取得件数（デフォルト: ``100``）
   * - ``message_count``
     - いいえ
     - メッセージのページあたり取得件数（デフォルト: ``100``）
   * - ``file_count``
     - いいえ
     - ファイルのページあたり取得件数（デフォルト: ``20``）
   * - ``user_count``
     - いいえ
     - ユーザー一覧のページあたり取得件数（デフォルト: ``100``）
   * - ``user_cache_size``
     - いいえ
     - ユーザー情報キャッシュの最大エントリ数（デフォルト: ``10000``）
   * - ``bot_cache_size``
     - いいえ
     - ボット情報キャッシュの最大エントリ数（デフォルト: ``10000``）
   * - ``channel_cache_size``
     - いいえ
     - チャンネル情報キャッシュの最大エントリ数（デフォルト: ``10000``）

高度なパラメーター
~~~~~~~~~~~~~~~~~~

以下のパラメーターは接続・リトライの挙動やクロール対象の細かい制御、権限同期を扱います:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 説明
   * - ``connection_timeout``
     - 各Slack APIリクエストの接続タイムアウト（ミリ秒、デフォルト: ``20000``）
   * - ``read_timeout``
     - 各Slack APIリクエストの読み取りタイムアウト（ミリ秒、デフォルト: ``20000``）
   * - ``max_retry_count``
     - ``429``\ （レート制限）または ``5xx`` 応答を受けたときの最大リトライ回数（デフォルト: ``3``）
   * - ``retry_interval``
     - 応答に ``Retry-After`` ヘッダーが無い場合の、最初のリトライまでの待機時間（ミリ秒、デフォルト: ``3000``）。リトライごとに倍増し、``60000`` ミリ秒で頭打ちになります。``Retry-After`` ヘッダーがある場合はその値（秒）が優先されます
   * - ``executor_timeout``
     - クロール終了時に、キューに残っている処理の完了を待つ秒数（デフォルト: ``60``）。この秒数を過ぎると強制終了します
   * - ``exclude_archived``
     - ``conversations.list`` の取得結果からアーカイブ済みチャンネルを除外するか（デフォルト: ``false``）。 ``true`` にすると、``channels`` にチャンネル名で指定したアーカイブ済みチャンネルが名前解決できなくなります（詳細はトラブルシューティングを参照）
   * - ``ignore_system_events``
     - Slackが自動生成するチャンネル管理系のメッセージ（``channel_join``、``channel_topic``、``pinned_item`` など）を索引対象から除外するか（デフォルト: ``true``）
   * - ``read_interval``
     - メッセージまたはファイルを1件処理するごとに待機する時間（ミリ秒、デフォルト: ``0`` ＝待機なし）。レート制限が厳しいワークスペースに対してクロール速度を落とす場合に使用します
   * - ``max_content_length``
     - コンテンツ抽出（Tika）が1ファイルから抽出できる最大文字数（デフォルト: 未設定＝MIMEタイプ別の既定上限に委ねる）。 ``max_filesize`` はダウンロード前にファイルサイズで弾く転送量の上限、``max_content_length`` はダウンロード後に抽出するテキスト量の上限で、それぞれ独立して働きます。 ``max_filesize`` を小さくしても、``max_content_length`` の代わりにはなりません（例: 1MBの圧縮ファイルでも、展開後は遥かに大きなテキストになり得ます）
   * - ``permission_sync``
     - プライベートチャンネルのメンバーシップを検索用の権限（ロール）に変換するかどうか（デフォルト: ``false``）。詳細は後述の「権限同期（ACL）」を参照してください
   * - ``default_permissions``
     - チャンネルメンバーシップに関わらず、索引されたすべての文書に付与する追加の権限（``{user}``/``{group}``/``{role}`` 形式、カンマ区切り、デフォルト: 空）。``permission_sync`` が有効な場合にのみ適用されます

.. note::

   ``ignore_system_events`` の既定値は ``true`` です。このパラメーターを指定していない既存の
   クロール設定でも、|Fess| をアップグレードすると ``channel_join`` などのシステムイベント
   メッセージが索引されなくなり、エラーや警告なしに索引される文書数が減ります。従来どおり
   システムイベントも索引したい場合は、``ignore_system_events=false`` を明示的に指定してください。

スクリプト設定
--------------

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

利用可能なフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``message.title``
     - タイトル（メッセージの場合は空文字列、ファイルの場合はファイル名とタイトル）
   * - ``message.text``
     - メッセージのテキストコンテンツ（ファイルの場合はファイル名と抽出されたファイル本文）
   * - ``message.user``
     - メッセージ送信者の表示名（表示名が未設定の場合は実名、ユーザー名、ユーザーIDの順に解決）
   * - ``message.channel``
     - メッセージが送信されたチャンネル名
   * - ``message.timestamp``
     - メッセージ送信日時
   * - ``message.permalink``
     - メッセージのパーマリンク
   * - ``message.attachments``
     - 添付ファイルのフォールバック情報
   * - ``message.roles``
     - このメッセージまたはファイルを閲覧できる検索権限（ロール）の一覧。``permission_sync=true`` の場合のみ存在するフィールドです。スクリプトで ``role=message.roles`` と指定しない限り、計算した権限は索引される文書に反映されません

Slack App設定
=============

1. Slack Appの作成
------------------

https://api.slack.com/apps にアクセス:

1. 「Create New App」をクリック
2. 「From scratch」を選択
3. アプリ名を入力（例: Fess Crawler）
4. ワークスペースを選択
5. 「Create App」をクリック

2. OAuth & Permissionsの設定
----------------------------

「OAuth & Permissions」メニューで:

**Bot Token Scopes**\ に以下を追加:

基本スコープ（常に必要）:

- ``channels:history`` - パブリックチャンネルメッセージの読み取り
- ``channels:read`` - パブリックチャンネル情報の読み取り
- ``users:read`` - ユーザー情報の読み取り（表示名の解決に必要）
- ``team:read`` - ワークスペース情報の読み取り。``team.info`` を毎回呼び出すため必須です。
  このスコープが無いと、メッセージ1件ごとに ``chat.getPermalink`` を追加で呼び出すように
  なり、API呼び出し数が大幅に増加します

プライベートチャンネルも含める場合（``include_private=true``）に追加:

- ``groups:history`` - プライベートチャンネルメッセージの読み取り
- ``groups:read`` - プライベートチャンネル情報の読み取り

ファイルもクロールする場合（``file_crawl=true``）に追加:

- ``files:read`` - ファイルコンテンツの読み取り

プライベートチャンネルの権限を同期する場合（``permission_sync=true``）に追加:

- ``users:read.email`` - メンバーのメールアドレスの読み取り（権限同期に必須）

3. アプリのインストール
-----------------------

「Install App」メニューで:

1. 「Install to Workspace」をクリック
2. 権限を確認して「許可する」をクリック
3. 「Bot User OAuth Token」をコピー（``xoxb-`` で始まる）

.. note::
   通常は ``xoxb-`` で始まるBot User OAuth Tokenを使用しますが、
   パラメーターでは ``xoxp-`` で始まるUser OAuth Tokenも使用可能です。

4. チャンネルへの追加
---------------------

クロール対象のチャンネルにAppを追加:

1. Slackでチャンネルを開く
2. チャンネル名をクリック
3. 「インテグレーション」タブを選択
4. 「アプリを追加する」をクリック
5. 作成したアプリを追加

権限同期（ACL）
===============

Slackコネクタは、プライベートチャンネルのメンバーシップを |Fess| の検索権限（ロール）に変換し、
そのチャンネルのメンバーだけが内容を検索できるようにする機能を提供します。既定では無効です。

.. note::

   ``permission_sync`` は権限（ロール）を計算するだけで、自動的には適用されません。スクリプトに
   ``role=message.roles`` を指定して初めて、計算した権限が索引される文書に反映されます。この
   指定を忘れると、``permission_sync=true`` によるAPI呼び出しの増加やプライベートチャンネルの
   スキップだけが発生し、アクセス制御は一切行われません。

有効化する
----------

1. Slack Appに ``users:read.email`` スコープを追加します（メンバーのメールアドレス解決に必須）
2. パラメーターに ``permission_sync=true`` を設定します
3. スクリプトに ``role=message.roles`` を追加します

パラメーター:

::

    include_private=true
    permission_sync=true

スクリプト:

::

    role=message.roles

フェイルクローズ動作
--------------------

次のいずれかに該当するプライベートチャンネルは、そのクロールでは索引されません（内容が誤って
公開されるのではなく、索引しない方向に倒す「フェイルクローズ」の動作です）:

- チャンネルのメンバー一覧の取得に失敗した
- メンバー一覧が0件だった（クロールに使うトークンのボットユーザー自身がそのプライベート
  チャンネルに参加していない場合に発生します）
- メンバーはいるが、誰のメールアドレスも解決できなかった（``users:read.email`` スコープの
  不足が主な原因です）

パブリックチャンネルは ``conversations.members`` を呼び出さず、常に全員が閲覧できるものとして
扱われます。

プリンシパル名の一致
--------------------

検索時の権限判定は |Fess| のログイン名（プリンシパル名）で行われます。この機能が計算する権限は
Slackのメールアドレスから作られるため、|Fess| のログイン名とSlackのメールアドレスを一致させる
必要があります。Slackはメールアドレスを小文字に正規化するため、|Fess| 側のログイン名も小文字に
しておいてください。一致しない場合、他人の文書が見えてしまうのではなく、該当ユーザーの検索結果
が常に0件になります（原因が分かりにくいため注意してください）。

その他の注意点
--------------

- Slackのユーザーグループ（User Group）は使用しません。権限は個々のメンバーのメールアドレス
  から直接計算します
- ``default_permissions`` で、チャンネルメンバーシップに関わらずすべての文書に付与する追加の
  権限を指定できます（``permission_sync=true`` の場合のみ適用）
- ``permission_sync=false`` のまま ``include_private=true`` にすると、プライベートチャンネル
  の内容はデータストア設定の「権限」欄の設定だけで索引されます。この欄が空の場合、実質的に
  全員に公開されます
- 既に索引済みのワークスペースで ``permission_sync`` を後から有効にしても、過去に索引された
  文書に遡って権限は付与されません。適用するには、``permission_sync=true`` と
  ``role=message.roles`` を設定した上で再クロールしてください

使用例
======

特定のチャンネルをクロール
--------------------------

パラメーター:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random,tech-discussion
    file_crawl=false
    include_private=false

スクリプト:

::

    title=message.user + " #" + message.channel
    digest=message.text + "\n" + message.attachments
    content=message.text
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

すべてのチャンネルをクロール
----------------------------

パラメーター:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=false

スクリプト:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

プライベートチャンネルを含めてクロール
--------------------------------------

パラメーター:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    file_crawl=false
    include_private=true

スクリプト:

::

    title=message.user + " #" + message.channel
    digest=message.text
    content=message.text + "\n添付: " + message.attachments
    created=message.timestamp
    url=message.permalink

ファイルも含めてクロール
------------------------

パラメーター:

::

    token=xoxb-your-slack-bot-token-here
    channels=general,random
    file_crawl=true
    include_private=false

スクリプト:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink

詳細なメッセージ情報を含める
----------------------------

スクリプト:

::

    title="[" + message.channel + "] " + message.user
    content=message.text
    digest=message.text.substring(0, Math.min(200, message.text.length()))
    created=message.timestamp
    timestamp=message.timestamp
    url=message.permalink

権限を同期してクロール
----------------------

プライベートチャンネルの内容を、そのチャンネルのメンバーだけが検索できるようにします。
事前に ``users:read.email`` スコープをSlack Appに追加してください。

パラメーター:

::

    token=xoxb-your-slack-bot-token-here
    channels=*all
    include_private=true
    permission_sync=true

スクリプト:

::

    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    url=message.permalink
    role=message.roles

.. note::
   ``role=message.roles`` を書き忘れると、計算した権限は索引される文書に反映されません。
   詳細は「権限同期（ACL）」を参照してください。

トラブルシューティング
======================

エラー処理の仕組み
------------------

Slackコネクタは、Slack APIのエラーを次の3種類に分けて扱います:

- **致命的エラー**\ （``invalid_auth``、``token_revoked``、``account_inactive``、
  ``missing_scope``、``not_authed``、``token_expired``）: トークン自体が使えない状態のため、
  クロールジョブ全体を失敗させます
- **一時的エラー**\ （``ratelimited``、``internal_error``、``fatal_error``、
  ``service_unavailable``、``request_timeout``）: リトライしても解消しない場合、クロール
  ジョブ全体を失敗させます（リトライの挙動は後述の「APIレート制限」を参照）
- **チャンネル単位のエラー**\ （``channel_not_found``、``not_in_channel`` など）: そのチャンネル
  だけを警告付きでスキップし、他のチャンネルのクロールは継続します

以前のバージョンでは、致命的エラーが発生してもクロールが「成功」と扱われ、結果的に0件や
一部だけが索引される「サイレントな部分成功」が起きていました。現在はこの3分類に従い、
致命的・一時的なエラーは必ずジョブの失敗として報告されます。

認証エラー
----------

**症状**: ``invalid_auth`` または ``not_authed``

**確認事項**:

1. トークンが正しくコピーされているか確認
2. トークンの形式を確認:

   - Bot User OAuth Token: ``xoxb-`` で始まる
   - User OAuth Token: ``xoxp-`` で始まる

3. アプリがワークスペースにインストールされているか確認
4. 必要な権限が付与されているか確認

チャンネルが見つからない
------------------------

**症状**: ``channel_not_found``

**確認事項**:

1. チャンネル名が正しいか確認（# は不要）
2. アプリがチャンネルに追加されているか確認
3. プライベートチャンネルの場合、``include_private=true`` を設定
4. ``exclude_archived=true`` を設定していないか確認してください。既定（``exclude_archived=false``）
   ではアーカイブ済みチャンネルも一覧に含まれ、クロールされます。``true`` にした場合のみ、
   ``channels`` にチャンネル名で指定したアーカイブ済みチャンネルが名前解決できなくなります

メッセージが取得できない
------------------------

**症状**: クロールは成功したが、索引される文書が少ない、または0件

**確認事項**:

1. ``ignore_system_events`` の既定値は ``true`` です。チャンネル内のメッセージが
   ``channel_join`` などのシステムイベントだけの場合、索引される文書は0件になります
   （「高度なパラメーター」を参照）
2. チャンネルに実際にメッセージが投稿されているか確認
3. アプリがチャンネルに追加されているか確認
4. ``permission_sync=true`` の場合、プライベートチャンネルのメンバー取得に失敗すると、
   そのチャンネルはこのクロールでは索引されません（フェイルクローズ。「権限同期（ACL）」を参照）

.. note::

   以前のバージョンでは、スコープ不足（``missing_scope``）が発生してもクロールが成功したまま
   メッセージ0件になっていました。現在は ``missing_scope`` を含む致命的エラーが発生すると、
   クロールジョブ自体が失敗します。ジョブが失敗している場合は、この節ではなく次の
   「権限不足エラー」を確認してください。

権限不足エラー
--------------

**症状**: ``missing_scope``\ （クロールジョブ全体が失敗します）

**解決方法**:

1. Slack App設定で必要なスコープを追加:

   **基本**\ （常に必要）:

   - ``channels:history``
   - ``channels:read``
   - ``users:read``
   - ``team:read``

   **プライベートチャンネル**:

   - ``groups:history``
   - ``groups:read``

   **ファイル**:

   - ``files:read``

   **権限同期**\ （``permission_sync=true``）:

   - ``users:read.email``

2. アプリを再インストール
3. |Fess| を再起動

ファイルがクロールできない
--------------------------

**症状**: ``file_crawl=true`` でもファイルが取得されない

**確認事項**:

1. ``files:read`` スコープが付与されているか確認
2. チャンネルに実際にファイルが投稿されているか確認
3. ファイルのアクセス権限を確認
4. ``max_filesize`` を超えるファイルはダウンロードされません（ログの警告を確認）

APIレート制限
-------------

**症状**: ``ratelimited``\ （クロールジョブ全体が失敗します）

**解決方法**:

1. ``max_retry_count``、``retry_interval`` の既定値で解決しない場合は値を増やす
2. ``read_interval`` を設定してクロール速度を落とす
3. チャンネル数を減らす、またはデータストアを複数に分割してスケジュールを分散する

Slack APIの ``ratelimited`` エラーは、``Retry-After`` ヘッダーがあればその秒数、無ければ
``retry_interval`` を起点に倍増するバックオフ（``max_retry_count`` 回まで、最大60秒）で
自動的にリトライされます。リトライを使い切ってもレート制限が解消しない場合、クロール
ジョブ全体が失敗します。

Slack APIのTier（呼び出し可能回数の上限）:

- Tier 1: 1+ リクエスト/分
- Tier 2: 20+ リクエスト/分 — ``conversations.list``、``users.list``\ （クロール開始時に
  無条件で全件取得するため、最も枯渇しやすい）
- Tier 3: 50+ リクエスト/分 — ``conversations.history``、``conversations.replies``、
  ``files.list``
- Tier 4: 100+ リクエスト/分 — ``conversations.members``\ （``permission_sync=true`` のとき
  のみ）、``files.info``

.. note::

   2025年5月29日のSlackのレート制限強化（``conversations.history``、``conversations.replies``
   の2メソッドを50+リクエスト/分に制限）は、Slack Marketplaceなど社外に配布されたアプリのみが
   対象です。|Fess| 用に作成する、配布しない社内アプリ（作成したワークスペースにのみインストール
   するアプリ）には適用されません。

大量のメッセージがある場合
--------------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

1. チャンネルを分割して複数のデータストアを設定
2. クロールスケジュールを分散

スクリプトの応用例
==================

メッセージの加工
----------------

長いメッセージのダイジェスト:

::

    title=message.user + " #" + message.channel
    content=message.text
    digest=message.text.length() > 100 ? message.text.substring(0, 100) + "..." : message.text
    created=message.timestamp
    url=message.permalink

チャンネル名の整形:

::

    title="[Slack: " + message.channel + "] " + message.user
    content=message.text
    created=message.timestamp
    url=message.permalink

参考情報
========

- :doc:`ds-overview` - データストアコネクタ概要
- :doc:`ds-atlassian` - Atlassianコネクタ
- :doc:`../../admin/dataconfig-guide` - データストア設定ガイド
- :doc:`../security-role` - 検索権限（ACL）の設定ガイド
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
- `Slack API Rate Limits <https://docs.slack.dev/apis/web-api/rate-limits>`_
