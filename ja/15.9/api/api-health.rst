==========
Health API
==========

このドキュメントでは、 |Fess| の v2 Health API について説明します。
共通のレスポンスエンベロープ・エラーモデルについては :doc:`api-overview` を参照してください。

ベースURLは ``http://<Server Name>/api/v2/`` です（ローカル環境の例: ``http://localhost:8080/api/v2`` ）。

状態の取得
========

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/health``
==================  ====================================================

検索エンジンクラスターの状態スナップショットを返します（ ``monitor`` タグ）。
HTTP ステータスは、クラスターの状態が ``GREEN`` / ``YELLOW`` の場合は 200、 ``RED`` の場合、または検索エンジンに接続できない場合は 503 になります。

このエンドポイントはエンベロープの不変条件「 ``status >= 1`` ⇔ HTTP ステータス ``>= 400`` 」を守ります。

- ``GREEN`` / ``YELLOW`` の場合: 成功エンベロープ（ ``status: 0`` ）で ``engine`` を返します。
- ``RED`` の場合: エラーエンベロープ（ ``status: 9`` , ``error.code: service_unavailable`` ）を返し、エンジンスナップショットを ``error.details.engine`` の下に埋め込みます（監視ツールがクラスターメタデータを解析できるようにするため）。
- 検索エンジンに接続できない場合: ``RED`` と同様にエラーエンベロープ（ ``error.code: service_unavailable`` , ``error.message: search engine is not reachable`` ）を返し、 ``error.details.engine`` は ``status: UNAVAILABLE`` 、 ``ping_status: 1`` になります。

``engine`` の各フィールドは以下の通りです。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine フィールド

   * - ``status``
     - クラスターの状態。大文字の ``GREEN`` / ``YELLOW`` / ``RED`` のいずれか。検索エンジンに接続できない場合は ``UNAVAILABLE`` 。
   * - ``ping_status``
     - ping のステータス（int）。クラスターが ``RED`` の場合と、検索エンジンに接続できない場合は ``1`` 、それ以外（ ``GREEN`` / ``YELLOW`` ）の場合は ``0`` になります。

表: engine フィールド

クラスター名（ ``cluster_name`` ）は、このエンドポイントが認証なしで呼び出せるため、返しません。

リクエストパラメーター
-----------------

使用できるリクエストパラメーターはありません。

レスポンス
--------

クラスターが ``GREEN`` / ``YELLOW`` の場合（200）は、成功エンベロープで ``engine`` が返ります。

::

    {
      "response": {
        "status": 0,
        "engine": {
          "status": "GREEN",
          "ping_status": 0
        }
      }
    }

クラスターが ``RED`` の場合（503）は、エラーエンベロープで返り、エンジンスナップショットが ``error.details.engine`` の下に埋め込まれます。

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "status": "RED",
              "ping_status": 1
            }
          }
        }
      }
    }

使用例
====

curl コマンドでのリクエスト例:

::

    curl "http://localhost:8080/api/v2/health"

レスポンス・エラーレスポンス
========================

エラーモデルの詳細は :doc:`api-overview` を参照してください。このエンドポイントが返す HTTP ステータスは以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: レスポンス一覧

   * - ステータスコード
     - 説明
   * - 200 OK
     - クラスターが ``GREEN`` / ``YELLOW`` で到達可能な場合。成功エンベロープに ``engine`` が含まれます。
   * - 405 Method Not Allowed
     - HTTP メソッドが許可されていない場合。
   * - 503 Service Unavailable
     - クラスターが ``RED`` の場合、または検索エンジンに接続できない場合。エラーエンベロープ（ ``error.code: service_unavailable`` ）で ``error.details.engine`` にエンジンスナップショットが含まれます。

表: レスポンス一覧
