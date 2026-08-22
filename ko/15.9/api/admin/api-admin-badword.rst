==========================
BadWord API
==========================

개요
====

BadWord API는 |Fess| 의 NG 워드(부적절한 서제스트 워드 제외)를 관리하기 위한 API입니다.
서제스트 기능에서 표시하고 싶지 않은 키워드를 설정할 수 있습니다.

기본 URL
=========

::

    /api/admin/badword

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
     - NG 워드 목록 조회
   * - GET
     - /setting/{id}
     - NG 워드 조회
   * - POST
     - /setting
     - NG 워드 만들기
   * - PUT
     - /setting
     - NG 워드 업데이트
   * - DELETE
     - /setting/{id}
     - NG 워드 삭제
   * - PUT
     - /upload
     - NG 워드 CSV 업로드
   * - GET
     - /download
     - NG 워드 CSV 다운로드

NG 워드 목록 조회
================

요청
----------

::

    GET /api/admin/badword/settings

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

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
     - 페이지 번호 (1부터 시작, 기본값: 1)
   * - ``id``
     - String
     - 아니오
     - 지정한 ID의 NG 워드만으로 필터링

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "settings": [
          {
            "id": "badword_id_1",
            "suggestWord": "inappropriate_word"
          }
        ],
        "total": 5
      }
    }

NG 워드 조회
============

요청
----------

::

    GET /api/admin/badword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "badword_id_1",
          "suggestWord": "inappropriate_word"
        }
      }
    }

NG 워드 만들기
============

요청
----------

::

    POST /api/admin/badword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "suggestWord": "spam_keyword"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``suggestWord``
     - 예
     - 제외할 키워드 (공백 문자를 포함할 수 없습니다)

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_badword_id",
        "created": true
      }
    }

NG 워드 업데이트
============

요청
----------

::

    PUT /api/admin/badword/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_badword_id",
      "suggestWord": "updated_spam_keyword",
      "versionNo": 1
    }

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_badword_id",
        "created": false
      }
    }

NG 워드 삭제
============

요청
----------

::

    DELETE /api/admin/badword/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "deleted_badword_id",
        "created": false
      }
    }

NG 워드 CSV 업로드
==================

CSV 파일에서 NG 워드를 일괄 등록합니다. 파일은 ``multipart/form-data`` 로 전송합니다. 가져오기는 서버 측에서 비동기로 실행됩니다.

요청
----------

::

    PUT /api/admin/badword/upload
    Content-Type: multipart/form-data

파라미터
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 파라미터
     - 필수
     - 설명
   * - ``badWordFile``
     - 예
     - 업로드할 NG 워드 CSV 파일

CSV 형식
~~~~~~~~~~

- 1행째는 헤더 행으로 건너뜁니다 (열 이름은 임의. 다운로드 시에는 ``BadWord`` 가 출력됩니다).
- 2행째 이후로는 1행에 1개의 NG 워드를 ``suggestWord`` 로 기재합니다.
- 값이 공백뿐인 행은 무시됩니다.
- 단어 앞에 ``--`` 를 붙이면 해당 단어를 삭제합니다 (예: ``--spam`` 은 ``spam`` 을 삭제).
- 이미 등록된 단어를 지정한 경우에는 업데이트 (업데이트한 사람·업데이트 일시의 재설정)로 처리됩니다.

.. note::

   가져오기 처리는 서버 측에서 비동기로 실행되므로, 응답의 ``status: 0`` 은
   요청의 접수를 나타내는 것이며 가져오기 완료를 보장하는 것은 아닙니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

NG 워드 CSV 다운로드
====================

등록된 NG 워드를 CSV 파일(``badword.csv``)로 다운로드합니다. 응답은 ``application/octet-stream`` 스트림입니다.
CSV는 1행째에 ``BadWord`` 라는 헤더 행을 가지며, 2행째 이후로는 등록된 NG 워드가 1행에 1개씩 출력됩니다.

요청
----------

::

    GET /api/admin/badword/download

사용 예
======

스팸 키워드 제외
----------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/badword/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "suggestWord": "spam"
         }'

CSV 파일 업로드
-------------------------

.. code-block:: bash

    curl -X PUT "http://localhost:8080/api/admin/badword/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "badWordFile=@badword.csv"

CSV 파일 다운로드
-------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/badword/download" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o badword.csv

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-suggest` - 서제스트 관리 API
- :doc:`api-admin-elevateword` - 엘리베이트 워드 API
- :doc:`../../admin/badword-guide` - NG 워드 관리 가이드
