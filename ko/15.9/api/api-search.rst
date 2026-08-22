========
검색 API
========

이 문서에서는 |Fess| 의 v2 검색 API 에 대해 설명합니다.
공통 응답 엔벨로프·오류 모델·CSRF 에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

``q`` 파라미터에는 일반 검색 화면과 동일한 검색 구문(AND/OR/NOT 검색, 필드 지정, 와일드카드, 유사 검색 등)을 사용할 수 있습니다. 검색 구문에 대한 자세한 내용은 :doc:`../user/index` 를 참조하십시오.

문서 검색
=========

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/search``
==================  ====================================================

쿼리에 일치하는 문서를 검색하고 공통 엔벨로프로 결과를 반환합니다.
페이로드 내의 필드 이름은 모두 ``snake_case`` 입니다.

요청 파라미터
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``q``
     - 검색어 (URL 인코딩).
   * - ``start``
     - 0 시작 시작 위치 (integer, ``>=0`` , 기본값 ``0`` ).
   * - ``offset``
     - ``start`` 로부터의 오프셋 (integer, ``>=0`` , 기본값 ``0`` ).
   * - ``num``
     - 페이지 크기 (integer, ``>=1`` , 기본값 ``10`` ). ``<= 0`` 은 ``invalid_request`` 가 됩니다. 설정된 최대값을 초과하는 값은 자동으로 클램프됩니다. 클램프 여부는 요청의 ``num`` 과 응답의 ``page_size`` 를 비교하여 감지할 수 있습니다.
   * - ``sort``
     - 정렬 (예: ``score`` ).
   * - ``lang``
     - 검색 언어. 반복 지정 가능 (배열). 예: ``en`` .
   * - ``ex_q``
     - 추가 쿼리 식. 반복 지정 가능.
   * - ``sdh``
     - 유사 문서 해시 (similar-document hash).
   * - ``fields.label``
     - 레이블 이름으로 필터링합니다. 반복 지정 가능. 이는 범용적인 ``fields.<name>`` 패밀리의 가장 일반적인 경우로, 임의의 ``fields.<name>`` 쿼리 파라미터는 문서 필드 ``<name>`` 이 지정값과 일치하는 결과로 좁혀줍니다.
   * - ``as.*``
     - 고급 검색 조건. 임의의 ``as.<name>`` (예: ``as.q`` , ``as.filetype`` ) 이 고급 검색 조건 빌더에 전달됩니다. name 별로 반복 지정 가능합니다.
   * - ``track_total_hits``
     - 검색 엔진에 전달되어 정확한 히트 수 계산을 제어합니다 (예: ``true`` 또는 정수 임계값). ``record_count_relation`` 이 ``eq`` 인지 ``gte`` 인지에 영향을 줍니다.
   * - ``facet.field``
     - 패싯 필드. 반복 지정 가능 (배열).
   * - ``facet.query``
     - 패싯 쿼리. 반복 지정 가능 (배열).
   * - ``facet.size``
     - 반환할 패싯 단어의 최대 수 (integer).
   * - ``facet.minDocCount``
     - 패싯 단어가 포함된 최소 문서 수 (integer).
   * - ``facet.sort``
     - 패싯 정렬.
   * - ``facet.missing``
     - 값이 없는 문서에 대한 패싯 처리 방식.
   * - ``geo.location.point``
     - 지리 좌표 중심점 (예: ``35.0,139.0`` ).
   * - ``geo.location.distance``
     - 중심점으로부터의 거리 (예: ``10km`` ).

표: 요청 파라미터

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

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

각 필드에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드

   * - ``q``
     - 검색어 (nullable).
   * - ``query_id``
     - 쿼리 식별자.
   * - ``exec_time``
     - 실행 시간 (double, 초).
   * - ``query_time``
     - 검색 엔진의 쿼리 시간 (int64, 밀리초).
   * - ``page_size``
     - 페이지 크기.
   * - ``page_number``
     - 현재 페이지 번호.
   * - ``record_count``
     - 히트 건수 (int64).
   * - ``record_count_relation``
     - ``eq`` 일 때는 정확한 카운트, ``gte`` 일 때는 하한만 확인된 것을 나타냅니다.
   * - ``page_count``
     - 총 페이지 수.
   * - ``highlight_params``
     - 하이라이트용 쿼리 파라미터 문자열.
   * - ``next_page``
     - 다음 페이지 존재 여부 (bool).
   * - ``prev_page``
     - 이전 페이지 존재 여부 (bool).
   * - ``start_record_number``
     - 이 페이지의 시작 레코드 번호.
   * - ``end_record_number``
     - 이 페이지의 종료 레코드 번호.
   * - ``page_numbers``
     - 페이지네이션에 표시할 페이지 번호 배열 (문자열).
   * - ``partial``
     - 결과가 부분적인지 여부 (bool).
   * - ``search_query``
     - 실제로 실행된 검색 쿼리.
   * - ``requested_time``
     - 요청 시각 (int64, epoch 밀리초).
   * - ``related_query``
     - 관련 쿼리 배열 (문자열).
   * - ``related_contents``
     - 관련 콘텐츠 배열 (문자열).
   * - ``data``
     - 검색 결과 배열. 1 문서당 1 요소. ``QueryFieldConfig#isApiResponseField`` 가 허용하는 필드만 포함되며, null 이나 빈 키는 제외됩니다.
   * - ``facet_field``
     - 패싯 필드가 요청된 경우에만 존재하는 배열. 각 요소는 ``{name, result:[{value, count}]}`` .
   * - ``facet_query``
     - 패싯 쿼리가 요청된 경우에만 존재하는 배열. 각 요소는 ``{value, count}`` .

표: 응답 필드

오류 응답
---------

오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오. 이 엔드포인트가 반환하는 HTTP 상태는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청이 잘못된 경우.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답

전체 문서 취득 (스크롤 검색·NDJSON)
=====================================

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/documents/all``
==================  ====================================================

쿼리에 일치하는 모든 문서를 NDJSON ( ``application/x-ndjson`` ) 으로 스트림 배신합니다.
각 행은 ``{"data":{...}}`` 객체로, ``QueryFieldConfig#isApiResponseField`` 가 허용하는 필드를 포함합니다.

스트림 도중에 실패한 경우에는 마지막 행에 다음 행을 출력하고 플러시합니다.

::

    {"error":{"code":"internal_error","message":"stream error"}}

이 때문에 클라이언트는 마지막 행의 첫 번째 키를 확인하여 정상 완료 ( ``data`` ) 인지 서버 이상 ( ``error`` ) 인지 구별해야 합니다.

쿼리는 ``GET /search`` 와 동일한 파라미터 세트 ( ``q`` , ``sort`` , ``num`` , ``lang`` , ``ex_q`` , ``sdh`` , ``fields.*`` , ``as.*`` , ``track_total_hits`` , ``facet.*`` , ``geo.*`` ) 로 구성됩니다.
``api.search.scroll=false`` 로 스크롤 검색이 비활성화된 경우에는 ``invalid_request`` (400) 를 반환합니다.

요청 파라미터
-------------

사양에 명시된 파라미터는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``q``
     - 검색어.
   * - ``sort``
     - 정렬.
   * - ``num``
     - 페이지 (스크롤 배치) 크기 (integer, ``>=1`` ). ``<= 0`` 은 ``invalid_request`` 가 됩니다.
   * - ``lang``
     - 검색 언어. 반복 지정 가능 (배열).
   * - ``ex_q``
     - 추가 쿼리 식. 반복 지정 가능 (배열).
   * - ``fields.label``
     - 레이블 이름으로 필터링. 반복 지정 가능 (배열). 범용적인 ``fields.<name>`` 패밀리의 일부입니다 ( ``GET /search`` 참조).
   * - ``sdh``
     - 유사 문서 해시 (similar-document hash).

표: 요청 파라미터

응답
----

성공 시 (200) 의 Content-Type 은 ``application/x-ndjson`` 으로, 다음과 같이 1행 1문서로 반환됩니다.

::

    {"data":{"url":"https://example.com/","title":"Example"}}
    {"data":{"url":"https://example.org/","title":"Example Org"}}

오류 응답
---------

오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오. 이 엔드포인트가 반환하는 HTTP 상태는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 잘못된 쿼리, ``num <= 0`` , 또는 ``api.search.scroll=false`` 로 스크롤 검색이 비활성화된 경우.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답


관련 항목
=====================================

- :doc:`../user/search-field` - 필드 지정 검색
- :doc:`../user/special-char` - 특수 문자
- :doc:`../user/search-wildcard` - 와일드카드 검색
