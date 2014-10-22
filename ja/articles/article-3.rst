===============================================================
Fessで作るApache Solrベースの検索サーバー 〜 ロールベース検索編
===============================================================

はじめに
========

前回の\ `モバイル編 <http://codezine.jp/article/detail/4527>`__\ では、Fessを用いてどのように携帯端末向け検索システムを構築するかをご紹介しました。
本記事ではFessの特徴的な機能の一つでもあるロールベース検索機能についてご紹介します。

本記事ではFess 8.2.0 を利用して説明します。
Fessの構築方法については\ `導入編 <http://codezine.jp/article/detail/4526>`__\ を参照してください。

対象読者
========

-  ポータルサイトなどの認証があるシステムで検索システムを構築してみたい方

-  閲覧権限ごとに検索する環境を構築したい方

必要な環境
==========

この記事の内容に関しては次の環境で、動作確認を行っています。

-  CentOS 5.5

-  JDK 1.6.0\_22

ロールベース検索
================

Fessのロールベース検索とは、任意の認証システムで認証されたユーザーの認証情報を元に検索結果を出し分ける機能です。
たとえば、営業部ロールを持つ営業担当者Aは検索結果に営業部ロールの情報が表示されるが、営業部ロールを持たない技術担当者Bは検索してもそれが表示されません。
この機能を利用することで、ポータルやシングルサインオン環境でログインしているユーザーの所属する部門別や役職別などに検索を実現することができます。

Fessのロールベース検索ではロール情報を以下の場所から取得できます。

1. リクエストパラメータ

2. リクエストヘッダー

3. クッキー

4. J2EE の認証情報

利用方法としては、ポータルサーバーやエージェント型シングルサインオンシステムでは認証時にFessの稼働しているドメインとパスに対してクッキーで認証情報を保存することで、ロール情報をFessに渡すことができます。
また、リバースプロキシ型シングルサインオンシステムではFessへのアクセス時にリクエストパラメータやリクエストヘッダーに認証情報を付加することで、Fessでロール情報を取得することができます。
このように様々な認証システムと連携することで、ユーザーごとに検索結果を出し分けることができます。

独自の認証システムを運用しているような場合は、jp.sf.fess.helper.RoleQueryHelperインターフェースを実装してクラスを用意することで対応することができます。
作成したクラスは「\ ``webapps/fess/WEB-INF/classes``\ 」などのクラスパスが通っている場所に配置して、「\ ``webapps/fess/WEB-INF/classes/fess.dicon``\ 」でjp.sf.fess.helper.impl.RoleQueryHelperImplに代わって指定します。

ロールベース検索を利用するための設定
====================================

Fess 8.2.0 がインストールしてあるものとします。
まだ、インストールしていない場合は、\ `導入編 <http://codezine.jp/article/detail/4526>`__\ を参考にしてインストールしてください。

認証システムには様々なものがありますが、Fessでは別途認証システムを構築せずにFessの既存のログイン画面を利用したTomcatの認証を試せる環境を提供しているので、本記事ではこれを利用してJ2EEの認証情報（Tomcatの認証）を利用したロールベース検索を説明します。

Tomcatにユーザーを追加
----------------------

まず、検索結果を出し分けて表示するためにユーザーをTomcatに追加します。
今回は、営業部（sales）と技術部（eng）の2つのロールを作成します。
そして、ユーザーはsalesロールに属するtaroユーザーとengロールに属するhanakoユーザーを追加します。
これらのユーザー情報を以下のように「\ ``conf/tomcat-users.xml``\ 」に記述します。

tomcat-users.xmlの内容
::

    <?xml version='1.0' encoding='utf-8'?>
    <tomcat-users>
      <role rolename="fess"/>
      <role rolename="solr"/>
      <role rolename="manager"/>
      <role rolename="sales"/><!-- 追加 -->
      <role rolename="eng"/><!-- 追加 -->
      <user username="admin" password="admin" roles="fess"/>
      <user username="solradmin" password="solradmin" roles="solr"/>
      <user username="manager" password="manager" roles="manager"/>
      <user username="taro" password="taropass" roles="sales"/><!-- 追加 -->
      <user username="hanako" password="hanakopass" roles="eng"/><!-- 追加 -->
    </tomcat-users>

既存の認証システムを利用する場合はこの設定は不要です。

fess.diconの設定
----------------

ここからがFessに対する設定になります。
まず、「\ ``webapps/fess/WEB-INF/classes/fess.dicon``\ 」のroleQueryHelperでデフォルトロールと認証情報の取得方法を設定します。
今回はJ2EEの認証情報を用いるので、「\ ``fess.dicon``\ 」のroleQueryHelperは以下のような設定になります。

fess.diconの内容
::

    :
    <component name="roleQueryHelper" class="jp.sf.fess.helper.impl.RoleQueryHelperImpl">
        <property name="defaultRoleList">
            {"guest"}
        </property>
    </component>
    :

上記のようにデフォルトロールを設定します。
デフォルトロールは、ログインしていない状態で検索するときにそのロールとして検索したと扱われます。
デフォルトロールを指定しないと、ログインしていない状態の検索ですべての検索結果が表示されてしまいます。

J2EEの認証情報以外で利用する場合についてもここで説明しておきます。
リクエストパラメータから認証情報を取得する場合は以下のように設定します。

fess.diconの内容
::

    :
    <component name="roleQueryHelper" class="jp.sf.fess.helper.impl.RoleQueryHelperImpl">
        <property name="parameterKey">"fessRoles"</property>
        <property name="encryptedParameterValue">false</property>
        <property name="defaultRoleList">
            {"guest"}
        </property>
    </component>
    :

ここでは、リクエストパラメータのキーにfessRolesを指定して、ロール情報をカンマ区切りの値で渡すことができます。
たとえば、salesロールとadminロールを持つユーザーが検索する際のURLは「\ ``http://hostname/fess/search?...&fessRoles=sales%0aadmin``\ 」のようにfessRolesを付加されます。
ここではencryptedParameterValueをfalseに設定していますが、この値をtrueにするとfessRolesの値部分をBlowfishやAESなどで暗号化して渡すことができます。
暗号化して値を渡す場合には、FessCipherコンポーネントを指定して復号化できるように設定する必要があります。

リクエストヘッダーから認証情報を取得する場合は以下のように設定します。

fess.diconの内容
::

    :
    <component name="roleQueryHelper" class="jp.sf.fess.helper.impl.RoleQueryHelperImpl">
        <property name="headerKey">"fessRoles"</property>
        <property name="encryptedParameterValue">false</property>
        <property name="defaultRoleList">
            {"guest"}
        </property>
    </component>
    :

リクエストヘッダーのキーにfessRolesを指定して、ロール情報をカンマ区切りの値で渡すことができます。

クッキーから認証情報を取得する場合は以下のように設定します。

fess.diconの内容
::

    :
    <component name="roleQueryHelper" class="jp.sf.fess.helper.impl.RoleQueryHelperImpl">
        <property name="cookieKey">"fessRoles"</property>
        <property name="encryptedParameterValue">false</property>
        <property name="defaultRoleList">
            {"guest"}
        </property>
    </component>
    :

リクエストパラメータと同様に、クッキーの名前にfessRolesを指定して、ロール情報をカンマ区切りの値で渡すことができます。

web.xmlの設定
-------------

「\ ``fess.dicon``\ 」と同様にログインできるようにするために「\ ``webapps/fess/WEB-INF/web.xml``\ 」のセキュリティ関連の設定を変更します。
以下のような設定になります。

web.xmlの内容
::

    :
    <security-constraint>
      <web-resource-collection>
        <web-resource-name>Fess Authentication</web-resource-name>
        <url-pattern>/login/login</url-pattern>
      </web-resource-collection>
      <auth-constraint>
        <role-name>fess</role-name>
        <role-name>sales</role-name>
        <role-name>eng</role-name>
      </auth-constraint>
    </security-constraint>
    :
    <security-role>
      <role-name>fess</role-name>
    </security-role>
    <security-role>
      <role-name>sales</role-name>
    </security-role>
    <security-role>
      <role-name>eng</role-name>
    </security-role>
    :

リクエストパラメータなどの他の認証を用いる場合には、この設定は不要です。

ロールベース検索の実行
======================

設定が一通り完了したので、Fessを起動してください。

登録ユーザーの確認
------------------

今回の設定でadmin、taro、hanakoの3つユーザーでFessにログインできる状態になっています。
順にログインできることを確認してください。
http://localhost:8080/fess/admin/\ にアクセスして、adminユーザーでログインすると通常通り管理画面が表示されます。
次にadminユーザーをログアウトして、再度\ http://localhost:8080/fess/admin/\ にアクセスして、taroとhanakoユーザーでログインしてください。
ログインが成功すると、\ http://localhost:8080/fess/\ の検索画面が表示されます。
ログアウトするときは、\ http://localhost:8080/fess/admin/\ にアクセスして［ログアウト］ボタンをクリックします。

ログアウト画面
|image0|

ロールの作成
------------

adminユーザーでログインして、左側のメニューの［ロール］をクリックしてロール一覧を表示します。
今回は次の3つのロールを作成してください。

ロール一覧
+--------------+-----------+
| ロール名     | 値        |
+--------------+-----------+
| デフォルト   | default   |
+--------------+-----------+
| 営業部       | sales     |
+--------------+-----------+
| 技術部       | eng       |
+--------------+-----------+

クロール設定の追加
------------------

クロール対象を登録します。
今回は営業部ロールのユーザーは\ http://www.n2sm.net/\ だけを検索でき、技術部ロールのユーザーは\ http://fess.codelibs.org/\ だけを検索できるようにします。
これらのクロール設定を登録するため、左側のメニューの［ウェブ］をクリックしてウェブクロール設定一覧を表示します。
[新規作成] をクリックして、ウェブクロール設定を作成してください。
まず、営業部用に\ http://www.n2sm.net/\ へのクロール設定として［ロール］項目に営業部を選択して作成します。
次に\ http://fess.codelibs.org/\ のクロール設定でロールに技術部を選択して作成します。

ウェブクロール設定のロール項目
|image1|

クロールの開始
--------------

クロール設定登録後、左側のメニューの［システム設定］をクリックして、システム設定画面で［開始］ボタンをクリックして、クロールを開始します。
クロールが完了するまでしばらく待ちます。

検索
----

クロール完了後、\ http://localhost:8080/fess/\ にアクセスして、ログインしていない状態で「fess」などの単語を検索して、検索結果が表示されないことを確認してください。
次にtaroユーザーでログインして、同様に検索してください。
taroユーザーはsalesロールを持つため、\ http://www.n2sm.net/\ の検索結果だけが表示されます。

salesロールでの検索画面
|image2|

taroユーザーをログアウトして、hanakoユーザーでログインしてください。
先ほどと同様に検索すると、hanakoユーザーはengロールを持つので、\ http://fess.codelibs.org/\ の検索結果だけが表示されます。

engロールでの検索画面
|image3|

まとめ
======

Fessのセキュリティー機能の一つであるロールベース検索についてご紹介しました。
J2EEの認証情報を用いたロールベース検索を中心に説明しましたが、Fessへの認証情報の受け渡しは汎用的な実装であるので様々な認証システムに対応できると思います。
ユーザーの属性ごとに検索結果を出し分けることができるので、社内ポータルサイトや共有フォルダなどの閲覧権限ごとに検索が必要なシステムも実現することが可能です。

次回は、Fessの提供しているAjax機能についてご紹介します。

参考資料
========

-  `Fess <http://fess.codelibs.org/ja/>`__

.. |image0| image:: ../../../resources/images/ja/article/3/logout.png
.. |image1| image:: ../../../resources/images/ja/article/3/crawl-conf-role.png
.. |image2| image:: ../../../resources/images/ja/article/3/search-by-sales.png
.. |image3| image:: ../../../resources/images/ja/article/3/search-by-eng.png
