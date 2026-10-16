====================
OGNLスクリプトガイド
====================

概要
====

OGNL（Object-Graph Navigation Language）は |Fess| で利用できるスクリプトエンジンの1つです。
``fess-script-ognl`` プラグインとして提供され、識別子は ``ognl`` です。

OGNLのスクリプトは、 ``title + " - " + siteName`` や ``content.length() > 0`` のような
1つの値式です。文、制御構文、 ``return`` はありません。フィールドマッピング、
ドキュメントブースト、パスマッピングなど、短い式で足りる用途に向いています。
文やループが必要なスクリプトには :doc:`scripting-javascript` または :doc:`scripting-groovy` を使用してください。

.. important::
   プラグインは **配布物に同梱されません** 。管理画面の「システム > プラグイン」ページ、
   または ``bin/fess-setup install plugin fess-script-ognl`` でインストールしてください。
   手動でインストールする場合は、JARファイル（例: ``fess-script-ognl-15.10.0.jar`` ）を
   ``app/WEB-INF/plugin/`` に配置し、 |Fess| を再起動します。

OGNLの選択
==========

OGNLは、スクリプトタイプとして明示的に選択した場所でのみ使われます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 場所
     - OGNLの選択方法
   * - データストア
     - データストア設定のパラメーターに ``script_type=ognl`` を追加します
   * - Webクロール・ファイルクロール
     - 設定パラメーターに ``config.script.type=ognl`` を追加し、フィールドのスクリプトを
       ``field.script.<フィールド名>=<式>`` の形式で記述します
   * - ブーストルール
     - ルールのスクリプトタイプを ``ognl`` にします（スクリプトタイプはルールごとに持ちます）
   * - パスマッピング
     - 置換文字列を ``ognl:`` で始めます。式の結果が置換後のURLになり、元のURLと
       ``Matcher`` は ``url`` と ``matcher`` で参照できます
   * - スケジュールジョブ
     - ジョブのスクリプトタイプを ``ognl`` にします。ジョブは通常、手続きを記述するもので、
       1つの式では表現できません

式の書き方
==========

データストアとフィールドのスクリプトは、1行に1つの ``フィールド名=式`` を記述します。
各パラメーターは ``name`` と ``#name`` のどちらでも参照できます。

::

    title=title
    content=content.trim()
    digest=content.length() > 200 ? content.substring(0, 200) + "..." : content

OGNLはGroovyのサブセットではありません。スクリプトを移植するときは次の点に注意してください。

- ``return`` 、文、 ``if`` / ``for`` はありません。三項演算子 ``cond ? a : b`` を使用します。
- エルビス演算子 ``?:`` とセーフナビゲーション演算子 ``?.`` は使えません。
  ``a != null ? a.b : null`` のように記述します。
- ``"x${id}"`` はエラーにならず、展開もされません。リテラル文字列 ``x${id}`` として評価されるため、
  フィールドには誤ったテキストが索引されます。連結には ``+`` を使用してください。

設定
====

エンジンは次のキーを ``system.properties`` 、またはJVMのシステムプロパティ
``-Dfess.system.<キー>`` から読み込みます。両方にある場合は ``system.properties`` が優先されます。
``system.properties`` は、ZIP版では ``app/WEB-INF/conf/system.properties`` 、
RPM版・DEB版では ``/etc/fess/system.properties`` です。

.. important::
   キーは、起動時にエンジンが初期化されるときに1度だけ読み込まれます。
   値を変更したら |Fess| を再起動してください。実行中のプロセスには反映されません。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - キー
     - 既定値
     - 説明
   * - ``script.ognl.mode``
     - ``compat``
     - ``compat`` または ``strict`` 。次のセクションを参照してください。それ以外の値は
       警告をログに出力し、 ``compat`` として扱います
   * - ``script.ognl.allowed.classes``
     - 後述
     - 許可するクラスのカンマ区切りリスト。 ``strict`` モードでのみ使われます
   * - ``script.ognl.denied.packages``
     - 後述
     - 呼び出しを拒否する、宣言クラスのカンマ区切りリスト。 ``strict`` モードでのみ使われます
   * - ``script.ognl.cache.size``
     - ``1000``
     - 解析済みの式をキャッシュする最大数。最小値は ``1`` です
   * - ``script.ognl.expression.max.length``
     - ``4000``
     - 式の最大文字数。これより長い式は評価されず、失敗します。最小値は ``1`` です
   * - ``script.ognl.max.log.length``
     - ``200``
     - ログメッセージに出力する式の最大文字数。最小値は ``3`` です

整数でない値は警告を出して無視され、既定値が使われます。最小値を下回る値は、警告を出して最小値に
引き上げられます。

compatモードとstrictモード
==========================

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - ``compat`` （既定）
     - ``strict``
   * - DIコンテナ
     - ``container`` として参照できます
     - 参照できません（ ``container`` は ``null`` と評価されます）
   * - クラス
     - ``@任意のクラス@メソッド(...)`` で任意のクラスに到達できます
     - ``script.ognl.allowed.classes`` に含まれるクラスにのみ到達できます
   * - メンバー
     - 制限なし
     - ``script.ognl.denied.packages`` のクラスが宣言するメンバーは呼び出せません。
       public でないメンバーは常に拒否されます

``compat`` は既存の設定の動作を維持します。 ``strict`` モードでは、
``@java.lang.System@getProperty("user.name")`` や ``new java.io.File("/etc/hosts")`` のような式は拒否されます。
拒否された式は ``null`` と評価されるのではなく、警告がログに出力され、評価がエラーで失敗します。

エンジンは起動時に、有効なモードを ``INFO`` レベルでログに出力します
（ ``ognl script engine: mode=strict, ...`` ）。 ``strict`` が有効になったかどうかは、この行で確認してください。

許可リスト
----------

``script.ognl.allowed.classes`` は、完全修飾クラス名との完全一致、またはパッケージ名・クラス名に
``.`` を付けた前方一致で判定します。たとえば ``java.time`` は ``java.time.LocalDate`` を含む、
このパッケージ配下のすべてのクラスを許可します。既定値は次のとおりです。

``java.lang.Math`` 、 ``java.lang.String`` 、 ``java.lang.Boolean`` 、 ``java.lang.Integer`` 、
``java.lang.Long`` 、 ``java.lang.Float`` 、 ``java.lang.Double`` 、 ``java.lang.Number`` 、
``java.util.Date`` 、 ``java.util.Arrays`` 、 ``java.util.List`` 、 ``java.util.Map`` 、
``java.util.Set`` 、 ``java.util.Collections`` 、 ``java.math.BigDecimal`` 、 ``java.time`` 、
``org.codelibs.core.lang.StringUtil`` 、 ``org.codelibs.fess.util.DocumentUtil`` 、
``org.codelibs.fess.taglib.FessFunctions``

ネストしたクラスの名前には ``$`` が含まれ（例: ``java.util.Map$Entry`` ）、外側のクラスの名前では
許可されません。必要な場合は、 ``$`` を含む名前をリストに追加してください。

拒否リスト
----------

``script.ognl.denied.packages`` は、メンバーを宣言しているクラスの名前がいずれかのエントリーで
始まる場合に、そのメンバーを拒否します。既定値は次のとおりです。

``java.io`` 、 ``java.nio`` 、 ``java.net`` 、 ``java.lang.reflect`` 、 ``java.lang.invoke`` 、
``java.lang.System`` 、 ``java.lang.Class`` 、 ``java.lang.Runtime`` 、 ``java.lang.ProcessBuilder`` 、
``java.lang.Process`` 、 ``java.lang.Thread`` 、 ``java.lang.ClassLoader`` 、 ``javax.script`` 、
``jdk.`` 、 ``sun.`` 、 ``org.lastaflute.di``

.. note::
   設定した値は既定のリストに追加されるのではなく、置き換えます。許可リストにクラスを1つ追加する場合は、
   既定のエントリーと新しいエントリーを合わせて記述してください。

.. warning::
   ``strict`` モードが制限するのは、式が到達できるクラスとメンバーです。式に渡されるオブジェクトから
   式を隔離するものではありません。 |Fess| のヘルパーやエンティティがパラメーターとして渡された場合、
   どちらのモードでも、そのpublicメソッドを式から呼び出せます。
