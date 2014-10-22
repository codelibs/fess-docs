=======================
Windowsサービスへの登録
=======================

Windowsサービスとしての登録
===========================

Windows 環境であれば Fess を Windows
のサービスとして登録することができます。サービスの登録方法は Tomcat
と同様です。

登録方法
--------

まず、Fess のインストール後、コマンドプロンプトから service.bat
を実行します (Vista などでは管理者として起動する必要があります)。Fess は
C:\\Java\\fess-server-2.0.0 にインストールしたものとします。

::

    > cd C:\Java\fess-server-2.0.0\bin
    > service.bat install fess
    ...
    The service 'fess' has been installed.

次に Fess 用のプロパティを追加します。以下を実行すると、Tomcat
のプロパティ設定ウィンドウが表示されます。

::

    > tomcat6w.exe //ES//fess

Java タブの Java Options に以下を設定します。

::

    -Dcatalina.base=C:\Java\fess-server-2.0.0
    -Dcatalina.home=C:\Java\fess-server-2.0.0
    -Djava.endorsed.dirs=C:\Java\fess-server-2.0.0\endorsed
    -Djava.io.tmpdir=C:\Java\fess-server-2.0.0\temp
    -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
    -Djava.util.logging.config.file=C:\Java\fess-server-2.0.0\conf\logging.properties
    -Dsolr.solr.home=C:\Java\fess-server-2.0.0\solr
    -Dsolr.data.dir=C:\Java\fess-server-2.0.0\solr\data
    -Dfess.log.file=C:\Java\fess-server-2.0.0\webapps\fess\WEB-INF\logs\fess.out
    -Djava.awt.headless=true
    -XX:+UseGCOverheadLimit
    -XX:+UseConcMarkSweepGC
    -XX:+CMSIncrementalMode
    -XX:+UseTLAB
    -Dpdfbox.cjk.support=true
    -XX:MaxPermSize=128m

Maximum memory pool の値を 512 に変更します。設定後、OK
ボタンを押下して設定を保存します。あとは、通常の Windows
サービスと同様に起動してください。
