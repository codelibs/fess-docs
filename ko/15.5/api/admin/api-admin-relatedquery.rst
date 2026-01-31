==========================
RelatedQuery API
==========================

개요
====

RelatedQuery API는 |Fess| 의 관련 쿼리를 관리하기 위한 API입니다.
특정 검색 쿼리에 대해 관련 검색 키워드를 제안할 수 있습니다.

기본 URL
=========

::

    /api/admin/relatedquery

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
     - 관련 쿼리 목록 조회
   * - GET
     - /setting/{id}
     - 관련 쿼리 조회
   * - POST
     - /setting
     - 관련 쿼리 만들기
   * - PUT
     - /setting
     - 관련 쿼리 업데이트
   * - DELETE
     - /setting/{id}
     - 관련 쿼리 삭제

관련 쿼리 목록 조회
==================

요청
----------

::

    GET /api/admin/relatedquery/settings
    PUT /api/admin/relatedquery/settings

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
            "id": "query_id_1",
            "term": "fess",
            "queries": ["fess tutorial", "fess installation", "fess configuration"]
          }
        ],
        "total": 5
      }
    }

관련 쿼리 조회
==============

요청
----------

::

    GET /api/admin/relatedquery/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": ["fess tutorial", "fess installation", "fess configuration"],
          "virtualHost": ""
        }
      }
    }

관련 쿼리 만들기
==============

요청
----------

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search"],
      "virtualHost": ""
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
   * - ``queries``
     - 예
     - 관련 쿼리 배열
   * - ``virtualHost``
     - 아니오
     - 가상 호스트

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

관련 쿼리 업데이트
==============

요청
----------

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": ["search tutorial", "search syntax", "advanced search", "search tips"],
      "virtualHost": "",
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

관련 쿼리 삭제
==============

요청
----------

::

    DELETE /api/admin/relatedquery/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_query_id",
        "created": false
      }
    }

사용 예
======

제품 관련 쿼리
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": ["product features", "product pricing", "product comparison", "product reviews"]
         }'

도움말 관련 쿼리
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": ["help center", "help documentation", "help contact support"]
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-relatedcontent` - 관련 콘텐츠 API
- :doc:`api-admin-suggest` - 서제스트 관리 API
- :doc:`../../admin/relatedquery-guide` - 관련 쿼리 관리 가이드
