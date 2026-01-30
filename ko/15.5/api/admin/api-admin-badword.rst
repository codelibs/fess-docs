==========================
BadWord API
==========================

개요
====

BadWord API는 |Fess| 의 NG 워드(부적절한 서제스트 워드 제외)를 관리하기 위한 API입니다.
서제스트 기능에서 표시하고 싶지 않은 키워드를 설정할 수 있습니다.

기본 URL
=========

::

    /api/admin/badword

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
     - NG 워드 목록 조회
   * - GET
     - /setting/{id}
     - NG 워드 조회
   * - POST
     - /setting
     - NG 워드 만들기
   * - PUT
     - /setting
     - NG 워드 업데이트
   * - DELETE
     - /setting/{id}
     - NG 워드 삭제

NG 워드 목록 조회
================

요청
----------

::

    GET /api/admin/badword/settings
    PUT /api/admin/badword/settings

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
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word",
            "targetRole": "",
            "targetLabel": ""
          }
        ],
        "total": 5
      }
    }

NG 워드 조회
============

요청
----------

::

    GET /api/admin/badword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word",
          "targetRole": "",
          "targetLabel": ""
        }
      }
    }

NG 워드 만들기
============

요청
----------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword",
      "targetRole": "guest",
      "targetLabel": ""
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``suggestWord``
     - 예
     - 제외할 키워드
   * - ``targetRole``
     - 아니오
     - 대상 역할 (비어 있으면 모든 역할)
   * - ``targetLabel``
     - 아니오
     - 대상 라벨 (비어 있으면 모든 라벨)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

NG 워드 업데이트
============

요청
----------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "targetRole": "guest",
      "targetLabel": "",
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

NG 워드 삭제
============

요청
----------

::

    DELETE /api/admin/badword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

사용 예
======

스팸 키워드 제외
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam",
           "targetRole": "",
           "targetLabel": ""
         }'

특정 역할용 NG 워드
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "internal",
           "targetRole": "guest",
           "targetLabel": ""
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-suggest` - 서제스트 관리 API
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/badword-guide` - NG 워드 관리 가이드
