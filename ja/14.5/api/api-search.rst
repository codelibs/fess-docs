==================
検索API
==================

検索結果の取得
==============

|Fess| に、
``http://<Server Name>/json/?q=検索語``
のようなリクエストを送ることで、
|Fess| の検索結果をJSON形式で受け取ることができます。
検索APIを利用するには、管理画面のシステム > 全般の設定でJSONレスポンスを有効にしておく必要があります。

リクエストパラメータ
--------------------

``http://<Server Name>/json/?q=検索語&num=50&fields.label=fess``
というようにリクエストパラメータを指定することで、より高度な検索を行うことができます。
使用できるリクエストパラメータは以下の通りです。

.. TODO: facet.field, facet.query の説明を詳しく
.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - 検索語。URLエンコードして渡します。
   * - start
     - 開始する件数位置。0から始まります。
   * - num
     - 表示件数。デフォルトは20件です。100件まで表示できます。
   * - sort
     - ソート。検索結果をソートする場合に利用します。
   * - fields.label
     - ラベル値。ラベルを指定する場合に利用します。
   * - callback
     - JSONPを利用する場合のコールバック名。JSONPを利用しない場合は指定する必要はありません。
   * - facet.field
     - ファセットフィールドの指定。 (例) ``facet.field=label``
   * - facet.query
     - ファセットクエリの指定。     (例) ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - 取得するファセットの最大件数の指定。facet.field が指定されているとき、有効です。
   * - facet.minDocCount
     - 件数がこの値以上のファセットを取得します。 facet.field が指定されているとき、有効です。
   * - geo.location.point
     - 緯度経度の指定。 (例) ``geo.location.point=35.0,139.0``
   * - geo.location.distance
     - 中心点からの距離の指定。 (例) ``geo.location.distance=10km``
   * - lang
     - 検索言語の指定。 (例) ``lang=en``
   * - preference
     - 検索時のシャードを指定する文字列。 (例) ``preference=abc``

表: リクエストパラメータ


レスポンス
----------

| 以下のようなレスポンスが返ります。
| （整形後のものです）

::

   {
     "response": {
       "version": "14.5",
       "status": 0,
       "q": "Fess",
       "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
       "exec_time": 0.21,
       "query_time": 171,
       "page_size": 20,
       "page_number": 1,
       "record_count": 31625,
       "page_count": 1582,
       "highlight_params": "&hq=n2sm&hq=Fess",
       "next_page": true,
       "prev_page": false,
       "start_record_number": 1,
       "end_record_number": 20,
       "page_numbers": [
         "1",
         "2",
         "3",
         "4",
         "5",
         "6"
       ],
       "partial": false,
       "search_query": "(Fess OR n2sm)",
       "requested_time": 1507822131845,
       "related_query": [
         "n2sm"
       ],
       "related_contents": [],
       "result": [
         {
           "filetype": "html",
           "title": "Open Source Enterprise Search Server: Fess — Fess 11.0 documentation",
           "content_title": "Open Source Enterprise Search Server: Fess — Fe...",
           "digest": "Docs » Open Source Enterprise Search Server: Fess Commercial Support Open Source Enterprise Search Server: Fess What is Fess ? Fess is very powerful and easily deployable Enterprise Search Server. ...",
           "host": "fess.codelibs.org",
           "last_modified": "2017-10-09T22:28:56.000Z",
           "content_length": "29624",
           "timestamp": "2017-10-09T22:28:56.000Z",
           "url_link": "https://fess.codelibs.org/",
           "created": "2017-10-10T15:00:48.609Z",
           "site_path": "fess.codelibs.org/",
           "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
           "url": "https://fess.codelibs.org/",
           "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is Elasticsearch-based search",
           "site": "fess.codelibs.org/",
           "boost": "10.0",
           "mimetype": "text/html"
         },

         ...

       ]
     }
   }

各要素については以下の通りです。

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: レスポンス情報

   * - response
     - ルート要素
   * - version
     - フォーマットバージョン
   * - status
     - レスポンスのステータス(status値は、0:正常、1:検索エラー、2または3:リクエストパラメータエラー、9:サービス停止中、-1:API種別エラーです)
   * - q
     - 検索語
   * - exec_time
     - 応答時間(単位は秒)
   * - query_time
     - クエリ処理時間(単位はミリ秒)
   * - page_size
     - 表示件数
   * - page_number
     - ページ番号
   * - record_count
     - 検索語に対してヒットした件数
   * - page_count
     - 検索語に対してヒットした件数のページ数
   * - highlight_params
     - ハイライトのパラメータ
   * - next_page
     - true:次のページが存在する。false:次のページが存在しない。
   * - prev_page
     - true:前のページが存在する。false:前のページが存在しない。
   * - start_record_number
     - レコード番号の開始位置
   * - end_record_number
     - レコード番号の終了位置
   * - page_numbers
     - ページ番号の配列
   * - partial
     - 検索がタイムアウトしたなど検索結果が打ち切られた場合にtrueとなる。
   * - search_query
     - 検索クエリ
   * - requested_time
     - リクエスト時刻(単位はepochミリ秒)
   * - related_query
     - 関連クエリ
   * - related_contents
     - 関連コンテンツのクエリ
   * - facet_field
     - 与えられたファセットフィールドにヒットするドキュメントの情報 (リクエストパラメータに ``facet.field`` が与えられた場合のみ)
   * - facet_query
     - 与えられたファセットクエリにヒットするドキュメントの数 (リクエストパラメータに ``facet.query`` が与えられた場合のみ)
   * - result
     - 検索結果の親要素
   * - filetype
     - ファイルの種別
   * - created
     - ドキュメントの生成日時
   * - title
     - ドキュメントのタイトル
   * - doc_id
     - ドキュメントのID
   * - url
     - ドキュメントのURL
   * - site
     - サイト名
   * - content_description
     - コンテンツの説明
   * - host
     - ホスト名
   * - digest
     - ドキュメントのダイジェスト文字列
   * - boost
     - ドキュメントのブースト値
   * - mimetype
     - MIMEタイプ
   * - last_modified
     - 最終更新日時
   * - content_length
     - ドキュメントのサイズ
   * - url_link
     - 検索結果としてのURL
   * - timestamp
     - ドキュメントの更新日時
