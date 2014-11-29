=======================
Windowsサービスへの登録
=======================

Windowsサービスとしての登録
===========================

Windows 環境であれば |Fess| を Windows
のサービスとして登録することができます。サービスの登録方法は Tomcat
と同様です。

事前準備
--------

Windows のサービスとして登録する場合、クロールプロセスは Windows
のシステムの環境変数を見にいくため、\ **Java の JAVA\_HOME
をシステムの環境変数に登録し**\ 、同様に **%JAVA\_HOME%\\bin も Path
に追加する**\ 必要があります。

設定
----

webapps\\fess\\WEB-INF\\classes\\fess.dicon を編集して、-server
オプションを取り除きます。

::

        <component name="systemHelper" class="jp.sf.fess.helper.SystemHelper">
            <!--
            <property name="adminRole">"fess"</property>
            <property name="authenticatedRoles">"role1"</property>
            -->
            <property name="crawlerJavaOptions">new String[] {
                "-Djava.awt.headless=true", "-XX:+UseGCOverheadLimit",
                "-XX:+UseConcMarkSweepGC", "-XX:+CMSIncrementalMode",
                "-XX:+UseTLAB", "-Xmx512m", "-XX:MaxPermSize=128m"
            }</property>
        </component>

登録方法
--------

まず、 |Fess| のインストール後、コマンドプロンプトから service.bat
を実行します (Vista などでは管理者として起動する必要があります)。 |Fess| は
C:\\Java\\fess-server-8.0.0 にインストールしたものとします。

::

    > cd C:\Java\fess-server-8.0.0\bin
    > service.bat install fess
    ...
    The service 'fess' has been installed.

設定の確認方法
--------------

以下のようにすることで |Fess| 
用のプロパティを確認できます。以下を実行すると、Tomcat
のプロパティ設定ウィンドウが表示されます。

::

    > tomcat7w.exe //ES//fess

サービスの設定
--------------

コントロールパネル - 管理ツール - サービスで管理ツールを表示して、通常の
Windows のサービスと同様に自動起動などが設定できます。

その他
======

64bit環境での利用
-----------------

|Fess| で配布しているものは 64bit Windows 用の Tomcat
バイナリをベースにビルドされています。 32bit Windows で利用する場合は
`Tomcat <http://tomcat.apache.org/download-70.cgi>`__ のサイトから 32bit
Windows zip などを取得して、tomcat7.exe, tomcat7w.exe, tcnative-1.dll
を差し替えてください。
