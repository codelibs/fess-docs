=============
유사 문서 API
=============

이 문서에서는 지정한 문서와 내용이 같은 문서를 목록으로 반환하는 |Fess| 의 v2 유사 문서 API 에 대해 설명합니다. 공통 응답 엔벨로프·오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

.. note::

   이 API가 찾는 것은 복사본이나 내용이 거의 같은 문서입니다. 주제가 비슷할 뿐인 문서는 찾지 못합니다(아래의 "반환되는 문서" 참조).

유사 문서 가져오기
==================

요청
----

==================  ====================================================
HTTP 메서드         GET
엔드포인트          ``/api/v2/documents/{docId}/similar``
==================  ====================================================

``docId`` 문서와 같은 내용 서명을 가진 문서를 반환합니다. 검색 결과 옆에 "유사 문서" 링크를 표시하는 데 사용할 수 있습니다.

- 지정한 문서와 반환되는 문서 모두에 ``/api/v2/search`` 와 같은 역할 필터·가상 호스트 필터·추가 쿼리가 적용됩니다. 존재하지 않는 문서와 호출자에게 보이지 않는 문서는 모두 ``not_found`` (404) 가 됩니다. 지정한 문서 자체와 같은 URL의 문서는 반환되지 않습니다.
- ``login.required=true`` 일 때 로그인하지 않은 호출자는 ``auth_required`` (401) 가 됩니다. 액세스 토큰은 ``/api/v2/search`` 와 같은 방법으로 사용할 수 있습니다.
- 요청은 ``api.search.similar.rate.limit.per.minute`` (기본값: ``30`` , ``0`` 은 무제한)회/분으로 제한되며, 로그인한 사용자별, 게스트는 클라이언트 IP별로 집계합니다. 한도를 넘으면 ``429`` 와 ``Retry-After`` 헤더가 반환됩니다.
- 반환되는 것은 한 페이지뿐이며 URL, 문서 ID 순으로 정렬됩니다. ``start`` 나 오프셋 파라미터는 없습니다.

반환되는 문서
-------------

|Fess| 는 문서를 색인에 등록할 때 내용 서명( ``content_minhash_bits`` )을 계산합니다. 이 API는 지정한 문서와 서명이 같은 문서를 반환합니다. 중복 문서 리포트( :doc:`../admin/docreport-guide` ), 검색 파라미터 ``sdh`` , ``similar_docs_*`` 필드와 같은 그룹화이지만, 중복 결과 묶기를 활성화하지 않아도 사용할 수 있습니다.

- 반환되는 것은 복사본이나 내용이 거의 같은 문서입니다. 서명이 바뀔 만큼 내용을 편집한 문서는 반환되지 않으므로, 주제가 비슷한 문서를 찾는 기능이 아닙니다.
- 지정한 문서에 내용이나 단어가 없는 경우와 검색 엔진이 CodeLibs 플러그인 없이 동작하는 경우( ``search_engine.type`` 이 ``vanilla`` , ``aws`` , 사용 중단 예정인 ``cloud`` . :doc:`../config/search-engine-type` 참조)에는 오류가 아니라 ``data`` 가 빈 배열이 됩니다.

요청 파라미터
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터
   :widths: 27 73
   :header-rows: 1

   * - 파라미터
     - 설명
   * - ``docId``
     - 문서 식별자(경로, 필수, 패턴 ``[A-Za-z0-9_-]{1,512}`` ). 일치하지 않는 값은 ``invalid_request`` (400) 가 됩니다.
   * - ``num``
     - 반환할 문서 수(쿼리, 기본값 ``10`` ). ``20`` 과 ``paging.search.page.max.size`` 중 작은 쪽을 넘는 값은 그 값으로 줄어들며, 응답의 ``page_size`` 로 확인할 수 있습니다. ``0`` 이하는 ``invalid_request`` (400) 가 됩니다. 숫자가 아닌 값은 무시되고 기본값이 사용됩니다.

표: 요청 파라미터

응답
----

성공 시(HTTP 200) 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "exec_time": "0.01",
        "query_time": 5,
        "page_size": 10,
        "record_count": 1,
        "record_count_relation": "EQUAL_TO",
        "partial": false,
        "timed_out": false,
        "shard_failed": false,
        "data": [
          {
            "doc_id": "f6e5d4c3b2a1",
            "url": "https://example.com/copy/",
            "title": "Example",
            "content_description": "An example document about Fess."
          }
        ]
      }
    }

각 필드는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드
   :widths: 27 73
   :header-rows: 1

   * - 필드
     - 설명
   * - ``doc_id``
     - 지정한 문서의 ID.
   * - ``exec_time``
     - 실행 시간(초). ``"0.01"`` 과 같은 소수 문자열.
   * - ``query_time``
     - 검색 엔진의 쿼리 시간(int64, 밀리초).
   * - ``page_size``
     - 위의 상한을 적용한 후 요청한 문서 수.
   * - ``record_count``
     - 서명이 같은 문서의 건수( ``data`` 에 포함되지 않은 것도 포함). 정확한 건수는 ``query.track.total.hits`` (기본값: ``10000`` )까지만 집계합니다.
   * - ``record_count_relation``
     - ``EQUAL_TO`` 이면 건수가 정확하고, ``GREATER_THAN_OR_EQUAL_TO`` 이면 하한만 알 수 있습니다.
   * - ``partial``
     - 결과가 불완전할 수 있는지 여부(bool). 검색과 마찬가지로 쿼리 타임아웃( ``query.timeout`` )이 적용됩니다.
   * - ``timed_out``
     - 쿼리 타임아웃에 도달했는지 여부(bool).
   * - ``shard_failed``
     - 하나 이상의 샤드가 실패했는지 여부(bool).
   * - ``data``
     - 문서의 배열(URL, 문서 ID 순). 각 요소는 ``/api/v2/search`` 의 히트와 같은 필드를 가지며( :doc:`api-search` 참조), ``tags`` (호출자에게 보이는 태그. :doc:`api-tag` 참조)도 포함합니다. 하이라이트할 쿼리가 없으므로 ``content_description`` 은 본문의 다이제스트이며, ``score`` 는 없습니다.

표: 응답 필드

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답
   :widths: 25 75
   :header-rows: 1

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - ``docId`` 가 패턴과 일치하지 않거나 ``num`` 이 ``0`` 이하인 경우.
   * - 401 Unauthorized
     - 인증이 필요한 경우(로그인 필수 설정이 활성화되어 있는데 로그인하지 않았거나, 등록되지 않았거나 만료된 액세스 토큰이 지정됨).
   * - 404 Not Found
     - 지정한 문서가 존재하지 않거나 호출자에게 보이지 않는 경우( ``not_found`` ).
   * - 405 Method Not Allowed
     - 허용되지 않는 HTTP 메서드가 지정된 경우.
   * - 429 Too Many Requests
     - 1분당 요청 수 한도를 넘은 경우. ``Retry-After`` 헤더에 기다릴 초(``60``)가 들어갑니다.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.
   * - 503 Service Unavailable
     - 검색 엔진이 요청을 받을 수 없는 경우(연결할 수 없거나 용량 부족으로 거부됨). ``error.code`` 는 ``service_unavailable`` 이고, ``Retry-After`` 헤더에 기다릴 초(``5``)가 들어갑니다. 요청 자체에는 문제가 없으므로 잠시 기다린 후 다시 시도하십시오.

표: 오류 응답
