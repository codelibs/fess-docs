==========================
Stats API
==========================

개요
====

Stats API는 |Fess| 가 가동되는 서버의 시스템 메트릭을 조회하기 위한 API입니다.
JVM, OS, 프로세스, 검색 엔진(OpenSearch) 클러스터, 파일 시스템의 각 통계 정보를 확인할 수 있습니다.

.. note::

   이 API는 검색 쿼리나 클릭 등의 검색 분석 데이터를 반환하지 않습니다.
   인덱스 내 문서의 검색 및 관리에는 :doc:`api-admin-searchlist` 를 참조하십시오.

기본 URL
=========

::

    /api/admin/stats

이 API에 접근하려면 ``Radmin-api`` 권한을 가진 액세스 토큰이 필요합니다.
인증 방법의 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

엔드포인트 목록
==================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - 메서드
     - 경로
     - 설명
   * - GET
     - /
     - 시스템 통계 정보 조회

시스템 통계 정보 조회
======================

요청
----

::

    GET /api/admin/stats

이 엔드포인트는 쿼리 파라미터를 받지 않습니다.

응답
----

응답은 제품 버전을 나타내는 ``version``, 처리 결과를 나타내는 ``status`` 와,
시스템 메트릭을 저장하는 ``stats`` 객체를 포함합니다.
``stats`` 는 ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` 의 5개 키를 가집니다.

.. note::

   ``stats`` 하위 객체의 필드명은 스네이크 케이스(소문자와 밑줄로 구분, 예: ``non_heap``)로 출력됩니다.
   값이 ``null`` 인 필드는 응답에서 생략됩니다.

.. code-block:: json

    {
      "response": {
        "version": "15.8.0",
        "status": 0,
        "stats": {
          "jvm": {
            "memory": {
              "heap": {
                "used": 536870912,
                "committed": 1073741824,
                "max": 2147483648,
                "percent": 25
              },
              "non_heap": {
                "used": 134217728,
                "committed": 268435456,
                "max": 0,
                "percent": 0
              }
            },
            "pools": [
              {"key": "mapped", "count": 1, "used": 4096, "capacity": 4096}
            ],
            "gc": [
              {"key": "young", "count": 12, "time": 345}
            ],
            "threads": {"count": 80, "peak": 95},
            "classes": {"loaded": 12000, "total_loaded": 12500, "unloaded": 500},
            "uptime": 3600000
          },
          "os": {
            "memory": {
              "physical": {"free": 2147483648, "total": 8589934592},
              "swap_space": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "load_averages": [0.5, 0.4, 0.3]
          },
          "process": {
            "file_fescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtual_memory": {"total": 4294967296}
          },
          "engine": {
            "cluster_name": "fess",
            "number_of_nodes": 1,
            "number_of_data_nodes": 1,
            "active_primary_shards": 10,
            "active_shards": 10,
            "active_shards_percent": 100.0,
            "relocating_shards": 0,
            "initializing_shards": 0,
            "unassigned_shards": 0,
            "delayed_unassigned_shards": 0,
            "number_of_pending_tasks": 0,
            "number_of_in_flight_fetch": 0,
            "status": "green"
          },
          "fs": [
            {
              "path": "/",
              "total": 107374182400,
              "free": 53687091200,
              "usable": 53687091200,
              "used": 53687091200,
              "percent": 50
            }
          ]
        }
      }
    }

응답 필드 (최상위)
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 필드
     - 설명
   * - ``version``
     - |Fess| 의 제품 버전 (예: ``15.8.0``).
   * - ``status``
     - 처리 결과를 나타내는 코드. ``0`` 은 정상 종료를 나타냅니다.
   * - ``stats``
     - 시스템 메트릭을 저장하는 객체. ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` 의 5개 키를 가집니다.

``jvm``: JVM 통계
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 필드
     - 설명
   * - ``memory.heap.used``
     - 사용 중인 힙 메모리 (바이트).
   * - ``memory.heap.committed``
     - 확보된 힙 메모리 (바이트).
   * - ``memory.heap.max``
     - 힙 메모리의 최대값 (바이트).
   * - ``memory.heap.percent``
     - 힙 메모리 사용률 (%).
   * - ``memory.non_heap.used``
     - 사용 중인 비힙 메모리 (바이트).
   * - ``memory.non_heap.committed``
     - 확보된 비힙 메모리 (바이트).
   * - ``memory.non_heap.max``
     - 비힙 메모리의 최대값 (바이트). 현재 구현에서는 값이 설정되지 않으며 항상 ``0`` 이 반환됩니다.
   * - ``memory.non_heap.percent``
     - 비힙 메모리 사용률 (%). 현재 구현에서는 값이 설정되지 않으며 항상 ``0`` 이 반환됩니다.
   * - ``pools``
     - 버퍼 풀의 배열. 각 요소는 ``key`` (풀 이름), ``count`` (버퍼 수), ``used`` (사용량, 바이트), ``capacity`` (총 용량, 바이트)를 포함합니다.
   * - ``gc``
     - 가비지 컬렉터의 배열. 각 요소는 ``key`` (컬렉터 이름), ``count`` (실행 횟수), ``time`` (누적 실행 시간, 밀리초)를 포함합니다.
   * - ``threads.count``
     - 현재 스레드 수.
   * - ``threads.peak``
     - 스레드 수의 최댓값.
   * - ``classes.loaded``
     - 현재 로드된 클래스 수.
   * - ``classes.total_loaded``
     - JVM 시작 이후 로드된 총 클래스 수.
   * - ``classes.unloaded``
     - 언로드된 총 클래스 수.
   * - ``uptime``
     - JVM 가동 시간 (밀리초).

``os``: OS 통계
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 필드
     - 설명
   * - ``memory.physical.free``
     - 여유 물리 메모리 (바이트).
   * - ``memory.physical.total``
     - 총 물리 메모리 (바이트).
   * - ``memory.swap_space.free``
     - 여유 스왑 공간 (바이트).
   * - ``memory.swap_space.total``
     - 총 스왑 공간 (바이트).
   * - ``cpu.percent``
     - 시스템 전체 CPU 사용률 (%).
   * - ``load_averages``
     - 로드 애버리지 배열 (1분, 5분, 15분). 취득할 수 없는 값은 ``-1`` 이 될 수 있습니다.

``process``: 프로세스 통계
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 필드
     - 설명
   * - ``file_fescriptor.open``
     - 현재 열려 있는 파일 디스크립터 수.
   * - ``file_fescriptor.max``
     - 열 수 있는 파일 디스크립터의 최대 수.
   * - ``cpu.percent``
     - 프로세스 CPU 사용률 (%).
   * - ``cpu.total``
     - 프로세스가 사용한 누적 CPU 시간 (밀리초).
   * - ``virtual_memory.total``
     - 프로세스의 총 가상 메모리 크기 (바이트).

.. note::

   ``process.file_fescriptor`` 라는 키 이름은 소스 코드의 필드명 ``fileFescriptor``
   (``fileDescriptor`` 의 철자 오류에서 유래)를 스네이크 케이스로 변환한 것입니다. 구현을 따른 것이며 이 문서의 오타가 아닙니다.

``engine``: 검색 엔진 클러스터 통계
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

검색 엔진(OpenSearch) 클러스터의 헬스 정보입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 필드
     - 설명
   * - ``cluster_name``
     - 클러스터 이름.
   * - ``number_of_nodes``
     - 클러스터 내 총 노드 수.
   * - ``number_of_data_nodes``
     - 데이터 노드 수.
   * - ``active_primary_shards``
     - 활성 프라이머리 샤드 수.
   * - ``active_shards``
     - 활성 샤드 수.
   * - ``active_shards_percent``
     - 활성 샤드의 비율 (%).
   * - ``relocating_shards``
     - 재배치 중인 샤드 수.
   * - ``initializing_shards``
     - 초기화 중인 샤드 수.
   * - ``unassigned_shards``
     - 미할당 샤드 수.
   * - ``delayed_unassigned_shards``
     - 할당이 지연된 미할당 샤드 수.
   * - ``number_of_pending_tasks``
     - 대기 중인 태스크 수.
   * - ``number_of_in_flight_fetch``
     - 실행 중인 페치 작업 수.
   * - ``status``
     - 클러스터 헬스 상태 (``green`` / ``yellow`` / ``red``).
   * - ``exception``
     - 클러스터에 연결할 수 없는 등 오류 발생 시에만 포함되는 오류 메시지. 이 경우 ``status`` 는 ``red`` 가 됩니다.

``fs``: 파일 시스템 통계
~~~~~~~~~~~~~~~~~~~~~~~~~

각 루트 (``File.listRoots()`` 로 얻은 루트)별 통계 정보를 저장한 배열입니다.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 필드
     - 설명
   * - ``path``
     - 루트의 절대 경로.
   * - ``total``
     - 총 용량 (바이트).
   * - ``free``
     - 여유 용량 (바이트).
   * - ``usable``
     - 사용 가능한 용량 (바이트).
   * - ``used``
     - 사용된 용량 (바이트). ``total`` 에서 ``usable`` 을 뺀 값입니다.
   * - ``percent``
     - 사용률 (%).

사용 예
=======

시스템 통계 정보 조회
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

JVM 힙 사용률 확인
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

검색 엔진 클러스터 상태 확인
-----------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

참고 정보
=========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`api-admin-searchlist` - 문서 검색 및 관리 API
