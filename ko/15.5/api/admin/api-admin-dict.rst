==========================
Dict API
==========================

개요
====

Dict API는 |Fess| 의 사전 파일을 관리하기 위한 API입니다.
동의어 사전, 매핑 사전, 보호어 사전 등의 관리를 수행할 수 있습니다.

기본 URL
=========

::

    /api/admin/dict

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
     - 사전 목록 조회
   * - GET
     - /{id}
     - 사전 내용 조회
   * - PUT
     - /{id}
     - 사전 내용 업데이트
   * - POST
     - /upload
     - 사전 파일 업로드

사전 목록 조회
============

요청
----------

::

    GET /api/admin/dict

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dicts": [
          {
            "id": "synonym",
            "name": "동의어 사전",
            "path": "/var/lib/fess/dict/synonym.txt",
            "type": "synonym",
            "updatedAt": "2025-01-29T10:00:00Z"
          },
          {
            "id": "mapping",
            "name": "매핑 사전",
            "path": "/var/lib/fess/dict/mapping.txt",
            "type": "mapping",
            "updatedAt": "2025-01-28T15:30:00Z"
          },
          {
            "id": "protwords",
            "name": "보호어 사전",
            "path": "/var/lib/fess/dict/protwords.txt",
            "type": "protwords",
            "updatedAt": "2025-01-27T12:00:00Z"
          }
        ],
        "total": 3
      }
    }

사전 내용 조회
============

요청
----------

::

    GET /api/admin/dict/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "dict": {
          "id": "synonym",
          "name": "동의어 사전",
          "path": "/var/lib/fess/dict/synonym.txt",
          "type": "synonym",
          "content": "검색,서치,리서치\nFess,페스\n전문검색,풀텍스트서치",
          "updatedAt": "2025-01-29T10:00:00Z"
        }
      }
    }

사전 내용 업데이트
============

요청
----------

::

    PUT /api/admin/dict/{id}
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "content": "검색,서치,리서치,search\nFess,페스\n전문검색,풀텍스트서치,full-text search"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``content``
     - 예
     - 사전 내용 (줄바꿈 구분)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary updated successfully"
      }
    }

사전 파일 업로드
========================

요청
----------

::

    POST /api/admin/dict/upload
    Content-Type: multipart/form-data

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: bash

    --boundary
    Content-Disposition: form-data; name="type"

    synonym
    --boundary
    Content-Disposition: form-data; name="file"; filename="synonym.txt"
    Content-Type: text/plain

    검색,서치,리서치
    Fess,페스
    --boundary--

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``type``
     - 예
     - 사전 타입 (synonym/mapping/protwords/stopwords)
   * - ``file``
     - 예
     - 사전 파일

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Dictionary uploaded successfully"
      }
    }

사전 타입
==========

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 타입
     - 설명
   * - ``synonym``
     - 동의어 사전 (검색 시 동의어 확장)
   * - ``mapping``
     - 매핑 사전 (문자 정규화)
   * - ``protwords``
     - 보호어 사전 (스테밍 대상 제외 단어)
   * - ``stopwords``
     - 스톱워드 사전 (인덱스 대상 제외 단어)
   * - ``kuromoji``
     - Kuromoji 사전 (일본어 형태소 분석)

사전 형식 예시
============

동의어 사전
----------

::

    # 쉼표로 동의어 지정
    검색,서치,리서치,search
    Fess,페스,fess
    전문검색,풀텍스트서치,full-text search

매핑 사전
--------------

::

    # 변환 전 => 변환 후
    ０ => 0
    １ => 1
    ２ => 2

보호어 사전
----------

::

    # 스테밍 처리에서 보호할 단어
    running
    searching
    indexing

사용 예
======

사전 목록 조회
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict" \
         -H "Authorization: Bearer YOUR_TOKEN"

동의어 사전 내용 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN"

동의어 사전 업데이트
----------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/dict/synonym" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "content": "검색,서치,search\nFess,페스,fess\n문서,도큐먼트,document"
         }'

사전 파일 업로드
--------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/dict/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "type=synonym" \
         -F "file=@synonym.txt"

주의 사항
========

- 사전을 업데이트한 후에는 인덱스 재구축이 필요할 수 있습니다
- 대규모 사전 파일은 검색 성능에 영향을 줄 수 있습니다
- 사전의 문자 인코딩은 UTF-8을 사용하세요

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`../../admin/dict-guide` - 사전 관리 가이드
- :doc:`../../config/dict-config` - 사전 설정 가이드
