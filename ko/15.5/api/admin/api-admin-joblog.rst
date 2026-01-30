==========================
JobLog API
==========================

개요
====

JobLog API는 |Fess| 의 작업 실행 로그를 조회하기 위한 API입니다.
스케줄 작업이나 크롤링 작업의 실행 이력, 오류 정보 등을 확인할 수 있습니다.

기본 URL
=========

::

    /api/admin/joblog

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
     - 작업 로그 목록 조회
   * - GET
     - /{id}
     - 작업 로그 상세 조회
   * - DELETE
     - /{id}
     - 작업 로그 삭제
   * - DELETE
     - /delete-all
     - 모든 작업 로그 삭제

작업 로그 목록 조회
==================

요청
----------

::

    GET /api/admin/joblog

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
   * - ``status``
     - String
     - 아니오
     - 상태 필터 (ok/fail/running)
   * - ``from``
     - String
     - 아니오
     - 시작 일시 (ISO 8601 형식)
   * - ``to``
     - String
     - 아니오
     - 종료 일시 (ISO 8601 형식)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "joblog_id_1",
            "jobName": "Default Crawler",
            "jobStatus": "ok",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Job completed successfully",
            "startTime": "2025-01-29T02:00:00Z",
            "endTime": "2025-01-29T02:45:23Z",
            "executionTime": 2723000
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "2025-01-28T02:00:00Z",
            "endTime": "2025-01-28T02:10:15Z",
            "executionTime": 615000
          }
        ],
        "total": 100
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
     - 작업 로그 ID
   * - ``jobName``
     - 작업 이름
   * - ``jobStatus``
     - 작업 상태 (ok/fail/running)
   * - ``target``
     - 실행 대상
   * - ``scriptType``
     - 스크립트 타입
   * - ``scriptData``
     - 실행 스크립트
   * - ``scriptResult``
     - 실행 결과
   * - ``startTime``
     - 시작 시각
   * - ``endTime``
     - 종료 시각
   * - ``executionTime``
     - 실행 시간 (밀리초)

작업 로그 상세 조회
==================

요청
----------

::

    GET /api/admin/joblog/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "joblog_id_1",
          "jobName": "Default Crawler",
          "jobStatus": "ok",
          "target": "all",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "scriptResult": "Crawl completed successfully.\nDocuments indexed: 1234\nDocuments updated: 567\nDocuments deleted: 12\nErrors: 0",
          "startTime": "2025-01-29T02:00:00Z",
          "endTime": "2025-01-29T02:45:23Z",
          "executionTime": 2723000
        }
      }
    }

작업 로그 삭제
==============

요청
----------

::

    DELETE /api/admin/joblog/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job log deleted successfully"
      }
    }

모든 작업 로그 삭제
================

요청
----------

::

    DELETE /api/admin/joblog/delete-all

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
     - 이 일시 이전의 로그 삭제 (ISO 8601 형식)
   * - ``status``
     - String
     - 아니오
     - 특정 상태의 로그만 삭제

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Job logs deleted successfully",
        "deletedCount": 50
      }
    }

사용 예
======

작업 로그 목록 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

실패한 작업만 조회
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 기간의 작업 로그
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?from=2025-01-01&to=2025-01-31" \
         -H "Authorization: Bearer YOUR_TOKEN"

작업 로그 상세 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

오래된 작업 로그 삭제
--------------------

.. code-block:: bash

    # 30일 이전 로그 삭제
    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?before=2024-12-30T00:00:00Z" \
         -H "Authorization: Bearer YOUR_TOKEN"

실패한 작업 로그만 삭제
--------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/delete-all?status=fail" \
         -H "Authorization: Bearer YOUR_TOKEN"

실행 시간이 긴 작업 검출
--------------------------

.. code-block:: bash

    # 1시간 이상 걸린 작업 추출
    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.executionTime > 3600000) | {jobName, startTime, executionTime}'

작업 성공률 계산
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-scheduler` - 스케줄러 API
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/joblog-guide` - 작업 로그 관리 가이드
