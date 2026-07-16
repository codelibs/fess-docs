==================================
テーマ開発ガイド
==================================

概要
====

|Fess| では、検索画面のデザインを次の 2 つの方法でカスタマイズできます。

静的テーマ (Static Theme)
    |Fess| 15.7 で導入された仕組みです。テーマを ZIP ファイルとして配布し、
    管理画面からアップロードして有効化します。テーマ本体は ``/api/v2/*`` API を
    利用する独立した SPA(シングルページアプリケーション)であり、|Fess| 本体の
    JSP には依存しません。新しくテーマを作成する場合は、こちらの方法を推奨します。

JAR テーマプラグイン(レガシー)
    ``view`` / ``css`` / ``js`` / ``images`` を上書きする従来型のプラグインです。
    JAR としてビルドし、プラグインとしてインストールします。既存の JSP ベースの
    画面を部分的に差し替えたい場合に使用します。

.. note::

   静的テーマは |Fess| 15.7 以降で利用できます。15.6 以前を対象とする場合は、
   JAR テーマプラグインを使用してください。検索画面の JSP・CSS・画像を管理画面から
   直接編集する方法については、:doc:`../admin/design-guide` を参照してください。

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
    version: "1.0.0"
    minFessVersion: "15.7"
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
     - 固定値 ``fess.codelibs.org/v1``。
   * - ``kind``
     - 必須
     - 固定値 ``StaticTheme``。
   * - ``name``
     - 必須
     - テーマ名。``^[a-z0-9][a-z0-9_-]{0,63}$`` に一致する必要があります。
       ``themes/`` 配下に展開されるテーマのディレクトリ名(アップロード時は
       この ``name`` から自動的に決まります)、および配信 URL
       (``/themes/<name>/``)に使用されます。
   * - ``displayName``
     - 必須
     - 管理画面に表示される名前。
   * - ``version``
     - 必須
     - セマンティックバージョニング形式(例: ``1.0.0``、``1.2.3-beta.1``)。
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
     - テーマが対応する |Fess| の最小バージョン。
   * - ``supportedLocales``
     - 任意
     - 対応ロケールの一覧(例: ``[en, ja, de]``)。
   * - ``entry``
     - 任意
     - SPA のエントリー HTML。既定値は ``index.html``。
   * - ``spaFallback``
     - 任意
     - SPA フォールバックの有効・無効。既定値は ``true``。

.. note::

   ZIP からアップロードする場合、展開先のディレクトリ名は ``name`` から自動的に
   決まります。``themes/`` ディレクトリに手動でテーマを配置する場合は、ディレクトリ名を
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
- ``spaFallback`` が有効な場合、``/``、``/search``、``/help``、``/error``、
  ``/profile``、``/cache``、``/chat`` の各パスでエントリー HTML(既定は
  ``index.html``)が返され、以降のルーティングは SPA が行います。
- 管理画面(``/admin/*``)、``/api/*``、ログイン画面などは静的テーマの対象外で、
  |Fess| 本体が処理します。
- テーマの SPA は、検索結果やチャットなどのデータを ``/api/v2/*`` API から取得
  します。

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

インストールと有効化
--------------------

1. 管理画面で「システム」→「テーマ」(``/admin/theme/``)を開きます。
2. 作成した ZIP ファイルをアップロードします。
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

JAR テーマプラグイン(レガシー)
================================

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
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>
    </project>

CSS・画像のカスタマイズ
-----------------------

検索画面は Bootstrap ベースの JSP で構成されています。CSS を上書きして配色や
レイアウトを変更したり、``images/logo.png`` を差し替えてロゴを変更したりできます。
対象となるクラス名やマークアップは、実際の JSP(``view/index.jsp`` /
``view/search.jsp`` など)を確認してください。

ビルドとインストール
--------------------

::

    mvn clean package

``target/`` ディレクトリに JAR ファイル(例: ``fess-theme-example-15.8.0.jar``)が
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
- :doc:`../admin/design-guide` - ページのデザイン(JSP・CSS・画像の直接編集)
- :doc:`../admin/plugin-guide` - プラグインのインストール
