==================================
데이터스토어 플러그인 개발
==================================

개요
====

데이터스토어 플러그인을 개발하여 |Fess| 에 새로운 데이터 소스로부터
콘텐츠 취득 기능을 추가할 수 있습니다. 데이터스토어는 데이터베이스·API·파일 등의
외부 시스템에서 레코드를 취득하고, 관리 화면에서 설정한 매핑 스크립트에 따라
인덱스 필드로 변환한 다음, |Fess| 의 인덱스에 등록합니다.

CSV·JSON·데이터베이스·Git·각종 클라우드 서비스 등, 공개되어 있는
커넥터(``fess-ds-*``)는 모두 이 구조로 구현되어 있습니다. 구현 템플릿으로
`fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ 가 공개되어 있으므로,
새로운 커넥터를 작성할 때는 이를 복사해서 시작하는 것이 간단합니다.

기본 구조
========

데이터스토어 플러그인은 다음 3가지 요소로 구성됩니다.

- ``AbstractDataStore`` 를 상속한 클래스를 작성한다
- ``getName()`` 과 ``storeData()`` 두 개의 메서드를 구현한다
- ``fess_ds++.xml`` 에 컴포넌트로 등록한다

최소 구현
--------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.entity.DataStoreParams;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

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

            // 데이터 취득 및 처리를 여기에 구현
        }
    }

.. note::

   ``getName()`` 과 ``storeData()`` 는 모두 ``protected`` 추상 메서드입니다.
   ``DataConfig`` 의 패키지는 |Fess| 15.x 에서는 ``org.codelibs.fess.opensearch.config.exentity``
   임에 유의하십시오(이전의 ``org.codelibs.fess.es.config.exentity`` 는 폐지되었습니다).

컴포넌트 등록
--------------------

작성한 데이터스토어를 |Fess| 가 인식하도록 하기 위해, ``src/main/resources/fess_ds++.xml`` 에
컴포넌트를 등록합니다.

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleDataStore" class="org.codelibs.fess.ds.example.ExampleDataStore">
            <postConstruct name="register"></postConstruct>
        </component>
    </components>

``<postConstruct name="register">`` 에 의해 컴포넌트 생성 후 ``AbstractDataStore``
가 가진 ``register()`` 메서드가 자동으로 호출되어 ``DataStoreFactory`` 에 자신이 등록됩니다.
이때 등록되는 이름이 ``getName()`` 의 반환값(위 예에서는 ``ExampleDataStore``)이며,
관리 화면의 데이터스토어 설정에서 선택하는 「핸들러 이름」이 됩니다.

AbstractDataStore
=================

주요 메서드
------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - 메서드
     - 구분
     - 설명
   * - ``getName()``
     - 구현(필수)
     - 데이터스토어의 핸들러 이름을 반환하는 추상 메서드. ``getClass().getSimpleName()`` 을 반환하는 것이 관례
   * - ``storeData()``
     - 구현(필수)
     - 데이터의 취득·변환·인덱스 등록을 수행하는 추상 메서드
   * - ``register()``
     - 상속(통상 변경 불필요)
     - ``fess_ds++.xml`` 의 ``postConstruct`` 에서 자동으로 호출되어 ``DataStoreFactory`` 에 등록한다
   * - ``store()``
     - 상속(프레임워크 호출)
     - 프레임워크가 호출하는 진입점. ``defaultDataMap`` 등을 준비하여 ``storeData()`` 를 호출한다
   * - ``convertValue()``
     - 상속(헬퍼)
     - ``scriptMap`` 의 값(템플릿)을 스크립트 엔진으로 평가한다
   * - ``getScriptType()``
     - 상속(헬퍼)
     - ``script_type`` 파라미터를 취득한다(기본값은 Groovy)
   * - ``getReadInterval()``
     - 상속(헬퍼)
     - ``readInterval`` 파라미터(밀리초)를 취득한다
   * - ``sleep()``
     - 상속(헬퍼)
     - 지정한 밀리초만큼 대기한다(레코드 간 대기에 사용)

storeData의 파라미터
------------------------

``storeData()`` 메서드에 전달되는 파라미터:

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 파라미터
     - 타입
     - 설명
   * - ``dataConfig``
     - ``DataConfig``
     - 데이터스토어 설정(ID·핸들러 이름·파라미터·스크립트 등)
   * - ``callback``
     - ``IndexUpdateCallback``
     - 생성한 문서를 인덱스에 등록하는 콜백
   * - ``paramMap``
     - ``DataStoreParams``
     - 관리 화면 「파라미터」란의 설정값. ``getAsString(key)`` / ``getAsString(key, default)`` / ``get(key)`` / ``asMap()`` / ``containsKey(key)`` 로 접근한다
   * - ``scriptMap``
     - ``Map<String, String>``
     - 관리 화면 「스크립트」란의 설정. 키가 인덱스 필드 이름, 값이 평가 대상 스크립트 템플릿
   * - ``defaultDataMap``
     - ``Map<String, Object>``
     - 각 문서의 기본 필드 값(설정 ID·boost·role·mimetype·가상 호스트 등). 프레임워크가 준비한다

.. warning::

   ``paramMap`` 의 타입은 ``Map<String, String>`` 이 아니라 ``DataStoreParams`` 입니다.
   ``DataStoreParams`` 는 ``Map`` 을 구현하지 않으므로, 값을 가져올 때는 ``get()`` 이 아니라
   문자열을 반환하는 ``getAsString()`` 을 사용하십시오.

데이터 처리 흐름
----------------

``storeData()`` 구현은 다음 흐름으로 데이터를 처리합니다.

#. 외부 시스템에서 소스 레코드를 취득한다.
#. ``paramMap.asMap()`` 에 소스 레코드의 필드를 병합하여 ``resultMap`` 을 구축한다
   (스크립트는 이 ``resultMap`` 에 대해 평가된다).
#. ``scriptMap`` 의 각 엔트리를 ``convertValue(scriptType, template, resultMap)`` 로 평가하여
   결과를 ``dataMap`` 에 저장한다. 매핑을 코드 안에 하드코딩하는 것이 아니라
   관리자가 「스크립트」란에서 정의한다는 점이 중요합니다.
#. ``callback.store(paramMap, dataMap)`` 을 호출하여 문서로 인덱스에 등록한다.

구현 예
======

심플한 데이터스토어
----------------------

외부 API 에서 레코드를 취득하여 인덱스에 등록하는 예입니다.

.. code-block:: java

    @Override
    protected void storeData(final DataConfig dataConfig, final IndexUpdateCallback callback,
            final DataStoreParams paramMap, final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // 파라미터 취득(DataStoreParams 에서는 getAsString 을 사용한다)
        final String apiUrl = paramMap.getAsString("api.url");
        final String apiKey = paramMap.getAsString("api.key");

        // 스크립트 평가 타입(기본값은 Groovy)
        final String scriptType = getScriptType(paramMap);
        // 레코드 간 대기 시간(밀리초)
        final long readInterval = getReadInterval(paramMap);

        try {
            // 외부 시스템에서 데이터 취득
            final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey);

            for (final Map<String, Object> record : records) {
                // 기본 필드를 복사하여 dataMap 초기화
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // 파라미터와 소스 레코드를 병합한 resultMap 구축
                // (스크립트는 이 resultMap 에 대해 평가된다)
                final Map<String, Object> resultMap = new LinkedHashMap<>(paramMap.asMap());
                resultMap.putAll(record);

                // scriptMap 의 각 엔트리를 평가하여 인덱스 필드 생성
                for (final Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    final Object value = convertValue(scriptType, entry.getValue(), resultMap);
                    if (value != null) {
                        dataMap.put(entry.getKey(), value);
                    }
                }

                // 인덱스에 등록
                callback.store(paramMap, dataMap);

                if (readInterval > 0) {
                    sleep(readInterval);
                }
            }
        } catch (final Exception e) {
            throw new DataStoreException("Failed to crawl data from " + apiUrl, e);
        }
    }

``fetchRecords()`` 는 외부 시스템에서 레코드 목록을 취득하는 자체 메서드입니다. 취득한
각 레코드(``Map<String, Object>``)의 필드 이름이, ``scriptMap`` 의 스크립트에서
참조할 수 있는 이름이 됩니다. ``DataStoreException`` 은 ``org.codelibs.fess.exception``
패키지의 클래스입니다.

페이지네이션 대응
--------------------

대량의 데이터를 다루는 경우에는 페이지 단위로 취득하면서 처리합니다. 레코드 1건당 처리
(``resultMap`` 구축·``scriptMap`` 평가·``callback.store()`` 호출)를
``processRecord()`` 와 같은 메서드로 분리해두면 취득 로직과 분리할 수 있습니다.

.. code-block:: java

    int offset = 0;
    final int pageSize = 100;

    while (true) {
        final List<Map<String, Object>> records = fetchRecords(apiUrl, apiKey, offset, pageSize);

        if (records.isEmpty()) {
            break;
        }

        for (final Map<String, Object> record : records) {
            processRecord(record, callback, paramMap, scriptMap, defaultDataMap);
        }

        offset += pageSize;
    }

인증 구현
==========

외부 시스템의 인증은 커넥터 측에서 구현합니다. 아래는 일반적인 HTTP 클라이언트
라이브러리를 사용한 구현 예시로, |Fess| 가 제공하는 API 는 아닙니다. 사용할 라이브러리는
플러그인의 의존 관계로 함께 포함시켜 주십시오.

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(final String clientId, final String clientSecret, final String refreshToken) {
        // 리프레시 토큰을 이용해 액세스 토큰을 취득하는 예
        final OkHttpClient client = new OkHttpClient();

        final RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        final Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            final JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

API 키 인증
-----------

.. code-block:: java

    protected Response callApi(final String url, final String apiKey) {
        final Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

오류 처리
==================

처리를 중단해야 하는 치명적인 오류에서는 ``DataStoreException`` 을 던집니다.

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // 처리
        } catch (final AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (final RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            sleep(60000L);
            // 재시도 로직
        } catch (final Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

.. note::

   ``fess-ds-example`` 을 비롯한 실제 커넥터에서는 레코드 1건의 오류로
   크롤링 전체가 중단되지 않도록, 레코드 단위로 ``CrawlingAccessException`` 을 포착하여
   ``FailureUrlService`` 에 오류 URL 을 기록합니다. 또한
   ``DataStoreCrawlingException`` 의 중단 플래그를 사용하여, 크롤링 전체를 중단할지 여부를
   제어합니다. 견고한 커넥터를 구현하려는 경우에는 ``ExampleDataStore`` 의 구현을 참조하십시오.

테스트
======

유닛 테스트
--------------

|Fess| 의 플러그인은 UTFlute 의 ``LastaDiTestCase`` 를 사용하여 테스트합니다. 테스트는
JUnit 5(Jupiter)로 작성합니다. ``IndexUpdateCallback`` 을, 등록된 ``dataMap`` 을
수집하는 구현으로 교체함으로써, 목(mock) 라이브러리를 사용하지 않고도 매핑 결과를 검증할 수 있습니다.

.. code-block:: java

    public class ExampleDataStoreTest extends LastaDiTestCase {

        public ExampleDataStore dataStore;

        @Override
        protected String prepareConfigFile() {
            return "test_app.xml";
        }

        @Override
        public void setUp(final TestInfo testInfo) throws Exception {
            super.setUp(testInfo);
            dataStore = new ExampleDataStore();
        }

        @Test
        public void test_getName() {
            assertEquals("ExampleDataStore", dataStore.getName());
        }

        @Test
        public void test_storeData() {
            final TestIndexUpdateCallback callback = new TestIndexUpdateCallback();
            final DataStoreParams paramMap = new DataStoreParams();

            final Map<String, String> scriptMap = new HashMap<>();
            scriptMap.put("title", "title");

            dataStore.storeData(new DataConfig(), callback, paramMap, scriptMap, new HashMap<>());

            assertFalse(callback.getDataMapList().isEmpty());
        }

        // 등록된 dataMap 을 수집하는 테스트용 콜백
        private static class TestIndexUpdateCallback implements IndexUpdateCallback {
            private final List<Map<String, Object>> dataMapList = new ArrayList<>();

            @Override
            public void store(final DataStoreParams paramMap, final Map<String, Object> dataMap) {
                dataMapList.add(new HashMap<>(dataMap));
            }

            @Override
            public long getExecuteTime() {
                return 0;
            }

            @Override
            public long getDocumentSize() {
                return dataMapList.size();
            }

            @Override
            public void commit() {
                // 아무것도 하지 않음
            }

            public List<Map<String, Object>> getDataMapList() {
                return dataMapList;
            }
        }
    }

.. note::

   ``setUp`` 은 기반 클래스에서 ``@BeforeEach`` 가 부여되어 있으므로, 오버라이드하는 쪽에
   라이프사이클 애너테이션을 다시 붙일 필요가 없습니다. 각 테스트 메서드에는
   ``@Test``(``org.junit.jupiter.api.Test``)를 부여합니다.

빌드와 설치
====================

pom.xml
-------

플러그인은 ``fess-parent`` 를 부모 POM 으로 하는 jar 로 빌드합니다. ``fess`` 및
``opensearch`` 에 대한 의존성은 실행 시 |Fess| 본체에서 제공되므로 ``provided`` 로 설정합니다.

.. code-block:: xml

    <project xmlns="http://maven.apache.org/POM/4.0.0" ...>
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

테스트에는 JUnit 5 와 ``org.dbflute.utflute:utflute-lastaflute`` 를 사용합니다.

빌드
------

.. code-block:: bash

    mvn clean package

``target/`` 디렉터리에 ``fess-ds-example-15.8.0.jar`` 가 생성됩니다.

설치
------------

생성한 JAR 를 |Fess| 에 설치하고 |Fess| 를 재시작합니다. 설치 절차의 자세한 내용은
:doc:`../admin/plugin-guide` 를 참조하십시오. 설치 후 관리 화면의
「크롤러 > 데이터스토어」에서 신규 설정을 작성하고, 「핸들러 이름」에 ``getName()`` 이 반환하는 이름
(이 예에서는 ``ExampleDataStore``)을 지정합니다.

설정 예
======

관리 화면에서의 설정 예:

파라미터
------------

「파라미터」란에는 커넥터가 ``paramMap`` 에서 읽어들이는 키와 값을 기술합니다.

::

    api.url=https://api.example.com/v1
    api.key=your_api_key

스크립트
----------

「스크립트」란에는 ``좌변=우변`` 형식으로 매핑을 기술합니다. 좌변이 인덱스
필드 이름, 우변이 소스 레코드의 필드를 참조하는 스크립트(기본값은 Groovy)입니다.
아래는 소스 레코드가 ``url`` / ``title`` / ``content`` / ``updated_at`` /
``content_type`` 필드를 가지고 있는 경우의 예입니다.

::

    url=url
    title=title
    content=content
    last_modified=updated_at
    mimetype=content_type

.. note::

   우변에서 참조할 수 있는 필드 이름은 커넥터가 ``resultMap`` 에 저장하는 값
   (``paramMap`` 의 값과 소스 레코드의 필드)에 따라 결정됩니다. CSV 나 JSON 등
   기존 커넥터에서는 ``data.*`` 와 같은 독자적인 프리픽스가 붙는 경우가 있으므로,
   각 커넥터의 문서를 참조하십시오.

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`../admin/plugin-guide` - 플러그인 설치
- :doc:`../config/datastore/ds-overview` - 데이터스토어 커넥터 개요
- `fess-ds-example <https://github.com/codelibs/fess-ds-example>`__ - 데이터스토어 플러그인 구현 템플릿
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - 공개 커넥터 예시
