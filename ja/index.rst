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
   :target: http://search.n2sm.co.jp/

   標準デモ

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: サイト内検索デモ
   :figclass: side-by-side
   :target: http://demo.n2search.net/aspdemo/

   サイト内検索デモ

.. figure:: ../resources/images/ja/demo-3.png
   :scale: 100%
   :alt: EC向け商品検索デモ
   :figclass: side-by-side
   :target: http://demo.n2search.net/ecdemo/

   EC向け商品検索デモ

特徴
====

-  Apache ライセンスで提供 (フリーソフトなので、無料で利用可能)

-  Web、ファイルシステム、Windows共有フォルダ、データベースをクロール

-  MS Office(Word/Excel/PowerPoint) や PDF など多くのファイル形式に対応

-  OS 非依存 (Java ベースで構築)

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

-  用途に応じて柔軟に対応可能な設計

ニュース
========

2017-07-05
    `Google Site Searchからの移行に対応したFess Site Searchを提供 <http://fess.codelibs.org/ja/11.2/api/api-ss.html>`__

2017-06-30
    `Fess 11.2.1 リリース <https://github.com/codelibs/fess/releases/tag/fess-11.2.1>`__

2017-06-15
    `Fess 11.2 リリース <https://github.com/codelibs/fess/releases/tag/fess-11.2.0>`__

過去のニュースは\ `こちら <news.html>`__\ をご覧ください。

ダウンロード
============

ダウンロードについては\ `こちら <downloads.html>`__\ をご覧ください。

商用サポート
============

|Fess| は Apache ライセンスで提供されるオープンソース製品で、個人や商用向けでも無料でご自由にご利用いただけます。

|Fess| のカスタマイズや導入・構築などのサポートサービスが必要な場合は、\ `商用サポート(有償) <http://www.n2sm.net/products/n2search.html>`__\ をご覧ください。
また、検索品質やクロールが遅いなどのパフォーマンスチューニングも商用サポートで対応しています。
詳しくは、 `こちら <support-services.html>`__ を参照してください。

N2 Search
---------

企業内検索などの用途に最適化されたパッケージ製品として、N2 Searchも販売しています。
N2 Searchでは、約25万語の辞書のバンドルやセキュリティ観点の強化等が行われています。

|image3|

N2 Search on AWS Marketplace
----------------------------

N2 Search (商用版Fessの試用版)を AWS Marketplace で無料でご利用いただくことができます(EC2のインスタンス料金は別途かかります)。 `N2 Search <https://aws.amazon.com/marketplace/pp/B014JFU5EW>`__ をご覧ください。


.. |image0| image:: ../resources/images/ja/demo-1.png
.. |image1| image:: ../resources/images/ja/demo-2.png
.. |image2| image:: ../resources/images/ja/demo-3.png
.. |image3| image:: ../resources/images/ja/n2search_225x50.png
   :target: http://www.n2sm.net/products/n2search.html
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

