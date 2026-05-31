==================
인증·세션 API
==================

개요
====

v2 API 는 세션 기반 인증을 채택하고 있습니다.
로그인은 ``POST /auth/login`` 으로 수행하며, 성공하면 세션이 확립되고 CSRF 토큰이 발급됩니다.

상태를 변경하는 요청 ( ``POST`` ) 에는 ``X-Fess-CSRF-Token`` 헤더가 필요합니다.
CSRF 토큰 취득 방법 및 교체 메커니즘, 공통 응답 엔벨로프 및 오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

이 페이지에서는 다음 4개의 엔드포인트를 설명합니다.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: 엔드포인트 목록
   :header-rows: 1
   :widths: 25 15 60

   * - 엔드포인트
     - 메서드
     - 설명
   * - ``/auth/me``
     - GET
     - 현재 인증된 사용자를 취득합니다.
   * - ``/auth/login``
     - POST
     - 사용자 이름과 비밀번호로 로그인합니다.
   * - ``/auth/logout``
     - POST
     - 로그아웃합니다 (멱등).
   * - ``/auth/password``
     - POST
     - 현재 사용자의 비밀번호를 변경합니다.

.. _api-auth-userpayload:

공통 사용자 정보 (UserPayload)
==============================

``GET /auth/me`` 및 ``POST /auth/login`` 응답에 포함되는 사용자 정보는 공통 ``UserPayload`` 구조로 반환됩니다.
모든 배열 필드는 non-null 이며, 값이 없는 경우 빈 배열이 반환됩니다.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 타입
     - 설명
   * - ``user_id``
     - string
     - 사용자 ID. (필수)
   * - ``username``
     - string
     - SPA 계정 메뉴용 표시 사용자 이름. 현재는 ``user_id`` 와 동일한 값이지만, 향후 백엔드가 독립적으로 제공될 가능성이 있습니다. (필수)
   * - ``name``
     - string
     - SPA 계정 메뉴용 표시 이름. 현재는 ``user_id`` 와 동일한 값입니다. (필수)
   * - ``roles``
     - string[]
     - 사용자 역할 배열. (필수)
   * - ``groups``
     - string[]
     - 사용자 그룹 배열. (필수)
   * - ``permissions``
     - string[]
     - 사용자 권한 배열. (필수)
   * - ``editable``
     - boolean
     - 사용자 정보를 편집할 수 있는지 여부. (필수)
   * - ``admin``
     - boolean
     - 사용자가 설정된 ``authentication.admin.roles`` 중 하나를 가질 때 ``true`` 가 됩니다. SPA 의 "Administration" 항목 표시를 제어합니다. (필수)

인증 상태 취득
==============

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/auth/me``
==================  ====================================================

현재 인증된 사용자를 취득합니다.
익명 호출에 대해서는 오류가 되지 않으며, ``authenticated: false`` 를 반환합니다.
인증된 경우 ``user`` 가 :ref:`UserPayload <api-auth-userpayload>` 를 가집니다.

응답
----

성공 시 (HTTP 200) 에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다 (인증된 예).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "authenticated": true,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        }
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 응답 정보
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 타입
     - 설명
   * - ``authenticated``
     - boolean
     - 인증되었는지 여부. (필수)
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>` . ``authenticated`` 가 ``true`` 인 경우에만 존재합니다.

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답
   :header-rows: 1
   :widths: 25 75

   * - 상태 코드
     - 설명
   * - 405 Method Not Allowed
     - 지원되지 않는 HTTP 메서드가 지정된 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

로그인
======

요청
----

==================  ====================================================
HTTP 메서드          POST
엔드포인트           ``/api/v2/auth/login``
==================  ====================================================

사용자 이름과 비밀번호로 로그인합니다.
로그인 성공 시에는 서블릿의 세션 ID 가 교체되고, 새 CSRF 토큰이 발급되며, 호출 원 IP 와 대상 사용자의 속도 제한 버킷이 초기화됩니다.
속도 제한을 초과한 경우 ``Retry-After`` 헤더 (초) 가 부여됩니다.

이미 인증된 세션에서도 단락 없이, 전달된 자격증명은 항상 검증됩니다.

``return_to`` 는 ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$`` 에 일치하는 상대 경로여야 합니다.
또한 프로토콜 상대 (선두 ``//`` ) 경로나 ASCII 제어 문자를 포함하는 경로는 거부되어, 에코되는 응답에서 자동으로 제거됩니다.

.. note::

   이 엔드포인트는 **CSRF 대상 외** 입니다 (로그인 전에 토큰이 존재하지 않으므로).

.. note::

   다른 상태 변경 엔드포인트와 달리, 이 엔드포인트는 과도한 요청 본문이나 비지원 ``Content-Type`` 을 ``400 invalid_request`` 로 통합합니다 (다른 엔드포인트는 ``413`` / ``415`` 를 반환합니다).

요청 본문 (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type 은 ``application/json`` 입니다.

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``username``
     - string
     - 예
     - 사용자 이름. ``minLength`` 는 1입니다.
   * - ``password``
     - string
     - 예
     - 비밀번호. ``minLength`` 는 1입니다.
   * - ``return_to``
     - string
     - 아니오
     - 로그인 후 리다이렉트 대상. 위 패턴에 일치하는 상대 경로여야 합니다.

요청 예:

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

응답
----

성공 시 (HTTP 200, LoginResponse) 에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 응답 정보
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 타입
     - 설명
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>` .
   * - ``csrf_token``
     - string
     - 새 세션에 연결된 새 CSRF 토큰. (필수)
   * - ``return_to``
     - string
     - 요청 값이 허용 목록을 통과한 경우에만 에코됩니다.

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답
   :header-rows: 1
   :widths: 25 75

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청이 잘못된 경우 (과도한 요청 본문이나 비지원 ``Content-Type`` 포함).
   * - 401 Unauthorized
     - 자격증명이 올바르지 않은 경우.
   * - 405 Method Not Allowed
     - 지원되지 않는 HTTP 메서드가 지정된 경우.
   * - 429 Too Many Requests
     - 속도 제한을 초과한 경우. ``Retry-After`` 헤더에 대기해야 할 초 단위 시간이 표시됩니다.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

로그아웃
========

요청
----

==================  ====================================================
HTTP 메서드          POST
엔드포인트           ``/api/v2/auth/logout``
==================  ====================================================

로그아웃합니다. 이 조작은 멱등이며, 활성 세션이 없어도 no-op 로 오류가 되지 않습니다. 항상 ``ok: true`` 를 반환합니다.

``X-Fess-CSRF-Token`` 헤더가 필요합니다.

응답
----

성공 시 (HTTP 200, OkResponse) 에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 응답 정보
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 타입
     - 설명
   * - ``ok``
     - boolean
     - 항상 ``true`` 입니다. (필수)

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답
   :header-rows: 1
   :widths: 25 75

   * - 상태 코드
     - 설명
   * - 403 Forbidden
     - CSRF 토큰이 누락·만료된 경우.
   * - 405 Method Not Allowed
     - POST 이외의 메서드가 지정된 경우. ``Allow: POST`` 헤더가 부여됩니다.

비밀번호 변경
=============

요청
----

==================  ====================================================
HTTP 메서드          POST
엔드포인트           ``/api/v2/auth/password``
==================  ====================================================

현재 사용자의 비밀번호를 변경합니다.
``current_password`` 를 검증하고, ``new_password`` 에 설정된 비밀번호 정책을 적용하며, 현재 세션을 무효화하고, ``re_login_required: true`` 로 SPA 에 로그인 페이지로의 리다이렉트를 촉구합니다.

세션이 서버 측에서 파기되므로 ``csrf_token`` 은 반환되지 않습니다. SPA 는 재인증 후 새 토큰을 취득해야 합니다.

``X-Fess-CSRF-Token`` 헤더가 필요합니다.

요청 본문 (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type 은 ``application/json`` 입니다.

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - 필드
     - 타입
     - 필수
     - 설명
   * - ``current_password``
     - string
     - 예
     - 현재 비밀번호. ``minLength`` 는 1입니다.
   * - ``new_password``
     - string
     - 예
     - 새 비밀번호. 설정된 비밀번호 정책을 충족해야 합니다. ``minLength`` 는 1입니다.
   * - ``confirm_password``
     - string
     - 예
     - 확인용 비밀번호. ``new_password`` 와 일치해야 합니다. ``minLength`` 는 1입니다.

응답
----

성공 시 (HTTP 200) 에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다.

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 응답 정보
   :header-rows: 1
   :widths: 25 15 60

   * - 필드
     - 타입
     - 설명
   * - ``ok``
     - boolean
     - 항상 ``true`` 입니다. (필수)
   * - ``re_login_required``
     - boolean
     - 항상 ``true`` 입니다. 현재 세션은 서버 측에서 무효화되었습니다. SPA 는 로그인 페이지로 리다이렉트하여 새 세션과 CSRF 토큰을 취득해야 합니다. (필수)

오류 응답
---------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답
   :header-rows: 1
   :widths: 25 75

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청이 잘못된 경우.
   * - 401 Unauthorized
     - 인증이 필요하거나 ``current_password`` 가 올바르지 않은 경우.
   * - 403 Forbidden
     - CSRF 토큰이 누락·만료된 경우.
   * - 405 Method Not Allowed
     - 지원되지 않는 HTTP 메서드가 지정된 경우.
   * - 413 Payload Too Large
     - 요청 본문이 크기 제한을 초과한 경우.
   * - 415 Unsupported Media Type
     - 지원되지 않는 ``Content-Type`` 인 경우.
   * - 429 Too Many Requests
     - 속도 제한을 초과한 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.
