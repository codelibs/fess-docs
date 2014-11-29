==============================================
オープンソース全文検索サーバー - |Fess| 開発概要
==============================================

概要
====

|Fess| を開発するために必要な情報をまとめます。

必要な知識
==========

|Fess| は Java 7
以上の環境で動作するアプリケーションとして開発されています。以下のような知識が必要になります。

-  Java

-  Seasar 2

-  SAStruts (ウェブ画面を開発する場合)

-  DBFlute (DB 周りを開発する場合)

-  Solr (検索インデックス周りを開発する場合)

-  S2Robot (クローラー周りを開発する場合)

開発する際には Eclipse および Maven を利用する前提で進めます(fess-server
でのリリース物を生成するためのビルドには Ant
が必要になります)。また、開発するにあたり、 |Fess| 
サーバも動作させるためにダウンロードおよびインストールしておきます。必要なものは事前にインストールしておいてください。

ウェブ画面周りの開発について
============================

管理画面や検索画面の開発方法をまとめます。ここでは、Eclipseを用いた開発方法を説明します。Eclipse上でWTPで開発できる状態にしておく必要があります(J2EE版をインストールしておくなど)。

1. Java, Eclipse, Maven 3.x, |Fess| 
   をインストールして準備します。 |Fess| のzipファイルは<FESS\_HOME>ディレクトリに展開したと仮定します。

2. |Fess| のソースコードを github から clone します。

   ::

       git clone https://github.com/codelibs/fess.git

3. EclipseにMavenプロジェクトとしてインポートします。

4. Serversビューを表示します。表示されていない場合は、Window > Show View
   > Other... でダイアログを表示して、Server > Servers を選択して OK
   ボタンを押下します。

5. Serversビューで新規サーバを追加します。Tomcat v7.0 Server
   を選択して、サーバ名は適当に設定して、Nextボタンを押下します。次にfessをConfiguredに追加して、Finishボタンを押下します。Serversビューに登録したサーバが表示されるので、ダブルクリックをして設定情報(Overview)を表示します。

6. Server LocationsでUse Tomcat Installationを選択します。

7. TimeoutsでStartを180秒、Stopを60秒に変更します。

8. General InformationのOpen Launch
   Configurationをクリックします。Argumentsタグをクリックします。VM
   argumentsに「-Dsolr.solr.home=<FESS\_HOME>/solr
   -Dfess.log.file=<FESS\_HOME>/logs/fess.out
   -Dsolr.log.file=<FESS\_HOME>/logs/solr.log -Djava.awt.headless=true
   -server -Xmx1g -XX:+UseTLAB -XX:+DisableExplicitGC
   -XX:MaxMetaspaceSize=128m -XX:CompressedClassSpaceSize=32m
   -XX:-UseGCOverheadLimit -XX:+UseConcMarkSweepGC
   -XX:CMSInitiatingOccupancyFraction=75 -XX:+CMSIncrementalMode
   -XX:+CMSIncrementalPacing -XX:CMSIncrementalDutyCycleMin=0
   -XX:+UseParNewGC
   -XX:+OptimizeStringConcat」を追加します。<FESS\_HOME>は環境にあわせて変更してください。OKボタンを押下します。(Java
   7の場合は-XX:MaxMetaspaceSize=128m
   -XX:CompressedClassSpaceSize=32mを-XX:MaxPermSize=128mに置き換える)

9. Serversビューから登録したサーバを起動します。

HOT Deploy で開発したい場合は、src/main/resources/env.txt を product
から ct に変更します。これにより、Tomcat( |Fess| )
を再起動することなく、ソースコードを変更することができます。

クロール周りの開発について
==========================

クロールプロセスは Tomcat( |Fess| )
からプロセスが起動されます。そのため、デバッガで追いたい場合などは
Eclipse 上でデバッグ用の Java
アプリケーションとして登録する必要があります。

1. 通常の Java Application として Eclipse
   でデバッグできるように登録します。main関数は jp.sf.fess.exec.Crawler
   になります。

2. 1 の設定において、引数の設定では、まず、プログラムの設定は -sessionId
   20100101000000 のように適当なセッション ID を渡します。VM Settings
   には |Fess| の bin/setenv.sh の内容を展開して登録します。

3. classpath の設定では、/fess/src/main/webapp/WEB-INF/cmd
   とgeronimo\_servlet\_2.4\_spec-1.0.jar を追加します。

4. 実行します。

|Fess| の配布物の作成について
===========================

|Fess| の配布物は、Tomcat に |Fess| の war ファイルおよび Solr
を同梱したものになります。 |Fess| の配布物は SVN の fess-server
でビルドします。ビルドするためには Ant が必要になります。

::

    $ git clone https://github.com/codelibs/fess-server.git
    $ cd fess-server
    $ ant clean
    $ ant

参考資料
========

-  `Seasar 2 徹底入門 SAStruts/S2JDBC
   対応 <http://www.amazon.co.jp/Seasar-%E5%BE%B9%E5%BA%95%E5%85%A5%E9%96%80-SAStruts-S2JDBC-%E5%AF%BE%E5%BF%9C/dp/4798121509>`__
   (Seasar2, SAStrutsに関して参考になります。S2JDBC
   などは利用していないのでその辺などは不要です)

-  `DBFlute <http://dbflute.sandbox.seasar.org/>`__

-  `S2Robot <http://s2robot.sandbox.seasar.org/ja/>`__

-  `Solr <http://lucene.apache.org/solr/>`__
