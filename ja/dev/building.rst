==============
ビルドとテスト
==============

このページでは、|Fess| のビルド方法、テスト方法、
配布パッケージの作成方法について説明します。

.. contents:: 目次
   :local:
   :depth: 2

ビルドシステムの概要
==================

|Fess| は Maven をビルドツールとして使用しています。
Maven は、依存関係の管理、コンパイル、テスト、パッケージングを自動化します。

pom.xml
-------

Maven の設定ファイルです。プロジェクトのルートディレクトリに配置されています。

主な設定内容：

- プロジェクト情報（groupId、artifactId、version）
- 依存ライブラリ
- ビルドプラグイン
- プロファイル

基本的なビルドコマンド
==================

クリーンビルド
------------

ビルド成果物を削除してから、再ビルドします：

.. code-block:: bash

    mvn clean compile

パッケージの作成
--------------

WAR ファイルと配布用 zip パッケージを作成します：

.. code-block:: bash

    mvn package

成果物は ``target/`` ディレクトリに生成されます：

.. code-block:: text

    target/
    ├── fess.war
    └── releases/
        └── fess-{version}.zip

フルビルド
--------

クリーン、コンパイル、テスト、パッケージをすべて実行します：

.. code-block:: bash

    mvn clean package

依存関係のダウンロード
--------------------

依存ライブラリをダウンロードします：

.. code-block:: bash

    mvn dependency:resolve

OpenSearch プラグインのダウンロード
---------------------------------

OpenSearch と必須プラグインをダウンロードします：

.. code-block:: bash

    mvn antrun:run

.. note::

   このコマンドは、開発環境のセットアップ時や
   プラグインを更新する際に実行します。

テスト
====

|Fess| では、JUnit を使用してテストを実装しています。

単体テストの実行
--------------

すべての単体テストを実行
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

特定のテストクラスを実行
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

特定のテストメソッドを実行
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

複数のテストクラスを実行
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

テストのスキップ
--------------

テストをスキップしてビルドする場合：

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   開発中はテストをスキップせず、必ず実行してください。
   PR を作成する前には、すべてのテストが通ることを確認してください。

統合テストの実行
--------------

統合テストには ``integrationTests`` プロファイルを使用します。
実行するには、|Fess| サーバーと OpenSearch が起動している必要があります：

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

.. note::

   統合テストのクラス名は ``*Tests.java`` パターンです（単体テストは ``*Test.java``）。

テストの書き方
============

単体テストの作成
--------------

テストクラスの配置
~~~~~~~~~~~~~~~~

テストクラスは ``src/test/java/`` 以下に配置します。
パッケージ構造は本体コードと同じにします。

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

テストクラスの基本構造
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: テストの前提条件
            SearchService service = new SearchService();
            String query = "test";

            // When: テスト対象の実行
            SearchResponse response = service.search(query);

            // Then: 結果の検証
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

テストのライフサイクル
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // すべてのテストの前に 1 回実行
        }

        @BeforeEach
        void setUp() {
            // 各テストの前に実行
        }

        @Test
        void testSomething() {
            // テスト
        }

        @AfterEach
        void tearDown() {
            // 各テストの後に実行
        }

        @AfterAll
        static void tearDownClass() {
            // すべてのテストの後に 1 回実行
        }
    }

アサーション
~~~~~~~~~~

JUnit 5 のアサーションを使用します：

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // 等価性
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // null チェック
    assertNull(obj);
    assertNotNull(obj);

    // 真偽値
    assertTrue(condition);
    assertFalse(condition);

    // 例外
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // コレクション
    assertIterableEquals(expectedList, actualList);

テストカバレッジ
--------------

JaCoCo でテストカバレッジを測定します：

.. code-block:: bash

    mvn clean test jacoco:report

レポートは ``target/site/jacoco/index.html`` に生成されます。

コードフォーマット
================

|Fess| では、コードの品質を維持するために以下のツールを使用しています。

コードフォーマッター
------------------

コーディングスタイルを統一します：

.. code-block:: bash

    mvn formatter:format

ライセンスヘッダー
----------------

ソースファイルにライセンスヘッダーを追加します：

.. code-block:: bash

    mvn license:format

コミット前のチェック
------------------

コミット前に両方を実行してください：

.. code-block:: bash

    mvn formatter:format
    mvn license:format

配布パッケージの作成
==================

zip パッケージの作成
------------------

配布用の zip パッケージを作成します：

.. code-block:: bash

    mvn clean package

生成される成果物：

.. code-block:: text

    target/releases/
    └── fess-{version}.zip

RPM パッケージの作成
------------------

.. code-block:: bash

    mvn rpm:rpm

DEB パッケージの作成
------------------

.. code-block:: bash

    mvn jdeb:jdeb

プロファイル
==========

Maven プロファイルを使用して、テストの種類を切り替えることができます。

build（デフォルト）
-----------------

デフォルトのプロファイルです。単体テスト（``*Test.java``）を実行します：

.. code-block:: bash

    mvn package

integrationTests
----------------

統合テスト（``*Tests.java``）を実行するためのプロファイルです：

.. code-block:: bash

    mvn test -P integrationTests \
        -Dtest.fess.url="http://localhost:8080" \
        -Dtest.search_engine.url="http://localhost:9201"

CI/CD
=====

|Fess| では、GitHub Actions を使用して CI/CD を実行しています。

GitHub Actions
-------------

``.github/workflows/`` ディレクトリに設定ファイルがあります。

自動実行されるチェック：

- ビルド
- 単体テスト
- パッケージの作成

ローカルでの CI チェック
-----------------------

PR を作成する前に、ローカルで CI と同様のチェックを実行できます：

.. code-block:: bash

    mvn clean package

トラブルシューティング
====================

ビルドエラー
----------

**エラー: 依存関係のダウンロード失敗**

.. code-block:: bash

    # Maven のローカルリポジトリをクリア
    rm -rf ~/.m2/repository
    mvn clean compile

**エラー: メモリ不足**

.. code-block:: bash

    # Maven のメモリを増やす
    export MAVEN_OPTS="-Xmx2g"
    mvn clean package

**エラー: Java バージョンが古い**

Java 21 以降を使用してください：

.. code-block:: bash

    java -version

テストエラー
----------

**テストがタイムアウトする**

テストのタイムアウト時間を延長：

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch が起動しない**

ポートを確認し、使用中の場合は変更します：

.. code-block:: bash

    lsof -i :9201

依存関係の問題
------------

**依存関係の競合**

依存関係ツリーを確認：

.. code-block:: bash

    mvn dependency:tree

特定の依存関係を除外：

.. code-block:: xml

    <dependency>
        <groupId>org.example</groupId>
        <artifactId>example-lib</artifactId>
        <version>1.0</version>
        <exclusions>
            <exclusion>
                <groupId>conflicting-lib</groupId>
                <artifactId>conflicting-lib</artifactId>
            </exclusion>
        </exclusions>
    </dependency>

ビルドのベストプラクティス
========================

定期的なクリーンビルド
--------------------

定期的にクリーンビルドを実行して、ビルドキャッシュの問題を回避します：

.. code-block:: bash

    mvn clean package

テストの実行
----------

コミット前に必ずテストを実行します：

.. code-block:: bash

    mvn test

コードフォーマットの実行
----------------------

PR を作成する前にコードフォーマットを実行します：

.. code-block:: bash

    mvn formatter:format
    mvn license:format

依存関係の更新
------------

定期的に依存関係を更新します：

.. code-block:: bash

    mvn versions:display-dependency-updates

ビルドキャッシュの活用
--------------------

ビルド時間を短縮するため、Maven のキャッシュを活用します：

.. code-block:: bash

    # 既にコンパイル済みの場合はスキップ
    mvn compile

Maven コマンドリファレンス
========================

よく使うコマンド
--------------

.. code-block:: bash

    # クリーン
    mvn clean

    # コンパイル
    mvn compile

    # テスト
    mvn test

    # パッケージ
    mvn package

    # インストール（ローカルリポジトリに登録）
    mvn install

    # 検証（統合テストを含む）
    mvn verify

    # 依存関係の解決
    mvn dependency:resolve

    # 依存関係ツリーの表示
    mvn dependency:tree

    # プロジェクト情報の表示
    mvn help:effective-pom

    # コードフォーマット
    mvn formatter:format

    # ライセンスヘッダー追加
    mvn license:format

次のステップ
==========

ビルドとテストの方法を理解したら、以下のドキュメントを参照してください：

- :doc:`workflow` - 開発ワークフロー
- :doc:`contributing` - コントリビューションガイドライン
- :doc:`architecture` - コードベースの理解

参考資料
======

- `Maven 公式ドキュメント <https://maven.apache.org/guides/>`__
- `JUnit 5 ユーザーガイド <https://junit.org/junit5/docs/current/user-guide/>`__
- `JaCoCo ドキュメント <https://www.jacoco.org/jacoco/trunk/doc/>`__
