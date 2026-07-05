==========================
User API
==========================

개요
====

User API는 |Fess| 의 사용자 계정을 관리하기 위한 API입니다.
사용자의 생성, 업데이트, 삭제, 권한 설정 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/user

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
     - 사용자 목록 조회
   * - GET
     - /setting/{id}
     - 사용자 조회
   * - POST
     - /setting
     - 사용자 만들기
   * - PUT
     - /setting
     - 사용자 업데이트
   * - DELETE
     - /setting/{id}
     - 사용자 삭제

사용자 목록 조회
================

요청
----------

::

    GET /api/admin/user/settings
    PUT /api/admin/user/settings

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
            "id": "user_id_1",
            "name": "admin",
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "roles": ["admin"],
            "groups": []
          }
        ],
        "total": 10
      }
    }

사용자 조회
============

요청
----------

::

    GET /api/admin/user/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "user_id_1",
          "name": "admin",
          "surname": "Administrator",
          "givenName": "System",
          "mail": "admin@example.com",
          "telephoneNumber": "",
          "homePhone": "",
          "homePostalAddress": "",
          "labeledUri": "",
          "roomNumber": "",
          "description": "",
          "title": "",
          "pager": "",
          "street": "",
          "postalCode": "",
          "physicalDeliveryOfficeName": "",
          "destinationIndicator": "",
          "internationaliSDNNumber": "",
          "state": "",
          "employeeNumber": "",
          "facsimileTelephoneNumber": "",
          "postOfficeBox": "",
          "initials": "",
          "carLicense": "",
          "mobile": "",
          "postalAddress": "",
          "city": "",
          "teletexTerminalIdentifier": "",
          "x121Address": "",
          "businessCategory": "",
          "registeredAddress": "",
          "displayName": "",
          "preferredLanguage": "",
          "departmentNumber": "",
          "uidNumber": "",
          "gidNumber": "",
          "homeDirectory": "",
          "roles": ["admin"],
          "groups": []
        }
      }
    }

사용자 만들기
============

요청
----------

::

    POST /api/admin/user/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "surname": "Test",
      "givenName": "User",
      "mail": "testuser@example.com",
      "roles": ["user"],
      "groups": ["group_id_1"]
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
     - 사용자명 (로그인 ID)
   * - ``password``
     - 예
     - 비밀번호
   * - ``surname``
     - 아니오
     - 성
   * - ``givenName``
     - 아니오
     - 이름
   * - ``mail``
     - 아니오
     - 이메일 주소
   * - ``telephoneNumber``
     - 아니오
     - 전화번호
   * - ``roles``
     - 아니오
     - 역할 ID 배열
   * - ``groups``
     - 아니오
     - 그룹 ID 배열

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

사용자 업데이트
============

요청
----------

::

    PUT /api/admin/user/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "surname": "Test",
      "givenName": "User Updated",
      "mail": "testuser.updated@example.com",
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

사용자 삭제
============

요청
----------

::

    DELETE /api/admin/user/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

사용 예
======

새 사용자 만들기
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "surname": "Doe",
           "givenName": "John",
           "mail": "john.doe@example.com",
           "roles": ["user"],
           "groups": []
         }'

사용자 역할 변경
--------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "id": "user_id_123",
           "name": "john.doe",
           "roles": ["user", "editor", "admin"],
           "versionNo": 1
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-role` - 역할 관리 API
- :doc:`api-admin-group` - 그룹 관리 API
- :doc:`../../admin/user-guide` - 사용자 관리 가이드
