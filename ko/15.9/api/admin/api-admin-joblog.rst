==========================
JobLog API
==========================

개요
====

JobLog API는 |Fess| 의 작업 실행 로그를 참조 및 관리하기 위한 API입니다.
스케줄 작업이나 크롤링 작업의 실행 이력, 실행 결과, 오류 정보 등을 조회하거나 삭제할 수 있습니다.

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
     - /logs
     - 작업 로그 목록 조회
   * - GET
     - /log/{id}
     - 작업 로그 조회
   * - DELETE
     - /log/{id}
     - 작업 로그 삭제

작업 로그 목록 조회
====================

요청
----------

::

    GET /api/admin/joblog/logs

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
     - 페이지 번호 (1부터 시작, 기본값: 1)
   * - ``id``
     - String
     - 아니오
     - 작업 로그 ID로 필터링 (완전 일치)

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
            "startTime": "1738116000000",
            "endTime": "1738118723000"
          },
          {
            "id": "joblog_id_2",
            "jobName": "Default Crawler",
            "jobStatus": "fail",
            "target": "all",
            "scriptType": "groovy",
            "scriptData": "return container.getComponent(\"crawlJob\").execute();",
            "scriptResult": "Error: Connection timeout",
            "startTime": "1738029600000",
            "endTime": "1738030215000"
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
     - 작업 상태 (``ok``: 성공, ``fail``: 실패, ``running``: 실행 중)
   * - ``target``
     - 실행 대상 (스케줄러의 타겟 이름. 기본값은 ``all``)
   * - ``scriptType``
     - 스크립트 타입 (예: ``groovy``)
   * - ``scriptData``
     - 실행 스크립트
   * - ``scriptResult``
     - 실행 결과
   * - ``startTime``
     - 시작 시각 (에포크 밀리초. 문자열로 반환됨)
   * - ``endTime``
     - 종료 시각 (에포크 밀리초. 문자열로 반환됨). 실행 중인 작업에서는 반환되지 않습니다.

.. note::

   응답의 각 로그 오브젝트에는 내부적으로 사용되는 ``crudMode`` 필드
   (CRUD 작업 모드를 나타내는 정수값으로, 읽기 작업 시 항상 ``0``)가 포함됩니다.
   클라이언트 측에서는 무시해도 됩니다.

작업 로그 조회
==============

요청
----------

::

    GET /api/admin/joblog/log/{id}

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
          "startTime": "1738116000000",
          "endTime": "1738118723000"
        }
      }
    }

지정한 ID의 작업 로그가 존재하지 않는 경우, ``status`` 에 0 이외의 값이 설정된
오류 응답이 반환됩니다.

작업 로그 삭제
==============

요청
----------

::

    DELETE /api/admin/joblog/log/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

지정한 ID의 작업 로그가 존재하지 않는 경우, ``status`` 에 0 이외의 값이 설정된
오류 응답이 반환됩니다.

사용 예
=======

작업 로그 목록 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

실패한 작업만 추출
----------------------

.. code-block:: bash

    # jq로 실패한 작업을 필터링
    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs[] | select(.jobStatus=="fail")'

작업 로그 조회
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

작업 로그 삭제
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/joblog/log/joblog_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

작업 성공률 계산
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/joblog/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '.response.logs | {total: length, ok: [.[] | select(.jobStatus=="ok")] | length, fail: [.[] | select(.jobStatus=="fail")] | length}'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-scheduler` - 스케줄러 API
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/joblog-guide` - 작업 로그 관리 가이드
