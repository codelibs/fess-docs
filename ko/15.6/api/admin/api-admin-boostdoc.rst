==========================
BoostDoc API
==========================

개요
====

BoostDoc API는 |Fess| 의 문서 부스트 설정을 관리하기 위한 API입니다.
특정 조건에 일치하는 문서의 검색 순위를 조정할 수 있습니다.

기본 URL
=========

::

    /api/admin/boostdoc

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
     - 문서 부스트 목록 조회
   * - GET
     - /setting/{id}
     - 문서 부스트 조회
   * - POST
     - /setting
     - 문서 부스트 만들기
   * - PUT
     - /setting
     - 문서 부스트 업데이트
   * - DELETE
     - /setting/{id}
     - 문서 부스트 삭제

문서 부스트 목록 조회
============================

요청
----------

::

    GET /api/admin/boostdoc/settings
    PUT /api/admin/boostdoc/settings

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
            "id": "boostdoc_id_1",
            "urlExpr": ".*docs\\.example\\.com.*",
            "boostExpr": "3.0",
            "sortOrder": 0
          }
        ],
        "total": 5
      }
    }

문서 부스트 조회
========================

요청
----------

::

    GET /api/admin/boostdoc/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "boostdoc_id_1",
          "urlExpr": ".*docs\\.example\\.com.*",
          "boostExpr": "3.0",
          "sortOrder": 0
        }
      }
    }

문서 부스트 만들기
========================

요청
----------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "5.0",
      "sortOrder": 0
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``urlExpr``
     - 예
     - URL 정규 표현식 패턴
   * - ``boostExpr``
     - 예
     - 부스트 식 (숫자 또는 표현식)
   * - ``sortOrder``
     - 아니오
     - 적용 순서

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_boostdoc_id",
        "created": true
      }
    }

문서 부스트 업데이트
========================

요청
----------

::

    PUT /api/admin/boostdoc/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_boostdoc_id",
      "urlExpr": ".*important\\.example\\.com.*",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_boostdoc_id",
        "created": false
      }
    }

문서 부스트 삭제
========================

요청
----------

::

    DELETE /api/admin/boostdoc/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_boostdoc_id",
        "created": false
      }
    }

부스트 식 예시
==============

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 부스트 식
     - 설명
   * - ``2.0``
     - 고정값으로 부스트
   * - ``doc['boost'].value * 2``
     - 문서의 boost 값을 2배
   * - ``Math.log(doc['click_count'].value + 1)``
     - 클릭 수에 기반한 로그 스케일 부스트
   * - ``doc['last_modified'].value > now - 7d ? 3.0 : 1.0``
     - 최종 업데이트가 1주일 이내면 3배

사용 예
======

문서 사이트 부스트
----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*docs\\.example\\.com.*",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

새로운 콘텐츠 부스트
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": ".*",
           "boostExpr": "doc[\"last_modified\"].value > now - 30d ? 2.0 : 1.0",
           "sortOrder": 10
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/boostdoc-guide` - 문서 부스트 관리 가이드
