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
   * - GET
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
     - 페이지당 건수（기본값: 25。``fess_config.properties`` 의 ``paging.page.size`` 로 변경 가능）
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호（1부터 시작。기본값: 1）

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "job_id_1",
            "name": "Default Crawler",
            "target": "all",
            "cronExpression": "0 0 0 * * ?",
            "scriptType": "groovy",
            "scriptData": "...",
            "jobLogging": "true",
            "crawler": "true",
            "available": "true",
            "sortOrder": 0,
            "versionNo": 1,
            "running": false
          }
        ],
        "total": 5
      }
    }

.. note::

   ``response`` 오브젝트에는 제품 버전을 나타내는 ``version`` 과 처리 결과를 나타내는 ``status`` 가 항상 포함됩니다（공통 사양은 :doc:`api-admin-overview` 를 참조）。이후 예시에서는 간결함을 위해 ``version`` 을 생략하는 경우가 있습니다.

.. note::

   응답의 ``jobLogging`` / ``crawler`` / ``available`` 은 문자열（``"true"`` / ``"false"``）로 반환됩니다. ``running`` 은 불리언 값으로, 작업이 현재 실행 중인지 여부를 나타내는 응답 전용 필드입니다（요청에서는 지정할 수 없습니다）。``total`` 은 조건에 일치하는 전체 작업 수입니다.

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
          "jobLogging": "true",
          "crawler": "true",
          "available": "true",
          "sortOrder": 0,
          "versionNo": 1,
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
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
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
     - 작업 이름（최대 100자）
   * - ``target``
     - 예
     - 실행 대상（최대 100자）。``all`` 또는 특정 대상 이름을 지정합니다
   * - ``cronExpression``
     - 아니오
     - Cron 표현식（초 분 시 일 월 요일）。최대 100자이며 Cron 표현식으로 검증됩니다. 비어 있으면 스케줄 실행되지 않고 수동으로만 시작할 수 있습니다
   * - ``scriptType``
     - 예
     - 스크립트 타입（최대 100자）。현재는 ``groovy`` 만 지원됩니다
   * - ``scriptData``
     - 아니오
     - 실행 스크립트。최대 크기는 ``fess_config.properties`` 의 ``form.admin.max.input.size`` 에 따릅니다
   * - ``jobLogging``
     - 아니오
     - 작업 로그 기록 활성화（문자열）
   * - ``crawler``
     - 아니오
     - 크롤러 작업인지 여부（문자열）
   * - ``available``
     - 아니오
     - 활성화/비활성화（문자열）
   * - ``sortOrder``
     - 예
     - 표시 순서（0〜2147483647의 정수）

.. note::

   ``jobLogging`` / ``crawler`` / ``available`` 은 문자열 필드입니다. 요청에서 ``"on"`` 또는 ``"true"``（대소문자 구분 없음）를 지정하면 활성화되며, 그 외의 값（``"false"``, 빈 문자열, 미지정 등）은 비활성화로 처리됩니다. 응답에서는 ``"true"`` / ``"false"`` 로 반환됩니다.

.. note::

   ``crudMode`` 는 서버 측에서 자동으로 설정되므로 요청에서 지정할 필요가 없습니다. ``createdBy`` / ``createdTime`` 등의 감사 필드도 서버 측에서 설정됩니다.

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
      "jobLogging": "true",
      "crawler": "true",
      "available": "true",
      "sortOrder": 1,
      "versionNo": 1
    }

.. note::

   업데이트 시 ``id``（최대 1000자）와 ``versionNo`` 는 필수입니다. ``versionNo`` 는 낙관적 잠금에 사용되며, 조회 시 응답에 포함된 값을 지정합니다. 값이 일치하지 않으면 업데이트가 실패합니다. 그 밖의 필수 필드（``name`` / ``target`` / ``scriptType`` / ``sortOrder``）는 작성 시와 동일합니다.

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
        "status": 0,
        "jobLogId": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``jobLogId``
     - 시작된 작업의 작업 로그 ID. 작업 로그가 활성화된 경우에 발행됩니다. 작업 로그가 비활성화된 경우에는 ``null`` 이 됩니다.

주의 사항
--------

- 작업이 이미 실행 중인 경우 시작에 실패하고 오류（``status`` 가 ``0`` 이 아닌 값）가 반환됩니다
- 작업이 비활성화（``available`` 이 활성화되지 않은）된 경우에도 마찬가지로 시작에 실패하고 오류가 반환됩니다
- ``jobLogId`` 는 작업 로그가 활성화（``jobLogging`` 이 활성화）된 경우에만 발행됩니다

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
           "jobLogging": "true",
           "crawler": "true",
           "available": "true",
           "sortOrder": 1
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
