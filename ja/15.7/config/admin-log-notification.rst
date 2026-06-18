================
ログ通知
================

概要
====

|Fess| には、ERROR や WARN レベルのログイベントを自動的に捕捉し、管理者へ通知する機能があります。
この機能により、システムの異常を迅速に検知し、障害対応を早期に開始できます。

主な特徴:

- **対応する通知チャネル**: メール、Slack、Google Chat
- **対象プロセス**: メインアプリケーション、クローラー、サジェスト生成、サムネイル生成
- **デフォルト無効**: オプトイン方式のため、明示的に有効化する必要があります

仕組み
======

ログ通知は以下の流れで動作します。

1. Log4j2 の ``LogNotificationAppender`` が、設定されたレベル以上のログイベントを捕捉します。
2. 捕捉されたイベントはメモリ上のバッファ（デフォルト最大 1,000 件）に蓄積されます。バッファが上限を超えた場合は、最も古いイベントから順に破棄されます。
3. タイマーが 30 秒間隔でバッファ内のイベントを OpenSearch のインデックス（``fess_log.notification_queue``）に書き出します。
4. 「Log Notification」スケジュールジョブが 5 分間隔で OpenSearch からイベントを読み取り、ログレベルごとにグルーピングして、レベルごとに通知を送信します。
5. 通知送信後、処理済みのイベントはインデックスから削除されます。

.. note::
   各ノードは自身が記録したログのみを対象に通知します（イベントは ``hostname`` で絞り込まれます）。
   クラスター構成では、ノードごとに個別の通知が送信されます。

.. note::
   無限ループを防止するため、通知機能自体に関連するロガー
   （``LogNotificationAppender``、``LogNotificationHelper``、``LogNotificationTarget``、
   ``LogNotificationJob``、``NotificationHelper``、および HTTP 通信に使用される
   ``org.codelibs.curl``）のログは通知対象から除外されます。

セットアップ
============

有効化
------

管理画面からの有効化
~~~~~~~~~~~~~~~~~~~~

1. 管理画面にログインします。
2. 「システム」メニューから「全般」を選択します。
3. 「ログ通知」チェックボックスを有効にします。
4. 「ログ通知レベル」で通知対象のレベルを選択します（``ERROR``、``WARN``、``INFO``、``DEBUG``、``TRACE``）。
5. 「更新」ボタンをクリックします。

.. note::
   デフォルトでは ``ERROR`` レベルのみが通知対象です。
   ``WARN`` を選択すると、``WARN`` と ``ERROR`` の両方が通知されます。

システムプロパティによる有効化
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

管理画面の「全般」設定で保存されるシステムプロパティ（``system.properties``）を直接設定することもできます。

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

通知先の設定
------------

通知先（メールの宛先、Slack / Google Chat の Webhook URL）は、いずれも管理画面の
「システム」→「全般」設定で構成します。少なくとも 1 つの通知先を設定してください。
通知先が 1 つも設定されていない場合、ログ通知ジョブは何も送信せずに終了します。

メール通知
~~~~~~~~~~

メール通知を利用するには、以下の設定が必要です。

1. メールサーバーの設定（``fess_env.properties``）:

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. 管理画面の「全般」設定の「通知メール」にメールアドレスを入力します。
   複数のアドレスはカンマ区切りで指定できます。

Slack 通知
~~~~~~~~~~

Slack の Incoming Webhook URL を、管理画面の「全般」設定の「Slack Webhook URL」に入力します。
複数の URL はカンマまたは空白で区切って指定できます。
この値はシステムプロパティ ``slack.webhook.urls`` として保存されます。

Google Chat 通知
~~~~~~~~~~~~~~~~

Google Chat の Webhook URL を、管理画面の「全般」設定の「Google Chat Webhook URL」に入力します。
複数の URL はカンマまたは空白で区切って指定できます。
この値はシステムプロパティ ``google.chat.webhook.urls`` として保存されます。

.. note::
   「通知メール」を設定せずに Slack または Google Chat の Webhook URL のみを設定した場合、
   メールは送信されず、Slack / Google Chat への通知のみが行われます。
   Slack / Google Chat には、メール通知と同じ件名と本文がメッセージとして送信されます。

設定プロパティ
==============

``fess_config.properties`` で以下のプロパティを設定できます。

.. list-table:: ログ通知設定プロパティ
   :header-rows: 1
   :widths: 40 15 45

   * - プロパティ
     - デフォルト値
     - 説明
   * - ``log.notification.flush.interval``
     - ``30``
     - バッファから OpenSearch へのフラッシュ間隔（秒）
   * - ``log.notification.buffer.size``
     - ``1000``
     - メモリ上のバッファに保持するイベントの最大数
   * - ``log.notification.interval``
     - ``300``
     - 通知メッセージに表示される集計期間（秒）。表示専用の値であり、実際のジョブ実行間隔ではありません（後述の注記を参照）。
   * - ``log.notification.search.size``
     - ``1000``
     - 1回のジョブ実行で OpenSearch から取得するイベントの最大数
   * - ``log.notification.max.display.events``
     - ``50``
     - 1回の通知メッセージに含めるイベントの最大数
   * - ``log.notification.max.message.length``
     - ``200``
     - 各ログメッセージの最大文字数（超過分は切り詰め）
   * - ``log.notification.max.details.length``
     - ``3000``
     - 通知メッセージの詳細部分の最大文字数

.. note::
   ``log.notification.flush.interval`` の変更は |Fess| の再起動後に反映されます。
   その他のプロパティは次回の通知サイクルから反映されます。

.. note::
   ``log.notification.interval`` は通知メッセージ内の「過去 N 秒間」という表示テキストに
   使用される値であり、ジョブの実行頻度は変わりません。実際の実行間隔は「Log Notification」
   スケジュールジョブの cron 設定（デフォルトは 5 分間隔）で決まります。ジョブの実行間隔を
   変更する場合は、「システム」→「スケジューラ」からこのジョブの cron 式を変更し、
   表示が実態と一致するように ``log.notification.interval`` も合わせて調整してください。

通知メッセージの形式
====================

メール通知
----------

メール通知は以下の形式で送信されます。

**件名:**

::

    [FESS] ERROR Log Alert: hostname

**本文:**

::

    --- Server Info ---
    Host Name: hostname

    --- Log Summary ---
    Level: ERROR
    Total: 2 event(s) in the last 300 seconds

    --- Log Details ---
    Total: 2 event(s)

    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR と WARN のイベントはレベルごとに別々の通知として送信されます。

.. note::
   表示するイベント数が ``log.notification.max.display.events`` を超える場合、詳細部分の
   先頭は ``Total: N event(s) (showing M)`` となり、末尾に ``... and X more`` が付加されます。
   各ログメッセージは ``log.notification.max.message.length`` を超えると末尾が ``...`` で
   切り詰められ、詳細部分全体が ``log.notification.max.details.length`` を超えると以降は
   切り捨てられます。

Slack / Google Chat 通知
------------------------

Slack および Google Chat の通知も同様の内容がメッセージとして送信されます。

運用ガイド
==========

推奨設定
--------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 環境
     - 推奨レベル
     - 理由
   * - 本番環境
     - ``ERROR``
     - 重要なエラーのみ通知し、ノイズを減らす
   * - ステージング環境
     - ``WARN``
     - 潜在的な問題も含めて通知
   * - 開発環境
     - 無効
     - ログファイルを直接確認

OpenSearch インデックス
----------------------

ログ通知機能は、イベントの一時保存に ``fess_log.notification_queue`` インデックスを使用します
（インデックス名は ``index.log`` の値（デフォルト ``fess_log``）に ``.notification_queue`` を
付加したものです）。このインデックスは機能の初回使用時に自動作成されます。
通知送信後にイベントは削除されるため、通常はインデックスサイズが大きくなることはありません。

.. note::
   1 回のジョブ実行で処理されるイベント数は ``log.notification.search.size``（デフォルト
   1,000 件）が上限です。この上限を超えて蓄積されたイベントは、通知送信後にまとめて破棄され、
   次回以降の実行には引き継がれません。短時間に大量のログが発生する環境では、必要に応じて
   ``log.notification.search.size`` を引き上げてください。

トラブルシューティング
======================

通知が送信されない
------------------

1. **有効化の確認**

   管理画面の「全般」設定で「ログ通知」が有効になっているか確認します。

2. **通知先の確認**

   少なくとも 1 つの通知先（「通知メール」、「Slack Webhook URL」、「Google Chat Webhook URL」の
   いずれか）が設定されているか確認します。いずれも未設定の場合、ジョブは
   ``No notification targets configured.`` を出力して何も送信しません。

3. **メールサーバー設定の確認**

   メール通知を使用する場合、``fess_env.properties`` でメールサーバーが正しく
   設定されているか確認します。

4. **スケジュールジョブの確認**

   「システム」→「スケジューラ」で「Log Notification」ジョブが有効になっているか確認します。
   このジョブが無効化されていると、通知は送信されません。

5. **ログの確認**

   ``fess.log`` で通知関連のエラーメッセージを確認します。

   ::

       grep -i "notification" /var/log/fess/fess.log

通知が多すぎる
--------------

1. **ログレベルの引き上げ**

   通知レベルを ``WARN`` から ``ERROR`` に変更します。

2. **根本原因の対処**

   頻繁にエラーが発生している場合は、エラーの根本原因を調査してください。

通知内容が切り詰められる
------------------------

以下のプロパティを調整してください。

- ``log.notification.max.details.length``: 詳細部分の最大文字数
- ``log.notification.max.display.events``: 表示するイベントの最大数
- ``log.notification.max.message.length``: 各メッセージの最大文字数

参考情報
========

- :doc:`admin-logging` - ログ設定
- :doc:`setup-memory` - メモリ設定
