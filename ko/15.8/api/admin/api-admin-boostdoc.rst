==========================
BoostDoc API
==========================

개요
====

BoostDoc API는 |Fess| 의 문서 부스트 설정을 관리하기 위한 API입니다.
문서 부스트를 설정하면, 특정 조건에 일치하는 문서의 점수를 높여
검색 결과 상위에 표시되기 쉽게 할 수 있습니다.

부스트는 인덱스 생성 시(크롤링 시)에 각 문서에 적용됩니다.
조건(``urlExpr``)과 부스트 값(``boostExpr``)은 모두 Groovy 식으로 평가됩니다.
여러 규칙은 ``sortOrder`` 의 오름차순으로 평가되며, 처음 조건이 일치한 규칙의 부스트 값만 적용됩니다
(일치하는 규칙이 발견되면, 이후 규칙은 평가되지 않습니다).

.. note::

   관리 화면에서는 ``urlExpr`` 은 "조건", ``boostExpr`` 은 "부스트 값 식"으로 표시됩니다.
   설정 항목의 자세한 내용은 :doc:`../../admin/boostdoc-guide` 를 참조하십시오.

기본 URL
=========

::

    /api/admin/boostdoc

인증
====

이 API를 사용하려면 ``Radmin-api`` 권한을 가진 액세스 토큰이 필요합니다.
액세스 토큰 취득 방법과 지정 방법은 :doc:`api-admin-overview` 를 참조하십시오.

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
=====================

요청
----------

::

    GET /api/admin/boostdoc/settings

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
     - 페이지당 건수 (기본값: 25)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작. 기본값: 1)
   * - ``urlExpr``
     - String
     - 아니오
     - 조건식으로 필터링 (부분 일치)
   * - ``boostExpr``
     - String
     - 아니오
     - 부스트 값 식으로 필터링 (부분 일치)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "boostdoc_id_1",
            "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
            "boostExpr": "3.0",
            "sortOrder": 1,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   위에 표시된 필드 외에도, 응답의 각 설정 객체에는 생성/업데이트 메타데이터(``createdBy``, ``createdTime``, ``updatedBy``, ``updatedTime``)가 포함됩니다.
   ``versionNo`` 는 업데이트(PUT) 시에 필수이므로, 업데이트 전에 조회 또는 목록 API를 통해 현재 값을 취득하십시오.

문서 부스트 조회
================

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
          "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
          "boostExpr": "3.0",
          "sortOrder": 1,
          "versionNo": 1
        }
      }
    }

문서 부스트 만들기
==================

요청
----------

::

    POST /api/admin/boostdoc/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
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
     - 조건식. 부스트 대상 문서를 판별하는 Groovy 식으로, ``Boolean`` 을 반환합니다. 관리 화면의 "조건"에 해당합니다 (최대 10000자).
   * - ``boostExpr``
     - 예
     - 부스트 값 식. 부스트 값(숫자)을 반환하는 Groovy 식입니다. ``3.0`` 과 같은 고정값도 지정할 수 있습니다. 관리 화면의 "부스트 값 식"에 해당합니다 (최대 10000자).
   * - ``sortOrder``
     - 예
     - 적용 순서. 규칙은 오름차순으로 평가되며, 처음 조건이 일치한 규칙의 부스트 값이 적용됩니다 (폼 초기값: 0, 0 이상의 정수).

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
====================

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
      "urlExpr": "url.startsWith(\"https://important.example.com/\")",
      "boostExpr": "10.0",
      "sortOrder": 0,
      "versionNo": 1
    }

업데이트 시에는 만들기 시의 필드에 더하여 ``id`` (대상 규칙의 ID, 최대 1000자)와 ``versionNo`` (낙관적 잠금을 위한 버전 번호)가 필수입니다.
``versionNo`` 에는 조회 또는 목록 API 응답에서 취득한 현재 버전 번호를 지정하십시오.
버전 번호가 일치하지 않으면 업데이트는 실패합니다.

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
================

요청
----------

::

    DELETE /api/admin/boostdoc/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

조건식 및 부스트 값 식에 대하여
================================

``urlExpr`` (조건)과 ``boostExpr`` (부스트 값 식)은 모두 Groovy 식으로 평가됩니다.
식 안에서는 인덱스 대상 문서의 필드 값을 필드명 변수로 참조할 수 있습니다.

- ``urlExpr`` 은 ``Boolean`` 을 반환해야 합니다 (예: ``url.startsWith("https://docs.example.com/")``). 단순 정규식 문자열 (예: ``.*docs\.example\.com.*``)은 Groovy 식으로서 ``Boolean`` 을 반환하지 않으므로 조건으로 동작하지 않습니다. 정규식을 사용하는 경우에는 Groovy의 ``String#matches`` 를 이용합니다.
- ``boostExpr`` 은 숫자를 반환해야 합니다. 결과는 ``float`` 으로 변환되며, 0보다 큰 경우에만 부스트가 적용됩니다.

.. note::

   식 안에서 참조할 수 있는 주요 필드 변수: ``url``, ``title``, ``content``, ``content_length``, ``last_modified`` 등.
   ``click_count`` 와 ``favorite_count`` 는 각각 ``indexer.click.count.enabled`` /
   ``indexer.favorite.count.enabled`` (모두 기본적으로 활성화)가 설정된 경우에 참조할 수 있습니다.
   ``now - 7d`` 와 같은 OpenSearch 날짜 계산 구문은 Groovy에서 사용할 수 없습니다.

조건식(``urlExpr``) 예시
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 조건식
     - 설명
   * - ``url.startsWith("https://docs.example.com/")``
     - 지정한 URL로 시작하는 문서를 대상으로 함
   * - ``url.matches("https://www\\.example\\.com/.*")``
     - 정규식(Groovy의 ``String#matches``)으로 URL을 판별함
   * - ``title.contains("릴리스 노트")``
     - 제목에 특정 단어를 포함하는 문서를 대상으로 함

부스트 값 식(``boostExpr``) 예시
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 부스트 값 식
     - 설명
   * - ``3.0``
     - 고정값으로 부스트
   * - ``click_count * 0.1 + 1``
     - 클릭 수에 따라 부스트
   * - ``Math.log(click_count + 1)``
     - 클릭 수에 기반한 로그 스케일 부스트

사용 예
======

문서 사이트 부스트
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://docs.example.com/\")",
           "boostExpr": "5.0",
           "sortOrder": 0
         }'

클릭 수가 많은 콘텐츠 부스트
-----------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/boostdoc/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "urlExpr": "url.startsWith(\"https://www.example.com/\")",
           "boostExpr": "click_count * 0.1 + 1",
           "sortOrder": 10
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/boostdoc-guide` - 문서 부스트 관리 가이드
