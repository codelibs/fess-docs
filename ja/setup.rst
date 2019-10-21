================
セットアップ手順
================

インストール方法
================

|Fess| は Java 実行環境があればどの OS
でも実行可能です。動作環境は以下のとおりです。

-  Windows や Unix など Java が実行できる OS 環境

-  Java: Java 11

運用環境を構築する場合は必ずインストールガイドを参照してください。

Javaのインストール
==================

Java がインストールされていない場合は以下の手順でJavaをインストールしてください。

Java SE のダウンロードページへアクセス
--------------------------------------

JavaScriptが有効な状態でOracle社の「`Java SE
Downloads <http://www.oracle.com/technetwork/java/javase/downloads/index.html>`_」ページにアクセスします。

JavaSE 11 の「Download JDK」をクリックします。(JavaScriptが無効になっているとダウンロードが有効となりません)

|image0|

ライセンスの確認
----------------

「Oracle Binary Code License Agreement for Java SE」を読んでライセンスに同意されたら「Accept License Agreement」にチェックを入れます。

|image1|

ダウンロードの開始
------------------

インストールを行うパソコンのOSに合わせてJDKのダウンロードを行います。
Windwos 64ビットの場合は「Windows x64」、Windows 32ビットの場合は「Windows x86」を選択します (以下はWindows 64ビット版の例です) 。

|image2|

JDKインストーラーの実行
-----------------------

ダウンロードしたJDKインストーラー (jdk-11.X.X-windows-x64_bin.exe)
を実行します(XXはダウンロードしたアップデートリリースのバージョン)。以下はWindows
64ビット版の例です。

|image3|

Windowsの設定によっては、「次のプログラムにこのコンピュータへの変更を許可しますか？」というダイアログが表示されることがあります。その場合、[はい]ボタンをクリックしてください。

JDKのインストール
-----------------

インストーラが起動します。[次へ]ボタンを押します。

|image4|

インストール先のフォルダが変更できます。デフォルトのままで問題なければ、[次へ]ボタンを押します。

|image5|

JDKのインストールが開始されるので、しばらく待ちます。

|image6|


インストール完了
----------------

インストール完了のメッセージが表示されます。 [閉じる]ボタンを押します。

|image7|

インストール完了です。

インストールされたコンポーネントは、以下の2つです。以下で確認できます。(Windows
7の場合)

1. [コントロールパネル]→[プログラム]→[プログラムと機能]の一覧に表示されます。

   -  Java SE Development Kit 11 Update XX (64-bit)

   -  Java(TM) 11 Update XX (64-bit)

環境変数の設定
--------------

「環境変数」とは、プログラムに渡される設定情報です。コマンドプロンプトでJDKのコマンドを実行するために、Javaインストールの後、環境変数の設定が必要です。

Windows 7
では以下のように設定します。[コントロールパネル]→[システムとセキュリティ]→[システム]→[システムの詳細設定]→[環境変数]を選択します。

|image8|

「システムとセキュリティ」をクリックします。

|image9|

「システム」をクリックします。

|image10|

「詳細設定」をクリックします。

|image11|

「環境変数」をクリックします。

|image12|

「システム環境変数」の「新規」ボタン（画面下部）をクリックします。

|image13|

「変数名」には「JAVA\_HOME」と入力します。

|image14|

「変数値」には、JDKがインストールしたディレクトリを記述します。

エクスプローラで「C:\\Program
Files\\Java」を開き、「jdk・・・」というフォルダを探して、そのアドレスを記述します。

たとえばjdkのバージョン11.X.Xをインストールした場合は、「C:\\Program
Files\\Java\\jdk11.X.X」となります。(XXの部分にはインストールしたバージョンが入ります)

記述後、「OK」を押します。

「システム環境変数」のリストから、「変数」が「Path」である行を探します。

|image15|

その行をクリックして「編集」ボタンを押して開き、「新規」ボタンを押します。

|image16|

「%JAVA\_HOME%\\bin」という文字列を追加し、「OK」をクリックします。

|image17|

|Fess| のインストール
==================

|Fess| のダウンロードページへアクセス
----------------------------------

https://github.com/codelibs/fess/releases から最新の |Fess| パッケージをダウンロードします。

URL先のリリースファイル一覧から「fess-x.y.z.zip」をクリックします。

|image18|

インストール
------------

ダウンロードしたzipファイルを解凍します。Windows環境の場合はzip解凍ツールなどで展開してください。

Unix 環境にインストールした場合、bin
以下にあるスクリプトに実行権を付加します。

::

    $ unzip fess-x.y.z.zip
    $ cd fess-x.y.z

|image19|

解凍したフォルダーをダブルクリックで開きます。

|image20|

binフォルダーをダブルクリックで開きます。

|image21|

|Fess| の起動
-----------

binフォルダにあるfess.batファイルをダブルクリックして、 |Fess| を起動させます。

Unix環境の場合は以下を実行します。

::

    $ ./bin/fess

|image22|

コマンドプロンプトが表示され起動されます。
fess\logs\server_*.log(更新日時が最新のもの)の内容に
「Boot successful」が出力されていれば起動完了です。

動作確認
========

http://localhost:8080/
にアクセスすることによって、起動を確認できます。

管理 UI は http://localhost:8080/admin/ です。
デフォルトの管理者アカウントのユーザー名/パスワードは、admin/admin
になります。
管理者アカウントはアプリケーションサーバーにより管理されています。 |Fess|
の管理 UI では、アプリケーションサーバーで fess
ロールで認証されたユーザーを管理者として判断しています。

その他
======

|Fess| の停止
-----------

|Fess| のプロセスを停止してください。

管理者パスワードの変更
----------------------

管理 UI のユーザー編集画面で変更することができます。

.. |image0| image:: ../resources/images/ja/install/java-1.png
.. |image1| image:: ../resources/images/ja/install/java-2.png
.. |image2| image:: ../resources/images/ja/install/java-3.png
.. |image3| image:: ../resources/images/ja/install/java-4.png
.. |image4| image:: ../resources/images/ja/install/java-5.png
.. |image5| image:: ../resources/images/ja/install/java-6.png
.. |image6| image:: ../resources/images/ja/install/java-7.png
.. |image7| image:: ../resources/images/ja/install/java-8.png
.. |image8| image:: ../resources/images/ja/install/java-9.png
.. |image9| image:: ../resources/images/ja/install/java-10.png
.. |image10| image:: ../resources/images/ja/install/java-11.png
.. |image11| image:: ../resources/images/ja/install/java-12.png
.. |image12| image:: ../resources/images/ja/install/java-13.png
.. |image13| image:: ../resources/images/ja/install/java-14.png
.. |image14| image:: ../resources/images/ja/install/java-15.png
.. |image15| image:: ../resources/images/ja/install/java-16.png
.. |image16| image:: ../resources/images/ja/install/java-17.png
.. |image17| image:: ../resources/images/ja/install/java-18.png
.. |image18| image:: ../resources/images/ja/install/Fess-1.png
.. |image19| image:: ../resources/images/ja/install/Fess-2.png
.. |image20| image:: ../resources/images/ja/install/Fess-3.png
.. |image21| image:: ../resources/images/ja/install/Fess-4.png
.. |image22| image:: ../resources/images/ja/install/Fess-5.png
