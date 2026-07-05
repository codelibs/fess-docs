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

플러그인 정보 필드
==========================

목록 조회 계열 엔드포인트(``/installed`` 및 ``/available``)가 반환하는 ``plugins``
배열의 각 요소는 다음 필드를 가진 객체입니다.

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 필드
     - 설명
   * - ``type``
     - 아티팩트의 종별 ID. ``fess-ds`` (데이터 스토어), ``fess-theme`` (테마),
       ``fess-ingest`` (Ingest), ``fess-script`` (스크립트), ``fess-webapp`` (웹 앱),
       ``fess-thumbnail`` (썸네일), ``fess-crawler`` (크롤러), ``fess-llm`` (LLM),
       ``jar`` (위 이외의 범용 JAR) 중 하나입니다.
   * - ``id``
     - ``{name}:{version}`` 형식의 식별자.
   * - ``name``
     - 플러그인 이름.
   * - ``version``
     - 플러그인 버전.
   * - ``url``
     - 다운로드 원본 URL. ``/available`` 응답에만 포함됩니다. ``/installed`` 에서는
       값이 존재하지 않으므로 필드 자체가 생략됩니다.

.. note::

   |Fess| 의 API 응답에서는 값이 ``null`` 인 필드는 출력되지 않습니다. 따라서
   설치된 플러그인의 각 요소에는 ``url`` 이 포함되지 않습니다.

설치된 플러그인 목록 조회
==================================

설치된 플러그인의 목록을 반환합니다. 플러그인 디렉터리의 아티팩트를
종별로 탐색하여 이름 순으로 정렬하여 반환합니다.

요청
----------

::

    GET /api/admin/plugin/installed

응답
----------

``plugins`` 에 플러그인 정보를 나타내는 객체의 배열이 저장됩니다.
각 객체의 필드는 `플러그인 정보 필드`_ 를 참조하십시오.
설치된 플러그인에서는 ``url`` 은 출력되지 않습니다.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.8.0",
            "name": "fess-ds-slack",
            "version": "15.8.0"
          }
        ]
      }
    }

설치 가능한 플러그인 목록 조회
==================================

설치 가능한 플러그인의 목록을 반환합니다. ``fess_config.properties`` 의
``plugin.repositories`` 에 설정된 리포지터리에서 전체 종별 아티팩트를 가져옵니다.
가져온 결과는 일정 시간(기본값 5분) 캐시됩니다.

요청
----------

::

    GET /api/admin/plugin/available

응답
----------

``plugins`` 에 설치 가능한 플러그인 정보를 나타내는 객체의 배열이 저장됩니다.
각 객체의 필드는 `플러그인 정보 필드`_ 를 참조하십시오.
설치 가능한 플러그인에서는 다운로드 원본 ``url`` 이 포함됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "plugins": [
          {
            "type": "fess-ds",
            "id": "fess-ds-slack:15.8.0",
            "name": "fess-ds-slack",
            "version": "15.8.0",
            "url": "https://repo1.maven.org/maven2/org/codelibs/fess/fess-ds-slack/15.8.0/fess-ds-slack-15.8.0.jar"
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
      "version": "15.8.0"
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

.. note::

   ``name`` 과 ``version`` 은 ``/available`` 로 조회할 수 있는 설치 가능한 플러그인 중
   하나와 일치해야 합니다. 일치하는 아티팩트가 존재하지 않는 경우 오류가 됩니다.

응답
----------

요청이 수락되면 ``status`` 가 ``0`` (OK)인 응답을 반환합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

``name`` 또는 ``version`` 에 해당하는 아티팩트가 존재하지 않는 경우에는 ``status`` 가
``1`` (BAD_REQUEST)이 되고, ``message`` 에 ``invalid name or version`` 이 설정됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 1,
        "message": "invalid name or version"
      }
    }

.. note::

   설치 처리는 백그라운드에서 비동기로 실행됩니다. ``status: 0`` 응답은
   요청이 수락되었음을 나타내는 것이며, 설치 완료를 보장하지는 않습니다.
   설치 완료 후 동일한 이름으로 다른 버전의 플러그인이 설치되어 있는 경우에는
   해당 플러그인이 자동으로 삭제됩니다. 다운로드나 설치에 실패한 경우에는
   서버 로그에 기록되지만 API 응답에는 반영되지 않습니다.

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
      "version": "15.8.0"
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
     - 플러그인 버전 (최대 100자). 삭제 대상을 고유하게 특정하기 위해 지정하는 것을 권장합니다.

응답
----------

요청이 수락되면 ``status`` 가 ``0`` (OK)인 응답을 반환합니다.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0
      }
    }

.. note::

   삭제 처리는 백그라운드에서 비동기로 실행됩니다. ``status: 0`` 응답은
   요청이 수락되었음을 나타내는 것으로, 해당 플러그인이 존재하는지 또는 삭제가
   성공했는지는 판정하지 않습니다. 삭제에 실패한 경우(대상 파일이 존재하지 않는 경우 등)에는
   서버 로그에 기록되지만 API 응답에는 반영되지 않습니다.

사용 예
========

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
           "version": "15.8.0"
         }'

플러그인 삭제
----------------

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/plugin" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "fess-ds-slack",
           "version": "15.8.0"
         }'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
