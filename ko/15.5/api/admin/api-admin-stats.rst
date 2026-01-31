==========================
Stats API
==========================

개요
====

Stats API는 |Fess| 의 통계 정보를 조회하기 위한 API입니다.
검색 쿼리, 클릭, 즐겨찾기 등의 통계 데이터를 확인할 수 있습니다.

기본 URL
=========

::

    /api/admin/stats

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
     - 통계 정보 조회

통계 정보 조회
============

요청
----------

::

    GET /api/admin/stats

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
   * - ``type``
     - String
     - 아니오
     - 통계 타입 (query/click/favorite)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 12345,
          "uniqueQueries": 5678,
          "totalClicks": 9876,
          "totalFavorites": 543,
          "averageResponseTime": 123.45,
          "topQueries": [
            {
              "query": "fess",
              "count": 567
            },
            {
              "query": "search",
              "count": 432
            }
          ],
          "topClickedDocuments": [
            {
              "url": "https://example.com/doc1",
              "title": "Document 1",
              "count": 234
            }
          ],
          "queryTrends": [
            {
              "date": "2025-01-01",
              "count": 234
            },
            {
              "date": "2025-01-02",
              "count": 267
            }
          ]
        }
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``totalQueries``
     - 총 검색 쿼리 수
   * - ``uniqueQueries``
     - 고유 검색 쿼리 수
   * - ``totalClicks``
     - 총 클릭 수
   * - ``totalFavorites``
     - 총 즐겨찾기 수
   * - ``averageResponseTime``
     - 평균 응답 시간 (밀리초)
   * - ``topQueries``
     - 인기 검색 쿼리
   * - ``topClickedDocuments``
     - 인기 문서
   * - ``queryTrends``
     - 쿼리 트렌드

검색 쿼리 통계
==============

요청
----------

::

    GET /api/admin/stats?type=query&from=2025-01-01&to=2025-01-31

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalQueries": 5678,
          "uniqueQueries": 2345,
          "topQueries": [
            {
              "query": "documentation",
              "count": 234,
              "avgResponseTime": 98.7
            }
          ],
          "queriesByHour": [
            {
              "hour": 0,
              "count": 45
            },
            {
              "hour": 1,
              "count": 23
            }
          ],
          "queriesByDay": [
            {
              "day": "Monday",
              "count": 567
            }
          ]
        }
      }
    }

클릭 통계
============

요청
----------

::

    GET /api/admin/stats?type=click&from=2025-01-01&to=2025-01-31

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "stats": {
          "totalClicks": 3456,
          "topClickedDocuments": [
            {
              "url": "https://example.com/popular-doc",
              "title": "Popular Document",
              "count": 234,
              "clickThroughRate": 0.45
            }
          ],
          "clicksByPosition": [
            {
              "position": 1,
              "count": 1234
            },
            {
              "position": 2,
              "count": 567
            }
          ]
        }
      }
    }

사용 예
======

전체 통계 정보 조회
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

기간 지정 통계 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

검색 쿼리 통계 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query&from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

인기 쿼리 TOP10 조회
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats?type=query" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.stats.topQueries[:10]'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-log` - 로그 API
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`../../admin/stats-guide` - 통계 관리 가이드
