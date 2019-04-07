==================
ラベルAPI
==================

ラベルの取得
============

|Fess| に、 ``http://<Server Name>/json/?type=label`` のリクエストを送ることで、|Fess| に登録されているラベルの一覧をJSON形式で受け取ることができます。

リクエストパラメータ
--------------------

使用できるリクエストパラメータはありません。


レスポンス
----------

以下のようなレスポンスが返ります。

::

    {
        "response":{
            "version":12.6,
            "status":0,
            "record_count":3,
            "result":[
                {"label":"label1", "value":"label1"},
                {"label":"label2", "value":"label2"},
                {"label":"label3", "value":"label3"}
            ]
        }
    }

各要素については以下の通りです。

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - response
     - ルート要素。
   * - version
     - フォーマットバージョン。
   * - status
     - レスポンスのステータス。status値は、0:正常、1:検索エラー、2または3:リクエストパラメータエラー、9:サービス停止中、-1:API種別エラーです。
   * - record_count
     - ラベルの登録件数。
   * - result
     - 検索結果の親要素。
   * - label
     - ラベルの名前。
   * - value
     - ラベルの値。

表: レスポンス情報
