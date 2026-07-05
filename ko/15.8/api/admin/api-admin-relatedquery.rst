==========================
RelatedQuery API
==========================

개요
====

RelatedQuery API는 |Fess| 의 관련 쿼리를 관리하기 위한 API입니다.
사용자가 입력하는 검색 키워드(``term``)에 대해 관련 검색 키워드 후보
(``queries``)를 등록·관리할 수 있습니다. 등록한 관련 쿼리는 검색 화면에서 관련 검색 후보로
표시됩니다.

인증 방법, 공통 응답 형식(``version`` 필드 및 ``status`` 코드),
페이지네이션, 오류 응답의 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

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
   * - GET
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
====================

요청
----

::

    GET /api/admin/relatedquery/settings

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
     - 페이지 번호 (1부터 시작. 기본값: 1)

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "settings": [
          {
            "id": "query_id_1",
            "term": "fess",
            "queries": "fess tutorial\nfess installation\nfess configuration",
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   각 설정에는 ``versionNo`` (낙관적 잠금용 버전 번호)가 포함됩니다. ``virtualHost``
   및 감사용 필드(``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``)는
   값이 설정된 경우에만 포함됩니다. 값이 비어 있는 ``virtualHost`` 는 응답에 포함되지 않습니다.

관련 쿼리 조회
==============

요청
----

::

    GET /api/admin/relatedquery/setting/{id}

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "setting": {
          "id": "query_id_1",
          "term": "fess",
          "queries": "fess tutorial\nfess installation\nfess configuration",
          "virtualHost": "site1.example.com",
          "versionNo": 1
        }
      }
    }

관련 쿼리 만들기
================

요청
----

::

    POST /api/admin/relatedquery/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search",
      "virtualHost": ""
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 10 70

   * - 필드
     - 필수
     - 설명
   * - ``term``
     - 예
     - 검색 키워드 (최대 10000자)
   * - ``queries``
     - 예
     - 관련 쿼리. 한 줄에 한 건씩 작성한 줄바꿈 구분 문자열입니다 (빈 줄은 무시됩니다. 최대 10000자)
   * - ``virtualHost``
     - 아니오
     - 가상 호스트 (최대 1000자)

.. note::

   ``crudMode`` 는 API 측에서 자동으로 설정되므로 요청 본문에 포함할 필요가 없습니다.

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "new_query_id",
        "created": true
      }
    }

관련 쿼리 업데이트
==================

요청
----

::

    PUT /api/admin/relatedquery/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_query_id",
      "term": "search",
      "queries": "search tutorial\nsearch syntax\nadvanced search\nsearch tips",
      "virtualHost": "",
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
     - 업데이트 대상 관련 쿼리 ID (최대 1000자)
   * - ``term``
     - 예
     - 검색 키워드 (최대 10000자)
   * - ``queries``
     - 예
     - 관련 쿼리. 한 줄에 한 건씩 작성한 줄바꿈 구분 문자열입니다 (빈 줄은 무시됩니다. 최대 10000자)
   * - ``virtualHost``
     - 아니오
     - 가상 호스트 (최대 1000자)
   * - ``versionNo``
     - 예
     - 낙관적 잠금용 버전 번호. 조회 시 응답에 포함된 값을 지정합니다

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "id": "existing_query_id",
        "created": false
      }
    }

관련 쿼리 삭제
==============

요청
----

::

    DELETE /api/admin/relatedquery/setting/{id}

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

오류 응답
=========

요청이 실패한 경우 ``status`` 에 0 이외의 값이 설정되고, ``message`` 에 오류 내용이
포함됩니다. 예를 들어 필수 필드 누락 등의 유효성 검사 오류에서는 ``status`` 가 ``1`` 이 됩니다.
상태 코드 목록은 :doc:`api-admin-overview` 를 참조하십시오.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "..."
      }
    }

사용 예
=======

제품 관련 쿼리
--------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product",
           "queries": "product features\nproduct pricing\nproduct comparison\nproduct reviews"
         }'

도움말 관련 쿼리
----------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/relatedquery/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "help",
           "queries": "help center\nhelp documentation\nhelp contact support"
         }'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-relatedcontent` - 관련 콘텐츠 API
- :doc:`api-admin-suggest` - 서제스트 관리 API
- :doc:`../../admin/relatedquery-guide` - 관련 쿼리 관리 가이드
