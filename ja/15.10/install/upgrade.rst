====================
アップグレード手順
====================

このページでは、 |Fess| を以前のバージョンから最新版にアップグレードする手順について説明します。

.. warning::

   **アップグレード前の重要な注意事項**

   - アップグレード前に必ずバックアップを取得してください
   - テスト環境で事前にアップグレードを検証することを強く推奨します
   - アップグレード中はサービスが停止するため、適切なメンテナンス時間を設定してください
   - バージョンによっては、設定ファイルの形式が変更されている場合があります

対応バージョン
==============

このアップグレード手順は、以下のバージョン間のアップグレードに対応しています：

- Fess 14.x → Fess 15.10
- Fess 15.x → Fess 15.10

.. important::

   |Fess| 14.x は OpenSearch 2.x 系、\ |Fess| 15.10 は OpenSearch 3.9.0 に対応しています。
   |Fess| 用の OpenSearch プラグインは OpenSearch のバージョンと完全に一致している必要があるため、
   14.x からアップグレードする場合は OpenSearch のメジャーバージョンアップも必須です。
   :ref:`upgrade-opensearch` を参照してください。

.. note::

   さらに古いバージョン（13.x 以前）からアップグレードする場合は、段階的なアップグレードが必要な場合があります。
   詳細はリリースノートを確認してください。

アップグレード前の準備
======================

バージョン互換性の確認
----------------------

アップグレード先のバージョンと現在のバージョンの互換性を確認してください。

- `リリースノート <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - |Fess| 15.10 の動作環境（Java、OpenSearch のバージョン）

ダウンタイムの計画
------------------

アップグレード作業には、システムの停止が必要です。以下を考慮してダウンタイムを計画してください：

- バックアップ時間: 10分 〜 数時間（データ量による）
- アップグレード時間: 10 〜 30分
- 動作確認時間: 30分 〜 1時間
- 予備時間: 30分

**推奨メンテナンス時間**: 合計 2 〜 4時間

ステップ 1: データのバックアップ
================================

アップグレード前に、すべてのデータをバックアップしてください。

設定データのバックアップ
------------------------

1. **管理画面からのバックアップ**

   管理画面にログインし、「システム情報」→「バックアップ」をクリックします。

   バックアップページには、以下の設定データが項目ごとに一覧表示されます。
   各行をクリックしてダウンロードします（単一の ZIP ファイルではなく、項目ごとの個別ファイルです。
   一括ダウンロードの機能はないため、必要な項目を 1 つずつダウンロードします）。

   - ``fess_basic_config.bulk`` - 設定インデックス（クロール設定、スケジューラー、ラベル、
     キーマッチ、ロール、Web/ファイル認証など 19 インデックス）
   - ``fess_config.bulk`` - 上記 19 インデックスに加えて、クロール情報、障害 URL、ジョブログ、
     サムネイルキューなどの実行時データを含む 25 インデックス（15.8 まで。15.9 ではユーザータグを
     保持する ``tag_type`` インデックスが加わり 26 インデックス）
   - ``fess_user.bulk`` - ユーザー、ロール、グループ
   - ``system.properties`` - 全般設定を含むシステム設定
   - ``fess.json`` - インデックスの設定（シャード数、\ ``index.knn`` など）
   - ``doc.json`` - ドキュメントのマッピング（フィールド定義）

   .. note::

      ``fess_config.bulk`` は ``fess_basic_config.bulk`` を包含しています。アップグレード前の
      設定バックアップとしては、\ ``fess_basic_config.bulk``\ 、\ ``fess_user.bulk``\ 、
      ``system.properties`` の 3 つで十分です。ただし、バックアップ元が 15.9 以降でユーザータグを使っている場合は、ユーザータグを保持する ``tag_type`` インデックスが ``fess_basic_config.bulk`` には含まれないため、\ ``fess_config.bulk`` も取得してください（ :doc:`../admin/tagtype-guide` を参照）。

   .. note::

      検索ログやクリックログなどのログデータ（``search_log.ndjson``、``click_log.ndjson``、
      ``favorite_log.ndjson``、``user_info.ndjson``。15.9 では ``chat_log.ndjson`` も表示されます）も
      同じページからダウンロードできます。
      設定のみをバックアップする場合は不要です。なお、これらの ``*.ndjson`` ファイルは
      バックアップページからアップロードして復元することはできません
      （「ロールバック手順」を参照）。

2. **設定ファイルのバックアップ**

   ZIP 版::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   RPM 版::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   DEB 版::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess``\ （RPM 版）と ``/etc/default/fess``\ （DEB 版）は、
      ``FESS_PORT``\ 、\ ``FESS_HEAP_SIZE``\ 、\ ``SEARCH_ENGINE_HTTP_URL``\ 、
      ``FESS_DICTIONARY_PATH`` などを指定する環境変数ファイルです。
      ZIP 版でこれらに相当する設定は ``bin/fess.in.sh`` にあります。

3. **カスタマイズした設定ファイル**

   カスタマイズした設定ファイルがある場合、それらもバックアップします::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/
       $ cp /path/to/fess/lib/classes/tomcat_config.properties /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` は |Fess| 本体（Web）プロセスのログ設定です。
      クローラーなどの子プロセスは別々のファイル
      （``app/WEB-INF/env/crawler/resources/log4j2.xml`` など、\ ``crawler``\ 、\ ``suggest``\ 、
      ``thumbnail``\ 、\ ``chunk`` の 4 つ）を使用するため、これらを変更している場合は
      あわせてバックアップしてください。

インデックスデータのバックアップ
--------------------------------

OpenSearch のインデックスデータをバックアップします。

方法 1: スナップショット機能を使用（推奨）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch のスナップショット機能を使用して、インデックスをバックアップします。

.. note::

   ファイルシステムリポジトリ（``fs``）を登録するには、事前に OpenSearch の ``opensearch.yml`` の
   ``path.repo`` にバックアップ先ディレクトリを指定し、OpenSearch を再起動しておく必要があります。

1. リポジトリの設定::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. スナップショットの作成::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. スナップショットの確認::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

方法 2: ディレクトリごとバックアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OpenSearch を停止してから、データディレクトリをバックアップします。

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Docker 版のバックアップ
-----------------------

OpenSearch のデータは Docker ボリュームに保存されます。\ ``compose-opensearch3.yaml`` では、
インデックスデータ用の ``search01_data`` と、辞書ファイル用の ``search01_dictionary`` の
2 つのボリュームが定義されています。

.. note::

   実際のボリューム名には、Compose のプロジェクト名（既定では Compose ファイルを配置した
   ディレクトリ名）が接頭辞として付与されます。正確な名前は次のコマンドで確認してください::

       $ docker volume ls

コンテナーを停止してから、ボリュームをバックアップします。\ ``docker run`` の ``-v`` には、
接頭辞を含む実際のボリューム名を指定します::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   ``-v`` に接頭辞なしの ``search01_data`` を指定すると、Docker は既存のボリュームを参照せず、
   同名の空のボリュームを新規作成します。コマンドはエラーにならず中身が空のアーカイブが
   作成されるため、バックアップが取得できたように見えてしまいます。

.. note::

   |Fess| 本体（``fess01``）のコンテナーには専用のボリュームがないため、バックアップ対象は
   上記の 2 つのみです。ただし、管理画面から変更した全般設定や、管理画面からインストールした
   プラグインはコンテナー内にのみ保存され、コンテナーを再作成すると失われます。
   これらは Compose ファイルの ``FESS_JAVA_OPTS`` や ``FESS_PLUGINS`` で指定して永続化してください。

ステップ 2: 現在のバージョンの停止
==================================

Fess と OpenSearch を停止します。

ZIP 版には停止用のスクリプトは同梱されていません。\ ``bin/fess`` を ``-p`` オプション付きで
起動していた場合は、PID ファイルを使って停止します::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

``-p`` を指定せずに起動していた場合は、プロセス ID を確認して ``kill`` します
（``-d`` だけでは PID ファイルは作成されません）。

RPM/DEB 版 (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. warning::

   ステップ 3 を始める前に |Fess| が停止していることを確認してください。起動中の |Fess| のパッケージや
   ファイルを入れ替えないでください。起動中の 15.8 の |Fess| で DEB パッケージを 15.10 のものに
   入れ替えたところ、|Fess| を再起動するまで検索画面が ``404`` を返しました。パッケージ版では
   ``systemctl status fess.service`` で確認できます。

ステップ 3: 新しいバージョンのインストール
==========================================

インストール方法により、手順が異なります。

ZIP 版
-------------

1. 新しいバージョンをダウンロードして展開::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.10.0/fess-15.10.0.zip
       $ unzip fess-15.10.0.zip

   .. note::

      |Fess| のアーカイブ版は ZIP 形式でのみ配布されています（``fess-15.10.0.tar.gz`` は
      提供されていません）。

2. 古いバージョンの設定をコピー::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.10.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/

   .. warning::

      ``fess_config.properties`` と ``fess.in.sh`` をそのままコピーすると、15.9 で既定値が変わった
      値も含めて、旧バージョンの値が引き継がれます。たとえば、アップグレード後に作成したジョブの
      既定は Groovy になります。後の 2 つのコマンドを実行する前に、各ファイルを ``fess-15.10.0``
      のファイルと比較し、自分で変更した値だけを移してください。確認すべき項目は
      :ref:`upgrade-159-carried-over-config` を参照してください。

3. カスタマイズしている場合は、以下もコピーします::

       # Tomcat の設定（SAML で必要な tomcat.sameSiteCookies=none もここにあります）
       $ cp /path/to/old-fess/lib/classes/tomcat_config.properties /path/to/fess-15.10.0/lib/classes/
       # インストール済みプラグイン
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.10.0/app/WEB-INF/plugin/
       # 自分でアップロードしたテーマ（テーマごとのディレクトリ。bootstrap は除く）
       $ cp -r /path/to/old-fess/app/themes/<your-theme> /path/to/fess-15.10.0/app/themes/

   .. warning::

      旧バージョンの ``tomcat_config.properties`` をコピーしないと、 ``tomcat.sameSiteCookies`` は
      何も知らせずに既定値の ``lax`` に戻り、SAML ログインが動作しなくなります
      （ :ref:`upgrade-159-saml` を参照）。このファイルの同梱の内容は 15.8.0 と 15.10 で同じなので、
      そのままコピーできます。

   .. warning::

      ``log4j2.xml`` を 15.10 のファイルに上書きコピーしないでください。15.10 のファイルは
      ``RequestLoggingFilter`` のロガーを ``warn`` に固定しており、15.8 のファイルをコピーすると
      この設定が失われます。ログレベルを DEBUG にすると、リクエストヘッダー（ ``Authorization`` を含む）と
      リクエストパラメーター（ログインフォームに入力したパスワードを含む）がログに書き出されます。
      2 つのファイルを ``diff`` で比較し、自分で変更した内容だけを 15.10 のファイルに再適用してください。

   .. warning::

      ``app/themes/`` ディレクトリ全体はコピーしないでください。このディレクトリには |Fess| に
      同梱のテーマ ``bootstrap`` も入っており、15.10 のものに上書きすると、15.10 の検索画面が
      15.8 版のテーマに置き換わります。コピーするのは自分で作成したテーマのディレクトリだけにして
      ください。 |Fess| プロジェクトが公開しているテーマは、 ``bin/fess-setup install theme <name>``
      で 15.10 向けのビルドをインストールしてください（ :doc:`fess-setup` を参照）。

   .. warning::

      管理画面「デザイン」で編集した JSP（``app/WEB-INF/view/``）はコピーしないでください。
      15.10 の検索画面はテーマで、これらの JSP を使いません。変更内容の移し先は
      :ref:`upgrade-159-static-theme` を参照してください。

   .. note::

      ``app/WEB-INF/plugin/`` からコピーしたプラグインは、旧バージョン向けにビルドされています。
      コピーした後、 ``fess-15.10.0`` で ``bin/fess-setup upgrade plugins`` を実行し、15.10 向けに
      ビルドされたバージョンに入れ替えてください（ :ref:`upgrade-plugin-versions` を参照）。

4. 設定差分を確認し、必要に応じて調整します

RPM/DEB 版
----------

新しいバージョンのパッケージをインストール::

    # RPM
    $ sudo rpm -Uvh fess-15.10.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.10.0.deb

.. note::

   RPM 版では ``/etc/fess/*`` の設定ファイルは ``%config(noreplace)`` として登録されているため、
   アップグレード時も保持されます（新しい既定のファイルは ``.rpmnew`` として併置されます）。
   新しい設定オプションが追加されている場合は、手動で調整が必要です。変更を加えた
   ``/etc/fess/fess_config.properties`` は、ZIP 版の手順でコピーしたファイルと同様に、15.10 でも
   旧バージョンの値のまま使われます。 :ref:`upgrade-159-carried-over-config` を参照してください。

.. warning::

   DEB 版では、 ``/etc/fess`` 以下のファイル（ ``fess_config.properties`` や
   ``tomcat_config.properties`` など）は、 ``/etc/default/fess``\ 、\ ``/etc/init.d/fess``\ 、
   ``/usr/lib/systemd/system/fess.service`` と同様に conffile として登録されています。15.8 からの
   最初のアップグレードでは、 ``dpkg`` は次のように扱います。

   - 編集していないファイルは、確認なしに 15.10 のファイルへ置き換えられます。
   - 編集したファイルについては、 ``dpkg`` が確認を求めます。自分のファイルを残す場合（既定の回答、または
     ``--force-confold`` ）は、15.10 のファイルが ``<ファイル名>.dpkg-dist`` として併置されます。新しいファイルを
     インストールする場合（ ``Y`` または ``--force-confnew`` ）は、自分のファイルが
     ``<ファイル名>.dpkg-old`` として保存されます。
   - 回答する人がいないとき、 ``dpkg -i`` と ``apt-get install -y`` は最初の確認で停止します。
     無人でアップグレードする場合は ``--force-confold`` を指定してください（ ``--force-confdef`` でも確認は
     出なくなります）。たとえば ``sudo dpkg --force-confold -i fess-15.10.0.deb`` や
     ``sudo apt-get install -y -o Dpkg::Options::=--force-confold ./fess-15.10.0.deb`` です。

   いずれの場合も、事前に ``/etc/fess`` をバックアップしてください（ステップ 1）。残したファイルは 15.8 の値の
   ままなので、そのまま使わず ``.dpkg-dist`` のファイルと比較してください（
   :ref:`upgrade-159-carried-over-config` を参照）。なお ``/etc/fess/system.properties`` はパッケージに
   含まれない実行時生成ファイルのため、上書きされません。

Docker 版
---------

1. 新しいバージョンの Compose ファイルを取得::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.10.0/compose/compose-opensearch3.yaml

2. 新しいイメージを取得::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

ステップ 4: OpenSearch のアップグレード
=======================================

|Fess| 15.10 は OpenSearch 3.9.0 に対応しています。接続先の OpenSearch がこれより古い場合は、
以下の手順でアップグレードしてください。

.. note::

   この手順は ZIP 版および RPM/DEB 版で OpenSearch を手動運用している場合の手順です。
   Docker 版では、ステップ 3 で新しいイメージを取得すると OpenSearch とプラグインも
   まとめて更新されるため、本ステップは不要です。

.. important::

   |Fess| 15.10 は、チャンクベクトル検索（セマンティック検索）の利用有無にかかわらず、
   検索インデックスの設定に ``index.knn`` を、マッピングに ``content_chunk_vector``\ （\ ``knn_vector``
   型）を常に含めます。そのため、接続先の OpenSearch には **k-NN プラグインが必須** です。

   - 標準配布の OpenSearch および Docker 版のイメージには同梱されています。
   - **minimal 配布には含まれないため、インデックスの新規作成に失敗し、\ |Fess| が起動できません。**
   - インデックス設定には ``knn.derived_source.enabled`` も常に送信されます。これを認識できない
     古い OpenSearch では、k-NN プラグインの有無にかかわらずインデックスの作成に失敗します。

   詳細は :doc:`../config/search-semantic` の「前提条件」を参照してください。

.. warning::

   OpenSearch のメジャーバージョンアップグレードは慎重に行ってください。
   インデックスの互換性に問題が発生する可能性があります。
   |Fess| 14.x は OpenSearch 2.x 系のため、14.x からのアップグレードでは必ずこのケースに該当します。

   OpenSearch 3.9.0 で取得したスナップショットは、3.8.0 以前の OpenSearch には復元できません。切り戻しに備えて、アップグレード前に取得したスナップショットを残しておいてください。

1. 新しいバージョンの OpenSearch をインストール

2. プラグインを再インストール::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-fess/3.9.0/opensearch-analysis-fess-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-analysis-extension/3.9.0/opensearch-analysis-extension-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-minhash/3.9.0/opensearch-minhash-3.9.0.zip
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install https://maven.codelibs.org/release/org/codelibs/opensearch/opensearch-configsync/3.9.0/opensearch-configsync-3.9.0.zip

   .. note::

      これらのプラグインのバージョンは、使用する OpenSearch のバージョンと一致させる必要があります。
      |Fess| 15.10 は OpenSearch 3.9.0 に対応しています。バージョンが一致しない場合、
      プラグインのインストールに失敗します。

      |Fess| 用の 4 つのプラグインは maven.codelibs.org で公開しているため、URL で指定します。 ``opensearch-plugin install`` の ``groupId:artifactId:version`` 形式は Maven Central だけを参照します。

3. 辞書ディレクトリを OpenSearch の設定ディレクトリの下へ移動

   OpenSearch 3.8.0 以降は、辞書ファイルが OpenSearch の設定ディレクトリの外にあるとインデックスの作成を拒否します。
   以前の手順どおり ``configsync.config_path`` に ``/var/lib/opensearch/data/config/`` （ZIP 版では ``/path/to/opensearch/data/config/``）など設定ディレクトリの外を指定している場合、
   |Fess| はインデックスを作成できず、起動しません。
   RPM/DEB 版では、次のように辞書ファイルを ``/etc/opensearch/dictionary/`` へコピーします::

       $ sudo install -d -o opensearch -g opensearch -m 0750 /etc/opensearch/dictionary
       $ sudo cp -a /var/lib/opensearch/data/config/. /etc/opensearch/dictionary/
       $ sudo chown -R opensearch:opensearch /etc/opensearch/dictionary

   そのうえで、 ``/etc/opensearch/opensearch.yml`` の ``configsync.config_path`` と、 |Fess| の ``FESS_DICTIONARY_PATH`` （RPM 版は ``/etc/sysconfig/fess`` 、DEB 版は ``/etc/default/fess``）を、どちらも ``/etc/opensearch/dictionary/`` に変更します。
   ZIP 版では、OpenSearch の ``config/dictionary/`` を使用します。詳細は :doc:`install-linux` を参照してください。

4. OpenSearch を起動::

       $ sudo systemctl start opensearch.service

ステップ 5: 新しいバージョンの起動
==================================

ZIP 版::

    $ cd /path/to/fess-15.10.0
    $ ./bin/fess -d -p /path/to/fess-15.10.0/fess.pid

.. note::

   ``-p`` を指定すると PID ファイルが作成され、次回の停止時に
   ``kill $(cat /path/to/fess-15.10.0/fess.pid)`` で停止できます。

RPM/DEB 版::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

ステップ 6: 動作確認
====================

1. **ログの確認**

   エラーがないことを確認します。

   ZIP 版::

       $ tail -f /path/to/fess/logs/fess.log

   RPM/DEB 版::

       $ sudo tail -f /var/log/fess/fess.log

   Docker 版::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      同じログディレクトリーに、クロール処理の ``fess-crawler.log``\ 、認証や管理操作の
      ``audit.log``\ 、検索リクエストの ``searchlog.log`` も出力されます。

2. **Web インターフェースへのアクセス**

   ブラウザーで http://localhost:8080/ にアクセスします。

3. **管理画面へのログイン**

   http://localhost:8080/admin にアクセスし、管理者アカウントでログインします。

4. **バージョンの確認**

   管理画面で「システム情報」→「設定情報」をクリックし、「システムのプロパティ」に表示される
   ``fess.version`` が新しいバージョンになっていることを確認します。

5. **検索の動作確認**

   検索画面で検索を実行し、正常に結果が返されることを確認します。

ステップ 7: インデックスの再作成（推奨）
========================================

メジャーバージョンアップの場合、インデックスを再作成することを推奨します。

.. note::

   以下の手順はクロールの再実行であり、インデックスのマッピング（フィールド定義）自体は
   更新されません。チャンクベクトル検索（セマンティック検索）を新たに有効にする場合など、
   マッピングの更新を伴う再インデックスが必要な場合は、管理画面 > システム情報 > メンテナンス の
   「再インデクシング」を別途実行してください。詳細は
   :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）を
   参照してください。

   15.8 以前で作成した文書インデックスを引き続き使う場合は、 :ref:`upgrade-reindex-new-fields` も参照してください。

.. warning::

   15.8 が受け付けた辞書のエントリーのうち、OpenSearch 3.9.0 が拒否するものがあります。たとえば
   同じ ``mapping`` のエントリーを 2 回保存している場合や、 ``kuromoji`` のトークンに空白が含まれる
   場合です。そのようなエントリーがあると「再インデクシング」は新しい文書インデックスを作成しません。
   ``fess.log`` には ``Failed to create index`` としか出力されず、古いインデックスが検索を提供し続けます。
   「システム」→「辞書」で辞書をダウンロードし、重複または不正な行を削除してから再度アップロードし、
   「再インデクシング」をもう一度実行してください。15.10 が保存しなくなったエントリーは
   :ref:`upgrade-159-api-requests` を参照してください。

1. 既存のクロールスケジュールを確認
2. 「システム」→「スケジューラ」から「Default Crawler」を実行
3. クロールが完了するまで待機
4. 検索結果を確認

.. warning::

   再インデクシングでは新しいマッピングでインデックスが作り直されるため、k-NN プラグインの
   ない OpenSearch では失敗します。ステップ 4 の注意事項を確認してください。

15.9 から 15.10 へのアップグレード
==================================

このセクションの変更は、15.10 へのすべてのアップグレードに関係します。15.8 以前からアップグレードする場合は、続く「15.8 から 15.10 へのアップグレード」も読んでください。

.. _upgrade-1510-client-ip:

ログに記録されるクライアントの IP アドレス
------------------------------------------

15.9 までは、監査ログの ``ip`` と検索ログの ``clientIp`` には、リクエストの ``X-Forwarded-For`` ヘッダーの値が、送信元にかかわらずそのまま記録されていました。複数のアドレスがあれば全体が記録され、クライアントが任意の値を送ることもできました。
15.10 は、回数制限（ :doc:`../config/rate-limiting` ）と同じ規則でアドレスを決めます。リクエストの送信元が ``rate.limit.trusted.proxies`` （既定値は ``127.0.0.1,::1`` ）に含まれる場合だけ ``X-Forwarded-For`` （複数の行に分かれていればすべての行）と ``X-Real-IP`` を使い、 ``X-Forwarded-For`` は右端から読んで、信頼するプロキシではない最初のアドレスを記録します。含まれない場合は送信元のアドレスを記録します。この規則は ``rate.limit.enabled`` が ``false`` でも適用されます。

``rate.limit.trusted.proxies`` に含まれないリバースプロキシの背後では、すべてのリクエストがプロキシのアドレスで記録されます。元のクライアントのアドレスを記録するには、プロキシのアドレスを ``rate.limit.trusted.proxies`` に追加してください。

``rate.limit.trusted.proxies`` に含まれないアドレスから届いたリクエストが ``X-Forwarded-For`` または ``X-Real-IP`` を持っている場合、15.10 は、送信元のアドレスと ``rate.limit.trusted.proxies`` を示す警告を ``fess.log`` へ出力します。警告はリクエストごとではなく起動後に 1 回だけ出力されるため、示されるのは最初に見つかったアドレスだけで、ヘッダーの値は含まれません。ヘッダーは従来どおり無視されるので、ログ以外の動作は変わりません。ログインフォームも同じ制限を使うため（下の「ログインフォームの回数制限」を参照）、このようなプロキシの背後にあるすべてのクライアントは 1 つのアドレスとして数えられ、ログインの失敗が制限に達すると、そのすべてのクライアントのログインが拒否されます。この警告が出た場合は、プロキシのアドレスを ``rate.limit.trusted.proxies`` に追加してください。

.. _upgrade-1510-cipher-key:

``app.cipher.key`` の警告
-------------------------

``app.cipher.key`` が空か、``fess_config.properties`` に同梱の値（ ``___change__me___`` ）のままの場合、15.10 は起動時に ``fess.log`` へ警告を出力します。クローラーなどのジョブのプロセスは出力しません。
この鍵は、クロール設定やデータストア設定に保存されるパスワードなどの暗号化に使われ、同梱の値は公開されています。|Fess| は鍵を自動では変更しません。変更すると、以前の鍵で暗号化された値は復号できなくなるため、運用を始める前に設定してください。

その他の動作の変更
------------------

- 管理画面の「検索リスト」と「クロール情報」の「すべて削除」には、編集ロール（ ``admin-searchlist`` ・ ``admin-crawlinginfo`` ）が必要です。15.9 までは、画面にボタンが表示されないだけで、表示ロール（ ``-view`` が付くロール）だけを持つユーザーのリクエストも受け付けていました。
- マッピング辞書の項目は、変換後（ ``output`` ）が必須です。15.9 までは、省略しても管理画面と管理 API が受け付け、何も保存されませんでした。
- 検索で、ダブルクォーテーションで囲んだ 1 語（ ``"less"`` など）は、その語だけに一致します。15.9 までは、 ``query.boost.fuzzy.min.length`` （既定値は ``4`` ）以上の長さの語に、あいまい一致の条件が加わり、 ``fess`` を含む文書も ``"less"`` に一致していました。引用符のない語と、フィールドを指定した語（ ``content:"less"`` など）は変わりません。
- ``suggest.popular.word.cache.expire`` は秒として読み込まれます（``fess_config.properties`` と :doc:`../config/properties` の記載どおりです）。15.9 までは値が分として使われていたため、既定値の ``60`` では人気ワードが 60 分間キャッシュされていましたが、15.10 では 60 秒間です。長いキャッシュを維持するには、秒単位でより大きい値（60 分なら ``3600``）を設定してください。キャッシュは、サジェストジョブが実行されるたびにクリアもされます。
- 文書 ID による文書の取得にも、検索と同じように仮想ホストの絞り込みが適用されます。15.9 までは、``/api/v2/cache/{docId}``、``/go/`` のリダイレクト、サムネイル、お気に入りのエンドポイントなど、文書 ID による取得にはロールの絞り込みだけが適用されていたため、ロールが一致すれば別の仮想ホストの文書にも応答していました。15.10 では、そのような文書は見つからないものとして扱われます。検索と同じく、リクエストで仮想ホストが決まる場合は、仮想ホストの値を持たない文書は返されません。仮想ホストが決まらないリクエスト（既定のホスト）では、動作は変わりません。
- サジェストジョブは、検索で隠れる文書から語を取り込まなくなりました。``role`` の値を持たない文書と、拒否エントリーを持つ文書（``role.search.denied.prefix``\ （既定は ``D``）の後にユーザー、グループ、ロールのいずれかの接頭辞が続く値。既定では ``D1``、``D2``、``DR``）は、対象外になります。15.9 までは、これらの文書の語がすべてのユーザーにサジェストされていました。許可エントリーと拒否エントリーの両方を持つ文書は、サジェストのリクエストでは特定のユーザーだけを拒否する条件を表せないため、文書全体が対象外になります。すでにこれらの文書から作られたサジェストのエントリーは、サジェストの古いデータを消去する通常の処理で期限切れになります。

.. _upgrade-1510-tika:

Apache Tika 4 と ``tika.xml``
-----------------------------

15.9.0 は Apache Tika 3.3.2 を使用していましたが、15.10 は Apache Tika 4.1.0 を使用します。
Tika 4 には XML 形式の設定ファイルがないため、|Fess| 15.10 は Tika のパーサーをコード内で構築し、``tika.xml`` を読み込みません。
15.10 の ZIP 版、RPM/DEB 版、Docker イメージには、このファイルは含まれません。

``tika.xml`` に記述した ``parser-exclude`` などの設定は適用されなくなり、除外していたパーサーは再び動作します。
以前のバージョンの ``tika.xml`` が設定ディレクトリに残っている場合、|Fess| はそのファイルを無視し、起動時に ``fess.log`` へ警告を出力します。ファイルを削除してください。

- ZIP 版: 15.9 以前の ZIP 版では ``app/WEB-INF/classes/tika.xml`` にあります。15.10 の起動時の警告は、``app/WEB-INF/classes`` と ``app/WEB-INF/conf`` の両方を調べます
- RPM/DEB 版: ``/etc/fess/tika.xml``

.. _upgrade-1510-tika-metadata:

メタデータ名
------------

Tika 4 では、多くのメタデータ名が変更されました。たとえば、``pdf:charsPerPage`` は ``pdf:chars-per-page`` に、``access_permission:*`` は ``access-permission:*`` に、``Message:*`` は ``message:*`` になりました。
Tika の ``LegacyKeyMigrationFilter`` が対応しているメタデータ名は、|Fess| が Tika 3 の名前に戻します。そのため、それらの名前を使った ``crawler.metadata.name.mapping`` の設定はそのまま動作します。
このフィルターが変換しないメタデータ名は、Tika 4 の名前のまま渡されます。たとえば、Excel ファイルの ``protected`` は ``msoffice:excel:protected-worksheet`` になりました。このような名前を ``crawler.metadata.name.mapping`` で使っている場合は、Tika 4 の名前に変更してください。

Tika 4 で新たに加わったメタデータは、ほかのメタデータと同じように扱われ、``crawler.metadata.content.excludes`` に名前が一致しない限りコンテンツに追加されます。

例外は、Tika が内部の管理用に使う ``tk:``、``X-TIKA:``、``zip:`` で始まる名前です（Tika 3 の ``X-TIKA:Parsed-By`` は ``tk:parsed-by`` になりました）。|Fess| はこれらの名前をドキュメントに渡す前に削除します。Tika 3 の名前には戻されず、``crawler.metadata.content.excludes`` に指定があるかどうかにかかわらずコンテンツにも追加されません。``crawler.metadata.name.mapping`` で ``X-TIKA:*`` や ``tk:*`` の名前をマッピングしている場合や、スクリプトで使っている場合、これらの値は取得できなくなります。

画像のメタデータとコンテンツ
----------------------------

15.9 までは、画像ファイル（PNG、JPEG、TIFF、GIF、BMP など）のメタデータがすべてコンテンツに追加されていたため、画像のコンテンツは、ピクセル、カラープロファイル、カメラの設定に関する値の羅列になっていました。
15.10 では、MIME タイプが ``image/*`` のドキュメントのコンテンツには、名前が ``crawler.metadata.content.image.includes`` に一致するメタデータだけを追加します。デフォルトでは、EXIF、XMP、IPTC のタイトル、説明、作成者、キーワード、コメント、著作権、地名と、Windows エクスプローラーのプロパティ、PNG のテキストチャンクが対象です。
それ以外のメタデータも抽出はされるため、``crawler.metadata.name.mapping`` やスクリプトで使えます。このリストに一致する名前にも ``crawler.metadata.content.excludes`` は適用されます。

アップグレード前にインデックスした画像のコンテンツは、その画像を再度クロールするまで変わりません。

クロール設定の Tesseract と PDF のプロパティファイル
----------------------------------------------------

クロール設定で ``config.tika.tesseract.config`` または ``config.tika.pdf.config`` を指定している場合は、Tika 4 でプロパティの名前変更や削除があったため、そのプロパティファイルを確認してください。
適用できないキーがあると、|Fess| はキーごとに ``fess-crawler.log`` へ警告を出力し、そのキーを無視します。

- Tesseract のファイルの ``timeoutSeconds`` は ``timeoutMillis`` になりました。|Fess| は ``timeoutSeconds`` を ``timeoutMillis``\ （値を 1000 倍）に変換しますが、今後は ``timeoutMillis`` にミリ秒で記述してください。``crawler.document.ocr.timeout`` は引き続き秒単位です。
- PDF のファイルの ``ocrStrategy``、``ocrDPI``、``ocrImageType``、``ocrImageFormatName``、``ocrImageQuality``、``ocrRenderingStrategy``、``accessChecker``、``renderer`` などのプロパティは、Tika 4 の ``PDFParserConfig`` から削除されました。|Fess| はこれらを無視し、``fess-crawler.log`` に警告を出力します。この場合、PDF の OCR は Tika 4 の既定の動作（自動）に従います。つまり、``tesseract`` が使用でき、|Fess| で OCR が有効なときに、テキストの少ないページに対して OCR が実行されます。
- ``tesseract`` の場所は ``tika.xml`` では設定できなくなり、Tesseract のファイルの ``tesseractPath``、``tessdataPath``、``imageMagickPath`` も効果がありません。``tesseract``（および使用する場合は ImageMagick）は、クローラープロセスの ``PATH`` から見つかる必要があります。

文字エンコーディングの判定
--------------------------

Tika 4 がテキストファイルについて報告する文字エンコーディング名は、15.9 と異なる場合があります。たとえば、Shift_JIS は ``windows-31j``、ISO-8859-1 は ``windows-1252``、EUC-JP は ``x-eucJP-Open`` と報告されます。

``Content-Length`` がコンテンツに追加されなくなった
---------------------------------------------------

15.8.0 と 15.9.0 は、文書のコンテンツに ``Content-Length`` メタデータの値を追加していました。プレーンテキストのファイルではその値が ``0`` だったため、索引内のコンテンツの末尾に空白と ``0`` が付いていました。15.10 は、 ``crawler.metadata.content.excludes`` に含まれているかどうかにかかわらず、 ``Content-Length`` をコンテンツに追加しません。値の抽出は引き続き行われるため、 ``crawler.metadata.name.mapping`` やスクリプトでは利用できます。アップグレード前にインデックスした文書のコンテンツは、再クロールするまで変わりません。

ログインフォームの回数制限
--------------------------

15.9 では、``theme.api.login.rate.limit.*`` の回数制限は ``/api/v2/auth/login`` だけに適用され、ログイン画面（``/login/``）のログインフォームには適用されませんでした。
15.10 では、ログインフォームも同じ制限と同じカウンターを使います。同じ IP アドレスから失敗したログインが毎分 10 回に達するか、同じ IP アドレスから同じユーザー名でパスワードを 5 回間違えると、``theme.api.login.lockout.seconds``\ （既定は 900 秒）の間、その IP アドレス、またはその IP アドレスとユーザー名の組み合わせからのログインが拒否されます。
拒否されたときは正しいパスワードでもログインできず、画面にはパスワードを間違えたときと同じメッセージが表示されます。ログインに成功すると、その試行が使った枠は戻ります。
パスワードを間違える可能性のあるスクリプトや、同じ IP アドレスを共有する多数の利用者がいる環境では、この制限を考慮してください。

リバースプロキシが ``X-Forwarded-For`` を別の行として追加する場合（HAProxy の ``option forwardfor`` など）、15.10 はすべての行を読んで右端から信頼するプロキシではない最初のアドレスをクライアントの IP とします（:doc:`../config/rate-limiting`）。15.9 までは 1 行目（クライアントが送った値）だけを読むため、クライアントが回数制限に使われるアドレスを選べました。

クロール設定のパーミッションの (deny)
-------------------------------------

クロール設定などのパーミッション欄に ``(deny) {user}name`` のように ``(deny)`` の後に空白を入れて書くと、15.9 では拒否として保存されず、空白付きの文字列がそのまま保存されました。さらに、その設定を編集画面で開いて更新すると、許可（``{user}name``）に変わりました。
15.10 では ``(deny)`` と ``(allow)`` の後の空白を取り除いて保存し、更新しても拒否のままです。``{user}``、``{group}``、``{role}`` のいずれも伴わない ``(deny)`` の行は保存されません。

15.9 以前に保存した設定は自動では直りません。``(deny)`` を使っているクロール設定のパーミッション欄を確認し、``(deny){user}name`` の形に書き直して保存してから再クロールしてください。

監査ログの制御文字
------------------

LTSV 形式では、フィールドの値に含まれるすべての制御文字と、Unicode の行区切り（NEL・LS・PS）が空白に置き換わります（タブはアンダースコア）。入力された利用者名で 2 件目のレコードを始めることはできません。15.9 が置き換えていたのは CR と LF だけでした。

ACL から読み取るファイルのロール
--------------------------------

ACL を持つファイルシステム（NTFS など）上のローカルファイル（``file:`` の URL）をクロールし、``file.role.from.file`` が既定の ``true`` のままの場合、15.9 は、ファイルのすべての ACL エントリーを、エントリーの種類や権限にかかわらず、その文書を読めるロールにしていました。そのため、読み取りを拒否されたユーザーや、書き込みだけを許可されたユーザーも、インデックスされた文書の閲覧者になっていました。

15.10 は、各エントリーの種類と権限を確認します。

- データの読み取り（``READ_DATA``）を含む ALLOW エントリーは、従来どおり、そのユーザーまたはグループにロールを与えます。
- ``READ_DATA`` を含む DENY エントリーは、拒否ロール、つまり ``role.search.denied.prefix``\ （既定は ``D``）を前に付けたロールを与えます。SMB クロールが使う接頭辞と同じです。検索では、そのユーザーまたはグループに対して文書が表示されなくなります。
- AUDIT と ALARM のエントリー、および ``READ_DATA`` を含まないエントリーは無視されます。

POSIX 権限（所有者とグループ）から読み取るロールは変わりません。

文書は、再度クロールされるまで、インデックスされたときのロールを保持します。すでにある文書に新しい規則を適用するには、ファイルクロールをもう一度実行してください。

LDAP のロール OU とネストされたグループ
---------------------------------------

|Fess| が LDAP / Active Directory のユーザーの権限を解決するとき（:doc:`../config/ldap-integration` を参照）、グループエントリーの DN によって、そのエントリーがロール（権限の接頭辞は ``role.search.role.prefix``、既定は ``R``）になるか、グループ（``role.search.group.prefix``、既定は ``2``）になるかが決まります。15.9 までは、DN のどこかに ``ou=role`` というテキストが含まれていればロールとして扱われたため、``OU=Roles-Requests`` や ``OU=RoleOwners`` の下のエントリーもロールになっていました。

15.10 は DN を解析し、``ou`` の要素のいずれかがちょうど ``Role`` または ``Roles`` である（大文字小文字は区別しません）場合だけ、そのエントリーをロールとして扱います。それ以外のエントリーはすべてグループです。DN を解析できないエントリーもグループです。

そのため、``OU=Roles-Requests`` のような OU の下のエントリーは、ロールの権限名ではなくグループの権限名（``Rname`` ではなく ``2name``）になり、古い権限名を持つ文書は、これらのグループのユーザーに一致しなくなります。このような OU を利用していた場合は、エントリーを ``OU=Role`` または ``OU=Roles`` に移すか、古い権限名を使っている権限設定を更新し、もう一度クロール（または再インデックス）してください。

``ldap.group.filter`` を設定している場合（既定は空です）、|Fess| はこのフィルターで、ユーザーのグループを含むグループ（ネストされたグループ）を検索します。15.9 までは、ユーザーのグループの DN をエスケープせずにこのフィルターへ入れていました。``CN=Sales\, EMEA,...`` のカンマのようにエスケープされた文字を含む DN には一致しないため、そのグループのネストされたグループはエラーも出ずに取得されず、LDAP フィルターで特別な意味を持つ文字を含む DN はフィルターそのものを変えてしまいました。15.10 は DN をエスケープします（RFC 4515）。そのようなグループのネストされたグループも取得されるようになり、該当するユーザーはそれらのグループの権限も持つようになります。

cipher を設定していない場合のリクエストのロール
-----------------------------------------------

``fess.xml`` の ``roleQueryHelper`` コンポーネントに ``parameterKey``、``headerKey``、``cookieKey`` を設定すると、|Fess| はリクエストのパラメーター、ヘッダー、Cookie からユーザーのロールを読み取ります。値は、``encryptedParameterValue``、``encryptedHeaderValue``、``encryptedCookieValue`` を ``false`` にしない限り、暗号化されていることが前提です（3 つとも既定は ``true`` です）。

15.9 までは、暗号化されていることが前提の値でも、``cipher`` が設定されていなければ平文として読み取られたため、どのクライアントでもロールの一覧を送ることができました。15.10 はそのような値を無視し、起動後に 1 回だけ ``fess.log`` へ警告を出力します。フラグが ``false`` の値は従来どおりそのまま読み取られ、``cipher`` が設定されていれば従来どおり復号されます。

``roleQueryHelper`` でキーを設定しているのに ``cipher`` を設定していない場合は、``cipher`` を設定して暗号化した値を送るか、暗号化せずに送る値のフラグを ``false`` にしてください。同梱の ``fess.xml`` ではこれらの設定がコメントアウトされているため、既定の構成は影響を受けません。

プラグイン開発者向けの変更
--------------------------

次の変更は、``fess-crawler`` のクラスを使うプラグインに影響します。そのようなプラグインは 15.10 向けに再ビルドしてください（:ref:`upgrade-plugin-versions` を参照）。

- ``ExtractData`` は Tika のインターフェース（``TikaCoreProperties``、``HttpHeaders`` など）を実装しなくなりました。文字列定数 ``CONTENT_TYPE`` と ``CONTENT_ENCODING`` は ``ExtractData`` 自身が定義します。``RESOURCE_NAME_KEY`` は従来どおり ``"resourceName"`` です。
- ``TikaExtractor.setTikaConfig`` と、``fess.xml`` の ``tikaConfig`` コンポーネントを削除しました。
- ログレベルが ``debug`` のとき、``CrawlJob`` はクローラーに ``-Dorg.apache.tika.service.error.warn=true`` を渡さなくなりました。Tika 4 がこの値を読まないためです。

15.10 の ``WEB-INF/lib`` には、15.9 に含まれていた次のライブラリも含まれなくなりました。これらは Tika 3 のモジュールが引き込んでいたもので、15.10 が使う Tika 4 のモジュールは依存していません。15.10 の WAR のクラスはこれらを参照していません。

- 含まれなくなったライブラリは、JAXB（``jakarta.xml.bind-api``、``jaxb-core``、``jaxb-runtime``、``txw2``、``istack-commons-runtime``）、``jempbox``、``xmpbox``、``juniversalchardet`` です。``jakarta.activation-api`` と ``angus-activation`` は引き続き含まれます。
- プラグインがこれらのライブラリのクラスを使う場合は、ライブラリをプラグインの JAR に含めてください（たとえば Maven Shade Plugin で同梱します）。プラグインは WAR が提供するクラスには依存できますが、他のプラグインのクラスには依存できず、15.10 の WAR はこれらを提供しません。``WEB-INF/lib`` のクラスは ``WEB-INF/plugin`` のクラスより先に解決されるため、WAR に無いライブラリを同梱しても重複しません。
- プラグインが影響を受けるかどうかは、必要とするクラスが 15.10 の ``WEB-INF/lib`` の JAR に含まれているかで確認できます。削除されたクラスを使う処理は、たとえば ``NoClassDefFoundError`` で実行時に失敗します。これらのクラスを使わない処理には影響しません。

15.9 向けにビルドされたプラグイン
---------------------------------

15.9.0 向けにビルドされたプラグインは、再ビルドしなくても 15.10 の war で導入・起動・クロールができることを確認しています。ただしこれは確認した結果であり、互換性の保証ではありません。 ``fess-crawler`` のクラスを使うプラグインは、「プラグイン開発者向けの変更」のとおり再ビルドが必要です。

それでもプラグインは 15.10 のものに入れ替えてください（ :ref:`upgrade-plugin-versions` ）。 ``bin/fess-setup check`` は、15.9.0 のプラグインの jar を「別のリリース向けにビルドされている」として FAIL と報告し、 ``upgrade plugins`` を案内します。

特に、 ``fess-storage-s3`` と ``fess-storage-gcs`` の 15.9.0 の jar を残さないでください。15.9.0 のこれらのプラグインは、ストレージの一覧取得に失敗してもエラーを返しません。そのため、ストレージに到達できない場合、認証が正しくない場合、バケットが存在しない場合のいずれでも、管理 API の ``/api/admin/storage/list`` は成功を表す空の一覧 ``{"items":[],"status":0}`` を返します。15.10 のプラグインは失敗を例外として返し、15.10 はそれをエラー応答にします。古い jar が残っていると、この 15.10 の改善は効きません。

15.8 から 15.10 へのアップグレード
==================================

15.8 からアップグレードする場合、以下が互換性のない変更です。15.7 以前からアップグレードする場合も
これらがすべて当てはまります。「組み込み OpenSearch の廃止」から「既存の文書インデックスへの新しい
フィールドとかなの正規化の反映」までの各節（組み込み OpenSearch、スクリプトエンジン、S3 と SSO の
プラグイン、Index Exporter ジョブなど）と、このページの最後にある「機能別の移行作業」をすべて
読んでください。

組み込み OpenSearch の廃止
--------------------------

15.8 までは ``SEARCH_ENGINE_HTTP_URL`` を設定せずに ``bin/fess`` を起動すると、|Fess| が自身の
JVM 内で OpenSearch ノードを起動していました。15.10 ではこの構成がなくなり、検索エンジンは常に
別のサーバーになります。

``bin/fess.in.sh`` は既定で ``SEARCH_ENGINE_HTTP_URL=http://localhost:9200`` を設定します。
接続先の OpenSearch がない場合、|Fess| は起動に失敗します。 ``bin/fess-setup install opensearch``
で導入できます（Linux と Windows のみ。macOS には OpenSearch の公式配布がないため、Homebrew か
Docker を使用してください）。

また、 ``FESS_DICTIONARY_PATH`` をその OpenSearch の ``opensearch.yml`` にある ``configsync.config_path`` と一致させる必要があります。設定されていないか一致していないと、 |Fess| はインデックスを作成できません。15.10 の ``bin/fess.in.sh`` （Windows では ``bin\fess.in.bat`` ）は、 |Fess| のディレクトリの ``opensearch/`` に ``bin/fess-setup install opensearch`` で導入した OpenSearch が 1 つだけある場合に、これを自動で設定します。それ以外の OpenSearch を使う場合は、 :doc:`install-linux` または :doc:`install-windows` のとおりに設定してください。

あわせて次が廃止されました。

- ``es/`` ディレクトリ（ ``es/modules`` 、 ``es/plugins`` 、 ``es/data`` ）
- ``-Dfess.es.dir`` と ``SEARCH_ENGINE_HOME``
- ``bin/module.xml`` と ``bin/plugin.xml``
- 旧 ``elasticsearch.*`` 設定キーのフォールバック

また、OpenSearch 3 より前のバージョンに接続した場合、15.8 まではエラーログを出して起動を続行して
いましたが、15.10 では起動に失敗します。これらのバージョンは全文書を走査する処理が使う
``_shard_doc`` ソートを実装しておらず、HTTP 経由では失敗せずに応答が返らなくなるためです。

.. warning::

   組み込み OpenSearch で運用していた場合、インデックスデータは引き継げません。外部の
   OpenSearch サーバーを新しく構築し、管理画面「バックアップ」で設定を移したうえで
   再クロールしてください。バックアップに含まれるのはクロール設定・ユーザー・ログで、
   **クロール済みの文書は含まれません**。

.. note::

   15.8 のバックアップを新しい 15.10 のサーバーへ復元するときは、次の 2 点に注意してください。

   - ジョブは、サーバー上のものより新しい場合にだけ復元されます。そのため、15.8 で編集していない同梱ジョブは
     15.10 の JavaScript 版のまま残ります。15.8 で編集または作成したジョブは、保存されたスクリプトエンジン
     （同梱ジョブなら ``groovy``）のまま復元され、 ``fess-script-groovy`` プラグインがないと
     ``groovy is not found`` で失敗します。プラグインを導入するか、そのジョブを JavaScript に切り替えてください。
     どちらも :ref:`upgrade-159-script-engine` で説明しています。
   - Web 認証、クロール設定、データストア設定のパラメーターに保存されたパスワードやシークレットは
     ``app.cipher.key`` で暗号化されています。新しいサーバーの ``fess_config.properties`` に、旧環境の値を
     設定してください（ :ref:`upgrade-159-carried-over-config` を参照）。そうしないと復号できません。

Playwright クローラをプラグインへ移動
-------------------------------------

Playwright クローラと、それが使用する Node.js の実行ファイルは、配布物に含まれなく
なりました。 ``fess-15.8.0.zip``\ （457.1 MiB）では、Node.js の実行ファイルを収めた
Playwright のドライバーバンドルが 204.3 MiB を占めていました。

クロール設定の設定パラメータで ``client.crawlerClients=playwright:http://.*`` のように
Playwright クライアントを指定している場合は、プラグインと Node.js の両方を導入してください。
プラグインは管理画面の「システム > プラグイン」ページからも導入できます。 ``bin/fess.in.sh``
が Node.js の導入先を検出し、 ``PLAYWRIGHT_NODEJS_PATH`` を設定します。

::

    $ bin/fess-setup install plugin fess-crawler-playwright
    $ bin/fess-setup install nodejs

プラグインがない場合でも、そのような設定はクロールされますが、通常の HTTP クライアントが
使われるため、JavaScript によって生成されるテキストはインデックスされません。クロールジョブは
正常に終了し、障害 URL も記録されません。クロールのたびに、 ``fess-crawler.log`` にはクロール設定
ごとに 1 件、プラグイン名と上記の 2 つのコマンドを示す警告が記録されます。

Playwright で HTML ページのサムネイルを生成する ``fess-thumbnail-playwright`` プラグインも
Node.js で動作します。このプラグインを使用している場合も、 ``bin/fess-setup install nodejs``
で Node.js を導入してください。導入した Node.js は 2 つのプラグインで共用されます。

Playwright クローラも ``fess-thumbnail-playwright`` プラグインも使用していない場合、対応は不要です。

Google Cloud Storage をプラグインへ移動
---------------------------------------

Google Cloud Storage の SDK は配布物に含まれなくなり、 ``gcs://`` のクロールと ``gcs``
ストレージタイプは ``fess-storage-gcs`` プラグインから提供されます。管理画面の
「システム > プラグイン」ページ、または次のコマンドで導入してください。

::

    $ bin/fess-setup install plugin fess-storage-gcs

``crawler.file.protocols`` の既定値からも ``gcs`` が外れ、 ``file,smb,smb1,ftp`` に
なりました。プラグインを導入すると再び追加されます。導入前は、パスが ``gcs:`` で始まる
ファイルクロール設定について警告がログに記録されるだけで、何も取得できません。
アップグレードした既存インストールでは ``crawler.file.protocols`` がそのまま残るため、
パスは受け付けられますが、対応するクローラクライアントがありません。新規インストールでは
``gcs:`` が設定済みのプロトコルではないため、管理画面はそのパスの保存を拒否し、以前に
保存されたパスはローカルファイルパスとして扱われます。ストレージ画面も警告をログに記録し、
導入すべきプラグイン名を含むエラーを表示します。以前は空のファイル一覧を表示するだけでした。

Google Cloud Storage を使用していない場合、対応は不要です。Amazon S3 と MinIO などの
S3 互換ストレージも同じようにプラグインへ移動しました。次の節を参照してください。

Amazon S3 をプラグインへ移動
----------------------------

AWS SDK は配布物に含まれなくなり、 ``s3://`` のクロールと ``s3`` および ``s3_compat`` の
ストレージタイプは ``fess-storage-s3`` プラグインから提供されます。管理画面の
「システム > プラグイン」ページ、または次のコマンドで導入してください。

::

    $ bin/fess-setup install plugin fess-storage-s3

``crawler.file.protocols`` の既定値からも ``s3`` が外れ、 ``file,smb,smb1,ftp`` に
なりました。プラグインを導入すると再び追加されます。 ``storage.type`` の既定値は ``auto``
のままで、エンドポイントが未設定なら S3 に解決されるため、 ``s3`` を明示していなくても
プラグインを導入するまで管理画面のストレージは機能しません。 ``storage.*`` の設定値は
``WEB-INF/conf/system.properties`` にあるため残り、既存の ``crawler.file.protocols`` も
アップグレードで置き換わりません。

Amazon S3 と MinIO などの S3 互換ストレージを使用していない場合、対応は不要です。

SSO 認証をプラグインへ移動
--------------------------

4 種類の SSO 認証はいずれも配布物に含まれなくなり、 ``sso.type`` の値ごとに専用の
プラグインから提供されます。プラグインには必要な認証ライブラリも含まれます。 ``saml`` は
``fess-sso-saml`` 、 ``spnego`` は ``fess-sso-spnego`` 、 ``entraid`` （旧名の ``aad`` も
同じ）は ``fess-sso-entraid`` 、 ``oic`` は ``fess-sso-oidc`` です。最後の組み合わせに
注意してください。プラグイン名は ``fess-sso-oidc`` ですが ``sso.type`` の値は ``oic`` の
ままで、両者が異なるのはここ 1 か所だけです。使用するものを管理画面の
「システム > プラグイン」ページ、または次のコマンドで導入してください。

::

    $ bin/fess-setup install plugin fess-sso-saml

``sso.type`` と ``saml.*`` 、 ``spnego.*`` 、 ``entraid.*`` 、 ``aad.*`` 、 ``oic.*`` の各キーは
``WEB-INF/conf/system.properties`` にあるため、設定値はそのまま残ります。管理画面
「システム」→「全般」も 4 種類すべてを選択肢として表示し、設定欄も残ります。プラグインから
JSP を提供できないためで、この画面はプラグインが未導入であることを知らせません。

プラグインを導入するまで、 ``/sso/`` へのリクエストは SSO ログインの失敗を表示する
ログインページへリダイレクトされ、SSO でログインできません。15.10 では探した
コンポーネント名と提供元のプラグイン名を含む警告が ``fess.log`` に記録されます。
15.8 まではどのログレベルでも何も出力されませんでした。

``oic`` プラグインは、15.8 の認証機能より検証が厳しくなっています。 ``oic.token.server.url`` は HTTPS
である必要があり（ ``http`` が使えるのは ``localhost`` 、 ``127.x.x.x`` 、 ``::1`` のみです）、ID Token の ``aud`` と
``exp`` を検証します。新しいキー ``oic.issuer`` を設定した場合は ``iss`` も検証します。詳しくは
:doc:`../config/sso-oidc` を参照してください。

15.8 では ``oic.token.server.url`` に ``http`` のURLを指定でき、ホスト名の制限もありませんでした。15.10 では、Docker Composeのサービス名（``http://keycloak:8080/...`` など）や社内のホスト名への ``http`` は、同じマシンを指していても拒否されます。拒否されるとログインに失敗し、 ``fess.log`` に ``Failed to process the OpenID Connect callback: oic.token.server.url must be https`` で始まる警告が出力されます。更新する前に、トークンエンドポイントを HTTPS のURLに変更してください。

あわせて ``oic.issuer`` に、OPのDiscoveryドキュメントの ``issuer`` の値を設定することをお勧めします。設定しない場合、 ``iss`` は検証されず、起動後の最初のログインで警告が出力されます。 ``oic.issuer`` を設定しても HTTPS の規則は緩和されません。

15.10 では ID Token の ``nonce`` も検証します。認可リクエストごとに ``nonce`` を送信し、ID Token に同じ値の ``nonce`` クレームがない場合は、ログインを拒否します。OpenID Connect Core はOPに ``nonce`` をそのまま返すことを求めていますが、返さないOPではログインできなくなり、この検証を無効にする設定はありません。更新する前に、使用中のOPが ``nonce`` クレームを返すことを確認してください。また、プラグインの更新前に開始したログインは1回失敗するため、ログインをやり直してください。

SSO を使用していない場合、つまり ``sso.type`` が ``none`` または未設定の場合、
対応は不要です。

.. _upgrade-159-script-engine:

標準のスクリプトエンジンが Groovy から JavaScript に変更
--------------------------------------------------------

15.8 までは標準のスクリプトエンジンが Groovy で、 ``job.default.script`` の既定値も ``groovy``
でした。15.10 では標準のエンジンが JavaScript になり、既定値は ``javascript`` です。Groovy は
標準では組み込まれなくなり、 ``fess-script-groovy`` プラグインで提供されます。 ``scriptType``
に ``groovy`` を指定するには、このプラグインをインストールしておく必要があります。

アップグレードでは、各設定に保存されたスクリプトエンジンは変更されません。また、15.10 より前に
保存され、エンジンを記録していない設定は ``groovy`` として扱われます。プラグインがない場合、
次の設定が動作しなくなります。

- ``groovy`` として保存されたスケジュールジョブ。
  **15.8 が自動で登録したジョブもこれに該当します。**\ Default Crawler、Suggest Indexer、
  Config Reloader、Log Aggregator、Doc Purger などの同梱ジョブはすべて ``groovy`` として保存されて
  おり、15.10 は起動時にまだ存在しない同梱ジョブだけを追加するため、これらは書き換えられません。
  各ジョブはスケジュールで起動されるたびに失敗し、Default Crawler によるクロールも行われなく
  なります。同梱ジョブの多くは「ロギング」が無効なため、失敗はジョブログには残らず、
  ``fess.log`` に ``Failed to execute job`` の警告として出力されるだけです。
- 「設定パラメーター」にフィールドスクリプト（ ``field.script.<フィールド名>`` ）を書いた Web
  クロール設定とファイルクロール設定。その設定のドキュメントはすべて ``ScriptEngineException``
  で失敗して障害 URL に記録されますが、クロールジョブ自体は正常に終了します。
- 「スクリプト」を設定したデータストア設定。パラメーター名そのもの以外の値は評価できません。
  :doc:`../config/datastore/ds-overview` を参照してください。
- ドキュメントブーストのルール。そのルールは何もブーストしません。
- 「置換」が ``groovy:`` で始まるパスマッピング。そのマッピングは適用されず、URL は変更されません。

最初の起動後、 ``fess.log`` で
``Settings use the script engine groovy, which is not registered`` で始まる警告を確認して
ください。\ |Fess| は起動時に上記の設定を一度確認し、どのプラグインも提供していないエンジンを
使う設定の数を種類ごとに出力します。15.8 から引き継いだ ``fess_config.properties`` に
``job.default.script=groovy`` が残っている場合はそれも示され、この場合はアップグレード後に作成した
ジョブも Groovy を使います（ :ref:`upgrade-159-carried-over-config` を参照）。次のいずれかで
対応してください。

- プラグインをインストールして |Fess| を再起動します。保存済みの Groovy スクリプトはそのまま
  動作し、警告も出力されなくなります。プラグインは管理画面「システム」→「プラグイン」からも
  インストールできます。

  ::

      $ bin/fess-setup install plugin fess-script-groovy

- 各設定を JavaScript に移行します。Groovy だけが受け付ける構文を先に書き換えてから、
  JavaScript を選択します。

  - スケジュールジョブ: 管理画面「システム」→「スケジューラ」で「実行方法」を ``javascript``
    にします。同梱ジョブのスクリプトは、次の 2 つを除いてそのまま JavaScript として有効です。
    Thumbnail Purger は Groovy の ``long`` リテラル ``1000L`` を使っており、JavaScript では
    構文エラーになります（ ``1000`` と書きます）。Index Exporter には
    :ref:`upgrade-159-index-exporter` の変更が必要です。JavaScript では配列リテラルが Java の
    ``String[]`` へ自動的に変換されるため、Groovy 形式の ``as String[]`` は不要です。

    ::

        return container.getComponent("crawlJob").logLevel("info").webConfigIds(["1", "2"]).fileConfigIds(["1"]).dataConfigIds([]).execute(executor);

  - Web クロール設定とファイルクロール設定: 「設定パラメーター」に
    ``config.script.type=javascript`` を追加します。
  - データストア設定: 「パラメーター」に ``script_type=javascript`` を追加します。
  - ドキュメントブーストのルール: 「スクリプト種別」を ``javascript`` にします。
  - パスマッピング: 「置換」の先頭を ``groovy:`` から ``javascript:`` に変えます。
  - ``job.default.script``: 15.8 から引き継いだ ``fess_config.properties`` で ``javascript``
    に設定します。

``crawler.default.script`` の削除
---------------------------------

``crawler.default.script`` は ``fess_config.properties`` から削除されました。設定に残していても
効果はないため、削除してください。

クロールプロトコル ``storage`` の削除
-------------------------------------

``crawler.file.protocols`` で ``storage`` は指定できなくなりました。同梱の値は
``file,smb,smb1,ftp`` です。代わりに ``s3`` を使用し、 ``storage:`` で始まるパスを
指定しているファイルクロール設定は ``s3:`` のパスへ変更してください。 ``s3`` には
``fess-storage-s3`` プラグインが必要です。

.. _upgrade-159-index-exporter:

Index Exporter ジョブが削除されたパッケージを参照
-------------------------------------------------

15.10 には ``org.opensearch`` のクラスが含まれなくなり、ジョブのスクリプトで使用するクエリビルダーは
``org.codelibs.fesen.opensearch`` の下に移りました。15.8 が Index Exporter ジョブに保存した
スクリプトは ``org.opensearch.index.query.QueryBuilders`` を参照しており、アップグレードでも
置き換えられないため、 ``fess-script-groovy`` をインストールしてもこのジョブは失敗します。
このジョブは無効かつスケジュールなしの状態で同梱されているため、影響があるのは実行している
場合だけです。管理画面「システム」→「スケジューラ」でジョブを開き、スクリプトのパッケージを
15.10 のものに変更してください。

::

    return new org.codelibs.fess.job.IndexExportJob().query(org.codelibs.fesen.opensearch.index.query.QueryBuilders.matchAllQuery()).execute()

独自に作成したスクリプトで ``org.opensearch.index.query`` を参照している場合も、同じように
変更してください。クエリの例は :doc:`../config/admin-index-export` を参照してください。

.. _upgrade-159-carried-over-config:

15.8 から引き継いだ設定ファイル
-------------------------------

ステップ 3 の ZIP 版の手順では、旧バージョンの ``fess_config.properties`` と ``bin/fess.in.sh``
をコピーします。RPM 版のアップグレードでは、変更を加えた ``/etc/fess/fess_config.properties``
がそのまま残ります（15.10 のファイルは ``fess_config.properties.rpmnew`` として併置されます）。
DEB 版でも、確認で自分のファイルを残した場合は同様です（15.10 のファイルは
``fess_config.properties.dpkg-dist`` として併置されます）。
いずれの場合も 15.10 は 15.8 の値のまま動作し、15.10 で同梱の値が変わったキーも例外ではありません。
少なくとも次のキーを確認してください。

.. list-table::
   :header-rows: 1

   * - キー
     - 15.8.0
     - 15.10
     - 15.8 の値が残った場合の影響
   * - ``job.default.script``
     - ``groovy``
     - ``javascript``
     - 管理画面「システム」→「スケジューラ」で作成するジョブの既定が ``groovy`` になり、
       ``fess-script-groovy`` プラグインがないと失敗します。
   * - ``job.template.script``
     - ``as String[]`` を含む Groovy 形式
     - JavaScript 形式
     - クロール設定から作成したジョブのスクリプトが Groovy 形式になります。
   * - ``crawler.file.protocols``
     - ``file,smb,smb1,ftp,storage,s3,gcs``
     - ``file,smb,smb1,ftp``
     - ``s3:`` や ``gcs:`` で始まるパスがプラグインなしでも受け付けられ、クロール時に警告を
       出して処理されません。 ``storage`` はサポートされなくなりました。
   * - ``search_engine.http.url``
     - ``http://localhost:9201``
     - ``http://localhost:9200``
     - ``SEARCH_ENGINE_HTTP_URL`` が設定されていない場合に使われます。15.8 からコピーした
       ``bin/fess.in.sh`` で設定していなかった場合がこれに当たり、\ |Fess| は 15.10 で廃止された
       組み込み OpenSearch のポートである 9201 で OpenSearch を探します。
   * - ``jvm.crawler.options``\ 、\ ``jvm.thumbnail.options``
     - ``-Djcifs.smb.client.*``\ 、\ ``-Djcifs.smb1.smb.client.*``
     - ``-Djcifs.client.*``
     - SMB のタイムアウトが jcifs の既定値のままになります。 :ref:`upgrade-159-jcifs` を
       参照してください。
   * - ``response.headers``
     - ``text/html=Content-Security-Policy: reflected-xss block`` の行を含む
     - その行なし
     - ログイン画面や管理画面など、\ |Fess| 自身が描画するページのレスポンスに、ブラウザーが認識しない
       ``Content-Security-Policy: reflected-xss block`` ヘッダーが付き、ブラウザーのコンソールに
       ``Unrecognized Content-Security-Policy directive 'reflected-xss'`` が出ます。このヘッダーは
       何も制限しません。次の段落のとおり、その行を削除してください。
   * - ``app.encrypt.property.pattern``
     - ``.*password|.*key|.*token|.*secret``
     - ``.*password|.*passphrase|.*key|.*token|.*secret``
     - 名前が ``passphrase`` で終わるパラメーター（たとえばデータストア設定の ``ssh.passphrase``）が
       平文で保存されます。すでに保存されている値は、15.10 のパターンで設定を保存し直すまで平文のままです。
   * - ``index.backup.log.targets``
     - ``click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
     - 「システム情報」→「バックアップ」ページに ``chat_log.ndjson`` が表示されません。
   * - ``index.export.exclude.fields``
     - ``cache``
     - ``cache,tag``
     - ユーザータグを保持する ``tag`` フィールドが、Index Export ジョブが書き出すファイルから
       除外されなくなります。
   * - ``crawler.default.script``\ 、\ ``theme.allowed.archive.extensions``\ 、
       ``theme.assets.cache.max.age``\ 、\ ``theme.assets.precompressed``\ 、
       ``rag.chat.message.max.length``\ 、\ ``supported.uploaded.js.extentions``\ 、
       ``supported.uploaded.css.extentions``\ 、\ ``supported.uploaded.media.extentions``\ 、
       ``supported.uploaded.files``\ 、\ ``online.help.name.design``
     - あり
     - 削除
     - 効果はありません。削除してください。

``response.headers`` の同梱の値には、15.0 から 15.8 まで ``text/html=Content-Security-Policy: reflected-xss block``
の行があります。 ``reflected-xss`` は Content-Security-Policy の初期の草案にあったディレクティブで、現在の
ブラウザーは認識しないため、このヘッダーは何も制限せず、コンソールにエラーを出すだけです。15.10 は同梱の値から
この行を削除しました。 ``X-XSS-Protection`` と ``X-Frame-Options`` の行は変わりません。15.8 から引き継いだ
``response.headers`` にはこの行が残るため、 ``fess_config.properties`` の ``response.headers`` から、次の行だけを
削除してください。各行の末尾の ``\n\`` は値が次の行に続くことを表すため、行ごと削除すれば、ほかの行はそのまま
使えます::

    text/html=Content-Security-Policy: reflected-xss block\n\

``response.headers`` を ``-Dfess.config.response.headers`` で指定している場合は、その値から同じ項目を削除してください。

15.8 からコピーした ``bin/fess.in.sh`` には、15.10 のファイルにある次の 2 点もありません。
15.10 は ``SEARCH_ENGINE_HTTP_URL`` に ``http://localhost:9200`` を設定しますが、15.8 のファイルは
自分で設定しない限り未設定のままです。また、 ``bin/fess-setup install nodejs`` で導入した
Node.js を検出しないため、 ``PLAYWRIGHT_NODEJS_PATH`` を自分で設定しない限り、Playwright
系のプラグインは Node.js を見つけられません。

どちらのファイルも丸ごとコピーするのではなく、15.10 に同梱のファイルを元にして、変更した値を
再適用してください。変更した値は ``diff`` で確認できます::

    $ diff /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.10.0/app/WEB-INF/classes/fess_config.properties
    $ diff /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.10.0/bin/fess.in.sh

RPM 版では、同じように ``/etc/fess/fess_config.properties`` と
``/etc/fess/fess_config.properties.rpmnew`` を、DEB 版では
``/etc/fess/fess_config.properties.dpkg-dist`` を比較してください。DEB 版のアップグレードでは、
編集していない ``fess_config.properties`` は 15.10 のファイルに置き換えられるため（ステップ 3 を参照）、
15.10 の値から始まります。

``app.cipher.key`` は、15.10 で変わっていなくても必ず引き継ぐ必要がある値です。Web 認証、クロール設定、
データストア設定のパラメーターに保存されたパスワードやシークレットを暗号化する鍵だからです。新しい
環境が、それらを保存したときとは別の鍵で動作していると（同梱の ``fess_config.properties`` を使った場合や、
バックアップを新しいサーバーへ復元した場合など）復号できず、 ``fess-crawler.log`` に
``CipherFailureException`` が記録され、そのような設定を含むクロールは何も索引できないことがあります。

.. note::

   15.9 の |Fess| は、Web 認証とファイル認証の ``password`` も ``app.cipher.key`` で暗号化して保存するため、
   バックアップの ``fess_basic_config.bulk`` と ``fess_config.bulk`` には暗号化された値が含まれます。
   別のインストールに復元するときは同じ ``app.cipher.key`` を引き継いでください。鍵が異なると、これらの認証情報を使う
   クロールはエラーで失敗します。15.9 より前のバックアップには平文で含まれており、そのまま使えます
   （詳細は :doc:`../admin/backup-guide` を参照）。

.. _upgrade-159-jcifs:

SMB のタイムアウトは jcifs 3 のプロパティ名を使用
-------------------------------------------------

SMB ファイルサーバーのクロールに |Fess| が使用する jcifs は、バージョン 3 でプロパティ名を
変更しました。 ``jcifs.smb.client.*`` は ``jcifs.client.*`` になり、SMB1 用の
``jcifs.smb1.smb.client.*`` も同じプロパティに統合されました。15.8 までの ``jvm.crawler.options``
と ``jvm.thumbnail.options`` は旧名を渡しており、jcifs はそれを読まないため、SMB のクロールは
jcifs の既定値で動作していました。15.10 は新しい名前を渡します。

::

    -Djcifs.client.responseTimeout=30000
    -Djcifs.client.soTimeout=35000
    -Djcifs.client.connTimeout=60000
    -Djcifs.client.sessionTimeout=60000

そのため、接続タイムアウトとセッションタイムアウトが初めて有効になり、jcifs の既定値の 35 秒から
60 秒に延びます。応答しない SMB サーバーに対して、クロールは最大 60 秒待つようになります。
応答タイムアウトとソケットタイムアウトは jcifs の既定値と同じ値のため、変わりません。

これらのタイムアウトを変更していた場合は、両方のオプションで名前を変更してください。旧名のままでは
15.8 でも効果はありませんでした。15.8 から引き継いだ ``fess_config.properties`` には旧名が残り、
jcifs の既定値のままになります。

効果のなかった 4 つのプロパティの削除
-------------------------------------

次のキーは ``fess_config.properties`` から削除されました。\ |Fess| はこれらをこのファイルから
読み込んでいなかったため、これまでと同様、この名前で残した値に効果はありません。

- ``theme.allowed.archive.extensions``
- ``theme.assets.cache.max.age``
- ``theme.assets.precompressed``
- ``rag.chat.message.max.length``

``rag.chat.message.max.length`` による上限は引き続き有効ですが、システムプロパティとして
読み込まれます。 :doc:`../config/rag-chat` のとおり、 ``app/WEB-INF/conf/system.properties``
または ``-Dfess.system.rag.chat.message.max.length`` で設定してください。

.. _upgrade-159-static-theme:

検索画面はテーマに
----------------------

別のテーマを選んでいない限り、検索画面は |Fess| に同梱のテーマ ``bootstrap`` で表示されます。
対象は ``/`` 、 ``/search`` 、 ``/advance`` 、 ``/help`` 、 ``/profile`` 、 ``/cache`` 、 ``/chat`` と
エラーページです。15.8 までは、既定のテーマを設定していなければ、これらのページは JSP でした。

この切り替えはアップグレードでも起こります。既定のテーマを設定したことのない 15.8 の環境では
``system.properties`` に ``theme.default`` が無いため、アップグレード後はテーマで表示されます。
設定ファイルには何も書き込まれず、ログにも何も出ません。JSP の検索画面に戻す設定はありません。
15.8 で既定のテーマを設定していた場合、その設定は引き継がれます。そのテーマは 15.10 向けのビルドを
インストールしてください（ ``bin/fess-setup install theme <name>`` ）。インストールされていないテーマを
既定に指定していると、 ``fess.log`` に警告を出して ``bootstrap`` で表示します。

管理画面の「ページのデザイン」や JAR テーマプラグインで検索画面の JSP、CSS、画像を変更していた場合、
その変更は表示されなくなります。変更はテーマで行ってください。同梱のテーマを複製して変更するか
（ :ref:`theme-customize-bundled` を参照）、公開されているテーマを管理画面の「システム」>「テーマ」または
``bin/fess-setup install theme <name>`` でインストールします。仮想ホストごとの見た目は、仮想ホスト名と
同じ名前のテーマで変えます（ :doc:`../config/security-virtual-host` を参照）。

次の 2 つも無くなりました。

- 仮想ホストごとのログイン画面。15.8 までは「システム」>「全般」を保存すると、ログイン画面を含む
  JSP が ``WEB-INF/view/<仮想ホスト名>/`` にコピーされ、仮想ホストごとに編集できました。15.10 は
  このコピーを作りません。ログイン画面（ ``/login/`` ）は引き続き JSP ですが、すべての仮想ホストで
  共通の ``WEB-INF/view/admin/login/`` のものが表示されます。以前にコピーされた JSP は使われません。
- JAR テーマプラグイン（ ``fess-theme-*`` ）。インストールしても種類 ``jar`` の汎用 JAR として
  置かれるだけで、画面は変わりません。残っている JAR は「システム」>「プラグイン」ページ、または
  ``bin/fess-setup remove plugin <name>`` で削除できます（ :doc:`../dev/theme-development` を参照）。

15.8 で JSP の検索結果に独自のフィールドを表示していた場合は、 ``query.additional.response.fields``
に加えて ``query.additional.api.response.fields`` にも同じフィールドを追加してください。テーマは
検索結果を ``/api/v2/search`` から取得します。 ``query.additional.response.fields`` は検索エンジンから
取得するフィールドを追加するだけで、この API が応答に含めるのは ``query.additional.api.response.fields``
に列挙されたフィールドだけです（ :doc:`../config/search-advanced` を参照）。そのフィールドを表示するように
テーマも変更してください。

クライアントから見た変化
~~~~~~~~~~~~~~~~~~~~~~~~

エラーは、要求された URL のまま、実際の HTTP ステータスで返るようになりました。ブラウザ
（ ``Accept`` ヘッダーに ``text/html`` を含むリクエスト）にはテーマのエラーページを、それ以外の
クライアントには ``Not Found.`` のような 1 行の ``text/plain`` を返します。15.8 までは、ほとんどの
エラーが ``/error/...`` のページへの ``302`` リダイレクトになり、そのページが ``200`` を返していました。
監視、ヘルスチェック、 ``Location`` ヘッダーをたどるクライアントや ``/error/`` の URL を前提とする
クライアントを見直してください。

.. list-table::
   :header-rows: 1

   * - リクエスト
     - 15.8 まで
     - 15.10
   * - パラメーターが欠けた、または存在しない文書に対する ``/go/``
     - ``200`` 、または ``/error/`` への ``302``
     - ``400`` または ``404``
   * - パラメーターが欠けた、未知の文書に対する、またはサムネイルの無い ``/thumbnail/``
     - ``200`` または ``302``
     - ``400`` または ``404``
   * - 設定した SSO の種類が扱わない ``/sso/metadata`` と ``/sso/logout``
     - ``/error/badrequest/`` への ``302``
     - ``400``
   * - ``/api/v1/*`` 、 ``/json`` 、および存在しない URL
     - ``/error/notfound/`` への ``302``
     - ``404``
   * - 捕捉されない例外（管理 API を含む）
     - ``/error/systemerror/`` への ``302``
     - ``500`` 。本文は ``System Error.`` （JSON ではありません）
   * - ``/error/notfound/`` 、 ``/error/badrequest/`` 、 ``/error/systemerror/`` そのもの
     - ``200``
     - ``404`` 、 ``400`` 、 ``500``

``login.required=true`` のとき、検索系のページは未ログインのユーザーをリダイレクトしなくなりました。
ページはテーマとともに ``200`` を返してログインを求め、その裏のデータの方を拒否します。 ``/health`` 、
``/auth/*`` 、 ``/ui/config`` 以外の ``/api/v2/`` のエンドポイントは、 ``/api/v2/search`` を含め、ログインするまで
``401`` を返します。 ``/go/`` 、 ``/thumbnail/`` 、 ``/osdd`` は従来どおりログインへ
リダイレクトします。未ログインで ``/`` にアクセスしたときのリダイレクトを確認している監視は、
``/api/v2/search`` が ``401`` を返すことを確認するように変えてください。

検索画面は ``/api/v2/search`` を使って検索するため、検索ログは ``/search`` へのリクエストではなく
この API の呼び出しで記録されます。JavaScript を実行しないクライアントには、検索結果の無いページが
返ります。

検索画面の HTML には ``X-Frame-Options: DENY`` と、 ``frame-ancestors 'none'`` を含む
``Content-Security-Policy`` が付き、他のページのフレームには表示されません。15.8 の JSP の検索画面は
``response.headers`` の既定値により ``X-Frame-Options: SAMEORIGIN`` で、同じオリジンのページの ``iframe`` に\
表示できました。検索画面を同じオリジンの ``iframe`` に埋め込んでいる場合は、 ``fess_config.properties`` の
``theme.index.frame.ancestors`` （既定値 ``'none'`` ）に ``'self'`` を設定してください。別のオリジンから\
埋め込むときは、そのオリジンを指定します（ :doc:`../dev/theme-development` を参照）。

管理画面の「ページのデザイン」を削除
------------------------------------

管理画面の [システム > ページのデザイン] を削除しました。検索画面の JSP、CSS、画像を管理画面から
編集することはできません。検索画面の見た目はテーマで変更してください（ :ref:`theme-customize-bundled`
を参照）。

次のキーも ``fess_config.properties`` から削除しました。この名前で残した値は使われません。

- ``supported.uploaded.js.extentions``
- ``supported.uploaded.css.extentions``
- ``supported.uploaded.media.extentions``
- ``supported.uploaded.files``
- ``online.help.name.design``

``admin-design`` と ``admin-design-view`` のロールは、何の権限も与えなくなりました。これらのロールだけを
持つユーザーは、ログインすると管理画面ではなく検索画面に移動します。

``api.access.token.required`` の削除
------------------------------------

``api.access.token.required`` は ``fess_config.properties`` から削除されました。15.8 から引き継いだ
``fess_config.properties`` に残っている場合も含め、この名前の値は効果がありません。 ``true`` にすると、
ログインしていないユーザーからの API リクエストをすべて拒否していました。検索画面は
``/api/v2/search`` を使って検索するようになったため、この設定では匿名ユーザーに結果のない検索画面が
表示されることにもなります。

``true`` に設定していた環境では、匿名ユーザーからの API リクエストにも、検索画面と同じくゲストのロールで
応答するようになります。匿名ユーザーに検索させない場合は ``login.required=true`` を設定してください。
アクセストークンの動作は変わりません。登録済みのアクセストークンを付けたリクエストにはそのトークンの
権限が与えられ、未登録または期限切れのトークンを付けたリクエストは拒否されます。

.. _upgrade-159-api-requests:

API が拒否するようになったリクエスト
------------------------------------

15.8 では受け付けられていた次のリクエストを、15.10 は拒否します。15.8 向けに作ったクライアントやスクリプトが\
送っていないか確認してください。管理 API の拒否は HTTP ``400`` で、本文の ``status`` は ``1`` です。

.. list-table::
   :header-rows: 1

   * - リクエスト
     - 15.8
     - 15.10
   * - ``/api/v2/search`` に ``facet.field`` または ``facet.query`` と一緒に、 ``0`` 以下の ``facet.size`` 、\
       または整数でない ``facet.size`` ・ ``facet.minDocCount`` を指定する
     - ``200`` 。ただし ``record_count`` が ``0`` で ``partial`` が ``true`` の空の結果
     - ``400`` （ ``invalid_request`` ）。 ``facet.size`` は ``1`` 以上です
   * - ``track_total_hits=false`` を指定する。 ``query.track.total.hits`` を ``false`` にしている場合は\
       すべての検索が対象です
     - ``200`` 。ただし検索結果が 0 件
     - 検索が拒否されます（ ``/api/v2/search`` は ``400`` で ``invalid_request`` ）。 ``true`` と正の整数は\
       従来どおりです
   * - 管理 API の辞書（ ``mapping`` ・ ``kuromoji`` ）に、既にある項目と重複する項目を登録・更新する
     - 保存されます。辞書を読み込むときに失敗し、検索できなくなる原因になります
     - ``400``
   * - 管理 API の ``kuromoji`` 辞書に、 ``token`` が空白を含む項目や、 ``segmentation`` と ``reading`` で\
       空白区切りの語の数が異なる項目を登録・更新する
     - 保存されます。上と同じく、辞書を読み込むときに失敗します
     - ``400``
   * - ``DELETE /api/admin/searchlist/doc/{doc_id}`` で、何も削除されなかった場合（存在しない ``doc_id`` 、\
       または文書一覧が返す ``_id`` のように ``doc_id`` でない値）
     - ``200`` （ ``status`` は ``0`` ）。文書は削除されません
     - ``400``
   * - 管理 API のユーザーの ``roles`` ・ ``groups`` に、ロール名・グループ名を指定する
     - 保存されますが、指定した名前はロールとして働きません。名前によっては、そのユーザーの読み込みに失敗します
     - ``400`` 。ロール・グループの ID（ ``GET /api/admin/role/settings`` ・ ``GET /api/admin/group/settings`` の
       ``id`` ）を指定します
   * - 管理 API のユーザーに、パスワードポリシー（ ``password.min.length`` の既定値 ``8`` など）に反する\
       パスワードを設定する。作成時にパスワードを省略する。 ``confirm_password`` を送り、 ``password`` と\
       一致しない
     - 保存され、そのパスワードでログインできます
     - ``400``
   * - ``GET /api/admin/log/file/{id}`` で、ログファイルとして許可されない名前（ ``.log`` ・ ``.log.gz`` で終わらない名前など）や、ログのディレクトリにないファイルを指定する
     - 許可されない名前は ``200`` で空のレスポンス
     - ``400``
   * - 管理 API の ``mapping`` 辞書に、 ``output`` を省略した項目を登録・更新する
     - ``200`` （ ``id`` は ``0`` ）。何も保存されません
     - ``400``
   * - ストレージにアクセスできないときの ``GET /api/admin/storage/list`` （ストレージクライアントのプラグインが導入されていない場合を含む）
     - ``200`` （ ``status`` は ``0`` ）。空の一覧
     - ``400`` 。 ``message`` に原因が入り、プラグインがない場合は導入するプラグインが示されます
   * - ログインフォーム（ ``POST /login/login`` ）で、同じ IP アドレスから、または同じ IP アドレスから同じユーザーに対して、ログインを短時間に繰り返し失敗する
     - 制限なし
     - IP 単位または IP とユーザーの組ごとの上限（ ``theme.api.login.rate.limit.per.ip.per.minute`` ・ ``theme.api.login.rate.limit.per.user.per.minute`` ）を超えると、その IP アドレス（ユーザー単位の上限の場合は、その IP アドレスからのそのユーザー）からのログインは、正しい資格情報でも ``theme.api.login.lockout.seconds`` 秒間拒否されます。応答は資格情報が誤っているときと同じログインエラーです。上限とロックアウトは ``/api/v2/auth/login`` と共有されます（ :doc:`../api/api-auth` を参照）リバースプロキシの背後で、そのアドレスが ``rate.limit.trusted.proxies`` に含まれていない場合、すべてのクライアントが 1 つのアドレスとして数えられ、失敗が続くと全ユーザーがログインできなくなります。プロキシのアドレスを ``rate.limit.trusted.proxies`` に追加してください（ ``X-Forwarded-For`` が信頼されないピアから届くと、 ``fess.log`` に警告が一度出力されます）。

``/api/v2/documents/all`` の各行から ``score`` がなくなりました。15.8 では各文書に検索スコアが付いていましたが、
15.10 は全件の取得を point in time と ``search_after`` で行うため、スコアは付きません。旧 API プラグインの
``/json?type=scroll`` ・ ``/api/v1/documents/all`` も同じです。 ``score`` を読むスクリプトは、値がない場合を\
扱えるようにしてください。

管理 API のファイルのアップロード（辞書 6 種類、 ``badword`` 、 ``elevateword`` 、 ``storage`` ）は、 ``POST`` で\
受け付けます。15.8 の文書は ``PUT`` を案内していましたが、 ``multipart/form-data`` の ``PUT`` ではファイルが\
届かず、15.8 でも 15.10 でも「ファイルが必要です」という検証エラーになります。 ``PUT`` のエンドポイントは\
残っていますが、アップロードには ``POST`` を使ってください。

次の変更は、リクエストの拒否ではありませんが、API や管理画面を使うスクリプトやクライアントに影響する場合があります。

- 管理 API の ``webauth`` ・ ``fileauth`` の取得（ ``/api/admin/webauth/settings`` ・ ``/api/admin/webauth/setting/{id}`` と、 ``fileauth`` の同じエンドポイント）は、保存されているパスワードを返さなくなりました。 ``PUT`` でパスワードを省略するか空にすると、保存されているパスワードが残ります。空でないパスワードを送ると置き換えられます。
- ログインしているユーザーは、リクエストに含まれる ``userCode`` パラメーターや Cookie ではなく、セッションで識別されます（お気に入りの API など）。匿名のユーザーは従来どおりパラメーターと Cookie を使います。
- 管理画面の「検索リスト」と「クロール情報」の「すべて削除」には、編集ロール（ ``admin-searchlist`` ・ ``admin-crawlinginfo`` ）が必要です。表示ロール（ ``-view`` が付くロール）だけを持つユーザーのリクエストは拒否されます。
- ``fess.xml`` の ``roleQueryHelper`` で ``parameterKey`` ・ ``headerKey`` ・ ``cookieKey`` を有効にしたのに ``cipher`` を設定せず、値の暗号化のフラグ（ ``encryptedParameterValue`` ・ ``encryptedHeaderValue`` ・ ``encryptedCookieValue`` ）が既定値の ``true`` のままの場合、15.8 は値を暗号化されていないロール情報として読んでいました。15.10 はその値を無視し、警告を一度ログに出力します。暗号化した値を使うなら ``cipher`` を設定し、暗号化していない値を受け取る意図なら、フラグを ``false`` にしてください。
- Content-Type に、JVM が認識しない文字コード（ ``charset=nope`` など）を指定したリクエストは、文字コードの指定がないものとして処理されます。以前は ``/api/v2/search`` が ``500`` （ ``internal_error`` ）を返していました。
- ``kuromoji`` ・ ``mapping`` ・ ``stemmeroverride`` ・ ``synonym`` の辞書をアップロード・ダウンロードする管理 API が失敗したときのメッセージは、その辞書の種類を示すようになりました。15.8 では、どの辞書でも「protwords ファイル」と表示されていました。

``search_engine.type`` の ``cloud`` は非推奨
--------------------------------------------

15.9 では、CodeLibs のプラグインを含まない素の OpenSearch 用に、 ``search_engine.type`` の値として ``vanilla`` が追加されました（ :doc:`../config/search-engine-type` を参照）。 ``cloud`` は ``vanilla`` の非推奨の別名になりました。引き続き動作しますが、起動時に警告をログに出力します。15.10 で運用するようになったら、 ``vanilla`` に変更してください。 ``aws`` はこれまでどおり動作します。

* ``vanilla`` は 15.9 以降で使えます。15.8 以前の |Fess| はこの値を認識しません。15.8 に戻す可能性がある間は ``cloud`` のままにしてください。
* ``aws`` と ``cloud`` のインデックス定義は ``fess_indices/_vanilla/`` から読み込まれます。同梱されていた ``fess_indices/_aws/`` と ``fess_indices/_cloud/`` はなくなりました。独自に追加した ``fess_indices/_aws/`` または ``fess_indices/_cloud/`` は読み込まれなくなるため、変更内容を ``fess_indices/_vanilla/`` に移してください。作成済みのインデックスは変更されません。
* 15.8 が検索エンジンに保存したサジェストの設定は、自動的に移行されます。対応は不要です。

CSV データストアが引用符で囲まれたフィールドを解釈
--------------------------------------------------

15.10 の ``fess-ds-csv`` プラグインは、既定で引用符を解釈します。 ``"山田, 太郎"`` のようなフィールドは
1 つの列になります。15.8.0 のプラグインはカンマの位置で分割していました。
``bin/fess-setup upgrade plugins`` の実行後は、引用符で囲まれたフィールドを含む CSV ファイルを読む
データストア設定を確認してください。15.8 の動作を維持するには、「パラメーター」に
``quote_disabled=true`` を追加します。対応する引用符がない場合の動作も含め、
:doc:`../config/datastore/ds-csv` を参照してください。

.. _upgrade-reindex-new-fields:

既存の文書インデックスへの新しいフィールドとかなの正規化の反映
--------------------------------------------------------------

15.10 は起動時に、設定・ログ・ユーザーのインデックスへ新しいフィールドを追加します。文書の
インデックスに追加するのは、ユーザータグを保持する ``tag`` フィールド（ ``keyword`` ）だけで、
マッピングのそれ以外の部分と解析の設定は変更しません。15.8 以前で作成した文書インデックスを
そのまま使うと、次の 15.10 の変更が効きません。

- **ファイルの所有者と最終更新者**\ （\ ``owner``\ ・\ ``last_modifier``\ ）: ファイルシステム・SMB・FTP の
  クロールで新たに索引されるフィールドです。既存の文書インデックスには定義がないため、最初に
  クロールした値から ``text`` 型として自動でマッピングされ、\ ``owner:alice`` のような検索や
  ``facet.field=owner`` が期待どおりに動きません。
- **ETag**\ （\ ``etag``\ ）: クロールしたページの ETag を保存するフィールドです。15.10 はこれを
  ``If-None-Match`` として送り返し、変更のないページを再取得しません。既存の文書インデックスにはこれも
  定義がないため、同梱の「索引されない ``keyword``」ではなく ``text`` 型として自動でマッピングされます。
  このマッピングでも条件付きリクエストは動作します。
- **かなの表記ゆれと、長音符の代わりに書かれたダッシュの正規化**\ （例: ``サ―バ－`` を ``サーバー`` と
  同じ語として扱う）: 規則は文書インデックスの解析の設定と辞書 ``mapping.txt`` にあるため、
  既存のインデックスには反映されません。

両方を反映するには、管理画面の「システム情報」→「メンテナンス」で「エイリアスの更新」と
「辞書の初期化」を有効にして「再インデクシング」を実行します。再インデクシングは既存の文書を
新しいインデックスへコピーするため、クロールし直す必要はありません。

.. warning::

   「辞書の初期化」は、同梱の辞書ファイルで OpenSearch 側の辞書を上書きします。管理画面の「辞書」で
   同義語などを編集している場合は、事前にダウンロードしておき、再インデクシングの後に反映し直して
   ください。ダウンロードしたファイルから重複または不正なエントリーを削除し（ステップ 7 を参照）、
   アップロードしたうえで、「システム情報」→「メンテナンス」の「ドキュメントインデックスのリロード」で
   [リロード] をクリックしてください。リロードするまで、文書インデックスのアナライザーは同梱の辞書を
   使い続けるため、復元した同義語は、どれだけ待っても一致しません。インデックス時に効く辞書は、さらに
   文書の再クロールが必要です。 :ref:`dict-apply-changes` を参照してください。

.. note::

   15.8 以前に索引したファイルには、所有者と最終更新者の値がありません。差分クロールでは変更のない
   ファイルは取得し直されないため、値を付けるには「システム」→「全般」の「最終更新日時の確認」を
   一時的に無効にしてクロールしてください。


機能別の移行作業
================

15.7 以前から 15.10 へアップグレードする場合、利用している機能に応じて以下の作業が必要です。

セマンティック検索を利用していた場合
------------------------------------

15.7 以前でセマンティック検索を提供していた ``fess-webapp-semantic-search`` プラグインは、
15.8 でコアに統合されたため不要になりました（非推奨）。プラグインの削除、\ ``-Dfess.semantic_search.*``
および ``-Drank.fusion.searchers=default,semantic`` の削除、旧 ingest pipeline のデタッチが
必要です。手順は :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）を
参照してください。

AI 検索モード（RAG チャット）を利用していた場合
-----------------------------------------------

15.6 から、AI 検索モード（RAG チャット）の機能は ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、
``fess-llm-gemini`` などのプラグインとして分離されました。利用しているプロバイダーに対応する
プラグインを管理画面「システム」→「プラグイン」からインストールしてください。
また、15.9 では Amazon Bedrock 用の ``fess-llm-bedrock`` が追加されています。

SPNEGO（Windows 統合認証）を利用していた場合
--------------------------------------------

15.8 から、クライアントのプリンシパルの Kerberos レルムがサーバーのレルムと異なる場合、
SPNEGO ログインは拒否されます。AD のドメインツリーの子ドメインや信頼関係を結んだフォレストの
ユーザーがログインする構成では、管理画面「システム」→「全般」または
``app/WEB-INF/conf/system.properties`` の ``spnego.allowed.realms`` に該当するレルムを
カンマ区切りで列挙してください。列挙しない場合、15.7 まではログインできていたユーザーが
``Kerberos realm is not allowed`` として拒否されます。
詳細は :doc:`../config/sso-spnego` を参照してください。

また、15.8 では ``spnego.allow.unsecure.basic`` と ``spnego.allow.localhost`` のコード上の
既定値が ``true`` から ``false`` へ変更されました。これらのキーが
``app/WEB-INF/conf/system.properties`` に存在しない環境では、アップグレードによって
より厳格な挙動が適用されます。特に ``spnego.allow.unsecure.basic=false`` では、SPNEGO ライブラリは
``HttpServletRequest#isSecure()`` が ``true`` を返すリクエストにのみ Basic 認証を提示するため、
TLS をリバースプロキシで終端して HTTP で転送している構成では、これまで Basic 認証へ
フォールバックしていたクライアントがログインできなくなります。その場合は
``tomcat_config.properties`` で ``tomcat.secure=true`` を設定してください。
詳細は :doc:`../config/sso-spnego` を参照してください。

.. warning::

   コード上の既定値は、キーが存在しない場合にのみ適用されます。管理画面「システム」→「全般」は
   保存のたびにすべての ``spnego.*`` キーを書き込むため、15.7 でこの画面から一度でも更新した環境には
   ``spnego.allow.unsecure.basic=true`` と ``spnego.allow.localhost=true`` が保存されたままです。
   この場合、15.10 へアップグレードしても設定は強化されず、緩い挙動が黙って引き継がれます。
   15.10 は SPNEGO の初期化時に ``fess.log`` へ警告を出力するだけです。管理画面「システム」→「全般」
   または ``system.properties`` で、両方を明示的に無効化してください。特に
   ``spnego.allow.localhost=true`` は危険です。SPNEGO ライブラリが同一ホストからのリクエストを
   Kerberos の検証なしにサーバーの OS ユーザーとして認証するため、同一ホスト上にリバースプロキシを
   置く構成では安全ではありません。

.. _upgrade-159-saml:

SAML 認証（SSO）を利用していた場合
----------------------------------

15.8 から、\ |Fess| は送信した AuthnRequest の ID と SAML レスポンスを対応付けて検証するため、
IdP-Initiated（未承諾・unsolicited）SSO は動作しなくなりました。IdP のポータル（Okta の
ダッシュボードや Microsoft Entra ID の「マイアプリ」など）に置いたタイルから開始したログインは、
対応付ける AuthnRequest が存在せず拒否されます。15.7 では、\ |Fess| が対応付けできないレスポンスを
IdP へ差し戻し、IdP が即座に SP-Initiated のアサーションを返していたため動作していました。
IdP 側にタイルを配置する場合は、リンク先を |Fess| の ``/sso/`` に変更し、SP-Initiated の
ログインにしてください。

また、IdP はアサーションをクロスサイトの POST で返すため、``tomcat_config.properties`` の
``tomcat.sameSiteCookies`` に ``none`` を設定する必要があります。同梱の既定値 ``lax`` のままでは
セッション Cookie がこのリクエストに送信されず、SAML ログインが完了しません。このファイルは
ZIP 版では ``lib/classes/``\ 、DEB/RPM 版では ``/etc/fess/`` に配置されており、変更後は
|Fess| の再起動が必要です。``none`` はブラウザーが ``Secure`` 属性付きの Cookie に対してのみ
受け入れるため、\ |Fess| を HTTPS で提供する必要があります。15.7 までは同じ設定不備が明確な
エラーにならず、IdP への再リダイレクトが繰り返されるループになっていたため、動作しているように
見えていた環境でも設定を確認してください。15.10 ではループせずに 1 回で失敗します。
詳細は :doc:`../config/sso-saml` を参照してください。

Microsoft Entra ID（Azure AD）を利用していた場合
------------------------------------------------

15.8 から、認可エンドポイントに要求するレスポンスモードの既定値が ``form_post`` から ``query``
に変わりました。15.7 まではコールバックがクロスサイトの POST で返るため、\ |Fess| の既定値である
``tomcat.sameSiteCookies = lax`` ではセッションクッキーが送信されず、\ ``none`` への変更が必要で
した。この回避策のためだけに ``none`` を設定していた場合は、既定値に戻せます。従来どおり
``form_post`` を使う場合は ``entraid.response.mode=form_post`` を指定し、
``tomcat.sameSiteCookies = none`` を維持してください。``none`` はブラウザーが ``Secure`` 属性付きの
Cookie に対してのみ受け入れるため、この場合も |Fess| を HTTPS で提供する必要があります。

また 15.8 からは、ログイン完了後にユーザーのグループ・ロール権限をバックグラウンドで解決するように
なり、ログインがMicrosoft Graphの応答を待って止まることはなくなりました。解決が完了するまでの間、
または解決が完全には成功しなかった場合、ユーザーが保持するのは、ユーザー自身のユーザーレベルの
権限と、\ ``entraid.default.groups``\ ・\ ``entraid.default.roles``\ に設定したグループ・ロール
だけです。どちらも未設定（同梱の既定値）の場合、この間の検索は1件もヒットしません。同梱の既定値の
まま作成したクロール設定でクロールした文書には ``{role}guest`` が付与されますが、
ログイン済みユーザーはこのロールを持たないためです。解決中は検索画面にその旨のメッセージが表示され、
完全には成功しなかった場合は別のメッセージが表示されます（直接所属の取得とネストしたグループの
探索の両方が成功しない限り、解決は失敗として扱われます）。アクセストークンが更新されるたびに解決が
再実行され、その後成功すればメッセージは消えるため、トークンの有効期間を超えて続くセッションでは
失敗が最終的なものになるとは限りません。すぐに再試行したい場合は、いったんログアウトしてから
ログインし直してください。
詳細は :doc:`../config/sso-entraid` を参照してください。

バックグラウンドで解決することの副作用として、解決が完了するまでの間は、解決済みの
ロールがまだ分かりません。そのため、管理者は管理ダッシュボードではなく検索画面にリダイレクトされ、
その間に管理画面を開いても検索画面に戻されます。この時間は、最大で約1秒のスケジューリング遅延に
加えて、Microsoft Graphの呼び出しそのもの（直接所属の取得で1回、さらにネストしたグループをたどる
ために直接所属グループごとに1回ずつを順番に実行。キャッシュが未作成の場合）だけかかるため、
ユーザーが所属するグループ数に応じて長くなります。この間にアクセスが許可されてしまうことはなく、
拒否されるだけです。また、この時間帯をなくすための設定は必要ありません。認可は同じセッションの
リクエストごとに評価し直されるため、解決の完了後に開き直せば、ログインし直さなくても管理画面に
正常にアクセスできます。

.. warning::

   この時間帯を短くするために、\ |Fess| の管理者ロールを
   ``entraid.default.roles``\ に設定してはいけません。この設定は単一のグローバル設定で、\
   |Fess| はログイン時にすべてのEntra IDユーザーへ適用し、その後の解決のたびに再適用します。
   テナント内のすべてのユーザーに、永続的な |Fess| の管理者権限を与えてしまいます。

LDAP / Active Directory 連携を利用していた場合
------------------------------------------------

15.8 から、グループやロールの権限名はエントリーの DN をテキストとして切り出すのではなく、
RDN として解析した値になりました。DN の中でエスケープされる文字（一般的にはカンマ）を CN に含む
グループは、15.7 までとは異なる権限名になります。

.. list-table::
   :header-rows: 1

   * - グループのエントリー DN
     - 15.7 までの権限名
     - 15.10 の権限名
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

15.7 までは、カンマの手前までが一致する複数のグループが同じ権限名に潰れていたため、\
``Sales, EMEA`` と ``Sales, APAC`` の所属者は互いの文書と ``Sales`` グループの文書を
読めていました。
15.10 ではそれぞれ別の権限名になり、この横断的なアクセスは発生しません。

その代わり、\ **旧来の権限名でインデックスされた文書は、該当グループの利用者から見えなくなります**\ 。
クロール設定の「パーミッション」に旧来の権限名を設定していた場合は、新しい権限名に更新して
再クロール（または再インデクシング）してください。CN にカンマなどを含むグループを使っていない場合、
権限名は変わりません。

``ldap.role.search.user.enabled`` の挙動変更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

15.7 までは、\ ``ldap.role.search.user.enabled=false`` を設定していても、ユーザー名から導出した
権限（``role.search.user.prefix`` ＋ ユーザー名）は付与されていました。15.8 からはこの設定が
実際に反映され、\ ``false`` の場合は付与されません。

``false`` を設定している環境では、アップグレード後にユーザーが自分自身の権限を失うため、
個々のユーザーに対して設定した権限を持つ文書が検索できなくなります。従来の挙動を維持する場合は、
同梱の既定値である ``true`` に戻してください。

/api/v2 の設定キーを変更していた場合
------------------------------------------------

15.8.0 から、4 つの設定キーが ``api.v2.`` の接頭辞を失いました。値・既定値・挙動は変わりませんが、\
**後方互換のための別名は用意されていません**\ 。古い名前のまま残した設定は警告もなく無視され、\
同梱の既定値が使われます。

.. list-table::
   :header-rows: 1

   * - 15.7 まで
     - 15.8.0 以降
     - 既定値
   * - ``api.v2.chat.stream.keepalive.interval.ms``
     - ``api.chat.stream.keepalive.interval.ms``
     - ``15000``
   * - ``api.v2.param.max.length``
     - ``api.param.max.length``
     - ``1000``
   * - ``api.v2.param.max.array.size``
     - ``api.param.max.array.size``
     - ``100``
   * - ``api.v2.click.max.rt``
     - ``api.click.max.timestamp``
     - ``9999999999999``

``fess_config.properties`` または ``-Dfess.config.<キー>`` の JVM 引数でこれらを設定していた場合は、\
新しい名前に変更してください。影響を受けるのは明示的に設定していた場合だけで、\
変更していなかった環境で対応は不要です。

1 つ目のキーは ``POST /api/v2/chat/stream`` がモデルの応答を待つあいだに送出する keep-alive の\
間隔を決めるため、設定が失われたことに気づくのは AI 検索モードの利用時になります。\
最後のキーは名前の正確さのためにも変更されました。これはクリックログが持てる ``rt`` の値の上限で、\
応答時間ではなくタイムスタンプを指します。


.. _upgrade-plugin-versions:

プラグインのバージョン更新
--------------------------

``app/WEB-INF/plugin/`` にインストールされているプラグインは、\ |Fess| のバージョンに対応した
ものへ入れ替えが必要です。 ``bin/fess-setup upgrade plugins`` は、インストール済みのすべての
プラグインについて、この |Fess| 向けにビルドされたバージョンをインストールし、古いものを
削除します。その後 |Fess| を再起動してください。 ``bin/fess-setup check`` は、OpenSearch と
そのプラグイン、インストール済みの |Fess| プラグインの状態を報告し、問題がある場合は終了コード 1
で終了します。 ``bin/fess.in.sh``\ 、\ ``/etc/sysconfig/fess``\ 、\ ``/etc/default/fess`` は読み込まないため、
OpenSearch が ``http://localhost:9200`` にない場合は、 ``--url`` を指定するか、実行するシェルで
``SEARCH_ENGINE_HTTP_URL`` を設定してください。そうしないと、エンジンに接続できないと報告されます。

::

    $ bin/fess-setup upgrade plugins
    $ bin/fess-setup check

``upgrade plugins`` が対象にするのはインストール済みのプラグインだけです。 ``fess-script-groovy``
など、15.9 で配布物から外れた部分を補うプラグインは、前述の各節のとおり
``bin/fess-setup install plugin`` でインストールしてください。

Docker 版で ``FESS_PLUGINS`` を指定している場合は、
``fess-ds-wikipedia:15.10.0`` のようにバージョン部分を更新してください。

ロールバック手順
================

アップグレードに失敗した場合、以下の手順でロールバックできます。

ステップ 1: 新しいバージョンの停止
----------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

ステップ 2: 古いバージョンの復元
--------------------------------

バックアップから設定ファイルとデータを復元します。

RPM/DEB 版の場合::

    $ sudo rpm -Uvh --oldpackage --nodeps fess-<old-version>.rpm

または::

    $ sudo dpkg -i fess-<old-version>.deb

.. note::

   RPM では ``--nodeps`` が必要です。15.8.0 のパッケージは ``fess`` と ``opensearch`` のユーザーとグループを
   必須としているため、指定しないと ``rpm`` は ``Failed dependencies: group(fess) is needed by fess-15.8.0``
   でダウングレードを拒否します。

.. warning::

   15.8.0 の DEB パッケージは ``/etc/fess/*`` を conffile として登録していないため、 ``dpkg -i`` は、
   編集した ``/etc/fess/fess_config.properties`` などを、コピーを残さずに上書きします。ステップ 1 で
   取ったバックアップから戻してください。

ステップ 3: データの復元
------------------------

スナップショットから復元します。OpenSearch を起動し、 |Fess| は停止したままにしてください。

1. OpenSearch を起動します::

       $ sudo systemctl start opensearch.service

2. スナップショットは、存在するインデックスの上には復元できません。そのため、アップグレード後に
   （再インデクシングなどで）作成されたものと、OpenSearch のプラグインが作成する ``configsync``
   インデックスを含め、Fess のインデックスをすべて先に削除します。スナップショットに含まれる
   インデックスだけを削除すると、再インデクシングで作られたインデックスが残り、 ``fess.search`` が
   2 つのインデックスを指して、15.8.0 が起動しません::

       $ curl "http://localhost:9200/_cat/indices/fess*,configsync?h=index"
       $ curl -X DELETE "http://localhost:9200/<index name>"

   2 つ目のコマンドは、1 つ目が表示したインデックスごとに実行します。

3. スナップショットを復元します::

       $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

.. note::

   辞書ディレクトリ（ ``configsync.config_path`` 。辞書ファイルを含む）は、以前と同じように存在している
   必要があります。失われたマシンでは、復元は完了しても、辞書を使うインデックスは red のままになります。

または、バックアップからディレクトリを復元（ステップ 1 で作成したアーカイブの名前を指定します）::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-<YYYYMMDD>.tar.gz -C /
    $ sudo systemctl start opensearch

Docker 版では、旧バージョンの Compose ファイルに戻したうえで、ボリュームの内容を復元します::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   管理画面からダウンロードした設定データは、\ |Fess| の起動後に「システム情報」→「バックアップ」
   ページのアップロード機能から再度インポートして復元できます。アップロードできるのは
   ``*.bulk``\ 、\ ``system`` で始まる ``*.properties``\ 、\ ``gsa`` で始まる ``*.xml``\ 、
   ``fess`` で始まる ``*.json``\ 、\ ``doc`` で始まる ``*.json`` のみで、1 回の操作につき 1 ファイルです。
   検索ログなどの ``*.ndjson`` ファイルは受け付けられず、エラーになります。

.. warning::

   ``fess.json`` と ``doc.json`` のアップロードは、\ |Fess| に同梱されているインデックス定義
   ファイルそのものを上書きします。アップグレード後に旧バージョンの ``fess.json`` や
   ``doc.json`` をアップロードすると、新しいバージョンのインデックス設定・マッピングが失われます。
   ロールバックの目的以外ではアップロードしないでください。

.. note::

   アップロードされた ``system.properties`` はメモリー上にのみ読み込まれ、ファイルには
   書き出されません。そのため ``system.properties`` の内容は |Fess| を再起動すると失われます。
   確実に復元するには、バックアップしたファイルを所定の場所（ZIP 版は
   ``app/WEB-INF/conf/``\ 、RPM/DEB 版は ``/etc/fess/``\ ）へ直接配置してから起動してください。

.. note::

   インポートは非同期で実行され、画面には開始した旨のみが表示されます。
   実際に成功したかどうかは ``fess.log`` を確認してください。

ステップ 4: サービスの起動と確認
--------------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

動作を確認し、正常に戻ったことを確認します。

よくある質問
============

Q: ダウンタイムなしでアップグレードできますか？
-----------------------------------------------

A: Fess のアップグレードには、サービスの停止が必要です。ダウンタイムを最小限にするには、以下を検討してください：

- 事前にテスト環境で手順を確認する
- バックアップを事前に取得しておく
- メンテナンス時間を十分に確保する

Q: OpenSearch もアップグレードする必要がありますか？
----------------------------------------------------

A: |Fess| のバージョンごとに対応する OpenSearch のバージョンが決まっています。
|Fess| 15.10 は OpenSearch 3.9.0 に対応しています。
``opensearch-analysis-fess`` などの |Fess| 用 OpenSearch プラグインは OpenSearch のバージョンと
完全に一致している必要があるため、OpenSearch をアップグレードする場合は、
対応するバージョン（3.9.0）のプラグインに更新してください。

なお |Fess| 15.10 は k-NN プラグインを必須とし、インデックス設定に ``knn.derived_source.enabled``
を常に送信します。古い OpenSearch のままでは新しいインデックスの作成に失敗するため、
実質的に OpenSearch のアップグレードが必要です。詳細はステップ 4 を参照してください。

Q: インデックスを再作成する必要がありますか？
---------------------------------------------

A: |Fess| のマイナーバージョンアップ（15.x → 15.10）で、チャンクベクトル検索を利用しない場合は
通常不要です。既存インデックスはそのまま利用でき、\ ``content_chunker.enabled`` などは既定で
無効のため挙動は変わりません。

次の場合は再作成・再インデクシングが必要です。

- **新たにチャンクベクトル検索（セマンティック検索）を有効にする場合**: 既存インデックスには
  新しいマッピングが反映されないため、再インデクシングが必須です。詳細は
  :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）を参照してください。
- **14.x からアップグレードする場合**: OpenSearch が 2.x から 3.x へメジャーバージョンアップ
  するため、インデックスの再作成を推奨します。
- **15.8 以前で作成した文書インデックスで、所有者での検索やかなの正規化を使う場合**: 再インデクシングが
  必要です。詳細は :ref:`upgrade-reindex-new-fields` を参照してください。

.. warning::

   インデックスを新規に作成する操作（再インデクシングを含む）は、k-NN プラグインのない
   OpenSearch では失敗します。ステップ 4 の注意事項を確認してください。

Q: アップグレード後、検索結果が表示されません
---------------------------------------------

A: 以下を確認してください：

1. OpenSearch が起動しているか確認
2. インデックスが存在するか確認（``curl http://localhost:9200/_cat/indices``）
3. クロールを再実行

次のステップ
============

アップグレードが完了したら：

- :doc:`run` - 起動と初期設定の確認
- :doc:`security` - セキュリティ設定の見直し
- :doc:`../config/search-semantic` - チャンクベクトル検索（セマンティック検索）の設定と移行手順
- リリースノートで新機能を確認

