==========================
CrawlingInfo API
==========================

개요
====

CrawlingInfo API는 |Fess| 의 크롤링 정보를 조회하기 위한 API입니다.
크롤링 세션의 상태, 진행 상황, 통계 정보 등을 참조할 수 있습니다.

기본 URL
=========

::

    /api/admin/crawlinginfo

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
     - 크롤링 정보 목록 조회
   * - GET
     - /{sessionId}
     - 크롤링 세션 상세 조회
   * - DELETE
     - /{sessionId}
     - 크롤링 세션 삭제

크롤링 정보 목록 조회
====================

요청
----------

::

    GET /api/admin/crawlinginfo

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

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "sessions": [
          {
            "sessionId": "session_20250129_100000",
            "name": "Default Crawler",
            "status": "running",
            "startTime": "2025-01-29T10:00:00Z",
            "endTime": null,
            "crawlingInfoCount": 567,
            "createdDocCount": 234,
            "updatedDocCount": 123,
            "deletedDocCount": 12
          },
          {
            "sessionId": "session_20250128_100000",
            "name": "Default Crawler",
            "status": "completed",
            "startTime": "2025-01-28T10:00:00Z",
            "endTime": "2025-01-28T10:45:23Z",
            "crawlingInfoCount": 1234,
            "createdDocCount": 456,
            "updatedDocCount": 678,
            "deletedDocCount": 23
          }
        ],
        "total": 10
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``sessionId``
     - 세션 ID
   * - ``name``
     - 크롤러 이름
   * - ``status``
     - 상태 (running/completed/failed)
   * - ``startTime``
     - 시작 시각
   * - ``endTime``
     - 종료 시각
   * - ``crawlingInfoCount``
     - 크롤링 정보 수
   * - ``createdDocCount``
     - 생성 문서 수
   * - ``updatedDocCount``
     - 업데이트 문서 수
   * - ``deletedDocCount``
     - 삭제 문서 수

크롤링 세션 상세 조회
==========================

요청
----------

::

    GET /api/admin/crawlinginfo/{sessionId}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "session": {
          "sessionId": "session_20250129_100000",
          "name": "Default Crawler",
          "status": "running",
          "startTime": "2025-01-29T10:00:00Z",
          "endTime": null,
          "crawlingInfoCount": 567,
          "createdDocCount": 234,
          "updatedDocCount": 123,
          "deletedDocCount": 12,
          "infos": [
            {
              "url": "https://example.com/page1",
              "status": "OK",
              "method": "GET",
              "httpStatusCode": 200,
              "contentLength": 12345,
              "executionTime": 123,
              "lastModified": "2025-01-29T09:55:00Z"
            }
          ]
        }
      }
    }

크롤링 세션 삭제
======================

요청
----------

::

    DELETE /api/admin/crawlinginfo/{sessionId}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Crawling session deleted successfully"
      }
    }

사용 예
======

크롤링 정보 목록 조회
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

실행 중인 크롤링 세션 조회
------------------------------

.. code-block:: bash

    # 모든 세션을 조회하여 running 필터링
    curl -X GET "http://localhost:8080/api/admin/crawlinginfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.sessions[] | select(.status=="running")'

특정 세션의 상세 조회
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/session_20250129_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

오래된 세션 삭제
--------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/session_20250101_100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

진행 상황 모니터링
--------------

.. code-block:: bash

    # 실행 중인 세션의 진행 상황을 정기적으로 확인
    while true; do
      curl -s "http://localhost:8080/api/admin/crawlinginfo" \
           -H "Authorization: Bearer YOUR_TOKEN" | \
           jq '.response.sessions[] | select(.status=="running") | {sessionId, crawlingInfoCount, createdDocCount}'
      sleep 10
    done

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-failureurl` - 실패 URL API
- :doc:`api-admin-joblog` - 작업 로그 API
- :doc:`../../admin/crawlinginfo-guide` - 크롤링 정보 가이드
