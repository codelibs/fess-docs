=======================
検索結果エクスポートAPI
=======================

このドキュメントでは、検索結果を CSV または JSON のファイルとしてダウンロードする |Fess| の v2 エクスポート API について説明します。共通のレスポンスエンベロープ・エラーモデルについては :doc:`api-overview` を参照してください。

ベースURLは ``http://<Server Name>/api/v2/`` です（ローカル環境の例: ``http://localhost:8080/api/v2`` ）。

.. note::

   エクスポートはデフォルトで無効です。利用するには ``fess_config.properties`` で ``api.search.export=true`` を設定してください。有効な場合、同梱の ``bootstrap`` テーマでは検索結果の件数の横にエクスポートのメニュー（CSV / JSON）が表示されます。 ``/api/v2/ui/config`` の ``features.search_export`` で状態を確認できます。

検索結果のダウンロード
======================

リクエスト
----------

==================  ====================================================
HTTPメソッド        GET
エンドポイント      ``/api/v2/documents/export``
==================  ====================================================

検索に一致するドキュメントを、ファイルのダウンロード（ ``Content-Disposition: attachment`` 、ファイル名は ``search_results.csv`` または ``search_results.json`` ）として返します。

- ``/api/v2/search`` と同じロールの絞り込みが適用されます。 ``login.required=true`` の場合も、 ``/api/v2/search`` と同じようにアクセストークンを使えます。
- 出力する件数は最大 ``api.search.export.max.size`` （デフォルト: ``1000`` ）件です。ページングのパラメーター（ ``start`` 、 ``num`` ）は使いません。
- 出力するフィールドは ``api.search.export.fields`` （デフォルト: ``title,url_link,last_modified,content_length,filetype`` ）のうち、API のレスポンスに含められるフィールドだけです。
- リクエストは 1 分あたり ``api.search.export.rate.limit.per.minute`` （デフォルト: ``10`` 、 ``0`` で無制限）回に制限されます。ログインしているユーザーはユーザーごと、ゲストはクライアントの IP アドレスごとに数えます。超えると ``429`` と ``Retry-After`` ヘッダーが返ります。
- エクスポートは検索ログに記録されません。

リクエストパラメーター
----------------------

``q`` 、 ``ex_q`` 、 ``fields.*`` 、 ``sort`` 、 ``lang`` など、 ``/api/v2/documents/all`` と同じ検索条件のパラメーターを指定できます（ :doc:`api-search` を参照）。これに加えて次のパラメーターがあります。

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: リクエストパラメーター

   * - ``format``
     - ファイルの形式。 ``csv`` （デフォルト）または ``json`` 。それ以外は ``invalid_request`` (400) になります。

表: リクエストパラメーター

レスポンス
----------

CSV は 1 行目がフィールド名の見出し行で、 ``csv.file.encoding`` の文字コードで出力されます（UTF-8 の場合は BOM が付きます）。 ``=`` 、 ``+`` 、 ``-`` 、 ``@`` 、タブ、復帰文字（CR）で始まる値には、表計算ソフトで数式として扱われないように先頭に ``'`` が付きます。複数の値を持つフィールドは空白でつなげます。

::

    "title","url_link","last_modified","content_length","filetype"
    "Example","https://example.com/","2025-01-01T00:00:00.000Z","1234","html"

JSON は ``{"data":[{...},...]}`` の形式で、複数の値を持つフィールドは配列のままです。

ファイルの出力が始まる前に失敗した場合は、通常のエラーエンベロープが返ります。出力が始まった後に失敗した場合は、ファイルが途中で終わります（CSV は途中まで、JSON は解析できない内容になります）。

エラーレスポンス
----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: エラーレスポンス

   * - ステータスコード
     - 説明
   * - 400 Bad Request
     - 不正なクエリ、 ``format`` が ``csv`` / ``json`` 以外、または ``api.search.export=false`` でエクスポートが無効な場合。
   * - 401 Unauthorized
     - 認証が必要な場合（ ``login.required=true`` で匿名の呼び出し元など）。
   * - 405 Method Not Allowed
     - HTTP メソッドが許可されていない場合。
   * - 429 Too Many Requests
     - 1 分あたりのリクエスト数の上限を超えた場合。
   * - 500 Internal Server Error
     - サーバー内部エラーが発生した場合。

表: エラーレスポンス
