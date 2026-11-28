==================================================
Google Drive・SharePoint・Box のファイルを検索する
==================================================

はじめに
========

部門ごとに Google Drive、SharePoint Online、Box を使い分けていると、「あの資料はどこに置いたか」を探す時間が増えます。
Fess のデータストアプラグインを使うと、3 つのサービスのファイルを 1 つの検索画面から探せるようになります。

ただし、クラウドストレージには閲覧権限の違うファイルが混在しています。
設定を誤ると、契約書のような機密ファイルがログインしていない利用者の検索結果にも出てしまいます。
この記事では、サービスごとに「そのまま写して動く最小構成」と、元の権限を Fess に持ち込む方法を説明します。

プラグインのインストール、ハンドラー名・パラメーター・スクリプトの書き方、ジョブの作り方といったデータストア共通の手順は :doc:`datastore-basics` にまとめています。
先にそちらを読んでから進めてください。
記事中の設定値は Fess 15.9 と、15.9.0 版の各プラグインに合わせています。

この記事で作る構成
==================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - サービス
     - プラグイン
     - ハンドラー名
     - サービス側で用意するもの
   * - Google Drive
     - ``fess-ds-gsuite``
     - ``GoogleDriveDataStore``
     - サービスアカウントの JSON キーと、ドメイン全体の委任
   * - SharePoint Online
     - ``fess-ds-microsoft365``
     - ``OneDriveDataStore``
     - Entra ID のアプリ登録（クライアントシークレット）と、Microsoft Graph のアプリケーション権限
   * - Box
     - ``fess-ds-box``
     - ``BoxDataStore``
     - JWT 認証の Box カスタムアプリ

Docker で動かしている場合は、環境変数 ``FESS_PLUGINS`` にプラグイン名とバージョンを空白区切りで並べると、起動時にまとめて導入できます。

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-gsuite:15.9.0 fess-ds-microsoft365:15.9.0 fess-ds-box:15.9.0

管理画面や ``fess-setup`` で入れた場合は、インストール後に Fess の再起動が必要です（\ ``FESS_PLUGINS`` は Fess の起動前にインストールするため、再起動は不要です）。

先に決めること：検索結果を誰に見せるか
======================================

データストア設定を新規作成すると、「パーミッション」欄には最初から ``{role}guest`` が入っています。
この値が残っていると、取り込んだファイルはログインしていない利用者にも検索されます。
3 つのプラグインとも、元の共有設定から作ったロールを ``file.roles`` に入れます。
そのため、設定方法は 3 つとも次の 2 点で共通です。

- 「パーミッション」欄の ``{role}guest`` を消して空にする
- スクリプトに ``role=file.roles`` を書く

この 2 点が必要な理由は、プラグインによって「パーミッション」欄の扱いが違うからです。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - プラグイン
     - 「パーミッション」欄の値
     - ``default_permissions`` パラメーター
   * - Google Drive
     - ``role=file.roles`` を書くと使われない。書かないと欄の値（初期値は ``{role}guest``\ ）がそのまま全ファイルに付く
     - Drive の ACL から何も得られなかったファイルにだけ使う。それも未設定なら、そのファイルは取り込まない
   * - SharePoint（OneDriveDataStore）
     - ``file.roles`` に合流する。\ ``{role}guest`` を残すと全ファイルが公開になる
     - 全ファイルに追加する
   * - Box
     - ``file.roles`` に合流する。\ ``{role}guest`` を残すと全ファイルが公開になる
     - 全ファイルに追加する

``file.roles`` に入るのは、各サービスの利用者やグループを表す文字列です。

- Google Drive: ユーザーとグループはメールアドレス、ファイルのオーナーも同じ形式です。ドメイン共有は ``{group}<ドメイン名>``\ （\ ``domain_permission_format`` で変更可）、検索で見つけられる一般公開（\ ``anyone``\ ）は ``guest`` ロールになります。リンクを知っている人だけに共有した設定はロールになりません。
- SharePoint: ユーザーはオブジェクト ID と UPN、グループは ID と表示名です。「組織内の全員」向けの共有リンクはグループ ``EVERYONE_IN_TENANT`` になります。
- Box: ユーザーは Box のユーザー ID とログイン（メールアドレス）、グループは Box のグループ ID です。ファイル自身のコラボレーションに加え、上位フォルダーのコラボレーションとオーナーも含みます。

検索時にこれらと照合されるのは、Fess にログインした利用者のユーザー名とグループ名です。
たとえば Google Drive のユーザー権限を効かせるには、Fess のユーザー名がメールアドレスと一致している必要があります。
ロールの考え方は :doc:`guide-05`\ 、SSO によるログインは :doc:`guide-15` を参照してください。

サービスごとに検索結果を絞り込めるようにするラベルは、データストア設定に専用の欄がありません。
スクリプトに ``label="box"`` のような行を足すか、URL に一致するラベルを作ります（詳しくは :doc:`datastore-basics`\ ）。
ラベルの値に使えるのは英数字と ``_`` だけで、\ ``google-drive`` のようにハイフンを含む値は作れません。

Google Drive：共有ドライブを取り込む
====================================

Google 側の準備
---------------

15.9 の ``fess-ds-gsuite`` は、既定で ``crawl_target=shared_drives`` として動きます。
ドメイン内のすべての共有ドライブを、ドメイン管理者になりすまして読み取る方式です。

1. Google Cloud コンソールでプロジェクトを作り、Google Drive API を有効にする
2. サービスアカウントを作成し、［キー］タブで JSON 形式の鍵を作ってダウンロードする
3. サービスアカウントで「ドメイン全体の委任」を有効にし、OAuth 2 クライアント ID を控える
4. Google Workspace 管理コンソールの［セキュリティ］>［アクセスとデータ管理］>［API の制御］>［ドメイン全体の委任］で、そのクライアント ID にスコープ ``https://www.googleapis.com/auth/drive.readonly`` を許可する

``impersonate_user`` に指定するアカウントは、Google Workspace のドメイン管理者である必要があります。
``crawl_target`` が ``legacy`` 以外で ``impersonate_user`` がないと、クロール開始時にエラーで止まります。

パラメーターとスクリプト
------------------------

［クローラー］>［データストア］>［新規作成］で、「ハンドラー名」に ``GoogleDriveDataStore`` を選び、「パーミッション」欄を空にします。
``private_key``\ 、\ ``private_key_id``\ 、\ ``client_email`` には、JSON キーの同名の値を写します。
``private_key`` の改行は ``\n`` のまま 1 行で書きます。

.. code-block:: properties

    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    private_key_id=46812a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r
    client_email=fess-crawler@your-project.iam.gserviceaccount.com
    impersonate_user=admin@example.com
    crawl_target=shared_drives
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_time
    last_modified=file.modified_time
    role=file.roles

``file.url`` はファイルの ``webViewLink`` です。
削除の反映は、インデックスされた URL に Drive のファイル ID が含まれていることを前提にしています。
そのため、\ ``url`` は書き換えずにこのまま使います。

ほかの取り込み範囲は次のとおりです。

- ``crawl_target=users``\ ：全ユーザーのマイドライブを読みます。Admin SDK API の有効化と、スコープ ``https://www.googleapis.com/auth/admin.directory.user.readonly`` の追加（委任の設定と ``scopes`` パラメーターの両方）が必要です。
- ``crawl_target=legacy``\ ：サービスアカウントのアドレスに直接共有されたファイルだけを読みます。委任と ``impersonate_user`` は不要です。

差分クロール
------------

``incremental=true`` を加えると、2 回目以降は Drive の変更フィードだけを読みます。
このとき ``delete_old_docs`` は強制的に ``false`` になり、Drive から消えたファイルがインデックスに残ることがあります。
また、変更のないファイルは登録し直されないため、そのままでは「以前のドキュメントを削除」の日数（初期値 3 日）が過ぎると検索結果から消えます（\ :doc:`datastore-basics` の「文書の有効期限」）。

差分クロールを使う場合は、次の組み合わせにします。

- ``incremental`` を付けない全件クロール用の設定も作り、週 1 回など定期的に実行する
- 両方の設定に、全件クロールの間隔より少し長い ``time_to_live`` を指定する（週 1 回の全件クロールなら ``time_to_live=11520``\ 、8 日）

Drive から消えたファイルは、この期限が切れた時点で検索結果から消えます。
変更フィードの位置はプラグインが「パラメーター」欄に書き戻すので、書き戻された値は編集しないでください。

SharePoint Online：ドキュメントライブラリのファイルを取り込む
=============================================================

どのハンドラーを使うか
----------------------

SharePoint のドキュメントライブラリにあるファイルの本文を検索するには、\ ``fess-ds-microsoft365`` の ``OneDriveDataStore`` を使います。

- ``SharePointDocLibDataStore`` は、ライブラリ 1 つを 1 件として登録するだけで、中のファイルは取り込みません。
- ``fess-ds-sharepoint``\ （\ ``SharePointDataStore``\ ）はオンプレミスの SharePoint Server 向けです。Microsoft Graph には対応しておらず、SharePoint Online には ``fess-ds-microsoft365`` を使うよう案内されています。

Entra ID 側の準備
-----------------

1. Azure Portal の［アプリの登録］で新規登録する
2. ［証明書とシークレット］で新しいクライアントシークレットを作り、値を控える（有効期限はここで決めます）
3. ［API のアクセス許可］>［Microsoft Graph］>［アプリケーションの許可］で、下の 4 つを追加する
4. ［管理者の同意を与えます］を実行する

追加するアプリケーション権限は次のとおりです。

- ``Files.Read.All``
- ``User.Read.All``\ 、\ ``Group.Read.All``\ ：ACL のユーザー名・グループ名を引くために、どの取り込み範囲でも必要
- ``Sites.Read.All``\ ：\ ``shared_documents_drive_crawler=true`` でサイトを列挙するために必要

パラメーターとスクリプト
------------------------

``OneDriveDataStore`` は、何も指定しないと SharePoint の全サイトに加えて、全ユーザーの OneDrive と全 Microsoft 365 グループのドライブも読みます。
SharePoint だけを対象にするには、3 つのフラグを明示します。

.. code-block:: properties

    tenant=12345678-1234-1234-1234-123456789abc
    client_id=87654321-4321-4321-4321-123456789abc
    client_secret=your-client-secret
    shared_documents_drive_crawler=true
    user_drive_crawler=false
    group_drive_crawler=false
    script_type=javascript

.. code-block:: properties

    url=file.web_url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created
    last_modified=file.last_modified
    role=file.roles

特定のライブラリだけに絞りたい場合は、3 つのフラグをすべて ``false`` にして ``drive_id`` にドライブ ID を指定します。
ドライブ ID は Microsoft Graph の ``GET /sites/{site-id}/drives`` で確認できます。
``drive_id`` だけを指定してフラグを残すと、そのドライブは全体の取り込みに「追加」されるだけです。

権限の取りこぼしとリトライ
--------------------------

ファイルの ACL は、ファイルごとの Graph 呼び出しで取得します。
この呼び出しが失敗したときの扱いは ``permission_failure_policy`` で決まります。
既定の ``skip`` では、そのファイルを登録せず、［システム情報］>［障害URL］と WARN ログに記録します。
``index_without_acl`` に変えると ACL が不完全なまま登録されるため、機密性の高いライブラリでは既定のままにしておくのが安全です。

Graph 呼び出しの再試行は ``max_retry_count``\ （既定 3、上限 10）と ``retry_interval``\ （秒、既定 3、上限 180）で調整できます。
``OneDriveDataStore`` には差分クロールのオプションはなく、毎回全件を読みます。

Box：契約書フォルダーを権限付きで取り込む
=========================================

Box 側の準備
------------

``fess-ds-box`` は JWT によるサーバー認証だけに対応しています。

1. Box Developer Console で「Custom App」を作り、認証方法に「Server Authentication (with JWT)」を選ぶ
2. ［Configuration］タブの Application Scopes で「Read all files and folders stored in Box」を有効にする
3. App Access Level に「App + Enterprise Access」を選ぶ
4. ［Generate a Public/Private Keypair］で鍵ペアを作り、JSON ファイルを保存する
5. Box 管理コンソールでアプリを承認する

JSON ファイルの ``clientID``\ 、\ ``clientSecret``\ 、\ ``publicKeyID``\ 、\ ``privateKey``\ 、\ ``passphrase``\ 、\ ``enterpriseID`` が、それぞれ ``client_id``\ 、\ ``client_secret``\ 、\ ``public_key_id``\ 、\ ``private_key``\ 、\ ``passphrase``\ 、\ ``enterprise_id`` に対応します。
6 つすべてが必須です。

対象フォルダーを 1 つに絞る
---------------------------

法務部の契約書のように対象が決まっている場合は、\ ``root_folder_id`` でフォルダーを 1 つだけ読みます。
このモードでは利用者へのなりすましを行わず、アプリのサービスアカウントとしてフォルダーを読みます。
そのため、サービスアカウントを対象フォルダーのコラボレーターに追加しておく必要があります。
フォルダー ID は、Box の Web 画面でフォルダーを開いたときの URL の末尾にある数字です。

.. code-block:: properties

    client_id=hdf8a7sd9f8a7sdf9a87sdf98a7sd
    client_secret=kMN7sd8f7a9sd8f7a9sd8f7a9sd8f
    public_key_id=4tg5h6j7
    private_key=-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFDj...\n-----END ENCRYPTED PRIVATE KEY-----\n
    passphrase=7ba8sd9f7a9sd8f7a9sd8f7a9sd8f
    enterprise_id=1923456
    root_folder_id=123456789
    default_permissions={group}legal
    script_type=javascript

.. code-block:: properties

    url=file.url
    title=file.name
    content=file.contents
    mimetype=file.mimetype
    filetype=file.filetype
    content_length=file.size
    created=file.created_at
    last_modified=file.modified_at
    role=file.roles

「パーミッション」欄の ``{role}guest`` は必ず消してください。
Box では欄の値が ``file.roles`` に合流するため、残すと契約書がログインしていない利用者にも検索されます。

Box のグループはグループ ID としてロールになるため、Fess 側のグループ名とはそのままでは一致しません。
この例では ``default_permissions={group}legal`` で、Fess の ``legal`` グループに全ファイルを見せています。
Box で個別に共有された利用者は、ログイン（メールアドレス）が Fess のユーザー名と一致すれば、それに加えて検索できます。
社内全体向けの共有リンクが付いたファイルにロールを足したい場合は、\ ``company_shared_link_role`` を使います。

全ユーザーのファイルを読む場合
------------------------------

``root_folder_id`` を省くと、エンタープライズの全ユーザーを列挙し、1 人ずつなりすましてファイルを読みます。
対象のユーザーは ``filter_term`` で絞り込めます。
なりすましでの API 呼び出しが Box 側のアプリ設定で許可されている必要があるため、Box の開発者向けドキュメントで設定を確認してください。

レート制限への対応
------------------

``429`` と ``5xx`` 応答の再試行回数は ``max_retry_attempts``\ （既定 5）です。
``max_retry_count``\ （既定 10）は ``401`` 応答で接続を作り直す回数で、レート制限とは関係しません。
API の呼び出しを間引きたいときは、\ ``readInterval``\ （ミリ秒）で 1 件ごとの待ち時間を入れます。
``fess-ds-box`` には差分クロールのオプションはありません。

運用で押さえておくこと
======================

認証情報の期限
--------------

- Entra ID のクライアントシークレットには、作成時に決めた有効期限があります。期限が切れると認証エラーになり取り込めなくなるので、期限前に新しいシークレットを作ってパラメーターの ``client_secret`` を差し替えます。
- Google のアクセストークンは、プラグインが使うライブラリによって自動で更新されます。15.9 では ``refresh_token_interval`` は無視され、警告がログに出ます。
- Box のアクセストークンは ``refresh_token_interval``\ （既定 3540 秒）ごとに自動で更新されます。

取り込みきれない場合
--------------------

3 つのプラグインとも、クロールの最後に作業スレッドの終了を既定で 60 秒待ち、終わらなかった分は取り込まれません。
大きなテナントで件数が足りないときは、待ち時間を延ばしてください。
パラメーター名は Google Drive が ``thread_pool_timeout_seconds``\ 、SharePoint が ``executor_shutdown_timeout``\ 、Box が ``thread_pool_await_timeout`` です（いずれも秒）。

Google Drive では、429、500、502、503、504 の応答とレート制限による 403 が、指数バックオフで再試行されます。
再試行は ``max_retries``\ （既定 5）、\ ``retry_initial_interval_ms``\ （既定 1000）、\ ``max_backoff_ms``\ （既定 32000）で調整できます。

動作を確認する
==============

ジョブの結果やログの見方は :doc:`datastore-basics` で説明しています。
データストアのクロールはファイルの取得に失敗してもジョブが「OK」と表示されることがあるため、件数とログで判断してください。
この記事の構成では、さらに次の 3 点を確かめます。

1. ログアウトした状態で、取り込んだファイルに含まれる語を検索し、1 件も出ないことを確認する（「パーミッション」欄の消し忘れがないか）
2. 共有されている利用者でログインすると、同じファイルが出ることを確認する
3. Google Drive の設定では、\ ``fess-crawler.log`` に ``Skipped ... because no permission could be resolved`` が出ていないか確認する（ACL が空で取り込まれなかったファイルです）

2 で出ない場合は、利用者のユーザー名やグループ名が ``file.roles`` の値と一致しているかを見直します。

まとめ
======

- SharePoint のファイル本文は ``OneDriveDataStore`` で取り込み、不要なら OneDrive とグループのドライブを ``false`` にします。
- 3 サービスとも「パーミッション」欄の ``{role}guest`` を消し、スクリプトに ``role=file.roles`` を書きます。
- ``default_permissions`` は、Google Drive では空の ACL の代わり、SharePoint と Box では全ファイルへの追加です。
- 差分クロールがあるのは Google Drive（\ ``incremental=true``\ ）だけです。使う場合は全件クロール用の設定と組み合わせ、両方に ``time_to_live`` を指定します。

参考資料
========

- `Google Workspace コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-gsuite.html>`__
- `Microsoft 365 コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-microsoft365.html>`__
- `Box コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-box.html>`__
- `データストア設定 <https://fess.codelibs.org/ja/stable/admin/dataconfig-guide.html>`__
- `fess-ds-microsoft365 15.9.0 README（Graph 権限の一覧） <https://github.com/codelibs/fess-ds-microsoft365/blob/fess-ds-microsoft365-15.9.0/README.md>`__
- `fess-ds-box 15.9.0 README（file.roles と root_folder_id） <https://github.com/codelibs/fess-ds-box/blob/fess-ds-box-15.9.0/README.md>`__
