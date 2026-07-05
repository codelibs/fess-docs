==========================
Windows 서비스 등록
==========================

Windows 서비스로 등록
======================

|Fess| 를 Windows 서비스로 등록할 수 있습니다. 서비스로 등록하면 시스템 시작 시 |Fess| 를 자동으로 시작할 수 있습니다.
|Fess| 를 실행하려면 OpenSearch를 미리 시작해 두어야 합니다.
여기서는 |Fess| 를 ``c:\opt\fess`` 에, OpenSearch를 ``c:\opt\opensearch`` 에 설치했다고 가정합니다（경로는 환경에 맞게 읽어 주십시오）.

.. note::
   |Fess| 및 OpenSearch는 64비트 버전만 지원합니다.

사전 준비
---------

시스템 환경 변수로 ``JAVA_HOME`` 을 설정하십시오. ``service.bat`` 는 ``JAVA_HOME`` 이 설정되어 있지 않으면 오류로 종료됩니다.

OpenSearch를 서비스로 등록
--------------------------

명령 프롬프트를 관리자 권한으로 시작하고 ``c:\opt\opensearch\bin\opensearch-service.bat`` 를 실행합니다.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

자세한 내용은 `OpenSearch 문서 <https://opensearch.org/docs/latest/install-and-configure/install-opensearch/windows/>`_ 를 참조하십시오.

|Fess| 설정
-----------

서비스는 ``c:\opt\fess\bin\service.bat`` 에서 등록합니다. ``service.bat`` 는 등록 시 ``bin\fess.in.bat`` 를 읽어 그 내용을 |Fess| 의 시작 옵션에 반영합니다.
OpenSearch에 연결하기 위한 설정을 ``c:\opt\fess\bin\fess.in.bat`` 에 추가하십시오.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.search_engine.http_address=http://localhost:9200
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.dictionary.path=c:/opt/opensearch/data/config/

.. note::
   - ``fess.search_engine.http_address`` 에는 등록한 OpenSearch 서비스의 연결 대상을 지정합니다. 이 설정을 하지 않으면 |Fess| 는 연결 대상을 찾지 못하고 프로덕션 환경에서는 권장하지 않는 내장 OpenSearch를 시작합니다.
   - OpenSearch를 다른 호스트에서 실행하는 경우 호스트명 또는 IP 주소를 적절히 변경하십시오.
   - 경로 구분 문자는 ``/`` 를 사용하십시오.

|Fess| 의 검색 화면·관리 화면의 기본 포트 번호는 ``8080`` 입니다. 다른 포트로 변경하는 경우 ``c:\opt\fess\bin\fess.in.bat`` 의 ``-Dfess.port`` 를 편집합니다.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80

.. note::
   서비스로 등록하는 경우 ``bin\service.bat`` 의 ``FESS_PARAMS`` 에 ``-Dfess.port=8080`` 이 하드코딩되어 있습니다. 이 값은 ``fess.in.bat`` 의 설정보다 우선되므로 포트를 변경할 때는 ``service.bat`` 의 ``FESS_PARAMS`` 도 함께 편집하십시오.

서비스 커스터마이즈（선택）
----------------------------

``service.bat install`` 을 실행하기 전에 환경 변수를 설정하면 서비스 구성을 변경할 수 있습니다. 주요 환경 변수는 다음과 같습니다.

.. list-table::
   :header-rows: 1

   * - 환경 변수
     - 설명
   * - ``FESS_START_TYPE``
     - 시작 유형（``auto`` 또는 ``manual``）. 기본값은 ``manual`` 입니다.
   * - ``FESS_HEAP_SIZE``
     - 힙 크기（예: ``1g``）. 최소·최대 힙 크기를 개별로 지정하는 경우 ``FESS_MIN_MEM``（기본값 ``256m``）과 ``FESS_MAX_MEM``（기본값 ``1g``）을 사용합니다.
   * - ``SERVICE_USERNAME`` / ``SERVICE_PASSWORD``
     - 서비스를 실행할 Windows 계정.
   * - ``SERVICE_DISPLAY_NAME``
     - 서비스 표시 이름.
   * - ``SERVICE_DESCRIPTION``
     - 서비스 설명.

등록 방법
---------

관리자 권한의 명령 프롬프트에서 ``c:\opt\fess\bin\service.bat`` 를 실행합니다.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.

서비스 설정
-----------

서비스를 수동으로 시작하는 경우 OpenSearch 서비스를 먼저 시작하고, 그 후 |Fess| 서비스를 시작합니다.
시스템 시작 시 자동으로 시작하는 경우 시작 유형과 의존 관계를 설정합니다.

1. 서비스의 일반 설정에서 시작 유형을 "자동(지연된 시작)"으로 설정합니다.
2. 서비스의 의존 관계는 레지스트리에서 설정합니다.

레지스트리 편집기(regedit)에서 다음 키와 값을 추가합니다.

.. list-table::

   * - *키*
     - ``Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService``
   * - *값*
     - ``opensearch-service-x64``

추가하면 |Fess| 서비스의 속성 의존 관계에 opensearch-service-x64가 표시됩니다.

.. note::
   ``service.bat install`` 전에 환경 변수 ``FESS_START_TYPE=auto`` 를 설정해 두면 시작 유형을 "자동"으로 등록할 수 있습니다. 다만 "자동(지연된 시작)"이나 의존 관계 설정은 ``service.bat`` 에서는 수행할 수 없으므로 위의 절차로 설정하십시오.

서비스 관리
-----------

``service.bat`` 에서 다음 명령으로 서비스를 조작할 수 있습니다.

.. list-table::
   :header-rows: 1

   * - 명령
     - 설명
   * - ``service.bat install``
     - 서비스를 등록합니다.
   * - ``service.bat remove``
     - 서비스를 삭제합니다.
   * - ``service.bat start``
     - 서비스를 시작합니다.
   * - ``service.bat stop``
     - 서비스를 정지합니다.
   * - ``service.bat manager``
     - 서비스 관리용 GUI를 시작합니다.
