==========================
Log API
==========================

개요
====

Log API는 |Fess| 의 로그 정보를 조회하기 위한 API입니다.
검색 로그, 크롤러 로그, 시스템 로그 등을 참조할 수 있습니다.

기본 URL
=========

::

    /api/admin/log

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /search
     - 검색 로그 조회
   * - GET
     - /click
     - 클릭 로그 조회
   * - GET
     - /favorite
     - 즐겨찾기 로그 조회
   * - DELETE
     - /search/delete
     - 검색 로그 삭제

검색 로그 조회
============

요청
----------

::

    GET /api/admin/log/search

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``size``
     - Integer
     - 아니오
     - 페이지당 건수 (기본값: 20)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (0부터 시작)
   * - ``from``
     - String
     - 아니오
     - 시작 일시 (ISO 8601 형식)
   * - ``to``
     - String
     - 아니오
     - 종료 일시 (ISO 8601 형식)
   * - ``query``
     - String
     - 아니오
     - 검색 쿼리 필터

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "log_id_1",
            "queryId": "query_id_1",
            "query": "fess search",
            "requestedAt": "2025-01-29T10:30:00Z",
            "responseTime": 123,
            "hitCount": 567,
            "user": "guest",
            "roles": ["guest"],
            "languages": ["ja"],
            "clientIp": "192.168.1.100",
            "userAgent": "Mozilla/5.0..."
          }
        ],
        "total": 1234
      }
    }

클릭 로그 조회
================

요청
----------

::

    GET /api/admin/log/click

파라미터
~~~~~~~~~~~~

검색 로그와 동일한 파라미터 외에 다음 항목을 지정 가능:

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``url``
     - String
     - 아니오
     - 클릭된 URL 필터
   * - ``queryId``
     - String
     - 아니오
     - 검색 쿼리 ID 필터

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "click_log_id_1",
            "queryId": "query_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "order": 1,
            "clickedAt": "2025-01-29T10:31:00Z",
            "user": "guest",
            "clientIp": "192.168.1.100"
          }
        ],
        "total": 567
      }
    }

즐겨찾기 로그 조회
==================

요청
----------

::

    GET /api/admin/log/favorite

파라미터
~~~~~~~~~~~~

클릭 로그와 동일한 파라미터

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "favorite_log_id_1",
            "url": "https://example.com/doc1",
            "docId": "doc_id_1",
            "createdAt": "2025-01-29T10:32:00Z",
            "user": "user123"
          }
        ],
        "total": 123
      }
    }

검색 로그 삭제
============

요청
----------

::

    DELETE /api/admin/log/search/delete

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``before``
     - String
     - 예
     - 이 일시 이전의 로그를 삭제 (ISO 8601 형식)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deletedCount": 5678
      }
    }

사용 예
======

최근 검색 로그 조회
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 기간의 검색 로그
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 쿼리의 검색 로그
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/search?query=fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

클릭 로그 조회
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/click?size=100" \
         -H "Authorization: Bearer YOUR_TOKEN"

오래된 검색 로그 삭제
------------------

.. code-block:: bash

    # 30일 이전 로그 삭제
    curl -X DELETE "http://localhost:8080/api/admin/log/search/delete?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-stats` - 통계 API
- :doc:`../../admin/log-guide` - 로그 관리 가이드
