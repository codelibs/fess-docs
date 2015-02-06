==========
ポート変更
==========

ポートの変更
============

|Fess| がデフォルトで利用するポートは 8080 になります。
変更するには以下の手順で変更します。

Tomcat のポート変更
-------------------

|Fess| が利用している Tomcat のポートを変更します。 変更は conf/server.xml
に記述されている以下のものを変更します。

-  8080: HTTP アクセスポート

-  8005: シャットダウンポート

-  8009: AJP ポート

-  8443: SSL の HTTP アクセスポート (デフォルトは無効)

-  19092: データベースポート(h2databaseが利用)

Solr の設定
-----------

標準構成では、Solr も同じ Tomcat の設定を利用しているので、Tomcat
のポートを変更した場合は、 |Fess| の Solr
サーバーの参照先情報も変更する必要があります。

webapps/|fess_context_name|/WEB-INF/classes/app.dicon の以下の箇所を変更します。

::

    <property name="managerUrl">"http://localhost:8080/manager/text/"</property>

webapps/|fess_context_name|/WEB-INF/classes/solrlib.dicon の以下の箇所を変更します。

::

    <arg>"http://localhost:8080/solr/core1"</arg>

solr/core1/conf/solrconfig.xml の以下の箇所を変更します。

::

    <arg>"http://localhost:8080/solr/core1-suggest"</arg>

**注: Tomcat
のポートを変更した場合は上記のポートを同様に変更しないと、Solr
サーバーにアクセスできないために検索画面やインデックス更新時にエラーが表示されます。**
