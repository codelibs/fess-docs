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
     - /log/{id}
     - 크롤링 정보 조회
   * - DELETE
     - /log/{id}
     - 크롤링 정보 삭제
   * - DELETE
     - /all
     - 오래된 크롤링 세션 일괄 삭제

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
     - 페이지당 건수
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호
   * - ``sessionId``
     - String
     - 아니오
     - 세션 ID 필터

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "crawling_info_id_1",
            "sessionId": "20250129100000",
            "name": "Default Crawler",
            "expiredTime": "1738200000000",
            "createdTime": 1738108800000
          },
          {
            "id": "crawling_info_id_2",
            "sessionId": "20250128100000",
            "name": "Default Crawler",
            "expiredTime": "1738113600000",
            "createdTime": 1738022400000
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
   * - ``sessionId``
     - 세션 ID
   * - ``name``
     - 세션 이름
   * - ``expiredTime``
     - 유효 기간
   * - ``createdTime``
     - 작성 시각 (에포크 밀리초)

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
          "sessionId": "20250129100000",
          "name": "Default Crawler",
          "expiredTime": "1738200000000",
          "createdTime": 1738108800000
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

오래된 크롤링 세션 일괄 삭제
==============================

실행 중인 세션을 제외한 오래된 크롤링 세션을 한꺼번에 삭제합니다.

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

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?size=50&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 세션으로 필터링
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/crawlinginfo/logs?sessionId=20250129100000" \
         -H "Authorization: Bearer YOUR_TOKEN"

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

오래된 세션 일괄 삭제
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
