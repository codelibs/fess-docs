==================================
開発者ドキュメント概要
==================================

概要
====

このセクションでは、|Fess| の拡張開発について説明します。
プラグイン開発、カスタムコネクタの作成、テーマのカスタマイズなど、
|Fess| を拡張するための情報を提供します。

対象読者
========

- |Fess| のカスタム機能を開発したい開発者
- プラグインを作成したい開発者
- |Fess| のソースコードを理解したい開発者

前提知識
--------

- Java 21の基本的な知識
- Maven（ビルドシステム）の基本
- Webアプリケーション開発の経験
- OpenSearchの基本的な知識（|Fess| は検索エンジンとして OpenSearch を使用します）

開発環境
========

推奨環境
--------

- **JDK**: OpenJDK 21以上
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **ビルドツール**: Maven（ビルドで最小バージョンは強制されていませんが、Java 21 に対応する新しめの 3.x を推奨）
- **Git**: バージョン管理
- **OpenSearch**: 検索エンジンのバックエンド（IDEから起動する場合、必要なモジュールとプラグインはビルド時にダウンロードされます）

セットアップ
------------

|Fess| は Maven プロジェクトとしてビルドします。開発時は IDE から起動するのが最も簡単です。

1. ソースコードの取得:

   ::

       git clone https://github.com/codelibs/fess.git

2. IDEへのインポート:

   取得したディレクトリを Maven プロジェクトとして IDE にインポートします。

3. OpenSearch用モジュール・プラグインのダウンロード:

   初回のみ、以下のコマンドで検索エンジンのモジュールとプラグインを ``plugins`` ディレクトリに取得します。

   ::

       mvn antrun:run

4. 開発サーバーの起動（IDEから）:

   IDE上で ``org.codelibs.fess.FessBoot`` を実行またはデバッグ実行し、
   ブラウザで http://localhost:8080/ を開きます。
   管理画面は http://localhost:8080/admin/ （初期アカウント: ``admin`` / ``admin``）です。

5. パッケージのビルド（配布物の作成）:

   配布パッケージが必要な場合は ``package`` ゴールを実行します。
   成果物は ``target/releases`` に生成されます（ユニットテストを省略するには ``-DskipTests`` を付与）。

   ::

       mvn package

   生成された配布物を展開すると ``bin/fess`` 起動スクリプトが利用できます。

   ::

       unzip target/releases/fess-*.zip
       ./fess-*/bin/fess

.. note::

    ``bin/fess`` 起動スクリプトは配布パッケージ（zip/rpm/deb）に含まれるものです。
    ソースツリーで ``mvn package`` を実行しただけでは、リポジトリ直下に ``bin/fess`` は生成されません。
    ソースからの開発では、上記のように IDE で ``FessBoot`` を実行するか、
    展開した配布物の ``bin/fess`` を使用してください。

アーキテクチャ概要
==================

|Fess| は以下の主要コンポーネントで構成されています:

コンポーネント構成
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - コンポーネント
     - 説明
   * - Web層
     - LastaFluteフレームワークによるMVC実装
   * - サービス層
     - ビジネスロジック
   * - データアクセス層
     - DBFlute（ESFlute/FreeGen）による型安全なOpenSearchアクセス
   * - クローラー
     - fess-crawlerライブラリによるコンテンツ収集
   * - 検索エンジン
     - OpenSearchによる全文検索

主要フレームワーク
------------------

- **LastaFlute**: Webフレームワーク（アクション、フォーム、バリデーション）
- **DBFlute**: データアクセスフレームワーク。OpenSearch向けの型安全なアクセスクラス（``Bhv`` / ``ConditionBean``）は、
  DBFlute の FreeGen 機能と ESFlute テンプレートによって生成されます
  （再生成は ``mvn dbflute:freegen``）
- **Lasta Di**: 依存性注入コンテナ

ディレクトリ構造
================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # コントローラー（Action）
    │   │   ├── service/     # サービス
    │   │   ├── logic/       # ロジック
    │   │   └── pager/       # ページネーション
    │   ├── api/             # REST API（api/v2 など）
    │   ├── helper/          # ヘルパークラス
    │   ├── crawler/         # クローラー関連
    │   ├── indexer/         # インデックス処理
    │   ├── opensearch/      # OpenSearchアクセス（ESFlute/FreeGen生成）
    │   ├── llm/             # LLM統合
    │   ├── ds/              # データストアコネクタ
    │   ├── ingest/          # Ingest（インデックス時のデータ加工）
    │   ├── script/          # スクリプトエンジン
    │   ├── entity/          # エンティティ
    │   └── mylasta/         # LastaFlute設定（DI・メッセージ・型安全設定）
    ├── src/main/resources/
    │   ├── fess_config.properties  # 設定
    │   └── fess_*.xml              # DI設定（app.xml, fess_ds.xml など）
    └── src/main/webapp/
        └── WEB-INF/view/    # JSPテンプレート

拡張ポイント
============

|Fess| は以下の拡張ポイントを提供しています:

プラグイン
----------

プラグインを使用して機能を追加できます。

- **データストアプラグイン**: 新しいデータソースからのクロール（``AbstractDataStore`` を継承）
- **スクリプトエンジンプラグイン**: 新しいスクリプト言語のサポート（``ScriptEngine`` を実装）
- **Webアプリプラグイン**: Webインターフェースの拡張（Lasta Di のコンポーネント上書きとリソースのマージ）
- **Ingestプラグイン**: インデックス時のデータ加工（``Ingester`` を継承）

詳細: :doc:`plugin-architecture`

.. note::

    |Fess| 本体は ``war`` としてパッケージングされます。プラグインをローカルでビルドする際に、
    |Fess| を依存関係として解決できない場合は、``pom.xml`` の ``<packaging>`` を一時的に ``jar`` に変更して
    ``mvn clean install -DskipTests`` を実行し、その後 ``war`` に戻してください。

テーマ
------

検索画面のデザインをカスタマイズできます。

詳細: :doc:`theme-development`

設定
----

``fess_config.properties`` で多くの動作をカスタマイズできます。

詳細: :doc:`../config/intro`

プラグイン開発
==============

プラグイン開発の詳細については、以下を参照してください:

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`datastore-plugin` - データストアプラグイン開発
- :doc:`script-engine-plugin` - スクリプトエンジンプラグイン
- :doc:`webapp-plugin` - Webアプリプラグイン
- :doc:`ingest-plugin` - Ingestプラグイン

テーマ開発
==========

- :doc:`theme-development` - テーマのカスタマイズ

ベストプラクティス
==================

コーディング規約
----------------

- |Fess| の既存コードスタイルに従う
- ``mvn formatter:format`` でコードフォーマット
- ``mvn license:format`` でライセンスヘッダー追加

テスト
------

- ユニットテスト（``*Test.java``）: デフォルトの ``build`` プロファイルで ``mvn test`` として実行されます
- 統合テスト（``*Tests.java``）: ``mvn test -P integrationTests`` で実行されます。
  統合テストの実行には、稼働中の |Fess| サーバーと OpenSearch が必要です

ロギング
--------

- Log4j2を使用
- ``logger.debug()`` / ``logger.info()`` / ``logger.warn()`` / ``logger.error()``
- センシティブな情報はログに出力しない

リソース
========

- `GitHub Repository <https://github.com/codelibs/fess>`__
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__
- `Discussions <https://github.com/codelibs/fess/discussions>`__
