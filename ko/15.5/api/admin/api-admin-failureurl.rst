==========================
FailureUrl API
==========================

개요
====

FailureUrl API는 |Fess| 의 크롤링 실패 URL을 관리하기 위한 API입니다.
크롤링 중 오류가 발생한 URL의 확인, 삭제 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/failureurl

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
     - 실패 URL 목록 조회
   * - DELETE
     - /{id}
     - 실패 URL 삭제
   * - DELETE
     - /delete-all
     - 모든 실패 URL 삭제

실패 URL 목록 조회
===============

요청
----------

::

    GET /api/admin/failureurl

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
   * - ``errorCountMin``
     - Integer
     - 아니오
     - 최소 오류 횟수 필터
   * - ``configId``
     - String
     - 아니오
     - 설정 ID 필터

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "failures": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "configId": "webconfig_id_1",
            "errorName": "ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": 3,
            "lastAccessTime": "2025-01-29T10:00:00Z",
            "threadName": "Crawler-1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "configId": "webconfig_id_1",
            "errorName": "HttpStatusException",
            "errorLog": "404 Not Found",
            "errorCount": 1,
            "lastAccessTime": "2025-01-29T09:30:00Z",
            "threadName": "Crawler-2"
          }
        ],
        "total": 45
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
     - 실패 URL ID
   * - ``url``
     - 실패한 URL
   * - ``configId``
     - 크롤링 설정 ID
   * - ``errorName``
     - 오류 이름
   * - ``errorLog``
     - 오류 로그
   * - ``errorCount``
     - 오류 발생 횟수
   * - ``lastAccessTime``
     - 최종 접근 시각
   * - ``threadName``
     - 스레드 이름

실패 URL 삭제
===========

요청
----------

::

    DELETE /api/admin/failureurl/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Failure URL deleted successfully"
      }
    }

모든 실패 URL 삭제
=============

요청
----------

::

    DELETE /api/admin/failureurl/delete-all

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``configId``
     - String
     - 아니오
     - 특정 설정 ID의 실패 URL만 삭제
   * - ``errorCountMin``
     - Integer
     - 아니오
     - 지정 횟수 이상의 오류만 삭제

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "All failure URLs deleted successfully",
        "deletedCount": 45
      }
    }

오류 타입
============

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 오류 이름
     - 설명
   * - ``ConnectException``
     - 연결 오류
   * - ``HttpStatusException``
     - HTTP 상태 오류 (404, 500 등)
   * - ``SocketTimeoutException``
     - 타임아웃 오류
   * - ``UnknownHostException``
     - 호스트명 해석 오류
   * - ``SSLException``
     - SSL 인증서 오류
   * - ``IOException``
     - 입출력 오류

사용 예
======

실패 URL 목록 조회
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?size=100&page=0" \
         -H "Authorization: Bearer YOUR_TOKEN"

오류 횟수로 필터링
----------------------

.. code-block:: bash

    # 3회 이상 오류가 발생한 URL만 조회
    curl -X GET "http://localhost:8080/api/admin/failureurl?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 설정의 실패 URL 조회
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

실패 URL 삭제
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

모든 실패 URL 삭제
---------------

.. code-block:: bash

    # 모든 실패 URL 삭제
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 특정 설정의 실패 URL만 삭제
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?configId=webconfig_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 3회 이상 오류가 발생한 URL만 삭제
    curl -X DELETE "http://localhost:8080/api/admin/failureurl/delete-all?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

오류 타입별 집계
--------------------

.. code-block:: bash

    # 오류 타입별 카운트
    curl -X GET "http://localhost:8080/api/admin/failureurl?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.failures[].errorName] | group_by(.) | map({error: .[0], count: length})'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`api-admin-joblog` - 작업 로그 API
- :doc:`../../admin/failureurl-guide` - 실패 URL 관리 가이드
