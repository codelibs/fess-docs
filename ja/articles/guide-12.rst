================================================
データベース・CSV・Salesforce のデータを検索する
================================================

はじめに
========

製品マスタは社内のデータベースに、取引先の一覧は基幹システムが毎晩書き出す CSV に、商談や問い合わせの記録は Salesforce に入っている。
このような業務データは、それぞれのシステムの画面からしか探せないことがよくあります。
Fess のデータストアプラグインを使うと、これらをレコード単位で取り込み、ファイルサーバーや社内サイトの文書と同じ検索画面から探せるようになります。

この記事では、3 つの情報源をそれぞれ取り込む設定と、情報源ごとの絞り込み・実行スケジュール・結果の確かめ方を説明します。
プラグインのインストール、ハンドラー名・パラメーター・スクリプトの書き方、ジョブの作り方といったデータストア共通の手順は :doc:`datastore-basics` にまとめています。
先にそちらを読んでから進めてください。
記事中の設定値は Fess 15.9 と、15.9.0 版の各プラグインに合わせています。

この記事で作る構成
==================

.. list-table::
   :header-rows: 1
   :widths: 18 22 22 38

   * - 情報源
     - プラグイン
     - ハンドラー名
     - 事前に用意するもの
   * - データベース（製品マスタ）
     - ``fess-ds-db``
     - ``DatabaseDataStore``
     - JDBC ドライバーの jar ファイルと、SELECT だけできる DB ユーザー
   * - CSV（取引先一覧）
     - ``fess-ds-csv``
     - ``CsvDataStore``
     - CSV を書き出すディレクトリ（クローラーから読める場所）
   * - Salesforce（取引先・商談・ケース）
     - ``fess-ds-salesforce``
     - ``SalesforceDataStore``
     - 接続アプリケーションと、JWT 署名用の鍵ペア

Docker で動かしている場合は、``compose.yaml`` の ``fess01`` の ``environment`` に、3 つのプラグインを空白区切りで指定します。

.. code-block:: yaml

    environment:
      - "FESS_PLUGINS=fess-ds-db:15.9.0 fess-ds-csv:15.9.0 fess-ds-salesforce:15.9.0"

管理画面や ``fess-setup`` でインストールした場合は、Fess の再起動が必要です。

先に決めること：検索結果を誰に見せるか
======================================

3 つのプラグインはどれも、元のシステムの閲覧権限（ACL）を Fess に持ち込みません。
取り込んだ文書のロールは、データストア設定の「パーミッション」欄の値だけで決まります。
この欄には最初から ``{role}guest`` が入っており、そのままではログインしていない利用者も検索できます。

価格や顧客情報を含むデータでは、欄を見せたいグループに書き換えます（例: ``{group}sales``\ ）。
1 つの設定から登録される文書には、すべて同じパーミッションが付きます。
見せる相手が違うデータは、別のデータストア設定に分けてください。
グループの設計は :doc:`guide-05` を参照してください。

データベース：製品マスタを取り込む
==================================

JDBC ドライバーを置く
---------------------

``fess-ds-db`` には JDBC ドライバーが含まれていません。
接続先のデータベースに合ったドライバーの jar ファイル（PostgreSQL なら ``postgresql-<バージョン>.jar``\ 、MySQL なら ``mysql-connector-j-<バージョン>.jar``\ ）を入手し、クローラーのクラスパスに置きます。
データストアのクロールは Fess 本体とは別のクローラープロセスで動き、そのクラスパスには次の 2 つのディレクトリの jar が含まれます。

- ``app/WEB-INF/lib/``
- ``app/WEB-INF/env/crawler/lib/``

ZIP パッケージでは Fess を展開したディレクトリの下、RPM / DEB では ``/usr/share/fess/`` の下にあります。
置いたら Fess を再起動します。

Docker イメージでも、Fess は ``/usr/share/fess/`` に置かれています。
コンテナ内にコピーした jar はコンテナを作り直すと消えるため、``compose.yaml`` の ``fess01`` に jar ファイル 1 つだけをマウントします。

.. code-block:: yaml

    volumes:
      - ./postgresql-42.7.4.jar:/usr/share/fess/app/WEB-INF/env/crawler/lib/postgresql.jar:ro

ディレクトリごとマウントすると、イメージがそのディレクトリに置いている jar が見えなくなり、クローラーが起動できなくなります。
必ずファイル単位でマウントしてください。
変更後は ``docker compose -f compose.yaml -f compose-opensearch3.yaml up -d`` でコンテナを作り直します。

パラメーターと SQL
------------------

ここでは PostgreSQL の ``products`` テーブルを例にします。
検索結果のリンク先には、製品マスタの照会画面（例: ``https://erp.example.com/products/<製品ID>``\ ）を使います。
［クローラー］>［データストア］>［新規作成］で、ハンドラー名に ``DatabaseDataStore`` を選び、パラメーターを次のようにします。

.. code-block:: properties

    script_type=javascript
    driver=org.postgresql.Driver
    url=jdbc:postgresql://db.example.com:5432/erp
    username=fess_reader
    password=your-password
    query_timeout=600
    sql=SELECT p.product_id, concat('https://erp.example.com/products/', p.product_id) AS page_url, p.product_name AS title, concat_ws(' ', p.product_name, p.model_number, c.category_name, p.description) AS body, p.updated_at FROM products p JOIN categories c ON c.category_id = p.category_id WHERE p.discontinued = false

スクリプトは次のとおりです。

.. code-block:: properties

    url=page_url
    title=title
    content=body
    last_modified=updated_at
    label="products"

``sql`` は 1 行で書きます。
SQL はそのままデータベースに送られ、結果の 1 行が 1 件の文書になります。
リンク先の URL と本文を SQL の中で組み立てておくと、スクリプトは列名を書くだけで済みます。
``concat_ws`` は NULL の列を飛ばして連結するため、説明が空の製品でも本文が NULL になりません。
MySQL でも ``CONCAT_WS`` は同じ動作ですが、``CONCAT`` は引数に NULL があると結果全体が NULL になります。

Docker で動かしている場合、``url`` の ``localhost`` はデータベースのサーバーではなく Fess のコンテナ自身を指します。
データベースのホスト名か IP アドレスを書いてください。

列名とスクリプトの対応
----------------------

スクリプトの右辺には、SELECT の結果の列ラベル（\ ``AS`` で付けた別名）をそのまま書きます。
次の 3 点に注意してください。

- 列ラベルの大文字・小文字はデータベースによって変わります。引用符で囲まない別名を、PostgreSQL は小文字に、Oracle や H2 は大文字に変え、MySQL は書いたとおりに返します。スクリプトには、データベースが返すとおりの大文字・小文字で書きます。一致しないとそのフィールドには値が入りません
- スクリプトからは、パラメーター欄の値も同じ名前の変数として見えます。結果に ``url`` という列がないまま ``url=url`` と書くと、JDBC の接続 URL が文書の URL になります。リンク先の列には ``page_url`` のように、パラメーターと重ならない名前を付けてください
- ハングしたクエリーはジョブを止めても止まりません。``query_timeout``\ （秒）を必ず設定します

``fess-ds-db`` に差分クロールのオプションはありません。
実行のたびに ``sql`` 全体を実行して、全行を登録し直します。
件数が多いテーブルでは、データベースの負荷が低い時間帯にジョブを実行してください（後述の「情報源ごとにジョブを作る」）。

CSV：基幹システムが書き出す取引先一覧を取り込む
===============================================

CSV コネクタの基本的な使い方は、:doc:`datastore-basics` の「例：CSV ファイルを検索できるようにする」で説明しています。
ここでは、基幹システムが定期的に書き出す CSV を取り込むときに必要になる点だけを補足します。

例として、基幹システムが毎晩 2:00 に次のような ``customers_20261128.csv`` を書き出すとします。
文字コードは MS932（Windows の Shift_JIS）、1 行目は日本語の見出しです。

.. code-block:: text

    取引先コード,取引先名,所在地,担当部署,取引状況
    C0001,株式会社サンプル商事,東京都千代田区,第一営業部,取引中
    C0002,サンプル工業株式会社,大阪府大阪市,第二営業部,取引終了

ファイルの置き場所
------------------

CSV は、Fess のクローラーが動くサーバーから読めるパスに書き出します。
Docker では、書き出し先のディレクトリを ``fess01`` に読み取り専用でマウントします。

.. code-block:: yaml

    volumes:
      - ./export/customers:/data/customers:ro

パラメーターとスクリプト
------------------------

.. code-block:: properties

    script_type=javascript
    directories=/data/customers
    file_encoding=MS932
    has_header_line=true

.. code-block:: javascript

    url=cell5 == "取引中" ? "https://crm.example.com/customers/" + cell1 : null
    title=cell2
    content=cell2 + " " + cell3 + " " + cell4
    label="customers"

- ``directories`` を指定すると、そのディレクトリ内の拡張子 ``.csv`` / ``.tsv`` のファイルをすべて、更新日時の古い順に読みます。日付付きのファイル名で毎日書き出される場合に、パラメーターを書き換えずに済みます。古いファイルを残すと、そのファイルの行も毎回読み込まれます
- Excel や Windows 向けのシステムが書き出す CSV は多くの場合 MS932 です。``Shift_JIS`` を指定すると ``①`` や ``㈱`` のような文字が置換文字になるため、``MS932`` を指定します
- 見出しが日本語でも ``has_header_line=true`` で 1 行目を読み飛ばせます。スクリプトでは列の番号（``cell1``\ 、``cell2`` …）で参照すると確実です。見出しに空白や記号を含む列は、見出し名では参照できません
- タブ区切りのファイルは ``separator_character=\t`` を追加します
- ``url`` が ``null`` になった行は登録されません。この例では「取引終了」の取引先を除外しています。除外した行数は ``fess-crawler.log`` に ``Skipped 1 row(s) in ... because the script did not set the url field.`` という WARN で出ます

書き出しの途中のファイルを読むと、途中までの行しか登録されません。
ジョブは CSV の書き出しが終わる時刻より後に実行してください。

Salesforce：取引先・商談・ケースを取り込む
==========================================

Salesforce 側の準備
-------------------

``fess-ds-salesforce`` は、``auth_type=oauth_token``\ （JWT ベアラーフロー）と ``auth_type=oauth_password``\ （ユーザー名とパスワード）の 2 つの認証方式に対応しています。
ここではパスワードを保存せずに済む ``oauth_token`` を使います。
``oauth_password`` で使うユーザー名・パスワードによる OAuth フローは、Salesforce 組織の設定によっては無効にされていることがあります。

1. 鍵ペアと証明書を作ります

   .. code-block:: bash

       openssl genrsa -out private_key.pem 2048
       openssl req -new -x509 -key private_key.pem -out certificate.crt -days 365

2. Salesforce の［設定］で接続アプリケーションを作り、OAuth 設定を有効にして「デジタル署名を使用」に ``certificate.crt`` をアップロードします。OAuth スコープはリファレンスのとおりに選びます
3. 接続アプリケーションのポリシーで「許可されているユーザー」を「管理者が承認したユーザーは事前承認済み」にし、クロールに使うユーザーのプロファイルか権限セットを割り当てます
4. 接続アプリケーションのコンシューマー鍵を控えます

Salesforce 側の画面や名称は変わることがあるため、詳しくは Salesforce のヘルプの JWT ベアラーフローの説明も確認してください。

Fess が取り込めるのは、クロールに使うユーザーが読めるレコードと項目だけです。
読めない項目を後述の ``contents`` に指定すると、そのオブジェクトの取得が失敗します。

パラメーターとスクリプト
------------------------

``private_key`` には ``private_key.pem`` の中身を、改行を ``\n`` に置き換えて 1 行で書きます。
プラグインが読めるのは PKCS#8 形式（\ ``-----BEGIN PRIVATE KEY-----`` で始まる形式）だけです。
古い OpenSSL で作った ``-----BEGIN RSA PRIVATE KEY-----`` で始まる鍵は、``openssl pkcs8 -topk8 -nocrypt -in private_key.pem -out private_key_pkcs8.pem`` で変換してから使います。

.. code-block:: properties

    script_type=javascript
    base_url=https://login.salesforce.com
    auth_type=oauth_token
    username=fess-crawler@example.com
    client_id=3MVG9...
    private_key=-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n
    include_pattern=.*/(001|006|500)[A-Za-z0-9]+
    OPPORTUNITY.contents=Name,StageName,NextStep,Description

.. code-block:: javascript

    url=object.url
    title="[" + object.type + "] " + object.title
    content=object.content
    digest=object.description
    created=object.created
    last_modified=object.last_modified
    label="salesforce"

Sandbox を対象にする場合は ``base_url=https://test.salesforce.com`` にします。

右辺の項目は、すべて ``object.`` で始まります。
``url=url`` のように接頭辞を付けずに書くと式の評価が失敗し、レコードは登録されずに障害URL に記録されます。
``object.url`` は ``<インスタンスの URL>/<レコード ID>`` の形式で、クリックすると Salesforce のレコード画面が開きます。

取り込む範囲を絞る
------------------

``fess-ds-salesforce`` は、取引先・取引先責任者・リード・商談・ケース・ToDo・ユーザーなど 23 種類の標準オブジェクトを常にすべて読みます。
オブジェクトを選んで読む設定はありません。
範囲を絞るには、次の 3 つを組み合わせます。

- ``include_pattern`` / ``exclude_pattern``\ ：\ ``object.url`` 全体に一致する正規表現で、登録するレコードを選びます。Salesforce のレコード ID は、先頭 3 文字がオブジェクトごとに決まっています（取引先 ``001``\ 、商談 ``006``\ 、ケース ``500`` など）。上の例はこの 3 種類だけを登録します。取得自体は全オブジェクトに対して行われ、登録の前に捨てられるだけです
- ``<オブジェクト名>.title`` / ``<オブジェクト名>.contents``\ ：タイトルと本文に使う項目を、項目の API 参照名で指定します。標準オブジェクトの名前は ``ACCOUNT``\ 、``OPPORTUNITY``\ 、``CASE`` のような大文字のスネークケースです。指定しない場合はプラグインの既定の項目が使われます
- ``custom``\ ：カスタムオブジェクトの API 参照名をカンマ区切りで指定すると、標準オブジェクトに加えて読みます

カスタムオブジェクトには既定の項目がないため、``.title`` と ``.contents`` を必ず指定します。
タイトルの項目は本文の項目にも含めてください。
プラグインは ``.contents`` などに書いた項目だけを取得するため、``.title`` にしか書いていない項目は取得されず、タイトルが空になります。

.. code-block:: properties

    custom=Project__c
    Project__c.title=Name
    Project__c.contents=Name,Customer_Name__c,Summary__c

ラベルで情報源ごとに絞り込む
============================

ここまでの例では、スクリプトの ``label`` で ``products``\ 、``customers``\ 、``salesforce`` を付けています。
検索画面のラベルの選択肢に表示するには、［クローラー］>［ラベル］で同じ「値」のラベルを作成します（「対象とするパス」は空でかまいません）。
ラベルの値に使えるのは英数字と ``_`` だけです。

Salesforce をオブジェクトごとに分けたい場合は、スクリプトの ``label`` の代わりに、「対象とするパス」でレコード ID の先頭 3 文字を見るラベルを作ります。
たとえば値 ``sf_case``\ 、対象とするパス ``https://example\.my\.salesforce\.com/500.*`` のラベルは、ケースだけに付きます。
URL に一致するラベルがあると、スクリプトで付けたラベルは失われます。
1 つのデータストア設定では、どちらか一方の方法だけを使ってください（詳しくは :doc:`datastore-basics` の「ラベル」）。

情報源ごとにジョブを作る
========================

初期状態の「Default Crawler」は、毎日 0:00 にすべての設定をまとめてクロールします。
情報源ごとに都合のよい時刻は違うため、データストア設定ごとにジョブを作ります。
各設定の詳細画面で［新しいジョブの作成］をクリックし、「スケジュール」に cron 形式で時刻を入れます（手順は :doc:`datastore-basics` の「スケジュール」）。

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - 情報源
     - スケジュールの例
     - 考えること
   * - データベース
     - ``0 3 * * *``
     - 毎回全行を読むため、データベースの負荷が低い時間帯にする
   * - CSV
     - ``30 2 * * *``
     - 書き出しが終わる時刻より後にする
   * - Salesforce
     - ``0 7,12,18 * * *``
     - 1 回の実行で、標準オブジェクトとカスタムオブジェクトの数だけ Bulk API のジョブを作る。組織の API 制限の残りを見て回数を決める

Default Crawler も引き続きこれらの設定をクロールします。
二重に実行したくない場合は、データストア設定の「状態」を無効にします（設定 ID を指定したジョブは、無効な設定もクロールします）。

元のデータから消えた行の扱い
============================

データベースの行を削除したり、CSV から行がなくなったりしても、その文書は次のクロールでは削除されません。
データストアで登録した文書には有効期限が付き、期限は登録のたびに延びます。
登録されなくなった文書は、最後に登録されてから［システム］>［全般］の「以前のドキュメントを削除」の日数（初期値 3 日）が過ぎると、自動で削除されます。

この仕組みには注意が必要な面もあります。
データベースに接続できない日が続いて、この日数を過ぎると、その設定の文書はすべて検索結果から消えます。
取り込みの失敗は、次の節の方法で早めに見つけてください。

動作を確認する
==============

ジョブログ、［システム情報］>［クロール情報］、障害URL、``fess-crawler.log`` の見方は :doc:`datastore-basics` の「結果を確かめる」で説明しています。
データストアのクロールは、取り込みに失敗してもジョブが「OK」になることがあるため、件数とログで判断してください。

1. ［システム情報］>［検索］で ``label:products``\ 、``label:customers``\ 、``label:salesforce`` と検索し、件数を元のデータと比べます（データベースなら ``sql`` と同じ条件の ``SELECT count(*)``\ ）
2. ``fess-crawler.log`` の WARN と ERROR を確認します。この記事の構成で出やすいのは次のメッセージです

   - ``The JDBC driver ... is not on the crawler classpath.``\ ：ドライバーの置き場所か ``driver`` のクラス名が違う
   - ``Failed to connect to ...``\ ：データベースのホスト名・ポート・ユーザー名・パスワードを確認する
   - ``is not a directory.`` や ``No CSV file.``\ ：\ ``directories`` のパスにクローラーから読める CSV がない
   - ``Batch:... Failed caused by ...``\ ：Salesforce の一部のオブジェクトが取得できなかった。``.contents`` の項目名や、クロールに使うユーザーの項目の権限を確認する
   - ``Failed to process a data crawling: <設定名>``\ ：設定全体が失敗した。Salesforce では認証の失敗がこれに当たる。続くスタックトレースで原因を確認する

3. 「パーミッション」欄を書き換えた設定では、対象のグループの利用者でログインして検索結果に出ること、ログアウトした状態では出ないことを確認します

まとめ
======

- 3 つのプラグインとも元のシステムの権限は持ち込まないため、「パーミッション」欄の ``{role}guest`` を見せたいグループに書き換えます
- データベースは JDBC ドライバーをクローラーのクラスパスに置き、リンク先の URL と本文を SQL で組み立てます。毎回全件を読みます
- 基幹システムの CSV は ``directories`` と ``file_encoding=MS932`` で読み、``cellN`` で参照します。``url`` を ``null`` にした行は登録されません
- Salesforce のスクリプトは ``object.*`` で書きます。標準オブジェクトは選べないため、``include_pattern`` と ``<オブジェクト名>.contents`` で絞ります
- 情報源ごとにジョブを作り、元データから消えた行は「以前のドキュメントを削除」の日数後に消えることを前提に運用します

次に読む記事
============

- データストアの共通の仕組み（スクリプト、パーミッション、ラベル、結果の確かめ方）: :doc:`datastore-basics`
- Git、Confluence、Jira、Slack を取り込みたい: :doc:`guide-06`
- Google Drive、SharePoint、Box を取り込みたい: :doc:`guide-07`
- 部署ごとに見える検索結果を変えたい: :doc:`guide-05`
- 取り込みの失敗を監視したい: :doc:`guide-10`

参考資料
========

- `データベースコネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-database.html>`__
- `CSV コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-csv.html>`__
- `Salesforce コネクタ <https://fess.codelibs.org/ja/stable/config/datastore/ds-salesforce.html>`__
- `データストア設定 <https://fess.codelibs.org/ja/stable/admin/dataconfig-guide.html>`__
- `スケジューラ <https://fess.codelibs.org/ja/stable/admin/scheduler-guide.html>`__
- `ラベル <https://fess.codelibs.org/ja/stable/admin/labeltype-guide.html>`__
- `全般 <https://fess.codelibs.org/ja/stable/admin/general-guide.html>`__
