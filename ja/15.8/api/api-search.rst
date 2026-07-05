========
検索API
========

このドキュメントでは、 |Fess| の v2 検索 API について説明します。
共通のレスポンスエンベロープ・エラーモデル・CSRF については :doc:`api-overview` を参照してください。

ベースURLは ``http://<Server Name>/api/v2/`` です（ローカル環境の例: ``http://localhost:8080/api/v2`` ）。

ドキュメントの検索
================

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/search``
==================  ====================================================

クエリにマッチするドキュメントを検索し、共通エンベロープで結果を返します。
ペイロード内のフィールド名はすべて ``snake_case`` です。

リクエストパラメーター
-----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: リクエストパラメーター

   * - ``q``
     - 検索語（URLエンコード）。
   * - ``start``
     - 0始まりの開始位置（integer, ``>=0`` , 既定値 ``0`` ）。
   * - ``offset``
     - ``start`` からのオフセット（integer, ``>=0`` , 既定値 ``0`` ）。
   * - ``num``
     - ページサイズ（integer, ``>=1`` , 既定値 ``10`` ）。 ``<= 0`` は ``invalid_request`` になります。設定された最大値を超える値は無言でクランプされます。クランプされたかどうかは、リクエストの ``num`` とレスポンスの ``page_size`` を比較することで検出できます。
   * - ``sort``
     - ソート（例: ``score`` ）。
   * - ``lang``
     - 検索言語。繰り返し指定可能（配列）。例: ``en`` 。
   * - ``ex_q``
     - 追加のクエリ式。繰り返し指定可能。
   * - ``sdh``
     - 類似ドキュメントハッシュ（similar-document hash）。
   * - ``fields.label``
     - ラベル名でフィルターします。繰り返し指定可能。これは汎用的な ``fields.<name>`` ファミリーの最も一般的なケースで、任意の ``fields.<name>`` クエリパラメーターは、ドキュメントフィールド ``<name>`` が指定値に一致する結果に絞り込みます。
   * - ``as.*``
     - 高度な検索条件。任意の ``as.<name>`` （例: ``as.q`` , ``as.filetype`` ）が高度な検索条件ビルダーに渡されます。name ごとに繰り返し指定可能です。
   * - ``track_total_hits``
     - 検索エンジンに転送され、正確なヒット数カウントを制御します（例: ``true`` または整数しきい値）。 ``record_count_relation`` が ``eq`` か ``gte`` かに影響します。
   * - ``facet.field``
     - ファセットフィールド。繰り返し指定可能（配列）。
   * - ``facet.query``
     - ファセットクエリ。繰り返し指定可能（配列）。
   * - ``facet.size``
     - 返すファセット語の最大数（integer）。
   * - ``facet.minDocCount``
     - ファセット語が含まれる最小ドキュメント数（integer）。
   * - ``facet.sort``
     - ファセットのソート。
   * - ``facet.missing``
     - 値を持たないドキュメントに対するファセットの扱い。
   * - ``geo.location.point``
     - 地理座標の中心点（例: ``35.0,139.0`` ）。
   * - ``geo.location.distance``
     - 中心点からの距離（例: ``10km`` ）。

表: リクエストパラメーター

レスポンス
--------

成功時（200）は、共通エンベロープの ``response`` 直下に以下のフィールドが返ります。

::

    {
      "response": {
        "status": 0,
        "q": "Fess",
        "query_id": "f8b1c2d3e4a5",
        "exec_time": 0.012,
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 42,
        "record_count_relation": "eq",
        "page_count": 3,
        "highlight_params": "&hq=Fess",
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "related_query": ["enterprise search"],
        "related_contents": [],
        "data": [
          {
            "doc_id": "a1b2c3d4e5f6",
            "url": "https://example.com/",
            "title": "Example",
            "content_description": "An example document about Fess.",
            "score": 1.2345
          }
        ],
        "facet_field": [
          {
            "name": "label",
            "result": [
              { "value": "news", "count": 12 }
            ]
          }
        ],
        "facet_query": [
          { "value": "filetype:html", "count": 30 }
        ]
      }
    }

各フィールドについては以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: レスポンスフィールド

   * - ``q``
     - 検索語（nullable）。
   * - ``query_id``
     - クエリの識別子。
   * - ``exec_time``
     - 実行時間（double, 秒）。
   * - ``query_time``
     - 検索エンジンのクエリ時間（int64, ミリ秒）。
   * - ``page_size``
     - ページサイズ。
   * - ``page_number``
     - 現在のページ番号。
   * - ``record_count``
     - ヒット件数（int64）。
   * - ``record_count_relation``
     - ``eq`` のときは正確なカウント、 ``gte`` のときは下限のみ判明していることを示します。
   * - ``page_count``
     - 総ページ数。
   * - ``highlight_params``
     - ハイライト用のクエリパラメーター文字列。
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
     - リクエスト時刻（int64, epoch ミリ秒）。
   * - ``related_query``
     - 関連クエリの配列（文字列）。
   * - ``related_contents``
     - 関連コンテンツの配列（文字列）。
   * - ``data``
     - 検索結果の配列。1ドキュメントにつき1要素。 ``QueryFieldConfig#isApiResponseField`` が許可するフィールドのみが含まれ、null や空キーは除外されます。
   * - ``facet_field``
     - ファセットフィールドが要求された場合のみ存在する配列。各要素は ``{name, result:[{value, count}]}`` 。
   * - ``facet_query``
     - ファセットクエリが要求された場合のみ存在する配列。各要素は ``{value, count}`` 。

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
   * - 405 Method Not Allowed
     - HTTP メソッドが許可されていない場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。

表: エラーレスポンス

全ドキュメントの取得（スクロール検索・NDJSON）
=========================================

リクエスト
--------

==================  ====================================================
HTTPメソッド         GET
エンドポイント        ``/api/v2/documents/all``
==================  ====================================================

クエリにマッチするすべてのドキュメントを NDJSON （ ``application/x-ndjson`` ）でストリーム配信します。
各行は ``{"data":{...}}`` オブジェクトで、 ``QueryFieldConfig#isApiResponseField`` が許可するフィールドを含みます。

ストリームの途中で失敗した場合は、最終行に次の行を出力してフラッシュします。

::

    {"error":{"code":"internal_error","message":"stream error"}}

このため、クライアントは最後の行の最初のキーを確認し、正常完了（ ``data`` ）かサーバー異常（ ``error`` ）かを区別しなければなりません。

クエリは ``GET /search`` と同じパラメーターセット（ ``q`` , ``sort`` , ``num`` , ``lang`` , ``ex_q`` , ``sdh`` , ``fields.*`` , ``as.*`` , ``track_total_hits`` , ``facet.*`` , ``geo.*`` ）で構築されます。
``api.search.scroll=false`` でスクロール検索が無効な場合は ``invalid_request`` （400）を返します。

リクエストパラメーター
-----------------

仕様に明示されているパラメーターは以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: リクエストパラメーター

   * - ``q``
     - 検索語。
   * - ``sort``
     - ソート。
   * - ``num``
     - ページ（スクロールバッチ）のサイズ（integer, ``>=1`` ）。 ``<= 0`` は ``invalid_request`` になります。
   * - ``lang``
     - 検索言語。繰り返し指定可能（配列）。
   * - ``ex_q``
     - 追加のクエリ式。繰り返し指定可能（配列）。
   * - ``fields.label``
     - ラベル名でフィルター。繰り返し指定可能（配列）。汎用的な ``fields.<name>`` ファミリーの一部です（ ``GET /search`` を参照）。
   * - ``sdh``
     - 類似ドキュメントハッシュ（similar-document hash）。

表: リクエストパラメーター

レスポンス
--------

成功時（200）の Content-Type は ``application/x-ndjson`` で、以下のように1行1ドキュメントで返ります。

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

エラーレスポンス
------------

エラーモデルの詳細は :doc:`api-overview` を参照してください。このエンドポイントが返す HTTP ステータスは以下の通りです。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス

   * - ステータスコード
     - 説明
   * - 400 Bad Request
     - 不正なクエリ、 ``num <= 0`` 、または ``api.search.scroll=false`` でスクロール検索が無効な場合。
   * - 405 Method Not Allowed
     - HTTP メソッドが許可されていない場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。

表: エラーレスポンス
