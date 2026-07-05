==========================
AccessToken API
==========================

개요
====

AccessToken API는 |Fess| 의 API 액세스 토큰을 관리하기 위한 API입니다.
토큰의 생성, 업데이트, 삭제 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/accesstoken

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
     - 액세스 토큰 목록 조회
   * - GET
     - /setting/{id}
     - 액세스 토큰 조회
   * - POST
     - /setting
     - 액세스 토큰 만들기
   * - PUT
     - /setting
     - 액세스 토큰 업데이트
   * - DELETE
     - /setting/{id}
     - 액세스 토큰 삭제

액세스 토큰 목록 조회
========================

요청
----------

::

    GET /api/admin/accesstoken/settings
    PUT /api/admin/accesstoken/settings

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
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "token",
            "expiredTime": 1735689600000,
            "permissions": ["admin"]
          }
        ],
        "total": 5
      }
    }

액세스 토큰 조회
====================

요청
----------

::

    GET /api/admin/accesstoken/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "token",
          "expiredTime": 1735689600000,
          "permissions": ["admin"]
        }
      }
    }

액세스 토큰 만들기
====================

요청
----------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "parameterName": "token",
      "permissions": ["user"]
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
     - 토큰 이름
   * - ``token``
     - 아니오
     - 토큰 문자열 (미지정 시 자동 생성)
   * - ``parameterName``
     - 아니오
     - 파라미터 이름 (기본값: "token")
   * - ``expiredTime``
     - 아니오
     - 유효 기한 (Unix 시간 밀리초)
   * - ``permissions``
     - 아니오
     - 허용 역할

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "token": "generated_token_string",
        "created": true
      }
    }

액세스 토큰 업데이트
====================

요청
----------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "parameterName": "token",
      "expiredTime": 1767225600000,
      "permissions": ["user", "editor"],
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

액세스 토큰 삭제
====================

요청
----------

::

    DELETE /api/admin/accesstoken/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_token_id",
        "created": false
      }
    }

사용 예
======

API 토큰 만들기
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "External App Token",
           "parameterName": "token",
           "permissions": ["guest"]
         }'

토큰을 사용한 API 호출
-----------------------------

.. code-block:: bash

    # 토큰을 파라미터로 사용
    curl "http://localhost:8080/json/?q=test&token=your_token_here"

    # 토큰을 Authorization 헤더로 사용
    curl "http://localhost:8080/json/?q=test" \
         -H "Authorization: Bearer your_token_here"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../api-search` - 검색 API
- :doc:`../../admin/accesstoken-guide` - 액세스 토큰 관리 가이드
