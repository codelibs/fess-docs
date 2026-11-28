============================
プラグインで Fess を拡張する
============================

はじめに
========

社内の独自システムに合う ``fess-ds-*`` プラグインがない場合や、すべての文書を登録前に加工したい場合は、自分でプラグインを作ります。
本記事は Java 開発者向けに、Fess 15.9 で動くプラグインを公式のテンプレートから作り、インストールして動作を確かめるまでを説明します。

この記事の手順をそのまま実行すると、次のことができるようになります。

- プラグインの種類と、Fess がそれを見分ける仕組みを理解する
- ``fess-ds-example`` をもとにデータストアプラグインをビルドし、Fess に組み込んで文書を登録する
- ``fess-ingest-example`` をもとに、登録前の文書を加工する Ingester を作る

前提として、Java 21 以降と Maven 3 が使えること、Fess 15.9 が動いていること（:doc:`guide-02`）を想定します。
データストア設定の画面の使い方は :doc:`datastore-basics` で説明しているので、先に読んでおくと手順が追いやすくなります。

プラグインの種類
================

プラグインは jar ファイルで、Fess のインストールディレクトリの ``app/WEB-INF/plugin/`` に置かれます。
Fess は jar のファイル名の先頭（プレフィックス）でプラグインの種類を判別します（``PluginHelper.ArtifactType``）。
15.9 の種類は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 22 43 35

   * - プレフィックス
     - 役割
     - 参考になるリポジトリ
   * - ``fess-ds``
     - データストア。外部システムからレコードを取得して登録する
     - ``fess-ds-example``
   * - ``fess-ingest``
     - Ingester。登録前の文書を加工する
     - ``fess-ingest-example``
   * - ``fess-script``
     - スクリプトエンジン
     - ``fess-script-groovy``
   * - ``fess-webapp``
     - Web アプリの拡張（API やエンドポイントの追加）
     - ``fess-webapp-mcp``
   * - ``fess-thumbnail``
     - サムネイル生成
     - ``fess-thumbnail-playwright``
   * - ``fess-crawler``
     - クローラーのクライアント
     - ``fess-crawler-playwright``
   * - ``fess-llm``
     - AI 検索モードで使う LLM プロバイダー
     - ``fess-llm-openai``
   * - ``fess-storage``
     - オブジェクトストレージ（S3 / GCS）
     - ``fess-storage-s3``
   * - ``fess-sso``
     - シングルサインオンの認証方式
     - ``fess-sso-oidc``

どのリポジトリも https://github.com/codelibs で公開されています。

検索画面のデザインはプラグインでは変えません。
JSP を差し替える ``fess-theme-*`` の JAR テーマプラグインは 15.9 で削除され、検索画面は ``theme.yml``・``index.html``・``assets/`` からなる ZIP のテーマになりました。
テーマは［システム］>［テーマ］からアップロードします。
作り方は `テーマ開発ガイド <https://fess.codelibs.org/ja/stable/dev/theme-development.html>`__ を、既存サイトへの組み込みは :doc:`guide-03` を参照してください。

データストアプラグインを作る
============================

テンプレートを取得する
----------------------

``fess-ds-example`` は、データストアプラグインのひな形として公開されているリポジトリです。
既定ブランチは開発中の版（15.10.0-SNAPSHOT）に合わせてあるため、15.9 向けにビルドするには 15.9.0 に合わせたコミットを使います。

::

    $ git clone https://github.com/codelibs/fess-ds-example.git
    $ cd fess-ds-example
    $ git checkout 0252a8b08d7de4eeea7a88c52aa884094ef099be

このコミットと既定ブランチの違いは ``pom.xml`` の 2 行（プロジェクトと親 POM のバージョン）だけです。
既定ブランチのまま、次の節の 2 か所を 15.9 向けに書き換えても同じ結果になります。

pom.xml
-------

``pom.xml`` の要点は次の部分です。

.. code-block:: xml

    <artifactId>fess-ds-example</artifactId>
    <packaging>jar</packaging>
    <version>15.9.0-SNAPSHOT</version>

    <parent>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-parent</artifactId>
        <version>15.9.0</version>
        <relativePath />
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess</artifactId>
            <version>${fess.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>org.opensearch</groupId>
            <artifactId>opensearch</artifactId>
            <version>${opensearch.version}</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

``fess-parent`` のバージョンは、プラグインを入れる Fess のバージョンに合わせます。
``fess-parent`` 15.9.0 では ``fess.version`` が ``15.9.0`` なので、Fess 15.9.0 の API に対してコンパイルされます。
Fess 本体と OpenSearch のクラスは実行時に Fess が持っているため、``provided`` にします。
実際の ``pom.xml`` にはこのほかの依存関係とビルド設定もあるので、まずはそのまま使ってください。
``fess`` の jar は Maven Central ではなく、``fess-parent`` が宣言している CodeLibs のリポジトリ（``https://maven.codelibs.org/release/``）から取得されます。
プロキシやミラーを使う環境では、このリポジトリに到達できるようにしておきます。

自分のプラグインにするときは、``artifactId`` を必ず ``fess-ds-`` で始めます。
後で説明するとおり、管理画面の「ハンドラー名」の候補は、ファイル名が ``fess-ds`` で始まる jar からしか集められません。

データストアクラス
------------------

データストアは ``org.codelibs.fess.ds.AbstractDataStore`` を継承し、``getName()`` と ``storeData(...)`` を実装します。
次は ``ExampleDataStore`` から、処理の骨格だけを残したものです。
これは仕組みを理解するためのもので、ビルドにはリポジトリの ``ExampleDataStore`` をそのまま使います（テストが骨格にないメソッドを使っているため、置き換えるとテストのコンパイルが通りません）。

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.HashMap;
    import java.util.LinkedHashMap;
    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback, final DataStoreParams paramMap,
                final Map<String, String> scriptMap, final Map<String, Object> defaultDataMap) {
            final String scriptType = getScriptType(paramMap);
            final int dataSize = Integer.parseInt(paramMap.getAsString("data.size", "10"));

            for (int i = 0; i < dataSize && alive; i++) {
                // 外部システムから取得した 1 件分のレコード（ここでは固定値）
                final Map<String, Object> source = new HashMap<>();
                source.put("title", "Sample " + i);
                source.put("body", "Sample body text for record " + i);
                source.put("url", "http://fess.codelibs.org/?sample=" + i);

                // スクリプトは「パラメーター + レコード」に対して評価される
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(source);

                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }
                callback.store(paramMap, dataMap);
            }
        }
    }

各部分の役割は次のとおりです。

- ``getName()`` の戻り値が、このデータストアの名前として ``DataStoreFactory`` に登録されます。クラスの単純名を返すのが慣例です
- ``paramMap`` には、データストア設定の「パラメーター」欄の値が入っています。``getAsString(キー, 既定値)`` で取り出します
- ``scriptMap`` は「スクリプト」欄の ``フィールド名=式`` の各行です。``convertValue()`` が式を評価し、その結果をインデックスのフィールドに入れます
- ``defaultDataMap`` には、設定 ID・パーミッション（ロール）・ブースト値・仮想ホストなど、データストア設定から決まる値が入っています。これをコピーしてから各フィールドを足します
- ``callback.store()`` で 1 件ずつ登録します。``alive`` はジョブが停止されると ``false`` になるので、ループの条件に入れておきます

つまり、どのレコードの値をどのフィールドに入れるかはプラグインには書かず、管理者が「スクリプト」欄で決めます。
プラグインの役目は、レコードを取得して ``resultMap`` に並べることです。

実際の ``ExampleDataStore`` は、このほかにレコード単位の例外処理（［障害URL］への記録）とクロール統計（``CrawlerStatsHelper``）を実装しています。
自分のプラグインを作るときは、こちらの骨格ではなく ``ExampleDataStore`` をコピーし、``// CUSTOMIZE:`` と書かれた箇所（レコードの取得部分）を書き換えてください。

DI 設定ファイル
---------------

クラスを作っただけでは Fess に読み込まれません。
``src/main/resources/fess_ds++.xml`` にコンポーネントとして登録します。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

DI コンテナ（Lasta Di）は、クラスパス上の ``fess_ds++.xml`` を Fess 本体の ``fess_ds.xml`` に取り込みます。
``<postConstruct name="register">`` により、生成後に ``AbstractDataStore.register()`` が呼ばれ、``getName()`` の名前で登録されます。
クラス名やパッケージを変えたら、``class`` 属性も合わせて変えます。

ビルドする
----------

::

    $ mvn clean package

``target/`` に 3 つの jar ができます。
Fess に入れるのは、``-sources`` や ``-javadoc`` が付かない ``fess-ds-example-15.9.0-SNAPSHOT.jar`` です。
中に ``fess_ds++.xml`` と ``ExampleDataStore.class`` が入っていることは ``unzip -l`` で確認できます。

インストールする
================

管理画面から入れるのが手軽です。

1. ［システム］>［プラグイン］で［インストール］をクリックします
2. ［リモート］タブのプルダウンは先頭の ``-`` のままにします。ほかのプラグインを選んでいると、そちらがインストールされます
3. ［ローカル］タブの「Jarファイル」でビルドした jar を選び、［インストール］をクリックします
4. Fess を再起動します

アップロードした jar は ``app/WEB-INF/plugin/`` に ``<名前>-<バージョン>.jar`` の形で保存されます。
ファイル名から名前とバージョンを読み取るので、Maven が付けたファイル名を変えずにアップロードしてください。
管理画面を使わずに、jar をこのディレクトリへ直接コピーして再起動しても同じです（Docker イメージでは ``/usr/share/fess/app/WEB-INF/plugin/``）。

Docker の場合、``FESS_PLUGINS`` はリポジトリに公開されたプラグインを取得する仕組みなので、自作の jar には使えません。
管理画面から入れたうえで ``docker compose -f compose.yaml -f compose-opensearch3.yaml restart fess01`` で再起動します。
jar はコンテナ内に置かれるため、``down`` と ``up`` でコンテナを作り直すと消えます。
その場合は入れ直してください。

動作を確かめる
==============

ハンドラー名を確認する
----------------------

再起動後、［クローラー］>［データストア］>［新規作成］を開き、「ハンドラー名」のプルダウンに ``ExampleDataStore`` があることを確認します。
この候補は、``app/WEB-INF/plugin/`` にある、ファイル名が ``fess-ds`` で始まる jar から作られます。
jar の中の ``fess_ds++.xml`` を読み、``class`` 属性に書かれたクラスの単純名を候補にします（60 秒間キャッシュされます）。
表示されない場合は、jar のファイル名、jar の中の ``fess_ds++.xml``、再起動したかどうかを確認してください。

データストア設定を作る
----------------------

同じ画面で次のように入力し、［作成］をクリックします。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 値
   * - 名前
     - ``Example``
   * - ハンドラー名
     - ``ExampleDataStore``
   * - パラメーター
     - 入力済みの ``script_type=javascript`` の次の行に ``data.size=5`` を足す
   * - スクリプト
     - ``title=title``、``content=body``、``url=url`` の 3 行

スクリプトの右辺がレコードのキー（``title``、``body``、``url``）と一致する場合、``convertValue()`` はスクリプトエンジンを使わずにその値をそのまま返します。
``content=title + " " + body`` のような式を書くと、``script_type`` で指定したエンジンで評価されます。
``script_type`` を消すと ``groovy`` として扱われ、``fess-script-groovy`` が入っていない環境では式の評価に失敗するので、消さずに残してください。

``url`` は必須です。
``callback.store()`` は ``url`` のない文書を受け付けず、例外を投げます。

ジョブを実行する
----------------

1. ［クローラー］>［データストア］の一覧で ``Example`` をクリックし、［新しいジョブの作成］をクリックします
2. スケジューラの作成画面が開くので、そのまま［作成］をクリックします
3. ［システム］>［スケジューラ］で作成したジョブを開き、［今すぐ開始］をクリックします

結果を確認する
--------------

次の 4 点を確認します。

1. ［システム情報］>［ジョブログ］で、ジョブの状態が「OK」になっている
2. ［システム情報］>［クロール情報］で、そのセッションの「インデックスのサイズ (データストア)」が ``5`` になっている
3. ［システム情報］>［障害URL］に記録がない
4. ［システム情報］>［検索］で ``Sample`` を検索すると、``Sample 0`` から ``Sample 4`` の 5 件が表示される

ジョブの状態が「OK」でも、データストアの処理が成功したとは限りません。
例えばスクリプトから ``url=url`` を消して実行すると、``callback.store()`` が全レコードで例外を投げ、登録は 0 件になります。
``ExampleDataStore`` はレコード単位で例外を捕まえるので、［障害URL］に ``record:0`` から ``record:4`` が記録され、``fess-crawler.log`` に WARN が出ますが、ジョブログは「OK」のままです。
例外を捕まえない骨格のようなコードでは、設定全体が失敗し、［障害URL］に ``D<設定ID>:Example`` の形で 1 件だけ記録されます。
確認の手順とログの場所は :doc:`datastore-basics` の「結果を確かめる」にまとめています。

ここまで確認できたら、``createSourceRecord()`` などのレコード取得部分を、実際の API やファイルを読む処理に置き換えていきます。
外部システムの接続先や認証情報は、コードに書かずに「パラメーター」欄から ``paramMap`` で受け取るようにします。

テンプレートの ``src/test`` には、UTFlute の ``LastaDiTestCase`` を使ったテストがあります。
``IndexUpdateCallback`` を実装したテスト用クラスで ``store()`` に渡された ``dataMap`` を集め、件数やフィールドの値を確かめます。
そのため、OpenSearch なしで ``mvn test`` を実行できます。
レコード取得部分を書き換えたら、このテストも合わせて直してください。

Ingester で登録前の文書を加工する
=================================

Ingester は、データストア・ウェブ・ファイルシステムのどのクロールでも、文書をインデックスに送る直前に呼び出されます。
すべての文書に共通のフィールドを足す、値を正規化する、といった処理に使います。
設定ごとに有効・無効を切り替える仕組みはなく、インストールすると全クロールに適用されます。

``org.codelibs.fess.ingest.Ingester`` を継承し、必要な ``process`` メソッドだけをオーバーライドします。

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - メソッド
     - 呼び出される場面
   * - ``process(Map<String, Object> target, DataStoreParams params)``
     - データストアのクロール（``callback.store()`` の中）
   * - ``process(Map<String, Object> target, AccessResult<String> accessResult)``
     - ウェブ・ファイルクロールのインデックス登録時
   * - ``process(ResultData target, ResponseData responseData)``
     - ウェブ・ファイルクロールで取得した応答の処理時
   * - ``protected process(Map<String, Object> target)``
     - 上の 2 つの ``Map`` 版が既定で呼ぶメソッド。データストアとウェブ・ファイルの両方に効かせたいときはこれだけをオーバーライドする

次は ``fess-ingest-example`` の ``ExampleIngester`` から、データストア向けの処理だけを残したものです。

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.apache.logging.log4j.LogManager;
    import org.apache.logging.log4j.Logger;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {
        private static final Logger logger = LogManager.getLogger(ExampleIngester.class);

        public ExampleIngester() {
            setPriority(50);
        }

        @Override
        public Map<String, Object> process(final Map<String, Object> target, final DataStoreParams params) {
            target.put("ingested_by", ExampleIngester.class.getSimpleName());
            logger.info("DATASTORE CRAWL: {}", target);
            return target;
        }
    }

登録は ``src/main/resources/fess_ingest++.xml`` で行います。
中身は ``fess_ds++.xml`` と同じ形で、``exampleIngester`` という名前のコンポーネントに ``<postConstruct name="register">`` を付けます。
``Ingester.register()`` が ``IngestFactory`` に自身を追加します。

テンプレートの取得・ビルド・インストール・再起動は、データストアと同じ手順です（15.9 向けのコミットは ``8a1e45ddb63a118802287120effd3ce49fb60bfb``、jar は ``fess-ingest-example-15.9.0-SNAPSHOT.jar``）。
自分のプラグインでは artifactId を ``fess-ingest-`` で始めます。

実装するときは次の点に注意してください。

- ``target`` は変更したうえで必ず返します。戻り値は次の Ingester とインデクサーにそのまま渡され、``null`` のチェックはありません。``null`` を返しても文書は除外されず、登録の処理が壊れます
- 複数の Ingester は ``priority`` の小さい順に実行されます（既定値は 99）。前の Ingester が変更した ``target`` を次の Ingester が受け取ります
- ``process`` で例外が出ると、Fess は WARN をログに出して次の Ingester に進みます。文書の登録は止まりません。例外の前に ``target`` へ加えた変更はそのまま残ります

動作は、上の「動作を確かめる」で作ったデータストア設定のジョブをもう一度実行して確かめます。
Ingester はクローラーのプロセスで動くため、``fess-crawler.log`` に ``DATASTORE CRAWL:`` の行が文書ごとに出ていれば呼び出されています。
リポジトリの ``ExampleIngester`` は、ウェブ・ファイルクロールの文書も ``WEB/FILE CRAWL:`` として 1 件ずつログに出します。
すべてのクロールに効くので、確認が済んだら［システム］>［プラグイン］で削除し、Fess を再起動してください。

Fess をアップグレードするとき
=============================

プラグインは、入れる Fess と同じマイナーバージョンの ``fess-parent`` でビルドします（Fess 15.9 なら 15.9.x）。
公開されているプラグインも、Fess のマイナーバージョンごとに対応する版がリリースされています。

Fess を 15.10 に上げるときは、``pom.xml`` の ``fess-parent`` のバージョンを合わせてビルドし直します。
［システム］>［プラグイン］の一覧で古い jar を削除し、新しい jar をインストールして再起動します。
``bin/fess-setup upgrade plugins`` は新しい版をプラグインのリポジトリから取得する仕組みなので、リポジトリにない自作のプラグインはこの方法では更新できません。

次に読む記事
============

- データストア設定のパラメーター・スクリプト・権限・スケジュールを詳しく知りたい: :doc:`datastore-basics`
- 公開されているデータストアプラグインの設定例を見たい: :doc:`guide-06`・:doc:`guide-07`・:doc:`guide-12`
- 検索画面の見た目を変えたい: :doc:`guide-03`
- LLM プラグインを使って AI 検索モードを有効にしたい: :doc:`guide-19`
- Web アプリプラグイン（MCP サーバー）を使いたい: :doc:`guide-20`

参考資料
========

- `プラグインアーキテクチャ <https://fess.codelibs.org/ja/stable/dev/plugin-architecture.html>`__
- `データストアプラグイン開発 <https://fess.codelibs.org/ja/stable/dev/datastore-plugin.html>`__
- `Ingestプラグイン <https://fess.codelibs.org/ja/stable/dev/ingest-plugin.html>`__
- `テーマ開発ガイド <https://fess.codelibs.org/ja/stable/dev/theme-development.html>`__
- `プラグイン（管理画面） <https://fess.codelibs.org/ja/stable/admin/plugin-guide.html>`__
- `fess-ds-example（GitHub） <https://github.com/codelibs/fess-ds-example>`__
- `fess-ingest-example（GitHub） <https://github.com/codelibs/fess-ingest-example>`__
