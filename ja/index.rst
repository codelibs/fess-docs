=====================================
オープンソース全文検索サーバー |Fess|
=====================================

概要
====

|Fess| (フェス) は「\ **5 分で簡単に構築可能な全文検索サーバー**\ 」です。
Java 実行環境があればどの OS でも実行可能です。
|Fess| は Apache ライセンスで提供され、無料 (フリーソフト) でご利用いただけます。

.. figure:: ../resources/images/ja/demo-1.png
   :scale: 100%
   :alt: 標準デモ
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   標準デモ

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: サイト内検索デモ
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   サイト内検索デモ

ダウンロード
============

- :doc:`Fess 12.3.2 <downloads>` (zip/rpm/debパッケージ)

特徴
====

-  Apache ライセンスで提供 (フリーソフトなので、無料で利用可能)

-  Web、ファイルシステム、Windows共有フォルダ、データベースをクロール

-  MS Office(Word/Excel/PowerPoint) や PDF など多くのファイル形式に対応

-  OS 非依存 (Java ベースで構築)

-  既存サイトへの組み込み用JavaScriptの提供

-  Elasticsearch を検索エンジンとして利用

-  BASIC/DIGEST/NTLM/FORM認証のサイトも検索可能

-  ログイン状態により検索結果の出し分けが可能
   (ActiveDirectoryなど、シングルサイオン環境での利用可能)

-  地図情報と連携したジオサーチ

-  ブラウザ上でクロール対象設定や検索画面編集など可能

-  検索結果をラベル付けにより分類

-  リクエストヘッダーに情報付加、重複ドメインの設定、検索結果のパス変換

-  JSON形式で検索結果出力により外部システムとの連携が可能

-  検索ログおよびクリックログの集計

-  ファセット・ドリルダウン対応

-  オートコンプリート・サジェスト機能

-  ユーザー辞書および同義語辞書編集機能

-  検索結果のキャッシュ表示機能とスクリーンショット表示機能

-  検索結果のプロキシ機能

-  スマートフォン対応 (Responsive Web Design)

-  アクセストークンにより外部システム連携

-  Learning To Rankサポート

-  OCRなどの外部テキスト抽出対応

-  用途に応じて柔軟に対応可能な設計

ニュース
========

2018-11-01
    `Fess 12.2.3 <https://github.com/codelibs/fess/releases/tag/fess-12.2.3>`__ リリース

2018-10-09
    `Fess 12.3.2 <https://github.com/codelibs/fess/releases/tag/fess-12.3.2>`__ リリース

2018-09-24
    `Fess 12.3.1 <https://github.com/codelibs/fess/releases/tag/fess-12.3.1>`__ リリース

2018-09-23
    `Fess 12.2.2 <https://github.com/codelibs/fess/releases/tag/fess-12.2.2>`__ リリース

2018-09-04
    `Fess 12.3 <https://github.com/codelibs/fess/releases/tag/fess-12.3.0>`__ リリース

2018-09-01
    `Fess 12.2.1 <https://github.com/codelibs/fess/releases/tag/fess-12.2.1>`__ リリース

2018-08-09
    `Fess 12.2.0 <https://github.com/codelibs/fess/releases/tag/fess-12.2.0>`__ リリース

2018-07-27
    `Fess 12.1.5 <https://github.com/codelibs/fess/releases/tag/fess-12.1.5>`__ リリース

過去のニュースは :doc:`こちら <news>` をご覧ください。

商用サポート
============

|Fess| は Apache ライセンスで提供されるオープンソース製品で、個人や商用向けでも無料でご自由にご利用いただけます。

|Fess| のカスタマイズや導入・構築などのサポートサービスが必要な場合は、\ `商用サポート(有償) <https://www.n2sm.net/products/n2search.html>`__\ をご覧ください。
また、検索品質やクロールが遅いなどのパフォーマンスチューニングも商用サポートで対応しています。

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (最適化されたFessの商用向けパッケージ)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (Google Site Search代替サービス)

- `N2 Search on AWS Marketplace <https://aws.amazon.com/marketplace/pp/B014JFU5EW>`__ (AWSのAMI)

- :doc:`各種サポートサービス <support-services>`


Fess Site Search
================

CodeLibsプロジェクトでは `Fess Site Search(FSS) <https://fss-generator.codelibs.org/ja/>`__ を提供しています。
既存のサイトにJavaScriptを配置するだけで、Fessの検索ページを組み込むことができます。
FSSを利用することで、Google Site Search(GSS)やGoogle Custom Searchからの移行も簡単にできます。
安価なFessサーバが必要な場合は、 `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ をご覧ください。

X-Pack対応
==========

FessでのX-Pack対応については `fess-xpack <https://github.com/codelibs/fess-xpack>`__ を参照してください。
サポートが必要な場合は、 `商用サポート(有償) <https://www.n2sm.net/products/n2search.html>`__ をご利用ください。


掲載メディア
============

- `【第6回】日本語の全文検索でのAnalyzer <https://news.mynavi.jp/itsearch/article/devsoft/3671>`__

- `【第5回】全文検索のトークナイズ処理 <https://news.mynavi.jp/itsearch/article/devsoft/3539>`__

- `【第4回】Fessを使って自然言語処理 <https://news.mynavi.jp/itsearch/article/bizapp/3445>`__

- `【第3回】設定だけでできるWebスクレイピング <https://news.mynavi.jp/itsearch/article/bizapp/3341>`__

- `【第2回】Google Site Searchからの簡単移行 <https://news.mynavi.jp/itsearch/article/bizapp/3260>`__

- `【第1回】全文検索サーバFessを導入しよう <https://news.mynavi.jp/itsearch/article/bizapp/3154>`__

.. |image0| image:: ../resources/images/ja/demo-1.png
.. |image1| image:: ../resources/images/ja/demo-2.png
.. |image2| image:: ../resources/images/ja/demo-3.png
.. |image3| image:: ../resources/images/ja/n2search_225x50.png
   :target: https://www.n2sm.net/products/n2search.html
.. |image4| image:: ../resources/images/ja/n2search_b.png


.. hidden toctree

.. toctree::
   :maxdepth: 3
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives

