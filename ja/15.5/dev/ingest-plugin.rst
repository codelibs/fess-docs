==================================
Ingestプラグイン
==================================

概要
====

Ingestプラグインは、ドキュメントがインデックスに登録される前に
データを加工・変換する機能を提供します。

用途
====

- テキストの正規化（全角/半角変換など）
- メタデータの追加
- センシティブ情報のマスキング
- カスタムフィールドの追加

基本実装
========

``IngestHandler`` インターフェースを実装します:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // コンテンツの正規化
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // カスタムフィールドの追加
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // 正規化ロジック
            return text.trim().replaceAll("\\s+", " ");
        }
    }

登録
====

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

設定
====

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

参考情報
========

- :doc:`plugin-architecture` - プラグインアーキテクチャ
