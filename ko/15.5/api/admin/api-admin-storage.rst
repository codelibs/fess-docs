==========================
Storage API
==========================

개요
====

Storage API는 |Fess| 의 스토리지 관리를 위한 API입니다.
인덱스의 스토리지 사용 상황이나 최적화를 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/storage

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
     - 스토리지 정보 조회
   * - POST
     - /optimize
     - 인덱스 최적화
   * - POST
     - /flush
     - 인덱스 플러시

스토리지 정보 조회
==================

요청
----------

::

    GET /api/admin/storage

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "storage": {
          "indices": [
            {
              "name": "fess.20250129",
              "status": "open",
              "health": "green",
              "docsCount": 123456,
              "docsDeleted": 234,
              "storeSize": "5.2gb",
              "primariesStoreSize": "2.6gb",
              "shards": 5,
              "replicas": 1
            }
          ],
          "totalStoreSize": "5.2gb",
          "totalDocsCount": 123456,
          "clusterHealth": "green",
          "diskUsage": {
            "total": "107374182400",
            "available": "53687091200",
            "used": "53687091200",
            "usedPercent": 50.0
          }
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
   * - ``indices``
     - 인덱스 목록
   * - ``name``
     - 인덱스 이름
   * - ``status``
     - 인덱스 상태 (open/close)
   * - ``health``
     - 헬스 상태 (green/yellow/red)
   * - ``docsCount``
     - 문서 수
   * - ``docsDeleted``
     - 삭제된 문서 수
   * - ``storeSize``
     - 스토리지 크기
   * - ``primariesStoreSize``
     - 프라이머리 샤드 크기
   * - ``shards``
     - 샤드 수
   * - ``replicas``
     - 레플리카 수
   * - ``totalStoreSize``
     - 총 스토리지 크기
   * - ``totalDocsCount``
     - 총 문서 수
   * - ``clusterHealth``
     - 클러스터 헬스
   * - ``diskUsage``
     - 디스크 사용량

인덱스 최적화
==================

요청
----------

::

    POST /api/admin/storage/optimize
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129",
      "maxNumSegments": 1,
      "onlyExpungeDeletes": false,
      "flush": true
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``index``
     - 아니오
     - 인덱스 이름 (미지정 시 전체 인덱스)
   * - ``maxNumSegments``
     - 아니오
     - 최대 세그먼트 수 (기본값: 1)
   * - ``onlyExpungeDeletes``
     - 아니오
     - 삭제된 문서만 삭제 (기본값: false)
   * - ``flush``
     - 아니오
     - 최적화 후 플러시 (기본값: true)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index optimization started"
      }
    }

인덱스 플러시
======================

요청
----------

::

    POST /api/admin/storage/flush
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "index": "fess.20250129"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``index``
     - 아니오
     - 인덱스 이름 (미지정 시 전체 인덱스)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Index flushed successfully"
      }
    }

사용 예
======

스토리지 정보 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage" \
         -H "Authorization: Bearer YOUR_TOKEN"

전체 인덱스 최적화
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "maxNumSegments": 1,
           "flush": true
         }'

특정 인덱스 최적화
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129",
           "maxNumSegments": 1,
           "onlyExpungeDeletes": false
         }'

삭제된 문서 제거
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/optimize" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "onlyExpungeDeletes": true
         }'

인덱스 플러시
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/storage/flush" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "index": "fess.20250129"
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`../../admin/storage-guide` - 스토리지 관리 가이드
