================================================
오픈소스 전문 검색 서버 - |Fess| 개발 개요
================================================

이 페이지에서는 |Fess| 개발의 전체 모습과 개발을 시작하기 위한 기본 정보를 제공합니다.

.. contents:: 목차
   :local:
   :depth: 2

개요
====

|Fess| 는 Java로 개발된 오픈소스 전문 검색 서버입니다.
엔터프라이즈 검색을 쉽게 구축할 수 있는 것을 목표로 하며
강력한 검색 기능과 사용하기 쉬운 관리 화면을 제공합니다.

|Fess| 의 특징
-------------

- **간편한 설정**: Java 환경만 있으면 바로 시작 가능
- **강력한 크롤러**: 웹사이트, 파일 시스템, 데이터베이스 등 다양한 데이터 소스 지원
- **일본어 대응**: 일본어 전문 검색에 최적화
- **확장성**: 플러그인을 통한 기능 확장 가능
- **REST API**: 검색 기능을 다른 애플리케이션에서 이용 가능

기술 스택
==========

|Fess| 는 다음 기술을 사용하여 개발됩니다.

대상 버전
------------

이 문서는 다음 버전을 대상으로 합니다:

- **Fess**: 15.3.0
- **Java**: 21 이상
- **OpenSearch**: 3.3.0
- **Maven**: 3.x

주요 기술 및 프레임워크
----------------------

Java 21
~~~~~~~

|Fess| 는 Java 21 이상에서 동작하는 애플리케이션입니다.
최신 Java 기능을 활용하여 성능과 유지보수성을 향상시켰습니다.

- **권장**: Eclipse Temurin 21(구 AdoptOpenJDK)
- **최소 버전**: Java 21

LastaFlute
~~~~~~~~~~

`LastaFlute <https://github.com/lastaflute/lastaflute>`__ 는
|Fess| 의 웹 애플리케이션 계층에서 사용되는 프레임워크입니다.

**주요 기능:**

- DI(의존성 주입) 컨테이너
- Action 기반 웹 프레임워크
- 검증
- 메시지 관리
- 설정 관리

**학습 리소스:**

- `LastaFlute 공식 문서 <https://github.com/lastaflute/lastaflute>`__
- Fess 코드를 읽는 것으로 실전적인 사용법 학습 가능

DBFlute
~~~~~~~

`DBFlute <https://dbflute.seasar.org/>`__ 는
데이터베이스 액세스를 위한 O/R 매핑 도구입니다.
|Fess| 에서는 OpenSearch 스키마에서 Java 코드를 자동 생성하기 위해 사용합니다.

**주요 기능:**

- 타입 세이프한 SQL 빌더
- 스키마에서 코드 자동 생성
- 데이터베이스 문서 자동 생성

**학습 리소스:**

- `DBFlute 공식 사이트 <https://dbflute.seasar.org/>`__

OpenSearch
~~~~~~~~~~

`OpenSearch <https://opensearch.org/>`__ 는
|Fess| 의 검색 엔진으로 사용되는 분산 검색·분석 엔진입니다.

**지원 버전**: OpenSearch 3.3.0

**필수 플러그인:**

- opensearch-analysis-fess: Fess 전용 형태소 분석 플러그인
- opensearch-analysis-extension: 추가 언어 분석 기능
- opensearch-minhash: 유사 문서 검출
- opensearch-configsync: 설정 동기화

**학습 리소스:**

- `OpenSearch 문서 <https://opensearch.org/docs/latest/>`__

Maven
~~~~~

Maven은 |Fess| 의 빌드 도구로 사용됩니다.

**주요 용도:**

- 의존 라이브러리 관리
- 빌드 처리 실행
- 테스트 실행
- 패키지 생성

개발 도구
========

권장 개발 환경
----------------

Eclipse
~~~~~~~

공식 문서에서는 Eclipse를 사용한 개발 방법을 설명합니다.

**권장 버전**: Eclipse 2023-09 이상

**필요한 플러그인:**

- Maven Integration for Eclipse (m2e)
- Eclipse Java Development Tools

IntelliJ IDEA
~~~~~~~~~~~~~

IntelliJ IDEA에서도 개발이 가능합니다.

**권장 에디션**: Community Edition 또는 Ultimate Edition

**필요한 기능:**

- Maven 지원(기본 포함)
- Java 지원

VS Code
~~~~~~~

경량 개발에는 VS Code도 이용할 수 있습니다.

**필요한 확장 기능:**

- Java Extension Pack
- Maven for Java

버전 관리
~~~~~~~~~~~~

- **Git**: 소스 코드 관리
- **GitHub**: 리포지토리 호스팅, Issue 관리, 풀 리퀘스트

필요한 지식
========

기초 지식
--------

|Fess| 개발에는 다음 지식이 필요합니다:

**필수**

- **Java 프로그래밍**: 클래스, 인터페이스, 제네릭, 람다식 등
- **객체 지향**: 상속, 다형성, 캡슐화
- **Maven**: 기본 명령과 pom.xml 이해
- **Git**: clone, commit, push, pull, branch, merge 등

**권장**

- **LastaFlute**: Action, Form, Service 개념
- **DBFlute**: Behavior, ConditionBean 사용법
- **OpenSearch/Elasticsearch**: 인덱스, 매핑, 쿼리 기본
- **웹 개발**: HTML, CSS, JavaScript(특히 프론트엔드 개발의 경우)
- **Linux 명령**: 서버 환경에서의 개발·디버그

학습 리소스
----------

처음 |Fess| 개발에 참여하는 경우 다음 리소스가 도움이 됩니다:

공식 문서
~~~~~~~~~~~~~~

- `Fess 사용자 매뉴얼 <https://fess.codelibs.org/ja/>`__
- `Fess 관리자 가이드 <https://fess.codelibs.org/ja/15.3/admin/index.html>`__

커뮤니티
~~~~~~~~~~

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 질문 및 토론
- `Issue Tracker <https://github.com/codelibs/fess/issues>`__: 버그 보고 및 기능 요청
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 일본어 커뮤니티 포럼

소스 코드
~~~~~~~~~~

실제 코드를 읽는 것이 가장 효과적인 학습 방법입니다:

- 먼저 작은 기능부터 읽기 시작
- 디버거를 사용하여 코드 동작 추적
- 기존 테스트 코드 참조

개발 기본 플로우
==============

|Fess| 개발은 일반적으로 다음과 같은 흐름으로 진행합니다:

1. **Issue 확인·작성**

   GitHub의 Issue를 확인하고 작업할 내용을 결정합니다.
   새로운 기능이나 버그 수정의 경우 Issue를 작성합니다.

2. **브랜치 생성**

   작업용 브랜치를 생성합니다:

   .. code-block:: bash

       git checkout -b feature/my-new-feature

3. **코딩**

   기능 구현이나 버그 수정을 수행합니다.

4. **테스트**

   단위 테스트를 작성·실행하고 변경 사항이 올바르게 동작하는지 확인합니다.

5. **커밋**

   변경 사항을 커밋합니다:

   .. code-block:: bash

       git add .
       git commit -m "Add new feature"

6. **풀 리퀘스트**

   GitHub에 푸시하고 풀 리퀘스트를 작성합니다:

   .. code-block:: bash

       git push origin feature/my-new-feature

자세한 내용은 :doc:`workflow` 를 참조하세요.

프로젝트 구조 개요
==================

|Fess| 의 소스 코드는 다음과 같은 구조로 되어 있습니다:

.. code-block:: text

    fess/
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── org/codelibs/fess/
    │   │   │       ├── app/           # 웹 애플리케이션 계층
    │   │   │       │   ├── web/       # 검색 화면
    │   │   │       │   └── service/   # 서비스 계층
    │   │   │       ├── crawler/       # 크롤러 기능
    │   │   │       ├── es/            # OpenSearch 관련
    │   │   │       ├── helper/        # 헬퍼 클래스
    │   │   │       ├── job/           # 작업 처리
    │   │   │       ├── util/          # 유틸리티
    │   │   │       └── FessBoot.java  # 시작 클래스
    │   │   ├── resources/
    │   │   │   ├── fess_config.properties
    │   │   │   ├── fess_config.xml
    │   │   │   └── ...
    │   │   └── webapp/
    │   │       └── WEB-INF/
    │   │           └── view/          # JSP 파일
    │   └── test/
    │       └── java/                  # 테스트 코드
    ├── pom.xml                        # Maven 설정 파일
    └── README.md

주요 패키지
--------------

app
~~~

웹 애플리케이션 계층의 코드입니다.
관리 화면이나 검색 화면의 Action, Form, Service 등이 포함됩니다.

crawler
~~~~~~~

웹 크롤러, 파일 크롤러, 데이터 스토어 크롤러 등
데이터 수집 기능의 코드입니다.

es
~~

OpenSearch와의 연동 코드입니다.
인덱스 조작, 검색 쿼리 구축 등이 포함됩니다.

helper
~~~~~~

애플리케이션 전체에서 사용되는 헬퍼 클래스입니다.

job
~~~

스케줄 실행되는 작업의 코드입니다.
크롤 작업, 인덱스 최적화 작업 등이 포함됩니다.

자세한 내용은 :doc:`architecture` 를 참조하세요.

개발 환경 빠른 시작
=======================

최소한의 절차로 개발 환경을 설정하고 |Fess| 를 실행하는 방법을 설명합니다.

전제 조건
--------

- Java 21 이상이 설치되어 있을 것
- Git이 설치되어 있을 것
- Maven 3.x가 설치되어 있을 것

절차
----

1. **리포지토리 클론**

   .. code-block:: bash

       git clone https://github.com/codelibs/fess.git
       cd fess

2. **OpenSearch 플러그인 다운로드**

   .. code-block:: bash

       mvn antrun:run

3. **실행**

   Maven에서 실행:

   .. code-block:: bash

       mvn compile exec:java

   또는 IDE(Eclipse, IntelliJ IDEA 등)에서 ``org.codelibs.fess.FessBoot`` 클래스를 실행합니다.

4. **접속**

   브라우저에서 다음에 접속합니다:

   - 검색 화면: http://localhost:8080/
   - 관리 화면: http://localhost:8080/admin/
     - 기본 사용자: admin / admin

자세한 설정 절차는 :doc:`setup` 을 참조하세요.

개발 팁
==========

디버그 실행
----------

IDE에서 디버그 실행하는 경우 ``FessBoot`` 클래스를 실행합니다.
브레이크포인트를 설정함으로써 코드의 동작을 자세히 추적할 수 있습니다.

핫 디플로이
------------

LastaFlute는 일부 변경에 대해 재시작 없이 반영할 수 있습니다.
다만 클래스 구조 변경 등은 재시작이 필요합니다.

로그 확인
--------

로그는 ``target/fess/logs/`` 디렉터리에 출력됩니다.
문제가 발생한 경우 로그 파일을 확인하세요.

OpenSearch 조작
----------------

내장 OpenSearch는 ``target/fess/es/`` 에 배치됩니다.
직접 OpenSearch API를 호출하여 디버그할 수도 있습니다:

.. code-block:: bash

    # 인덱스 확인
    curl -X GET http://localhost:9201/_cat/indices?v

    # 문서 검색
    curl -X GET http://localhost:9201/fess.search/_search?pretty

커뮤니티 및 지원
==================

질문 및 상담
--------

개발 중 질문이나 상담이 있는 경우 다음을 이용하세요:

- `GitHub Discussions <https://github.com/codelibs/fess/discussions>`__: 일반적인 질문 및 토론
- `GitHub Issues <https://github.com/codelibs/fess/issues>`__: 버그 보고 및 기능 요청
- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__: 일본어 포럼

기여 방법
--------

|Fess| 에 대한 기여 방법은 :doc:`contributing` 을 참조하세요.

다음 단계
==========

개발 환경 설정 준비가 되었다면 :doc:`setup` 으로 진행하세요.

자세한 정보는 다음 문서도 참조하세요:

- :doc:`architecture` - 아키텍처 및 코드 구조
- :doc:`workflow` - 개발 워크플로우
- :doc:`building` - 빌드 및 테스트
- :doc:`contributing` - 기여 가이드

참고 자료
========

공식 리소스
----------

- `Fess 공식 사이트 <https://fess.codelibs.org/ja/>`__
- `GitHub 리포지토리 <https://github.com/codelibs/fess>`__
- `다운로드 페이지 <https://fess.codelibs.org/ja/downloads.html>`__

기술 문서
--------------

- `LastaFlute <https://github.com/lastaflute/lastaflute>`__
- `DBFlute <https://dbflute.seasar.org/>`__
- `OpenSearch <https://opensearch.org/docs/latest/>`__

커뮤니티
----------

- `Fess Forum <https://discuss.codelibs.org/c/FessJA>`__
- `Twitter: @codelibs <https://twitter.com/codelibs>`__
