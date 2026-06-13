==========================
Backup API
==========================

개요
====

Backup API는 |Fess| 의 백업 대상 데이터를 참조 및 다운로드하기 위한 API입니다.
백업 대상의 목록 조회와 개별 백업 파일 (시스템 프로퍼티, 각 인덱스의 벌크 데이터, 로그의 NDJSON 데이터)의 다운로드를 수행할 수 있습니다.

기본 URL
=========

::

    /api/admin/backup

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
     - 백업 대상 목록 조회
   * - GET
     - /file/{id}
     - 백업 파일 다운로드

백업 대상 목록 조회
========================

백업 대상의 목록을 반환합니다. 대상은 ``index.backup.targets`` 및 ``index.backup.log.targets`` 의 설정에 기반합니다.

요청
----------

::

    GET /api/admin/backup/files

응답
----------

``files`` 에 백업 대상을 나타내는 객체의 배열, ``total`` 에 건수가 저장됩니다.
각 객체는 ``id`` 와 ``name`` 을 가지며, 둘 다 대상 이름 (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson`` 등)이 설정됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          {
            "id": "fess_config.bulk",
            "name": "fess_config.bulk"
          },
          {
            "id": "system.properties",
            "name": "system.properties"
          },
          {
            "id": "search_log.ndjson",
            "name": "search_log.ndjson"
          }
        ],
        "total": 3
      }
    }

백업 파일 다운로드
==================================

지정한 백업 파일의 내용을 다운로드합니다. ``{id}`` 에는 목록 조회에서 얻은 ``id`` (대상 이름)를 지정합니다.
``{id}`` 의 종류에 따라 응답 내용이 다음과 같이 전환됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - 내용
   * - ``system.properties``
     - 시스템 프로퍼티의 내용
   * - ``*.bulk`` 또는 ``.bulk`` 확장자 없는 인덱스 이름
     - 대상 인덱스를 스크롤하여 생성한 벌크 데이터
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - 대응하는 로그의 NDJSON 데이터

백업 대상에 존재하지 않는 ``{id}`` 를 지정한 경우 오류가 발생합니다.

요청
----------

::

    GET /api/admin/backup/file/{id}

응답
----------

백업 파일의 스트림. NDJSON 형식인 경우 ``Content-Type: application/x-ndjson``, 그 외에는 ``application/octet-stream`` 으로 반환됩니다.

사용 예
======

백업 대상 목록 조회
--------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

설정 인덱스 다운로드
------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

검색 로그 다운로드
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-log` - 로그 API
