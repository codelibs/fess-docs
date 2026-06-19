==========================
AccessToken API
==========================

개요
====

AccessToken API는 |Fess| 의 API 액세스 토큰을 관리하기 위한 API입니다.
토큰의 생성, 조회, 업데이트, 삭제를 실행할 수 있습니다.

액세스 토큰은 |Fess| 의 검색 API나 Admin API를 프로그램에서 호출할 때의 인증에 사용합니다.
이 API를 포함한 Admin API의 공통 사양(인증 방법, 응답 형식, ``status`` 의 값, 오류 응답,
HTTP 상태 코드)에 대해서는 :doc:`api-admin-overview` 를 참조하십시오.

.. note::

   이 API에 접근하려면 요청에 사용하는 액세스 토큰에 ``api.admin.access.permissions``
   (기본값 ``{role}admin-api`` )에 일치하는 권한이 필요합니다.

기본 URL
=========

::

    /api/admin/accesstoken

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
     - 액세스 토큰 목록 조회
   * - GET
     - /setting/{id}
     - 액세스 토큰 조회
   * - POST
     - /setting
     - 액세스 토큰 만들기
   * - PUT
     - /setting
     - 액세스 토큰 업데이트
   * - DELETE
     - /setting/{id}
     - 액세스 토큰 삭제

액세스 토큰 목록 조회
========================

요청
----------

::

    GET /api/admin/accesstoken/settings

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
     - 페이지당 건수 (기본값: 25. ``paging.page.size`` 로 변경 가능)
   * - ``page``
     - Integer
     - 아니오
     - 페이지 번호 (1부터 시작. 기본값: 1)
   * - ``id``
     - String
     - 아니오
     - 지정한 ID의 토큰만 조회하는 필터

응답
----------

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "settings": [
          {
            "id": "token_id_1",
            "name": "API Token 1",
            "token": "abcd1234efgh5678",
            "parameterName": "permission",
            "permissions": "{role}admin-api",
            "expires": "2026-01-01T00:00:00",
            "createdBy": "admin",
            "createdTime": 1735689600000,
            "updatedBy": "admin",
            "updatedTime": 1735689600000,
            "versionNo": 1
          }
        ],
        "total": 5
      }
    }

.. note::

   각 토큰 객체에는 ``createdBy`` , ``createdTime`` , ``updatedBy`` ,
   ``updatedTime`` , ``versionNo`` 와 같은 감사 정보 및 버전 정보도 포함됩니다.
   ``createdTime`` 과 ``updatedTime`` 은 에포크 기준 밀리초(숫자)입니다.
   값이 ``null`` 인 필드는 응답에서 제외됩니다.
   ``permissions`` 는 줄 바꿈( ``\n`` ) 구분 문자열로 반환됩니다.

액세스 토큰 조회
====================

요청
----------

::

    GET /api/admin/accesstoken/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "setting": {
          "id": "token_id_1",
          "name": "API Token 1",
          "token": "abcd1234efgh5678",
          "parameterName": "permission",
          "permissions": "{role}admin-api",
          "expires": "2026-01-01T00:00:00",
          "createdBy": "admin",
          "createdTime": 1735689600000,
          "updatedBy": "admin",
          "updatedTime": 1735689600000,
          "versionNo": 1
        }
      }
    }

액세스 토큰 만들기
====================

요청
----------

::

    POST /api/admin/accesstoken/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "name": "Integration API Token",
      "permissions": "{role}admin-api",
      "expires": "2026-01-01T00:00:00"
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
     - 토큰 이름 (최대 1000자)
   * - ``permissions``
     - 아니오
     - 이 토큰에 부여할 권한. 줄 바꿈( ``\n`` ) 구분으로 여러 개를 지정할 수 있습니다 (예: ``{role}admin-api`` ). Admin API를 호출하는 토큰에는 ``api.admin.access.permissions`` (기본값 ``{role}admin-api`` )에 일치하는 권한이 필요합니다.
   * - ``parameterName``
     - 아니오
     - 추가 권한을 전달하기 위한 요청 파라미터 이름. 이 토큰으로 인증된 요청에 여기서 지정한 이름의 파라미터가 포함된 경우 해당 값이 ``permissions`` 에 추가됩니다. 생략하면 설정되지 않습니다.
   * - ``expires``
     - 아니오
     - 유효 기한. ``YYYY-MM-DDTHH:MM:SS`` 형식의 문자열로 지정합니다 (예: ``2026-01-01T00:00:00`` ). 생략하면 무기한입니다.

.. note::

   토큰 문자열( ``token`` )은 서버 측에서 자동으로 생성됩니다. 요청 본문에 ``token``
   을 지정해도 무시됩니다. 생성 응답에는 토큰 문자열이 포함되지 않으므로, 생성된
   토큰 문자열은 "액세스 토큰 조회"( ``GET /setting/{id}`` )를 통해 취득하십시오.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "new_token_id",
        "created": true
      }
    }

액세스 토큰 업데이트
====================

요청
----------

::

    PUT /api/admin/accesstoken/setting
    Content-Type: application/json

요청 본문
~~~~~~~~~~~~~~~~

.. code-block:: json

    {
      "id": "existing_token_id",
      "name": "Updated API Token",
      "permissions": "{role}admin-api\n{role}user",
      "expires": "2026-01-01T00:00:00",
      "versionNo": 1
    }

필드 설명
~~~~~~~~~~~~~~

업데이트 시에는 생성 시의 필드에 더하여 다음 필드를 사용합니다.

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - 필드
     - 필수
     - 설명
   * - ``id``
     - 예
     - 업데이트 대상 토큰 ID
   * - ``versionNo``
     - 예
     - 낙관적 잠금용 버전 번호. 사전에 조회한 토큰의 ``versionNo`` 를 지정합니다.

.. note::

   토큰 문자열( ``token`` )은 업데이트할 수 없습니다. 요청 본문에 ``token`` 을 지정해도
   무시되며 기존 값이 유지됩니다.

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "id": "existing_token_id",
        "created": false
      }
    }

액세스 토큰 삭제
====================

요청
----------

::

    DELETE /api/admin/accesstoken/setting/{id}

응답
----------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

사용 예
========

API 토큰 만들기
---------------

.. code-block:: bash

    curl -X POST "http://localhost:8080/api/admin/accesstoken/setting" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{
           "name": "Search API Token",
           "permissions": "{role}guest"
         }'

토큰을 사용한 API 호출
-----------------------------

생성한 토큰은 검색 API 등을 호출할 때의 인증에 사용합니다.

.. code-block:: bash

    # 토큰을 Authorization 헤더로 사용
    curl "http://localhost:8080/api/v2/search?q=test" \
         -H "Authorization: Bearer your_token_here"

    # 토큰을 쿼리 파라미터로 사용 ( api.access.token.request.parameter 설정 필요)
    curl "http://localhost:8080/api/v2/search?q=test&token=your_token_here"

참고 정보
==========

- :doc:`api-admin-overview` - Admin API 개요 (인증·응답 형식·오류)
- :doc:`../api-search` - 검색 API
- :doc:`../../admin/accesstoken-guide` - 액세스 토큰 관리 가이드
