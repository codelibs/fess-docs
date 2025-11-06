====================
開発環境のセットアップ
====================

このページでは、|Fess| の開発環境を構築する手順を詳しく説明します。
IDE の選択から、ソースコードの取得、実行、デバッグまで、
ステップバイステップで解説します。

.. contents:: 目次
   :local:
   :depth: 2

システム要件
==========

開発環境には、以下のハードウェア要件を推奨します。

ハードウェア要件
--------------

- **CPU**: 4コア以上
- **メモリ**: 8GB 以上（16GB を推奨）
- **ディスク**: 20GB 以上の空き容量

.. note::

   開発中は |Fess| 本体と組み込みの OpenSearch が同時に動作するため、
   十分なメモリとディスク容量を確保してください。

ソフトウェア要件
--------------

- **OS**: Windows 10/11、macOS 11 以降、Linux（Ubuntu 20.04 以降など）
- **Java**: JDK 21 以降
- **Maven**: 3.x 以降
- **Git**: 2.x 以降
- **IDE**: Eclipse、IntelliJ IDEA、VS Code など

必須ソフトウェアのインストール
==========================

Java のインストール
-----------------

|Fess| の開発には Java 21 以降が必要です。

Eclipse Temurin のインストール（推奨）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Eclipse Temurin（旧 AdoptOpenJDK）を推奨します。

1. `Adoptium <https://adoptium.net/temurin/releases/>`__ にアクセス
2. Java 21 の LTS 版をダウンロード
3. インストーラーの指示に従ってインストール

インストール確認
~~~~~~~~~~~~~~

ターミナルまたはコマンドプロンプトで以下を実行：

.. code-block:: bash

    java -version

以下のような出力が表示されれば成功です：

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

環境変数の設定
~~~~~~~~~~~~

**Linux/macOS:**

``~/.bashrc`` または ``~/.zshrc`` に以下を追加：

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. 「システム環境変数の編集」を開く
2. 「環境変数」をクリック
3. ``JAVA_HOME`` を追加：``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. ``PATH`` に ``%JAVA_HOME%\bin`` を追加

Maven のインストール
------------------

Maven 3.x 以降をインストールします。

ダウンロードとインストール
~~~~~~~~~~~~~~~~~~~~~~~~

1. `Maven ダウンロードページ <https://maven.apache.org/download.cgi>`__ にアクセス
2. Binary zip/tar.gz archive をダウンロード
3. 解凍して適切な場所に配置

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. ZIP ファイルを解凍
2. ``C:\Program Files\Apache\maven`` などに配置

環境変数の設定
~~~~~~~~~~~~

**Linux/macOS:**

``~/.bashrc`` または ``~/.zshrc`` に以下を追加：

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. ``MAVEN_HOME`` を追加：``C:\Program Files\Apache\maven``
2. ``PATH`` に ``%MAVEN_HOME%\bin`` を追加

インストール確認
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

以下のような出力が表示されれば成功です：

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Git のインストール
----------------

Git がインストールされていない場合は、以下からインストールします。

- **Windows**: `Git for Windows <https://git-scm.com/download/win>`__
- **macOS**: ``brew install git`` または `Git ダウンロードページ <https://git-scm.com/download/mac>`__
- **Linux**: ``sudo apt install git`` (Ubuntu/Debian) または ``sudo yum install git`` (RHEL/CentOS)

インストール確認：

.. code-block:: bash

    git --version

IDE のセットアップ
===============

Eclipse の場合
------------

Eclipse は |Fess| の公式ドキュメントで推奨されている IDE です。

Eclipse のインストール
~~~~~~~~~~~~~~~~~~~~

1. `Eclipse ダウンロードページ <https://www.eclipse.org/downloads/>`__ にアクセス
2. "Eclipse IDE for Enterprise Java and Web Developers" をダウンロード
3. インストーラーを実行し、指示に従ってインストール

推奨プラグイン
~~~~~~~~~~~~

Eclipse には以下のプラグインがデフォルトで含まれています：

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

プロジェクトのインポート
~~~~~~~~~~~~~~~~~~~~

1. Eclipse を起動
2. ``File`` > ``Import`` を選択
3. ``Maven`` > ``Existing Maven Projects`` を選択
4. Fess のソースコードディレクトリを指定
5. ``Finish`` をクリック

実行構成の設定
~~~~~~~~~~~~

1. ``Run`` > ``Run Configurations...`` を選択
2. ``Java Application`` を右クリックして ``New Configuration`` を選択
3. 以下を設定：

   - **Name**: Fess Boot
   - **Project**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``

4. ``Apply`` をクリック

IntelliJ IDEA の場合
-------------------

IntelliJ IDEA も広く使用されている IDE です。

IntelliJ IDEA のインストール
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. `IntelliJ IDEA ダウンロードページ <https://www.jetbrains.com/idea/download/>`__ にアクセス
2. Community Edition（無料）または Ultimate Edition をダウンロード
3. インストーラーを実行し、指示に従ってインストール

プロジェクトのインポート
~~~~~~~~~~~~~~~~~~~~

1. IntelliJ IDEA を起動
2. ``Open`` を選択
3. Fess のソースコードディレクトリの ``pom.xml`` を選択
4. ``Open as Project`` をクリック
5. Maven プロジェクトとして自動的にインポートされます

実行構成の設定
~~~~~~~~~~~~

1. ``Run`` > ``Edit Configurations...`` を選択
2. ``+`` ボタンをクリックして ``Application`` を選択
3. 以下を設定：

   - **Name**: Fess Boot
   - **Module**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``
   - **JRE**: Java 21

4. ``OK`` をクリック

VS Code の場合
------------

軽量な開発環境を好む場合は、VS Code も選択肢です。

VS Code のインストール
~~~~~~~~~~~~~~~~~~~~

1. `VS Code ダウンロードページ <https://code.visualstudio.com/>`__ にアクセス
2. インストーラーをダウンロードして実行

必要な拡張機能のインストール
~~~~~~~~~~~~~~~~~~~~~~~~

以下の拡張機能をインストールします：

- **Extension Pack for Java**: Java 開発に必要な拡張機能のセット
- **Maven for Java**: Maven サポート

プロジェクトを開く
~~~~~~~~~~~~~~~~

1. VS Code を起動
2. ``File`` > ``Open Folder`` を選択
3. Fess のソースコードディレクトリを選択

ソースコードの取得
==============

GitHub からのクローン
-------------------

|Fess| のソースコードを GitHub からクローンします。

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

SSH を使用する場合：

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   フォークして開発する場合は、まず GitHub で Fess リポジトリをフォークし、
   フォークしたリポジトリをクローンします：

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

プロジェクトのビルド
==================

OpenSearch プラグインのダウンロード
---------------------------------

Fess の実行には、OpenSearch 用のプラグインが必要です。
以下のコマンドでダウンロードします：

.. code-block:: bash

    mvn antrun:run

このコマンドは以下を実行します：

- OpenSearch のダウンロード
- 必須プラグインのダウンロードとインストール
- OpenSearch の設定

.. note::

   このコマンドは初回のみ、またはプラグインを更新する際に実行します。
   毎回実行する必要はありません。

初回ビルド
--------

プロジェクトをビルドします：

.. code-block:: bash

    mvn clean compile

初回ビルドには時間がかかる場合があります（依存ライブラリのダウンロードなど）。

ビルドが成功すると、以下のようなメッセージが表示されます：

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Fess の実行
==========

コマンドラインからの実行
--------------------

Maven を使用して実行：

.. code-block:: bash

    mvn compile exec:java

または、パッケージ化してから実行：

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

IDE からの実行
------------

Eclipse の場合
~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` クラスを右クリック
2. ``Run As`` > ``Java Application`` を選択

または、作成した実行構成を使用：

1. ツールバーの実行ボタンのドロップダウンをクリック
2. ``Fess Boot`` を選択

IntelliJ IDEA の場合
~~~~~~~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` クラスを右クリック
2. ``Run 'FessBoot.main()'`` を選択

または、作成した実行構成を使用：

1. ツールバーの実行ボタンのドロップダウンをクリック
2. ``Fess Boot`` を選択

VS Code の場合
~~~~~~~~~~~~

1. ``src/main/java/org/codelibs/fess/FessBoot.java`` を開く
2. ``Run`` メニューから ``Run Without Debugging`` を選択

起動の確認
--------

Fess の起動には 1〜2 分かかります。
コンソールに以下のようなログが表示されれば起動完了です：

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

ブラウザーで以下にアクセスして動作を確認：

- **検索画面**: http://localhost:8080/
- **管理画面**: http://localhost:8080/admin/

  - デフォルトユーザー: ``admin``
  - デフォルトパスワード: ``admin``

ポート番号の変更
--------------

デフォルトのポート 8080 が使用中の場合、以下のファイルで変更できます：

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # ポート番号を変更
    server.port=8080

デバッグ実行
==========

IDE でのデバッグ実行
------------------

Eclipse の場合
~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` クラスを右クリック
2. ``Debug As`` > ``Java Application`` を選択
3. ブレークポイントを設定して、コードの動作を追跡

IntelliJ IDEA の場合
~~~~~~~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` クラスを右クリック
2. ``Debug 'FessBoot.main()'`` を選択
3. ブレークポイントを設定して、コードの動作を追跡

VS Code の場合
~~~~~~~~~~~~

1. ``src/main/java/org/codelibs/fess/FessBoot.java`` を開く
2. ``Run`` メニューから ``Start Debugging`` を選択

リモートデバッグ
--------------

コマンドラインから起動した Fess にデバッガーを接続することもできます。

Fess をデバッグモードで起動：

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

IDE からリモートデバッグ接続：

**Eclipse:**

1. ``Run`` > ``Debug Configurations...`` を選択
2. ``Remote Java Application`` を右クリックして ``New Configuration`` を選択
3. ``Port: 5005`` を設定
4. ``Debug`` をクリック

**IntelliJ IDEA:**

1. ``Run`` > ``Edit Configurations...`` を選択
2. ``+`` > ``Remote JVM Debug`` を選択
3. ``Port: 5005`` を設定
4. ``OK`` をクリックして ``Debug`` を実行

開発に役立つ設定
==============

ログレベルの変更
--------------

デバッグ時にログレベルを変更すると、詳細な情報を確認できます。

``src/main/resources/log4j2.xml`` を編集：

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

ホットデプロイの有効化
-------------------

LastaFlute は、一部の変更について再起動なしで反映できます。

``src/main/resources/fess_config.properties`` で以下を設定：

.. code-block:: properties

    # ホットデプロイを有効化
    development.here=true

ただし、以下の変更は再起動が必要です：

- クラス構造の変更（メソッドの追加・削除など）
- 設定ファイルの変更
- 依存ライブラリの変更

組み込み OpenSearch の操作
------------------------

開発環境では、組み込みの OpenSearch が使用されます。

OpenSearch の配置場所：

.. code-block:: text

    target/fess/es/

OpenSearch API への直接アクセス：

.. code-block:: bash

    # インデックスの一覧
    curl -X GET http://localhost:9201/_cat/indices?v

    # ドキュメントの検索
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # マッピングの確認
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

外部 OpenSearch の使用
--------------------

外部の OpenSearch サーバーを使用する場合は、
``src/main/resources/fess_config.properties`` を編集：

.. code-block:: properties

    # 組み込み OpenSearch を無効化
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

DBFlute によるコード生成
======================

|Fess| は、DBFlute を使用して OpenSearch のスキーマから
Java コードを自動生成しています。

スキーマが変更された場合の再生成
----------------------------

OpenSearch のマッピングを変更した場合、以下のコマンドで
対応する Java コードを再生成します：

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

各コマンドの説明：

- ``rm -rf mydbflute``: 既存の DBFlute 作業ディレクトリを削除
- ``mvn antrun:run``: OpenSearch プラグインをダウンロード
- ``mvn dbflute:freegen``: スキーマから Java コードを生成
- ``mvn license:format``: ライセンスヘッダーを追加

トラブルシューティング
==================

ビルドエラー
----------

**エラー: Java バージョンが古い**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

解決方法：Java 21 以降をインストールし、``JAVA_HOME`` を適切に設定してください。

**エラー: 依存ライブラリのダウンロード失敗**

.. code-block:: text

    [ERROR] Failed to collect dependencies

解決方法：ネットワーク接続を確認し、Maven のローカルリポジトリをクリアしてから再試行：

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

実行エラー
--------

**エラー: ポート 8080 がすでに使用されている**

.. code-block:: text

    Address already in use

解決方法：

1. ポート 8080 を使用しているプロセスを終了
2. または、``fess_config.properties`` でポート番号を変更

**エラー: OpenSearch が起動しない**

ログファイル ``target/fess/es/logs/`` を確認してください。

よくある原因：

- メモリ不足：JVM ヒープサイズを増やす
- ポート 9201 が使用中：ポート番号を変更
- ディスク容量不足：ディスク容量を確保

IDE でプロジェクトが認識されない
----------------------------

**Maven プロジェクトの更新**

- **Eclipse**: プロジェクトを右クリック > ``Maven`` > ``Update Project``
- **IntelliJ IDEA**: ``Maven`` ツールウィンドウで ``Reload All Maven Projects`` をクリック
- **VS Code**: コマンドパレットから ``Java: Clean Java Language Server Workspace`` を実行

次のステップ
==========

開発環境のセットアップが完了したら、以下のドキュメントを参照してください：

- :doc:`architecture` - コード構造の理解
- :doc:`workflow` - 開発ワークフローの学習
- :doc:`building` - ビルドとテストの方法
- :doc:`contributing` - プルリクエストの作成

リソース
========

- `Eclipse ダウンロード <https://www.eclipse.org/downloads/>`__
- `IntelliJ IDEA ダウンロード <https://www.jetbrains.com/idea/download/>`__
- `VS Code ダウンロード <https://code.visualstudio.com/>`__
- `Maven ドキュメント <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
