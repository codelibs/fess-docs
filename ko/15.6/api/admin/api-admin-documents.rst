==========================
Documents API
==========================

개요
====

Documents API는 |Fess| 인덱스 내의 문서를 관리하기 위한 API입니다.
문서의 일괄 삭제, 업데이트, 검색 등의 작업을 수행할 수 있습니다.

기본 URL
=========

::

    /api/admin/documents

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - DELETE
     - /
     - 문서 삭제 (쿼리 지정)
   * - DELETE
     - /{id}
     - 문서 삭제 (ID 지정)

쿼리 지정 문서 삭제
==============================

검색 쿼리와 일치하는 문서를 일괄 삭제합니다.

요청
----------

::

    DELETE /api/admin/documents

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``q``
     - String
     - 예
     - 삭제 대상 검색 쿼리

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

사용 예
~~~~~~

.. code-block:: bash

    # 특정 사이트의 문서 삭제
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 오래된 문서 삭제
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 라벨 지정으로 문서 삭제
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

ID 지정 문서 삭제
==========================

문서 ID를 지정하여 삭제합니다.

요청
----------

::

    DELETE /api/admin/documents/{id}

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``id``
     - String
     - 예
     - 문서 ID (경로 파라미터)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

사용 예
~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

쿼리 구문
==========

삭제 쿼리에는 |Fess| 의 표준 검색 구문을 사용할 수 있습니다.

기본 쿼리
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 쿼리 예
     - 설명
   * - ``url:example.com``
     - URL에 "example.com"을 포함하는 문서
   * - ``url:https://example.com/*``
     - 특정 프리픽스를 가진 URL
   * - ``host:example.com``
     - 특정 호스트의 문서
   * - ``title:keyword``
     - 제목에 키워드를 포함하는 문서
   * - ``content:keyword``
     - 본문에 키워드를 포함하는 문서
   * - ``label:mylabel``
     - 특정 라벨을 가진 문서

날짜 범위 쿼리
--------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 쿼리 예
     - 설명
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - 지정 기간 내에 업데이트된 문서
   * - ``lastModified:[* TO 2023-01-01]``
     - 지정일 이전에 업데이트된 문서
   * - ``created:[2024-01-01 TO *]``
     - 지정일 이후에 생성된 문서

복합 쿼리
----------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 쿼리 예
     - 설명
   * - ``url:example.com AND label:blog``
     - AND 조건
   * - ``url:example.com OR url:sample.com``
     - OR 조건
   * - ``NOT url:example.com``
     - NOT 조건
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - 그룹화

주의 사항
========

삭제 작업 주의
--------------

.. warning::
   삭제 작업은 되돌릴 수 없습니다. 운영 환경에서 실행하기 전에 반드시 테스트 환경에서 확인하세요.

- 대량의 문서를 삭제하는 경우 처리에 시간이 걸릴 수 있습니다
- 삭제 중에는 인덱스 성능에 영향이 있을 수 있습니다
- 삭제 후 검색 결과에 반영되기까지 약간의 시간이 걸릴 수 있습니다

권장 사항
----------------

1. **삭제 전 확인**: 같은 쿼리로 검색 API를 사용하여 삭제 대상 확인
2. **단계적 삭제**: 대량 삭제는 여러 번에 나누어 실행
3. **백업**: 중요한 데이터는 사전에 백업

사용 예
======

사이트 전체 재크롤링 준비
--------------------------

.. code-block:: bash

    # 특정 사이트의 오래된 문서 삭제
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # 크롤링 작업 시작
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

오래된 문서 정리
--------------------------------

.. code-block:: bash

    # 1년 이상 업데이트되지 않은 문서 삭제
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/searchlist-guide` - 검색 목록 관리 가이드
