============================================================
第6回 開発チームのナレッジハブ -- コード・Wiki・チケットの統合検索環境
============================================================

はじめに
========

ソフトウェア開発チームでは、日々の業務で様々なツールを使い分けています。
コードは Git リポジトリに、仕様書は Confluence に、タスクは Jira に、日常的なやりとりは Slack に。
それぞれのツールには検索機能がありますが、「あの議論はどこでしたっけ？」という問いに対して、すべてのツールを個別に検索するのは非効率です。

本記事では、開発チームが日常的に使うツールの情報を Fess に集約し、統合検索できるナレッジハブを構築します。

対象読者
========

- ソフトウェア開発チームのリーダーやインフラ担当者
- 開発関連ツールの情報を横断検索したい方
- データストアプラグインの基本的な使い方を知りたい方

シナリオ
========

開発チーム（20名）の情報を統合検索できるようにします。

.. list-table:: 対象データソース
   :header-rows: 1
   :widths: 20 30 50

   * - ツール
     - 用途
     - 検索したい情報
   * - Git リポジトリ
     - ソースコード管理
     - コード、README、設定ファイル
   * - Confluence
     - ドキュメント管理
     - 設計書、議事録、手順書
   * - Jira
     - チケット管理
     - バグ報告、タスク、ストーリー
   * - Slack
     - コミュニケーション
     - 技術的な議論、意思決定の記録

データストアクロールとは
========================

Web クロールやファイルクロールは、URL やファイルパスを辿ってドキュメントを収集します。
一方、SaaS ツールの情報を収集するには「データストアクロール」を使用します。

データストアクロールは、各ツールの API を通じてデータを取得し、Fess のインデックスに登録します。
Fess では、ツールごとにデータストアプラグインが用意されています。

プラグインのインストール
========================

データストアプラグインは、Fess の管理画面からインストールできます。

1. 管理画面の ［システム］ > ［プラグイン］ を選択
2. インストール済みプラグインの一覧を確認
3. ［インストール］ ボタンからインストール画面に移動し、［リモート］ タブから必要なプラグインをインストール

今回のシナリオでは、以下のプラグインを利用します。

- ``fess-ds-git``: Git リポジトリのクロール
- ``fess-ds-atlassian``: Confluence / Jira のクロール
- ``fess-ds-slack``: Slack メッセージのクロール

各データソースの設定
====================

Git リポジトリの設定
---------------------

Git リポジトリをクロールして、コードやドキュメントを検索対象にします。

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: GitDataStore を選択
3. パラメータの設定

**パラメータの設定例**

.. code-block:: properties

    uri=https://github.com/example/my-repo.git
    username=git-user
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    include_pattern=.*\.(java|py|js|ts|md|rst|txt)$
    max_size=10000000

**スクリプトの設定例**

.. code-block:: properties

    url=url
    title=name
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp

``uri`` にリポジトリの URL を、``username`` / ``password`` に認証情報を指定します。プライベートリポジトリの場合はアクセストークンを ``password`` に設定します。``include_pattern`` でクロール対象のファイル拡張子を正規表現で絞り込めます。

Confluence の設定
------------------

Confluence のページやブログ記事を検索対象にします。

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: ConfluenceDataStore を選択
3. パラメータの設定

**パラメータの設定例**

.. code-block:: properties

    home=https://your-domain.atlassian.net/wiki
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token

**スクリプトの設定例**

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body
    last_modified=content.last_modified

``home`` に Confluence の URL を指定し、``auth_type`` で認証方式を選択します。Confluence Cloud の場合は ``basic`` 認証で、``basic.password`` に API トークンを設定します。

Jira の設定
------------

Jira のチケット（Issue）を検索対象にします。

同じ ``fess-ds-atlassian`` プラグインに含まれる JiraDataStore ハンドラーを使用します。
JQL（Jira Query Language）を使って、クロール対象のチケットを絞り込むこともできます。
例えば、特定のプロジェクトのチケットのみを対象にしたり、特定のステータス（Closed 以外）のチケットのみを対象にしたりできます。

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: JiraDataStore を選択
3. パラメータの設定

**パラメータの設定例**

.. code-block:: properties

    home=https://your-domain.atlassian.net
    auth_type=basic
    basic.username=user@example.com
    basic.password=your-api-token
    issue.jql=project = MYPROJ AND status != Closed

**スクリプトの設定例**

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description
    last_modified=issue.last_modified

``issue.jql`` に JQL クエリを指定して、クロール対象のチケットを絞り込みます。

Slack の設定
-------------

Slack のメッセージを検索対象にします。

1. ［クローラー］ > ［データストア］ > ［新規作成］
2. ハンドラー名: SlackDataStore を選択
3. パラメータの設定

**パラメータの設定例**

.. code-block:: properties

    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=general,engineering,design
    include_private=false

**スクリプトの設定例**

.. code-block:: properties

    url=message.permalink
    title=message.title
    content=message.text
    last_modified=message.timestamp

``token`` に Slack Bot の OAuth トークンを指定します。``channels`` でクロール対象のチャンネルを指定でき、すべてのチャンネルを対象にする場合は ``*all`` を設定します。プライベートチャンネルを対象にする場合は ``include_private=true`` を設定し、Bot をそのチャンネルに招待しておく必要があります。

ラベルの活用
============

ラベルで情報源を区別する
------------------------

各データソースにラベルを設定することで、検索時に情報源を切り替えられるようにします。

- ``code``: Git リポジトリからのコード
- ``docs``: Confluence のドキュメント
- ``tickets``: Jira のチケット
- ``discussions``: Slack のメッセージ

利用者は「すべて」で横断検索し、必要に応じてラベルで絞り込めます。

検索品質の向上
===============

ドキュメントブーストの活用
--------------------------

開発チームのナレッジハブでは、すべてのドキュメントが同じ重要度ではありません。
例えば、以下のような優先度が考えられます。

1. Confluence のドキュメント（正式な仕様書・手順書）
2. Jira のチケット（最新の課題・進行中のタスク）
3. Git リポジトリ（コード・README）
4. Slack のメッセージ（議論の記録）

ドキュメントブーストを使うと、特定の条件に一致するドキュメントの検索スコアを上げることができます。
管理画面の ［クローラー］ > ［ドキュメントブースト］ から、URL パターンやラベルに基づいてブースト値を設定できます。

関連コンテンツの活用
--------------------

検索結果に「関連コンテンツ」を表示することで、利用者が求めている情報への到達を支援できます。
例えば、Confluence の設計書を検索した際に、関連する Jira チケットが「関連コンテンツ」として表示されると便利です。

運用上の考慮点
===============

クロールスケジュール
--------------------

データソースごとに適切なクロール頻度を設定します。

.. list-table:: スケジュール例
   :header-rows: 1
   :widths: 25 25 50

   * - データソース
     - 推奨頻度
     - 理由
   * - Confluence
     - 4時間ごと
     - ドキュメントの更新頻度は中程度
   * - Jira
     - 2時間ごと
     - チケットの更新は頻繁
   * - Git
     - 日次
     - リリースサイクルに合わせる
   * - Slack
     - 4時間ごと
     - リアルタイム性は不要だが鮮度は重要

API レート制限への対応
----------------------

SaaS ツールの API にはレート制限があります。
クロールの間隔（インターバル）を適切に設定して、API のレート制限に抵触しないようにします。
特に Slack API はレート制限が厳しいため、クロール間隔に余裕を持たせることが重要です。

アクセストークンの管理
----------------------

データストアプラグインの設定には、各ツールの API アクセストークンが必要です。
セキュリティの観点から、以下の点に注意してください。

- 最小権限の原則: 読み取り専用のアクセストークンを使用
- 定期的なローテーション: トークンを定期的に更新
- 専用アカウントの利用: 個人アカウントではなく、サービスアカウントを使用

まとめ
======

本記事では、開発チームが日常的に使うツールの情報を Fess に集約し、統合検索できるナレッジハブを構築しました。

- データストアプラグインで Git、Confluence、Jira、Slack のデータを収集
- ラベルで開発者に使いやすい検索体験を提供
- ドキュメントブーストで情報の優先度を制御
- API レート制限やトークン管理などの運用上の考慮点

開発チームのナレッジハブにより、「あの議論はどこで？」「この仕様書は？」という問いに素早く答えられる環境が実現します。

次回は、クラウドストレージの横断検索について扱います。

参考資料
========

- `Fess データストア設定 <https://fess.codelibs.org/ja/15.5/admin/dataconfig.html>`__

- `Fess プラグイン管理 <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
