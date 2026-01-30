==========================
Scheduler API
==========================

개요
====

Scheduler API는 |Fess| 의 스케줄 작업을 관리하기 위한 API입니다.
크롤링 작업의 시작/중지, 스케줄 설정의 생성/업데이트/삭제 등을 수행할 수 있습니다.

기본 URL
=========

::

    /api/admin/scheduler

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET/PUT
     - /settings
     - 스케줄 작업 목록 조회
   * - GET
     - /setting/{id}
     - 스케줄 작업 조회
   * - POST
     - /setting
     - 스케줄 작업 만들기
   * - PUT
     - /setting
     - 스케줄 작업 업데이트
   * - DELETE
     - /setting/{id}
     - 스케줄 작업 삭제
   * - PUT
     - /{id}/start
     - 작업 시작
   * - PUT
     - /{id}/stop
     - 작업 중지

스케줄 작업 목록 조회
==========================

요청
----------

::

    GET /api/admin/scheduler/settings
    PUT /api/admin/scheduler/settings

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
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": true,
            "crawler": true,
            "available": true,
            "sortOrder": 0,
            "running": false
          }
        ],
        "total": 5
      }
    }

스케줄 작업 조회
======================

요청
----------

::

    GET /api/admin/scheduler/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "job_id_1",
          "name": "Default Crawler",
          "target": "all",
          "cronExpression": "0 0 0 * * ?",
          "scriptType": "groovy",
          "scriptData": "return container.getComponent(\"crawlJob\").execute();",
          "jobLogging": true,
          "crawler": true,
          "available": true,
          "sortOrder": 0,
          "running": false
        }
      }
    }

스케줄 작업 만들기
======================

요청
----------

::

    POST /api/admin/scheduler/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Daily Crawler",
      "target": "all",
      "cronExpression": "0 0 2 * * ?",
      "scriptType": "groovy",
      "scriptData": "return container.getComponent(\"crawlJob\").execute();",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``name``
     - 예
     - 작업 이름
   * - ``target``
     - 예
     - 실행 대상 ("all" 또는 특정 대상)
   * - ``cronExpression``
     - 예
     - Cron 표현식 (초 분 시 일 월 요일)
   * - ``scriptType``
     - 예
     - 스크립트 타입 ("groovy")
   * - ``scriptData``
     - 예
     - 실행 스크립트
   * - ``jobLogging``
     - 아니오
     - 로그 기록 활성화 (기본값: true)
   * - ``crawler``
     - 아니오
     - 크롤러 작업인지 여부 (기본값: false)
   * - ``available``
     - 아니오
     - 활성화/비활성화 (기본값: true)
   * - ``sortOrder``
     - 아니오
     - 표시 순서

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_job_id",
        "created": true
      }
    }

Cron 표현식 예시
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Cron 표현식
     - 설명
   * - ``0 0 2 * * ?``
     - 매일 오전 2시에 실행
   * - ``0 0 0/6 * * ?``
     - 6시간마다 실행
   * - ``0 0 2 * * MON``
     - 매주 월요일 오전 2시에 실행
   * - ``0 0 2 1 * ?``
     - 매월 1일 오전 2시에 실행

스케줄 작업 업데이트
======================

요청
----------

::

    PUT /api/admin/scheduler/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_job_id",
      "name": "Updated Crawler",
      "target": "all",
      "cronExpression": "0 0 3 * * ?",
      "scriptType": "groovy",
      "scriptData": "...",
      "jobLogging": true,
      "crawler": true,
      "available": true,
      "sortOrder": 1,
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_job_id",
        "created": false
      }
    }

스케줄 작업 삭제
======================

요청
----------

::

    DELETE /api/admin/scheduler/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_job_id",
        "created": false
      }
    }

작업 시작
==========

스케줄 작업을 즉시 실행합니다.

요청
----------

::

    PUT /api/admin/scheduler/{id}/start

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

주의 사항
--------

- 작업이 이미 실행 중인 경우 오류가 반환됩니다
- 작업이 비활성화 (``available: false``) 된 경우 오류가 반환됩니다

작업 중지
==========

실행 중인 작업을 중지합니다.

요청
----------

::

    PUT /api/admin/scheduler/{id}/stop

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

사용 예
======

크롤링 작업 만들기 및 실행
--------------------------

.. code-block:: bash

    # 작업 만들기
    curl -X POST "http://localhost:8080/api/admin/scheduler/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Hourly Crawler",
           "target": "all",
           "cronExpression": "0 0 * * * ?",
           "scriptType": "groovy",
           "scriptData": "return container.getComponent(\"crawlJob\").execute();",
           "jobLogging": true,
           "crawler": true,
           "available": true
         }'

    # 작업을 즉시 실행
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

작업 상태 확인
----------------

.. code-block:: bash

    # 모든 작업의 상태 확인
    curl "http://localhost:8080/api/admin/scheduler/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # running 필드로 실행 상태를 확인할 수 있습니다

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-joblog` - 작업 로그 API
- :doc:`../../admin/scheduler-guide` - 스케줄러 관리 가이드
