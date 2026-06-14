==========================
Plugin API
==========================

개요
====

Plugin API는 |Fess| 의 플러그인(아티팩트)을 관리하기 위한 API입니다.
설치된 플러그인 및 설치 가능한 플러그인의 목록 조회, 플러그인 설치·삭제를 조작할 수 있습니다.

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
     - /installed
     - 설치된 플러그인 목록 조회
   * - GET
     - /available
     - 설치 가능한 플러그인 목록 조회
   * - POST
     - /
     - 플러그인 설치
   * - DELETE
     - /
     - 플러그인 삭제

설치된 플러그인 목록 조회
==================================

설치된 플러그인의 목록을 반환합니다.

요청
----------

::

    GET /api/admin/plugin/installed

응답
----------

``plugins`` 에 플러그인 정보를 나타내는 객체의 배열이 저장됩니다.
각 객체는 문자열 키와 값의 맵으로, ``name`` (플러그인 이름)이나 ``version`` (버전) 등을 포함합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

설치 가능한 플러그인 목록 조회
==================================

설치 가능한 플러그인의 목록을 반환합니다.

요청
----------

::

    GET /api/admin/plugin/available

응답
----------

``plugins`` 에 설치 가능한 플러그인 정보를 나타내는 객체의 배열이 저장됩니다.
각 객체는 ``installed`` 와 동일하게 문자열 키와 값의 맵입니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "plugins": [
          {
            "name": "fess-ds-slack",
            "version": "15.7.0"
          }
        ]
      }
    }

플러그인 설치
======================

지정한 이름과 버전의 플러그인을 설치합니다.

요청
----------

::

    POST /api/admin/plugin
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 필드
     - 필수
     - 설명
   * - ``name``
     - 예
     - 플러그인 이름 (최대 100자)
   * - ``version``
     - 예
     - 플러그인 버전 (최대 100자)

응답
----------

성공 시 ``status`` 만 반환합니다.
``name`` 또는 ``version`` 에 해당하는 아티팩트가 존재하지 않는 경우에는 ``status`` 가 ``1`` (BAD_REQUEST)이 되고, ``message`` 에 ``invalid name or version`` 이 설정됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0
      }
    }

플러그인 삭제
==============

지정한 이름과 버전의 플러그인을 삭제합니다.

요청
----------

::

    DELETE /api/admin/plugin
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "fess-ds-slack",
      "version": "15.7.0"
    }

필드 설명
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 필드
     - 필수
     - 설명
   * - ``name``
     - 예
     - 플러그인 이름 (최대 100자)
   * - ``version``
     - 아니오
     - 플러그인 버전 (최대 100자)

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

설치된 플러그인 목록 조회
------------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/plugin/installed" \
         -H "Authorization: Bearer YOUR_TOKEN"

플러그인 설치
------------------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

플러그인 삭제
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.7.0"
         }'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
