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
HTTP 상태는 클러스터 상태가 ``green`` / ``yellow`` 인 경우 200, ``red`` 인 경우 503 이 됩니다.

이 엔드포인트는 엔벨로프의 불변 조건 "``status >= 1`` ⇔ HTTP 상태 ``>= 400``" 을 준수합니다.

- ``green`` / ``yellow`` 인 경우: 성공 엔벨로프 ( ``status: 0`` ) 로 ``engine`` 을 반환합니다.
- ``red`` 인 경우: 오류 엔벨로프 ( ``status: 9`` , ``error.code: service_unavailable`` ) 를 반환하고, 엔진 스냅샷을 ``error.details.engine`` 아래에 포함합니다 (모니터링 도구가 클러스터 메타데이터를 분석할 수 있도록 하기 위해서입니다).

``engine`` 의 각 필드는 다음과 같습니다.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: engine 필드

   * - ``cluster_name``
     - 클러스터 이름 (str).
   * - ``status``
     - 클러스터 상태. ``green`` / ``yellow`` / ``red`` 중 하나.
   * - ``ping_status``
     - ping 상태 (int). 클러스터가 ``red`` 인 경우 ``1`` , 그 외 ( ``green`` / ``yellow`` ) 인 경우 ``0`` 이 됩니다.

표: engine 필드

요청 파라미터
-------------

사용 가능한 요청 파라미터는 없습니다.

응답
----

클러스터가 ``green`` / ``yellow`` 인 경우 (200) 에는 성공 엔벨로프로 ``engine`` 이 반환됩니다.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess-es",
          "status": "green",
          "ping_status": 0
        }
      }
    }

클러스터가 ``red`` 인 경우 (503) 에는 오류 엔벨로프로 반환되고, 엔진 스냅샷이 ``error.details.engine`` 아래에 포함됩니다.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "cluster_name": "fess-es",
              "status": "red",
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
     - 클러스터가 ``green`` / ``yellow`` 이며 도달 가능한 경우. 성공 엔벨로프에 ``engine`` 이 포함됩니다.
   * - 405 Method Not Allowed
     - HTTP 메서드가 허용되지 않는 경우.
   * - 503 Service Unavailable
     - 클러스터가 ``red`` 인 경우. 오류 엔벨로프 ( ``error.code: service_unavailable`` ) 로 ``error.details.engine`` 에 엔진 스냅샷이 포함됩니다.

표: 응답 목록
