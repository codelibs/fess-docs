==================================
データストアプラグイン開発
==================================

概要
====

データストアプラグインを開発することで、|Fess| に新しいデータソースからの
コンテンツ取得機能を追加できます。データストアは、データベース・API・ファイルなどの
外部システムからレコードを取得し、管理画面で設定したマッピングスクリプトに従って
インデックスフィールドへ変換したうえで、|Fess| のインデックスへ登録します。

CSV・JSON・データベース・Git・各種クラウドサービスなど、公開されている
コネクター(``fess-ds-*``)はすべてこの仕組みで実装されています。実装の雛形として
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ が公開されているため、
新しいコネクターを作成する場合はこれをコピーして始めるのが簡単です。

基本構造
========

データストアプラグインは、次の3点で構成されます。

- ``AbstractDataStore`` を継承したクラスを作成する
- ``getName()`` と ``storeData()`` の2つのメソッドを実装する
- ``fess_ds++.xml`` でコンポーネントとして登録する

最小実装
--------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // ハンドラー名として使用される。クラスの単純名を返すのが慣例
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // データの取得と処理をここに実装
        }
    }

.. note::

   ``getName()`` と ``storeData()`` はいずれも ``protected`` の抽象メソッドです。
   ``DataConfig`` のパッケージは |Fess| 15.x では ``org.codelibs.fess.opensearch.config.exentity``
   である点に注意してください(以前の ``org.codelibs.fess.es.config.exentity`` は廃止されています)。

コンポーネントの登録
--------------------

作成したデータストアを |Fess| に認識させるため、``src/main/resources/fess_ds++.xml`` に
コンポーネントを登録します。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

``<postConstruct name="register">`` により、コンポーネント生成後に ``AbstractDataStore``
が持つ ``register()`` メソッドが自動的に呼び出され、``DataStoreFactory`` へ自身が登録されます。
このとき登録される名前が ``getName()`` の戻り値(上記の例では ``ExampleDataStore``)であり、
管理画面のデータストア設定で選択する「ハンドラー名」になります。

AbstractDataStore
=================

主要メソッド
------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - メソッド
     - 区分
     - 説明
   * - ``getName()``
     - 実装(必須)
     - データストアのハンドラー名を返す抽象メソッド。\ ``getClass().getSimpleName()`` を返すのが慣例
   * - ``storeData()``
     - 実装(必須)
     - データの取得・変換・インデックス登録を行う抽象メソッド
   * - ``register()``
     - 継承(通常は変更不要)
     - ``fess_ds++.xml`` の ``postConstruct`` から自動呼び出しされ、``DataStoreFactory`` へ登録する
   * - ``store()``
     - 継承(フレームワーク呼び出し)
     - フレームワークが呼び出す入口。\ ``defaultDataMap`` などを準備して ``storeData()`` を呼ぶ
   * - ``convertValue()``
     - 継承(ヘルパー)
     - ``scriptMap`` の値(テンプレート)をスクリプトエンジンで評価する
   * - ``getScriptType()``
     - 継承(ヘルパー)
     - ``script_type`` パラメーターを取得する(既定は Groovy)
   * - ``getReadInterval()``
     - 継承(ヘルパー)
     - ``readInterval`` パラメーター(ミリ秒)を取得する
   * - ``sleep()``
     - 継承(ヘルパー)
     - 指定ミリ秒スリープする(レコード間の待機に使用)

storeData のパラメーター
------------------------

``storeData()`` メソッドに渡されるパラメーター:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - パラメーター
     - 型
     - 説明
   * - ``dataConfig``
     - ``DataConfig``
     - データストア設定(ID・ハンドラー名・パラメーター・スクリプトなど)
   * - ``callback``
     - ``IndexUpdateCallback``
     - 生成したドキュメントをインデックスへ登録するコールバック
   * - ``paramMap``
     - ``DataStoreParams``
     - 管理画面「パラメーター」欄の設定値。\ ``getAsString(key)`` / ``getAsString(key, default)`` / ``get(key)`` / ``asMap()`` / ``containsKey(key)`` でアクセスする
   * - ``scriptMap``
     - ``Map<String, String>``
     - 管理画面「スクリプト」欄の設定。キーがインデックスフィールド名、値が評価対象のスクリプトテンプレート
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - 各ドキュメントの既定フィールド値(設定ID・boost・role・mimetype・仮想ホストなど)。フレームワークが用意する

.. warning::

   ``paramMap`` の型は ``Map<String, String>`` ではなく ``DataStoreParams`` です。
   ``DataStoreParams`` は ``Map`` を実装していないため、値の取得には ``get()`` ではなく
   文字列を返す ``getAsString()`` を使用してください。

データ処理の流れ
----------------

``storeData()`` の実装は、次の流れでデータを処理します。

#. 外部システムからソースレコードを取得する。
#. ``paramMap.asMap()`` にソースレコードのフィールドをマージして ``resultMap`` を構築する
   (スクリプトはこの ``resultMap`` に対して評価される)。
#. ``scriptMap`` の各エントリを ``convertValue(scriptType, template, resultMap)`` で評価し、
   結果を ``dataMap`` に格納する。マッピングはコード内にハードコードするのではなく、
   管理者が「スクリプト」欄で定義する点が重要です。
#. ``callback.store(paramMap, dataMap)`` を呼び出してドキュメントとしてインデックス登録する。

実装例
======

シンプルなデータストア
----------------------

外部 API からレコードを取得してインデックス登録する例です。

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // パラメーターの取得(DataStoreParams では getAsString を使用する)
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // スクリプトの評価タイプ(既定は Groovy)
        final String scriptType = getScriptType(paramMap);
        // レコード間の待機時間(ミリ秒)
        final long readInterval = getReadInterval(paramMap);

        try {
            // 外部システムからデータを取得
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // 既定フィールドをコピーして dataMap を初期化
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // パラメーターとソースレコードをマージした resultMap を構築
                // (スクリプトはこの resultMap に対して評価される)
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // scriptMap の各エントリを評価してインデックスフィールドを生成
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // インデックスに登録
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` は外部システムからレコード一覧を取得する独自メソッドです。取得した
各レコード(``Map<String, Object>``)のフィールド名が、``scriptMap`` のスクリプトから
参照できる名前になります。\ ``DataStoreException`` は ``org.codelibs.fess.exception``
パッケージのクラスです。

ページネーション対応
--------------------

大量のデータを扱う場合は、ページ単位で取得しながら処理します。1レコードあたりの処理
(``resultMap`` の構築・``scriptMap`` の評価・``callback.store()`` の呼び出し)を
``processRecord()`` のようなメソッドに切り出しておくと、取得ロジックと分離できます。

.. code-block:: java

    int offset = 0;
    final int pageSize = 100;

    while (true) {
        final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey, offset, pageSize);

        if (records.isEmpty()) {
            break;
        }

        for (final Map<String, Object> record : records) {
            processRecord(record, callback, paramMap, scriptMap, defaultDataMap);
        }

        offset += pageSize;
    }

認証の実装
==========

外部システムの認証は、コネクター側で実装します。以下は一般的な HTTP クライアント
ライブラリを用いた実装例で、|Fess| が提供する API ではありません。利用するライブラリは
プラグインの依存関係として同梱してください。

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // リフレッシュトークンを用いてアクセストークンを取得する例
        final OkHttpClient client = new OkHttpClient();

        final RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        final Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            final JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

APIキー認証
-----------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

エラーハンドリング
==================

処理を中断すべき致命的なエラーでは ``DataStoreException`` をスローします。

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // 処理
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // リトライロジック
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   ``fess-ds-example`` をはじめとする実際のコネクターでは、1レコードのエラーで
   クロール全体を止めないよう、レコード単位で ``CrawlingAccessException`` を捕捉し、
   ``FailureUrlService`` にエラー URL を記録しています。また
   ``DataStoreCrawlingException`` の中断フラグを用いて、クロール全体を中断するかどうかを
   制御しています。堅牢なコネクターを実装する場合は ``ExampleDataStore`` の実装を参照してください。

テスト
======

ユニットテスト
--------------

|Fess| のプラグインは UTFlute の ``LastaDiTestCase`` を用いてテストします。テストは
JUnit 5(Jupiter)で記述します。\ ``IndexUpdateCallback`` を、登録された ``dataMap`` を
収集する実装に差し替えることで、モックライブラリを使わずにマッピング結果を検証できます。

.. code-block:: java

    public class ExampleDataStoreTest extends LastaDiTestCase {

        public ExampleDataStore dataStore;

        @Override
        protected String prepareConfigFile() {
            return "test_app.xml";
        }

        @Override
        public void setUp(final TestInfo testInfo) throws Exception {
            super.setUp(testInfo);
            dataStore = new ExampleDataStore();
        }

        @Test
        public void test_getName() {
            assertEquals("ExampleDataStore", dataStore.getName());
        }

        @Test
        public void test_storeData() {
            final TestIndexUpdateCallback callback = new TestIndexUpdateCallback();
            final DataStoreParams paramMap = new DataStoreParams();

            final Map<String, String> scriptMap = new HashMap<>();
            scriptMap.put("title", "title");

            dataStore.storeData(new DataConfig(), callback, paramMap, scriptMap, new HashMap<>());

            assertFalse(callback.getDataMapList().isEmpty());
        }

        // 登録された dataMap を収集するテスト用コールバック
        private static class TestIndexUpdateCallback implements IndexUpdateCallback {
            private final List<Map<String, Object>> dataMapList = new ArrayList<>();

            @Override
            public void store(final DataStoreParams paramMap, final Map<String, Object> dataMap) {
                dataMapList.add(new HashMap<>(dataMap));
            }

            @Override
            public long getExecuteTime() {
                return 0;
            }

            @Override
            public long getDocumentSize() {
                return dataMapList.size();
            }

            @Override
            public void commit() {
                // 何もしない
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   ``setUp`` は基底クラスで ``@BeforeEach`` が付与されているため、オーバーライド側に
   ライフサイクルアノテーションを付け直す必要はありません。各テストメソッドには
   ``@Test``\ (``org.junit.jupiter.api.Test``)を付与します。

ビルドとインストール
====================

pom.xml
-------

プラグインは ``fess-parent`` を親 POM とする jar としてビルドします。\ ``fess`` および
``opensearch`` への依存は、実行時に |Fess| 本体から提供されるため ``provided`` にします。

.. code-block:: xml

    <project xmlns="http://maven.apache.org/POM/4.0.0" ...>
        <modelVersion>4.0.0</modelVersion>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

テストには JUnit 5 と ``org.dbflute.utflute:utflute-lastaflute`` を利用します。

ビルド
------

.. code-block:: bash

    mvn clean package

``target/`` ディレクトリに ``fess-ds-example-15.8.0.jar`` が生成されます。

インストール
------------

生成した JAR を |Fess| にインストールし、|Fess| を再起動します。インストール手順の詳細は
:doc:`../admin/plugin-guide` を参照してください。インストール後、管理画面の
「クローラー > データストア」から新規設定を作成し、「ハンドラー名」に ``getName()`` が返す名前
(この例では ``ExampleDataStore``)を指定します。

設定例
======

管理画面での設定例:

パラメーター
------------

「パラメーター」欄には、コネクターが ``paramMap`` から読み取るキーと値を記述します。

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

スクリプト
----------

「スクリプト」欄には、``左辺=右辺`` の形式でマッピングを記述します。左辺がインデックス
フィールド名、右辺がソースレコードのフィールドを参照するスクリプト(既定では Groovy)です。
以下は、ソースレコードが ``url`` / ``title`` / ``content`` / ``updated_at`` /
``content_type`` フィールドを持つ場合の例です。

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   右辺で参照できるフィールド名は、コネクターが ``resultMap`` に格納する値
   (``paramMap`` の値とソースレコードのフィールド)によって決まります。CSV や JSON など
   既存コネクターでは ``data.*`` のような独自のプレフィックスが付く場合があるため、
   各コネクターのドキュメントを参照してください。

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`../admin/plugin-guide` - プラグインのインストール
- :doc:`../config/datastore/ds-overview` - データストアコネクター概要
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ - データストアプラグインの実装テンプレート
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - 公開コネクターの例
