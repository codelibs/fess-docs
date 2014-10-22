============
インストール
============

インストール要件
================

Fess は以下の環境で利用することができます。

-  OS: Windows や Unix など Java が実行できる OS 環境

-  Java: Java 7 以上 (Java 6 でも動作可能)

Fess を利用したい環境に Java
がインストールされていない場合は、http://java.sun.com/ より Java 7
以上の JDK を取得してインストールしてください。

ダウンロード
============

http://sourceforge.jp/projects/fess/releases/ から最新の Fess
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

管理者アカウントはアプリケーションサーバーにより管理されています。標準の
Fess サーバーは Tomcat を利用しているので、Tomcat
のユーザー変更方法と同様になります。変更する場合は、conf/tomcat-user.xml
の admin アカウントのパスワードを修正してください。

::

    <user username="admin" password="admin" roles="fess"/>

tomcat-user.xml のファイルによる管理方法以外を利用する場合は、Tomcat
のドキュメントや JAAS 認証の仕様を参照してください。

Solr サーバーのパスワード変更
=============================

Fess サーバーには Solr
が組み込まれていますが、アクセスするためにはパスワードが必要になります。実運用などにおいては、デフォルトのパスワードを変更してください。

パスワードの変更方法は、まず、conf/tomcat-user.xml の solradmin
のパスワード属性を変更します。

::

      <user username="solradmin" password="solradmin" roles="solr"/>

次に webapps/fess/WEB-INF/classes/solrlib.dicon
の以下のパスワードの箇所を tomcat-user.xml で指定したものを記述します。

::

    <component class="org.apache.commons.httpclient.UsernamePasswordCredentials">
        <arg>"solradmin"</arg> <!-- ユーザー名 -->
        <arg>"solradmin"</arg> <!-- パスワード -->
    </component>

Tomcat コンソールのパスワード変更
=================================

Fess サーバーから Tomcat に配置した Solr
のコンテキストを管理することができますが、管理するためにはパスワードが必要になります。実運用などにおいては、デフォルトのパスワードを変更してください。

パスワードの変更方法は、conf/tomcat-user.xml の manager
のパスワード属性を変更します。

::

      <user username="manager" password="manager" roles="manager-script"/>

次に webapps/fess/WEB-INF/classes/app.dicon の以下のパスワードの箇所を
tomcat-user.xml で指定したものを記述します。

::

    <component class="jp.sf.fess.helper.impl.TomcatManagementHelperImpl$SolrInstance">
      <property name="name">"solrServer1"</property>
      <property name="managerUrl">"http://localhost:8080/manager/text/"</property>
      <property name="contextPath">"/solr"</property>
      <property name="username">"manager"</property>
      <property name="password">"manager"</property> <!-- パスワード -->
    </component>

暗号化キーの変更
================

ログイン時の戻りパスの設定などで暗号化/復号化が利用されています。実運用などにおいてはデフォルトのパスワードを変更してください。

変更方法は、webapps/fess/WEB-INF/classes/app.dicon で key
の値を変更します。16 文字の半角英数字を設定してください。

::

    <!-- CHANGE THE FOLLOWING KEY -->
    <property name="key">"1234567890123456"</property>
