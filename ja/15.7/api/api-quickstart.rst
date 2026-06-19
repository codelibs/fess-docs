===================
APIクイックスタート
===================

このページでは、|Fess| API (v2) をすぐに試すための実践的なガイドを提供します。

5分で始めるAPI
============

前提条件
------

- |Fess| が起動していること（http://localhost:8080/ でアクセス可能）

検索APIを試す
-----------

v2 の検索エンドポイントは ``GET /api/v2/search`` です。

**curlコマンドの例:**

.. code-block:: bash

    # 基本的な検索
    curl "http://localhost:8080/api/v2/search?q=fess"

    # 検索結果を20件取得（num はページサイズ。既定値は 10）
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # 先頭20件をスキップして取得（start は0始まりの開始位置）
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # ラベルを指定して検索
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # ファセット（集計）を含めて検索
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # 日本語検索（URLエンコード）
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**レスポンス例（整形済み）:**

v2 のレスポンスは ``response`` エンベロープで返されます。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fess",
        "record_count": 125,
        "page_size": 10,
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
    }

.. note::

   上記は代表的な例です。 ``data`` に含まれるドキュメントのフィールドは、サーバーの設定
   （応答フィールドの許可リスト）に依存します。利用可能なリクエストパラメーターと
   レスポンスフィールドの全一覧は :doc:`api-search` を、共通のレスポンスエンベロープ・
   エラーモデル・CSRF については :doc:`api-overview` を参照してください。

サジェストAPIを試す
----------------

サジェストエンドポイントは ``GET /api/v2/suggest-words`` です。

.. code-block:: bash

    # サジェストを取得
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**レスポンス例（整形済み）:**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fes",
        "suggest_words": [
          { "text": "fess", "types": ["document"] }
        ]
      }
    }

ラベルAPIを試す
-------------

.. code-block:: bash

    # 利用可能なラベル一覧を取得
    curl "http://localhost:8080/api/v2/labels"

ヘルスチェックAPIを試す
--------------------

ヘルスチェックエンドポイントは ``GET /api/v2/health`` です。

.. code-block:: bash

    # サーバー（検索エンジンクラスター）の状態を確認
    curl "http://localhost:8080/api/v2/health"

**レスポンス例（整形済み）:**

.. code-block:: json

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess",
          "status": "green",
          "ping_status": 200
        }
      }
    }

Postman での利用
==============

|Fess| APIはPostmanからも簡単に利用できます。

コレクションのセットアップ
------------------------

1. Postmanを起動し、新しいコレクションを作成
2. 以下のリクエストを追加：

**検索API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query Parameters:
  - ``q``: 検索キーワード
  - ``num``: 取得件数（オプション）
  - ``start``: 開始位置（オプション）

**サジェストAPI:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query Parameters:
  - ``q``: 入力文字列

**ラベルAPI:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

環境変数の設定
------------

Postmanの環境変数を使って、サーバーURLを管理することを推奨します。

1. 「Environments」で新しい環境を作成
2. 変数を追加: ``fess_url`` = ``http://localhost:8080``
3. リクエストURLを ``{{fess_url}}/api/v2/search`` に変更

プログラミング言語別サンプル
========================

いずれのサンプルも ``GET /api/v2/search`` を呼び出し、 ``response`` エンベロープを参照します。

Python
------

.. code-block:: python

    import requests

    # Fess サーバーのURL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess検索APIを呼び出す"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # 使用例
    results = search("Fess 検索")
    print(f"ヒット件数: {results['response']['record_count']}")
    for doc in results["response"]["data"]:
        print(f"- {doc['title']}")
        print(f"  URL: {doc['url']}")

JavaScript (Node.js)
--------------------

.. code-block:: javascript

    const fetch = require('node-fetch');

    const FESS_URL = 'http://localhost:8080';

    async function search(query, num = 20, start = 0) {
      const params = new URLSearchParams({ q: query, num, start });
      const response = await fetch(`${FESS_URL}/api/v2/search?${params}`);
      return response.json();
    }

    // 使用例
    search('Fess 検索').then(results => {
      console.log(`ヒット件数: ${results.response.record_count}`);
      results.response.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

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
                .uri(URI.create(FESS_URL + "/api/v2/search?q=" + encodedQuery))
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
     - v2
     - 最新版。すべての機能をサポート
   * - 14.x
     - v1
     - 旧APIのみサポート
   * - 13.x
     - v1
     - 基本的なAPIをサポート

.. note::

   |Fess| 15.7 で、従来の ``/api/v1`` の JSON 検索 API およびチャット API は廃止されました。
   ``/api/v1`` を利用していたクライアントは ``/api/v2`` へ移行してください。
   バージョン間の詳細な差異については、`リリースノート <https://github.com/codelibs/fess/releases>`__ を参照してください。

トラブルシューティング
==================

APIが動作しない場合
-----------------

1. **|Fess| が起動しているか確認**

   http://localhost:8080/ にアクセスできることを確認してください。

2. **エンドポイントが v2 になっているか確認**

   リクエスト先のパスが ``/api/v2/...`` になっていることを確認してください。
   従来の ``/api/v1`` のエンドポイントは廃止されています。

3. **認証が必要な場合**

   認証が必要なエンドポイントについては、 :doc:`api-auth` を参照してください。

次のステップ
==========

- :doc:`api-overview` - APIの共通仕様（レスポンスエンベロープ、エラーモデル、認証/CSRF）
- :doc:`api-search` - 検索APIの詳細
- :doc:`api-suggest` - サジェストAPIの詳細
- :doc:`api-label` - ラベルAPIの詳細
- :doc:`api-health` - ヘルスチェックAPIの詳細
- :doc:`admin/index` - 管理APIの利用方法
