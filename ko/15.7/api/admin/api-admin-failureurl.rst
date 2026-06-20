==========================
FailureUrl API
==========================

개요
====

FailureUrl API는 |Fess| 의 크롤링 실패 URL을 관리하기 위한 API입니다.
크롤링 중 오류가 발생한 URL의 목록 조회, 개별 조회, 삭제 등을 조작할 수 있습니다.

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
     - /logs
     - 실패 URL 목록 조회
   * - GET
     - /log/{id}
     - 실패 URL 조회
   * - DELETE
     - /log/{id}
     - 실패 URL 삭제
   * - DELETE
     - /all
     - 모든 실패 URL 삭제

실패 URL 목록 조회
===============

요청
----------

::

    GET /api/admin/failureurl/logs

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
   * - ``url``
     - String
     - 아니오
     - URL 필터 (와일드카드 ``*`` ``?`` 지원)
   * - ``errorCountMin``
     - Integer
     - 아니오
     - 오류 횟수의 하한값 (지정한 값 이상)
   * - ``errorCountMax``
     - Integer
     - 아니오
     - 오류 횟수의 상한값 (지정한 값 이하)
   * - ``errorName``
     - String
     - 아니오
     - 오류 이름 필터 (저장된 완전한정 클래스명에 대한 와일드카드 매칭; ``*`` ``?`` 지원)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "logs": [
          {
            "id": "failure_id_1",
            "url": "https://example.com/broken-page",
            "threadName": "Crawler-1",
            "errorName": "java.net.ConnectException",
            "errorLog": "Connection refused: connect",
            "errorCount": "3",
            "lastAccessTime": "1738144800000",
            "configId": "webConfig_id_1"
          },
          {
            "id": "failure_id_2",
            "url": "https://example.com/not-found",
            "threadName": "Crawler-2",
            "errorName": "org.codelibs.fess.exception.ContentNotFoundException",
            "errorLog": "Not found: https://example.com/not-found",
            "errorCount": "1",
            "lastAccessTime": "1738143000000",
            "configId": "webConfig_id_1"
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
   * - ``threadName``
     - 스레드 이름
   * - ``errorName``
     - 오류 이름 (발생한 예외의 완전한정 클래스명; 예: ``java.net.ConnectException``)
   * - ``errorLog``
     - 오류 로그 (예외 메시지 또는 스택 트레이스)
   * - ``errorCount``
     - 오류 발생 횟수 (문자열로 표현된 숫자값)
   * - ``lastAccessTime``
     - 최종 접근 시각 (문자열로 표현된 에포크 밀리초)
   * - ``configId``
     - 크롤링 설정 ID

.. note::

   모든 응답 필드는 문자열(JSON string)로 반환됩니다. ``errorCount`` 는 문자열로 표현된 숫자값이며, ``lastAccessTime`` 은 문자열로 표현된 에포크 밀리초입니다.

실패 URL 조회
===========

요청
----------

::

    GET /api/admin/failureurl/log/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "log": {
          "id": "failure_id_1",
          "url": "https://example.com/broken-page",
          "threadName": "Crawler-1",
          "errorName": "java.net.ConnectException",
          "errorLog": "Connection refused: connect",
          "errorCount": "3",
          "lastAccessTime": "1738144800000",
          "configId": "webConfig_id_1"
        }
      }
    }

실패 URL 삭제
===========

요청
----------

::

    DELETE /api/admin/failureurl/log/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

모든 실패 URL 삭제
=============

모든 실패 URL을 삭제합니다. 파라미터는 없습니다.

요청
----------

::

    DELETE /api/admin/failureurl/all

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

오류 타입
============

``errorName`` 에는 크롤링 중 발생한 예외의 완전한정 클래스명이 있는 그대로 저장됩니다. 고정된 열거형이 아니며, 발생한 예외에 따라 어떠한 클래스명도 나타날 수 있습니다. 다음은 대표적인 예시입니다.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 오류 이름 (예시)
     - 설명
   * - ``java.net.ConnectException``
     - 연결 거부 (서버에 접속할 수 없음)
   * - ``java.net.UnknownHostException``
     - 호스트명을 해석할 수 없음 (DNS 오류)
   * - ``java.net.SocketTimeoutException``
     - 연결 또는 읽기 타임아웃
   * - ``javax.net.ssl.SSLException``
     - SSL/TLS 핸드셰이크 또는 인증서 오류
   * - ``java.io.IOException``
     - 입출력 오류
   * - ``org.codelibs.fess.exception.ContentNotFoundException``
     - ``crawler.failure.url.status.codes`` 에 설정된 HTTP 상태 코드를 반환한 URL (기본값: 403, 404, 410)
   * - ``org.codelibs.fess.crawler.exception.MaxLengthExceededException``
     - 콘텐츠가 최대 길이를 초과함

사용 예
======

실패 URL 목록 조회
-----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=100&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

오류 횟수로 필터링
----------------------

.. code-block:: bash

    # 3회 이상 오류가 발생한 URL만 조회
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorCountMin=3" \
         -H "Authorization: Bearer YOUR_TOKEN"

오류 이름으로 필터링
--------------------

.. code-block:: bash

    # errorName에는 완전한정 클래스명을 저장하므로 와일드카드를 사용하여 지정합니다
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?errorName=*ConnectException" \
         -H "Authorization: Bearer YOUR_TOKEN"

실패 URL 조회
-------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

실패 URL 삭제
-------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/log/failure_id_1" \
         -H "Authorization: Bearer YOUR_TOKEN"

모든 실패 URL 삭제
---------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/failureurl/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

오류 타입별 집계
--------------------

.. code-block:: bash

    # 오류 타입별 카운트
    curl -X GET "http://localhost:8080/api/admin/failureurl/logs?size=1000" \
         -H "Authorization: Bearer YOUR_TOKEN" | \
         jq '[.response.logs[].errorName] | group_by(.) | map({error: .[0], count: length})'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`api-admin-joblog` - 작업 로그 API
- :doc:`../../admin/failureurl-guide` - 실패 URL 관리 가이드
