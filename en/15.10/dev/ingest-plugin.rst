==================================
Ingest Plugin
==================================

Overview
========

Ingest plugins provide functionality to process and transform data
immediately before a document is registered in the index. Each document
retrieved by a crawl passes through the registered Ingesters before it is
sent to the index.

Use Cases
=========

- Text normalization (full-width/half-width conversion, whitespace formatting, etc.)
- Adding metadata or custom fields
- Masking sensitive information
- Value conversion (e.g., decoding encoded vector embeddings)

Ingester Class
==============

Ingest functionality is implemented by extending the
``org.codelibs.fess.ingest.Ingester`` abstract class. ``Ingester`` provides
``process`` methods that are invoked depending on the type of crawl and the
processing stage. Since the default implementations simply return the
received ``target`` unchanged (i.e., do nothing), you only need to override
the methods you actually need.

- ``protected Map<String, Object> process(Map<String, Object> target)``

  This is the common delegation target for the two ``Map``-based methods.
  Overriding this method applies it to documents from both data store crawls
  and web/file crawls (at index registration time). For most use cases,
  overriding only this method is sufficient.

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  Called during a data store crawl. By default, it delegates to
  ``process(target)``.

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  Called when registering a document from a web/file crawl into the index.
  By default, it delegates to ``process(target)``.

- ``public ResultData process(ResultData target, ResponseData responseData)``

  Called during response processing of a web/file crawl (before the access
  result is saved). By default, it returns ``target`` unchanged.

Execution Order (priority)
---------------------------

When multiple Ingesters are registered, they are executed in ascending
order of the ``priority`` field (lower values run first). The default
value is ``99``. You can set it directly in the constructor, or change it
using ``setPriority(int)``.

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

Implementation Example
=======================

The following example overrides ``process(Map<String, Object>)`` to
normalize the content and add a custom field:

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // Set the execution order (lower values execute first; default is 99)
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // Normalize the content
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // Add a custom field
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // Return the processed document
            return target;
        }
    }

.. note::

    Returning ``null`` from the ``process`` method will cause index
    registration to fail. There is no mechanism for skipping a document,
    so always return ``target``.

Registration
============

Ingesters are registered via the DI container. Include ``fess_ingest++.xml``
in your plugin. The ``++`` suffix in the file name follows the merge
convention that appends the configuration to |Fess|'s own
``fess_ingest.xml`` (which defines the ``ingestFactory`` that manages
Ingesters).

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE components PUBLIC "-//DBFLUTE//DTD LastaDi 1.0//EN"
        "http://dbflute.org/meta/lastadi10.dtd">
    <components>
        <component name="exampleIngester"
                   class="org.codelibs.fess.ingest.example.ExampleIngester">
            <postConstruct name="register"/>
        </component>
    </components>

With ``<postConstruct name="register"/>``, ``Ingester#register()`` is
called after the component is created, registering itself with the
``ingestFactory``.

There are no ``fess_config.properties`` settings related to the Ingest
functionality. Whether it is enabled or disabled is determined by whether
the plugin is installed, and the execution order is controlled by
``priority``.

Execution Flow
==============

Ingesters are called, in ascending order of ``priority``, immediately
before the processed document is sent to the index, at the following
points:

- **Data store crawl**: ``process(Map, DataStoreParams)`` is called
  immediately before the document is sent.
- **Web/file crawl (response processing)**: ``process(ResultData,
  ResponseData)`` is called before the crawl result is saved.
- **Web/file crawl (index registration)**: ``process(Map, AccessResult)``
  is called immediately before the document is sent.

In every case, if an Ingester throws an exception, a warning is logged and
processing continues (index registration of that document is not
interrupted).

.. note::

    Since Ingesters are registered in the crawler's runtime environment
    (``ingestFactory``), they operate as part of the crawl process.

Reference Implementations
==========================

For reference, the following plugins are published on GitHub under
`CodeLibs <https://github.com/codelibs>`__:

- ``fess-ingest-example`` - A minimal sample implementation
- ``fess-webapp-multimodal`` - A plugin that includes ``EmbeddingIngester``, which decodes vector embeddings

References
==========

- :doc:`plugin-architecture` - Plugin Architecture
