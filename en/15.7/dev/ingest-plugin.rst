==================================
Ingest Plugin
==================================

Overview
========

Ingest plugins provide functionality to process and transform data
before documents are registered in the index.

Use Cases
=========

- Text normalization (full-width/half-width conversion, etc.)
- Adding metadata
- Masking sensitive information
- Adding custom fields

Basic Implementation
====================

Implement the ``IngestHandler`` interface:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import org.codelibs.fess.ingest.IngestHandler;
    import java.util.Map;

    public class ExampleIngestHandler implements IngestHandler {

        @Override
        public Map<String, Object> process(Map<String, Object> document) {
            // Content normalization
            String content = (String) document.get("content");
            if (content != null) {
                content = normalizeText(content);
                document.put("content", content);
            }

            // Add custom field
            document.put("processed_at", new Date());

            return document;
        }

        private String normalizeText(String text) {
            // Normalization logic
            return text.trim().replaceAll("\\s+", " ");
        }
    }

Registration
============

``fess_ingest.xml``:

.. code-block:: xml

    <component name="exampleIngestHandler"
               class="org.codelibs.fess.ingest.example.ExampleIngestHandler">
        <postConstruct name="register"/>
    </component>

Configuration
=============

``fess_config.properties``:

::

    ingest.handler.example.enabled=true

Reference
=========

- :doc:`plugin-architecture` - Plugin Architecture

