============================================================
第3回 社内ポータルに検索を埋め込む -- 既存Webサイトへの検索機能追加シナリオ
============================================================

はじめに
========

前回は Docker Compose で Fess を起動し、検索を体験しました。
しかし、実際の業務では「Fess の検索画面をそのまま使う」だけでなく、「既存の社内サイトやポータルに検索機能を追加したい」というニーズが多くあります。

本記事では、既存の Web サイトに Fess の検索機能を組み込むための3つのアプローチを紹介し、それぞれの特徴と選択基準を解説します。

対象読者
========

- 社内ポータルや Web サイトに検索機能を追加したい方
- フロントエンド開発の基本知識がある方
- 第2回の手順で Fess が起動済みであること

必要な環境
==========

- 第2回で構築した Fess 環境（Docker Compose）
- テスト用の Web ページ（ローカルの HTML ファイルでも可）

3つの統合アプローチ
====================

Fess の検索機能を既存サイトに組み込む方法は、大きく3つあります。

.. list-table:: 統合アプローチの比較
   :header-rows: 1
   :widths: 15 30 25 30

   * - アプローチ
     - 概要
     - 開発工数
     - 適しているケース
   * - FSS（Fess Site Search）
     - JavaScript タグを埋め込むだけ
     - 最小（数行のコード）
     - 手軽に検索を追加したい場合
   * - 検索フォーム連携
     - HTML フォームから Fess に遷移
     - 小（HTML の修正のみ）
     - Fess の検索画面をそのまま使いたい場合
   * - 検索 API 連携
     - JSON API でカスタム UI を構築
     - 中〜大（フロントエンド開発）
     - デザインや動作を完全にカスタマイズしたい場合

それぞれの方法を、具体的なシナリオとともに解説していきます。

アプローチ1: FSS（Fess Site Search）で手軽に追加
==================================================

シナリオ
--------

社内ポータルサイトがあり、HTML の編集権限はあるが、大きな改修は避けたい。
最小限の変更で、ポータル上から社内ドキュメントを検索できるようにしたい。

FSS とは
--------

Fess Site Search（FSS）は、JavaScript タグを Web ページに埋め込むだけで検索機能を追加できる仕組みです。
検索窓と検索結果の表示がすべて JavaScript で処理されるため、既存のページ構造をほとんど変更する必要がありません。

実装手順
--------

1. Fess 管理画面で API のアクセスを許可します。
   ［システム］ > ［全般］ のページ内で、JSON レスポンスを有効にしておきます。

2. 検索機能を追加したいページに、以下のコードを埋め込みます。

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

``<fess:search>`` タグを配置した場所に、検索窓と検索結果が表示されます。

カスタマイズ
------------

FSS の見た目は CSS でカスタマイズできます。
Fess が提供するデフォルトのスタイルを上書きすることで、既存サイトのデザインに合わせることが可能です。

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

アプローチ2: 検索フォーム連携でシンプルに実現
================================================

シナリオ
--------

社内ポータルにはすでにヘッダーにナビゲーションバーがある。
そこに検索窓を追加し、検索実行時に Fess の検索結果画面に遷移させたい。
JavaScript は使わず、HTML だけで実現したい。

実装手順
--------

既存のナビゲーションバーに、以下のような HTML フォームを追加します。

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="社内検索..." />
      <button type="submit">検索</button>
    </form>

これだけで、検索実行時に Fess の検索結果画面へ遷移します。
Fess 側の検索画面のデザインをカスタマイズすることで、統一感のある体験を提供できます。

Fess の検索画面カスタマイズ
----------------------------

Fess の検索画面は JSP ファイルで構成されており、管理画面からも編集可能です。

1. 管理画面の ［システム］ > ［ページのデザイン］ を選択
2. ヘッダー、フッター、CSS などをカスタマイズ

例えば、ロゴを社内ポータルと合わせたり、配色を統一したりすることで、利用者にとって違和感のない検索体験を提供できます。

パスマッピングの活用
--------------------

検索結果に表示される URL を、利用者がアクセスしやすい URL に変換できます。
例えば、クロール時の URL が ``http://internal-server:8888/docs/`` であっても、検索結果には ``https://portal.example.com/docs/`` と表示させることが可能です。

管理画面の ［クローラー］ > ［パスマッピング］ から設定できます。

アプローチ3: 検索 API で完全カスタム
======================================

シナリオ
--------

社内の業務アプリケーション内に検索機能を組み込みたい。
デザインや検索結果の表示方法を完全にコントロールしたい。
フロントエンドの開発リソースがある。

検索 API の基本
----------------

Fess は JSON ベースの検索 API を提供しています。

::

    GET http://localhost:8080/api/v1/documents?q=検索キーワード

レスポンスは以下のような JSON 形式です。

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "ドキュメントタイトル",
          "url": "https://example.com/doc.html",
          "content_description": "...検索キーワードを含む本文の抜粋..."
        }
      ]
    }

JavaScript での実装例
----------------------

以下は、検索 API を使った基本的な実装例です。

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

API の追加パラメータ
---------------------

検索 API は、様々なパラメータで検索動作をカスタマイズできます。

.. list-table:: 主な API パラメータ
   :header-rows: 1
   :widths: 20 50 30

   * - パラメータ
     - 説明
     - 例
   * - ``q``
     - 検索キーワード
     - ``q=Fess``
   * - ``num``
     - 1ページあたりの表示件数
     - ``num=20``
   * - ``start``
     - 検索結果の開始位置
     - ``start=20``
   * - ``fields.label``
     - ラベルによる絞り込み
     - ``fields.label=intranet``
   * - ``sort``
     - ソート順
     - ``sort=last_modified.desc``

API を活用することで、検索結果のフィルタリング、ソート、ページネーションなど、きめ細かな制御が可能です。

どのアプローチを選ぶか
========================

3つのアプローチは、状況に応じて選択します。

**FSS を選ぶ場合**

- 開発リソースが限られている
- 既存ページに最小限の変更で検索を追加したい
- 検索機能の見た目は標準的なもので十分

**検索フォーム連携を選ぶ場合**

- Fess の検索画面のデザインで十分
- JavaScript を使いたくない
- ヘッダーやサイドバーに検索窓を追加するだけでよい

**検索 API を選ぶ場合**

- 検索結果の表示を完全にカスタマイズしたい
- SPA（Single Page Application）に組み込みたい
- 検索結果に独自のロジック（フィルタリング、ハイライト等）を適用したい
- フロントエンド開発のリソースがある

組み合わせも可能
----------------

これらのアプローチは排他的ではありません。
例えば、トップページには FSS で手軽に検索機能を追加し、専用の検索ページでは API を使ったカスタム UI を提供する、という組み合わせも有効です。

まとめ
======

本記事では、既存の Web サイトに Fess の検索機能を組み込む3つのアプローチを紹介しました。

- **FSS**: JavaScript タグの埋め込みだけで検索機能を追加
- **検索フォーム連携**: HTML フォームから Fess の検索画面に遷移
- **検索 API**: JSON API で完全にカスタマイズされた検索体験を構築

どのアプローチでも、Fess のバックエンドが提供する検索品質はそのまま活用できます。
要件と開発リソースに応じて、最適な方法を選択してください。

次回は、ファイルサーバーやクラウドストレージなど複数のデータソースを一元的に検索するシナリオを扱います。

参考資料
========

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `Fess 検索 API <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
