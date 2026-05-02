========
레이블 API
=======

레이블 조회
======

요청
--

==================  ====================================================
HTTP 메서드         GET
엔드포인트        ``/api/v1/labels``
==================  ====================================================

|Fess| 에, ``http://<Server Name>/api/v1/labels`` 요청을 전송하여, |Fess| 에 등록된 레이블 목록을 JSON 형식으로 받을 수 있습니다.

요청 매개변수
-------

사용 가능한 요청 매개변수는 없습니다.


응답
--

다음과 같은 응답이 반환됩니다.

::

    {
      "record_count": 9,
      "data": [
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

각 요소는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - 레이블 등록 건수.
   * - data
     - 검색 결과의 부모 요소.
   * - label
     - 레이블 이름.
   * - value
     - 레이블 값.

표: 응답 정보

사용 예
====

curl 명령으로 요청 예:

::

    curl "http://localhost:8080/api/v1/labels"

JavaScript로 요청 예:

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('레이블 목록:', data.data);
      });

오류 응답
=====

레이블 API가 실패한 경우 다음과 같은 오류 응답이 반환됩니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 오류 응답

   * - 상태 코드
     - 설명
   * - 500 Internal Server Error
     - 서버 내부 오류가 발생한 경우
