==============================================
オープンソース全文検索サーバー - |Fess| 開発概要
==============================================

概要
====

|Fess| を開発するために必要な情報をまとめます。

必要な知識
==========

|Fess| は Java 11 以上の環境で動作するアプリケーションとして開発されています。
以下のような知識が必要になります。

-  Java 11

-  LastaFlute

-  DBFlute

-  Elasticsearch

開発する際には Eclipse および Maven を利用する前提で進めます。
必要なものは事前にインストールしておいてください。

ウェブ画面周りの開発について
============================

管理画面や検索画面の開発方法をまとめます。
ここでは、Eclipseを用いた開発方法を説明します。

セットアップ
------------

1. Java 11, Eclipse, Maven 3.x, |Fess| をインストールして準備します。

2. |Fess| のソースコードを github から clone します。

   ::

       git clone https://github.com/codelibs/fess.git

3. EclipseにMavenプロジェクトとしてインポートします。

プラグインのダウンロード
------------------------

Elasticsearch のプラグインのダウンロードをします。
毎回実行する必要はありません。
プラグインを更新する際に実行してください。

::

   mvn antrun:run

実行
----

org.codelibs.fess.FessBoot を Eclipse 上でデバッグ実行をします。

ソースコードの自動生成
----------------------

Fess は DBFlute の機能を利用して、Elasticsearch のスキーマに合わせてソースコードを自動生成しています。
対象のソースコードを自動生成するには以下を実行します。

::

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format


|Fess| の配布物の作成について
===========================

|Fess| の配布物は、以下を実行することでtarget/releasesに生成されます。

::

    mvn package

参考資料
========

-  `LastaFlute <http://github.com/lastaflute>`__

-  `DBFlute <http://github.com/dbflute>`__

