========
ラベルAPI
========

ラベルの取得
=========

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v1/labels``
==================  ====================================================

|Fess| に、 ``http://<Server Name>/api/v1/labels`` のリクエストを送ることで、|Fess| に登録されているラベルの一覧をJSON形式で受け取ることができます。

リクエストパラメーター
-----------------

使用できるリクエストパラメーターはありません。


レスポンス
--------

以下のようなレスポンスが返ります。

::

    {
      "record_count": 9,
      "data": [
        {
          "label": "AWS",
          "value": "aws"
        },
        {
          "label": "Azure",
          "value": "azure"
        }
      ]
    }

各要素については以下の通りです。

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - ラベルの登録件数。
   * - data
     - 検索結果の親要素。
   * - label
     - ラベルの名前。
   * - value
     - ラベルの値。

表: レスポンス情報

使用例
====

curlコマンドでのリクエスト例:

::

    curl "http://localhost:8080/api/v1/labels"

JavaScriptでのリクエスト例:

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('ラベル一覧:', data.data);
      });

エラーレスポンス
==============

ラベルAPIが失敗した場合、以下のようなエラーレスポンスが返されます。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス

   * - ステータスコード
     - 説明
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合
