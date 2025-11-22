==============
빌드 및 테스트
==============

이 페이지에서는 |Fess| 의 빌드 방법, 테스트 방법,
배포 패키지 생성 방법에 대해 설명합니다.

.. contents:: 목차
   :local:
   :depth: 2

빌드 시스템 개요
==================

|Fess| 는 Maven을 빌드 도구로 사용합니다.
Maven은 의존성 관리, 컴파일, 테스트, 패키징을 자동화합니다.

pom.xml
-------

Maven 설정 파일입니다. 프로젝트 루트 디렉터리에 배치되어 있습니다.

주요 설정 내용:

- 프로젝트 정보(groupId, artifactId, version)
- 의존 라이브러리
- 빌드 플러그인
- 프로파일

기본 빌드 명령
==================

클린 빌드
------------

빌드 산출물을 삭제한 후 재빌드합니다:

.. code-block:: bash

    mvn clean compile

패키지 생성
--------------

실행 가능한 JAR 파일을 생성합니다:

.. code-block:: bash

    mvn package

산출물은 ``target/`` 디렉터리에 생성됩니다:

.. code-block:: text

    target/
    ├── fess-15.3.x.jar
    └── fess-15.3.x/

전체 빌드
--------

클린, 컴파일, 테스트, 패키지를 모두 실행합니다:

.. code-block:: bash

    mvn clean package

의존성 다운로드
--------------------

의존 라이브러리를 다운로드합니다:

.. code-block:: bash

    mvn dependency:resolve

OpenSearch 플러그인 다운로드
---------------------------------

OpenSearch와 필수 플러그인을 다운로드합니다:

.. code-block:: bash

    mvn antrun:run

.. note::

   이 명령은 개발 환경 설정 시나
   플러그인을 업데이트할 때 실행합니다.

테스트
====

|Fess| 에서는 JUnit을 사용하여 테스트를 구현합니다.

단위 테스트 실행
--------------

모든 단위 테스트 실행
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test

특정 테스트 클래스 실행
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest

특정 테스트 메서드 실행
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest#testSearch

여러 테스트 클래스 실행
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    mvn test -Dtest=SearchServiceTest,CrawlerTest

테스트 건너뛰기
--------------

테스트를 건너뛰고 빌드하는 경우:

.. code-block:: bash

    mvn package -DskipTests

.. warning::

   개발 중에는 테스트를 건너뛰지 말고 반드시 실행하세요.
   PR 작성 전에는 모든 테스트가 통과하는지 확인하세요.

통합 테스트 실행
--------------

통합 테스트를 포함한 모든 테스트를 실행합니다:

.. code-block:: bash

    mvn verify

테스트 작성
============

단위 테스트 작성
--------------

테스트 클래스 배치
~~~~~~~~~~~~~~~~

테스트 클래스는 ``src/test/java/`` 이하에 배치합니다.
패키지 구조는 본체 코드와 동일하게 합니다.

.. code-block:: text

    src/
    ├── main/java/org/codelibs/fess/app/service/SearchService.java
    └── test/java/org/codelibs/fess/app/service/SearchServiceTest.java

테스트 클래스 기본 구조
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    package org.codelibs.fess.app.service;

    import org.junit.jupiter.api.Test;
    import static org.junit.jupiter.api.Assertions.*;

    public class SearchServiceTest {

        @Test
        public void testSearch() {
            // Given: 테스트 전제 조건
            SearchService service = new SearchService();
            String query = "test";

            // When: 테스트 대상 실행
            SearchResponse response = service.search(query);

            // Then: 결과 검증
            assertNotNull(response);
            assertTrue(response.getResultCount() > 0);
        }
    }

테스트 라이프사이클
~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

    import org.junit.jupiter.api.*;

    public class MyServiceTest {

        @BeforeAll
        static void setUpClass() {
            // 모든 테스트 전에 1회 실행
        }

        @BeforeEach
        void setUp() {
            // 각 테스트 전에 실행
        }

        @Test
        void testSomething() {
            // 테스트
        }

        @AfterEach
        void tearDown() {
            // 각 테스트 후에 실행
        }

        @AfterAll
        static void tearDownClass() {
            // 모든 테스트 후에 1회 실행
        }
    }

어설션
~~~~~~~~~~

JUnit 5의 어설션을 사용합니다:

.. code-block:: java

    import static org.junit.jupiter.api.Assertions.*;

    // 동등성
    assertEquals(expected, actual);
    assertNotEquals(unexpected, actual);

    // null 체크
    assertNull(obj);
    assertNotNull(obj);

    // 참/거짓
    assertTrue(condition);
    assertFalse(condition);

    // 예외
    assertThrows(IllegalArgumentException.class, () -> {
        service.doSomething();
    });

    // 컬렉션
    assertIterableEquals(expectedList, actualList);

모의 객체 사용
~~~~~~~~~~

Mockito를 사용하여 모의 객체를 생성합니다:

.. code-block:: java

    import static org.mockito.Mockito.*;
    import org.mockito.Mock;
    import org.mockito.junit.jupiter.MockitoExtension;
    import org.junit.jupiter.api.extension.ExtendWith;

    @ExtendWith(MockitoExtension.class)
    public class SearchServiceTest {

        @Mock
        private SearchEngineClient searchEngineClient;

        @Test
        public void testSearch() {
            // 모의 객체 설정
            when(searchEngineClient.search(anyString()))
                .thenReturn(new SearchResponse());

            // 테스트 실행
            SearchService service = new SearchService();
            service.setSearchEngineClient(searchEngineClient);
            SearchResponse response = service.search("test");

            // 검증
            assertNotNull(response);
            verify(searchEngineClient, times(1)).search("test");
        }
    }

테스트 커버리지
--------------

JaCoCo로 테스트 커버리지를 측정합니다:

.. code-block:: bash

    mvn clean test jacoco:report

리포트는 ``target/site/jacoco/index.html`` 에 생성됩니다.

코드 품질 검사
================

Checkstyle
----------

코딩 스타일을 검사합니다:

.. code-block:: bash

    mvn checkstyle:check

설정 파일은 ``checkstyle.xml`` 에 있습니다.

SpotBugs
--------

잠재적 버그를 검출합니다:

.. code-block:: bash

    mvn spotbugs:check

PMD
---

코드 품질 문제를 검출합니다:

.. code-block:: bash

    mvn pmd:check

모든 검사 실행
--------------------

.. code-block:: bash

    mvn clean verify checkstyle:check spotbugs:check pmd:check

배포 패키지 생성
==================

릴리스 패키지 생성
--------------------

배포용 패키지를 생성합니다:

.. code-block:: bash

    mvn clean package

생성되는 산출물:

.. code-block:: text

    target/releases/
    ├── fess-15.3.x.tar.gz      # Linux/macOS용
    ├── fess-15.3.x.zip         # Windows용
    ├── fess-15.3.x.rpm         # RPM 패키지
    └── fess-15.3.x.deb         # DEB 패키지

Docker 이미지 생성
-------------------

Docker 이미지를 생성합니다:

.. code-block:: bash

    mvn package docker:build

생성되는 이미지:

.. code-block:: bash

    docker images | grep fess

프로파일
==========

Maven 프로파일을 사용하여 환경별로 다른 설정을 적용할 수 있습니다.

개발 프로파일
--------------

개발용 설정으로 빌드합니다:

.. code-block:: bash

    mvn package -Pdev

프로덕션 프로파일
--------------

프로덕션용 설정으로 빌드합니다:

.. code-block:: bash

    mvn package -Pprod

고속 빌드
--------

테스트와 검사를 건너뛰고 빠르게 빌드합니다:

.. code-block:: bash

    mvn package -Pfast

.. warning::

   고속 빌드는 개발 중 확인용입니다.
   PR 작성 전에는 반드시 전체 빌드를 실행하세요.

CI/CD
=====

|Fess| 에서는 GitHub Actions를 사용하여 CI/CD를 실행합니다.

GitHub Actions
-------------

``.github/workflows/`` 디렉터리에 설정 파일이 있습니다.

자동 실행되는 검사:

- 빌드
- 단위 테스트
- 통합 테스트
- 코드 스타일 검사
- 코드 품질 검사

로컬 CI 검사
-----------------------

PR 작성 전에 로컬에서 CI와 동일한 검사를 실행할 수 있습니다:

.. code-block:: bash

    mvn clean verify checkstyle:check

문제 해결
====================

빌드 오류
----------

**오류: 의존성 다운로드 실패**

.. code-block:: bash

    # Maven 로컬 리포지토리 정리
    rm -rf ~/.m2/repository
    mvn clean compile

**오류: 메모리 부족**

.. code-block:: bash

    # Maven 메모리 증가
    export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512m"
    mvn clean package

**오류: Java 버전이 오래됨**

Java 21 이상을 사용하세요:

.. code-block:: bash

    java -version

테스트 오류
----------

**테스트 타임아웃**

테스트 타임아웃 시간 연장:

.. code-block:: bash

    mvn test -Dmaven.test.timeout=600

**OpenSearch가 시작되지 않음**

포트를 확인하고 사용 중인 경우 변경합니다:

.. code-block:: bash

    lsof -i :9201

의존성 문제
------------

**의존성 충돌**

의존성 트리 확인:

.. code-block:: bash

    mvn dependency:tree

특정 의존성 제외:

.. code-block:: xml

    <dependency>
        <groupId>org.example</groupId>
        <artifactId>example-lib</artifactId>
        <version>1.0</version>
        <exclusions>
            <exclusion>
                <groupId>conflicting-lib</groupId>
                <artifactId>conflicting-lib</artifactId>
            </exclusion>
        </exclusions>
    </dependency>

빌드 모범 사례
========================

정기적인 클린 빌드
--------------------

정기적으로 클린 빌드를 실행하여 빌드 캐시 문제를 회피합니다:

.. code-block:: bash

    mvn clean package

테스트 실행
----------

커밋 전에 반드시 테스트를 실행합니다:

.. code-block:: bash

    mvn test

코드 품질 검사
------------------

PR 작성 전에 코드 품질을 검사합니다:

.. code-block:: bash

    mvn checkstyle:check spotbugs:check

의존성 업데이트
------------

정기적으로 의존성을 업데이트합니다:

.. code-block:: bash

    mvn versions:display-dependency-updates

빌드 캐시 활용
--------------------

빌드 시간을 단축하기 위해 Maven 캐시를 활용합니다:

.. code-block:: bash

    # 이미 컴파일된 경우 건너뛰기
    mvn compile

Maven 명령 참조
========================

자주 사용하는 명령
--------------

.. code-block:: bash

    # 클린
    mvn clean

    # 컴파일
    mvn compile

    # 테스트
    mvn test

    # 패키지
    mvn package

    # 설치(로컬 리포지토리에 등록)
    mvn install

    # 검증(통합 테스트 포함)
    mvn verify

    # 의존성 해결
    mvn dependency:resolve

    # 의존성 트리 표시
    mvn dependency:tree

    # 프로젝트 정보 표시
    mvn help:effective-pom

다음 단계
==========

빌드 및 테스트 방법을 이해했다면 다음 문서를 참조하세요:

- :doc:`workflow` - 개발 워크플로우
- :doc:`contributing` - 기여 가이드라인
- :doc:`architecture` - 코드베이스 이해

참고 자료
======

- `Maven 공식 문서 <https://maven.apache.org/guides/>`__
- `JUnit 5 사용자 가이드 <https://junit.org/junit5/docs/current/user-guide/>`__
- `Mockito 문서 <https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html>`__
- `JaCoCo 문서 <https://www.jacoco.org/jacoco/trunk/doc/>`__
