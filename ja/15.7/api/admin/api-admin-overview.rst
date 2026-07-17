==========================
Admin API 概要
==========================

概要
====

|Fess| Admin APIは、管理機能にプログラムからアクセスするためのRESTful APIです。
クロール設定、ユーザー管理、スケジューラー制御など、管理画面で行える操作のほとんどをAPI経由で実行できます。

このAPIを使用することで、|Fess| の設定を自動化したり、外部システムと連携したりすることが可能です。

ベースURL
=========

Admin APIのベースURLは以下の形式です:

::

    http://<Server Name>/api/admin/

例えば、ローカル環境の場合:

::

    http://localhost:8080/api/admin/

認証
====

Admin APIにアクセスするには、アクセストークンによる認証が必要です。

アクセストークンの取得
----------------------

1. 管理画面にログイン
2. 「システム」→「アクセストークン」に移動
3. 「新規作成」をクリック
4. トークン名を入力し、「権限」欄にトークンへ付与する権限を設定（Admin API を利用する場合は ``{role}admin-api`` を入力）
5. 「作成」をクリックしてトークンを取得

トークンの使用
--------------

リクエストヘッダーにアクセストークンを含めます:

::

    Authorization: Bearer <アクセストークン>

``Bearer`` を省略し、トークンのみを指定することもできます:

::

    Authorization: <アクセストークン>

クエリパラメーターによる指定も可能ですが、既定では無効です。\ ``fess_config.properties`` の
``api.access.token.request.parameter`` にパラメーター名を設定すると、その名前で
トークンを渡せるようになります（既定値は空のため、ヘッダーによる指定のみが有効です）。
たとえば ``api.access.token.request.parameter=token`` を設定した場合:

::

    ?token=<アクセストークン>

cURL例
~~~~~~

.. code-block:: bash

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "http://localhost:8080/api/admin/scheduler/settings"

必要な権限
----------

Admin APIへのアクセスは、機能ごとではなく単一の権限セットで制御されます。Admin APIの
いずれかのエンドポイントを利用するには、アクセストークンに ``fess_config.properties`` の
``api.admin.access.permissions`` で設定された権限のいずれかが付与されている必要があります。

既定値は ``Radmin-api`` で、これはロール ``admin-api`` をエンコードした形式です
（先頭の ``R`` は ``role.search.role.prefix`` の値）。アクセストークンの作成時に、
権限欄へ ``{role}admin-api`` と入力すると、内部的に ``Radmin-api`` として保存されます。

.. note::

   個別のリソースごとに異なる権限（``admin-scheduler`` や ``admin-user`` など）や、
   ワイルドカード（``admin-*``）は存在しません。設定された権限を持つトークンは、
   すべての Admin API エンドポイントにアクセスできます。アクセスを許可する権限を
   変更したい場合は、``api.admin.access.permissions`` の値を変更してください。

共通パターン
============

設定を持つリソース（webconfig、user、role など）は、以下の共通的なCRUDパターンに従います。
ただし、一部のリソース（systeminfo、stats、storage、plugin、log、backup、documents、suggest、dict ルート等）は
この共通パターンとは異なる独自のエンドポイント構成を持つため、各リソースのページを参照してください。

一覧取得（GET /settings）
-------------------------

設定の一覧を取得します。

リクエスト
~~~~~~~~~~

::

    GET /api/admin/<resource>/settings

パラメーター（ページネーション）:

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - パラメーター
     - 型
     - 説明
   * - ``size``
     - Integer
     - 1ページあたりの件数（デフォルト: 25。\ ``fess_config.properties`` の ``paging.page.size`` で変更可能）
   * - ``page``
     - Integer
     - ページ番号（1から開始。デフォルト: 1。0以下を指定した場合は1として扱われます）

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [...],
        "total": 100
      }
    }

.. note::

   すべてのレスポンスの ``response`` オブジェクトには、製品バージョンを示す ``version``
   （例: ``"15.7.0"``）が常に含まれます。以降の例では簡潔さのために省略している場合があります。

単一設定取得（GET /setting/{id}）
---------------------------------

IDを指定して単一の設定を取得します。

リクエスト
~~~~~~~~~~

::

    GET /api/admin/<resource>/setting/{id}

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {...}
      }
    }

新規作成（POST /setting）
-------------------------

新しい設定を作成します。

リクエスト
~~~~~~~~~~

::

    POST /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "name": "...",
      "...": "..."
    }

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "created_id",
        "created": true
      }
    }

更新（PUT /setting）
--------------------

既存の設定を更新します。

リクエスト
~~~~~~~~~~

::

    PUT /api/admin/<resource>/setting
    Content-Type: application/json

    {
      "id": "...",
      "name": "...",
      "...": "..."
    }

レスポンス
~~~~~~~~~~

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "updated_id",
        "created": false
      }
    }

削除（DELETE /setting/{id}）
----------------------------

設定を削除します。

リクエスト
~~~~~~~~~~

::

    DELETE /api/admin/<resource>/setting/{id}

レスポンス
~~~~~~~~~~

削除レスポンスの形式はリソース（アクション）ごとに異なります。多くのリソースは
``status`` のみを返します。

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

一部のリソースでは、削除結果が ``ApiUpdateResponse`` として返され、削除した設定の
``id`` と ``created``\ （削除時は ``false``）が付与されます。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_id",
        "created": false
      }
    }

また、``ApiDeleteResponse`` を返すリソースでは、削除件数を示す ``count``
（既定値 ``1``）が付与される場合があります。実際の形式は各リソースのページを参照してください。

レスポンス形式
==============

すべてのレスポンスは ``response`` オブジェクトでラップされ、製品バージョンを示す
``version`` と、処理結果を示す ``status`` を常に含みます。

``status`` の値は以下のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 値
     - 説明
   * - ``0``
     - OK（成功）
   * - ``1``
     - BAD_REQUEST（リクエスト不正）
   * - ``2``
     - SYSTEM_ERROR（システムエラー）
   * - ``3``
     - UNAUTHORIZED（認証エラー）
   * - ``9``
     - FAILED（処理失敗）

成功レスポンス
--------------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "...": "..."
      }
    }

``status: 0`` は成功を示します。

エラーレスポンス
----------------

エラー時は ``status`` に 0 以外の値が設定され、``message`` にエラーメッセージが
含まれます。

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to process the request."
      }
    }

HTTPステータスコード
--------------------

Admin APIは、ほとんどの場合 HTTP ステータス ``200`` を返し、処理結果はレスポンス本文の
``status`` フィールドで表します。そのため、成功・失敗の判定は HTTP ステータスコードではなく、
本文の ``status`` の値で行ってください。

実際に返される HTTP ステータスコードは以下のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - コード
     - 説明
   * - 200
     - 通常のレスポンス。成功時（``status: 0``）に加えて、ほとんどのエラーもこのコードで
       返されます。たとえば、アクセストークンが未指定・無効な場合や権限が不足している場合は
       ``status: 3``、システムエラーは ``status: 2`` として、いずれも HTTP ``200`` で返されます。
   * - 400
     - リクエストパラメーターの検証エラー。レスポンス本文の ``status`` は ``1`` になります。
       存在しないリソースを取得しようとした場合もこのコードで返されます。
   * - 401
     - ログイン認証に関する例外が発生した場合。レスポンス本文の ``status`` は ``3`` になります。
       なお、アクセストークンが未指定・無効な場合は、このコードではなく HTTP ``200`` で
       ``status: 3`` が返されます。

.. note::

   Admin APIでは ``403``、``404``、``500`` といった HTTP ステータスコードは返されません。
   権限不足やリソースの不存在も、HTTP ``200`` または ``400`` のレスポンス本文に含まれる
   ``status`` で示されます。

利用可能なAPI
=============

|Fess| は以下のAdmin APIを提供しています。

クロール設定
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-webconfig`
     - Webクロール設定
   * - :doc:`api-admin-fileconfig`
     - ファイルクロール設定
   * - :doc:`api-admin-dataconfig`
     - データストア設定

.. note::

   このほか、認証情報やクロール制御に関する以下のリソースもAPIとして提供されています
   （現時点では個別ページは未整備です）: ``webauth``\ （Web認証）、``fileauth``\ （ファイル認証）、
   ``reqheader``\ （リクエストヘッダー）、``pathmap``\ （パスマッピング）、
   ``duplicatehost``\ （重複ホスト）、``searchlist``\ （検索/ドキュメント一覧操作）。

インデックス管理
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-documents`
     - ドキュメント一括操作
   * - :doc:`api-admin-crawlinginfo`
     - クロール情報
   * - :doc:`api-admin-failureurl`
     - 障害URL管理
   * - :doc:`api-admin-backup`
     - バックアップ/リストア

スケジューラー
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-scheduler`
     - ジョブスケジューリング
   * - :doc:`api-admin-joblog`
     - ジョブログ取得

ユーザー・権限管理
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-user`
     - ユーザー管理
   * - :doc:`api-admin-role`
     - ロール管理
   * - :doc:`api-admin-group`
     - グループ管理
   * - :doc:`api-admin-accesstoken`
     - APIトークン管理

検索チューニング
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-labeltype`
     - ラベルタイプ
   * - :doc:`api-admin-keymatch`
     - キーマッチ
   * - :doc:`api-admin-boostdoc`
     - ドキュメントブースト
   * - :doc:`api-admin-elevateword`
     - エレベートワード
   * - :doc:`api-admin-badword`
     - NGワード
   * - :doc:`api-admin-relatedcontent`
     - 関連コンテンツ
   * - :doc:`api-admin-relatedquery`
     - 関連クエリ
   * - :doc:`api-admin-suggest`
     - サジェスト管理

システム
--------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-general`
     - 一般設定
   * - :doc:`api-admin-systeminfo`
     - システム情報
   * - :doc:`api-admin-stats`
     - システム統計
   * - :doc:`api-admin-log`
     - ログ取得
   * - :doc:`api-admin-searchlist`
     - ドキュメント検索・管理
   * - :doc:`api-admin-storage`
     - ストレージ管理
   * - :doc:`api-admin-plugin`
     - プラグイン管理

辞書
----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - エンドポイント
     - 説明
   * - :doc:`api-admin-dict`
     - 辞書管理（シノニム、ストップワード等）

使用例
======

Webクロール設定の作成
---------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Example Site",
           "urls": "https://example.com/",
           "includedUrls": ".*example.com.*",
           "excludedUrls": "",
           "userAgent": "Mozilla/5.0 (compatible; Fess)",
           "numOfThread": 1,
           "intervalTime": 1000,
           "boost": 1.0,
           "maxAccessCount": 1000,
           "depth": 3,
           "sortOrder": 1,
           "available": "true"
         }'

.. note::

   Webクロール設定の作成では、``name``、``urls``、``userAgent``、``numOfThread``、
   ``intervalTime``、``boost``、``available``、``sortOrder`` が必須です。これらを
   省略すると検証エラー（``status: 1``）になります。\ ``available`` は文字列で指定し、
   ``"true"`` または ``"false"`` を設定します。

スケジュールジョブの開始
------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

ユーザーの一覧取得
------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/user/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

参考情報
========

- :doc:`../api-overview` - API概要
- :doc:`../../admin/accesstoken-guide` - アクセストークン管理ガイド
