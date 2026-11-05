==========================
CrawlingInfo API
==========================

개요
====

CrawlingInfo API는 |Fess| 의 크롤링 정보(크롤링 세션)를 참조 및 관리하기 위한 API입니다.
크롤링 세션의 목록 조회, 개별 조회, 삭제 등을 조작할 수 있습니다.

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
     - /logs
     - 크롤링 정보 목록 조회
   * - GET
     - /progress
     - 실행 중인 크롤링의 진행 상황 조회
   * - GET
     - /log/{id}
     - 크롤링 정보 조회
   * - DELETE
     - /log/{id}
     - 크롤링 정보 삭제
   * - DELETE
     - /all
     - 크롤링 세션 일괄 삭제 (실행 중 제외)

크롤링 정보 목록 조회
====================

요청
----------

::

    GET /api/admin/crawlinginfo/logs

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
     - 페이지당 건수 (기본값: 25. ``fess_config.properties`` 의 ``paging.page.size`` 로 변경 가능)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작, 기본값: 1)
   * - ``session_id``
     - String
     - 아니오
     - 세션 ID 필터 (부분 일치)

이 파라미터들은 JSON 요청 본문(예: ``{"size": 50, "page": 1}`` )으로 지정합니다. URL 쿼리 문자열(예: ``?size=50`` )로 지정한 값은 무시되므로, 본문에 지정하지 않으면 항상 처음 25건이 반환됩니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "session_id": "20250129100000",
            "name": "Default Crawler",
            "expired_time": "1738200000000",
            "created_time": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "session_id": "20250128100000",
            "name": "Default Crawler",
            "expired_time": "1738113600000",
            "created_time": 1738022400000
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
   * - ``id``
     - 크롤링 정보 ID
   * - ``session_id``
     - 세션 ID
   * - ``name``
     - 세션 이름
   * - ``expired_time``
     - 유효 기간 (에포크 밀리초; 문자열로 반환됨)
   * - ``created_time``
     - 작성 시각 (에포크 밀리초; 숫자로 반환됨)

.. note::

   응답의 각 로그 오브젝트에는 내부적으로 사용되는 ``crud_mode`` 필드
   (CRUD 작업 모드를 나타내는 정수값으로, 읽기 작업 시 항상 ``0``)가 포함됩니다.
   클라이언트 측에서는 무시해도 됩니다.

실행 중인 크롤링의 진행 상황 조회
=================================

실행 중인 크롤링의 진행 상황을 웹·파일 시스템·데이터 스토어 크롤링 설정마다 하나씩 반환합니다. 관리 화면의 크롤링 정보에 있는 "실행 중인 크롤링"과 같은 내용입니다( :doc:`../../admin/crawlinginfo-guide` 참조).

요청
----

::

    GET /api/admin/crawlinginfo/progress

이 엔드포인트는 파라미터를 받지 않습니다.

응답
----

.. code-block:: json

    {
      "response": {
        "status": 0,
        "progress": [
          {
            "config_id": "Wabc123",
            "name": "Example Site",
            "count": 4200,
            "last_count": 10000,
            "updated_time": 1738144800000,
            "percent": 42
          },
          {
            "config_id": "Ddef456",
            "name": "Example Database",
            "count": 1500,
            "last_count": 0,
            "updated_time": 1738144795000
          }
        ],
        "total": 2
      }
    }

응답 필드
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``progress``
     - 실행 중인 크롤링의 배열(크롤링 설정 이름순). 실행 중인 크롤링이 없으면 빈 배열
   * - ``total``
     - ``progress`` 의 요소 수

``progress`` 의 각 요소는 다음 필드를 가집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``config_id``
     - 크롤링 설정의 ID(웹은 ``W`` , 파일 시스템은 ``F`` , 데이터 스토어는 ``D`` 로 시작)
   * - ``name``
     - 크롤링 설정의 이름(설정을 찾을 수 없으면 ``config_id`` )
   * - ``count``
     - 실행 중인 크롤링이 지금까지 처리한 문서 수
   * - ``last_count``
     - 직전에 완료된 크롤링의 문서 수(알 수 없으면 ``0`` )
   * - ``updated_time``
     - ``count`` 를 기록한 시각(에포크 밀리초, 숫자)
   * - ``percent``
     - ``count`` 가 ``last_count`` 에서 차지하는 비율(%, ``0`` 에서 ``99`` 까지). 직전에 완료된 크롤링이 없으면 생략

.. note::

   완료되거나 중지된 크롤링은 포함되지 않습니다. 크롤러가 이를 기록하지 못하고 멈춘 경우(프로세스가 강제 종료된 경우 등)에는 마지막 갱신으로부터 약 30초(기본값)가 지난 크롤링도 포함되지 않습니다. 웹·파일 시스템 크롤링의 ``count`` 는 액세스 결과의 건수이고, 데이터 스토어 크롤링의 ``count`` 는 해당 크롤링 설정으로 색인 등록한 문서 수입니다.

크롤링 정보 조회
================

요청
----------

::

    GET /api/admin/crawlinginfo/log/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "crawling_info_id_1",
          "session_id": "20250129100000",
          "name": "Default Crawler",
          "expired_time": "1738200000000",
          "created_time": 1738108800000
        }
      }
    }

크롤링 정보 삭제
================

요청
----------

::

    DELETE /api/admin/crawlinginfo/log/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

크롤링 세션 일괄 삭제
==============================

현재 실행 중인 세션을 제외한 모든 크롤링 세션(및 해당 파라미터 데이터)을 삭제합니다.
경과 시간에 의한 판정은 수행하지 않으며, 실행 중이지 않은 세션은 모두 삭제됩니다.

요청
----------

::

    DELETE /api/admin/crawlinginfo/all

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

크롤링 정보 목록 조회
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"size": 50, "page": 1}'

특정 세션으로 필터링
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"session_id": "20250129100000"}'

크롤링 정보 조회
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

크롤링 정보 삭제
------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/log/crawling_info_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

세션 일괄 삭제
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/crawlinginfo/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-failureurl` - 실패 URL API
- :doc:`api-admin-joblog` - 작업 로그 API
- :doc:`../../admin/crawlinginfo-guide` - 크롤링 정보 가이드
