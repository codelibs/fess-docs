======
검색 API
======

검색 결과 조회
===========

요청
--------

==================  ====================================================
HTTP 메서드         GET
엔드포인트        ``/api/v1/documents``
==================  ====================================================

|Fess| 에,
``http://<Server Name>/api/v1/documents?q=검색어``
와 같은 요청을 전송하여,
|Fess| 의 검색 결과를 JSON 형식으로 받을 수 있습니다.
검색 API를 사용하려면 관리 화면의 시스템 > 일반 설정에서 JSON 응답을 활성화해야 합니다.

요청 매개변수
-----------------

``http://<Server Name>/api/v1/documents?q=검색어&num=50&fields.label=fess``
와 같이 요청 매개변수를 지정하여 더 고급 검색을 수행할 수 있습니다.
사용 가능한 요청 매개변수는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - 검색어. URL 인코딩하여 전달합니다.
   * - start
     - 시작 레코드 위치. 0부터 시작합니다.
   * - num
     - 표시 건수. 기본값은 20건입니다. 최대 100건까지 표시할 수 있습니다.
   * - sort
     - 정렬. 검색 결과를 정렬할 때 사용합니다.
   * - fields.label
     - 레이블 값. 레이블을 지정할 때 사용합니다.
   * - facet.field
     - 패싯 필드 지정. (예) ``facet.field=label``
   * - facet.query
     - 패싯 쿼리 지정.     (예) ``facet.query=timestamp:[now/d-1d TO *]``
   * - facet.size
     - 조회할 패싯의 최대 건수 지정. facet.field가 지정된 경우 유효합니다.
   * - facet.minDocCount
     - 건수가 이 값 이상인 패싯을 조회합니다. facet.field가 지정된 경우 유효합니다.
   * - geo.location.point
     - 위도 경도 지정. (예) ``geo.location.point=35.0,139.0``
   * - geo.location.distance
     - 중심점으로부터의 거리 지정. (예) ``geo.location.distance=10km``
   * - lang
     - 검색 언어 지정. (예) ``lang=en``
   * - preference
     - 검색 시 샤드를 지정하는 문자열. (예) ``preference=abc``
   * - callback
     - JSONP를 사용할 때의 콜백 이름. JSONP를 사용하지 않는 경우 지정할 필요가 없습니다.

표: 요청 매개변수


응답
--------

| 다음과 같은 응답이 반환됩니다.
| (포맷팅 후)

::

    {
      "q": "Fess",
      "query_id": "bd60f9579a494dfd8c03db7c8aa905b0",
      "exec_time": 0.21,
      "query_time": 0,
      "page_size": 20,
      "page_number": 1,
      "record_count": 31625,
      "page_count": 1,
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
        "5"
      ],
      "partial": false,
      "search_query": "(Fess OR n2sm)",
      "requested_time": 1507822131845,
      "related_query": [
        "aaa"
      ],
      "related_contents": [],
      "data": [
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
          "created": "2017-10-10T15.30:48.609Z",
          "site_path": "fess.codelibs.org/",
          "doc_id": "e79fbfdfb09d4bffb58ec230c68f6f7e",
          "url": "https://fess.codelibs.org/",
          "content_description": "Enterprise Search Server: <strong>Fess</strong> Commercial Support Open...Search Server: <strong>Fess</strong> What is <strong>Fess</strong> ? <strong>Fess</strong> is very powerful...You can install and run <strong>Fess</strong> quickly on any platforms...Java runtime environment. <strong>Fess</strong> is provided under Apache...Apache license. Demo <strong>Fess</strong> is OpenSearch-based search",
          "site": "fess.codelibs.org/",
          "boost": "10.0",
          "mimetype": "text/html"
        }
      ]
    }

각 요소는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 응답 정보

   * - q
     - 검색어
   * - exec_time
     - 응답 시간(단위: 초)
   * - query_time
     - 쿼리 처리 시간(단위: 밀리초)
   * - page_size
     - 표시 건수
   * - page_number
     - 페이지 번호
   * - record_count
     - 검색어에 대해 히트한 건수
   * - page_count
     - 검색어에 대해 히트한 건수의 페이지 수
   * - highlight_params
     - 하이라이트 매개변수
   * - next_page
     - true: 다음 페이지가 존재함. false: 다음 페이지가 존재하지 않음.
   * - prev_page
     - true: 이전 페이지가 존재함. false: 이전 페이지가 존재하지 않음.
   * - start_record_number
     - 레코드 번호의 시작 위치
   * - end_record_number
     - 레코드 번호의 종료 위치
   * - page_numbers
     - 페이지 번호 배열
   * - partial
     - 검색이 타임아웃되는 등 검색 결과가 중단된 경우 true가 됨.
   * - search_query
     - 검색 쿼리
   * - requested_time
     - 요청 시각(단위: epoch 밀리초)
   * - related_query
     - 관련 쿼리
   * - related_contents
     - 관련 콘텐츠 쿼리
   * - facet_field
     - 주어진 패싯 필드에 히트하는 문서 정보 (요청 매개변수에 ``facet.field`` 가 주어진 경우만)
   * - facet_query
     - 주어진 패싯 쿼리에 히트하는 문서 수 (요청 매개변수에 ``facet.query`` 가 주어진 경우만)
   * - result
     - 검색 결과의 부모 요소
   * - filetype
     - 파일 유형
   * - created
     - 문서 생성 일시
   * - title
     - 문서 제목
   * - doc_id
     - 문서 ID
   * - url
     - 문서 URL
   * - site
     - 사이트명
   * - content_description
     - 콘텐츠 설명
   * - host
     - 호스트명
   * - digest
     - 문서 요약 문자열
   * - boost
     - 문서 부스트 값
   * - mimetype
     - MIME 타입
   * - last_modified
     - 최종 수정 일시
   * - content_length
     - 문서 크기
   * - url_link
     - 검색 결과로서의 URL
   * - timestamp
     - 문서 갱신 일시


모든 문서 검색
==================

대상의 모든 문서를 검색하려면 다음 요청을 전송합니다.
``http://<Server Name>/api/v1/documents/all?q=검색어``

이 기능을 사용하려면 fess_config.properties에서 api.search.scroll을 true로 설정해야 합니다.

요청 매개변수
-----------------

사용 가능한 요청 매개변수는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - q
     - 검색어. URL 인코딩하여 전달합니다.
   * - num
     - 표시 건수. 기본값은 20건입니다. 최대 100건까지 표시할 수 있습니다.
   * - sort
     - 정렬. 검색 결과를 정렬할 때 사용합니다.

표: 요청 매개변수

오류 응답
==============

검색 API가 실패한 경우 다음과 같은 오류 응답이 반환됩니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청 매개변수가 올바르지 않은 경우
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우

오류 응답 예:

::

    {
      "message": "Invalid request parameter",
      "status": 400
    }
