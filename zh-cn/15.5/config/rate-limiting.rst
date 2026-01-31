==================================
速率限制配置
==================================

概述
====

|Fess| 具有速率限制功能，用于维护系统的稳定性和性能。
通过此功能，可以保护系统免受过度请求的影响，实现公平的资源分配。

速率限制适用于以下场景:

- 搜索API
- AI模式API
- 爬虫请求

搜索API的速率限制
===================

可以限制对搜索API的请求数。

设置
----

``app/WEB-INF/conf/system.properties``:

::

    # 启用速率限制
    api.rate.limit.enabled=true

    # 每个IP地址每分钟的最大请求数
    api.rate.limit.requests.per.minute=60

    # 速率限制窗口大小（秒）
    api.rate.limit.window.seconds=60

行为
----

- 超过速率限制的请求返回HTTP 429 (Too Many Requests)
- 限制按IP地址单位应用
- 限制值使用滑动窗口方式计数

AI模式的速率限制
=======================

AI模式功能具有速率限制，用于控制LLM API的成本和资源消耗。

设置
----

``app/WEB-INF/conf/system.properties``:

::

    # 启用聊天的速率限制
    rag.chat.rate.limit.enabled=true

    # 每分钟最大请求数
    rag.chat.rate.limit.requests.per.minute=10

.. note::
   AI模式的速率限制与LLM提供商端的速率限制分别应用。
   请同时考虑两者的限制进行设置。

爬虫的速率限制
======================

可以设置请求间隔，以避免爬虫对目标站点造成过度负载。

Web爬取设置
---------------

在管理界面的「爬虫」→「Web」中设置以下内容:

- **请求间隔**: 请求间的等待时间（毫秒）
- **线程数**: 并行爬取线程数

推荐设置:

::

    # 一般站点
    intervalTime=1000
    numOfThread=1

    # 大型站点（有授权时）
    intervalTime=500
    numOfThread=3

遵守robots.txt
----------------

|Fess| 默认遵守robots.txt的Crawl-delay指令。

::

    # robots.txt示例
    User-agent: *
    Crawl-delay: 10

高级速率限制设置
====================

自定义速率限制
------------------

要对特定用户或角色应用不同限制，
需要实现自定义组件。

::

    // RateLimitHelper自定义示例
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // 自定义逻辑
        }
    }

突发限制
------------

允许短时间突发请求，同时防止持续高负载的设置:

::

    # 突发容量
    api.rate.limit.burst.size=20

    # 持续限制
    api.rate.limit.sustained.requests.per.second=1

排除设置
========

可以将特定IP地址或用户从速率限制中排除。

::

    # 排除IP地址（逗号分隔）
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # 排除角色
    api.rate.limit.excluded.roles=admin

监控与告警
==============

用于监控速率限制状况的设置:

日志输出
--------

应用速率限制时，会记录在日志中:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

指标
----------

速率限制相关的指标可以通过系统统计API获取:

::

    GET /api/admin/stats

故障排除
======================

正常请求被阻止
--------------------------------

**原因**: 限制值过于严格

**解决方法**:

1. 增加 ``requests.per.minute``
2. 将特定IP添加到排除列表
3. 调整窗口大小

速率限制不生效
--------------------

**原因**: 设置未正确生效

**确认事项**:

1. 是否设置了 ``api.rate.limit.enabled=true``
2. 配置文件是否正确加载
3. 是否重启了 |Fess|

性能影响
----------------------

速率限制检查本身影响性能时:

1. 将速率限制存储更改为Redis等
2. 调整检查频率

参考信息
========

- :doc:`rag-chat` - AI模式功能配置
- :doc:`../admin/webconfig-guide` - Web爬取配置指南
- :doc:`../api/api-overview` - API概述
