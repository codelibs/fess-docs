=========
레이블 API
=========

이 문서에서는 |Fess| 의 v2 레이블 API 에 대해 설명합니다.
공통 응답 엔벨로프·오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

레이블 취득
===========

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/labels``
==================  ====================================================

|Fess| 에 등록된 설정된 레이블 목록을 공통 엔벨로프로 취득합니다.

요청 파라미터
-------------

사용 가능한 요청 파라미터는 없습니다.

응답
----

성공 시 (200) 에는 공통 엔벨로프의 ``response`` 바로 아래에 다음 필드가 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
          {
            "label": "AWS",
            "value": "aws"
          },
          {
            "label": "Azure",
            "value": "azure"
          }
        ]
      }
    }

각 필드에 대해서는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: 응답 필드

   * - ``record_count``
     - 레이블 등록 건수 (integer).
   * - ``labels``
     - 레이블 배열.
   * - ``label``
     - 레이블 이름.
   * - ``value``
     - 레이블 값.

표: 응답 필드

사용 예
=======

curl 명령으로 요청 예:

::

    curl "http://localhost:8080/api/v2/labels"

오류 응답
=========

오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오. 이 엔드포인트가 반환하는 HTTP 상태는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우.

표: 오류 응답
