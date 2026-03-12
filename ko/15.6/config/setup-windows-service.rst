===================
Windows 서비스 등록
===================

Windows 서비스로 등록
======================

|Fess| 를 Windows의 서비스로 등록할 수 있습니다.
|Fess| 를 실행하려면 OpenSearch를 시작해 두어야 합니다.
여기서는 |Fess| 를 ``c:\opt\fess`` 에, OpenSearch를 ``c:\opt\opensearch`` 에 설치했다고 가정합니다.

사전 준비
------

시스템 환경 변수로 JAVA_HOME을 설정하십시오.

OpenSearch를 서비스로 등록
-------------------------

| 명령 프롬프트에서 ``c:\opt\opensearch\bin\opensearch-service.bat`` 를 관리자 권한으로 실행합니다.

::

    > cd c:\opt\opensearch\bin
    > opensearch-service.bat install
    ...
    The service 'opensearch-service-x64' has been installed.

자세한 내용은 `OpenSearch 문서 <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_ 를 참조하십시오.

설정
----

``c:\opt\fess\bin\fess.in.bat`` 를 편집하여 SEARCH_ENGINE_HOME에 OpenSearch의 설치 경로를 설정합니다.

::

    set SEARCH_ENGINE_HOME=c:/opt/opensearch

|Fess| 의 검색 화면, 관리 화면의 기본 포트 번호는 8080입니다. 80번으로 변경하는 경우 ``c:\opt\fess\bin\fess.in.bat`` 의 fess.port를 변경합니다.

::

    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80


등록 방법
------

명령 프롬프트에서 ``c:\opt\fess\bin\service.bat`` 를 관리자 권한으로 실행합니다.

::

    > cd c:\opt\fess\bin
    > service.bat install
    ...
    The service 'fess-service-x64' has been installed.


서비스 설정
-----------

서비스를 수동으로 시작하는 경우 OpenSearch 서비스를 먼저 시작하고, 그 후 |Fess| 서비스를 시작합니다.
자동 시작하는 경우 의존 관계를 추가합니다.

1. 서비스의 일반 설정에서 시작 유형을 "자동(지연된 시작)"으로 설정합니다.
2. 서비스의 의존 관계는 레지스트리에서 설정합니다.

레지스트리 편집기(regedit)에서 다음 키와 값을 추가합니다.

.. list-table::

   * - *키*
     - ``컴퓨터\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services \fess-service-x64\DependOnService``
   * - *값*
     - ``opensearch-service-x64``

추가하면 |Fess| 서비스의 속성의 의존 관계에 opensearch-service-x64가 표시됩니다.
