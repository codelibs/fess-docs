================
セットアップ手順
================

インストール方法
================

FessではDockerイメージを配布しています。
Docker Compose を使うことで、Java、Elasticsearch、Fessを個別にインストールすることなく簡単にFessを構築できます。

運用環境を構築する場合は必ずインストールガイドを参照してください。

Docker Composer のインストール
==================

Docker Compose がインストールされていない場合は、以下の手順でインストールしてください。

OSごとにダウンロードするファイルや手順に違いがあるので、お使いの環境に合わせて実施する必要があります。
詳細は`Docker <https://docs.docker.com/get-docker/>`_ のドキュメントを参照してください。

以降の説明はWindows環境での手順になります。

ダウンロード
--------------------------------------

`Docker Desktop <https://www.docker.com/products/docker-desktop/>`_ で該当OSのインストーラーをダウンロードします。

インストーラーの実行
-----------------------

ダウンロードしたインストーラーをダブルクリックして、インストールを開始します。

「Install required Windows components for WSL 2」 または
「Install required Enable Hyper-V Windows Features」 が選択されていることを確認して、
OKボタンをクリックします。

|image0|

インストールが完了したら、「close」ボタンをクリックして画面を閉じます。

|image1|

Docker Desktop の起動
-----------------

Windows メニュー内の「Docker Desktop」をクリックして起動します。

|image2|

Docker Desktop 起動後、利用規約が表示されるので、「I accept the terms」にチェックを入れて「Accept」ボタンをクリックします。

チュートリアル開始の案内が出ますが、ここでは「Skip tutorial」をクリックしてスキップします。
「Skip tutorial」をクリックすると Dashboard が表示されます。

|image3|

設定
==================

Elasticsearch が Docker コンテナとして実行できるようにするため、OS側で「vm.max_map_count」の値を調整します。
利用する環境によって設定方法が異なるので、それぞれの設定方法については「`Set vm.max_map_count to at least 262144 <https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_set_vm_max_map_count_to_at_least_262144>`_ 」を参照してください。

|Fess| のインストール
==================

Fessの起動に必要な設定は GitHub のリポジトリに登録しているので、gitコマンドでcloneするか、zip形式でダウンロードします。

|Fess| のダウンロード
----------------------------------

`docker-fess<https://github.com/codelibs/docker-fess>`_ にアクセスして、docker-fess をお使いの環境に展開します。

|Fess| の起動
-----------

docker compose コマンドで起動します。

Fessに関する設定は「compose.yaml」に、Elasticsearchの設定は「compose-elasticsearch8.yaml」、「compose-elasticsearch7.yaml」に記載しています。

Elasticsearch 7.x を使う場合は「compose-elasticsearch7.yaml」、
Elasticsearch 8.x を使う場合は「compose-elasticsearch8.yaml」を指定します。

以下の例では Elasticsearch 8.x で起動しています。

::

    cd docker-fess/compose
    docker compose -f compose.yaml -f compose-elasticsearch8.yaml up -d


コマンドの実行が終了したら、ターミナルで以下のコマンドを実行し、FessとElasticsearchの状態を確認します。

::

    docker ps

「STARUS」が「UP」になっていれば、起動完了です。

動作確認
========

http://localhost:8080/
にアクセスすることによって、起動を確認できます。

管理 UI は http://localhost:8080/admin/ です。
デフォルトの管理者アカウントのユーザー名/パスワードは、admin/adminになります。
管理者アカウントはアプリケーションサーバーにより管理されています。
|Fess|の管理 UI では、アプリケーションサーバーで fess ロールで認証されたユーザーを管理者として判断しています。

その他
======

|Fess| の停止
-----------

Fess停止は、ターミナルで以下のコマンドを実行します。

::

    docker compose -f compose.yaml -f compose-elasticsearch8.yaml down

管理者パスワードの変更
----------------------

管理 UI のユーザー編集画面で変更することができます。

.. |image0| image:: ../resources/images/ja/install/dockerdesktop-1.png
.. |image1| image:: ../resources/images/ja/install/dockerdesktop-2.png
.. |image2| image:: ../resources/images/ja/install/dockerdesktop-3.png
.. |image3| image:: ../resources/images/ja/install/dockerdesktop-4.png
