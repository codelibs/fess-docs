==========================
Group API
==========================

개요
====

Group API는 |Fess| 의 그룹을 관리하기 위한 API입니다.
그룹의 생성, 업데이트, 삭제 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/group

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
     - 그룹 목록 조회
   * - GET
     - /setting/{id}
     - 그룹 조회
   * - POST
     - /setting
     - 그룹 만들기
   * - PUT
     - /setting
     - 그룹 업데이트
   * - DELETE
     - /setting/{id}
     - 그룹 삭제

그룹 목록 조회
================

요청
----------

::

    GET /api/admin/group/settings
    PUT /api/admin/group/settings

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
            "id": "group_id_1",
            "name": "Engineering",
            "gidNumber": 1000
          },
          {
            "id": "group_id_2",
            "name": "Sales",
            "gidNumber": 1001
          }
        ],
        "total": 5
      }
    }

그룹 조회
============

요청
----------

::

    GET /api/admin/group/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "group_id_1",
          "name": "Engineering",
          "gidNumber": 1000
        }
      }
    }

그룹 만들기
============

요청
----------

::

    POST /api/admin/group/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Marketing",
      "gidNumber": 1002
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
     - 그룹 이름
   * - ``gidNumber``
     - 아니오
     - 그룹 ID 번호

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_group_id",
        "created": true
      }
    }

그룹 업데이트
============

요청
----------

::

    PUT /api/admin/group/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_group_id",
      "name": "Marketing Team",
      "gidNumber": 1002,
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_group_id",
        "created": false
      }
    }

그룹 삭제
============

요청
----------

::

    DELETE /api/admin/group/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_group_id",
        "created": false
      }
    }

사용 예
======

새 그룹 만들기
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/group/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Product Team",
           "gidNumber": 2000
         }'

그룹 목록 조회
----------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/group/settings" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-user` - 사용자 관리 API
- :doc:`api-admin-role` - 역할 관리 API
- :doc:`../../admin/group-guide` - 그룹 관리 가이드
