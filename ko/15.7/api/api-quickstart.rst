===================
API 빠른 시작
===================

이 페이지에서는 |Fess| API를 빠르게 사용하기 위한 실용 가이드를 제공합니다.

5분 만에 시작하기
========================

사전 준비
-------------

- |Fess| 가 실행 중 (http://localhost:8080/ 에 접속 가능)
- 관리 화면 > 시스템 > 일반에서 JSON 응답이 활성화되어 있어야 합니다

검색 API 사용해 보기
------------------

**curl 명령 예시:**

.. code-block:: bash

    # 기본 검색
    curl "http://localhost:8080/api/v1/documents?q=fess"

    # 20건의 검색 결과 가져오기
    curl "http://localhost:8080/api/v1/documents?q=fess&num=20"

    # 2페이지 가져오기 (21번째 결과부터)
    curl "http://localhost:8080/api/v1/documents?q=fess&start=20"

    # 라벨 필터를 사용한 검색
    curl "http://localhost:8080/api/v1/documents?q=fess&fields.label=docs"

    # 패싯(집계)을 사용한 검색
    curl "http://localhost:8080/api/v1/documents?q=fess&facet.field=label"

    # 특수 문자가 포함된 검색 (URL 인코딩)
    curl "http://localhost:8080/api/v1/documents?q=search%20engine"

**응답 예시 (정형화):**

.. code-block:: json

    {
      "q": "fess",
      "exec_time": 0.15,
      "record_count": 125,
      "page_size": 20,
      "page_number": 1,
      "data": [
        {
          "title": "Fess - Open Source Enterprise Search Server",
          "url": "https://fess.codelibs.org/",
          "content_description": "<strong>Fess</strong> is an easy to deploy...",
          "host": "fess.codelibs.org",
          "mimetype": "text/html"
        }
      ]
    }

제안 API 사용해 보기
-------------------

.. code-block:: bash

    # 제안 가져오기
    curl "http://localhost:8080/api/v1/suggest?q=fes"

    # 응답 예시
    # {"q":"fes","result":[{"text":"fess","kind":"document"}]}

라벨 API 사용해 보기
-----------------

.. code-block:: bash

    # 사용 가능한 라벨 가져오기
    curl "http://localhost:8080/api/v1/labels"

헬스 체크 API 사용해 보기
------------------------

.. code-block:: bash

    # 서버 상태 확인
    curl "http://localhost:8080/api/v1/health"

    # 응답 예시
    # {"data":{"status":"green","cluster_name":"fess"}}

Postman 사용하기
=============

|Fess| API는 Postman으로 간편하게 사용할 수 있습니다.

컬렉션 설정
----------------

1. Postman을 열고 새 컬렉션을 작성합니다
2. 다음 요청을 추가합니다:

**검색 API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/documents``
- Query Parameters:
  - ``q``: 검색 키워드
  - ``num``: 결과 수 (옵션)
  - ``start``: 시작 위치 (옵션)

**제안 API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/suggest``
- Query Parameters:
  - ``q``: 입력 문자열

**라벨 API:**

- Method: ``GET``
- URL: ``http://localhost:8080/api/v1/labels``

환경 변수
---------------------

서버 URL을 관리하기 위해 Postman 환경 변수를 사용하는 것을 권장합니다.

1. "Environments"에서 새 환경을 작성합니다
2. 변수 추가: ``fess_url`` = ``http://localhost:8080``
3. 요청 URL을 ``{{fess_url}}/api/v1/documents`` 로 변경합니다

프로그래밍 언어별 코드 샘플
====================================

Python
------

.. code-block:: python

    import requests
    import urllib.parse

    # Fess 서버 URL
    FESS_URL = "http://localhost:8080"

    def search(query, num=20, start=0):
        """Fess 검색 API 호출"""
        params = {
            "q": query,
            "num": num,
            "start": start
        }
        response = requests.get(f"{FESS_URL}/api/v1/documents", params=params)
        return response.json()

    # 사용 예시
    results = search("enterprise search")
    print(f"총 건수: {results['record_count']}")
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

    // 사용 예시
    search('enterprise search').then(results => {
      console.log(`총 건수: ${results.record_count}`);
      results.data.forEach(doc => {
        console.log(`- ${doc.title}`);
        console.log(`  URL: ${doc.url}`);
      });
    });

JavaScript (브라우저)
--------------------

.. code-block:: javascript

    // JSONP 사용
    function search(query, callback) {
      const script = document.createElement('script');
      const url = `http://localhost:8080/api/v1/documents?q=${encodeURIComponent(query)}&callback=${callback}`;
      script.src = url;
      document.body.appendChild(script);
    }

    // 콜백 함수
    function handleResults(results) {
      console.log(`총 건수: ${results.record_count}`);
    }

    // 사용 예시
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
            String result = client.search("enterprise search");
            System.out.println(result);
        }
    }

API 버전 호환성
=========================

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Fess 버전
     - API 버전
     - 비고
   * - 15.x
     - v1
     - 최신 버전. 전 기능 지원
   * - 14.x
     - v1
     - 유사한 API. 일부 파라미터 차이가 있을 수 있음
   * - 13.x
     - v1
     - 기본 API 지원

.. note::

   API 호환성은 유지되지만 새로운 기능은 최신 버전에서만 사용 가능합니다.
   버전 간 차이에 대한 자세한 내용은 `릴리스 노트 <https://github.com/codelibs/fess/releases>`__ 를 참조하세요.

트러블슈팅
===============

API가 작동하지 않는 경우
---------------

1. **JSON 응답이 활성화되어 있는지 확인**

   관리 화면 > 시스템 > 일반에서 "JSON 응답"이 활성화되어 있는지 확인합니다.

2. **브라우저에서 CORS 에러**

   브라우저에서 접근 시 CORS 에러가 발생하면 JSONP를 사용하거나
   서버에서 CORS 설정을 구성합니다.

   JSONP 예시:

   .. code-block:: bash

       curl "http://localhost:8080/api/v1/documents?q=fess&callback=myCallback"

3. **인증이 필요한 경우**

   액세스 토큰이 설정된 경우 요청 헤더에 포함합니다:

   .. code-block:: bash

       curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
            "http://localhost:8080/api/v1/documents?q=fess"

다음 단계
==========

- :doc:`api-search` - 검색 API 상세
- :doc:`api-suggest` - 제안 API 상세
- :doc:`admin/index` - 관리 API 사용법
