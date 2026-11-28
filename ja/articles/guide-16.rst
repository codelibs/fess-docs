===============================================
Fess の設定をコードで管理し、同じ環境を作り直す
===============================================

はじめに
========

管理画面で積み上げた設定は、誰がいつ何を変えたのかを後から追えません。
検証環境で確かめた設定を本番に持っていくときも、同じ画面操作を手で繰り返すことになります。

本記事では、Fess 15.9 の設定を Git リポジトリのファイルとして書き、新しく起動した Docker 環境にスクリプトで適用して、適用できたことを確かめるところまでを進めます。
使うのは、docker-fess の Compose ファイル、Fess の管理 API、その CLI である fessctl です。

バックアップの対象範囲とリストアの手順は扱いません。
:doc:`guide-10` を参照してください。

設定の置き場所ごとに管理方法を決める
====================================

Fess の設定は 1 か所にまとまっていません。
置き場所によって、コードにする方法が変わります。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 設定
     - 保存される場所
     - コードにする方法
   * - Fess の版、プラグイン
     - Docker イメージ、コンテナ
     - Compose ファイルのイメージタグと ``FESS_PLUGINS``
   * - ``fess_config.properties`` の項目（``app.cipher.key`` など）
     - コンテナ内のファイル
     - ``FESS_JAVA_OPTS`` の ``-Dfess.config.<キー>``
   * - ［システム］>［全般］の項目
     - コンテナ内の ``system.properties``
     - ``FESS_JAVA_OPTS`` の ``-Dfess.system.<キー>``
   * - クロール設定、ラベル、スケジューラ、ユーザーなど
     - OpenSearch の設定用インデックス
     - 管理 API（fessctl）
   * - 辞書（同義語など）
     - OpenSearch コンテナの ``FESS_DICTIONARY_PATH``
     - 管理 API の辞書アップロード（fessctl）
   * - アクセストークン、暗号鍵の値
     - トークンは OpenSearch、暗号鍵は起動オプション
     - Git に入れず、 ``.env`` や CI のシークレットに置く

docker-fess の ``fess01`` コンテナにはボリュームがないため、 ``system.properties`` は ``docker compose down`` でコンテナと一緒に消えます。
OpenSearch に保存されるクロール設定などはボリュームに残ります。

リポジトリの構成
================

この記事では、次のファイルを Git で管理します。

::

    fess-infra/
    ├── compose.yaml               docker-fess v15.9.0 のファイル
    ├── compose-opensearch3.yaml   docker-fess v15.9.0 のファイル
    ├── compose-site.yaml          自分の環境向けの差分
    ├── dict/
    │   └── synonym.txt            同義語辞書
    ├── apply.sh                   設定を適用するスクリプト
    ├── .gitignore
    └── .env                       Git に入れない（暗号鍵とトークン）

Docker 構成を版ごと固定する
===========================

Compose ファイルを取得する
--------------------------

docker-fess の ``v15.9.0`` タグのファイルを取得します。
``compose.yaml`` はイメージ ``ghcr.io/codelibs/fess:15.9.0`` を、 ``compose-opensearch3.yaml`` は ``ghcr.io/codelibs/fess-opensearch:3.9.0`` を指しており、版が固定されます。

::

    $ mkdir fess-infra && cd fess-infra
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose.yaml
    $ curl -LO https://raw.githubusercontent.com/codelibs/docker-fess/v15.9.0/compose/compose-opensearch3.yaml

この 2 つのファイルは編集せず、自分の環境の差分は別のファイルに書きます。
docker-fess の版を上げるときに、ファイルを取得し直すだけで済みます。

自分の環境の差分を書く
----------------------

``compose-site.yaml`` を作ります。

.. code-block:: yaml

    services:
      fess01:
        environment:
          - "FESS_PLUGINS=fess-ds-git:15.9.0"
          - "FESS_JAVA_OPTS=-Dfess.config.app.cipher.key=${FESS_CIPHER_KEY:?FESS_CIPHER_KEY is not set} -Dfess.system.purge.searchlog.day=180"

- ``FESS_PLUGINS`` には、起動時に取得するプラグインを ``名前:版`` の形式でスペース区切りで書きます。版は Fess と同じ 15.9.x にします。例の ``fess-ds-git`` は、Git リポジトリをデータストアでクロールする場合のプラグインです。取得先は ``maven.codelibs.org`` に固定されているため、ここに書けるのは公開されているプラグインだけで、コンテナからインターネットに出られる必要があります
- ``-Dfess.config.<キー>`` は ``fess_config.properties`` の同名の項目より優先されます
- ``-Dfess.system.<キー>`` は［全般］の項目の既定値になります。例の ``purge.searchlog.day`` は［全般］の「以前の検索ログを削除」の日数です

Compose は ``environment`` を変数名ごとにマージするので、 ``compose.yaml`` にある ``SEARCH_ENGINE_HTTP_URL`` などはそのまま残ります。
ただし、同じ変数を複数のファイルに書くと後のファイルの値で置き換わります。
``compose-openai.yaml`` などのオーバーレイも ``FESS_PLUGINS`` と ``FESS_JAVA_OPTS`` を設定するので、組み合わせる場合は値を 1 つのファイルにまとめてください。

.. note::

   ``-Dfess.system.<キー>`` は、 ``system.properties`` にそのキーがないときだけ使われます。
   管理画面の［全般］で一度でも保存するか ``fessctl general update`` を実行すると、画面の各項目が ``system.properties`` に書き込まれ、以後はそちらが優先されます。
   この状態で ``compose-site.yaml`` の値を変えても、 ``down`` してコンテナを作り直すまで反映されません。

暗号鍵を決める
--------------

``app.cipher.key`` は、ウェブ認証・ファイル認証のパスワードや、クロール設定・データストア設定のパラメーターに保存した秘密の値を暗号化する鍵です。
既定値の ``___change__me___`` のまま使わず、最初の起動の前に決めます。

鍵の文字列はそのまま AES の鍵として使われるため、16・24・32 バイトのいずれかにします。
``openssl rand -hex 16`` の出力（16 進数 32 文字）なら 32 バイトになります。

::

    $ printf 'FESS_CIPHER_KEY=%s\n' "$(openssl rand -hex 16)" > .env
    $ printf '.env\nbackup/\n' > .gitignore

認証情報を保存した後で鍵を変えると、保存済みの値を復号できず、その設定を使うクロールが失敗します。
バックアップを別の環境に戻すときも同じ鍵が必要です（:doc:`guide-10`）。
``.env`` とは別に、パスワード管理ツールなどにも控えておきます。

``FESS_JAVA_OPTS`` の値は ``docker inspect`` で見えます。
これを避けたい場合は、 ``fess_config.properties`` を ``/opt/fess`` にマウントする方法を使います（`Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__ の「設定ファイルの反映方法」）。

起動する
--------

Compose コマンドには毎回 3 つのファイルを指定します。

::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml -f compose-site.yaml up -d

``fess01`` のヘルスチェックは ``/api/v2/health`` を呼んでおり、 ``docker compose ... ps`` で ``fess01`` が ``(healthy)`` になれば準備完了です。

管理 API 用のアクセストークンを作る
===================================

管理 API の呼び出しにはアクセストークンが必要で、トークンを作る API もトークンなしでは呼べません。
そのため、新しい環境ごとに最初の 1 回だけ管理画面で作ります。

1. ``http://localhost:8080/admin/`` に ``admin`` / ``admin`` でログインし、求められる新しいパスワード（8 文字以上）を設定します
2. ［システム］>［アクセストークン］を開き、［新規作成］をクリックします
3. 「名前」に ``fess-infra``、「パーミッション」に ``{role}admin-api`` を入力して［作成］をクリックします
4. 一覧から作ったトークンを開き、「トークン」の値をコピーします

コピーした値を ``.env`` に追記します。

::

    $ echo 'FESS_ACCESS_TOKEN=<コピーした値>' >> .env

``{role}admin-api`` を持つトークンは、管理 API のすべての操作ができます。
設定の変更、ユーザーの作成、バックアップの取得まで含まれ、用途を絞ったトークンは作れません。
管理者パスワードと同じ扱いにし、Git やブラウザーで動く JavaScript には入れないでください。

fessctl を準備する
==================

fessctl は、管理 API を呼ぶコマンドラインツールです。
Fess 15.9 向けの既定値を持つ 0.4.0 を、版を固定してインストールします。
Python 3.13 以降が必要です。

::

    $ pipx install fessctl==0.4.0

``uv tool install fessctl==0.4.0`` でもかまいません。
以降のスクリプトでは、応答から値を取り出すために ``jq`` と ``curl`` も使います。

fessctl は、接続先を ``FESS_ENDPOINT`` （既定値 ``http://localhost:8080``）、トークンを ``FESS_ACCESS_TOKEN`` 、接続先の Fess の版を ``FESS_VERSION`` から読みます。
``FESS_VERSION`` には ``15.9.0`` を指定します。
版によって API の呼び方が変わるためです。

接続を確かめます。

::

    $ set -a; . ./.env; set +a
    $ export FESS_VERSION=15.9.0
    $ fessctl ping
    $ fessctl webconfig list

``ping`` は、クラスターの状態が GREEN か YELLOW なら終了コード 0 で終わります。
ヘルスチェックはトークンなしでも通るので、トークンが有効かどうかは ``webconfig list`` で確かめます。
認証エラーになる場合は、トークンの値とパーミッションを見直してください。
どのコマンドも ``-o json`` を付けると管理 API の応答をそのまま出力するので、 ``jq`` で値を取り出せます。

辞書の初期値を Git に入れる
---------------------------

辞書のアップロードは、ファイル全体の置き換えです。
既定の内容を消さないように、まず今の同義語辞書をダウンロードしてリポジトリに入れ、それを編集します。

::

    $ mkdir -p dict
    $ SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    $ fessctl dict synonym download "$SYNONYM_ID" --file dict/synonym.txt

ダウンロードしたファイルには、既定の同義語 ``fess,フエス`` が入っています。
その末尾に、同義語を 1 行追記します。
カンマで区切った語は、どれで検索してもほかの語を含む文書が見つかるようになります（書式は `同義語辞書 <https://fess.codelibs.org/ja/stable/admin/synonym-guide.html>`__ を参照）。

::

    テレワーク,在宅勤務

ひらがなはカタカナ、小さいカタカナは大きいカタカナ（「フェス」は「フエス」）、全角英数字は半角英数字にして登録します。

設定を適用するスクリプト
========================

``apply.sh`` には、環境に入れたい設定を fessctl のコマンドとして書きます。
新しい環境に対して流すことを前提にしていますが、同じ名前の設定があれば作成を飛ばすので、もう一度流しても重複しません。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_ENDPOINT="${FESS_ENDPOINT:-http://localhost:8080}"
    export FESS_VERSION=15.9.0

    until curl -fsS "$FESS_ENDPOINT/api/v2/health" > /dev/null; do sleep 10; done
    fessctl ping

    # ラベル: 対象とするパスに一致した文書に、クロール時に付く
    if ! fessctl labeltype list -o json | jq -e '.response.settings[] | select(.value == "fess_docs")' > /dev/null; then
      fessctl labeltype create --name "Fess ドキュメント" --value fess_docs --version-no 1 \
        --included-path 'https://fess\.codelibs\.org/ja/stable/.*' \
        --permission '{role}guest'
    fi

    # Web クロール設定
    if ! fessctl webconfig list -o json | jq -e '.response.settings[] | select(.name == "Fess 検索ガイド")' > /dev/null; then
      fessctl webconfig create --name "Fess 検索ガイド" \
        --url https://fess.codelibs.org/ja/stable/user/index.html \
        --included-url 'https://fess\.codelibs\.org/ja/stable/user/.*' \
        --depth 2 --max-access-count 50 \
        --permission '{role}guest'
    fi

    # 同義語辞書: ファイル全体を置き換え、ドキュメントインデックスを開き直して読み込ませる
    SYNONYM_ID=$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')
    fessctl dict synonym upload "$SYNONYM_ID" dict/synonym.txt --yes
    curl -fsS -X POST "localhost:9200/_configsync/flush" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_close" > /dev/null
    curl -fsS -X POST "localhost:9200/fess.update/_open" > /dev/null

    # クロールを開始し、ジョブの終了を待つ
    SCHEDULER_ID=$(fessctl scheduler list -o json | jq -er '.response.settings[] | select(.name == "Default Crawler") | .id')
    JOBLOG_ID=$(fessctl scheduler start "$SCHEDULER_ID" -o json | jq -er '.response.job_log_id')
    until fessctl joblog get "$JOBLOG_ID" -o json \
        | jq -e '.response.log.job_status == "ok" or .response.log.job_status == "fail"' > /dev/null; do
      sleep 30
    done
    fessctl joblog get "$JOBLOG_ID" -o json | jq -e '.response.log.job_status == "ok"'

スクリプトのポイントは次のとおりです。

- fessctl は、既定のテキスト出力では API がエラーを返すと 0 以外の終了コードで終わるので、 ``set -e`` で途中で止まります。 ``-o json`` では多くのコマンドがエラーの応答を出力して 0 で終わるため、取り出した値を ``jq -e`` で確かめます。値がなければ jq が失敗し、そこで止まります
- ``labeltype create`` の ``--version-no`` は fessctl 0.4.0 では必須です。新規作成では ``1`` を指定します
- ``webconfig create`` で省略した項目は fessctl の既定値になります。 ``--depth`` は ``1``、 ``--max-access-count`` は ``1000000`` なので、意図する値は省略せずに書きます。 ``--permission`` の既定値は ``{role}guest`` です
- ラベルの値は英数字と ``_`` だけが使えます。ラベルはクロール時に付くので、クロール設定より先に作ります
- 辞書のアップロードは ``--yes`` を付けないと確認を求めて止まります
- 同義語辞書は検索時に効きますが、OpenSearch がアナライザーを作るのはインデックスを開くときだけです。そのため ``_configsync/flush`` で辞書をファイルに書き出してから、 ``fess.update`` を close / open します。この間は検索できないので、運用中の環境ではアクセスの少ない時間に流します。管理画面の［システム情報］>［メンテナンス］の「ドキュメントインデックスのリロード」と同じ操作です
- ``scheduler start`` の応答の ``job_log_id`` が、そのまま［ジョブログ］の ID になります。ジョブの状態が ``ok`` か ``fail`` になるまで待ち、 ``ok`` でなければ失敗として終わります。「Default Crawler」は有効なクロール設定をすべて実行します

すでにある設定の値を変えるときは、このスクリプトは作成を飛ばすだけで、値は書き換えません。
``fessctl webconfig update <ID> --max-access-count 100`` のように ID を指定して更新するか、ボリュームごと作り直した環境に流し直します。

スクリプトを CI から流す場合は、 ``.env`` を置かずに、CI のシークレットから ``FESS_ACCESS_TOKEN`` と ``FESS_ENDPOINT`` を環境変数で渡します。
その場合、 ``localhost:9200`` の 3 行は OpenSearch に届く宛先に書き換えてください。

適用できたことを確かめる
========================

``apply.sh`` が終了コード 0 で終わったら、次の順に確認します。

1. プラグインが入っていること

   ::

       $ fessctl plugin installed

   ``fess-ds-git`` の 15.9.0 が一覧にあれば導入できています。
   ``FESS_PLUGINS`` のプラグインは取得に失敗しても Fess の起動は止まらず、 ``docker compose ... logs fess01`` に ``Failed to download`` が出るだけなので、ここで確かめます。

2. ［全般］の値が反映されていること

   ::

       $ fessctl general get -o json | jq '.response.setting.purge_search_log_day'

   ``180`` が返れば、 ``-Dfess.system.purge.searchlog.day`` が効いています。
   管理 API での名前は ``purge_search_log_day`` のような snake_case で、 ``-Dfess.system.`` に続くキーとは異なります。

3. 辞書が置き換わったこと

   ::

       $ fessctl dict synonym download "$(fessctl dict list --type synonym -o json | jq -er '.response.settings[0].id')" | grep '在宅勤務'

   追記した行が表示されれば、アップロードできています。
   ``fessctl dict synonym list`` でも確かめられますが、既定では 100 件ずつの表示なので、末尾に足した行は最初のページに出ないことがあります。

4. ラベル付きで検索できること

   ::

       $ curl -fsS --get --data-urlencode 'q=検索' --data-urlencode 'fields.label=fess_docs' \
           http://localhost:8080/api/v2/search | jq '.response.record_count'

   1 以上が返れば、クロール・ラベル付け・検索までつながっています。
   0 の場合は、管理画面の［システム情報］>［障害URL］と［ジョブログ］の結果を確認します。

管理 API を直接呼ぶ
===================

fessctl が呼んでいるのは ``/api/admin/`` の管理 API です。
クロール設定のように設定を持つリソースは、どれも次の形をしています（``<resource>`` は ``webconfig``、``fileconfig``、``dataconfig``、``labeltype``、``keymatch`` など）。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - リクエスト
     - 操作
   * - ``GET /api/admin/<resource>/settings``
     - 一覧
   * - ``GET /api/admin/<resource>/setting/<ID>``
     - 1 件の取得
   * - ``POST /api/admin/<resource>/setting``
     - 作成
   * - ``PUT /api/admin/<resource>/setting``
     - 更新
   * - ``DELETE /api/admin/<resource>/setting/<ID>``
     - 削除

fessctl にも同じ名前のサブコマンド（``create``、``list``、``get``、``update``、``delete``）があり、 ``fessctl fileconfig create --help`` のように項目を確かめられます。
辞書のアップロードは ``POST /api/admin/dict/<種別>/upload/<辞書ID>`` に multipart で送ります。
ファイルの項目名は種別ごとに異なり、同義語では ``synonymFile`` です。
JSON の項目名は ``max_access_count`` のような snake_case です。
各項目は `Admin API 概要 <https://fess.codelibs.org/ja/stable/api/admin/api-admin-overview.html>`__ からたどれるリソースごとのページを参照してください。

次のコマンドは、Web クロール設定の件数を返します。

::

    $ curl -fsS -H "Authorization: Bearer $FESS_ACCESS_TOKEN" \
        http://localhost:8080/api/admin/webconfig/settings | jq '.response.total'

``-f`` を付けないと、404 や 401 の応答でも curl が成功扱いになり、スクリプトが失敗に気づきません。

設定の控えを取得する
====================

Git に書いていない設定（管理画面で直接変えたものなど）に備えて、バックアップも定期的に取得します。
対象のファイルと、リストアの手順は :doc:`guide-10` で説明しています。
ここでは、 ``apply.sh`` と同じ準備で動くスクリプトの例だけを示します。

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail
    cd "$(dirname "$0")"
    if [ -f .env ]; then set -a; . ./.env; set +a; fi
    export FESS_VERSION=15.9.0
    dest="backup/$(date +%Y%m%d)"
    umask 077
    mkdir -p "$dest"
    for id in fess_basic_config.bulk fess_config.bulk fess_user.bulk system.properties fess.json doc.json; do
      fessctl backup download "$id" --dest "$dest/$id" --force
    done

``fessctl backup download`` は、ID にドットを含むときに必要な URL 末尾の ``/`` を付けて ``/api/admin/backup/file/<ID>/`` を呼びます。
curl で呼ぶ場合は、末尾の ``/`` と ``-f`` を忘れないでください。
末尾の ``/`` がないと 404 になります。

管理 API でできるのはダウンロードまでで、リストアは管理画面の［システム情報］>［バックアップ］からしか行えません。
バックアップで別の環境を作り直す手順にはならないので、設定の正本は ``apply.sh`` 側に置きます。

Git に入れてはいけないもの
==========================

- ``.env`` （暗号鍵とアクセストークン）
- バックアップのファイル。 ``*.bulk`` には暗号化されていない値も含まれ、機密ファイルとして扱う必要があります。 ``system.properties`` にも、［全般］で入力したストレージの秘密鍵や SSO のクライアントシークレットなどが入ります

``.gitignore`` に ``.env`` と ``backup/`` を入れたのはこのためです。
バックアップは、暗号化したストレージなど、アクセスを絞った場所に保管します。

次に読む記事
============

- バックアップの対象とリストア、監視を整えたい: :doc:`guide-10`
- Docker での起動と停止の基本を確かめたい: :doc:`guide-02`
- 業務システムから検索 API を呼びたい: :doc:`guide-11`
- アクセストークンの扱いや SSO を含めて管理画面を守りたい: :doc:`guide-15`
- 自分でプラグインを作りたい: :doc:`guide-17`

参考資料
========

- `Docker でのインストール (詳細) <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__
- `Admin API 概要 <https://fess.codelibs.org/ja/stable/api/admin/api-admin-overview.html>`__
- `辞書 API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-dict.html>`__
- `Backup API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-backup.html>`__
- `辞書（反映のタイミング） <https://fess.codelibs.org/ja/stable/admin/dict-guide.html>`__
- `アクセストークン <https://fess.codelibs.org/ja/stable/admin/accesstoken-guide.html>`__
- `fessctl（GitHub） <https://github.com/codelibs/fessctl>`__
- `docker-fess（GitHub） <https://github.com/codelibs/docker-fess>`__
