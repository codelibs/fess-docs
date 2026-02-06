==============
빠른 구축 가이드
==============

시작하기
========

여기에서의 설명은 빠르게 Fess를 경험해보고 싶은 분을 위한 것입니다.
Fess를 이용하기 위한 최소한의 절차를 설명합니다.

.. tip::

   **가장 빠른 방법: Docker (권장)**

   Docker가 설치되어 있다면 몇 가지 명령만으로 약 3분 만에 Fess를 실행할 수 있습니다.
   다른 의존성을 설치할 필요가 없습니다.

----

Docker로 빠른 시작 (권장)
=========================

Docker는 Fess를 가장 빠르고 안정적으로 실행하는 방법을 제공합니다.
모든 의존성이 포함되어 있으므로 별도로 설치할 것이 없습니다.

**요구 사항:**

- Docker 20.10 이상
- Docker Compose 2.0 이상

**Step 1: Docker Compose 파일 다운로드**

.. code-block:: bash

    mkdir fess-docker && cd fess-docker
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose.yaml
    curl -OL https://raw.githubusercontent.com/codelibs/docker-fess/master/compose/compose-opensearch3.yaml

**Step 2: 컨테이너 시작**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

**Step 3: 시작 확인**

서비스가 초기화될 때까지 몇 분 정도 기다린 후 브라우저에서 접속합니다:

- **검색 화면:** http://localhost:8080/
- **관리 화면:** http://localhost:8080/admin
- **기본 관리자 계정:** admin / admin

.. warning::

   **보안 안내:** 첫 로그인 후 기본 관리자 비밀번호를 즉시 변경하세요.

**Step 4: 중지**

.. code-block:: bash

    docker compose -f compose.yaml -f compose-opensearch3.yaml down

.. note::

   고급 Docker 설정(커스텀 설정, 외부 OpenSearch, Kubernetes)에 대해서는
   `Docker 설치 가이드 <15.5/install/install-docker.html>`__ 를 참조하세요.

----

ZIP 패키지로 시작
==================

Docker를 사용하지 않는 경우 ZIP 패키지에서 직접 Fess를 실행할 수 있습니다.

.. note::

   이 방법은 시험용 시작 방법이므로 운용 환경 구축 절차는 Docker를 이용하는 :doc:`설치 절차 <setup>` 등을 참조하세요.
   (이 절차로 시작한 Fess는 간단한 동작 확인용으로서의 이용을 상정하고 있으며 이 환경의 운용은 권장하지 않습니다)

사전 준비
--------

Fess를 시작하기 전에 Java 21을 설치해두세요.
Java 21은 `Eclipse Temurin <https://adoptium.net/temurin>`__ 을 권장합니다.

Java 설치를 확인합니다:

.. code-block:: bash

    java -version

다운로드
--------

`GitHub 릴리스 사이트 <https://github.com/codelibs/fess/releases>`__ 에서 최신 Fess의 ZIP 패키지를 다운로드합니다.

설치
--------

다운로드한 fess-x.y.z.zip을 압축 해제합니다.

.. code-block:: bash

    unzip fess-x.y.z.zip
    cd fess-x.y.z

Fess 시작
---------

.. code-block:: bash

    # Linux/Mac
    ./bin/fess

    # Windows
    bin\fess.bat

약 30초 후 다음 주소에 접속할 수 있습니다:

- http://localhost:8080/ (검색)
- http://localhost:8080/admin (관리 화면 - 로그인: admin/admin)

Fess 정지
---------

Ctrl-C나 kill 명령 등으로 fess 프로세스를 정지합니다.

----

첫 검색: 빠른 튜토리얼
========================

Fess가 실행되었으므로 첫 웹 크롤을 설정해 봅시다.

Step 1: 크롤 설정 작성
------------------------

1. 관리 화면(http://localhost:8080/admin)에 로그인합니다
2. 왼쪽 메뉴의 **크롤러** > **웹** 을 클릭합니다
3. **신규 작성** 버튼을 클릭합니다
4. 다음 정보를 입력하세요:

   - **이름**: 크롤 설정 이름(예: 회사 웹사이트)
   - **URL**: 크롤 대상 URL(예: https://fess.codelibs.org/)
   - **최대 접속 수**: 100 (크롤할 페이지 수 상한)
   - **간격**: 1000 (밀리초)

5. **작성** 을 클릭하여 저장합니다

Step 2: 크롤 실행
------------------

1. **시스템** > **스케줄러** 를 클릭합니다
2. **Default Crawler** 를 찾습니다
3. **지금 시작** 버튼을 클릭합니다
4. **시스템** > **크롤 정보** 에서 진행 상황을 확인합니다

Step 3: 검색
--------------

크롤이 완료되면 (세션 정보에 WebIndexSize가 표시됩니다):

1. http://localhost:8080/ 에 접속합니다
2. 크롤한 페이지와 관련된 검색어를 입력합니다
3. 검색 결과를 확인합니다!

----

더 자세히 알려면
==================

**더 깊이 알아보고 싶으신가요?**

- `문서 목록 <documentation.html>`__ - 종합 참조 가이드
- `설치 가이드 <setup.html>`__ - 프로덕션 배포 옵션
- `관리 가이드 <15.5/admin/index.html>`__ - 설정 및 관리
- `API 참조 <15.5/api/index.html>`__ - 검색을 애플리케이션에 통합

**도움이 필요하시면:**

- `디스커션 포럼 <https://discuss.codelibs.org/c/fessja/>`__ - 질문 및 정보 공유
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - 버그 보고, 기능 요청
- `상용 지원 <support-services.html>`__ - 전문 지원
