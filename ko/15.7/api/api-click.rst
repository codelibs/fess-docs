===============
클릭 로그 API
===============

이 문서에서는 |Fess| 의 v2 클릭 로그 API 에 대해 설명합니다.
공통 응답 엔벨로프·오류 모델·CSRF 에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

클릭 기록
=========

요청
----

==================  ====================================================
HTTP 메서드          POST
엔드포인트           ``/api/v2/click``
==================  ====================================================

검색 결과의 클릭을 검색 로그에 기록합니다.
익명 호출자 및 검색 로그 기능이 비활성화된 설치에서는 성공 응답으로 ``logged: false`` 를 반환합니다 (오류가 되지 않습니다).

상태를 변경하는 요청이므로 ``X-Fess-CSRF-Token`` 헤더가 필요합니다 ( :doc:`api-overview` 참조).

요청 본문
---------

``Content-Type: application/json`` 으로, 다음 필드를 가지는 JSON (ClickRequest) 을 전송합니다.

::

    {
      "doc_id": "a1b2c3d4e5f6",
      "query_id": "f8b1c2d3e4a5",
      "rank": 1,
      "rt": 1717142400000
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 본문

   * - ``doc_id``
     - 문서 ID (str, 필수, 패턴 ``^[A-Za-z0-9_-]+$`` ).
   * - ``query_id``
     - 검색 API 가 반환하는 ``query_id`` (str).
   * - ``rank``
     - 결과 목록 내의 1 시작 위치 (int, ``>=1`` ).
   * - ``rt``
     - 원래 검색 요청의 epoch 밀리초 (int64). 미지정 시 서버의 현재 시각이 기본값이 됩니다.

표: 요청 본문

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "ok": true,
        "logged": true
      }
    }

각 필드에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드

   * - ``ok``
     - 항상 ``true`` (bool).
   * - ``logged``
     - 검색 로그 영속화가 비활성화되거나 호출자가 익명인 경우 ``false`` (bool). 그 경우에도 ``200`` 응답을 반환합니다.

표: 응답 필드

오류 응답
---------

오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오. 이 엔드포인트가 반환하는 HTTP 상태는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청이 잘못된 경우.
   * - 403 Forbidden
     - CSRF 토큰 누락·만료 등으로 허가되지 않는 경우.
   * - 404 Not Found
     - 리소스를 찾을 수 없는 경우.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 413 Payload Too Large
     - 요청 본문이 크기 제한을 초과한 경우.
   * - 415 Unsupported Media Type
     - 지원되지 않는 ``Content-Type`` 인 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답
