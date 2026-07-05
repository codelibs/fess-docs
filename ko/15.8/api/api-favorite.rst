===============
즐겨찾기 API
===============

이 문서에서는 |Fess| 의 v2 즐겨찾기 API 에 대해 설명합니다.
공통 응답 엔벨로프·오류 모델·CSRF 에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

.. note::

   즐겨찾기 기능을 사용하려면 ``user.favorite`` 설정이 활성화되어 있어야 합니다 (기본값은 비활성화).

즐겨찾기 문서 목록 취득
=======================

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/favorites``
==================  ====================================================

``query_id`` 로 식별되는 검색 결과 중 호출 사용자가 과거에 즐겨찾기 등록한 문서의 ID 를 반환합니다.
``query_id`` 는 검색 API ( ``/search`` ) 가 반환하는 불투명한 식별자 ( ``query_id`` 필드) 입니다.

익명 호출자 (세션에 연결된 사용자 코드가 없는 경우) 는 ``auth_required`` (401) 가 됩니다.
``user.favorite`` 기능이 비활성화된 경우 ``invalid_request`` (400) 가 됩니다.
``query_id`` 가 세션 내 캐시된 결과 세트에 일치하지 않는 경우 ``200`` 과 빈 ``data`` 배열을 반환합니다.

요청 파라미터
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``query_id``
     - 검색 API ( ``/search`` ) 가 반환하는 불투명한 ``query_id`` (query, 필수, str).

표: 요청 파라미터

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "data": [
          { "doc_id": "a1b2c3d4e5f6" },
          { "doc_id": "f6e5d4c3b2a1" }
        ]
      }
    }

각 필드에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드

   * - ``record_count``
     - ``data`` 내의 즐겨찾기 문서 수 (int).
   * - ``data``
     - 쿼리 대상 결과 세트 중 즐겨찾기 문서를 검색 결과 순서를 유지하며 반환하는 배열. 각 요소는 ``{doc_id}`` .

표: 응답 필드

오류 응답
---------

오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오. 이 엔드포인트가 반환하는 HTTP 상태는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청이 잘못된 경우 ( ``user.favorite`` 기능이 비활성화된 경우 포함).
   * - 401 Unauthorized
     - 인증이 필요한 경우 (익명 호출자).
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답

즐겨찾기 상태 취득
==================

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

지정한 문서의 즐겨찾기 상태를 취득합니다.

익명 (미인증) 호출자도 이 엔드포인트를 이용할 수 있습니다. 이 경우 ``favorite`` 는 ``false`` 를 반환하지만, ``count`` 에는 저장된 즐겨찾기 수가 그대로 반환됩니다 (이 때문에 이 엔드포인트는 ``401`` 을 반환하지 않습니다).

즐겨찾기 기능 (``user.favorite``) 이 비활성화된 경우 엔드포인트는 ``invalid_request`` (400) 로 응답합니다.

요청 파라미터
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``docId``
     - 문서 식별자 (path, 필수, 패턴 ``^[A-Za-z0-9_-]+$`` ).

표: 요청 파라미터

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "favorite": true,
        "count": 5
      }
    }

각 필드에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드

   * - ``doc_id``
     - 문서 ID (str).
   * - ``favorite``
     - 호출 사용자의 즐겨찾기 여부 (bool).
   * - ``count``
     - 이 문서의 즐겨찾기 수 (int64).

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
   * - 404 Not Found
     - 리소스를 찾을 수 없는 경우.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답

즐겨찾기 등록
=============

요청
----

==================  ====================================================
HTTP 메서드          POST
엔드포인트           ``/api/v2/documents/{docId}/favorite``
==================  ====================================================

지정한 문서를 즐겨찾기에 등록합니다.
상태를 변경하는 요청이므로 ``X-Fess-CSRF-Token`` 헤더가 필요합니다 ( :doc:`api-overview` 참조). 또한 호출 사용자가 인증되어 있어야 합니다. 익명 호출자는 ``auth_required`` (401) 가 됩니다.

``query_id`` 는 대상 문서가 직근 검색 결과에 포함되어 있는지 확인하기 위해 사용됩니다. ``query_id`` 가 세션 내 캐시된 결과 세트에 일치하지 않는 경우 ``invalid_request`` (400) 로, ``docId`` 가 해당 결과 세트에 포함되지 않는 경우 ``not_found`` (404) 로 응답합니다.

요청 파라미터
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``docId``
     - 문서 식별자 (path, 필수, 패턴 ``^[A-Za-z0-9_-]+$`` ).

표: 요청 파라미터

요청 본문
---------

``Content-Type: application/json`` (문자 인코딩 UTF-8) 으로, 다음 필드를 가지는 JSON (FavoritePostRequest) 을 전송합니다. 요청 본문의 최대 크기는 1 KiB (1024 바이트) 입니다. 이를 초과하는 경우 ``payload_too_large`` (413) 가 됩니다.

::

    {
      "query_id": "f8b1c2d3e4a5"
    }

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 본문

   * - ``query_id``
     - 검색 API ( ``/search`` ) 가 반환하는 불투명한 ``query_id`` (str, 필수).

표: 요청 본문

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "ok": true,
        "favorite": true,
        "count": 6
      }
    }

각 필드에 대해서는 다음과 같습니다. 위 예시는 신규 등록 시의 예입니다. 즐겨찾기가 이미 등록된 상태에서 멱등하게 재 POST 한 경우에는 이에 더하여 ``already_existed`` 필드 ( ``true`` 로 설정) 가 응답에 포함됩니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드

   * - ``doc_id``
     - 문서 ID (str).
   * - ``ok``
     - 항상 ``true`` (bool).
   * - ``favorite``
     - 항상 ``true`` (bool). 신규 추가이든 기존이든 문서는 호출 사용자의 즐겨찾기가 됩니다.
   * - ``count``
     - 조작 후 현재 즐겨찾기 수 (int64). 신규 추가 시에는 조작 전 카운트 +1 (낙관적), 멱등한 재 POST 시에는 저장된 카운트를 반영합니다.
   * - ``already_existed``
     - 즐겨찾기가 이미 등록되어 있던 경우 ``true`` (bool, 멱등한 재 POST). 즐겨찾기를 신규 등록한 최초 POST 에는 존재하지 않습니다.

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
   * - 401 Unauthorized
     - 인증이 필요한 경우.
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
