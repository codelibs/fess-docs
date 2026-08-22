===========
人気ワードAPI
===========

人気ワード一覧の取得
===============

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/popular-words``
==================  ====================================================

|Fess| に、 ``http://<Server Name>/api/v2/popular-words?seed=123`` のようなリクエストを送ることで、人気検索ワードの一覧をJSON形式で受け取ることができます。

``web.api.popularword=false`` の場合、このAPIは ``invalid_request`` （HTTP 400）を返します（v1 の「unsupported operation」相当の挙動です）。

レスポンスの共通エンベロープおよびエラーモデルについては :doc:`api-overview` を参照してください。

リクエストパラメーター
-----------------

使用できるリクエストパラメーターは以下の通りです。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: リクエストパラメーター

   * - seed
     - 人気ワードを取得するシード（文字列）。この値により異なるパターンの単語を取得できます。 (例) ``seed=123``
   * - label
     - フィルターするラベル名。繰り返し指定することで配列として扱われます。 (例) ``label=java``
   * - field
     - 人気ワードを生成するフィールド名。繰り返し指定することで配列として扱われます。 (例) ``field=label``

レスポンス
--------

成功時には、以下のような共通エンベロープ形式のレスポンスが返ります。

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

``response`` の各要素については以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: レスポンス情報

   * - record_count
     - 人気ワードの件数（整数）。
   * - popular_words
     - 人気ワードの配列（文字列の配列）。

.. note::

   v2 では、人気ワードは ``popular_words`` （文字列の配列）として返されます（v1 の ``data`` ではありません）。

使用例
====

curlコマンドでのリクエスト例:

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

エラーレスポンス
==============

人気ワードAPIが失敗した場合、共通のエラーエンベロープが返されます。エラーモデルの詳細は :doc:`api-overview` を参照してください。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス

   * - ステータスコード
     - 説明
   * - 400 Bad Request
     - リクエストが不正な場合（ ``web.api.popularword=false`` で機能が無効な場合を含む）。 ``error.code`` は ``invalid_request`` です。
   * - 405 Method Not Allowed
     - サポートされていない HTTP メソッドが指定された場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。
