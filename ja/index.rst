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

- :doc:`Fess 12.1 <downloads>` (zip/rpm/debパッケージ)

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

-  OCRなどの外部テキスト抽出対応

-  用途に応じて柔軟に対応可能な設計

ニュース
========

2018-02-19
    `Fess 12.1 リリース <https://github.com/codelibs/fess/releases/tag/fess-12.1.0>`__

2018-02-08
    `[連載記事] 簡単導入! OSS全文検索サーバFess入門 第4回 Fessを使って自然言語処理 <https://news.mynavi.jp/itsearch/article/bizapp/3445>`__

2018-02-06
    `Fess 12.0.2 リリース <https://github.com/codelibs/fess/releases/tag/fess-12.0.2>`__

2018-02-04
    `Fess 11.4.8 リリース <https://github.com/codelibs/fess/releases/tag/fess-11.4.8>`__

2018-01-18
    `Fess 11.4.7 リリース <https://github.com/codelibs/fess/releases/tag/fess-11.4.7>`__

2018-01-16
    `Fess 12.0.1 リリース <https://github.com/codelibs/fess/releases/tag/fess-12.0.1>`__

2018-01-02
    `Fess 12.0 リリース <https://github.com/codelibs/fess/releases/tag/fess-12.0.0>`__

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


Google Site Searchからの移行
----------------------------

Google Site Search(GSS)は2018年4月1日までにサービスを終了します。
CodeLibsプロジェクトでは `Fess Site Search(FSS) <https://fss-generator.codelibs.org/ja/>`__ を提供しています。
FSSで提供しているJavaScriptを利用することで、既存のJavaScriptを置き換えるだけでFessへ移行できます。
安価なFessサーバが必要な場合は、 `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ をご覧ください。

掲載メディア
============

- `[IT Search+] 【第4回】Fessを使って自然言語処理 <https://news.mynavi.jp/itsearch/article/bizapp/3445>`__

- `[IT Search+] 【第3回】設定だけでできるWebスクレイピング <https://news.mynavi.jp/itsearch/article/bizapp/3341>`__

- `[IT Search+] 【第2回】Google Site Searchからの簡単移行 <https://news.mynavi.jp/itsearch/article/bizapp/3260>`__

- `[IT Search+] 【第1回】全文検索サーバFessを導入しよう <https://news.mynavi.jp/itsearch/article/bizapp/3154>`__

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

