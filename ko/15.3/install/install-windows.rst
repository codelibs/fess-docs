====================================
Windows 설치 (상세 절차)
====================================

이 페이지에서는 Windows 환경에 |Fess| 를 설치하는 절차를 설명합니다.
ZIP 패키지를 사용한 설치 방법에 대해 기재하고 있습니다.

.. warning::

   운영 환경에서는 내장 OpenSearch를 사용한 운영을 권장하지 않습니다.
   반드시 외부 OpenSearch 서버를 구축하시기 바랍니다.

전제 조건
========

- :doc:`prerequisites` 에 기재된 시스템 요구사항을 충족할 것
- Java 21이 설치되어 있을 것
- OpenSearch 3.3.2를 사용 가능한 상태로 할 것(또는 신규 설치)
- Windows 환경 변수 ``JAVA_HOME`` 이 적절히 설정되어 있을 것

Java 설치 확인
====================

명령 프롬프트 또는 PowerShell을 열고 다음 명령으로 Java 버전을 확인합니다.

명령 프롬프트의 경우::

    C:\> java -version

PowerShell의 경우::

    PS C:\> java -version

Java 21 이상이 표시되는지 확인하십시오.

환경 변수 설정
============

1. ``JAVA_HOME`` 환경 변수 설정

   Java가 설치된 디렉터리를 ``JAVA_HOME`` 으로 설정합니다.

   예::

       JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.1.12-hotspot

2. ``PATH`` 환경 변수에 추가

   ``%JAVA_HOME%\bin`` 을 ``PATH`` 환경 변수에 추가합니다.

.. tip::

   환경 변수 설정 방법:

   1. "시작" 메뉴에서 "설정" 열기
   2. "시스템"→"정보"→"고급 시스템 설정" 클릭
   3. "환경 변수" 버튼 클릭
   4. "시스템 환경 변수" 또는 "사용자 환경 변수"에서 설정

단계 1: OpenSearch 설치
===================================

OpenSearch 다운로드
-----------------------

1. `Download OpenSearch <https://opensearch.org/downloads.html>`__ 에서 Windows용 ZIP 패키지를 다운로드합니다.

2. 다운로드한 ZIP 파일을 임의의 디렉터리에 압축 해제합니다.

   예::

       C:\opensearch-3.3.2

   .. note::

      경로에 한국어나 공백 문자가 포함되지 않은 디렉터리를 선택할 것을 권장합니다.

OpenSearch 플러그인 설치
---------------------------------

명령 프롬프트를 **관리자 권한으로** 열고 다음 명령을 실행합니다.

::

    C:\> cd C:\opensearch-3.3.2
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.3.1
    C:\opensearch-3.3.2> bin\opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.3.1

.. important::

   플러그인 버전은 OpenSearch 버전과 일치시켜야 합니다.
   위의 예제에서는 모두 3.3.2를 지정하고 있습니다.

OpenSearch 설정
---------------

``config\opensearch.yml`` 을 텍스트 편집기로 열고 다음 설정을 추가합니다.

::

    # 설정 동기화용 경로(절대 경로로 지정)
    configsync.config_path: C:/opensearch-3.3.2/data/config/

    # 보안 플러그인 비활성화(개발 환경 전용)
    plugins.security.disabled: true

.. warning::

   **보안 관련 중요 주의사항**

   ``plugins.security.disabled: true`` 는 개발 환경이나 테스트 환경에서만 사용하십시오.
   운영 환경에서는 OpenSearch의 보안 플러그인을 활성화하고 적절한 인증·권한 설정을 수행하십시오.
   자세한 내용은 :doc:`security` 를 참조하십시오.

.. note::

   Windows의 경우 경로 구분 문자는 ``\`` 가 아닌 ``/`` 를 사용하십시오.
   ``C:\opensearch-3.3.2\data\config\`` 가 아니라 ``C:/opensearch-3.3.2/data/config/`` 로 기술합니다.

.. tip::

   기타 권장 설정::

       cluster.name: fess-cluster
       node.name: fess-node-1
       network.host: 0.0.0.0
       discovery.type: single-node

단계 2: Fess 설치
=============================

Fess 다운로드
-----------------

1. `다운로드 사이트 <https://fess.codelibs.org/ko/downloads.html>`__ 에서 Windows용 ZIP 패키지를 다운로드합니다.

2. 다운로드한 ZIP 파일을 임의의 디렉터리에 압축 해제합니다.

   예::

       C:\fess-15.3.2

   .. note::

      경로에 한국어나 공백 문자가 포함되지 않은 디렉터리를 선택할 것을 권장합니다.

Fess 설정
----------

``bin\fess.in.bat`` 을 텍스트 편집기로 열고 다음 설정을 추가하거나 변경합니다.

::

    set SEARCH_ENGINE_HTTP_URL=http://localhost:9200
    set FESS_DICTIONARY_PATH=C:/opensearch-3.3.2/data/config/

.. note::

   - OpenSearch를 다른 호스트에서 실행하는 경우 ``SEARCH_ENGINE_HTTP_URL`` 을 적절한 호스트 이름 또는 IP 주소로 변경하십시오.
   - 경로 구분 문자는 ``/`` 를 사용하십시오.

설치 확인
----------------

설정 파일이 올바르게 편집되었는지 확인합니다.

명령 프롬프트에서::

    C:\> findstr "SEARCH_ENGINE_HTTP_URL" C:\fess-15.3.2\bin\fess.in.bat
    C:\> findstr "FESS_DICTIONARY_PATH" C:\fess-15.3.2\bin\fess.in.bat

단계 3: 시작
==============

시작 절차는 :doc:`run` 을 참조하십시오.

Windows 서비스로 등록(옵션)
=======================================

|Fess| 및 OpenSearch를 Windows 서비스로 등록하면 시스템 시작 시 자동으로 시작되도록 설정할 수 있습니다.

.. note::

   Windows 서비스로 등록하려면 타사 도구(NSSM 등)를 사용해야 합니다.
   자세한 절차는 각 도구의 문서를 참조하십시오.

NSSM 사용 예
----------------

1. `NSSM (Non-Sucking Service Manager) <https://nssm.cc/download>`__ 를 다운로드하여 압축 해제합니다.

2. OpenSearch를 서비스로 등록::

       C:\> nssm install OpenSearch C:\opensearch-3.3.2\bin\opensearch.bat

3. Fess를 서비스로 등록::

       C:\> nssm install Fess C:\fess-15.3.2\bin\fess.bat

4. 서비스 종속성 설정(Fess는 OpenSearch에 종속)::

       C:\> sc config Fess depend= OpenSearch

5. 서비스 시작::

       C:\> net start OpenSearch
       C:\> net start Fess

방화벽 설정
==================

Windows Defender 방화벽에서 필요한 포트를 개방합니다.

1. "제어판"→"Windows Defender 방화벽"→"고급 설정" 열기

2. "인바운드 규칙"에서 새 규칙 만들기

   - 규칙 유형: 포트
   - 프로토콜 및 포트: TCP, 8080
   - 작업: 연결 허용
   - 이름: Fess Web Interface

또는 PowerShell에서 실행::

    PS C:\> New-NetFirewallRule -DisplayName "Fess Web Interface" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow

문제 해결
====================

포트 번호 충돌
--------------

포트 8080 또는 9200이 이미 사용 중인 경우 다음 명령으로 확인할 수 있습니다::

    C:\> netstat -ano | findstr :8080
    C:\> netstat -ano | findstr :9200

사용 중인 포트 번호를 변경하거나 충돌하는 프로세스를 중지하십시오.

경로 길이 제한
------------

Windows에서는 경로 길이에 제한이 있습니다. 가능한 한 짧은 경로에 설치할 것을 권장합니다.

예::

    C:\opensearch  (권장)
    C:\Program Files\opensearch-3.3.2  (비권장 - 경로가 김)

Java가 인식되지 않음
-----------------

``java -version`` 명령에서 오류가 표시되는 경우:

1. ``JAVA_HOME`` 환경 변수가 올바르게 설정되어 있는지 확인
2. ``PATH`` 환경 변수에 ``%JAVA_HOME%\bin`` 이 포함되어 있는지 확인
3. 명령 프롬프트를 재시작하여 설정 반영

다음 단계
==========

설치가 완료되면 다음 문서를 참조하십시오:

- :doc:`run` - |Fess| 시작 및 초기 설정
- :doc:`security` - 운영 환경의 보안 설정
- :doc:`troubleshooting` - 문제 해결

자주 묻는 질문
==========

Q: Windows Server에서의 운영이 권장됩니까?
------------------------------------------

A: 예, Windows Server에서의 운영이 가능합니다.
Windows Server에서 운영하는 경우 Windows 서비스로 등록하고 적절한 모니터링을 설정하십시오.

Q: 64비트 버전과 32비트 버전의 차이는?
------------------------------------

A: |Fess| 및 OpenSearch는 64비트 버전만 지원합니다.
32비트 버전의 Windows에서는 작동하지 않습니다.

Q: 경로에 한국어가 포함된 경우 대처 방법은?
--------------------------------------

A: 가능한 한 한국어나 공백 문자가 포함되지 않은 경로에 설치하십시오.
어쩔 수 없이 한국어 경로를 사용해야 하는 경우 설정 파일에서 경로를 적절히 이스케이프해야 합니다.
