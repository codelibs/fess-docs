====================
개발 환경 설정
====================

이 페이지에서는 |Fess| 개발 환경을 구축하는 절차를 자세히 설명합니다.
IDE 선택부터 소스 코드 취득, 실행, 디버그까지
단계별로 해설합니다.

.. contents:: 목차
   :local:
   :depth: 2

시스템 요구사항
==========

개발 환경에는 다음 하드웨어 요구사항을 권장합니다.

하드웨어 요구사항
--------------

- **CPU**: 4코어 이상
- **메모리**: 8GB 이상(16GB 권장)
- **디스크**: 20GB 이상의 여유 공간

.. note::

   개발 중에는 |Fess| 본체와 내장 OpenSearch가 동시에 동작하므로
   충분한 메모리와 디스크 용량을 확보하세요.

소프트웨어 요구사항
--------------

- **OS**: Windows 10/11, macOS 11 이상, Linux(Ubuntu 20.04 이상 등)
- **Java**: JDK 21 이상
- **Maven**: 3.x 이상
- **Git**: 2.x 이상
- **IDE**: Eclipse, IntelliJ IDEA, VS Code 등

필수 소프트웨어 설치
==========================

Java 설치
-----------------

|Fess| 개발에는 Java 21 이상이 필요합니다.

Eclipse Temurin 설치(권장)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Eclipse Temurin(구 AdoptOpenJDK)을 권장합니다.

1. `Adoptium <https://adoptium.net/temurin/releases/>`__ 에 접속
2. Java 21 LTS 버전 다운로드
3. 설치 프로그램 지시에 따라 설치

설치 확인
~~~~~~~~~~~~~~

터미널 또는 명령 프롬프트에서 다음을 실행:

.. code-block:: bash

    java -version

다음과 같은 출력이 표시되면 성공입니다:

.. code-block:: text

    openjdk version "21.0.x" 2024-xx-xx LTS
    OpenJDK Runtime Environment Temurin-21.0.x+x (build 21.0.x+x-LTS)
    OpenJDK 64-Bit Server VM Temurin-21.0.x+x (build 21.0.x+x-LTS, mixed mode, sharing)

환경 변수 설정
~~~~~~~~~~~~

**Linux/macOS:**

``~/.bashrc`` 또는 ``~/.zshrc`` 에 다음을 추가:

.. code-block:: bash

    export JAVA_HOME=/path/to/java21
    export PATH=$JAVA_HOME/bin:$PATH

**Windows:**

1. "시스템 환경 변수 편집" 열기
2. "환경 변수" 클릭
3. ``JAVA_HOME`` 추가: ``C:\Program Files\Eclipse Adoptium\jdk-21.x.x.x-hotspot``
4. ``PATH`` 에 ``%JAVA_HOME%\bin`` 추가

Maven 설치
------------------

Maven 3.x 이상을 설치합니다.

다운로드 및 설치
~~~~~~~~~~~~~~~~~~~~~~~~

1. `Maven 다운로드 페이지 <https://maven.apache.org/download.cgi>`__ 에 접속
2. Binary zip/tar.gz archive 다운로드
3. 압축 해제하고 적절한 위치에 배치

**Linux/macOS:**

.. code-block:: bash

    tar xzvf apache-maven-3.x.x-bin.tar.gz
    sudo mv apache-maven-3.x.x /opt/
    sudo ln -s /opt/apache-maven-3.x.x /opt/maven

**Windows:**

1. ZIP 파일 압축 해제
2. ``C:\Program Files\Apache\maven`` 등에 배치

환경 변수 설정
~~~~~~~~~~~~

**Linux/macOS:**

``~/.bashrc`` 또는 ``~/.zshrc`` 에 다음을 추가:

.. code-block:: bash

    export MAVEN_HOME=/opt/maven
    export PATH=$MAVEN_HOME/bin:$PATH

**Windows:**

1. ``MAVEN_HOME`` 추가: ``C:\Program Files\Apache\maven``
2. ``PATH`` 에 ``%MAVEN_HOME%\bin`` 추가

설치 확인
~~~~~~~~~~~~~~

.. code-block:: bash

    mvn -version

다음과 같은 출력이 표시되면 성공입니다:

.. code-block:: text

    Apache Maven 3.x.x
    Maven home: /opt/maven
    Java version: 21.0.x, vendor: Eclipse Adoptium

Git 설치
----------------

Git이 설치되어 있지 않은 경우 다음에서 설치합니다.

- **Windows**: `Git for Windows <https://git-scm.com/download/win>`__
- **macOS**: ``brew install git`` 또는 `Git 다운로드 페이지 <https://git-scm.com/download/mac>`__
- **Linux**: ``sudo apt install git`` (Ubuntu/Debian) 또는 ``sudo yum install git`` (RHEL/CentOS)

설치 확인:

.. code-block:: bash

    git --version

IDE 설정
===============

Eclipse의 경우
------------

Eclipse는 |Fess| 공식 문서에서 권장하는 IDE입니다.

Eclipse 설치
~~~~~~~~~~~~~~~~~~~~

1. `Eclipse 다운로드 페이지 <https://www.eclipse.org/downloads/>`__ 에 접속
2. "Eclipse IDE for Enterprise Java and Web Developers" 다운로드
3. 설치 프로그램을 실행하고 지시에 따라 설치

권장 플러그인
~~~~~~~~~~~~

Eclipse에는 다음 플러그인이 기본적으로 포함되어 있습니다:

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

프로젝트 가져오기
~~~~~~~~~~~~~~~~~~~~

1. Eclipse 시작
2. ``File`` > ``Import`` 선택
3. ``Maven`` > ``Existing Maven Projects`` 선택
4. Fess 소스 코드 디렉터리 지정
5. ``Finish`` 클릭

실행 구성 설정
~~~~~~~~~~~~

1. ``Run`` > ``Run Configurations...`` 선택
2. ``Java Application`` 을 우클릭하고 ``New Configuration`` 선택
3. 다음을 설정:

   - **Name**: Fess Boot
   - **Project**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``

4. ``Apply`` 클릭

IntelliJ IDEA의 경우
-------------------

IntelliJ IDEA도 널리 사용되는 IDE입니다.

IntelliJ IDEA 설치
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. `IntelliJ IDEA 다운로드 페이지 <https://www.jetbrains.com/idea/download/>`__ 에 접속
2. Community Edition(무료) 또는 Ultimate Edition 다운로드
3. 설치 프로그램을 실행하고 지시에 따라 설치

프로젝트 가져오기
~~~~~~~~~~~~~~~~~~~~

1. IntelliJ IDEA 시작
2. ``Open`` 선택
3. Fess 소스 코드 디렉터리의 ``pom.xml`` 선택
4. ``Open as Project`` 클릭
5. Maven 프로젝트로 자동 가져오기됨

실행 구성 설정
~~~~~~~~~~~~

1. ``Run`` > ``Edit Configurations...`` 선택
2. ``+`` 버튼을 클릭하고 ``Application`` 선택
3. 다음을 설정:

   - **Name**: Fess Boot
   - **Module**: fess
   - **Main class**: ``org.codelibs.fess.FessBoot``
   - **JRE**: Java 21

4. ``OK`` 클릭

VS Code의 경우
------------

경량 개발 환경을 선호하는 경우 VS Code도 선택 가능합니다.

VS Code 설치
~~~~~~~~~~~~~~~~~~~~

1. `VS Code 다운로드 페이지 <https://code.visualstudio.com/>`__ 에 접속
2. 설치 프로그램 다운로드 및 실행

필수 확장 기능 설치
~~~~~~~~~~~~~~~~~~~~~~~~

다음 확장 기능을 설치합니다:

- **Extension Pack for Java**: Java 개발에 필요한 확장 기능 세트
- **Maven for Java**: Maven 지원

프로젝트 열기
~~~~~~~~~~~~~~~~

1. VS Code 시작
2. ``File`` > ``Open Folder`` 선택
3. Fess 소스 코드 디렉터리 선택

소스 코드 취득
==============

GitHub에서 클론
-------------------

|Fess| 소스 코드를 GitHub에서 클론합니다.

.. code-block:: bash

    git clone https://github.com/codelibs/fess.git
    cd fess

SSH를 사용하는 경우:

.. code-block:: bash

    git clone git@github.com:codelibs/fess.git
    cd fess

.. tip::

   포크하여 개발하는 경우 먼저 GitHub에서 Fess 리포지토리를 포크하고
   포크한 리포지토리를 클론합니다:

   .. code-block:: bash

       git clone https://github.com/YOUR_USERNAME/fess.git
       cd fess
       git remote add upstream https://github.com/codelibs/fess.git

프로젝트 빌드
==================

OpenSearch 플러그인 다운로드
---------------------------------

Fess 실행에는 OpenSearch용 플러그인이 필요합니다.
다음 명령으로 다운로드합니다:

.. code-block:: bash

    mvn antrun:run

이 명령은 다음을 실행합니다:

- OpenSearch 다운로드
- 필수 플러그인 다운로드 및 설치
- OpenSearch 설정

.. note::

   이 명령은 처음 한 번만 실행하거나 플러그인을 업데이트할 때 실행합니다.
   매번 실행할 필요는 없습니다.

초기 빌드
--------

프로젝트를 빌드합니다:

.. code-block:: bash

    mvn clean compile

초기 빌드는 시간이 걸릴 수 있습니다(의존 라이브러리 다운로드 등).

빌드가 성공하면 다음과 같은 메시지가 표시됩니다:

.. code-block:: text

    [INFO] BUILD SUCCESS
    [INFO] Total time: xx:xx min
    [INFO] Finished at: 2024-xx-xxTxx:xx:xx+09:00

Fess 실행
==========

명령줄에서 실행
--------------------

Maven을 사용하여 실행:

.. code-block:: bash

    mvn compile exec:java

또는 패키징 후 실행:

.. code-block:: bash

    mvn package
    java -jar target/fess-15.3.x.jar

IDE에서 실행
------------

Eclipse의 경우
~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` 클래스를 우클릭
2. ``Run As`` > ``Java Application`` 선택

또는 생성한 실행 구성 사용:

1. 툴바의 실행 버튼 드롭다운 클릭
2. ``Fess Boot`` 선택

IntelliJ IDEA의 경우
~~~~~~~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` 클래스를 우클릭
2. ``Run 'FessBoot.main()'`` 선택

또는 생성한 실행 구성 사용:

1. 툴바의 실행 버튼 드롭다운 클릭
2. ``Fess Boot`` 선택

VS Code의 경우
~~~~~~~~~~~~

1. ``src/main/java/org/codelibs/fess/FessBoot.java`` 열기
2. ``Run`` 메뉴에서 ``Run Without Debugging`` 선택

시작 확인
--------

Fess 시작에는 1~2분이 소요됩니다.
콘솔에 다음과 같은 로그가 표시되면 시작 완료입니다:

.. code-block:: text

    [INFO] Boot Thread: Boot process completed successfully.

브라우저에서 다음에 접속하여 동작 확인:

- **검색 화면**: http://localhost:8080/
- **관리 화면**: http://localhost:8080/admin/

  - 기본 사용자: ``admin``
  - 기본 비밀번호: ``admin``

포트 번호 변경
--------------

기본 포트 8080이 사용 중인 경우 다음 파일에서 변경할 수 있습니다:

``src/main/resources/fess_config.properties``

.. code-block:: properties

    # 포트 번호 변경
    server.port=8080

디버그 실행
==========

IDE에서 디버그 실행
------------------

Eclipse의 경우
~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` 클래스를 우클릭
2. ``Debug As`` > ``Java Application`` 선택
3. 브레이크포인트를 설정하고 코드 동작 추적

IntelliJ IDEA의 경우
~~~~~~~~~~~~~~~~~~

1. ``org.codelibs.fess.FessBoot`` 클래스를 우클릭
2. ``Debug 'FessBoot.main()'`` 선택
3. 브레이크포인트를 설정하고 코드 동작 추적

VS Code의 경우
~~~~~~~~~~~~

1. ``src/main/java/org/codelibs/fess/FessBoot.java`` 열기
2. ``Run`` 메뉴에서 ``Start Debugging`` 선택

원격 디버그
--------------

명령줄에서 시작한 Fess에 디버거를 연결할 수도 있습니다.

Fess를 디버그 모드로 시작:

.. code-block:: bash

    mvn compile exec:java -Dexec.args="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

IDE에서 원격 디버그 연결:

**Eclipse:**

1. ``Run`` > ``Debug Configurations...`` 선택
2. ``Remote Java Application`` 을 우클릭하고 ``New Configuration`` 선택
3. ``Port: 5005`` 설정
4. ``Debug`` 클릭

**IntelliJ IDEA:**

1. ``Run`` > ``Edit Configurations...`` 선택
2. ``+`` > ``Remote JVM Debug`` 선택
3. ``Port: 5005`` 설정
4. ``OK`` 클릭하고 ``Debug`` 실행

개발에 유용한 설정
==============

로그 레벨 변경
--------------

디버그 시 로그 레벨을 변경하면 상세 정보를 확인할 수 있습니다.

``src/main/resources/log4j2.xml`` 편집:

.. code-block:: xml

    <Configuration status="INFO">
        <Loggers>
            <Logger name="org.codelibs.fess" level="DEBUG"/>
            <Root level="INFO">
                <AppenderRef ref="console"/>
            </Root>
        </Loggers>
    </Configuration>

핫 디플로이 활성화
-------------------

LastaFlute는 일부 변경에 대해 재시작 없이 반영할 수 있습니다.

``src/main/resources/fess_config.properties`` 에서 다음을 설정:

.. code-block:: properties

    # 핫 디플로이 활성화
    development.here=true

다만 다음 변경은 재시작이 필요합니다:

- 클래스 구조 변경(메서드 추가·삭제 등)
- 설정 파일 변경
- 의존 라이브러리 변경

내장 OpenSearch 조작
------------------------

개발 환경에서는 내장 OpenSearch가 사용됩니다.

OpenSearch 배치 위치:

.. code-block:: text

    target/fess/es/

OpenSearch API 직접 접속:

.. code-block:: bash

    # 인덱스 목록
    curl -X GET http://localhost:9201/_cat/indices?v

    # 문서 검색
    curl -X GET http://localhost:9201/fess.search/_search?pretty

    # 매핑 확인
    curl -X GET http://localhost:9201/fess.search/_mapping?pretty

외부 OpenSearch 사용
--------------------

외부 OpenSearch 서버를 사용하는 경우
``src/main/resources/fess_config.properties`` 편집:

.. code-block:: properties

    # 내장 OpenSearch 비활성화
    opensearch.cluster.name=fess
    opensearch.http.url=http://localhost:9200

DBFlute 코드 생성
======================

|Fess| 는 DBFlute를 사용하여 OpenSearch 스키마에서
Java 코드를 자동 생성합니다.

스키마가 변경된 경우 재생성
----------------------------

OpenSearch 매핑을 변경한 경우 다음 명령으로
해당 Java 코드를 재생성합니다:

.. code-block:: bash

    rm -rf mydbflute
    mvn antrun:run
    mvn dbflute:freegen
    mvn license:format

각 명령 설명:

- ``rm -rf mydbflute``: 기존 DBFlute 작업 디렉터리 삭제
- ``mvn antrun:run``: OpenSearch 플러그인 다운로드
- ``mvn dbflute:freegen``: 스키마에서 Java 코드 생성
- ``mvn license:format``: 라이센스 헤더 추가

문제 해결
==================

빌드 오류
----------

**오류: Java 버전이 오래됨**

.. code-block:: text

    [ERROR] Failed to execute goal ... requires at least Java 21

해결 방법: Java 21 이상을 설치하고 ``JAVA_HOME`` 을 적절히 설정하세요.

**오류: 의존 라이브러리 다운로드 실패**

.. code-block:: text

    [ERROR] Failed to collect dependencies

해결 방법: 네트워크 연결을 확인하고 Maven 로컬 리포지토리를 정리한 후 재시도:

.. code-block:: bash

    rm -rf ~/.m2/repository
    mvn clean compile

실행 오류
--------

**오류: 포트 8080이 이미 사용 중**

.. code-block:: text

    Address already in use

해결 방법:

1. 포트 8080을 사용하는 프로세스 종료
2. 또는 ``fess_config.properties`` 에서 포트 번호 변경

**오류: OpenSearch가 시작되지 않음**

로그 파일 ``target/fess/es/logs/`` 를 확인하세요.

자주 발생하는 원인:

- 메모리 부족: JVM 힙 크기 증가
- 포트 9201 사용 중: 포트 번호 변경
- 디스크 용량 부족: 디스크 용량 확보

IDE에서 프로젝트가 인식되지 않음
----------------------------

**Maven 프로젝트 업데이트**

- **Eclipse**: 프로젝트 우클릭 > ``Maven`` > ``Update Project``
- **IntelliJ IDEA**: ``Maven`` 툴 윈도우에서 ``Reload All Maven Projects`` 클릭
- **VS Code**: 명령 팔레트에서 ``Java: Clean Java Language Server Workspace`` 실행

다음 단계
==========

개발 환경 설정이 완료되면 다음 문서를 참조하세요:

- :doc:`architecture` - 코드 구조 이해
- :doc:`workflow` - 개발 워크플로우 학습
- :doc:`building` - 빌드 및 테스트 방법
- :doc:`contributing` - 풀 리퀘스트 작성

리소스
========

- `Eclipse 다운로드 <https://www.eclipse.org/downloads/>`__
- `IntelliJ IDEA 다운로드 <https://www.jetbrains.com/idea/download/>`__
- `VS Code 다운로드 <https://code.visualstudio.com/>`__
- `Maven 문서 <https://maven.apache.org/guides/>`__
- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
