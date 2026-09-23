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

- Fess 14.x → Fess 15.9
- Fess 15.x → Fess 15.9

.. important::

   |Fess| 14.x は OpenSearch 2.x 系、\ |Fess| 15.9 は OpenSearch 3.8.0 に対応しています。
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
- :doc:`prerequisites` - |Fess| 15.9 の動作環境（Java、OpenSearch のバージョン）

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
     サムネイルキューなどの実行時データを含む 25 インデックス
   - ``fess_user.bulk`` - ユーザー、ロール、グループ
   - ``system.properties`` - 全般設定を含むシステム設定
   - ``fess.json`` - インデックスの設定（シャード数、\ ``index.knn`` など）
   - ``doc.json`` - ドキュメントのマッピング（フィールド定義）

   .. note::

      ``fess_config.bulk`` は ``fess_basic_config.bulk`` を包含しています。アップグレード前の
      設定バックアップとしては、\ ``fess_basic_config.bulk``\ 、\ ``fess_user.bulk``\ 、
      ``system.properties`` の 3 つで十分です。

   .. note::

      検索ログやクリックログなどのログデータ（``search_log.ndjson``、``click_log.ndjson``、
      ``favorite_log.ndjson``、``user_info.ndjson``）も同じページからダウンロードできます。
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

ステップ 3: 新しいバージョンのインストール
==========================================

インストール方法により、手順が異なります。

ZIP 版
-------------

1. 新しいバージョンをダウンロードして展開::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.9.0/fess-15.9.0.zip
       $ unzip fess-15.9.0.zip

   .. note::

      |Fess| のアーカイブ版は ZIP 形式でのみ配布されています（``fess-15.9.0.tar.gz`` は
      提供されていません）。

2. 古いバージョンの設定をコピー::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.9.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.9.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.9.0/bin/

   .. warning::

      ``fess_config.properties`` と ``fess.in.sh`` をそのままコピーすると、15.9 で既定値が変わった
      値も含めて、旧バージョンの値が引き継がれます。たとえば、アップグレード後に作成したジョブの
      既定は Groovy になります。後の 2 つのコマンドを実行する前に、各ファイルを ``fess-15.9.0``
      のファイルと比較し、自分で変更した値だけを移してください。確認すべき項目は
      :ref:`upgrade-159-carried-over-config` を参照してください。

3. カスタマイズしている場合は、以下もコピーします::

       # ログ設定
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.9.0/app/WEB-INF/classes/
       # インストール済みプラグイン
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.9.0/app/WEB-INF/plugin/
       # 自分でアップロードした静的テーマ（テーマごとのディレクトリ。bootstrap は除く）
       $ cp -r /path/to/old-fess/app/themes/<your-theme> /path/to/fess-15.9.0/app/themes/

   .. warning::

      ``app/themes/`` ディレクトリ全体はコピーしないでください。このディレクトリには |Fess| に
      同梱のテーマ ``bootstrap`` も入っており、15.9 のものに上書きすると、15.9 の検索画面が
      15.8 版のテーマに置き換わります。コピーするのは自分で作成したテーマのディレクトリだけにして
      ください。 |Fess| プロジェクトが公開しているテーマは、 ``bin/fess-setup install theme <name>``
      で 15.9 向けのビルドをインストールしてください（ :doc:`fess-setup` を参照）。

   .. warning::

      管理画面「デザイン」で編集した JSP（``app/WEB-INF/view/``）はコピーしないでください。
      15.9 の検索画面は静的テーマで、これらの JSP を使いません。変更内容の移し先は
      :ref:`upgrade-159-static-theme` を参照してください。

   .. note::

      ``app/WEB-INF/plugin/`` からコピーしたプラグインは、旧バージョン向けにビルドされています。
      コピーした後、 ``fess-15.9.0`` で ``bin/fess-setup upgrade plugins`` を実行し、15.9 向けに
      ビルドされたバージョンに入れ替えてください（ :ref:`upgrade-plugin-versions` を参照）。

4. 設定差分を確認し、必要に応じて調整します

RPM/DEB 版
----------

新しいバージョンのパッケージをインストール::

    # RPM
    $ sudo rpm -Uvh fess-15.9.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.9.0.deb

.. note::

   RPM 版では ``/etc/fess/*`` の設定ファイルは ``%config(noreplace)`` として登録されているため、
   アップグレード時も保持されます（新しい既定のファイルは ``.rpmnew`` として併置されます）。
   新しい設定オプションが追加されている場合は、手動で調整が必要です。変更を加えた
   ``/etc/fess/fess_config.properties`` は、ZIP 版の手順でコピーしたファイルと同様に、15.9 でも
   旧バージョンの値のまま使われます。 :ref:`upgrade-159-carried-over-config` を参照してください。

.. warning::

   DEB 版では ``/etc/fess/*`` は conffile として登録されていません（conffile は
   ``/etc/default/fess``\ 、\ ``/etc/init.d/fess``\ 、\ ``/usr/lib/systemd/system/fess.service``
   の 3 つのみです）。そのため ``dpkg -i`` を実行すると ``/etc/fess/fess_config.properties`` などが
   新しいバージョンのファイルで上書きされます。確認は求められず、旧ファイルのコピーも残らないため、
   事前にバックアップしてください（ステップ 1）。アップグレード後は、旧ファイルをそのまま戻すの
   ではなく、新しいファイルに変更内容を再適用してください（ :ref:`upgrade-159-carried-over-config`
   を参照）。
   なお ``/etc/fess/system.properties`` はパッケージに含まれない実行時生成ファイルのため、
   上書きされません。

Docker 版
---------

1. 新しいバージョンの Compose ファイルを取得::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

2. 新しいイメージを取得::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

ステップ 4: OpenSearch のアップグレード
=======================================

|Fess| 15.9 は OpenSearch 3.8.0 に対応しています。接続先の OpenSearch がこれより古い場合は、
以下の手順でアップグレードしてください。

.. note::

   この手順は ZIP 版および RPM/DEB 版で OpenSearch を手動運用している場合の手順です。
   Docker 版では、ステップ 3 で新しいイメージを取得すると OpenSearch とプラグインも
   まとめて更新されるため、本ステップは不要です。

.. important::

   |Fess| 15.9 は、チャンクベクトル検索（セマンティック検索）の利用有無にかかわらず、
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

1. 新しいバージョンの OpenSearch をインストール

2. プラグインを再インストール::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      これらのプラグインのバージョンは、使用する OpenSearch のバージョンと一致させる必要があります。
      |Fess| 15.9 は OpenSearch 3.8.0 に対応しています。バージョンが一致しない場合、
      プラグインのインストールに失敗します。

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

    $ cd /path/to/fess-15.9.0
    $ ./bin/fess -d -p /path/to/fess-15.9.0/fess.pid

.. note::

   ``-p`` を指定すると PID ファイルが作成され、次回の停止時に
   ``kill $(cat /path/to/fess-15.9.0/fess.pid)`` で停止できます。

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

1. 既存のクロールスケジュールを確認
2. 「システム」→「スケジューラ」から「Default Crawler」を実行
3. クロールが完了するまで待機
4. 検索結果を確認

.. warning::

   再インデクシングでは新しいマッピングでインデックスが作り直されるため、k-NN プラグインの
   ない OpenSearch では失敗します。ステップ 4 の注意事項を確認してください。

15.8 から 15.9 へのアップグレード
=================================

15.8 からアップグレードする場合、以下が互換性のない変更です。

組み込み OpenSearch の廃止
--------------------------

15.8 までは ``SEARCH_ENGINE_HTTP_URL`` を設定せずに ``bin/fess`` を起動すると、|Fess| が自身の
JVM 内で OpenSearch ノードを起動していました。15.9 ではこの構成がなくなり、検索エンジンは常に
別のサーバーになります。

``bin/fess.in.sh`` は既定で ``SEARCH_ENGINE_HTTP_URL=http://localhost:9200`` を設定します。
接続先の OpenSearch がない場合、|Fess| は起動に失敗します。 ``bin/fess-setup install opensearch``
で導入できます（Linux と Windows のみ。macOS には OpenSearch の公式配布がないため、Homebrew か
Docker を使用してください）。

また、 ``FESS_DICTIONARY_PATH`` をその OpenSearch の ``opensearch.yml`` にある ``configsync.config_path`` と一致させる必要があります。設定されていないか一致していないと、 |Fess| はインデックスを作成できません。15.9 の ``bin/fess.in.sh`` （Windows では ``bin\fess.in.bat`` ）は、 |Fess| のディレクトリの ``opensearch/`` に ``bin/fess-setup install opensearch`` で導入した OpenSearch が 1 つだけある場合に、これを自動で設定します。それ以外の OpenSearch を使う場合は、 :doc:`install-linux` または :doc:`install-windows` のとおりに設定してください。

あわせて次が廃止されました。

- ``es/`` ディレクトリ（ ``es/modules`` 、 ``es/plugins`` 、 ``es/data`` ）
- ``-Dfess.es.dir`` と ``SEARCH_ENGINE_HOME``
- ``bin/module.xml`` と ``bin/plugin.xml``
- 旧 ``elasticsearch.*`` 設定キーのフォールバック

また、OpenSearch 3 より前のバージョンに接続した場合、15.8 まではエラーログを出して起動を続行して
いましたが、15.9 では起動に失敗します。これらのバージョンは全文書を走査する処理が使う
``_shard_doc`` ソートを実装しておらず、HTTP 経由では失敗せずに応答が返らなくなるためです。

.. warning::

   組み込み OpenSearch で運用していた場合、インデックスデータは引き継げません。外部の
   OpenSearch サーバーを新しく構築し、管理画面「バックアップ」で設定を移したうえで
   再クロールしてください。バックアップに含まれるのはクロール設定・ユーザー・ログで、
   **クロール済みの文書は含まれません**。

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

Playwright クローラを使用していない場合、対応は不要です。

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
ログインページへリダイレクトされ、SSO でログインできません。15.9 では探した
コンポーネント名と提供元のプラグイン名を含む警告が ``fess.log`` に記録されます。
15.8 まではどのログレベルでも何も出力されませんでした。

SSO を使用していない場合、つまり ``sso.type`` が ``none`` または未設定の場合、
対応は不要です。

標準のスクリプトエンジンが Groovy から JavaScript に変更
--------------------------------------------------------

15.8 までは標準のスクリプトエンジンが Groovy で、 ``job.default.script`` の既定値も ``groovy``
でした。15.9 では標準のエンジンが JavaScript になり、既定値は ``javascript`` です。Groovy は
標準では組み込まれなくなり、 ``fess-script-groovy`` プラグインで提供されます。 ``scriptType``
に ``groovy`` を指定するには、このプラグインをインストールしておく必要があります。

アップグレードでは、各設定に保存されたスクリプトエンジンは変更されません。また、15.9 より前に
保存され、エンジンを記録していない設定は ``groovy`` として扱われます。プラグインがない場合、
次の設定が動作しなくなります。

- ``groovy`` として保存されたスケジュールジョブ。
  **15.8 が自動で登録したジョブもこれに該当します。**\ Default Crawler、Suggest Indexer、
  Config Reloader、Log Aggregator、Doc Purger などの同梱ジョブはすべて ``groovy`` として保存されて
  おり、15.9 は起動時にまだ存在しない同梱ジョブだけを追加するため、これらは書き換えられません。
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

15.9 には ``org.opensearch`` のクラスが含まれなくなり、ジョブのスクリプトで使用するクエリビルダーは
``org.codelibs.fesen.opensearch`` の下に移りました。15.8 が Index Exporter ジョブに保存した
スクリプトは ``org.opensearch.index.query.QueryBuilders`` を参照しており、アップグレードでも
置き換えられないため、 ``fess-script-groovy`` をインストールしてもこのジョブは失敗します。
このジョブは無効かつスケジュールなしの状態で同梱されているため、影響があるのは実行している
場合だけです。管理画面「システム」→「スケジューラ」でジョブを開き、スクリプトのパッケージを
15.9 のものに変更してください。

::

    return new org.codelibs.fess.job.IndexExportJob().query(org.codelibs.fesen.opensearch.index.query.QueryBuilders.matchAllQuery()).execute()

独自に作成したスクリプトで ``org.opensearch.index.query`` を参照している場合も、同じように
変更してください。クエリの例は :doc:`../config/admin-index-export` を参照してください。

.. _upgrade-159-carried-over-config:

15.8 から引き継いだ設定ファイル
-------------------------------

ステップ 3 の ZIP 版の手順では、旧バージョンの ``fess_config.properties`` と ``bin/fess.in.sh``
をコピーします。RPM 版のアップグレードでは、変更を加えた ``/etc/fess/fess_config.properties``
がそのまま残ります（15.9 のファイルは ``fess_config.properties.rpmnew`` として併置されます）。
いずれの場合も 15.9 は 15.8 の値のまま動作し、15.9 で同梱の値が変わったキーも例外ではありません。
少なくとも次のキーを確認してください。

.. list-table::
   :header-rows: 1

   * - キー
     - 15.8.0
     - 15.9
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
       ``bin/fess.in.sh`` で設定していなかった場合がこれに当たり、\ |Fess| は 15.9 で廃止された
       組み込み OpenSearch のポートである 9201 で OpenSearch を探します。
   * - ``jvm.crawler.options``\ 、\ ``jvm.thumbnail.options``
     - ``-Djcifs.smb.client.*``\ 、\ ``-Djcifs.smb1.smb.client.*``
     - ``-Djcifs.client.*``
     - SMB のタイムアウトが jcifs の既定値のままになります。 :ref:`upgrade-159-jcifs` を
       参照してください。
   * - ``crawler.default.script``\ 、\ ``theme.allowed.archive.extensions``\ 、
       ``theme.assets.cache.max.age``\ 、\ ``theme.assets.precompressed``\ 、
       ``rag.chat.message.max.length``\ 、\ ``supported.uploaded.js.extentions``\ 、
       ``supported.uploaded.css.extentions``\ 、\ ``supported.uploaded.media.extentions``\ 、
       ``supported.uploaded.files``\ 、\ ``online.help.name.design``
     - あり
     - 削除
     - 効果はありません。削除してください。

15.8 からコピーした ``bin/fess.in.sh`` には、15.9 のファイルにある次の 2 点もありません。
15.9 は ``SEARCH_ENGINE_HTTP_URL`` に ``http://localhost:9200`` を設定しますが、15.8 のファイルは
自分で設定しない限り未設定のままです。また、 ``bin/fess-setup install nodejs`` で導入した
Node.js を検出しないため、 ``PLAYWRIGHT_NODEJS_PATH`` を自分で設定しない限り、Playwright
クローラは Node.js を見つけられません。

どちらのファイルも丸ごとコピーするのではなく、15.9 に同梱のファイルを元にして、変更した値を
再適用してください。変更した値は ``diff`` で確認できます::

    $ diff /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.9.0/app/WEB-INF/classes/fess_config.properties
    $ diff /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.9.0/bin/fess.in.sh

RPM 版では、同じように ``/etc/fess/fess_config.properties`` と
``/etc/fess/fess_config.properties.rpmnew`` を比較してください。DEB 版のアップグレードでは
``/etc/fess/fess_config.properties`` が上書きされるため（ステップ 3 を参照）、15.9 の値から
始まり、再適用が必要なのは自分で変更した値だけです。

.. _upgrade-159-jcifs:

SMB のタイムアウトは jcifs 3 のプロパティ名を使用
-------------------------------------------------

SMB ファイルサーバーのクロールに |Fess| が使用する jcifs は、バージョン 3 でプロパティ名を
変更しました。 ``jcifs.smb.client.*`` は ``jcifs.client.*`` になり、SMB1 用の
``jcifs.smb1.smb.client.*`` も同じプロパティに統合されました。15.8 までの ``jvm.crawler.options``
と ``jvm.thumbnail.options`` は旧名を渡しており、jcifs はそれを読まないため、SMB のクロールは
jcifs の既定値で動作していました。15.9 は新しい名前を渡します。

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

検索画面は静的テーマに
----------------------

別のテーマを選んでいない限り、検索画面は |Fess| に同梱の静的テーマ ``bootstrap`` で表示されます。
対象は ``/`` 、 ``/search`` 、 ``/advance`` 、 ``/help`` 、 ``/profile`` 、 ``/cache`` 、 ``/chat`` と
エラーページです。15.8 までは、既定のテーマを設定していなければ、これらのページは JSP でした。

この切り替えはアップグレードでも起こります。既定のテーマを設定したことのない 15.8 の環境では
``system.properties`` に ``theme.default`` が無いため、アップグレード後は静的テーマで表示されます。
設定ファイルには何も書き込まれず、ログにも何も出ません。JSP の検索画面に戻す設定はありません。
15.8 で既定のテーマを設定していた場合、その設定は引き継がれます。そのテーマは 15.9 向けのビルドを
インストールしてください（ ``bin/fess-setup install theme <name>`` ）。インストールされていないテーマを
既定に指定していると、 ``fess.log`` に警告を出して ``bootstrap`` で表示します。

管理画面の「ページのデザイン」や JAR テーマプラグインで検索画面の JSP、CSS、画像を変更していた場合、
その変更は表示されなくなります。変更は静的テーマで行ってください。同梱のテーマを複製して変更するか
（ :ref:`theme-customize-bundled` を参照）、公開されているテーマを管理画面の「システム」>「テーマ」または
``bin/fess-setup install theme <name>`` でインストールします。仮想ホストごとの見た目は、仮想ホスト名と
同じ名前の静的テーマで変えます（ :doc:`../config/security-virtual-host` を参照）。ログイン画面
（ ``/login/`` ）は引き続き JSP です。

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
     - 15.9
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

管理画面の「ページのデザイン」を削除
------------------------------------

管理画面の [システム > ページのデザイン] を削除しました。検索画面の JSP、CSS、画像を管理画面から
編集することはできません。検索画面の見た目は静的テーマで変更してください（ :ref:`theme-customize-bundled`
を参照）。

次のキーも ``fess_config.properties`` から削除しました。この名前で残した値は使われません。

- ``supported.uploaded.js.extentions``
- ``supported.uploaded.css.extentions``
- ``supported.uploaded.media.extentions``
- ``supported.uploaded.files``
- ``online.help.name.design``

``admin-design`` と ``admin-design-view`` のロールは、何の権限も与えなくなりました。これらのロールだけを
持つユーザーは、ログインすると管理画面ではなく検索画面に移動します。

15.9 固有の移行作業
===================

15.7 以前から 15.9 へアップグレードする場合、利用している機能に応じて以下の作業が必要です。

セマンティック検索を利用していた場合
------------------------------------

15.7 以前でセマンティック検索を提供していた ``fess-webapp-semantic-search`` プラグインは、
15.9 でコアに統合されたため不要になりました（非推奨）。プラグインの削除、\ ``-Dfess.semantic_search.*``
および ``-Drank.fusion.searchers=default,semantic`` の削除、旧 ingest pipeline のデタッチが
必要です。手順は :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）を
参照してください。

AI 検索モード（RAG チャット）を利用していた場合
-----------------------------------------------

15.9 から、AI 検索モード（RAG チャット）の機能は ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、
``fess-llm-gemini`` などのプラグインとして分離されました。利用しているプロバイダーに対応する
プラグインを管理画面「システム」→「プラグイン」からインストールしてください。

SPNEGO（Windows 統合認証）を利用していた場合
--------------------------------------------

15.9 から、クライアントのプリンシパルの Kerberos レルムがサーバーのレルムと異なる場合、
SPNEGO ログインは拒否されます。AD のドメインツリーの子ドメインや信頼関係を結んだフォレストの
ユーザーがログインする構成では、管理画面「システム」→「全般」または
``app/WEB-INF/conf/system.properties`` の ``spnego.allowed.realms`` に該当するレルムを
カンマ区切りで列挙してください。列挙しない場合、15.7 まではログインできていたユーザーが
``Kerberos realm is not allowed`` として拒否されます。
詳細は :doc:`../config/sso-spnego` を参照してください。

また、15.9 では ``spnego.allow.unsecure.basic`` と ``spnego.allow.localhost`` のコード上の
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
   この場合、15.9 へアップグレードしても設定は強化されず、緩い挙動が黙って引き継がれます。
   15.9 は SPNEGO の初期化時に ``fess.log`` へ警告を出力するだけです。管理画面「システム」→「全般」
   または ``system.properties`` で、両方を明示的に無効化してください。特に
   ``spnego.allow.localhost=true`` は危険です。SPNEGO ライブラリが同一ホストからのリクエストを
   Kerberos の検証なしにサーバーの OS ユーザーとして認証するため、同一ホスト上にリバースプロキシを
   置く構成では安全ではありません。

SAML 認証（SSO）を利用していた場合
----------------------------------

15.9 から、\ |Fess| は送信した AuthnRequest の ID と SAML レスポンスを対応付けて検証するため、
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
見えていた環境でも設定を確認してください。15.9 ではループせずに 1 回で失敗します。
詳細は :doc:`../config/sso-saml` を参照してください。

Microsoft Entra ID（Azure AD）を利用していた場合
------------------------------------------------

15.9 から、認可エンドポイントに要求するレスポンスモードの既定値が ``form_post`` から ``query``
に変わりました。15.7 まではコールバックがクロスサイトの POST で返るため、\ |Fess| の既定値である
``tomcat.sameSiteCookies = lax`` ではセッションクッキーが送信されず、\ ``none`` への変更が必要で
した。この回避策のためだけに ``none`` を設定していた場合は、既定値に戻せます。従来どおり
``form_post`` を使う場合は ``entraid.response.mode=form_post`` を指定し、
``tomcat.sameSiteCookies = none`` を維持してください。``none`` はブラウザーが ``Secure`` 属性付きの
Cookie に対してのみ受け入れるため、この場合も |Fess| を HTTPS で提供する必要があります。

また 15.9 からは、ログイン完了後にユーザーのグループ・ロール権限をバックグラウンドで解決するように
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

15.9 から、グループやロールの権限名はエントリーの DN をテキストとして切り出すのではなく、
RDN として解析した値になりました。DN の中でエスケープされる文字（一般的にはカンマ）を CN に含む
グループは、15.7 までとは異なる権限名になります。

.. list-table::
   :header-rows: 1

   * - グループのエントリー DN
     - 15.7 までの権限名
     - 15.9 の権限名
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

15.7 までは、カンマの手前までが一致する複数のグループが同じ権限名に潰れていたため、\
``Sales, EMEA`` と ``Sales, APAC`` の所属者は互いの文書と ``Sales`` グループの文書を
読めていました。
15.9 ではそれぞれ別の権限名になり、この横断的なアクセスは発生しません。

その代わり、\ **旧来の権限名でインデックスされた文書は、該当グループの利用者から見えなくなります**\ 。
クロール設定の「パーミッション」に旧来の権限名を設定していた場合は、新しい権限名に更新して
再クロール（または再インデクシング）してください。CN にカンマなどを含むグループを使っていない場合、
権限名は変わりません。

``ldap.role.search.user.enabled`` の挙動変更
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

15.7 までは、\ ``ldap.role.search.user.enabled=false`` を設定していても、ユーザー名から導出した
権限（``role.search.user.prefix`` ＋ ユーザー名）は付与されていました。15.9 からはこの設定が
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
で終了します。

::

    $ bin/fess-setup upgrade plugins
    $ bin/fess-setup check

``upgrade plugins`` が対象にするのはインストール済みのプラグインだけです。 ``fess-script-groovy``
など、15.9 で配布物から外れた部分を補うプラグインは、前述の各節のとおり
``bin/fess-setup install plugin`` でインストールしてください。

Docker 版で ``FESS_PLUGINS`` を指定している場合は、
``fess-ds-wikipedia:15.9.0`` のようにバージョン部分を更新してください。

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

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

または::

    $ sudo dpkg -i fess-<old-version>.deb

ステップ 3: データの復元
------------------------

スナップショットから復元::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

または、バックアップからディレクトリを復元::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
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
|Fess| 15.9 は OpenSearch 3.8.0 に対応しています。
``opensearch-analysis-fess`` などの |Fess| 用 OpenSearch プラグインは OpenSearch のバージョンと
完全に一致している必要があるため、OpenSearch をアップグレードする場合は、
対応するバージョン（3.8.0）のプラグインに更新してください。

なお |Fess| 15.9 は k-NN プラグインを必須とし、インデックス設定に ``knn.derived_source.enabled``
を常に送信します。古い OpenSearch のままでは新しいインデックスの作成に失敗するため、
実質的に OpenSearch のアップグレードが必要です。詳細はステップ 4 を参照してください。

Q: インデックスを再作成する必要がありますか？
---------------------------------------------

A: |Fess| のマイナーバージョンアップ（15.x → 15.9）で、チャンクベクトル検索を利用しない場合は
通常不要です。既存インデックスはそのまま利用でき、\ ``content_chunker.enabled`` などは既定で
無効のため挙動は変わりません。

次の場合は再作成・再インデクシングが必要です。

- **新たにチャンクベクトル検索（セマンティック検索）を有効にする場合**: 既存インデックスには
  新しいマッピングが反映されないため、再インデクシングが必須です。詳細は
  :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）を参照してください。
- **14.x からアップグレードする場合**: OpenSearch が 2.x から 3.x へメジャーバージョンアップ
  するため、インデックスの再作成を推奨します。

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

