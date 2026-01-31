==================================
플러그인 아키텍처
==================================

개요
====

|Fess| 의 플러그인 시스템을 통해 코어 기능을 확장할 수 있습니다.
플러그인은 JAR 파일로 배포되며 동적으로 로드됩니다.

플러그인 종류
================

|Fess| 는 다음 종류의 플러그인을 지원합니다:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 종류
     - 설명
   * - 데이터스토어
     - 새로운 데이터 소스에서 콘텐츠 취득 (Box, Slack 등)
   * - 스크립트 엔진
     - 새로운 스크립트 언어 지원
   * - 웹앱
     - 웹 인터페이스 확장
   * - Ingest
     - 인덱싱 시 데이터 가공

플러그인 구조
==============

기본 구조
--------

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/java/org/codelibs/fess/ds/example/
        ├── ExampleDataStore.java      # 데이터스토어 구현
        └── ExampleDataStoreHandler.java # 핸들러 (옵션)

pom.xml 예시
-----------

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.5.0</version>
        <packaging>jar</packaging>

        <name>fess-ds-example</name>
        <description>Example DataStore for Fess</description>

        <properties>
            <fess.version>15.5.0</fess.version>
            <java.version>21</java.version>
        </properties>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <version>${fess.version}</version>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

플러그인 등록
================

DI 컨테이너에 등록
------------------

플러그인은 ``fess_ds.xml`` 등의 설정 파일로 등록됩니다:

.. code-block:: xml

    <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
        <postConstruct name="register"/>
    </component>

자동 등록
--------

대부분의 플러그인은 ``@PostConstruct`` 어노테이션으로 자동 등록합니다:

.. code-block:: java

    @PostConstruct
    public void register() {
        ComponentUtil.getDataStoreManager().add(this);
    }

플러그인 라이프사이클
==========================

초기화
------

1. JAR 파일이 로드됨
2. DI 컨테이너가 컴포넌트를 초기화
3. ``@PostConstruct`` 메서드가 호출됨
4. 플러그인이 매니저에 등록됨

종료
----

1. ``@PreDestroy`` 메서드가 호출됨 (정의된 경우)
2. 리소스 클린업

의존 관계
========

Fess 본체와의 의존
----------------

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <version>${fess.version}</version>
        <scope>provided</scope>
    </dependency>

외부 라이브러리
--------------

플러그인은 독자적인 의존 라이브러리를 포함할 수 있습니다:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

의존 라이브러리는 플러그인 JAR와 함께 배포하거나
Maven Shade Plugin으로 fat JAR를 작성합니다.

설정 취득
==========

FessConfig에서 취득
------------------

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(DataConfig dataConfig, IndexUpdateCallback callback,
                Map<String, String> paramMap, Map<String, String> scriptMap,
                Map<String, Object> defaultDataMap) {

            // 파라미터 취득
            String apiKey = paramMap.get("api.key");
            String baseUrl = paramMap.get("base.url");

            // FessConfig 취득
            FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

빌드와 설치
====================

빌드
------

::

    mvn clean package

설치
------------

1. **관리 화면에서**:

   - "시스템" → "플러그인" → "설치"
   - 플러그인 이름을 입력하여 설치

2. **명령줄**:

   ::

       ./bin/fess-plugin install fess-ds-example

3. **수동**:

   - JAR 파일을 ``plugins/`` 디렉토리에 복사
   - |Fess| 를 재시작

디버그
========

로그 출력
--------

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

개발 모드
----------

개발 시 |Fess| 를 IDE에서 시작하여 디버그할 수 있습니다:

1. ``FessBoot`` 클래스를 디버그 실행
2. 플러그인 소스를 프로젝트에 포함
3. 브레이크포인트 설정

공개 플러그인 목록
==================

|Fess| 프로젝트에서 공개하고 있는 주요 플러그인:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 플러그인
     - 설명
   * - fess-ds-box
     - Box.com 커넥터
   * - fess-ds-dropbox
     - Dropbox 커넥터
   * - fess-ds-slack
     - Slack 커넥터
   * - fess-ds-atlassian
     - Confluence/Jira 커넥터
   * - fess-ds-git
     - Git 리포지토리 커넥터
   * - fess-theme-*
     - 커스텀 테마

이러한 플러그인은 개발 참고로
`GitHub <https://github.com/codelibs>`__ 에서 공개되어 있습니다.

참고 정보
========

- :doc:`datastore-plugin` - 데이터스토어 플러그인 개발
- :doc:`script-engine-plugin` - 스크립트 엔진 플러그인
- :doc:`webapp-plugin` - 웹앱 플러그인
- :doc:`ingest-plugin` - Ingest 플러그인
