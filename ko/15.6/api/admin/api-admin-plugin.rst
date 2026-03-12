==========================
Plugin API
==========================

개요
====

Plugin API는 |Fess| 의 플러그인을 관리하기 위한 API입니다.
플러그인의 설치, 활성화, 비활성화, 삭제 등을 조작할 수 있습니다.

기본 URL
=========

::

    /api/admin/plugin

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
     - 플러그인 목록 조회
   * - POST
     - /install
     - 플러그인 설치
   * - DELETE
     - /{id}
     - 플러그인 삭제

플러그인 목록 조회
==================

요청
----------

::

    GET /api/admin/plugin

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "plugins": [
          {
            "id": "analysis-kuromoji",
            "name": "Japanese (kuromoji) Analysis Plugin",
            "version": "2.11.0",
            "description": "Japanese language analysis plugin",
            "enabled": true,
            "installed": true
          },
          {
            "id": "analysis-icu",
            "name": "ICU Analysis Plugin",
            "version": "2.11.0",
            "description": "Unicode normalization and collation",
            "enabled": true,
            "installed": true
          }
        ],
        "total": 2
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``id``
     - 플러그인 ID
   * - ``name``
     - 플러그인 이름
   * - ``version``
     - 플러그인 버전
   * - ``description``
     - 플러그인 설명
   * - ``enabled``
     - 활성화 상태
   * - ``installed``
     - 설치 상태

플러그인 설치
======================

요청
----------

::

    POST /api/admin/plugin/install
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "url": "https://example.com/plugins/my-plugin-1.0.0.zip"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 필수
     - 설명
   * - ``url``
     - 예
     - 플러그인 다운로드 URL

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin installed successfully. Restart required.",
        "pluginId": "my-plugin"
      }
    }

플러그인 삭제
==============

요청
----------

::

    DELETE /api/admin/plugin/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "message": "Plugin deleted successfully. Restart required."
      }
    }

사용 예
======

플러그인 목록 조회
--------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN"

플러그인 설치
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin/install" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "url": "https://artifacts.opensearch.org/releases/plugins/analysis-icu/2.11.0/analysis-icu-2.11.0.zip"
         }'

플러그인 삭제
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin/analysis-icu" \
         -H "Authorization: Bearer YOUR_TOKEN"

주의 사항
========

- 플러그인 설치 또는 삭제 후에는 Fess 재시작이 필요합니다
- 호환되지 않는 플러그인을 설치하면 Fess가 시작되지 않을 수 있습니다
- 플러그인 삭제는 신중하게 수행하세요. 의존 관계가 있는 경우 시스템에 영향을 줄 수 있습니다

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`../../admin/plugin-guide` - 플러그인 관리 가이드
