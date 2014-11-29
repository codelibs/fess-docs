============================
既存の Tomcat にインストール
============================

概要
====

|Fess| の標準配布物は Tomcat に配備済みの状態で配布されています。 |Fess| は
Tomcat に依存していないので、任意の Java
アプリケーションサーバーに配備することも可能です。
ここでは、既に利用している Tomcat に |Fess| を配備する方法を説明します。

ダウンロード
============

|Fess| 
サーバーを\ `ここ <http://sourceforge.jp/projects/fess/releases/>`__\ からダウンロードします。

設定
====

ダウンロードした |Fess| サーバーを展開します。 展開した |Fess| 
サーバーのトップディレクトリを $FESS\_HOME とします。 既存の Tomcat 7
のトップディレクトリを $TOMCAT\_HOME とします。 必要な |Fess| 
サーバーのデータをコピーします。

::

    cp $FESS_HOME/bin/setenv.bat $TOMCAT_HOME/bin
    cp $FESS_HOME/bin/setenv.sh $TOMCAT_HOME/bin
    cp $FESS_HOME/conf/tomcat-users.xml $TOMCAT_HOME/conf
    cp $FESS_HOME/conf/server.xml $TOMCAT_HOME/conf
    cp -r $FESS_HOME/solr $TOMCAT_HOME/
    cp -r $FESS_HOME/webapps/solr $TOMCAT_HOME/webapps
    cp -r $FESS_HOME/webapps/fess $TOMCAT_HOME/webapps
    # 以下は省略可
    cp $FESS_HOME/bin/crawler.sh $TOMCAT_HOME/bin
    cp $FESS_HOME/bin/service.bat $TOMCAT_HOME/bin

コピー先のファイルに変更など加えている場合は、diff
コマンドなどで更新差分を確認して差分だけを適用します。

起動
====

startup.\* で通常の Tomcat と同様に起動して http://localhost:8080/fess/
にアクセスします。
