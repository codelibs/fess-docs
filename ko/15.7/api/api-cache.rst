===========
캐시 API
===========

이 문서에서는 |Fess| 의 v2 캐시 API 에 대해 설명합니다.
공통 응답 엔벨로프·오류 모델·CSRF 에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

캐시된 문서 취득
================

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/cache/{docId}``
==================  ====================================================

문서의 캐시된 (하이라이트 적용된) HTML 을 반환합니다.

로그인 필수 설정 (시스템 설정의 「로그인 필수」) 이 활성화되어 있고 호출자가 익명인 경우 ``auth_required`` (401) 가 됩니다.

요청 파라미터
-------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 요청 파라미터

   * - ``docId``
     - 문서 식별자 (path, 필수, 패턴 ``^[A-Za-z0-9_-]+$`` ).
   * - ``hq``
     - 하이라이트 쿼리어 (query). 반복 지정 가능 (배열).

표: 요청 파라미터

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "doc_id": "a1b2c3d4e5f6",
        "mimetype": "text/html",
        "content": "<html><body>...</body></html>",
        "url": "https://example.com/",
        "created": "2024-05-31T12:00:00.000Z",
        "charset": "UTF-8"
      }
    }

각 필드에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 필드

   * - ``doc_id``
     - 문서 ID (str).
   * - ``mimetype``
     - MIME 타입 (enum: ``text/html`` ).
   * - ``content``
     - 캐시된 HTML 본문 (str).
   * - ``url``
     - 문서 URL (str). 존재하면 ``url_link`` 필드, 없으면 인덱스의 원시 URL. 둘 다 없는 경우 생략됩니다.
   * - ``created``
     - 인덱스의 문서 생성 타임스탬프 (str). 존재하지 않을 때는 생략됩니다.
   * - ``charset``
     - 문서의 mimetype 에서 파싱한 문자 세트 (str). 없는 경우 ``UTF-8`` 이 기본값입니다.

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
     - 인증이 필요한 경우 (로그인 필수 설정이 활성화되어 있고 익명 호출자).
   * - 404 Not Found
     - 리소스를 찾을 수 없는 경우.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답
