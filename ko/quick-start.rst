==============
빠른 구축 가이드
==============

시작하기
========

Fess는 웹사이트와 파일 서버를 대상으로 크롤(순회)하고, 수집한 콘텐츠를 횡단 검색할 수 있는 오픈소스 전문 검색 서버입니다.

여기에서의 설명은 빠르게 Fess를 경험해보고 싶은 분을 위한 것으로, Fess를 이용하기 위한 최소한의 절차를 설명합니다.

어떤 방법을 사용할까요?
========================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * -
     - Docker (권장)
     - ZIP 패키지
   * - 사전 준비
     - Docker와 Docker Compose
     - Java 21, OpenSearch
   * - 시작의 간편함
     - ◎ 명령 몇 줄만으로 가능
     - △ 여러 소프트웨어 설치 필요
   * - 이런 분에게
     - 먼저 시도해보고 싶은 분
     - Docker를 사용할 수 없는 환경의 분

Docker로 빠른 시작 (권장)
=========================

소요 시간 목표: **초회 5〜10분 정도** (Docker 이미지 다운로드 시간 포함)

Docker는 Fess를 가장 빠르고 안정적으로 실행하는 방법을 제공합니다.
모든 의존성이 포함되어 있으므로 별도로 설치할 것이 없습니다.

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

고급 Docker 설정(커스텀 설정, 외부 OpenSearch, Kubernetes)에 대해서는
`Docker 설치 가이드 <15.6/install/install-docker>`__ 를 참조하세요.

----

ZIP 패키지로 시작
==================

소요 시간 목표: **초회 20〜30분 정도** (Java·OpenSearch 설치 시간 포함)

Docker를 사용하지 않는 경우 ZIP 패키지에서 직접 Fess를 실행할 수 있습니다.

.. note::

   이 방법은 시험용 시작 방법이므로 운용 환경 구축 절차는 Docker를 이용하는 :doc:`설치 절차 <setup>` 등을 참조하세요.
   (이 절차로 시작한 Fess는 간단한 동작 확인용으로서의 이용을 상정하고 있으며 이 환경의 운용은 권장하지 않습니다)

사전 준비
--------

Fess를 시작하기 전에 다음 소프트웨어를 설치해두세요.

**1. Java 21 설치**

Java 21은 `Eclipse Temurin <https://adoptium.net/temurin>`__ 을 권장합니다.

**2. OpenSearch 설치 및 시작**

Fess의 데이터를 저장하기 위해 OpenSearch가 필요합니다.
:doc:`설치 절차 <setup>` 를 참조하여 설치하고 시작해주세요.

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

.. warning::

   기본 비밀번호는 반드시 변경하세요.
   프로덕션 환경에서는 첫 로그인 후 즉시 비밀번호를 변경하는 것을 강력히 권장합니다.

Fess 정지 (ZIP)
---------------

Ctrl-C나 kill 명령 등으로 fess 프로세스를 정지합니다.

----

크롤 설정과 검색
================

**1. 크롤 설정 작성**

1. 관리 화면(http://localhost:8080/admin)에 로그인합니다
2. 왼쪽 메뉴의 **크롤러** > **웹** 을 클릭합니다
3. **신규 작성** 버튼을 클릭합니다
4. 다음 정보를 입력하세요:

   - **이름**: 크롤 설정 이름(예: 회사 웹사이트)
   - **URL**: 크롤 대상 URL(예: https://www.example.com/)
   - **최대 접속 수**: 10 (처음에는 작은 값을 권장)
   - **간격**: 1000 (밀리초, 기본값 ``1000`` ms를 권장)

5. **작성** 을 클릭하여 저장합니다

.. warning::

   최대 접속 수를 너무 크게 설정하면 대상 사이트에 과도한 부하를 줄 수 있습니다.
   동작 확인 시에는 반드시 작은 값(10~100 정도)부터 시작하세요.
   자신이 관리하지 않는 사이트를 크롤할 경우 robots.txt 설정에 따라 주세요.

**2. 크롤 실행**

1. **시스템** > **스케줄러** 를 클릭합니다
2. **Default Crawler** 를 찾습니다
3. **지금 시작** 버튼을 클릭합니다
4. **시스템** > **크롤 정보** 에서 진행 상황을 확인합니다

정기 실행의 경우 **Default Crawler** 를 선택하여 스케줄을 설정합니다.
시작 시간이 오전 10:35이면 ``35 10 * * ?`` 를 입력합니다 (형식: ``분 시 일 월 요일``).

**3. 검색**

크롤이 완료되면 (세션 정보에 WebIndexSize가 표시됩니다):

http://localhost:8080/ 에 접속하여 검색어를 입력하면 검색 결과가 표시됩니다.

----

더 자세히 알려면
================

- `문서 목록 <documentation>`__ - 종합 참조 가이드
- `설치 가이드 <setup>`__ - 프로덕션 배포 옵션
- `관리 가이드 <15.6/admin/index>`__ - 설정 및 관리
- `API 참조 <15.6/api/index>`__ - 검색을 애플리케이션에 통합
- `디스커션 포럼 <https://discuss.codelibs.org/c/fessja/>`__ - 질문 및 정보 공유
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__ - 버그 보고, 기능 요청
