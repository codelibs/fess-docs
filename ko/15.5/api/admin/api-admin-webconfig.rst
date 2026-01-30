==========================
WebConfig API
==========================

개요
====

WebConfig API는 |Fess| 의 Web 크롤링 설정을 관리하기 위한 API입니다.
크롤링 대상 URL, 크롤링 깊이, 제외 패턴 등의 설정을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/webconfig

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
     - Web 크롤링 설정 목록 조회
   * - GET
     - /setting/{id}
     - Web 크롤링 설정 조회
   * - POST
     - /setting
     - Web 크롤링 설정 만들기
   * - PUT
     - /setting
     - Web 크롤링 설정 업데이트
   * - DELETE
     - /setting/{id}
     - Web 크롤링 설정 삭제

Web 크롤링 설정 목록 조회
======================

요청
----------

::

    GET /api/admin/webconfig/settings
    PUT /api/admin/webconfig/settings

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
            "id": "webconfig_id_1",
            "name": "Example Site",
            "urls": "https://example.com/",
            "includedUrls": ".*example\\.com.*",
            "excludedUrls": ".*\\.(pdf|zip)$",
            "includedDocUrls": "",
            "excludedDocUrls": "",
            "configParameter": "",
            "depth": 3,
            "maxAccessCount": 1000,
            "userAgent": "",
            "numOfThread": 1,
            "intervalTime": 1000,
            "boost": 1.0,
            "available": true,
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

Web 크롤링 설정 조회
==================

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
          "urls": "https://example.com/",
          "includedUrls": ".*example\\.com.*",
          "excludedUrls": ".*\\.(pdf|zip)$",
          "includedDocUrls": "",
          "excludedDocUrls": "",
          "configParameter": "",
          "depth": 3,
          "maxAccessCount": 1000,
          "userAgent": "",
          "numOfThread": 1,
          "intervalTime": 1000,
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
        }
      }
    }

Web 크롤링 설정 만들기
==================

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
      "depth": 5,
      "maxAccessCount": 5000,
      "numOfThread": 3,
      "intervalTime": 500,
      "boost": 1.0,
      "available": true,
      "permissions": ["admin", "user"],
      "labelTypeIds": ["label_id_1"]
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
     - 설정 이름
   * - ``urls``
     - 예
     - 크롤링 시작 URL (여러 개인 경우 줄바꿈으로 구분)
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
     - 추가 설정 파라미터
   * - ``depth``
     - 아니오
     - 크롤링 깊이 (기본값: -1=무제한)
   * - ``maxAccessCount``
     - 아니오
     - 최대 접근 수 (기본값: 100)
   * - ``userAgent``
     - 아니오
     - 사용자 정의 User-Agent
   * - ``numOfThread``
     - 아니오
     - 병렬 스레드 수 (기본값: 1)
   * - ``intervalTime``
     - 아니오
     - 요청 간격 (밀리초, 기본값: 0)
   * - ``boost``
     - 아니오
     - 검색 결과 부스트 값 (기본값: 1.0)
   * - ``available``
     - 아니오
     - 활성화/비활성화 (기본값: true)
   * - ``sortOrder``
     - 아니오
     - 표시 순서
   * - ``permissions``
     - 아니오
     - 접근 허용 역할
   * - ``virtualHosts``
     - 아니오
     - 가상 호스트
   * - ``labelTypeIds``
     - 아니오
     - 라벨 타입 ID

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

Web 크롤링 설정 업데이트
==================

요청
----------

::

    PUT /api/admin/webconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_webconfig_id",
      "name": "Updated Corporate Site",
      "urls": "https://www.example.com/",
      "includedUrls": ".*www\\.example\\.com.*",
      "excludedUrls": ".*\\.(pdf|zip|exe|dmg)$",
      "depth": 10,
      "maxAccessCount": 10000,
      "numOfThread": 5,
      "intervalTime": 300,
      "boost": 1.2,
      "available": true,
      "versionNo": 1
    }

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

Web 크롤링 설정 삭제
==================

요청
----------

::

    DELETE /api/admin/webconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_webconfig_id",
        "created": false
      }
    }

URL 패턴 예시
===============

includedUrls / excludedUrls
---------------------------

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
======

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
           "depth": 5,
           "maxAccessCount": 10000,
           "numOfThread": 3,
           "intervalTime": 500,
           "available": true,
           "permissions": ["guest"]
         }'

문서 사이트 크롤링 설정
--------------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/webconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Documentation Site",
           "urls": "https://docs.example.com/",
           "includedUrls": ".*docs\\.example\\.com.*",
           "excludedUrls": "",
           "includedDocUrls": ".*\\.(html|htm)$",
           "depth": -1,
           "maxAccessCount": 50000,
           "numOfThread": 5,
           "intervalTime": 200,
           "boost": 1.5,
           "available": true,
           "labelTypeIds": ["documentation_label_id"]
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-fileconfig` - 파일 크롤링 설정 API
- :doc:`api-admin-dataconfig` - 데이터스토어 설정 API
- :doc:`../../admin/webconfig-guide` - Web 크롤링 설정 가이드
