==========================
Suggest API
==========================

개요
====

Suggest API는 |Fess| 의 서제스트 기능에서 사용되는 서제스트 워드를 관리하기 위한 API입니다.
서제스트 워드의 건수에 관한 통계 정보 조회와 서제스트 워드 삭제를 수행할 수 있습니다.

서제스트 워드에는 크롤링한 문서에서 생성된 것(문서 유래)과
사용자의 검색 쿼리에서 생성된 것(검색 쿼리 유래)이 있습니다. 본 API에서는 이를
종류별로 삭제하거나, 전체를 일괄 삭제할 수 있습니다.

인증
====

본 API에 접근하려면 액세스 토큰을 통한 인증이 필요합니다. 요청 헤더에
액세스 토큰을 지정하십시오.

::

    Authorization: Bearer <액세스 토큰>

액세스 토큰에는 Admin API 권한(기본값: ``Radmin-api``)이 부여되어 있어야 합니다.
액세스 토큰 취득 방법 및 권한에 대한 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

기본 URL
=========

::

    /api/admin/suggest

엔드포인트 목록
================

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
----

::

    GET /api/admin/suggest

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "totalWordsNum": 1500,
          "documentWordsNum": 1200,
          "queryWordsNum": 450
        }
      }
    }

응답 필드
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``setting.totalWordsNum``
     - 서제스트 워드의 총수(서제스트 인덱스에 등록된 서제스트 워드의 건수)
   * - ``setting.documentWordsNum``
     - 문서에서 유래한 서제스트 워드 수(문서 빈도가 1 이상인 서제스트 워드의 건수)
   * - ``setting.queryWordsNum``
     - 검색 쿼리에서 유래한 서제스트 워드 수(쿼리 빈도가 1 이상인 서제스트 워드의 건수)

.. note::

   ``documentWordsNum`` 과 ``queryWordsNum`` 은 배타적이지 않습니다. 하나의 서제스트 워드가
   문서와 검색 쿼리 양쪽에서 유래한 경우, 양쪽 건수에 모두 포함됩니다. 이로 인해
   ``documentWordsNum`` 과 ``queryWordsNum`` 의 합계가 ``totalWordsNum`` 과 일치하지 않을 수 있습니다.

전체 서제스트 워드 삭제
========================

모든 서제스트 워드를 삭제합니다. 문서 유래·검색 쿼리 유래의 구분 없이
서제스트 인덱스 내의 모든 서제스트 워드가 대상입니다.

요청
----

::

    DELETE /api/admin/suggest/all

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

문서에서 유래한 서제스트 워드 삭제
====================================

문서에서 생성된 서제스트 워드(문서 유래 서제스트 워드)를 삭제합니다.

요청
----

::

    DELETE /api/admin/suggest/document

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

검색 쿼리에서 유래한 서제스트 워드 삭제
==========================================

검색 쿼리에서 생성된 서제스트 워드(검색 쿼리 유래 서제스트 워드)를 삭제합니다.

요청
----

::

    DELETE /api/admin/suggest/query

응답
----

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

오류 응답
=========

삭제 처리에 실패한 경우, HTTP 상태 ``400`` 과 함께 응답 본문의 ``status`` 에
``1``(BAD_REQUEST)이 설정되고, ``message`` 에 오류 메시지가 포함됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 1,
        "message": "Failed to delete a document."
      }
    }

액세스 토큰이 미지정·무효하거나 권한이 부족한 경우, 응답 본문의 ``status`` 에
``3``(UNAUTHORIZED)이 설정됩니다. ``status`` 값 및 HTTP 상태 코드 목록에 대해서는
:doc:`api-admin-overview` 를 참조하십시오.

사용 예
=======

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
------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/document" \
         -H "Authorization: Bearer YOUR_TOKEN"

검색 쿼리에서 유래한 서제스트 워드 삭제
------------------------------------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/suggest/query" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-badword` - NG 워드 API
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/suggest-guide` - 서제스트 관리 가이드
