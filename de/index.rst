===================================
Open Source Volltextsuchserver Fess
===================================

Überblick
=========

Fess ist ein **"in 5 Minuten einfach zu erstellender Volltextsuchserver"**.

.. figure:: ../resources/images/ja/demo-1.png
   :scale: 100%
   :alt: Standard-Demo
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   Standard-Demo

.. figure:: ../resources/images/ja/demo-3.png
   :scale: 100%
   :alt: Site-Suche Demo
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   Site-Suche Demo

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: Code Search
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   Quellcode-Suche

.. figure:: ../resources/images/ja/demo-4.png
   :scale: 100%
   :alt: Document Search
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   Dokumentensuche

Fess kann auf jedem Betriebssystem ausgeführt werden, auf dem Java oder Docker verfügbar ist.
Fess wird unter der Apache-Lizenz bereitgestellt und ist kostenlos (Freeware) nutzbar.


Download
========

- :doc:`Fess 15.3.0 <downloads>` (zip/rpm/deb-Pakete)

Funktionen
==========

-  Bereitstellung unter Apache-Lizenz (kostenlose Nutzung als Freeware)

-  Crawling von Web, Dateisystemen, Windows-Freigabeordnern und Datenbanken

-  Unterstützung vieler Dateiformate wie MS Office (Word/Excel/PowerPoint) und PDF

-  Betriebssystemunabhängig (Java-basiert)

-  Bereitstellung von JavaScript zur Integration in bestehende Websites

-  Verwendung von OpenSearch oder Elasticsearch als Suchmaschine

-  Durchsuchbar auch für Sites mit BASIC/DIGEST/NTLM/FORM-Authentifizierung

-  Unterschiedliche Suchergebnisse je nach Anmeldestatus möglich

-  Single Sign-On (SSO) mit Active Directory, SAML usw.

-  Standortbasierte Suche in Verbindung mit Karteninformationen

-  Konfiguration von Crawl-Zielen und Bearbeitung der Suchoberfläche im Browser möglich

-  Klassifizierung von Suchergebnissen durch Labeling

-  Hinzufügen von Informationen zu Anfrage-Headern, Konfiguration doppelter Domains, Pfadkonvertierung von Suchergebnissen

-  Integration mit externen Systemen durch Ausgabe von Suchergebnissen im JSON-Format

-  Aggregation von Suchprotokollen und Klickprotokollen

-  Unterstützung von Facetten und Drill-Down

-  Autovervollständigungs- und Vorschlagsfunktionen

-  Bearbeitungsfunktion für Benutzerwörterbücher und Synonymwörterbücher

-  Cache-Anzeigefunktion und Miniaturbildanzeigefunktion für Suchergebnisse

-  Proxy-Funktion für Suchergebnisse

-  Unterstützung für Smartphones (Responsive Web Design)

-  Integration externer Systeme durch Zugangstoken

-  Unterstützung für externe Textextraktion wie OCR

-  Flexibles Design je nach Verwendungszweck

Nachrichten
===========

2025-10-25
    `Fess 15.3.0 Release <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Fess 15.2.0 Release <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Fess 15.1.0 Release <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

2025-06-22
    `Fess 15.0.0 Release <https://github.com/codelibs/fess/releases/tag/fess-15.0.0>`__

2025-05-24
    `Fess 14.19.2 Release <https://github.com/codelibs/fess/releases/tag/fess-14.19.2>`__

Für ältere Nachrichten siehe :doc:`hier <news>`.

Forum
=====

Wenn Sie Fragen haben, nutzen Sie bitte das `Forum <https://discuss.codelibs.org/c/FessJA/>`__.

Kommerzieller Support
=====================

Fess ist ein Open-Source-Produkt unter der Apache-Lizenz und kann sowohl privat als auch kommerziell kostenlos genutzt werden.

Wenn Sie Unterstützungsdienste für die Anpassung, Einführung oder den Aufbau von Fess benötigen, siehe `kommerzieller Support (kostenpflichtig) <https://www.n2sm.net/products/n2search.html>`__.
Darüber hinaus werden auch Performance-Tuning-Maßnahmen wie die Verbesserung der Suchqualität und Crawl-Geschwindigkeit im kommerziellen Support angeboten.

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (optimiertes kommerzielles Fess-Paket)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (Alternative zum Google Site Search Service)

- :doc:`Verschiedene Support-Services <support-services>`


Fess Site Search
================

Das CodeLibs-Projekt bietet `Fess Site Search (FSS) <https://fss-generator.codelibs.org/ja/>`__ an.
Durch einfaches Platzieren von JavaScript auf bestehenden Websites können Sie die Fess-Suchseite integrieren.
Mit FSS ist auch die Migration von Google Site Search oder Yahoo! Custom Search einfach möglich.
Wenn Sie einen kostengünstigen Fess-Server benötigen, siehe `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__.

Data Store Plugins
==================

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

Theme Plugins
=============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Ingester Plugins
================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Script Plugins
==============

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

Verwandte Projekte
==================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__

Medienberichte
==============

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


