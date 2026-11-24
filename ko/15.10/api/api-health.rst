==========
Health API
==========

이 문서에서는 |Fess| 의 v2 Health API 에 대해 설명합니다.
공통 응답 엔벨로프·오류 모델에 대해서는 :doc:`api-overview` 를 참조하십시오.

베이스 URL은 ``http://<Server Name>/api/v2/`` 입니다 (로컬 환경 예: ``http://localhost:8080/api/v2`` ).

상태 취득
=========

요청
----

==================  ====================================================
HTTP 메서드          GET
엔드포인트           ``/api/v2/health``
==================  ====================================================

검색 엔진 클러스터의 상태 스냅샷을 반환합니다 ( ``monitor`` 태그).
HTTP 상태는 클러스터 상태가 ``GREEN`` / ``YELLOW`` 인 경우 200, ``RED`` 인 경우 또는 검색 엔진에 접속할 수 없는 경우 503 이 됩니다.

``YELLOW`` 는 클러스터 상태가 ``YELLOW`` 인 경우 외에, 클러스터 상태가 ``GREEN`` 이더라도 |Fess| 의 인덱스 중 하나 또는 클러스터 전체에 쓰기를 거부하는 블록이 걸려 있는 경우에도 반환됩니다. 예를 들어 OpenSearch는 디스크 사용량이 플러드 스테이지 워터마크를 넘으면 인덱스를 읽기 전용으로 만듭니다. 이 상태에서도 검색은 동작하지만 크롤링, 설정 변경, 인덱스 갱신은 실패합니다. 같은 클러스터를 공유하는 다른 애플리케이션의 인덱스는 대상에 포함되지 않습니다. 블록을 읽을 수 없는 경우 상태는 ``GREEN`` 으로 유지됩니다. 이 엔드포인트는 인증 없이 호출할 수 있으므로 응답에는 ``YELLOW`` 인 이유가 포함되지 않습니다. 이유는 관리자가 OpenSearch 쪽에서 확인하십시오.

이 엔드포인트는 엔벨로프의 불변 조건 "``status >= 1`` ⇔ HTTP 상태 ``>= 400``" 을 준수합니다.

- ``GREEN`` / ``YELLOW`` 인 경우: 성공 엔벨로프 ( ``status: 0`` ) 로 ``engine`` 을 반환합니다.
- ``RED`` 인 경우: 오류 엔벨로프 ( ``status: 9`` , ``error.code: service_unavailable`` ) 를 반환하고, 엔진 스냅샷을 ``error.details.engine`` 아래에 포함합니다 (모니터링 도구가 클러스터 메타데이터를 분석할 수 있도록 하기 위해서입니다).
- 검색 엔진에 접속할 수 없는 경우: ``RED`` 와 마찬가지로 오류 엔벨로프 ( ``error.code: service_unavailable`` , ``error.message: search engine is not reachable`` ) 를 반환하며, ``error.details.engine`` 은 ``status: UNAVAILABLE`` , ``ping_status: 1`` 이 됩니다.

.. note::

   ``/api/v2/search`` 는 검색 엔진에 연결할 수 없을 때 503을 반환하지 않습니다. HTTP 상태 200으로 ``partial: true`` 이고 히트가 0건인 응답을 반환합니다(:doc:`api-search` 참조). "검색 결과 없음"과 "검색 엔진 중지"를 구분해야 하는 클라이언트는 검색 응답의 ``partial`` 을 확인하고, 검색 엔진의 상태는 이 엔드포인트로 확인하십시오.

``engine`` 의 각 필드는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine 필드

   * - ``status``
     - 클러스터 상태. 대문자 ``GREEN`` / ``YELLOW`` / ``RED`` 중 하나. 클러스터가 ``GREEN`` 이더라도 |Fess| 의 인덱스에 쓰기 블록이 걸려 있는 동안에는 ``YELLOW`` 가 됩니다(위 참조). 검색 엔진에 접속할 수 없는 경우에는 ``UNAVAILABLE`` .
   * - ``ping_status``
     - ping 상태 (int). 클러스터가 ``RED`` 이거나 검색 엔진에 접속할 수 없는 경우 ``1`` , 그 외 ( ``GREEN`` / ``YELLOW`` ) 인 경우 ``0`` 이 됩니다.

표: engine 필드

클러스터 이름 ( ``cluster_name`` ) 은 이 엔드포인트가 인증 없이 호출될 수 있으므로 반환하지 않습니다.

요청 파라미터
-------------

사용 가능한 요청 파라미터는 없습니다.

응답
----

클러스터가 ``GREEN`` / ``YELLOW`` 인 경우 (200) 에는 성공 엔벨로프로 ``engine`` 이 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "status": "GREEN",
          "ping_status": 0
        }
      }
    }

클러스터가 ``RED`` 인 경우 (503) 에는 오류 엔벨로프로 반환되고, 엔진 스냅샷이 ``error.details.engine`` 아래에 포함됩니다.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "status": "RED",
              "ping_status": 1
            }
          }
        }
      }
    }

사용 예
=======

curl 명령으로 요청 예:

::

    curl "http://localhost:8080/api/v2/health"

응답 및 오류 응답
=================

오류 모델의 자세한 내용은 :doc:`api-overview` 를 참조하십시오. 이 엔드포인트가 반환하는 HTTP 상태는 다음과 같습니다.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 응답 목록

   * - 상태 코드
     - 설명
   * - 200 OK
     - 클러스터가 ``GREEN`` / ``YELLOW`` 이며 도달 가능한 경우. 성공 엔벨로프에 ``engine`` 이 포함됩니다.
   * - 400 Bad Request
     - 디코딩할 수 없는 요청 파라미터 (예: ``?q=%ff``)가 지정된 경우. ``error.code`` 는 ``invalid_request`` 입니다.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 503 Service Unavailable
     - 클러스터가 ``RED`` 이거나 검색 엔진에 접속할 수 없는 경우. 오류 엔벨로프 ( ``error.code: service_unavailable`` ) 로 ``error.details.engine`` 에 엔진 스냅샷이 포함됩니다. ``Retry-After: 5`` 헤더로 클라이언트가 재시도하기 전에 기다려야 하는 초 수를 알려줍니다.

표: 응답 목록
