==================
データベースの変更
==================

概要
====

標準の環境ではデータベースには H2 Database
を利用しています。設定を変更することで他のデータベースを利用することができます。

MySQLを利用する場合
===================

インストール
------------

MySQL 用のバイナリを展開します。

設定
----

データベースを作成します。

::

    $ mysql -u root -p
    mysql> create database fess_db;
    mysql> grant all privileges on fess_db.* to fess_user@localhost identified by 'fess_pass';
    mysql> create database fess_robot;
    mysql> grant all privileges on fess_robot.* to s2robot@localhost identified by 's2robot';
    mysql> FLUSH PRIVILEGES;

作成したデータベースにテーブルを作成します。DDL ファイルは
extension/mysql にあります。

::

    $ mysql -u fess_user --password=fess_pass fess_db < extension/mysql/fess.ddl 
    $ mysql -u s2robot --password=s2robot fess_robot < extension/mysql/robot.ddl 

webapps/fess/WEB-INF/lib に mysql ドライバの jar を配置します。

::

    $ cd webapps/fess/WEB-INF/lib/
    $ $ rm h2-1.*.jar 
    $ wget http://mirrors.ibiblio.org/pub/mirrors/maven2/mysql/mysql-connector-java/5.1.18/mysql-connector-java-5.1.18.jar
    $ cd ../../../../

webapps/fess/WEB-INF/classes/jdbc.dicon を編集します。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//SEASAR2.1//DTD S2Container//EN"
        "http://www.seasar.org/dtd/components21.dtd">
    <components namespace="jdbc">
        <include path="jta.dicon"/>

        <!-- MySQL -->
        <component name="xaDataSource"
            class="org.seasar.extension.dbcp.impl.XADataSourceImpl">
            <property name="driverClassName">
                "com.mysql.jdbc.Driver"
            </property>
            <property name="URL">
                "jdbc:mysql://localhost:3306/fess_db?" +
                "noDatetimeStringSync=true&amp;" +
                "zeroDateTimeBehavior=convertToNull&amp;" +
                "useUnicode=true&amp;characterEncoding=UTF-8&amp;" +
                "autoReconnect=true"
            </property>
            <property name="user">"fess_user"</property>
            <property name="password">"fess_pass"</property>
        </component>

        <component name="connectionPool"
            class="org.seasar.extension.dbcp.impl.ConnectionPoolImpl">
            <property name="timeout">600</property>
            <property name="maxPoolSize">10</property>
            <property name="allowLocalTx">true</property>
            <destroyMethod name="close"/>
        </component>

        <component name="DataSource"
            class="org.seasar.extension.dbcp.impl.DataSourceImpl"
        />
    </components>

webapps/fess/WEB-INF/classes/s2robot\_jdbc.dicon を編集します。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//SEASAR2.1//DTD S2Container//EN"
        "http://www.seasar.org/dtd/components21.dtd">
    <components namespace="jdbc">
        <include path="jta.dicon"/>

        <!-- for MySQL -->
        <component name="xaDataSource"
            class="org.seasar.extension.dbcp.impl.XADataSourceImpl">
            <property name="driverClassName">
                "com.mysql.jdbc.Driver"
            </property>
            <property name="URL">
                "jdbc:mysql://localhost:3306/fess_robot?" +
                "noDatetimeStringSync=true&amp;" +
                "zeroDateTimeBehavior=convertToNull&amp;" +
                "useUnicode=true&amp;characterEncoding=UTF-8&amp;" +
                "autoReconnect=true"
            </property>
            <property name="user">"s2robot"</property>
            <property name="password">"s2robot"</property>
        </component>

        <component name="connectionPool"
            class="org.seasar.extension.dbcp.impl.ConnectionPoolImpl">
            <property name="timeout">600</property>
            <property name="maxPoolSize">10</property>
            <property name="allowLocalTx">true</property>
            <property name="transactionIsolationLevel">@java.sql.Connection@TRANSACTION_REPEATABLE_READ</property>
            <destroyMethod name="close"/>
        </component>

        <component name="DataSource"
            class="org.seasar.extension.dbcp.impl.DataSourceImpl"
        />

    </components>
