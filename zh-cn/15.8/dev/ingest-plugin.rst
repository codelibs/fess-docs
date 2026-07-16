==================================
Ingest插件
==================================

概述
====

Ingest插件提供在文档注册到索引之前对数据进行加工和转换的功能。
通过抓取获取的各个文档，在发送到索引之前都会经过已注册的 Ingester。

用途
====

- 文本规范化（全角/半角转换、空白整理等）
- 添加元数据或自定义字段
- 敏感信息脱敏
- 值转换（例如：解码已编码的向量嵌入）

Ingester 类
===============

Ingest 功能通过继承 ``org.codelibs.fess.ingest.Ingester`` 抽象类来实现。
``Ingester`` 提供了根据抓取类型和处理阶段调用的 ``process`` 方法。由于
默认实现均直接返回接收到的 ``target``（不做任何处理），因此只需重写
所需的方法即可。

- ``protected Map<String, Object> process(Map<String, Object> target)``

  这是两个 ``Map`` 版本方法共同的委托目标。重写此方法后，将同时适用于
  数据存储抓取以及 Web/文件抓取（索引注册时）的文档。在多数场景下，
  只需重写此方法即可满足需求。

- ``public Map<String, Object> process(Map<String, Object> target, DataStoreParams params)``

  在数据存储抓取时被调用。默认情况下会委托给 ``process(target)``。

- ``public Map<String, Object> process(Map<String, Object> target, AccessResult<String> accessResult)``

  在 Web/文件抓取的索引注册时被调用。默认情况下会委托给 ``process(target)``。

- ``public ResultData process(ResultData target, ResponseData responseData)``

  在 Web/文件抓取的响应处理时（保存访问结果之前）被调用。默认情况下
  会直接返回 ``target``。

执行顺序（priority）
--------------------

当注册了多个 Ingester 时，将按照 ``priority`` 字段的升序（值越小越先
执行）执行。默认值为 ``99``。可以在构造函数中直接设置，也可以通过
``setPriority(int)`` 进行修改。

.. code-block:: java

    public int getPriority()
    public void setPriority(final int priority)

实现示例
======

以下是重写 ``process(Map<String, Object>)`` 方法，对内容进行规范化并
添加自定义字段的示例：

.. code-block:: java

    package org.codelibs.fess.ingest.example;

    import java.util.Map;

    import org.codelibs.fess.ingest.Ingester;

    public class ExampleIngester extends Ingester {

        public ExampleIngester() {
            // 设置执行顺序（值越小越先执行。默认值为 99）
            setPriority(50);
        }

        @Override
        protected Map<String, Object> process(final Map<String, Object> target) {
            // 内容规范化
            final Object content = target.get("content");
            if (content instanceof String) {
                target.put("content", ((String) content).trim().replaceAll("\\s+", " "));
            }

            // 添加自定义字段
            target.put("ingested_by", ExampleIngester.class.getSimpleName());

            // 返回加工后的文档
            return target;
        }
    }

.. note::

    在 ``process`` 方法中返回 ``null`` 会导致索引注册失败。由于没有跳过
    文档的机制，因此请务必返回 ``target``。

注册
====

Ingester 通过 DI 容器进行注册。插件中需包含 ``fess_ingest++.xml``
文件。文件名末尾的 ``++`` 是一种合并约定，表示将配置追加到 |Fess|
本体的 ``fess_ingest.xml``（其中定义了管理 Ingester 的 ``ingestFactory``）中。

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

通过 ``<postConstruct name="register"/>``，组件生成后会调用
``Ingester#register()``，从而将自身注册到 ``ingestFactory`` 中。

关于 Ingest 功能，``fess_config.properties`` 中没有相应的配置项。
是否启用取决于插件是否安装，执行顺序则通过 ``priority`` 控制。

执行流程
==========

在加工后的文档发送到索引之前，Ingester 会在以下位置按照 ``priority``
的升序被调用：

- **数据存储抓取**：在发送文档之前，会调用
  ``process(Map, DataStoreParams)``。
- **Web/文件抓取（响应处理时）**：在保存抓取结果之前，会调用
  ``process(ResultData, ResponseData)``。
- **Web/文件抓取（索引注册时）**：在发送文档之前，会调用
  ``process(Map, AccessResult)``。

无论在哪个位置，如果某个 Ingester 抛出异常，都会输出警告日志并继续
处理（该文档的索引注册不会中断）。

.. note::

    由于 Ingester 是注册到抓取器的运行环境（``ingestFactory``）中的，
    因此它作为抓取处理的一部分运行。

参考实现
========

作为实现参考，以下插件已在 GitHub 的
`CodeLibs <https://github.com/codelibs>`__ 上公开：

- ``fess-ingest-example`` - 最小配置的示例实现
- ``fess-webapp-multimodal`` - 包含用于解码向量嵌入的 ``EmbeddingIngester`` 的插件

参考信息
========

- :doc:`plugin-architecture` - 插件架构
