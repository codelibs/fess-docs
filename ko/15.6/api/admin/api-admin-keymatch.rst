==========================
KeyMatch API
==========================

개요
====

KeyMatch API는 |Fess| 의 키 매치(검색 키워드와 결과의 연결)를 관리하기 위한 API입니다.
특정 키워드에 대해 특정 문서를 상위에 표시할 수 있습니다.

기본 URL
=========

::

    /api/admin/keymatch

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
     - 키 매치 목록 조회
   * - GET
     - /setting/{id}
     - 키 매치 조회
   * - POST
     - /setting
     - 키 매치 만들기
   * - PUT
     - /setting
     - 키 매치 업데이트
   * - DELETE
     - /setting/{id}
     - 키 매치 삭제

키 매치 목록 조회
==================

요청
----------

::

    GET /api/admin/keymatch/settings
    PUT /api/admin/keymatch/settings

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
            "id": "keymatch_id_1",
            "term": "download",
            "query": "title:download OR content:download",
            "maxSize": 10,
            "boost": 10.0
          }
        ],
        "total": 5
      }
    }

키 매치 조회
==============

요청
----------

::

    GET /api/admin/keymatch/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "keymatch_id_1",
          "term": "download",
          "query": "title:download OR content:download",
          "maxSize": 10,
          "boost": 10.0
        }
      }
    }

키 매치 만들기
==============

요청
----------

::

    POST /api/admin/keymatch/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing",
      "maxSize": 5,
      "boost": 20.0
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``term``
     - 예
     - 검색 키워드
   * - ``query``
     - 예
     - 매치 조건 쿼리
   * - ``maxSize``
     - 아니오
     - 최대 표시 건수 (기본값: 10)
   * - ``boost``
     - 아니오
     - 부스트 값 (기본값: 1.0)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_keymatch_id",
        "created": true
      }
    }

키 매치 업데이트
==============

요청
----------

::

    PUT /api/admin/keymatch/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_keymatch_id",
      "term": "pricing",
      "query": "url:*/pricing* OR title:pricing OR content:price",
      "maxSize": 10,
      "boost": 15.0,
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_keymatch_id",
        "created": false
      }
    }

키 매치 삭제
==============

요청
----------

::

    DELETE /api/admin/keymatch/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_keymatch_id",
        "created": false
      }
    }

사용 예
======

제품 페이지 키 매치 만들기
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "maxSize": 10,
           "boost": 15.0
         }'

지원 페이지 키 매치
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "query": "url:*/support/* OR url:*/help/* OR url:*/faq/*",
           "maxSize": 5,
           "boost": 20.0
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/keymatch-guide` - 키 매치 관리 가이드
