==========================
SearchList API
==========================

개요
====

SearchList API는 |Fess| 의 인덱스 내 문서를 검색하고 관리하기 위한 API입니다.
문서의 검색, 조회, 생성, 업데이트, 삭제를 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/searchlist

엔드포인트 목록
==================

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
     - 문서 조회
   * - POST
     - /doc
     - 문서 생성
   * - PUT
     - /doc
     - 문서 업데이트
   * - DELETE
     - /doc/{id}
     - 문서 삭제 (ID 지정)
   * - DELETE
     - /query
     - 문서 삭제 (쿼리 지정)

문서 검색
================

검색 조건에 일치하는 문서를 검색합니다.

요청
----------

::

    GET /api/admin/searchlist/docs
    PUT /api/admin/searchlist/docs

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``q``
     - String
     - 아니오
     - 검색 쿼리. 미지정 시 전체 건이 대상이 됩니다.
   * - ``sort``
     - String
     - 아니오
     - 정렬 필드와 방향
   * - ``start``
     - Integer
     - 아니오
     - 검색 결과의 시작 위치
   * - ``offset``
     - Integer
     - 아니오
     - 페이징 오프셋
   * - ``num``
     - Integer
     - 아니오
     - 조회 건수
   * - ``size``
     - Integer
     - 아니오
     - 조회 건수 ( ``num`` 의 별칭)
   * - ``lang``
     - String[]
     - 아니오
     - 언어

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "queryId": "...",
        "execTime": "0.05",
        "pageSize": 20,
        "pageNumber": 1,
        "recordCount": 234,
        "recordCountRelation": "EQUAL_TO",
        "pageCount": 12,
        "docs": [
          {
            "doc_id": "abcdef0123456789",
            "url": "https://example.com/page1",
            "title": "サンプルページ1",
            "content_description": "..."
          }
        ]
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``queryId``
     - 검색 쿼리 ID
   * - ``docs``
     - 검색 결과 문서의 배열
   * - ``execTime``
     - 검색 실행 시간
   * - ``pageSize``
     - 페이지당 건수
   * - ``pageNumber``
     - 현재 페이지 번호
   * - ``recordCount``
     - 해당 건수
   * - ``recordCountRelation``
     - 해당 건수의 관계 (완전 일치 또는 하한값)
   * - ``pageCount``
     - 전체 페이지 수

문서 조회
================

문서 ID를 지정하여 한 건의 문서를 조회합니다.

요청
----------

::

    GET /api/admin/searchlist/doc/{id}

파라미터
~~~~~~~~~~~~

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
     - 문서 ID ( ``doc_id`` , 경로 파라미터)

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "doc": {
          "doc_id": "abcdef0123456789",
          "url": "https://example.com/page1",
          "title": "サンプルページ1"
        }
      }
    }

문서 생성
================

새 문서를 인덱스에 생성합니다.

요청
----------

::

    POST /api/admin/searchlist/doc
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "url": "https://example.com/page1",
        "title": "サンプルページ1",
        "content": "本文テキストです。"
      }
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``doc``
     - 예
     - 등록할 문서. 필드 이름과 값의 맵으로 지정합니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": true
      }
    }

문서 업데이트
================

기존 문서를 업데이트합니다.

요청
----------

::

    PUT /api/admin/searchlist/doc
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "doc": {
        "doc_id": "abcdef0123456789",
        "url": "https://example.com/page1",
        "title": "更新後のタイトル",
        "content": "更新後の本文テキストです。"
      }
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``doc``
     - 예
     - 업데이트할 문서. 필드 이름과 값의 맵으로 지정합니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "abcdef0123456789",
        "created": false
      }
    }

문서 삭제 (ID 지정)
==========================

문서 ID를 지정하여 삭제합니다.

요청
----------

::

    DELETE /api/admin/searchlist/doc/{id}

파라미터
~~~~~~~~~~~~

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
     - 문서 ID ( ``doc_id`` , 경로 파라미터)

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

문서 삭제 (쿼리 지정)
==============================

검색 쿼리에 일치하는 문서를 일괄 삭제합니다.

요청
----------

::

    DELETE /api/admin/searchlist/query

파라미터
~~~~~~~~~~~~

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
     - 삭제 대상 검색 쿼리

응답
----------

삭제된 문서 건수를 ``count`` 로 반환합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "count": 150
      }
    }

사용 예
======

문서 검색
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/docs?q=Fess&size=20" \
         -H "Authorization: Bearer YOUR_TOKEN"

문서 조회
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlist/doc/abcdef0123456789" \
         -H "Authorization: Bearer YOUR_TOKEN"

쿼리 지정으로 문서 삭제
------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/searchlist/query?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-documents` - 문서 일괄 등록 API
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/searchlist-guide` - 검색 목록 관리 가이드
