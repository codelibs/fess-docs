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
   * - GET/PUT
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
    PUT /api/admin/dataconfig/settings

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
            "id": "dataconfig_id_1",
            "name": "Database Crawler",
            "handlerName": "DatabaseDataStore",
            "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb",
            "handlerScript": "...",
            "boost": 1.0,
            "available": true,
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
          "handlerName": "DatabaseDataStore",
          "handlerParameter": "driver=org.postgresql.Driver\nurl=jdbc:postgresql://localhost/mydb\nusername=dbuser\npassword=dbpass",
          "handlerScript": "...",
          "boost": 1.0,
          "available": true,
          "sortOrder": 0,
          "permissions": ["admin"],
          "virtualHosts": [],
          "labelTypeIds": []
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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description",
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
   * - ``handlerName``
     - 예
     - 데이터스토어 핸들러 이름
   * - ``handlerParameter``
     - 아니오
     - 핸들러 파라미터 (연결 정보 등)
   * - ``handlerScript``
     - 예
     - 데이터 변환 스크립트
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
      "handlerScript": "url=\"https://example.com/product/\" + data.product_id\ntitle=data.product_name\ncontent=data.description + \" \" + data.features",
      "boost": 1.5,
      "available": true,
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_dataconfig_id",
        "created": false
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
     - CSV 파일에서 데이터 읽기
   * - ``JsonDataStore``
     - JSON 파일 또는 JSON API에서 데이터 읽기

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
           "handlerScript": "url=\"https://example.com/user/\" + data.user_id\ntitle=data.username\ncontent=data.profile",
           "boost": 1.0,
           "available": true
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-webconfig` - Web 크롤링 설정 API
- :doc:`api-admin-fileconfig` - 파일 크롤링 설정 API
- :doc:`../../admin/dataconfig-guide` - 데이터스토어 설정 가이드
