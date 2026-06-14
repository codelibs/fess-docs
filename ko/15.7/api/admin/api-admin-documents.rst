==========================
Documents API
==========================

개요
====

Documents API는 |Fess| 인덱스에 문서를 일괄 등록하기 위한 API입니다.
여러 문서를 한꺼번에 인덱스에 추가할 수 있습니다.

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
   * - PUT
     - /bulk
     - 문서 일괄 등록

문서 일괄 등록
====================

여러 문서를 인덱스에 일괄 등록합니다.

요청
----------

::

    PUT /api/admin/documents/bulk
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "documents": [
        {
          "url": "https://example.com/page1",
          "title": "サンプルページ1",
          "content": "ページ1の本文テキストです。"
        },
        {
          "url": "https://example.com/page2",
          "title": "サンプルページ2",
          "content": "ページ2の本文テキストです。"
        }
      ]
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``documents``
     - 예
     - 등록할 문서의 배열. 각 문서는 필드 이름과 값의 맵으로 지정합니다. 빈 배열은 지정할 수 없습니다.

각 문서에는 ``url`` 、 ``title`` 、 ``content`` 등의 인덱스 필드를 자유롭게 지정할 수 있습니다.
``content_length`` 、 ``favorite_count`` 、 ``click_count`` 、 ``boost`` 、 ``role`` 、 ``last_modified`` 、 ``timestamp`` 등이 생략된 경우에는 기본값이 자동으로 보완됩니다.
또한, ``doc_id`` 와 ID는 등록 시 자동 생성됩니다.

응답
----------

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

어느 한 항목에서 등록이 실패한 경우, ``status`` 는 ``9`` (FAILED)가 되며, 해당 항목에는 ``message`` 필드가 포함됩니다.

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

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``items``
     - 각 문서의 처리 결과의 배열
   * - ``items[].result``
     - 처리 결과 상태 (예: ``CREATED``)
   * - ``items[].id``
     - 등록된 문서의 ID (성공 시)
   * - ``items[].message``
     - 실패 이유 메시지 (실패 시)

사용 예
======

문서의 일괄 등록
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/documents/bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "documents": [
             {
               "url": "https://example.com/page1",
               "title": "サンプルページ1",
               "content": "ページ1の本文テキストです。"
             }
           ]
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-searchlist` - 문서 검색 및 관리 API
- :doc:`api-admin-crawlinginfo` - 크롤링 정보 API
- :doc:`../../admin/searchlist-guide` - 검색 목록 관리 가이드
