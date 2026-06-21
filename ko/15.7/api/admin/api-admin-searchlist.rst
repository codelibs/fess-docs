==========================
SearchList API
==========================

개요
====

SearchList API는 |Fess| 인덱스의 문서를 검색·관리하기 위한 Admin API입니다.
문서의 검색, 취득, 작성, 업데이트, 삭제를 수행할 수 있습니다.

응답의 필드 이름은 모두 ``snake_case`` 입니다. 값이 ``null`` 인 필드는 응답에서 생략됩니다.

기본 URL
========

::

    /api/admin/searchlist

인증
====

이 API를 호출하려면 :doc:`api-admin-overview` 에서 설명하는 액세스 토큰을 통한 인증이 필요합니다.
토큰에는 Admin API에 대한 접근 권한(기본값: ``Radmin-api``)이 부여되어 있어야 합니다.
이 권한은 설정 키 ``api.admin.access.permissions`` 에서 변경할 수 있습니다.

엔드포인트 목록
===============

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET / PUT
     - /docs
     - 문서 검색
   * - GET
     - /doc/{id}
     - 문서 취득
   * - POST
     - /doc
     - 문서 작성
   * - PUT
     - /doc
     - 문서 업데이트
   * - DELETE
     - /doc/{id}
     - 문서 삭제(ID 지정)
   * - DELETE
     - /query
     - 문서 삭제(쿼리 지정)

문서 검색
=========

검색 조건에 일치하는 문서를 검색합니다.

요청
----

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

파라미터
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``q``
     - String
     - 아니요
     - 검색 쿼리(최대 1000자). 미지정 시 전체 문서가 대상이 됩니다.
   * - ``sort``
     - String
     - 아니요
     - 정렬 필드 및 방향(예: ``last_modified.desc``).
   * - ``start``
     - Integer
     - 아니요
     - 0 기반 시작 위치(기본값 ``0``).
   * - ``offset``
     - Integer
     - 아니요
     - ``start`` 로부터의 오프셋(기본값 ``0``).
   * - ``pn``
     - Integer
     - 아니요
     - 페이지 번호.
   * - ``num``
     - Integer
     - 아니요
     - 취득 건수(기본값 ``10``). 설정된 최댓값(기본 ``100``)을 초과하거나 ``0`` 이하인 값은 최댓값으로 클램프됩니다.
   * - ``size``
     - Integer
     - 아니요
     - 취득 건수(``num`` 의 별칭. 다른 Admin API와의 호환성을 위해 제공됩니다).
   * - ``lang``
     - String[]
     - 아니요
     - 검색 언어. 반복 지정 가능(배열). 예: ``en``.
   * - ``ex_q``
     - String[]
     - 아니요
     - 추가 쿼리 식. 반복 지정 가능(배열).
   * - ``fields.<name>``
     - String[]
     - 아니요
     - 필드 값으로 필터링합니다. 가장 일반적인 예는 ``fields.label``(레이블 이름으로 필터링)이며, 임의의 ``fields.<name>`` 은 문서 필드 ``<name>`` 이 지정 값과 일치하는 결과로 좁혀줍니다. 반복 지정 가능합니다.
   * - ``as.<name>``
     - String[]
     - 아니요
     - 고급 검색 조건. 임의의 ``as.<name>``(예: ``as.q``)이 고급 검색 조건 빌더에 전달됩니다. name별로 반복 지정 가능합니다.
   * - ``sdh``
     - String
     - 아니요
     - 유사 문서 해시(similar-document hash).

.. note::

   이 엔드포인트는 패싯·하이라이트·지리(geo) 검색을 지원하지 않습니다. 해당 파라미터를 지정해도 무시됩니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "query_id": "f8b1c2d3e4a5",
        "exec_time": "0.05",
        "query_time": 8,
        "page_size": 20,
        "page_number": 1,
        "record_count": 234,
        "record_count_relation": "eq",
        "page_count": 12,
        "next_page": true,
        "prev_page": false,
        "start_record_number": 1,
        "end_record_number": 20,
        "page_numbers": ["1", "2", "3", "4", "5"],
        "partial": false,
        "search_query": "title:Fess OR content:Fess",
        "requested_time": 1717142400000,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "Sample Page 1",
            "content_description": "..."
          }
        ]
      }
    }

응답 필드
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``version``
     - 실행 중인 |Fess| 의 버전(예시 값은 설명용입니다).
   * - ``status``
     - 상태 코드(``0`` 은 성공. 자세한 내용은 "상태 코드" 참조).
   * - ``query_id``
     - 검색 쿼리 ID.
   * - ``docs``
     - 검색 결과 문서의 배열. 각 문서는 필드 이름과 값의 맵으로, 인덱스의 필드 이름(``doc_id``, ``url``, ``title``, ``content_description`` 등)이 그대로 사용됩니다.
   * - ``exec_time``
     - 검색 실행 시간(초, 문자열).
   * - ``query_time``
     - 검색 엔진의 쿼리 시간(밀리초).
   * - ``page_size``
     - 페이지당 건수.
   * - ``page_number``
     - 현재 페이지 번호.
   * - ``record_count``
     - 일치하는 건수.
   * - ``record_count_relation``
     - 일치 건수의 관계. ``eq`` 는 정확한 건수, ``gte`` 는 하한만 확인된 것을 나타냅니다.
   * - ``page_count``
     - 총 페이지 수.
   * - ``next_page``
     - 다음 페이지 존재 여부(bool).
   * - ``prev_page``
     - 이전 페이지 존재 여부(bool).
   * - ``start_record_number``
     - 이 페이지의 시작 레코드 번호.
   * - ``end_record_number``
     - 이 페이지의 종료 레코드 번호.
   * - ``page_numbers``
     - 페이지네이션에 표시할 페이지 번호 배열(문자열).
   * - ``partial``
     - 결과가 부분적인지 여부(bool).
   * - ``search_query``
     - 실제로 실행된 검색 쿼리.
   * - ``requested_time``
     - 요청 시각(epoch 밀리초).
   * - ``highlight_params``
     - 하이라이트용 쿼리 파라미터 문자열(이 Admin API에서는 보통 비어 있습니다).

문서 취득
=========

문서 ID를 지정하여 문서 1건을 취득합니다.

요청
----

::

    GET /api/admin/searchlist/doc/{id}

파라미터
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``id``
     - String
     - 예
     - 문서 ID(``doc_id`` 의 값. 경로 파라미터).

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "Sample Page 1"
        }
      }
    }

지정한 ID의 문서가 존재하지 않는 경우 오류 응답(``status`` = ``1``)이 반환됩니다.

문서 작성
=========

새 문서를 인덱스에 작성합니다.

요청
----

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "Sample Page 1",
        "content": "This is the body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``doc``
     - 예
     - 등록할 문서. 인덱스의 필드 이름과 값의 맵으로 지정합니다.

``doc`` 에 지정하는 필드 중, ``index.admin.required.fields`` 에 설정된 필수 필드(기본값 ``url,title,role,boost``)는 모두 지정해야 합니다.
일괄 등록용 :doc:`Documents API <api-admin-documents>` 와 달리, 이 엔드포인트는 ``role`` 이나 ``boost`` 등의 기본값을 자동으로 보완하지 않으므로, 필수 필드는 요청에 명시적으로 지정해야 합니다.
``doc_id`` 는 서버 측에서 자동 생성되므로 작성 시에는 지정하지 않습니다.

각 필드의 값은 필드 타입 설정에 따라 검증됩니다. 타입이 일치하지 않으면 오류(``status`` = ``1``)가 반환됩니다.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 설정 키
     - 기본값
   * - ``index.admin.array.fields``
     - ``lang,role,label,anchor,virtual_host``
   * - ``index.admin.date.fields``
     - ``expires,created,timestamp,last_modified``
   * - ``index.admin.integer.fields``
     - (비어 있음)
   * - ``index.admin.long.fields``
     - ``content_length,favorite_count,click_count``
   * - ``index.admin.float.fields``
     - ``boost``
   * - ``index.admin.double.fields``
     - (비어 있음)

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 등록된 문서의 ``doc_id``.
   * - ``created``
     - 작성 시 ``true``.

문서 업데이트
=============

기존 문서를 업데이트합니다.

요청
----

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "Updated Title",
        "content": "This is the updated body text.",
        "role": ["{role}guest"],
        "boost": 1.0
      }
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``doc``
     - 예
     - 업데이트할 문서. 인덱스의 필드 이름과 값의 맵으로 지정합니다.

업데이트 대상 문서는 ``doc`` 내의 ``doc_id`` 로 특정됩니다. ``doc_id`` 가 지정되지 않았거나 해당 문서가 존재하지 않는 경우 오류(``status`` = ``1``)가 반환됩니다.
작성 시와 마찬가지로, ``index.admin.required.fields`` 에 설정된 필수 필드(기본값 ``url,title,role,boost``)는 모두 지정해야 하며, 각 필드의 값은 타입 설정에 따라 검증됩니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 업데이트된 문서의 ``doc_id``.
   * - ``created``
     - 업데이트 시 ``false``.

ID로 문서 삭제
==============

문서 ID를 지정하여 문서를 삭제합니다.

요청
----

::

    DELETE /api/admin/searchlist/doc/{id}

파라미터
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``id``
     - String
     - 예
     - 문서 ID(``doc_id`` 의 값. 경로 파라미터).

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

쿼리로 문서 삭제
================

검색 쿼리에 일치하는 문서를 일괄 삭제합니다.

요청
----

::

    DELETE /api/admin/searchlist/query

파라미터
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``q``
     - String
     - 예
     - 삭제 대상의 검색 쿼리.

삭제 대상은 "문서 검색"과 동일한 방법으로 쿼리가 구성되므로, ``fields.<name>`` 이나 ``ex_q`` 등의 좁히기 파라미터도 함께 사용할 수 있습니다. ``q`` 가 미지정인 경우 오류(``status`` = ``1``)가 반환됩니다.

응답
----

삭제된 문서 건수를 ``count`` 로 반환합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

상태 코드
=========

응답의 ``status`` 필드에는 다음 값 중 하나가 설정됩니다.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - 값
     - 이름
     - 설명
   * - ``0``
     - OK
     - 성공.
   * - ``1``
     - BAD_REQUEST
     - 요청이 잘못됨(필수 필드 누락, 타입 불일치, 대상 문서를 찾을 수 없음, 잘못된 쿼리 등).
   * - ``2``
     - SYSTEM_ERROR
     - 시스템 오류.
   * - ``3``
     - UNAUTHORIZED
     - 인증 오류.
   * - ``9``
     - FAILED
     - 처리 실패.

사용 예
=======

문서 검색
---------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

문서 취득
---------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

문서 작성
---------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/searchlist/doc" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "doc": {
             "url": "https://example.com/page1",
             "title": "Sample Page 1",
             "content": "This is the body text.",
             "role": ["{role}guest"],
             "boost": 1.0
           }
         }'

쿼리로 문서 삭제
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-documents` - 문서 일괄 등록 API
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/searchlist-guide` - 검색 목록 관리 가이드
