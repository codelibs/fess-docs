==================================
Webアプリプラグイン
==================================

概要
====

Web アプリプラグイン(``fess-webapp-*``)は、|Fess| の Web アプリケーションを
拡張するプラグインです。他の種類のプラグインと異なり、Action クラスや JSP を
直接追加するのではなく、DI コンテナ(Lasta Di)に対して \*\*コンポーネントを追加
または置き換える\*\* ことで機能を拡張します。代表的な用途は次のとおりです:

- 新しいコンポーネント(ヘルパー・サービスなど)の追加
- |Fess| 本体のコンポーネントの置き換え(サブクラス化)
- REST API エンドポイントの追加(``WebApiManager``)
- 検索動作の拡張(クエリコマンド、ランクフュージョンなど)

.. note::

   Web アプリプラグインは JAR として配布され、内部のクラスと DI 設定ファイルが
   |Fess| の Web アプリケーションのクラスパスに読み込まれます。JSP ビューを
   追加するものではありません。検索画面のデザインをカスタマイズする場合は
   :doc:`theme-development` を参照してください。

基本構造
========

Web アプリプラグインの実装テンプレートである
`fess-webapp-example <https://github.com/codelibs/fess-webapp-example>`__ を
例にすると、プラグインは「実装クラス」と「DI 登録ファイル」で構成されます:

::

    fess-webapp-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/webapp/example/helper/
        │   ├── ExampleHelper.java        # 追加するコンポーネント
        │   └── CustomSystemHelper.java   # コアコンポーネントの置き換え
        └── resources/
            ├── app++.xml                 # コンポーネントの追加(マージ)
            └── fess+systemHelper.xml     # コンポーネントの置き換え

.. note::

   実装クラスのパッケージは ``org.codelibs.fess.webapp.<プラグイン名>`` を使用します。
   DI 設定ファイルは ``src/main/resources/`` に配置します。データストアプラグインと
   異なり ``src/main/webapp/`` や JSP は含めません。

pom.xmlとマニフェスト
=====================

Web アプリプラグインは ``fess-parent`` を親 POM とする jar としてビルドします。
|Fess| 本体から実行時に提供される ``fess`` や ``opensearch`` は ``provided``
スコープで宣言し、``lastaflute``・``dbflute-runtime``・``corelib`` など実行時に
必要なライブラリは通常のスコープで宣言します。

Web アプリプラグインで最も重要なのは、JAR マニフェストに ``Fess-WebAppJar: true``
を付与することです。この宣言により、|Fess| はプラグインのクラスと DI 設定ファイルを
Web アプリケーションのクラスローダーへマウントします。この設定は
``maven-jar-plugin`` で行います:

.. code-block:: xml

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-jar-plugin</artifactId>
                <configuration>
                    <archive>
                        <manifestEntries>
                            <Fess-WebAppJar>true</Fess-WebAppJar>
                        </manifestEntries>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>

.. warning::

   ``Fess-WebAppJar: true`` を付与しないと、プラグインのクラスや DI 設定ファイルは
   Web アプリケーションのクラスパスに読み込まれず、コンポーネントの追加・置き換えが
   有効になりません。

pom.xml 全体の構成(親 POM・依存関係の宣言方法など)は
:doc:`plugin-architecture` を参照してください。

拡張パターン
============

コンポーネントの追加(app++.xml)
--------------------------------

最も基本的な拡張方法は、独自のコンポーネントを追加することです。
Lasta Di は、クラスパス上の ``app++.xml`` を |Fess| 本体の ``app.xml`` から
構築される ``app`` 名前空間へ **マージ** します(末尾の ``++`` は追加マージの
規約です)。追加するコンポーネントは |Fess| 本体に存在しない名前を使用するため、
何も上書きされません。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleHelper"
            class="org.codelibs.fess.webapp.example.helper.ExampleHelper">
        </component>
    </components>

コンポーネントの実装では、初期化に ``@PostConstruct`` を使用し、|Fess| 本体の
コンポーネントは ``ComponentUtil`` から取得して再利用します(コピーや上書きは
しません):

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import org.codelibs.fess.helper.SystemHelper;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;

    public class ExampleHelper {

        protected String pluginName = "fess-webapp-example";

        @PostConstruct
        public void init() {
            // DI による生成後に一度だけ呼び出される初期化処理
        }

        public String getPluginLabel() {
            // コアの SystemHelper を再利用して稼働中の Fess バージョンを取得
            final SystemHelper systemHelper = ComponentUtil.getSystemHelper();
            final String version = systemHelper != null ? systemHelper.getProductVersion() : "unknown";
            return pluginName + " (Fess " + version + ")";
        }
    }

.. tip::

   まずはこの「コンポーネントの追加」を検討してください。コア機能を変更する必要が
   ない限り、置き換えよりも安全でメンテナンス性に優れます。

コアコンポーネントの置き換え(fess+componentName.xml)
-----------------------------------------------------

|Fess| 本体のコンポーネントの挙動を変更したい場合は、対象クラスをサブクラス化し、
``<baseDicon>+<componentName>.xml`` という名前の DI 設定ファイルで \*\*同じ
コンポーネント名で再登録\*\* します。例えば ``systemHelper`` は |Fess| 本体の
``fess.xml`` で宣言されているため、置き換えファイルは ``fess+systemHelper.xml``
になります(``app+systemHelper.xml`` ではありません)。

.. code-block:: java

    package org.codelibs.fess.webapp.example.helper;

    import java.nio.file.Path;

    import org.codelibs.fess.helper.SystemHelper;

    public class CustomSystemHelper extends SystemHelper {

        @Override
        protected void parseProjectProperties(final Path propPath) {
            try {
                super.parseProjectProperties(propPath);
            } catch (final Exception e) {
                // 独自の処理
            }
            System.setProperty("fess.webapp.plugin", "true");
        }
    }

.. warning::

   置き換え(単一の ``+``)は、コンポーネント定義を **丸ごと** 置き換えます。
   このため、置き換えファイルにはコア定義が行っている ``<postConstruct>`` を
   すべて記述する必要があります。例えば ``systemHelper`` を置き換える場合は、
   デザイン JSP 名のマッピング(``addDesignJspFileName``)をコアの ``fess.xml`` から
   すべてコピーして記述しなければなりません。これらは |Fess| のリリースごとに
   同期する必要があり、漏れがあると一部の画面(``chat`` / ``login`` など)が
   解決できなくなります。この保守コストが、置き換えよりも追加が推奨される理由です。

REST APIの追加(fess_api++.xml)
-------------------------------

新しい REST API エンドポイントを追加するには、``WebApiManager`` を実装します。
``BaseApiManager`` を継承し、``@PostConstruct`` で ``WebApiManagerFactory`` に
自身を登録します。登録された API マネージャーは、リクエストごとに ``WebApiFilter``
から呼び出されます。\ ``fess_api++.xml`` でコンポーネントを登録します:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleApiManager"
            class="org.codelibs.fess.webapp.example.api.ExampleApiManager">
        </component>
    </components>

.. code-block:: java

    package org.codelibs.fess.webapp.example.api;

    import java.io.IOException;

    import org.codelibs.fess.api.BaseApiManager;
    import org.codelibs.fess.util.ComponentUtil;

    import jakarta.annotation.PostConstruct;
    import jakarta.servlet.FilterChain;
    import jakarta.servlet.ServletException;
    import jakarta.servlet.http.HttpServletRequest;
    import jakarta.servlet.http.HttpServletResponse;

    public class ExampleApiManager extends BaseApiManager {

        public ExampleApiManager() {
            // このマネージャーが処理するパスのプレフィックス
            setPathPrefix("/api/example");
        }

        @PostConstruct
        public void register() {
            ComponentUtil.getWebApiManagerFactory().add(this);
        }

        @Override
        public boolean matches(final HttpServletRequest request) {
            // このマネージャーがリクエストを処理するかどうかを判定
            return request.getServletPath().startsWith(pathPrefix);
        }

        @Override
        public void process(final HttpServletRequest request, final HttpServletResponse response,
                final FilterChain chain) throws IOException, ServletException {
            // リクエストの処理とレスポンスの書き込み
        }

        @Override
        protected void writeHeaders(final HttpServletResponse response) {
            // レスポンスヘッダーの設定(必要に応じて)
        }
    }

実装例としては、``/api/v1`` を提供する
`fess-webapp-v1-api <https://github.com/codelibs/fess-webapp-v1-api>`__ や、
``/json`` / ``/suggest`` を提供する
`fess-webapp-classic-api <https://github.com/codelibs/fess-webapp-classic-api>`__ が
参考になります。

検索画面のカスタマイズ
======================

Web アプリプラグインは JSP ビューを追加できません。JSP ビューは |Fess| 本体の WAR の
``WEB-INF/view/`` に配置されており、プラグイン JAR はクラスパス
(``WEB-INF/classes``)にマウントされるためです。検索画面のデザインを変更する場合は、
次のいずれかを使用します:

- **テーマ**: 検索画面のデザイン(HTML/CSS/JavaScript)をカスタマイズします。
  :doc:`theme-development` を参照してください。
- **systemHelper の置き換え**: 上記の「コアコンポーネントの置き換え」により、
  デザイン JSP 名のマッピングを変更できます(ただし JSP ファイル自体は |Fess| 本体が
  提供します)。

ビルドとインストール
====================

::

    mvn clean package

``target/`` ディレクトリに JAR ファイル(例: ``fess-webapp-example-15.8.0.jar``)が
生成されます。生成した JAR は管理画面からインストールするか、
``app/WEB-INF/plugin/`` ディレクトリに配置して |Fess| を再起動します。
インストール手順の詳細は :doc:`../admin/plugin-guide` を参照してください。

公開プラグインの例
==================

|Fess| プロジェクトでは、以下の Web アプリプラグインが公開されています。
開発の参考として `GitHub <https://github.com/codelibs>`__ で公開されています:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - プラグイン
     - 説明
   * - ``fess-webapp-example``
     - プラグイン実装のテンプレート
   * - ``fess-webapp-v1-api``
     - ``/api/v1`` REST API
   * - ``fess-webapp-classic-api``
     - ``/json`` / ``/suggest`` レガシー REST API
   * - ``fess-webapp-mcp``
     - MCP(Model Context Protocol)サーバー
   * - ``fess-webapp-semantic-search``
     - ニューラル検索/ベクトル検索(15.8でコアに統合されたため非推奨)
   * - ``fess-webapp-multimodal``
     - マルチモーダル(画像・テキスト)検索

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`theme-development` - テーマのカスタマイズ
- :doc:`../admin/plugin-guide` - プラグインのインストール
- :doc:`overview` - 開発者ドキュメント概要
