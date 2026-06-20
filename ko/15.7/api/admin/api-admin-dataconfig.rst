==========================
DataConfig API
==========================

개요
====

DataConfig API는 |Fess| 의 데이터스토어 설정을 관리하기 위한 API입니다.
데이터베이스, CSV, JSON 등의 데이터 소스 크롤링 설정을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/dataconfig

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
     - 데이터스토어 설정 목록 조회
   * - GET
     - /setting/{id}
     - 데이터스토어 설정 조회
   * - POST
     - /setting
     - 데이터스토어 설정 만들기
   * - PUT
     - /setting
     - 데이터스토어 설정 업데이트
   * - DELETE
     - /setting/{id}
     - 데이터스토어 설정 삭제

데이터스토어 설정 목록 조회
========================

요청
----------

::

    GET /api/admin/dataconfig/settings

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
     - 페이지당 건수 (기본값: 25)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작, 기본값: 1)
   * - ``name``
     - String
     - 아니오
     - 설정 이름으로 필터링
   * - ``handlerName``
     - String
     - 아니오
     - 핸들러 이름으로 필터링
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
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "description": "데이터베이스 크롤러",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
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

데이터스토어 설정 조회
====================

요청
----------

::

    GET /api/admin/dataconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "dataconfig_id_1",
          "name": "Database Crawler",
          "description": "데이터베이스 크롤러",
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": "true",
          "sortOrder": 0,
          "permissions": "{role}admin",
          "virtualHosts": ""
        }
      }
    }

데이터스토어 설정 만들기
====================

요청
----------

::

    POST /api/admin/dataconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=pass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description",
      "boost": 1.0,
      "available": "true",
      "sortOrder": 0,
      "permissions": "{role}admin\n{role}user"
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
   * - ``description``
     - 아니오
     - 설정 설명
   * - ``handlerName``
     - 예
     - 데이터스토어 핸들러 이름
   * - ``handlerParameter``
     - 아니오
     - 핸들러 파라미터 (연결 정보 등)
   * - ``handlerScript``
     - 아니오
     - 데이터 변환 스크립트
   * - ``boost``
     - 예
     - 검색 결과 부스트 값
   * - ``available``
     - 예
     - 활성화/비활성화 (문자열 ``"true"`` / ``"false"``)
   * - ``sortOrder``
     - 예
     - 표시 순서
   * - ``permissions``
     - 아니오
     - 접근 허용 역할 (여러 개인 경우 줄바꿈으로 구분)
   * - ``virtualHosts``
     - 아니오
     - 가상 호스트 (여러 개인 경우 줄바꿈으로 구분)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_dataconfig_id",
        "created": true
      }
    }

데이터스토어 설정 업데이트
====================

요청
----------

::

    PUT /api/admin/dataconfig/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_dataconfig_id",
      "name": "Updated Product Database",
      "handlerName": "DatabaseDataStore",
      "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/products\nusername=user\npassword=newpass",
      "handlerScript": "url=\"https://example.com/product/\" + product_id\ntitle=product_name\ncontent=description + \" \" + features",
      "boost": 1.5,
      "available": "true",
      "sortOrder": 0,
      "versionNo": 1
    }

업데이트 요청에는 생성 시와 동일한 필수 필드(``name``, ``handlerName``, ``boost``, ``available``, ``sortOrder``)에 더해 다음 필드가 필수입니다.

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``id``
     - 예
     - 업데이트할 설정 ID
   * - ``versionNo``
     - 예
     - 낙관적 잠금을 위한 버전 번호(조회 시 얻은 값을 지정)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_dataconfig_id",
        "created": false
      }
    }

데이터스토어 설정 삭제
====================

요청
----------

::

    DELETE /api/admin/dataconfig/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

핸들러 타입
================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 핸들러 이름
     - 설명
   * - ``DatabaseDataStore``
     - JDBC를 통해 데이터베이스에 연결
   * - ``CsvDataStore``
     - CSV 파일에서 데이터를 읽어 들임 (각 행을 하나의 문서로 처리)
   * - ``CsvListDataStore``
     - CSV 파일을 읽어 들이고 처리된 파일을 자동 삭제 (타임스탬프 기반 필터링을 지원하는 ``CsvDataStore`` 의 확장)
   * - ``JsonDataStore``
     - JSON 파일 또는 JSON API에서 데이터 읽기

.. note::

   이용 가능한 핸들러 타입은 설치된 데이터스토어 플러그인에 따라 다릅니다.
   위 목록은 기본으로 포함된 핸들러입니다. SharePoint, Slack, Salesforce 등의 데이터스토어
   플러그인을 추가로 설치하면 각각에 해당하는 핸들러 이름을 사용할 수 있게 됩니다.

사용 예
======

데이터베이스 크롤링 설정
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dataconfig/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "User Database",
           "handlerName": "DatabaseDataStore",
           "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/userdb\nusername=dbuser\npassword=dbpass\nsql=SELECT * FROM users WHERE active=true",
           "handlerScript": "url=\"https://example.com/user/\" + user_id\ntitle=username\ncontent=profile",
           "boost": 1.0,
           "available": "true",
           "sortOrder": 0
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-webconfig` - Web 크롤링 설정 API
- :doc:`api-admin-fileconfig` - 파일 크롤링 설정 API
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
