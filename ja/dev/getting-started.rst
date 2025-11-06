================================================
オープンソース全文検索サーバー - |Fess| 開発概要
================================================

このページでは、|Fess| 開発の全体像と、開発を始めるための基本情報を提供します。

.. contents:: 目次
   :local:
   :depth: 2

概要
====

|Fess| は、Java で開発されたオープンソースの全文検索サーバーです。
エンタープライズ検索を簡単に構築できることを目指し、
強力な検索機能と使いやすい管理画面を提供しています。

|Fess| の特徴
-------------

- **簡単なセットアップ**: Java 環境があればすぐに起動できる
- **強力なクローラー**: Web サイト、ファイルシステム、データベースなど多様なデータソースに対応
- **日本語対応**: 日本語の全文検索に最適化
- **拡張性**: プラグインによる機能拡張が可能
- **REST API**: 検索機能を他のアプリケーションから利用可能

技術スタック
==========

|Fess| は以下の技術を使用して開発されています。

対象バージョン
------------

このドキュメントは、以下のバージョンを対象としています：

- **Fess**: 15.3.0
- **Java**: 21 以降
- **OpenSearch**: 3.3.0
- **Maven**: 3.x

主要な技術とフレームワーク
----------------------

Java 21
~~~~~~~

|Fess| は Java 21 以降で動作するアプリケーションです。
最新の Java 機能を活用し、パフォーマンスと保守性を向上させています。

- **推奨**: Eclipse Temurin 21（旧 AdoptOpenJDK）
- **最小バージョン**: Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ は、
|Fess| の Web アプリケーション層で使用されているフレームワークです。

**主な機能:**

- DI（依存性注入）コンテナ
- Action ベースの Web フレームワーク
- バリデーション
- メッセージ管理
- 設定管理

**学習リソース:**

- `LastaFlute 公式ドキュメント <https://github.com/lastaflute/lastaflute>`__
- Fess のコードを読むことで実践的な使い方を学べます

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ は、
データベースアクセスのための O/R マッピングツールです。
|Fess| では OpenSearch のスキーマから Java コードを自動生成するために使用しています。

**主な機能:**

- タイプセーフな SQL ビルダー
- スキーマからのコード自動生成
- データベースドキュメントの自動生成

**学習リソース:**

- `DBFlute 公式サイト <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ は、
|Fess| の検索エンジンとして使用されている分散検索・分析エンジンです。

**対応バージョン**: OpenSearch 3.3.0

**必須プラグイン:**

- opensearch-analysis-fess: Fess 専用の形態素解析プラグイン
- opensearch-analysis-extension: 追加の言語解析機能
- opensearch-minhash: 類似ドキュメント検出
- opensearch-configsync: 設定の同期

**学習リソース:**

- `OpenSearch ドキュメント <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven は、|Fess| のビルドツールとして使用されています。

**主な用途:**

- 依存ライブラリの管理
- ビルド処理の実行
- テストの実行
- パッケージの作成

開発ツール
========

推奨される開発環境
----------------

Eclipse
~~~~~~~

公式ドキュメントでは Eclipse を使用した開発方法を説明しています。

**推奨バージョン**: Eclipse 2023-09 以降

**必要なプラグイン:**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

IntelliJ IDEA でも開発が可能です。

**推奨エディション**: Community Edition または Ultimate Edition

**必要な機能:**

- Maven サポート（デフォルトで含まれています）
- Java サポート

VS Code
~~~~~~~

軽量な開発には VS Code も利用できます。

**必要な拡張機能:**

- Java Extension Pack
- Maven for Java

バージョン管理
~~~~~~~~~~~~

- **Git**: ソースコード管理
- **GitHub**: リポジトリのホスティング、Issue 管理、プルリクエスト

必要な知識
========

基礎知識
--------

|Fess| の開発には、以下の知識が必要です：

**必須**

- **Java プログラミング**: クラス、インターフェース、ジェネリクス、ラムダ式など
- **オブジェクト指向**: 継承、ポリモーフィズム、カプセル化
- **Maven**: 基本的なコマンドと pom.xml の理解
- **Git**: clone、commit、push、pull、branch、merge など

**推奨**

- **LastaFlute**: Action、Form、Service の概念
- **DBFlute**: Behavior、ConditionBean の使い方
- **OpenSearch/Elasticsearch**: インデックス、マッピング、クエリの基本
- **Web 開発**: HTML、CSS、JavaScript（特にフロントエンド開発の場合）
- **Linux コマンド**: サーバー環境での開発・デバッグ

学習リソース
----------

初めて |Fess| の開発に取り組む場合、以下のリソースが役立ちます：

公式ドキュメント
~~~~~~~~~~~~~~

- `Fess ユーザーマニュアル <https://fess.codelibs.org/ja/>`__
- `Fess 管理者ガイド <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

コミュニティ
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 質問や議論
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__: バグ報告や機能リクエスト
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 日本語コミュニティフォーラム

ソースコード
~~~~~~~~~~

実際のコードを読むことが最も効果的な学習方法です：

- まずは小さな機能から読み始める
- デバッガーを使ってコードの動作を追う
- 既存のテストコードを参照する

開発の基本フロー
==============

|Fess| の開発は、一般的に以下のような流れで進めます：

1. **Issue の確認・作成**

   GitHub の Issue を確認し、取り組む内容を決めます。
   新しい機能やバグ修正の場合は Issue を作成します。

2. **ブランチの作成**

   作業用のブランチを作成します：

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **コーディング**

   機能の実装やバグ修正を行います。

4. **テスト**

   単体テストを作成・実行し、変更が正しく動作することを確認します。

5. **コミット**

   変更をコミットします：

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **プルリクエスト**

   GitHub にプッシュし、プルリクエストを作成します：

   .. code-block:: bash

       git push origin feature/my-new-feature

詳細は :doc:`workflow` を参照してください。

プロジェクト構造の概要
==================

|Fess| のソースコードは、以下のような構造になっています：

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # Web アプリケーション層
    │   │   │       │   ├── web/       # 検索画面
    │   │   │       │   └── service/   # サービス層
    │   │   │       ├── crawler/       # クローラー機能
    │   │   │       ├── es/            # OpenSearch 関連
    │   │   │       ├── helper/        # ヘルパークラス
    │   │   │       ├── job/           # ジョブ処理
    │   │   │       ├── util/          # ユーティリティ
    │   │   │       └── FessBoot.java  # 起動クラス
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # JSP ファイル
    │   └── test/
    │       └── java/                  # テストコード
    ├── pom.xml                        # Maven 設定ファイル
    └── README.md

主要なパッケージ
--------------

app
~~~

Web アプリケーション層のコードです。
管理画面や検索画面の Action、Form、Service などが含まれます。

crawler
~~~~~~~

Web クローラー、ファイルクローラー、データストアクローラーなど、
データ収集機能のコードです。

es
~~

OpenSearch との連携コードです。
インデックス操作、検索クエリの構築などが含まれます。

helper
~~~~~~

アプリケーション全体で使用されるヘルパークラスです。

job
~~~

スケジュール実行されるジョブのコードです。
クロールジョブ、インデックス最適化ジョブなどが含まれます。

詳細は :doc:`architecture` を参照してください。

開発環境のクイックスタート
=======================

最小限の手順で開発環境をセットアップし、|Fess| を実行する方法を説明します。

前提条件
--------

- Java 21 以降がインストールされていること
- Git がインストールされていること
- Maven 3.x がインストールされていること

手順
----

1. **リポジトリのクローン**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **OpenSearch プラグインのダウンロード**

   .. code-block:: bash

       mvn antrun:run

3. **実行**

   Maven から実行：

   .. code-block:: bash

       mvn compile exec:java

   または、IDE（Eclipse、IntelliJ IDEA など）から ``org.codelibs.fess.FessBoot`` クラスを実行します。

4. **アクセス**

   ブラウザーで以下にアクセスします：

   - 検索画面: http://localhost:8080/
   - 管理画面: http://localhost:8080/admin/
     - デフォルトユーザー: admin / admin

詳細なセットアップ手順は :doc:`setup` を参照してください。

開発のヒント
==========

デバッグ実行
----------

IDE でデバッグ実行する場合、``FessBoot`` クラスを実行します。
ブレークポイントを設定することで、コードの動作を詳しく追跡できます。

ホットデプロイ
------------

LastaFlute は、一部の変更について再起動なしで反映できます。
ただし、クラス構造の変更などは再起動が必要です。

ログの確認
--------

ログは ``target/fess/logs/`` ディレクトリに出力されます。
問題が発生した場合は、ログファイルを確認してください。

OpenSearch の操作
----------------

組み込みの OpenSearch は ``target/fess/es/`` に配置されます。
直接 OpenSearch API を呼び出してデバッグすることも可能です：

.. code-block:: bash

    # インデックスの確認
    curl -X GET http://localhost:9201/_cat/indices?v

    # ドキュメントの検索
    curl -X GET http://localhost:9201/fess.search/_search?pretty

コミュニティとサポート
==================

質問や相談
--------

開発中に質問や相談がある場合は、以下を利用してください：

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 一般的な質問や議論
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__: バグ報告や機能リクエスト
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 日本語フォーラム

貢献方法
--------

|Fess| への貢献方法については、:doc:`contributing` を参照してください。

次のステップ
==========

開発環境をセットアップする準備ができたら、:doc:`setup` に進んでください。

詳細な情報については、以下のドキュメントも参照してください：

- :doc:`architecture` - アーキテクチャとコード構造
- :doc:`workflow` - 開発ワークフロー
- :doc:`building` - ビルドとテスト
- :doc:`contributing` - コントリビューションガイド

参考資料
========

公式リソース
----------

- `Fess 公式サイト <https://fess.codelibs.org/ja/>`__
- `GitHub リポジトリ <https://github.com/codelibs/fess>`__
- `ダウンロードページ <https://fess.codelibs.org/ja/downloads.html>`__

技術ドキュメント
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

コミュニティ
----------

- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
