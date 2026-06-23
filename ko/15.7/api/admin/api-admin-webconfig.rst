==========================
WebConfig API
==========================

개요
====

WebConfig API는 |Fess| 의 웹 크롤링 설정을 관리하기 위한 API입니다.
크롤링 대상 URL, 크롤링 깊이, 제외 패턴 등의 설정을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/webconfig

.. note::

   모든 엔드포인트에는 관리자 권한과 유효한 액세스 토큰이 필요합니다.
   인증 방법에 대해서는 :doc:`api-admin-overview` 를 참조하십시오.

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
     - 웹 크롤링 설정 목록 조회
   * - GET
     - /setting/{id}
     - 웹 크롤링 설정 조회
   * - POST
     - /setting
     - 웹 크롤링 설정 생성
   * - PUT
     - /setting
     - 웹 크롤링 설정 업데이트
   * - DELETE
     - /setting/{id}
     - 웹 크롤링 설정 삭제

웹 크롤링 설정 목록 조회
==========================

요청
----------

::

    GET /api/admin/webconfig/settings

.. note::

   목록 조회 엔드포인트는 ``GET`` 외에 ``PUT`` 으로도 접근할 수 있습니다.

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 10 55

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작, 기본값: 1)
   * - ``size``
     - Integer
     - 아니오
     - 페이지당 건수 (기본값: 25. ``paging.page.size`` 설정에 따릅니다)
   * - ``name``
     - String
     - 아니오
     - 설정 이름으로 필터링
   * - ``urls``
     - String
     - 아니오
     - 크롤링 URL로 필터링
   * - ``description``
     - String
     - 아니오
     - 설명으로 필터링

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "webconfig_id_1",
            "name": "Example Site",
            "description": "샘플 사이트",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "Mozilla/5.0",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": "true",
            "permissions": "{role}admin",
            "virtualHosts": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

``total`` 은 조건에 일치하는 설정의 총 건수를 나타냅니다.

웹 크롤링 설정 조회
====================

요청
----------

::

    GET /api/admin/webconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "webconfig_id_1",
          "name": "Example Site",
          "description": "샘플 사이트",
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "Mozilla/5.0",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": "",
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   응답에는 등록 및 업데이트 시 자동으로 설정되는 ``createdBy``, ``createdTime``,
   ``updatedBy``, ``updatedTime``, ``versionNo`` 가 포함됩니다.
   ``versionNo`` 는 업데이트 시 필요합니다 (아래의 「웹 크롤링 설정 업데이트」를 참조).

웹 크롤링 설정 생성
====================

요청
----------

::

    POST /api/admin/webconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe)$",
      "userAgent": "Mozilla/5.0",
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 필드
     - 필수
     - 설명
   * - ``name``
     - 예
     - 설정 이름 (최대 200자)
   * - ``description``
     - 아니오
     - 설정 설명 (최대 1000자)
   * - ``urls``
     - 예
     - 크롤링 시작 URL (여러 개인 경우 줄바꿈으로 구분). ``http:`` 또는 ``https:`` 로 지정합니다
   * - ``includedUrls``
     - 아니오
     - 크롤링 대상 URL의 정규 표현식 패턴
   * - ``excludedUrls``
     - 아니오
     - 크롤링 제외 URL의 정규 표현식 패턴
   * - ``includedDocUrls``
     - 아니오
     - 인덱스 대상 URL의 정규 표현식 패턴
   * - ``excludedDocUrls``
     - 아니오
     - 인덱스 제외 URL의 정규 표현식 패턴
   * - ``configParameter``
     - 아니오
     - 추가 설정 파라미터 (``key=value`` 형식, 한 줄에 한 항목)
   * - ``depth``
     - 아니오
     - 크롤링 깊이 (0 이상)
   * - ``maxAccessCount``
     - 아니오
     - 최대 접근 수 (0 이상)
   * - ``userAgent``
     - 예
     - User-Agent 문자열 (최대 200자)
   * - ``numOfThread``
     - 예
     - 병렬 스레드 수 (1 이상)
   * - ``intervalTime``
     - 예
     - 접근 간격 (밀리초, 0 이상)
   * - ``boost``
     - 예
     - 검색 결과 부스트 값
   * - ``available``
     - 예
     - 활성화/비활성화 (문자열 ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - 예
     - 표시 순서 (0 이상)
   * - ``permissions``
     - 아니오
     - 접근 허용 역할 (여러 개인 경우 줄바꿈으로 구분)
   * - ``virtualHosts``
     - 아니오
     - 가상 호스트 (여러 개인 경우 줄바꿈으로 구분)

.. note::

   ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` 등의 감사용 필드는
   서버 측에서 자동으로 설정되므로 요청 본문에 지정할 필요가 없습니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_webconfig_id",
        "created": true
      }
    }

웹 크롤링 설정 업데이트
========================

요청
----------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

업데이트 시에는 생성 시의 필드에 더하여, 업데이트 대상을 식별하는 ``id`` 와 버전 번호 ``versionNo`` 가 필수입니다.
``versionNo`` 에는 조회 API (GET)의 응답에 포함된 현재 값을 지정합니다.

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "userAgent": "Mozilla/5.0",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

업데이트 시 추가 필드
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 필드
     - 필수
     - 설명
   * - ``id``
     - 예
     - 업데이트 대상의 설정 ID (최대 1000자)
   * - ``versionNo``
     - 예
     - 업데이트 대상의 현재 버전 번호. 조회 API (GET)의 응답에 포함된 ``versionNo`` 를 지정합니다

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_webconfig_id",
        "created": false
      }
    }

웹 크롤링 설정 삭제
====================

요청
----------

::

    DELETE /api/admin/webconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

URL 패턴 예시
===============

``includedUrls`` / ``excludedUrls`` / ``includedDocUrls`` / ``excludedDocUrls`` 에는 정규 표현식을 지정합니다.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 패턴
     - 설명
   * - ``.*example\\.com.*``
     - example.com을 포함하는 모든 URL
   * - ``https://example\\.com/docs/.*``
     - /docs/ 하위만
   * - ``.*\\.(pdf|doc|docx)$``
     - PDF, DOC, DOCX 파일
   * - ``.*\\?.*``
     - 쿼리 파라미터가 있는 URL
   * - ``.*/(login|logout|admin)/.*``
     - 특정 경로를 포함하는 URL

사용 예
==========

기업 사이트 크롤링 설정
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Corporate Website",
           "urls": "https://www.example.com/",
           "includedUrls": ".*www\\.example\\.com.*",
           "excludedUrls": ".*/(login|admin|api)/.*",
           "userAgent": "Mozilla/5.0",
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

문서 사이트 크롤링 설정
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "includedDocUrls": ".*\\.(html|htm)$",
           "userAgent": "Mozilla/5.0",
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": "true",
           "sortOrder": 0
         }'

참고 정보
============

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-fileconfig` - 파일 크롤링 설정 API
- :doc:`api-admin-dataconfig` - 데이터스토어 설정 API
- :doc:`../../admin/webconfig-guide` - 웹 크롤링 설정 가이드
