=================================
検索 API で業務システムと連携する
=================================

はじめに
========

CRM の顧客画面に関連資料を並べたい、問い合わせ起票画面で似た FAQ を先に見せたい、自社システムが作るレポートも検索対象にしたい。
こうした要望は、業務システムのサーバーから Fess の検索 API（``/api/v2``）を呼ぶことで実現できます。

本記事では、Fess 15.9 を対象に次のことを順に進めます。

- curl で検索・ラベル・サジェスト・人気ワードの API を呼び、レスポンスの形を確かめる
- アクセストークンを作り、トークンのロールで返る文書を制御する
- 業務システムのサーバー側から検索 API を呼ぶ関数を書く
- クロールできないデータを ``PUT /api/admin/documents/bulk`` で登録する
- エラーとレート制限に備える

既存の Web サイトに検索窓や検索画面を組み込む方法（ブラウザー側の組み込み、テーマ、Fess Site Search）は :doc:`guide-03` で扱います。
Fess の起動とクロールがまだの場合は、先に :doc:`guide-02` を済ませてください。

この記事で作る構成
==================

::

    [利用者のブラウザー] --> [業務システムのサーバー] --(トークン付き)--> [Fess /api/v2]
                                   トークンはここだけに置く

ブラウザーがアクセスするのは業務システムだけで、Fess を呼ぶのは業務システムのサーバーです。
アクセストークンはサーバーの環境変数などに置き、ブラウザーへは渡しません。
理由は「アクセストークンを作る」で説明します。

API の全体像
============

Fess 15.9 の本体が提供する検索系 API は ``/api/v2`` 以下にあります。
本記事で使うものは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - エンドポイント
     - 用途
   * - ``GET /api/v2/search``
     - 全文検索。結果は ``response.data`` に入ります
   * - ``GET /api/v2/labels``
     - 呼び出し元が使えるラベルの一覧
   * - ``GET /api/v2/suggest-words``
     - 入力途中の語に対するサジェスト候補
   * - ``GET /api/v2/popular-words``
     - 人気ワード
   * - ``GET /api/v2/health``
     - 検索エンジンの状態（監視での使い方は :doc:`guide-10`）
   * - ``PUT /api/admin/documents/bulk``
     - 文書の一括登録（管理 API）

``/api/v2`` のレスポンスはすべて ``{"response": {...}}`` で包まれ、 ``response.status`` が 0 なら成功です。
JSON のキーは ``snake_case`` です。

.. note::

   15.9 の本体は ``/api/v1`` を提供しません。
   ``/api/v1`` を呼ぶ既存のクライアントを動かし続ける場合は、プラグイン ``fess-webapp-v1-api`` が必要です（Docker イメージには同梱されていません）。
   新しく作る連携は ``/api/v2`` を使ってください。

まず curl で試す
================

匿名で検索できる状態（［システム］>［全般］の「ログインが必要」がオフ、既定の状態）なら、トークンなしで呼べます。
日本語の検索語は ``-G --data-urlencode`` で URL エンコードして送ります。
出力を読みやすくするために ``jq`` を使っています。

::

    $ curl -s -G "http://localhost:8080/api/v2/search" \
        --data-urlencode "q=検索 ガイド" \
        --data-urlencode "num=3" \
      | jq '.response | {status, record_count, page_size, data: [.data[] | {doc_id, title, url_link, content_description}]}'

レスポンスは次の形です（``data`` は先頭の 1 件だけを示しています。値は環境によって変わります）。

.. code-block:: json

    {
      "status": 0,
      "record_count": 12,
      "page_size": 3,
      "data": [
        {
          "doc_id": "5d4c0e0e5a7b4b5c9d2f6a1b3c8e7f90",
          "title": "検索ガイド",
          "url_link": "https://fess.codelibs.org/ja/stable/user/index.html",
          "content_description": "Fess の<strong>検索</strong><strong>ガイド</strong>です。..."
        }
      ]
    }

``response`` には、ほかに ``page_count``、``next_page``、``exec_time``、``query_id`` などが入ります。
``data`` の各要素に入るのは ``title``、``url``、``url_link``、``content_description``、``last_modified``、``filetype``、``score`` など、API 応答用に許可されたフィールドだけです。
本文全体（``content``）とラベル（``label``）は既定では返りません。
返すフィールドを増やす場合は ``fess_config.properties`` の ``query.additional.api.response.fields`` に追加します。
``content_description`` は検索語を ``<strong>`` タグで囲んだ抜粋なので、画面に出すときは HTML として扱うかタグを除去してください。

よく使うパラメーターは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - パラメーター
     - 意味
   * - ``q``
     - 検索語。検索画面と同じ構文（AND、OR、除外、フィールド指定など）が使えます
   * - ``num`` / ``start``
     - 1 ページの件数（既定 10、上限を超えると上限に丸められます）と開始位置（0 始まり）
   * - ``sort``
     - 並び順。例: ``last_modified.desc`` （更新日時の新しい順）
   * - ``fields.label``
     - ラベルの値で絞り込み。繰り返し指定できます

ほかのパラメーター（ファセット、言語、位置情報など）は `検索 API <https://fess.codelibs.org/ja/stable/api/api-search.html>`__ を参照してください。

ラベル・サジェスト・人気ワードも同じ要領で呼べます。

::

    $ curl -s "http://localhost:8080/api/v2/labels" | jq .response
    $ curl -s -G "http://localhost:8080/api/v2/suggest-words" --data-urlencode "q=fe" | jq .response
    $ curl -s "http://localhost:8080/api/v2/popular-words" | jq .response

それぞれ ``response.labels[]`` （``label`` と ``value``）、 ``response.suggest_words[]`` （``text`` と ``types``）、 ``response.popular_words`` （文字列の配列）に結果が入ります。
サジェストと人気ワードが空になる理由は「ラベル・サジェスト・人気ワードを使う」で説明します。

アクセストークンを作る
======================

業務システムからの呼び出しには、アクセストークンを使います。
トークンには「パーミッション」を持たせ、そのパーミッションで検索結果が絞り込まれます。

作成手順
--------

1. 管理画面の［システム］>［アクセストークン］を開き、［新規作成］をクリックします。
2. 「名前」に用途が分かる名前（例: ``crm-search``）を入力します。
3. 「パーミッション」に、このトークンで見せてよい文書のロールを 1 行に 1 つずつ書きます。書式は ``{role}ロール名``、``{group}グループ名``、``{user}ユーザー名`` です。
4. 「有効期限」を ``2027-03-31T23:59:59`` の形式で入力します。空欄なら期限はありません。
5. 「パラメーター名」は空欄のままにします。
6. ［作成］をクリックします。一覧に戻ったら名前をクリックし、詳細画面の「トークン」に表示される値（英数字 60 文字）を控えます。

「パラメーター名」を設定すると、呼び出し側がそのリクエストパラメーターでパーミッションを追加できるようになります。
呼び出し側を完全に管理できる場合以外は使わないでください。

トークンの送り方
----------------

トークンは ``Authorization`` ヘッダーで送ります。
``Bearer`` を付けない ``Authorization: <トークン>`` も受け付けます。

::

    $ export FESS_SEARCH_TOKEN=<控えたトークン>
    $ curl -s -G "http://localhost:8080/api/v2/search" \
        -H "Authorization: Bearer $FESS_SEARCH_TOKEN" \
        --data-urlencode "q=提案書" | jq '.response.record_count'

クエリーパラメーターでトークンを渡す方法は、 ``api.access.token.request.parameter`` が既定で空のため無効です。
URL はアクセスログに残るので、ヘッダーを使ってください。

トークンのロールで結果が決まる
------------------------------

トークン付きのリクエストでは、トークンのパーミッションだけがロールとして使われます。
トークンを付けない匿名の呼び出しに付くゲストロール（``{role}guest``）は、トークンのパーミッションが空でない限り付きません。

一方、クロール設定を新規作成するとパーミッション欄には ``{role}guest`` が入っているため、通常の公開文書には ``{role}guest`` が付いています。
そのため、パーミッションを ``{group}sales`` だけにしたトークンでは、公開文書が検索結果から消えます。
公開文書と営業部向けの文書の両方を返したい場合は、トークンのパーミッションを次のように 2 行にします。

::

    {role}guest
    {group}sales

設定したら、同じ検索語でトークンなしとトークン付きの ``record_count`` を比べ、想定どおり増減することを確かめてください。
文書側のパーミッションの設計は :doc:`guide-05` で扱います。

ブラウザーにトークンを渡さない理由
----------------------------------

- ブラウザーの JavaScript に書いたトークンは、開発者ツールで誰でも読み取れます。読み取った人は、トークンのパーミッションで見える文書をすべて、業務システムを通さずに検索できます。
- トークンは利用者ごとのものではなく、発行時に指定したパーミッションをひとまとめにしたものです。ブラウザーに配ると、利用者ごとの権限の違いがなくなります。
- 「ログインが必要」をオンにしていても、有効なトークンがあれば ``/search``、``/documents/all``、``/documents/export``、``/suggest-words``、``/labels``、``/popular-words`` はログインなしで応答します。漏れたトークンは、ログインの代わりとして使えてしまいます。

業務システムの利用者によって見せる範囲を変えたい場合は、範囲ごとにトークンを分け、サーバー側で利用者に応じて使い分けます。

サーバー側から検索 API を呼ぶ
=============================

業務システムのバックエンドに置く Python の関数の例です。
標準ライブラリだけを使い、検索結果を画面に必要な項目だけに絞って返します。

.. code-block:: python

    import json
    import os
    import urllib.error
    import urllib.parse
    import urllib.request

    FESS_URL = os.environ.get("FESS_URL", "http://localhost:8080")
    FESS_SEARCH_TOKEN = os.environ["FESS_SEARCH_TOKEN"]


    class FessApiError(Exception):
        def __init__(self, http_status, code, retry_after=None):
            super().__init__(f"Fess API error: {http_status} {code}")
            self.http_status = http_status
            self.code = code
            self.retry_after = retry_after


    def search_documents(query, label=None, num=5):
        params = [("q", query), ("num", str(num))]
        if label:
            params.append(("fields.label", label))
        url = FESS_URL + "/api/v2/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + FESS_SEARCH_TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                body = json.load(res)
        except urllib.error.HTTPError as e:
            try:
                code = json.load(e)["response"]["error"]["code"]
            except (ValueError, KeyError, TypeError):
                code = "unknown"
            raise FessApiError(e.code, code, e.headers.get("Retry-After")) from e
        response = body["response"]
        return {
            "total": response["record_count"],
            "items": [
                {
                    "title": doc.get("title"),
                    "url": doc.get("url_link"),
                    "snippet": doc.get("content_description"),
                    "last_modified": doc.get("last_modified"),
                }
                for doc in response["data"]
            ],
        }

CRM の顧客画面なら ``search_documents("株式会社サンプル", label="sales_docs")`` のように顧客名とラベルを渡し、戻り値をそのまま画面に描画します。

- タイムアウトは、Fess 側の検索タイムアウト（``query.timeout`` 、既定 10000 ミリ秒）より少し長めにしています。
- ``FessApiError`` の ``code`` と ``retry_after`` を見て、利用者へのメッセージと再試行を決めます（「エラーへの対処」を参照）。
- ``content_description`` は ``<strong>`` タグを含むため、テンプレートで HTML として出力する場合は、許可するタグを ``<strong>`` に限ってください。

外部システムのデータを登録する
==============================

クロールできないデータ（業務システムが生成するレポート、チケットの要約など）は、管理 API の ``PUT /api/admin/documents/bulk`` で直接インデックスに登録できます。

管理 API 用のトークンを分ける
-----------------------------

管理 API には、パーミッションに ``{role}admin-api`` を持つトークンが必要です（``api.admin.access.permissions=Radmin-api``）。
このパーミッションでは管理 API の全エンドポイントが許可されます。
文書登録だけに絞った権限はありません。
クロール設定、ユーザー、アクセストークン自体も操作できるため、管理者のパスワードと同じように扱って保管してください。

また、 ``{role}admin-api`` だけのトークンで検索すると、ロールが ``admin-api`` だけになるため、ほとんどの文書が返りません。
検索用と登録用でトークンを分けてください。
［システム］>［アクセストークン］で、パーミッションを ``{role}admin-api`` の 1 行だけにしたトークン（例: 名前 ``crm-indexer``）をもう 1 つ作り、値を控えます。

::

    $ export FESS_ADMIN_TOKEN=<控えた管理 API 用トークン>

登録する
--------

``url`` と ``title`` が必須です。
``content`` は本文、 ``label`` はラベルの値の配列です。

::

    $ curl -s -X PUT "http://localhost:8080/api/admin/documents/bulk" \
        -H "Authorization: Bearer $FESS_ADMIN_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "documents": [
            {
              "url": "https://crm.example.com/reports/2026-11",
              "title": "2026年11月 営業月報",
              "content": "11月の新規商談は前月より増加しました。",
              "label": ["sales_docs"]
            }
          ]
        }' | jq .response

成功すると、文書ごとの結果が ``items`` に返ります。
新規作成は ``CREATED`` 、既存文書の更新は ``OK`` です。

.. code-block:: json

    {
      "version": "15.9",
      "status": 0,
      "items": [
        { "result": "CREATED", "id": "9c1e47b2...e04b" }
      ]
    }

``id`` は ``url`` などから計算したハッシュ値（16 進数 128 桁）で、上の例では途中を省略しています。
登録した文書は、検索用トークンで ``q=営業月報`` を検索して見つかれば完了です。

登録時の注意
------------

- ``role`` を省略すると、ゲストロールが付いて誰でも検索できる文書になります。見せる範囲を限る場合は、 ``role`` に内部形式の値を配列で入れます。内部形式は ``{role}x`` が ``Rx``、``{group}x`` が ``2x``、``{user}x`` が ``1x`` です（例: ``"role": ["2sales"]``）。
- 文書の ID は ``url`` と ``role`` （と仮想ホスト）から作られます。同じ ``url`` で送り直すと更新になりますが、 ``role`` を変えて送ると別の文書として追加され、古い文書が残ります。
- レスポンスの ``items[].id`` はインデックス上の ID で、文書の ``doc_id`` とは別の値です。1 件ずつ削除する ``DELETE /api/admin/searchlist/doc/{id}`` には検索結果の ``doc_id`` を渡します。条件でまとめて消す場合は ``DELETE /api/admin/searchlist/query`` を使います（ `検索リスト API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-searchlist.html>`__ ）。
- 一部の文書だけ失敗した場合は、 ``status`` が 9 になり、失敗した要素に ``message`` が入ります。 ``url`` や ``title`` の欠落、型の合わない値など、リクエスト自体が不正な場合は ``status`` が 1 になり、何も登録されません。

ラベル・サジェスト・人気ワードを使う
====================================

ラベルでカテゴリーを作る
------------------------

``fields.label`` で絞り込むラベルは、［クローラー］>［ラベル］で作成します。
「値」に使える文字は英数字とアンダースコアだけです（``sales-docs`` や日本語は使えません）。
クロールした文書には、ラベルの「対象とするパス」に URL が一致したときにラベルが付きます（:doc:`guide-04`）。
bulk 登録する文書には、前の節のように ``label`` を送ります。

``/api/v2/labels`` は、呼び出し元のロールで使えるラベルだけを返します。
ラベルにもパーミッションがあるため、トークンのパーミッションと合わないラベルは一覧に出ません。
ポータルのカテゴリー一覧は、このレスポンスの ``label`` （表示名）と ``value`` （``fields.label`` に渡す値）から作ります。

サジェスト
----------

``/api/v2/suggest-words`` は ``q`` の前方一致で候補を返します。
件数は ``num`` （既定 10）で、対象フィールドは ``fn`` を繰り返して指定します。
候補の元は、クロールした文書の語（［システム］>［全般］の「ドキュメントでサジェスト」）、検索語（同「検索語でサジェスト」）、管理者が登録したサジェストワードです。
文書の語は、スケジューラの「Suggest Indexer」ジョブ（既定で 1 日 1 回）が実行されるまで候補に出ません。
候補も呼び出し元のロールで絞り込まれます。

人気ワード
----------

``/api/v2/popular-words`` は、検索ログから集めた検索語のうち、よく検索された語を返します。
空の配列が返る場合は、次の点を確認してください。

- ［システム］>［全般］の「人気ワードのレスポンス」（``web.api.popularword`` 、既定オン）がオフだと、 ``invalid_request`` （HTTP 400）になります。
- 「検索語でサジェスト」がオンであること。検索語はこの設定がオンのときだけ集められます。
- 同じ語が 10 回以上検索されていること（\ ``suggest.popular.word.query.freq=10``\ ）。同じセッションからの繰り返しの検索は、1 分以内なら 1 回として数えられます。導入直後は空なのが普通です。
- 集計の対象は、ゲストロールだけで行われた検索です（``suggest.search.log.permissions={user}guest,{role}guest``）。 ``{group}sales`` などを持つトークンやログイン利用者の検索は数えられません。
- 人気ワードも呼び出し元のロールで絞り込まれます。集計される語にはゲストロールしか付かないため、パーミッションに ``{role}guest`` を含まないトークンでは常に空になります。
- 結果はキャッシュされるため、検索が増えてもすぐには変わりません。

``seed`` を変えると、候補の中から別の組み合わせが返ります。

エラーへの対処
==============

``/api/v2`` は、エラー時に HTTP ステータスと ``response.error.code`` を返します。

::

    {"response": {"status": 1, "error": {"code": "invalid_request", "message": "..."}}}

連携先で扱いを決めておくべきものは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - HTTP
     - ``error.code``
     - 原因と対処
   * - 400
     - ``invalid_request``
     - ``num`` が 0 以下、検索語の構文誤り、 ``q`` が ``api.param.max.length`` （既定 1000 文字）を超えたなど。再試行せず、入力を見直します
   * - 401
     - ``auth_required``
     - 未登録・期限切れのトークン、または「ログインが必要」がオンでトークンなし。無効なトークンを付けると、匿名扱いには戻らず 401 になります。トークンを作り直します
   * - 503
     - ``service_unavailable``
     - 検索エンジンが処理しきれずに検索を拒否した。 ``Retry-After: 5`` が付くので、5 秒待って再試行できます
   * - 500
     - ``internal_error``
     - Fess 内部のエラー。［システム情報］>［ログファイル］の ``fess.log`` を確認します

レート制限は、ログイン、パスワード変更、チャット、エクスポートの各エンドポイントに個別の上限があり、超えると 429 ``rate_limited`` と ``Retry-After`` が返ります。
サーバー全体のリクエスト数の制限（``rate.limit.enabled``）は既定で無効です。
有効にした場合、超過時の 429 の本文は ``{"error":"rate_limit_exceeded", ...}`` で、上の ``response`` の形ではありません。
業務システムのサーバーから呼ぶ場合は、すべての検索が同じ IP アドレスから届く点に注意してください。
詳細は `レート制限 <https://fess.codelibs.org/ja/stable/config/rate-limiting.html>`__ を参照してください。

管理 API（``/api/admin/*``）では、エラーの形が異なります。
トークンがない、または ``{role}admin-api`` を持たない場合は HTTP 401 で、 ``response.status`` が 3、理由は ``response.message`` に入ります。

ブラウザーから直接呼ぶ場合（CORS）
==================================

サーバー間の呼び出しには CORS は関係しません。
ブラウザーの JavaScript から別オリジンの Fess を直接呼ぶ場合にだけ、 ``fess_config.properties`` の ``api.cors.allow.origin`` （既定 ``*``）、 ``api.cors.allow.methods``、``api.cors.allow.headers`` （既定で ``Authorization`` を含む）、 ``api.cors.allow.credentials`` （既定 ``true``）、 ``api.cors.max.age`` （既定 ``3600`` 秒）が効きます。

``api.cors.allow.origin`` が ``*`` のときは、Cookie などの認証情報付きのリクエストは許可されません。
ログイン済みの利用者の権限でブラウザーから検索させる場合は、 ``https://portal.example.com`` のようにオリジンを列挙します（カンマ区切り）。
Docker では ``FESS_JAVA_OPTS`` に ``-Dfess.config.api.cors.allow.origin=https://portal.example.com`` を指定する方法もあります。
変更後は Fess を再起動してください。
ブラウザー側の組み込み方は :doc:`guide-03` を参照してください。

次に読む記事
============

- 既存サイトに検索窓や検索画面を組み込みたい: :doc:`guide-03`
- トークンや利用者ごとに見える文書を設計したい: :doc:`guide-05`
- ヘルスチェックや監視に API を使いたい: :doc:`guide-10`
- 管理 API と fessctl で設定をコード管理したい: :doc:`guide-16`
- SSO やアクセストークンの運用を含めて検索基盤を守りたい: :doc:`guide-15`

参考資料
========

- `API の概要 <https://fess.codelibs.org/ja/stable/api/api-overview.html>`__
- `検索 API <https://fess.codelibs.org/ja/stable/api/api-search.html>`__
- `ラベル API <https://fess.codelibs.org/ja/stable/api/api-label.html>`__
- `サジェスト API <https://fess.codelibs.org/ja/stable/api/api-suggest.html>`__
- `人気ワード API <https://fess.codelibs.org/ja/stable/api/api-popularword.html>`__
- `Documents API <https://fess.codelibs.org/ja/stable/api/admin/api-admin-documents.html>`__
- `Admin API 概要 <https://fess.codelibs.org/ja/stable/api/admin/api-admin-overview.html>`__
- `アクセストークン <https://fess.codelibs.org/ja/stable/admin/accesstoken-guide.html>`__
