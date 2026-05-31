===================
API 빠른 시작
===================

이 페이지에서는 |Fess| API (v2) 를 바로 시험해 볼 수 있는 실용 가이드를 제공합니다.

5분으로 시작하기
================

전제 조건
---------

- |Fess| 가 실행 중일 것 (http://localhost:8080/ 에서 접근 가능)

검색 API 시험하기
-----------------

v2 의 검색 엔드포인트는 ``GET /api/v2/search`` 입니다.

**curl 명령 예:**

.. code-block:: bash

    # 기본 검색
    curl "http://localhost:8080/api/v2/search?q=fess"

    # 검색 결과를 20건 취득
    curl "http://localhost:8080/api/v2/search?q=fess&num=20"

    # 2페이지 취득 (21번째부터)
    curl "http://localhost:8080/api/v2/search?q=fess&start=20"

    # 레이블을 지정하여 검색
    curl "http://localhost:8080/api/v2/search?q=fess&fields.label=docs"

    # 패싯 (집계) 을 포함하여 검색
    curl "http://localhost:8080/api/v2/search?q=fess&facet.field=label"

    # 일본어 검색 (URL 인코딩)
    curl "http://localhost:8080/api/v2/search?q=%E6%A4%9C%E7%B4%A2"

**응답 예 (정형화):**

v2 의 응답은 ``response`` 엔벨로프로 반환됩니다.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "q": "fess",
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
    }

자동완성 API 시험하기
---------------------

자동완성 엔드포인트는 ``GET /api/v2/suggest-words`` 입니다.

.. code-block:: bash

    # 자동완성 취득
    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

**응답 예 (정형화):**

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

레이블 API 시험하기
-------------------

.. code-block:: bash

    # 사용 가능한 레이블 목록 취득
    curl "http://localhost:8080/api/v2/labels"

헬스 체크 API 시험하기
----------------------

헬스 체크 엔드포인트는 ``GET /api/v2/health`` 입니다.

.. code-block:: bash

    # 서버 (검색 엔진 클러스터) 의 상태 확인
    curl "http://localhost:8080/api/v2/health"

**응답 예 (정형화):**

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

Postman 에서 사용하기
=====================

|Fess| API 는 Postman 에서도 간편하게 사용할 수 있습니다.

컬렉션 설정
-----------

1. Postman 을 실행하고 새 컬렉션을 작성
2. 다음 요청을 추가:

**검색 API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/search``
- Query Parameters:
  - ``q``: 검색 키워드
  - ``num``: 취득 건수 (옵션)
  - ``start``: 시작 위치 (옵션)

**자동완성 API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/suggest-words``
- Query Parameters:
  - ``q``: 입력 문자열

**레이블 API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v2/labels``

환경 변수 설정
--------------

Postman 의 환경 변수를 사용하여 서버 URL 을 관리하는 것을 권장합니다.

1. "Environments" 에서 새 환경을 작성
2. 변수 추가: ``fess_url`` = ``http://localhost:8080``
3. 요청 URL 을 ``{{fess_url}}/api/v2/search`` 로 변경

프로그래밍 언어별 샘플
======================

모든 샘플에서 ``GET /api/v2/search`` 를 호출하고 ``response`` 엔벨로프를 참조합니다.

Python
------

.. code-block:: python

    import requests

    # Fess 서버의 URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess 검색 API 를 호출합니다"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v2/search", params=params)
        return response.json()

    # 사용 예
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

API 버전 대응표
===============

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess 버전
     - API 버전
     - 비고
   * - 15.x
     - v2
     - 최신판. 모든 기능 지원
   * - 14.x
     - v1
     - 구 API 만 지원
   * - 13.x
     - v1
     - 기본적인 API 지원

.. note::

   |Fess| 15.7 에서 기존의 ``/api/v1`` JSON 검색 API 및 채팅 API 는 폐지되었습니다.
   ``/api/v1`` 을 사용하던 클라이언트는 ``/api/v2`` 로 마이그레이션하십시오.
   버전 간 자세한 차이에 대해서는 `릴리스 노트 <https://github.com/codelibs/fess/releases>`__ 를 참조하십시오.

트러블슈팅
==========

API 가 동작하지 않는 경우
-------------------------

1. **|Fess| 가 실행 중인지 확인**

   http://localhost:8080/ 에 접근할 수 있는지 확인하십시오.

2. **엔드포인트가 v2 인지 확인**

   요청 경로가 ``/api/v2/...`` 인지 확인하십시오.
   기존의 ``/api/v1`` 엔드포인트는 폐지되었습니다.

3. **인증이 필요한 경우**

   인증이 필요한 엔드포인트에 대해서는 :doc:`api-auth` 를 참조하십시오.

다음 단계
=========

- :doc:`api-search` - 검색 API 상세
- :doc:`api-suggest` - 자동완성 API 상세
- :doc:`admin/index` - 관리 API 사용법
