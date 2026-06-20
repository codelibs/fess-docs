==========================
LabelType API
==========================

개요
====

LabelType API는 |Fess| 의 라벨 타입을 관리하기 위한 API입니다.
라벨 타입을 사용하면 크롤링 대상 경로나 가상 호스트를 기반으로 검색 결과를 분류하고,
검색 화면에서 라벨을 이용한 필터링에 활용할 수 있습니다.

인증 방법 및 응답의 공통 사양(``status`` 코드, ``version`` 필드, 오류 형식,
HTTP 상태 코드 등)에 대해서는 :doc:`api-admin-overview` 를 참조하십시오.
이 API에 접근하려면 관리 API 권한(``admin-api``)을 가진 액세스 토큰을
``Authorization: Bearer <액세스 토큰>`` 헤더로 지정해야 합니다.

기본 URL
=========

::

    /api/admin/labeltype

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
     - 라벨 타입 목록 조회
   * - GET
     - /setting/{id}
     - 라벨 타입 조회
   * - POST
     - /setting
     - 라벨 타입 생성
   * - PUT
     - /setting
     - 라벨 타입 업데이트
   * - DELETE
     - /setting/{id}
     - 라벨 타입 삭제

라벨 타입 목록 조회
====================

요청
----------

::

    GET /api/admin/labeltype/settings

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
     - 아니요
     - 페이지당 건수. 기본값은 ``paging.page.size`` 의 설정값(기본 ``25``)입니다.
   * - ``page``
     - Integer
     - 아니요
     - 페이지 번호(1부터 시작). 기본값은 ``1`` 입니다.
   * - ``name``
     - String
     - 아니요
     - 표시 이름으로 필터링(와일드카드 검색).
   * - ``value``
     - String
     - 아니요
     - 라벨 값으로 필터링(와일드카드 검색).

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "permissions": "{role}admin",
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

   각 설정 객체에는 감사용 ``createdBy`` / ``createdTime`` / ``updatedBy`` /
   ``updatedTime`` 과 낙관적 잠금용 ``versionNo`` 도 포함됩니다(값이 ``null`` 인
   필드는 생략됩니다). ``response`` 객체에는 제품 버전을 나타내는
   ``version`` 이 항상 포함되지만, 이후 예시에서는 간결함을 위해 생략하는 경우가 있습니다.

라벨 타입 조회
================

요청
----------

::

    GET /api/admin/labeltype/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "label_id_1",
          "name": "Documentation",
          "value": "docs",
          "includedPaths": ".*docs\\.example\\.com.*",
          "excludedPaths": "",
          "permissions": "{role}admin",
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

라벨 타입 생성
================

요청
----------

::

    POST /api/admin/labeltype/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "News",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/news/.*",
      "excludedPaths": ".*/(archive|old)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``name``
     - String
     - 예
     - 라벨 표시 이름(최대 100자).
   * - ``value``
     - String
     - 예
     - 라벨 값(검색 시 ``label`` 파라미터로 사용). 영숫자와 언더스코어(``_``)만 사용 가능하며, 정규 표현식 ``^[a-zA-Z0-9_]+$`` 에 일치해야 합니다(최대 100자).
   * - ``includedPaths``
     - String
     - 아니요
     - 라벨 대상 경로의 정규 표현식. 여러 개 지정 시 줄바꿈(``\n``)으로 구분합니다.
   * - ``excludedPaths``
     - String
     - 아니요
     - 라벨 대상에서 제외할 경로의 정규 표현식. 여러 개 지정 시 줄바꿈(``\n``)으로 구분합니다.
   * - ``permissions``
     - String
     - 아니요
     - 접근을 허용할 역할/그룹/사용자(예: ``{role}admin``). 여러 개 지정 시 줄바꿈(``\n``)으로 구분합니다.
   * - ``sortOrder``
     - Integer
     - 아니요
     - 표시 순서(0 이상의 정수). 지정하지 않으면 ``0`` 입니다.
   * - ``virtualHost``
     - String
     - 아니요
     - 가상 호스트(최대 1000자).

.. note::

   ``createdBy`` / ``createdTime`` 등의 감사 필드는 서버 측에서 자동으로 설정되므로
   요청에서 지정할 필요가 없습니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_label_id",
        "created": true
      }
    }

생성에 성공하면 ``created`` 는 ``true`` 가 됩니다.

라벨 타입 업데이트
====================

요청
----------

::

    PUT /api/admin/labeltype/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_label_id",
      "name": "News Articles",
      "value": "news",
      "includedPaths": ".*news\\.example\\.com.*\n.*example\\.com/(news|articles)/.*",
      "excludedPaths": ".*/(archive|old|draft)/.*",
      "sortOrder": 1,
      "permissions": "{role}guest",
      "versionNo": 1
    }

업데이트 시에는 생성 시의 필드에 더해 다음 필드가 필수입니다.

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 56

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``id``
     - String
     - 예
     - 업데이트 대상 라벨 타입 ID.
   * - ``versionNo``
     - Integer
     - 예
     - 낙관적 잠금용 버전 번호. 조회 시 응답에 포함된 ``versionNo`` 를 지정합니다. 지정한 버전이 현재 버전과 일치하지 않으면 업데이트가 실패합니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_label_id",
        "created": false
      }
    }

업데이트의 경우 ``created`` 는 ``false`` 가 됩니다.

라벨 타입 삭제
================

요청
----------

::

    DELETE /api/admin/labeltype/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

사용 예시
==========

문서용 라벨 생성
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/labeltype/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Technical Documentation",
           "value": "tech_docs",
           "includedPaths": ".*docs\\.example\\.com.*\n.*example\\.com/documentation/.*",
           "sortOrder": 0,
           "permissions": "{role}guest"
         }'

라벨 타입 목록 조회
--------------------

.. code-block:: bash

    curl "http://localhost:8080/api/admin/labeltype/settings?size=50&page=1" \
         -H "Authorization: Bearer YOUR_TOKEN"

라벨을 사용한 검색
--------------------

.. code-block:: bash

    # 라벨로 필터링
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

참고 정보
==========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../api-search` - 검색 API
- :doc:`../../admin/labeltype-guide` - 라벨 타입 관리 가이드
