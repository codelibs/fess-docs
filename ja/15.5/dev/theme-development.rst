==================================
テーマ開発ガイド
==================================

概要
====

|Fess| のテーマシステムを使用して、検索画面のデザインをカスタマイズできます。
テーマはプラグインとして配布でき、複数のテーマを切り替えて使用できます。

テーマ構造
==========

::

    fess-theme-example/
    ├── pom.xml
    └── src/main/resources/
        └── theme/example/
            ├── css/
            │   ├── style.css
            │   └── custom.css
            ├── js/
            │   └── custom.js
            ├── images/
            │   └── logo.png
            └── templates/
                └── search.html

基本的なテーマ作成
==================

CSSカスタマイズ
---------------

``css/style.css``:

.. code-block:: css

    /* ヘッダーのカスタマイズ */
    .navbar {
        background-color: #1a237e;
    }

    /* 検索ボックスのスタイル */
    .search-box {
        border-radius: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* 検索結果のスタイル */
    .search-result-item {
        border-left: 3px solid #1a237e;
        padding-left: 15px;
    }

ロゴの変更
----------

1. カスタムロゴを ``images/logo.png`` に配置
2. CSSでロゴを参照:

.. code-block:: css

    .logo img {
        content: url("../images/logo.png");
        max-height: 40px;
    }

テンプレートのカスタマイズ
--------------------------

テンプレートはJSP形式です。

``templates/search.html`` (一部):

.. code-block:: html

    <div class="search-header">
        <h1>カスタム検索ポータル</h1>
        <p>社内ドキュメントを検索</p>
    </div>

テーマの登録
============

pom.xml
-------

.. code-block:: xml

    <groupId>org.codelibs.fess</groupId>
    <artifactId>fess-theme-example</artifactId>
    <version>15.5.0</version>
    <packaging>jar</packaging>

設定ファイル
------------

``src/main/resources/theme.properties``:

::

    theme.name=example
    theme.display.name=Example Theme
    theme.version=1.0.0

インストール
============

::

    ./bin/fess-plugin install fess-theme-example

管理画面からテーマを選択:

1. 「システム」→「デザイン」
2. テーマを選択
3. 保存して適用

既存テーマの例
==============

- `fess-theme-simple <https://github.com/codelibs/fess-theme-simple>`__
- `fess-theme-minimal <https://github.com/codelibs/fess-theme-minimal>`__

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
- :doc:`../admin/design-guide` - デザイン設定ガイド
