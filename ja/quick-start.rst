==============
簡単構築ガイド
==============

はじめに
========

Fess（フェス）は、オープンソースの全文検索サーバーです。
Webサイトやファイルサーバーなどを対象にクロール（巡回）し、収集したコンテンツを横断検索できます。

ここでの説明は素早く Fess に触れてみたい人向けのものです。
Fess を利用するための最小限の手順を記述します。

どちらの方法を使う？
====================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - Docker（推奨）
     - ZIP パッケージ
   * - 事前準備
     - Docker と Docker Compose
     - Java 21（OpenSearch は ``fess-setup`` コマンドでインストールします）
   * - 起動の手軽さ
     - ◎ コマンド数行のみ
     - △ Java をインストールし、数個のセットアップコマンドを実行
   * - こんな人に
     - まず試してみたい人
     - Docker を使えない環境の人

Docker を使った起動（推奨）
==========================

所要時間の目安：**初回 5〜10 分程度**\ （Docker イメージのダウンロード時間を含む）

Docker と Docker Compose がインストールされている場合、以下のコマンドで Fess をすぐに起動できます。

**1. 設定ファイルのダウンロード**

::

    $ mkdir fess-docker && cd fess-docker
    $ curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose.yaml
    $ curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose-opensearch3.yaml

**2. コンテナの起動**

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**3. 起動の確認**

数分後、以下の URL にアクセスしてください：

- 検索画面: http://localhost:8080/
- 管理画面: http://localhost:8080/admin （admin/admin でログイン）

.. warning::

   管理者パスワードは必ず変更してください。

**4. 停止方法**

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

より詳細な Docker 環境の設定については、:doc:`Docker インストールガイド <15.9/install/install-docker>` を参照してください。

----

ZIP パッケージを使った起動
=========================

所要時間の目安：**初回 20〜30 分程度**\ （Java のインストールと OpenSearch のダウンロード時間を含む）

Docker を使用しない場合は、以下の手順で ZIP パッケージから起動できます。
Fess には検索エンジンが同梱されていないため、ZIP パッケージに含まれる ``fess-setup`` コマンドで
OpenSearch をダウンロードし、Fess に必要なプラグインをインストールします。

ここでの手順はお試し用の起動方法なので、運用向けの構築手順は、:doc:`インストール手順 <setup>` などを参照してください。
（この手順で起動したFessは簡単な動作確認用としての利用を想定しており、この環境の運用は推奨していません）

事前準備
--------

起動する前に Java 21 をインストールしてください。`Eclipse Temurin <https://adoptium.net/temurin>`__ の Java 21 を推奨します。
OpenSearch を事前にインストールする必要はありません。ステップ 2 でインストールします。

.. note::

   OpenSearch の公式ビルドが提供されているのは Linux と Windows のみです。macOS では
   ``fess-setup install opensearch`` はエラーで終了します。Docker（方法 1）を使用するか、
   Homebrew で OpenSearch をインストールする方法は :doc:`15.9/install/install-linux` を参照してください。

ステップ 1: ダウンロードと展開
------------------------------

`GitHubのリリースサイト <https://github.com/codelibs/fess/releases>`__ から最新のFessのZIPパッケージをダウンロードし、
展開してディレクトリに移動します。

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

ステップ 2: OpenSearch のインストール
-------------------------------------

``fess-setup`` は ``root`` ではなく一般ユーザーで実行してください。OpenSearch は ``root`` では起動しません。

::

    # Linux
    $ bin/fess-setup install opensearch

    # Windows
    > bin\fess-setup.bat install opensearch

このコマンドは、この Fess が対応するバージョンの OpenSearch を Fess ディレクトリ内の ``opensearch/`` にダウンロードし、
Fess に必要な 4 つのプラグインをインストールして、Fess に必要な設定を ``config/opensearch.yml`` に追加します。
``bin/fess`` はこの OpenSearch を自動的に見つけるため、OpenSearch を同じホストで実行する限り、設定ファイルを編集する必要はありません。

.. warning::

   このコマンドは ``plugins.security.disabled: true`` を設定するため、OpenSearch は認証なしでリクエストを受け付けます。
   デフォルトではループバックアドレスのみで待ち受けます。ネットワークに公開しないでください。
   本番環境向けの設定は :doc:`15.9/install/security` を参照してください。

すべてのコマンド（Node.js やプラグインのインストール、``check`` など）については、:doc:`15.9/install/fess-setup` を参照してください。

ステップ 3: OpenSearch と Fess の起動
-------------------------------------

先に OpenSearch を起動し、次に Fess を起動します。

::

    # Linux
    $ opensearch/opensearch-3.9.0/bin/opensearch -d
    $ bin/fess

.. code-block:: bat

    :: Windows（それぞれ別のコマンドプロンプトで実行）
    opensearch\opensearch-3.9.0\bin\opensearch.bat
    bin\fess.bat

Fess の起動まで 30 秒ほど待ってから、以下にアクセスします。

- http://localhost:8080/ （検索画面）
- http://localhost:8080/admin （管理画面 - ログイン: admin/admin）

インストールを確認するには、``bin/fess-setup check`` を実行します（Windows では ``bin\fess-setup.bat check``）。
OpenSearch に接続できるか、Fess に必要なプラグインが入っているかを報告します。

管理 UI にアクセス
------------------

\http://localhost:8080/admin にアクセスします。
デフォルトの管理者アカウントのユーザー名/パスワードは、admin/admin になります。

.. warning::

   デフォルトのパスワードは必ず変更してください。
   本番環境では、初回ログイン後すぐにパスワードを変更することを強く推奨します。

Fess の停止（ZIP版）
--------------------

Ctrl-C や kill コマンド等で fess のプロセスを停止します。
続けて、OpenSearch も同様に停止します（プロセスを ``kill`` するか、フォアグラウンドで実行している場合は Ctrl-C）。

----

クロール設定と検索
==================

**1. クロール設定の作成**

ログイン後、左側のメニューの「クローラー」>「ウェブ」をクリックします。
「新規作成」ボタンをクリックして、ウェブクロールの設定情報を作ります。

以下の情報を入力してください：

- **名前**: クロール設定の名前（例：会社のWebサイト）
- **URL**: クロール対象の URL（例：https://www.example.com/）
- **最大アクセス数**: クロールするページ数の上限（初めての場合は ``10`` 程度の小さい値を推奨）
- **間隔**: クロールの間隔（ミリ秒）（デフォルトの ``10000`` ミリ秒を推奨）

.. warning::

   最大アクセス数を大きくしすぎると、対象サイトに過剰な負荷をかける場合があります。
   動作確認の際は必ず小さい値（10〜100程度）から始めてください。
   自分が管理していないサイトをクロールする場合は、robots.txt の設定に従ってください。

**2. クロールの実行**

左側のメニューの「システム」>「スケジューラー」をクリックします。
「Default Crawler」ジョブの「今すぐ開始」ボタンをクリックして、即座にクロールを開始できます。

スケジュール実行する場合は、「Default Crawler」を選択して、スケジュールを設定します。
開始時刻が 10:35 am の場合は、35 10 \* \* ? とします（フォーマットは「分 時 日 月 曜日 年」）。
更新すると、その時間以降にクロールが開始されます。

開始されているかどうかは、「クロール情報」で確認できます。
クロール完了後、セッション情報に WebIndexSize の情報が表示されます。

**3. 検索**

クロール完了後、\http://localhost:8080/ にアクセスし、検索すると検索結果が表示されます。

より詳しく知るには
==================

以下のドキュメントなどを参照してください。

* :doc:`ドキュメント一覧 <documentation>`
* `[連載] 簡単導入！ OSS全文検索サーバーFess入門 <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* :doc:`開発者向け情報 <development>`
* `ディスカッションフォーラム <https://discuss.codelibs.org/c/fessja/>`__
