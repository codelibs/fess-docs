==========================
Suggest API
==========================

개요
====

Suggest API는 |Fess| 의 서제스트 기능을 관리하기 위한 API입니다.
서제스트 워드의 통계 정보 조회와 서제스트 워드 삭제를 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/suggest

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /
     - 서제스트 워드 통계 정보 조회
   * - DELETE
     - /all
     - 전체 서제스트 워드 삭제
   * - DELETE
     - /document
     - 문서에서 유래한 서제스트 워드 삭제
   * - DELETE
     - /query
     - 검색 쿼리에서 유래한 서제스트 워드 삭제

서제스트 워드 통계 정보 조회
==============================

서제스트 워드의 건수에 관한 통계 정보를 조회합니다.

요청
----------

::

    GET /api/admin/suggest

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 300
        }
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``setting.totalWordsNum``
     - 서제스트 워드의 총수
   * - ``setting.documentWordsNum``
     - 문서에서 유래한 서제스트 워드 수
   * - ``setting.queryWordsNum``
     - 검색 쿼리에서 유래한 서제스트 워드 수

전체 서제스트 워드 삭제
========================

모든 서제스트 워드를 삭제합니다.

요청
----------

::

    DELETE /api/admin/suggest/all

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

문서에서 유래한 서제스트 워드 삭제
========================================

문서에서 생성된 서제스트 워드를 삭제합니다.

요청
----------

::

    DELETE /api/admin/suggest/document

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

검색 쿼리에서 유래한 서제스트 워드 삭제
======================================

검색 쿼리에서 생성된 서제스트 워드를 삭제합니다.

요청
----------

::

    DELETE /api/admin/suggest/query

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

사용 예
======

통계 정보 조회
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/suggest" \
         -H "Authorization: Bearer YOUR_TOKEN"

전체 서제스트 워드 삭제
------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/all" \
         -H "Authorization: Bearer YOUR_TOKEN"

문서에서 유래한 서제스트 워드 삭제
----------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-badword` - NG 워드 API
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/suggest-guide` - 서제스트 관리 가이드
