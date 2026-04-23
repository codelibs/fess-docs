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
     - Java 21、OpenSearch
   * - 起動の手軽さ
     - ◎ コマンド数行のみ
     - △ 複数ソフトのインストールが必要
   * - こんな人に
     - まず試してみたい人
     - Docker を使えない環境の人

Docker を使った起動（推奨）
==========================

所要時間の目安：**初回 5〜10 分程度**（Docker イメージのダウンロード時間を含む）

Docker と Docker Compose がインストールされている場合、以下のコマンドで Fess をすぐに起動できます。

**1. 設定ファイルのダウンロード**

::

    $ mkdir fess-docker && cd fess-docker
    $ curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    $ curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

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

より詳細な Docker 環境の設定については、`Docker インストールガイド <15.6/install/install-docker>`__ を参照してください。

----

ZIP パッケージを使った起動
=========================

所要時間の目安：**初回 20〜30 分程度**（Java・OpenSearch のインストール時間を含む）

Docker を使用しない場合は、以下の手順で ZIP パッケージから起動できます。

ここでの手順はお試し用の起動方法なので、運用向けの構築手順は、:doc:`インストール手順 <setup>` などを参照してください。
（この手順で起動したFessは簡単な動作確認用としての利用を想定しており、この環境の運用は推奨していません）

事前準備
--------

Fessを起動する前に、以下のソフトウェアをインストールしておいてください。

**1. Java 21 のインストール**

`Eclipse Temurin <https://adoptium.net/temurin>`__ の Java 21 を推奨します。

**2. OpenSearch のインストールと起動**

Fess のデータを保存するために OpenSearch が必要です。
:doc:`インストール手順 <setup>` を参照してインストールし、起動しておいてください。

ダウンロード
------------

`GitHubのリリースサイト <https://github.com/codelibs/fess/releases>`__ から最新のFessのZIPパッケージをダウンロードします。

インストール
------------

ダウンロードした fess-x.y.z.zip を展開します。

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

Fess の起動
-----------

fess スクリプトを実行して Fess を起動します。
（Windowsの場合は、fess.batを実行してください）

::

    $ ./bin/fess

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
- **間隔**: クロールの間隔（ミリ秒）（デフォルトの ``1000`` ミリ秒を推奨）

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

* `ドキュメント一覧 <documentation>`__
* `[連載] 簡単導入！ OSS全文検索サーバーFess入門 <https://news.mynavi.jp/techplus/series/_ossfess/>`__
* `開発者向け情報 <development>`__
* `ディスカッションフォーラム <https://discuss.codelibs.org/c/fessja/>`__
