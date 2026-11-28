===============================
Fess でできることと導入の進め方
===============================

はじめに
========

社内の文書は、Web サイト、ファイルサーバー、クラウドストレージ、チャットやチケット管理などの SaaS、データベースに分かれて置かれています。
それぞれのツールに検索機能があっても、場所をまたいで一度に探すことはできません。
Fess は、これらの場所から文書を集めて 1 つのインデックスにまとめ、1 つの検索画面や API から探せるようにする検索サーバーです。

この記事は、Fess の導入を検討している情報システム部門の担当者や開発者に向けて、次のことを説明します。

- Fess が何でできていて、どのように動くのか
- 標準で使える機能と、プラグインを追加して使う機能の区別
- 目的ごとに、どの記事から読み進めればよいか

各機能の設定手順は、それぞれの記事で扱います。

この実践ガイドが対象とするバージョン
====================================

実践ガイドの各記事は、Fess 15.9 を対象にしています。
画面の項目名、設定キー、既定値は 15.9 で確かめたものです。
15.10 以降でのみ使える機能を紹介する場合は、その旨を記事中に明記しています。

リファレンスへのリンクは ``https://fess.codelibs.org/ja/stable/`` で始まり、現在の安定版のドキュメントを指します。
別のバージョンを使っている場合は、URL の ``stable`` をバージョン番号（例: ``15.9``）に置き換えたページで、項目名や既定値を確かめてください。

Fess とは
=========

Fess は、Java で書かれたオープンソースの全文検索サーバーです。
ライセンスは Apache License 2.0 で、商用環境でも無償で利用できます。

文書の保存と検索には OpenSearch を使います。
Fess 15.9 は起動時に接続先を確かめ、OpenSearch 3 以降でなければ起動を中止します。
OpenSearch 2 以前や Elasticsearch には接続できません。
15.9 では本体に組み込まれていた検索エンジンが取り除かれたので、OpenSearch は必ず別に用意します（Docker の構成では、OpenSearch のコンテナも一緒に起動します）。

1 つの Fess に、次のものがそろっています。

- 文書を集めるクローラー（Web、ファイルサーバー、プラグイン経由の各種サービス）
- クロール設定、ユーザー、権限、辞書、スケジュールなどを設定する管理画面
- 利用者が使う検索画面
- 検索やサジェストを外部のシステムから呼び出すための API（``/api/v2/``）

検索画面は、HTML・CSS・JavaScript をまとめた静的なテーマで表示されます。
Fess には ``bootstrap`` テーマが同梱されており、別のテーマは ZIP ファイルとして［システム］>［テーマ］から追加します。

Fess の構成
===========

Fess を動かすときに登場する要素は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 要素
     - 役割
   * - Fess 本体（Web アプリケーション）
     - 検索画面、管理画面、API を提供します。スケジューラもここで動き、設定された時刻にクロールなどのジョブを起動します
   * - クローラー（別プロセス）
     - クロールのジョブは、Fess 本体とは別の Java プロセスとして起動されます。Web ページやファイルを取得し、本文を抽出して OpenSearch に登録します。サジェストの作成、サムネイルの作成、セマンティック検索用のベクトル作成のジョブも、同じように別プロセスで動きます
   * - OpenSearch
     - 検索対象の文書のインデックスを保持し、検索を実行します。クロール設定やユーザー、ジョブログ、検索ログなど、管理画面で登録した情報の多くもここに保存されます

クローラーは別の Java プロセスなので、使うメモリも Fess 本体とは別に設定します（:doc:`guide-14` で扱います）。

文書が検索できるようになるまでの流れは次のとおりです。

1. 管理画面でクロール設定（対象の URL やパス、検索結果を見せる相手を決めるパーミッションなど）を登録します
2. スケジューラがクロールのジョブを起動します。管理画面から［今すぐ開始］で手動で起動することもできます
3. クローラーが文書を取得し、本文を抽出して、パーミッションと一緒に OpenSearch に登録します
4. 利用者が検索すると、Fess は利用者のロールやグループで結果を絞り込んでから返します

Docker での起動からクロール、検索までの一連の操作は、:doc:`guide-02` で実際に試せます。

本体の機能とプラグイン
======================

Fess 15.9 では、多くの機能がプラグインとして本体から分けて提供されています。
必要なプラグインがあらかじめ入っているかどうかは、導入方法によって異なります。

- ZIP・RPM・DEB で導入した Fess には、プラグインは 1 つも入っていません
- Docker の標準イメージ（``ghcr.io/codelibs/fess:15.9.0`` など）には、次の 7 つのプラグインがあらかじめ入っています: ``fess-script-groovy``\ 、\ ``fess-storage-s3``\ 、\ ``fess-storage-gcs``\ 、\ ``fess-sso-saml``\ 、\ ``fess-sso-spnego``\ 、\ ``fess-sso-entraid``\ 、\ ``fess-sso-oidc``
- Docker の slim イメージ（``15.9.0-slim`` など）には、プラグインは入っていません

主な機能と、必要なプラグインを次の表にまとめます。

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * - 機能
     - 本体だけで使えるもの
     - プラグインが必要なもの
   * - クロール
     - Web（http・https）、ファイルシステム、ファイルサーバー（SMB）、FTP
     - Amazon S3（``fess-storage-s3``）、Google Cloud Storage（``fess-storage-gcs``）、ブラウザーで JavaScript を実行して取得する Web クロール（``fess-crawler-playwright``）
   * - SaaS・データベースなど
     - データストアの設定画面と実行の仕組み
     - 取り込む対象ごとのデータストアプラグイン（``fess-ds-*``）。Slack、Confluence・Jira、Google Drive、Microsoft 365、Box、データベース、CSV、Git など
   * - ログインと権限
     - Fess に登録したユーザー・ロール・グループ、LDAP / Active Directory との連携
     - SSO（OpenID Connect は ``fess-sso-oidc``\ 、SAML は ``fess-sso-saml``\ 、Entra ID は ``fess-sso-entraid``\ 、SPNEGO は ``fess-sso-spnego``）
   * - スクリプト
     - JavaScript
     - Groovy（``fess-script-groovy``）、OGNL（``fess-script-ognl``）
   * - 検索画面
     - 同梱テーマ ``bootstrap``
     - プラグインではなく、テーマの ZIP ファイルを追加します
   * - API
     - ``/api/v2/``\ （検索、ラベル、サジェスト、人気ワード、ヘルスチェックなど）と管理 API
     - ``/api/v1/``\ （``fess-webapp-v1-api``）、``/json`` と ``/suggest``\ （``fess-webapp-classic-api``）。Fess Site Search は ``/api/v1/`` を使うため、``fess-webapp-v1-api`` が必要です
   * - AI 関連
     - セマンティック検索と AI 検索モード（RAG）の仕組み。OpenSearch にデプロイした埋め込みモデルを使う場合は、セマンティック検索にプラグインは不要です
     - LLM や外部の埋め込みモデルとの接続（``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、\ ``fess-llm-gemini``\ 、\ ``fess-llm-bedrock``）、MCP サーバー（``fess-webapp-mcp``）、画像検索（``fess-webapp-multimodal``）

表の「プラグインが必要なもの」のうち、Docker の標準イメージに入っているのは、S3・GCS、SSO の 4 種類、Groovy だけです。
それ以外は、どの導入方法でも追加のインストールが必要です。

スクリプトの種類に Groovy を指定した設定と、以前のバージョンから引き継いだ設定のうちスクリプトの種類が記録されていないものは、Groovy として実行されます。
これらを使うには ``fess-script-groovy`` が必要です。
新しく作るデータストア設定では、スクリプトの種類の初期値は JavaScript です。

プラグインは次のいずれかの方法でインストールします。
インストールや削除をした後は、Fess を再起動します。
プラグインのバージョンは、Fess のバージョンに合わせます（Fess 15.9 なら 15.9.x）。

- 管理画面の［システム］>［プラグイン］で［インストール］をクリックし、一覧から選ぶ
- コマンドラインで ``bin/fess-setup install plugin <プラグイン名>:<バージョン>`` を実行する
- Docker では、環境変数 ``FESS_PLUGINS`` に ``fess-ds-slack:15.9.0 fess-webapp-mcp:15.9.0`` のように空白区切りで指定する

データストアプラグインの使い方は :doc:`datastore-basics`\ 、プラグインを自作する方法は :doc:`guide-17` で説明しています。

検索できるファイルの形式
========================

ファイルからの本文の抽出には、Apache Tika などの抽出処理を使います。
HTML、PDF、Microsoft Office の文書、テキスト、圧縮ファイルの中身などを検索できます。
確認済みの形式の一覧は `検索対象ファイル <https://fess.codelibs.org/ja/supported-files.html>`__ を参照してください。

画像や、スキャンして作った PDF の中の文字は、既定では検索できません。
クローラーが動くホストに ``tesseract`` を入れ、OCR を有効にすると検索できるようになります。
手順は `OCR（画像内の文字認識）の設定 <https://fess.codelibs.org/ja/stable/config/crawler-ocr.html>`__ を参照してください。

導入方法を選ぶ
==============

Fess は Docker、ZIP、RPM、DEB で配布されています。
まず試すなら、Fess と OpenSearch をまとめて起動できる Docker が手早い方法です。
手順は :doc:`guide-02` で説明しています。

本番環境では、OpenSearch を別のサーバーやクラスターとして用意することもできます。
必要な Java や OpenSearch のバージョン、CPU・メモリ・ディスクの目安は `システム要件 <https://fess.codelibs.org/ja/stable/install/prerequisites.html>`__ を確認してください。

目的別の読み進め方
==================

記事は目的ごとに読み進められるように分かれています。
目的に近い行を選び、記事を左から順に読んでください。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 目的
     - 読む記事
   * - まず試してみたい
     - :doc:`guide-02`
   * - ファイルサーバーを検索したい
     - :doc:`file-server-search` → :doc:`guide-04` → :doc:`guide-05`
   * - クラウドや SaaS のデータを検索したい
     - :doc:`datastore-basics` → :doc:`guide-07` / :doc:`guide-06` / :doc:`guide-12`
   * - 既存のサイトやシステムに検索を組み込みたい
     - :doc:`guide-03` → :doc:`guide-11`
   * - 部署や利用者ごとに見せる情報を分けたい
     - :doc:`guide-05` → :doc:`guide-15` → :doc:`guide-13`
   * - AI で検索を強化したい
     - :doc:`guide-18` → :doc:`guide-19` → :doc:`guide-20`
   * - 本番運用を始める
     - :doc:`guide-10` → :doc:`guide-16` → :doc:`guide-14`

このほかに、次の記事があります。

- 検索品質を高める: :doc:`guide-08`\ 、:doc:`guide-09`\ 、:doc:`guide-22`
- 画像とテキストをまとめて検索する: :doc:`guide-21`
- プラグインを自作する: :doc:`guide-17`
- 全社展開を計画する: :doc:`guide-23`
- 活用事例や他の製品との比較: :doc:`use-cases`\ 、:doc:`comparison`

記事の一覧は :doc:`../guide` のページにもまとめています。

参考資料
========

- `Fess ドキュメント（安定版） <https://fess.codelibs.org/ja/stable/>`__
- `システム要件 <https://fess.codelibs.org/ja/stable/install/prerequisites.html>`__
- `プラグイン <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `プラグインアーキテクチャ <https://fess.codelibs.org/ja/stable/dev/plugin-architecture.html>`__
- `テーマ <https://fess.codelibs.org/ja/stable/admin/theme-guide.html>`__
- `検索対象ファイル <https://fess.codelibs.org/ja/supported-files.html>`__
- `docker-fess（GitHub） <https://github.com/codelibs/docker-fess>`__
- `codelibs/fess（GitHub） <https://github.com/codelibs/fess>`__
