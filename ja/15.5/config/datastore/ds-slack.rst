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
- ファイル添付（オプション）

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

    token=xoxp-123456789012-123456789012-123456789012-abc123def456ghi789jkl012mno345pq
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
     - はい
     - クロール対象チャンネル（カンマ区切り、または ``*all``）
   * - ``file_crawl``
     - いいえ
     - ファイルもクロールする（デフォルト: ``false``）
   * - ``include_private``
     - いいえ
     - プライベートチャンネルも含める（デフォルト: ``false``）

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
   * - ``message.text``
     - メッセージのテキストコンテンツ
   * - ``message.user``
     - メッセージ送信者のディスプレイネーム
   * - ``message.channel``
     - メッセージが送信されたチャンネル名
   * - ``message.timestamp``
     - メッセージ送信日時
   * - ``message.permalink``
     - メッセージのパーマリンク
   * - ``message.attachments``
     - 添付ファイルのフォールバック情報

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

**Bot Token Scopes**に以下を追加:

パブリックチャンネルのみの場合:

- ``channels:history`` - パブリックチャンネルメッセージの読み取り
- ``channels:read`` - パブリックチャンネル情報の読み取り

プライベートチャンネルも含める場合（``include_private=true``）:

- ``channels:history``
- ``channels:read``
- ``groups:history`` - プライベートチャンネルメッセージの読み取り
- ``groups:read`` - プライベートチャンネル情報の読み取り

ファイルもクロールする場合（``file_crawl=true``）:

- ``files:read`` - ファイルコンテンツの読み取り

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

トラブルシューティング
======================

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
4. チャンネルが存在し、アーカイブされていないか確認

メッセージが取得できない
------------------------

**症状**: クロールは成功するがメッセージが0件

**確認事項**:

1. 必要なスコープが付与されているか確認:

   - ``channels:history``
   - ``channels:read``
   - プライベートチャンネルの場合: ``groups:history``、``groups:read``

2. チャンネルにメッセージが存在するか確認
3. アプリがチャンネルに追加されているか確認
4. Slackアプリが有効になっているか確認

権限不足エラー
--------------

**症状**: ``missing_scope``

**解決方法**:

1. Slack App設定で必要なスコープを追加:

   **パブリックチャンネル**:

   - ``channels:history``
   - ``channels:read``

   **プライベートチャンネル**:

   - ``groups:history``
   - ``groups:read``

   **ファイル**:

   - ``files:read``

2. アプリを再インストール
3. |Fess| を再起動

ファイルがクロールできない
--------------------------

**症状**: ``file_crawl=true`` でもファイルが取得されない

**確認事項**:

1. ``files:read`` スコープが付与されているか確認
2. チャンネルに実際にファイルが投稿されているか確認
3. ファイルのアクセス権限を確認

APIレート制限
-------------

**症状**: ``rate_limited``

**解決方法**:

1. クロール間隔を長くする
2. チャンネル数を減らす
3. データストアを複数に分割してスケジュール分散

Slack APIの制限:

- Tier 3メソッド: 50+ リクエスト/分
- Tier 4メソッド: 100+ リクエスト/分

大量のメッセージがある場合
--------------------------

**症状**: クロールに時間がかかる、またはタイムアウトする

**解決方法**:

1. チャンネルを分割して複数のデータストアを設定
2. クロールスケジュールを分散
3. 古いメッセージを除外する設定を検討

スクリプトの高度な使用例
========================

メッセージのフィルタリング
--------------------------

特定のユーザーのメッセージのみインデックス:

::

    if (message.user == "田中太郎") {
        title=message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

キーワードを含むメッセージのみ:

::

    if (message.text.contains("重要") || message.text.contains("障害")) {
        title="[重要] " + message.user + " #" + message.channel
        content=message.text
        created=message.timestamp
        url=message.permalink
    }

メッセージの加工
----------------

長いメッセージの要約:

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
- `Slack API Documentation <https://api.slack.com/>`_
- `Slack Bot Token Scopes <https://api.slack.com/scopes>`_
