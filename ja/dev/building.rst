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

実行可能な JAR ファイルを作成します：

.. code-block:: bash

    mvn package

成果物は ``target/`` ディレクトリに生成されます：

.. code-block:: text

    target/
    ├── fess-15.3.x.jar
    └── fess-15.3.x/

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

統合テストを含むすべてのテストを実行します：

.. code-block:: bash

    mvn verify

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

モックの使用
~~~~~~~~~~

Mockito を使用してモックを作成します：

.. code-block:: java

    import static org.mockito.Mockito.*;
    import org.mockito.Mock;
    import org.mockito.junit.jupiter.MockitoExtension;
    import org.junit.jupiter.api.extension.ExtendWith;

    @ExtendWith(MockitoExtension.class)
    public class SearchServiceTest {

        @Mock
        private SearchEngineClient searchEngineClient;

        @Test
        public void testSearch() {
            // モックの設定
            when(searchEngineClient.search(anyString()))
                .thenReturn(new SearchResponse());

            // テスト実行
            SearchService service = new SearchService();
            service.setSearchEngineClient(searchEngineClient);
            SearchResponse response = service.search("test");

            // 検証
            assertNotNull(response);
            verify(searchEngineClient, times(1)).search("test");
        }
    }

テストカバレッジ
--------------

JaCoCo でテストカバレッジを測定します：

.. code-block:: bash

    mvn clean test jacoco:report

レポートは ``target/site/jacoco/index.html`` に生成されます。

コード品質チェック
================

Checkstyle
----------

コーディングスタイルをチェックします：

.. code-block:: bash

    mvn checkstyle:check

設定ファイルは ``checkstyle.xml`` にあります。

SpotBugs
--------

潜在的なバグを検出します：

.. code-block:: bash

    mvn spotbugs:check

PMD
---

コード品質の問題を検出します：

.. code-block:: bash

    mvn pmd:check

すべてのチェックを実行
--------------------

.. code-block:: bash

    mvn clean verify checkstyle:check spotbugs:check pmd:check

配布パッケージの作成
==================

リリースパッケージの作成
--------------------

配布用のパッケージを作成します：

.. code-block:: bash

    mvn clean package

生成される成果物：

.. code-block:: text

    target/releases/
    ├── fess-15.3.x.tar.gz      # Linux/macOS 用
    ├── fess-15.3.x.zip         # Windows 用
    ├── fess-15.3.x.rpm         # RPM パッケージ
    └── fess-15.3.x.deb         # DEB パッケージ

Docker イメージの作成
-------------------

Docker イメージを作成します：

.. code-block:: bash

    mvn package docker:build

生成されるイメージ：

.. code-block:: bash

    docker images | grep fess

プロファイル
==========

Maven プロファイルを使用して、環境ごとに異なる設定を適用できます。

開発プロファイル
--------------

開発用の設定でビルドします：

.. code-block:: bash

    mvn package -Pdev

本番プロファイル
--------------

本番用の設定でビルドします：

.. code-block:: bash

    mvn package -Pprod

高速ビルド
--------

テストとチェックをスキップして高速にビルドします：

.. code-block:: bash

    mvn package -Pfast

.. warning::

   高速ビルドは開発中の確認用です。
   PR を作成する前には、必ずフルビルドを実行してください。

CI/CD
=====

|Fess| では、GitHub Actions を使用して CI/CD を実行しています。

GitHub Actions
-------------

``.github/workflows/`` ディレクトリに設定ファイルがあります。

自動実行されるチェック：

- ビルド
- 単体テスト
- 統合テスト
- コードスタイルチェック
- コード品質チェック

ローカルでの CI チェック
-----------------------

PR を作成する前に、ローカルで CI と同様のチェックを実行できます：

.. code-block:: bash

    mvn clean verify checkstyle:check

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
    export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512m"
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

コード品質のチェック
------------------

PR を作成する前にコード品質をチェックします：

.. code-block:: bash

    mvn checkstyle:check spotbugs:check

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
- `Mockito ドキュメント <https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html>`__
- `JaCoCo ドキュメント <https://www.jacoco.org/jacoco/trunk/doc/>`__
