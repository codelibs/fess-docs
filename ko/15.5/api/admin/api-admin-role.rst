==========================
Role API
==========================

개요
====

Role API는 |Fess| 의 역할을 관리하기 위한 API입니다.
역할의 생성, 업데이트, 삭제 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/role

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
     - 역할 목록 조회
   * - GET
     - /setting/{id}
     - 역할 조회
   * - POST
     - /setting
     - 역할 만들기
   * - PUT
     - /setting
     - 역할 업데이트
   * - DELETE
     - /setting/{id}
     - 역할 삭제

역할 목록 조회
==============

요청
----------

::

    GET /api/admin/role/settings
    PUT /api/admin/role/settings

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
            "id": "role_id_1",
            "name": "admin"
          },
          {
            "id": "role_id_2",
            "name": "user"
          }
        ],
        "total": 5
      }
    }

역할 조회
==========

요청
----------

::

    GET /api/admin/role/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "role_id_1",
          "name": "admin"
        }
      }
    }

역할 만들기
==========

요청
----------

::

    POST /api/admin/role/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "editor"
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
     - 역할 이름

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_role_id",
        "created": true
      }
    }

역할 업데이트
==========

요청
----------

::

    PUT /api/admin/role/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_role_id",
      "name": "editor_updated",
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_role_id",
        "created": false
      }
    }

역할 삭제
==========

요청
----------

::

    DELETE /api/admin/role/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_role_id",
        "created": false
      }
    }

사용 예
======

새 역할 만들기
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/role/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "content_manager"
         }'

역할 목록 조회
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/role/settings?size=50" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-user` - 사용자 관리 API
- :doc:`api-admin-group` - 그룹 관리 API
- :doc:`../../admin/role-guide` - 역할 관리 가이드
