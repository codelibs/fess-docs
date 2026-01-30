==================================
Ingest 플러그인
==================================

개요
====

Ingest 플러그인은 문서가 인덱스에 등록되기 전에
데이터를 가공/변환하는 기능을 제공합니다.

용도
====

- 텍스트 정규화(전각/반각 변환 등)
- 메타데이터 추가
- 민감한 정보 마스킹
- 커스텀 필드 추가

기본 구현
========

``IngestHandler`` 인터페이스를 구현합니다:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // 콘텐츠 정규화
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // 커스텀 필드 추가
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // 정규화 로직
            return text.trim().replaceAll("\\s+", " ");
        }
    }

등록
====

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

설정
====

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

참고 정보
========

- :doc:`plugin-architecture` - 플러그인 아키텍처
