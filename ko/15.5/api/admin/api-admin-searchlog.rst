==========================
SearchLog API
==========================

개요
====

SearchLog API는 |Fess| 의 검색 로그를 조회 및 관리하기 위한 API입니다.
사용자의 검색 행동 분석, 검색 품질 개선에 활용할 수 있습니다.

기본 URL
=========

::

    /api/admin/searchlog

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /
     - 검색 로그 목록 조회
   * - GET
     - /{id}
     - 검색 로그 상세 조회
   * - DELETE
     - /{id}
     - 검색 로그 삭제
   * - DELETE
     - /delete-all
     - 검색 로그 일괄 삭제
   * - GET
     - /stats
     - 검색 통계 조회

검색 로그 목록 조회
================

요청
----------

::

    GET /api/admin/searchlog

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
     - 검색 쿼리로 필터
   * - ``user``
     - String
     - 아니오
     - 사용자 ID로 필터

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "searchlog_id_1",
            "searchWord": "Fess 설치",
            "requestedAt": "2025-01-29T10:00:00Z",
            "responseTime": 125,
            "hitCount": 234,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user001",
            "userSessionId": "session_abc123",
            "clientIp": "192.168.1.100",
            "referer": "https://example.com/",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user", "admin"],
            "languages": ["ja"]
          },
          {
            "id": "searchlog_id_2",
            "searchWord": "검색 설정",
            "requestedAt": "2025-01-29T09:55:00Z",
            "responseTime": 98,
            "hitCount": 567,
            "queryOffset": 0,
            "queryPageSize": 10,
            "user": "user002",
            "userSessionId": "session_def456",
            "clientIp": "192.168.1.101",
            "referer": "",
            "userAgent": "Mozilla/5.0 ...",
            "roles": ["user"],
            "languages": ["ja", "en"]
          }
        ],
        "total": 10000
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 검색 로그 ID
   * - ``searchWord``
     - 검색 키워드
   * - ``requestedAt``
     - 검색 일시
   * - ``responseTime``
     - 응답 시간 (밀리초)
   * - ``hitCount``
     - 히트 건수
   * - ``queryOffset``
     - 결과의 오프셋
   * - ``queryPageSize``
     - 페이지 크기
   * - ``user``
     - 사용자 ID
   * - ``userSessionId``
     - 세션 ID
   * - ``clientIp``
     - 클라이언트 IP 주소
   * - ``referer``
     - 리퍼러
   * - ``userAgent``
     - 사용자 에이전트
   * - ``roles``
     - 사용자 역할
   * - ``languages``
     - 검색 언어

검색 로그 상세 조회
================

요청
----------

::

    GET /api/admin/searchlog/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "searchlog_id_1",
          "searchWord": "Fess 설치",
          "requestedAt": "2025-01-29T10:00:00Z",
          "responseTime": 125,
          "hitCount": 234,
          "queryOffset": 0,
          "queryPageSize": 10,
          "user": "user001",
          "userSessionId": "session_abc123",
          "clientIp": "192.168.1.100",
          "referer": "https://example.com/",
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
          "roles": ["user", "admin"],
          "languages": ["ja"],
          "clickLogs": [
            {
              "url": "https://fess.codelibs.org/install.html",
              "docId": "doc_123",
              "order": 1,
              "clickedAt": "2025-01-29T10:00:15Z"
            }
          ]
        }
      }
    }

검색 로그 삭제
============

요청
----------

::

    DELETE /api/admin/searchlog/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search log deleted successfully"
      }
    }

검색 로그 일괄 삭제
================

요청
----------

::

    DELETE /api/admin/searchlog/delete-all

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
     - 아니오
     - 이 일시 이전의 로그를 삭제 (ISO 8601 형식)
   * - ``user``
     - String
     - 아니오
     - 특정 사용자의 로그만 삭제

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Search logs deleted successfully",
        "deletedCount": 5000
      }
    }

검색 통계 조회
============

요청
----------

::

    GET /api/admin/searchlog/stats

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``from``
     - String
     - 아니오
     - 시작 일시 (ISO 8601 형식)
   * - ``to``
     - String
     - 아니오
     - 종료 일시 (ISO 8601 형식)
   * - ``interval``
     - String
     - 아니오
     - 집계 간격 (hour/day/week/month)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalSearches": 50000,
          "uniqueUsers": 1234,
          "averageResponseTime": 156,
          "averageHitCount": 345,
          "zeroHitRate": 0.05,
          "topSearchWords": [
            {"word": "Fess", "count": 1500},
            {"word": "설치", "count": 800},
            {"word": "설정", "count": 650}
          ],
          "searchesByDate": [
            {"date": "2025-01-29", "count": 2500},
            {"date": "2025-01-28", "count": 2300},
            {"date": "2025-01-27", "count": 2100}
          ]
        }
      }
    }

사용 예
======

검색 로그 목록 조회
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

기간 지정 조회
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?from=2025-01-01T00:00:00Z&to=2025-01-31T23:59:59Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 사용자의 검색 로그
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?user=user001" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 키워드의 검색 로그
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog?query=Fess" \
         -H "Authorization: Bearer YOUR_TOKEN"

검색 통계 조회
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31&interval=day" \
         -H "Authorization: Bearer YOUR_TOKEN"

오래된 검색 로그 삭제
------------------

.. code-block:: bash

    # 30일 이전 로그 삭제
    curl -X DELETE "http://localhost:8080/api/admin/searchlog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

인기 검색 키워드 추출
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.topSearchWords'

검색 품질 분석
--------------

.. code-block:: bash

    # 제로 히트율 확인
    curl -X GET "http://localhost:8080/api/admin/searchlog/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '{zeroHitRate: .response.stats.zeroHitRate, averageHitCount: .response.stats.averageHitCount}'

일별 검색 수 추이
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/searchlog/stats?interval=day&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.stats.searchesByDate'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-stats` - 시스템 통계 API
- :doc:`../../admin/searchlog-guide` - 검색 로그 관리 가이드
- :doc:`../../config/admin-opensearch-dashboards` - 검색 분석 설정 가이드
