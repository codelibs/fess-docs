========
API 개요
========


|Fess| 에서 제공하는 API
========================

이 문서에서는 |Fess| 가 제공하는 Web API (v2) 에 대해 설명합니다.
API를 활용하면 기존 웹 시스템이나 싱글 페이지 애플리케이션 (SPA) 등에서도 |Fess| 를 검색 서버로 사용할 수 있습니다.

.. note::

   |Fess| 15.7 에서 API 가 **v2** 로 전면 개편되었습니다. 기존의 ``/api/v1``
   JSON 검색 API 및 채팅 API 는 폐지되어 ``/api/v2`` 로 통합되었습니다.
   ``/api/v1`` 을 사용하던 클라이언트는 ``/api/v2`` 로 마이그레이션하십시오.

베이스 URL
==========

|Fess| 의 v2 API 엔드포인트는 다음 베이스 URL로 제공됩니다.

::

    http://<Server Name>/api/v2/

예를 들어, 로컬 환경에서 실행 중인 경우는 다음과 같습니다.

::

    http://localhost:8080/api/v2/

응답 엔벨로프
=============

v2 의 모든 JSON 응답은 공통 엔벨로프 구조로 반환됩니다.

::

    {
      "response": {
        "status": 0,
        ...
      }
    }

``response.status`` 는 처리 결과를 나타내며, v1 의 규약을 계승합니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: status 값

   * - 0
     - 성공
   * - 1
     - 클라이언트 오류
   * - 9
     - 시스템 오류

표: status 값

``response.status >= 1`` 인 경우와 HTTP 상태 코드가 ``400`` 이상인 경우는 항상 일치합니다.

필드 이름
---------

요청 본문, 응답 본문, SSE 이벤트 데이터를 포함한 모든 JSON 키는 ``snake_case`` 로 통일됩니다.

오류 응답
=========

오류 시에는 엔벨로프에 ``error`` 객체가 추가됩니다.

::

    {
      "response": {
        "status": 1,
        "error": {
          "code": "invalid_request",
          "message": "..."
        }
      }
    }

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: error 요소

   * - code
     - 안정적인 오류 코드 ( ``snake_case`` ). 클라이언트는 이 값을 기반으로 현지화하는 것을 권장합니다.
   * - message
     - 사람이 읽을 수 있는 오류 메시지 (영어). 표시 시에는 클라이언트 측에서 ``code`` 를 기반으로 현지화하십시오.

표: error 요소

오류 코드와 HTTP 상태 코드
--------------------------

``error.code`` 에 따라 기본 HTTP 상태 코드가 결정됩니다.

.. tabularcolumns:: |p{5cm}|p{3cm}|p{7cm}|
.. list-table:: 오류 코드 목록

   * - error.code
     - HTTP 상태
     - 설명
   * - ``invalid_request``
     - 400
     - 요청이 잘못되었습니다.
   * - ``auth_required``
     - 401
     - 인증이 필요하거나 인증 정보가 올바르지 않습니다.
   * - ``forbidden``
     - 403
     - 허가되지 않았습니다 (CSRF 토큰 누락·만료 등).
   * - ``not_found``
     - 404
     - 리소스를 찾을 수 없습니다.
   * - ``method_not_allowed``
     - 405
     - HTTP 메서드가 허용되지 않습니다. ``Allow`` 헤더에 대응 메서드가 나열됩니다.
   * - ``not_acceptable``
     - 406
     - 허용할 수 없는 요청입니다.
   * - ``conflict``
     - 409
     - 리소스 충돌이 발생했습니다.
   * - ``payload_too_large``
     - 413
     - 요청 본문이 크기 제한을 초과했습니다.
   * - ``unsupported_media_type``
     - 415
     - 지원되지 않는 ``Content-Type`` 입니다 (대부분의 엔드포인트는 ``application/json`` 을 요구합니다).
   * - ``rate_limited``
     - 429
     - 속도 제한을 초과했습니다. ``Retry-After`` 헤더에 대기해야 할 초 단위 시간이 표시됩니다.
   * - ``internal_error``
     - 500
     - 서버 내부에서 오류가 발생했습니다.
   * - ``service_unavailable``
     - 503
     - 서비스를 일시적으로 사용할 수 없습니다.

표: 오류 코드 목록

.. note::

   ``method_not_allowed`` 응답에는 대응하는 HTTP 메서드를 나열한
   ``Allow`` 헤더가 부여됩니다.

인증과 세션
===========

v2 API 는 세션 기반 인증을 채택하고 있습니다.
로그인은 ``POST /auth/login`` 으로 수행하며, 성공하면 세션이 확립되고 CSRF 토큰이 발급됩니다.
현재 인증 상태는 ``GET /auth/me`` 로 확인할 수 있습니다. 자세한 내용은 :doc:`api-auth` 를 참조하십시오.

로그인이 불필요한 검색 등의 엔드포인트는 익명으로도 사용할 수 있습니다 ( ``app.login.required`` 등의 설정에 따라 다릅니다).

CSRF 토큰
---------

상태를 변경하는 요청 ( ``POST`` / ``PUT`` / ``DELETE`` ) 에는 ``X-Fess-CSRF-Token`` 헤더가 필요합니다.
CSRF 토큰은 다음 방법으로 취득할 수 있습니다.

- ``POST /auth/login`` 응답의 ``csrf_token`` 필드
- ``GET /ui/config`` 응답 ( ``csrf_required=true`` 인 경우의 ``csrf_token`` 필드)

토큰은 로그인·로그아웃·비밀번호 변경 때마다 교체됩니다.

.. note::

   CSRF 검증은 인증보다 **먼저** 수행됩니다. 따라서 세션도 유효한
   CSRF 토큰도 없는 상태에서의 상태 변경 요청은 ``401 auth_required`` 가 아닌
   ``403 forbidden`` 을 받습니다. ``/auth/login`` 은 로그인 전에 토큰이
   존재하지 않으므로 CSRF 검증 대상에서 제외됩니다.

스트리밍 형식
=============

일부 엔드포인트는 일반적인 JSON 대신 스트리밍 형식으로 응답을 반환합니다.

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: 스트리밍 형식

   * - 엔드포인트
     - Content-Type
     - 설명
   * - ``/chat/stream``
     - ``text/event-stream``
     - Server-Sent Events (SSE). 자세한 내용은 :doc:`api-chat` 을 참조하십시오.
   * - ``/documents/all``
     - ``application/x-ndjson``
     - NDJSON (각 행이 ``{"data":{...}}`` 형식의 1개 문서. 스트림 도중에 실패한 경우에만 마지막 행이 ``{"error":{...}}`` 가 됩니다). 자세한 내용은 :doc:`api-search` 를 참조하십시오.

표: 스트리밍 형식

API 종류
========

|Fess| 는 다음 v2 API 를 제공합니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table::

   * - search
     - 문서 검색, 레이블 목록, 전체 취득 (스크롤) 을 수행하는 API.
   * - suggest
     - 자동완성 단어를 취득하는 API.
   * - popularword
     - 인기 검색어를 취득하는 API.
   * - related
     - 관련 쿼리 및 관련 콘텐츠를 취득하는 API.
   * - monitor
     - 서버 (검색 엔진 클러스터) 의 상태를 취득하는 API.
   * - auth
     - 인증·세션 조작 (로그인, 로그아웃, 인증 상태 취득, 비밀번호 변경) 을 수행하는 API.
   * - ui
     - SPA 용 초기 설정 (UI 설정) 을 취득하는 API.
   * - favorite
     - 즐겨찾기 문서를 조작하는 API.
   * - click
     - 검색 결과 클릭을 기록하는 API.
   * - cache
     - 캐시된 문서 본문을 취득하는 API.
   * - chat
     - AI 검색 모드 (RAG 채팅) 기능을 사용하는 API.

표: API 종류
