==========================
Storage API
==========================

개요
========

Storage API는 |Fess| 의 오브젝트 스토리지를 관리하기 위한 API입니다.
스토리지 내 파일·디렉터리 목록 조회, 파일 다운로드·삭제·업로드를 수행할 수 있습니다.

기본 URL
============

::

    /api/admin/storage

인증
========

Storage API를 포함한 Admin API의 모든 엔드포인트에는 액세스 토큰을 통한 인증이 필요합니다.
요청의 ``Authorization`` 헤더에 액세스 토큰을 지정합니다.

::

    Authorization: Bearer <액세스 토큰>

액세스 토큰 취득 방법 및 필요한 권한(기본값은 ``admin-api`` 역할)에 대한 자세한 내용은
:doc:`api-admin-overview` 를 참조하십시오.

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
     - 파일·디렉터리 목록 조회
   * - GET
     - /download/{id}
     - 파일 다운로드
   * - DELETE
     - /delete/{id}
     - 파일 삭제
   * - PUT
     - /upload
     - 파일 업로드

파일·디렉터리 목록 조회
==============================

지정한 디렉터리 하위의 파일 및 디렉터리 목록을 반환합니다.
``{id}`` 에는 목록 조회에서 얻은 디렉터리의 ``id`` 를 지정합니다. ``{id}`` 를 생략하면 루트 디렉터리의 목록을 조회합니다.

요청
----------

::

    GET /api/admin/storage/list/{id}

응답
----------

``items`` 에 파일·디렉터리 정보를 나타내는 오브젝트의 배열이 저장됩니다(디렉터리가 먼저, 파일이 나중 순서).
각 오브젝트는 다음 필드를 가집니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 인코딩된 식별자. 오브젝트 경로를 URL 안전 Base64로 인코딩한 문자열이며, 다운로드·삭제 시의 ``{id}`` 에 사용합니다.
   * - ``path``
     - 상위 디렉터리 경로
   * - ``name``
     - 파일명 또는 디렉터리명
   * - ``hashCode``
     - 내부 처리에서 사용되는 해시값(오브젝트의 내용을 나타내는 안정적인 값이 아닙니다)
   * - ``size``
     - 크기(바이트)
   * - ``directory``
     - 디렉터리 여부(boolean)
   * - ``lastModified``
     - 마지막 수정 일시(ISO 8601 형식. 파일인 경우에만 포함됩니다)

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
==============

스토리지 내의 파일을 다운로드합니다. ``{id}`` 에는 목록 조회에서 얻은 ``id`` 를 지정합니다.
응답은 ``application/octet-stream`` 스트림으로 반환됩니다.

요청
----------

::

    GET /api/admin/storage/download/{id}

응답
----------

파일의 바이너리 스트림(``Content-Type: application/octet-stream``).

.. note::

   이 API의 응답에는 ``Content-Disposition`` 헤더가 부여되지 않습니다.
   저장할 파일명은 클라이언트 측에서 지정하십시오(cURL의 경우 ``-o`` 옵션).

파일 삭제
==========

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
============

스토리지에 파일을 업로드합니다. ``multipart/form-data`` 형식으로 전송합니다.
업로드 대상 디렉터리는 URL 경로가 아니라 폼 필드 ``path`` 로 지정합니다.

요청
----------

::

    PUT /api/admin/storage/upload
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
     - 업로드 대상 디렉터리 경로(앞뒤 슬래시 불필요). 미지정 시 루트(버킷 바로 아래)에 저장됩니다.
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

오류
======

각 엔드포인트는 처리에 실패한 경우 ``status`` 가 0 이외의 값(검증 오류의 경우 ``1``)인 응답을 반환합니다.
응답 본문의 ``message`` 에 오류 내용이 포함됩니다. 상태값 및 HTTP 상태 코드에 대한 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

주요 오류 케이스는 다음과 같습니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 엔드포인트
     - 오류가 발생하는 주요 케이스
   * - 파일·디렉터리 목록 조회
     - 조회 건수가 상한을 초과한 경우
   * - 파일 다운로드
     - ``id`` 가 잘못된 경우, 또는 다운로드에 실패한 경우
   * - 파일 삭제
     - ``id`` 가 잘못된 경우, 또는 삭제에 실패한 경우
   * - 파일 업로드
     - ``file`` 이 지정되지 않은 경우, 또는 업로드에 실패한 경우

사용 예
========

루트 디렉터리 목록 조회
------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/list/" \
         -H "Authorization: Bearer YOUR_TOKEN"

파일 다운로드
--------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/storage/download/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o sample.txt

파일 삭제
----------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/storage/delete/c2FtcGxlLnR4dA==" \
         -H "Authorization: Bearer YOUR_TOKEN"

파일 업로드
------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/storage/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "path=subdir" \
         -F "file=@sample.txt"

참고 정보
============

- :doc:`api-admin-overview` - Admin API 개요
