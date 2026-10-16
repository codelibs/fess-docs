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
   * - GET
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
     - 페이지당 건수 (기본값: 25。\ ``paging.page.size`` 의 설정값)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작, 기본값: 1)
   * - ``term``
     - String
     - 아니오
     - 검색 키워드로 필터링 (와일드카드 일치)
   * - ``query``
     - String
     - 아니오
     - 매치 조건 쿼리로 필터링 (와일드카드 일치)

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
            "max_size": 10,
            "boost": 10.0,
            "version_no": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   ``total`` 에는 필터링 조건에 일치하는 총 건수가 설정됩니다 (현재 페이지의 건수가 아닙니다).
   각 설정 객체에는 위의 필드 외에도, 값이 설정되어 있는 경우 ``virtual_host`` 、
   ``created_by`` 、 ``created_time`` 、 ``updated_by`` 、 ``updated_time`` 이 포함됩니다.

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
          "max_size": 10,
          "boost": 10.0,
          "created_by": "admin",
          "created_time": 1700000000000,
          "updated_by": "admin",
          "updated_time": 1700000000000,
          "version_no": 1
        }
      }
    }

.. note::

   ``version_no`` 는 낙관적 잠금(Optimistic Lock)을 위한 버전 번호입니다. 키 매치를 업데이트할 때는
   조회 시 얻은 ``version_no`` 를 요청 본문에 지정해 주세요. 지정한 ID가 존재하지 않는 경우 오류가 반환됩니다.

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
      "max_size": 5,
      "boost": 20.0
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``term``
     - String
     - 예
     - 검색 키워드 (최대 100자)
   * - ``query``
     - String
     - 예
     - 매치 조건 쿼리 (최대 길이는 ``form.admin.max.input.size`` 의 설정값에 따름)
   * - ``max_size``
     - Integer
     - 예
     - 최대 표시 건수 (0 이상의 정수. 관리 화면 초기값: 10)
   * - ``boost``
     - Float
     - 예
     - 부스트 값 (관리 화면 초기값: 100.0)
   * - ``virtual_host``
     - String
     - 아니오
     - 가상 호스트명 (최대 1000자. 가상 호스트별로 키 매치를 전환할 경우 지정)

.. note::

   ``max_size`` 와 ``boost`` 는 API를 통해서는 필수 항목입니다. 초기값은 관리 화면 폼에 표시되는 값이며,
   API에서는 적용되지 않습니다. 생략한 경우 유효성 검사 오류가 발생합니다.
   또한, ``created_by`` 와 ``created_time`` 은 요청에서 지정하더라도 서버 측에서 덮어씁니다.

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
================

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
      "max_size": 10,
      "boost": 15.0,
      "version_no": 1
    }

필드 설명
~~~~~~~~~~~~~~

만들기 시의 필드 ( ``term`` 、 ``query`` 、 ``max_size`` 、 ``boost`` 、 ``virtual_host`` ) 에 더해,
아래 필드를 지정합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``id``
     - String
     - 예
     - 업데이트 대상 키 매치 ID (최대 1000자)
   * - ``version_no``
     - Integer
     - 예
     - 낙관적 잠금을 위한 버전 번호. 조회 시 얻은 값을 지정

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
        "status": 0
      }
    }

사용 예
=======

제품 페이지 키 매치 만들기
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/keymatch/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "term": "product features",
           "query": "url:*/products/* AND (title:features OR content:features)",
           "max_size": 10,
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
           "max_size": 5,
           "boost": 20.0
         }'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/keymatch-guide` - 키 매치 관리 가이드
