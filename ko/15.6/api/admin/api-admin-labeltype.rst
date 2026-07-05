==========================
LabelType API
==========================

개요
====

LabelType API는 |Fess| 의 라벨 타입을 관리하기 위한 API입니다.
검색 결과의 라벨 분류, 필터링용 라벨 타입을 조작할 수 있습니다.

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
   * - GET/PUT
     - /settings
     - 라벨 타입 목록 조회
   * - GET
     - /setting/{id}
     - 라벨 타입 조회
   * - POST
     - /setting
     - 라벨 타입 만들기
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
    PUT /api/admin/labeltype/settings

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
            "id": "label_id_1",
            "name": "Documentation",
            "value": "docs",
            "includedPaths": ".*docs\\.example\\.com.*",
            "excludedPaths": "",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

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
          "sortOrder": 0,
          "permissions": [],
          "virtualHost": ""
        }
      }
    }

라벨 타입 만들기
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
      "permissions": ["guest"]
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
     - 라벨 표시 이름
   * - ``value``
     - 예
     - 라벨 값 (검색 시 사용)
   * - ``includedPaths``
     - 아니오
     - 라벨 대상 경로의 정규 표현식 (여러 개인 경우 줄바꿈으로 구분)
   * - ``excludedPaths``
     - 아니오
     - 라벨 제외 경로의 정규 표현식 (여러 개인 경우 줄바꿈으로 구분)
   * - ``sortOrder``
     - 아니오
     - 표시 순서
   * - ``permissions``
     - 아니오
     - 접근 허용 역할
   * - ``virtualHost``
     - 아니오
     - 가상 호스트

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

라벨 타입 업데이트
================

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
      "permissions": ["guest"],
      "versionNo": 1
    }

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
        "status": 0,
        "id": "deleted_label_id",
        "created": false
      }
    }

사용 예
======

문서용 라벨 만들기
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
           "permissions": ["guest"]
         }'

라벨을 사용한 검색
--------------------

.. code-block:: bash

    # 라벨로 필터링
    curl "http://localhost:8080/json/?q=search&label=tech_docs"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../api-search` - 검색 API
- :doc:`../../admin/labeltype-guide` - 라벨 타입 관리 가이드
