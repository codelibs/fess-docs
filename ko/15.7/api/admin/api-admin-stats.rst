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
====================

요청
----------

::

    GET /api/admin/stats

이 엔드포인트는 쿼리 파라미터를 받지 않습니다.

응답
----------

응답은 제품 버전을 나타내는 ``version``, 처리 결과를 나타내는 ``status`` 와,
시스템 메트릭을 저장하는 ``stats`` 객체를 포함합니다.
``stats`` 는 ``jvm`` / ``os`` / ``process`` / ``engine`` / ``fs`` 의 5개 키를 가집니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
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
              "nonHeap": {
                "used": 134217728,
                "committed": 268435456
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
              "swapSpace": {"free": 0, "total": 0}
            },
            "cpu": {"percent": 12},
            "loadAverages": [0.5, 0.4, 0.3]
          },
          "process": {
            "fileFescriptor": {"open": 256, "max": 65536},
            "cpu": {"percent": 5, "total": 123456},
            "virtualMemory": {"total": 4294967296}
          },
          "engine": {
            "clusterName": "fess",
            "numberOfNodes": 1,
            "numberOfDataNodes": 1,
            "activePrimaryShards": 10,
            "activeShards": 10,
            "activeShardsPercent": 100.0,
            "relocatingShards": 0,
            "initializingShards": 0,
            "unassignedShards": 0,
            "delayedUnassignedShards": 0,
            "numberOfPendingTasks": 0,
            "numberOfInFlightFetch": 0,
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

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 필드
     - 설명
   * - ``jvm``
     - JVM 통계. ``memory``(``heap`` / ``nonHeap``), ``pools``(버퍼 풀), ``gc``(GC), ``threads``, ``classes``, ``uptime``(밀리초)를 포함합니다.
   * - ``os``
     - OS 통계. ``memory``(``physical`` / ``swapSpace``), ``cpu``, ``loadAverages``(로드 애버리지 배열)를 포함합니다.
   * - ``process``
     - 프로세스 통계. ``fileFescriptor``(열린/최대 파일 디스크립터 수), ``cpu``, ``virtualMemory`` 를 포함합니다.
   * - ``engine``
     - 검색 엔진(OpenSearch) 클러스터의 상태. ``clusterName``, 노드 수, 샤드 수, ``status`` 등을 포함합니다. 클러스터에 연결할 수 없는 경우 ``status`` 가 ``"red"`` 가 되며, ``exception`` 에 오류 메시지가 포함됩니다.
   * - ``fs``
     - 파일 시스템 통계의 배열. 각 루트에 대해 ``path``, ``total``, ``free``, ``usable``, ``used``(바이트), ``percent``(사용률)를 포함합니다.

.. note::

   ``process.fileFescriptor`` 라는 키 이름은 소스 코드 구현을 따릅니다(``fileDescriptor`` 철자가 아닙니다).

사용 예
======

시스템 통계 정보 조회
----------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN"

JVM 힙 사용률 확인
---------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.jvm.memory.heap.percent'

검색 엔진 클러스터 상태 확인
--------------------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/stats" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq '.response.stats.engine.status'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-systeminfo` - 시스템 정보 API
- :doc:`api-admin-searchlist` - 문서 검색 및 관리 API
