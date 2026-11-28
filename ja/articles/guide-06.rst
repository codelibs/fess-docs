====================================================
開発チームの Git・Confluence・Jira・Slack を検索する
====================================================

はじめに
========

開発チームの情報は、コードと README なら Git、設計書なら Confluence、課題なら Jira、議論なら Slack と、ツールごとに分かれています。
「あの仕様はどこで決まったか」を探すたびに 4 つのツールを順に検索するのは手間です。
Fess のデータストアプラグインを使うと、4 つのツールの情報を 1 つの検索画面から探せるようになります。

ただし、設定を誤ると次のような状態になります。

- Git のファイルがすべて URL 空で登録され、検索結果から元のファイルを開けない
- Slack のメッセージがすべてタイトル空で表示される
- プライベートチャンネルの発言が、ログインしていない利用者の検索結果にも出る
- Git のファイルが、数日後にインデックスから消える

この記事では、ツールごとに「そのまま写して動く最小構成」を示し、それぞれの設定で上の落とし穴をどう避けるかを説明します。
プラグインのインストール、ハンドラー名・パラメーター・スクリプトの書き方、ジョブの作り方といったデータストア共通の手順は :doc:`datastore-basics` にまとめています。
先にそちらを読んでから進めてください。
記事中の設定値は Fess 15.9 と、15.9.0 版の各プラグインに合わせています。

この記事で作る構成
==================

.. list-table::
   :header-rows: 1
   :widths: 14 20 26 40

   * - ツール
     - プラグイン
     - ハンドラー名
     - ツール側で用意するもの
   * - Git
     - ``fess-ds-git``
     - ``GitDataStore``
     - 読み取り権限のあるアクセストークン（HTTPS で clone できること）
   * - Confluence / Jira
     - ``fess-ds-atlassian``
     - ``ConfluenceDataStore`` / ``JiraDataStore``
     - クロール用アカウントの API トークン
   * - Slack
     - ``fess-ds-slack``
     - ``SlackDataStore``
     - Slack App の Bot User OAuth Token（``xoxb-``）

Docker で動かしている場合は、環境変数 ``FESS_PLUGINS`` にプラグイン名とバージョンを空白区切りで並べると、起動時にまとめて導入できます。

.. code-block:: yaml

    environment:
      - FESS_PLUGINS=fess-ds-git:15.9.0 fess-ds-atlassian:15.9.0 fess-ds-slack:15.9.0

管理画面や ``fess-setup`` で入れた場合は、インストール後に Fess を再起動します。

先に決めること：検索結果を誰に見せるか
======================================

データストア設定を新規作成すると、「パーミッション」欄には最初から ``{role}guest`` が入っています。
このままでは、取り込んだ情報はログインしていない利用者にも検索されます。

Git、Confluence、Jira のプラグインは、元のツールのアクセス権を Fess に持ち込みません。
クロールに使うアカウントが読めるものはすべて取り込まれ、「パーミッション」欄に書いたロールやグループを持つ人に見えます。
そのため、次の 2 点を組み合わせて範囲を決めます。

- 「パーミッション」欄の ``{role}guest`` を、見せたい相手（例: ``{group}developers``\ ）に書き換える
- クロール用アカウントの権限や、後で説明する ``jira.jql`` と ``include_pattern`` で、取り込む範囲をその相手に見せてよいものに絞る

Slack のプラグインだけは、プライベートチャンネルのメンバーを権限として取り込めます（後述）。
グループやロールの考え方は :doc:`guide-05` を参照してください。

Git リポジトリ
==============

準備
----

``fess-ds-git`` は HTTPS で clone します。
SSH の URI（``git@...`` 形式）には対応していません。
プライベートリポジトリの場合は、読み取り用のアクセストークンを作ります。
GitHub の classic トークンなら ``repo`` スコープ、GitLab なら ``read_repository`` スコープです。

パラメーターとスクリプト
------------------------

［クローラー］>［データストア］>［新規作成］で、「ハンドラー名」に ``GitDataStore`` を選びます。

.. code-block:: properties

    script_type=javascript
    uri=https://github.com/example/dev-platform.git
    username=fess-crawler
    password=ghp_xxxxxxxxxxxxxxxxxxxx
    base_url=https://github.com/example/dev-platform/blob/main/
    include_pattern=.*\.(md|rst|txt|java|py|ts|yml|yaml)$
    time_to_live=5256000

.. code-block:: properties

    url=url
    title=path
    content=content
    mimetype=mimetype
    content_length=contentLength
    last_modified=timestamp
    label="code"

各行の意味は次のとおりです。

- ``base_url``\ ：スクリプトの ``url`` は、\ ``base_url`` とリポジトリ内のパスをそのまま連結した値です。省略すると ``url`` が空文字列になり、全ファイルが同じ文書 ID になって上書きし合います。末尾は ``/`` で終え、ブランチ名はクロールするブランチ（既定はリモートの既定ブランチ、変えるときは ``commit_id``\ ）と合わせます。
- ``username`` / ``password``\ ：両方を指定したときだけ認証に使われます。トークンは ``uri`` に埋め込まず、\ ``password`` に書きます（\ ``password`` は保存時に暗号化されますが、\ ``uri`` はされません）。
- ``include_pattern``\ ：リポジトリ内のパス（例: ``docs/setup.md``\ ）全体に一致する正規表現です。URL ではありません。
- ``title=path``\ ：ファイル名だけの ``name`` にすると、\ ``README.md`` のような同名ファイルを検索結果で区別できないため、パスを使います。

差分クロールと有効期限
----------------------

``fess-ds-git`` は、クロールが成功すると、そのコミット ID を「パラメーター」欄の ``prev_commit_id`` に書き戻します。
2 回目以降は、前回のコミットとの差分にあるファイルだけを登録し、削除・リネームされたファイルの文書を消します（削除の反映には ``base_url`` が必要です）。

この差分クロールは、Fess の文書の有効期限と相性が悪いため、上の例では ``time_to_live`` を指定しています。
データストアの文書には、登録時に有効期限が付きます。
既定では［システム］>［全般］の「以前のドキュメントを削除」（既定 3 日）で決まり、期限を過ぎた文書は毎分動くジョブ「Doc Purger」が削除します。
差分クロールでは変更のないファイルが登録し直されないため、有効期限が延びず、最初のクロールから数日で消えてしまいます。
``time_to_live`` はこの設定の文書の有効期限を分単位で指定するパラメーターで、\ ``5256000`` は約 10 年です。

このため、スクリプト、\ ``base_url``\ 、\ ``include_pattern``\ 、「パーミッション」欄を変えても、変更のないファイルには反映されません。
全ファイルを登録し直すには、次の手順を踏みます。

1. ［システム情報］>［検索］で ``label:code`` を検索し、［このクエリですべてを削除］で古い文書を消す
2. 「パラメーター」欄の ``prev_commit_id=`` の値を消して保存する
3. ジョブを実行する

「パーミッション」欄や ``base_url`` を変えた場合は、文書 ID が変わるため、手順 1 を省くと古い文書が残ります。
このデータストア設定を削除するときも、先に手順 1 で文書を消してください。

Confluence
==========

Atlassian Cloud では、クロール用のアカウントで API トークンを作り、Basic 認証のパスワードとして使います。
取り込まれるのは、このアカウントが閲覧できるスペースのページとブログ投稿です。
「ハンドラー名」に ``ConfluenceDataStore`` を選びます。

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    include_pattern=https://example\.atlassian\.net/wiki/spaces/(DEV|OPS)/.*

.. code-block:: properties

    url=content.view_url
    title=content.title
    content=content.body + content.comments
    last_modified=content.last_modified
    label="docs"

- ``home`` は ``/wiki`` を付けても付けなくても動きます。Cloud では、Confluence 用に ``/wiki`` が補われます。
- ``deployment`` は、省略するとホスト名が ``.atlassian.net`` で終わる場合に ``cloud``\ 、それ以外は ``datacenter`` とみなされます。
- ``content.comments`` を足すと、ページのコメントも本文として検索できます。各コメントは空行で区切られて連結されています。
- ``include_pattern`` は文書の URL 全体との一致で判定されます。Cloud のページの URL は ``https://<サイト>/wiki/spaces/<スペースキー>/pages/<ページID>`` なので、スペースキーで絞り込めます。Data Center の URL（``/pages/viewpage.action?pageId=...``\ ）にはスペースキーが含まれないため、この方法は使えません。

Data Center では ``deployment=datacenter`` とし、個人用アクセストークンを使う場合は ``auth_type=pat`` と ``pat.token`` を指定します。

Jira
====

認証は Confluence と同じです。
「ハンドラー名」に ``JiraDataStore`` を選び、取り込む課題を JQL で絞ります。

.. code-block:: properties

    script_type=javascript
    home=https://example.atlassian.net
    deployment=cloud
    auth_type=basic
    basic.username=fess-crawler@example.com
    basic.password=your-api-token
    jira.jql=project in (DEV, OPS)

.. code-block:: properties

    url=issue.view_url
    title=issue.summary
    content=issue.description + issue.comments
    last_modified=issue.last_modified
    label="tickets"

JQL のパラメーター名は ``jira.jql`` です。
古い名前の ``issue.jql`` もまだ動きますが、ログに ``Parameter "issue.jql" is deprecated`` という警告が出ます。
古い名前は 16.0 で削除される予定です。
``jira.jql`` を省略すると ``created is not empty``\ 、つまりアカウントが閲覧できるすべての課題が対象になります。

``issue.comments`` を足すと、課題のコメントも空行区切りで本文に入り、検索できます。
コメントは課題ごとに API で取得するため、呼び出し回数が増えます（後述のレート制限を参照）。

Slack
=====

Slack App の準備
----------------

https://api.slack.com/apps で App を作り、［OAuth & Permissions］の Bot Token Scopes に次のスコープを追加してワークスペースにインストールします。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - スコープ
     - 必要な場合
   * - ``channels:read``\ 、\ ``channels:history``\ 、\ ``users:read``\ 、\ ``team:read``
     - 常に必要
   * - ``groups:read``\ 、\ ``groups:history``
     - プライベートチャンネルを取り込む（\ ``include_private=true``\ ）
   * - ``users:read.email``
     - プライベートチャンネルのメンバーを権限にする（\ ``permission_sync=true``\ ）
   * - ``files:read``
     - ファイルも取り込む（\ ``file_crawl=true``\ ）

``team:read`` がないと、メッセージごとに ``chat.getPermalink`` を呼ぶようになり、API 呼び出しが大幅に増えます。
インストール後、取り込むチャンネルそれぞれに App を追加します。
App が参加していないチャンネルは、警告が出て読み飛ばされます。

公開チャンネルとプライベートチャンネルは、データストア設定を分けて 2 つ作ります。
理由は「プライベートチャンネル」の節で説明します。

公開チャンネル
--------------

「ハンドラー名」に ``SlackDataStore`` を選び、「パーミッション」欄は公開チャンネルを見せたい相手にします。

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=*all
    include_private=false

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    label="slack"

``message.title`` はメッセージでは常に空文字列なので、\ ``title=message.title`` と書くとすべての結果がタイトルなしになります。
上の例のように、投稿者とチャンネル名からタイトルを作ります。
スレッドの返信も 1 件ずつの文書として登録されます。
``channel_join`` などのシステムメッセージは、既定（\ ``ignore_system_events=true``\ ）で除外されます。

プライベートチャンネル
----------------------

``permission_sync=true`` を指定すると、プライベートチャンネルのメンバーのメールアドレスから、メンバーごとのユーザーロールを作って ``message.roles`` に入れます。
ただし、この値には ``default_permissions`` と「パーミッション」欄の値も加えられます。
公開チャンネルは自前のロールを持たないため、この 2 つが空だと、公開チャンネルの文書は誰にも見えなくなります。
逆に 2 つのどちらかに公開チャンネル向けの相手を書くと、その相手にプライベートチャンネルの文書も見えてしまいます。
1 つの設定で両方を正しく扱えないため、プライベートチャンネルは別の設定にします。

2 つ目のデータストア設定では、「パーミッション」欄の ``{role}guest`` を消して空にし、取り込むプライベートチャンネルの名前を ``channels`` に並べます。

.. code-block:: properties

    script_type=javascript
    token=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
    channels=dev-security,dev-incident
    include_private=true
    permission_sync=true

.. code-block:: properties

    url=message.permalink
    title=message.user + " #" + message.channel
    content=message.text
    created=message.timestamp
    last_modified=message.timestamp
    role=message.roles
    label="slack"

- ``role=message.roles`` を書かないと、計算したロールは使われません。このときクロール開始時に ``no script value references message.roles`` という警告が出ます。
- ``channels`` に公開チャンネルを混ぜると、その文書はロールが空になり誰にも見えません。
- この設定では、クロール開始時に ``default_permissions is not set and this crawl's DataConfig permission field is empty`` という警告が出ます。公開チャンネルを含めていなければ問題ありません。
- メンバーを取得できなかったチャンネルや、メールアドレスを 1 件も解決できなかったチャンネル（\ ``users:read.email`` の付け忘れなど）は、そのクロールでは取り込まれません。\ ［システム情報］>［障害URL］に、チャンネル ID とチャンネル名で記録されます。

検索時には、Fess にログインした利用者のユーザー名が、このメールアドレスと照合されます。
そのため、Fess のユーザー名が Slack のメールアドレスと一致している必要があります。
Slack はメールアドレスを小文字で扱うので、Fess のユーザー名も小文字にします。
一致しない利用者には、プライベートチャンネルの文書が表示されないだけで、他人の文書が見えることはありません。
SSO でログインした場合にどの値がユーザー名になるかは、\ :doc:`guide-15` を参照してください。

すでに ``permission_sync`` なしでプライベートチャンネルを取り込んでいた場合、その文書は有効期限が切れるまで、権限が付かないまま残ります。
［システム情報］>［検索］で該当の文書を削除してから、この設定でクロールしてください。

ラベル・ブースト値・スケジュール
================================

ラベルは、上の各スクリプトの ``label="..."`` の行で付けています。
検索画面の絞り込みに表示するには、［クローラー］>［ラベル］で同じ値（\ ``code``\ 、\ ``docs``\ 、\ ``tickets``\ 、\ ``slack``\ ）のラベルを作ります。
文書の URL に一致する「対象とするパス」を持つラベルがあると、スクリプトのラベルが失われる点に注意してください（\ :doc:`datastore-basics`\ ）。

［クローラー］>［ドキュメントブースト］のルールは、データストアの文書には適用されません。
Confluence の設計書を Slack の発言より上位に出したい場合は、Confluence のデータストア設定の「ブースト値」（初期値 ``1.0``\ ）を上げます。
値は検索スコアに掛け合わされるので、少しずつ変えて検索結果を見比べてください。

ツールごとに実行頻度を変えるには、各データストア設定の詳細画面で［新しいジョブの作成］を使います（\ :doc:`datastore-basics`\ ）。

API のレート制限
================

Slack と Atlassian のプラグインは、\ ``429`` と ``5xx`` の応答を自動で再試行し、\ ``Retry-After`` ヘッダーがあればその秒数待ちます（Slack は最大 60 秒）。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - プラグイン
     - 調整できるパラメーター
   * - Slack
     - ``read_interval``\ （メッセージ 1 件ごとの待ち時間、ミリ秒、既定 ``0``\ ）、\ ``max_retry_count``\ （既定 ``3``\ ）、\ ``retry_interval``\ （最初の再試行までの待ち時間、ミリ秒、既定 ``3000``\ 。再試行ごとに倍になり、上限 60 秒）
   * - Atlassian
     - ``read_interval``\ （API 呼び出しの最小間隔、ミリ秒、既定 ``0``\ 。スレッド間で共有）。再試行の回数と間隔は固定です

Slack で再試行を使い切ると、そのクロールは中断されます。
ジョブログの状態は「OK」のままなので、次の節の手順で確認します。

動作を確認する
==============

ジョブの結果やログの見方は :doc:`datastore-basics` で説明しています。
データストアのクロールは失敗してもジョブが「OK」と表示されることがあるため、件数とログで判断してください。
この記事の構成では、さらに次の点を確かめます。

1. ［システム情報］>［検索］で ``label:code``\ 、\ ``label:docs``\ 、\ ``label:tickets``\ 、\ ``label:slack`` をそれぞれ検索し、件数が 0 でないことを確認する
2. Git の文書の URL を開き、リポジトリのファイルが表示されることを確認する。\ ``fess-crawler.log`` に ``base_url is blank`` の警告が出ていれば ``base_url`` を見直す
3. Git の設定の詳細画面を開き、パラメーターに ``prev_commit_id`` が書き戻されていることを確認する
4. ログアウトした状態で、プライベートチャンネルにだけある語を検索し、1 件も出ないことを確認する
5. そのチャンネルのメンバーでログインすると、同じ語で見つかることを確認する

5 で見つからない場合は、Fess のユーザー名と Slack のメールアドレスが一致しているか、\ ``fess-crawler.log`` に ``private channel(s) skipped`` の警告が出ていないかを確認します。
認証エラーなどで設定全体が失敗した場合は、\ ［システム情報］>［障害URL］に設定単位で記録されます。

まとめ
======

- Git は ``base_url`` を必ず指定し、差分クロールで文書が期限切れにならないよう ``time_to_live`` を付けます。
- Confluence と Jira は ``content.comments`` / ``issue.comments`` でコメントも取り込み、JQL は ``jira.jql`` に書きます。
- Slack のタイトルは ``message.user`` と ``message.channel`` から作ります。
- Git、Confluence、Jira は元の権限を持ち込まないので、「パーミッション」欄と取り込み範囲で公開範囲を決めます。
- Slack のプライベートチャンネルは別の設定にし、\ ``permission_sync=true``\ 、\ ``role=message.roles``\ 、空の「パーミッション」欄で取り込みます。
- 情報源の優先度は、データストア設定の「ブースト値」で調整します。

参考資料
========

- `Gitコネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-git.html>`__
- `Atlassianコネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-atlassian.html>`__
- `Slackコネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-slack.html>`__
- `データストア設定 <https://fess.codelibs.org/ja/stable/admin/dataconfig-guide.html>`__
- `全般設定 <https://fess.codelibs.org/ja/stable/admin/general-guide.html>`__
- `fess-ds-slack 15.9.0 README（スコープと権限同期） <https://github.com/codelibs/fess-ds-slack/blob/fess-ds-slack-15.9.0/README.md>`__
