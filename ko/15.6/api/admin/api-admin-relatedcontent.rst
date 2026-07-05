==========================
RelatedContent API
==========================

개요
====

RelatedContent API는 |Fess| 의 관련 콘텐츠를 관리하기 위한 API입니다.
특정 키워드에 관련된 콘텐츠를 커스텀 표시할 수 있습니다.

기본 URL
=========

::

    /api/admin/relatedcontent

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
     - 관련 콘텐츠 목록 조회
   * - GET
     - /setting/{id}
     - 관련 콘텐츠 조회
   * - POST
     - /setting
     - 관련 콘텐츠 만들기
   * - PUT
     - /setting
     - 관련 콘텐츠 업데이트
   * - DELETE
     - /setting/{id}
     - 관련 콘텐츠 삭제

관련 콘텐츠 목록 조회
======================

요청
----------

::

    GET /api/admin/relatedcontent/settings
    PUT /api/admin/relatedcontent/settings

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
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

관련 콘텐츠 조회
==================

요청
----------

::

    GET /api/admin/relatedcontent/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "sortOrder": 0,
          "virtualHost": ""
        }
      }
    }

관련 콘텐츠 만들기
==================

요청
----------

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
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
   * - ``content``
     - 예
     - 표시할 HTML 콘텐츠
   * - ``sortOrder``
     - 아니오
     - 표시 순서
   * - ``virtualHost``
     - 아니오
     - 가상 호스트

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

관련 콘텐츠 업데이트
==================

요청
----------

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

관련 콘텐츠 삭제
==================

요청
----------

::

    DELETE /api/admin/relatedcontent/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_content_id",
        "created": false
      }
    }

사용 예
======

제품 정보 관련 콘텐츠
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "content": "<div class=\"product-info\"><h3>Our Products</h3><ul><li>Product A</li><li>Product B</li></ul></div>",
           "sortOrder": 0
         }'

지원 정보 관련 콘텐츠
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedcontent/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "support",
           "content": "<div><p>Need help? Contact: support@example.com</p></div>",
           "sortOrder": 0
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-relatedquery` - 관련 쿼리 API
- :doc:`../../admin/relatedcontent-guide` - 관련 콘텐츠 관리 가이드
