============
インストール
============

インストール要件
================

|Fess| は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境

-  Java: Java 6 以上

|Fess| を利用したい環境に Java
がインストールされていない場合は、http://java.sun.com/ より Java 6
以上の JDK を取得してインストールしてください。

ダウンロード
============

http://sourceforge.jp/projects/fess/releases/ から最新の |Fess| 
パッケージをダウンロードします。

インストール
============

ダウンロードした fess-server-x.y.zip を展開します。 Unix
環境にインストールした場合、bin
以下にあるスクリプトに実行権を付加します。

::

    $ unzip fess-server-x.y.zip
    $ cd fess-server-x.y
    $ chmod +x bin/*.sh   # (Unix環境のみ)

管理者パスワードの変更
======================

管理者アカウントはアプリケーションサーバーにより管理されています。
標準の |Fess| サーバーは Tomcat を利用しているので、Tomcat
のユーザー変更方法と同様になります。
変更する場合は、conf/tomcat-user.xml の admin
アカウントのパスワードを修正してください。

::

    <user username="admin" password="admin" roles="fess"/>

Solr サーバーのパスワード変更
=============================

|Fess| サーバーには Solr
が組み込まれていますが、アクセスするためにはパスワードが必要になります。
実運用などにおいては、デフォルトのパスワードを変更してください。

パスワードの変更方法は、まず、conf/tomcat-user.xml の solradmin
のパスワード属性を変更します。

::

      <user username="solradmin" password="solradmin" roles="solr"/>

次に webapps/fess/WEB-INF/classes/fess\_solr.dicon
の以下のパスワードの箇所を tomcat-user.xml で指定したものを記述します。

::

    <component class="org.apache.commons.httpclient.UsernamePasswordCredentials">
        <arg>"solradmin"</arg> <!-- Username -->
        <arg>"solradmin"</arg> <!-- Password -->
    </component>
