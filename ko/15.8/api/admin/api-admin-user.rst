==========================
User API
==========================

개요
====

User API는 |Fess| 의 사용자 계정을 관리하기 위한 REST API입니다.
사용자의 생성, 조회, 업데이트, 삭제, 역할 및 그룹 할당을 조작할 수 있습니다.

이 API는 관리용 API이며, 이용하려면 관리용 액세스 토큰으로 인증해야 합니다.
인증 방법 및 공통 사양에 대해서는 :doc:`api-admin-overview` 를 참조하십시오.

모든 응답은 ``response`` 객체로 래핑되며, 다음 공통 필드를 포함합니다.

- ``version`` : |Fess| 제품 버전 문자열.
- ``status`` : 처리 결과 상태 코드 (``0`` =성공, ``1`` =잘못된 요청, ``2`` =시스템 오류, ``3`` =인증 오류, ``9`` =실패).

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
   * - GET
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
=================

요청
----

::

    GET /api/admin/user/settings

파라미터
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 15 10 10 65

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``size``
     - Integer
     - 아니오
     - 페이지당 건수. 기본값은 설정값 ``paging.page.size`` (기본: 25).
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작). 기본값은 1.

.. note::

   현재 구현에서 사용자 목록 엔드포인트는 ``size`` 및 ``page`` 파라미터를 적용하지 않습니다.
   항상 1페이지를, 서버 설정 ``paging.page.size`` (기본: 25)의 건수로, 사용자명(``name``) 오름차순으로 반환합니다.
   일치하는 사용자의 총 건수는 ``response.total`` 에서 확인할 수 있습니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "YWRtaW4=",
            "name": "admin",
            "attributes": {
              "surname": "Administrator",
              "givenName": "System",
              "mail": "admin@example.com"
            },
            "roles": ["admin"],
            "groups": [],
            "versionNo": 1
          }
        ],
        "total": 10
      }
    }

- ``settings`` : 현재 페이지의 사용자 배열.
- ``total`` : 조건에 일치하는 사용자의 총 건수.

사용자 조회
===========

요청
----

::

    GET /api/admin/user/setting/{id}

``{id}`` 에는 대상 사용자의 문서 ID를 지정합니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "YWRtaW4=",
          "name": "admin",
          "attributes": {
            "surname": "Administrator",
            "givenName": "System",
            "mail": "admin@example.com",
            "telephoneNumber": "",
            "uidNumber": "",
            "gidNumber": "",
            "homeDirectory": ""
          },
          "roles": ["admin"],
          "groups": [],
          "versionNo": 1
        }
      }
    }

.. note::

   ``attributes`` 에는 ``name``, ``password``, ``roles``, ``groups`` 를 제외하고 사용자에게 저장된 모든 속성이 포함됩니다.
   ``password`` 는 응답에 포함되지 않습니다.

사용자 만들기
=============

요청
----

::

    POST /api/admin/user/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "name": "testuser",
      "password": "securepassword",
      "confirmPassword": "securepassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User",
        "mail": "testuser@example.com"
      },
      "roles": ["user"],
      "groups": ["group_id_1"]
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 필드
     - 필수
     - 설명
   * - ``name``
     - 예
     - 사용자명 (로그인 ID)
   * - ``password``
     - 아니오
     - 비밀번호
   * - ``confirmPassword``
     - 아니오
     - 확인용 비밀번호
   * - ``attributes``
     - 아니오
     - 속성 맵 (아래 참조)
   * - ``roles``
     - 아니오
     - 역할 ID 배열
   * - ``groups``
     - 아니오
     - 그룹 ID 배열

.. note::

   REST API에서는 비밀번호 필수 확인, ``password`` 와 ``confirmPassword`` 의 일치 확인,
   비밀번호 정책 검증을 수행하지 않습니다 (이것들은 관리 UI에서만 적용됩니다).
   실제 운용 시, ``password`` 의 값이 ``confirmPassword`` 와 일치하는 유효한 값을 지정하는 것을 권장합니다.

``attributes`` 의 키에는 사용자 엔티티의 속성명 (LDAP 스키마에서 유래한 항목명)을 지정합니다.
대표적인 키는 다음과 같습니다.

- ``surname``, ``givenName``, ``displayName``, ``mail``
- ``telephoneNumber``, ``mobile``, ``homePhone``
- ``employeeNumber``, ``title``, ``description``, ``homeDirectory``
- ``uidNumber``, ``gidNumber``

``uidNumber`` 와 ``gidNumber`` 는 숫자여야 합니다 (업데이트 시 타입이 검증됩니다).
그 외에도 많은 LDAP 속성 키를 지정할 수 있습니다.

.. note::

   사용자 만들기 시, 사용자의 ID(문서 ID)는 사용자명을 Base64 URL 인코딩한 값으로 자동 생성됩니다
   (예: 사용자명 ``admin`` 의 경우 ``YWRtaW4=`` ).

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_user_id",
        "created": true
      }
    }

- ``id`` : 생성된 사용자의 문서 ID.
- ``created`` : 생성된 경우 ``true``.

사용자 업데이트
===============

요청
----

::

    PUT /api/admin/user/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_user_id",
      "name": "testuser",
      "password": "newpassword",
      "confirmPassword": "newpassword",
      "attributes": {
        "surname": "Test",
        "givenName": "User Updated",
        "mail": "testuser.updated@example.com"
      },
      "roles": ["user", "editor"],
      "groups": ["group_id_1", "group_id_2"],
      "versionNo": 1
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 필드
     - 필수
     - 설명
   * - ``id``
     - 예
     - 업데이트 대상 사용자의 문서 ID.
   * - ``name``
     - 예
     - 사용자명 (로그인 ID)
   * - ``versionNo``
     - 예
     - 버전 번호 (낙관적 잠금용)
   * - ``password``
     - 아니오
     - 새 비밀번호 (지정한 경우에만 업데이트)
   * - ``confirmPassword``
     - 아니오
     - 확인용 비밀번호
   * - ``attributes``
     - 아니오
     - 속성 맵 ("사용자 만들기" 참조)
   * - ``roles``
     - 아니오
     - 역할 ID 배열
   * - ``groups``
     - 아니오
     - 그룹 ID 배열

.. note::

   업데이트 시 ``id``, ``name``, ``versionNo`` 는 필수입니다.
   ``versionNo`` 는 대상 사용자 조회(GET) 시 반환되는 값이며, OpenSearch 문서의 버전에 대응합니다.
   현재 버전과 일치하지 않으면 충돌로 판단되어 업데이트가 거부됩니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_user_id",
        "created": false
      }
    }

- ``created`` : 업데이트의 경우 ``false``.

사용자 삭제
===========

요청
----

::

    DELETE /api/admin/user/setting/{id}

``{id}`` 에는 삭제 대상 사용자의 문서 ID를 지정합니다.

.. note::

   현재 로그인 중인 사용자 자신은 삭제할 수 없습니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "deleted_user_id",
        "created": false
      }
    }

- ``id`` : 삭제된 사용자의 문서 ID.

사용 예
=======

새 사용자 만들기
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/user/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "john.doe",
           "password": "SecureP@ss123",
           "confirmPassword": "SecureP@ss123",
           "attributes": {
             "surname": "Doe",
             "givenName": "John",
             "mail": "john.doe@example.com"
           },
           "roles": ["user"],
           "groups": []
         }'

사용자 역할 변경
----------------

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
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-role` - 역할 관리 API
- :doc:`api-admin-group` - 그룹 관리 API
- :doc:`../../admin/user-guide` - 사용자 관리 가이드
