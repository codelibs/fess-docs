==================
Search Engine Type
==================

Overview
========

|Fess| stores its data in OpenSearch. The ``search_engine.type`` setting tells |Fess| what kind of OpenSearch it is connected to. This decides which index definitions |Fess| creates and which features it offers.

With the default value, ``default``, |Fess| expects an OpenSearch that has the four CodeLibs plugins installed (``opensearch-analysis-fess``, ``opensearch-analysis-extension``, ``opensearch-minhash`` and ``opensearch-configsync``; see :doc:`../install/install`). To connect to a plain OpenSearch without these plugins, for example a managed service on which you cannot install plugins of your own, set it to ``vanilla``.

Types
=====

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Description
   * - ``default``
     - OpenSearch with the CodeLibs plugins. This is the default.
   * - ``vanilla``
     - A plain OpenSearch without the CodeLibs plugins. New in 15.9. The index definitions are read from ``fess_indices/_vanilla/``. |Fess| 15.8 and earlier do not know this value; use ``cloud`` with them.
   * - ``aws``
     - The same as ``vanilla``, intended for Amazon OpenSearch Service. See :ref:`search-engine-type-aws`.
   * - ``cloud``
     - A deprecated alias of ``vanilla``. |Fess| logs a warning at startup. Change it to ``vanilla``.
   * - Any other value
     - Treated like ``default``, except that definition files under ``fess_indices/_<type>/`` take precedence over the files of the same name under ``fess_indices/``.

|Fess| does not detect the plugins automatically; you set the type yourself. Set it before the first start. The index definitions are applied when an index is created, so changing the value later does not change the indices that already exist.

Features Unavailable Without the Plugins
========================================

With ``vanilla`` and ``aws`` (including the deprecated ``cloud``), the following features are not available. The items of the administration screens that depend on them are hidden.

* **Dictionary management**: [System > Dictionary] is hidden. The dictionary pages and the dictionary administration API (``/api/admin/dict/``) cannot be used. "Reset Dictionaries" and "Reload Document Index" on the Maintenance page are hidden as well. The analyzers use the rules contained in the index definition, not dictionary files.
* **Result collapsing**: "Collapse Duplicate Results" in General Settings is hidden and collapsing is always off.
* **Duplicate detection**: the content signature used to find documents with the same content is not computed. The "Duplicates" tab of the Document Report is hidden (the dormant documents report is still available), and the ``sdh`` search parameter (similar documents) is ignored.
* **Analyzers**: Japanese, Korean and Simplified Chinese are tokenized by the OpenSearch Kuromoji, Nori and SmartCN analyzers instead of the CodeLibs tokenizers, so the tokens differ from those of ``default``. Vietnamese (``*_vi`` fields) and Traditional Chinese (``*_zh-tw`` fields) fall back to an empty analyzer that registers no terms. Documents in these languages are still indexed in the language-independent ``content`` and ``title`` fields.

Required OpenSearch Plugins
===========================

The index definitions for ``vanilla`` and ``aws`` use analyzers and a vector field type provided by official OpenSearch plugins. The OpenSearch you connect to must have these plugins:

* ``analysis-kuromoji``
* ``analysis-nori``
* ``analysis-smartcn``
* ``opensearch-knn`` (k-NN)

The CodeLibs plugins are not required. On an OpenSearch that you operate yourself, install a plugin with ``opensearch-plugin install``, for example ``bin/opensearch-plugin install analysis-nori``. For Amazon OpenSearch Service, see :ref:`search-engine-type-aws`.

When the type is ``vanilla`` or ``aws``, |Fess| lists the installed plugins (``GET /_cat/plugins``) at startup. If any of the plugins above is missing, it logs one warning that names the missing plugins and continues to start. If the request fails, for example because the service does not allow it, the check is skipped.

Setting the Type
================

Docker
------

Set the ``SEARCH_ENGINE_TYPE`` environment variable on the ``fess01`` service in ``compose.yaml``::

    services:
      fess01:
        environment:
          - "SEARCH_ENGINE_HTTP_URL=http://search01:9200"
          - "SEARCH_ENGINE_TYPE=vanilla"

``vanilla`` can be used with |Fess| 15.9 and later images. With an earlier image, set ``SEARCH_ENGINE_TYPE=cloud``. For the other Docker settings, see :doc:`../install/install-docker`.

Non-Docker Installations
------------------------

``bin/fess.in.sh`` does not read ``SEARCH_ENGINE_TYPE``. Use one of the following instead.

* Write ``search_engine.type`` in ``fess_config.properties`` (``app/WEB-INF/classes/fess_config.properties`` in the ZIP edition, ``/etc/fess/fess_config.properties`` in the RPM and DEB editions).
* Append a JVM option to ``FESS_JAVA_OPTS`` in ``bin/fess.in.sh`` (``bin\fess.in.bat`` on Windows) of the ZIP edition.

::

    # fess_config.properties
    search_engine.type=vanilla

    # bin/fess.in.sh
    FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dfess.config.search_engine.type=vanilla"

    REM bin\fess.in.bat
    set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.config.search_engine.type=vanilla

Restart |Fess| after the change. The crawler and the other job processes receive the setting from |Fess|, so you do not have to set it for them separately.

Connection Settings
===================

The connection to OpenSearch is configured in the same way as for any other type.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Setting
     - Description
   * - ``search_engine.http.url``
     - The HTTP endpoint of OpenSearch. If the environment variable ``SEARCH_ENGINE_HTTP_URL`` is set, it takes precedence.
   * - ``search_engine.username`` / ``search_engine.password``
     - The user name and password for HTTP Basic authentication. They are used only when both are set. In Docker, use the environment variables ``SEARCH_ENGINE_USERNAME`` and ``SEARCH_ENGINE_PASSWORD``.
   * - ``search_engine.http.ssl.certificate_authorities``
     - The path of a CA certificate file (X.509) used to verify the server certificate of an HTTPS endpoint. It is not needed when the certificate is issued by a CA that Java already trusts.

A ``fess_config.properties`` item can also be given as ``-Dfess.config.<item name>`` in ``FESS_JAVA_OPTS`` (see :doc:`../install/install-docker`).

.. _search-engine-type-aws:

Amazon OpenSearch Service
=========================

To use an Amazon OpenSearch Service domain, set ``search_engine.type`` to ``aws`` (``vanilla`` behaves in the same way).

Requirements
------------

* The domain runs OpenSearch 3.x. |Fess| checks the engine at startup and does not start with anything other than OpenSearch 3.
* The plugins listed in "Required OpenSearch Plugins" are available on the domain. On Amazon OpenSearch Service, Nori is an optional package: associate it with the domain before you start |Fess|.
* The endpoint uses HTTPS.
* Fine-grained access control is enabled and has an internal user for |Fess| to sign in as (HTTP Basic authentication). Signing requests with AWS IAM credentials (SigV4) is not supported yet, so a domain that accepts only IAM-signed requests cannot be used.

Example Configuration
---------------------

::

    search_engine.type=aws
    search_engine.http.url=https://<domain-endpoint>:443
    search_engine.username=<internal-user-name>
    search_engine.password=<password>

Checks at Startup
-----------------

* The plugin check described in "Required OpenSearch Plugins" also runs for ``aws``. If you forgot to associate Nori, a warning appears in ``fess.log``.
* If the domain rejects a request with HTTP 401 or 403, |Fess| logs a warning. When this makes the startup fail, the error message points to the user name, the password and the access policy of the domain.

DNS Cache TTL
-------------

The endpoint of a managed service can resolve to different IP addresses over time, and the JVM caches the result of a DNS lookup. A short cache time lets |Fess| follow such a change. Set ``-Dsun.net.inetaddr.ttl=5`` (seconds) in the following two places.

1. The |Fess| process: append it to ``FESS_JAVA_OPTS``.

   ::

       FESS_JAVA_OPTS="$FESS_JAVA_OPTS -Dsun.net.inetaddr.ttl=5"

2. The job processes: the crawler, suggest, chunk and thumbnail processes are started by |Fess| as separate JVMs and do not inherit ``FESS_JAVA_OPTS``. Add the same option to the end of ``jvm.crawler.options``, ``jvm.suggest.options``, ``jvm.chunk.options`` and ``jvm.thumbnail.options`` in ``fess_config.properties``. Each of these values has one option per line, and every line ends with ``\n\``.

   ::

       jvm.crawler.options=\
       -Djava.awt.headless=true\n\
       ...
       -Dsun.net.inetaddr.ttl=5\n\

   Append the line after the existing ones, and do the same for the other three items.

In Docker, specify ``FESS_JAVA_OPTS`` in the environment variables of the Compose file. To change the ``jvm.*.options`` items, mount a modified ``fess_config.properties`` (see :doc:`../install/install-docker`).
