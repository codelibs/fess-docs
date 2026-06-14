==========================
SystemInfo API
==========================

개요
====

SystemInfo API는 |Fess| 의 시스템 정보를 조회하기 위한 API입니다.
환경 변수, Java의 시스템 프로퍼티, |Fess| 의 설정 프로퍼티, 버그 리포트용 정보를 확인할 수 있습니다.

기본 URL
=========

::

    /api/admin/systeminfo

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
     - 시스템 정보 조회

시스템 정보 조회
================

요청
----------

::

    GET /api/admin/systeminfo

응답
----------

응답은 제품 버전을 나타내는 ``version``, 처리 결과를 나타내는 ``status`` 와
다음 4개의 프로퍼티 그룹을 포함합니다. 각 프로퍼티 그룹은 ``key`` 와 ``value`` 를 가진
객체의 배열입니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"key": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"key": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"key": "java.version", "value": "21.0.1"},
          {"key": "java.vendor", "value": "Oracle Corporation"},
          {"key": "os.name", "value": "Linux"},
          {"key": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"key": "crawler.document.max.site.length", "value": "50"},
          {"key": "indexer.thread.dump.enabled", "value": "true"}
        ],
        "bugReportProps": [
          {"key": "os.name", "value": "Linux"},
          {"key": "java.vm.version", "value": "21.0.1+12"}
        ]
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``envProps``
     - 환경 변수 목록 (``key`` / ``value`` 의 배열)
   * - ``systemProps``
     - Java의 시스템 프로퍼티 목록 (``key`` / ``value`` 의 배열)
   * - ``fessProps``
     - |Fess| 의 설정 프로퍼티 목록 (``key`` / ``value`` 의 배열)
   * - ``bugReportProps``
     - 버그 리포트용으로 수집되는 정보 목록 (``key`` / ``value`` 의 배열)

사용 예
======

시스템 정보 조회
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

특정 시스템 프로퍼티 추출
------------------------------

.. code-block:: bash

    # java.version 값만 추출
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.systemProps[] | select(.key == "java.version") | .value'

환경 변수 목록 표시
------------------

.. code-block:: bash

    # 환경 변수를 key=value 형식으로 표시
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.key)=\(.value)"'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-stats` - 통계 API
- :doc:`api-admin-general` - 일반 설정 API
- :doc:`../../admin/systeminfo-guide` - 시스템 정보 가이드
