===============================================
Namazu・Hyper Estraier から Fess への移行ガイド
===============================================

はじめに
========

社内の Web サイトやファイル共有を検索するために、Namazu や Hyper Estraier のような全文検索ソフトウェアを CGI で動かしている組織は今もあります。導入当時は手軽で十分な仕組みでしたが、長く使っているうちに「サーバーを入れ替えたら動かなくなりそう」「担当者が異動して誰も中身を知らない」といった不安が積み重なっていきます。

本ページでは、こうした自前運用の全文検索を、メンテナンスが続いているオープンソースの全文検索サーバー Fess に置き換える手順をまとめます。今の構成要素が Fess のどの機能に当たるかを整理し、棚卸しから旧システムの撤去までを順に説明します。

対象読者
========

- Namazu や Hyper Estraier などで、社内サイトやファイル共有の検索を運用している情報システム担当の方
- CGI の検索ページを、保守されている仕組みに置き換えたい方
- 置き換え作業の全体像と、どこで何を確認すればよいかを知りたい方

Fess は Apache License 2.0 で公開されており、ライセンス費用なしで利用できます。

移行を検討する理由
==================

いちばんの理由は、ソフトウェアのメンテナンス状況です。それぞれの公式サイトに掲載されている情報は次のとおりです（2026 年 11 月に確認）。

.. list-table:: 公式サイトに掲載されている最新の情報
   :header-rows: 1
   :widths: 20 80

   * - ソフトウェア
     - 公式サイトの記載
   * - Namazu
     - 新着情報の最新の項目は、2011 年 7 月 18 日の「Namazu 2.0.21 を公開」（セキュリティフィックスリリース）です
   * - Hyper Estraier
     - ダウンロード欄の最新のソースパッケージはバージョン 1.4.13 で、ページの最終更新日は 2007 年 3 月 6 日と表示されています

どちらも、公式サイトのトップページに載っている最新の日付は 10 年以上前です。新しいリリースが出ていないソフトウェアを使い続けると、OS や Web サーバー、Perl などの実行環境を更新したときの修正も、脆弱性が見つかったときの修正も、自分たちで引き受けることになります。CGI として公開している検索ページは、外部からの入力を直接受け取る部分でもあります。

上の表にないツールを使っている場合も、公式サイトやリポジトリで最終リリースの時期を確認しておくと、移行の優先度を判断する材料になります。

今の構成は Fess のどの機能に当たるか
====================================

Namazu や Hyper Estraier による検索は、おおむね「インデックスを作るコマンド」「それを定期的に動かす cron」「検索を受け付ける CGI」の 3 つでできています。Fess では、これらを管理画面の設定に置き換えます。

.. list-table:: 旧来の構成と Fess の機能の対応
   :header-rows: 1
   :widths: 40 60

   * - 旧来の構成
     - Fess での対応
   * - Web サイトを巡回してインデックスを作る（Hyper Estraier の ``estwaver`` など）
     - ウェブクロール。 ［クローラー］ > ［ウェブ］ で開始 URL を登録します
   * - ディレクトリや共有フォルダのファイルからインデックスを作る（ ``mknmz`` 、 ``estcmd gather`` ）
     - ファイルクロール。 ［クローラー］ > ［ファイルシステム］ でパスを登録します
   * - 共有フォルダにアクセスするためのアカウント
     - ［クローラー］ > ［ファイル認証］ に登録します
   * - ``file://`` の URL を ``http://`` に置き換えて表示する（ ``mknmz`` の ``--replace`` 、 ``estseek.cgi`` の置換機能）
     - パスマッピング。 ［クローラー］ > ［パスマッピング］ で正規表現による置換を設定します
   * - 検索するインデックスを選ばせる（Namazu の ``idxname`` ）
     - ラベル。 ［クローラー］ > ［ラベル］ で登録すると、検索画面で絞り込めるようになります
   * - cron でインデックスを定期的に作り直す
     - ［システム］ > ［スケジューラ］ のクロールジョブ（「Default Crawler」）を CRON 形式で設定します
   * - 検索ページの CGI（ ``namazu.cgi`` 、 ``estseek.cgi`` ）
     - Fess の検索画面。見た目は ［システム］ > ［テーマ］ で管理するテーマで変更できます
   * - 各ページに埋め込んだ検索フォーム
     - フォームの送信先を Fess の検索ページ（ ``/search/`` ）に変えます
   * - 検索結果を別のプログラムで使う
     - 検索 API（ ``/api/v2/search`` ）が JSON で結果を返します

Web サイトを検索している場合
----------------------------

社内サイトを検索対象にしている場合は、ウェブクロールを使います。 ［クローラー］ > ［ウェブ］ で、開始 URL と「クロール対象とするURL」（正規表現）を登録すると、Fess のクローラーがリンクをたどってページを集めます。

Web サーバーの公開ディレクトリ（ ``public_html`` など）をファイルとしてインデックスしていた場合も、Fess ではサイトを URL でクロールするのが基本です。検索結果のリンクが最初から ``http://`` や ``https://`` になるため、パスの置換を考える必要がなくなります。

BASIC 認証、DIGEST 認証、NTLM 認証、フォーム認証で保護されたサイトもクロールできます。認証情報は ［クローラー］ > ［ウェブ認証］ に登録します。

ファイル共有を検索している場合
------------------------------

ディレクトリや Windows の共有フォルダを検索対象にしている場合は、ファイルクロールを使います。 ［クローラー］ > ［ファイルシステム］ の「パス」に、次のような形式で開始位置を指定します。

.. list-table:: ファイルクロールのパスの例
   :header-rows: 1
   :widths: 40 60

   * - パス
     - 対象
   * - ``file:/home/share``
     - Fess を動かすサーバー上のディレクトリ。マウント済みのファイルシステムもここに含まれます
   * - ``smb://SERVER/SharedFolder/``
     - Windows の共有フォルダ（SMB）
   * - ``smb1://SERVER/SharedFolder/``
     - SMB1 しか使えない古い機器の共有フォルダ

共有フォルダにユーザー名とパスワードが必要な場合は、 ［クローラー］ > ［ファイル認証］ で認証設定を作ります。スキームに「SAMBA」を選び、ホスト名にはクロールする URL に書いたものと同じ名前を指定します。IP アドレスと別名のように書き方が違うと、その認証は使われません。ドメインアカウントを使う場合は、パラメーターに ``domain=ドメイン名`` の形式でドメインを指定します。

Office 文書や PDF などは、ファイル名だけでなく本文も検索対象になります。対応している形式は `検索対象ファイル <https://fess.codelibs.org/ja/supported-files.html>`__ で確認できます。

ファイル共有の検索を導入する前に確認しておきたい点（アクセス権限の扱いや規模の見積もり）は、 `オープンソースで実現するファイルサーバ全文検索 <https://fess.codelibs.org/ja/articles/file-server-search.html>`__ にまとめています。

検索フォームを各ページに埋め込んでいる場合
------------------------------------------

既存のページに置いた検索フォームは、送信先とキーワードのパラメーター名を変えると、Fess の検索画面につながります。Fess の検索ページは ``/search/`` で、キーワードは ``q`` パラメーターで受け取ります。

.. list-table:: キーワードを渡すパラメーター
   :header-rows: 1
   :widths: 40 30 30

   * - 検索ページ
     - 送信先
     - キーワードのパラメーター
   * - Namazu
     - ``namazu.cgi``
     - ``query``
   * - Hyper Estraier
     - ``estseek.cgi``
     - ``phrase``
   * - Fess
     - ``/search/``
     - ``q``

Fess に置き換えたフォームは、たとえば次のようになります。 ``https://search.example.com`` は、構築した Fess サーバーの URL に読み替えてください。

::

    <form method="get" action="https://search.example.com/search/" accept-charset="UTF-8">
    <input type="text" name="q" maxlength="1000">
    <input type="submit" value="検索">
    </form>

Fess は検索語を UTF-8 として受け取ります。旧来のページが EUC-JP や Shift_JIS で書かれている場合は、例のように ``accept-charset="UTF-8"`` を付けて、検索語が UTF-8 で送られるようにしてください。

このフォームに、入力中に候補を表示するサジェストを追加することもできます。手順は `検索フォームの配置 <https://fess.codelibs.org/ja/stable/config/search-form-integration.html>`__ を参照してください。

検索結果を自分たちのページの中に表示したい場合や、ほかの業務システムから検索したい場合は、検索 API を使います。 ``/api/v2/search`` に ``q`` パラメーターを付けて呼び出すと、検索結果が JSON で返ります。

移行の進め方
============

1. 今のインデックスの対象を棚卸しする
-------------------------------------

まず、旧システムが何を検索対象にしているかを書き出します。設定が担当者の記憶にしか残っていないことも多いので、実際に動いているものから確認するのが確実です。

- cron に登録されたコマンドと、その引数に指定されたディレクトリや URL
- ``mknmz`` の ``--replace`` オプションや、 ``estseek.cgi`` の設定ファイル（ ``estseek.conf`` ）の ``replace`` に書かれた URL の置換規則
- インデックスが複数ある場合は、それぞれの対象と、どの検索ページから使われているか
- 検索フォームを置いているページの一覧
- 検索ページを見られる人の範囲（社内全体か、特定の部門だけか）

ここで書き出した一覧が、そのまま Fess のクロール設定と、後で切り替える検索フォームのリストになります。

2. Docker で Fess を試す
------------------------

本番の構築に入る前に、手元で Fess を動かして検索の結果を確かめます。Docker と Docker Compose があれば、次のコマンドで起動できます。

::

    $ mkdir fess-docker && cd fess-docker
    $ curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose.yaml
    $ curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/main/compose/compose-opensearch3.yaml
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

数分後、 ``http://localhost:8080/`` で検索画面、 ``http://localhost:8080/admin`` で管理画面が開きます。管理画面には admin/admin でログインし、最初に管理者のパスワードを変更してください。詳しい手順は `簡単構築ガイド <https://fess.codelibs.org/ja/quick-start.html>`__ と `Docker でのインストール <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__ にあります。

3. クロールを設定して結果を比べる
---------------------------------

棚卸しした対象を、ウェブクロールとファイルクロールの設定として登録します。最初は対象を 1 つに絞り、うまく取り込めることを確かめてから増やしていくと、問題が起きたときに原因を絞り込みやすくなります。

登録したら、 ［システム］ > ［スケジューラ］ で「Default Crawler」を開き、「今すぐ開始」でクロールを実行します。このジョブは、有効になっているすべてのクロール設定を対象に動きます。クロールが終わったら、旧システムでよく使われていたキーワードで両方を検索し、結果を見比べます。

定期的なクロールの時刻は、同じ「Default Crawler」のスケジュールに CRON 形式（ ``分 時 日 月 曜日`` ）で設定します。旧システムの cron と同じ頻度から始めると、利用者から見た情報の鮮度が変わりません。

4. 検索できる人の範囲を設定する
-------------------------------

旧システムでは、公開範囲ごとにインデックスや検索ページを分けて運用していることがあります。Fess では、検索ページを分ける代わりに、文書ごとに「誰に見せるか」を設定し、ログインしたユーザーに応じて検索結果を出し分けます。

- クロール設定の「パーミッション」で、その設定で集めた文書を見られるユーザー、グループ、ロールを指定します（例: ``{group}developer`` ）
- SMB でクロールしたファイルは、ファイルサーバーに設定されたアクセス権限（ACL）からロールを取り出して文書に記録します。この動作は既定で有効です
- 検索するユーザーの所属グループを Fess に伝えるには、Active Directory や LDAP との連携を設定します

全員が同じ範囲を見てよいのであれば、この手順は省略できます。部門ごとに検索範囲を分けたいだけであれば、ラベルで絞り込めるようにする方法もあります。

5. 本番環境を構築して検索の入口を切り替える
-------------------------------------------

試した設定をもとに本番環境を構築し、検索の入口を Fess に切り替えます。

- 各ページの検索フォームを、送信先 ``/search/`` 、パラメーター ``q`` のフォームに書き換えます。ページが UTF-8 でない場合は ``accept-charset="UTF-8"`` も付けます
- 旧検索ページの URL がブックマークや他のページのリンクに残っている場合は、Web サーバーの設定で Fess の検索ページへリダイレクトします。そのとき、 ``query`` や ``phrase`` の値を ``q`` に移しておくと、検索語を入れたリンクもそのまま使えます
- 切り替え後しばらくは旧システムを残しておき、Fess で見つからないという問い合わせがあれば、クロール設定の漏れを確認します

6. 旧システムを撤去する
-----------------------

Fess への切り替えが落ち着いたら、旧システムを片付けます。

- cron に登録したインデックス作成のコマンドを止めます
- Web サーバーから検索用の CGI を外します。リダイレクトを設定した場合は、その設定は残します
- 旧システムのインデックスを削除します。インデックスには文書の内容が含まれているため、不要になったものを残しておかないようにします

まとめ
======

- Namazu と Hyper Estraier は、どちらも公式サイトのトップページに載っている最新の日付が 10 年以上前です
- インデックスを作るコマンドはクロール設定に、cron はスケジューラに、CGI の検索ページは Fess の検索画面に置き換えます
- Web サイトはウェブクロールで、ディレクトリや共有フォルダはファイルクロールとファイル認証で検索対象にします
- 既存の検索フォームは、送信先を ``/search/`` 、キーワードのパラメーターを ``q`` に変えると Fess につながります。ページが UTF-8 でない場合は ``accept-charset="UTF-8"`` も付けます
- 棚卸しと Docker での試行から始め、検索の入口を切り替えてから旧システムを撤去します

参考資料
========

- `ウェブクロール（Webサイト検索） <https://fess.codelibs.org/ja/stable/admin/webconfig-guide.html>`__
- `ウェブ認証 <https://fess.codelibs.org/ja/stable/admin/webauth-guide.html>`__
- `ファイルクロール（ファイルサーバー検索） <https://fess.codelibs.org/ja/stable/admin/fileconfig-guide.html>`__
- `ファイル認証 <https://fess.codelibs.org/ja/stable/admin/fileauth-guide.html>`__
- `パスマッピング <https://fess.codelibs.org/ja/stable/admin/pathmap-guide.html>`__
- `ラベル <https://fess.codelibs.org/ja/stable/admin/labeltype-guide.html>`__
- `スケジューラ <https://fess.codelibs.org/ja/stable/admin/scheduler-guide.html>`__
- `テーマ <https://fess.codelibs.org/ja/stable/admin/theme-guide.html>`__
- `検索フォームの配置 <https://fess.codelibs.org/ja/stable/config/search-form-integration.html>`__
- `検索API <https://fess.codelibs.org/ja/stable/api/api-search.html>`__
- `ロールベース検索の設定 <https://fess.codelibs.org/ja/stable/config/security-role.html>`__
- `LDAP統合ガイド <https://fess.codelibs.org/ja/stable/config/ldap-integration.html>`__
- `簡単構築ガイド <https://fess.codelibs.org/ja/quick-start.html>`__
- `Docker でのインストール <https://fess.codelibs.org/ja/stable/install/install-docker.html>`__
- `オープンソースで実現するファイルサーバ全文検索 <https://fess.codelibs.org/ja/articles/file-server-search.html>`__
- `Namazu 公式サイト <http://www.namazu.org/index.html.ja>`__
- `Hyper Estraier 公式サイト <https://dbmx.net/hyperestraier/index.ja.html>`__
