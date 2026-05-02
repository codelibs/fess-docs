==================================
Ingest插件
==================================

概述
====

Ingest插件提供在文档注册到索引之前进行数据加工和转换的功能。

用途
====

- 文本规范化（全角/半角转换等）
- 添加元数据
- 敏感信息脱敏
- 添加自定义字段

基本实现
========

实现 ``IngestHandler`` 接口:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // 内容规范化
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // 添加自定义字段
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // 规范化逻辑
            return text.trim().replaceAll("\\s+", " ");
        }
    }

注册
====

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

配置
====

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

参考信息
========

- :doc:`plugin-architecture` - 插件架构

