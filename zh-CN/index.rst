===================================
开源全文搜索服务器 Fess
===================================

概述
====

Fess 是一个"**可在5分钟内轻松构建的全文搜索服务器**"。

.. figure:: ../resources/images/ja/demo-1.png
   :scale: 100%
   :alt: 标准演示
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   标准演示

.. figure:: ../resources/images/ja/demo-3.png
   :scale: 100%
   :alt: 站内搜索演示
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   站内搜索演示

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: Code Search
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   源代码搜索

.. figure:: ../resources/images/ja/demo-4.png
   :scale: 100%
   :alt: Document Search
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   文档搜索

只要有 Java 或 Docker 运行环境，就可以在任何操作系统上运行。
Fess 采用 Apache 许可证提供，可以免费使用（自由软件）。


下载
============

- :doc:`Fess 15.3.0 <downloads>` (zip/rpm/deb包)

特点
====

-  采用 Apache 许可证提供（自由软件，可免费使用）

-  可爬取 Web、文件系统、Windows 共享文件夹、数据库

-  支持 MS Office（Word/Excel/PowerPoint）和 PDF 等多种文件格式

-  操作系统独立（基于 Java 构建）

-  提供用于集成到现有站点的 JavaScript

-  使用 OpenSearch 或 Elasticsearch 作为搜索引擎

-  可搜索 BASIC/DIGEST/NTLM/FORM 认证的站点

-  可根据登录状态区分搜索结果

-  使用 ActiveDirectory 或 SAML 等进行单点登录（SSO）

-  与地图信息联动的位置信息搜索

-  可在浏览器上配置爬取目标和编辑搜索页面等

-  通过标签对搜索结果进行分类

-  添加请求头信息、重复域名设置、搜索结果路径转换

-  可通过 JSON 格式输出搜索结果与外部系统集成

-  统计搜索日志和点击日志

-  支持 Facet（分面）和 Drill-down（向下钻取）

-  自动补全和建议功能

-  用户词典和同义词词典编辑功能

-  搜索结果缓存显示功能和缩略图显示功能

-  搜索结果代理功能

-  支持智能手机（响应式网页设计）

-  通过访问令牌与外部系统集成

-  支持 OCR 等外部文本提取

-  可根据用途灵活应对的设计

新闻
========

2025-10-25
    `Fess 15.3.0 发布 <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Fess 15.2.0 发布 <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Fess 15.1.0 发布 <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

2025-06-22
    `Fess 15.0.0 发布 <https://github.com/codelibs/fess/releases/tag/fess-15.0.0>`__

2025-05-24
    `Fess 14.19.2 发布 <https://github.com/codelibs/fess/releases/tag/fess-14.19.2>`__

过去的新闻请查看 :doc:`这里 <news>`。

论坛
==========

如有任何问题，请访问 `论坛 <https://discuss.codelibs.org/c/FessJA/>`__。

商业支持
============

Fess 是采用 Apache 许可证提供的开源产品，个人和商业用途均可免费使用。

如需 Fess 的定制、导入、构建等支持服务，请参阅\ `商业支持（收费） <https://www.n2sm.net/products/n2search.html>`__。
此外，商业支持还提供搜索质量和爬取速度改善等性能调优服务。

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (优化的 Fess 商业包)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (Google Site Search 替代服务)

- :doc:`各种支持服务 <support-services>`


Fess Site Search
================

CodeLibs 项目提供 `Fess Site Search(FSS) <https://fss-generator.codelibs.org/ja/>`__。
只需在现有站点中放置 JavaScript，即可嵌入 Fess 的搜索页面。
使用 FSS 可以轻松从 Google Site Search 或 Yahoo! 搜索定制服务迁移。
如需价格实惠的 Fess 服务器，请参阅 `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__。

Data Store 插件
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

Theme 插件
===============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Ingester 插件
==================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Script 插件
==================

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

相关项目
================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__

媒体报道
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


