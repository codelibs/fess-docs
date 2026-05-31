==========
キャッシュAPI
==========

このドキュメントでは、 |Fess| の v2 キャッシュ API について説明します。
共通のレスポンスエンベロープ・エラーモデル・CSRF については :doc:`api-overview` を参照してください。

ベースURLは ``http://<Server Name>/api/v2/`` です（ローカル環境の例: ``http://localhost:8080/api/v2`` ）。

キャッシュされたドキュメントの取得
==============================

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/cache/{docId}``
==================  ====================================================

ドキュメントのキャッシュされた（ハイライト適用済みの）HTML を返します。

``app.login.required=true`` で呼び出し元が匿名の場合は、 ``auth_required`` (401) になります。

リクエストパラメーター
-----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: リクエストパラメーター

   * - ``docId``
     - ドキュメント識別子（path, 必須, パターン ``^[A-Za-z0-9_-]+$`` ）。
   * - ``hq``
     - ハイライトクエリ語（query）。繰り返し指定可能（配列）。

表: リクエストパラメーター

レスポンス
--------

成功時（200）は、共通エンベロープの ``response`` 直下に以下のフィールドが返ります。

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

各フィールドについては以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: レスポンスフィールド

   * - ``doc_id``
     - ドキュメント ID（str）。
   * - ``mimetype``
     - MIME タイプ（enum: ``text/html`` ）。
   * - ``content``
     - キャッシュされた HTML 本文（str）。
   * - ``url``
     - ドキュメント URL（str）。存在すれば ``url_link`` フィールド、なければインデックスの生 URL。どちらもないときは省略されます。
   * - ``created``
     - インデックスのドキュメント作成タイムスタンプ（str）。存在しないときは省略されます。
   * - ``charset``
     - ドキュメントの mimetype から解析した文字セット（str）。ない場合は ``UTF-8`` が既定値です。

表: レスポンスフィールド

エラーレスポンス
------------

エラーモデルの詳細は :doc:`api-overview` を参照してください。このエンドポイントが返す HTTP ステータスは以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス

   * - ステータスコード
     - 説明
   * - 400 Bad Request
     - リクエストが不正な場合。
   * - 401 Unauthorized
     - 認証が必要な場合（ ``app.login.required=true`` で匿名の呼び出し元）。
   * - 404 Not Found
     - リソースが見つからない場合。
   * - 405 Method Not Allowed
     - HTTP メソッドが許可されていない場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。

表: エラーレスポンス
