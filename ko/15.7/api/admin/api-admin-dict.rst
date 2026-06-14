==========================
Dict API
==========================

개요
====

Dict API는 |Fess| 의 사전을 관리하기 위한 API입니다.
루트 엔드포인트에서 사용 가능한 사전 목록을 조회할 수 있습니다.
개별 사전 항목의 참조, 생성, 업데이트, 삭제 및 사전 파일의 업로드, 다운로드는
사전 종류별 서브 엔드포인트(synonym、kuromoji、mapping、protwords、stopwords、stemmerOverride)에서 조작합니다.

기본 URL
=========

::

    /api/admin/dict

엔드포인트 목록
==================

사전 루트
----------

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /
     - 사전 목록 조회

사전 종류별 엔드포인트
----------------------

``{type}`` 에는 ``synonym`` 、 ``kuromoji`` 、 ``mapping`` 、 ``protwords`` 、 ``stopwords`` 、 ``stemmerOverride`` 중 하나를 지정합니다.
``{dictId}`` 는 사전 목록 조회에서 얻은 사전의 ID입니다.

.. list-table::
   :header-rows: 1
   :widths: 15 50 35

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /{type}/settings/{dictId}
     - 사전 항목 목록 조회
   * - GET
     - /{type}/setting/{dictId}/{id}
     - 사전 항목 조회
   * - POST
     - /{type}/setting/{dictId}
     - 사전 항목 생성
   * - PUT
     - /{type}/setting/{dictId}
     - 사전 항목 업데이트
   * - DELETE
     - /{type}/setting/{dictId}/{id}
     - 사전 항목 삭제
   * - PUT
     - /{type}/upload/{dictId}
     - 사전 파일 업로드
   * - GET
     - /{type}/download/{dictId}
     - 사전 파일 다운로드

사전 목록 조회
============

사용 가능한 사전 파일의 목록을 조회합니다.

요청
----------

::

    GET /api/admin/dict

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "ZjA5...synonym.txt",
            "type": "synonym",
            "path": "/var/lib/fess/dict/synonym.txt",
            "timestamp": "2025-01-29T10:00:00.000+0000"
          },
          {
            "id": "ZjA5...mapping.txt",
            "type": "mapping",
            "path": "/var/lib/fess/dict/mapping.txt",
            "timestamp": "2025-01-28T15:30:00.000+0000"
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
   * - ``settings[].id``
     - 사전 ID (개별 사전 조작 시 ``{dictId}`` 로 사용)
   * - ``settings[].type``
     - 사전 종류
   * - ``settings[].path``
     - 사전 파일의 경로
   * - ``settings[].timestamp``
     - 사전 파일의 업데이트 일시

사전 항목 목록 조회
================

지정한 사전 내의 항목을 목록으로 조회합니다.

요청
----------

::

    GET /api/admin/dict/{type}/settings/{dictId}

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``dictId``
     - String
     - 예
     - 사전 ID (경로 파라미터)
   * - ``size``
     - Integer
     - 아니오
     - 페이지당 건수
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호

응답
----------

응답의 ``settings`` 배열의 각 항목의 필드는 사전 종류에 따라 다릅니다(후술하는 "사전 종류별 항목 필드" 참조).

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": 1,
            "dictId": "ZjA5...synonym.txt",
            "inputs": "検索,サーチ",
            "outputs": "検索,サーチ,リサーチ"
          }
        ]
      }
    }

사전 항목 조회
============

사전 내의 특정 항목을 조회합니다.

요청
----------

::

    GET /api/admin/dict/{type}/setting/{dictId}/{id}

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``dictId``
     - String
     - 예
     - 사전 ID (경로 파라미터)
   * - ``id``
     - Long
     - 예
     - 항목 ID (경로 파라미터)

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "setting": {
          "id": 1,
          "dictId": "ZjA5...synonym.txt",
          "inputs": "検索,サーチ",
          "outputs": "検索,サーチ,リサーチ"
        }
      }
    }

사전 항목 생성
============

사전에 새로운 항목을 생성합니다.

요청
----------

::

    POST /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

요청 본문 (synonym 예시)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ"
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": true
      }
    }

사전 항목 업데이트
============

사전 내의 기존 항목을 업데이트합니다.

요청
----------

::

    PUT /api/admin/dict/{type}/setting/{dictId}
    Content-Type: application/json

요청 본문 (synonym 예시)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": 1,
      "inputs": "検索,サーチ",
      "outputs": "検索,サーチ,リサーチ,search"
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

사전 항목 삭제
============

사전 내의 항목을 삭제합니다.

요청
----------

::

    DELETE /api/admin/dict/{type}/setting/{dictId}/{id}

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - 파라미터
     - 타입
     - 필수
     - 설명
   * - ``dictId``
     - String
     - 예
     - 사전 ID (경로 파라미터)
   * - ``id``
     - Long
     - 예
     - 항목 ID (경로 파라미터)

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "id": "1",
        "created": false
      }
    }

사전 파일 업로드
========================

사전 파일 전체를 업로드하여 교체합니다.

요청
----------

::

    PUT /api/admin/dict/{type}/upload/{dictId}
    Content-Type: multipart/form-data

파일 필드의 이름은 사전 종류별로 다릅니다(후술하는 "사전 종류별 항목 필드" 참조).

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

사전 파일 다운로드
========================

사전 파일을 다운로드합니다.

요청
----------

::

    GET /api/admin/dict/{type}/download/{dictId}

응답은 사전 파일의 바이너리( ``application/octet-stream`` )입니다.

사전 종류별 항목 필드
============================

사전 항목의 생성, 업데이트 요청 본문 및 응답의 필드는 사전 종류별로 다릅니다.
``id`` (항목 ID)와 ``dictId`` (사전 ID)는 응답에 공통으로 포함됩니다.

.. list-table::
   :header-rows: 1
   :widths: 18 42 40

   * - 종류
     - 항목 필드
     - 업로드 파일 필드
   * - ``synonym``
     - ``inputs`` (필수)、 ``outputs`` (필수)
     - ``synonymFile``
   * - ``kuromoji``
     - ``token`` (필수)、 ``segmentation`` (필수)、 ``reading`` (필수)、 ``pos`` (필수)
     - ``kuromojiFile``
   * - ``mapping``
     - ``inputs`` (필수)、 ``output``
     - ``charMappingFile``
   * - ``protwords``
     - ``input`` (필수)
     - ``protwordsFile``
   * - ``stopwords``
     - ``input`` (필수)
     - ``stopwordsFile``
   * - ``stemmerOverride``
     - ``input`` (필수)、 ``output`` (필수)
     - ``stemmerOverrideFile``

사용 예
======

사전 목록 조회
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

동의어 사전 항목 목록 조회
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/settings/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN"

동의어 사전에 항목 추가
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/synonym/setting/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "inputs": "検索,サーチ",
           "outputs": "検索,サーチ,リサーチ"
         }'

동의어 사전 파일 업로드
--------------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym/upload/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "synonymFile=@synonym.txt"

동의어 사전 파일 다운로드
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym/download/{dictId}" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o synonym.txt

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../../admin/dict-guide` - 사전 관리 가이드
