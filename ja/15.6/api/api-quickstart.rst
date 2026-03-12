===================
APIクイックスタート
===================

このページでは、|Fess| APIをすぐに試すための実践的なガイドを提供します。

5分で始めるAPI
============

前提条件
------

- |Fess| が起動していること（http://localhost:8080/ でアクセス可能）
- 管理画面（http://localhost:8080/admin）で「システム」>「全般」のJSONレスポンスが有効になっていること

検索APIを試す
-----------

**curlコマンドの例:**

.. code-block:: bash

    # 基本的な検索
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # 検索結果を20件取得
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # 2ページ目を取得（21件目から）
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # ラベルを指定して検索
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # ファセット（集計）を含めて検索
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # 日本語検索（URLエンコード）
    curl "http://localhost:8080/api/v1/documents?q=%E6%A4%9C%E7%B4%A2"

**レスポンス例（整形済み）:**

.. code-block:: json

    {
      "q": "fess",
      "exec_time": 0.15,
      "record_count": 125,
      "page_size": 20,
      "page_number": 1,
      "data": [
        {
          "title": "Fess - オープンソース全文検索サーバー",
          "url": "https://fess.codelibs.org/ja/",
          "content_description": "<strong>Fess</strong>は簡単に構築できる...",
          "host": "fess.codelibs.org",
          "mimetype": "text/html"
        }
      ]
    }

サジェストAPIを試す
----------------

.. code-block:: bash

    # サジェストを取得
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # レスポンス例
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

ラベルAPIを試す
-------------

.. code-block:: bash

    # 利用可能なラベル一覧を取得
    curl "http://localhost:8080/api/v1/labels"

ヘルスチェックAPIを試す
--------------------

.. code-block:: bash

    # サーバーの状態を確認
    curl "http://localhost:8080/api/v1/health"

    # レスポンス例
    # {"data":{"status":"green","cluster_name":"fess"}}

Postman での利用
==============

|Fess| APIはPostmanからも簡単に利用できます。

コレクションのセットアップ
------------------------

1. Postmanを起動し、新しいコレクションを作成
2. 以下のリクエストを追加：

**検索API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/documents``
- Query Parameters:
  - ``q``: 検索キーワード
  - ``num``: 取得件数（オプション）
  - ``start``: 開始位置（オプション）

**サジェストAPI:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/suggest``
- Query Parameters:
  - ``q``: 入力文字列

**ラベルAPI:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/labels``

環境変数の設定
------------

Postmanの環境変数を使って、サーバーURLを管理することを推奨します。

1. 「Environments」で新しい環境を作成
2. 変数を追加: ``fess_url`` = ``http://localhost:8080``
3. リクエストURLを ``{{fess_url}}/api/v1/documents`` に変更

プログラミング言語別サンプル
========================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # Fess サーバーのURL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess検索APIを呼び出す"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # 使用例
    results = search("Fess 検索")
    print(f"ヒット件数: {results['record_count']}")
    for doc in results['data']:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v1/documents?${params}`);
      return response.json();
    }

    // 使用例
    search('Fess 検索').then(results => {
      console.log(`ヒット件数: ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

JavaScript (ブラウザ)
--------------------

.. code-block:: javascript

    // JSONP を使用する場合
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // コールバック関数
    function handleResults(results) {
      console.log(`ヒット件数: ${results.record_count}`);
    }

    // 使用例
    search('Fess', 'handleResults');

Java
----

.. code-block:: java

    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;
    import java.net.URLEncoder;
    import java.nio.charset.StandardCharsets;

    public class FessApiClient {
        private static final String FESS_URL = "http://localhost:8080";
        private final HttpClient client = HttpClient.newHttpClient();

        public String search(String query) throws Exception {
            String encodedQuery = URLEncoder.encode(query, StandardCharsets.UTF_8);
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(FESS_URL + "/api/v1/documents?q=" + encodedQuery))
                .GET()
                .build();

            HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
            return response.body();
        }

        public static void main(String[] args) throws Exception {
            FessApiClient client = new FessApiClient();
            String result = client.search("Fess 検索");
            System.out.println(result);
        }
    }

APIバージョン対応表
================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fessバージョン
     - APIバージョン
     - 備考
   * - 15.x
     - v1
     - 最新版。すべての機能をサポート
   * - 14.x
     - v1
     - ほぼ同等のAPI。一部パラメータが異なる場合あり
   * - 13.x
     - v1
     - 基本的なAPIをサポート

.. note::

   APIの互換性は維持されていますが、新機能は最新バージョンでのみ利用可能です。
   バージョン間の詳細な差異については、`リリースノート <https://github.com/codelibs/fess/releases>`__ を参照してください。

トラブルシューティング
==================

APIが動作しない場合
-----------------

1. **JSONレスポンスが有効か確認**

   管理画面 > システム > 全般 で「JSONレスポンス」が有効になっていることを確認してください。

2. **CORSエラーが発生する場合**

   ブラウザからのアクセスでCORSエラーが発生する場合は、JSONPを使用するか、
   サーバー側でCORS設定を行ってください。

   JSONP使用例:

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **認証が必要な場合**

   アクセストークンが設定されている場合は、リクエストヘッダーに含めてください：

   .. code-block:: bash

       curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
            "http://localhost:8080/api/v1/documents?q=fess"

次のステップ
==========

- :doc:`api-search` - 検索APIの詳細
- :doc:`api-suggest` - サジェストAPIの詳細
- :doc:`admin/index` - 管理APIの利用方法

