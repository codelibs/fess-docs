==================================
Webアプリプラグイン
==================================

概要
====

Web アプリプラグイン(``fess-webapp-*``)は、|Fess| の Web アプリケーションを
拡張するプラグインです。他の種類のプラグインと異なり、Action クラスや JSP を
直接追加するのではなく、DI コンテナ(Lasta Di)に対して **コンポーネントを追加
または置き換える** ことで機能を拡張します。代表的な用途は次のとおりです:

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
``<baseDicon>+<componentName>.xml`` という名前の DI 設定ファイルで **同じ
コンポーネント名で再登録** します。例えば ``systemHelper`` は |Fess| 本体の
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
   すべて記述する必要があります(例えば ``app.xml`` の ``queryHelper``)。これらは
   |Fess| のリリースごとに同期する必要があります。コアから削除されたメソッドを呼び続けると、
   そのコンポーネント定義は ``BeanMethodNotFoundException`` で初期化に失敗します。例えば
   15.9 では ``systemHelper`` の ``addDesignJspFileName`` が削除されたため、これを呼ぶ
   置き換えファイルは失敗します。この保守コストが、置き換えよりも追加が推奨される理由です。

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

.. _webapp-plugin-password-encoder:

パスワードハッシュアルゴリズムの追加(fess++.xml)
------------------------------------------------

ローカルユーザーのパスワードのハッシュは、コンポーネントが作ります。保存されたパスワードは ``{id}hash`` の形式です。 |Fess| は、保存された値の ``id`` と、新しいパスワードについては ``app.password.algorithm`` の値（既定は ``bcrypt`` ）から、DI コンポーネント ``<id>PasswordEncoder`` を探します。 ``<sso.type>Authenticator`` や ``<storage.type>StorageClient`` の解決と同じ方法です。 |Fess| は ``bcryptPasswordEncoder`` を自分で登録します。アルゴリズムを追加するには、 ``org.codelibs.fess.crypto.password.PasswordEncoder`` を実装し、そのクラスを ``fess++.xml`` に登録します。 ``fess++.xml`` は、Lasta Di が |Fess| 本体の ``fess.xml`` にマージします。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="argon2PasswordEncoder"
            class="com.example.Argon2PasswordEncoder">
        </component>
    </components>

インターフェースには次のメソッドがあります。

.. list-table:: PasswordEncoder のメソッド
   :header-rows: 1
   :widths: 35 65

   * - メソッド
     - 説明
   * - ``String encode(String rawPassword)``
     - パスワードをハッシュ化します。結果は、 |Fess| が付ける ``{id}`` の後ろに保存されます。元のパスワードを正しく表せないパスワードには ``IllegalArgumentException`` を投げてください。メッセージにパスワードを含めてはいけません。
   * - ``boolean matches(String rawPassword, String encodedPassword)``
     - このエンコーダーが作ったハッシュに対してパスワードを検証します。パスワードが違う場合と、ハッシュの形式が壊れている場合は ``false`` を返してください。
   * - ``boolean needsUpgrade(String encodedPassword)``
     - 省略可（既定は ``false`` ）。保存されているハッシュが、現在の ``encode`` が作るものより弱いかどうかを返します。 ``true`` の場合、そのユーザーの次のログイン時にハッシュを作り直します。BCrypt は、コストが ``app.password.bcrypt.cost`` より小さい場合に ``true`` を返します。
   * - ``int getMaxPasswordBytes()``
     - 省略可（既定は ``0`` で、制限なし）。 ``encode`` が受け付ける、UTF-8 でのパスワードの最大バイト数です。BCrypt は ``72`` を返します。
   * - ``boolean isVerificationCostly()`` と ``void applyTimingPadding()``
     - 省略可（既定は ``false`` と何もしない）。意図的に遅いアルゴリズムは ``true`` を返し、 ``applyTimingPadding()`` で ``matches`` 1 回分ほどの時間を使います。ハッシュを検証しないままログインが失敗したとき（たとえばユーザーが存在しない場合）に |Fess| がこれを呼ぶため、応答時間からユーザーの有無は分かりません。

エンコーダーを使うには、次のようにします。

#. jar を ``WEB-INF/plugin`` ディレクトリに置きます。Web アプリプラグインと同じく、マニフェストに ``Fess-WebAppJar: true`` が必要です（「pom.xmlとマニフェスト」を参照）。これがないとコンポーネントが見つかりません。
#. ``fess_config.properties`` の ``app.password.algorithm`` に ID を設定します（ ``argon2PasswordEncoder`` なら ``argon2`` ）。ID は小文字で、 ``}`` を含めてはいけません。以後、新規または変更されたパスワードはこのエンコーダーでハッシュ化されます。別の ID で保存されたパスワードや、ID のない従来のハッシュは、 ``app.password.upgrade.enabled`` が ``true`` （既定）の間、そのユーザーの次のログイン成功時にハッシュを作り直します。

次の点に注意してください。

- エンコーダーは全スレッドで共有されるシングルトンなので、スレッドセーフにしてください。
- 長さの制限はエンコーダーのものです。パスワードを設定するとき（ユーザー管理画面、強制パスワード変更、 ``/api/v2/auth/password`` 、Admin API）、 |Fess| は ``app.password.algorithm`` のアルゴリズムの ``getMaxPasswordBytes()`` を超えるパスワードを「パスワードは N バイト以内である必要があります。」として拒否します。 ``0`` 以下の場合は ``password.max.length`` だけを確認します。保存されたハッシュを検証するときに、 |Fess| は長さの制限を適用しません。長いパスワードが一致してよいかどうかは ``matches`` に任されます。
- その ID で保存されたパスワードがある間は、プラグインを入れたままにしてください。コンポーネントがないと、その ID のハッシュはどのパスワードにも一致せず、そのユーザーはログインできません。ハッシュも作り直されません。
- ``app.password.algorithm`` にコンポーネントのない ID を指定した場合（たとえばプラグインの jar を削除したあとなど）、 |Fess| は起動し、別の ID のハッシュを持つユーザーはログインできますが、パスワードの設定は ``app.password.algorithm`` を示すエラーで失敗します。

検索画面のカスタマイズ
======================

Web アプリプラグインは JSP ビューを追加できません。JSP ビューは |Fess| 本体の WAR の
``WEB-INF/view/`` に配置されており、プラグイン JAR はクラスパス
(``WEB-INF/classes``)にマウントされるためです。検索画面のデザインを変更する場合は、
テーマを使用します。テーマは検索画面のデザイン(HTML/CSS/JavaScript)を
カスタマイズします。:doc:`theme-development` を参照してください。

ビルドとインストール
====================

::

    mvn clean package

``target/`` ディレクトリに JAR ファイル(例: ``fess-webapp-example-15.10.0.jar``)が
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
   * - ``fess-webapp-bangs``
     - DuckDuckGo 形式のバング(``!g``)。別のサイトへ検索を送る
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
