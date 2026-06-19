==========================
Backup API
==========================

개요
====

Backup API는 |Fess| 의 백업 대상 데이터를 참조 및 다운로드하기 위한 API입니다.
백업 대상의 목록 조회와 개별 백업 파일 (시스템 프로퍼티, 각 인덱스의 벌크 데이터, 로그의 NDJSON 데이터)의 다운로드를 수행할 수 있습니다.

이 API는 참조 및 다운로드 (읽기 전용) 전용입니다. 백업 파일을 업로드하여 복원하는 리스토어 기능은 API에서 제공되지 않으므로, 리스토어가 필요한 경우에는 관리 화면의 시스템 정보 → 백업 에서 수행해 주십시오.

기본 URL
=========

::

    /api/admin/backup

인증
====

다른 Admin API와 마찬가지로 액세스 토큰을 통한 인증이 필요합니다. 액세스 토큰에는 ``Radmin-api`` 권한 (``api.admin.access.permissions`` 으로 설정. 기본값은 ``Radmin-api``)이 필요합니다.
요청 헤더에 액세스 토큰을 지정합니다.

::

    Authorization: Bearer <액세스 토큰>

인증 및 액세스 토큰 취득 방법의 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

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
====================

백업 대상의 목록을 반환합니다. 대상은 ``index.backup.targets`` 및 ``index.backup.log.targets`` 의 설정에 기반하며, 양쪽을 합친 목록이 반환됩니다.

요청
----

::

    GET /api/admin/backup/files

응답
----

``files`` 에 백업 대상을 나타내는 객체의 배열, ``total`` 에 건수가 저장됩니다.
각 객체는 ``id`` 와 ``name`` 을 가지며, 둘 다 대상 이름 (``fess_config.bulk``, ``system.properties``, ``search_log.ndjson`` 등)이 설정됩니다.

다음은 기본 설정 (``index.backup.targets`` 와 ``index.backup.log.targets`` 가 기본값)인 경우의 예입니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "files": [
          { "id": "fess_basic_config.bulk", "name": "fess_basic_config.bulk" },
          { "id": "fess_config.bulk", "name": "fess_config.bulk" },
          { "id": "fess_user.bulk", "name": "fess_user.bulk" },
          { "id": "system.properties", "name": "system.properties" },
          { "id": "fess.json", "name": "fess.json" },
          { "id": "doc.json", "name": "doc.json" },
          { "id": "click_log.ndjson", "name": "click_log.ndjson" },
          { "id": "favorite_log.ndjson", "name": "favorite_log.ndjson" },
          { "id": "search_log.ndjson", "name": "search_log.ndjson" },
          { "id": "user_info.ndjson", "name": "user_info.ndjson" }
        ],
        "total": 10
      }
    }

.. note::

   ``version`` 에는 실행 중인 |Fess| 의 제품 버전이 설정됩니다. ``files`` 의 내용은
   ``index.backup.targets`` / ``index.backup.log.targets`` 의 설정에 따라 달라지므로,
   위의 내용은 기본값에서의 예시입니다.

백업 파일 다운로드
==================

지정한 백업 파일의 내용을 다운로드합니다. ``{id}`` 에는 목록 조회에서 얻은 ``id`` (대상 이름)를 지정합니다.
``{id}`` 의 종류에 따라 응답 내용이 다음과 같이 전환됩니다.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ID
     - 내용
   * - ``system.properties``
     - 시스템 프로퍼티의 내용 (``application/octet-stream``)
   * - ``*.bulk`` 또는 확장자 없는 인덱스 이름
     - 대상 이름과 동일한 인덱스를 스크롤하여 생성한 벌크 데이터 (``application/octet-stream``). ``.bulk`` 를 제거한 이름을 인덱스 이름으로 처리합니다.
   * - ``*.ndjson`` (``search_log`` / ``user_info`` / ``click_log`` / ``favorite_log``)
     - 대응하는 로그의 NDJSON 데이터 (``application/x-ndjson``)

.. note::

   ``fess.json`` 과 ``doc.json`` 은 인덱스의 매핑 정의 (스키마) 파일입니다.
   백업 대상 목록 (``/files``) 에는 포함되지만, 이 API의 다운로드에서는 ``.bulk`` 와 마찬가지로
   인덱스 스크롤 처리로 취급됩니다. 매핑 정의를 포함한 백업/
   리스토어는 관리 화면의 시스템 정보 → 백업 을 이용해 주십시오.

백업 대상에 존재하지 않는 ``{id}`` 를 지정한 경우에는, ``status`` 에 0 이외의 값과 오류 메시지 (``Could not find any backup index.``)를 포함한 오류 응답이 반환됩니다.

요청
----

::

    GET /api/admin/backup/file/{id}

응답
----

백업 파일의 스트림. NDJSON 형식인 경우 ``Content-Type: application/x-ndjson``, 그 외에는 ``application/octet-stream`` 으로 반환됩니다.

.. note::

   로그 (``*.ndjson``) 의 내보내기는 ``index.backup.log.load.timeout`` (기본값 ``60000`` 밀리초)
   의 제약을 받습니다. 출력에 시간이 걸리는 경우 로그 데이터가 도중에 잘릴 수 있습니다.

사용 예
=======

백업 대상 목록 조회
-------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/files" \
         -H "Authorization: Bearer YOUR_TOKEN"

설정 인덱스 다운로드
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/fess_config.bulk" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o fess_config.bulk

검색 로그 다운로드
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/backup/file/search_log.ndjson" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -o search_log.ndjson

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-log` - 로그 API
