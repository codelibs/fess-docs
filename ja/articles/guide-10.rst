=============================================
Fess の本番運用：監視・バックアップ・障害対応
=============================================

はじめに
========

Fess を社内に公開したあと、運用担当者が困るのは次のような場面です。
検索できなくなったことに利用者からの問い合わせで初めて気づく、夜間のクロールが失敗していたのに数日気づかない、サーバーを作り直したら設定が戻らない。

本記事では、Fess 15.9 が備えている仕組みを使って、これらに備える手順を説明します。

- ``/api/v2/health`` と ``/api/admin/stats`` で、Fess と OpenSearch の状態を外部の監視ツールから確かめる
- クロールの終了、OpenSearch の状態の変化、エラーログを、メール・Slack・Google Chat に通知する
- どのログファイルに何が書かれ、どこにあるかを知る
- 設定のバックアップを cron で取得し、別のサーバーへ復元する
- 障害が起きたときに、Fess のどの画面とどのログを見るかを知る

設定をコードで管理する方法は :doc:`guide-16`、文書数や利用者の増加に合わせた拡張（ヒープの調整を含む）は :doc:`guide-14` で扱います。
例のコマンドは、:doc:`guide-02` の Docker 構成（``fess01`` と ``search01``）を前提にしています。
ZIP 版・RPM/DEB 版での違いは、その都度書き添えます。

監視する
========

死活監視：/api/v2/health
------------------------

Fess は認証なしで呼べるヘルスチェック API を備えています。

::

    $ curl -fsS --max-time 10 http://localhost:8080/api/v2/health
    {"response":{"status":0,"engine":{"status":"GREEN","ping_status":0}}}

HTTP ステータスの意味は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ステータス
     - 状態
   * - 200
     - Fess が応答し、OpenSearch のクラスターが ``GREEN`` または ``YELLOW``
   * - 503
     - OpenSearch のクラスターが ``RED``、または Fess から OpenSearch に接続できない（``error.details.engine.status`` は ``UNAVAILABLE``）
   * - 応答なし・タイムアウト
     - Fess のプロセスが止まっている、または OpenSearch が応答せず待たされている

監視ツールでは、このステータスコードを判定に使います。
``curl`` を使う場合は、``-f`` を付けると 503 のときに終了コードが 0 以外になります。
OpenSearch のプロセスが止まらないまま応答しなくなった場合、この API は OpenSearch の応答を ``index.health.timeout``\ （既定 ``10m``）まで待ちます。
監視側では上の例の ``--max-time 10`` のようにタイムアウトを設定し、タイムアウトも異常として扱ってください。
なお、以前の版の記事で紹介していた ``/api/v1/health`` は、15.9 の標準構成では使えません（``/api/v1`` はプラグイン ``fess-webapp-v1-api`` を入れた場合だけ提供されます）。

Docker の ``fess01`` は、この API を 2 つの仕組みで使っています。

- ``compose.yaml`` の ``healthcheck`` が 30 秒ごとに呼び、``docker compose ps`` の ``(healthy)`` 表示になります
- コンテナ内の起動スクリプトも 60 秒ごとに呼び、起動後に 200 以外が 5 回続くとコンテナを終了します。``restart: unless-stopped`` によって、コンテナは再起動されます

そのため、OpenSearch が ``RED`` のまま数分たつと ``fess01`` が再起動を繰り返します。
``fess01`` の再起動が続くときは、まず ``search01`` を確認してください。

リソースの監視：/api/admin/stats
--------------------------------

ヒープ使用率やディスク残量は、管理 API の ``GET /api/admin/stats`` で取得します。
［システム情報］>［設定情報］にはプロパティの一覧しかなく、メモリ使用量は表示されません。

管理 API には、アクセストークンが必要です。

1. ［システム］>［アクセストークン］を開き、［新規作成］をクリックします
2. 「名前」に用途（例: ``monitoring``）を、「パーミッション」に ``{role}admin-api`` を入力して［作成］をクリックします
3. 一覧から作成したトークンを開き、「トークン」の値を控えます

.. warning::

   ``{role}admin-api`` のトークンでは、設定の変更や削除を含むすべての管理 API を使えます。
   読み取り専用に絞る設定はありません。
   監視サーバーのファイルなど、管理者のパスワードと同じ扱いで保管してください。

トークンは ``Authorization`` ヘッダーで渡します。
次の例では、ヒープ使用率（%）と、ファイルシステムごとの使用率を取り出します。

::

    $ curl -fsS -H "Authorization: Bearer <トークン>" http://localhost:8080/api/admin/stats \
        | jq '{heap: .response.stats.jvm.memory.heap.percent, fs: [.response.stats.fs[] | {path, percent}]}'

ほかに、GC の回数と累積時間（``jvm.gc``）、OS の CPU 使用率とロードアベレージ（``os``）、OpenSearch のクラスター状態とシャード数（``engine``）も返ります。
項目の一覧は `Stats API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-stats.html>`__ を参照してください。

値を読むときは、次の 2 点に注意してください。

- ``jvm`` は Fess 本体（Web アプリケーション）の JVM の値です。クロールは別の JVM プロセスで動くため、クローラーのメモリ不足はここには現れません。``fess-crawler.log`` で確認します（後述）
- ``fs`` は Fess が動いているホスト（Docker ではコンテナ）のファイルシステムです。OpenSearch のデータ領域の残量は、OpenSearch に直接問い合わせます

::

    $ curl -s "http://localhost:9200/_cat/allocation?v"

ヒープの大きさを変える方法は :doc:`guide-14` を参照してください。

通知を受け取る
--------------

Fess の通知先は、［システム］>［全般］の「通知」欄にある 3 つの項目で設定します。

- 「通知メール」: 宛先のメールアドレス（複数はカンマ区切り）
- 「Slack Webhook URL」: Slack の Incoming Webhook URL
- 「Google Chat Webhook URL」: Google Chat の Webhook URL

いずれか 1 つを設定すると、次の 3 種類の通知が同じ宛先に送られます。

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 通知
     - 送られる条件
     - 追加で必要な設定
   * - クロール完了（件名 ``[FESS] Crawler completed``）
     - クロールのジョブが終わるたびに、成否にかかわらず送られます。状態（OK/FAIL）と、登録した文書数が入ります
     - なし
   * - OpenSearch の状態変化（件名 ``[FESS] Status Change``）
     - スケジューラのジョブ「Search Engine Monitor」が毎分 OpenSearch に問い合わせ、``RED`` になったときと ``RED`` から戻ったときに送られます
     - なし
   * - ログ通知（件名 ``[FESS] ERROR Log Alert``）
     - Fess とクローラーなどが出力した ERROR（または指定したレベル以上）のログを、ジョブ「Log Notification」が 5 分ごとにまとめて送ります
     - ［全般］の「ログ通知」を有効にし、「ログ通知レベル」を選ぶ

OpenSearch に接続できなくなった場合は、「Search Engine Monitor」のジョブ自体が失敗し、状態変化の通知は送られません。
接続断は、前節の ``/api/v2/health`` を外部から監視して検知してください。

ログ通知の既定のレベルは ``ERROR`` です。
失敗したスケジュールジョブは ``WARN``\ （``Failed to execute job: ...``）で記録されるため、ジョブの失敗も知りたい場合は「ログ通知レベル」を ``WARN`` にします。
その場合、ほかの ``WARN`` もすべて通知されます。

メールで受け取る場合は、SMTP サーバーを 2 つのファイルに設定し、Fess を再起動します。

::

    mail.smtp.server.main.host.and.port=smtp.example.com:587

- ``fess_env_web.properties``: ログ通知、状態変化の通知、［テストメールの送信］ボタンで使われます
- ``fess_env_crawler.properties``: クロール完了の通知で使われます（クロールは別のプロセスで動くためです）

ファイルの場所は、ZIP 版では ``app/WEB-INF/classes/``、RPM/DEB 版では ``/etc/fess/`` です。
設定後、［全般］の［テストメールの送信］で届くことを確かめます。

Docker で手早く通知を受け取りたい場合は、ファイルの編集が要らない Slack か Google Chat の Webhook が手軽です。
ただし、［全般］の設定は ``fess01`` コンテナ内の ``system.properties`` に保存されるため、``docker compose down`` でコンテナを作り直すと消えます（:doc:`guide-02` の「停止と再開」を参照）。
後述のバックアップで ``system.properties`` も取っておきます。

検索の応答時間とクロールの結果を見る
------------------------------------

外部からの監視とは別に、管理画面では次の 3 つの画面を定期的に確認します。

- ［システム情報］>［ジョブログ］: 「Default Crawler」などのジョブの状態（OK/失敗）と結果。「Search Engine Monitor」「Log Notification」のように毎分・数分ごとに動くジョブは、ここに記録されません
- ［システム情報］>［クロール情報］: セッションごとの「クローラーの状態」と「インデックスのサイズ (ウェブ/ファイル)」「インデックスのサイズ (データストア)」。前回より大きく減っていないかを見ます
- ［システム情報］>［検索ログ］の［パフォーマンス］タブ: 応答時間の中央値・p95・p99 と、応答の遅い検索語。検索ログの見方は :doc:`guide-08` を参照してください

ログを読む
==========

ログファイルの種類
------------------

Fess は処理ごとに別のファイルにログを出力します。
調べたい内容に応じて、開くファイルを選びます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ファイル
     - 内容
   * - ``fess.log``
     - Fess 本体（検索画面・管理画面・API・スケジューラ）のログ。起動の失敗、OpenSearch への接続エラー、バックアップの取り込みの失敗など
   * - ``fess-crawler.log``
     - クローラーのプロセスのログ。URL ごとの取得エラー、認証の失敗、クローラーのメモリ不足など
   * - ``audit.log``
     - ログイン・ログアウトと管理操作の監査ログ
   * - ``fess-suggest.log`` / ``fess-thumbnail.log``
     - サジェストの生成、サムネイルの生成のログ
   * - ``fess-llm.log``
     - AI 検索モード（RAG）と LLM 連携のログ
   * - ``searchlog.log``
     - 検索ごとの記録（［全般］の「検索ログ」が有効な場合）
   * - ``server_*.log``
     - Tomcat のログ

置き場所はインストール方法によって違います。

- ZIP 版: Fess を展開したディレクトリの ``logs/``
- RPM/DEB 版: ``/var/log/fess/``
- Docker: コンテナ内の ``/var/log/fess/``。``fess.log``・``fess-crawler.log``・``audit.log`` などは標準出力にも流れるので、``docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01`` で読めます。コンテナを作り直すと消えます

どのインストール方法でも、［システム情報］>［ログファイル］でファイル名をクリックするとダウンロードできます。
サーバーにログインできない担当者でも、ここからログを確かめられます。

各ログは、日付が変わるか 100 MB を超えると ``.log.gz`` に圧縮して切り替わります。
圧縮したファイルは、``fess.log`` と ``searchlog.log`` では 90 日、``audit.log`` では 360 日で自動的に削除されます。
一方、``fess-crawler.log``・``fess-suggest.log``・``fess-thumbnail.log`` などクローラーや子プロセスのログの圧縮ファイルは自動では削除されません。
ログディレクトリの容量を監視し、古いものを定期的に削除してください。

詳しく調べるとき
----------------

既定では、``fess.log`` には WARN 以上、``fess-crawler.log`` には INFO 以上が出力されます。
``fess.log`` を詳しくするには、［システム］>［全般］の「ログレベル」を ``INFO`` や ``DEBUG`` に上げます。
この変更は Fess を再起動すると元に戻ります。
クローラーのログのレベルは、ジョブのスクリプトで決まります。
「Default Crawler」のスクリプトには ``logLevel("info")`` が含まれているので、［システム］>［スケジューラ］でこれを ``logLevel("debug")`` に変えると、次のクロールから詳しいログが出ます。
調べ終わったら元に戻してください。
レベルを常に変えておく方法は `ログ設定 <https://fess.codelibs.org/ja/stable/config/admin-logging.html>`__ を参照してください。

フォーラムなどで相談するときは、［システム情報］>［メンテナンス］の「診断」にある［ログのダウンロード］が役に立ちます。
ログ、``system.properties``、``fess_config.properties``、設定インデックスの内容、OpenSearch の状態をまとめた zip がダウンロードされます。
API キーや ``app.cipher.key`` などの値は ``XXXXXXXX`` に置き換えられますが、ログ本体と設定インデックスの内容はマスクされません。
外部に渡す前に中身を確認してください。

バックアップする
================

何がどこにあるか
----------------

Fess のデータは 3 か所に分かれています。
［システム情報］>［バックアップ］で取得できるのは、このうち 1 つ目だけです。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - データ
     - 保存場所
     - バックアップの方法
   * - クロール設定、スケジューラ、ラベル、ユーザー、［全般］の設定
     - OpenSearch の設定インデックスと ``system.properties``
     - ［システム情報］>［バックアップ］、または管理 API
   * - クロールした文書、辞書（同義語・ストップワードなど）
     - OpenSearch の ``fess.*`` インデックスと ``configsync`` インデックス
     - OpenSearch のスナップショット（辞書だけならファイルのコピーも可）
   * - ``fess_config.properties``\ （``app.cipher.key`` を含む）、起動設定、導入したプラグイン
     - Fess のサーバー上のファイル
     - ファイルのコピー、または構成管理

クロールした文書は、設定さえ戻せば再クロールで作り直せます。
再クロールに時間がかかりすぎる場合に限り、スナップショットを取ります。

［バックアップ］で取得できるファイル
------------------------------------

［システム情報］>［バックアップ］には、次のファイルが並びます。
名前をクリックすると、1 ファイルずつダウンロードできます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - ``fess_basic_config.bulk``
     - クロール設定、スケジューラ、ラベル、キーマッチ、Web/ファイル認証などの設定
   * - ``fess_config.bulk``
     - 上記に加え、クロール情報、障害URL、ジョブログ、ユーザータグなど
   * - ``fess_user.bulk``
     - ユーザー、ロール、グループ
   * - ``system.properties``
     - ［システム］>［全般］の設定
   * - ``fess.json`` / ``doc.json``
     - 文書インデックスの設定とマッピング
   * - ``*.ndjson``
     - 検索ログ、クリックログ、お気に入り、AI チャットのログ、検索ユーザー。ダウンロードはできますが、アップロードして復元することはできません

設定を戻すのに使うのは、``fess_basic_config.bulk``、``fess_user.bulk``、``system.properties`` の 3 つです。
ユーザータグを使っている場合は、``fess_config.bulk`` も取得します。

``*.bulk`` には、後述の認証情報を除き、設定の値が暗号化されずに入っています。
機密ファイルとして保管してください。

cron で毎日取得する
-------------------

管理 API ``GET /api/admin/backup/file/<ファイル名>/`` で、画面と同じファイルを取得できます。
トークンは、前述の「リソースの監視」と同じ手順で作り、スクリプトを実行するユーザーだけが読めるファイルに保存します。

::

    $ sudo mkdir -p /etc/fess-backup
    $ sudo sh -c 'umask 077; echo "<トークン>" > /etc/fess-backup/token'

次のスクリプトは、日付ごとのディレクトリにファイルを保存し、30 日より古いディレクトリを削除します（保存期間は例です）。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    FESS_URL=http://localhost:8080
    FESS_TOKEN=$(cat /etc/fess-backup/token)
    BASE_DIR=/var/backups/fess
    BACKUP_DIR="${BASE_DIR}/$(date +%Y%m%d)"

    umask 077
    mkdir -p "${BACKUP_DIR}"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      curl -fsS -H "Authorization: Bearer ${FESS_TOKEN}" \
        -o "${BACKUP_DIR}/${id}" "${FESS_URL}/api/admin/backup/file/${id}/"
      test -s "${BACKUP_DIR}/${id}"
    done

    # Docker 構成の場合: 辞書ファイルもコピーする
    docker cp search01:/usr/share/opensearch/config/dictionary/. "${BACKUP_DIR}/dictionary"

    find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

ポイントは次のとおりです。

- URL の末尾の ``/`` は省略できません。ファイル名にドットが含まれるため、``/`` がないと静的ファイルへのリクエストとして扱われ、404 になります
- ``curl`` に ``-f`` を付けないと、404 やエラーの応答もファイルに保存され、スクリプトは成功したように見えます。``-f`` と ``set -e`` で、失敗したら止まるようにしています
- ZIP 版・RPM/DEB 版では、``docker cp`` の行の代わりに、OpenSearch 側の辞書ディレクトリ（Fess の ``FESS_DICTIONARY_PATH`` が指す場所）をコピーします

スクリプトを ``/usr/local/bin/fess-backup.sh`` に保存して実行権限を付け、root の crontab に登録します（毎日 2 時 30 分に実行する例です）。

::

    30 2 * * * /usr/local/bin/fess-backup.sh

登録したら一度手動で実行します。
``fess_basic_config.bulk`` を開き、``{"index":{"_index":`` で始まる行と、設定内容の JSON の行が交互に並んでいることを確かめます。
同じ処理は ``fessctl`` でも書けます（:doc:`guide-16` を参照）。

app.cipher.key を控える
-----------------------

Fess 15.9 は、ウェブ認証・ファイル認証のパスワードと、クロール設定・データストア設定のパラメーターに保存したパスワードやシークレットを、``fess_config.properties`` の ``app.cipher.key`` で暗号化して保存します。
``*.bulk`` にも暗号化されたまま入ります。
別のサーバーに復元するときは、同じ ``app.cipher.key`` を設定しておく必要があります。
鍵が違うと復号できず、``fess-crawler.log`` に ``CipherFailureException`` が記録され、その認証情報を使うクロールは失敗します。

``fess_config.properties`` は、ZIP 版では ``app/WEB-INF/classes/``、RPM/DEB 版では ``/etc/fess/`` にあります。
値を変えている場合は、このファイルも ``*.bulk`` と同じく機密として扱い、別の場所に保管してください。
Docker で値を変える場合は、``compose.yaml`` の ``FESS_JAVA_OPTS`` に ``-Dfess.config.app.cipher.key=<値>`` を指定します。
こうすると、コンテナを作り直しても同じ鍵が使われます。

.. warning::

   認証情報を保存した後で ``app.cipher.key`` を変えると、それまでに保存した値を復号できなくなります。
   変える場合は、ウェブ認証・ファイル認証やデータストアの認証情報を登録する前に変えてください。
   すでに運用している環境では、値を変えずに控えておきます。

文書インデックスのスナップショット
----------------------------------

再クロールせずに文書を戻したい場合は、OpenSearch のスナップショットを使います。
対象には ``fess*`` に加えて、辞書を保持する ``configsync`` インデックスを必ず含めます。
``configsync`` がないと、新しい OpenSearch に戻したときに辞書ファイルがなく、文書インデックスを開けません。

スナップショットを使うには、OpenSearch 側でリポジトリのパス（``path.repo``）を設定しておく必要があります。
docker-fess の ``compose-opensearch3.yaml`` には設定されていないので、使う場合は追加します。
リポジトリの登録、取得、リストアの手順は `インデックスの管理 <https://fess.codelibs.org/ja/stable/config/admin-index-backup.html>`__ にあります。
リストアは Fess を停止した状態で行い、``configsync`` を先に戻す必要があります。

復元する
========

復元の前に知っておくこと
------------------------

［バックアップ］からの復元は、OpenSearch の内容を丸ごと置き換える操作ではありません。

- 復元はアップロードでだけ行います。管理 API はダウンロード専用で、復元の API はありません
- ``*.bulk`` の各設定は、サーバー上に同じ設定がないか、サーバー上のものより新しい場合にだけ書き込まれます。バックアップの取得後に変更した設定は、古い内容に戻りません
- バックアップの取得後に作った設定は、削除されずに残ります

そのため、「誤って変えた設定を昨日の状態に戻す」用途には向きません。
新しいサーバーへの移行や、作り直した環境への復元に使います。

別のサーバーへ設定を戻す手順
----------------------------

1. 移行先に同じバージョンの Fess をインストールし、``fess_config.properties`` の ``app.cipher.key`` を移行元と同じ値にします
2. 移行元で使っていたプラグイン（データストア、SSO など）を入れ、Fess を再起動します
3. 管理画面にログインし、［システム情報］>［バックアップ］を開きます
4. 「バルクファイル」で ``fess_basic_config.bulk`` を選び、［アップロード］をクリックします。「バルク処理を開始しました。」と表示されます
5. 同じように ``fess_user.bulk`` と ``system.properties`` をアップロードします。ユーザータグを使っている場合は ``fess_config.bulk`` もアップロードします（移行元のクロール情報やジョブログも取り込まれます）

取り込みはバックグラウンドで行われます。
少し待ってから、次の点を確かめます。

- ［クローラー］>［ウェブ］・［ファイルシステム］・［データストア］と［システム］>［スケジューラ］に、移行元の設定が並んでいる
- ［ユーザー］>［ユーザー］に、移行元のユーザーが並んでいる
- ［システム］>［全般］の通知先などが、移行元の値になっている

最後に、辞書を戻し、文書を作り直します。

- 辞書: ［システム］>［辞書］で種類ごとの画面を開き、バックアップした辞書ファイルをアップロードします。その後、［システム情報］>［メンテナンス］の「ドキュメントインデックスのリロード」を実行します。リロード中は、短時間ですが検索できなくなります
- 文書: ［システム］>［スケジューラ］で「Default Crawler」の［今すぐ開始］をクリックして再クロールします。スナップショットから戻す場合は、前述の手順に従います

クロールが終わったら、［システム情報］>［クロール情報］で登録件数を確かめます。
認証付きのクロール設定で件数が 0 の場合は、``fess-crawler.log`` に ``CipherFailureException`` がないかを確認します。
ある場合は、``app.cipher.key`` が移行元と一致していません。

障害に対応する
==============

よくある症状と、Fess で確かめる場所をまとめます。

検索画面が開かない、/api/v2/health が 503 を返す
------------------------------------------------

1. OpenSearch の状態を確かめます。``curl -s "http://localhost:9200/_cluster/health?pretty"`` の ``status`` が ``red`` なら、OpenSearch 側の問題です。Docker では ``docker compose -f compose.yaml -f compose-opensearch3.yaml logs search01`` を確認します
2. OpenSearch が正常なのに Fess が応答しない場合は、``fess.log`` の起動時のエラーを確認します
3. スナップショットから戻した直後に ``red`` になる場合は、``configsync`` を戻していない可能性があります（前述）

クロールが失敗する、登録件数が減った
------------------------------------

1. ［システム情報］>［ジョブログ］で、該当ジョブの行を開き、「結果」を確認します
2. ［システム情報］>［クロール情報］で、最新のセッションの「クローラーの状態」とインデックスのサイズを前回と比べます
3. ［システム情報］>［障害URL］で、取得できなかった URL の「種別」「ログ」「エラー回数」を確認します。HTTP の 404・403・410・401 もここに記録されます
4. 詳細は ``fess-crawler.log`` にあります。障害URL の詳細にある「スレッド名」で検索すると、そのときの前後のログを追えます

``fess-crawler.log`` に ``OutOfMemoryError`` がある場合は、クローラーのプロセスのヒープが不足しています。
クローラーのヒープは ``fess_config.properties`` の ``jvm.crawler.options``\ （既定 ``-Xmx512m``）で決まり、Fess 本体のヒープとは別です。
調整方法は :doc:`guide-14` を参照してください。

通知が届かない
--------------

メールの場合は、まず［全般］の［テストメールの送信］で届くかを確かめます。
クロール完了のメールだけが届かない場合は、``fess_env_crawler.properties`` の SMTP サーバーを確認します。
Docker では、``down`` と ``up`` でコンテナを作り直したために［全般］の設定が消えていないかも確認します。
ログ通知だけが届かない場合は、「ログ通知」が有効か、「Log Notification」ジョブが有効か、「ログ通知レベル」（ジョブの失敗は ``WARN``）が適切かを確認します。
ほかの確認項目は `ログ通知 <https://fess.codelibs.org/ja/stable/config/admin-log-notification.html>`__ の「トラブルシューティング」にあります。

検索が遅い
----------

1. ［システム情報］>［検索ログ］の［パフォーマンス］タブで、遅いのが特定の検索語か、全体かを確かめます
2. ``/api/admin/stats`` の ``jvm.memory.heap.percent`` と ``jvm.gc`` の累積時間を、遅くなる前と比べます

次に読む記事
============

- 設定をスクリプトや ``fessctl`` で管理したい: :doc:`guide-16`
- ヒープの調整や、OpenSearch・Fess を複数台にしたい: :doc:`guide-14`
- SSO や監査ログなど、アクセス保護を固めたい: :doc:`guide-15`
- 検索ログから検索の品質を改善したい: :doc:`guide-08`

参考資料
========

- `Health API <https://fess.codelibs.org/ja/stable/api/api-health.html>`__
- `Stats API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-stats.html>`__
- `ログ通知 <https://fess.codelibs.org/ja/stable/config/admin-log-notification.html>`__
- `ログ設定 <https://fess.codelibs.org/ja/stable/config/admin-logging.html>`__
- `ログファイル <https://fess.codelibs.org/ja/stable/admin/log-guide.html>`__
- `バックアップ <https://fess.codelibs.org/ja/stable/admin/backup-guide.html>`__
- `Backup API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-backup.html>`__
- `インデックスの管理 <https://fess.codelibs.org/ja/stable/config/admin-index-backup.html>`__
- `障害URL <https://fess.codelibs.org/ja/stable/admin/failureurl-guide.html>`__
- `メンテナンス <https://fess.codelibs.org/ja/stable/admin/maintenance-guide.html>`__
