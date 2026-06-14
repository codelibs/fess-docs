==========================
Log API
==========================

개요
====

Log API는 |Fess| 의 로그 파일을 참조·다운로드하기 위한 API입니다.
서버에 출력된 로그 파일의 목록 조회와 개별 로그 파일의 다운로드를 수행할 수 있습니다.

기본 URL
=========

::

    /api/admin/log

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /files
     - 로그 파일 목록 조회
   * - GET
     - /file/{id}
     - 로그 파일 다운로드

로그 파일 목록 조회
====================

서버의 로그 출력 디렉터리에 존재하는 로그 파일(``.log`` 및 ``.log.gz``)의 목록을 반환합니다.

요청
----------

::

    GET /api/admin/log/files

응답
----------

``files`` 에 각 로그 파일의 정보를 나타내는 객체의 배열, ``total`` 에 건수가 저장됩니다.
각 객체는 다음 필드를 가집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 파일명을 Base64 URL 인코딩한 값 (다운로드 시의 ``{id}`` 에 사용)
   * - ``name``
     - 로그 파일명
   * - ``lastModified``
     - 최종 수정 일시

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "ZmVzcy5sb2c=",
            "name": "fess.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          },
          {
            "id": "ZmVzcy1jcmF3bGVyLmxvZw==",
            "name": "fess-crawler.log",
            "lastModified": "2025-01-01T00:00:00.000+00:00"
          }
        ],
        "total": 2
      }
    }

로그 파일 다운로드
==========================

지정한 로그 파일의 내용을 다운로드합니다.
``{id}`` 에는 목록 조회로 얻은 ``id`` (파일명을 Base64 인코딩한 값)를 지정합니다.
응답은 ``application/octet-stream`` 의 스트림으로 반환됩니다.
존재하지 않는 파일명이나 로그 파일로 허용되지 않는 이름을 지정한 경우에는 빈 응답이 반환됩니다.

요청
----------

::

    GET /api/admin/log/file/{id}

응답
----------

로그 파일의 바이너리 스트림(``Content-Type: application/octet-stream``).

사용 예
======

로그 파일 목록 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

로그 파일 다운로드
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/log/file/ZmVzcy5sb2c=" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess.log

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-backup` - 백업 API
