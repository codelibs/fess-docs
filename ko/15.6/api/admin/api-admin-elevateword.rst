==========================
ElevateWord API
==========================

개요
====

ElevateWord API는 |Fess| 의 엘리베이트 워드(특정 키워드에서의 검색 순위 조작)를 관리하기 위한 API입니다.
특정 검색 쿼리에 대해 특정 문서를 상위 또는 하위에 배치할 수 있습니다.

기본 URL
=========

::

    /api/admin/elevateword

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
     - 엘리베이트 워드 목록 조회
   * - GET
     - /setting/{id}
     - 엘리베이트 워드 조회
   * - POST
     - /setting
     - 엘리베이트 워드 만들기
   * - PUT
     - /setting
     - 엘리베이트 워드 업데이트
   * - DELETE
     - /setting/{id}
     - 엘리베이트 워드 삭제

엘리베이트 워드 목록 조회
========================

요청
----------

::

    GET /api/admin/elevateword/settings
    PUT /api/admin/elevateword/settings

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "페스",
            "permissions": [],
            "boost": 10.0,
            "targetRole": "",
            "targetLabel": ""
          }
        ],
        "total": 5
      }
    }

엘리베이트 워드 조회
====================

요청
----------

::

    GET /api/admin/elevateword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "페스",
          "permissions": [],
          "boost": 10.0,
          "targetRole": "",
          "targetLabel": ""
        }
      }
    }

엘리베이트 워드 만들기
====================

요청
----------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "도큐멘테이션",
      "permissions": ["guest"],
      "boost": 15.0,
      "targetRole": "user",
      "targetLabel": "docs"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``suggestWord``
     - 예
     - 엘리베이트 대상 키워드
   * - ``reading``
     - 아니오
     - 읽기 가나
   * - ``permissions``
     - 아니오
     - 접근 허용 역할
   * - ``boost``
     - 아니오
     - 부스트 값 (기본값: 1.0)
   * - ``targetRole``
     - 아니오
     - 대상 역할
   * - ``targetLabel``
     - 아니오
     - 대상 라벨

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

엘리베이트 워드 업데이트
====================

요청
----------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "도큐멘테이션",
      "permissions": ["guest", "user"],
      "boost": 20.0,
      "targetRole": "user",
      "targetLabel": "docs",
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

엘리베이트 워드 삭제
====================

요청
----------

::

    DELETE /api/admin/elevateword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

사용 예
======

제품명 엘리베이트
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 20.0,
           "permissions": ["guest"]
         }'

특정 라벨로의 엘리베이트
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 10.0,
           "targetLabel": "technical_docs",
           "permissions": ["guest"]
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-keymatch` - 키 매치 API
- :doc:`api-admin-boostdoc` - 문서 부스트 API
- :doc:`../../admin/elevateword-guide` - 엘리베이트 워드 관리 가이드
