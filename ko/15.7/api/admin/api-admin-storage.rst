==========================
Storage API
==========================

개요
====

Storage API는 |Fess| 의 오브젝트 스토리지를 관리하기 위한 API입니다.
스토리지 내 파일 및 디렉터리의 목록 조회, 파일의 다운로드, 삭제, 업로드를 조작할 수 있습니다.

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
     - /list/{id}
     - 파일 및 디렉터리 목록 조회
   * - GET
     - /download/{id}
     - 파일 다운로드
   * - DELETE
     - /delete/{id}
     - 파일 삭제
   * - PUT
     - /upload/{pathId}
     - 파일 업로드

파일 및 디렉터리 목록 조회
==============================

지정한 디렉터리 하위의 파일 및 디렉터리 목록을 반환합니다.
``{id}`` 에는 인코딩된 경로를 지정합니다. ``{id}`` 를 생략하면 루트 디렉터리의 목록을 조회합니다.

요청
----------

::

    GET /api/admin/storage/list/{id}

응답
----------

``items`` 에 파일 및 디렉터리 정보를 나타내는 객체의 배열이 저장됩니다 (디렉터리가 먼저, 파일이 나중 순서).
각 객체는 다음 필드를 가집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 인코딩된 식별자 (다운로드, 삭제 시의 ``{id}`` 에 사용)
   * - ``path``
     - 상위 경로
   * - ``name``
     - 파일 이름 또는 디렉터리 이름
   * - ``hashCode``
     - 해시 코드
   * - ``size``
     - 크기 (바이트)
   * - ``directory``
     - 디렉터리 여부 (boolean)
   * - ``lastModified``
     - 최종 수정 일시 (파일만)

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "items": [
          {
            "id": "c3ViZGly",
            "path": "/",
            "name": "subdir",
            "hashCode": 12345,
            "size": 0,
            "directory": true
          },
          {
            "id": "c2FtcGxlLnR4dA==",
            "path": "/",
            "name": "sample.txt",
            "hashCode": 67890,
            "size": 1024,
            "directory": false,
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ]
      }
    }

파일 다운로드
======================

스토리지 내의 파일을 다운로드합니다. ``{id}`` 에는 목록 조회에서 얻은 ``id`` 를 지정합니다.
응답은 ``application/octet-stream`` 의 스트림으로 반환됩니다.

요청
----------

::

    GET /api/admin/storage/download/{id}

응답
----------

파일의 바이너리 스트림 (``Content-Type: application/octet-stream``).

파일 삭제
==============

스토리지 내의 파일을 삭제합니다. ``{id}`` 에는 목록 조회에서 얻은 ``id`` 를 지정합니다.

요청
----------

::

    DELETE /api/admin/storage/delete/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

파일 업로드
======================

스토리지에 파일을 업로드합니다. ``multipart/form-data`` 형식으로 전송합니다.

요청
----------

::

    PUT /api/admin/storage/upload/{pathId}
    Content-Type: multipart/form-data

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 필드
     - 필수
     - 설명
   * - ``path``
     - 아니오
     - 업로드 대상 경로 (미지정 시 기본 위치)
   * - ``file``
     - 예
     - 업로드할 파일

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

루트 디렉터리 목록 조회
----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

파일 다운로드
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

파일 삭제
--------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

파일 업로드
----------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload/" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=/" \
         -F "file=@sample.txt"

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
