==========================
Documents API
==========================

개요
====

Documents API는 |Fess| 인덱스에 문서를 일괄 등록하기 위한 Admin API입니다.
크롤러를 거치지 않고 외부 시스템이 생성한 문서를 직접 인덱스에 추가할 수 있습니다.
1회 요청으로 여러 문서를 한꺼번에 등록할 수 있습니다.

기본 URL
=========

::

    /api/admin/documents

인증
====

이 API를 호출하려면 :doc:`api-admin-overview` 에서 설명하는 액세스 토큰을 통한 인증이 필요합니다.
토큰에는 Admin API에 대한 접근 권한(기본값: ``Radmin-api``)이 부여되어 있어야 합니다.
이 권한은 설정 키 ``api.admin.access.permissions`` 에서 변경할 수 있습니다.

엔드포인트 목록
================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - PUT
     - /bulk
     - 문서 일괄 등록

.. note::

   이 엔드포인트는 ``PUT`` 메서드만 허용합니다.

문서 일괄 등록
==============

여러 문서를 인덱스에 일괄 등록합니다.

요청
----

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

요청 본문
~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "샘플 페이지 1",
          "content": "페이지 1의 본문 텍스트입니다."
        },
        {
          "url": "https://example.com/page2",
          "title": "샘플 페이지 2",
          "content": "페이지 2의 본문 텍스트입니다."
        }
      ]
    }

필드 설명
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``documents``
     - 예
     - 등록할 문서의 배열. 각 문서는 필드 이름과 값의 맵으로 지정합니다. ``null`` 또는 빈 배열인 경우 오류(``status`` = ``1``)가 발생합니다.

문서 필드
~~~~~~~~~

각 문서에는 인덱스 필드를 이름과 값의 맵으로 자유롭게 지정할 수 있습니다.
최소한 ``url`` 과 ``title`` 은 지정해야 합니다(필수 필드 설정
``index.admin.required.fields`` 에 따릅니다. 기본값은 ``url,title,role,boost`` 이며,
``role`` 과 ``boost`` 는 후술하는 바와 같이 자동으로 보완되므로 실질적으로 ``url`` 과 ``title`` 이 필수입니다).

다음 필드는 생략한 경우 자동으로 보완됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 생략 시 기본값
   * - ``content_length``
     - ``title`` 과 ``content`` 의 문자 수 합계
   * - ``favorite_count``
     - ``0``
   * - ``click_count``
     - ``0``
   * - ``boost``
     - ``1.0``
   * - ``role``
     - 검색 게스트 역할(게스트 사용자용으로 설정된 검색 역할)
   * - ``last_modified``
     - 현재 시각
   * - ``timestamp``
     - 현재 시각

또한 다음 필드는 등록 시 자동 생성됩니다.

- ``id`` - 문서의 ``url`` (및 ``role``, ``virtual_host``)로부터 결정론적으로 생성되며,
  OpenSearch 상의 문서 ID(``_id``)로 사용됩니다. 응답의 ``items[].id``
  에는 이 값이 반환됩니다.
- ``doc_id`` - 등록마다 무작위 UUID가 생성되어 문서 필드로 저장됩니다.

.. note::

   ``id`` 는 ``url`` 로부터 결정론적으로 생성되므로, 동일한 ``url`` 의 문서를 다시 등록하면
   기존 문서가 업데이트됩니다(``items[].result`` 가 ``OK`` 가 됩니다).

보충 설명
~~~~~~~~~

- ``lang`` 필드에 ``"auto"`` 를 포함하면 본문에서 언어가 자동 판별됩니다.
- ``config_id`` 를 지정하면 해당 크롤링 설정의 수집 파이프라인(ingest pipeline)이
  적용됩니다.
- 썸네일 생성이 활성화된 경우(``thumbnail.crawler.enabled``), 등록 시 썸네일 생성이 시도됩니다.
- 각 필드의 값은 필드 타입 설정(``index.admin.array.fields``,
  ``index.admin.date.fields``, ``index.admin.long.fields`` 등)에 따라 검증됩니다.
  타입이 일치하지 않으면 오류(``status`` = ``1``)가 발생합니다.

응답
----

응답은 등록한 각 문서의 처리 결과를 ``items`` 배열로 반환합니다.
성공한 항목은 ``result`` 와 ``id`` 를, 실패한 항목은 ``result`` 와 ``message`` 를 포함합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "CREATED",
            "id": "0123456789abcdef"
          }
        ]
      }
    }

``status`` 가 ``0`` 인 경우 모든 문서가 정상적으로 등록되었음을 나타냅니다.
``items[].result`` 에는 신규 생성 시 ``CREATED``, 기존 문서 업데이트 시 ``OK`` 가 설정됩니다.

어느 항목에서 등록이 실패한 경우 ``status`` 는 ``9`` (FAILED)가 되며,
실패한 항목에는 ``message`` 필드가 포함됩니다(``result`` 에는 ``CONFLICT`` 나
``BAD_REQUEST`` 등의 오류 상태 이름이 설정됩니다). 성공한 항목은 그대로 ``id`` 를 반환합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 9,
        "items": [
          {
            "result": "CREATED",
            "id": "abcdef0123456789"
          },
          {
            "result": "BAD_REQUEST",
            "message": "failure reason ..."
          }
        ]
      }
    }

.. note::

   요청 자체가 잘못된 경우(``documents`` 가 미지정·비어 있음, 필수 필드 누락,
   필드 타입 불일치 등)에는 문서 등록 처리가 실행되지 않으며,
   ``status`` = ``1`` (BAD_REQUEST)과 ``message`` 를 포함한 오류 응답이 반환됩니다.
   이 경우 ``items`` 배열은 반환되지 않습니다.

응답 필드
~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``items``
     - 각 문서의 처리 결과 배열
   * - ``items[].result``
     - 처리 결과 상태 이름. 신규 생성 시 ``CREATED``, 업데이트 시 ``OK``, 실패 시 ``BAD_REQUEST`` 등의 오류 상태 이름
   * - ``items[].id``
     - 등록된 문서의 ID(성공 시만)
   * - ``items[].message``
     - 실패 이유 메시지(실패 시만)

사용 예
=======

문서 일괄 등록
--------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "샘플 페이지 1",
               "content": "페이지 1의 본문 텍스트입니다."
             }
           ]
         }'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-searchlist` - 문서 검색 및 관리 API
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/searchlist-guide` - 검색 목록 관리 가이드
