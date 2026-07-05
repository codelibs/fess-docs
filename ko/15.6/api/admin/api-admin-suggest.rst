==========================
Suggest API
==========================

개요
====

Suggest API는 |Fess| 의 서제스트 기능을 관리하기 위한 API입니다.
서제스트 워드의 추가, 삭제, 업데이트 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/suggest

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
     - 서제스트 워드 목록 조회
   * - GET
     - /setting/{id}
     - 서제스트 워드 조회
   * - POST
     - /setting
     - 서제스트 워드 만들기
   * - PUT
     - /setting
     - 서제스트 워드 업데이트
   * - DELETE
     - /setting/{id}
     - 서제스트 워드 삭제
   * - DELETE
     - /delete-all
     - 전체 서제스트 워드 삭제

서제스트 워드 목록 조회
========================

요청
----------

::

    GET /api/admin/suggest/settings
    PUT /api/admin/suggest/settings

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
            "id": "suggest_id_1",
            "text": "fess",
            "reading": "페스",
            "fields": ["title", "content"],
            "tags": ["product"],
            "roles": ["guest"],
            "lang": "ja",
            "score": 1.0
          }
        ],
        "total": 100
      }
    }

서제스트 워드 조회
====================

요청
----------

::

    GET /api/admin/suggest/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "suggest_id_1",
          "text": "fess",
          "reading": "페스",
          "fields": ["title", "content"],
          "tags": ["product"],
          "roles": ["guest"],
          "lang": "ja",
          "score": 1.0
        }
      }
    }

서제스트 워드 만들기
====================

요청
----------

::

    POST /api/admin/suggest/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "text": "search engine",
      "reading": "서치엔진",
      "fields": ["title"],
      "tags": ["feature"],
      "roles": ["guest"],
      "lang": "en",
      "score": 1.0
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``text``
     - 예
     - 서제스트 텍스트
   * - ``reading``
     - 아니오
     - 읽기 가나
   * - ``fields``
     - 아니오
     - 대상 필드
   * - ``tags``
     - 아니오
     - 태그
   * - ``roles``
     - 아니오
     - 접근 허용 역할
   * - ``lang``
     - 아니오
     - 언어 코드
   * - ``score``
     - 아니오
     - 스코어 (기본값: 1.0)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_suggest_id",
        "created": true
      }
    }

서제스트 워드 업데이트
====================

요청
----------

::

    PUT /api/admin/suggest/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_suggest_id",
      "text": "search engine",
      "reading": "서치엔진",
      "fields": ["title", "content"],
      "tags": ["feature", "popular"],
      "roles": ["guest"],
      "lang": "en",
      "score": 2.0,
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_suggest_id",
        "created": false
      }
    }

서제스트 워드 삭제
====================

요청
----------

::

    DELETE /api/admin/suggest/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_suggest_id",
        "created": false
      }
    }

전체 서제스트 워드 삭제
======================

요청
----------

::

    DELETE /api/admin/suggest/delete-all

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "count": 250
      }
    }

사용 예
======

인기 키워드 추가
--------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/suggest/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "text": "getting started",
           "fields": ["title"],
           "tags": ["tutorial"],
           "roles": ["guest"],
           "lang": "en",
           "score": 5.0
         }'

서제스트 일괄 삭제
--------------------

.. code-block:: bash

    # 전체 서제스트 삭제
    curl -X DELETE "http://localhost:8080/api/admin/suggest/delete-all" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-badword` - NG 워드 API
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/suggest-guide` - 서제스트 관리 가이드
