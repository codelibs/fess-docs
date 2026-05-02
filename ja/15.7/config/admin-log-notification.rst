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
2. 捕捉されたイベントはメモリ上のバッファ（最大1,000件）に蓄積されます。
3. タイマーが 30 秒間隔でバッファ内のイベントを OpenSearch のインデックス（``fess_log.notification_queue``）に書き出します。
4. スケジュールジョブが 5 分間隔で OpenSearch からイベントを読み取り、ログレベルごとにグルーピングして通知を送信します。
5. 通知送信後、処理済みのイベントはインデックスから削除されます。

.. note::
   通知機能自体のログ（``LogNotificationHelper``、``LogNotificationJob`` など）は、
   無限ループを防止するため通知対象から除外されます。

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

管理画面の「全般」設定で保存されるシステムプロパティを直接設定することもできます。

::

    log.notification.enabled=true
    fess.log.notification.level=ERROR

通知先の設定
------------

メール通知
~~~~~~~~~~

メール通知を利用するには、以下の設定が必要です。

1. メールサーバーの設定（``fess_env.properties``）:

   ::

       mail.smtp.server.main.host.and.port=smtp.example.com:587

2. 管理画面の「全般」設定で「通知先」にメールアドレスを入力します。複数のアドレスはカンマ区切りで指定できます。

Slack 通知
~~~~~~~~~~

Slack の Incoming Webhook URL を設定することで、Slack チャネルに通知を送信できます。

Google Chat 通知
~~~~~~~~~~~~~~~~

Google Chat の Webhook URL を設定することで、Google Chat スペースに通知を送信できます。

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
     - 通知ジョブの実行間隔（秒）
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
   これらのプロパティの変更は |Fess| の再起動後に反映されます。

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
    Total: 5 event(s) in the last 300 seconds

    --- Log Details ---
    [2025-03-26T10:30:45.123] ERROR org.codelibs.fess.crawler - Connection timeout
    [2025-03-26T10:30:46.456] ERROR org.codelibs.fess.app.web - Failed to process request

    Note: See the log files for full details.

.. note::
   ERROR と WARN のイベントはレベルごとに別々の通知として送信されます。

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

ログ通知機能は、イベントの一時保存に ``fess_log.notification_queue`` インデックスを使用します。
このインデックスは機能の初回使用時に自動作成されます。
通知送信後にイベントは削除されるため、通常はインデックスサイズが大きくなることはありません。

トラブルシューティング
======================

通知が送信されない
------------------

1. **有効化の確認**

   管理画面の「全般」設定で「ログ通知」が有効になっているか確認します。

2. **通知先の確認**

   メール通知の場合、「通知先」にメールアドレスが設定されているか確認します。

3. **メールサーバー設定の確認**

   ``fess_env.properties`` でメールサーバーが正しく設定されているか確認します。

4. **ログの確認**

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
