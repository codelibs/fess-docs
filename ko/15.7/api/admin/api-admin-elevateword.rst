==========================
ElevateWord API
==========================

개요
====

ElevateWord API는 |Fess| 의 엘리베이트 워드(특정 키워드에서의 검색 순위 조작)를 관리하기 위한 API입니다.
특정 검색 쿼리에 대해 특정 문서를 상위 또는 하위에 배치할 수 있습니다.

기본 URL
=========

::

    /api/admin/elevateword

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
     - 엘리베이트 워드 목록 조회
   * - GET
     - /setting/{id}
     - 엘리베이트 워드 조회
   * - POST
     - /setting
     - 엘리베이트 워드 만들기
   * - PUT
     - /setting
     - 엘리베이트 워드 업데이트
   * - DELETE
     - /setting/{id}
     - 엘리베이트 워드 삭제
   * - PUT
     - /upload
     - 엘리베이트 워드 CSV 업로드
   * - GET
     - /download
     - 엘리베이트 워드 CSV 다운로드

엘리베이트 워드 목록 조회
========================

요청
----------

::

    GET /api/admin/elevateword/settings

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15.70

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
            "id": "elevate_id_1",
            "suggestWord": "fess",
            "reading": "페스",
            "permissions": "{role}guest",
            "boost": 100.0,
            "labelTypeIds": []
          }
        ],
        "total": 5
      }
    }

엘리베이트 워드 조회
====================

요청
----------

::

    GET /api/admin/elevateword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "elevate_id_1",
          "suggestWord": "fess",
          "reading": "페스",
          "permissions": "{role}guest",
          "boost": 100.0,
          "labelTypeIds": []
        }
      }
    }

엘리베이트 워드 만들기
====================

요청
----------

::

    POST /api/admin/elevateword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "documentation",
      "reading": "도큐멘테이션",
      "permissions": "{role}guest",
      "boost": 100.0,
      "labelTypeIds": ["label1"]
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15.70

   * - 필드
     - 필수
     - 설명
   * - ``suggestWord``
     - 예
     - 엘리베이트 대상 키워드
   * - ``reading``
     - 아니오
     - 읽기 가나
   * - ``permissions``
     - 아니오
     - 접근 권한 (한 줄에 한 건씩 줄바꿈으로 구분된 문자열. 폼 초기값: 검색의 기본 표시 권한)
   * - ``boost``
     - 예
     - 부스트 값 (폼 초기값: 100.0)
   * - ``labelTypeIds``
     - 아니오
     - 대상 라벨 ID (문자열 배열)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_elevate_id",
        "created": true
      }
    }

엘리베이트 워드 업데이트
====================

요청
----------

::

    PUT /api/admin/elevateword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_elevate_id",
      "suggestWord": "documentation",
      "reading": "도큐멘테이션",
      "permissions": "{role}guest\n{role}user",
      "boost": 100.0,
      "labelTypeIds": ["label1"],
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_elevate_id",
        "created": false
      }
    }

엘리베이트 워드 삭제
====================

요청
----------

::

    DELETE /api/admin/elevateword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_elevate_id",
        "created": false
      }
    }

엘리베이트 워드 CSV 업로드
===============================

CSV 파일에서 엘리베이트 워드를 일괄 등록합니다. 파일은 ``multipart/form-data`` 로 전송합니다. 가져오기는 서버 측에서 비동기적으로 실행됩니다.

요청
----------

::

    PUT /api/admin/elevateword/upload
    Content-Type: multipart/form-data

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``elevateWordFile``
     - 예
     - 업로드할 엘리베이트 워드 CSV 파일

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

엘리베이트 워드 CSV 다운로드
===============================

등록된 엘리베이트 워드를 CSV 파일 (``elevate.csv``) 로 다운로드합니다. 응답은 ``application/octet-stream`` 스트림입니다.

요청
----------

::

    GET /api/admin/elevateword/download

사용 예
======

제품명 엘리베이트
------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "Product X",
           "boost": 100.0,
           "permissions": "{role}guest"
         }'

특정 라벨로의 엘리베이트
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/elevateword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "API reference",
           "boost": 100.0,
           "labelTypeIds": ["technical_docs"],
           "permissions": "{role}guest"
         }'

CSV 파일 업로드
-------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/elevateword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "elevateWordFile=@elevate.csv"

CSV 파일 다운로드
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/elevateword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o elevate.csv

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-keymatch` - 키 매치 API
- :doc:`api-admin-boostdoc` - 문서 부스트 API
- :doc:`../../admin/elevateword-guide` - 엘리베이트 워드 관리 가이드
