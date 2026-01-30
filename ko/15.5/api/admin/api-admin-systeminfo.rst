==========================
SystemInfo API
==========================

개요
====

SystemInfo API는 |Fess| 의 시스템 정보를 조회하기 위한 API입니다.
버전 정보, 환경 변수, JVM 정보 등을 확인할 수 있습니다.

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

.. code-block:: json

    {
      "response": {
        "status": 0,
        "systemInfo": {
          "fessVersion": "15.5.0",
          "opensearchVersion": "2.11.0",
          "javaVersion": "21.0.1",
          "serverName": "Apache Tomcat/10.1.15",
          "osName": "Linux",
          "osVersion": "5.15.0-89-generic",
          "osArchitecture": "amd64",
          "jvmTotalMemory": "2147483648",
          "jvmFreeMemory": "1073741824",
          "jvmMaxMemory": "4294967296",
          "processorCount": "8",
          "fileEncoding": "UTF-8",
          "userLanguage": "ja",
          "userTimezone": "Asia/Tokyo"
        },
        "environmentInfo": {
          "JAVA_HOME": "/usr/lib/jvm/java-21",
          "FESS_DICTIONARY_PATH": "/var/lib/fess/dict",
          "FESS_LOG_PATH": "/var/log/fess"
        },
        "systemProperties": {
          "java.version": "21.0.1",
          "java.vendor": "Oracle Corporation",
          "os.name": "Linux",
          "os.version": "5.15.0-89-generic",
          "user.dir": "/opt/fess",
          "user.home": "/home/fess",
          "user.name": "fess"
        }
      }
    }

응답 필드
~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 필드
     - 설명
   * - ``fessVersion``
     - Fess 버전
   * - ``opensearchVersion``
     - OpenSearch 버전
   * - ``javaVersion``
     - Java 버전
   * - ``serverName``
     - 애플리케이션 서버 이름
   * - ``osName``
     - OS 이름
   * - ``osVersion``
     - OS 버전
   * - ``osArchitecture``
     - OS 아키텍처
   * - ``jvmTotalMemory``
     - JVM 총 메모리 (바이트)
   * - ``jvmFreeMemory``
     - JVM 여유 메모리 (바이트)
   * - ``jvmMaxMemory``
     - JVM 최대 메모리 (바이트)
   * - ``processorCount``
     - 프로세서 수
   * - ``fileEncoding``
     - 파일 인코딩
   * - ``userLanguage``
     - 사용자 언어
   * - ``userTimezone``
     - 사용자 타임존

사용 예
======

시스템 정보 조회
------------------

.. code-block:: bash

    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN"

버전 확인
--------------

.. code-block:: bash

    # Fess 버전만 추출
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo.fessVersion'

메모리 사용 상황 확인
--------------------

.. code-block:: bash

    # JVM 메모리 정보 추출
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" | jq '.response.systemInfo | {total: .jvmTotalMemory, free: .jvmFreeMemory, max: .jvmMaxMemory}'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-stats` - 통계 API
- :doc:`api-admin-general` - 일반 설정 API
- :doc:`../../admin/systeminfo-guide` - 시스템 정보 가이드
