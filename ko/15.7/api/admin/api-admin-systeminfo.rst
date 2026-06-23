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

이 API에 접근하려면 ``Radmin-api`` 권한을 가진 액세스 토큰이 필요합니다.
인증 방법에 대한 자세한 내용은 :doc:`api-admin-overview` 를 참조하십시오.

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

이 엔드포인트는 쿼리 파라미터를 허용하지 않습니다.

응답
----------

응답은 제품 버전을 나타내는 ``version``, 처리 결과를 나타내는 ``status`` 와
다음 4개의 프로퍼티 그룹을 포함합니다. 각 프로퍼티 그룹은 ``label`` 과 ``value`` 를 가진
객체의 배열입니다.

.. code-block:: json

    {
      "response": {
        "version": "15.7.0",
        "status": 0,
        "envProps": [
          {"label": "JAVA_HOME", "value": "/usr/lib/jvm/java-21"},
          {"label": "FESS_DICTIONARY_PATH", "value": "/var/lib/fess/dict"}
        ],
        "systemProps": [
          {"label": "java.version", "value": "21.0.1"},
          {"label": "java.vendor", "value": "Oracle Corporation"},
          {"label": "os.name", "value": "Linux"},
          {"label": "user.dir", "value": "/opt/fess"}
        ],
        "fessProps": [
          {"label": "crawler.document.max.site.length", "value": "100"},
          {"label": "indexer.thread.dump.enabled", "value": "true"},
          {"label": "app.cipher.key", "value": "XXXXXXXX"}
        ],
        "bugReportProps": [
          {"label": "os.name", "value": "Linux"},
          {"label": "java.vm.version", "value": "21.0.1+12"}
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
   * - ``version``
     - |Fess| 의 제품 버전 (예: ``15.7.0``).
   * - ``status``
     - 처리 결과를 나타내는 코드. ``0`` 은 정상 종료를 의미합니다.
   * - ``envProps``
     - 환경 변수 목록 (``label`` / ``value`` 의 배열). ``System.getenv()`` 로 취득한 값이 그대로 반환됩니다.
   * - ``systemProps``
     - Java의 시스템 프로퍼티 목록 (``label`` / ``value`` 의 배열). ``System.getProperties()`` 로 취득한 값이 그대로 반환됩니다.
   * - ``fessProps``
     - |Fess| 의 설정 프로퍼티 목록 (``label`` / ``value`` 의 배열). ``fess_config.properties`` 의 설정값과 관리 화면에서 설정된 시스템 프로퍼티가 포함됩니다. 민감한 항목은 마스킹됩니다 (아래 주의 사항 참조).
   * - ``bugReportProps``
     - 버그 리포트용으로 수집되는 정보 목록 (``label`` / ``value`` 의 배열). OS 및 Java 실행 환경에 관한 주요 시스템 프로퍼티 (``os.name``, ``os.version``, ``java.vm.version`` 등) 와 |Fess| 의 시스템 프로퍼티 설정값이 포함됩니다.

.. note::

   ``fessProps`` 에서는 다음 민감한 설정값이 마스킹되어 ``XXXXXXXX`` 로 반환됩니다:
   ``http.proxy.password``, ``ldap.admin.security.credentials``, ``spnego.preauth.password``,
   ``app.cipher.key``, ``oic.client.id``, ``oic.client.secret``.

.. warning::

   ``envProps`` (환경 변수) 와 ``systemProps`` (Java 시스템 프로퍼티) 는 마스킹되지 않으며,
   설정된 값이 그대로 반환됩니다. 환경 변수나 시스템 프로퍼티에 인증 정보 등의
   민감한 정보가 포함된 경우, 해당 값들이 응답에 포함되는 점에 주의하십시오.

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
         | jq -r '.response.systemProps[] | select(.label == "java.version") | .value'

환경 변수 목록 표시
------------------

.. code-block:: bash

    # 환경 변수를 label=value 형식으로 표시
    curl -X GET "http://localhost:8080/api/admin/systeminfo" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         | jq -r '.response.envProps[] | "\(.label)=\(.value)"'

참고 정보
========

- :doc:`api-admin-overview` - Admin API 개요
- :doc:`api-admin-stats` - 통계 API
- :doc:`api-admin-general` - 일반 설정 API
- :doc:`../../admin/systeminfo-guide` - 시스템 정보 가이드
