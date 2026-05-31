===========
자동완성 API
===========

자동완성 단어 목록 취득
========================

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/suggest-words``
==================  ====================================================

|Fess| 에 ``http://<Server Name>/api/v2/suggest-words?q=fes`` 와 같은 요청을 전송하면 입력한 접두사에 대한 자동완성 단어 목록을 JSON 형식으로 받을 수 있습니다.
자동완성 API 를 사용하려면 관리 화면의 시스템 > 일반 설정에서 "문서로 자동완성" 또는 "검색어로 자동완성"을 활성화해야 합니다.

응답 공통 엔벨로프 및 오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

요청 파라미터
-------------

사용 가능한 요청 파라미터는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 요청 파라미터

   * - q
     - 자동완성할 검색어 (접두사). (예) ``q=fes``
   * - num
     - 자동완성될 단어 수 (0 이상의 정수). 기본값 ``10`` . (예) ``num=20``
   * - fn
     - 자동완성 대상을 좁히는 필드 이름. 반복 지정으로 배열로 처리됩니다. (예) ``fn=content&fn=title``
   * - lang
     - 검색 언어 지정. 반복 지정으로 배열로 처리됩니다. (예) ``lang=en``
   * - label
     - 필터링할 레이블 이름. 반복 지정으로 배열로 처리됩니다. (예) ``label=java``

.. note::

   v2 에서는 필드 이름 지정에 ``fn`` 파라미터를 사용합니다 (v1 의 ``fields`` 와는 다릅니다).
   또한 레이블 지정에는 ``label`` 파라미터를 사용합니다 (v1 의 ``labels`` 파라미터와는 다릅니다).

응답
----

성공 시에는 다음과 같은 공통 엔벨로프 형식의 응답이 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "document",
              "query"
            ]
          }
        ]
      }
    }

``response`` 의 각 요소에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 정보

   * - q
     - 요청된 검색어 (문자열).
   * - page_size
     - 페이지 크기 (정수).
   * - record_count
     - 자동완성 단어 해당 건수 (64비트 정수).
   * - query_time
     - 쿼리 처리 시간. 단위는 밀리초 (64비트 정수).
   * - suggest_words
     - 자동완성 단어 배열. 각 요소는 ``text`` 와 ``types`` 를 가집니다.
   * - text
     - 자동완성 단어 (문자열).
   * - types
     - 자동완성 단어의 종별 배열 (문자열 배열).

.. note::

   v2 에서는 자동완성 항목의 필드가 ``text`` 와 ``types`` 입니다 (v1 의 ``labels`` 와는 다릅니다).

사용 예
=======

curl 명령으로 요청 예:

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

오류 응답
=========

자동완성 API 가 실패한 경우 공통 오류 엔벨로프가 반환됩니다. 오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 405 Method Not Allowed
     - 지원되지 않는 HTTP 메서드가 지정된 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.
