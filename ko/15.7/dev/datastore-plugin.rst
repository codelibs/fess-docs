==================================
데이터스토어 플러그인 개발
==================================

개요
====

데이터스토어 플러그인을 개발하여 |Fess| 에 새로운 데이터 소스에서
콘텐츠 취득 기능을 추가할 수 있습니다.

기본 구조
========

데이터스토어 플러그인은 ``AbstractDataStore`` 를 상속하여 구현합니다.

최소 구현
--------

.. code-block:: java

    package org.codelibs.fess.ds.example;

    import java.util.Map;

    import org.codelibs.fess.ds.AbstractDataStore;
    import org.codelibs.fess.ds.callback.IndexUpdateCallback;
    import org.codelibs.fess.opensearch.config.exentity.DataConfig;

    public class ExampleDataStore extends AbstractDataStore {

        @Override
        public String getName() {
            return "Example";
        }

        @Override
        protected void storeData(
                final DataConfig dataConfig,
                final IndexUpdateCallback callback,
                final Map<String, String> paramMap,
                final Map<String, String> scriptMap,
                final Map<String, Object> defaultDataMap) {

            // 데이터 취득 및 처리를 여기에 구현
        }
    }

AbstractDataStore
=================

주요 메서드
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 메서드
     - 설명
   * - ``getName()``
     - 데이터스토어 이름을 반환 (필수)
   * - ``storeData()``
     - 데이터 취득 및 인덱스 등록 수행 (필수)
   * - ``register()``
     - 플러그인 등록

파라미터
------------

``storeData()`` 메서드에 전달되는 파라미터:

- ``dataConfig``: 데이터스토어 설정
- ``callback``: 인덱스 업데이트용 콜백
- ``paramMap``: 관리 화면에서 설정된 파라미터
- ``scriptMap``: 스크립트 설정
- ``defaultDataMap``: 기본 데이터 맵

구현 예
======

심플한 데이터스토어
----------------------

.. code-block:: java

    @Override
    protected void storeData(
            final DataConfig dataConfig,
            final IndexUpdateCallback callback,
            final Map<String, String> paramMap,
            final Map<String, String> scriptMap,
            final Map<String, Object> defaultDataMap) {

        // 파라미터 취득
        final String apiUrl = paramMap.get("api.url");
        final String apiKey = paramMap.get("api.key");

        try {
            // 데이터 취득
            List<Document> documents = fetchDocuments(apiUrl, apiKey);

            // 각 문서 처리
            for (Document doc : documents) {
                final Map<String, Object> dataMap = new HashMap<>(defaultDataMap);

                // 데이터 매핑
                dataMap.put("url", doc.getUrl());
                dataMap.put("title", doc.getTitle());
                dataMap.put("content", doc.getContent());
                dataMap.put("lastModified", doc.getUpdatedAt());

                // 스크립트 실행 (매핑)
                final Map<String, Object> resultMap = new HashMap<>();
                for (Map.Entry<String, String> entry : scriptMap.entrySet()) {
                    Object value = convertValue(entry.getValue(), dataMap);
                    if (value != null) {
                        resultMap.put(entry.getKey(), value);
                    }
                }

                // 인덱스에 등록
                callback.store(paramMap, resultMap);
            }
        } catch (Exception e) {
            logger.error("Failed to crawl data", e);
        }
    }

페이지네이션 대응
--------------------

.. code-block:: java

    @Override
    protected void storeData(...) {
        int page = 0;
        int pageSize = 100;

        while (true) {
            List<Document> documents = fetchDocuments(apiUrl, apiKey, page, pageSize);

            if (documents.isEmpty()) {
                break;
            }

            for (Document doc : documents) {
                processDocument(doc, callback, paramMap, scriptMap, defaultDataMap);
            }

            page++;
        }
    }

인증 구현
==========

OAuth 2.0
---------

.. code-block:: java

    protected String getAccessToken(String clientId, String clientSecret, String refreshToken) {
        // 토큰 리프레시
        OkHttpClient client = new OkHttpClient();

        RequestBody body = new FormBody.Builder()
            .add("grant_type", "refresh_token")
            .add("client_id", clientId)
            .add("client_secret", clientSecret)
            .add("refresh_token", refreshToken)
            .build();

        Request request = new Request.Builder()
            .url("https://oauth.example.com/token")
            .post(body)
            .build();

        try (Response response = client.newCall(request).execute()) {
            JsonNode json = objectMapper.readTree(response.body().string());
            return json.get("access_token").asText();
        }
    }

API 키 인증
-----------

.. code-block:: java

    protected Response callApi(String url, String apiKey) {
        Request request = new Request.Builder()
            .url(url)
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return httpClient.newCall(request).execute();
    }

오류 처리
==================

.. code-block:: java

    @Override
    protected void storeData(...) {
        try {
            // 처리
        } catch (AuthenticationException e) {
            logger.error("Authentication failed. Check your credentials.", e);
            throw new DataStoreException("Authentication failed", e);
        } catch (RateLimitException e) {
            logger.warn("Rate limit exceeded. Waiting...");
            Thread.sleep(60000);
            // 재시도 로직
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            throw new DataStoreException("Failed to crawl data", e);
        }
    }

테스트
======

유닛 테스트
--------------

.. code-block:: java

    public class ExampleDataStoreTest {

        private ExampleDataStore dataStore;

        @Before
        public void setUp() {
            dataStore = new ExampleDataStore();
        }

        @Test
        public void testGetName() {
            assertEquals("Example", dataStore.getName());
        }

        @Test
        public void testFetchDocuments() {
            // 목을 사용한 테스트
        }
    }

설정 예
======

관리 화면에서의 설정 예:

파라미터
------------

::

    api.url=https://api.example.com/v1
    api.key=your_api_key
    max.items=1000
    include.folders=folder1,folder2

스크립트
----------

::

    url=data.url
    title=data.name
    content=data.content
    lastModified=data.updated_at
    mimetype=data.content_type

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
- :doc:`../config/datastore/ds-overview` - 데이터스토어 커넥터 개요
- `GitHub: fess-ds-* <https://github.com/codelibs?q=fess-ds>`__ - 공개 플러그인 예시
