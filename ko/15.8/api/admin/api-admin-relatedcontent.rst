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
   * - GET
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
----

::

    GET /api/admin/relatedcontent/settings

파라미터
~~~~~~~~

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
     - 페이지당 건수 (기본값: 25. ``fess_config.properties`` 의 ``paging.page.size`` 로 변경 가능)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작. 기본값: 1. 0 이하를 지정한 경우 1로 처리됩니다)
   * - ``term``
     - String
     - 아니오
     - 검색 키워드로 필터링 (와일드카드 검색)
   * - ``content``
     - String
     - 아니오
     - 콘텐츠 본문으로 필터링 (와일드카드 검색)

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "content_id_1",
            "term": "fess",
            "content": "<div>Fess is an open source search server.</div>",
            "virtualHost": "",
            "sortOrder": 0,
            "createdBy": "admin",
            "createdTime": 1700000000000,
            "updatedBy": "admin",
            "updatedTime": 1700000000000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``settings`` 의 각 요소 및 단일 조회 엔드포인트가 반환하는 ``setting`` 객체에는
   저장된 엔티티의 필드가 그대로 포함됩니다. ``term``, ``content``, ``sortOrder``,
   ``virtualHost`` 외에도 감사 필드인 ``createdBy``, ``createdTime``, ``updatedBy``,
   ``updatedTime`` 과 낙관적 잠금 필드인 ``versionNo`` 도 반환됩니다. ``createdTime``
   및 ``updatedTime`` 은 에포크 기준 밀리초(숫자)로 표현됩니다. 값이 설정되지 않은
   (null) 필드는 응답에서 생략됩니다. 또한 모든 응답의 ``response`` 객체에는 제품
   버전을 나타내는 ``version`` 이 항상 포함됩니다 (자세한 내용은 :doc:`api-admin-overview`
   를 참조하십시오).

관련 콘텐츠 조회
================

요청
----

::

    GET /api/admin/relatedcontent/setting/{id}

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "content_id_1",
          "term": "fess",
          "content": "<div>Fess is an open source search server.</div>",
          "virtualHost": "",
          "sortOrder": 0,
          "createdBy": "admin",
          "createdTime": 1700000000000,
          "updatedBy": "admin",
          "updatedTime": 1700000000000,
          "versionNo": 1
        }
      }
    }

.. note::

   업데이트(PUT) 시 필요한 ``versionNo`` 는 이 조회 응답에 포함된 값을 지정합니다.

관련 콘텐츠 만들기
==================

요청
----

::

    POST /api/admin/relatedcontent/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "content": "<div class='related'><h3>About Search</h3><p>Learn more about search features...</p></div>",
      "sortOrder": 0,
      "virtualHost": ""
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 필드
     - 필수
     - 설명
   * - ``term``
     - **예**
     - 검색 키워드 (최대 10000자)
   * - ``content``
     - **예**
     - 표시할 HTML 콘텐츠 (최대 10000자)
   * - ``sortOrder``
     - **아니오**
     - 표시 순서 (0 이상 2147483647 이하의 정수)
   * - ``virtualHost``
     - **아니오**
     - 가상 호스트 (최대 1000자)

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_content_id",
        "created": true
      }
    }

관련 콘텐츠 업데이트
====================

요청
----

::

    PUT /api/admin/relatedcontent/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_content_id",
      "term": "search",
      "content": "<div class='related updated'><h3>About Search</h3><p>Updated information...</p></div>",
      "sortOrder": 0,
      "virtualHost": "",
      "versionNo": 1
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 필드
     - 필수
     - 설명
   * - ``id``
     - **예**
     - 업데이트할 관련 콘텐츠의 ID (최대 1000자)
   * - ``term``
     - **예**
     - 검색 키워드 (최대 10000자)
   * - ``content``
     - **예**
     - 표시할 HTML 콘텐츠 (최대 10000자)
   * - ``sortOrder``
     - **아니오**
     - 표시 순서 (0 이상 2147483647 이하의 정수)
   * - ``virtualHost``
     - **아니오**
     - 가상 호스트 (최대 1000자)
   * - ``versionNo``
     - **예**
     - 낙관적 잠금용 버전 번호. ``setting/{id}`` 의 조회 응답에 포함된 값을 지정합니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_content_id",
        "created": false
      }
    }

.. note::

   ``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime`` 등의 감사 필드나
   ``crudMode`` 를 요청 본문에 포함해도 서버 측에서 자동으로 설정되므로 무시됩니다.
   만들기 또는 업데이트 시 지정할 필요는 없습니다.

관련 콘텐츠 삭제
================

요청
----

::

    DELETE /api/admin/relatedcontent/setting/{id}

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

사용 예
=======

제품 정보 관련 콘텐츠
---------------------

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
---------------------

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
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-relatedquery` - 관련 쿼리 API
- :doc:`../../admin/relatedcontent-guide` - 관련 콘텐츠 관리 가이드
