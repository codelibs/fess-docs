==========================
SearchList API
==========================

概要
====

SearchList APIは、|Fess| のインデックス内のドキュメントを検索・管理するためのAdmin APIです。
ドキュメントの検索、取得、作成、更新、削除を操作できます。

レスポンスのフィールド名はすべて ``snake_case`` です。値が ``null`` のフィールドはレスポンスから省略されます。

ベースURL
=========

::

    /api/admin/searchlist

認証
====

このAPIを呼び出すには、:doc:`api-admin-overview` で説明しているアクセストークンによる認証が必要です。
トークンにはAdmin APIへのアクセス権限（既定では ``Radmin-api`` ）が付与されている必要があります。
この権限は設定キー ``api.admin.access.permissions`` で変更できます。

エンドポイント一覧
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - メソッド
     - パス
     - 説明
   * - GET / PUT
     - /docs
     - ドキュメント検索
   * - GET
     - /doc/{id}
     - ドキュメント取得
   * - POST
     - /doc
     - ドキュメント作成
   * - PUT
     - /doc
     - ドキュメント更新
   * - DELETE
     - /doc/{id}
     - ドキュメント削除（ID指定）
   * - DELETE
     - /query
     - ドキュメント削除（クエリ指定）

ドキュメント検索
================

検索条件に一致するドキュメントを検索します。

リクエスト
----------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``q``
     - String
     - いいえ
     - 検索クエリ（最大1000文字）。未指定の場合は全件が対象になります。
   * - ``sort``
     - String
     - いいえ
     - ソートフィールドと方向（例: ``last_modified.desc`` ）。
   * - ``start``
     - Integer
     - いいえ
     - 0始まりの開始位置（既定値 ``0`` ）。
   * - ``offset``
     - Integer
     - いいえ
     - ``start`` からのオフセット（既定値 ``0`` ）。
   * - ``pn``
     - Integer
     - いいえ
     - ページ番号。
   * - ``num``
     - Integer
     - いいえ
     - 取得件数（既定値 ``10`` ）。設定された最大値（既定 ``100`` ）を超える値、または ``0`` 以下の値は最大値にクランプされます。
   * - ``size``
     - Integer
     - いいえ
     - 取得件数（ ``num`` のエイリアス。他のAdmin APIとの互換性のために用意されています）。
   * - ``lang``
     - String[]
     - いいえ
     - 検索言語。繰り返し指定可能（配列）。例: ``en`` 。
   * - ``ex_q``
     - String[]
     - いいえ
     - 追加のクエリ式。繰り返し指定可能（配列）。
   * - ``fields.<name>``
     - String[]
     - いいえ
     - フィールド値でフィルターします。最も一般的な例は ``fields.label`` （ラベル名でのフィルター）で、任意の ``fields.<name>`` はドキュメントフィールド ``<name>`` が指定値に一致する結果に絞り込みます。繰り返し指定可能。
   * - ``as.<name>``
     - String[]
     - いいえ
     - 高度な検索条件。任意の ``as.<name>`` （例: ``as.q`` ）が高度な検索条件ビルダーに渡されます。name ごとに繰り返し指定可能。
   * - ``sdh``
     - String
     - いいえ
     - 類似ドキュメントハッシュ（similar-document hash）。

.. note::

   このエンドポイントはファセット・ハイライト・地理（geo）検索には対応していません。これらのパラメーターを指定しても無視されます。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "サンプルページ1",
            "content_description": "..."
          }
        ]
      }
    }

レスポンスフィールド
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``version``
     - 稼働中の |Fess| のバージョン（例の値は説明用です）。
   * - ``status``
     - ステータスコード（ ``0`` は成功。詳細は「ステータスコード」を参照）。
   * - ``query_id``
     - 検索クエリID。
   * - ``docs``
     - 検索結果ドキュメントの配列。各ドキュメントはフィールド名と値のマップで、インデックスのフィールド名（ ``doc_id`` , ``url`` , ``title`` , ``content_description`` など）がそのまま使われます。
   * - ``exec_time``
     - 検索実行時間（秒、文字列）。
   * - ``query_time``
     - 検索エンジンのクエリ時間（ミリ秒）。
   * - ``page_size``
     - 1ページあたりの件数。
   * - ``page_number``
     - 現在のページ番号。
   * - ``record_count``
     - 該当件数。
   * - ``record_count_relation``
     - 該当件数の関係。 ``eq`` は正確な件数、 ``gte`` は下限のみ判明していることを示します。
   * - ``page_count``
     - 総ページ数。
   * - ``next_page``
     - 次ページの有無（bool）。
   * - ``prev_page``
     - 前ページの有無（bool）。
   * - ``start_record_number``
     - このページの開始レコード番号。
   * - ``end_record_number``
     - このページの終了レコード番号。
   * - ``page_numbers``
     - ページャーに表示するページ番号の配列（文字列）。
   * - ``partial``
     - 結果が部分的かどうか（bool）。
   * - ``search_query``
     - 実際に実行された検索クエリ。
   * - ``requested_time``
     - リクエスト時刻（epoch ミリ秒）。
   * - ``highlight_params``
     - ハイライト用のクエリパラメーター文字列（この管理APIでは通常空です）。

ドキュメント取得
================

ドキュメントIDを指定して、1件のドキュメントを取得します。

リクエスト
----------

::

    GET /api/admin/searchlist/doc/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - ドキュメントID（ ``doc_id`` の値。パスパラメーター）。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "サンプルページ1"
        }
      }
    }

指定したIDのドキュメントが存在しない場合は、エラーレスポンス（ ``status`` = ``1`` ）が返ります。

ドキュメント作成
================

新しいドキュメントをインデックスに作成します。

リクエスト
----------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "サンプルページ1",
        "content": "本文テキストです。",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``doc``
     - はい
     - 登録するドキュメント。インデックスのフィールド名と値のマップで指定します。

``doc`` に指定するフィールドのうち、 ``index.admin.required.fields`` で設定された必須フィールド（既定値 ``url,title,role,boost`` ）はすべて指定する必要があります。
一括登録用の :doc:`Documents API <api-admin-documents>` とは異なり、このエンドポイントは ``role`` や ``boost`` などの既定値を自動補完しないため、必須フィールドはリクエストで明示的に指定してください。
``doc_id`` はサーバー側で自動生成されるため、作成時には指定しません。

各フィールドの値は、フィールドの型設定に従って検証されます。型が一致しない場合はエラー（ ``status`` = ``1`` ）になります。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 設定キー
     - 既定値
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - （空）
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - （空）

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - 登録されたドキュメントの ``doc_id`` 。
   * - ``created``
     - 作成時は ``true`` 。

ドキュメント更新
================

既存のドキュメントを更新します。

リクエスト
----------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

リクエストボディ
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "更新後のタイトル",
        "content": "更新後の本文テキストです。",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

フィールド説明
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - フィールド
     - 必須
     - 説明
   * - ``doc``
     - はい
     - 更新するドキュメント。インデックスのフィールド名と値のマップで指定します。

更新対象のドキュメントは ``doc`` 内の ``doc_id`` で特定されます。 ``doc_id`` が指定されていない、または該当するドキュメントが存在しない場合はエラー（ ``status`` = ``1`` ）になります。
作成時と同様に、 ``index.admin.required.fields`` で設定された必須フィールド（既定値 ``url,title,role,boost`` ）はすべて指定する必要があり、各フィールドの値は型設定に従って検証されます。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 説明
   * - ``id``
     - 更新されたドキュメントの ``doc_id`` 。
   * - ``created``
     - 更新時は ``false`` 。

ドキュメント削除（ID指定）
==========================

ドキュメントIDを指定して削除します。

リクエスト
----------

::

    DELETE /api/admin/searchlist/doc/{id}

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``id``
     - String
     - はい
     - ドキュメントID（ ``doc_id`` の値。パスパラメーター）。

レスポンス
----------

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

ドキュメント削除（クエリ指定）
==============================

検索クエリに一致するドキュメントを一括削除します。

リクエスト
----------

::

    DELETE /api/admin/searchlist/query

パラメーター
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - パラメーター
     - 型
     - 必須
     - 説明
   * - ``q``
     - String
     - はい
     - 削除対象の検索クエリ。

削除対象は「ドキュメント検索」と同じ方法でクエリが構築されるため、 ``fields.<name>`` や ``ex_q`` などの絞り込みパラメーターも併用できます。 ``q`` が未指定の場合はエラー（ ``status`` = ``1`` ）になります。

レスポンス
----------

削除されたドキュメント件数を ``count`` で返します。

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "count": 150
      }
    }

ステータスコード
================

レスポンスの ``status`` フィールドには以下の値が設定されます。

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 値
     - 名称
     - 説明
   * - ``0``
     - OK
     - 成功。
   * - ``1``
     - BAD_REQUEST
     - リクエストが不正（必須フィールドの欠落、型不一致、対象ドキュメントが見つからない、クエリが不正など）。
   * - ``2``
     - SYSTEM_ERROR
     - システムエラー。
   * - ``3``
     - UNAUTHORIZED
     - 認証エラー。
   * - ``9``
     - FAILED
     - 処理に失敗。

使用例
======

ドキュメント検索
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

ドキュメント取得
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

ドキュメント作成
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "サンプルページ1",
             "content": "本文テキストです。",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

クエリ指定でのドキュメント削除
------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`api-admin-overview` - Admin API概要
- :doc:`api-admin-documents` - ドキュメント一括登録API
- :doc:`api-admin-crawlinginfo` - クロール情報API
- :doc:`../../admin/searchlist-guide` - 検索一覧管理ガイド
