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

開発環境
========

推奨環境
--------

- **JDK**: OpenJDK 21以上
- **IDE**: IntelliJ IDEA / Eclipse / VS Code
- **ビルドツール**: Maven 3.9以上
- **Git**: バージョン管理

セットアップ
------------

1. ソースコードの取得:

::

    git clone https://github.com/codelibs/fess.git
    cd fess

2. ビルド:

::

    mvn package -DskipTests

3. 開発サーバーの起動:

::

    ./bin/fess

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
     - DBFluteによるOpenSearch連携
   * - クローラー
     - fess-crawlerライブラリによるコンテンツ収集
   * - 検索エンジン
     - OpenSearchによる全文検索

主要フレームワーク
------------------

- **LastaFlute**: Webフレームワーク（アクション、フォーム、バリデーション）
- **DBFlute**: データアクセスフレームワーク（OpenSearch連携）
- **Lasta Di**: 依存性注入コンテナ

ディレクトリ構造
================

::

    fess/
    ├── src/main/java/org/codelibs/fess/
    │   ├── app/
    │   │   ├── web/         # コントローラー（Action）
    │   │   ├── service/     # サービス
    │   │   └── pager/       # ページネーション
    │   ├── api/             # REST API
    │   ├── helper/          # ヘルパークラス
    │   ├── crawler/         # クローラー関連
    │   ├── opensearch/      # OpenSearch連携（DBFlute生成）
    │   ├── llm/             # LLM統合
    │   └── ds/              # データストアコネクタ
    ├── src/main/resources/
    │   ├── fess_config.properties  # 設定
    │   └── fess_*.xml              # DI設定
    └── src/main/webapp/
        └── WEB-INF/view/    # JSPテンプレート

拡張ポイント
============

|Fess| は以下の拡張ポイントを提供しています:

プラグイン
----------

プラグインを使用して機能を追加できます。

- **データストアプラグイン**: 新しいデータソースからのクロール
- **スクリプトエンジンプラグイン**: 新しいスクリプト言語のサポート
- **Webアプリプラグイン**: Webインターフェースの拡張
- **Ingestプラグイン**: インデックス時のデータ加工

詳細: :doc:`plugin-architecture`

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

- ユニットテストを記述（``*Test.java``）
- 統合テストは ``*Tests.java``

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
