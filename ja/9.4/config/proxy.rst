==============
プロキシの設定
==============

クローラ用プロキシの設定
========================

イントラネット内から外部サイトをクロールするような場合は、ファイアフォールにクロールがブロックされてしまうかもしれません。そのような場合にはクローラ用のプロキシを設定してください。

設定方法
========

下記の内容で webapps/fess/WEB-INF/classes/s2robot\_client.dicon
を作成することでプロキシが設定されます。

::

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//SEASAR//DTD S2Container 2.4//EN"
        "http://www.seasar.org/dtd/components24.dtd">
    <components>
        <include path="s2robot_robotstxt.dicon"/>
        <include path="s2robot_contentlength.dicon"/>

        <component name="internalHttpClient"
            class="org.codelibs.robot.client.http.HcHttpClient" instance="prototype">
            <property name="cookieSpec">@org.apache.http.client.params.CookiePolicy@BEST_MATCH</property>
            <property name="clientConnectionManager">clientConnectionManager</property>
            <property name="proxyHost">"プロキシサーバー名(ex. 192.168.1.1)"</property>
            <property name="proxyPort">プロキシサーバーのポート(ex. 8080) (" は不要)</property>
            <!-- プロキシに認証がある場合
            <property name="proxyCredentials">
                <component class="org.apache.http.auth.UsernamePasswordCredentials">
                    <arg>"プロキシ用ユーザー名"</arg>
                    <arg>"プロキシ用パスワード"</arg>
                </component>
            </property>
            -->
        </component>
        <component name="httpClient"
            class="org.codelibs.robot.client.FaultTolerantClient" instance="prototype">
            <property name="robotClient">internalHttpClient</property>
            <property name="maxRetryCount">5</property>
            <property name="retryInterval">500</property>
        </component>
        
        <component name="clientConnectionManager"
            class="org.apache.http.impl.conn.PoolingHttpClientConnectionManager">
            <arg>5</arg><!-- timeToLive -->
            <arg>@java.util.concurrent.TimeUnit@MINUTES</arg><!-- tunit -->
            <!-- Increase max total connection to 200 -->
            <property name="maxTotal">200</property>
            <!-- Increase default max connection per route to 20 -->
            <property name="defaultMaxPerRoute">20</property>
            <destroyMethod name="shutdown"></destroyMethod>
        </component>

        <component name="fsClient"
            class="org.codelibs.robot.client.fs.FileSystemClient" instance="prototype">
            <property name="charset">"UTF-8"</property>
        </component>

        <component name="smbClient"
            class="org.codelibs.robot.client.smb.SmbClient" instance="prototype">
            <property name="charset">"UTF-8"</property>
            <!-- ntlmPasswordAuthentication -->
        </component>

        <component name="clientFactory"
            class="org.codelibs.robot.client.S2RobotClientFactory" instance="prototype">
            <initMethod name="addClient">
                <arg>{"http:.*", "https:.*"}</arg>
                <arg>httpClient</arg>
            </initMethod>
            <initMethod name="addClient">
                <arg>"file:.*"</arg>
                <arg>fsClient</arg>
            </initMethod>
            <initMethod name="addClient">
                <arg>"smb:.*"</arg>
                <arg>smbClient</arg>
            </initMethod>
        </component>

    </components>
