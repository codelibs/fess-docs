======================
ロールベース検索の設定
======================

ロールベース検索とは
====================

|Fess| 
では任意の認証システムで認証されたユーザーの認証情報を元に検索結果を出し分けることができます。たとえば、ロールaを持つユーザーAは検索結果にロールaの情報が表示されるが、ロールaを持たないユーザーBは検索してもそれが表示されません。この機能を利用することで、ポータルやシングルサインオン環境でログインしているユーザーの所属する部門別や役職別などに検索を実現することができます。

|Fess| のロールベース検索ではロール情報を以下より取得できます。

-  リクエストパラメータ

-  リクエストヘッダー

-  クッキー

-  J2EE の認証情報

ポータルやエージェント型シングルサインオンシステムでは認証時に |Fess| 
の稼働しているドメインとパスに対してクッキーで認証情報を保存することで、ロール情報を取得することができます。また、リバースプロキシ型シングルサインオンシステムでは
|Fess| 
へのアクセス時にリクエストパラメータやリクエストヘッダーに認証情報を付加することでロール情報を取得することができます。

ロールベース検索の設定
======================

ここでは J2EE
の認証情報を利用したロールベース検索の設定方法を説明します。

tomcat-users.xmlの設定
----------------------

conf/tomcat-users.xml にロールとユーザーを追加します。今回は role1
ロールでロールベース検索を行います。ログインするユーザーは role1
になります。

::

    <?xml version='1.0' encoding='utf-8'?>
    <tomcat-users>
      <role rolename="fess"/>
      <role rolename="solr"/>
      <role rolename="role1"/>
      <user username="admin" password="admin" roles="fess"/>
      <user username="solradmin" password="solradmin" roles="solr"/>
      <user username="role1" password="role1" roles="role1"/>
    </tomcat-users>

fess.diconの設定
----------------

webapps/|fess_context_name|/WEB-INF/classes/fess.dicon を以下のように設定します。

::

        :
        <component name="roleQueryHelper" class="jp.sf.fess.helper.impl.RoleQueryHelperImpl">
            <property name="defaultRoleList">
                {"guest"}
            </property>
        :

defaultRoleList
を設定することで、認証情報がない場合のロール情報を設定できます。設定することでログインしていないユーザーに対して、ロールが必要な検索結果を表示させないようにできます。

web.xmlの設定
-------------

webapps/|fess_context_name|/WEB-INF/web.xml を以下のように設定します。

::

      :
      <security-constraint>
        <web-resource-collection>
          <web-resource-name> |Fess| Authentication</web-resource-name>
          <url-pattern>/login/login</url-pattern>
        </web-resource-collection>
        <auth-constraint>
          <role-name>fess</role-name>
          <role-name>role1</role-name>
        </auth-constraint>
      </security-constraint>
      :
      <security-role>
        <role-name>fess</role-name>
      </security-role>

      <security-role>
        <role-name>role1</role-name>
      </security-role>
      :

|Fess| の管理画面での設定
-----------------------

|Fess| を起動して管理者としてログインします。メニューのロールから設定名を
Role1 (設定名は任意)、値を role1 でロールを登録します。あとは role1
を持つユーザーで利用したいクロール設定で、Role1
を選択してクロール設定を登録してクロールします。

ロールでログイン
----------------

管理画面からログアウトします。role1
ユーザーでログインします。ログインに成功すると検索画面のトップにリダイレクトされます。

通常通り検索すると、クロール設定で Role1
のロール設定されたものだけが表示されます。

また、ログインしていない状態での検索は、guest
ユーザーによる検索となります。

ロールのログアウト
------------------

管理者以外のロールでログインした状態で http://localhost:8080/|fess_context_name|/admin
にアクセスすると、ログアウトするかどうかの画面が表示されます。ログアウトボタンを押下することでログアウトされます。
