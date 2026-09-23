==================================
テーマ開発ガイド
==================================

概要
====

|Fess| 15.9 の検索画面は、常に静的テーマで表示されます。静的テーマは ``/api/v2/*`` API を
利用する独立した SPA(シングルページアプリケーション)です。テーマは ZIP ファイルとして
配布し、管理画面からアップロードして有効化します。テーマを選んでいない場合は、|Fess| に
同梱の静的テーマ ``bootstrap`` が使われます。

検索画面の見た目を変えるには、別のテーマをインストールするか(:doc:`../admin/theme-guide`
を参照)、独自のテーマを作ります。独自のテーマは、同梱のテーマを複製して変更するのが
最も簡単です(`同梱テーマのカスタマイズ`_ を参照)。

.. note::

   静的テーマは |Fess| 15.7 以降で利用でき、15.9 で既定の検索画面になりました。検索画面の
   JSP を差し替える JAR テーマプラグインは、15.9 では検索画面を変えません。
   `JAR テーマプラグイン(レガシー)`_ を参照してください。

静的テーマ
==========

静的テーマは、``theme.yml`` マニフェストと ``index.html`` を含む静的リソースの
集合です。テーマ本体は |Fess| の ``/api/v2/*`` API を呼び出すフロントエンド
アプリケーションとして実装します。

構造
----

静的テーマは、次のようなディレクトリ構成になります。

::

    example/
    ├── theme.yml          # マニフェスト(必須)
    ├── index.html         # SPA のエントリー HTML
    ├── assets/            # JavaScript・CSS などの静的リソース
    │   └── styles.css
    ├── i18n/              # 多言語メッセージ(messages.<locale>.json)
    │   └── messages.en.json
    ├── help/              # ヘルプ定義(<locale>.json)
    │   └── en.json
    └── thumbnail.png      # プレビュー画像(任意)

マニフェスト (theme.yml)
------------------------

``theme.yml`` は ZIP のルートに配置する必須のマニフェストです。以下は最小構成の
例です。

.. code-block:: yaml

    apiVersion: fess.codelibs.org/v1
    kind: StaticTheme
    name: example
    displayName: "Example Theme"
    version: "15.9.0"
    minFessVersion: "15.9"
    entry: index.html
    spaFallback: true

指定できるフィールドは以下のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 22 12 66

   * - フィールド
     - 必須
     - 説明
   * - ``apiVersion``
     - 必須
     - 固定値 ``fess.codelibs.org/v1``\ 。
   * - ``kind``
     - 必須
     - 固定値 ``StaticTheme``\ 。
   * - ``name``
     - 必須
     - テーマ名。\ ``^[a-z0-9][a-z0-9_-]{0,63}$`` に一致する必要があります。
       ``themes/`` 配下に展開されるテーマのディレクトリ名(アップロード時は
       この ``name`` から自動的に決まります)、および配信 URL
       (``/themes/<name>/``)に使用されます。
   * - ``displayName``
     - 必須
     - 管理画面に表示される名前。
   * - ``version``
     - 必須
     - セマンティックバージョニング形式(例: ``15.9.0``、``15.9.1-beta.1``)。慣例として
       ``major.minor`` はテーマが対象とする |Fess| の系列に合わせます。こうすると
       バージョンだけでどの |Fess| 用のテーマか分かります。
   * - ``author``
     - 任意
     - 作者名。
   * - ``description``
     - 任意
     - テーマの説明。
   * - ``license``
     - 任意
     - ライセンス。
   * - ``homepage``
     - 任意
     - ホームページ URL。
   * - ``minFessVersion``
     - 任意
     - テーマが対応する |Fess| の最小バージョン。 ``version`` の ``major.minor`` と
       同じ値にします。 ``maxFessVersion`` はありません。 `公開`_ を参照してください。
   * - ``supportedLocales``
     - 任意
     - 対応ロケールの一覧(例: ``[en, ja, de]``)。
   * - ``entry``
     - 任意
     - SPA のエントリー HTML。既定値は ``index.html``\ 。
   * - ``spaFallback``
     - 任意
     - 非推奨。互換性のために受け付けますが、読まれません。15.9 からは検索画面の
       各パスで常にエントリー HTML が返ります。

.. note::

   ZIP からアップロードする場合、展開先のディレクトリ名は ``name`` から自動的に
   決まります。\ ``themes/`` ディレクトリに手動でテーマを配置する場合は、ディレクトリ名を
   ``name`` と一致させてください。一致しないテーマは再スキャン時に無視されます。

.. note::

   プレビュー用のサムネイルは、テーマのルートに ``thumbnail.png`` という固定名で
   配置します(管理画面のテーマ一覧で表示されます)。この画像はマニフェストの
   フィールドではなく、ファイル名で認識されます。サイズは 512KB 以内・512×512
   ピクセル以内を推奨します。

配信と API
----------

- 静的テーマは ``/themes/<name>/`` 配下で配信されます(``<name>`` は
  ``theme.yml`` の ``name``)。
- ``/``、``/search``、``/advance``、``/help``、``/error``、``/profile``、
  ``/cache``、``/chat`` の各パスでエントリー HTML(既定は ``index.html``)が返され、
  以降のルーティングは SPA が行います。15.9 からは ``spaFallback`` の値に関係なく
  こう動作し、このフィールドは読まれません。
- エラーもテーマが表示します。リクエストが失敗すると、ブラウザには要求された URL のまま、
  実際の HTTP ステータスでテーマのエントリー HTML が返ります。
- 管理画面(``/admin/*``)、``/api/*``、ログイン画面などは静的テーマの対象外で、
  |Fess| 本体が処理します。
- テーマの SPA は、検索結果やチャットなどのデータを ``/api/v2/*`` API から取得
  します。
- エントリー HTML の ``{{themePath}}`` は、配信時に ``themes/<name>`` に置き換えられます。
  テーマのファイルを ``index.html`` から参照するときは ``{{themePath}}/assets/styles.css``
  のように書きます。テーマ名を直接書かないので、別の名前でインストールしても自分の
  ファイルを読み込めます。
- エントリー HTML には、スクリプト・スタイル・画像・通信の取得元を |Fess| 自身に限る
  ``Content-Security-Policy`` ヘッダーが付きます(インラインのスタイルは許可され、
  インラインのスクリプトは許可されません)。そのため外部の CDN のフォントやスクリプトは
  読み込まれません。テーマに同梱してください。

パッケージング
--------------

`fess-themes <https://github.com/codelibs/fess-themes>`__ リポジトリの
``scripts/package.sh`` を使用すると、テーマを配布用の ZIP にまとめられます。

::

    ./scripts/package.sh example

``dist/example-<version>.zip`` が生成されます(``<version>`` は ``theme.yml`` の
``version``)。

.. note::

   ``theme.yml`` は ZIP のルートに配置する必要があります。サブディレクトリに
   入れると、アップロード時に認識されません。

公開
----

|Fess| プロジェクトが開発しているテーマは https://maven.codelibs.org/release/org/codelibs/fess/themes/ 以下に公開されています。配置は ``<name>/<version>/<name>-<version>.zip`` で、隣に ``.sha1`` が、テーマごとに公開済みバージョンを並べた ``maven-metadata.xml`` が置かれます。 ``bin/fess-setup install theme <name>`` はこのメタデータを読み、動作中の |Fess| 用に作られたバージョンを選びます。

テーマのバージョンは対象とする |Fess| の系列に合わせ、アーカイブの中身を変えたときは必ずバージョンを上げてください。公開済みのバージョンが上書きされることはないため、バージョンを据え置いた変更は配布されません。

マニフェストに上限を表すフィールドが無いのも同じ理由です。公開されたアーカイブは変更されないため、新しい |Fess| で動作しなくなったテーマにあとから上限を追加することはできません。その系列向けに公開しないことで、分かった時点で同じことを表せます。

.. note::

   公開済みのバージョンを調べるときは、ディレクトリ一覧ではなく ``maven-metadata.xml`` を使ってください。ディレクトリ索引は定期的に生成されるため、新しく公開したテーマは一覧に現れるより先にメタデータから読み取れます。

インストールと有効化
--------------------

1. 管理画面で「システム」→「テーマ」(``/admin/theme/``)を開きます。
2. 作成した ZIP ファイルをアップロードします。公開済みのテーマは、コマンドラインから
   ``bin/fess-setup install theme <name>`` でインストールすることもできます。
   :doc:`../install/fess-setup` を参照してください。
3. 一覧ページの「デフォルトテーマ」プルダウンから対象テーマを選び、「設定」ボタンを
   押して有効化します。

有効化の仕組みは以下のとおりです。

- 「設定」ボタンを押すと、選択したテーマ名がシステムプロパティ ``theme.default``
  に保存され、システム全体の既定テーマになります。
- テーマ名を仮想ホストのキーと一致させると、その仮想ホストにアクセスしたときだけ
  テーマが適用されます。これにより、仮想ホストごとにテーマを切り替えられます。
- ディスク上の ``themes/`` ディレクトリを直接更新した場合は、「再読み込み」で
  再スキャンできます。

.. note::

   ZIP のアップロードには、ファイルサイズ・展開後の合計サイズ・エントリー数などの
   上限があり、``fess_config.properties`` の ``theme.*`` プロパティで調整できます
   (例: ``theme.upload.max.size`` は既定 50MB、``theme.directory.path`` は既定
   ``themes``)。展開時には ZIP Slip や zip bomb を防ぐための検証が行われます。

.. _theme-customize-bundled:

同梱テーマのカスタマイズ
------------------------

同梱のテーマ ``bootstrap`` は、|Fess| のインストール先の ``app/themes/bootstrap/``
(RPM/DEB パッケージでは ``/usr/share/fess/app/themes/bootstrap/``)にあります。
直接編集しないでください。アップグレードで置き換わるうえ、``bootstrap`` という名前は
同梱のテーマ専用で、削除もアップロードによる置き換えもできません。別の名前で複製して
使います。

1. ディレクトリを複製します。例えば ``mytheme`` とします::

       $ cp -r app/themes/bootstrap /tmp/mytheme

2. ``theme.yml`` の ``name`` を ``mytheme`` に変え、``displayName`` も変えます。
   ``name`` はディレクトリ名と一致させます。

3. ``index.html`` は変更しません。同梱の ``index.html`` は、スタイルシート・ロゴ・
   スクリプトなど自分のファイルを ``{{themePath}}/assets/...`` で参照しており、|Fess| は
   配信時に ``{{themePath}}`` を ``themes/<name>`` (``theme.yml`` の ``name``)に
   置き換えます。そのため、名前を変えるだけで複製したテーマは自分のファイルを読み込みます。
   ``index.html`` から参照するファイルを追加するときも、``{{themePath}}/assets/...`` の
   形で書いてください。

4. 変更を加えます。

   - 配色・レイアウト: ``assets/styles.css``
   - ロゴ: ``assets/logo-head.png`` (ヘッダー)と ``assets/logo.png`` (検索トップ)
   - フッター(``footer.copyright_org``)などの文言: 言語ごとの
     ``i18n/messages.<locale>.json``
   - ページの構造: ``index.html``

5. ``theme.yml`` がルートに来るようにディレクトリを ZIP にまとめ、管理画面の
   「システム」>「テーマ」でアップロードします::

       $ cd /tmp/mytheme && zip -r ../mytheme.zip .

   ディレクトリを ``app/themes/`` に置き、同じページの「再読み込み」を押してもかまいません。

6. 同じページで ``mytheme`` を既定のテーマに設定します。

.. note::

   同梱のテーマは、その |Fess| のバージョンの ``/api/v2/*`` API に合わせてあります。
   |Fess| をアップグレードしたら、新しい同梱テーマから複製し直して変更を再適用してください。

JAR テーマプラグイン(レガシー)
================================

.. warning::

   |Fess| 15.9 からは検索画面が常に静的テーマで表示されるため、JAR テーマプラグインでは
   検索画面を変えられません。JAR テーマが提供する JSP のうち、使われるのはログイン画面
   (``/login/``)のものだけです。デザインは静的テーマに移してください。
   `同梱テーマのカスタマイズ`_ を参照してください。

JAR テーマプラグインは、|Fess| 本体の ``view`` / ``css`` / ``js`` / ``images``
ディレクトリをテーマ名ごとに上書きするプラグインです。プラグインの一般的な構造や
ビルド方法については :doc:`plugin-architecture` も参照してください。

構造
----

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        ├── view/      # JSP ファイル(search.jsp, index.jsp, header.jsp など)
        ├── css/       # CSS ファイル(style.css など)
        ├── js/        # JavaScript ファイル
        └── images/    # 画像ファイル(logo.png など)

.. note::

   ビュー(テンプレート)は JSP 形式です。リソースの最上位ディレクトリは
   ``view`` / ``css`` / ``js`` / ``images`` の 4 つのみが認識されます。
   アーティファクト名は ``fess-theme-`` で始まる必要があります。

pom.xml
-------

プラグインは ``fess-parent`` を親 POM とする jar としてビルドします。テーマは
リソースのみで構成されるため、通常は追加の依存関係を宣言する必要はありません。

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <artifactId>fess-theme-example</artifactId>
        <version>15.9.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.9.0</version>
            <relativePath />
        </parent>
    </project>

CSS・画像のカスタマイズ
-----------------------

JSP は Bootstrap ベースです。CSS を上書きして配色やレイアウトを変更したり、
``images/logo.png`` を差し替えてロゴを変更したりできます。15.9 では、この変更が
反映されるのはログイン画面だけです。検索画面は静的テーマです
(`同梱テーマのカスタマイズ`_ を参照)。

ビルドとインストール
--------------------

::

    mvn clean package

``target/`` ディレクトリに JAR ファイル(例: ``fess-theme-example-15.9.0.jar``)が
生成されます。管理画面の「システム」→「プラグイン」からインストールできます。
インストール手順の詳細は :doc:`../admin/plugin-guide` を参照してください。

インストールすると、JAR 内の各ディレクトリはテーマ名ごとに以下の場所へ展開されます
(テーマ名はアーティファクト名から ``fess-theme-`` を除いた部分。上記の例では
``example``)。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - JAR 内のディレクトリ
     - 展開先
   * - ``view/``
     - ``WEB-INF/view/<theme>/``
   * - ``css/``
     - ``css/<theme>/``
   * - ``js/``
     - ``js/<theme>/``
   * - ``images/``
     - ``images/<theme>/``

有効化
------

JAR テーマは、仮想ホスト機能を使って有効化します。仮想ホストのキーをテーマ名に
一致させると、そのホストへのアクセスでテーマが適用されます。

1. 「システム」→「全般」の仮想ホスト設定で、``Host:localhost:8080=example`` の
   ように、リクエストの ``Host`` ヘッダーとテーマ名(仮想ホストのキー)を対応付けます。
2. 必要に応じて、クローリングの Web 設定などの仮想ホストにも同じ名前(``example``)を
   設定します。

仮想ホストの設定方法の詳細は :doc:`../admin/general-guide` を参照してください。

既存テーマの例
==============

- `fess-themes <https://github.com/codelibs/fess-themes>`__ - 静的テーマ集
  (``codesearch``、``docsearch`` など複数の静的テーマを収録)
- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__ - JAR テーマ
- `fess-theme-classic <https://github.com/codelibs/fess-theme-classic>`__ - JAR テーマ

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`../admin/plugin-guide` - プラグインのインストール
