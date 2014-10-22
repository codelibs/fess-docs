==============
プロキシの設定
==============

クローラ用プロキシの設定
========================

イントラネット内から外部サイトをクロールするような場合は、ファイアフォールにクロールがブロックされてしまうかもしれません。そのような場合にはクローラ用のプロキシを設定してください。

設定方法
--------

下記の内容で webapps/fess/WEB-INF/classes/s2robot\_client.dicon
を作成することでプロキシが設定されます。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//SEASAR//DTD S2Container 2.4//EN"
        "http://www.seasar.org/dtd/components24.dtd">
    <components>
        <include path="s2robot_robotstxt.dicon"/>
        <include path="s2robot_contentlength.dicon"/>

        <component name="httpClient" class="org.seasar.robot.client.http.CommonsHttpClient" instance="prototype">
            <property name="cookiePolicy">@org.apache.commons.httpclient.cookie.CookiePolicy@BROWSER_COMPATIBILITY</property>
            <property name="proxyHost">"プロキシホスト名"</property>
            <property name="proxyPort">プロキシポート</property>
            <!-- プロキシに認証がある場合
            <property name="proxyCredentials">
                <component class="org.apache.commons.httpclient.UsernamePasswordCredentials">
                    <arg>"プロキシ用ユーザー名"</arg>
                    <arg>"プロキシ用パスワード"</arg>
                </component>
            </property>
            -->
        </component>

        <component name="fsClient" class="org.seasar.robot.client.fs.FileSystemClient" instance="prototype">
            <property name="charset">"UTF-8"</property>
        </component>

        <component name="clientFactory" class="org.seasar.robot.client.S2RobotClientFactory" instance="prototype">
            <initMethod name="addClient">
                <arg>{"http:.*", "https:.*"}</arg>
                <arg>httpClient</arg>
            </initMethod>
            <initMethod name="addClient">
                <arg>"file:.*"</arg>
                <arg>fsClient</arg>
            </initMethod>
        </component>

    </components>
