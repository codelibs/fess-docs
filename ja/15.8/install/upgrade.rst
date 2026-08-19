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

- Fess 14.x → Fess 15.8
- Fess 15.x → Fess 15.8

.. important::

   |Fess| 14.x は OpenSearch 2.x 系、\ |Fess| 15.8 は OpenSearch 3.8.0 に対応しています。
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
- :doc:`prerequisites` - |Fess| 15.8 の動作環境（Java、OpenSearch のバージョン）

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

   TAR.GZ/ZIP 版::

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
      TAR.GZ/ZIP 版でこれらに相当する設定は ``bin/fess.in.sh`` にあります。

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

TAR.GZ/ZIP 版には停止用のスクリプトは同梱されていません。\ ``bin/fess`` を ``-p`` オプション付きで
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

TAR.GZ/ZIP 版
-------------

1. 新しいバージョンをダウンロードして展開::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.zip
       $ unzip fess-15.8.0.zip

   .. note::

      |Fess| のアーカイブ版は ZIP 形式でのみ配布されています（``fess-15.8.0.tar.gz`` は
      提供されていません）。

2. 古いバージョンの設定をコピー::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.8.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. カスタマイズしている場合は、以下もコピーします::

       # ログ設定
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.8.0/app/WEB-INF/classes/
       # インストール済みプラグイン
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.8.0/app/WEB-INF/plugin/
       # テーマ
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.8.0/app/themes/

   .. warning::

      管理画面「デザイン」で編集した JSP（``app/WEB-INF/view/``）は、そのままコピーしないでください。
      新しいバージョンの JSP と構造が変わっている場合、画面が正しく表示されなくなります。
      新しいバージョンの JSP に対して変更内容を再適用してください。

4. 組み込み OpenSearch（``SEARCH_ENGINE_HTTP_URL`` を設定せずに ``bin/fess`` を起動する構成）を
   使用している場合は、インデックスデータもコピーします::

       $ cp -r /path/to/old-fess/es/data/. /path/to/fess-15.8.0/es/data/

5. 設定差分を確認し、必要に応じて調整します

RPM/DEB 版
----------

新しいバージョンのパッケージをインストール::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   RPM 版では ``/etc/fess/*`` の設定ファイルは ``%config(noreplace)`` として登録されているため、
   アップグレード時も保持されます（新しい既定のファイルは ``.rpmnew`` として併置されます）。
   新しい設定オプションが追加されている場合は、手動で調整が必要です。

.. warning::

   DEB 版では ``/etc/fess/*`` は conffile として登録されていません（conffile は
   ``/etc/default/fess``\ 、\ ``/etc/init.d/fess``\ 、\ ``/usr/lib/systemd/system/fess.service``
   の 3 つのみです）。そのため ``dpkg -i`` を実行すると ``/etc/fess/fess_config.properties`` などが
   新しいバージョンのファイルで上書きされます。ステップ 1 でバックアップした設定を、
   アップグレード後に再適用してください。
   なお ``/etc/fess/system.properties`` はパッケージに含まれない実行時生成ファイルのため、
   上書きされません。

Docker 版
---------

1. 新しいバージョンの Compose ファイルを取得::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. 新しいイメージを取得::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

ステップ 4: OpenSearch のアップグレード
=======================================

|Fess| 15.8 は OpenSearch 3.8.0 に対応しています。接続先の OpenSearch がこれより古い場合は、
以下の手順でアップグレードしてください。

.. note::

   この手順は TAR.GZ/ZIP 版および RPM/DEB 版で OpenSearch を手動運用している場合の手順です。
   Docker 版では、ステップ 3 で新しいイメージを取得すると OpenSearch とプラグインも
   まとめて更新されるため、本ステップは不要です。

.. important::

   |Fess| 15.8 は、チャンクベクトル検索（セマンティック検索）の利用有無にかかわらず、
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
      |Fess| 15.8 は OpenSearch 3.8.0 に対応しています。バージョンが一致しない場合、
      プラグインのインストールに失敗します。

3. OpenSearch を起動::

       $ sudo systemctl start opensearch.service

ステップ 5: 新しいバージョンの起動
==================================

TAR.GZ/ZIP 版::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d -p /path/to/fess-15.8.0/fess.pid

.. note::

   ``-p`` を指定すると PID ファイルが作成され、次回の停止時に
   ``kill $(cat /path/to/fess-15.8.0/fess.pid)`` で停止できます。

RPM/DEB 版::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker 版::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

ステップ 6: 動作確認
====================

1. **ログの確認**

   エラーがないことを確認します。

   TAR.GZ/ZIP 版::

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

15.8 固有の移行作業
===================

15.7 以前から 15.8 へアップグレードする場合、利用している機能に応じて以下の作業が必要です。

セマンティック検索を利用していた場合
------------------------------------

15.7 以前でセマンティック検索を提供していた ``fess-webapp-semantic-search`` プラグインは、
15.8 でコアに統合されたため不要になりました（非推奨）。プラグインの削除、\ ``-Dfess.semantic_search.*``
および ``-Drank.fusion.searchers=default,semantic`` の削除、旧 ingest pipeline のデタッチが
必要です。手順は :ref:`semantic-search-migration`\ （:doc:`../config/search-semantic`）を
参照してください。

AI 検索モード（RAG チャット）を利用していた場合
-----------------------------------------------

15.8 から、AI 検索モード（RAG チャット）の機能は ``fess-llm-ollama``\ 、\ ``fess-llm-openai``\ 、
``fess-llm-gemini`` などのプラグインとして分離されました。利用しているプロバイダーに対応する
プラグインを管理画面「システム」→「プラグイン」からインストールしてください。

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
   この場合、15.8 へアップグレードしても設定は強化されず、緩い挙動が黙って引き継がれます。
   15.8 は SPNEGO の初期化時に ``fess.log`` へ警告を出力するだけです。管理画面「システム」→「全般」
   または ``system.properties`` で、両方を明示的に無効化してください。特に
   ``spnego.allow.localhost=true`` は危険です。SPNEGO ライブラリが同一ホストからのリクエストを
   Kerberos の検証なしにサーバーの OS ユーザーとして認証するため、同一ホスト上にリバースプロキシを
   置く構成では安全ではありません。

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
見えていた環境でも設定を確認してください。15.8 ではループせずに 1 回で失敗します。
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
     - 15.8 の権限名
   * - ``CN=Sales\, EMEA,CN=Users,...``
     - ``2Sales``
     - ``2Sales, EMEA``
   * - ``CN=Sales\, APAC,CN=Users,...``
     - ``2Sales``
     - ``2Sales, APAC``

15.7 までは、カンマの手前までが一致する複数のグループが同じ権限名に潰れていたため、\
``Sales, EMEA`` と ``Sales, APAC`` の所属者は互いの文書と ``Sales`` グループの文書を
読めていました。
15.8 ではそれぞれ別の権限名になり、この横断的なアクセスは発生しません。

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

プラグインのバージョン更新
--------------------------

``app/WEB-INF/plugin/`` にインストールされているプラグインは、\ |Fess| のバージョンに対応した
ものへ入れ替えが必要です。Docker 版で ``FESS_PLUGINS`` を指定している場合は、
``fess-ds-wikipedia:15.8.0`` のようにバージョン部分を更新してください。

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
   確実に復元するには、バックアップしたファイルを所定の場所（TAR.GZ/ZIP 版は
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
|Fess| 15.8 は OpenSearch 3.8.0 に対応しています。
``opensearch-analysis-fess`` などの |Fess| 用 OpenSearch プラグインは OpenSearch のバージョンと
完全に一致している必要があるため、OpenSearch をアップグレードする場合は、
対応するバージョン（3.8.0）のプラグインに更新してください。

なお |Fess| 15.8 は k-NN プラグインを必須とし、インデックス設定に ``knn.derived_source.enabled``
を常に送信します。古い OpenSearch のままでは新しいインデックスの作成に失敗するため、
実質的に OpenSearch のアップグレードが必要です。詳細はステップ 4 を参照してください。

Q: インデックスを再作成する必要がありますか？
---------------------------------------------

A: |Fess| のマイナーバージョンアップ（15.x → 15.8）で、チャンクベクトル検索を利用しない場合は
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

