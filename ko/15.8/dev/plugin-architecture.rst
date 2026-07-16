==================================
플러그인 아키텍처
==================================

개요
====

|Fess| 의 플러그인 시스템을 통해 코어 기능을 확장할 수 있습니다.
플러그인은 JAR 파일로 배포되며, 클래스패스에 추가되면 DI 컨테이너
(Lasta Di)에 의해 컴포넌트가 로드되어 해당 팩토리나 매니저에
등록됩니다.

플러그인 종류
================

|Fess| 는 아티팩트 이름의 프리픽스로 플러그인의 종류를
판별합니다(``PluginHelper.ArtifactType``). 주요 종류는 다음과 같습니다:

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 종류
     - 프리픽스
     - 설명
   * - 데이터스토어
     - ``fess-ds-*``
     - 새로운 데이터 소스로부터의 콘텐츠 취득(Box, Slack, Git 등)
   * - 웹앱
     - ``fess-webapp-*``
     - 웹 인터페이스나 검색 기능의 확장
   * - 스크립트 엔진
     - ``fess-script-*``
     - 새로운 스크립트 언어 지원
   * - Ingest
     - ``fess-ingest-*``
     - 인덱스 등록 시 문서 가공
   * - 테마
     - ``fess-theme-*``
     - 검색 화면 디자인 커스터마이징
   * - 썸네일
     - ``fess-thumbnail-*``
     - 썸네일 생성 방식 추가
   * - LLM
     - ``fess-llm-*``
     - RAG/채팅에서 사용하는 LLM 프로바이더 추가
   * - 크롤러
     - ``fess-crawler-*``
     - 크롤러 클라이언트 확장

플러그인 구조
==============

기본 구조
---------

데이터스토어 플러그인의 구현 템플릿인
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ 를 예로 들면,
플러그인은 「구현 클래스」와 「DI 등록 파일」로 구성됩니다:

::

    fess-ds-example/
    ├── pom.xml
    └── src/main/
        ├── java/org/codelibs/fess/ds/example/
        │   └── ExampleDataStore.java     # 데이터스토어 구현
        └── resources/
            └── fess_ds++.xml             # DI 컴포넌트 등록

pom.xml 예제
------------

플러그인은 ``fess-parent`` 를 부모 POM 으로 하는 jar 로 빌드합니다.
``fess`` 나 ``opensearch`` 등, 실행 시 |Fess| 본체에서 제공되는 라이브러리는
``provided`` 스코프로 선언합니다. 버전 번호나 빌드 설정(포맷터·
라이선스 헤더 등)은 부모 POM 에서 상속됩니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                                 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>

        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess-ds-example</artifactId>
        <version>15.8.0</version>
        <packaging>jar</packaging>

        <parent>
            <groupId>org.codelibs.fess</groupId>
            <artifactId>fess-parent</artifactId>
            <version>15.8.0</version>
            <relativePath />
        </parent>

        <dependencies>
            <dependency>
                <groupId>org.codelibs.fess</groupId>
                <artifactId>fess</artifactId>
                <scope>provided</scope>
            </dependency>
            <dependency>
                <groupId>org.opensearch</groupId>
                <artifactId>opensearch</artifactId>
                <scope>provided</scope>
            </dependency>
        </dependencies>
    </project>

.. note::

   개발 중인 브랜치에서는 버전이 ``15.8.0-SNAPSHOT`` 처럼 ``-SNAPSHOT`` 이 붙은
   형태가 됩니다. 플러그인 고유의 의존 라이브러리는 일반적인 Maven 의존 관계로
   선언합니다. 이들은 |Fess| 본체에는 포함되지 않으므로, 플러그인과 함께 배포해야 합니다.

플러그인 등록
================

DI 컨테이너 등록
------------------

플러그인은 ``fess_ds++.xml`` 처럼 끝이 ``++`` 로 끝나는 DI 설정 파일로
컴포넌트를 등록합니다. Lasta Di 는 클래스패스 상에서 발견한 ``++`` 가 붙은
파일을, |Fess| 본체의 대응하는 설정 파일(이 예에서는 ``fess_ds.xml``)에
자동으로 병합합니다. 이 구조를 통해 플러그인은 |Fess| 본체의 파일을
수정하지 않고도 자신의 컴포넌트를 추가할 수 있습니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

플러그인 종류마다 병합 대상 파일이 다릅니다. 예를 들어 스크립트 엔진은
``fess_se++.xml``, Ingest 는 ``fess_ingest++.xml``, LLM 프로바이더는
``fess_llm++.xml``, 웹앱은 ``app++.xml`` 을 사용합니다.

컴포넌트 초기화
----------------------

``<postConstruct name="register">`` 는 컴포넌트 생성 후에 호출할
메서드를 지정하는 Lasta Di 의 라이프사이클 설정입니다. 데이터스토어의 경우,
``AbstractDataStore`` 가 가진 ``register()`` 메서드가 호출되어
자신이 ``DataStoreFactory`` 에 등록됩니다:

.. code-block:: java

    // AbstractDataStore 의 구현(통상 오버라이드 불필요)
    public void register() {
        ComponentUtil.getDataStoreFactory().add(getName(), this);
    }

.. note::

   이것은 Java 의 ``@PostConstruct`` 애너테이션이 아니라, DI 설정 파일의
   ``<postConstruct>`` 요소에 의한 초기화입니다. 등록되는 이름은 ``getName()`` 의
   반환값이며, 관리 화면에서 플러그인을 선택할 때의 이름이 됩니다.

플러그인 라이프사이클
==========================

초기화
------

1. 플러그인 JAR 가 클래스패스에 추가된다
2. DI 컨테이너가 ``fess_*++.xml`` 을 병합하여 컴포넌트를 생성한다
3. ``<postConstruct>`` 에서 지정한 메서드(예: ``register``)가 호출된다
4. 플러그인이 대응하는 팩토리/매니저에 등록된다

종료
----

1. DI 컨테이너 종료 시, ``<preDestroy>`` 에서 지정한 메서드가 호출된다
   (정의되어 있는 경우)
2. 리소스 정리

.. note::

   데이터스토어의 경우, 실행 중인 크롤링은 ``AbstractDataStore.stop()`` 에 의해
   정지 플래그가 설정되어 레코드 처리 루프가 안전하게 종료됩니다.

의존 관계
=========

Fess 본체 의존성
----------------

|Fess| 본체의 클래스는 실행 시 서버의 클래스패스 상에 존재하므로,
``provided`` 스코프로 의존합니다(플러그인 JAR 에는 포함하지 않습니다).

.. code-block:: xml

    <dependency>
        <groupId>org.codelibs.fess</groupId>
        <artifactId>fess</artifactId>
        <scope>provided</scope>
    </dependency>

외부 라이브러리
---------------

플러그인은 자체 의존 라이브러리를 포함할 수 있습니다:

.. code-block:: xml

    <dependency>
        <groupId>com.example</groupId>
        <artifactId>example-sdk</artifactId>
        <version>1.0.0</version>
    </dependency>

이들은 |Fess| 본체에는 포함되지 않으므로, 플러그인과 함께 배포해야 합니다.

설정 취득
==========

파라미터와 FessConfig 취득
------------------------------

데이터스토어의 ``storeData()`` 에서는 관리 화면에서 설정한 파라미터를
``DataStoreParams`` 에서 취득합니다. 값을 가져올 때는 ``getAsString()`` 을 사용합니다
(``DataStoreParams`` 는 ``Map`` 을 구현하지 않으므로 ``get()`` 은 문자열을 반환하지 않습니다).
또한 |Fess| 의 설정값은 ``ComponentUtil.getFessConfig()`` 에서 취득할 수 있습니다:

.. code-block:: java

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        protected String getName() {
            // 핸들러 이름으로 사용된다. 클래스의 단순 이름을 반환하는 것이 관례
            return this.getClass().getSimpleName();
        }

        @Override
        protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
                final DataStoreParams paramMap, final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // 파라미터 취득
            final String apiKey = paramMap.getAsString("api.key");
            final String baseUrl = paramMap.getAsString("base.url");

            // FessConfig 취득
            final FessConfig fessConfig = ComponentUtil.getFessConfig();
        }
    }

``storeData()`` 의 자세한 구현 방법(데이터 취득·스크립트 평가·인덱스 등록의
흐름)은 :doc:`datastore-plugin` 을 참조하십시오.

빌드와 설치
====================

빌드
------

::

    mvn clean package

``target/`` 디렉터리에 JAR 파일(예: ``fess-ds-example-15.8.0.jar``)이
생성됩니다.

설치
------------

1. **관리 화면에서**:

   - [시스템 > 플러그인 > 설치]를 연다
   - 플러그인 리포지토리 목록에서 선택하거나, 빌드한 JAR 파일을
     업로드하여 설치

2. **수동**:

   - JAR 파일을 ``app/WEB-INF/plugin/`` 디렉터리에 복사
   - |Fess| 를 재시작

설치 절차의 자세한 내용은 :doc:`../admin/plugin-guide` 를 참조하십시오.

디버깅
========

로그 출력
---------

|Fess| 는 Log4j2 를 사용합니다. 로거는 ``LogManager.getLogger()`` 로 취득합니다:

.. code-block:: java

    private static final Logger logger = LogManager.getLogger(ExampleDataStore.class);

    public void someMethod() {
        logger.debug("Debug message");
        logger.info("Info message");
    }

.. note::

   비밀번호나 토큰 등의 민감한 정보는 로그에 출력하지 마십시오.

개발 모드
----------

개발 시에는 |Fess| 를 IDE 에서 실행하여 디버깅할 수 있습니다:

1. ``org.codelibs.fess.FessBoot`` 클래스를 디버그 실행한다
2. 플러그인의 소스를 프로젝트에 포함시킨다
3. 브레이크포인트를 설정한다

공개 플러그인 목록
==================

|Fess| 프로젝트에서는 다수의 플러그인이 공개되어 있습니다. 다음은 대표적인 예입니다
(전부를 망라한 것은 아닙니다):

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 플러그인
     - 설명
   * - ``fess-ds-box``
     - Box 커넥터
   * - ``fess-ds-dropbox``
     - Dropbox 커넥터
   * - ``fess-ds-slack``
     - Slack 커넥터
   * - ``fess-ds-atlassian``
     - JIRA / Confluence 커넥터
   * - ``fess-ds-git``
     - Git 리포지토리 커넥터
   * - ``fess-llm-openai``
     - OpenAI LLM 프로바이더
   * - ``fess-theme-*``
     - 커스텀 테마

이 밖에도 ``fess-ds-csv`` / ``fess-ds-db`` / ``fess-ds-json`` /
``fess-ds-microsoft365`` / ``fess-ds-sharepoint`` 등의 데이터스토어 커넥터나,
``fess-llm-ollama`` / ``fess-llm-gemini`` 등의 LLM 프로바이더가 공개되어 있습니다.
이들 플러그인은 개발 참고용으로
`GitHub <https://github.com/codelibs>`__ 에 공개되어 있습니다.

참고 정보
=========

- :doc:`datastore-plugin` - 데이터스토어 플러그인 개발
- :doc:`script-engine-plugin` - 스크립트 엔진 플러그인
- :doc:`webapp-plugin` - 웹앱 플러그인
- :doc:`ingest-plugin` - Ingest 플러그인
- :doc:`theme-development` - 테마 커스터마이징
- :doc:`../admin/plugin-guide` - 플러그인 설치
