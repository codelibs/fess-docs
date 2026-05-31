============
인기 검색어 API
============

인기 검색어 목록 취득
=====================

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/popular-words``
==================  ====================================================

|Fess| 에 ``http://<Server Name>/api/v2/popular-words?seed=123`` 와 같은 요청을 전송하면 인기 검색어 목록을 JSON 형식으로 받을 수 있습니다.

``web.api.popular.word=false`` 인 경우 이 API 는 ``invalid_request`` (HTTP 400) 를 반환합니다 (v1 의 "unsupported operation" 에 해당하는 동작입니다).

응답 공통 엔벨로프 및 오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

요청 파라미터
-------------

사용 가능한 요청 파라미터는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 요청 파라미터

   * - seed
     - 인기 검색어를 취득하는 시드 (문자열). 이 값에 따라 다른 패턴의 단어를 취득할 수 있습니다. (예) ``seed=123``
   * - label
     - 필터링할 레이블 이름. 반복 지정으로 배열로 처리됩니다. (예) ``label=java``
   * - field
     - 인기 검색어를 생성할 필드 이름. 반복 지정으로 배열로 처리됩니다. (예) ``field=label``

응답
----

성공 시에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 정보

   * - record_count
     - 인기 검색어 건수 (정수).
   * - popular_words
     - 인기 검색어 배열 (문자열 배열).

.. note::

   v2 에서는 인기 검색어가 ``popular_words`` (문자열 배열) 로 반환됩니다 (v1 의 ``data`` 와는 다릅니다).

사용 예
=======

curl 명령으로 요청 예:

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

오류 응답
=========

인기 검색어 API 가 실패한 경우 공통 오류 엔벨로프가 반환됩니다. 오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 400 Bad Request
     - 요청이 잘못된 경우 ( ``web.api.popular.word=false`` 로 기능이 비활성화된 경우 포함). ``error.code`` 는 ``invalid_request`` 입니다.
   * - 405 Method Not Allowed
     - 지원되지 않는 HTTP 메서드가 지정된 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.
