===================================
オープンソース全文検索サーバー Fess
===================================

概要
====

Fess (フェス) は「\ **5 分で簡単に構築可能な全文検索サーバー**\ 」です。

.. figure:: ../resources/images/ja/demo-1.png
   :scale: 100%
   :alt: 標準デモ
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   標準デモ

.. figure:: ../resources/images/ja/demo-3.png
   :scale: 100%
   :alt: サイト内検索デモ
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   サイト内検索デモ

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: Code Search
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   ソースコード検索

.. figure:: ../resources/images/ja/demo-4.png
   :scale: 100%
   :alt: Document Search
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   ドキュメント検索

JavaまたはDockerの実行環境があればどの OS でも実行可能です。
Fess は Apache ライセンスで提供され、無料 (フリーソフト) でご利用いただけます。


ダウンロード
============

- :doc:`Fess 14.16.0 <downloads>` (zip/rpm/debパッケージ)

特徴
====

-  Apache ライセンスで提供 (フリーソフトなので、無料で利用可能)

-  Web、ファイルシステム、Windows共有フォルダ、データベースをクロール

-  MS Office(Word/Excel/PowerPoint) や PDF など多くのファイル形式に対応

-  OS 非依存 (Java ベースで構築)

-  既存サイトへの組み込み用JavaScriptの提供

-  OpenSearchまたはElasticsearchを検索エンジンとして利用

-  BASIC/DIGEST/NTLM/FORM認証のサイトも検索可能

-  ログイン状態により検索結果の出し分けが可能

-  ActiveDirectoryやSAMLなどを用いたシングルサイオン(SSO)

-  地図情報と連携した位置情報検索

-  ブラウザ上でクロール対象設定や検索画面編集など可能

-  検索結果をラベル付けにより分類

-  リクエストヘッダーに情報付加、重複ドメインの設定、検索結果のパス変換

-  JSON形式で検索結果出力により外部システムとの連携が可能

-  検索ログおよびクリックログの集計

-  ファセット・ドリルダウン対応

-  オートコンプリート・サジェスト機能

-  ユーザー辞書および同義語辞書編集機能

-  検索結果のキャッシュ表示機能とサムネイル表示機能

-  検索結果のプロキシ機能

-  スマートフォン対応 (Responsive Web Design)

-  アクセストークンにより外部システム連携

-  OCRなどの外部テキスト抽出対応

-  用途に応じて柔軟に対応可能な設計

ニュース
========

2024-08-11
    `Fess 14.16.0 リリース <https://github.com/codelibs/fess/releases/tag/fess-14.16.0>`__

2024-07-02
    `Fess 14.15.0 リリース <https://github.com/codelibs/fess/releases/tag/fess-14.15.0>`__

2024-05-27
    `Fess 14.14.0 リリース <https://github.com/codelibs/fess/releases/tag/fess-14.14.0>`__

2024-04-14
    `Fess 14.13.0 リリース <https://github.com/codelibs/fess/releases/tag/fess-14.13.0>`__

2024-02-24
    `Fess 14.12.0 リリース <https://github.com/codelibs/fess/releases/tag/fess-14.12.0>`__

過去のニュースは :doc:`こちら <news>` をご覧ください。

フォーラム
==========

質問などがあれば、 `フォーラム <https://discuss.codelibs.org/c/FessJA/>`__ をご利用ください。

商用サポート
============

Fess は Apache ライセンスで提供されるオープンソース製品で、個人や商用向けでも無料でご自由にご利用いただけます。

Fess のカスタマイズや導入・構築などのサポートサービスが必要な場合は、\ `商用サポート(有償) <https://www.n2sm.net/products/n2search.html>`__\ をご覧ください。
また、検索品質やクロール速度の改善などのパフォーマンスチューニングも商用サポートで対応しています。

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (最適化されたFessの商用向けパッケージ)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (Google Site Search代替サービス)

- :doc:`各種サポートサービス <support-services>`


Fess Site Search
================

CodeLibsプロジェクトでは `Fess Site Search(FSS) <https://fss-generator.codelibs.org/ja/>`__ を提供しています。
既存のサイトにJavaScriptを配置するだけで、Fessの検索ページを組み込むことができます。
FSSを利用することで、Google Site SearchやYahoo!検索カスタムサーチからの移行も簡単にできます。
安価なFessサーバが必要な場合は、 `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ をご覧ください。

Data Storeプラグイン
====================

- `Confluence/Jira <https://github.com/codelibs/fess-ds-atlassian>`__
- `Box <https://github.com/codelibs/fess-ds-box>`__
- `CSV <https://github.com/codelibs/fess-ds-csv>`__
- `Database <https://github.com/codelibs/fess-ds-db>`__
- `Dropbox <https://github.com/codelibs/fess-ds-dropbox>`__
- `Elasticsearch <https://github.com/codelibs/fess-ds-elasticsearch>`__
- `Git <https://github.com/codelibs/fess-ds-git>`__
- `Gitbucket <https://github.com/codelibs/fess-ds-gitbucket>`__
- `G Suite <https://github.com/codelibs/fess-ds-gsuite>`__
- `JSON <https://github.com/codelibs/fess-ds-json>`__
- `Office 365 <https://github.com/codelibs/fess-ds-office365>`__
- `S3 <https://github.com/codelibs/fess-ds-s3>`__
- `Salesforce <https://github.com/codelibs/fess-ds-salesforce>`__
- `SharePoint <https://github.com/codelibs/fess-ds-sharepoint>`__
- `Slack <https://github.com/codelibs/fess-ds-slack>`__

Themeプラグイン
===============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Ingesterプラグイン
==================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Scriptプラグイン
==================

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

関連プロジェクト
================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__

掲載メディア
============

- `【第48回】SAMLによるシングルサインオン <https://news.mynavi.jp/techplus/article/_ossfess-48/>`__

- `【第47回】MinIOでストレージ管理とクロール <https://news.mynavi.jp/techplus/article/_ossfess-47/>`__

- `【第46回】Amazon S3のクロール <https://news.mynavi.jp/techplus/article/_ossfess-46/>`__

- `【第45回】Compose V2での起動方法 <https://news.mynavi.jp/techplus/article/_ossfess-45/>`__

- `【第44回】FessでOpenSearchを使用する <https://news.mynavi.jp/techplus/article/_ossfess-44/>`__

- `【第43回】Elasticsearch 8の利用方法 <https://news.mynavi.jp/techplus/article/_ossfess-43/>`__

- `【第42回】アクセストークンを使った検索APIの利用方法 <https://news.mynavi.jp/techplus/article/_ossfess-42/>`__

- `【第41回】Microsoft Teamsのクロール <https://news.mynavi.jp/itsearch/article/bizapp/5880>`__

- `【第40回】各種機能の設定方法（ドキュメントブースト、関連コンテンツ、関連クエリー） <https://news.mynavi.jp/itsearch/article/bizapp/5804>`__

- `【第39回】各種機能の設定方法（パスマッピング、リクエストヘッダー、重複ホスト） <https://news.mynavi.jp/itsearch/article/bizapp/5686>`__

- `【第38回】各種機能の設定方法（ラベル、キーマッチ） <https://news.mynavi.jp/itsearch/article/bizapp/5646>`__

- `【第37回】AWS Elasticsearch Serviceの利用方法 <https://news.mynavi.jp/itsearch/article/devsoft/5557>`__

- `【第36回】Elastic Cloudの利用方法 <https://news.mynavi.jp/itsearch/article/devsoft/5507>`__

- `【第35回】SharePoint Serverのクロール <https://news.mynavi.jp/itsearch/article/devsoft/5457>`__

- `【第34回】OpenID Connectでの認証方法 <https://news.mynavi.jp/itsearch/article/devsoft/5338>`__

- `【第33回】入力支援環境の構築方法 <https://news.mynavi.jp/itsearch/article/devsoft/5292>`__

- `【第32回】インデックスの管理 <https://news.mynavi.jp/itsearch/article/devsoft/5233>`__

- `【第31回】Office 365のクロール <https://news.mynavi.jp/itsearch/article/bizapp/5180>`__

- `【第30回】Azure ADでの認証方法 <https://news.mynavi.jp/itsearch/article/bizapp/5136>`__

- `【第29回】Dockerでの使い方 <https://news.mynavi.jp/itsearch/article/devsoft/5058>`__

- `【第28回】ログファイルの参照方法 <https://news.mynavi.jp/itsearch/article/devsoft/5032>`__

- `【第27回】Fessのクラスタ化 <https://news.mynavi.jp/itsearch/article/devsoft/4994>`__

- `【第26回】位置情報の検索 <https://news.mynavi.jp/itsearch/article/devsoft/4963>`__

- `【第25回】Tesseract OCRを利用する <https://news.mynavi.jp/itsearch/article/devsoft/4928>`__

- `【第24回】GitBucketのクロール <https://news.mynavi.jp/itsearch/article/devsoft/4924>`__

- `【第23回】サジェスト機能の使い方 <https://news.mynavi.jp/itsearch/article/bizapp/4890>`__

- `【第22回】Dropboxのクロール <https://news.mynavi.jp/itsearch/article/bizapp/4844>`__

- `【第21回】Slackのメッセージのクロール <https://news.mynavi.jp/itsearch/article/bizapp/4808>`__

- `【第20回】検索ログを可視化する <https://news.mynavi.jp/itsearch/article/devsoft/4781>`__

- `【第19回】CSVファイルのクロール <https://news.mynavi.jp/itsearch/article/devsoft/4761>`__

- `【第18回】Google Driveのクロール <https://news.mynavi.jp/itsearch/article/devsoft/4732>`__

- `【第17回】データベースのクロール <https://news.mynavi.jp/itsearch/article/devsoft/4659>`__

- `【第16回】検索APIの利用方法 <https://news.mynavi.jp/itsearch/article/devsoft/4613>`__

- `【第15回】認証が必要なファイルサーバのクロール <https://news.mynavi.jp/itsearch/article/devsoft/4569>`__

- `【第14回】管理用APIの使い方 <https://news.mynavi.jp/itsearch/article/devsoft/4514>`__

- `【第13回】検索結果にサムネイル画像を表示する方法 <https://news.mynavi.jp/itsearch/article/devsoft/4456>`__

- `【第12回】仮想ホスト機能の使い方 <https://news.mynavi.jp/itsearch/article/devsoft/4394>`__

- `【第11回】Fessでシングルサインオン <https://news.mynavi.jp/itsearch/article/devsoft/4357>`__

- `【第10回】Windows環境での構築方法 <https://news.mynavi.jp/itsearch/article/bizapp/4320>`__

- `【第9回】FessでActive Directory連携 <https://news.mynavi.jp/itsearch/article/bizapp/4283>`__

- `【第8回】ロールベース検索 <https://news.mynavi.jp/itsearch/article/hardware/4201>`__

- `【第7回】認証のあるサイトのクロール <https://news.mynavi.jp/itsearch/article/hardware/4158>`__

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


.. toctree::
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives


